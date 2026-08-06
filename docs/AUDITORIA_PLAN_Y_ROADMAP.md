# Dictamen de auditoría: plan_de_trabajo.md y ROADMAP.md

**Proyecto:** SGMC — Concesión Transversal del Sisga S.A.S.
**Fecha:** 6 de agosto de 2026
**Alcance:** `plan_de_trabajo.md` v4.0 y `ROADMAP.md`, contrastados contra la fuente de verdad
`BD/Modelo de Datos (2).xlsx` leída físicamente en disco.
**Método:** lectura directa del archivo con `openpyxl` 3.1.5, sin capa de montaje ni caché.
No se auditó el Google Sheets de producción (fuera de alcance de acceso).

---

## 1. Dictamen

**Ninguno de los dos documentos es apto para ejecutarse tal como está.**

`ROADMAP.md` es **no conforme**: declara completada al 100% una Fase 0 y una Fase 1 que la
evidencia contradice, y pone el proyecto en Fase 1.5 (piloto de campo). Ejecutar el piloto sobre
el estado actual del modelo produce un fracaso garantizado en campo, no un hallazgo de piloto.

`plan_de_trabajo.md` v4.0 es **parcialmente conforme**: su metodología Audit-First y su fórmula de
geofencing son correctas, pero su Fase 0 está incompleta. Cubre 2 de los 8 bloqueantes reales, y
una de las dos que cubre ya estaba resuelta antes de escribirlo.

La Fase 0 no está cerrada. El piloto no debe arrancar.

---

## 2. Evidencia recogida del modelo

Verificaciones sobre `BD/Modelo de Datos (2).xlsx`:

| Verificación | Resultado |
|---|---|
| Número de hojas | 24, confirmado |
| `Modelo_Datos_SGMC_AsBuilt.xlsx` (raíz) vs `BD/Modelo de Datos (2).xlsx` | sha256 idéntico (`141880c4726a400d…`), 81 528 bytes ambos |
| `MAN_Mantenimientos.Coordenadas_Cierre` y `Precision_GPS` | Presentes |
| `MAN_Mantenimientos` columna `Observaciones` duplicada | No duplicada. 24 columnas únicas |
| `ACT_Activos.Ubicacion` (LatLong) | Presente y poblada en los 34 activos |
| Coordenadas distintas entre los 34 activos | **1 sola** |
| `TIP_TiposActivo.FormularioID` | **Vacío en los 18 tipos** |
| Formularios con banco de preguntas en `FRM_Preguntas` | **1 de 18** (`FRM_SOS`, 15 preguntas) |
| `SedeID` en `USR_Usuarios` | 1 (CCO) para los 11 usuarios |
| `SedeID` en `ACT_Activos` | 7, 8, 9, 10 (UF1–UF4) |
| Clave real de `OT_OrdenesTrabajo` | `Numero_OT`, valores `OT-0001`…`OT-0006` |
| `CHK_Checklists.OTID` | `'1'` — huérfano |
| Tablas sin datos | `MAN_Mantenimientos`, `FOT_Fotografias`, `FIR_Firmas`, `GPS` |

---

## 3. Hallazgos bloqueantes

### B-01. Geofencing inoperante: coordenada única y fuera del corredor

Los 34 registros de `ACT_Activos` tienen la misma `Ubicacion`: `4.728512, -74.114531`.
Ese punto está en Bogotá. Las sedes del corredor son Sutatenza, Machetá y San Luis de Gaceno,
a decenas de kilómetros.

Consecuencia con la regla `DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0`:
ningún técnico parado frente a un activo real podrá cerrar un mantenimiento, porque estará a más
de 1 km de la coordenada registrada. Y a la inversa, cualquiera en ese punto de Bogotá valida los
34 activos indistintamente.

La fórmula está bien. El dato está mal. Ninguno de los dos documentos lo detecta: ambos dan el
geofencing por resuelto una vez configurada la fórmula.

