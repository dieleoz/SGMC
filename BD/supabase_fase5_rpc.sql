-- ============================================================================
-- SGMC v2 — PROCEDIMIENTOS ALMACENADOS Y FUNCIONES DE FASE 5
-- Implementación de ESPEC-016 (Novedades de Ruta), ESPEC-017 (Planes) y ESPEC-021 (Reportes)
-- ============================================================================

SET search_path TO public, extensions;

-- ============================================================================
-- 1. ESPEC-016: PROCEDIMIENTO PARA REPORTAR NOVEDAD Y GENERAR OT CORRECTIVA
-- ============================================================================

CREATE OR REPLACE FUNCTION public.sgmc_reportar_novedad(p_payload JSONB)
RETURNS JSONB AS $$
DECLARE
    v_novedad_id VARCHAR(100);
    v_usuario_id VARCHAR(100);
    v_tipo VARCHAR(100);
    v_descripcion TEXT;
    v_ubicacion VARCHAR(100);
    v_fotografia TEXT;
    v_activo_id VARCHAR(100);
    v_genera_ot BOOLEAN;
    v_ot_id VARCHAR(100);
    v_tecnico_id VARCHAR(100);
    v_supervisor_id VARCHAR(100);
    v_uf_id VARCHAR(100);
BEGIN
    -- 1. Extraer campos del payload
    v_novedad_id := COALESCE(p_payload ->> 'NovedadID', 'NOV-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 6));
    v_usuario_id := COALESCE(p_payload ->> 'UsuarioID', public.sgmc_usuario_id(), 'USR-004');
    v_tipo := COALESCE(p_payload ->> 'Tipo', 'Falla detectada');
    v_descripcion := COALESCE(p_payload ->> 'Descripcion', 'Novedad reportada en campo sin detalle');
    v_ubicacion := p_payload ->> 'Ubicacion_LatLong';
    v_fotografia := COALESCE(p_payload ->> 'Fotografia', 'https://placeholder.sgmc.co/novedad.webp');
    v_activo_id := p_payload ->> 'ActivoID';
    v_genera_ot := COALESCE((p_payload ->> 'GeneraOT')::BOOLEAN, TRUE);

    -- 2. Insertar en NOV_Novedades
    INSERT INTO public."NOV_Novedades" (
        "NovedadID",
        "UsuarioID",
        "Tipo",
        "Descripcion",
        "Ubicacion_LatLong",
        "Fotografia",
        "ActivoID",
        "Estado",
        "FechaHora"
    ) VALUES (
        v_novedad_id,
        v_usuario_id,
        v_tipo,
        v_descripcion,
        v_ubicacion,
        v_fotografia,
        v_activo_id,
        'Reportada',
        NOW()
    );

    -- 3. Si genera OT y hay activo asociado, crear OT Correctiva
    IF v_genera_ot AND v_activo_id IS NOT NULL THEN
        v_ot_id := 'OT-CORR-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || SUBSTRING(MD5(RANDOM()::TEXT), 1, 6);

        -- Buscar UF del activo
        SELECT "UnidadFuncionalID" INTO v_uf_id FROM public."ACT_Activos" WHERE "ActivoID" = v_activo_id;
        
        -- Buscar técnico de la zona
        SELECT a."UsuarioID" INTO v_tecnico_id
        FROM public."ASG_AsignacionZona" a
        JOIN public."USR_Usuarios" u ON a."UsuarioID" = u."UsuarioID"
        JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
        WHERE a."UnidadFuncionalID" = v_uf_id AND r."Nombre" = 'Técnico' AND a."Activo" = TRUE
        LIMIT 1;

        IF v_tecnico_id IS NULL THEN
            v_tecnico_id := v_usuario_id;
        END IF;

        -- Buscar supervisor de la zona
        SELECT a."UsuarioID" INTO v_supervisor_id
        FROM public."ASG_AsignacionZona" a
        JOIN public."USR_Usuarios" u ON a."UsuarioID" = u."UsuarioID"
        JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
        WHERE a."UnidadFuncionalID" = v_uf_id AND r."Nombre" = 'Supervisor' AND a."Activo" = TRUE
        LIMIT 1;

        IF v_supervisor_id IS NULL THEN
            v_supervisor_id := 'USR-006'; -- Fernand Bolívar (Supervisor 4 UFs)
        END IF;

        INSERT INTO public."OT_OrdenesTrabajo" (
            "OTID",
            "ActivoID",
            "TecnicoID",
            "SupervisorID",
            "Tipo",
            "FechaProgramada",
            "EstadoOrdenID",
            "Observaciones"
        ) VALUES (
            v_ot_id,
            v_activo_id,
            v_tecnico_id,
            v_supervisor_id,
            'Correctivo',
            CURRENT_DATE,
            'Asignada',
            'OT Correctiva automática por novedad de ruta ' || v_novedad_id || ': ' || v_descripcion
        );
    END IF;

    RETURN jsonb_build_object(
        'exito', TRUE,
        'novedad_id', v_novedad_id,
        'ot_id', v_ot_id,
        'mensaje', 'Novedad registrada exitosamente'
    );
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'exito', FALSE,
        'error', SQLERRM,
        'codigo', SQLSTATE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

-- ============================================================================
-- 2. ESPEC-017: GENERADOR DE PLANES PREVENTIVOS MENSUALES
-- ============================================================================

CREATE OR REPLACE FUNCTION public.sgmc_generar_plan_mensual(
    p_anio INT,
    p_mes INT,
    p_uf_id VARCHAR(100) DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    v_activo RECORD;
    v_plan_id VARCHAR(100);
    v_ot_id VARCHAR(100);
    v_tecnico_id VARCHAR(100);
    v_supervisor_id VARCHAR(100);
    v_fecha_prog DATE;
    v_ots_creadas INT := 0;
    v_planes_creados INT := 0;
BEGIN
    -- Validar mes
    IF p_mes < 1 OR p_mes > 12 THEN
        RETURN jsonb_build_object('exito', FALSE, 'error', 'Mes inválido. Debe estar entre 1 y 12');
    END IF;

    -- Fecha base programada: día 5 del mes indicado
    v_fecha_prog := MAKE_DATE(p_anio, p_mes, 5);

    -- Recorrer activos activos de la(s) UF(s) seleccionada(s)
    FOR v_activo IN 
        SELECT a."ActivoID", a."Nombre", a."UnidadFuncionalID", a."TipoActivoID"
        FROM public."ACT_Activos" a
        WHERE (p_uf_id IS NULL OR a."UnidadFuncionalID" = p_uf_id)
          AND a."EstadoActivoID" != 'EST-04' -- No retirados
        ORDER BY a."UnidadFuncionalID", a."PK"
    LOOP
        -- Buscar técnico asignado a la UF del activo
        SELECT a_zona."UsuarioID" INTO v_tecnico_id
        FROM public."ASG_AsignacionZona" a_zona
        JOIN public."USR_Usuarios" u ON a_zona."UsuarioID" = u."UsuarioID"
        JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
        WHERE a_zona."UnidadFuncionalID" = v_activo."UnidadFuncionalID" 
          AND r."Nombre" = 'Técnico' 
          AND a_zona."Activo" = TRUE
        LIMIT 1;

        IF v_tecnico_id IS NULL THEN
            v_tecnico_id := 'USR-004'; -- Fallback técnico
        END IF;

        -- Buscar supervisor de la zona
        SELECT a_zona."UsuarioID" INTO v_supervisor_id
        FROM public."ASG_AsignacionZona" a_zona
        JOIN public."USR_Usuarios" u ON a_zona."UsuarioID" = u."UsuarioID"
        JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
        WHERE a_zona."UnidadFuncionalID" = v_activo."UnidadFuncionalID" 
          AND r."Nombre" = 'Supervisor' 
          AND a_zona."Activo" = TRUE
        LIMIT 1;

        IF v_supervisor_id IS NULL THEN
            v_supervisor_id := 'USR-006'; -- Fernand Bolívar (Supervisor 4 UFs)
        END IF;

        -- 1. Crear o actualizar Plan en PLA_PlanMantenimiento
        v_plan_id := 'PLA-' || TO_CHAR(v_fecha_prog, 'YYYYMM') || '-' || v_activo."ActivoID";
        
        INSERT INTO public."PLA_PlanMantenimiento" (
            "PlanID",
            "ActivoID",
            "FrecuenciaID",
            "UltimaEjecucion",
            "ProximaFecha",
            "ResponsableID",
            "Activo"
        ) VALUES (
            v_plan_id,
            v_activo."ActivoID",
            'FRE-04', -- Mensual
            v_fecha_prog - INTERVAL '1 month',
            v_fecha_prog,
            v_tecnico_id,
            TRUE
        ) ON CONFLICT ("PlanID") DO UPDATE SET
            "ProximaFecha" = v_fecha_prog,
            "ResponsableID" = v_tecnico_id;

        v_planes_creados := v_planes_creados + 1;

        -- 2. Crear OT Preventiva si no existe ya una para ese mes y activo
        v_ot_id := 'OT-' || TO_CHAR(v_fecha_prog, 'YYYYMM') || '-' || v_activo."ActivoID";

        IF NOT EXISTS (SELECT 1 FROM public."OT_OrdenesTrabajo" WHERE "OTID" = v_ot_id) THEN
            INSERT INTO public."OT_OrdenesTrabajo" (
                "OTID",
                "ActivoID",
                "TecnicoID",
                "SupervisorID",
                "Tipo",
                "FechaProgramada",
                "EstadoOrdenID",
                "Observaciones"
            ) VALUES (
                v_ot_id,
                v_activo."ActivoID",
                v_tecnico_id,
                v_supervisor_id,
                'Preventivo',
                v_fecha_prog,
                'Programada',
                'Mantenimiento preventivo programado para ciclo ' || TO_CHAR(v_fecha_prog, 'YYYY-MM') || ' (' || v_activo."UnidadFuncionalID" || ')'
            );

            v_ots_creadas := v_ots_creadas + 1;
        END IF;
    END LOOP;

    RETURN jsonb_build_object(
        'exito', TRUE,
        'ciclo', TO_CHAR(v_fecha_prog, 'YYYY-MM'),
        'uf', COALESCE(p_uf_id, 'TODAS'),
        'planes_procesados', v_planes_creados,
        'ots_generadas', v_ots_creadas
    );
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object(
        'exito', FALSE,
        'error', SQLERRM,
        'codigo', SQLSTATE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

-- ============================================================================
-- 3. ESPEC-021: CÁLCULO DE DISPONIBILIDAD CONTRACTUAL ($D_i$)
-- ============================================================================

CREATE OR REPLACE FUNCTION public.sgmc_calcular_disponibilidad(
    p_anio INT DEFAULT EXTRACT(YEAR FROM CURRENT_DATE)::INT,
    p_mes INT DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)::INT
)
RETURNS TABLE(
    "TipoActivoID" VARCHAR(100),
    "TipoActivoNombre" VARCHAR(255),
    "UnidadFuncionalID" VARCHAR(100),
    "TotalActivos" BIGINT,
    "HorasProgramadas" NUMERIC,
    "HorasIndisponibles" NUMERIC,
    "DisponibilidadPorcentaje" NUMERIC,
    "CumpleMeta" BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    WITH ActivosFiltrados AS (
        SELECT 
            a."TipoActivoID",
            t."Nombre" AS "TipoActivoNombre",
            a."UnidadFuncionalID",
            a."ActivoID"
        FROM public."ACT_Activos" a
        JOIN public."TIP_TiposActivo" t ON a."TipoActivoID" = t."TipoActivoID"
        WHERE a."EstadoActivoID" != 'EST-04'
    ),
    Indisponibilidades AS (
        SELECT 
            nov."ActivoID",
            COUNT(*) * 4.0 AS "HorasFalla" -- Estimación de 4 horas por evento no programado
        FROM public."NOV_Novedades" nov
        WHERE EXTRACT(YEAR FROM nov."FechaHora") = p_anio
          AND EXTRACT(MONTH FROM nov."FechaHora") = p_mes
          AND nov."Tipo" = 'Falla detectada'
        GROUP BY nov."ActivoID"
    )
    SELECT 
        af."TipoActivoID",
        af."TipoActivoNombre",
        af."UnidadFuncionalID",
        COUNT(DISTINCT af."ActivoID") AS "TotalActivos",
        (COUNT(DISTINCT af."ActivoID") * 720.0) AS "HorasProgramadas", -- 30 días * 24 horas
        COALESCE(SUM(ind."HorasFalla"), 0.0) AS "HorasIndisponibles",
        ROUND(
            (100.0 * (1.0 - (COALESCE(SUM(ind."HorasFalla"), 0.0) / (COUNT(DISTINCT af."ActivoID") * 720.0))))::NUMERIC, 
            2
        ) AS "DisponibilidadPorcentaje",
        (
            ROUND((100.0 * (1.0 - (COALESCE(SUM(ind."HorasFalla"), 0.0) / (COUNT(DISTINCT af."ActivoID") * 720.0))))::NUMERIC, 2) >= 98.5
        ) AS "CumpleMeta"
    FROM ActivosFiltrados af
    LEFT JOIN Indisponibilidades ind ON af."ActivoID" = ind."ActivoID"
    GROUP BY af."TipoActivoID", af."TipoActivoNombre", af."UnidadFuncionalID"
    ORDER BY af."UnidadFuncionalID", af."TipoActivoNombre";
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public;
