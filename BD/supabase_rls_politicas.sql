-- ============================================================================
-- SGMC v2 — POLÍTICAS ROW LEVEL SECURITY (RLS) ESTRICTAS Y BLINDADAS
-- Implementación de ESPEC-012 / Paso 6 de Fase 4 (Aislamiento por Sujeto y Zona)
-- ============================================================================

SET search_path TO public, extensions;

-- ============================================================================
-- 1. FUNCIONES AUXILIARES DE IDENTIDAD (STABLE, SECURITY DEFINER)
-- ============================================================================

-- 1.1 Obtiene el UsuarioID a partir del correo del JWT autenticado
CREATE OR REPLACE FUNCTION public.sgmc_usuario_id()
RETURNS VARCHAR(100) AS $$
DECLARE
    v_correo TEXT;
    v_usuario_id VARCHAR(100);
BEGIN
    v_correo := lower(auth.jwt() ->> 'email');
    IF v_correo IS NULL THEN
        RETURN NULL;
    END IF;

    SELECT "UsuarioID" INTO v_usuario_id
    FROM public."USR_Usuarios"
    WHERE lower("Correo") = v_correo AND "Activo" = TRUE;

    RETURN v_usuario_id;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public;

-- 1.2 Obtiene el Nombre del Rol del usuario autenticado
CREATE OR REPLACE FUNCTION public.sgmc_rol()
RETURNS VARCHAR(100) AS $$
DECLARE
    v_correo TEXT;
    v_rol VARCHAR(100);
BEGIN
    v_correo := lower(auth.jwt() ->> 'email');
    IF v_correo IS NULL THEN
        RETURN 'Anonimo';
    END IF;

    SELECT r."Nombre" INTO v_rol
    FROM public."USR_Usuarios" u
    JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
    WHERE lower(u."Correo") = v_correo AND u."Activo" = TRUE;

    RETURN COALESCE(v_rol, 'Anonimo');
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public;

-- 1.3 Obtiene la lista de Unidades Funcionales asignadas al usuario
CREATE OR REPLACE FUNCTION public.sgmc_unidades()
RETURNS TABLE("UnidadFuncionalID" VARCHAR(100)) AS $$
DECLARE
    v_usuario_id VARCHAR(100);
BEGIN
    v_usuario_id := public.sgmc_usuario_id();
    IF v_usuario_id IS NULL THEN
        RETURN;
    END IF;

    RETURN QUERY
    SELECT a."UnidadFuncionalID"
    FROM public."ASG_AsignacionZona" a
    WHERE a."UsuarioID" = v_usuario_id AND a."Activo" = TRUE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public;

-- ============================================================================
-- 2. HABILITAR RLS EN TODAS LAS 28 TABLAS
-- ============================================================================

DO $$
DECLARE
    tbl text;
    tablas text[] := ARRAY[
        'SED_Sedes', 'UNF_UnidadesFuncionales', 'ROL_Roles', 'USR_Usuarios', 'ASG_AsignacionZona',
        'EST_Activo', 'EOT_EstadosOrden', 'MOT_MotivosPendiente', 'PAR_Parametros', 'FRE_Frecuencias',
        'CAL_Calzadas', 'SEN_Sentidos', 'TPR_TiposRespuesta', 'FRM_Formularios', 'FRM_Secciones',
        'FRM_Preguntas', 'LST_ValoresLista', 'TIP_TiposActivo', 'FAL_ModosFalla', 'ACT_Activos',
        'OT_OrdenesTrabajo', 'MAN_Mantenimientos', 'NOV_Novedades', 'PLA_PlanMantenimiento',
        'CHK_Checklists', 'CHD_ChecklistDetalle', 'FOT_Fotografias', 'FIR_Firmas'
    ];
BEGIN
    FOREACH tbl IN ARRAY tablas LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', tbl);
    END LOOP;
END $$;

-- ============================================================================
-- 3. CATÁLOGOS BASE (Lectura Pública/Auth, Escritura solo Administrador)
-- ============================================================================

DO $$
DECLARE
    tbl text;
    catalogos text[] := ARRAY[
        'SED_Sedes', 'UNF_UnidadesFuncionales', 'ROL_Roles', 'EST_Activo', 'EOT_EstadosOrden',
        'MOT_MotivosPendiente', 'PAR_Parametros', 'FRE_Frecuencias', 'CAL_Calzadas', 'SEN_Sentidos',
        'TPR_TiposRespuesta', 'FRM_Formularios', 'FRM_Secciones', 'FRM_Preguntas', 'LST_ValoresLista',
        'TIP_TiposActivo', 'FAL_ModosFalla'
    ];