**No es un ajuste de configuración: es un levantamiento de campo.** Hay que capturar las
coordenadas reales de los 34 activos. Ese trabajo no está en el cronograma de ningún documento.

### B-02. `TIP_TiposActivo.FormularioID` vacío en los 18 tipos

La columna existe pero no tiene un solo valor. Es el puente que resuelve qué checklist corresponde
a cada tipo de activo. Sin él, RF-007 y RF-008 (formularios dinámicos) no pueden operar: la app no
sabe qué formulario abrir al escanear un QR.

`FRM_Formularios` sí declara los 18 formularios con IDs (`FRM_SOS`, `FRM_CCTV`, …) que mapean uno a
uno con los 18 tipos. Es una carga de 18 celdas, pero nadie la hizo y ningún documento la pide.

### B-03. Security Filter dejaría a todos los técnicos sin activos

Los 11 usuarios de `USR_Usuarios` están en `SedeID = 1` (CCO). Los 34 activos están repartidos
entre `SedeID` 7, 8, 9 y 10 (UF1 a UF4). La intersección es vacía.

Un Security Filter que restrinja `ACT_Activos` por el `SedeID` del usuario descarga **cero activos**
en los 10 celulares del piloto.

Adicionalmente, el plan y el README describen el filtro sobre las sedes `Sutatenza`,
`Peaje Machetá` y `Peaje SLG`. En `SED_Sedes`, "Sutatenza" no es un nombre de sede sino la ciudad
de la sede `CCO`. La nomenclatura del documento no corresponde al catálogo.

Falta la decisión de fondo: la sede del activo es una unidad funcional (UF1–UF4) y la del usuario
es una sede física (CCO, peajes, básculas). Son dos taxonomías distintas usando la misma columna.
Hay que definir cuál gobierna el filtro antes de configurarlo.

### B-04. Motor de formularios cubierto al 5.5 %

`FRM_Preguntas` solo contiene preguntas de `FRM_SOS` (15). Los otros 17 formularios están
declarados en `FRM_Formularios` pero sin una sola pregunta.

Nota sobre un error de diagnóstico previo: la auditoría anterior estimó "3 de 18 construidos"
contando las hojas `FRM_SOS`, `FRM_CCTV` y `FRM_PMVF`. Esas hojas son una **estructura paralela**,
no el motor. Tienen otro esquema (usan `Sección` en texto libre en lugar de `SeccionID`, y carecen
de `PreguntaID`, `VisibleSi`, `RequiereFoto`, `RequiereGPS`, `RequiereFirma`). El motor real es
`FRM_Preguntas`, y ahí la cobertura es 1 de 18.

Coexisten por tanto dos arquitecturas de formularios, y `FRM_SOS` está definido en ambas. Hay que
elegir una y eliminar la otra, o `FRM_SOS` se comportará de forma distinta según de dónde lea la app.

### B-05. Integridad referencial rota entre checklist y orden de trabajo

`OT_OrdenesTrabajo` tiene por primera columna `Numero_OT` con valores `OT-0001` a `OT-0006`.
El único checklist existente, `d02d8a3d`, referencia `OTID = '1'`. No hay ninguna OT con clave `1`.

La tarea T-00.4 del plan ("confirmar que la llave primaria sea `Numero_OT`") identifica la
ambigüedad pero se queda corta: aunque se confirme la clave, el dato existente queda huérfano.
Falta la tarea de remediar los datos, no solo de declarar la clave.

### B-06. Evidencias y GPS modelados por duplicado

`MAN_Mantenimientos` embebe `Imagen_Inicio`, `Imagen_Final`, `Firma_Tecnico`, `Firma_Supervisor`,
`Coordenadas_Cierre` y `Precision_GPS`. En paralelo existen `FOT_Fotografias`, `FIR_Firmas` y `GPS`,
las tres vacías, para lo mismo.

