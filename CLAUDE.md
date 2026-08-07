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

## 2. Dónde está la verdad: hay dos modelos y no coinciden

**Verificado el 2026-08-06: el Excel local y el Google Sheets de producción son modelos
distintos.** No es deriva menor: difieren en las tablas que más importan. Cualquier afirmación
sobre "el modelo" es ambigua hasta que declares cuál de los dos leíste.

| Tabla | `BD/Modelo de Datos (2).xlsx` (local) | Google Sheets (producción) |
|---|---|---|
| `TIP_TiposActivo.FormularioID` | Vacío en los 18 tipos | **Poblado en los 18** |
| `MAN_Mantenimientos` | 24 col, con `Coordenadas_Cierre` y `Precision_GPS` | 27 col. Las dos de GPS **se agregaron el 2026-08-06** en `Z1` y `AA1`. Ademas tiene `Diagnostico`, `Trabajo_Realizado`, `Duracion_Minutos`, `Repuestos_Utilizados`, `Requiere_Repuesto` |
| `CHK_Checklists` | 9 col, 1 fila | 21 col, 3 filas |
| `CHD_ChecklistDetalle` | 6 col, pregunta en texto libre | 21 col, **con `PreguntaID`** |
| `MAN_Mantenimientos.ActivoID` | **Existe** (columna 3), verificado el 2026-08-07 con `openpyxl` | **No existe.** AppSheet lo confirmó al rechazar la fórmula |
| `CHK.OTID` del registro `d02d8a3d` | `'1'`, huérfano | `'OT-0001'`, válido |

Hasta el 2026-08-06 en producción no existían las columnas de GPS, de modo que la regla de
geofencing ni siquiera podía configurarse. **Ya se agregaron al Sheets**, pero eso resuelve solo el
lado del dato: siguen pendientes el *Regenerate Structure* en el editor de AppSheet, el tipado de
las columnas y las reglas. Ver `docs/ROADMAP.md` sección 4.5.1.

Reglas mientras esto no se reconcilie:
- El **Sheets es el que corre la app**. El Excel es un registro paralelo que alguien ha estado
  editando por separado. Ante una discrepancia, manda producción.
- **Antes de afirmar cualquier cosa sobre el modelo, lee producción**, no el Excel. Se lee con el
  conector de Google Drive: `fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.
- Al reportar un hallazgo, escribe siempre contra cuál de los dos lo verificaste.
- No "sincronices" uno con otro sin decisión explícita: ninguno es superconjunto del otro y
  copiar en cualquier dirección destruye trabajo.
- `entregables/Modelo_Datos_SGMC_AsBuilt.xlsx` es copia byte a byte del Excel local
  (sha256 verificado). Artefacto de publicación, no una tercera fuente.

## 2.1 Propiedad y edición del backend

El Sheets de producción es propiedad de `valentinwebdeveloper@gmail.com`. Valentín es el
desarrollador y product owner, y **hay una entrega planificada** a la Concesión una vez recibido el
sistema. No es una falla de gobierno: es un paso de transición con responsable.

Nota de método: `get_file_permissions` devuelve únicamente al propietario, pero eso **no** implica
que no haya otros editores. Comprobado en la práctica: la cuenta del cliente sí tiene permiso de
edición. No infieras el nivel de acceso desde esa API.

## 3. Regla de verificación (no negociable)

Este proyecto arrastra un historial de subsanaciones reportadas como cerradas que no lo estaban.

- **No declares nada conforme por reporte. Verifícalo contra el archivo.**
- Para el Excel, usa `openpyxl` (disponible, 3.1.5) y muestra el dato leído, no un resumen.
- Distingue siempre **estructura** de **población**: que exista la columna no significa que el
  campo tenga datos, y que la tabla exista no significa que el flujo se haya ejercitado.
  Cuatro tablas del modelo están hoy vacías (`MAN_Mantenimientos`, `FOT_Fotografias`,
  `FIR_Firmas`, `GPS`).
- Al cerrar un hallazgo, deja constancia de con qué comando y qué salida lo cerraste.

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

El procedimiento completo, con su orden y su reversión, está en
`docs/CABLEADO_REFERENCIAS_SGMC.md`. Aquí van las reglas que no se negocian.

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

## 7. Estado real (verificado 2026-08-06)

La Fase 0 **no está cerrada**. `docs/ROADMAP.md` ya fue corregido; `docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md` sigue afirmando lo contrario.

**Confirmados en producción** (leídos en el Sheets, no en el Excel):

1. Los 34 activos de `ACT_Activos` comparten una sola coordenada, `4.728512, -74.114531`, que está
   en Bogotá y no en el corredor.
2. `MAN_Mantenimientos` ya tiene `Coordenadas_Cierre` (LatLong) y `Precision_GPS` (Number),
   agregadas al Sheets y reconocidas por la aplicación el 2026-08-06. **Falta la regla de
   validación**, que no pudo escribirse porque no hay ruta de referencia al activo. Ver sección 6.
2b. Las referencias del modelo no existen en la aplicación: `OTID` es `Text`, no `Ref`. Sin eso no
   hay geofencing, ni navegación padre-hijo, ni reportes por activo. **El procedimiento de
   corrección ya está escrito y validado** en `docs/CABLEADO_REFERENCIAS_SGMC.md`; falta que un
   operador lo ejecute. `MAN_Mantenimientos` tiene 0 filas, de modo que la conversión no arrastra
   datos: es el momento más barato en que se podrá hacer.
3. Solo `FRM_SOS` tiene banco de preguntas en `FRM_Preguntas` (15). Faltan 17 de 18.
4. Todos los usuarios están en `SedeID = 1`; todos los activos en `SedeID` 7 a 10. El Security
   Filter dejaría a cada técnico con cero activos.
5. `MAN_Mantenimientos`, `FOT_Fotografias`, `FIR_Firmas` y `GPS` están vacías: el ciclo nunca se
   ha ejecutado.
6. Evidencias modeladas por duplicado (campos en `MAN` + tablas hijas vacías).
7. Datos de prueba sin limpiar en `CHK_Checklists`: el registro `CHK001` trae
   `TecnicoID = "Santiago Moreno"` en lugar de un identificador y `FechaInicio = "NOW()"` como
   texto literal.

**Resueltos en producción, pendientes solo en el Excel local:** el mapeo
`TIP_TiposActivo.FormularioID`, la trazabilidad de `CHD_ChecklistDetalle` mediante `PreguntaID`, y
el checklist huérfano.

Detalle, evidencia y remediación en `docs/AUDITORIA_PLAN_Y_ROADMAP.md`.

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

## 8. Deriva documental conocida

Estos documentos contienen afirmaciones que no corresponden al archivo real. No los uses como
fuente sin contrastar:

- `docs/bd.md` — **corrección**: una revisión anterior marcó su sección 3.1 como inventada por
  describir un `MAN_Mantenimientos` de 25 columnas con `MttoID`, `Diagnostico`,
  `Trabajo_Realizado` y `Duracion_Minutos`. Estaba describiendo **producción**, y es correcta.
  Lo mismo su conteo de 21 columnas para `CHK`/`CHD`. Lo desactualizado es el Excel local.
  `bd.md` sigue sin declarar contra cuál de los dos modelos está escrito, y eso hay que corregirlo.
- `docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md` e `docs/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md` — dictaminan
  100% conforme sobre un modelo anterior y describen un mantenimiento ejecutado en vivo que no
  existe en `MAN_Mantenimientos` (0 filas).

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
