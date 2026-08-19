-- ============================================================================
-- SGMC v2 — ESQUEMA DDL SANEADO PARA SUPABASE (POSTGRESQL 16 + POSTGIS)
-- Generado fielmente a partir de scripts/modelo_objetivo.py
-- ============================================================================

-- 1. Extensiones y Search Path
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
SET search_path TO public, extensions;

-- 2. Limpieza previa (DROP en orden inverso)
DROP TABLE IF EXISTS public."FIR_Firmas" CASCADE;
DROP TABLE IF EXISTS public."FOT_Fotografias" CASCADE;
DROP TABLE IF EXISTS public."CHD_ChecklistDetalle" CASCADE;
DROP TABLE IF EXISTS public."CHK_Checklists" CASCADE;
DROP TABLE IF EXISTS public."PLA_PlanMantenimiento" CASCADE;
DROP TABLE IF EXISTS public."NOV_Novedades" CASCADE;
DROP TABLE IF EXISTS public."MAN_Mantenimientos" CASCADE;
DROP TABLE IF EXISTS public."OT_OrdenesTrabajo" CASCADE;
DROP TABLE IF EXISTS public."ACT_Activos" CASCADE;
DROP TABLE IF EXISTS public."FAL_ModosFalla" CASCADE;
DROP TABLE IF EXISTS public."TIP_TiposActivo" CASCADE;
DROP TABLE IF EXISTS public."LST_ValoresLista" CASCADE;
DROP TABLE IF EXISTS public."FRM_Preguntas" CASCADE;
DROP TABLE IF EXISTS public."FRM_Secciones" CASCADE;
DROP TABLE IF EXISTS public."FRM_Formularios" CASCADE;
DROP TABLE IF EXISTS public."TPR_TiposRespuesta" CASCADE;
DROP TABLE IF EXISTS public."SEN_Sentidos" CASCADE;
DROP TABLE IF EXISTS public."CAL_Calzadas" CASCADE;
DROP TABLE IF EXISTS public."FRE_Frecuencias" CASCADE;
DROP TABLE IF EXISTS public."PAR_Parametros" CASCADE;
DROP TABLE IF EXISTS public."MOT_MotivosPendiente" CASCADE;
DROP TABLE IF EXISTS public."EOT_EstadosOrden" CASCADE;
DROP TABLE IF EXISTS public."EST_Activo" CASCADE;
DROP TABLE IF EXISTS public."ASG_AsignacionZona" CASCADE;
DROP TABLE IF EXISTS public."USR_Usuarios" CASCADE;
DROP TABLE IF EXISTS public."ROL_Roles" CASCADE;
DROP TABLE IF EXISTS public."SED_Sedes" CASCADE;
DROP TABLE IF EXISTS public."UNF_UnidadesFuncionales" CASCADE;

-- 3. Creación de las 28 Tablas