La tarea T-00.5 del plan ordena marcar `IsPartOf = TRUE` en `FOT_Fotografias` y `FIR_Firmas`. Esa
instrucción **presupone resuelta una decisión de arquitectura que nadie tomó** y contradice el
modelo inline que ya trae `MAN`. Ejecutarla produce doble captura: el técnico firmaría dos veces.

Además, RF-010 promete hasta 6 fotografías por mantenimiento. Los campos inline de `MAN` solo
admiten 2 (`Imagen_Inicio`, `Imagen_Final`). Si se opta por el modelo inline, RF-010 queda
incumplido; si se opta por las tablas hijas, sobran los campos de `MAN`. No hay una tercera vía.

### B-07. Ninguna transacción ejecutada: `MAN_Mantenimientos` vacía

La tabla tiene encabezado y cero filas. Nunca se ha registrado un mantenimiento.

Esto invalida el respaldo de `DICTAMEN_AUDITORIA_LOCAL_SGMC.md` e
`INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md`, que describen un flujo ejecutado y guardado en vivo.
Lo único que existe es el checklist `d02d8a3d` con 2 ítems de detalle, sin mantenimiento asociado.

En consecuencia, el geofencing, la compresión de fotos, la firma y la sincronización offline
**nunca se han ejercitado contra un dato real**. Están especificados, no probados.

### B-08. Trazabilidad del detalle de checklist

`CHD_ChecklistDetalle` guarda `Sección` y `PreguntaItem` como texto libre, sin `PreguntaID` que
apunte a `FRM_Preguntas`. El detalle no es relacional: no se puede agregar ni reportar por
pregunta, y cualquier cambio de redacción rompe la comparabilidad histórica.

---

## 4. Auditoría de `plan_de_trabajo.md` v4.0

### Lo correcto

- La metodología Audit-First y la directiva de no editar antes de diagnosticar.
- La declaración del archivo de 24 hojas como fuente única.
- La fórmula de geofencing sobre `[ActivoID].[Ubicacion]`, correcta contra este modelo.
- El mensaje de error en texto plano sin iconos.

### No conformidades

| # | Ubicación | Hallazgo | Corrección |
|---|---|---|---|
| P-1 | T-00.1 | Pide desduplicar `Observaciones`. Ya está resuelto: 24 columnas únicas. Tarea abierta sobre trabajo hecho. | Cerrar como verificada, con la evidencia |
| P-2 | Fase 0 completa | Cubre 2 de 8 bloqueantes. Faltan B-01, B-02, B-03, B-04, B-06, B-08 | Reemplazar la Fase 0 (sección 6) |
| P-3 | T-00.5 | Ordena `IsPartOf` sin haber decidido inline vs. tablas hijas; contradice el modelo de `MAN` | Convertir en decisión de arquitectura previa |
| P-4 | T-00.4 | Confirma la clave de OT pero no remedia el huérfano `OTID='1'` | Añadir la remediación de datos |
| P-5 | T-00.2 | Da por suficiente configurar la fórmula. Con una sola coordenada para 34 activos, la regla es inoperante | Condicionar a la carga de coordenadas reales |
| P-6 | Gantt | Fase 0 en 3 días (07 a 10 de agosto) y piloto el 11 | Irreal: solo B-01 y B-04 son semanas de trabajo |
| P-7 | T-02 | Nombra sedes `Sutatenza`, `Peaje Machetá`, `Peaje SLG`, que no corresponden a `SED_Sedes` ni a las sedes de los activos | Corregir contra el catálogo y resolver B-03 |
| P-8 | Todo el documento | Emojis en títulos y tareas, contra la convención de entregables | Retirar |

Observación sobre secuencia: el plan pone el piloto de campo (Fase 1) inmediatamente después de la
configuración. Falta una etapa intermedia de prueba en vivo controlada — un mantenimiento completo
ejecutado por una persona, sobre un activo con coordenada real — antes de repartir 10 celulares.
Con `MAN_Mantenimientos` vacía, el piloto sería la primera ejecución del sistema.

---

