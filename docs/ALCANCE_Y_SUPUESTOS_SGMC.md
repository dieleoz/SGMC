# Alcance del sistema y supuestos adoptados — SGMC

> ## Qué cambió desde que se escribió (2026-08-09)
>
> **Sigue vigente el método: se construye bajo supuestos y no se espera respuesta.** Lo que cambió
> es que **ocho de los catorce ya no son supuestos, sino decisiones aplicadas al modelo** —D-02,
> D-03, D-04, D-06, D-07, D-08, D-10 y D-11, las ocho del apartado 3.2—, y alguna se cerró con un
> valor distinto del que aquí se propuso.
>
> - **La aplicación se reconstruyó desde cero**, y la vigente es `_SISGA_-323965761`. Las
>   aplicaciones y hojas superadas están nombradas, con su motivo, en `scripts/sistema.py`; vuélquelo
>   con `python scripts/sistema.py` en vez de copiar el nombre de aquí.
> - **La hoja se genera del modelo**, no se hereda: `BD/Modelo_Datos_PLANTILLA.xlsx` es el mismo
>   archivo que está publicado como `Modelo_Datos_10082026`.
> - **D-02 se cerró con otros números.** Aquí se proponían 200 m; lo que hay es radio por familia
>   de activo, entre 50 m y 1,5 km.
> - **D-04 se cerró con 40 m, no con 50.**
>
> ### Y el 2026-08-10 cambió el modelo de datos, no solo la aplicación
>
> Los cambios tocan supuestos de este documento. El motivo de cada uno y quién lo hace
> cumplir están en [`REGLAS_DEL_MODELO_DE_DATOS.md`](REGLAS_DEL_MODELO_DE_DATOS.md), generado:
>
> - **Toda clave es alfanumérica con prefijo** —`ACT-0001`, `TIP-001`, `UNF-01`, `SED-001`,
>   `USR-001`, `ROL-01`, `EST-01`, `FRE-01`, `CAL-01`, `SEC-01`, `TPR-01`—. AppSheet tipaba la clave
>   `Number` y descartaba en silencio la fila alfanumérica.
> - **Las seis columnas de coordenada llevan `_LatLong` en el nombre**, que es lo único que hace que
>   AppSheet infiera el tipo.
> - **`SED_Sedes` volvió como padre de ubicación del equipo bajo techo**, con `UnidadFuncionalID`,
>   `PR`, `TramoINVIAS`, `PK` y `Ubicacion_LatLong`; `ACT_Activos.SedeID` la referencia. Eso cierra
>   D-03 por el otro lado: `USR_Usuarios.SedeID` **ya está retirada del modelo**, no pendiente.
> - **`ACT_Activos` tiene `PK` y `TramoINVIAS` además de `PR`.** El corredor atraviesa tres rutas
>   de INVÍAS y tiene dos puntos distintos llamados `PR 0+000`: un PR sin ruta no identifica nada.
> - **Las cuatro unidades funcionales son las del contrato**, Apéndice Técnico 1 Tabla 3, con su
>   nombre real y sus dos referencias: `PKInicial`/`PKFinal` de `00+000` a `137+170`, y
>   `PRInicial`/`PRFinal` **con la ruta dentro del valor**, de `55CN03 PR0+0+000` a `5608 PR92+048`.
>   **No son cuartos iguales** —50,01 · 22,00 · 17,80 · 47,36 km—, que es como estaban repartidas, y
>   de eso cuelga D-03: `RG-04` filtra por unidad funcional, así que un reparto inventado le da a
>   cada técnico un conjunto de activos que no es el suyo **sin que nada falle**.
> - **Y hay cinco verificadores, no cuatro.** El quinto es `verificar_reproducible.py`.
>
> La tabla del apartado 3 lleva ahora una columna de estado, y el apartado 3.2 dice qué se cerró y
> contra qué se comprueba. **Lo que sigue abierto está en el apartado 3.3.**

**Fecha original:** 6 de agosto de 2026 · **Revisado:** 9 de agosto de 2026
**Estado:** Vigente con nota. Sustituye el enfoque de consulta previa al líder funcional.
**Regla:** todo lo que aquí siga declarado como supuesto es **vinculante hasta que el campo lo
desmienta**. No se espera confirmación para construir.

