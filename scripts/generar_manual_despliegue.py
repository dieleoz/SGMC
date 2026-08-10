# -*- coding: utf-8 -*-
"""Genera docs/MANUAL_DESPLIEGUE.md desde el modelo.

Es el manual que se entrega a quien construye la aplicacion en AppSheet. Se
genera para que sus listas no puedan desviarse del modelo: las 28 tablas, las
28 claves, las 38 referencias y las 20 reglas salen de modelo_objetivo.py.

Esta escrito por ROL, no por persona, para poder replicarlo en otro contrato.

Uso:  python scripts/generar_manual_despliegue.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from modelo_objetivo import (MODELO, REGLAS, RETIRADAS, CLAVE_GENERADA,
                             CAMPOS_RETIRADOS, COLUMNAS_SIN_DECIDIR)

# Orden de construccion. Cada nivel solo referencia tablas de niveles anteriores
# o del suyo propio con el destino antes. Verificado topologicamente.
NIVELES = [
    ("1. Catalogos", ["ROL_Roles", "SED_Sedes", "UNF_UnidadesFuncionales", "CAL_Calzadas",
                      "SEN_Sentidos", "FRE_Frecuencias", "EST_Activo", "EOT_EstadosOrden",
                      "MOT_MotivosPendiente", "TPR_TiposRespuesta", "PAR_Parametros"]),
    ("2. Formularios", ["FRM_Formularios", "FRM_Secciones", "FRM_Preguntas", "LST_ValoresLista"]),
    ("3. Maestras", ["TIP_TiposActivo", "USR_Usuarios", "ASG_AsignacionZona", "FAL_ModosFalla"]),
    ("4. Activos", ["ACT_Activos"]),
    ("5. Ordenes", ["OT_OrdenesTrabajo", "PLA_PlanMantenimiento", "NOV_Novedades"]),
    ("6. Ejecucion", ["MAN_Mantenimientos", "CHK_Checklists", "CHD_ChecklistDetalle",
                      "FOT_Fotografias", "FIR_Firmas"]),
]

# Tipos que AppSheet no infiere desde una hoja de texto.
TIPOS_MANUALES = [
    ("ACT_Activos", "Ubicacion", "LatLong", "Sobre ella se calcula la distancia al activo"),
    ("ACT_Activos", "FechaBaja", "Date", ""),
    ("ACT_Activos", "Activo", "Yes/No", ""),
    ("MAN_Mantenimientos", "Coordenadas_Cierre", "LatLong", "**La mas importante.** DISTANCE() no funciona sobre texto"),
    ("MAN_Mantenimientos", "UbicacionEscaneo", "LatLong", ""),
    ("MAN_Mantenimientos", "Precision_GPS", "Number", ""),
    ("MAN_Mantenimientos", "CierreConExcepcion", "Yes/No", ""),
    ("MAN_Mantenimientos", "OrigenApertura", "Enum", "Valores: `QR`, `Lista`"),
    ("OT_OrdenesTrabajo", "Tipo", "Enum", "Valores: `Preventivo`, `Correctivo`"),
    ("FOT_Fotografias", "Ubicacion", "LatLong", ""),
    ("FOT_Fotografias", "Archivo", "Image", ""),
    ("FIR_Firmas", "Imagen", "Signature", ""),
    ("NOV_Novedades", "Ubicacion", "LatLong", ""),
    ("NOV_Novedades", "Fotografia", "Image", ""),
    ("MAN_Mantenimientos", "FechaHoraRegistro", "ChangeTimestamp", "**Marca del servidor.** AppSheet no lo infiere nunca"),
    ("FOT_Fotografias", "FechaHora", "ChangeTimestamp", "**Sin esto la hora de la fotografia no prueba nada**"),
    ("FIR_Firmas", "FechaHora", "ChangeTimestamp", "Idem para la firma"),
    ("NOV_Novedades", "FechaHora", "ChangeTimestamp", ""),
]

# Columnas muertas que siguen en la hoja y se llaman igual que la clave de otra
# tabla. AppSheet infiere referencias por coincidencia de nombre y las convierte
# sola. Descubierto el 2026-08-09.
TRAMPAS = [
    ("CHK_Checklists", "ActivoID", "ACT_Activos", "El checklist cuelga del mantenimiento, no del activo"),
    ("CHD_ChecklistDetalle", "TipoRespuestaID", "TPR_TiposRespuesta", "El tipo de respuesta lo da la pregunta"),
    ("OT_OrdenesTrabajo", "FormularioID", "FRM_Formularios", "El formulario lo determina el tipo del activo"),
]

L = []
w = L.append

w("# Manual de despliegue — SGMC sobre AppSheet")
w("")
w("**Para quien construye la aplicacion.** De cero a desplegada.")
w("")
w("> **Manual por rol, no por persona.** Quien lo ejecuta es el **Funcional**: perfil que configura")
w("> AppSheet, sin necesidad de programar. Escrito para poder replicarlo en otro contrato.")
w("")
w("| | |")
w("|---|---|")
w("| Sistema | Gestion de Mantenimiento en Campo |")
w("| Plataforma | Google AppSheet sobre Google Sheets |")
w("| Fuente del modelo | `scripts/modelo_objetivo.py`. Este manual se genera de ahi |")
w("| Tablas | **%d** |" % len(MODELO))
w("| Referencias | **%d** |" % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("| Reglas | **%d** |" % len(REGLAS))
w("")
w("## Por que este manual existe")
w("")
w("La primera version de esta aplicacion se construyo, y despues el modelo de datos se corrigio **en")
w("la hoja**: columnas renombradas, tablas nuevas, campos retirados. **No hubo forma de que AppSheet")
w("lo recogiera.**")
w("")
w("Dos limites de la plataforma, los dos verificados, explican por que:")
w("")
w("**`Regenerate` fusiona, no reemplaza.** Su documentacion dice que combina la informacion nueva con")
w("la existente e intenta mantener las columnas que ya estan. Sirve para anadir una columna; con un")
w("esquema muy divergente **impide converger**. El propio AppSheet indica la salida: *Delete and")
w("re-add the table*.")
w("")
w("**AppSheet ignora las pestanas ocultas, y no avisa.** Ocho pestanas del libro estaban ocultas y")
w("cargaban 24 tablas de 32, sin un solo mensaje.")
w("")
w("**Por debajo de cierto umbral se repara; por encima se reconstruye.** Este manual es el camino de")
w("reconstruir, que resulto ser mas rapido y mas limpio.")
w("")
w("---")
w("")
w("## Paso 0 — Antes de abrir AppSheet")
w("")
w("**Comprobar la hoja.** Si algo esta mal aqui, todo lo demas hereda el error.")
w("")
w("```bash")
w('python scripts/verificar_faseA.py "BD/<archivo>.xlsx"')
w("```")
w("")
w("Tiene que decir **`FASE A CERRADA`**. Si dice otra cosa, no siga.")
w("")
w("**Y mirar las pestanas ocultas**, que es lo que mas cuesta descubrir despues:")
w("")
w("```bash")
w('python -c "import openpyxl;wb=openpyxl.load_workbook(\'BD/<archivo>.xlsx\',read_only=True);'
  'print([n for n in wb.sheetnames if wb[n].sheet_state!=\'visible\'])"')
w("```")
w("")
w("Tiene que devolver **una lista vacia**. Si hay pestanas ocultas, mostrarlas en Google Sheets —")
w("*Ver → Hojas ocultas*— antes de continuar. **`F-18` de la verificacion tambien lo detecta.**")
w("")
w("## Paso 1 — Crear la aplicacion")
w("")
w("En AppSheet: **Create → App → Start with existing data**, y elegir el Google Sheets.")
w("")
w("**Fuente: el documento de Google Sheets, no un archivo subido.** Si se sube un `.xlsx`, la")
w("aplicacion queda leyendo una foto fija y nada se sincroniza.")
w("")
w("**Quien crea la aplicacion es su propietario.** Conviene que sea la cuenta que va a operarla: un")
w("coautor no puede dar de alta tablas, y todo este manual consiste en eso.")
w("")
w("## Paso 2 — Dar de alta las %d tablas" % len(MODELO))
w("")
w("*Data → `+` → Add data*, una por una. **En este orden**, que no es alfabetico: cada nivel apunta a")
w("tablas cuyas claves quedaron fijadas antes.")
w("")
for nombre, tablas in NIVELES:
    presentes = [t for t in tablas if t in MODELO]
    w("**%s**" % nombre)
    w("")
    w("```")
    for i in range(0, len(presentes), 3):
        w("  " + " · ".join("%-24s" % t for t in presentes[i:i+3]).rstrip())
    w("```")
    w("")
w("### Las que NO se dan de alta")
w("")
w("Estan en la hoja y el modelo las retira:")
w("")
w("| Pestana | Por que |")
w("|---|---|")
for t, motivo in sorted(RETIRADAS.items()):
    w("| `%s` | %s |" % (t, motivo))
w("")
w("**No borre esas pestanas de la hoja.** Tres de ellas guardan bancos de preguntas que todavia no se")
w("han migrado.")
w("")
w("## Paso 3 — Las claves, todas `Text`")
w("")
w("*Data → Columns* de cada tabla. **Una sola casilla `KEY`**, sobre la columna correcta, tipo")
w("**`Text`**.")
w("")
w("| Tabla | Clave |")
w("|---|---|")
for t, d in sorted(MODELO.items()):
    pk = [c["nombre"] for c in d["columnas"] if c.get("pk")]
    if pk:
        w("| `%s` | `%s` |" % (t, pk[0]))
w("")
w("**`Text` sin excepcion, y hay un caso que lo justifica.** `USR_Usuarios.UsuarioID` tiene un valor")
w("alfanumerico entre otros numericos. Si AppSheet infiere `Number`, esa fila se queda sin clave")
w("valida y ese usuario **deja de existir para el sistema**.")
w("")
w("**Si ve dos casillas `KEY` marcadas, o la clave aparece como combinacion de dos columnas,")
w("corrijalo antes de seguir.** Contra una clave compuesta no resuelve ninguna referencia, y el")
w("sintoma es que falla todo el paso 5 sin decir por que.")
w("")
w("### Clave automatica para las filas nuevas")
w("")
w("Estas %d tablas crean filas desde la aplicacion. Sin esto, no sabe que identificador poner:" % len(CLAVE_GENERADA))
w("")
w("| Tabla | Columna | `Initial value` |")
w("|---|---|---|")
for t in sorted(CLAVE_GENERADA):
    pk = [c["nombre"] for c in MODELO[t]["columnas"] if c.get("pk")]
    if pk:
        w("| `%s` | `%s` | `UNIQUEID()` |" % (t, pk[0]))
w("")
w("## Paso 4 — Los tipos que AppSheet no adivina")
w("")
w("Todo llega de una hoja, asi que entra como texto o numero.")
w("")
w("| Tabla | Columna | Tipo | |")
w("|---|---|---|---|")
for t, c, tipo, nota in TIPOS_MANUALES:
    w("| `%s` | `%s` | `%s` | %s |" % (t, c, tipo, nota))
w("")
w("## Paso 5 — Las %d referencias" % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("")
w("> **Cuidado con las listas de otros documentos.** `ESPEC-002` lista **15**, y es correcto para lo")
w("> que norma: convertir una aplicacion existente donde otras 23 ya estaban puestas. **Construyendo")
w("> desde cero no sobrevive ninguna.** Si al terminar cuenta 15, siguio la lista equivocada.")
w("")
w("Una referencia de AppSheet **guarda el valor de la clave de la tabla destino**. De ahi que el orden")
w("importe: primero la clave del destino, despues quien la apunta.")
w("")
n = 0
for nombre, tablas in NIVELES:
    refs = [(t, c) for t in tablas if t in MODELO
            for c in MODELO[t]["columnas"] if c.get("ref")]
    if not refs:
        continue
    w("**%s**" % nombre)
    w("")
    w("```")
    for t, c in refs:
        n += 1
        marca = "   IsPartOf = TRUE" if c.get("es_parte_de") else ""
        w("%2d  %-34s -> %s%s" % (n, t + "." + c["nombre"], c["ref"], marca))
    w("```")
    w("")
w("**Nota sobre `OT_OrdenesTrabajo.OTOrigenID`**, que sale en el nivel 5: apunta a su propia tabla,")
w("para encadenar una orden derivada con la que la origino. **Dejela para el final del nivel.**")
w("")
w("### `IsPartOf` va marcado en cuatro, y en ninguna mas")
w("")
w("```")
for t, d in MODELO.items():
    for c in d["columnas"]:
        if c.get("es_parte_de"):
            w("%-34s -> %s" % (t + "." + c["nombre"], c["ref"]))
w("```")
w("")
w("**`MAN_Mantenimientos.OTID` va DESMARCADO, y es deliberado.** Con `IsPartOf`, borrar una orden")
w("borraria su ejecucion, sus fotografias y su firma **en cascada**. En un sistema cuyo proposito es")
w("que la evidencia sea dificil de falsificar, eso se decide, no se hereda de un ejemplo.")
w("")
w("### Despues de cada conversion")
w("")
w("**Mire si aparecieron celdas en blanco donde habia valores.** Convertir a `Ref` conserva solo las")
w("filas cuyo valor coincide con la clave del destino; las demas quedan huerfanas **sin mensaje de")
w("error**.")
w("")
w("## Paso 6 — Tres columnas que AppSheet convierte solo, y estan mal")
w("")
w("Son columnas muertas que siguen en la hoja **y se llaman igual que la clave de otra tabla**.")
w("AppSheet infiere referencias por coincidencia de nombre, asi que las convierte sin que nadie se lo")
w("pida.")
w("")
_cl = {}
for _t, _d in MODELO.items():
    for _c in _d["columnas"]:
        if _c.get("pk"):
            _cl[_c["nombre"]] = _t
_trampas = [(t, c, _cl[c], campos[c])
            for t, campos in sorted(CAMPOS_RETIRADOS.items())
            for c in sorted(campos) if c in _cl and _cl[c] != t]
w("| Tabla | Columna | Adonde apunta sola | Por que esta mal |")
w("|---|---|---|---|")
for t, c, destino, motivo in _trampas:
    w("| `%s` | `%s` | `%s` | %s |" % (t, c, destino, motivo))
w("")
w("**Son %d, derivadas del archivo y no escritas a mano.** Estan tambien en la ficha de cada tabla," % len(_trampas))
w("marcadas como TRAMPA.")
w("")
w("**Dejelas en `Text` y desmarque `Show?`.** Si se quedan como `Ref`, dibujan rutas de navegacion")
w("que el modelo prohibe y aparecen en la aplicacion como si fueran buenas.")
w("")
w("Un aviso del tipo *was set to be unsearchable because it is Hidden* es **normal**: confirma que la")
w("columna quedo oculta.")
w("")
w("## Paso 7 — Las reglas")
w("")
w("Las %d del modelo. Las expresiones completas estan en" % len(REGLAS))
w("[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) §2.")
w("")
w("| # | Tabla | Columna | Tipo |")
w("|---|---|---|---|")
for r in REGLAS:
    w("| %s | `%s` | `%s` | %s |" % (r.get("id", ""), r.get("tabla", ""),
                                     r.get("columna", "(tabla)"), r.get("tipo", "")))
w("")
w("### Las cuatro que no pueden faltar")
w("")
w("**Geofencing** — en `MAN_Mantenimientos.Coordenadas_Cierre`:")
w("")
w("```")
w("Initial value:  HERE()")
w("Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= 1.0")
w("Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.")
w("Editable_If:    FALSE")
w("```")
w("")
w("**El `1.0` es literal a proposito.** El modelo preve un radio por tipo de activo, pero esa columna")
w("esta vacia en los 18 tipos: la version por tipo comparia contra una celda en blanco y **rechazaria")
w("tambien los cierres legitimos**.")
w("")
w("**No editables** — en `MAN_Mantenimientos`, `Editable_If = FALSE` en las cuatro columnas de")
w("captura:")
w("")
w("```")
w("Coordenadas_Cierre · Precision_GPS · UbicacionEscaneo · FechaHoraEscaneo")
w("```")
w("")
w("**Sin esto el geofencing es decorativo:** el tecnico arrastra el pin del mapa y cierra desde donde")
w("quiera. La regla parece funcionar y no prueba nada.")
w("")
w("> **Supuesto sin verificar, y es el peor modo de fallo del sistema.** No hay pagina oficial que")
w("> confirme si AppSheet evalua un `Valid_If` sobre una columna con `Editable_If = FALSE`. **Si no lo")
w("> evalua, la regla parece funcionar por no ejercitarse nunca.** Se detecta asi: pruebe un cierre")
w("> cercano y uno lejano. **Si los dos salen aceptados, sospeche de esto antes que del radio.**")
w("")
w("**Excepcion por GPS deficiente** — en `MAN_Mantenimientos.CierreConExcepcion`:")
w("")
w("```")
w('App formula:')
w('OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")),')
w('   [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))')
w("```")
w("")
w("**El `ISBLANK` no sobra.** Sin el, borrar la fila del parametro hace que **todos los cierres")
w("salgan limpios y nadie se entere**. Con el, si el umbral no se puede leer el cierre se marca como")
w("excepcional: falla hacia el lado seguro. Es la forma exacta del defecto de RG-16.")
w("")
w("```")
w("```")
w("")
w("**Filtros de seguridad** — *Data → Tables → [tabla] → Security Filter*:")
w("")
w("```")
w("ACT_Activos:")
w("IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID],")
w("   AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))")
w("")
w("OT_OrdenesTrabajo:")
w("OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())")
w("```")
w("")
w("**No son solo control de acceso: son rendimiento.** Sin ellos, cada tecnico se descarga el")
w("inventario entero al telefono.")
w("")
w("### Retirar el borrado — sin esto el `IsPartOf` es peligroso")
w("")
w("*Data → Tables → [tabla] → Are updates allowed*:")
w("")
w("```")
w("OT_OrdenesTrabajo    Updates si · Adds si · Deletes NO")
w("MAN_Mantenimientos   Updates si · Adds si · Deletes NO")
w("```")
w("")
w("**Es la otra mitad del paso 5.** Marcar `IsPartOf` en cuatro referencias crea **borrado en")
w("cascada**: borrar un mantenimiento se lleva sus fotografias, su firma y su checklist.")
w("")
w("Eso solo es seguro **porque el mantenimiento nunca se borra**, y eso es exactamente lo que hace")
w("quitar `Deletes`. Configurar el `IsPartOf` sin esto deja la cascada abierta.")
w("")
w("## Paso 8 — Las vistas")
w("")
w("**La mayor parte se construye sola al poner las referencias.** AppSheet crea las columnas")
w("virtuales `Related ...` y con ellas la navegacion padre-hijo: al abrir un mantenimiento se ven sus")
w("fotografias y su firma; al abrir un activo, sus ordenes.")
w("")
w("Lo que hay que configurar a mano son las vistas principales:")
w("")
w("| Vista | Tipo | Sobre | Nota |")
w("|---|---|---|---|")
w("| Mapa de activos | `Map` | `ACT_Activos` | Columna de mapa: `Ubicacion` |")
w("| Mis ordenes | `Deck` | `OT_OrdenesTrabajo` | Es la pantalla de trabajo del tecnico |")
w("| Mantenimientos | `Table` | `MAN_Mantenimientos` | |")
w("")
w("## Paso 9 — Verificar antes de publicar")
w("")
w("**No lo de por cerrado usted.** Este proyecto tiene tres cierres reportados que no resistieron la")
w("comprobacion contra el archivo, y las tres veces lo paro un script.")
w("")
w("**La cadena navega** — en el Asistente de Expresiones, sobre `MAN_Mantenimientos`:")
w("")
w("```")
w("[OTID].[ActivoID].[Ubicacion]")
w("[OTID].[TecnicoID].[Correo]")
w("```")
w("")
w("Las dos en verde. Si la primera falla, casi siempre es `OT_OrdenesTrabajo.ActivoID`, que la lista")
w("antigua de 15 no incluia.")
w("")
w("**Cuente las referencias.** Las columnas de tipo `Ref` deben sumar **%d**."
  % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("")
w("**Y los tres verificadores del repositorio:**")
w("")
w("```bash")
w("python scripts/validar_modelo.py          # el modelo consigo mismo")
w('python scripts/verificar_faseA.py "..."   # el modelo contra la hoja')
w("python scripts/verificar_documentos.py    # la prosa contra el modelo")
w("```")
w("")
w("**Ninguno mira la aplicacion.** Para eso estan las pruebas de aceptacion de")
w("[`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).")
w("")
w("## Paso 10 — Publicar")
w("")
w("> **Antes de publicar, lea esto.** Los 34 activos de la hoja comparten **una sola coordenada**,")
w("> `4.728512, -74.114531`, que esta en Bogota y no en el corredor. Con el radio de 1 km, la")
w("> aplicacion **rechaza todo cierre hecho en via y acepta todo cierre hecho en Bogota**.")
w(">")
w("> **No es un defecto de la configuracion: faltan las coordenadas reales**, que es la decision")
w("> D-01. Publicar antes de cargarlas entrega un sistema donde ningun tecnico puede cerrar una")
w("> orden, y se descubre con el tecnico delante.")
w("")
w("*Manage → Deploy → Run deployment check*, y despues **Move app to Deployed state**.")
w("")
w("**Antes de publicar, si existe una aplicacion anterior sobre la misma hoja, despubliquela.** Dos")
w("aplicaciones sobre un backend sin integridad referencial es una fuente de corrupcion silenciosa:")
w("la vieja conserva permisos de anadir y borrar que el modelo nuevo ya no concede.")
w("")
w("## Reversion — hasta donde se puede volver atras")
w("")
w("**Todo lo anterior al paso 10 se puede abandonar sin coste.** La aplicacion no esta publicada y")
w("nadie la usa: se borra y se empieza de nuevo. La hoja no se toca en ningun paso salvo el 0.")
w("")
w("**El paso 0 SI escribe en la hoja** al mostrar las pestanas ocultas. Antes de empezar, haga una")
w("copia fechada del documento. Es el unico punto de restauracion del dato.")
w("")
w("**El punto de no retorno es el paso 10**, y no por publicar: por **despublicar la aplicacion")
w("anterior**. Si el *deployment check* falla despues, la vieja ya no esta en servicio. Compruebe")
w("todo el paso 9 **antes** de despublicar nada.")
w("")
w("## Lo que NO cabe en el plan gratuito")
w("")
w("No es *mas adelante*: es **no en este plan**. Solo cambia con la decision de licenciamiento.")
w("")
w("| Lo que se querria | Por que no |")
w("|---|---|")
w("| Generacion automatica de las ordenes del mes | Los procesos programados no se ejecutan |")
w("| Aviso al supervisor de que hay trabajo por recibir | Lo mismo |")
w("| Integracion con sistemas externos | Sin plan Core no hay API REST |")
w("| Atributos distintos por tipo de equipo | El backend es una hoja: no hay esquema dinamico |")
w("| Que una escritura directa en la hoja respete las validaciones | Imposible por diseno |")
w("")
w("**Ese ultimo importa mas de lo que parece.** Todas las garantias del sistema viven en la capa de")
w("aplicacion. Quien escriba en la hoja se las salta todas. Lo que el sistema puede ofrecer es que")
w("falsificar cueste mas que hacer el trabajo, no que sea imposible.")
w("")
w("---")
w("*Generado de `scripts/modelo_objetivo.py` por `scripts/generar_manual_despliegue.py`.*")
w("*Para actualizarlo, cambie el modelo y vuelva a generar.*")


# ------------------------------------------------------------------ ANEXO
_claves = {}
for _t, _d in MODELO.items():
    for _c in _d["columnas"]:
        if _c.get("pk"):
            _claves[_c["nombre"]] = _t

w("---")
w("")
w("# Anexo — Ficha de cada tabla")
w("")
w("**Columna por columna, sin nada que deducir.** Esta es la referencia contra la que se configura y")
w("contra la que se valida. Si una columna no aparece aqui, no deberia estar visible en la app.")
w("")
w("Leyenda:")
w("")
w("- **CLAVE** — casilla `KEY` marcada, tipo `Text`")
w("- **`Ref` -> Tabla** — tipo `Ref` con esa tabla como *Source table*")
w("- **IsPartOf** — ademas, casilla `Is a part of` marcada")
w("- **OCULTAR** — retirada del modelo: tipo `Text`, `Show?` desmarcado, sin formula")
w("- **TRAMPA** — AppSheet la convierte a `Ref` sola por coincidencia de nombre. **Deshagalo**")
w("- **SIN DECIDIR** — esta en la hoja y el modelo no la declara")
w("")

for tabla in sorted(MODELO):
    d = MODELO[tabla]
    w("## `%s`" % tabla)
    w("")
    w(d["proposito"])
    w("")
    w("| Columna | Tipo | Que hacer |")
    w("|---|---|---|")
    for c in d["columnas"]:
        acc = []
        if c.get("pk"):
            acc.append("**CLAVE**")
        if c.get("ref"):
            acc.append("`Ref` -> `%s`" % c["ref"])
            acc.append("**IsPartOf**" if c.get("es_parte_de") else "IsPartOf desmarcado")
        if c["tipo"] == "Enum" and c.get("nota"):
            acc.append("Valores: " + " · ".join("`%s`" % v.strip() for v in c["nota"].split(",")))
        if c.get("valor_inicial"):
            acc.append("`Initial value` = `%s`" % c["valor_inicial"])
        w("| `%s` | `%s` | %s |" % (c["nombre"], c["tipo"], " · ".join(acc)))
    ret = CAMPOS_RETIRADOS.get(tabla, {})
    sind = [c for (t2, c) in COLUMNAS_SIN_DECIDIR if t2 == tabla]
    if ret or sind:
        w("")
        w("**Y estas, que estan en la hoja y NO se usan:**")
        w("")
        w("| Columna | Que hacer | Por que |")
        w("|---|---|---|")
        for c, motivo in sorted(ret.items()):
            tr = " · **TRAMPA: AppSheet la pone `Ref` sola hacia `%s`**" % _claves[c] if c in _claves else ""
            w("| `%s` | **OCULTAR**%s | %s |" % (c, tr, motivo))
        for c in sorted(sind):
            w("| `%s` | **OCULTAR** · SIN DECIDIR | El modelo no la declara |" % c)
    w("")

salida = os.path.join(RAIZ, "docs", "MANUAL_DESPLIEGUE.md")
with open(salida, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

refs = sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref"))
print("Generado:", salida)
print("%d tablas, %d referencias, %d reglas, %d claves generadas"
      % (len(MODELO), refs, len(REGLAS), len(CLAVE_GENERADA)))
