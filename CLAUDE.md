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

- Aplicación: AppSheet `SGMC-886843353` (app en vivo, enlaces en `README.md`)
- Backend de producción: Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`
- Repositorio remoto: `github.com/dieleoz/SGMC`

## 2. Dónde está la verdad

**La fuente única es `scripts/modelo_objetivo.py`.** De ahí se generan el diccionario de datos, el
manual de despliegue y la lista de reposición. Nada se documenta a mano.

**El dato vive en Google Sheets** y se verifica descargándolo a `BD/` y corriendo
`verificar_faseA.py`. La hoja vigente es `Modelo_Datos_09082026`, propiedad de la Concesión: 32
pestañas, ninguna oculta, `FASE A CERRADA`.

### La divergencia de agosto está cerrada

Durante días el Excel local y el Sheets de producción fueron modelos distintos, y esa brecha causó
media docena de hallazgos. **Convergieron el 2026-08-07**: los dos tienen hoy 32 pestañas y el
mismo esquema.

Lo que queda de aquello son tres reglas que siguen valiendo:

- **Antes de afirmar algo sobre el modelo, declara contra qué archivo lo verificaste.**
- **Al leer un `.xlsx` con `openpyxl`, `data_only=True`** o estarás leyendo fórmulas en vez de
  valores. Y al revés para detectar fórmulas: hacen falta dos libros abiertos del mismo archivo.
- **Lo que el modelo declara y el archivo no tiene, es deriva.** `F-18` la caza para pestañas
  ocultas y `F-19` para columnas retiradas que ya no existen. Las dos nacieron de fallos reales.

## 2.1 Propiedad y edición del backend

El Sheets de producción es propiedad de `[correo del Propietario]`. el Propietario de la Aplicación es el
desarrollador y product owner, y **hay una entrega planificada** a la Concesión una vez recibido el
sistema. No es una falla de gobierno: es un paso de transición con responsable.

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
como supuesto, en la tabla del final de ese documento.

- **No declares nada conforme por reporte. Verifícalo contra el archivo.** Vale también para los
  informes de otros agentes, incluidos los que te dan la razón: el arquitecto propuso una lista de
  catálogos con clave legible que incluía siete tablas **numéricas**. Se detectó volcando la
  primera columna de las 31 hojas, no leyendo con más atención.
- Para el Excel, usa `openpyxl` (disponible, 3.1.5) y muestra el dato leído, no un resumen.
- Distingue siempre **estructura** de **población**: que exista la columna no significa que el
  campo tenga datos, y que la tabla exista no significa que el flujo se haya ejercitado.
  Cuatro tablas del modelo están hoy vacías (`MAN_Mantenimientos`, `FOT_Fotografias`,
  `FIR_Firmas`, `GPS`).
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

Advertencia sobre claves: la nomenclatura **no** es uniforme. `OT_OrdenesTrabajo` no tiene columna
`OTID`; su primera columna es `Numero_OT` con valores `OT-0001`. Otras tablas referencian `OTID`.
Verifica la clave real antes de asumirla.

## 6. Referencias: las reglas que gobiernan el cableado

El defecto raíz del sistema no es que falten columnas. Es que las que existen son texto.
`MAN_Mantenimientos.OTID` se llama como una referencia y figura como referencia en el diccionario,
pero AppSheet responde `Invalid dereference. Column OTID is not a Ref`. De ese único hecho cuelgan
el geofencing, la navegación padre-hijo y todo reporte por activo.

El procedimiento vigente está en `docs/sdd/ESPEC-002-cableado-en-appsheet.md`, con sus pruebas en
`PRUEBA-002`. Aquí van las reglas que no se negocian.

**R-1. Una referencia guarda el valor de la clave del destino.** De ahí todo lo demás. Antes de
cablear una referencia, verifica cuál es la clave real de la tabla destino: no la supongas por el
nombre. `OT_OrdenesTrabajo` tiene hoy la clave `Numero_OT`, no `OTID`.

**R-2. Renombrar y retipar son la misma tarea, no dos.** Si la clave se llama `Numero_OT` y quien
la apunta se llama `OTID`, no hay contra qué resolver. Por eso el renombrado no es cosmético y no
se pospone.

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
`[OTID].[ActivoID].[Ubicacion]` sobre `MAN_Mantenimientos` y ver que resuelve es la prueba de que
la referencia quedó. Es más rápido y más seguro que ejercitar la app.

**R-10. Un `Ref` guarda la clave, no el nombre — pero no toda comparación contra un literal está
mal.** `[EstadoActivoID] <> "Retirado"` es siempre cierto, porque `EST_Activo` tiene la clave `1..4`
y el texto vive en `Nombre`. Se escribe `[EstadoActivoID].[Nombre]`. **En cambio
`[EstadoOrdenID] = "Cerrada"` es correcto**, porque `EOT_EstadosOrden` tiene la palabra como clave,
por diseño (R-8). La distinción está en `CLAVE_LEGIBLE` de `scripts/modelo_objetivo.py`: las 10
tablas cuya clave es texto legible, **derivadas del archivo y no de una impresión**. La regla V-17
lo comprueba.

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

Geofencing de cierre, RG-01 (RF-012). `ACT_Activos` guarda un único campo `Ubicacion` de tipo
LatLong; no existen columnas `Latitud`/`Longitud` separadas. El radio sale del tipo de activo,
porque una subestación y un poste SOS no admiten la misma tolerancia:

```
DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
```

Mensaje de error, en texto plano:

```
Ubicación fuera de rango: debe estar junto al activo para cerrar.
```

Mientras `TIP_TiposActivo.RadioGeofencingKm` no exista o esté vacío, usar el literal `1.0` y
anotarlo como provisional.

Son incorrectas contra este modelo, y fallan en ejecución, todas estas variantes:

| Variante | Por qué falla |
|---|---|
| `[ActivoID].[Ubicacion]` desde `MAN_Mantenimientos` | Esa columna se retira: el activo va por la orden |
| `LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])` | No existen columnas de latitud y longitud separadas |
| `[OTID].[Activo].[Ubicacion]` | `Activo` es el nombre **anterior** al renombrado. Después de migrar apunta a la bandera `Yes/No` |

Security Filter por sede (RG-04, RF-004): filtra `ACT_Activos` por las unidades funcionales
asignadas al usuario resuelto vía `USEREMAIL()`. No por `SedeID`, que es donde trabaja la persona
y no donde está el activo; esa confusión es la que dejó a usuarios y activos en conjuntos
disjuntos.

**El cableado no basta para que el geofencing funcione.** Los 34 activos comparten la coordenada
`4.728512, -74.114531`, en Bogotá. Hasta que se carguen coordenadas reales (D-01), cualquier cierre
en la vía queda fuera de rango y cualquier cierre en Bogotá queda dentro.

## 7. Estado: no vive en este archivo

El estado del proyecto cambia cada semana y este archivo son **reglas**, que no cambian. Mezclarlos
hizo que durante dos dias `CLAUDE.md` describiera una Fase 0 abierta que ya se habia cerrado.

| Que quieres saber | Donde esta |
|---|---|
| En que fase vamos y que sigue | `docs/ROADMAP.md` §2, orden de implementacion |
| Que hace el sistema, para quien y como | `docs/FUNCIONAL_SGMC.md` |
| Que tiene la hoja hoy, columna a columna | `docs/bd.md`, **generado** |
| Por que se cerro cada fase | `docs/sdd/ACTA-00N-*.md` |

Para comprobar la hoja en cualquier momento: *Archivo → Descargar → Microsoft Excel*, guardar en
`BD/` y correr `python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"`. **No cierres nada
por el reporte de quien lo aplico**, ni siquiera por el tuyo.

