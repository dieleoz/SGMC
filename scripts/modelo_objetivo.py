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
    valid_if, mensaje_error, es_parte_de, nota, oculta, valores.

    valores es el DATO -la lista del Enum- y nota es PROSA. Estaban mezclados: el
    generador del manual partia la nota por comas y la publicaba como valores, asi
    que Criticidad salia con un valor llamado "Baja. Pondera la disponibilidad de
    D-13". Es justo el fallo que CLAUDE.md 7.9 prohibe, cometido por el generador."""
    d = {"nombre": nombre, "tipo": tipo}
    d.update(kw)
    return d


MODELO = {

    # ============================================================== CATALOGOS

    "SED_Sedes": dict(
        grupo="Catalogos",
        proposito=("Edificaciones del corredor: CCO, peajes y basculas. Cada una esta al lado "
                   "de la via, en un PR concreto, y por tanto dentro de una unidad funcional. "
                   "Es el PADRE DE UBICACION del equipo bajo techo: un servidor, un NAS o una "
                   "impresora no estan en un punto de la via, estan DENTRO de un edificio, y "
                   "de el heredan donde estan."),
        columnas=[
            col("SedeID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Ciudad", "Text"),
            col("UnidadFuncionalID", "Ref", ref="UNF_UnidadesFuncionales", obligatoria=True,
                nueva=True, nota="La UF en la que cae el PR del edificio. Sin esto la sede no sabe donde "
                     "esta, que es justo por lo que el requisito de que el equipo de un peaje "
                     "heredara su unidad funcional estuvo registrado como no cubierto"),
            col("PR", "Text", nueva=True, nota="Punto de referencia de INVIAS del edificio"),
            col("TramoINVIAS", "Text", nueva=True,
                nota="La ruta a la que pertenece ese PR. El peaje de Macheta esta en la 5607"),
            col("PK", "Text", nueva=True,
                nota="Punto kilometrico del proyecto, lineal. El que no es ambiguo"),
            col("Ubicacion", "LatLong", nueva=True, nota="Coordenada de la edificacion"),
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
            col("PKInicial", "Text", nueva=True,
                nota="Kilometro lineal del proyecto donde empieza la unidad funcional"),
            col("PKFinal", "Text", nueva=True,
                nota="Kilometro lineal del proyecto donde termina"),
            col("PRInicial", "Text",
                nota="PR de INVIAS del contrato, CON SU RUTA porque cada ruta reinicia la "
                     "numeracion. Apendice Tecnico 1, Tabla 3"),
            col("PRFinal", "Text",
                nota="Idem. La UF1 empieza en una ruta y termina en otra, de ahi que la ruta "
                     "viaje dentro del valor y no en una columna aparte"),
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
            col("Categoria", "Enum", valores=["ITS", "Electrico", "Comunicaciones", "TI"]),
            col("FormularioID", "Ref", ref="FRM_Formularios", obligatoria=True,
                nota="Sin este mapeo no hay checklist dinamico. Estuvo vacio en la hoja de la "
                     "aplicacion anterior, y de ahi viene el aviso. HOY ESTA "
                     "POBLADO EN LAS DOS HOJAS VIVAS: 18 de 18 en la de produccion y 27 de 27 en "
                     "la plantilla"),
            col("TieneQR", "Yes/No", valor_inicial="TRUE"),
            col("RequiereGPS", "Yes/No", valor_inicial="TRUE"),
            col("RadioGeofencingKm", "Decimal", valor_inicial="0.2",
                nota="Supuesto D-02: radio por tipo, no un numero unico. El catalogo "
                     "(scripts/catalogo_tipos.py) lo fija por tipo y la plantilla lo trae "
                     "poblado en los 27; el valor inicial solo aplica a un tipo nuevo"),
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
            col("QuienCambia", "Enum", valores=["Sistema", "Tecnico", "Supervisor"]),
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

    "PAR_Parametros": dict(
        grupo="Catalogos",
        proposito=("Umbrales que el administrador ajusta con las pruebas de campo, sin tocar la "
                   "configuracion de la aplicacion. Existe porque un numero magico escondido en "
                   "una expresion no se puede calibrar: hay que abrir el editor, encontrarlo y "
                   "arriesgarse a romper la regla. Aqui es una celda."),
        nueva=True,
        acceso_por_lookup=True,   # no la referencia nadie: se lee con LOOKUP()
        columnas=[
            col("ParametroID", "Text", pk=True),
            col("Nombre", "Text", obligatoria=True),
            col("Valor", "Decimal", obligatoria=True),
            col("Unidad", "Text"),
            col("Descripcion", "LongText"),
            col("Activo", "Yes/No", valor_inicial="TRUE",
                nota="DECORATIVA: LOOKUP() no filtra por esta columna, asi que desactivar un "
                     "parametro no lo desactiva. Se conserva por coherencia con los demas "
                     "catalogos, pero no es un interruptor: para dejar de aplicar un umbral se "
                     "cambia su valor, no su bandera"),
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
            col("PK", "Text", nueva=True,
                nota="Punto kilometrico DEL PROYECTO: lineal y continuo desde 0+000 hasta el "
                     "final. Es el unico que identifica un punto sin ambiguedad en todo el "
                     "corredor"),
            col("TramoINVIAS", "Text", nueva=True,
                nota="La ruta de INVIAS a la que pertenece el PR: 55CN03, 5607 o 5608. SIN ELLA "
                     "EL PR NO IDENTIFICA UN PUNTO, y no es teoria: el corredor tiene dos sitios "
                     "distintos llamados PR 0+000 -el arranque en El Sisga sobre la 55CN03 y "
                     "Guateque sobre la 5608-, separados por unos 50 km"),
            col("SedeID", "Ref", ref="SED_Sedes", nueva=True,
                nota="Solo para el equipo bajo techo -servidores, NAS, impresoras, video wall-, "
                     "que vive DENTRO de una edificacion y no en un punto de la via. Vacia en "
                     "el equipo de corredor, que tiene su propio PR y su propia coordenada. "
                     "Cuando esta puesta, RG-21 obliga a que la unidad funcional del activo sea "
                     "la de su edificacion: la UF se guarda en un solo sitio y no en dos"),
            col("EstadoActivoID", "Ref", ref="EST_Activo", obligatoria=True),
            col("CodigoQR", "Text", nota="Configurada como Searchable y Scan"),
            col("FrecuenciaID", "Ref", ref="FRE_Frecuencias"),
            col("Criticidad", "Enum", valores=["Alta", "Media", "Baja"],
                nota="Pondera la disponibilidad de D-13"),
            col("FechaBaja", "Date", nueva=True,
                nota="Cuando se dio de baja. Sin ella el historico no puede explicar por que el "
                     "activo dejo de recibir mantenimiento, y esa pregunta la hace la interventoria"),
            col("MotivoBaja", "Enum", nueva=True,
                valores=["Obsolescencia", "Dano irreparable", "Robo o vandalismo",
                         "Reemplazo", "Retiro por obra"]),
            col("Activo", "Yes/No", formula='[EstadoActivoID].[Nombre] <> "Retirado"',
                nota="NO se edita a mano: se deriva del estado. Tener dos formas de decir "
                     "'dado de baja' garantiza que algun dia se contradigan"),
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
            col("Tipo", "Enum", obligatoria=True, valores=["Preventivo", "Correctivo"]),
            col("FechaProgramada", "DateTime", obligatoria=True),
            col("EstadoOrdenID", "Ref", ref="EOT_EstadosOrden", obligatoria=True),
            col("OTOrigenID", "Ref", ref="OT_OrdenesTrabajo", nueva=True, alias_justificado="Autorreferencia: la orden que origino esta",
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
            col("OTID", "Ref", ref="OT_OrdenesTrabajo", obligatoria=True,
                nota="Era Text. Ese solo hecho impedia todo el geofencing. SIN IsPartOf por "
                     "decision del 2026-08-07: marcarlo haria que borrar una orden borrase su "
                     "ejecucion, y con ella las fotografias, las firmas y el checklist. La "
                     "ejecucion es el registro historico y sobrevive a su orden"),
            col("TecnicoID", "Ref", ref="USR_Usuarios", obligatoria=True, alias_justificado="Rol: quien ejecuta",
                valor_inicial='LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")'),
            col("FechaHoraInicio", "DateTime", obligatoria=True, valor_inicial="NOW()"),
            col("FechaHoraFin", "DateTime"),
            col("OrigenApertura", "Enum", valores=["QR", "Lista"], valor_inicial="Lista",
                nota="Abrir por lista no prueba presencia; se marca para poder exigir "
                     "QR donde importe y para medir cuantos cierres carecen de escaneo. El QR esta fuera de alcance desde el 2026-08-07, asi que hoy el valor inicial es Lista"),
            col("UbicacionEscaneo", "LatLong", editable=False,
                nota="Donde estaba el tecnico al escanear. Junto con Coordenadas_Cierre permite "
                     "comprobar que llego y se quedo, no que paso cerca"),
            col("FechaHoraEscaneo", "DateTime", editable=False,
                nota="Con FechaHoraFin da la duracion real de la intervencion"),
            col("EstadoActivoID", "Ref", ref="EST_Activo", obligatoria=True, nueva=True,
                nota="Estado en que queda el activo tras la intervencion. No existe en produccion: "
                     "se crea. El Excel local tiene 'Estado Final', que produccion no tiene"),
            col("Coordenadas_Cierre", "LatLong", obligatoria=True, valor_inicial="HERE()", editable=False,
                valid_if="DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]",
                mensaje_error="Ubicacion fuera de rango: debe estar junto al activo para cerrar."),
            col("Precision_GPS", "Number", valor_inicial="USERLOCATIONACCURACY()", editable=False),
            col("CierreConExcepcion", "Yes/No",
                formula='[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")',
                nota="Se calcula, no se edita (RG-19). El umbral vive en PAR_Parametros"),
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
            col("Tipo", "Enum", obligatoria=True,
                valores=["Activo no inventariado", "Falla detectada"]),
            col("Descripcion", "LongText", obligatoria=True),
            col("Ubicacion", "LatLong", obligatoria=True, valor_inicial="HERE()"),
            col("Fotografia", "Image", obligatoria=True),
            col("ActivoID", "Ref", ref="ACT_Activos", nota="Solo si la novedad es sobre uno existente"),
            col("Estado", "Enum", valor_inicial="Reportada",
                valores=["Reportada", "Aceptada", "Descartada"]),
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
            col("Criticidad", "Enum", valores=["Alta", "Media", "Baja"]),
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
            col("Tipo", "Enum", obligatoria=True, valores=["Antes", "Despues", "Novedad"]),
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
            col("TipoFirma", "Enum", obligatoria=True, valores=["Tecnico"],
                nota="Solo Tecnico. La firma del supervisor no se captura en campo"),
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
            col("RespuestaLista", "Enum",
                nota="Los valores salen de LST_ValoresLista por pregunta, no de una lista fija"),
            col("Contestada", "Yes/No", valor_inicial="FALSE"),
            col("Observacion", "LongText"),
        ]),

    # ============================================================= FORMULARIOS
    "FRM_Formularios": dict(
        grupo="Formularios",
        proposito="Registro maestro de los checklists, uno por tipo de activo: 27 en "
                  "BD/Modelo_Datos_PLANTILLA.xlsx, 18 en la hoja de produccion.",
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
                        col("RequiereGPS", "Yes/No", valor_inicial="FALSE",
                nota="La lee el show_if de CHD_ChecklistDetalle.RespuestaGPS"),
            col("RequiereFirma", "Yes/No", valor_inicial="FALSE"),
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

# ------------------------------------------- campos que se retiran
CAMPOS_RETIRADOS = {
    "USR_Usuarios": {
        "SedeID": "Retirada el 2026-08-10 para que el modelo diga lo que dice la "
                  "especificacion. FUNCIONAL_SGMC 6.3 la declara descartada frente a "
                  "ASG_AsignacionZona: la sede es un edificio y la asignacion es un tramo, "
                  "y un tecnico puede atender varias unidades funcionales, asi que la "
                  "relacion es de muchos a muchos y no cabe como columna. RG-04, el filtro "
                  "de seguridad que decide que activos ve cada tecnico, lee la asignacion y "
                  "no menciona la sede. El modelo la declaraba Ref obligatoria mientras la "
                  "spec la daba por descartada: se contradecian, y cablearla habria dejado "
                  "dos formas de decir donde trabaja alguien.",
    },
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
    "OT_OrdenesTrabajo": {
        "FormularioID": "El formulario lo determina el tipo del activo, no la orden.",
        "Motivo_Cierre": "Se tipifica en MOT_MotivosPendiente desde la ejecucion.",
        "Informe_Final": "Se genera del mantenimiento y su checklist, no se transcribe.",
    },
    "ACT_Activos": {
    },
    "CHK_Checklists": {
        "ActivoID": "Se alcanza por [MantenimientoID].[OTID].[ActivoID].",
        "TecnicoID": ("Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato "
                      "de prueba dejo 'Santiago Moreno' en lugar de un identificador."),
        "Observaciones": "La observacion es de la ejecucion o de la respuesta, no del encabezado.",
        "FechaCreacion": "Redundante con FechaInicio.",
        "Estado": "Sustituido por Finalizado, que produccion ya tiene.",
        "GPSInicio": "La coordenada es del mantenimiento y de cada fotografia, no del checklist.",
        "GPSFin": "Idem.",
        "FirmaTecnico": "Sustituido por FIR_Firmas.",
        "FirmaSupervisor": "El supervisor aprueba en el portal, no firma. Supuesto D-10.",
        "PDF": "El informe se genera al enviarlo, no se almacena en la fila.",
        "FechaEnvioCorreo": "Es traza del bot, no del checklist.",
        "Activo": "El checklist es parte de su mantenimiento: no se desactiva por separado.",
        "PreguntaActual": "Estado de la interfaz, no dato. Se deriva de las respuestas.",
        "TotalPreguntas": "Se cuenta de FRM_Preguntas.",
        "Porcentaje": "Se calcula. Guardarlo permite que contradiga al detalle.",
    },
    "CHD_ChecklistDetalle": {
        "Orden": "Se alcanza por [PreguntaID].[Orden].",
        "TipoRespuestaID": "Se alcanza por [PreguntaID].[TipoRespuestaID].",
        "PreguntaActual": "Estado de la interfaz, no dato.",
        "EstadoPregunta": "Redundante con Contestada.",
        "TotalPreguntas": "No es del detalle sino del encabezado, y ademas se cuenta.",
        "RespuestaFecha": "Fuera de alcance: ninguna pregunta usa tipo fecha.",
        "RespuestaHora": "Fuera de alcance: ninguna pregunta usa tipo hora.",
        "RespuestaFoto": "Sustituido por FOT_Fotografias.",
        "RespuestaFirma": "Sustituido por FIR_Firmas.",
        "RespuestaGPS": "La coordenada es del mantenimiento y de cada fotografia.",
        "FechaRespuesta": "Se deriva del ChangeTimestamp del mantenimiento.",
        "Activo": "El detalle es parte de su checklist: no se desactiva por separado.",
    },
}

# ------------------------------------- renombrados: nombre actual -> objetivo
#
# Cableado de referencias. Una referencia de AppSheet guarda el valor de la CLAVE
# de la tabla destino, de modo que renombrar y retipar no son dos tareas: son la
# misma. Se declaran aqui para que la migracion sea verificable y no dependa de
# que alguien recuerde el mapeo.
#
# FUENTE: Google Sheets de PRODUCCION, leido el 2026-08-07 con el conector de
# Drive, el que declara scripts/sistema.py. NO el Excel local.
#
# Una version anterior de este mapeo se construyo sobre el Excel y era incorrecta
# para MAN_Mantenimientos: el Excel la llama MantenimientoID y TecnicoID, y
# produccion las llama MttoID y Tecnico_Asignado. Produccion es lo que corre la
# app, de modo que manda produccion. Ese error es exactamente lo que el pipeline
# SDD viene a impedir.
CAMPOS_RETIRADOS = {
    "USR_Usuarios": {
        "SedeID": "Retirada el 2026-08-10 para que el modelo diga lo que dice la "
                  "especificacion. FUNCIONAL_SGMC 6.3 la declara descartada frente a "
                  "ASG_AsignacionZona: la sede es un edificio y la asignacion es un tramo, "
                  "y un tecnico puede atender varias unidades funcionales, asi que la "
                  "relacion es de muchos a muchos y no cabe como columna. RG-04, el filtro "
                  "de seguridad que decide que activos ve cada tecnico, lee la asignacion y "
                  "no menciona la sede. El modelo la declaraba Ref obligatoria mientras la "
                  "spec la daba por descartada: se contradecian, y cablearla habria dejado "
                  "dos formas de decir donde trabaja alguien.",
    },
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
    "OT_OrdenesTrabajo": {
        "FormularioID": "El formulario lo determina el tipo del activo, no la orden.",
        "Motivo_Cierre": "Se tipifica en MOT_MotivosPendiente desde la ejecucion.",
        "Informe_Final": "Se genera del mantenimiento y su checklist, no se transcribe.",
    },
    "ACT_Activos": {
    },
    "CHK_Checklists": {
        "ActivoID": "Se alcanza por [MantenimientoID].[OTID].[ActivoID].",
        "TecnicoID": ("Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato "
                      "de prueba dejo 'Santiago Moreno' en lugar de un identificador."),
        "Observaciones": "La observacion es de la ejecucion o de la respuesta, no del encabezado.",
        "FechaCreacion": "Redundante con FechaInicio.",
        "Estado": "Sustituido por Finalizado, que produccion ya tiene.",
        "GPSInicio": "La coordenada es del mantenimiento y de cada fotografia, no del checklist.",
        "GPSFin": "Idem.",
        "FirmaTecnico": "Sustituido por FIR_Firmas.",
        "FirmaSupervisor": "El supervisor aprueba en el portal, no firma. Supuesto D-10.",
        "PDF": "El informe se genera al enviarlo, no se almacena en la fila.",
        "FechaEnvioCorreo": "Es traza del bot, no del checklist.",
        "Activo": "El checklist es parte de su mantenimiento: no se desactiva por separado.",
        "PreguntaActual": "Estado de la interfaz, no dato. Se deriva de las respuestas.",
        "TotalPreguntas": "Se cuenta de FRM_Preguntas.",
        "Porcentaje": "Se calcula. Guardarlo permite que contradiga al detalle.",
    },
    "CHD_ChecklistDetalle": {
        "Orden": "Se alcanza por [PreguntaID].[Orden].",
        "TipoRespuestaID": "Se alcanza por [PreguntaID].[TipoRespuestaID].",
        "PreguntaActual": "Estado de la interfaz, no dato.",
        "EstadoPregunta": "Redundante con Contestada.",
        "TotalPreguntas": "No es del detalle sino del encabezado, y ademas se cuenta.",
        "RespuestaFecha": "Fuera de alcance: ninguna pregunta usa tipo fecha.",
        "RespuestaHora": "Fuera de alcance: ninguna pregunta usa tipo hora.",
        "RespuestaFoto": "Sustituido por FOT_Fotografias.",
        "RespuestaFirma": "Sustituido por FIR_Firmas.",
        "RespuestaGPS": "La coordenada es del mantenimiento y de cada fotografia.",
        "FechaRespuesta": "Se deriva del ChangeTimestamp del mantenimiento.",
        "Activo": "El detalle es parte de su checklist: no se desactiva por separado.",
    },
}

# ------------------------------------- renombrados: nombre actual -> objetivo
#
# Cableado de referencias. Una referencia de AppSheet guarda el valor de la CLAVE
# de la tabla destino, de modo que renombrar y retipar no son dos tareas: son la
# misma. Se declaran aqui para que la migracion sea verificable y no dependa de
# que alguien recuerde el mapeo.
#
# FUENTE: Google Sheets de PRODUCCION, leido el 2026-08-07 con el conector de
# Drive, el que declara scripts/sistema.py. NO el Excel local.
#
# Una version anterior de este mapeo se construyo sobre el Excel y era incorrecta
# para MAN_Mantenimientos: el Excel la llama MantenimientoID y TecnicoID, y
# produccion las llama MttoID y Tecnico_Asignado. Produccion es lo que corre la
# app, de modo que manda produccion. Ese error es exactamente lo que el pipeline
# SDD viene a impedir.
RENOMBRADOS = {
    "OT_OrdenesTrabajo": {
        "Numero_OT": ("OTID", "La clave se llamaba distinto de la referencia que la apunta. "
                              "Ese solo desajuste produjo el checklist huerfano d02d8a3d."),
        "Activo": ("ActivoID", "Guarda enteros que son ActivoID (2, 26, 5, 9, 27, 3). Es la "
                               "referencia al activo, con nombre que parece una bandera."),
        "Tecnico": ("TecnicoID", "Guarda enteros que son UsuarioID."),
        "SupervidorID": ("SupervisorID", "Error de escritura en el encabezado de produccion."),
        "Fecha Programada": ("FechaProgramada", "Los espacios en el nombre obligan a citarlo."),
        "Estado": ("EstadoOrdenID", "Pasa de texto libre a referencia contra EOT_EstadosOrden."),
        "Fecha_Cierre": ("FechaCierre", "Convencion de nombres."),
        "Cerrada_Por": ("CerradaPor", "Convencion de nombres."),
    },
    "ACT_Activos": {
        "EstadoID": ("EstadoActivoID", "La referencia se llama como la clave destino."),
    },
    "USR_Usuarios": {
        "usuarioID": ("UsuarioID", "Produccion la escribe en minuscula inicial. AppSheet resuelve "
                                   "por nombre literal."),
        "Estado": ("Activo", "Convencion: todas las tablas usan Activo como bandera."),
    },
    "MAN_Mantenimientos": {
        "MttoID": ("MantenimientoID", "La clave no seguia la convencion <Prefijo>ID legible."),
        "Tecnico_Asignado": ("TecnicoID", "Pasa a referencia contra USR_Usuarios."),
        "Fecha_Hora_Inicio": ("FechaHoraInicio", "Convencion de nombres."),
        "Fecha_Hora_Fin": ("FechaHoraFin", "Convencion de nombres."),
        "Requiere_Segunda_Visita": ("RequiereSegundaVisita", "Convencion de nombres."),
        "Motivo_Pendiente": ("MotivoPendienteID", "Pasa a referencia contra MOT_MotivosPendiente."),
        "Aprobado_Supervisor": ("AprobadoSupervisor", "Convencion de nombres."),
        "Usuario_Registro": ("UsuarioRegistro", "Convencion de nombres."),
        "Fecha_Hora_Registro": ("FechaHoraRegistro", "Convencion de nombres."),
    },
    "CHK_Checklists": {
        "OTID": ("MantenimientoID", "Cambia de padre: el checklist cuelga de la ejecucion, no "
                                    "de la orden. La inspeccion es parte de ejecutar."),
    },
    "CHD_ChecklistDetalle": {
        "Observaciones": ("Observacion", "Singular: es la observacion de una respuesta, no de la "
                                         "tabla."),
    },
    "LST_ValoresLista": {
        "ListaID": ("ValorListaID", "La clave se llamaba distinto de la convencion. Detectado el "
                                    "2026-08-07 al verificar la Fase A, no antes."),
    },
    "ROL_Roles": {
        "Descripción": ("Descripcion", "AppSheet resuelve por nombre literal: la tilde obliga "
                                        "a escribirla en cada expresion."),
    },
    "FRM_Formularios": {
        "Descripción": ("Descripcion", "Idem."),
        "Versión": ("Version", "Idem."),
    },
}

# ------------------------- retipados: conservan el nombre, cambian de tipo
#
# El defecto raiz del sistema actual. La columna existe y se llama bien, pero es
# Text, de modo que no se puede desreferenciar: AppSheet responde "Invalid
# dereference. Column OTID is not a Ref". No hay nada que renombrar, solo que
# retipar, y por eso es el error que lleva meses pasando desapercibido.
#
# Una conversion Text -> Ref solo conserva las filas cuyo valor coincide con la
# CLAVE del destino. Las que no coincidan quedan huerfanas y en silencio.
RETIPADOS = {
    "MAN_Mantenimientos": {
        "OTID": ("Text", "Ref", "OT_OrdenesTrabajo",
                 "Verificado: AppSheet rechaza la desreferencia porque es Text. La tabla tiene "
                 "0 filas, asi que hoy la conversion no arrastra ningun dato. Es el momento "
                 "mas barato en que se podra hacer."),
    },
    "ACT_Activos": {
        "TipoActivoID": ("Number", "Ref", "TIP_TiposActivo",
                         "Guarda enteros 1 a 18 en la hoja de produccion y 1 a 27 en la plantilla, "
                         "que trae los nueve tipos anadidos. Por confirmar en produccion."),
        "CalzadaID": ("Number", "Ref", "CAL_Calzadas", "Por confirmar en produccion."),
        "SentidoID": ("Number", "Ref", "SEN_Sentidos", "Por confirmar en produccion."),
        "FrecuenciaID": ("Number", "Ref", "FRE_Frecuencias", "Por confirmar en produccion."),
    },
    "CHK_Checklists": {
        "FormularioID": ("Text", "Ref", "FRM_Formularios", "Por confirmar en produccion."),
    },
    "CHD_ChecklistDetalle": {
        "ChecklistID": ("Text", "Ref", "CHK_Checklists",
                        "Ademas IsPartOf: el detalle vive y muere con su encabezado."),
        "PreguntaID": ("Text", "Ref", "FRM_Preguntas",
                       "Produccion ya la llama PreguntaID, pero LST_ValoresLista guarda ahi el "
                       "TEXTO 'Estado encontrado' en vez de la clave. Confirmar antes de convertir."),
    },
    "USR_Usuarios": {
        "RolID": ("Number", "Ref", "ROL_Roles", "Guarda enteros 2 a 5. Por confirmar el tipo."),
    },
    "TIP_TiposActivo": {
        "FormularioID": ("Text", "Ref", "FRM_Formularios",
                         "Poblado en las dos hojas vivas: 18 de 18 en la de produccion, con "
                         "valores FRM_SOS a FRM_SUBE, y 27 de 27 en la plantilla. Estuvo vacio en "
                         "la hoja de la aplicacion abandonada, que es de donde viene ese aviso en "
                         "documentos antiguos. Todos los valores existen en FRM_Formularios: la "
                         "conversion no produce huerfanos en ninguna de las dos."),
    },
    "LST_ValoresLista": {
        "PreguntaID": ("Text", "Ref", "FRM_Preguntas",
                       "PELIGRO: sus 4 filas guardan el TEXTO 'Estado encontrado', no una clave. "
                       "Convertir a Ref las deja huerfanas a las cuatro. Corregir los valores "
                       "antes, o dejarla como Text y anotarlo como deuda."),
    },
    "FRM_Preguntas": {
        "FormularioID": ("Text", "Ref", "FRM_Formularios", "Por confirmar el tipo."),
        "SeccionID": ("Number", "Ref", "FRM_Secciones", "Por confirmar el tipo."),
        "TipoRespuestaID": ("Number", "Ref", "TPR_TiposRespuesta", "Por confirmar el tipo."),
    },
}

# ------------------------------- valores iniciales de PAR_Parametros
#
# Se declaran aqui para que el verificador pueda contrastar la hoja contra el
# modelo. El administrador los ajusta EN LA HOJA tras las pruebas de campo; lo
# que no puede pasar es que la hoja diga una cosa y las reglas asuman otra.
PARAMETROS = {
    "UMBRAL_GPS": (40, "m",
                   "Error del satelite por encima del cual el cierre se marca como excepcional "
                   "(RG-19). La precision tipica de un movil a cielo abierto es de 4,9 m segun "
                   "GPS.gov, asi que 40 deja unas ocho veces de margen para montana y estructuras. "
                   "D-04 decia 50; se baja a 40 al comprobar que 45 m ya es nueve veces la norma."),
    "RADIO_GEOFENCING_KM": (1.0, "km",
                            "Valor de respaldo, calibrable por el administrador. RG-01 NO lo lee: "
                            "el radio va por tipo, en TIP_TiposActivo.RadioGeofencingKm, poblado "
                            "en los 27. Se conserva porque un umbral escondido en una expresion "
                            "no se puede calibrar sin abrir el editor."),
    "DISTANCIA_ESCANEO_CIERRE_KM": (0.5, "km",
                                    "Diferencia maxima entre donde se escaneo y donde se cerro "
                                    "antes de senalarlo en el reporte (RG-13). No bloquea."),
}

# ----------------------------------------- catalogos con clave legible
#
# Tablas donde LA CLAVE ES EL VALOR QUE EL DATO YA GUARDABA (regla R-8), no un
# identificador inventado aparte. Solo contra estas es legitimo comparar una
# columna Ref con un literal: la referencia guarda la clave, y aqui la clave es
# ese mismo valor.
#
# Ojo con el alcance: de las nueve, solo EOT_EstadosOrden ('Cerrada') y
# SEN_Sentidos ('SA') son palabras que alguien escribiria en una regla. Las otras
# siete son surrogates con prefijo -OT-0001, MOT-01, SOS001-, y V-17 queda
# apagada tambien para ellas. Es un alcance mayor del necesario, asumido a
# proposito: afinar mas la lista cuesta mas de lo que ahorra, y hoy no existe
# ninguna regla que compare contra un surrogate.
#
# EOT_EstadosOrden es el caso central: ESPEC-001B le puso 'Asignada', 'Cerrada'
# y 'Suspendida' como clave A PROPOSITO, siguiendo la regla R-8, para que las 6
# ordenes existentes resolvieran sin migrar nada. Escribir
# [EstadoOrdenID] = "Cerrada" es correcto.
#
# EST_Activo NO esta aqui: su clave es 1 a 4 y el nombre vive en Nombre. Por eso
# [EstadoActivoID] <> "Retirado" es siempre cierto y hay que escribir
# [EstadoActivoID].[Nombre].
#
# Derivado del dato el 2026-08-07 sobre BD/Modelo de Datos (7).xlsx, no de una
# impresion. Si una tabla cambia de clave numerica a legible, se actualiza aqui.
CLAVE_LEGIBLE = {
    "OT_OrdenesTrabajo",       # OT-0001
    "EOT_EstadosOrden",        # Asignada, Cerrada, Suspendida
    "MOT_MotivosPendiente",    # MOT-01
    "FAL_ModosFalla",          # FAL-01
    "ASG_AsignacionZona",      # ASG-01
    "SEN_Sentidos",            # SA, AS
    "FRM_Formularios",         # FRM_SOS
    "FRM_Preguntas",           # SOS001
    "PLA_PlanMantenimiento",   # PLA-001
    "PAR_Parametros",          # UMBRAL_GPS
    "LST_ValoresLista",        # SOS001-1, derivada de la pregunta que la usa.
                               # Cuatro de sus claves eran 1, 2, 3 y 4, y como el
                               # resto es texto AppSheet las habria descartado:
                               # el desplegable de la primera pregunta del
                               # checklist de SOS se habria quedado vacio.
}

# ------------------------------------------- catalogos de clave GENERADA
#
# Tablas cuya clave la genera la aplicacion con UNIQUEID(). Hoy sus valores
# parecen legibles -TEST-MTTO-001, TEST-FOT-001- pero eso es el fixture que
# escribio la Fase A a mano: desde la PRIMERA fila que cree la aplicacion son
# cadenas aleatorias.
#
# Por eso NO estan en CLAVE_LEGIBLE, aunque el archivo de hoy diga que lo son.
# Comparar un Ref a una de estas contra un literal de texto es SIEMPRE un error,
# y meterlas en CLAVE_LEGIBLE apagaria V-17 justo donde mas falta hace.
#
# Leccion de metodo: una lista derivada del dato puede ser cierta contra el
# fixture y falsa contra el diseno. Derivar no basta; hay que preguntarse si el
# dato del que se deriva es el definitivo.
CLAVE_GENERADA = {
    "MAN_Mantenimientos",
    "CHK_Checklists",
    "CHD_ChecklistDetalle",
    "FOT_Fotografias",
    "FIR_Firmas",
    "NOV_Novedades",
}

# ------------------------------------------ tablas PROPUESTAS que aun no existen
#
# Toda tabla que un documento mencione y no este en MODELO tiene que estar aqui,
# declarada UNA vez, con por que hace falta y donde se especifica.
#
# Por que existe esta lista
# -------------------------
# El 2026-08-07 se propusieron como "tablas a crear" ROL_Roles, FRM_Formularios,
# FRM_Secciones y FRM_Preguntas. Las cuatro YA ESTABAN en MODELO. Nadie mintio:
# se propusieron leyendo documentos en vez de volcar el modelo.
#
# verificar_documentos.py falla si una tabla aparece aqui y en MODELO a la vez.
# Esa comprobacion es lo unico que impide repetirlo.
PROPUESTAS = {
    "TUN_Tuneles": ("Los 15 tuneles del corredor, con su PR de entrada y salida. "
                    "DENTRO DE UN TUNEL EL GPS NO FIJA POSICION, y RG-01 comprueba la "
                    "distancia al activo al cerrar: todo equipo dentro de un tunel falla esa "
                    "comprobacion SIEMPRE, por diseno y no por averia. Hoy eso se manejaria "
                    "como excepcion caso por caso y el supervisor veria a un tecnico "
                    "acumulando cierres con excepcion sin saber que es el tunel y no el "
                    "tecnico. Con los tramos declarados se sabe de antemano. No es marginal: "
                    "son 7.224 metros, y en la UF3 son 6.000 de sus 17.800 -un tercio del "
                    "tramo va bajo tierra-. Datos en el contrato, Apendice Tecnico 1, "
                    "tablas 13, 19 y 20",
                    "sin especificar"),
    "TAR_Tareas": ("Un tipo de equipo tiene VARIAS tareas, cada una con su "
                   "periodicidad y su formulario. Hoy la periodicidad cuelga del "
                   "activo y el formulario del tipo, y ambos sitios son erroneos",
                   "ESPEC-003"),
    "ROL_Requeridos": ("Que rol exige cada tarea. Los doce roles ya estan en "
                       "ROL_Roles; lo que falta es colgarlos de la tarea",
                       "ESPEC-003"),
    "CRI_Criticidad": ("Criticidad de una correctiva y sus plazos de respuesta y "
                       "resolucion, para no enterrar los numeros en una expresion",
                       "ESPEC-003"),
    "PAU_Pausas": ("Pausas y reanudaciones de una orden. Tabla hija solo-anadir: "
                   "el reloj parado se DERIVA con SUM(), nunca se almacena como "
                   "acumulado, porque un acumulado compite consigo mismo sin senal",
                   "ESPEC-003"),
    "EVT_EventosOrden": ("Transiciones de estado de la orden, solo-anadir. De aqui "
                         "salen los tiempos de respuesta y resolucion. NO es lo mismo "
                         "que PAU_Pausas: un ChangeTimestamp en la propia orden se "
                         "reescribe en la segunda ida a En ejecucion y acorta el "
                         "tiempo de respuesta solo",
                         "ESPEC-003"),
    "ETR_Estructuras": ("Puentes y viaductos por los que pasa la fibra y que "
                        "exigen revision propia",
                        "MODELO_EVOLUCION_FASE_2 §4"),
    "MED_MedicionesHilo": ("Los 48 hilos de una medicion de ODF. Hija del "
                           "checklist, como FOT_Fotografias y FIR_Firmas",
                           "MODELO_EVOLUCION_FASE_2 §7"),
    "CER_Certificaciones": ("Catalogo de certificaciones: alturas, electricista, "
                            "electronico, ayudante, SISO",
                            "MODELO_EVOLUCION_FASE_2 §10 - Fase 2"),
    "USR_Certificaciones": ("Usuario x certificacion, con vigencia. Un certificado "
                            "de alturas caduca, y eso es una regla contra fecha, "
                            "no una etiqueta",
                            "MODELO_EVOLUCION_FASE_2 §10 - Fase 2"),
}

# ------------------------------- columnas de la hoja SIN DECIDIR
#
# Existen en la hoja y el modelo NO las declara: ni vivas, ni retiradas, ni
# renombradas. Al dar de alta una tabla, AppSheet las lee y aparecen en la
# aplicacion como si fueran buenas.
#
# No estan aqui para silenciar el verificador: estan para que la decision no se
# pierda. Cada una necesita que alguien diga si entra al modelo o se retira.
#
# Descubiertas el 2026-08-09 comparando encabezados de la hoja contra MODELO.
# ---------------------------- columnas PROPUESTAS sobre tablas que YA existen
#
# Mismo criterio que PROPUESTAS, para columnas. Una especificacion puede proponer
# una columna nueva sobre una tabla existente; verificar_documentos.py D-03 no
# sabe distinguir "propuesta" de "inventada", asi que se declara aqui.
COLUMNAS_PROPUESTAS = {
    ("ACT_Activos", "ActivoPadreID"):
        "Ref a ACT_Activos. El equipo compuesto: un panel de mensaje variable tiene portico, "
        "fuentes y camaras, y hoy cada pieza seria un activo suelto sin nada que diga de quien "
        "cuelga. Sin esto no se puede responder que se le hizo AL PANEL, solo que se le hizo a "
        "una de sus piezas.",
    ("TIP_TiposActivo", "SeVisita"): (
        "Discrimina los cinco tipos que no son cosas que se visitan -licencias, "
        "SSL, antivirus, ISP, radios-. NO reutilizar RequiereGPS: esa ya vale "
        "FALSE en SERVIDOR y NAS, que si se visitan",
        "ESPEC-003"),
    ("USR_Usuarios", "OficioID"): (
        "Donde se lee el oficio de la persona. Sin ella los doce oficios de "
        "ROL_Roles no compran nada",
        "ESPEC-003"),
}

COLUMNAS_SIN_DECIDIR = {
    ("USR_Usuarios", "UltimaSincronizacion"):
        "Probablemente de una version anterior. El modelo no la usa",
    ("FOT_Fotografias", "Fecha"):
        "El modelo guarda FechaHora. Sobra, o una de las dos esta mal nombrada. "
        "Merece mirada: la fecha de la fotografia es parte de la evidencia",
    ("FRM_Formularios", "Orden"):
        "Ordenaria los formularios en una lista. Hoy ninguna vista los ordena y la "
        "columna esta vacia. Si algun dia se ordenan, se decide aqui",
    ("FRM_Preguntas", "ValorDefecto"):
        "Precargaria la respuesta antes de que el tecnico conteste. En una evidencia "
        "eso es peligroso: una respuesta por defecto que nadie toca parece contestada",
    }

# ------------------------------------- una sola forma por proposito
#
# Cada entrada es un proposito donde habia dos caminos. Se eligio uno; el otro NO
# se implementa aunque aparezca mencionado en documentos anteriores.
#
# (proposito, se_usa, se_descarta, por_que)
#
# Por que existe
# --------------
# Con siete documentos de contexto, once rondas de revision y tres actas, el
# riesgo real no es equivocarse: es proponer DOS mecanismos para lo mismo y que
# alguien implemente los dos. Ya paso -Requiere_Repuesto y MotivoPendienteID
# registraban el mismo hecho- y el manual describia un bypass de GPS por nota
# libre mientras el modelo tenia CierreConExcepcion.
#
# verificar_documentos.py falla si un mecanismo descartado reaparece en MODELO.
DECISIONES = [
    ("Periodicidad de un trabajo",
     "TAR_Tareas.FrecuenciaID", "ACT_Activos.FrecuenciaID",
     "Un poste SOS tiene tarea semanal, mensual y trimestral",
     "se retira con ESPEC-003, revisar antes del 2026-08-31"),
    ("Que checklist se abre",
     "TAR_Tareas.FormularioID", "TIP_TiposActivo.FormularioID",
     "El formulario es de la tarea. La columna vieja llevaba 18 formulas de hoja",
     "se retira con ESPEC-003, revisar antes del 2026-08-31"),
    ("Donde trabaja un usuario",
     "ASG_AsignacionZona.UnidadFuncionalID", "USR_Usuarios.SedeID",
     "La sede es un edificio; la asignacion es un tramo. RETIRADA el 2026-08-10", ""),
    ("Cierre sin GPS valido",
     "MAN_Mantenimientos.CierreConExcepcion", "Nota libre en Observaciones",
     "Una excepcion tiene que ser contable y auditable, no un texto"),
    ("Que hizo falta un repuesto",
     "MAN_Mantenimientos.MotivoPendienteID", "MAN_Mantenimientos.Requiere_Repuesto",
     "Dos sitios que dicen lo mismo permiten decir cosas distintas"),
    ("Que se hizo en una preventiva",
     "CHD_ChecklistDetalle", "MAN_Mantenimientos.Trabajo_Realizado",
     "El checklist ES la descripcion, item por item"),
    ("Que se reparo en una correctiva",
     "Formulario propio de correctivo", "MAN_Mantenimientos.Diagnostico",
     "Un formulario no duplica columnas y encaja en la capa de tareas"),
    ("Cuanto duro",
     "FechaHoraInicio y FechaHoraFin", "MAN_Mantenimientos.Duracion_Minutos",
     "Un dato derivable no se guarda"),
    ("Coordenada de un activo",
     "ACT_Activos.Ubicacion", "Latitud y Longitud separadas",
     "AppSheet trata LatLong como un tipo, y DISTANCE() lo exige"),
    ("Preguntas de inspeccion",
     "FRM_Preguntas", "CHD_ChecklistDetalle",
     "CHD guarda RESPUESTAS. Editarlo para cambiar preguntas corrompe el historico"),
    ("Tiempo de reloj parado",
     "PAU_Pausas con SUM()", "Columna acumulada",
     "Un acumulado compite consigo mismo sin senal"),
    ("Marca de tiempo que sirve de prueba",
     "ChangeTimestamp en la transicion de estado", "Initial value = NOW()",
     "Un Initial value ES editable, y NOW() es el reloj del telefono"),
    ("Catalogo de roles",
     "ROL_Roles", "Crear una tabla nueva de roles",
     "Ya existe en MODELO. Falta poblarla con los doce del Plan Maestro"),
]

# Sin resolver. Estan aqui para que no se decidan dos veces en sitios distintos.
DECISIONES_ABIERTAS = [
    ("Activos sin ubicacion fisica -SSL, licencias, antivirus, ISP, radios-",
     "Camino sin evidencia de coordenada, o fuera del alcance del sistema"),
    ("Que hace falta volver",
     "MAN.RequiereSegundaVisita, o OT.OTOrigenID encadenando una orden nueva"),
]

# --------------------------------------------------------- reglas de la app
REGLAS = [
    dict(id="RG-01", tabla="MAN_Mantenimientos", columna="Coordenadas_Cierre",
         tipo="Valid_If", cubre="RF-012",
         expresion="DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]",
         descripcion=("Impide cerrar lejos del activo, con radio por tipo. La ruta atraviesa dos "
                      "referencias, de ahi que cablearlas sea el primer paso de todo.")),
    dict(id="RG-21", tabla="ACT_Activos", columna="UnidadFuncionalID",
         tipo="Valid_If", cubre="RF-002",
         expresion='OR(ISBLANK([SedeID]), [UnidadFuncionalID] = [SedeID].[UnidadFuncionalID])',
         descripcion=("El equipo bajo techo hereda donde esta de su edificacion. Sin esta regla "
                      "la unidad funcional se guardaria en dos sitios -en el activo y en su "
                      "sede- y podrian decir cosas distintas sin que nada protestara. Con ella "
                      "hay un solo sitio donde mirar: si el activo tiene sede, manda la sede.")),
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
    dict(id="RG-20", tabla="MAN_Mantenimientos", columna="(varias)",
         tipo="Editable_If", cubre="Prueba de presencia",
         expresion="FALSE",
         descripcion=("Sobre Coordenadas_Cierre, Precision_GPS, UbicacionEscaneo y "
                      "FechaHoraEscaneo. SIN ESTO EL GEOFENCING ES DECORATIVO: HERE() y "
                      "USERLOCATIONACCURACY() son Initial value, no App formula, y un Initial "
                      "value SI es editable. Coordenadas_Cierre es un LatLong, que en un "
                      "formulario AppSheet dibuja como un pin arrastrable sobre un mapa, y la "
                      "ubicacion del activo esta visible en la app: el tecnico arrastra el pin "
                      "encima del activo y RG-01 valida sin protestar. La regla se cumplia y la "
                      "presencia no quedaba probada.")),
    dict(id="RG-19", tabla="MAN_Mantenimientos", columna="CierreConExcepcion",
         tipo="App formula", cubre="D-04",
         expresion=('OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), '
                    '[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))'),
         descripcion=("Marca el cierre como excepcional cuando el error del satelite supera el "
                      "umbral. Sin ella la columna existe y nadie la puebla: un cierre con 45 m de "
                      "error seria indistinguible de uno con 8 m, y ahi se cae la cadena de "
                      "evidencia. EL UMBRAL ES UN PARAMETRO, no un numero en la expresion: se "
                      "calibra con las pruebas de campo y lo ajusta el administrador en una celda, "
                      "sin abrir el editor. FALLA DE FORMA RUIDOSA: si el umbral no se puede "
                      "leer, el OR con ISBLANK marca el cierre COMO EXCEPCIONAL. Sin eso, borrar la "
                      "fila del parametro haria que todos los cierres saliesen limpios y nadie se "
                      "enterase, que es la forma exacta del defecto de RG-16. Provisional 40 m, "
                      "unas ocho veces la precision "
                      "tipica de un movil a cielo abierto (4,9 m segun GPS.gov) y deja margen para "
                      "montana y estructuras. D-04 decia 50; se baja a 40 tras comprobar que 45 m "
                      "ya es nueve veces la norma.")),
    dict(id="RG-16", tabla="ACT_Activos", columna="Activo",
         tipo="App formula", cubre="Baja de activos",
         expresion='[EstadoActivoID].[Nombre] <> "Retirado"',
         descripcion=("La bandera se deriva del estado, no se edita. La comparacion va contra "
                      "[Nombre] y NO contra la columna a secas: EstadoActivoID es un Ref y un Ref "
                      "guarda la CLAVE del destino, que aqui vale 1 a 4. Comparar la clave con la "
                      "cadena 'Retirado' es siempre cierto, y como esto es una App formula, "
                      "ESCRIBE: pondria Activo=TRUE sobre el activo dado de baja. EST_Activo ya tiene el estado "
                      "Retirado; mantener ademas una bandera independiente es el mismo dato en dos "
                      "sitios, y algun dia diran cosas distintas sin forma de saber cual miente.")),
    dict(id="RG-17", tabla="ACT_Activos", columna="FechaBaja",
         tipo="Required_If", cubre="Baja de activos",
         expresion='[EstadoActivoID].[Nombre] = "Retirado"',
         descripcion=("Contra [Nombre], no contra la clave. Si se retira un activo hay que decir cuando. Un historico que no puede "
                      "explicar por que un activo dejo de recibir mantenimiento no es defendible.")),
    dict(id="RG-18", tabla="ACT_Activos", columna="(tabla)",
         tipo="Doctrina de reportes", cubre="Baja de activos",
         expresion='Ver descripcion: es una prohibicion, no una expresion a configurar',
         descripcion=("NO filtrar los reportes historicos por la bandera Activo del activo padre. "
                      "Un reporte HISTORICO filtra por la fecha y el estado de la TRANSACCION, "
                      "nunca por el estado actual del activo padre. Filtrar por [ActivoID].[Activo] "
                      "hace que al dar de baja un activo desaparezcan retroactivamente todos sus "
                      "mantenimientos pasados: el informe del ano anterior cambia solo y muestra "
                      "menos trabajo del que se hizo. Ante interventoria eso no parece un filtro "
                      "mal puesto, parece que el mantenimiento nunca se ejecuto.")),
    dict(id="RG-14", tabla="OT_OrdenesTrabajo", columna="(tabla)",
         tipo="Are updates allowed", cubre="Evidencia defendible",
         expresion="Updates, Adds",
         descripcion=("Se retira Deletes. Una orden no se borra: se anula con Activo = FALSE, que "
                      "deja traza de que existio. Si el boton no esta, no hay accidente posible.")),
    dict(id="RG-15", tabla="MAN_Mantenimientos", columna="(tabla)",
         tipo="Are updates allowed", cubre="Evidencia defendible",
         expresion="Updates, Adds",
         descripcion=("Se retira Deletes. Es la decision central del sistema: la ejecucion es la "
                      "prueba de que alguien estuvo frente al equipo. Protegido aqui arriba, el "
                      "IsPartOf de FOT, FIR y CHK nunca llega a dispararse. Nota: esto protege "
                      "DENTRO de la app; nadie impide borrar la fila a mano en el Sheets, donde "
                      "hay dos cuentas con permiso de edicion.")),
    dict(id="RG-10", tabla="MAN_Mantenimientos", columna="(tabla)",
         tipo="Bot", cubre="D-07",
         expresion='[RequiereSegundaVisita] = TRUE',
         descripcion="Genera una orden de seguimiento enlazada a la original mediante OTOrigenID."),
]