BEGIN
    FOREACH tbl IN ARRAY catalogos LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Lectura publica %s" ON public.%I;', tbl, tbl);
        EXECUTE format('CREATE POLICY "Lectura publica %s" ON public.%I FOR SELECT USING (auth.role() IN (''anon'', ''authenticated''));', tbl, tbl);
        
        EXECUTE format('DROP POLICY IF EXISTS "Admin write %s" ON public.%I;', tbl, tbl);
        EXECUTE format('CREATE POLICY "Admin write %s" ON public.%I FOR ALL TO authenticated USING (public.sgmc_rol() = ''Administrador'') WITH CHECK (public.sgmc_rol() = ''Administrador'');', tbl, tbl);
    END LOOP;
END $$;

-- ============================================================================
-- 4. ACT_Activos (Aislamiento por Unidad Funcional para Técnicos y Supervisores)
-- ============================================================================

DROP POLICY IF EXISTS "Lectura publica ACT_Activos" ON public."ACT_Activos";
DROP POLICY IF EXISTS "Admin write ACT_Activos" ON public."ACT_Activos";
DROP POLICY IF EXISTS "Lectura Activos por Rol y Zona" ON public."ACT_Activos";

CREATE POLICY "Lectura Activos por Rol y Zona" ON public."ACT_Activos"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    (public.sgmc_rol() IN ('Técnico', 'Supervisor') AND "UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades()))
);

CREATE POLICY "Admin write ACT_Activos" ON public."ACT_Activos"
FOR ALL TO authenticated 
USING (public.sgmc_rol() = 'Administrador')
WITH CHECK (public.sgmc_rol() = 'Administrador');

-- ============================================================================
-- 5. USR_Usuarios y ASG_AsignacionZona
-- ============================================================================

DROP POLICY IF EXISTS "Lectura usuarios" ON public."USR_Usuarios";
DROP POLICY IF EXISTS "Admin write USR_Usuarios" ON public."USR_Usuarios";

CREATE POLICY "Lectura usuarios" ON public."USR_Usuarios"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Supervisor', 'Consulta') OR
    lower("Correo") = lower(auth.jwt() ->> 'email') OR
    auth.role() = 'anon'
);

CREATE POLICY "Admin write USR_Usuarios" ON public."USR_Usuarios"
FOR ALL TO authenticated
USING (public.sgmc_rol() = 'Administrador')
WITH CHECK (public.sgmc_rol() = 'Administrador');

DROP POLICY IF EXISTS "Lectura asignaciones" ON public."ASG_AsignacionZona";
DROP POLICY IF EXISTS "Admin write ASG_AsignacionZona" ON public."ASG_AsignacionZona";

CREATE POLICY "Lectura asignaciones" ON public."ASG_AsignacionZona"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Supervisor', 'Consulta') OR
    "UsuarioID" = public.sgmc_usuario_id()
);

CREATE POLICY "Admin write ASG_AsignacionZona" ON public."ASG_AsignacionZona"
FOR ALL TO authenticated
USING (public.sgmc_rol() = 'Administrador')
WITH CHECK (public.sgmc_rol() = 'Administrador');

-- ============================================================================
-- 6. OT_OrdenesTrabajo (Aislamiento por Asignación y Zona)
-- ============================================================================

DROP POLICY IF EXISTS "Tecnico ve y edita sus OTs" ON public."OT_OrdenesTrabajo";
DROP POLICY IF EXISTS "Supervisor y Admin gestionan OTs" ON public."OT_OrdenesTrabajo";
DROP POLICY IF EXISTS "Lectura OTs por Rol y Zona" ON public."OT_OrdenesTrabajo";
DROP POLICY IF EXISTS "Gestion OTs" ON public."OT_OrdenesTrabajo";

CREATE POLICY "Lectura OTs por Rol y Zona" ON public."OT_OrdenesTrabajo"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    (public.sgmc_rol() = 'Técnico' AND "TecnicoID" = public.sgmc_usuario_id()) OR
    (public.sgmc_rol() = 'Supervisor' AND EXISTS (
        SELECT 1 FROM public."ACT_Activos" a 
        WHERE a."ActivoID" = "OT_OrdenesTrabajo"."ActivoID" 
          AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
    ))
);

