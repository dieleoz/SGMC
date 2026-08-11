# CLAUDE.md — SGMC (Concesión Transversal del Sisga S.A.S.)

Instrucciones de trabajo para agentes en este repositorio. Léelo antes de tocar cualquier archivo.

## 1. Qué es este proyecto

SGMC (Sistema de Gestión de Mantenimiento en Campo) digitaliza la inspección y el mantenimiento
preventivo/correctivo de la infraestructura ITS, eléctrica y de TI del corredor de la Concesión
Transversal del Sisga.

No es un repositorio de código de aplicación. Es un repositorio **documental y de modelo de datos**
de un sistema construido sobre **Google AppSheet** (no-code) con backend en **Google Sheets**.
El entregable de este repo es el As-Built: especificaciones, diccionario de datos, manuales,
dictámenes de auditoría y el archivo Excel maestro.

**Cuál es la aplicación y cuál es la hoja lo dice `scripts/sistema.py`, y nada más.** Vuélcalo con
`python scripts/sistema.py`. No copies un identificador aquí: es lo que produjo cinco aplicaciones y
tres hojas mencionadas por el repositorio en cuatro días. Ver §9.2.

- Repositorio remoto: `github.com/dieleoz/SGMC`

## 1.1 Antes de tocar el modelo

**`docs/REGLAS_DEL_MODELO_DE_DATOS.md` reúne las diez reglas que manda el motor**, cada una con el
fallo del que salió y **quién la hace cumplir**. Se genera de `modelo_objetivo.py`, así que sus
listas no pueden derivar.

Las secciones 7.x de este archivo cuentan la historia de cada fallo; ese documento dice qué hay que
respetar al cambiar algo. **Cualquier cambio en el modelo, en la plantilla o en la aplicación pasa
por él.**

## 2. Dónde está la verdad

**La fuente única es `scripts/modelo_objetivo.py`.** De ahí se generan el diccionario de datos, el
manual de despliegue y la lista de reposición. Nada se documenta a mano.

**El dato vive en Google Sheets** y se verifica descargándolo a `BD/` y corriendo
`verificar_faseA.py`. La hoja vigente es la que declara `scripts/sistema.py`, y el volcado local con
el que se comprueba es `BD/Modelo_Datos_PLANTILLA.xlsx`: 28 pestañas de datos más `_LEEME`, ninguna
oculta, `FASE A CERRADA`.

### La divergencia de agosto está cerrada, y de raíz

Durante días el Excel local y el Sheets de producción fueron modelos distintos, y esa brecha causó
media docena de hallazgos. **Desde el 2026-08-10 no pueden divergir: son el mismo archivo.** La hoja
publicada es la plantilla que genera `scripts/generar_plantilla.py`, así que no hay dos cosas que
comparar.

Lo que queda de aquello son tres reglas que siguen valiendo:

- **Antes de afirmar algo sobre el modelo, declara contra qué archivo lo verificaste.**
- **Al leer un `.xlsx` con `openpyxl`, `data_only=True`** o estarás leyendo fórmulas en vez de
  valores. Y al revés para detectar fórmulas: hacen falta dos libros abiertos del mismo archivo.
- **Lo que el modelo declara y el archivo no tiene, es deriva.** `F-18` la caza para pestañas
  ocultas y `F-19` para columnas retiradas que ya no existen. Las dos nacieron de fallos reales.

## 2.1 Propiedad y edición del backend

**La hoja vigente es propiedad de la Concesión.** Eso cierra el punto para el backend.

Lo que sigue abierto es la aplicación y la hoja **anteriores**, que son del desarrollador y product
owner. Están nombradas en `SUPERADOS` de `scripts/sistema.py`, y qué comunicarle está en
`docs/COMUNICACION_PROPIETARIO_APP.md`.

Nota de método: `get_file_permissions` devuelve únicamente al propietario, pero eso **no** implica
que no haya otros editores. Comprobado en la práctica: la cuenta del cliente sí tiene permiso de
edición. No infieras el nivel de acceso desde esa API.

## 3. Regla de verificación (no negociable)

Este proyecto arrastra un historial de subsanaciones reportadas como cerradas que no lo estaban.

**Y hay dos archivos que verificar, no uno.** Durante cinco rondas esta regla se aplicó solo a los
datos: todo lo que las especificaciones afirmaban sobre **cómo se comporta AppSheet** salía de la
memoria. Antes de escribir una regla, un tipo o un paso que dependa del comportamiento de la
plataforma, **busca la página oficial**. Lo verificado está en
`docs/BASE_CONOCIMIENTO_APPSHEET.md`, con su URL y su fecha; lo que no se encuentre se declara
como supuesto, en su sección **«Lo que sigue SIN verificar contra la fuente»** — que ya no está al
final del documento, porque después de ella se añadieron los puntos 13 a 16. Búscala por el título,
no por la posición.

- **No declares nada conforme por reporte. Verifícalo contra el archivo.** Vale también para los
  informes de otros agentes, incluidos los que te dan la razón: el arquitecto propuso una lista de
  catálogos con clave legible que incluía siete tablas **numéricas**. Se detectó volcando la
  primera columna de las 31 hojas, no leyendo con más atención.
- Para el Excel, usa `openpyxl` (disponible, 3.1.5) y muestra el dato leído, no un resumen.
- Distingue siempre **estructura** de **población**: que exista la columna no significa que el
  campo tenga datos, y que la tabla exista no significa que el flujo se haya ejercitado.
  Los dos ejemplos vivos: **las tablas de movimiento están vacías a propósito** desde que se
  retiraron los registros de prueba, así que el ciclo **sigue sin ejercitarse de extremo a extremo**;
  y **los 27 formularios tienen banco de preguntas, pero 288 de las 333 son borrador** y lo dicen en
  su ayuda. Que exista la fila no significa que esté acordada. Cuenta el archivo antes de afirmar
  cualquiera de las dos cosas.
- Al cerrar un hallazgo, deja constancia de con qué comando y qué salida lo cerraste.
- **Al leer un `.xlsx` con openpyxl, `data_only=True` o estarás leyendo fórmulas.** Sin él,
  `TIP_TiposActivo.FormularioID` devolvía `=CONCAT("FRM_",MID(B2,1,4))` en vez de `FRM_SOS`: 18
  huérfanos contra su tabla destino que ninguna regla veía, y un diccionario As-Built generado con
  esa basura. **Y al revés para detectar fórmulas:** con `data_only` openpyxl deja de verlas, así
  que F-17 necesita su propio libro sin él. Dos libros abiertos del mismo archivo.
- **Una regla de validación nueva se prueba reintroduciendo el defecto.** Si no la ves fallar, no
  sabes si funciona. V-17 se escribió el 2026-08-07 para cazar un defecto real y **su primera
  versión daba falso positivo** sobre una regla correcta: prohibía la clase entera en vez de
  discriminar, y habría detenido el pipeline. Se corrigió y se probó con siete casos, cinco que
  deben fallar y dos que deben pasar.
- **Una lista escrita a mano se contrasta contra el archivo, automáticamente.** No basta con
  derivarla bien una vez: alguien la editará después. `CLAVE_LEGIBLE` y `CLAVE_GENERADA` las
  comprueba F-11 contra la hoja, y de forma **asimétrica**: falla si una tabla fuera de la lista
  tiene clave legible —eso bloquea trabajo correcto— y solo avisa en el caso contrario.
- **Corregir una regla sin añadir su prueba deja el arreglo sin constancia.** RG-16 y RG-17 se
  corrigieron y no tenían ni una prueba de aceptación; son P-16 y P-17 porque alguien lo señaló, no
  porque el arreglo lo llevara puesto.
- **Quien aplica un cambio no modifica la comprobación que lo mide.** Ocurrió el 2026-08-07: el
  agente que aplicó `ESPEC-001C` editó `verificar_faseA.py` y después anunció que pasaba. Tenía
  razón en el fondo —la regla F-05 había quedado obsoleta— pero el bucle está mal aunque la
  conclusión sea buena: la prueba solo vale mientras sea independiente de quien la aprueba. Un
  cambio en `verificar_faseA.py` o `validar_modelo.py` propuesto por quien está siendo verificado
  se revisa antes de aceptarlo, y **se prefiere endurecer la comprobación a retirarla**. Si una
  fila debía borrarse, no basta con dejar de exigir que exista: hay que exigir que no exista.

## 4. Convenciones de entregables

- **Sin emojis ni iconos decorativos** en documentos, mensajes de error de la app y textos de
  interfaz. Los documentos heredados los tienen; al reescribir uno, quítalos.
- Español, con las tildes correctas. Ojo: varias hojas del Excel tienen encabezados con
  mojibake (`Descripci�n`, `T�cnicoID`, `Secci�n`) por codificación; al leer, no los normalices
  silenciosamente — repórtalos como hallazgo.
