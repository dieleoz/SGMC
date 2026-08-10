# ROADMAP de implementación — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 9 de agosto de 2026 | **Versión:** 4.1

> ## Para qué sirve este documento, y para qué no
>
> **El estado del proyecto está en [`ESTADO.md`](../ESTADO.md), no aquí.** Este documento es el
> **orden de implementación**: qué va antes que qué, y por qué ese orden y no otro. Es lo que no
> cabe en un tablero de estado y lo que más caro sale improvisar.
>
> **Qué cambió en la 4.1, del 2026-08-09:**
>
> - **La aplicación se reconstruyó desde cero.** `SGMC-886843353` se abandonó; la nueva es `SISGA`.
>   *Regenerate* fusiona en vez de reemplazar, así que con un esquema tan divergente no converge.
> - **La hoja se genera del modelo**, no se hereda: `BD/Modelo_Datos_PLANTILLA.xlsx`, con 34 activos
>   de fixture y 355 sintéticos.
> - **Las referencias son 38, no 15.** Las 15 eran las que faltaban en la aplicación anterior, donde
>   otras 23 ya estaban puestas. Sobre una aplicación nueva no sobrevive ninguna.
> - **La Fase 0.5 de reconciliación de modelos está cerrada**, y su lista de tareas —que ocupaba la
>   mitad de este documento— se ha reducido al registro de lo que dejó decidido.
>
> El documento funcional que se entrega es [`FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md). El contexto
> operativo destilado está en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md). El reparto de quién
> hace qué, en [`INDICACIONES_POR_ROL.md`](INDICACIONES_POR_ROL.md).

> **De dónde viene la versión 4.** La 3 declaraba completadas al 100 % la Fase 0 y la Fase 1, y la
> auditoría del 6 de agosto de 2026 verificó contra el archivo que era falso. Ese dictamen está en
> [`historico/AUDITORIA_PLAN_Y_ROADMAP.md`](historico/AUDITORIA_PLAN_Y_ROADMAP.md): sus hallazgos
> `B-01` a `B-14` son el origen de casi todo lo que se decidió después.
>
> Y la 4.0 amplió el alcance al leer los siete documentos de `contexto/`: la operación real tiene
> varias tareas por tipo de equipo, cuatro clases de mantenimiento, un flujo de correctivo con
> tiempos contractuales y cinco activos que no se visitan. **Ya no cabe todo de una vez**, y por eso
> esto dejó de ser una lista de fases y pasó a ser un orden con criterio explícito.

---

## 1. Principio de este roadmap

**Hay dos archivos contra los que verificar, no uno.** Los datos, en `BD/*.xlsx` y en el Sheets de
producción. Y el comportamiento de la plataforma, en la documentación oficial de AppSheet, recogido
en `BASE_CONOCIMIENTO_APPSHEET.md` con su cita y su URL. Durante cinco rondas de revisión solo se
verificaba lo primero.

Ninguna fase se declara cerrada sin un **criterio de cierre verificable**: un hecho que otra
persona pueda comprobar leyendo el archivo o el sistema, no un reporte de avance.

La versión anterior de este documento no tenía criterios de cierre. Por eso pudo marcar como
completadas fases que dejaron cuatro tablas vacías y el control GPS inoperante.

---

## 2. Orden de implementación

**No se ordena por importancia: se ordena por lo que cuesta hacerlo tarde.**

Es el riesgo que fijó operación — «que no falten campos, o cambiar la base y la aplicación después
de salir a producción, es un problema». Una implementación progresiva **agrava** ese riesgo si se
ordena mal: si el piloto sale con medio esquema, la otra mitad deja de ser una columna y pasa a ser
una migración.

De ahí salen tres clases, y el orden entre ellas no es negociable:

| Clase | Cuándo | Por qué |
|---|---|---|
| **Esquema** — tablas y columnas | **Antes del piloto, todo junto** | `MAN_Mantenimientos` solo tiene 2 filas, y las dos de prueba. Añadir hoy cuesta cero; después cuesta migración |
| **Datos** — inventario, coordenadas | En medio, con las referencias ya tipadas | Así AppSheet valida cada fila al cargarla, gratis |
| **Comportamiento** — reglas, permisos | Después, en cualquier orden | No tocan datos. Se endurece con el sistema andando |

### La secuencia

| # | Paso | Contenido | Depende de |
|---|---|---|---|
| **0** | **Cerrar la aplicación** | Las **38 referencias** ya están puestas. Falta la regla del umbral de GPS con su `OR(ISBLANK(...))`, terminar las columnas retiradas y correr las tres expresiones de prueba | En ejecución. Guion en `prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`; ficha por tabla en `MANUAL_DESPLIEGUE.md` |
| **0b** | **Decidir la migración a la hoja limpia** | Si se migra, las 47 columnas sobrantes desaparecen del archivo y el trabajo de ocultarlas se tira | **Se decide antes de terminar el paso 0**, o es trabajo perdido. Coste en `MIGRACION_HOJA_LIMPIA.md` |
| **1** | **Esquema completo** | `TAR_Tareas` · poblar `ROL_Roles` con los 12 · jerarquía de ubicación · columnas de tiempo en la orden · retirar `ACT.FrecuenciaID` y `TIP.FormularioID` | `ESPEC-003` y su veredicto |
| **2** | **Carga del inventario real** | Los 355 con identidad, serie y ubicación. **Los que hay hoy son sintéticos** y lo dicen de sí mismos | Paso 1, y que operación confirme que 355 son los de este corredor |
| **3** | **Reglas de integridad** | Imponer `QuienCambia` · estado de rechazo · valores de `TipoFirma` | Paso 1 |
| **4** | **Piloto de campo** | El levantamiento de coordenadas **como primera orden de trabajo** | Pasos 2 y 3 |
| **5** | **Correctivo** | Criticidad · pausas · escalado N1/N2/N3 | Decisión de alcance |
| **6** | **Fase 2 de modelo** | Certificaciones múltiples · mediciones de hilo · estructuras · almacén | Piloto en marcha |

**El paso 1 es el único que no admite trocearse.** Los demás sí.

### Lo que NO está en esta secuencia

No es «más adelante»: es **no en el plan actual**. Ponerlo en una fase futura daría la impresión de
que llega solo con tiempo, y no llega — llega con la decisión de licenciamiento **D-B**.

- Generación automática de las órdenes del mes
- Aviso al supervisor de que hay trabajo por recibir
- Integración con el SCADA para abrir correctivas
- Cualquier prueba automatizada, por falta de API REST

---

## 3. Estado por fase

> ### La decisión del 2026-08-09, que reordena lo que queda
>
> **Se migra a la hoja limpia, y el Excel del repositorio es lo que se entrega.** El funcional parte
> de ese archivo y desde ahí sigue las guías, así que tiene que salir generado y limpio, no ser una
> hoja heredada con 47 columnas escondidas encima.
>
> **Lo que cambia:** ocultar esas 47 en la aplicación **deja de estar en el plan** — desaparecen del
> archivo, y con ellas las tres trampas. Lo que queda en el editor son dos cosas, la regla del
> umbral de GPS y las tres expresiones de prueba.
>
> **Lo que abre:** `scripts/generar_plantilla.py`, que todavía no existe. Hoy la plantilla no la
> reproduce ningún comando, y eso la convierte en un artefacto que se conserva en vez de generarse.
> Es lo primero al retomar.

| Fase | Estado | Criterio de cierre |
|---|---|---|
| Sprint 0. Definición funcional | **Cerrado por supuestos.** No se espera respuesta | Los catorce adoptados por escrito en `ALCANCE_Y_SUPUESTOS_SGMC.md`, con su estado de cierre |
| Fase 0.5. Reconciliación de modelos | **CERRADA** el 2026-08-07 | `modelo_objetivo.py` es la fuente única; los documentos se generan de él. Ver 4.5 |
| **Fase A. La hoja** | **CERRADA.** Actas `ACTA-001` a `ACTA-004` | `verificar_faseA.py` en 0 fallos. Hoy: **61 conformes** sobre `Modelo_Datos_09082026.xlsx` y **60** sobre `Modelo_Datos_PLANTILLA.xlsx` |
| Reconstrucción de la aplicación | **HECHA** el 2026-08-09 | `SISGA`, con las 28 tablas dadas de alta sobre la hoja |
| **Fase B. Cableado y reglas** | **En ejecución** | Las **38** referencias puestas —ya lo están—, la migración a la hoja limpia hecha, y `PRUEBA-003` pasada |
| Fase 1. Datos maestros | Bloqueada por D-01 y D-09 | Coordenadas reales cargadas, sedes realineadas, bancos de preguntas construidos |
| Fase 2. Configuración de interfaz | Bloqueada por Fase 1 y por declarar vistas | Reportes y pantallas construidos. **Antes hay que declarar la interfaz en el modelo**: hoy no tiene vistas, ni acciones, ni slices |
| Fase 3. Prueba controlada | Bloqueada por Fase 2 | Registros reales en `MAN_Mantenimientos` y en las tablas de evidencia, verificados leyendo el archivo |
| Fase 4. Piloto de campo | Bloqueada por Fase 3 | 10 técnicos operando una semana, con registros sincronizados desde el corredor |
| Fase 5. Producción y evolución | Bloqueada por Fase 4 | Los 18 tipos con banco de preguntas, integraciones y respaldo automático |

**No hay fechas.** El cronograma depende de dos tareas que son trabajo del cliente y cuya duración
solo el equipo de la Concesión puede estimar: el levantamiento de las coordenadas reales (decisión
D-01) y la redacción de los bancos de preguntas (decisión D-09). Las fechas se fijan en el acta de
la mesa de trabajo, no antes.

---

## 3.1 Lo que sí está construido

Verificado el 2026-08-09 contra `scripts/modelo_objetivo.py` y `BD/Modelo_Datos_PLANTILLA.xlsx`.
**Cada cifra se rederiva con los verificadores; ninguna está escrita de memoria.**

- **Modelo de 28 tablas, 202 columnas, 38 referencias y 20 reglas.** `validar_modelo.py` sale
  `APTO PARA DESPLEGAR` con 0 errores.
- **La hoja se genera del modelo.** La plantilla trae 28 pestañas de datos más `_LEEME`, sin una
  sola columna de sobra. La hoja de producción todavía arrastra **47**.
- **Aplicación `SISGA` reconstruida**, con las 28 tablas dadas de alta, las 38 referencias puestas,
  `IsPartOf` en las cuatro que lo llevan, los dos filtros de seguridad y las cuatro marcas de tiempo
  como `ChangeTimestamp` del servidor.
- **Inventario de prueba:** 34 activos de fixture y 355 sintéticos con los códigos del Plan Maestro
  repartidos por los 137 km del corredor. Cada fila declara en `ACT_Activos.Observaciones` que no es
  inventario real.
- **`TIP_TiposActivo.RadioGeofencingKm` poblado en los 18 tipos** en
  `BD/Modelo_Datos_PLANTILLA.xlsx`, por familia: 0,05 km en 12, 0,1 km en 5 y 1,5 km en la fibra.
  **En la hoja que la aplicacion lee sigue vacio en los 18**, comprobado en Drive el 2026-08-09, asi
  que hoy rige el literal de 1,0 km. Es el mismo hecho que `PRUEBA-003` C-1.
- Catálogos poblados: 18 tipos de activo, 10 sedes, 4 unidades funcionales, 4 roles, 11 usuarios,
  4 asignaciones de zona, 5 motivos de pendiente, 7 estados de orden, 3 parámetros y los catálogos
  viales de calzada, sentido, estado y frecuencia.
- 6 órdenes de trabajo, 2 mantenimientos de prueba y 1 checklist con su detalle.
- Banco de preguntas de un solo formulario: **15 preguntas, todas de postes SOS**.

**Y lo que está construido pero no probado:** el geofencing. Los 34 activos de fixture comparten una
coordenada de Bogotá y los 355 sintéticos tienen coordenadas inventadas, así que la prueba del
cierre legítimo no se puede ejecutar sin desplazarse. Es D-01.

---

## 4. Sprint 0 — Definición funcional (cerrado por supuestos)

El documento y su correo salieron al líder funcional y **no se reenvían**. Pero el proyecto dejó de
esperar su respuesta: las catorce decisiones se adoptaron como supuestos en
`ALCANCE_Y_SUPUESTOS_SGMC.md` y son vinculantes hasta que el campo las desmienta.

- [x] Enviar el documento al líder funcional
- [x] Adoptar los catorce supuestos y declararlos por escrito
- [ ] Contrastar la respuesta del funcional, cuando llegue, contra los supuestos adoptados

**Por qué cambió.** Un cuestionario en abstracto a quien no tiene todavía el modelo mental produce
silencio, y el sistema actual no permite formarse criterio: no hay nada que mirar. Es más rápido
construir completo, poblar con datos, entregar con manual, y corregir con lo que diga el campo.

---

## 4.4 Decisiones pendientes de Dirección

La propuesta `entregables/Propuesta_Arquitectura_SGMC.docx` pide tres decisiones. Las dos primeras
condicionan la salida a producción y ninguna es técnica:

- **D-A. Propiedad del backend.** El documento y las fotografías pertenecen a una cuenta personal
  de Gmail. Las imágenes consumen su cuota de 15 GB, que con los 355 activos del Plan Maestro da
  **5,7 años** frente a los 5 de retención, y con el corredor completo de 500 se agota **en 4,1**.
  Sale de `python scripts/capacidad.py`.
- **D-B. Plan de licenciamiento.** En el plan gratuito los procesos programados no se ejecutan. Sin
  plan pagado no hay generación automática de órdenes ni notificaciones, que es lo que convierte el
  sistema en gestión y no en registro.
- **D-C. Definición contractual de disponibilidad.** Si el contrato o interventoría la definen de
  otra forma, esa prima sobre la propuesta.

---

## 4.5 Fase 0.5 — Reconciliación de modelos. CERRADA el 2026-08-07

**Qué pasó.** El 6 de agosto de 2026, al leer por primera vez el backend de producción, se encontró
que el Excel local y el Google Sheets **no eran el mismo modelo**: el Excel tenía las columnas de
GPS y no el mapeo de formularios, y producción al revés. Difería además `CHK_Checklists` y
`CHD_ChecklistDetalle`. Dos personas editaban por separado y nadie lo sabía.

**Cómo se cerró.** No eligiendo uno de los dos, que era lo que este documento proponía, sino
**sacando la verdad de los dos archivos**: desde entonces la fuente única es
`scripts/modelo_objetivo.py`, la hoja se genera de él y los documentos también. Un modelo declarado
en código no puede divergir en silencio de otro, porque solo hay uno.

**Lo que dejó decidido, y por eso no se reabre:**

| Decisión | Cómo quedó |
|---|---|
| Columnas de GPS en `MAN_Mantenimientos` | `Coordenadas_Cierre` como `LatLong` y `Precision_GPS` como `Number`. AppSheet las había inferido mal y cruzadas |
| `EOT_EstadosOrden` | Sus claves son el nombre del estado, no `1..7`. Un catálogo se diseña mirando los datos que va a resolver |
| `IsPartOf` sobre `MAN_Mantenimientos.OTID` | **Va sin él.** La ejecución es el registro histórico y sobrevive a su orden |
| Borrado del histórico | Se retira `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` (RG-14 y RG-15). Un error se corrige con `Activo = FALSE` |
| Reportes históricos | RG-18: un histórico nunca filtra por el estado actual del activo, o al dar de baja uno desaparecen sus mantenimientos pasados |
| Creación de órdenes desde la app | **Aplazada, no descartada.** `OT_OrdenesTrabajo` no admite `Adds` mientras `OTID` haga de clave y de etiqueta legible a la vez. Mientras tanto las órdenes se crean en el Sheets, que **se salta todas las validaciones**: es aceptable en el piloto por volumen, no como procedimiento |
| Quién edita el Sheets | **Sin resolver.** Sigue sin haber una regla escrita, y hay dos cuentas con permiso |

Las actas están en `docs/sdd/`: `ACTA-001` a `ACTA-004`. Las especificaciones que las produjeron
—`ESPEC-001`, `001B` y `001C`— están en `docs/historico/`, ejecutadas y cerradas.

**Y lo que esta fase no arregló, porque no era suyo:** la aplicación seguía con el esquema viejo.
Eso se resolvió el 2026-08-09 reconstruyéndola, no reconciliando nada más.

---

## 5. Fase 1 — Datos maestros

Es la fase más larga y la que fija el cronograma. **Todo su contenido es trabajo de operación**,
y por eso no hay forma de adelantarlo desde el repositorio.

- [ ] **D-01.** Levantamiento en campo de las coordenadas reales y carga en `ACT_Activos.Ubicacion`.
      Los 34 de fixture comparten una coordenada de Bogotá; las 355 sintéticas están interpoladas
      sobre el corredor. **Ninguna sirve para cerrar una orden con un técnico delante**
- [ ] **D-09.** Construcción de los 17 bancos de preguntas que faltan en `FRM_Preguntas`. Hoy hay
      15 preguntas y las 15 son del formulario de postes SOS
- [ ] Poblar `ROL_Roles` con los doce oficios del Plan Maestro. **Es lo más barato que hay
      pendiente:** doce filas en una tabla que ya existe, sin tocar ninguna regla
- [ ] Asignar zona en `ASG_AsignacionZona` a los técnicos que no la tienen. Hay 4 asignaciones y 11
      usuarios: quien no tenga fila abre la aplicación y no ve nada
- [ ] Confirmar el umbral de GPS. La hoja dice 40 m en `PAR_Parametros`; la propuesta enviada decía
      50. Hay que quedarse con uno
- [ ] Corrección de los encabezados con codificación corrupta en el Excel
- [~] **Código QR: FUERA DE ALCANCE por decisión del 7 de agosto de 2026.** Primero tiene que
      funcionar el ciclo básico. El hallazgo se conserva porque es real: `ACT_Activos.CodigoQR` está
      poblado, pero su valor es una copia literal de `CodigoActivo`, y AppSheet lee códigos pero no
      los genera ni los imprime. **Consecuencia que se asume:** el activo se abre por lista y
      `MAN_Mantenimientos.OrigenApertura = Lista` deja de ser excepción. Si se retoma, falta decidir
      qué se codifica, quién genera las imágenes, en qué material se imprime, quién las instala y
      cómo se verifica que cada etiqueta quedó en su equipo
- [x] **Diccionario de datos regenerado.** `docs/bd.md` ya no se escribe: sale de
      `generar_diccionario_bd.py` leyendo la hoja
- [x] **`TIP_TiposActivo.FormularioID` mapeado en los 18 tipos.** Y el modelo lo declara descartado:
      el formulario es de la tarea, no del tipo. Se retira en el paso 1 del orden de implementación
- [x] **Checklist huérfano remediado.** `CHK_Checklists` cuelga hoy de `MantenimientoID`, no de la
      orden

**Cierra cuando:** las coordenadas son todas distintas y están sobre el corredor; los 18 formularios
tienen preguntas; y un usuario de prueba ve activos al aplicar el filtro.

---

## 6. Fase 2 — Configuración en AppSheet

**Las reglas de datos ya están puestas.** Lo que queda de esta fase es la **interfaz**, y hay un
requisito previo que no es de configuración sino de modelo.

Hecho, y pendiente solo de demostrarlo con `PRUEBA-003`:

- [x] Geofencing, con la expresión que atraviesa la orden y el activo:
      `DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]`
      y mensaje de error en texto plano. **La variante con el literal `1.0` es la provisional**
- [x] Los dos filtros de seguridad: activos por unidad funcional, órdenes por técnico o supervisor
- [x] Las cuatro marcas de tiempo como `ChangeTimestamp` del servidor
- [x] Evidencia en tablas hijas, con `IsPartOf` en las cuatro que lo llevan

Pendiente:

- [ ] La regla del umbral de GPS **entera**, con su `OR(ISBLANK(...))`. Sin él, si alguien borra la
      fila del parámetro todos los cierres salen limpios y nadie se entera
- [ ] Imponer `QuienCambia`: hoy nada impide que un técnico ponga «Cerrada» él mismo
- [ ] Estado de rechazo. `MAN_Mantenimientos.ObservacionRechazo` existe y la orden no tiene a dónde
      volver
- [ ] Valores de `FIR_Firmas.TipoFirma`, hoy sin declarar
- [ ] Bots de notificación y de alerta. **No caben en el plan gratuito**: dependen de D-B
- [ ] **Declarar la interfaz en el modelo** —vistas, acciones y slices—, y generar de ahí el manual
      de pantallas. Mientras no exista, el paso de vistas de cualquier manual dice «se construye
      sola», que es la clase de instrucción que este proyecto tiene prohibida
- [ ] Reportes y tablero, según D-12 y D-13, encima de lo anterior

**Cierra cuando:** cada regla se demuestra funcionando en la app, no solo configurada.

---

## 7. Fase 3 — Prueba controlada

Etapa que no existía en la versión anterior y cuya ausencia habría llevado el primer error real
directamente a los 10 celulares del piloto.

- [ ] Un mantenimiento completo de extremo a extremo, ejecutado por una persona sobre un activo
      con coordenada real: apertura por lista, checklist, fotografías, firma y cierre con GPS
- [ ] El mismo flujo repetido en modo avión, con verificación de la sincronización posterior
- [ ] Prueba del bloqueo: intentar cerrar lejos del activo y confirmar que el sistema lo impide

> **El par de pruebas del geofencing no discrimina hoy, y hay que decirlo.** Los registros de prueba
> tienen su coordenada en Bogotá y el activo sintético más cercano queda a 60 km, así que el cierre
> legítimo que debe aceptarse **es imposible sin desplazarse** y el que debe rechazarse se vuelve
> trivial. Antes era al revés. **Solo D-01 lo arregla.**

**Cierra cuando:** hay filas reales en `MAN_Mantenimientos` y en las tablas de evidencia,
verificadas leyendo el archivo. Las de hoy son de prueba y llevan el prefijo `TEST-`.

---

## 8. Fase 4 — Piloto de campo

- [ ] Instalación en los 10 móviles del grupo piloto y autenticación corporativa
- [ ] Verificación de que cada técnico descarga solo los activos de su zona
- [ ] Operación real durante una semana, con acompañamiento
- [ ] Registro de incidencias y ajuste de formularios según lo observado

**Cierra cuando:** los 10 técnicos completaron mantenimientos sincronizados desde el corredor y
las incidencias críticas están resueltas.

---

## 9. Fase 5 — Producción y evolución

- [ ] Construcción de los bancos de preguntas de los tipos de activo restantes, en tandas
- [ ] Generación automática de órdenes por frecuencia. **No es cuestión de tiempo: depende de D-B**,
      porque en el plan gratuito los procesos programados no se ejecutan
- [ ] Integración con Power BI para tableros ejecutivos
- [ ] Integración con mesas de ayuda para tickets de TI
- [ ] Respaldo automático de evidencias y base de datos

---

## 10. Lo que la versión 3 daba por hecho y no lo estaba

Se conserva porque explica por qué este documento exige un criterio de cierre por fase. **Cada línea
es un hito marcado como completado sin nada que lo demostrara.**

| Afirmación de la versión 3 | Realidad verificada el 2026-08-06 |
|---|---|
| "Fase 0 y 1: completado 100 %" | 8 bloqueantes abiertos |
| "Modelo de datos 17 tablas: done" | El libro de entonces tenía 24 hojas |
| "18 formularios dinámicos: done" | 1 de 18 con banco de preguntas, y sin mapeo desde el tipo de activo |
| "Validaciones GPS y Security Filter: done" | GPS inoperante por coordenada única; el filtro dejaría a los técnicos sin activos |
| "Pruebas QA y dictamen: done" | `MAN_Mantenimientos` vacía: el flujo nunca se ejecutó |
| "Estado actual: Fase 1.5, piloto" | El proyecto estaba en definición funcional |

**El problema de fondo no era la desactualización: era marcar hitos sin criterio de cierre.** Por eso
cada fase de este documento lleva el suyo, y por eso son hechos que otra persona puede comprobar
leyendo un archivo, no reportes de avance.

---
*Referencias:* [ESTADO.md](../ESTADO.md) | [FUNCIONAL_SGMC.md](FUNCIONAL_SGMC.md) | [INDICACIONES_POR_ROL.md](INDICACIONES_POR_ROL.md) | [historico/AUDITORIA_PLAN_Y_ROADMAP.md](historico/AUDITORIA_PLAN_Y_ROADMAP.md) | [MAP.md](../MAP.md)