CREATE POLICY "Gestion OTs" ON public."OT_OrdenesTrabajo"
FOR ALL TO authenticated USING (
    public.sgmc_rol() = 'Administrador' OR
    (public.sgmc_rol() = 'Supervisor' AND EXISTS (
        SELECT 1 FROM public."ACT_Activos" a 
        WHERE a."ActivoID" = "OT_OrdenesTrabajo"."ActivoID" 
          AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
    )) OR
    (public.sgmc_rol() = 'Técnico' AND "TecnicoID" = public.sgmc_usuario_id())
);

-- ============================================================================
-- 7. MAN_Mantenimientos (Aislamiento de Ejecuciones en Campo)
-- ============================================================================

DROP POLICY IF EXISTS "Lectura Mantenimientos" ON public."MAN_Mantenimientos";
DROP POLICY IF EXISTS "Tecnico y Supervisor insertan/editan Mantenimientos" ON public."MAN_Mantenimientos";
DROP POLICY IF EXISTS "Escritura Mantenimientos" ON public."MAN_Mantenimientos";

CREATE POLICY "Lectura Mantenimientos" ON public."MAN_Mantenimientos"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    (public.sgmc_rol() = 'Técnico' AND "TecnicoID" = public.sgmc_usuario_id()) OR
    (public.sgmc_rol() = 'Supervisor' AND EXISTS (
        SELECT 1 FROM public."OT_OrdenesTrabajo" ot
        JOIN public."ACT_Activos" a ON a."ActivoID" = ot."ActivoID"
        WHERE ot."OTID" = "MAN_Mantenimientos"."OTID" 
          AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
    ))
);

CREATE POLICY "Escritura Mantenimientos" ON public."MAN_Mantenimientos"
FOR ALL TO authenticated USING (
    public.sgmc_rol() IN ('Administrador', 'Supervisor') OR
    (public.sgmc_rol() = 'Técnico' AND "TecnicoID" = public.sgmc_usuario_id())
);

-- ============================================================================
-- 8. EVIDENCIAS: FOT_Fotografias, FIR_Firmas, CHK_Checklists, CHD_ChecklistDetalle
-- ============================================================================

-- Fotografías
DROP POLICY IF EXISTS "Lectura Fotografias" ON public."FOT_Fotografias";
DROP POLICY IF EXISTS "Insertar Fotografias" ON public."FOT_Fotografias";

CREATE POLICY "Lectura Fotografias" ON public."FOT_Fotografias"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    EXISTS (
        SELECT 1 FROM public."MAN_Mantenimientos" m 
        WHERE m."MantenimientoID" = "FOT_Fotografias"."MantenimientoID"
          AND (
              (public.sgmc_rol() = 'Técnico' AND m."TecnicoID" = public.sgmc_usuario_id()) OR
              (public.sgmc_rol() = 'Supervisor' AND EXISTS (
                  SELECT 1 FROM public."OT_OrdenesTrabajo" ot
                  JOIN public."ACT_Activos" a ON a."ActivoID" = ot."ActivoID"
                  WHERE ot."OTID" = m."OTID" 
                    AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
              ))
          )
    )
);

CREATE POLICY "Insertar Fotografias" ON public."FOT_Fotografias"
FOR INSERT TO authenticated WITH CHECK (auth.role() = 'authenticated');

-- Firmas
DROP POLICY IF EXISTS "Lectura Firmas" ON public."FIR_Firmas";
DROP POLICY IF EXISTS "Insertar Firmas" ON public."FIR_Firmas";

CREATE POLICY "Lectura Firmas" ON public."FIR_Firmas"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    EXISTS (
        SELECT 1 FROM public."MAN_Mantenimientos" m 
        WHERE m."MantenimientoID" = "FIR_Firmas"."MantenimientoID"
          AND (
              (public.sgmc_rol() = 'Técnico' AND m."TecnicoID" = public.sgmc_usuario_id()) OR
              (public.sgmc_rol() = 'Supervisor' AND EXISTS (
                  SELECT 1 FROM public."OT_OrdenesTrabajo" ot
                  JOIN public."ACT_Activos" a ON a."ActivoID" = ot."ActivoID"
                  WHERE ot."OTID" = m."OTID" 
                    AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
              ))
          )
    )
);

CREATE POLICY "Insertar Firmas" ON public."FIR_Firmas"
FOR INSERT TO authenticated WITH CHECK (auth.role() = 'authenticated');