## 5. Auditoría de `ROADMAP.md`

Es el documento con mayor divergencia frente a la realidad.

| # | Ubicación | Afirmación | Realidad verificada |
|---|---|---|---|
| R-1 | Gantt y sección 1 | "Fase 0 y 1: COMPLETADO 100%" | 8 bloqueantes abiertos. Falso |
| R-2 | Gantt, `f1a` | "Modelo de Datos 17 Tablas: done" | El modelo vigente tiene 24 hojas. Obsoleto |
| R-3 | Gantt, `f1b` | "Formularios Dinámicos (18 tipos): done" | 1 de 18 con banco de preguntas, y `FormularioID` sin mapear. Falso |
| R-4 | Gantt, `f1c` | "Validaciones GPS & Security Filter: done" | GPS inoperante (B-01); Security Filter dejaría a todos sin activos (B-03). Falso |
| R-5 | Gantt, `f1d` | "Pruebas QA & Dictamen: done" | El dictamen se emitió sobre el modelo anterior; el flujo QA no dejó rastro en `MAN`. Sin respaldo |
| R-6 | Sección 1 | "Subsanaciones físicas de Excel … unificación de `FRM_Formularios`" | `FRM_Formularios` está poblada, pero sin preguntas ni mapeo desde `TIP_`. Cerrado en falso |
| R-7 | Encabezado y sección 2 | Estado actual "Fase 1.5: Grupo Piloto", con despliegue móvil `active` desde el 7 de agosto | El proyecto está en Fase 0. Arrancar el piloto quema la credibilidad del sistema ante los técnicos |
| R-8 | Sección 1 | "Geofencing GPS (RF-012): `DISTANCE() <= 1.0`" sin el operando | Fórmula incompleta; induce la variante errónea con `Latitud`/`Longitud` |
| R-9 | Todo | Emojis y semáforos decorativos | Contra la convención |

El problema de fondo del ROADMAP no es la desactualización: es que **marca hitos como cerrados
sin criterio de cierre**. No hay, para ninguna fase, una definición de qué evidencia se exige para
declararla completa. Por eso pudo pasar a "100% conforme" un modelo con cuatro tablas vacías.

---

## 6. Fase 0 corregida

Orden propuesto. Las dependencias son reales: no se puede saltar.

**Bloque A — Decisiones de arquitectura (nadie configura nada hasta cerrarlas)**

- A-1. Evidencias: inline en `MAN` o tablas hijas `FOT`/`FIR`. Si RF-010 (6 fotos) se mantiene,
  la respuesta es tablas hijas y hay que retirar los campos de imagen de `MAN`.
- A-2. GPS: `Coordenadas_Cierre`/`Precision_GPS` en `MAN` o tabla `GPS`. Recomendado: `MAN`, y
  eliminar la tabla `GPS`.
- A-3. Formularios: motor relacional `FRM_Preguntas` o plantillas planas `FRM_SOS`/`FRM_CCTV`/`FRM_PMVF`.
  Recomendado: el motor relacional; retirar las tres hojas planas.
- A-4. Semántica de `SedeID`: unidad funcional o sede física. Define el Security Filter.
- A-5. Clave de `OT_OrdenesTrabajo`: confirmar `Numero_OT` y alinear todos los `Ref`.

**Bloque B — Datos (el trabajo pesado, en paralelo con A)**

- B-1. Levantamiento en campo de las coordenadas reales de los 34 activos y carga en
  `ACT_Activos.Ubicacion`. Prerrequisito absoluto del geofencing.
- B-2. Mapeo de `TIP_TiposActivo.FormularioID` para los 18 tipos.
- B-3. Construcción de los 17 bancos de preguntas faltantes en `FRM_Preguntas`.
- B-4. Realineación de `SedeID` entre `USR_Usuarios` y `ACT_Activos` según A-4.
- B-5. Remediación del checklist huérfano `d02d8a3d` (`OTID='1'` a `OT-0001`, o su baja).
- B-6. Corrección de los encabezados con mojibake.