- No hagas commit ni push salvo petición explícita.

## 5. Nomenclatura del modelo

Prefijos de tabla por dominio: `USR_` usuarios, `ROL_` roles, `SED_` sedes, `TIP_` tipos de
activo, `ACT_` activos, `OT_` órdenes de trabajo, `MAN_` mantenimientos, `CHK_`/`CHD_` checklist
encabezado y detalle, `FOT_`/`FIR_` evidencias, `FRM_` formularios y preguntas, `TPR_` tipos de
respuesta, `LST_` listas de valores, `EST_`/`FRE_`/`CAL_`/`SEN_` catálogos.

Advertencia sobre claves: **la clave real se vuelca, no se supone.** Un nombre de columna que
parece una clave puede no serlo, y una tabla puede haber cambiado de clave desde la última vez que
alguien lo escribió aquí. Se deriva con una línea:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print({t:next((c['nombre'] for c in d['columnas'] if c.get('pk')),'?') for t,d in M.MODELO.items()})"
```

**El caso de `OT_OrdenesTrabajo` ya está resuelto y este apartado lo describía al revés.** Su clave
es hoy `OTID`, con valores `OT-0001`. Se llamó `Numero_OT`, y ese renombrado **está hecho**: figura
en `RENOMBRADOS` de `scripts/modelo_objetivo.py` y en la tabla §1 de
`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`. Si un documento vigente dice que la clave es `Numero_OT`,
está desactualizado.

## 6. Referencias: las reglas que gobiernan el cableado

El defecto raíz del sistema no es que falten columnas. Es que las que existen son texto.
`MAN_Mantenimientos.OTID` se llama como una referencia y figura como referencia en el diccionario,
pero AppSheet responde `Invalid dereference. Column OTID is not a Ref`. De ese único hecho cuelgan
el geofencing, la navegación padre-hijo y todo reporte por activo.

El procedimiento vigente está en `docs/sdd/ESPEC-002-cableado-en-appsheet.md`, con sus pruebas en
`PRUEBA-002`. Aquí van las reglas que no se negocian.

**R-1. Una referencia guarda el valor de la clave del destino.** De ahí todo lo demás. Antes de
cablear una referencia, verifica cuál es la clave real de la tabla destino: no la supongas por el
nombre **ni por lo que diga este archivo**, que es exactamente el fallo que esta regla arrastró:
durante días afirmó que `OT_OrdenesTrabajo` tenía la clave `Numero_OT` mientras el modelo ya
declaraba `OTID`. **Hoy la clave es `OTID`**, y la forma correcta de saberlo es volcarla (§5).

**R-2. Renombrar y retipar son la misma tarea, no dos.** Si la clave se llama de una forma y quien
la apunta se llama de otra, no hay contra qué resolver. Fue el caso de `OT_OrdenesTrabajo`:
`Numero_OT` como clave y `OTID` en quien la apuntaba. **Ese renombrado ya se hizo** y por eso las
dos se llaman igual. Por eso el renombrado no es cosmético y no se pospone.

**R-3. Primero la clave del destino, después quien la apunta.** Convertir una referencia antes de
que su destino tenga la clave definitiva deja las filas sin resolver.

**R-4. Una conversión `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave.**
Las demás quedan huérfanas y AppSheet no lo anuncia. Limpia los datos de prueba **antes** de
convertir, nunca después.

**R-5. Cada cambio de referencia se declara en el modelo antes de tocar nada.** En
`scripts/modelo_objetivo.py` hay dos estructuras para eso, y son de uso obligatorio:

- `RETIPADOS` — conserva el nombre, cambia de tipo. Aquí vive `MAN.OTID`.
- `RENOMBRADOS` — cambia de nombre, con el motivo de cada uno.

Las reglas V-14, V-15 y V-16 de `validar_modelo.py` detienen la validación si una referencia no
declara de dónde sale. No hay ruta legítima que se salte esto.

**R-6b. El histórico no se borra: se desactiva.** Decidido el 2026-08-07. `OT_OrdenesTrabajo` y
`MAN_Mantenimientos` van sin la acción `Deletes`, y un error se corrige con `Activo = FALSE`.
Por eso `MAN_Mantenimientos.OTID` va **sin `IsPartOf`**: marcarlo haría que borrar una orden borrase
la ejecución, las fotografías, las firmas y el checklist. `FOT`, `FIR` y `CHK` sí lo llevan respecto
del mantenimiento, y es inofensivo porque el mantenimiento nunca se borra. **`IsPartOf` describe
composición, no protege nada: la protección es retirar el borrado.**

**R-6c. Renombrar un encabezado no cambia lo que el dato significa.** `CHK_Checklists.OTID` se
renombró a `MantenimientoID` y su fila siguió guardando `OT-0001`, que es una **orden**. La columna
dice una cosa y el dato dice otra, y solo se descubre al convertir a `Ref`. Después de todo
renombrado, **comprueba que los valores resuelvan contra la nueva clave destino**: es la regla F-10
de `verificar_faseA.py`.

**R-6d. Un reporte histórico nunca filtra por el estado actual del padre (RG-18).** Filtrar los
mantenimientos por `[ActivoID].[Activo] = TRUE` hace que, al dar de baja un activo, **desaparezcan
retroactivamente todos sus mantenimientos pasados**: el informe del año anterior cambia solo y
muestra menos trabajo del que se hizo. Ante interventoría eso no parece un filtro mal puesto, parece
que el mantenimiento nunca se ejecutó. Un histórico filtra por la fecha y el estado de la
**transacción**; el activo aporta el nombre, no el filtro.

**R-6. Un dato se alcanza por referencia o se guarda, nunca las dos cosas.** `MAN_Mantenimientos`
no lleva `ActivoID`: el activo se alcanza por `[OTID].[ActivoID]`. Guardarlo también permitiría que
la ejecución diga un activo y su orden diga otro, sin forma de saber cuál miente.

**R-7. Cuidado con el nombre reutilizado.** `OT_OrdenesTrabajo.Activo` guarda hoy el identificador
del activo; en el modelo objetivo `Activo` es la bandera `Yes/No` de todas las tablas. Al migrar,
renombra la vieja **antes** de crear la nueva, o el Sheets queda con dos columnas iguales y
AppSheet resuelve una sin decir cuál.

**R-8. Al crear un catálogo nuevo, su clave debe ser el valor que ya guardan los datos.** No un
identificador nuevo y ordenado. `EOT_EstadosOrden` se creó con claves `1..7` mientras
`OT_OrdenesTrabajo.EstadoOrdenID` guardaba `Asignada`, `Cerrada` y `Suspendida`: se ve bien en la
hoja y deja las 6 órdenes huérfanas en cuanto se cablea. `UNF_UnidadesFuncionales` se hizo al revés
—claves 7 a 10, las que ya usaba `ACT_Activos`— y por eso las 34 filas siguen resolviendo sin tocar
ninguna. **Un catálogo se diseña mirando los datos que va a tener que resolver.**

**R-9. La cadena se prueba en el Asistente de Expresiones, no en la aplicación.** Escribir
`[OTID].[ActivoID].[Ubicacion_LatLong]` sobre `MAN_Mantenimientos` y ver que resuelve es la prueba de que
la referencia quedó. Es más rápido y más seguro que ejercitar la app.

**R-10. Un `Ref` guarda la clave, no el nombre — pero no toda comparación contra un literal está
mal.** `[EstadoActivoID] <> "Retirado"` es siempre cierto, porque la clave de `EST_Activo` es
`EST-01`…`EST-04` y el texto vive en `Nombre`. Se escribe `[EstadoActivoID].[Nombre]`. **En cambio
`[EstadoOrdenID] = "Cerrada"` es correcto**, porque `EOT_EstadosOrden` tiene la palabra como clave,
por diseño (R-8).