## Método de trabajo vigente: construir bajo supuestos

El enfoque de preguntar primero al líder funcional **está descartado**. El documento de las 14
decisiones ya se envió y no se reenvía, pero no se espera su respuesta para avanzar.

Los catorce supuestos están adoptados en `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` y son **vinculantes
hasta que el campo los desmienta**. Trabaja con ellos. No abras un punto para consultarlo: si
falta una definición, adóptala como supuesto, decláralo y sigue.

La razón es doble. Un cuestionario en abstracto a quien todavía no tiene el modelo mental produce
silencio o un "de acuerdo" a todo, que simula una decisión inexistente. Y el sistema actual no
permite formarse criterio: cuatro tablas vacías, un formulario de dieciocho y ninguna transacción.
Una suposición escrita y probada se corrige en una tarde; una pregunta sin responder bloquea
semanas.

La directiva de ejecución es `docs/prompts/PROMPT_CONSTRUCCION_SGMC.md`.

## Para qué existe el sistema

Antes de decidir nada, ancla contra esto:

> Garantizar que el mantenimiento se hizo, que quien lo hizo estuvo físicamente frente al equipo,
> y que la evidencia que lo respalda es difícil de falsificar.

Todo lo demás sirve a eso o sobra. La presencia se garantiza encadenando evidencias
independientes: escaneo del QR físico con hora y coordenada, fotografías tomadas con la cámara de
la app y no de la galería —cada una con su propia coordenada—, cierre dentro del radio del activo,
y marca de tiempo del servidor y no del teléfono. La cadena no es infalsificable: eleva el costo
de falsificar por encima del de hacer el trabajo, que es el objetivo realista.

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

