# Alcance del sistema y supuestos adoptados — SGMC

> ## Qué cambió desde que se escribió (2026-08-09)
>
> **Sigue vigente el método: se construye bajo supuestos y no se espera respuesta.** Lo que cambió
> es que **ocho de los catorce ya no son supuestos, sino decisiones aplicadas al modelo** —D-02,
> D-03, D-04, D-06, D-07, D-08, D-10 y D-11, las ocho del apartado 3.2—, y alguna se cerró con un
> valor distinto del que aquí se propuso.
>
> - **La aplicación se reconstruyó desde cero.** `SGMC-886843353` se abandonó; la nueva es `SISGA`.
> - **La hoja se genera del modelo**, no se hereda: `BD/Modelo_Datos_PLANTILLA.xlsx`.
> - **D-02 se cerró con otros números.** Aquí se proponían 200 m; lo que hay es radio por familia
>   de activo, entre 50 m y 1,5 km.
> - **D-04 se cerró con 40 m, no con 50.**
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
2. **No hay nada que mirar.** El sistema actual no permite formarse un criterio: cuatro tablas
   vacías, un solo formulario con preguntas de los dieciocho de la hoja de producción, las
   referencias sin cablear y ninguna transacción
   ejecutada. Pedirle a alguien que valide modos de uso sobre eso es pedirle que imagine.
3. **Una suposición escrita se corrige en una tarde. Una pregunta sin responder bloquea semanas.**

El método nuevo: **inferir, construir completo, poblar con datos de prueba, entregar con manual, y
corregir con lo que diga el campo.** El líder funcional deja de ser una compuerta previa y pasa a
ser el validador de algo que puede tocar.

---

## 2. Qué significa "sistema completo"

No es el alcance mínimo. Es el sistema que se puede usar y del que se puede opinar. La columna de
la derecha dice dónde está hoy cada dimensión:

| Dimensión | Alcance | Hoy |
|---|---|---|
| Modelo de datos | Referencias cableadas de extremo a extremo, sin tablas huérfanas ni duplicadas | **Hecho.** 28 tablas, 202 columnas, 38 referencias |
| Formularios | Los 27 tipos de activo con banco de preguntas redactado | **1 de 27** en la plantilla. `FRM_Preguntas` tiene 15 filas, todas de `FRM_SOS` |
| Flujos | Preventivo programado, correctivo desde campo, segunda visita, devolución y aprobación | Preventivo sí. Correctivo no: no hay criticidad, ni hora de aviso, ni escalado |
| Evidencia | Fotografías y firma con una sola vía de captura | **Hecho.** `FOT_Fotografias` y `FIR_Firmas`, con `IsPartOf` |
| Control | Geofencing operativo con excepción supervisada | Puesto. **No probado**: falta la coordenada real (D-01) |
| Reportes | Los seis reportes propuestos, construidos y con datos | **No.** El modelo no declara vistas, acciones ni slices |
| Datos | Toda la base poblada con datos de prueba realistas | **Hecho.** 389 activos en la plantilla: 34 de fixture y 355 sintéticos |
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
| D-10 | Evidencia | Tablas hijas para fotografías y firmas. Mínimo 3 fotos, máximo 6, tipificadas. El supervisor aprueba en el portal, no firma en campo | **CERRADA.** Falta declarar los valores de `FIR_Firmas.TipoFirma` |
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
| D-03 | `ASG_AsignacionZona`, técnico × unidad funcional. `RG-04` filtra `ACT_Activos` por ahí. `USR_Usuarios.SedeID` queda descartada y se retira en el paso 1 | `python scripts/verificar_documentos.py`, aviso D-04 |
| D-04 | `MAN_Mantenimientos.CierreConExcepcion` y `MotivoExcepcion`, con `RG-03` y `RG-19`. El umbral vive en `PAR_Parametros`, y **vale 40 m, no 50**: la precisión típica de un móvil a cielo abierto es de 4,9 m, así que 40 deja unas ocho veces de margen | La fila `UMBRAL_GPS` de `PAR_Parametros` |
| D-06 | `EOT_EstadosOrden`, siete filas, con `QuienCambia` y `EsFinal`. **La columna está escrita y ninguna regla la impone**: hoy nada impide que un técnico ponga «Cerrada» | Volcar `EOT_EstadosOrden` |
| D-07 | `MOT_MotivosPendiente`, cinco motivos con `GeneraSeguimiento`, y `RG-10`, que encadena la orden de seguimiento por `OT_OrdenesTrabajo.OTOrigenID` | Volcar `MOT_MotivosPendiente` |
| D-08 | `NOV_Novedades`, con `Estado` en `Reportada / Aceptada / Descartada` y coordenada propia. **El alta automática del activo no existe**: el supervisor decide | Volcar `NOV_Novedades` del modelo |
| D-10 | `FOT_Fotografias` y `FIR_Firmas` como tablas hijas con `IsPartOf`; los campos de imagen y firma embebidos en `MAN_Mantenimientos` están retirados | `CAMPOS_RETIRADOS` en `scripts/modelo_objetivo.py` |
| D-11 | `CHD_ChecklistDetalle.PreguntaID` es referencia a `FRM_Preguntas`, y `CHK_Checklists.VersionFormulario` congela la versión con `RG-09` | `python scripts/validar_modelo.py` |