`CLAVE_LEGIBLE` de `scripts/modelo_objetivo.py` reúne hoy **20 tablas** y `CLAVE_GENERADA` las
otras **8**; entre las dos cubren las 28, sin solaparse. **Eran 22 y 6 hasta que `ESPEC-005` sacó
`OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` de la primera y las metió en la segunda**: su clave
era legible y **nadie la generaba**. Se cuentan, no se citan:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(len(M.CLAVE_LEGIBLE),len(M.CLAVE_GENERADA))"
```

**Y aquí hay que decir algo incómodo: esa lista ya no distingue lo que R-10 necesita distinguir.**
`CLAVE_LEGIBLE` nació significando «la clave ES la palabra» —`Cerrada`, `Asignada`—, y tras la
resiembra del 2026-08-10 significa «la clave es alfanumérica con prefijo» —`EST-01`, `ACT-0001`—,
que es otra cosa. `EST_Activo` entró en la lista por lo segundo, así que **V-17 exime justamente la
comparación que nació para cazar**: `[EstadoActivoID] <> "Retirado"` pasa el validador sin un solo
error. Comprobado el 2026-08-10 reintroduciendo el defecto sobre `REGLAS` en memoria.

**Se separó ese mismo día, y ahora son dos listas.** `CLAVE_LEGIBLE` sigue diciendo *cómo se ve una
clave*; **`CLAVE_ES_LA_PALABRA`** dice *contra cuáles es legítimo comparar un literal*, y de las 20
solo son **cuatro** —`EOT_EstadosOrden`, `FRM_Formularios`, `PAR_Parametros`, `SEN_Sentidos`—,
comprobado contra los datos. V-17 pregunta a la segunda y vuelve a cazar
`[EstadoActivoID] <> "Retirado"`, probado reintroduciéndolo.

**`CLAVE_ES_LA_PALABRA` se declara a mano y no se deriva, a propósito.** Derivarla la habría hecho
apagarse sola el día que alguien resembrara una clave — que es exactamente lo que acababa de pasar.
Una salvaguarda que se desactiva sola cuando cambia el terreno no es una salvaguarda.

**Y la lección general, que vale más que el arreglo: un nombre que sirve para dos cosas acaba
sirviendo mal para una.** La lista no cambió de contenido por descuido, cambió de *significado*, y
nada podía avisar porque ningún verificador comprueba que un nombre siga queriendo decir lo mismo.

Y lo peligroso no es que la expresión falle: **no falla**. Devuelve siempre lo mismo. Si además es
una `App formula`, **escribe** ese resultado constante sobre los datos.

**R-10b. Una lista derivada del dato puede ser cierta contra el fixture y falsa contra el diseño.**
`CLAVE_LEGIBLE` se derivó volcando la clave de las 31 hojas, que es lo correcto — y aun así nació
mal: seis de sus quince entradas eran «legibles» solo porque la Fase A escribió a mano
`TEST-MTTO-001`, y esas seis reciben `UNIQUEID()`, de modo que serán cadenas aleatorias desde la
primera fila que cree la aplicación. **Derivar del dato no basta: hay que preguntar si ese dato es
el definitivo.** De ahí `CLAVE_GENERADA`, y la regla F-11 de `verificar_faseA.py`, que contrasta las
dos listas contra la hoja de forma asimétrica.

**R-11. Aplazar una referencia arrastra la regla que la usa.** Al posponer
`PLA_PlanMantenimiento.FrecuenciaID` quedó RG-11 —una `App formula` que usa `[FrecuenciaID].[Dias]`—
configurada contra una columna todavía de texto: `ProximaFecha` habría quedado en blanco sin decir
por qué. Antes de aplazar una referencia, busca qué reglas la desreferencian.

**R-12. Arreglar una regla puede despertar un peligro dormido.** Mientras RG-16 estuvo mal escrita
era siempre cierta, así que ningún activo llegaba nunca a `Activo = FALSE` y RG-18 no tenía a qué
morder. Corregirla activó el escenario. **Cuando arregles una condición que nunca se cumplía,
pregunta qué dependía de que no se cumpliera.**

### Expresiones vigentes

Geofencing de cierre, RG-01 (RF-012). `ACT_Activos` guarda un único campo `Ubicacion_LatLong` de
tipo LatLong; no existen columnas `Latitud`/`Longitud` separadas. El nombre lleva el sufijo desde
el 2026-08-10 y **la forma corta `Ubicacion` ya no existe en ninguna tabla**: si la lees en un
documento o en un comentario, habla de antes de esa fecha. El radio sale del tipo de activo,
porque una subestación y un poste SOS no admiten la misma tolerancia:

```
DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
```

Mensaje de error, en texto plano:

```
Ubicación fuera de rango: debe estar junto al activo para cerrar.
```

**Ese radio ya está poblado en la plantilla, y solo ahí.** `TIP_TiposActivo.RadioGeofencingKm` trae
valor en los **27 tipos** de `BD/Modelo_Datos_PLANTILLA.xlsx`: `0.05` en 18 —poste SOS, cámaras,
sensores, paso seguro y equipos de TI—, `0.1` en 8 —paneles de mensaje variable, básculas, peajes,
generador y subestación— y `1.5` en el tramo de fibra, que es lineal. **Y esa es la única hoja que hay**, desde que el
2026-08-10 se reconstruyó sobre ella: ya no existe una segunda con la columna vacía.

Sobre la plantilla, **el literal `1.0` ya no se usa**, y `PAR_Parametros.RADIO_GEOFENCING_KM` queda
como valor provisional histórico: la regla no lo lee. Un documento que mande el literal `1.0` sin
decir que habla de la hoja de producción describe un estado superado.

Y la regla no basta por sí sola: las cuatro columnas de captura de `MAN_Mantenimientos`
—`Coordenadas_Cierre_LatLong`, `Precision_GPS`, `UbicacionEscaneo_LatLong` y `FechaHoraEscaneo`—
van con `Editable_If = FALSE` (RG-20). Sin eso, `Coordenadas_Cierre_LatLong` dibuja un pin
arrastrable sobre el mapa, el técnico lo suelta encima del activo y RG-01 valida sin protestar.

**El nombre completo es `UbicacionEscaneo_LatLong`**, no `UbicacionEscaneo`. La descripción de
RG-20 en `scripts/modelo_objetivo.py` todavía la abrevia; al configurarla en el editor manda el
nombre de la columna, que se vuelca de `MODELO['MAN_Mantenimientos']`.

Son incorrectas contra este modelo, y fallan en ejecución, todas estas variantes:

| Variante | Por qué falla |
|---|---|
| `[ActivoID].[Ubicacion_LatLong]` desde `MAN_Mantenimientos` | Esa columna se retira: el activo va por la orden |
| `LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])` | No existen columnas de latitud y longitud separadas |
| `[OTID].[Activo].[Ubicacion_LatLong]` | `Activo` es el nombre **anterior** al renombrado. Después de migrar apunta a la bandera `Yes/No` |

Security Filter por sede (RG-04, RF-004): filtra `ACT_Activos` por las unidades funcionales
asignadas al usuario resuelto vía `USEREMAIL()`. No por `SedeID`, que es donde trabaja la persona
y no donde está el activo; esa confusión es la que dejó a usuarios y activos en conjuntos
disjuntos.

**El cableado no basta para que el geofencing funcione, y el radio poblado tampoco.** Lo que falta
es la coordenada del activo, y eso **no ha cambiado en el fondo, aunque sí en la forma**:

- `ACT_Activos` tiene **368 filas**: **34** del inventario real y **334** sintéticos, que se
  reconocen porque su `Observaciones` dice `ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL`.
- Las **368** tienen `Ubicacion_LatLong` poblada y **las 368 son distintas**. Ya no hay 34 puntos
  idénticos en Bogotá: esa descripción quedó obsoleta el 2026-08-10, cuando `generar_plantilla.py`
  pasó a **derivar la coordenada del `PK`** proyectándolo sobre el trazado del corredor.
- **Derivada no es levantada.** Ninguna de las 368 es el sitio real del equipo.

Se cuenta así, y no se repite de memoria:

```bash
python -c "import openpyxl;w=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',data_only=True)['ACT_Activos'];h=[c.value for c in w[1]];r=[x for x in w.iter_rows(min_row=2,values_only=True) if x[0]];i=h.index('Ubicacion_LatLong');o=h.index('Observaciones');print(len(r),'filas |',sum(1 for x in r if 'SINTETIC' in str(x[o] or '').upper()),'sinteticos |',len({x[i] for x in r}),'coordenadas distintas')"
```

Hasta que se carguen coordenadas reales (D-01), la comprobación de distancia al cerrar **no
significa nada**: dice si el técnico está donde el generador colocó el punto, no donde está el
equipo. **No declares el geofencing operativo por haber puesto la regla, ni por ver la columna
llena.**

## 7. Estado: no vive en este archivo

El estado del proyecto cambia cada semana y este archivo son **reglas**, que no cambian. Mezclarlos
hizo que durante dos dias `CLAUDE.md` describiera una Fase 0 abierta que ya se habia cerrado.

| Que quieres saber | Donde esta |
|---|---|
| **En que punto va todo y que falta** | **`ESTADO.md`. Es la verdad del estado, y se lee primero** |
| En que fase vamos y que sigue | `docs/ROADMAP.md` §2, orden de implementacion |
| Que hace el sistema, para quien y como | `docs/FUNCIONAL_SGMC.md` |
| Que tiene la hoja hoy, columna a columna | `docs/bd.md`, **generado** |
| Por que se cerro cada fase | `docs/sdd/ACTA-00N-*.md` |
| Por que se decidio algo que ya no aplica | `docs/historico/`, con su README |

Para comprobar la hoja en cualquier momento: *Archivo → Descargar → Microsoft Excel*, guardar en
`BD/` y correr `python scripts/verificar_faseA.py "BD/<archivo>.xlsx"`. **No cierres nada
por el reporte de quien lo aplico**, ni siquiera por el tuyo.

## Método de trabajo vigente: construir bajo supuestos

El enfoque de preguntar primero al líder funcional **está descartado**. El documento de las 14
decisiones ya se envió y no se reenvía, pero no se espera su respuesta para avanzar.

Los catorce supuestos están adoptados en `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` y son **vinculantes
hasta que el campo los desmienta**. Trabaja con ellos. No abras un punto para consultarlo: si
falta una definición, adóptala como supuesto, decláralo y sigue.

La razón es doble. Un cuestionario en abstracto a quien todavía no tiene el modelo mental produce
silencio o un "de acuerdo" a todo, que simula una decisión inexistente. Y el sistema todavía no
permite formarse criterio: un solo formulario con preguntas en toda la hoja, y ningún ciclo recorrido de
extremo a extremo. Una suposición escrita y probada se corrige en una tarde; una pregunta sin
responder bloquea semanas.

Lo que hay que ejecutar ahora está en `ESTADO.md` §2 y en
`docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`. La directiva anterior,
`PROMPT_CONSTRUCCION_SGMC.md`, construía la aplicación que se reemplazó y **está en
`docs/historico/`**: no la sigas.

## Para qué existe el sistema

Antes de decidir nada, ancla contra esto:

> Garantizar que el mantenimiento se hizo, que quien lo hizo estuvo físicamente frente al equipo,
> y que la evidencia que lo respalda es difícil de falsificar.

Todo lo demás sirve a eso o sobra. La presencia se garantiza encadenando evidencias
independientes: fotografías tomadas con la cámara de la app y no de la galería —cada una con su
propia coordenada—, cierre dentro del radio del tipo de activo con las columnas de captura no
editables, y marca de tiempo del servidor y no del teléfono. La cadena no es infalsificable: eleva
el costo de falsificar por encima del de hacer el trabajo, que es el objetivo realista.

**El escaneo del QR físico ya no es un eslabón de esa cadena**: quedó fuera de alcance el
2026-08-07 y el activo se abre por lista. Es el eslabón más fuerte que se perdió, y por eso el
peso recae en la fotografía y en el `Editable_If = FALSE` de la captura.

Detalle con consecuencia: la compresión a 600 px descarta los metadatos de la imagen, así que
fecha, hora y coordenada se guardan **como datos de cada fotografía**, nunca confiados al archivo.

## Restricciones de plataforma que condicionan el diseño

Verificadas el 2026-08-06. Repásalas antes de proponer nada:

| Restricción | Consecuencia |
|---|---|
| En el plan gratuito **los procesos programados no se ejecutan** | Sin plan pagado no hay generación automática de órdenes, ni correo semanal de tareas, ni marcado de vencidas |
| Las imágenes se guardan en el Drive del **propietario** del documento | Hoy es una cuenta personal de Gmail con 15 GB compartidos. Con el inventario completo la cuota se agota antes de la retención exigida |
| 10 millones de celdas por hoja | Rara vez muerde. Se degrada antes la sincronización, por encima de ~50.000 filas por tabla |
| API REST | Requiere plan Core o superior |

Las cifras de crecimiento se calculan con `python scripts/capacidad.py`, no a ojo.

## Los dos documentos que se generan, y por qué

Ninguno se edita a mano. Los dos existen porque su versión escrita derivó:

| Documento | Sale de | Describe |
|---|---|---|
| `docs/ARQUITECTURA_OBJETIVO_SGMC.md` | `scripts/modelo_objetivo.py` | El sistema que se va a construir |
| `docs/bd.md` | `scripts/generar_diccionario_bd.py` sobre el `.xlsx` | El sistema que existe hoy, y su distancia al objetivo |

**Si un documento describe un estado, se genera.** Escribirlo a mano garantiza que dentro de dos
días diga otra cosa que el archivo, y este proyecto ya perdió meses por eso exactamente.

## El modelo objetivo se edita en un solo sitio

La arquitectura correcta está codificada como datos en `scripts/modelo_objetivo.py`. De ahí salen
la validación y la documentación. **No edites `docs/ARQUITECTURA_OBJETIVO_SGMC.md` a mano:** se
regenera. Flujo obligatorio ante cualquier cambio de diseño:

```
1. editar  scripts/modelo_objetivo.py
2. correr  python scripts/validar_modelo.py        -> debe dar 0 errores
3. correr  python scripts/generar_doc_arquitectura.py
```

Esto existe porque el proyecto ya sufrió lo contrario: `bd.md` y el Excel describían modelos
distintos y nadie lo detectó durante meses.

## Economía de interfaz

Manejar el editor de AppSheet clic a clic consume muchos tokens y es frágil: los desplegables no
siempre se abren, y el viewport cambia de tamaño entre llamadas y desplaza las coordenadas.

- Los datos se cargan **por lote** sobre el Sheets, nunca celda por celda.
- La configuración de AppSheet no tiene API, así que va por navegador: **agrupa las acciones y
  verifica al final del bloque**, no después de cada clic.
- Para validar una expresión, el Asistente de Expresiones es más rápido y seguro que probarla en
  la aplicación.
- Prefiere leer el backend con el conector de Google Drive antes que navegar la interfaz.

Lo que sí está verificado como resuelto: `Coordenadas_Cierre_LatLong` y `Precision_GPS` existen en
`MAN_Mantenimientos`, y la columna `Observaciones` ya no está duplicada. **El recuento de columnas
de esa tabla se deriva, no se cita de memoria** —el modelo declara hoy 23— porque esa cifra cambió
tres veces y cada versión sobrevivió en algún documento.

## 7.4 Los seis verificadores, y qué mide cada uno

Ninguno sustituye a otro. Los seis se corren antes de dar nada por cerrado.

| Script | Mide | Cuándo falla |
|---|---|---|
| `validar_modelo.py` | El modelo consigo mismo: tipos, claves, rutas de desreferencia, reglas | Siempre. Es el único gate objetivo del pipeline |
| `verificar_faseA.py` | El modelo contra **la hoja descargada**: estructura, tipos, pestañas | Al cerrar una fase de datos |
| `verificar_datos.py` | **Los datos** de esa misma hoja: obligatorias vacías, referencias huérfanas, homogeneidad de tipo | Al entregar o publicar la plantilla |
| `verificar_documentos.py` | **La prosa** contra el modelo | Al escribir o tocar cualquier `.md` |
| `verificar_enlaces.py` | Que todo enlace relativo entre documentos **resuelve** | Al mover, renombrar o retirar cualquier documento |
| `verificar_reproducible.py` | Que **generar la plantilla dos veces dé lo mismo** | Al tocar cualquier generador |

**`verificar_enlaces.py` se añadió el 2026-08-09, y nació de un fallo concreto.** Al retirar 15
documentos a `docs/historico/` quedaron **31 enlaces rotos**, y se encontraron leyéndolos uno a uno.
Un enlace roto no es cosmético: manda a quien retoma el proyecto a un documento que no existe, y lo
que hará entonces es guiarse por el que sí encuentre, que suele ser el viejo. **Mover un documento
es la operación que más silenciosamente rompe cosas**, y era la única que no tenía red.

**`verificar_datos.py` es el sexto y se añadió el 2026-08-10**, por el hueco que los otros cinco
compartían: **ninguno abría el archivo de datos para mirar si las columnas estaban pobladas.** Ocho
cambios pasaron los cinco en verde y tres eran defectuosos, entre ellos
`ACT_Activos.Ubicacion_LatLong` vacía en las 368 filas siendo la columna que RG-01 desreferencia.
`DISTANCE()` contra blanco no da error: da un valor que rechaza el cierre legítimo. Su propio
encabezado explica cuál de los cinco dejaba pasar cada cosa.

**Hay además un auditor que no es un verificador:** `scripts/auditar_cableado.py` compara el
cableado **real de la aplicación** contra el que declara el modelo, leyendo por la API. No entra en
la lista porque no mide el repositorio contra sí mismo sino contra producción, **escribe en el
repositorio** (`docs/CORRECCIONES_CABLEADO.md`) y hay referencias de las que **no puede decir nada**.
Su método está asentado en `docs/BASE_CONOCIMIENTO_APPSHEET.md` §16, con sus límites.

**Y tres módulos que no verifican nada: declaran lo que nadie declaraba.** Se consultan **antes** de
tocar el editor, no después.

| Script | Declara |
|---|---|
| `scripts/lectura_de_vuelta.py` | **Quién comprueba cada clase de cambio** —3 con comando, 4 a ojo—, `FILTROS_AL_FINAL` y `VOLCADO_CIEGO_A` (7.15) |
| `scripts/navegacion_editor.py` | **Dónde está cada control en pantalla.** `Required_If` se llama `Require?` y no es una casilla |
| `scripts/alcance_reglas.py` | **Qué columnas toca de verdad cada regla, con su tabla**: 39 de 211. Por nombre suelto salían 94 |

**Lo que ninguno mide es si algo es buena idea.** Para eso está el arquitecto, y por eso su
veredicto no se sustituye por «los scripts pasan». **`ESPEC-005` es la prueba de que ese gate
termina en algo**: entró, la tumbaron con catorce hallazgos, se rehizo contra el archivo y pasó —el
primer dictamen del pipeline que lo consigue—. `ESPEC-004` va por la segunda pasada y quince
hallazgos, y sigue sin aplicarse.

## 7.5 Una sola forma por propósito (regla nueva, 2026-08-07)

**Riesgo real, señalado por operación:** con tanto material acumulado —los documentos de contexto,
once rondas de revisión, cuatro actas—, es fácil **proponer dos mecanismos para lo mismo** y que
alguien implemente los dos. Eso ya pasó dos veces: `Requiere_Repuesto` y `MotivoPendienteID`
registraban el mismo hecho, y el manual de usuario describía un bypass de GPS por nota libre
mientras el modelo tiene `CierreConExcepcion`.

**Las dos están cerradas.** El manual se reescribió el 2026-08-07 y hoy manda el cierre con
excepción; su versión ilustrada, que aún describía el bypass, se retiró a `docs/historico/` el
2026-08-09. Se dejan escritas porque el patrón vuelve, no porque sigan vivas.

**Antes de proponer un mecanismo, comprueba si ya existe uno para ese propósito.** El registro está
en `docs/FUNCIONAL_SGMC.md` §6. Si existe, se usa el que está; si el nuevo es mejor, se retira el
viejo **en el mismo cambio** y se anota en esa tabla. Nunca conviven los dos.

Ese mismo hábito evita el error inverso, que también ocurrió: **proponer como nuevo algo que ya está
en el modelo.** `ROL_Roles` y las cuatro tablas de plantilla de checklist —`FRM_Formularios`,
`FRM_Secciones`, `FRM_Preguntas`, `TPR_TiposRespuesta`— ya existían cuando se propusieron como
tablas a crear. **Vuelca `MODELO` antes de proponer una tabla.**

## 7.6 Los documentos de contexto no son la vara

`contexto/` tiene **ocho archivos sueltos más la carpeta `SISGA Contrato/`, con cinco PDF**: el
acta de inicio, el contrato en su parte general y especial, los apéndices 1 y 2, los apéndices 3 al
9 y los otrosíes 1 a 11. Trece piezas en total, no ocho. Se cuenta, no se recuerda:

```bash
python -c "import os;r='contexto';print(sum(1 for x in os.listdir(r) if os.path.isfile(os.path.join(r,x))),'sueltos +',{d:len(os.listdir(os.path.join(r,d))) for d in os.listdir(r) if os.path.isdir(os.path.join(r,d))})"
```

De los ocho sueltos, `docs/CONTEXTO_OPERACION.md` §1 cataloga siete; el octavo,
`MATRIZ_MANTENIMIENTO_SISGA_2026 (1).xlsx`, no está en esa tabla. **Y la carpeta del contrato
tampoco está catalogada en ningún sitio**, que es lo que hay que saber antes de fiarse de ese §1
como inventario.

**Tres de los sueltos no son del Sisga**: el PDF de ETRA y el informe de enero de 2025 son del
corredor Neiva–Girardot, y la propuesta de la manta es de INDRA en otra doble calzada. Su
procedencia está etiquetada en ese mismo documento.

**Los cinco PDF de `SISGA Contrato/` son harina de otro costal y conviene no mezclarlos con el
resto:** son la fuente contractual de esta Concesión, no ejemplos de otro corredor. Aun así **no
se han vaciado contra el modelo** y esta regla —«no es la vara»— se escribió para el material de
ejemplo, no para el contrato. Lo que el contrato exija es una obligación, no un supuesto; hasta
que alguien lo lea y lo destile, **lo prudente es no citarlo de oídas en ninguna de las dos
direcciones.**

**Son ejemplos que dan contexto, no obligaciones contractuales.** De ellos se copia método. Ninguna
cifra ni estructura suya se convierte en requisito del Sisga sin que operación lo confirme: entra
como **supuesto abierto**, nunca como carencia del modelo.

Este proyecto ya midió el modelo del Sisga contra la estructura de otro corredor una vez. La
advertencia de procedencia existía y contenía ella misma el error.

## 7.7 Una lista es correcta para UN punto de partida (regla nueva, 2026-08-09)

`ESPEC-002` lista **15 columnas** que pasan a `Ref`. Es correcto: quedaban 15 por convertir en la
aplicación existente, donde otras 23 ya estaban puestas.

**Al reconstruir la aplicación desde cero, no sobrevivió ninguna: eran 38.** Y siguiendo la
especificación al pie de la letra, `OT_OrdenesTrabajo.ActivoID` quedó en `Number`, de modo que
`[OTID].[ActivoID].[Ubicacion_LatLong]` —la desreferencia que la propia especificación usa como prueba— no
resolvía.

**El documento no mentía. Le faltaba declarar desde dónde se parte.**

De ahí dos reglas:

**Toda lista derivada declara su punto de partida.** «15 columnas pendientes» solo significa algo
respecto a un estado concreto. Sin esa referencia, la lista se aplica a un estado distinto y produce
un resultado incompleto que nadie detecta.

**Cuando una especificación y `modelo_objetivo.py` discrepan, manda el modelo.** La especificación
se generó de él en un momento dado; el modelo es lo que hay. `MODELO` tiene hoy **39** columnas con
`ref=` —eran 38 cuando se escribió este apartado, y el propio apartado es la razón de que aquí no se
cite el número sino el comando—:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sum(1 for d in M.MODELO.values() for c in d['columnas'] if c.get('ref')))"
```