Lo que sí está verificado como resuelto: `Coordenadas_Cierre` y `Precision_GPS` existen en
`MAN_Mantenimientos`; la columna `Observaciones` ya no está duplicada (24 columnas únicas).

## 7.4 Los tres verificadores, y qué mide cada uno

Ninguno sustituye a otro. Los tres se corren antes de dar nada por cerrado.

| Script | Mide | Cuándo falla |
|---|---|---|
| `validar_modelo.py` | El modelo consigo mismo: tipos, claves, rutas de desreferencia, reglas | Siempre. Es el único gate objetivo del pipeline |
| `verificar_faseA.py` | El modelo contra **la hoja descargada** | Al cerrar una fase de datos |
| `verificar_documentos.py` | **La prosa** contra el modelo | Al escribir o tocar cualquier `.md` |

**Lo que ninguno mide es si algo es buena idea.** Para eso está el arquitecto, y por eso su
veredicto no se sustituye por «los scripts pasan».

## 7.9 Una instruccion que exige criterio se ejecuta mal (regla nueva, 2026-08-09)

El manual de despliegue decia «oculte las 47 columnas retiradas» y «las 3 columnas trampa». **Quien
lo ejecuta no tiene el modelo delante**, asi que dedujo. Resultado: cableo `CHK_Checklists.ActivoID`
como referencia —es una trampa, habia que ocultarla— y propuso `Abierto / En Proceso / Completado`
como valores de `NOV_Novedades.Estado`, que el modelo declara `Reportada / Aceptada / Descartada`.

**Ninguno de los dos errores es del ejecutor. Son del documento.**

Y las trampas son **tres**, derivadas del archivo. Las conte de memoria en vez de derivarlas.

**Regla: todo documento operativo lleva la lista completa, generada.** Si una instruccion dice «las
retiradas», «las trampa» o «los valores correspondientes», esta mal escrita. El anexo de
`MANUAL_DESPLIEGUE.md` es el patron: **ficha por tabla, columna por columna, sin nada que deducir.**

**Y el corolario que falta:** hoy el modelo describe datos, no interfaz. `VISTAS`, `ACCIONES` y
`SLICES` no existen en `modelo_objetivo.py`, asi que el paso de vistas del manual sigue siendo
«se construye sola» — exactamente la clase de instruccion que esta regla prohibe.

## 7.7 Una lista es correcta para UN punto de partida (regla nueva, 2026-08-09)

`ESPEC-002` lista **15 columnas** que pasan a `Ref`. Es correcto: quedaban 15 por convertir en la
aplicación existente, donde otras 23 ya estaban puestas.

**Al reconstruir la aplicación desde cero, no sobrevivió ninguna: eran 38.** Y siguiendo la
especificación al pie de la letra, `OT_OrdenesTrabajo.ActivoID` quedó en `Number`, de modo que
`[OTID].[ActivoID].[Ubicacion]` —la desreferencia que la propia especificación usa como prueba— no
resolvía.

**El documento no mentía. Le faltaba declarar desde dónde se parte.**

De ahí dos reglas:

**Toda lista derivada declara su punto de partida.** «15 columnas pendientes» solo significa algo
respecto a un estado concreto. Sin esa referencia, la lista se aplica a un estado distinto y produce
un resultado incompleto que nadie detecta.