---

## 1. Por qué cambia el método

El enfoque anterior era preguntar al líder funcional catorce decisiones y construir con sus
respuestas. Se descartó por tres razones:

1. **El cuestionario no avanza.** Quien responde no tiene el modelo mental del sistema todavía, y
   preguntarle en abstracto produce silencio o un "de acuerdo" a todo, que es peor porque simula
   una decisión que no existe.
2. **No había nada que mirar.** Cuando se decidió el método, el sistema no permitía formarse un
   criterio: las tablas de movimiento vacías, un solo formulario con preguntas de los dieciocho de
   la hoja de entonces, las referencias sin cablear y ninguna transacción ejecutada. Pedirle a
   alguien que valide modos de uso sobre eso es pedirle que imagine. **Hoy los 27 formularios
   tienen banco de preguntas**, pero 288 de las 333 son borrador y las referencias siguen sin
   cablear: el argumento no ha caducado.
3. **Una suposición escrita se corrige en una tarde. Una pregunta sin responder bloquea semanas.**

El método nuevo: **inferir, construir completo, poblar con datos de prueba, entregar con manual, y
corregir con lo que diga el campo.** El líder funcional deja de ser una compuerta previa y pasa a
ser el validador de algo que puede tocar.

---

## 2. Qué significa "sistema completo"

No es el alcance mínimo. Es el sistema que se puede usar y del que se puede opinar. La columna de
la derecha dice dónde está hoy cada dimensión:

**Antes de leer la columna de la derecha:** declarada en el modelo, presente en la hoja y montada en
la aplicación son tres cosas distintas. La aplicación de hoy tiene **las 28 tablas dadas de alta y
nada más**; referencias, reglas y filtros están sin poner. Donde abajo dice «declarado», léase que la
expresión existe escrita y verificada, no que esté configurada.

| Dimensión | Alcance | Hoy |
|---|---|---|
| Modelo de datos | Referencias cableadas de extremo a extremo, sin tablas huérfanas ni duplicadas | **Declarado.** 28 tablas, 211 columnas, 39 referencias, 21 reglas, `validar_modelo.py` en 0 errores. **Sin cablear en la aplicación** |
| Formularios | Los 27 tipos de activo con banco de preguntas redactado | **Redactado: 27 de 27.** `FRM_Preguntas` tiene **333 filas** repartidas entre los 27 formularios; 288 llevan `[BORRADOR: validar con operacion]` y 45 —SOS, CCTV y PMV fijo, 15 cada uno— ya estaban acordadas |
| Flujos | Preventivo programado, correctivo desde campo, segunda visita, devolución y aprobación | Preventivo sí. Correctivo no: no hay criticidad, ni hora de aviso, ni escalado. La devolución no tiene estado al que mover la orden |
| Evidencia | Fotografías y firma con una sola vía de captura | **Declarado.** `FOT_Fotografias` y `FIR_Firmas` como tablas hijas con `IsPartOf`, y los campos embebidos retirados |
| Control | Geofencing operativo con excepción supervisada | **Declarado**, con el radio por tipo poblado en los 27. **Sin poner en la aplicación y sin probar**: falta la coordenada real (D-01) |
| Reportes | Los seis reportes propuestos, construidos y con datos | **No.** El modelo no declara vistas, acciones ni slices |
| Datos | Toda la base poblada con datos de prueba realistas | **A medias.** 368 filas en `ACT_Activos` —334 sintéticas y 34 del juego de arranque— y los catálogos completos, pero **ningún registro transaccional**: `OT`, `MAN`, `CHK`, `CHD`, `FOT`, `FIR`, `NOV` y `PLA` están vacías. Y **`ACT_Activos.Ubicacion_LatLong` está vacía en las 368**: se perdió al renombrar la columna, y ninguna de las que había era real |
| Documentación | Manual de uso por rol, con modos, usos y reportes explicados | Reparto por rol en `INDICACIONES_POR_ROL.md`. El manual de usuario **no se entrega** |

---

## 3. Los catorce supuestos adoptados

Cada uno es la opción que se marcó como propuesta en el documento de mesa de trabajo. Se adoptó
como decisión de trabajo. **La columna de estado dice cuáles ya son parte del modelo y cuáles
siguen siendo suposiciones.**

