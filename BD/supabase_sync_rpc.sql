-- ============================================================================
-- SGMC v2 — FUNCIÓN RPC ATÓMICA DE SINCRONIZACIÓN OUTBOX
-- Implementación de ESPEC-011 / ESPEC-020 (Corrección Atómica de Coordenadas e Idempotencia)
-- ============================================================================

-- 1. Trigger de actualización geométrica para MAN_Mantenimientos
CREATE OR REPLACE FUNCTION public.fn_actualizar_geom_man()
RETURNS TRIGGER AS $$
DECLARE
    coords TEXT[];
    lat NUMERIC;
    lng NUMERIC;
BEGIN
    IF NEW."Coordenadas_Cierre_LatLong" IS NOT NULL 
       AND NEW."Coordenadas_Cierre_LatLong" <> '' 
       AND NEW."Coordenadas_Cierre_LatLong" <> '0.000000, 0.000000' THEN
        coords := string_to_array(NEW."Coordenadas_Cierre_LatLong", ',');
        IF array_length(coords, 1) = 2 THEN
            lat := trim(coords[1])::NUMERIC;
            lng := trim(coords[2])::NUMERIC;
            NEW."geom" := ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography;
        END IF;
    ELSE
        NEW."geom" := NULL;
    END IF;
    NEW."updated_at" := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "trg_geom_MAN_Mantenimientos" ON public."MAN_Mantenimientos";
CREATE TRIGGER "trg_geom_MAN_Mantenimientos" 
BEFORE INSERT OR UPDATE ON public."MAN_Mantenimientos" 
FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom_man();

-- 2. Función RPC Atómica de Sincronización
CREATE OR REPLACE FUNCTION public.sgmc_sincronizar_mantenimiento(p_payload JSONB)
RETURNS JSONB AS $$
DECLARE
    v_otid VARCHAR(100);
    v_mantenimiento_id VARCHAR(100);
    v_checklist_id VARCHAR(100);
    v_tecnico_id VARCHAR(100);
    v_activo_id VARCHAR(100);
    v_chk_key TEXT;
    v_chk_val TEXT;
    v_foto JSONB;
    v_fecha_inicio TIMESTAMPTZ;
    v_fecha_cierre TIMESTAMPTZ;
    v_coordenadas TEXT;
    v_cierre_excepcion BOOLEAN;
    v_motivo_excepcion TEXT;
    v_observaciones TEXT;
    v_firma_path TEXT;
    v_formulario_id VARCHAR(100);
    v_pregunta_id VARCHAR(100);
    v_existing_man VARCHAR(100);
    v_user_email TEXT;
