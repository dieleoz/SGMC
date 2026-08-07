# -*- coding: utf-8 -*-
"""Modelo de datos OBJETIVO del SGMC.

Fuente unica de la arquitectura correcta. De aqui salen:
  - la validacion automatica (validar_modelo.py)
  - la documentacion (generar_doc_arquitectura.py)

Nada se documenta a mano: si el modelo cambia, se cambia aqui y se regenera.

Convenciones adoptadas
----------------------
1. Toda tabla tiene una clave primaria unica, de tipo texto, llamada <Prefijo>ID.
2. Toda referencia se llama igual que la clave a la que apunta. Sin excepciones:
   la mezcla de OTID/Numero_OT del modelo anterior fue causa directa de registros
   huerfanos.
3. Un dato se guarda en un solo lugar. Nada de evidencia duplicada entre campos
   embebidos y tablas hijas.
4. Las tablas hijas de una transaccion llevan IsPartOf: se crean, editan y borran
   con su padre.
5. Los catalogos llevan Activo para poder retirar un valor sin romper el historico.
"""

# ---------------------------------------------------------------- tipos validos
TIPOS = {
    "Text", "LongText", "Number", "Decimal", "Yes/No", "Date", "DateTime", "Time",
    "Enum", "EnumList", "Ref", "LatLong", "Image", "Signature", "Email", "Phone",
    "Name", "Percent", "ChangeTimestamp", "ChangeCounter",
}

GRUPOS = ["Catalogos", "Maestras", "Transaccionales", "Evidencias", "Checklist", "Formularios"]


def col(nombre, tipo, **kw):
    """Define una columna. kw admite: pk, ref, obligatoria, formula, valor_inicial,
    valid_if, mensaje_error, es_parte_de, nota, oculta."""
    d = {"nombre": nombre, "tipo": tipo}
    d.update(kw)
    return d