**Bloque C — Configuración en AppSheet (después de A y B)**

- C-1. Regla de geofencing y su mensaje de error.
- C-2. Security Filter según A-4, verificado con una cuenta real de técnico.
- C-3. `IsPartOf` y calidad de imagen, según A-1.

**Bloque D — Prueba controlada (nueva; no existe en los documentos)**

- D-1. Un mantenimiento completo de extremo a extremo ejecutado por una persona sobre un activo
  con coordenada real: apertura por QR, checklist, fotos, firma, cierre con geofencing.
- D-2. Repetición del mismo flujo en modo avión, con verificación de la sincronización posterior.
- D-3. Criterio de cierre de la Fase 0: filas efectivamente escritas en `MAN_Mantenimientos` y en
  las tablas de evidencia, verificadas leyendo el archivo.

Solo con D-3 cumplido se habilita la Fase 1 (piloto de 10 celulares).

**Estimación.** B-1 y B-3 dominan el cronograma. El levantamiento de 34 coordenadas es trabajo de
recorrido de corredor; los 17 bancos de preguntas son del orden de 250 preguntas que alguien con
criterio técnico debe redactar y validar. La ventana del 7 al 10 de agosto no es viable. El plan
debe rehacerse sobre una estimación de estas dos tareas, que solo tú o el líder funcional pueden dar.

---

## 7. Recomendaciones sobre los documentos

1. `ROADMAP.md`: revertir Fase 0 y Fase 1 a estado abierto, corregir 17 a 24 tablas, retirar el
   estado "Fase 1.5" y añadir a cada fase su criterio de cierre verificable.
2. `plan_de_trabajo.md`: sustituir la Fase 0 por la sección 6 de este dictamen; cerrar T-00.1 con
   evidencia; convertir T-00.5 en decisión A-1.
3. `bd.md`: reescribir la sección 3.1 (`MAN_Mantenimientos` real, 24 columnas) y corregir el conteo
   de `CHK`/`CHD`.
4. `MAP.md`: actualizar a 24 tablas y corregir el enlace `d.md` a `bd.md`.
5. `DICTAMEN_AUDITORIA_LOCAL_SGMC.md`: marcarlo como superado por este dictamen. Un documento que
   certifica 100% conforme un modelo con cuatro tablas vacías es un pasivo, no un activo.
6. `PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md`: su Paso 2 ordena configurar sin haber resuelto
   A-1 a A-5. Reescribirlo contra la Fase 0 corregida.

---

## 8. Reproducibilidad

La evidencia de este dictamen se reproduce leyendo `BD/Modelo de Datos (2).xlsx` con `openpyxl`.
Cualquier revisor puede rehacer las verificaciones de la sección 2 sin depender de este documento.

---

## 9. Adenda del 6 de agosto de 2026: los dos modelos no coinciden

**Alcance de esta adenda.** Las secciones 1 a 8 se elaboraron leyendo únicamente
`BD/Modelo de Datos (2).xlsx`. Ese mismo día se accedió por primera vez al backend de producción
en Google Sheets. Los dos no son el mismo modelo.

**Método.** Lectura del documento `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc` mediante el
conector de Google Drive, y contraste tabla por tabla contra el Excel local.

### 9.1 Divergencias verificadas

| Tabla | Excel local | Producción |
|---|---|---|
| `TIP_TiposActivo.FormularioID` | Vacío en los 18 tipos | Poblado en los 18 |
| `MAN_Mantenimientos` | 24 columnas, con `Coordenadas_Cierre` y `Precision_GPS` | 25 columnas, sin ninguna de las dos. Incluye `Diagnostico`, `Trabajo_Realizado`, `Duracion_Minutos`, `Repuestos_Utilizados`, `Requiere_Repuesto` |
| `CHK_Checklists` | 9 columnas, 1 fila | 21 columnas, 3 filas |
| `CHD_ChecklistDetalle` | 6 columnas, pregunta en texto libre | 21 columnas, con `PreguntaID` |
| `CHK.OTID` del registro `d02d8a3d` | `'1'`, huérfano | `'OT-0001'`, válido |

