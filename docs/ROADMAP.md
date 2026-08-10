# ROADMAP de implementación — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 10 de agosto de 2026 | **Versión:** 4.2

> ## Para qué sirve este documento, y para qué no
>
> **El estado del proyecto está en [`ESTADO.md`](../ESTADO.md), no aquí.** Este documento es el
> **orden de implementación**: qué va antes que qué, y por qué ese orden y no otro. Es lo que no
> cabe en un tablero de estado y lo que más caro sale improvisar.
>
> **Qué cambió en la 4.2, del 2026-08-10:**
>
> - **La aplicación se volvió a reconstruir desde cero, y la vigente es `SISGA_-323965761-26-08-10`
>   sobre la hoja `Modelo_Datos_10082026`.** Entre el 6 y el 10 de agosto hubo cinco aplicaciones y
>   tres hojas; las superadas están nombradas, con su motivo, en `scripts/sistema.py`.
> - **El cableado de la aplicación anterior no sobrevivió, y por eso se repone entero.** La versión
>   4.1 daba las 39 referencias por puestas: hoy la aplicación tiene **las 28 tablas dadas de alta y
>   nada más**. Referencias, reglas y filtros están sin poner.
> - **La migración a la hoja limpia ya se ejecutó**, así que dejó de ser una decisión y pasó a ser un
>   hecho. `BD/Modelo_Datos_PLANTILLA.xlsx` sale generada del modelo y es el archivo publicado.
> - **Las referencias son 38, no 15.** Las 15 eran las que faltaban en una aplicación anterior donde
>   otras 23 ya estaban puestas. Sobre una aplicación nueva no sobrevive ninguna.
> - **La Fase 0.5 de reconciliación de modelos está cerrada**, y su lista de tareas —que ocupaba la
>   mitad de este documento— se ha reducido al registro de lo que dejó decidido.
>
> El documento funcional que se entrega es [`FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md). El contexto
> operativo destilado está en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md). El reparto de quién
> hace qué, en [`INDICACIONES_POR_ROL.md`](INDICACIONES_POR_ROL.md).

> **De dónde viene la versión 4.** La 3 declaraba completadas al 100 % la Fase 0 y la Fase 1, y la
> auditoría del 6 de agosto de 2026 verificó contra el archivo que era falso. Ese dictamen,
> `AUDITORIA_PLAN_Y_ROADMAP.md`, se retiró en la limpieza del 2026-08-10; sus hallazgos `B-01` a
> `B-14` son el origen de casi todo lo que se decidió después.
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
| **Esquema** — tablas y columnas | **Antes del piloto, todo junto** | `MAN_Mantenimientos` está **vacía**, y con ella las demás transaccionales. Añadir hoy cuesta cero; después cuesta migración |
| **Datos** — inventario, coordenadas | En medio, con las referencias ya tipadas | Así AppSheet valida cada fila al cargarla, gratis |
| **Comportamiento** — reglas, permisos | Después, en cualquier orden | No tocan datos. Se endurece con el sistema andando |

### La secuencia

| # | Paso | Contenido | Depende de |
|---|---|---|---|
| **0** | **Cablear la aplicación entera** | **Las 39 referencias**, con `IsPartOf` en las cuatro que lo llevan; **las 21 reglas**; los dos filtros de seguridad; las cuatro marcas de tiempo como `ChangeTimestamp`; retirar `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos`; y correr `PRUEBA-003` | Sin empezar. Ficha por tabla en [`MANUAL_DESPLIEGUE.md`](MANUAL_DESPLIEGUE.md); expresión completa en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) |
| **0b** | ~~Decidir la migración~~ | **Ejecutada el 2026-08-10.** Las 47 columnas ya no existen en el archivo, así que ocultarlas dejó de estar en el plan y con ellas se fueron las tres trampas | Cerrado |
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

> ### La migración a la hoja limpia, decidida el 2026-08-09 y **ejecutada el 2026-08-10**
>
> **El Excel del repositorio es lo que se entrega, y es la hoja que la aplicación lee.** El funcional
> parte de ese archivo y desde ahí sigue las guías, así que tenía que salir generado y limpio en vez
> de ser una hoja heredada con 47 columnas escondidas encima.
>
> **Lo que cambió al ejecutarla:** ocultar esas 47 salió del plan —ya no existen en el archivo, y con
> ellas se fueron las tres trampas—, y el literal provisional de `1.0` km dejó de aplicar, porque
> `TIP_TiposActivo.RadioGeofencingKm` viene poblado en los 27 tipos de la hoja que la aplicación lee.
>
> **Lo que lo hizo posible:** `scripts/generar_plantilla.py`. La plantilla sale entera de un comando
> y se reproduce celda por celda, con los 27 tipos del catálogo y **cero activos viendo el checklist
> de otro equipo**.

| Fase | Estado | Criterio de cierre |
|---|---|---|
| Sprint 0. Definición funcional | **Cerrado por supuestos.** No se espera respuesta | Los catorce adoptados por escrito en `ALCANCE_Y_SUPUESTOS_SGMC.md`, con su estado de cierre |
| Fase 0.5. Reconciliación de modelos | **CERRADA** el 2026-08-07 | `modelo_objetivo.py` es la fuente única; los documentos se generan de él. Ver 4.5 |
| **Fase A. La hoja** | **CERRADA** | `verificar_faseA.py` en 0 fallos sobre `BD/Modelo_Datos_PLANTILLA.xlsx`. Hoy: **52 conformes y 4 avisos esperados** |
| Reconstrucción de la aplicación | **HECHA** el 2026-08-10 | `SISGA_-323965761-26-08-10`, con las 28 tablas dadas de alta sobre `Modelo_Datos_10082026` |
| **Fase B. Cableado y reglas** | **Sin empezar.** Se repone entero: el cableado de la aplicación anterior no sobrevivió a la reconstrucción | Las 39 referencias con su `IsPartOf`, las 21 reglas, los dos filtros, las cuatro marcas de tiempo, `Deletes` retirado, y `PRUEBA-003` pasada |
| Fase 1. Datos maestros | Bloqueada por D-01 y D-09 | Coordenadas reales cargadas, sedes realineadas, bancos de preguntas construidos |
| Fase 2. Configuración de interfaz | Bloqueada por Fase 1 y por declarar vistas | Reportes y pantallas construidos. **Antes hay que declarar la interfaz en el modelo**: hoy no tiene vistas, ni acciones, ni slices |
| Fase 3. Prueba controlada | Bloqueada por Fase 2 | Registros reales en `MAN_Mantenimientos` y en las tablas de evidencia, verificados leyendo el archivo |
| Fase 4. Piloto de campo | Bloqueada por Fase 3 | 10 técnicos operando una semana, con registros sincronizados desde el corredor |
| Fase 5. Producción y evolución | Bloqueada por Fase 4 | Ninguna pregunta marcada como borrador, integraciones y respaldo automático |

**No hay fechas.** El cronograma depende de dos tareas que son trabajo del cliente y cuya duración
solo el equipo de la Concesión puede estimar: el levantamiento de las coordenadas reales (decisión
D-01) y la redacción de los bancos de preguntas (decisión D-09). Las fechas se fijan en el acta de
la mesa de trabajo, no antes.

---

## 3.1 Lo que sí está construido

Verificado el 2026-08-10 contra `scripts/modelo_objetivo.py` y `BD/Modelo_Datos_PLANTILLA.xlsx`.
**Cada cifra se rederiva con los verificadores; ninguna está escrita de memoria.**

- **Modelo de 28 tablas, 205 columnas, 39 referencias y 21 reglas.** `validar_modelo.py` sale
  `APTO PARA DESPLEGAR` con 0 errores y 3 avisos.
- **La hoja se genera del modelo, y es la que la aplicación lee.** 28 pestañas de datos más `_LEEME`,
  ninguna oculta, sin una sola columna de sobra: las 43 retiradas ya no existen en el archivo.
- **Aplicación reconstruida el 2026-08-10 con las 28 tablas dadas de alta.** Eso es todo lo que
  tiene: las referencias, las reglas y los filtros **no están puestos**.
- **Inventario de prueba: 368 filas en `ACT_Activos`.** 334 son sintéticas —códigos del Plan Maestro
  repartidos por los 137 km del corredor, y cada una lo declara en `ACT_Activos.Observaciones`— y 34
  son el juego de arranque. Las familias contables suman los 355 del Plan Maestro; las 13 filas
  restantes son equipos que el Plan no cuenta por unidades.
- **`TIP_TiposActivo.RadioGeofencingKm` poblado en los 27 tipos**, por familia: 0,05 km en 18,
  0,1 km en 8 y 1,5 km en la fibra. **Al leer la aplicación esta hoja, el literal provisional de
  1,0 km dejó de aplicar**, y `PAR_Parametros.RADIO_GEOFENCING_KM` queda como valor histórico que
  `RG-01` no lee.
- Catálogos poblados: 27 tipos de activo con sus 27 formularios, 14 secciones, 10 tipos de respuesta,
  10 sedes, 4 unidades funcionales con su rango de PR, 4 roles, 11 usuarios, 4 asignaciones de zona,
  5 motivos de pendiente, 5 modos de falla, 7 estados de orden, 3 parámetros y los catálogos viales
  de calzada, sentido, estado y frecuencia.
- **Banco de preguntas: 333 preguntas, los 27 formularios con contenido**, y 108 valores de lista.
  288 preguntas llevan `[BORRADOR: validar con operacion]`; las 45 restantes —SOS, CCTV y PMV fijo,
  15 cada uno— ya estaban acordadas.
- **Sin un solo registro transaccional.** `OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `CHK_Checklists`,
  `CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `NOV_Novedades` y `PLA_PlanMantenimiento`
  están vacías. **El ciclo no se ha recorrido de extremo a extremo ni una vez.**

**Y lo que está declarado pero no se puede probar:** el geofencing. Los 34 activos del juego de
arranque comparten una coordenada de Bogotá y las 334 sintéticas están interpoladas, así que la
prueba del cierre legítimo no se puede ejecutar sin desplazarse. Es D-01.

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
| Columnas de GPS en `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` como `LatLong` y `Precision_GPS` como `Number`. AppSheet las había inferido mal y cruzadas |
| `EOT_EstadosOrden` | Sus claves son el nombre del estado, no `1..7`. Un catálogo se diseña mirando los datos que va a resolver |
| `IsPartOf` sobre `MAN_Mantenimientos.OTID` | **Va sin él.** La ejecución es el registro histórico y sobrevive a su orden |
| Borrado del histórico | Se retira `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` (RG-14 y RG-15). Un error se corrige con `Activo = FALSE` |
| Reportes históricos | RG-18: un histórico nunca filtra por el estado actual del activo, o al dar de baja uno desaparecen sus mantenimientos pasados |
| Creación de órdenes desde la app | **Aplazada, no descartada.** `OT_OrdenesTrabajo` no admite `Adds` mientras `OTID` haga de clave y de etiqueta legible a la vez. Mientras tanto las órdenes se crean en el Sheets, que **se salta todas las validaciones**: es aceptable en el piloto por volumen, no como procedimiento |
| Quién edita el Sheets | **Sin resolver.** Sigue sin haber una regla escrita, y hay dos cuentas con permiso |

Las actas que cerraron esta fase, `ACTA-001` a `ACTA-004`, y las especificaciones que las produjeron
—`ESPEC-001`, `001B` y `001C`— **se retiraron en la limpieza del 2026-08-10**: estaban ejecutadas y
cerradas, y describían aplicaciones y hojas superadas. Lo que dejaron decidido es la tabla de arriba,
y eso no se reabre.

**Y lo que esta fase no arregló, porque no era suyo:** la aplicación seguía con el esquema viejo.
Eso se resolvió el 2026-08-09 reconstruyéndola, no reconciliando nada más.

---

## 5. Fase 1 — Datos maestros

Es la fase más larga y la que fija el cronograma. **Todo su contenido es trabajo de operación**,
y por eso no hay forma de adelantarlo desde el repositorio.

- [ ] **D-01.** Levantamiento en campo de las coordenadas reales y carga en `ACT_Activos.Ubicacion_LatLong`.
      Los 34 del juego de arranque comparten una coordenada de Bogotá; las 334 sintéticas están
      interpoladas sobre el corredor. **Ninguna sirve para cerrar una orden con un técnico delante**
- [ ] **D-09.** Validación de las **288 preguntas en borrador** de `FRM_Preguntas`, repartidas en 24
      de los 27 formularios. No están por escribir: están escritas y marcadas
      `[BORRADOR: validar con operacion]` en su ayuda, y el día que no aparezca ninguna el banco
      está cerrado. Las 45 de SOS, CCTV y PMV fijo ya estaban acordadas
- [ ] Poblar `ROL_Roles` con los doce oficios del Plan Maestro. **Es lo más barato que hay
      pendiente:** doce filas en una tabla que ya existe, sin tocar ninguna regla. Ojo: para que
      compren algo hace falta `USR_Usuarios.OficioID`, que no existe — ver `ESPEC-003` §5.4
- [ ] Asignar zona en `ASG_AsignacionZona` a los técnicos que no la tienen. Hay 4 asignaciones y 11
      usuarios: quien no tenga fila abre la aplicación y no ve nada
- [ ] Confirmar el umbral de GPS. La hoja dice 40 m en `PAR_Parametros`; la propuesta enviada decía
      50. Hay que quedarse con uno
- [x] **Encabezados sin codificación corrupta.** La hoja se genera del modelo, así que el mojibake
      que arrastraba la heredada desapareció con ella: ninguno de los 202 encabezados lo tiene
- [~] **Código QR: FUERA DE ALCANCE por decisión del 7 de agosto de 2026.** Primero tiene que
      funcionar el ciclo básico. El hallazgo se conserva porque es real: `ACT_Activos.CodigoQR` está
      poblado, pero su valor es una copia literal de `CodigoActivo`, y AppSheet lee códigos pero no
      los genera ni los imprime. **Consecuencia que se asume:** el activo se abre por lista y
      `MAN_Mantenimientos.OrigenApertura = Lista` deja de ser excepción. Si se retoma, falta decidir
      qué se codifica, quién genera las imágenes, en qué material se imprime, quién las instala y
      cómo se verifica que cada etiqueta quedó en su equipo
- [x] **Diccionario de datos regenerado.** `docs/bd.md` ya no se escribe: sale de
      `generar_diccionario_bd.py` leyendo la hoja
- [x] **`TIP_TiposActivo.FormularioID` mapeado en los 27 tipos**, sin una fila sin formulario. Y el
      modelo lo declara descartado: el formulario es de la tarea, no del tipo. Se retira en el paso 1
      del orden de implementación
- [x] **Checklist huérfano remediado.** `CHK_Checklists` cuelga hoy de `MantenimientoID`, no de la
      orden

**Cierra cuando:** las coordenadas son todas distintas y están sobre el corredor; las 288 preguntas
en borrador están validadas; y un usuario de prueba ve activos al aplicar el filtro.

---

## 6. Fase 2 — Configuración en AppSheet

**Las reglas están declaradas en el modelo y ninguna está puesta en la aplicación.** La versión 4.1
las daba por configuradas, y describía el cableado de una aplicación que ya no existe. Lo que queda
de esta fase son dos bloques: reponer el comportamiento, y después la **interfaz**, que además tiene
un requisito previo que no es de configuración sino de modelo.

Declarado en el modelo, con su expresión completa en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md), y **sin poner**:

- [ ] Geofencing, con la expresión que atraviesa la orden y el activo:
      `DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]`
      y mensaje de error en texto plano. **El literal `1.0` ya no se usa**: la hoja que la aplicación
      lee trae el radio poblado en los 27 tipos
- [ ] `Editable_If = FALSE` en las cuatro columnas de captura de `MAN_Mantenimientos` (`RG-20`). **Sin
      esto el geofencing es decorativo**: el pin del mapa se arrastra encima del activo y la regla
      valida sin protestar
- [ ] Los dos filtros de seguridad: activos por unidad funcional, órdenes por técnico o supervisor
- [ ] Las cuatro marcas de tiempo como `ChangeTimestamp` del servidor
- [ ] Evidencia en tablas hijas, con `IsPartOf` en las cuatro que lo llevan, **y `Deletes` retirado
      antes** en `OT_OrdenesTrabajo` y `MAN_Mantenimientos`. El orden no es opcional: `IsPartOf` es
      borrado en cascada, y solo es seguro porque el mantenimiento nunca se borra
- [ ] La regla del umbral de GPS **entera**, con su `OR(ISBLANK(...))`. Sin él, si alguien borra la
      fila del parámetro todos los cierres salen limpios y nadie se entera

Pendiente, y además no declarado todavía en el modelo:

- [ ] Imponer `QuienCambia`: la columna está poblada en las siete filas y **ninguna de las 21 reglas
      la lee**, así que hoy nada impide que un técnico ponga «Cerrada» él mismo
- [ ] Estado de rechazo. `MAN_Mantenimientos.ObservacionRechazo` existe y la orden no tiene a dónde
      volver: falta una fila `Devuelta` en `EOT_EstadosOrden`, que es dato y no esquema
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

> **El par de pruebas del geofencing no discrimina hoy, y hay que decirlo.** Los 34 activos del juego
> de arranque tienen su coordenada en Bogotá, a unos 60 km del sintético más cercano sobre el
> corredor, así que el cierre legítimo que debe aceptarse **es imposible sin desplazarse** y el que
> debe rechazarse se vuelve trivial. **Solo D-01 lo arregla.**

**Cierra cuando:** hay filas reales en `MAN_Mantenimientos` y en las tablas de evidencia,
verificadas leyendo el archivo. **Hoy no hay ninguna, ni de prueba**: la hoja se entrega sin
registros a propósito, para que el primer ciclo que se recorra sea real.

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

- [ ] Cierre del banco de preguntas: que no quede ninguna marcada `[BORRADOR: validar con operacion]`
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
*Referencias:* [ESTADO.md](../ESTADO.md) | [FUNCIONAL_SGMC.md](FUNCIONAL_SGMC.md) | [INDICACIONES_POR_ROL.md](INDICACIONES_POR_ROL.md) | [MAP.md](../MAP.md)