## 7.8 Dos límites de AppSheet que cambiaron el plan (2026-08-09)

Los dos están verificados en `docs/BASE_CONOCIMIENTO_APPSHEET.md` §11 y §12, y entre los dos
explican por qué se abandonó reparar la aplicación y se reconstruyó.

**AppSheet ignora las pestañas ocultas, y no avisa.** Ocho pestañas del libro —`ACT_Activos`,
`USR_Usuarios`, `TIP_TiposActivo`, `ROL_Roles`, `SED_Sedes`, `CAL_Calzadas`, `SEN_Sentidos`,
`FRE_Frecuencias`— estaban ocultas. Cargaban 24 tablas de 32 y ninguna de esas ocho aparecía en el
desplegable de destino. **Lo cierra `F-18`**, que antes no existía: `verificar_faseA.py` declaró
`FASE A CERRADA` dos veces sobre ese libro, porque `openpyxl` lee las ocultas sin distinción.

**`Regenerate` fusiona, no reemplaza.** Conserva las columnas viejas a propósito. Sirve para añadir
una columna; **con un esquema muy divergente impide converger**. El propio AppSheet indica la
salida: «Delete and re-add the table». Y una cuenta coautora no puede dar de alta tablas, así que
ese camino tampoco estaba disponible.

**Por debajo de cierto umbral se repara; por encima se reconstruye.** El umbral no está escrito en
ninguna parte y hay que estimarlo. En su momento se estimó con 27 columnas renombradas, 8 tablas
nuevas y 45 campos retirados, que estaban muy por encima.