-- Checklists
DROP POLICY IF EXISTS "Lectura Checklists" ON public."CHK_Checklists";
DROP POLICY IF EXISTS "Insertar Checklists" ON public."CHK_Checklists";

CREATE POLICY "Lectura Checklists" ON public."CHK_Checklists"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    EXISTS (
        SELECT 1 FROM public."MAN_Mantenimientos" m 
        WHERE m."MantenimientoID" = "CHK_Checklists"."MantenimientoID"
          AND (
              (public.sgmc_rol() = 'Técnico' AND m."TecnicoID" = public.sgmc_usuario_id()) OR
              (public.sgmc_rol() = 'Supervisor' AND EXISTS (
                  SELECT 1 FROM public."OT_OrdenesTrabajo" ot
                  JOIN public."ACT_Activos" a ON a."ActivoID" = ot."ActivoID"
                  WHERE ot."OTID" = m."OTID" 
                    AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
              ))
          )
    )
);

CREATE POLICY "Insertar Checklists" ON public."CHK_Checklists"
FOR INSERT TO authenticated WITH CHECK (auth.role() = 'authenticated');

-- ChecklistDetalle
DROP POLICY IF EXISTS "Lectura ChecklistDetalle" ON public."CHD_ChecklistDetalle";
DROP POLICY IF EXISTS "Insertar ChecklistDetalle" ON public."CHD_ChecklistDetalle";

CREATE POLICY "Lectura ChecklistDetalle" ON public."CHD_ChecklistDetalle"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    EXISTS (
        SELECT 1 FROM public."CHK_Checklists" chk
        JOIN public."MAN_Mantenimientos" m ON m."MantenimientoID" = chk."MantenimientoID"
        WHERE chk."ChecklistID" = "CHD_ChecklistDetalle"."ChecklistID"
          AND (
              (public.sgmc_rol() = 'Técnico' AND m."TecnicoID" = public.sgmc_usuario_id()) OR
              (public.sgmc_rol() = 'Supervisor' AND EXISTS (
                  SELECT 1 FROM public."OT_OrdenesTrabajo" ot
                  JOIN public."ACT_Activos" a ON a."ActivoID" = ot."ActivoID"
                  WHERE ot."OTID" = m."OTID" 
                    AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
              ))
          )
    )
);

CREATE POLICY "Insertar ChecklistDetalle" ON public."CHD_ChecklistDetalle"
FOR INSERT TO authenticated WITH CHECK (auth.role() = 'authenticated');

-- ============================================================================
-- 9. NOV_Novedades y PLA_PlanMantenimiento
-- ============================================================================

DROP POLICY IF EXISTS "Lectura Novedades" ON public."NOV_Novedades";
DROP POLICY IF EXISTS "Insertar Novedades" ON public."NOV_Novedades";

CREATE POLICY "Lectura Novedades" ON public."NOV_Novedades"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    (public.sgmc_rol() = 'Técnico' AND "UsuarioID" = public.sgmc_usuario_id()) OR
    (public.sgmc_rol() = 'Supervisor' AND EXISTS (
        SELECT 1 FROM public."ACT_Activos" a 
        WHERE a."ActivoID" = "NOV_Novedades"."ActivoID" 
          AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
    ))
);

CREATE POLICY "Insertar Novedades" ON public."NOV_Novedades"
FOR INSERT TO authenticated WITH CHECK (auth.role() = 'authenticated');

DROP POLICY IF EXISTS "Lectura PlanMantenimiento" ON public."PLA_PlanMantenimiento";
DROP POLICY IF EXISTS "Admin PlanMantenimiento" ON public."PLA_PlanMantenimiento";

CREATE POLICY "Lectura PlanMantenimiento" ON public."PLA_PlanMantenimiento"
FOR SELECT USING (
    public.sgmc_rol() IN ('Administrador', 'Consulta') OR
    (public.sgmc_rol() = 'Técnico' AND "ResponsableID" = public.sgmc_usuario_id()) OR
    (public.sgmc_rol() = 'Supervisor' AND EXISTS (
        SELECT 1 FROM public."ACT_Activos" a 
        WHERE a."ActivoID" = "PLA_PlanMantenimiento"."ActivoID" 
          AND a."UnidadFuncionalID" IN (SELECT "UnidadFuncionalID" FROM public.sgmc_unidades())
    ))
);

CREATE POLICY "Admin PlanMantenimiento" ON public."PLA_PlanMantenimiento"
FOR ALL TO authenticated USING (public.sgmc_rol() IN ('Administrador', 'Supervisor'));
