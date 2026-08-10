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
import modelo_objetivo
from modelo_objetivo import (MODELO, REGLAS, RETIRADAS, CLAVE_GENERADA,
                             CAMPOS_RETIRADOS, COLUMNAS_SIN_DECIDIR)

# El modelo describe datos, no interfaz. Esto no se afirma de memoria: se
# comprueba. Si alguien declara vistas en el modelo, el manual deja de decir
# que no las hay en vez de quedarse mintiendo.
INTERFAZ = [n for n in ("VISTAS", "ACCIONES", "SLICES") if hasattr(modelo_objetivo, n)]

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

# Las columnas trampa NO se escriben a mano: se derivan mas abajo cruzando
# CAMPOS_RETIRADOS contra las claves del modelo. Una lista a mano aqui se
# desviaria del modelo en cuanto alguien lo edite.

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
w("### Las %d que el modelo retira" % len(RETIRADAS))
w("")
w("**Sobre la hoja vigente estas pestanas ya no existen.** La hoja se genera del modelo, asi que no")
w("aparecen en el desplegable y no hay nada que evitar. La lista se conserva para reconocerlas si")
w("alguien trabaja sobre una copia antigua:")
w("")
w("| Pestana | Por que se retiro |")
w("|---|---|")
for t, motivo in sorted(RETIRADAS.items()):
    w("| `%s` | %s |" % (t, motivo))
w("")
w("**No lo de por hecho: compruebelo contra el archivo.** Tiene que devolver una lista vacia.")
w("")
w("```bash")
w('python -c "import openpyxl;n=openpyxl.load_workbook(\'BD/Modelo_Datos_PLANTILLA.xlsx\','
  "read_only=True).sheetnames;print([t for t in %s if t in n])\"" % sorted(RETIRADAS))
w("```")
w("")
w("**Y los bancos de preguntas que guardaban tres de ellas ya estan migrados** a `FRM_Preguntas`, que")
w("es el motor unico. Se comprueba contando cuantos formularios distintos tienen preguntas:")
w("")
w("```bash")
w('python -c "import openpyxl;s=openpyxl.load_workbook(\'BD/Modelo_Datos_PLANTILLA.xlsx\','
  "read_only=True,data_only=True)['FRM_Preguntas'];f=[r[1] for r in s.iter_rows(min_row=2,values_only=True)];"
  'print(len(f),\'preguntas en\',len(set(f)),\'formularios\')"')
w("```")
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
w("## Paso 4 — Los tipos que AppSheet no adivina, y como comprobarlos")
w("")
w("**Subir el Excel arregla la hoja, no la aplicacion.** Son dos sitios distintos. El Excel")
w("fija que columnas hay y que datos tienen; **el tipo de cada columna vive en el esquema de")
w("AppSheet**, y ese se infiere. Reimportar no lo corrige: la inferencia vuelve a ser la misma")
w("sobre los mismos datos.")
w("")
w("**De donde sale la inferencia**, segun la documentacion oficial: AppSheet mira **el nombre")
w("de la cabecera Y el contenido de las filas**. Las palabras que disparan un tipo son")
w("concretas —`latlong` y `geolocation` para una coordenada, `birthday` o `day` para una fecha,")
w("una cabecera acabada en `?` para un Yes/No— y **ninguna de nuestras columnas las usa**. Ver")
w("`BASE_CONOCIMIENTO_APPSHEET.md` seccion 13.")
w("")
w("> **Y de ahi salen dos cosas que conviene tener claras.**")
w(">")
w("> **Ninguna de las referencias se creara sola.** AppSheet infiere `Ref` cuando el nombre de")
w("> una columna se parece al de otra tabla, y nuestras tablas llevan prefijo —`UNF_Unidades`")
w("> `Funcionales`, no `UnidadFuncional`—, asi que el parecido se rompe. Es el precio de la")
w("> convencion, y a la vez su proteccion: impide que AppSheet invente referencias.")
w(">")
w("> **Una columna de texto cuyos valores parecen numeros se tipara `Number`.** Paso el")
w("> 2026-08-10 con `SED_Sedes.TramoINVIAS`: el unico valor cargado era `5607`, asi que salio")
w("> `Number` — y los otros tramos del corredor son `55CN03`, que no cabe en un numero.")
w("")
w("**Como se comprueba, tabla por tabla.** Al terminar de dar de alta o de regenerar una tabla,")
w("abrela en *Data > Columns* y **recorre la columna TYPE de arriba abajo contra la ficha del")
w("anexo**. No es opcional ni es paranoia: el defecto no se ve en la hoja ni en los datos, solo")
w("en esta pantalla. Lo que se corrige aqui sobrevive a un `Regenerate` posterior, porque")
w("AppSheet conserva el tipo de las columnas que ya existen.")
w("")
w("**Los que siempre hay que poner a mano**, derivados del modelo:")
w("")
w("| Tabla | Columna | Tipo | |")
w("|---|---|---|---|")
for t, c, tipo, nota in TIPOS_MANUALES:
    w("| `%s` | `%s` | `%s` | %s |" % (t, c, tipo, nota))