**Esos tres números describen aquel momento, no el modelo de hoy: no los reutilices.** Las tablas
nuevas frente al modelo anterior siguen siendo ocho —`UNF_UnidadesFuncionales`, `ASG_AsignacionZona`,
`EOT_EstadosOrden`, `MOT_MotivosPendiente`, `PAR_Parametros`, `NOV_Novedades`, `PLA_PlanMantenimiento`
y `FAL_ModosFalla`—, pero `RENOMBRADOS` y `CAMPOS_RETIRADOS` se derivan del modelo y hoy dan otra
cifra. Vuélcalas antes de citarlas.

## 7.9 Una instruccion que exige criterio se ejecuta mal (regla nueva, 2026-08-09)

El manual de despliegue decia «oculte las 47 columnas retiradas» y «las 3 columnas trampa». **Quien
lo ejecuta no tiene el modelo delante**, asi que dedujo. Resultado: cableo `CHK_Checklists.ActivoID`
como referencia —es una trampa, habia que ocultarla— y propuso `Abierto / En Proceso / Completado`
como valores de `NOV_Novedades.Estado`, que el modelo declara `Reportada / Aceptada / Descartada`.

**Ninguno de los dos errores es del ejecutor. Son del documento.**

Y las trampas son **tres**, derivadas del archivo. Las conte de memoria en vez de derivarlas. Son
`OT_OrdenesTrabajo.FormularioID`, `CHK_Checklists.ActivoID` y `CHD_ChecklistDetalle.TipoRespuestaID`:
retiradas del modelo, pero con nombre de clave de otra tabla, así que invitan a cablearlas.