Ninguno de los dos modelos es superconjunto del otro. El Excel tiene las columnas de GPS pero no
el mapeo de formularios; producción tiene el mapeo pero no las columnas de GPS.

### 9.2 Efecto sobre los hallazgos de la sección 3

| Hallazgo | Estado tras leer producción |
|---|---|
| B-01 coordenada única en Bogotá | **Confirmado.** Los 34 activos comparten `4.728512, -74.114531` |
| B-02 `FormularioID` sin mapear | **Resuelto en producción.** Pendiente solo en el Excel local |
| B-03 sedes disjuntas | **Confirmado.** Usuarios en sede 1, activos en sedes 7 a 10 |
| B-04 un solo banco de preguntas | **Confirmado.** Solo `FRM_SOS`, con 15 preguntas |
| B-05 checklist huérfano | **Resuelto en producción** |
| B-06 evidencias duplicadas | **Confirmado** |
| B-07 cuatro tablas vacías | **Confirmado.** `MAN`, `FOT`, `FIR` y `GPS` sin registros |
| B-08 detalle sin trazabilidad | **Resuelto en producción.** `CHD` referencia `PreguntaID` |

### 9.3 Hallazgos nuevos

**B-09. Producción no tenía las columnas de GPS. SUBSANADO PARCIALMENTE el 2026-08-06.**
`MAN_Mantenimientos` carecía de `Coordenadas_Cierre` y `Precision_GPS`, de modo que la regla de
geofencing no podía siquiera configurarse.

Remediación aplicada el mismo día, con aprobación del cliente: se agregaron ambas columnas al
Sheets de producción, en `Z1` y `AA1` de la hoja `MAN_Mantenimientos`, a continuación de `Activo`.
Verificado leyendo cada celda en la barra de fórmulas, y por el cambio de `modifiedTime` del
documento a las 23:25:59 UTC.

**Queda pendiente y no debe darse por cerrado:** el *Regenerate Structure* en el editor de
AppSheet, sin el cual la aplicación no ve las columnas nuevas; el tipado de `Coordenadas_Cierre`
como `LatLong` y de `Precision_GPS` como `Number`; y la configuración de `Initial value` y
`Valid_If`. El criterio de cierre es una fila escrita desde la aplicación con valor en ambas.

**B-10. Entrega del backend pendiente.** El documento de producción pertenece a
`valentinwebdeveloper@gmail.com`. Consultado el cliente, Valentín es el desarrollador y product
owner del sistema, y existe una entrega planificada a la Concesión una vez recibido. El hallazgo se
reclasifica: no es una falla de gobierno sino **un paso de transición con responsable**, que debe
quedar con fecha en el acta.

Corrección de método: de que `get_file_permissions` devolviera únicamente al propietario se dedujo
que no había editores alternos. La deducción era incorrecta — la cuenta del cliente sí tiene
permiso de edición, comprobado al escribir en el documento. Esa API no es evidencia del nivel de
acceso de terceros.

**B-11. Datos de prueba sin limpiar.** `CHK_Checklists` contiene un registro `CHK001` con
`TecnicoID = "Santiago Moreno"` en lugar de un identificador, `ActivoID = "SOS001"` en lugar del
identificador numérico, y `FechaInicio = "NOW()"` almacenado como texto literal.

**B-12. Edición paralela sin control.** Que ambos modelos hayan evolucionado por separado implica
que no hay una regla de quién edita qué. Mientras eso siga así, cualquier corrección puede
perderse o duplicarse.

### 9.4 Corrección a la sección 7 de este dictamen