| # | Decisión | Supuesto adoptado | Estado |
|---|---|---|---|
| D-01 | Coordenadas | Se cargan coordenadas reales sobre el trazado de la vía de la Concesión; un subconjunto sirve para validar antes del levantamiento completo | **ABIERTA.** Es el bloqueo de la salida a campo |
| D-02 | Radio | 200 m en activos puntuales; tratamiento aparte para fibra óptica | **CERRADA con otro valor.** Radio por familia, de 50 m a 1,5 km |
| D-03 | Sede | La unidad funcional es atributo del activo; la zona de trabajo, del usuario. Un técnico puede tener varias | **CERRADA.** `ASG_AsignacionZona` |
| D-04 | GPS deficiente | Cierre con excepción: motivo escrito, fotografía, marca y aviso al supervisor. Umbral 50 m | **CERRADA en el mecanismo, con 40 m y no 50** |
| D-05 | Interrupción | Borrador local; la inspección queda en curso y debe cerrarse en la jornada | **ABIERTA.** Ninguna columna ni regla lo declara |
| D-06 | Ciclo de la OT | Siete estados. El técnico llega hasta En revisión; solo el supervisor cierra o suspende. Vencida al día siguiente. Se permite ejecutar sin orden previa como novedad | **CERRADA en la estructura, sin imponer.** Falta el rechazo |
| D-07 | Trabajo incompleto | Cierre parcial con motivo tipificado que genera orden de seguimiento. Devolución reabre el mismo registro con traza | **CERRADA en el motivo, ABIERTA en la segunda visita** |
| D-08 | Activo no inventariado | El técnico levanta novedad con foto y coordenada; el supervisor decide el alta. Fuera de servicio genera orden correctiva automática | **CERRADA en la estructura.** El alta automática no |
| D-09 | Tipos priorizados | **Se construyen los 27.** Se redactan a partir de los tres existentes y de la práctica de mantenimiento; el funcional corrige sobre texto concreto | **ABIERTA en la validación, no en la redacción.** Los 27 formularios de la plantilla tienen banco de preguntas: 3 acordados —SOS, CCTV y PMV fijo, 15 cada uno— y 24 en borrador, con sus 288 preguntas marcadas `[BORRADOR: validar con operacion]` |
| D-10 | Evidencia | Tablas hijas para fotografías y firmas. Mínimo 3 fotos, máximo 6, tipificadas. El supervisor aprueba en el portal, no firma en campo | **CERRADA, y entera.** `FIR_Firmas.TipoFirma` **ya declara sus valores**: la lista es `Tecnico`, y solo ese, que es lo coherente con que el supervisor no firme. Lo que ninguna regla impone todavía es el mínimo y el máximo de fotografías |
| D-11 | Trazabilidad | El detalle guarda `PreguntaID`; los formularios se versionan | **CERRADA** |
| D-12 | Reportes | Se construyen los seis propuestos. Productividad del técnico queda desactivado por defecto | **ABIERTA.** El modelo no describe interfaz |
| D-13 | Indicadores | Cumplimiento sobre órdenes cerradas en fecha. Excepción de GPS cuenta como cumplida y se reporta aparte. Disponibilidad por tiempo fuera de servicio | **ABIERTA** |
| D-14 | Gobierno | Interventoría sin acceso, solo reportes exportados. Cambios en producción solo por el administrador con autorización escrita. Retención de evidencia 5 años | **ABIERTA salvo la retención**, que ya usan los cálculos de capacidad |

**El supuesto que el campo todavía puede tumbar caro es D-13**: si las cifras van a interventoría,
la definición tiene que estar acordada antes de emitir el primer informe. D-10 ya dejó de ser
reversible barato — el modelo de evidencia está construido y la plantilla poblada.

### 3.2 Lo que se cerró, con qué y contra qué se comprueba

**Ninguna de estas ocho se decidió leyendo este documento: se decidió construyendo.** Cada fila
lleva dónde vive la decisión, para que nadie la vuelva a abrir por escrito.