**El «47» fue correcto en su día, y su historia es la mejor ilustración de la regla.** No salía de
una sola estructura: eran **43** de `CAMPOS_RETIRADOS` más **4** de `COLUMNAS_SIN_DECIDIR`. Quien
volcaba solo la primera obtenía 43 y creía haber pillado un error; quien contaba la hoja obtenía 47.
Las dos cuentas eran ciertas y el desacuerdo señalaba un hueco real: dos columnas de la hoja
—`FRM_Formularios.Orden` y `FRM_Preguntas.ValorDefecto`— que el modelo no mencionaba de ninguna
forma. **Se cerró declarándolas en la fuente**, no ajustando la cifra en los documentos.

**Y por eso hoy la cifra es otra: 48.** Al declararlas en la fuente, `COLUMNAS_SIN_DECIDIR` se vació
—vale `{}`— y `CAMPOS_RETIRADOS` absorbió su contenido, que es exactamente lo que se pretendía. Que
este apartado siguiera diciendo 47 después de arreglar aquello es la misma deriva que denuncia: una
cifra correcta el día que se escribió y falsa dos días después.

Se deriva con una línea, y nunca se repite de memoria:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sum(len(v) for v in M.CAMPOS_RETIRADOS.values())+len(M.COLUMNAS_SIN_DECIDIR))"
```

**Una cifra que dos caminos calculan distinto no es una errata: es un hueco en el modelo.**

**Regla: todo documento operativo lleva la lista completa, generada.** Si una instruccion dice «las
retiradas», «las trampa» o «los valores correspondientes», esta mal escrita. El anexo de
`MANUAL_DESPLIEGUE.md` es el patron: **ficha por tabla, columna por columna, sin nada que deducir.**

**Y el corolario que falta:** hoy el modelo describe datos, no interfaz. `VISTAS`, `ACCIONES` y
`SLICES` no existen en `modelo_objetivo.py` —comprobado—, asi que el paso de vistas del manual
sigue siendo «se construye sola», exactamente la clase de instruccion que esta regla prohibe.

## 7.10 Dos taxonomias con el mismo nombre (regla nueva, 2026-08-09)

`TIP_TiposActivo` tenia 18 tipos. El Plan Maestro tiene 18 familias. **Nadie habia escrito que no
son la misma lista**, y como los dos numeros coincidian, parecia que si.

No lo eran. Nueve familias no tenian tipo propio y colgaban del tipo de otra cosa: la impresora
heredaba el checklist del NAS, el portatil el del servidor, el carril de peaje el de la bascula.
**78 activos de 355 —el 22%— con el checklist equivocado.**

**Y ningun verificador lo veia, por la misma razon de siempre: la referencia resolvia.**
`TipoActivoID = 17` apunta a una fila que existe. `V-05` comprueba que no haya huerfanos, y no los
habia. Es el mismo patron que el inventario sintetico que reescribio los 34 activos reales.

**La regla: dos listas del mismo tamano no son la misma lista.** Cuando dos vocabularios describen
lo mismo desde sitios distintos —el catalogo de la aplicacion y el inventario de operacion—, la
correspondencia entre ellos **se escribe y se comprueba**, no se supone. Vive en
`scripts/catalogo_tipos.py`, con `comprobar()`, que falla si dos familias comparten tipo.

**Como quedo, y contra que archivo.** El catalogo pasa a **27 tipos** —los 18 de siempre mas los 9
que faltaban—, con **27 formularios**, uno por tipo, y el radio poblado en los 27. Eso esta en
`BD/Modelo_Datos_PLANTILLA.xlsx` desde el 2026-08-10, generado por `scripts/generar_plantilla.py`.
Durante un dia convivieron dos hojas, una con 18 tipos y otra con 27, y eso hizo que un mismo «18»
fuera correcto o falso segun de cual hablara la frase. **Desde el 2026-08-10 hay una sola**, con 27:
si un documento vigente dice 18, esta desactualizado.

**Lo que hay que preguntarse ante una referencia que resuelve:** no «apunta a algo», sino **«apunta
a lo correcto»**. Lo primero lo dice un verificador; lo segundo hay que derivarlo del dominio.

## 7.11 Un aviso que no vence es ruido (regla nueva, 2026-08-10)

`USR_Usuarios.SedeID` estuvo cuatro dias declarada `Ref` obligatoria en el modelo mientras
`FUNCIONAL_SGMC` 6.3 la daba por descartada. La fuente se contradecia consigo misma y **nadie lo
vio**.

**Lo incomodo es que si se vio.** `D-04` lo detectaba en cada ejecucion y lo imprimia:

```
- [D-04] USR_Usuarios.SedeID se descarto y sigue viva. Programada para retirarse en paso 1
```

La regla funcionaba. Lo que fallaba era **la valvula de escape**: bastaba escribir `'paso 1'` para
que el fallo bajara a aviso, y esa marca no tenia fecha ni dueno. Sin fecha, un aplazamiento no
vence: se queda entre los avisos que uno aprende a saltarse. Lo encontro una persona leyendo, que es
justo lo que este proyecto lleva dias intentando dejar de necesitar.

**La regla: todo aplazamiento lleva fecha, y el dia que pasa vuelve a ser fallo.** `D-04` ya no
acepta una marca sin `AAAA-MM-DD`. Al endurecerla salieron **otras dos** con el mismo vicio,
`ACT_Activos.FrecuenciaID` y `TIP_TiposActivo.FormularioID`, que llevaban ahi lo mismo.

**Y el corolario, que vale para las cinco reglas de `verificar_documentos` y las diecinueve de
`verificar_faseA`:** un aviso que nadie va a atender no es informacion, es ruido, y el ruido tapa lo
que si importa. Si algo merece un aviso permanente, no merece un aviso: merece estar resuelto o
tener fecha. **Preferir siempre endurecer a silenciar** — es la misma regla de 3 sobre no retirar
una comprobacion, aplicada a su version blanda.

## 7.12 AppSheet adivina el tipo de CADA columna, no solo el de la clave (2026-08-10)

`F-20` nacio de descubrir que AppSheet tipa la **clave** segun la mayoria de sus valores. Al abrir
el editor se vio que hace lo mismo con **todas** las columnas, y que la hoja no manda nada:

```
TramoINVIAS        Number   el unico valor es 5607, asi que parece numero
SedeID             Number   el modelo la declara Text
Ubicacion          Text     es una coordenada
UnidadFuncionalID  Number   tiene que ser Ref
```

Ese volcado es **literal del editor aquel día** y por eso conserva `Ubicacion` a secas. **La columna
se llama hoy `Ubicacion_LatLong`**: al buscarla en el editor, busca el nombre nuevo. Se deja el
transcrito sin retocar porque falsearlo destruiría lo único que prueba —qué vio AppSheet—, pero un
nombre viejo dentro de una cita sigue mandando a la gente a una columna que ya no existe.

**El peor es `TramoINVIAS`.** Los tramos de INVIAS de este corredor son `55CN03`, `5607` y `5608`.
Dos de los tres son numeros y uno no. Como el unico dato cargado hoy es `5607`, AppSheet la tipa
`Number` — y el dia que operacion escriba `55CN03` no cabe, sin que nada explique por que.

**La regla: subir el Excel arregla la hoja, no la aplicacion.** Son dos sitios. El Excel fija las
columnas y los datos; el tipo de cada columna, cual es la clave y que es una referencia viven en el
esquema de AppSheet, que se **infiere de los datos** y hay que corregir a mano. Por muchas veces que
se reimporte, la inferencia sera la misma porque los datos son los mismos.

**Corolario para el modelo:** una columna cuyo dominio mezcla valores numericos y alfanumericos es
una trampa aunque hoy solo tenga cargados los numericos. Al declararla, dejar dicho el tipo y por
que —lo hace `MANUAL_DESPLIEGUE.md`, ficha por tabla— y comprobarlo en el editor, columna a columna,
porque **el defecto no se ve en la hoja: se ve en la aplicacion**.

## 7.13 Una regla puede estar puesta y no hacer nada (regla nueva, 2026-08-10)

Es lo que más veces ha fallado, y siempre en silencio. **Configurada, bien escrita, sin dar un solo
error, y sin efecto.** Tres casos el mismo día, cada uno por un motivo distinto:

| | Por qué no hacía nada |
|---|---|
| `RG-03` | su columna era `Text` y comparaba contra el booleano `TRUE` |
| `RG-06` | `EST_Activo.GeneraAlerta` estaba vacía en los cuatro estados |
| `RG-02` | `USERLOCATIONACCURACY()` **no existe en AppSheet** |

**`verificar_datos.py` caza el segundo caso** desde que existe `G-05`: cruza el alcance real de las
23 reglas —por `(tabla, columna)`, con `scripts/alcance_reglas.py`— contra los datos, y dice cuáles
leen una columna vacía.

**Y el alcance hay que preguntárselo a `alcance_reglas.py`, no al nombre de la columna.** Los
generadores atribuían las reglas **por nombre suelto**: como `[Activo]` aparece en `RG-04` y en
`RG-16`, las 23 columnas llamadas `Activo` de 23 tablas distintas salían con esas dos reglas encima,
y daban **94** columnas «con regla» donde de verdad hay **39 de 211**. Una expresión se lee **desde
la tabla de su regla**, y los puntos saltan siguiendo las referencias; dentro de un
`SELECT(Tabla[…], …)` el contexto cambia. Esa atribución es lo que **ordena el trabajo del
ejecutor**, así que inflarla no es cosmética: convierte la prioridad en ruido.

**`G-04` es el hermano de `G-05`**: caza las tablas que llegaron **vacías y tipadas a ciegas**,
donde AppSheet eligió el tipo de cada columna sin un solo dato. Son las ocho de movimiento, y su
aviso dice en voz alta que el archivo las vacía por diseño (7.15).

Los otros dos **solo se ven mirando**. El tipo vive en el editor y la API v2 devuelve filas, no
esquema; la función es un hecho de la plataforma. No se anuncian como cubiertos.

**La consecuencia práctica:** «la puse» no es «hace algo». Antes de contar una regla como hecha,
`python scripts/verificar_datos.py` y el cotejo del tipo de las columnas que toca.

## 7.14 Declaramos atributos que la plataforma decide (regla nueva, 2026-08-10)

`MODELO` guarda `nombre`, `tipo`, `pk`, `ref`, `obligatoria`, `editable` y —hasta hoy— ni siquiera
`Label`, todos con la misma apariencia. **No son lo mismo.** `nombre` se cumple solo, porque
`generar_plantilla.py` lo escribe en la cabecera de la hoja. Los demás son deseos que alguien tiene
que ir a instalar a mano en el editor.

Cada vez que se escribe un atributo en `MODELO` **sin escribir al lado quién lo hace cumplir**, se
ha declarado un deseo y se ha guardado donde se guardan los hechos. Las tres facturas del día:

- **`tipo`**: 107 columnas necesitan mano, y el encargo nombraba 61. Lo resuelve
  `scripts/inferencia.py`, que clasifica las 211 por quién consigue el tipo.
- **`pk`**: las 8 tablas vacías se quedaron con `_RowNumber` de clave, y solo 3 avisan —las que
  tienen hijas—. Las otras 5 fallan en silencio.
- **`Label`**: no lo declaraba nadie. Es lo que el técnico ve en los 39 desplegables, y AppSheet
  elegía la primera columna de texto, que casi siempre es la clave.

`scripts/lectura_de_vuelta.py` dice, por clase de cambio, quién lo comprueba: **tres tienen comando
—`referencias`, `datos`, `estructura`— y cuatro no tiene nadie —`tipos`, `expresiones`, `permisos`,
`etiqueta`—**. Un paso sin comprobación declarada se lee como comprobado.

**Y `scripts/navegacion_editor.py` dice dónde está cada cosa en pantalla**, que es la otra mitad del
mismo problema: los encargos decían **qué** poner y no **dónde**. Los nombres de las reglas **no son
los de los controles**. `Required_If` se llama **`Require?`** y **no es una casilla que se marque**:
hay que pulsar el icono `=` de al lado. El 2026-08-10 acabó escrita en `Valid If`, que la habría
vuelto imposible de guardar.

## 7.15 Un instrumento que miente por diseño (regla nueva, 2026-08-11)

**`generar_plantilla.py` vacía a propósito las ocho tablas de movimiento cada vez que corre.** Son
registros de prueba y la plantilla es lo que recibe el funcional, así que vaciarlas es correcto.
Están declaradas en `scripts/lectura_de_vuelta.py` como `VOLCADO_CIEGO_A`:

```
OT_OrdenesTrabajo · MAN_Mantenimientos · CHK_Checklists · CHD_ChecklistDetalle
FOT_Fotografias   · FIR_Firmas         · NOV_Novedades  · PLA_PlanMantenimiento
```

**La consecuencia no estaba escrita en ninguna parte, y anula pruebas enteras.** `verificar_faseA.py`
y `verificar_datos.py` leen `BD/Modelo_Datos_PLANTILLA.xlsx` por defecto. Una fila creada **en la
aplicación** —un fixture, una orden real— **nunca llega a ese archivo**. Cualquier comprobación que
espere verla ahí **no puede dispararse jamás**, y pasa en verde **por no ejercitarse**. Lo encontró
el arquitecto sobre `PRUEBA-004`: dos de sus pruebas eran imposibles de fallar y de pasar.

**La regla: un instrumento cuyo silencio es indistinguible del acierto tiene que decirlo él mismo.**
No basta con que alguien lo sepa: quien lo sabía escribió las pruebas igual. Por eso `G-04` no dice
solo «llegó vacía», dice **«este archivo la vacía POR DISEÑO, así que aquí saldrá vacía aunque la
aplicación tenga filas»** y nombra el instrumento que sí ve —`instantanea.py`, que lee por API—.

**Para mirar datos de movimiento: `python scripts/instantanea.py`**, o se descarga el Sheets a un
archivo aparte y se le pasa por argumento al verificador. El volcado sirve para estructura y
catálogos, no para esto.

**Es la misma forma que `FILTROS_AL_FINAL`**, en ese mismo módulo: poner los `Security Filter` deja
ciegos a `instantanea.py` y a `auditar_cableado.py` sobre las tablas filtradas. No es que esté mal:
es que **deja de poderse ver**, y eso se lee igual que «está bien» si nadie lo dice. Cuando un
instrumento se apaga, hay que apuntarlo donde se apunta el estado, no donde se apunta el código.

## 7.16 Una regla declarada dos veces, y con expresiones distintas (regla nueva, 2026-08-11)

Una regla puede estar escrita en **dos sitios**: en la columna —`formula`, `valid_if`,
`valor_inicial`— y en `REGLAS`. Cuando divergen, **cada consumidor lee una cosa distinta y nadie lo
nota**. `V-18` de `validar_modelo.py` lo comprueba desde el 2026-08-10.

Pasó con `RG-19` y era el único caso. La columna decía `[Precision_GPS] > LOOKUP("UMBRAL_GPS", …)` y
`REGLAS` decía `OR(ISBLANK(LOOKUP(…)), [Precision_GPS] > LOOKUP(…))`. **No es un matiz**:
`RECONSTRUCCION_EXPRESIONES` —lo que el ejecutor teclea— toma la de `REGLAS`, la del `OR`. Sin la
guarda la regla es falsa siempre; **con** la guarda es falsa solo mientras exista la fila
`UMBRAL_GPS`, y **hay dos cuentas con permiso de edición sobre el Sheets**. Borrar esa fila habría
puesto `CierreConExcepcion` en `TRUE` en todos los cierres.

`V-18` compara **solo la propiedad que corresponde al tipo de la regla**. Compararlas todas daba un
falso positivo inmediato —`RG-01` es un `Valid_If` y la misma columna tiene `HERE()` de valor
inicial, que es otra propiedad—, y **un falso positivo en un gate que bloquea el despliegue enseña a
desactivarlo**.

**Y el corolario, que es el mismo agujero visto desde el otro lado: `V-11` ahora recorre también las
columnas.** Antes solo miraba `REGLAS`, mientras `V-17` sí recorría las dos — y **esa asimetría era
el agujero**: una expresión escrita en el `formula` o el `valid_if` de una columna **no se validaba
en absoluto**. Lo demostró el arquitecto metiendo en una columna la peor expresión posible
—desreferenciar un `Yes/No` y nombrar una columna que no existe, los dos defectos que `V-11` nació
para cazar—: el validador respondió `APTO PARA DESPLEGAR`. La misma expresión dentro de `REGLAS`
daba dos errores.

Con eso, `V-11` pasa a recorrer las **54 expresiones que el modelo declara en una columna** —de las
que **49 no tienen `REGLA` propia**, y por eso no salen en `RECONSTRUCCION_EXPRESIONES` ni en
`PROMPT_EXPRESIONES`, que se generan recorriendo `REGLAS`—. Se cuentan:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;print(sum(1 for t in MODELO for c in MODELO[t]['columnas'] for k in ('valid_if','formula','valor_inicial') if c.get(k)))"
```