La recomendación 3 afirmaba que la sección 3.1 de `bd.md` describía un `MAN_Mantenimientos`
inexistente. Era una conclusión correcta contra el Excel local e incorrecta en general:
**`bd.md` estaba describiendo producción**, y su conteo de 21 columnas para `CHK` y `CHD` también
corresponde a producción. Lo que procede no es reescribir `bd.md`, sino declarar en él contra cuál
de los dos modelos está escrito.

### 9.5 Consecuencia para el plan

Se incorpora una **Fase 0.5 de reconciliación de modelos**, bloqueante y previa a cualquier
configuración. Su detalle está en [ROADMAP.md](ROADMAP.md). Configurar sobre dos modelos que
divergen es trabajar sobre un blanco móvil.


---

## 10. Adenda del 6 de agosto de 2026, tarde: intervención en AppSheet

Se accedió al editor de la aplicación con la sesión del cliente, previa copia de respaldo hecha
por el equipo de desarrollo.

### 10.1 Aplicado y verificado

| Acción | Resultado |
|---|---|
| *Regenerate Structure* sobre `MAN_Mantenimientos` | La tabla pasó de 26 a 28 columnas: la aplicación ya reconoce las dos agregadas al Sheets |
| Tipado de `Coordenadas_Cierre` | `Text` a `LatLong` |
| Tipado de `Precision_GPS` | `LatLong` a `Number` |
| Guardado de la aplicación | Confirmado, con sincronización posterior |

AppSheet había inferido ambos tipos mal, y además cruzados: asignó `Text` a la coordenada y
`LatLong` a la precisión. Con esos tipos la función de distancia no habría operado.

### 10.2 Hallazgos nuevos, bloqueantes

**B-13. `MAN_Mantenimientos` no tiene ninguna columna que apunte al activo.** Al escribir la regla
de geofencing, el Asistente de Expresiones respondió: *Can't find column "ActivoID" in table
"MAN_Mantenimientos". Did you mean "Activo"?*. La columna `Activo` de esa tabla es un indicador de
registro vigente, no una referencia al activo intervenido.

Consecuencia: **la fórmula que este proyecto ha documentado durante meses como correcta,
`DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0`, no funciona.** No es un problema
de sintaxis ni de nombre de campo: no existe la relación que presupone.

**B-14. Las referencias del modelo no existen en la aplicación.** Probada la ruta alterna vía la
orden de trabajo, el error fue: *Invalid dereference. Column OTID is not a Ref*. `OTID` está
tipada como `Text`. La cadena relacional Activo → Orden → Mantenimiento, que el diccionario de
datos y todos los diagramas presentan como el núcleo del sistema, **está en el papel y no en la
aplicación**.

Alcance de este hallazgo, más amplio que el geofencing:
- No hay navegación padre-hijo desde una orden a su mantenimiento.
- No se puede construir un reporte por activo, ni la hoja de vida del activo de D-12.
- Las vistas que hoy muestran nombres de activo probablemente resuelven por texto y no por
  referencia, lo que se rompe ante cualquier cambio de nombre.

### 10.3 Estado de la regla de geofencing

No se escribió. Queda como **por revisar y por ajustar**, junto con el resto del cableado de
referencias, dentro del fix integral de base de datos y aplicación que se acometerá con la
definición funcional y el plan de trabajo ajustado.

Fórmula candidata, pendiente de validar una vez cableadas las referencias:

```
DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0
```

Requiere convertir `MAN_Mantenimientos.OTID` a `Ref` hacia `OT_OrdenesTrabajo`, y confirmar que
`OT_OrdenesTrabajo.Activo` sea `Ref` hacia `ACT_Activos`.

### 10.4 Lectura de conjunto

Estos dos hallazgos no empeoran el diagnóstico: lo aclaran. Explican por qué ninguna de las cuatro
tablas transaccionales tiene un solo registro, y por qué el flujo nunca se ejecutó de extremo a
extremo. No es que faltara ejercitarlo: **el sistema no está cableado para que funcione**.

Y dan por primera vez una ruta concreta de reparación, que es lo que faltaba para pasar de
auditar a arreglar.