| # | Se cerró con | Se comprueba |
|---|---|---|
| D-02 | **Radio por familia de activo** en `TIP_TiposActivo.RadioGeofencingKm`, no un número único: **0,05 km en 18 tipos** —postes SOS, cámaras, gálibos, sensores, paso seguro, video wall y equipos de TI—, **0,1 km en 8** —PMV fijos y móviles, generador, básculas, peajes y subestación— y **1,5 km en la fibra**. `RG-01` desreferencia esa columna a través de la orden y del activo | Volcar la columna de `TIP_TiposActivo` en `BD/Modelo_Datos_PLANTILLA.xlsx`: los 27 tipos con valor |
| D-03 | `ASG_AsignacionZona`, técnico × unidad funcional. `RG-04` filtra `ACT_Activos` por ahí. **`USR_Usuarios.SedeID` ya no está pendiente: se retiró del modelo el 2026-08-10** y vive en `CAMPOS_RETIRADOS`. La sede sigue existiendo, pero como sitio del **activo** —`ACT_Activos.SedeID`—, no de la persona | Volcar `CAMPOS_RETIRADOS['USR_Usuarios']` de `scripts/modelo_objetivo.py` |
| D-04 | `MAN_Mantenimientos.CierreConExcepcion` y `MotivoExcepcion`, con `RG-03` y `RG-19`. El umbral vive en `PAR_Parametros`, y **vale 40 m, no 50**: la precisión típica de un móvil a cielo abierto es de 4,9 m, así que 40 deja unas ocho veces de margen | La fila `UMBRAL_GPS` de `PAR_Parametros` |
| D-06 | `EOT_EstadosOrden`, siete filas, con `QuienCambia` y `EsFinal`. **La columna está escrita y ninguna regla la impone**: hoy nada impide que un técnico ponga «Cerrada» | Volcar `EOT_EstadosOrden` |
| D-07 | `MOT_MotivosPendiente`, cinco motivos con `GeneraSeguimiento`, y `RG-10`, que encadena la orden de seguimiento por `OT_OrdenesTrabajo.OTOrigenID` | Volcar `MOT_MotivosPendiente` |
| D-08 | `NOV_Novedades`, con `Estado` en `Reportada / Aceptada / Descartada` y coordenada propia. **El alta automática del activo no existe**: el supervisor decide | Volcar `NOV_Novedades` del modelo |
| D-10 | `FOT_Fotografias` y `FIR_Firmas` como tablas hijas con `IsPartOf`; los campos de imagen y firma embebidos en `MAN_Mantenimientos` están retirados | `CAMPOS_RETIRADOS` en `scripts/modelo_objetivo.py` |
| D-11 | `CHD_ChecklistDetalle.PreguntaID` es referencia a `FRM_Preguntas`, y `CHK_Checklists.VersionFormulario` congela la versión con `RG-09` | `python scripts/validar_modelo.py` |

**Un aviso que estas decisiones dejan abierto y no es un supuesto, es trabajo:** `QuienCambia` está
escrita y poblada en las siete filas, y **ninguna de las 21 reglas del modelo la lee**. Hasta que
alguna lo haga, la separación entre quien ejecuta y quien certifica está descrita y no aplicada. Está
en `FUNCIONAL_SGMC.md` §4.

### 3.3 Lo que sigue abierto