**`V-11` ampliada no caza nada hoy**, y eso es lo correcto: los tres `formula` / `valid_if` que hay
en una columna tienen todos su regla, así que ya se validaban. **Entró antes de que hubiera qué
cazar.** Una comprobación que se añade después del primer defecto llega tarde por definición.

## 8. Deriva documental: ahora es mecanica

Este archivo llevaba una lista escrita a mano de contradicciones conocidas entre documentos. Esa
lista envejecia igual que lo que denunciaba.

**Desde el 2026-08-07 la comprueba `scripts/verificar_documentos.py`**, que lee toda la prosa y la
cruza contra `modelo_objetivo.py`:

```
D-01  toda tabla citada existe en MODELO, RETIRADAS o PROPUESTAS
D-02  ninguna tabla PROPUESTA existe ya en MODELO
D-03  toda referencia Tabla.Columna apunta a una columna real
D-04  ningun mecanismo descartado en DECISIONES sigue vivo sin fecha de retiro
D-05  toda tabla del modelo la menciona algun documento
```

En su primera ejecucion encontro que `ESPEC-003` habia inventado dos tablas con nombres distintos de
los ya declarados, que `CHK_Checklists.OTID` no existe —esa tabla cuelga de `MantenimientoID`— y que
cuatro documentos la citaban. Ninguna de las tres la habia visto nadie leyendo.