-- Tabla: UNF_UnidadesFuncionales
CREATE TABLE public."UNF_UnidadesFuncionales" (
    "UnidadFuncionalID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "PKInicial" VARCHAR(255) NULL,
    "PKFinal" VARCHAR(255) NULL,
    "PRInicial" VARCHAR(255) NULL,
    "PRFinal" VARCHAR(255) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: SED_Sedes
CREATE TABLE public."SED_Sedes" (
    "SedeID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Ciudad" VARCHAR(255) NULL,
    "UnidadFuncionalID" VARCHAR(100) NULL,
    "PR" VARCHAR(255) NULL,
    "TramoINVIAS" VARCHAR(255) NULL,
    "PK" VARCHAR(255) NULL,
    "Ubicacion_LatLong" VARCHAR(100) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "geom" GEOGRAPHY(Point, 4326) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: ROL_Roles
CREATE TABLE public."ROL_Roles" (
    "RolID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Descripcion" VARCHAR(255) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: USR_Usuarios
CREATE TABLE public."USR_Usuarios" (
    "UsuarioID" VARCHAR(255) PRIMARY KEY,
    "Nombres" VARCHAR(255) NOT NULL,
    "Correo" VARCHAR(255) NOT NULL,
    "Cargo" VARCHAR(255) NULL,
    "Iniciales" VARCHAR(255) NULL,
    "RolID" VARCHAR(100) NOT NULL,
    "Telefono" VARCHAR(50) NULL,
    "FechaIngreso" DATE NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: ASG_AsignacionZona
CREATE TABLE public."ASG_AsignacionZona" (
    "AsignacionID" VARCHAR(255) PRIMARY KEY,
    "UsuarioID" VARCHAR(100) NOT NULL,
    "UnidadFuncionalID" VARCHAR(100) NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: EST_Activo
CREATE TABLE public."EST_Activo" (
    "EstadoActivoID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "GeneraAlerta" BOOLEAN NULL DEFAULT FALSE,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: EOT_EstadosOrden
CREATE TABLE public."EOT_EstadosOrden" (
    "EstadoOrdenID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Orden" INTEGER NULL,
    "QuienCambia" VARCHAR(100) NULL,
    "EsFinal" BOOLEAN NULL DEFAULT FALSE,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: MOT_MotivosPendiente
CREATE TABLE public."MOT_MotivosPendiente" (
    "MotivoPendienteID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "GeneraSeguimiento" BOOLEAN NULL DEFAULT TRUE,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: PAR_Parametros
CREATE TABLE public."PAR_Parametros" (
    "ParametroID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Valor" NUMERIC(12, 4) NOT NULL,
    "Unidad" VARCHAR(255) NULL,
    "Descripcion" TEXT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FRE_Frecuencias
CREATE TABLE public."FRE_Frecuencias" (
    "FrecuenciaID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Dias" INTEGER NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: CAL_Calzadas
CREATE TABLE public."CAL_Calzadas" (
    "CalzadaID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: SEN_Sentidos
CREATE TABLE public."SEN_Sentidos" (
    "SentidoID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: TPR_TiposRespuesta
CREATE TABLE public."TPR_TiposRespuesta" (
    "TipoRespuestaID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FRM_Formularios
CREATE TABLE public."FRM_Formularios" (
    "FormularioID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Descripcion" VARCHAR(255) NULL,
    "Version" INTEGER NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FRM_Secciones
CREATE TABLE public."FRM_Secciones" (
    "SeccionID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Orden" INTEGER NOT NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FRM_Preguntas
CREATE TABLE public."FRM_Preguntas" (
    "PreguntaID" VARCHAR(255) PRIMARY KEY,
    "FormularioID" VARCHAR(100) NOT NULL,
    "SeccionID" VARCHAR(100) NOT NULL,
    "Orden" INTEGER NOT NULL,
    "Pregunta" VARCHAR(255) NOT NULL,
    "TipoRespuestaID" VARCHAR(100) NOT NULL,
    "Obligatoria" BOOLEAN NULL DEFAULT TRUE,
    "ValorMinimo" NUMERIC(12, 4) NULL,
    "ValorMaximo" NUMERIC(12, 4) NULL,
    "Unidad" VARCHAR(255) NULL,
    "Ayuda" VARCHAR(255) NULL,
    "VisibleSi" VARCHAR(255) NULL,
    "RequiereFoto" BOOLEAN NULL DEFAULT FALSE,
    "Version" INTEGER NULL,
    "RequiereGPS" BOOLEAN NULL DEFAULT FALSE,
    "RequiereFirma" BOOLEAN NULL DEFAULT FALSE,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: LST_ValoresLista
CREATE TABLE public."LST_ValoresLista" (
    "ValorListaID" VARCHAR(255) PRIMARY KEY,
    "PreguntaID" VARCHAR(100) NOT NULL,
    "Valor" VARCHAR(255) NOT NULL,
    "Orden" INTEGER NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: TIP_TiposActivo
CREATE TABLE public."TIP_TiposActivo" (
    "TipoActivoID" VARCHAR(255) PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Categoria" VARCHAR(100) NULL,
    "FormularioID" VARCHAR(100) NOT NULL,
    "TieneQR" BOOLEAN NULL DEFAULT TRUE,
    "RequiereGPS" BOOLEAN NULL DEFAULT TRUE,
    "RadioGeofencingKm" NUMERIC(12, 4) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FAL_ModosFalla
CREATE TABLE public."FAL_ModosFalla" (
    "ModoFallaID" VARCHAR(255) PRIMARY KEY,
    "TipoActivoID" VARCHAR(100) NOT NULL,
    "Nombre" VARCHAR(255) NOT NULL,
    "Componente" VARCHAR(255) NULL,
    "Criticidad" VARCHAR(100) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: ACT_Activos
CREATE TABLE public."ACT_Activos" (
    "ActivoID" VARCHAR(255) PRIMARY KEY,
    "CodigoActivo" VARCHAR(255) NOT NULL,
    "Nombre" VARCHAR(255) NOT NULL,
    "TipoActivoID" VARCHAR(100) NOT NULL,
    "UnidadFuncionalID" VARCHAR(100) NOT NULL,
    "PR" VARCHAR(255) NULL,
    "CalzadaID" VARCHAR(100) NULL,
    "SentidoID" VARCHAR(100) NULL,
    "Ubicacion_LatLong" VARCHAR(100) NOT NULL,
    "PK" VARCHAR(255) NULL,
    "TramoINVIAS" VARCHAR(255) NULL,
    "SedeID" VARCHAR(100) NULL,
    "EstadoActivoID" VARCHAR(100) NOT NULL,
    "CodigoQR" VARCHAR(255) NULL,
    "FrecuenciaID" VARCHAR(100) NULL,
    "Criticidad" VARCHAR(100) NULL,
    "FechaBaja" DATE NULL,
    "MotivoBaja" VARCHAR(100) NULL,
    "Activo" BOOLEAN NULL,
    "Observaciones" TEXT NULL,
    "geom" GEOGRAPHY(Point, 4326) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: OT_OrdenesTrabajo
CREATE TABLE public."OT_OrdenesTrabajo" (
    "OTID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "ActivoID" VARCHAR(100) NOT NULL,
    "TecnicoID" VARCHAR(100) NOT NULL,
    "SupervisorID" VARCHAR(100) NOT NULL,
    "Tipo" VARCHAR(100) NOT NULL,
    "FechaProgramada" TIMESTAMPTZ NOT NULL,
    "EstadoOrdenID" VARCHAR(100) NOT NULL,
    "OTOrigenID" VARCHAR(100) NULL,
    "Observaciones" TEXT NULL,
    "FechaCierre" TIMESTAMPTZ NULL,
    "CerradaPor" VARCHAR(100) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: MAN_Mantenimientos
CREATE TABLE public."MAN_Mantenimientos" (
    "MantenimientoID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "OTID" VARCHAR(100) NOT NULL,
    "TecnicoID" VARCHAR(100) NOT NULL,
    "FechaHoraInicio" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "FechaHoraFin" TIMESTAMPTZ NULL,
    "OrigenApertura" VARCHAR(100) NULL,
    "UbicacionEscaneo_LatLong" VARCHAR(100) NULL,
    "FechaHoraEscaneo" TIMESTAMPTZ NULL,
    "EstadoActivoID" VARCHAR(100) NOT NULL,
    "Coordenadas_Cierre_LatLong" VARCHAR(100) NULL,
    "CierreConExcepcion" BOOLEAN NULL,
    "MotivoExcepcion" TEXT NULL,
    "RequiereSegundaVisita" BOOLEAN NULL DEFAULT FALSE,
    "MotivoPendienteID" VARCHAR(100) NULL,
    "ModoFallaID" VARCHAR(100) NULL,
    "Observaciones" TEXT NULL,
    "AprobadoSupervisor" BOOLEAN NULL DEFAULT FALSE,
    "FechaAprobacion" TIMESTAMPTZ NULL,
    "ObservacionRechazo" TEXT NULL,
    "UsuarioRegistro" VARCHAR(255) NULL,
    "FechaHoraRegistro" TIMESTAMPTZ DEFAULT NOW() NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "geom" GEOGRAPHY(Point, 4326) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: NOV_Novedades
CREATE TABLE public."NOV_Novedades" (
    "NovedadID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "UsuarioID" VARCHAR(100) NOT NULL,
    "Tipo" VARCHAR(100) NOT NULL,
    "Descripcion" TEXT NOT NULL,
    "Ubicacion_LatLong" VARCHAR(100) NOT NULL,
    "Fotografia" TEXT NOT NULL,
    "ActivoID" VARCHAR(100) NULL,
    "Estado" VARCHAR(100) NULL,
    "FechaHora" TIMESTAMPTZ DEFAULT NOW() NULL,
    "geom" GEOGRAPHY(Point, 4326) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: PLA_PlanMantenimiento
CREATE TABLE public."PLA_PlanMantenimiento" (
    "PlanID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "ActivoID" VARCHAR(100) NOT NULL,
    "FrecuenciaID" VARCHAR(100) NOT NULL,
    "UltimaEjecucion" DATE NULL,
    "ProximaFecha" DATE NOT NULL,
    "ResponsableID" VARCHAR(100) NULL,
    "Activo" BOOLEAN NULL DEFAULT TRUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: CHK_Checklists
CREATE TABLE public."CHK_Checklists" (
    "ChecklistID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "MantenimientoID" VARCHAR(100) NOT NULL,
    "FormularioID" VARCHAR(100) NOT NULL,
    "VersionFormulario" INTEGER NOT NULL,
    "FechaInicio" TIMESTAMPTZ NULL DEFAULT NOW(),
    "FechaFin" TIMESTAMPTZ NULL,
    "Finalizado" BOOLEAN NULL DEFAULT FALSE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: CHD_ChecklistDetalle
CREATE TABLE public."CHD_ChecklistDetalle" (
    "DetalleID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "ChecklistID" VARCHAR(100) NOT NULL,
    "PreguntaID" VARCHAR(100) NOT NULL,
    "RespuestaTexto" TEXT NULL,
    "RespuestaNumero" NUMERIC(12, 4) NULL,
    "RespuestaBoolean" BOOLEAN NULL,
    "RespuestaLista" VARCHAR(100) NULL,
    "Contestada" BOOLEAN NULL DEFAULT FALSE,
    "Observacion" TEXT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FOT_Fotografias
CREATE TABLE public."FOT_Fotografias" (
    "FotoID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "MantenimientoID" VARCHAR(100) NOT NULL,
    "Tipo" VARCHAR(100) NOT NULL,
    "Archivo" TEXT NOT NULL,
    "Ubicacion_LatLong" VARCHAR(100) NULL,
    "FechaHora" TIMESTAMPTZ DEFAULT NOW() NULL,
    "Usuario" VARCHAR(255) NULL,
    "geom" GEOGRAPHY(Point, 4326) NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla: FIR_Firmas
CREATE TABLE public."FIR_Firmas" (
    "FirmaID" VARCHAR(255) PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
    "MantenimientoID" VARCHAR(100) NOT NULL,
    "TipoFirma" VARCHAR(100) NOT NULL,
    "Imagen" TEXT NOT NULL,
    "FechaHora" TIMESTAMPTZ DEFAULT NOW() NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Llaves Foráneas (39 Foreign Keys con ON DELETE RESTRICT)
DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_SED_Sedes_UnidadFuncionalID') THEN 
    ALTER TABLE public."SED_Sedes" ADD CONSTRAINT "fk_SED_Sedes_UnidadFuncionalID" FOREIGN KEY ("UnidadFuncionalID") REFERENCES public."UNF_UnidadesFuncionales" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_USR_Usuarios_RolID') THEN 
    ALTER TABLE public."USR_Usuarios" ADD CONSTRAINT "fk_USR_Usuarios_RolID" FOREIGN KEY ("RolID") REFERENCES public."ROL_Roles" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ASG_AsignacionZona_UsuarioID') THEN 
    ALTER TABLE public."ASG_AsignacionZona" ADD CONSTRAINT "fk_ASG_AsignacionZona_UsuarioID" FOREIGN KEY ("UsuarioID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ASG_AsignacionZona_UnidadFuncionalID') THEN 
    ALTER TABLE public."ASG_AsignacionZona" ADD CONSTRAINT "fk_ASG_AsignacionZona_UnidadFuncionalID" FOREIGN KEY ("UnidadFuncionalID") REFERENCES public."UNF_UnidadesFuncionales" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FRM_Preguntas_FormularioID') THEN 
    ALTER TABLE public."FRM_Preguntas" ADD CONSTRAINT "fk_FRM_Preguntas_FormularioID" FOREIGN KEY ("FormularioID") REFERENCES public."FRM_Formularios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FRM_Preguntas_SeccionID') THEN 
    ALTER TABLE public."FRM_Preguntas" ADD CONSTRAINT "fk_FRM_Preguntas_SeccionID" FOREIGN KEY ("SeccionID") REFERENCES public."FRM_Secciones" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FRM_Preguntas_TipoRespuestaID') THEN 
    ALTER TABLE public."FRM_Preguntas" ADD CONSTRAINT "fk_FRM_Preguntas_TipoRespuestaID" FOREIGN KEY ("TipoRespuestaID") REFERENCES public."TPR_TiposRespuesta" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_LST_ValoresLista_PreguntaID') THEN 
    ALTER TABLE public."LST_ValoresLista" ADD CONSTRAINT "fk_LST_ValoresLista_PreguntaID" FOREIGN KEY ("PreguntaID") REFERENCES public."FRM_Preguntas" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_TIP_TiposActivo_FormularioID') THEN 
    ALTER TABLE public."TIP_TiposActivo" ADD CONSTRAINT "fk_TIP_TiposActivo_FormularioID" FOREIGN KEY ("FormularioID") REFERENCES public."FRM_Formularios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FAL_ModosFalla_TipoActivoID') THEN 
    ALTER TABLE public."FAL_ModosFalla" ADD CONSTRAINT "fk_FAL_ModosFalla_TipoActivoID" FOREIGN KEY ("TipoActivoID") REFERENCES public."TIP_TiposActivo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_TipoActivoID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_TipoActivoID" FOREIGN KEY ("TipoActivoID") REFERENCES public."TIP_TiposActivo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_UnidadFuncionalID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_UnidadFuncionalID" FOREIGN KEY ("UnidadFuncionalID") REFERENCES public."UNF_UnidadesFuncionales" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_CalzadaID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_CalzadaID" FOREIGN KEY ("CalzadaID") REFERENCES public."CAL_Calzadas" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_SentidoID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_SentidoID" FOREIGN KEY ("SentidoID") REFERENCES public."SEN_Sentidos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_SedeID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_SedeID" FOREIGN KEY ("SedeID") REFERENCES public."SED_Sedes" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_EstadoActivoID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_EstadoActivoID" FOREIGN KEY ("EstadoActivoID") REFERENCES public."EST_Activo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_ACT_Activos_FrecuenciaID') THEN 
    ALTER TABLE public."ACT_Activos" ADD CONSTRAINT "fk_ACT_Activos_FrecuenciaID" FOREIGN KEY ("FrecuenciaID") REFERENCES public."FRE_Frecuencias" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_ActivoID') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_ActivoID" FOREIGN KEY ("ActivoID") REFERENCES public."ACT_Activos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_TecnicoID') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_TecnicoID" FOREIGN KEY ("TecnicoID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_SupervisorID') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_SupervisorID" FOREIGN KEY ("SupervisorID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_EstadoOrdenID') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_EstadoOrdenID" FOREIGN KEY ("EstadoOrdenID") REFERENCES public."EOT_EstadosOrden" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_OTOrigenID') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_OTOrigenID" FOREIGN KEY ("OTOrigenID") REFERENCES public."OT_OrdenesTrabajo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_OT_OrdenesTrabajo_CerradaPor') THEN 
    ALTER TABLE public."OT_OrdenesTrabajo" ADD CONSTRAINT "fk_OT_OrdenesTrabajo_CerradaPor" FOREIGN KEY ("CerradaPor") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_MAN_Mantenimientos_OTID') THEN 
    ALTER TABLE public."MAN_Mantenimientos" ADD CONSTRAINT "fk_MAN_Mantenimientos_OTID" FOREIGN KEY ("OTID") REFERENCES public."OT_OrdenesTrabajo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_MAN_Mantenimientos_TecnicoID') THEN 
    ALTER TABLE public."MAN_Mantenimientos" ADD CONSTRAINT "fk_MAN_Mantenimientos_TecnicoID" FOREIGN KEY ("TecnicoID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_MAN_Mantenimientos_EstadoActivoID') THEN 
    ALTER TABLE public."MAN_Mantenimientos" ADD CONSTRAINT "fk_MAN_Mantenimientos_EstadoActivoID" FOREIGN KEY ("EstadoActivoID") REFERENCES public."EST_Activo" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_MAN_Mantenimientos_MotivoPendienteID') THEN 
    ALTER TABLE public."MAN_Mantenimientos" ADD CONSTRAINT "fk_MAN_Mantenimientos_MotivoPendienteID" FOREIGN KEY ("MotivoPendienteID") REFERENCES public."MOT_MotivosPendiente" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_MAN_Mantenimientos_ModoFallaID') THEN 
    ALTER TABLE public."MAN_Mantenimientos" ADD CONSTRAINT "fk_MAN_Mantenimientos_ModoFallaID" FOREIGN KEY ("ModoFallaID") REFERENCES public."FAL_ModosFalla" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_NOV_Novedades_UsuarioID') THEN 
    ALTER TABLE public."NOV_Novedades" ADD CONSTRAINT "fk_NOV_Novedades_UsuarioID" FOREIGN KEY ("UsuarioID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_NOV_Novedades_ActivoID') THEN 
    ALTER TABLE public."NOV_Novedades" ADD CONSTRAINT "fk_NOV_Novedades_ActivoID" FOREIGN KEY ("ActivoID") REFERENCES public."ACT_Activos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_PLA_PlanMantenimiento_ActivoID') THEN 
    ALTER TABLE public."PLA_PlanMantenimiento" ADD CONSTRAINT "fk_PLA_PlanMantenimiento_ActivoID" FOREIGN KEY ("ActivoID") REFERENCES public."ACT_Activos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_PLA_PlanMantenimiento_FrecuenciaID') THEN 
    ALTER TABLE public."PLA_PlanMantenimiento" ADD CONSTRAINT "fk_PLA_PlanMantenimiento_FrecuenciaID" FOREIGN KEY ("FrecuenciaID") REFERENCES public."FRE_Frecuencias" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_PLA_PlanMantenimiento_ResponsableID') THEN 
    ALTER TABLE public."PLA_PlanMantenimiento" ADD CONSTRAINT "fk_PLA_PlanMantenimiento_ResponsableID" FOREIGN KEY ("ResponsableID") REFERENCES public."USR_Usuarios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_CHK_Checklists_MantenimientoID') THEN 
    ALTER TABLE public."CHK_Checklists" ADD CONSTRAINT "fk_CHK_Checklists_MantenimientoID" FOREIGN KEY ("MantenimientoID") REFERENCES public."MAN_Mantenimientos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_CHK_Checklists_FormularioID') THEN 
    ALTER TABLE public."CHK_Checklists" ADD CONSTRAINT "fk_CHK_Checklists_FormularioID" FOREIGN KEY ("FormularioID") REFERENCES public."FRM_Formularios" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_CHD_ChecklistDetalle_ChecklistID') THEN 
    ALTER TABLE public."CHD_ChecklistDetalle" ADD CONSTRAINT "fk_CHD_ChecklistDetalle_ChecklistID" FOREIGN KEY ("ChecklistID") REFERENCES public."CHK_Checklists" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_CHD_ChecklistDetalle_PreguntaID') THEN 
    ALTER TABLE public."CHD_ChecklistDetalle" ADD CONSTRAINT "fk_CHD_ChecklistDetalle_PreguntaID" FOREIGN KEY ("PreguntaID") REFERENCES public."FRM_Preguntas" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FOT_Fotografias_MantenimientoID') THEN 
    ALTER TABLE public."FOT_Fotografias" ADD CONSTRAINT "fk_FOT_Fotografias_MantenimientoID" FOREIGN KEY ("MantenimientoID") REFERENCES public."MAN_Mantenimientos" ON DELETE RESTRICT; 
  END IF; 
END $$;

DO $$ BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_FIR_Firmas_MantenimientoID') THEN 
    ALTER TABLE public."FIR_Firmas" ADD CONSTRAINT "fk_FIR_Firmas_MantenimientoID" FOREIGN KEY ("MantenimientoID") REFERENCES public."MAN_Mantenimientos" ON DELETE RESTRICT; 
  END IF; 
END $$;

-- 5. Índices
CREATE INDEX IF NOT EXISTS "idx_SED_Sedes_UnidadFuncionalID" ON public."SED_Sedes" ("UnidadFuncionalID");
CREATE INDEX IF NOT EXISTS "idx_SED_Sedes_geom" ON public."SED_Sedes" USING GIST ("geom");
CREATE INDEX IF NOT EXISTS "idx_USR_Usuarios_RolID" ON public."USR_Usuarios" ("RolID");
CREATE INDEX IF NOT EXISTS "idx_ASG_AsignacionZona_UsuarioID" ON public."ASG_AsignacionZona" ("UsuarioID");
CREATE INDEX IF NOT EXISTS "idx_ASG_AsignacionZona_UnidadFuncionalID" ON public."ASG_AsignacionZona" ("UnidadFuncionalID");
CREATE INDEX IF NOT EXISTS "idx_FRM_Preguntas_FormularioID" ON public."FRM_Preguntas" ("FormularioID");
CREATE INDEX IF NOT EXISTS "idx_FRM_Preguntas_SeccionID" ON public."FRM_Preguntas" ("SeccionID");
CREATE INDEX IF NOT EXISTS "idx_FRM_Preguntas_TipoRespuestaID" ON public."FRM_Preguntas" ("TipoRespuestaID");
CREATE INDEX IF NOT EXISTS "idx_LST_ValoresLista_PreguntaID" ON public."LST_ValoresLista" ("PreguntaID");
CREATE INDEX IF NOT EXISTS "idx_TIP_TiposActivo_FormularioID" ON public."TIP_TiposActivo" ("FormularioID");
CREATE INDEX IF NOT EXISTS "idx_FAL_ModosFalla_TipoActivoID" ON public."FAL_ModosFalla" ("TipoActivoID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_TipoActivoID" ON public."ACT_Activos" ("TipoActivoID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_UnidadFuncionalID" ON public."ACT_Activos" ("UnidadFuncionalID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_CalzadaID" ON public."ACT_Activos" ("CalzadaID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_SentidoID" ON public."ACT_Activos" ("SentidoID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_SedeID" ON public."ACT_Activos" ("SedeID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_EstadoActivoID" ON public."ACT_Activos" ("EstadoActivoID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_FrecuenciaID" ON public."ACT_Activos" ("FrecuenciaID");
CREATE INDEX IF NOT EXISTS "idx_ACT_Activos_geom" ON public."ACT_Activos" USING GIST ("geom");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_ActivoID" ON public."OT_OrdenesTrabajo" ("ActivoID");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_TecnicoID" ON public."OT_OrdenesTrabajo" ("TecnicoID");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_SupervisorID" ON public."OT_OrdenesTrabajo" ("SupervisorID");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_EstadoOrdenID" ON public."OT_OrdenesTrabajo" ("EstadoOrdenID");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_OTOrigenID" ON public."OT_OrdenesTrabajo" ("OTOrigenID");
CREATE INDEX IF NOT EXISTS "idx_OT_OrdenesTrabajo_CerradaPor" ON public."OT_OrdenesTrabajo" ("CerradaPor");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_OTID" ON public."MAN_Mantenimientos" ("OTID");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_TecnicoID" ON public."MAN_Mantenimientos" ("TecnicoID");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_EstadoActivoID" ON public."MAN_Mantenimientos" ("EstadoActivoID");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_MotivoPendienteID" ON public."MAN_Mantenimientos" ("MotivoPendienteID");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_ModoFallaID" ON public."MAN_Mantenimientos" ("ModoFallaID");
CREATE INDEX IF NOT EXISTS "idx_MAN_Mantenimientos_geom" ON public."MAN_Mantenimientos" USING GIST ("geom");
CREATE INDEX IF NOT EXISTS "idx_NOV_Novedades_UsuarioID" ON public."NOV_Novedades" ("UsuarioID");
CREATE INDEX IF NOT EXISTS "idx_NOV_Novedades_ActivoID" ON public."NOV_Novedades" ("ActivoID");
CREATE INDEX IF NOT EXISTS "idx_NOV_Novedades_geom" ON public."NOV_Novedades" USING GIST ("geom");
CREATE INDEX IF NOT EXISTS "idx_PLA_PlanMantenimiento_ActivoID" ON public."PLA_PlanMantenimiento" ("ActivoID");
CREATE INDEX IF NOT EXISTS "idx_PLA_PlanMantenimiento_FrecuenciaID" ON public."PLA_PlanMantenimiento" ("FrecuenciaID");
CREATE INDEX IF NOT EXISTS "idx_PLA_PlanMantenimiento_ResponsableID" ON public."PLA_PlanMantenimiento" ("ResponsableID");
CREATE INDEX IF NOT EXISTS "idx_CHK_Checklists_MantenimientoID" ON public."CHK_Checklists" ("MantenimientoID");
CREATE INDEX IF NOT EXISTS "idx_CHK_Checklists_FormularioID" ON public."CHK_Checklists" ("FormularioID");
CREATE INDEX IF NOT EXISTS "idx_CHD_ChecklistDetalle_ChecklistID" ON public."CHD_ChecklistDetalle" ("ChecklistID");
CREATE INDEX IF NOT EXISTS "idx_CHD_ChecklistDetalle_PreguntaID" ON public."CHD_ChecklistDetalle" ("PreguntaID");
CREATE INDEX IF NOT EXISTS "idx_FOT_Fotografias_MantenimientoID" ON public."FOT_Fotografias" ("MantenimientoID");
CREATE INDEX IF NOT EXISTS "idx_FOT_Fotografias_geom" ON public."FOT_Fotografias" USING GIST ("geom");
CREATE INDEX IF NOT EXISTS "idx_FIR_Firmas_MantenimientoID" ON public."FIR_Firmas" ("MantenimientoID");

-- 6. Trigger para actualizar columna geom desde Ubicacion_LatLong
CREATE OR REPLACE FUNCTION public.fn_actualizar_geom()
RETURNS TRIGGER AS $$
DECLARE
    coords TEXT[];
    lat NUMERIC;
    lng NUMERIC;
BEGIN
    IF NEW."Ubicacion_LatLong" IS NOT NULL AND NEW."Ubicacion_LatLong" <> '' AND NEW."Ubicacion_LatLong" <> '0.000000, 0.000000' THEN
        coords := string_to_array(NEW."Ubicacion_LatLong", ',');
        IF array_length(coords, 1) = 2 THEN
            lat := trim(coords[1])::NUMERIC;
            lng := trim(coords[2])::NUMERIC;
            NEW."geom" := ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography;
        END IF;
    END IF;
    NEW."updated_at" := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "trg_geom_SED_Sedes" ON public."SED_Sedes";
CREATE TRIGGER "trg_geom_SED_Sedes" BEFORE INSERT OR UPDATE ON public."SED_Sedes" FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom();
DROP TRIGGER IF EXISTS "trg_geom_ACT_Activos" ON public."ACT_Activos";
CREATE TRIGGER "trg_geom_ACT_Activos" BEFORE INSERT OR UPDATE ON public."ACT_Activos" FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom();
DROP TRIGGER IF EXISTS "trg_geom_NOV_Novedades" ON public."NOV_Novedades";
CREATE TRIGGER "trg_geom_NOV_Novedades" BEFORE INSERT OR UPDATE ON public."NOV_Novedades" FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom();
DROP TRIGGER IF EXISTS "trg_geom_FOT_Fotografias" ON public."FOT_Fotografias";
CREATE TRIGGER "trg_geom_FOT_Fotografias" BEFORE INSERT OR UPDATE ON public."FOT_Fotografias" FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom();

CREATE OR REPLACE FUNCTION public.fn_actualizar_geom_man()
RETURNS TRIGGER AS $$
DECLARE
    coords TEXT[];
    lat NUMERIC;
    lng NUMERIC;
BEGIN
    IF NEW."Coordenadas_Cierre_LatLong" IS NOT NULL AND NEW."Coordenadas_Cierre_LatLong" <> '' AND NEW."Coordenadas_Cierre_LatLong" <> '0.000000, 0.000000' THEN
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
CREATE TRIGGER "trg_geom_MAN_Mantenimientos" BEFORE INSERT OR UPDATE ON public."MAN_Mantenimientos" FOR EACH ROW EXECUTE FUNCTION public.fn_actualizar_geom_man();

-- 7. Función de Validación de Geofencing en PostGIS (Falla en cerrado)
CREATE OR REPLACE FUNCTION public.validar_geofencing_cierre(
    p_lat_cierre NUMERIC,
    p_lng_cierre NUMERIC,
    p_activo_id VARCHAR(100)
) RETURNS JSONB AS $$
DECLARE
    v_activo_geom GEOGRAPHY;
    v_radio_km NUMERIC;
    v_distancia_metros NUMERIC;
    v_permitido BOOLEAN;
BEGIN
    SELECT "geom", COALESCE("RadioGeofencingKm", 0.05)
    INTO v_activo_geom, v_radio_km
    FROM public."ACT_Activos" a
    LEFT JOIN public."TIP_TiposActivo" t ON a."TipoActivoID" = t."TipoActivoID"
    WHERE a."ActivoID" = p_activo_id;

    IF v_activo_geom IS NULL THEN
        RETURN jsonb_build_object(
            'valido', FALSE,
            'distancia_metros', -1,
            'radio_permitido_metros', COALESCE(v_radio_km * 1000, 50),
            'mensaje', 'Activo no encontrado o sin coordenadas GPS registradas'
        );
    END IF;

    v_distancia_metros := ST_Distance(
        ST_SetSRID(ST_MakePoint(p_lng_cierre, p_lat_cierre), 4326)::geography,
        v_activo_geom
    );

    v_permitido := v_distancia_metros <= (v_radio_km * 1000);

    RETURN jsonb_build_object(
        'valido', v_permitido,
        'distancia_metros', round(v_distancia_metros::numeric, 2),
        'radio_permitido_metros', (v_radio_km * 1000),
        'mensaje', CASE WHEN v_permitido THEN 'Dentro del radio permitido' ELSE 'Fuera del radio de tolerancia GPS' END
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 8. Habilitar Row Level Security (RLS) en las 28 tablas
ALTER TABLE public."UNF_UnidadesFuncionales" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."SED_Sedes" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."ROL_Roles" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."USR_Usuarios" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."ASG_AsignacionZona" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."EST_Activo" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."EOT_EstadosOrden" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."MOT_MotivosPendiente" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."PAR_Parametros" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FRE_Frecuencias" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."CAL_Calzadas" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."SEN_Sentidos" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."TPR_TiposRespuesta" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FRM_Formularios" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FRM_Secciones" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FRM_Preguntas" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."LST_ValoresLista" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."TIP_TiposActivo" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FAL_ModosFalla" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."ACT_Activos" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."OT_OrdenesTrabajo" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."MAN_Mantenimientos" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."NOV_Novedades" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."PLA_PlanMantenimiento" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."CHK_Checklists" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."CHD_ChecklistDetalle" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FOT_Fotografias" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."FIR_Firmas" ENABLE ROW LEVEL SECURITY;