w("")
w("## Paso 5 — Las %d referencias" % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("")
w("> **Cuidado con las listas de otros documentos.** Circulo una lista de **15** referencias por")
w("> convertir, y era correcta para lo que normaba: una aplicacion existente donde otras 23 ya estaban")
w("> puestas. Ese documento esta retirado. **Construyendo desde cero no sobrevive ninguna: son %d.**"
  % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("> Si al terminar cuenta 15, siguio la lista equivocada.")
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
w("## Paso 6 — RETIRADO. Sobre la hoja vigente no hay nada que deshacer")
w("")
w("> **No ejecute este paso.** Se conserva numerado para que quien tenga una copia antigua del manual")
w("> sepa que salio del plan, y para poder reconocer el problema si algun dia se trabaja sobre una")
w("> hoja heredada.")
w(">")
w("> Estas columnas **no existen en la hoja vigente**, que se genera del modelo, asi que AppSheet no")
w("> tiene nada que convertir solo. **Compruebelo usted, con la regla `F-19`:**")
w(">")
w("> ```bash")
w('> python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"')
w("> ```")
w(">")
w("> ```")
w("> ok Hoja limpia: ninguna de las %d columnas retiradas existe ya. No hay nada que ocultar"
  % sum(len(v) for v in CAMPOS_RETIRADOS.values()))
w("> ```")
w(">")
w("> **Lo mismo vale para las marcas `OCULTAR` y `TRAMPA` del anexo:** describen una hoja que ya no se")
w("> usa y no aplican a la vigente.")
w("")
w("El problema que este paso resolvia: son columnas muertas que **se llaman igual que la clave de otra")
w("tabla**. Donde existan, AppSheet infiere la referencia por coincidencia de nombre y las convierte")
w("sin que nadie se lo pida.")
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
w("marcadas como TRAMPA, **y esas marcas tampoco aplican a la hoja vigente**.")
w("")
w("Si alguna vez aparecen —trabajando sobre una copia antigua del libro—, lo que habria que hacer es")
w("dejarlas en `Text` y desmarcar `Show?`. Como `Ref` dibujan rutas de navegacion que el modelo")
w("prohibe y aparecen en la aplicacion como si fueran buenas.")
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
w("Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion])")
w("                  <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]")
w("Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.")
w("Editable_If:    FALSE")
w("```")
w("")
w("**El radio va por tipo de activo, no como literal.** Una subestacion y un poste SOS no admiten la")
w("misma tolerancia, y un tramo de fibra es lineal. `PAR_Parametros.RADIO_GEOFENCING_KM` queda como")
w("valor provisional historico: **la regla no lo lee.**")
w("")
w("**Antes de pegarla, compruebe que la columna esta poblada**, porque contra celdas en blanco esta")
w("expresion **rechaza tambien los cierres legitimos**:")
w("")
w("```bash")
w('python -c "import openpyxl;s=openpyxl.load_workbook(\'BD/Modelo_Datos_PLANTILLA.xlsx\','
  "read_only=True,data_only=True)['TIP_TiposActivo'];h=[c.value for c in next(s.iter_rows(max_row=1))];"
  "i=h.index('RadioGeofencingKm');v=[r[i] for r in s.iter_rows(min_row=2,values_only=True)];"
  'print(len(v),\'tipos,\',sum(1 for x in v if x not in (None,\'\')),\'con radio\')"')
w("```")
w("")
w("Sobre la hoja vigente devuelve **27 tipos, 27 con radio**. Si devuelve alguno sin radio, pare: ese")
w("tipo de activo no se podra cerrar en campo.")
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
w("**Este manual no especifica las vistas, y hay que saberlo antes de empezar el paso.** El modelo")
if INTERFAZ:
    w("declara ahora %s en `scripts/modelo_objetivo.py`: **actualice este generador**, porque el paso"
      % " y ".join("`%s`" % n for n in INTERFAZ))
    w("sigue escrito como si no existieran.")
else:
    w("declara datos, no interfaz: `VISTAS`, `ACCIONES` y `SLICES` **no existen** en")
    w("`scripts/modelo_objetivo.py` —comprobado al generar este manual, no de memoria—. Por eso aqui no")
    w("hay ficha columna por columna como en los pasos anteriores, y por eso lo que decida en este paso")
    w("es lo unico que no queda escrito en ninguna parte.")
w("")
w("**Lo unico que AppSheet crea solo son las columnas virtuales `Related ...`**, que aparecen al poner")
w("las referencias del paso 5 y traen con ellas la navegacion padre-hijo: al abrir un mantenimiento se")
w("ven sus fotografias y su firma; al abrir un activo, sus ordenes. **Eso es todo lo que se construye")
w("solo.** Las pantallas no.")
w("")
w("**Y no se configuran a ojo.** Las tres de abajo van con el tipo y la tabla que dice la ficha; si")
w("una no encaja, no la improvise: **anote que falta y siga**. Una vista inventada aqui es")
w("configuracion activa que nadie declaro y que el siguiente que reconstruya la aplicacion no podra")
w("reproducir.")
w("")
w("| Vista | Tipo | Sobre | Nota |")
w("|---|---|---|---|")
w("| Mapa de activos | `Map` | `ACT_Activos` | Columna de mapa: `Ubicacion` |")
w("| Mis ordenes | `Deck` | `OT_OrdenesTrabajo` | Es la pantalla de trabajo del tecnico |")
w("| Mantenimientos | `Table` | `MAN_Mantenimientos` | |")
w("")
w("**Anote lo que haga.** Es la unica constancia que va a quedar de este paso.")
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
w("**Y los cuatro verificadores del repositorio:**")
w("")
w("```bash")
w("python scripts/validar_modelo.py          # el modelo consigo mismo")
w('python scripts/verificar_faseA.py "..."   # el modelo contra la hoja')
w("python scripts/verificar_documentos.py    # la prosa contra el modelo")
w("python scripts/verificar_enlaces.py       # que todo enlace entre documentos resuelve")
w("```")
w("")
w("**Ninguno mira la aplicacion.** Para eso estan las pruebas de aceptacion de")
w("[`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).")
w("")
w("## Paso 10 — Publicar")
w("")
w("> **Antes de publicar, lea esto.** Ninguna de las coordenadas de `ACT_Activos` se levanto en campo.")
w("> De los **368 activos** de la hoja vigente, **34 comparten** `4.728512, -74.114531`, que esta en")
w("> Bogota y no en el corredor, y los **334 restantes** llevan coordenada propia pero **calculada")
w("> sobre el trazado**, no medida. Con los radios por tipo —0,05 km en la mayoria— la aplicacion")
w("> **rechaza todo cierre hecho en via y acepta todo cierre hecho en Bogota**.")
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
w("> ## Las marcas `OCULTAR` y `TRAMPA` NO aplican a la hoja vigente")
w(">")
w("> **Describen una hoja que ya no se usa:** el libro heredado que arrastraba columnas que el modelo")
w("> no declara. **La hoja vigente se genera del modelo y no trae ninguna**, asi que no hay nada que")
w("> ocultar ni ninguna referencia que deshacer. Ignore las dos marcas.")
w(">")
w("> Se conservan por una sola razon: son la lista por nombre que permite reconocer esas columnas si")
w("> algun dia aparece una copia antigua del libro. **No son trabajo de nadie.**")
w(">")
w("> **Compruebelo, con la regla `F-19`:**")
w(">")
w("> ```bash")
w('> python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"')
w("> ```")
w(">")
w("> ```")
w("> ok Hoja limpia: ninguna de las %d columnas retiradas existe ya. No hay nada que ocultar"
  % sum(len(v) for v in CAMPOS_RETIRADOS.values()))
w("> ```")
w(">")
w("> La plantilla se rehace entera con `python scripts/generar_plantilla.py` y sale con las columnas")
w("> que el modelo declara, ni una mas.")
w("")
w("Leyenda:")
w("")
w("- **CLAVE** — casilla `KEY` marcada, tipo `Text`")
w("- **`Ref` -> Tabla** — tipo `Ref` con esa tabla como *Source table*")
w("- **IsPartOf** — ademas, casilla `Is a part of` marcada")
w("- **OCULTAR** — **no aplica a la hoja vigente.** Columna retirada del modelo que el libro heredado")
w("  arrastraba. Si apareciera: tipo `Text`, `Show?` desmarcado, sin formula")
w("- **TRAMPA** — **no aplica a la hoja vigente.** Donde exista, AppSheet la convierte a `Ref` sola")
w("  por coincidencia de nombre")
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
        # Los valores del Enum salen de `valores`, NUNCA de la nota. Partir la
        # nota por comas publicaba un valor llamado "Baja. Pondera la
        # disponibilidad de D-13" y otro con un parrafo entero dentro.
        if c["tipo"] == "Enum":
            if c.get("valores"):
                acc.append("Valores: " + " · ".join("`%s`" % v for v in c["valores"]))
            else:
                acc.append("**Valores sin declarar en el modelo.** No los invente: "
                           "pregunte antes de crear la columna")
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