| # | Qué falta decidir | Quién |
|---|---|---|
| D-01 | Las coordenadas reales. **`ACT_Activos.Ubicacion_LatLong` está vacía en las 368 filas** de `BD/Modelo_Datos_PLANTILLA.xlsx`, así que ya ni siquiera hay una coordenada inventada con la que ensayar. Hasta cargarlas, `RG-01` compara contra blanco y **rechaza también el cierre legítimo** | Operación |
| — | El **PR de INVÍAS** de cada activo, con su `TramoINVIAS`. Las dos columnas existen y están vacías en las 368; lo que está poblado es el `PK`, que es lineal y del proyecto. No se inventan: el corredor tiene dos puntos distintos llamados `PR 0+000` | Operación |
| — | Dónde están las otras cinco sedes. `SED_Sedes` tiene sus columnas de ubicación y solo el peaje de Machetá las trae —`UNF-01`, `PR 27+240`, ruta `5607`—; ninguna de las seis tiene `PK` ni `Ubicacion_LatLong` | Operación |
| — | Qué equipo va dentro de cada sede. `ACT_Activos.SedeID` existe, es opcional y **está vacía en las 368 filas**, así que el equipo bajo techo —servidores, portátiles, impresoras, NAS, video wall— sigue colgando solo de la unidad funcional. Mientras esté vacía, `RG-21` no tiene nada que comparar | Operación |
| D-05 | Qué pasa si la inspección se interrumpe. No hay columna de «en curso» ni regla que la cierre en la jornada | Operación |
| D-07 | Si volver es `MAN_Mantenimientos.RequiereSegundaVisita` o una orden nueva encadenada por `OT_OrdenesTrabajo.OTOrigenID`. **Los dos existen en el modelo**, que es exactamente lo que la regla de una sola forma por propósito prohíbe | Operación |
| D-09 | **Validar las 288 preguntas en borrador**, repartidas en 24 de los 27 formularios. No están por escribir: están escritas y marcadas `[BORRADOR: validar con operacion]` en su ayuda. Buscar esa marca en la hoja dice exactamente qué queda | Operación |
| D-12 | Los seis reportes. Antes hace falta declarar la interfaz: hoy `modelo_objetivo.py` no tiene vistas, ni acciones, ni slices | Operación, y luego quien construya |
| D-13 | La definición de cumplimiento y disponibilidad, si van a interventoría | Operación y Dirección |
| D-14 | Accesos de interventoría y regla escrita de quién edita el backend | Dirección |
| — | Los cinco tipos que no se visitan —antivirus, licencias, certificados SSL, radios e internet—: camino sin evidencia de coordenada, o fuera de alcance | Operación |

### 3.4 Cuáles de estos supuestos no caben en el modelo de hoy

**Distinguir «falta decidirlo» de «no hay dónde ponerlo» evita construir dos veces.** Contrastado
contra las 28 tablas y 211 columnas de `scripts/modelo_objetivo.py`:

| # | Qué le falta al modelo | Cabe hoy |
|---|---|---|
| D-05 | Ninguna columna dice que una inspección quedó en curso. `CHK_Checklists.Finalizado` distingue terminado de no terminado, pero **nada la cierra en la jornada** ni marca el borrador local | Sí: es una regla, no una tabla |
| D-06 | El rechazo necesita **una fila `Devuelta` en `EOT_EstadosOrden`**. `MAN_Mantenimientos.ObservacionRechazo` ya existe. Imponer `QuienCambia` es una regla sobre una columna que ya está poblada | Sí, sin tocar el esquema |
| D-12 | `modelo_objetivo.py` **no tiene vistas, ni acciones, ni slices**. No es que falten reportes: falta la capa donde declararlos | No. Es una estructura nueva en el modelo |
| D-13 | Cumplimiento es «planeadas contra ejecutadas», y **no hay puente entre `PLA_PlanMantenimiento` y `OT_OrdenesTrabajo`**: ninguna columna de la orden dice qué fila del plan satisface. `validar_modelo.py` ya lo avisa con `V-06`, «`PLA_PlanMantenimiento` no es referenciada por nadie». Disponibilidad necesita además el tiempo fuera de servicio, que hoy no se registra | No. Necesita `TAR_Tareas` y una referencia desde la orden |
| — | Los cinco tipos sin ubicación **no tienen fila** en `TIP_TiposActivo`, y `ACT_Activos.Ubicacion_LatLong` es obligatoria para todos. Faltaría `TIP_TiposActivo.SeVisita`, ya declarada en `COLUMNAS_PROPUESTAS` | No |
| D-04 | **Dentro de un túnel el GPS no fija posición**, así que `RG-01` falla siempre y el cierre con excepción deja de ser excepcional. No es marginal: quince túneles y 7.224 metros, de los que **6.000 caen en los 17.800 de la UF3**. Nada en el modelo dice qué tramos van bajo tierra, así que el supervisor ve un técnico acumulando excepciones sin poder distinguir el túnel del técnico | No. Necesita `TUN_Tuneles`, declarada en `PROPUESTAS` y sin especificar |