BEGIN
    -- 1. Extraer datos principales del payload
    v_otid := p_payload ->> 'OTID';
    v_activo_id := p_payload ->> 'ActivoID';
    v_coordenadas := NULLIF(TRIM(p_payload ->> 'Coordenadas_Cierre_LatLong'), '');
    v_cierre_excepcion := COALESCE((p_payload ->> 'CierreConExcepcion')::BOOLEAN, FALSE);
    v_motivo_excepcion := p_payload ->> 'MotivoExcepcion';
    v_observaciones := p_payload ->> 'Observaciones';
    v_firma_path := p_payload ->> 'FirmaBase64';
    v_fecha_inicio := COALESCE((p_payload ->> 'FechaInicio')::TIMESTAMPTZ, NOW());
    v_fecha_cierre := COALESCE((p_payload ->> 'FechaCierre')::TIMESTAMPTZ, NOW());
    v_user_email := COALESCE(lower(auth.jwt() ->> 'email'), 'sistema@concesiondelsisga.com.co');

    IF v_otid IS NULL THEN
        RETURN jsonb_build_object(
            'exito', FALSE,
            'error', 'OTID es obligatorio en el payload de sincronización'
        );
    END IF;

    -- 2. Idempotencia: Si ya existe un mantenimiento para esta OT, retornar éxito sin duplicar
    SELECT "MantenimientoID" INTO v_existing_man 
    FROM public."MAN_Mantenimientos" 
    WHERE "OTID" = v_otid 
    LIMIT 1;

    IF v_existing_man IS NOT NULL THEN
        RETURN jsonb_build_object(
            'exito', TRUE,
            'mantenimiento_id', v_existing_man,
            'otid', v_otid,
            'mensaje', 'Mantenimiento ya registrado previamente (operación idempotente)'
        );
    END IF;

    -- 3. Resolver y asegurar que la orden de trabajo exista en OT_OrdenesTrabajo
    IF NOT EXISTS (SELECT 1 FROM public."OT_OrdenesTrabajo" WHERE "OTID" = v_otid) THEN
        INSERT INTO public."OT_OrdenesTrabajo" (
            "OTID",
            "ActivoID",
            "TecnicoID",
            "SupervisorID",
            "Tipo",
            "FechaProgramada",
            "EstadoOrdenID"
        ) VALUES (
            v_otid,
            COALESCE(v_activo_id, 'ACT-0001'),
            COALESCE(v_tecnico_id, 'USR-004'),
            'USR-006',
            'Preventivo',
            NOW(),
            'En revision'
        );
    END IF;

    -- 4. Resolver TecnicoID
    v_tecnico_id := public.sgmc_usuario_id();
    IF v_tecnico_id IS NULL THEN
        SELECT "TecnicoID" INTO v_tecnico_id FROM public."OT_OrdenesTrabajo" WHERE "OTID" = v_otid;
        IF v_tecnico_id IS NULL THEN
            v_tecnico_id := 'USR-004'; -- Fallback técnico
        END IF;
    END IF;

    -- 5. Generar ID de Mantenimiento
    v_mantenimiento_id := 'MAN-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 6);

    -- 6. Insertar en MAN_Mantenimientos (Coordenadas_Cierre_LatLong exactas o NULL, CERO puntos falsos)
    INSERT INTO public."MAN_Mantenimientos" (
        "MantenimientoID",
        "OTID",
        "TecnicoID",
        "FechaHoraInicio",
        "FechaHoraFin",
        "OrigenApertura",
        "EstadoActivoID",
        "Coordenadas_Cierre_LatLong",
        "CierreConExcepcion",
        "MotivoExcepcion",
        "Observaciones"
    ) VALUES (
        v_mantenimiento_id,
        v_otid,
        v_tecnico_id,
        v_fecha_inicio,
        v_fecha_cierre,
        'Lista',
        'EST-01', -- Operativo
        v_coordenadas,
        v_cierre_excepcion,
        v_motivo_excepcion,
        v_observaciones
    );

    -- 7. Resolver FormularioID asociado al Tipo de Activo e Insertar Checklist
    SELECT t."FormularioID" INTO v_formulario_id
    FROM public."OT_OrdenesTrabajo" ot
    JOIN public."ACT_Activos" a ON ot."ActivoID" = a."ActivoID"
    JOIN public."TIP_TiposActivo" t ON a."TipoActivoID" = t."TipoActivoID"
    WHERE ot."OTID" = v_otid;

    IF v_formulario_id IS NULL THEN
        SELECT "FormularioID" INTO v_formulario_id FROM public."FRM_Formularios" LIMIT 1;
    END IF;

    v_checklist_id := 'CHK-' || SUBSTRING(v_mantenimiento_id, 5);
    
    INSERT INTO public."CHK_Checklists" (
        "ChecklistID",
        "MantenimientoID",
        "FormularioID",
        "VersionFormulario",
        "FechaInicio",
        "FechaFin",
        "Finalizado"
    ) VALUES (
        v_checklist_id,
        v_mantenimiento_id,
        COALESCE(v_formulario_id, 'FRM-01'),
        1,
        v_fecha_inicio,
        v_fecha_cierre,
        TRUE
    );

    -- 8. Insertar Detalles de Checklist Tipados
    IF p_payload ? 'ChecklistRespuestas' THEN
        FOR v_chk_key, v_chk_val IN SELECT * FROM jsonb_each_text(p_payload -> 'ChecklistRespuestas') LOOP
            SELECT "PreguntaID", "TipoRespuestaID" INTO v_pregunta_id, v_formulario_id -- reuso variable
            FROM public."FRM_Preguntas" 
            WHERE "PreguntaID" = v_chk_key;

            IF v_pregunta_id IS NOT NULL THEN
                INSERT INTO public."CHD_ChecklistDetalle" (
                    "DetalleID",
                    "ChecklistID",
                    "PreguntaID",
                    "RespuestaTexto",
                    "RespuestaNumero",
                    "RespuestaBoolean",
                    "RespuestaLista",
                    "Contestada"
                ) VALUES (
                    'CHD-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 8),
                    v_checklist_id,
                    v_pregunta_id,
                    v_chk_val,
                    CASE WHEN v_formulario_id = 'TPR-03' AND v_chk_val ~ '^[0-9]+(\.[0-9]+)?$' THEN v_chk_val::NUMERIC ELSE NULL END,
                    CASE WHEN v_formulario_id = 'TPR-01' THEN (v_chk_val IN ('Conforme', 'Sí', 'SI', 'true', 'TRUE')) ELSE NULL END,
                    CASE WHEN v_formulario_id = 'TPR-02' THEN v_chk_val ELSE NULL END,
                    TRUE
                );
            END IF;
        END LOOP;
    END IF;

    -- 9. Insertar Fotografías si vienen en el payload (sin coordenadas simuladas)
    IF p_payload ? 'Fotografias' AND jsonb_array_length(p_payload -> 'Fotografias') > 0 THEN
        FOR v_foto IN SELECT * FROM jsonb_array_elements(p_payload -> 'Fotografias') LOOP
            INSERT INTO public."FOT_Fotografias" (
                "FotoID",
                "MantenimientoID",
                "Tipo",
                "Archivo",
                "Ubicacion_LatLong",
                "FechaHora",
                "Usuario"
            ) VALUES (
                COALESCE(v_foto ->> 'id', 'FOT-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 8)),
                v_mantenimiento_id,
                COALESCE(v_foto ->> 'tipo', 'Despues'),
                COALESCE(v_foto ->> 'url', v_foto ->> 'base64', 'sin_imagen'),
                COALESCE(v_foto ->> 'ubicacion', v_foto ->> 'Ubicacion_LatLong', v_coordenadas),
                COALESCE((v_foto ->> 'timestamp')::TIMESTAMPTZ, NOW()),
                v_user_email
            );
        END LOOP;
    END IF;

    -- 10. Insertar Firma
    IF v_firma_path IS NOT NULL AND LENGTH(v_firma_path) > 0 THEN
        INSERT INTO public."FIR_Firmas" (
            "FirmaID",
            "MantenimientoID",
            "TipoFirma",
            "Imagen",
            "FechaHora"
        ) VALUES (
            'FIR-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 8),
            v_mantenimiento_id,
            'Tecnico',
            v_firma_path,
            v_fecha_cierre
        );
    END IF;

    -- 11. Actualizar estado de la OT a 'En revision'
    UPDATE public."OT_OrdenesTrabajo"
    SET "EstadoOrdenID" = 'En revision'
    WHERE "OTID" = v_otid;

    -- Retornar confirmación exitosa
    RETURN jsonb_build_object(
        'exito', TRUE,
        'mantenimiento_id', v_mantenimiento_id,
        'checklist_id', v_checklist_id,
        'otid', v_otid,
        'mensaje', 'Mantenimiento sincronizado y asentado exitosamente en Supabase'
    );

EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'exito', FALSE,
        'error', SQLERRM,
        'detalle', SQLSTATE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

-- Permiso de ejecución para usuarios autenticados y anónimos
GRANT EXECUTE ON FUNCTION public.sgmc_sincronizar_mantenimiento(JSONB) TO anon, authenticated;