**Lo que NO comprueba:** si la prosa es cierta. Solo si sus nombres existen. Un documento puede
pasar las cinco reglas y estar equivocado; por eso sigue haciendo falta el arquitecto.

Un documento que menciona un nombre **para descartarlo** lo declara con una linea
`<!-- verificar_documentos: ignorar NOMBRE -->`. Es incomoda a proposito: si aparece en muchos
sitios, el problema es el criterio y no el documento.

## 9. Estructura del repositorio

```
ESTADO.md          Dónde vamos y qué falta. La verdad del estado
README.md          Entrada: qué es el proyecto y cómo funciona
CLAUDE.md          Este archivo
MAP.md             Índice maestro y referencias cruzadas

BD/                Modelo_Datos_PLANTILLA.xlsx: el entregable, generado del
                   modelo. Es el único archivo de datos del repositorio
docs/              Documentación técnica y funcional (.md)
  sdd/             Artefactos del pipeline: ESPEC, PRUEBA y RECONSTRUCCION
  images/          Figuras de los documentos (fig_01 a fig_07)
Manuales/          MANUAL_DE_USUARIO.md
scripts/           Fuente del modelo, validadores y generadores
                   sistema.py declara la aplicacion y la hoja vigentes
                   lectura_de_vuelta.py declara quien comprueba cada cosa,
                   y VOLCADO_CIEGO_A: las 8 tablas que el volcado vacia
                   navegacion_editor.py, donde esta cada control en pantalla
                   alcance_reglas.py, que columnas toca de verdad cada regla
contexto/          Material de contexto operativo. No es la vara
archivo/           Material de origen. No versionado (en .gitignore)
```

Reglas de ubicación al crear archivos:

- Un `.md` de documentación va en `docs/`. Solo ESTADO, README, CLAUDE y MAP viven en la raíz.
- Un `.py` va en `scripts/` y resuelve sus rutas desde la raíz del repositorio con
  `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`. Nunca rutas absolutas `D:\`.
- Las figuras de un documento van en `docs/images/`.
- Todo documento nuevo se enlaza en `MAP.md` y en la tabla de `README.md`.

### 9.1 Qué se retira, y cómo (regla reescrita el 2026-08-10)

**Antes esta regla decía «nada se borra: se mueve a `docs/historico/`».** Sonaba prudente y salió
cara. En cuatro días esa carpeta juntó 26 documentos que describían aplicaciones y hojas
abandonadas, con enlaces vivos apuntando a ellos desde documentos vigentes. Quien llegaba no podía
distinguir el sistema de sus tres versiones anteriores, y lo dijo con estas palabras: **«cuando leo
los documentos principales, siguen locuras y legacy»**.

**El error era creer que la preservación necesita una carpeta. La hace git.**

- **Antes de una limpieza grande, una etiqueta.** `git tag -a <nombre> -m "<qué contiene>"`. Eso
  convierte el borrado en reversible con un comando, y es lo que permite limpiar de verdad en vez
  de acumular. La del punto de partida es `antes-de-la-limpieza-2026-08-10`.
- **Después, se borra.** Un documento que describe un sistema que ya no existe no se archiva: se
  quita del árbol de trabajo. Su valor histórico ya está en la etiqueta.
- **Y se arreglan los enlaces**, que es la parte que nadie hace. `verificar_enlaces.py` la vuelve
  mecánica: no se cierra una retirada mientras no diga `TODOS LOS ENLACES RESUELVEN`.

**Lo que sí se conserva en el árbol es la lección, no el documento.** Por qué se abandonó algo vale
más que el algo: vive en `ESTADO.md` §6 y en las secciones 7.x de este archivo.

### 9.2 Los identificadores viven en un solo sitio

**`scripts/sistema.py` dice cuál es la aplicación y cuál es la hoja.** Nada más lo dice.

Estaban escritos a mano en 37 documentos y 10 scripts. El sistema se reconstruyó tres veces en
cuatro días, y cada vez había que perseguirlos uno por uno: nunca se perseguían todos. El resultado
fue cinco aplicaciones y tres hojas mencionadas por el repositorio, con la portada ofreciendo un
enlace que daba 404.

- **Un generador nunca escribe un identificador a mano.** Lo pide a `sistema.py`.
- **Un `.md` vigente que nombre una aplicación o una hoja que no sea la de `sistema.py` está
  desactualizado**, o habla del pasado y entonces tiene que decirlo en la misma frase.
- Las superadas están en `SUPERADOS`, con el motivo por el que dejaron de serlo. **No se borran de
  ahí:** son lo que hay que reconocer para poder descartarlo.

## 10. Alcance y método de construcción

> **CORRECCIÓN DEL 2026-08-07.** Este apartado afirmaba que el agente no tenía acceso al editor de
> AppSheet ni al Sheets de producción. **Es falso.** El 6 de agosto de 2026 se agregaron
> `Coordenadas_Cierre_LatLong` y `Precision_GPS` al Sheets y se ejecutó *Regenerate Structure* en AppSheet.
> El acceso existe y ya se usó.

El acceso existe, pero es **caro y frágil**: manejar el editor de AppSheet clic a clic consume
muchos tokens, los desplegables no siempre abren y el viewport cambia de tamaño entre llamadas,
desplazando las coordenadas. Por eso el acceso no es la vía por defecto sino el último paso de un
pipeline.

### Nada se ejecuta contra producción sin las tres firmas

El método vigente es SDD, descrito en `docs/SDD_PIPELINE_SGMC.md`. Cinco agentes en
`.claude/agents/`, y un gate antes del paso caro:

| # | Agente | Produce | Toca producción |
|---|---|---|---|
| 1 | `sgmc-especificador` | `ESPEC-NNN` contra el archivo, no contra otro documento | No |
| 2 | `sgmc-verificador` | `PRUEBA-NNN`: positiva, negativa y lectura de vuelta | No |
| 3 | `sgmc-arquitecto` | Veredicto adversarial. Presunción de rechazo | No |
| 4 | `sgmc-ejecutor` | Aplica en Sheets y AppSheet | **Sí** |
| 5 | `sgmc-probador` | `ACTA` con el resultado real, pase o falle | Lectura |

**`python scripts/validar_modelo.py` en 0 errores es el único gate objetivo.** Si devuelve errores,
no hay veredicto que valga.

Pasa por el pipeline todo lo que escriba en el Sheets de producción, en el editor de AppSheet o en
`scripts/modelo_objetivo.py`. No pasan las correcciones de redacción, las auditorías de solo
lectura ni los cambios en `scripts/` que no alteren el modelo.

### Fuera de alcance

**El código QR, por decisión del 2026-08-07.** Primero tiene que funcionar el ciclo básico. El
activo se abre por lista, no por escaneo, y `OrigenApertura = Lista` deja de ser una excepción.
Detalle y consecuencias en `docs/SDD_PIPELINE_SGMC.md` sección 8.