**Y al revés, lo que ya está y algún documento anterior daba por pendiente:** el radio de geofencing
por tipo, poblado en los 27; el umbral de GPS como parámetro y no como literal; los valores de
`FIR_Firmas.TipoFirma`; los modos de falla, con `FAL_ModosFalla` poblada; la segunda visita
encadenada, con `OT_OrdenesTrabajo.OTOrigenID`; **el punto kilométrico**, con `ACT_Activos.PK` y
`ACT_Activos.TramoINVIAS` y con `PKInicial`/`PKFinal` en `UNF_UnidadesFuncionales`; y **la ubicación
de la edificación**, con `SED_Sedes` situada en la vía y `ACT_Activos.SedeID` colgando de ella.

### 3.1 D-09 diverge de lo que se envió al funcional

El documento que ya salió proponía **arrancar con tres tipos** y advertía, con estas palabras, que
*intentar construir los 18 a la vez es lo que hará que el proyecto se estanque otro mes*.

Aquí se adopta lo contrario: **se construyen todos**, que desde el 2026-08-09 son **27** y no 18 —el
catálogo pasó a 27 tipos al darle formulario propio a las nueve familias que colgaban del de otra
cosa—. La divergencia es deliberada y el motivo es
que cambió la premisa. Aquella advertencia suponía que los bancos los redactaba el equipo de la
Concesión, y en ese escenario era cierta. Con el método nuevo los redacta el agente a partir del
patrón existente, y el líder técnico corrige sobre texto concreto. Redactar es lo caro; corregir
es barato.

El riesgo que permanece es distinto y hay que nombrarlo, y con el catálogo de 27 pesa más que
antes: **288 preguntas escritas por quien no hace el mantenimiento**, repartidas en 24 bancos de
entre 10 y 13 preguntas. Saldrán razonables por venir del patrón de los tres existentes, pero no
son la práctica real del equipo. Por eso **cada una lleva `[BORRADOR: validar con operacion]` en su
ayuda**: la marca es la que distingue lo acordado de lo redactado, y el día que no aparezca ninguna
el banco está cerrado. La revisión del líder técnico es obligatoria antes del piloto.

Si al revisar aparece que la mayoría no sirve, se vuelve a la propuesta original de tres tipos.

---

## 4. Fuera de alcance

- Integración con Power BI o mesas de ayuda.
- Gestión de repuestos, inventario de almacén y costos.
- Firma con valor probatorio frente a terceros.
- Generación automática de órdenes por frecuencia. Se deja el catálogo listo pero sin el
  disparador, hasta ver el comportamiento del preventivo manual. **Y ya no es solo una decisión de
  producto:** en el plan gratuito de AppSheet los procesos programados no se ejecutan, así que
  depende de la decisión de licenciamiento D-B.
- **El código QR**, por decisión del 2026-08-07. El activo se abre por lista, y
  `MAN_Mantenimientos.OrigenApertura = Lista` deja de ser una excepción.

---

## 5. Cómo se corrige un supuesto

1. El campo o el líder funcional detecta que un supuesto no sirve.
2. Se registra en este documento con fecha y motivo.
3. Se evalúa el costo de cambio. **Para los cerrados, el costo ya no es el de la tabla: es el de
   migrar lo construido**, y hay que mirar el apartado 3.2 antes de estimarlo.
4. Si implica migrar datos, se decide antes de seguir cargando.

Un supuesto corregido no es un error del método: es el método funcionando.

---

## 6. Relación con los documentos existentes

- El documento de mesa de trabajo y su correo **ya se enviaron**. No se remiten de nuevo. Lo que
  responda el líder funcional se contrasta contra estos supuestos y se integra. El documento era
  `DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md`, retirado en la limpieza del 2026-08-10.
- `ESTADO.md` dice dónde va el proyecto hoy. **Es la verdad del estado**; este documento solo dice
  bajo qué supuestos se construyó.
- `docs/ROADMAP.md` §2 recoge el orden de implementación y por qué es ese.
- `docs/INDICACIONES_POR_ROL.md` reparte por rol lo que sigue abierto en el apartado 3.3.
- La directiva de construcción original, `PROMPT_CONSTRUCCION_SGMC.md`, y la que la sucedió,
  `PROMPT_CONTINUAR_DESPLIEGUE.md`, se retiraron en la limpieza del 2026-08-10.