**Dos avisos que estas decisiones dejan abiertos y no son supuestos, son trabajo:** `QuienCambia`
no la impone ninguna regla, y `FIR_Firmas.TipoFirma` no tiene valores declarados. Los dos están en
`FUNCIONAL_SGMC.md` §4.

### 3.3 Lo que sigue abierto

| # | Qué falta decidir | Quién |
|---|---|---|
| D-01 | Las coordenadas reales. Los 34 activos de fixture comparten una coordenada de Bogotá y los 355 sintéticos llevan coordenadas interpoladas sobre el corredor. **Ninguna sirve para cerrar una orden con un técnico delante** | Operación |
| D-05 | Qué pasa si la inspección se interrumpe. No hay columna de «en curso» ni regla que la cierre en la jornada | Operación |
| D-07 | Si volver es `MAN_Mantenimientos.RequiereSegundaVisita` o una orden nueva encadenada por `OT_OrdenesTrabajo.OTOrigenID`. **Los dos existen en el modelo**, que es exactamente lo que la regla de una sola forma por propósito prohíbe | Operación |
| D-09 | Los 26 bancos de preguntas que faltan, uno por cada formulario de la plantilla salvo `FRM_SOS` | Operación |
| D-12 | Los seis reportes. Antes hace falta declarar la interfaz: hoy `modelo_objetivo.py` no tiene vistas, ni acciones, ni slices | Operación, y luego quien construya |
| D-13 | La definición de cumplimiento y disponibilidad, si van a interventoría | Operación y Dirección |
| D-14 | Accesos de interventoría y regla escrita de quién edita el backend | Dirección |
| — | Los cinco tipos que no se visitan —antivirus, licencias, certificados SSL, radios e internet—: camino sin evidencia de coordenada, o fuera de alcance | Operación |

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
antes: **cerca de cuatrocientas preguntas escritas por quien no hace el mantenimiento** —26 bancos
por las 15 preguntas del molde de `FRM_SOS`—. Saldrán razonables por venir del patrón de los tres
existentes, pero no
son la práctica real del equipo. Deben presentarse como borrador técnico, nunca como definitivas,
y la revisión del líder técnico es obligatoria antes del piloto.

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
  responda el líder funcional se contrasta contra estos supuestos y se integra. El documento está
  en [`historico/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md`](historico/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md).
- `ESTADO.md` dice dónde va el proyecto hoy. **Es la verdad del estado**; este documento solo dice
  bajo qué supuestos se construyó.
- `docs/ROADMAP.md` §2 recoge el orden de implementación y por qué es ese.
- `docs/INDICACIONES_POR_ROL.md` reparte por rol lo que sigue abierto en el apartado 3.3.
- La directiva de construcción original está en
  [`historico/PROMPT_CONSTRUCCION_SGMC.md`](historico/PROMPT_CONSTRUCCION_SGMC.md); la vigente es
  [`prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`](prompts/PROMPT_CONTINUAR_DESPLIEGUE.md).