**Cuando una especificación y `modelo_objetivo.py` discrepan, manda el modelo.** La especificación
se generó de él en un momento dado; el modelo es lo que hay. `MODELO` tiene 38 columnas con `ref=`,
y ese número no opina:

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
ninguna parte y hay que estimarlo: 27 columnas renombradas, 8 tablas nuevas y 45 campos retirados
estaban muy por encima.

## 7.5 Una sola forma por propósito (regla nueva, 2026-08-07)

**Riesgo real, señalado por operación:** con tanto material acumulado —siete documentos de
contexto, once rondas de revisión, tres actas—, es fácil **proponer dos mecanismos para lo mismo** y
que alguien implemente los dos. Eso ya pasó: `Requiere_Repuesto` y `MotivoPendienteID` registraban
el mismo hecho; el manual de usuario describe un bypass de GPS por nota libre mientras el modelo
tiene `CierreConExcepcion`.

**Antes de proponer un mecanismo, comprueba si ya existe uno para ese propósito.** El registro está
en `docs/FUNCIONAL_SGMC.md` §6. Si existe, se usa el que está; si el nuevo es mejor, se retira el
viejo **en el mismo cambio** y se anota en esa tabla. Nunca conviven los dos.

Ese mismo hábito evita el error inverso, que también ocurrió: **proponer como nuevo algo que ya está
en el modelo.** `ROL_Roles` y las cuatro tablas de plantilla de checklist —`FRM_Formularios`,
`FRM_Secciones`, `FRM_Preguntas`, `TPR_TiposRespuesta`— ya existían cuando se propusieron como
tablas a crear. **Vuelca `MODELO` antes de proponer una tabla.**

## 7.6 Los documentos de contexto no son la vara

`contexto/` contiene siete documentos. **Tres no son del Sisga**: el PDF de ETRA y el informe de
enero de 2025 son del corredor Neiva–Girardot, y la propuesta de la manta es de INDRA en otra doble
calzada. Su procedencia está etiquetada en `docs/CONTEXTO_OPERACION.md`.

**Son ejemplos que dan contexto, no obligaciones contractuales.** De ellos se copia método. Ninguna
cifra ni estructura suya se convierte en requisito del Sisga sin que operación lo confirme: entra
como **supuesto abierto**, nunca como carencia del modelo.

Este proyecto ya midió el modelo del Sisga contra la estructura de otro corredor una vez. La
advertencia de procedencia existía y contenía ella misma el error.

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
README.md          Entrada: qué es el proyecto, cómo funciona, estado real
CLAUDE.md          Este archivo
MAP.md             Índice maestro y referencias cruzadas

BD/                FUENTE DE VERDAD: Modelo de Datos (2).xlsx, 24 hojas
docs/              Documentación técnica y funcional (.md)
  images/          Figuras de los documentos (fig_01 a fig_05)
  prompts/         Directivas para agentes de auditoría
Manuales/          Manuales de usuario
  images/          Maquetas del manual (img_01 a img_06)
entregables/       Word y Excel listos para enviar al cliente
scripts/           Generadores de figuras y documentos
archivo/           Material de origen. No versionado (en .gitignore)
```

Reglas de ubicación al crear archivos:

- Un `.md` de documentación va en `docs/`. Solo README, CLAUDE y MAP viven en la raíz.
- Un `.py` va en `scripts/` y resuelve sus rutas desde la raíz del repositorio con
  `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`. Nunca rutas absolutas `D:\`.
- Un `.docx` o `.xlsx` destinado al cliente va en `entregables/`. Los manuales van en `Manuales/`.
- Las figuras de un documento van en `docs/images/`; las del manual, en `Manuales/images/`.
- Todo documento nuevo se enlaza en `MAP.md` y en la tabla de `README.md`.

## 10. Alcance y método de construcción

> **CORRECCIÓN DEL 2026-08-07.** Este apartado afirmaba que el agente no tenía acceso al editor de
> AppSheet ni al Sheets de producción. **Es falso.** El 6 de agosto de 2026 se agregaron
> `Coordenadas_Cierre` y `Precision_GPS` al Sheets y se ejecutó *Regenerate Structure* en AppSheet.
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