MODELO = {

    # ============================================================== CATALOGOS
    "SED_Sedes": dict(
        grupo="Catalogos",
        proposito="Sedes fisicas donde trabaja el personal: CCO, peajes y basculas.",
        columnas=[
            col("SedeID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Ciudad", "Text"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "UNF_UnidadesFuncionales": dict(
        grupo="Catalogos",
        proposito=("Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque "
                   "son dos conceptos distintos que el modelo anterior mezclaba en una sola "
                   "columna, dejando usuarios y activos en conjuntos disjuntos."),
        nueva=True,
        columnas=[
            col("UnidadFuncionalID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("PRInicial", "Text"),
            col("PRFinal", "Text"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "ROL_Roles": dict(
        grupo="Catalogos",
        proposito="Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta.",
        columnas=[
            col("RolID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Descripcion", "Text"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "USR_Usuarios": dict(
        grupo="Catalogos",
        proposito="Personas del sistema. El correo resuelve la sesion contra USEREMAIL().",
        columnas=[
            col("UsuarioID", "Text", pk=True),
            col("Nombres", "Text", obligatoria=True),
            col("Correo", "Email", obligatoria=True, nota="Clave de resolucion de sesion"),
            col("Cargo", "Text"),
            col("Iniciales", "Text"),
            col("RolID", "Ref", ref="ROL_Roles", obligatoria=True),
            col("SedeID", "Ref", ref="SED_Sedes", obligatoria=True),
            col("Telefono", "Phone"),
            col("FechaIngreso", "Date"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "ASG_AsignacionZona": dict(
        grupo="Catalogos",
        proposito=("Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: "
                   "un tecnico puede tener varias, de modo que la relacion es de muchos a muchos "
                   "y no cabe como columna en USR_Usuarios."),
        nueva=True,
        columnas=[
            col("AsignacionID", "Text", pk=True),
            col("UsuarioID", "Ref", ref="USR_Usuarios", obligatoria=True),
            col("UnidadFuncionalID", "Ref", ref="UNF_UnidadesFuncionales", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "TIP_TiposActivo": dict(
        grupo="Catalogos",
        proposito="Taxonomia de activos. Determina que checklist abre la aplicacion.",
        columnas=[
            col("TipoActivoID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Categoria", "Enum", nota="ITS, Electrico, Comunicaciones, TI"),
            col("FormularioID", "Ref", ref="FRM_Formularios", obligatoria=True,
                nota="Sin este mapeo no hay checklist dinamico. Estaba vacio en los 18 tipos"),
            col("TieneQR", "Yes/No", valor_inicial="TRUE"),
            col("RequiereGPS", "Yes/No", valor_inicial="TRUE"),
            col("RadioGeofencingKm", "Decimal", valor_inicial="0.2",
                nota="Supuesto D-02: radio por tipo, no unico para los 18"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "EST_Activo": dict(
        grupo="Catalogos",
        proposito="Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado.",
        columnas=[
            col("EstadoActivoID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("GeneraAlerta", "Yes/No", valor_inicial="FALSE",
                nota="Fuera de servicio dispara el bot de alerta"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "EOT_EstadosOrden": dict(
        grupo="Catalogos",
        proposito=("Ciclo de vida de la orden segun el supuesto D-06. Declararlo como catalogo, "
                   "y no como texto libre, es lo que permite medir cumplimiento."),
        nueva=True,
        columnas=[
            col("EstadoOrdenID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True,
                nota="Programada, Asignada, En ejecucion, En revision, Cerrada, Suspendida, Vencida"),
            col("Orden", "Number"),
            col("QuienCambia", "Enum", nota="Sistema, Tecnico, Supervisor"),
            col("EsFinal", "Yes/No", valor_inicial="FALSE"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "MOT_MotivosPendiente": dict(
        grupo="Catalogos",
        proposito=("Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no "
                   "tiene donde declarar por que no pudo terminar, fuerza un cierre falso."),
        nueva=True,
        columnas=[
            col("MotivoPendienteID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True,
                nota="Falta de repuesto, Clima, Acceso restringido, Riesgo, Requiere especialista"),
            col("GeneraSeguimiento", "Yes/No", valor_inicial="TRUE"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "FRE_Frecuencias": dict(
        grupo="Catalogos",
        proposito="Periodicidad del mantenimiento preventivo.",
        columnas=[
            col("FrecuenciaID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Dias", "Number", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "CAL_Calzadas": dict(
        grupo="Catalogos", proposito="Calzadas del corredor.",
        columnas=[
            col("CalzadaID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "SEN_Sentidos": dict(
        grupo="Catalogos", proposito="Sentidos de circulacion.",
        columnas=[
            col("SentidoID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    # =============================================================== MAESTRAS
    "ACT_Activos": dict(
        grupo="Maestras",
        proposito="Inventario de los activos del corredor. Es el eje del sistema.",
        columnas=[
            col("ActivoID", "Text", pk=True),
            col("CodigoActivo", "Text", obligatoria=True, nota="Codigo visible, tipo SOS-001"),
            col("Nombre", "Text", obligatoria=True),
            col("TipoActivoID", "Ref", ref="TIP_TiposActivo", obligatoria=True),
            col("UnidadFuncionalID", "Ref", ref="UNF_UnidadesFuncionales", obligatoria=True,
                nota="Antes SedeID. El cambio resuelve el filtro de seguridad"),
            col("PR", "Text", nota="Punto de referencia vial"),
            col("CalzadaID", "Ref", ref="CAL_Calzadas"),
            col("SentidoID", "Ref", ref="SEN_Sentidos"),
            col("Ubicacion", "LatLong", obligatoria=True,
                nota="Coordenada real. Hoy los 34 activos comparten un punto en Bogota"),
            col("EstadoActivoID", "Ref", ref="EST_Activo", obligatoria=True),
            col("CodigoQR", "Text", nota="Configurada como Searchable y Scan"),
            col("FrecuenciaID", "Ref", ref="FRE_Frecuencias"),
            col("Criticidad", "Enum", nota="Alta, Media, Baja. Pondera la disponibilidad de D-13"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
            col("Observaciones", "LongText"),
        ]),

    # ========================================================= TRANSACCIONALES
    "OT_OrdenesTrabajo": dict(
        grupo="Transaccionales",
        proposito="Trabajo programado o levantado sobre un activo.",
        columnas=[
            col("OTID", "Text", pk=True,
                nota="Antes Numero_OT. Se renombra para que coincida con la referencia"),
            col("ActivoID", "Ref", ref="ACT_Activos", obligatoria=True),
            col("TecnicoID", "Ref", ref="USR_Usuarios", obligatoria=True, alias_justificado="Rol en la orden: quien ejecuta"),
            col("SupervisorID", "Ref", ref="USR_Usuarios", obligatoria=True, alias_justificado="Rol en la orden: quien supervisa"),
            col("Tipo", "Enum", obligatoria=True, nota="Preventivo, Correctivo"),
            col("FechaProgramada", "DateTime", obligatoria=True),
            col("EstadoOrdenID", "Ref", ref="EOT_EstadosOrden", obligatoria=True),
            col("OTOrigenID", "Ref", ref="OT_OrdenesTrabajo", alias_justificado="Autorreferencia: la orden que origino esta",
                nota="Orden que la origino, cuando es seguimiento de una segunda visita"),
            col("Observaciones", "LongText"),
            col("FechaCierre", "DateTime"),
            col("CerradaPor", "Ref", ref="USR_Usuarios", alias_justificado="Rol en el cierre"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "MAN_Mantenimientos": dict(
        grupo="Transaccionales",
        proposito="Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia.",
        columnas=[
            col("MantenimientoID", "Text", pk=True),
            col("OTID", "Ref", ref="OT_OrdenesTrabajo", obligatoria=True, es_parte_de=True,
                nota="Era Text. Ese solo hecho impedia todo el geofencing"),
            col("TecnicoID", "Ref", ref="USR_Usuarios", obligatoria=True, alias_justificado="Rol: quien ejecuta",
                valor_inicial='LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")'),
            col("FechaHoraInicio", "DateTime", obligatoria=True, valor_inicial="NOW()"),
            col("FechaHoraFin", "DateTime"),
            col("OrigenApertura", "Enum", obligatoria=True, valor_inicial="QR",
                nota="QR o Lista. Abrir por lista no prueba presencia; se marca para poder exigir "
                     "QR donde importe y para medir cuantos cierres carecen de escaneo"),
            col("UbicacionEscaneo", "LatLong",
                nota="Donde estaba el tecnico al escanear. Junto con Coordenadas_Cierre permite "
                     "comprobar que llego y se quedo, no que paso cerca"),
            col("FechaHoraEscaneo", "DateTime",
                nota="Con FechaHoraFin da la duracion real de la intervencion"),
            col("EstadoActivoID", "Ref", ref="EST_Activo", obligatoria=True,
                nota="Estado en que queda el activo tras la intervencion"),
            col("Coordenadas_Cierre", "LatLong", obligatoria=True, valor_inicial="HERE()",
                valid_if="DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]",
                mensaje_error="Ubicacion fuera de rango: debe estar junto al activo para cerrar."),
            col("Precision_GPS", "Number", valor_inicial="USERLOCATIONACCURACY()"),
            col("CierreConExcepcion", "Yes/No", valor_inicial="FALSE",
                nota="Supuesto D-04: se activa cuando la precision supera el umbral"),
            col("MotivoExcepcion", "LongText", nota="Obligatorio si CierreConExcepcion es verdadero"),
            col("RequiereSegundaVisita", "Yes/No", valor_inicial="FALSE"),
            col("MotivoPendienteID", "Ref", ref="MOT_MotivosPendiente"),
            col("ModoFallaID", "Ref", ref="FAL_ModosFalla",
                nota="Solo en correctivos. Alimenta el tiempo medio entre fallas y el analisis "
                     "de que componente falla mas"),
            col("Observaciones", "LongText"),
            col("AprobadoSupervisor", "Yes/No", valor_inicial="FALSE"),
            col("FechaAprobacion", "DateTime"),
            col("ObservacionRechazo", "LongText", nota="Traza de la devolucion, supuesto D-07"),
            col("UsuarioRegistro", "Text", valor_inicial="USEREMAIL()"),
            col("FechaHoraRegistro", "ChangeTimestamp"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "NOV_Novedades": dict(
        grupo="Transaccionales",
        proposito=("Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de "
                   "programacion. Supuesto D-08. Sin esta via los hallazgos se pierden o acaban "
                   "en WhatsApp, que es lo que el sistema viene a reemplazar."),
        nueva=True,
        columnas=[
            col("NovedadID", "Text", pk=True),
            col("UsuarioID", "Ref", ref="USR_Usuarios", obligatoria=True,
                valor_inicial='LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")'),
            col("Tipo", "Enum", obligatoria=True, nota="Activo no inventariado, Falla detectada"),
            col("Descripcion", "LongText", obligatoria=True),
            col("Ubicacion", "LatLong", obligatoria=True, valor_inicial="HERE()"),
            col("Fotografia", "Image", obligatoria=True),
            col("ActivoID", "Ref", ref="ACT_Activos", nota="Solo si la novedad es sobre uno existente"),
            col("Estado", "Enum", valor_inicial="Reportada", nota="Reportada, Aceptada, Descartada"),
            col("FechaHora", "ChangeTimestamp"),
        ]),

    "PLA_PlanMantenimiento": dict(
        grupo="Transaccionales",
        proposito=("Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al "
                   "sistema en gestion de mantenimiento y no en un registro de formularios: de "
                   "aqui salen las ordenes, en lugar de crearlas a mano una por una."),
        nueva=True,
        columnas=[
            col("PlanID", "Text", pk=True),
            col("ActivoID", "Ref", ref="ACT_Activos", obligatoria=True),
            col("FrecuenciaID", "Ref", ref="FRE_Frecuencias", obligatoria=True),
            col("UltimaEjecucion", "Date"),
            col("ProximaFecha", "Date", obligatoria=True,
                nota="Formula: [UltimaEjecucion] + [FrecuenciaID].[Dias]"),
            col("ResponsableID", "Ref", ref="USR_Usuarios", alias_justificado="Rol: tecnico habitual"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "FAL_ModosFalla": dict(
        grupo="Catalogos",
        proposito=("Taxonomia de fallas por tipo de activo. Sin clasificar la falla no hay "
                   "ingenieria de mantenimiento posible: no se puede calcular tiempo medio entre "
                   "fallas, ni saber que componente falla mas, ni pasar de correctivo a predictivo."),
        nueva=True,
        columnas=[
            col("ModoFallaID", "Text", pk=True),
            col("TipoActivoID", "Ref", ref="TIP_TiposActivo", obligatoria=True),
            col("Nombre", "Text", obligatoria=True),
            col("Componente", "Text"),
            col("Criticidad", "Enum", nota="Alta, Media, Baja"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    # ============================================================== EVIDENCIAS
    "FOT_Fotografias": dict(
        grupo="Evidencias",
        proposito=("Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. "
                   "Se elige tabla hija y se retiran los campos de imagen embebidos en MAN."),
        columnas=[
            col("FotoID", "Text", pk=True),
            col("MantenimientoID", "Ref", ref="MAN_Mantenimientos", obligatoria=True, es_parte_de=True),
            col("Tipo", "Enum", obligatoria=True, nota="Antes, Despues, Novedad"),
            col("Archivo", "Image", obligatoria=True,
                nota="Calidad baja, 600 px. La camara debe forzarse en la app: si permite elegir "
                     "de la galeria, toda la cadena de evidencia pierde valor"),
            col("Ubicacion", "LatLong", obligatoria=True, valor_inicial="HERE()",
                nota="Coordenada de CADA fotografia. La compresion a 600 px descarta el EXIF, "
                     "asi que la geolocalizacion debe guardarse como dato, no confiarse a la imagen"),
            col("PrecisionGPS", "Number", valor_inicial="USERLOCATIONACCURACY()"),
            col("FechaHora", "ChangeTimestamp",
                nota="Marca del servidor, no del reloj del telefono, que el usuario puede alterar"),
            col("Usuario", "Text", valor_inicial="USEREMAIL()"),
        ]),

    "FIR_Firmas": dict(
        grupo="Evidencias",
        proposito=("Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor "
                   "valida aprobando en el portal, no firmando."),
        columnas=[
            col("FirmaID", "Text", pk=True),
            col("MantenimientoID", "Ref", ref="MAN_Mantenimientos", obligatoria=True, es_parte_de=True),
            col("TipoFirma", "Enum", obligatoria=True, nota="Tecnico"),
            col("Imagen", "Signature", obligatoria=True),
            col("FechaHora", "ChangeTimestamp"),
        ]),

    # =============================================================== CHECKLIST
    "CHK_Checklists": dict(
        grupo="Checklist",
        proposito=("Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la "
                   "inspeccion es parte de la ejecucion."),
        columnas=[
            col("ChecklistID", "Text", pk=True),
            col("MantenimientoID", "Ref", ref="MAN_Mantenimientos", obligatoria=True, es_parte_de=True),
            col("FormularioID", "Ref", ref="FRM_Formularios", obligatoria=True),
            col("VersionFormulario", "Number", obligatoria=True,
                nota="Supuesto D-11: congela la version con que se respondio"),
            col("FechaInicio", "DateTime", valor_inicial="NOW()"),
            col("FechaFin", "DateTime"),
            col("Finalizado", "Yes/No", valor_inicial="FALSE"),
        ]),

    "CHD_ChecklistDetalle": dict(
        grupo="Checklist",
        proposito=("Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su "
                   "texto: sin eso no hay comparacion historica posible."),
        columnas=[
            col("DetalleID", "Text", pk=True),
            col("ChecklistID", "Ref", ref="CHK_Checklists", obligatoria=True, es_parte_de=True),
            col("PreguntaID", "Ref", ref="FRM_Preguntas", obligatoria=True,
                nota="Antes se guardaba el texto de la pregunta. Supuesto D-11"),
            col("RespuestaTexto", "LongText"),
            col("RespuestaNumero", "Decimal"),
            col("RespuestaBoolean", "Yes/No"),
            col("RespuestaLista", "Enum"),
            col("Contestada", "Yes/No", valor_inicial="FALSE"),
            col("Observacion", "LongText"),
        ]),

    # ============================================================= FORMULARIOS
    "FRM_Formularios": dict(
        grupo="Formularios",
        proposito="Registro maestro de los 18 checklists, uno por tipo de activo.",
        columnas=[
            col("FormularioID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Descripcion", "Text"),
            col("Version", "Number", obligatoria=True, valor_inicial="1"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "FRM_Secciones": dict(
        grupo="Formularios",
        proposito="Agrupacion de preguntas dentro del formulario.",
        columnas=[
            col("SeccionID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Orden", "Number", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "FRM_Preguntas": dict(
        grupo="Formularios",
        proposito=("Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, "
                   "FRM_CCTV y FRM_PMVF, que eran una arquitectura paralela con otro esquema."),
        columnas=[
            col("PreguntaID", "Text", pk=True),
            col("FormularioID", "Ref", ref="FRM_Formularios", obligatoria=True),
            col("SeccionID", "Ref", ref="FRM_Secciones", obligatoria=True),
            col("Orden", "Number", obligatoria=True),
            col("Pregunta", "Text", obligatoria=True),
            col("TipoRespuestaID", "Ref", ref="TPR_TiposRespuesta", obligatoria=True),
            col("Obligatoria", "Yes/No", valor_inicial="TRUE"),
            col("ValorMinimo", "Decimal"),
            col("ValorMaximo", "Decimal"),
            col("Unidad", "Text"),
            col("Ayuda", "Text"),
            col("VisibleSi", "Text", nota="Expresion de visibilidad condicional"),
            col("RequiereFoto", "Yes/No", valor_inicial="FALSE"),
            col("Version", "Number", valor_inicial="1"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "TPR_TiposRespuesta": dict(
        grupo="Formularios",
        proposito="Tipo de dato esperado en cada respuesta.",
        columnas=[
            col("TipoRespuestaID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),

    "LST_ValoresLista": dict(
        grupo="Formularios",
        proposito="Opciones de las preguntas de tipo lista.",
        columnas=[
            col("ValorListaID", "Text", pk=True),
            col("PreguntaID", "Ref", ref="FRM_Preguntas", obligatoria=True,
                nota="Antes referenciaba la pregunta por su texto"),
            col("Valor", "Text", obligatoria=True),
            col("Orden", "Number"),
            col("Activo", "Yes/No", valor_inicial="TRUE"),
        ]),
}


# ------------------------------------------------------- tablas que se retiran
RETIRADAS = {
    "GPS": ("Duplica Coordenadas_Cierre y Precision_GPS de MAN_Mantenimientos. "
            "Nunca recibio un registro."),
    "FRM_SOS": "Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.",
    "FRM_CCTV": "Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.",
    "FRM_PMVF": "Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.",
    "SEC_Secciones": "Duplicada con FRM_Secciones. Se consolida en una sola.",
}

# ------------------------------------------- campos que se retiran de MAN
CAMPOS_RETIRADOS = {
    "MAN_Mantenimientos": {
        "Imagen_Inicio": "Sustituido por FOT_Fotografias con Tipo=Antes.",
        "Imagen_Final": "Sustituido por FOT_Fotografias con Tipo=Despues.",
        "Firma_Tecnico": "Sustituido por FIR_Firmas.",
        "Firma_Supervisor": "El supervisor aprueba en el portal, no firma. Supuesto D-10.",
        "Localizacion": "Ambiguo y redundante con Coordenadas_Cierre.",
        "Diagnostico": "Se responde en el checklist, no en campo libre.",
        "Trabajo_Realizado": "Se responde en el checklist.",
        "Repuestos_Utilizados": "Gestion de repuestos esta fuera de alcance.",
        "Requiere_Repuesto": "Se cubre con MotivoPendienteID = Falta de repuesto.",
        "Duracion_Minutos": "Se calcula de FechaHoraInicio y FechaHoraFin.",
        "Tipo": "El tipo es de la orden, no de la ejecucion.",
        "Fecha": "Redundante con FechaHoraInicio.",
        "Estado_Intervencion": "Redundante con el estado de la orden.",
    },
}

# --------------------------------------------------------- reglas de la app
REGLAS = [
    dict(id="RG-01", tabla="MAN_Mantenimientos", columna="Coordenadas_Cierre",
         tipo="Valid_If", cubre="RF-012",
         expresion="DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]",
         descripcion=("Impide cerrar lejos del activo, con radio por tipo. La ruta atraviesa dos "
                      "referencias, de ahi que cablearlas sea el primer paso de todo.")),
    dict(id="RG-02", tabla="MAN_Mantenimientos", columna="Precision_GPS",
         tipo="Initial value", cubre="RF-011",
         expresion="USERLOCATIONACCURACY()",
         descripcion="Registra el error del satelite en metros, para distinguir un cierre legitimo de uno dudoso."),
    dict(id="RG-03", tabla="MAN_Mantenimientos", columna="MotivoExcepcion",
         tipo="Required_If", cubre="D-04",
         expresion="[CierreConExcepcion] = TRUE",
         descripcion="Si el tecnico cierra con excepcion por GPS deficiente, debe justificarlo por escrito."),
    dict(id="RG-04", tabla="ACT_Activos", columna="(tabla)",
         tipo="Security Filter", cubre="RF-004",
         expresion='IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))',
         descripcion=("Cada tecnico descarga solo los activos de las unidades funcionales que tiene "
                      "asignadas. Controla el volumen de sincronizacion, no solo la visibilidad.")),
    dict(id="RG-05", tabla="OT_OrdenesTrabajo", columna="(tabla)",
         tipo="Security Filter", cubre="RF-004",
         expresion='OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())',
         descripcion="El tecnico ve sus ordenes; el supervisor, las que supervisa."),
    dict(id="RG-06", tabla="MAN_Mantenimientos", columna="(tabla)",
         tipo="Bot", cubre="RF-016",
         expresion='[EstadoActivoID].[GeneraAlerta] = TRUE',
         descripcion="Envia correo con informe PDF al CCO y al supervisor cuando el activo queda fuera de servicio."),
    dict(id="RG-07", tabla="OT_OrdenesTrabajo", columna="(tabla)",
         tipo="Bot", cubre="RF-003",
         expresion="Adds",
         descripcion="Notifica por correo al tecnico cuando se le asigna una orden."),
    dict(id="RG-08", tabla="OT_OrdenesTrabajo", columna="EstadoOrdenID",
         tipo="Bot programado", cubre="D-06",
         expresion='AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())',
         descripcion="Marca como Vencida la orden cuya fecha programada paso sin cerrarse."),
    dict(id="RG-09", tabla="CHK_Checklists", columna="VersionFormulario",
         tipo="Initial value", cubre="D-11",
         expresion="[FormularioID].[Version]",
         descripcion="Congela la version del formulario con que se respondio, para comparar historico."),
    dict(id="RG-11", tabla="PLA_PlanMantenimiento", columna="ProximaFecha",
         tipo="App formula", cubre="Plan de mantenimiento",
         expresion="[UltimaEjecucion] + [FrecuenciaID].[Dias]",
         descripcion="Calcula cuando vuelve a tocar el preventivo de ese activo."),
    dict(id="RG-12", tabla="PLA_PlanMantenimiento", columna="(tabla)",
         tipo="Bot programado", cubre="Plan de mantenimiento",
         expresion="[ProximaFecha] <= TODAY() + 7",
         descripcion=("Genera las ordenes de la semana a partir del plan y notifica al tecnico "
                      "responsable. REQUIERE PLAN PAGADO: en el gratuito los bots programados no "
                      "se ejecutan.")),
    dict(id="RG-13", tabla="MAN_Mantenimientos", columna="(tabla)",
         tipo="Verificacion de evidencia", cubre="Prueba de presencia",
         expresion="DISTANCE([UbicacionEscaneo], [Coordenadas_Cierre]) <= 0.5",
         descripcion=("Contrasta donde escaneo con donde cerro. Una diferencia grande indica que "
                      "escaneo en un sitio y cerro en otro. No bloquea: se reporta.")),
    dict(id="RG-10", tabla="MAN_Mantenimientos", columna="(tabla)",
         tipo="Bot", cubre="D-07",
         expresion='[RequiereSegundaVisita] = TRUE',
         descripcion="Genera una orden de seguimiento enlazada a la original mediante OTOrigenID."),
]
