# Evolución del modelo de datos — Fase 2

Lo que el modelo actual no representa, descubierto al leer el **plan de mantenimiento real** de la
Concesión. No es una lista de mejoras: son huecos de dominio, y cada uno tiene detrás un documento
o una conversación con operación.

**Esto no invalida la Fase B.** Ver la sección 9.

> ## Qué cambió desde que se escribió (2026-08-09)
>
> El backlog sigue en pie entero. Dos cosas que este documento daba por pendientes ya no lo están:
>
> - **`TIP_TiposActivo.RadioGeofencingKm` ya no está vacío en `BD/Modelo_Datos_PLANTILLA.xlsx`.** Se
>   pobló por familia de activo, y con los valores que la sección 6 pedía, en los **27 tipos** que
>   trae hoy la plantilla. Deja de ser deuda; pasa a ser una decisión tomada. **En la hoja de
>   producción sigue vacío en sus 18 tipos**, y eso no ha cambiado.
> - **Los 355 activos ya están en `BD/Modelo_Datos_PLANTILLA.xlsx`**, como inventario **sintético**
>   de prueba. Son códigos reales del Plan Maestro con coordenadas interpoladas, y cada fila lo dice
>   de sí misma. No es el registro real, así que el hueco de la sección 13.1 sigue abierto.
>
> Y una cifra que estaba mal: la cuota de Drive **no** se agota antes de la retención con este
> inventario. Ver la sección 8, corregida contra `scripts/capacidad.py`.

| | |
|---|---|
| Estado | Backlog de modelo. Ninguna pieza es todavía una especificación ejecutable |
| Origen | `contexto/`, aportado el 2026-08-07. Revisado el 2026-08-09 |
| Cuando una pieza se pueda ejecutar | Pasa a `ESPEC-004`, `005`… con su `PRUEBA` y su veredicto |

## 1. Por qué existe

El modelo se construyó antes de ver el plan de mantenimiento. Por eso simplifica cosas que en la
operación son distintas: asume que un activo es **una cosa con una coordenada que se visita**, que
tiene **una frecuencia**, y que se inspecciona con **un formulario**.

Ninguna de las tres es cierta para una parte importante del parque.

### Los documentos que lo revelaron

| Documento | Qué aporta |
|---|---|
| `Plan Maestro de Mantenimiento ITS_TI.xlsx` | 24 tipos de equipo, cantidades reales, tarea, periodicidad, herramienta y **personal** |
| `PLAN_MANTENIMIENTO_SISGA_2026.docx` | El plan vigente, con alcance por subsistema |
| `Plan de actividades de mantenimiento 2025 Componente ITS.xls` | **Cronograma contractual**, supervisado por JOYCO S.A.S. Es contra lo que mide la interventoría |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` | **La manta**: rejilla semanal tarea × sector, con planeadas contra ejecutadas |
| `2-MANTENIMIENTO.pdf` | Flujo de correctivo, SLA con números, y **GIMAN**, el GMAO que este sistema replica |
| `Informe … enero 2025 v1.1.docx` | Las secciones que el informe mensual exige |

**Los siete documentos están leídos y destilados en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md).**
Lo que sigue en este documento son los huecos de modelo; lo que aporta cada fuente está allí.

## 2. El tamaño real

| | Modelo | Realidad |
|---|---|---|
| Activos | 34 | **355** contables |
| Tipos | 18 —hoy 27 en el catálogo, ver el recuadro | **24** |
| Postes SOS | 3 | **54** |
| Switches capa 2 | 0 | **142** |
| Fibra troncal | 1 fila | **137 km**, ~600 cajas |

Los 34 se reparten entre uno y tres por tipo sobre los 18 que había: una muestra sintética. El
piloto corre sobre el 10% del parque.

> **Desde el 2026-08-09 la plantilla lleva los 355**, con los códigos del Plan Maestro —`SOS_1` a
> `SOS_54`, `SWIT_1` a `SWIT_142`— y coordenadas interpoladas sobre los 137 km del corredor. **Son
> de prueba**: sirven para ejercitar el filtro por zona, la navegación y el volumen de
> sincronización, y cada fila lo declara en `ACT_Activos.Observaciones`. Con los 34 de fixture
> delante, la plantilla tiene **389 filas**.
>
> **Y los tipos del catálogo pasaron de 18 a 27**, no a 24. Se sumaron los nueve que le faltaban a
> las familias del Plan Maestro —báscula dinámica, carril de peaje, electrónica de peaje, estación
> de toma de datos, paso seguro, switch de capa 3, computador portátil, impresora y cámara OCR de
> pesaje—, con lo que **las 18 familias tienen hoy tipo y formulario propios**. Los otros nueve
> tipos —generador, báscula, fibra, video wall, router, firewall, UPS, NAS y subestación— no
> corresponden a ninguna familia contable y vienen del fixture. **Sigue siendo otra lista que la de
> los 24 tipos del Plan Maestro**, y el hueco de la sección 3 no lo cierra ninguna carga de datos.

**Órdenes preventivas al año, calculadas del plan real: 1.916.** Ocho por día hábil, dos por
técnico. Manejable a mano, aunque sean 2.000 filas anuales tecleadas.

---

## 3. Tareas por tipo de equipo

**Hoy:** un activo tiene una `FrecuenciaID`, y un tipo tiene un `FormularioID`.

**Realidad:** cada tipo de equipo tiene **varias tareas**, cada una con su periodicidad y su
contenido. El cronograma 2025 lo separa explícitamente:

```
S.O.S. cantidad 54
    ├── Inspección en campo
    └── Ejecución Mantenimiento
```

**Qué cambia**

```
TIP_TiposActivo
   └── TAR_Tareas        ← NO EXISTE
         TareaID · TipoActivoID · Nombre · FrecuenciaID · FormularioID · TipoMtto

ACT_Activos      hereda las tareas de su tipo. No define frecuencia propia
PLA_PlanMantenimiento        = activo × tarea, con su propia próxima fecha
OT_OrdenesTrabajo gana TareaID: la orden dice QUÉ rutina se ejecuta
```

**Se retiran dos columnas que están en el sitio equivocado:** `ACT_Activos.FrecuenciaID` —la
periodicidad es de la tarea, no del poste— y `TIP_TiposActivo.FormularioID` —el formulario es de la
tarea, no del tipo—. Esa segunda es la que llevaba 18 fórmulas de hoja de cálculo hasta el
2026-08-07.

**Efecto en volumen:** con dos tareas por tipo en lugar de una, las 1.916 órdenes anuales se acercan
a 3.000-3.500. Doce o catorce al día. Ahí la creación manual deja de ser razonable.

---

## 4. Ubicación jerárquica

**Hoy:** todo activo tiene `UnidadFuncionalID` y `PR`. Por eso el relleno le puso punto de
referencia vial a un servidor:

```
SVR-001   Servidor 001     PR = 01+111   UF4
NAS-001   NAS 001          PR = 02+111   UF4
```

**Realidad:** es una jerarquía, no una alternativa. El peaje **está** en la vía y pertenece a una
unidad funcional; el equipo de dentro hereda esa cadena.

```
Unidad Funcional
   ├── Edificación   (CCO, peaje, báscula)      ← con su PR y su coordenada
   ├── Estructura    (puente, viaducto)          ← NO EXISTE
   └── Punto de vía  (PR)
```

**Qué cambia**

- `SED_Sedes` gana `UnidadFuncionalID`, `PR` y `Ubicacion`. Hoy una edificación **no está en
  ningún sitio**: solo tiene nombre y ciudad.
- `ACT_Activos` gana `SedeID` **opcional**: se llena solo si el equipo está dentro de un recinto.
  `UnidadFuncionalID` sigue siendo obligatorio.
- Aparece **`ETR_Estructuras`**: puentes y viaductos por los que pasa la fibra y que exigen revisión
  propia.
- `SED_Sedes` se limpia de las filas UF1-UF4, que ya viven en `UNF_UnidadesFuncionales`.

**Lo que arregla:** el Security Filter deja de tener un agujero. Con todo colgando de la UF, el
técnico asignado a UF1 ve los postes de su tramo **y** los equipos del peaje que está en él. Hoy
funciona por accidente, porque el relleno metió los servidores en UF4.

**Decisión pendiente:** la sede de Bogotá no está en el corredor y aloja 29 portátiles y 3
impresoras. O `UnidadFuncionalID` admite vacío para sedes fuera del corredor, o se crea una UF
administrativa que no es un tramo de vía.

---

## 5. PR y PK conviven, y el PK hace falta

**No son dos nombres para lo mismo:**

| | Qué es | Uso |
|---|---|---|
| **PK** | Kilometraje lineal, continuo | Cálculo y localización de fallas |
| **PR** | Punto de referencia INVÍAS, marcado físicamente. **No es lineal** | Lo que usa operación |

**Consecuencia inmediata: con PR no se puede hacer aritmética.** `PR 12+400` menos `PR 10+200` no
son 2,2 km.

**Y por eso el PK es requisito, no comodidad.** El OTDR devuelve una distancia lineal —«pérdida a
37 km»— y para convertirla en una orden hay que traducirla a dónde ir:

```
37 km de fibra  →  PK 37+000  →  PR correspondiente  →  caja más cercana
```

Sin PK, el técnico recibe «pérdida a 37 km» y averigua a mano a qué altura del corredor está. Con
PK, el sistema le dice a qué caja ir. **El PK no sirve para medir longitudes: sirve para localizar
fallas.**

---

## 6. El subsistema de fibra

Es más rico que el resto del sistema junto, y **cuatro tareas distintas** con cuatro unidades de
trabajo:

| Tarea | Unidad de trabajo | Ubicación | Naturaleza |
|---|---|---|---|
| Inspección visual de cajas | Caja a caja | PR de cada caja | Lineal. Se tapa, se revisa que no haya robos ni daños, que esté marcada |
| Recorrido de la UF | **La unidad funcional** | Rango de PR | En vehículo, parando en cada caja |
| Inspección de estructura | **El puente, el viaducto** | La estructura | Revisión visual del paso de la fibra |
| Medición de potencia | **Entre edificaciones**, ODF a ODF | Dos puntos, ninguno en la vía | 48 hilos |

Ninguna de las cuatro es «visitar un activo puntual», que es lo único que el modelo sabe hacer hoy.

### Una medición que genera trabajo

La potencia se mide en los **ODF**, que están dentro de las edificaciones junto a los equipos L3.
De ahí sale:

- Pérdida progresiva → **orden preventiva**: ir a mejorar la potencia
- Corte → **orden correctiva**: ir a reparar, en el punto que indica el OTDR

Es el primer caso donde una inspección **genera automáticamente** otra orden, con su tipo y su
ubicación derivados de la medición. La pieza existe: `OT_OrdenesTrabajo.OTOrigenID`, que se puso
para las segundas visitas.

### Las cajas

~600 a georreferenciar, cada 2-3 km. **Fuera de alcance por ahora**: georreferenciarlas es un
proyecto propio, no una carga de datos. Mientras tanto, un tramo se representa por rango de PR con
una coordenada representativa.

### El radio de geofencing dejó de ser deuda

`TIP_TiposActivo.RadioGeofencingKm` se creó por tipo de activo y estuvo vacío en los 18 tipos que
había entonces. **Se pobló el 2026-08-09** en `BD/Modelo_Datos_PLANTILLA.xlsx`, y con los valores
que este apartado pedía. Al pasar el catálogo a 27 tipos, los 27 lo llevan:

| Familia | Radio | Tipos |
|---|---|---|
| Puntual: postes SOS, cámaras CCTV y OCR, gálibos, sensores, paso seguro, estación de toma de datos, video wall, UPS y equipos de TI | **0,05 km** — 50 m | 18 |
| Voluminoso o con recinto: PMV fijos y móviles, generador, básculas, peajes y subestación | **0,1 km** — 100 m | 8 |
| **Tramo de fibra** | **1,5 km** | 1 |

**En la hoja de producción esa columna sigue vacía en sus 18 tipos.** Lo poblado es la plantilla,
que todavía no se ha desplegado.

Sin él, o el poste admite 1 km —y no prueba nada— o el tramo rechaza cierres legítimos. Y con los 355
sintéticos repartidos por el corredor deja de ser una preferencia. Medido sobre las coordenadas de la
plantilla, contando cada activo dentro de su propio geofence:

| Radio | Activos por geofence | Máximo |
|---|---|---|
| 1 km, el literal provisional | **7,9 de media** | 14 |
| 0,05 km, el de los puntuales | 1,1 | 2 |
| 0,1 km | 1,3 | 4 |
| 1,5 km, el de la fibra | 11,7 | 20 |

**Con 1 km ninguno queda identificado de forma única**: el sistema probaría «estás en el corredor»,
no «estás frente al equipo». Con 50 m, **313 de los 355 —el 88 %— quedan solos en su geofence**. Ahí
está la diferencia entre una prueba de presencia y una de tránsito.

**El precio de la fibra, dicho claro:** 1,5 km mete 11,7 activos de media dentro del geofence, así
que confirma que el técnico estaba en ese tramo del corredor, no que estuviera trabajando en la
fibra. Un trabajo lineal no admite la misma prueba que uno puntual. Lo que conserva su valor son las
fotografías con coordenada propia.

**Lo que todavía no está cerrado es la expresión.** `PAR_Parametros` sigue llevando
`RADIO_GEOFENCING_KM = 1` como literal provisional, y hay documentos que mandan pegar esa variante.
Mientras la aplicación no lea el radio por tipo, la columna poblada no cambia nada.

---

## 7. Mediciones repetibles

Los **48 hilos** de una medición de ODF no son 48 preguntas de un formulario: un técnico no rellena
48 campos numéricos en un móvil, y triplicaría la tabla de detalle.

La forma correcta es la que el modelo **ya usa dos veces**, con `FOT_Fotografias` y `FIR_Firmas`:

```
MED_MedicionesHilo   (hija del checklist, IsPartOf)
    Hilo · Potencia_dBm · Atenuacion · Observacion
```

---

## 8. Dos hallazgos de capacidad, con número

Calculado con `scripts/capacidad.py`, escenario **«Inventario del Plan Maestro», 355 activos**. Es
el que corresponde a este documento; los otros tres del script son 34, 150 y 500.

**La sincronización se degrada.** AppSheet degrada por encima de **~50.000 filas por tabla**:

```
CHD_ChecklistDetalle:  76.680 filas/año  →  383.400 a 5 años
```

**Pasa el umbral en el primer año.** No es opcional archivar por año. Y eso **sin** contar las
mediciones de 48 hilos, que multiplicarían la tabla de detalle otra vez.

**El almacenamiento aprieta, y con 500 activos no llega.** Con los 355, la cuota de 15 GB de la
cuenta personal que hoy posee el backend da para **5,7 años** —13,10 GB a cinco años, el 87 %—
frente a los 5 de retención exigida. **No sobra nada.** Y en el escenario de corredor completo, 500
activos, **se agota en 4,1 años: antes de la retención**.

Esto da número a **D-A** (propiedad del backend) y **D-B** (plan de licenciamiento), enviadas a
Dirección como decisiones abstractas. Un «hace falta plan de pago» pesa poco; «la cuota da 5,7 años
para una retención de 5, y menos si el parque crece» decide.

---

## 9. El correctivo: lo más grande que falta

Fuente: `2-MANTENIMIENTO.pdf` §6 y §7. Detalle en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md) §3.

**Hoy `OT_OrdenesTrabajo` tiene `FechaProgramada` y `FechaCierre`.** Verificado contra
`BD/Modelo de Datos (11).xlsx` y `modelo_objetivo.py`: **no existe ninguna fecha de creación**.

Y eso es peor de lo que parece. `FechaCierre` menos `FechaProgramada` **no es una duración**: es
adherencia al cronograma —si se cerró antes o después de lo previsto—. El sistema no sabe cuándo
apareció el trabajo, solo cuándo estaba previsto. Para una preventiva eso basta. **Para una
correctiva no existe el dato de partida**, porque una avería no se programa: ocurre.

Ninguna de las tres cosas que se miden en un contrato de mantenimiento es derivable hoy:

- **Tiempo de respuesta** — desde el aviso hasta que **empiezan** los trabajos.
- **Tiempo de resolución** — desde el aviso hasta que está resuelta y el cliente informado.
- **Reloj parado** — el tiempo bloqueado por terceros o fuerza mayor **no cuenta**.

Sin `HoraAviso`, `HoraInicioTrabajos` y un acumulado de reloj parado, el sistema **no puede calcular
ninguno de los dos**. Y sin reloj parado, cualquier espera de repuesto se lee como incumplimiento.

**La criticidad tampoco es opinión:** se define por porcentaje de instalación afectada, y de ahí
salen los plazos.

| Criticidad | Servicio en avería | Respuesta | Resolución |
|---|---|---|---|
| Total / Crítica | 75–100 % | 2 h | 4 h |
| Parcial grave | 25–75 % | 4 h | 12 h |
| Parcial leve | ≤ 25 % | 12 h | 48 h |

**Qué cambia**

```
OT_OrdenesTrabajo gana   CriticidadID · HoraAviso · HoraInicioTrabajos
                          NivelAtencion (N1 · N2 · N3)  ← para el escalado
CRI_Criticidad     nuevo  catálogo con los plazos, para no enterrarlos en una expresión
EVT_EventosOrden   nuevo  hija de la orden: inicio · fin · motivo. El reloj parado se DERIVA
```

**`RelojParadoMin` no puede ser una columna acumulada.** Un total que se lee y se reescribe
**compite consigo mismo** en un backend offline-first sin transacciones: dos pausas registradas sin
señal producen una pérdida de actualización silenciosa. Es literalmente el argumento por el que
`OT_OrdenesTrabajo` perdió `Adds` en `ESPEC-002`. Va como tabla hija de eventos —solo se añade,
nunca se recalcula— y el total sale de un `SUM()`.

**`HoraInicioTrabajos` no se teclea, o no prueba nada.** RG-20 nos enseñó que un `Initial value` es
editable, y que en offline-first `NOW()` es el reloj del teléfono. Las tres formas obvias fallan:

| Forma | Por qué no sirve |
|---|---|
| `Initial value = NOW()` | Editable. El técnico puede cambiarla |
| `DateTime` que teclea el operador | Nada impide rellenarla al cerrar en vez de al empezar |
| `NOW()` en el dispositivo | Reloj del teléfono, no del servidor |

**Solo vale si la escribe la transición de estado**: al pasar la orden a `En ejecucion`, un
`ChangeTimestamp` la sella y `Editable_If = FALSE` la congela. Y aun así hay que decirlo entero:
**quien escriba directamente en el Sheets se lo salta**, porque hay dos cuentas con permiso de
edición. Eso no es gobierno, es arquitectura.

**Advertencia de procedencia: esos plazos son de ETRA en el corredor Neiva–Girardot, no del Sisga.**
Sirven como forma, no como cifra. Antes de codificarlos hay que confirmar los del Sisga — y si no
existen, decidir si el sistema los mide igual.

**Y hay una decisión de alcance del piloto detrás:** si el piloto incluye correctivo, `CU-02` deja
de estar diferido y `OT_OrdenesTrabajo` necesita `Adds`. Hoy está aplazado.

---

## 10. Perfiles del técnico

**Planteado por operación:** el usuario debería tener propiedades —electricista, alturas,
electrónico, ayudante, SISO— y programarse según ellas. Un técnico puede estar o no habilitado.

**Qué cambia**

```
CER_Certificaciones   catálogo: Alturas · Electricista · Electrónico · Ayudante · SISO
USR_Certificaciones   usuario × certificación · fecha de vencimiento
```

Dos tablas de cuatro columnas. Lo que sí toca algo construido es **la asignación**: hoy
`ASG_AsignacionZona` asigna técnico a unidad funcional y el filtro RG-04 se apoya en eso. Asignar
por especialidad significa que la asignación deja de depender solo de la zona.

**La parte que muerde es la vigencia.** Un certificado de alturas caduca. Si el sistema decide quién
puede hacer qué, tiene que saber si sigue vigente **el día del trabajo** — y eso ya no es una
etiqueta, es una regla que se evalúa contra una fecha.

**Un dato en contra, y conviene tenerlo escrito:** GIMAN, el GMAO de referencia, registra al técnico
con **nombre, identificador y empresa**, nada más. Resolvió la asignación por zona y por brigada, y
funcionó. No invalida la propuesta; sí sugiere que no es lo primero.

**Va a Fase 2**, por decisión de operación del 2026-08-07.

**Y falta un nivel intermedio que GIMAN sí tiene:** Técnico → Supervisor/Capataz → **Cuadrilla**.
Nuestro modelo salta de técnico a zona sin brigada.

---

## 11. El informe mensual, y tres columnas que no se retiran

El informe de enero 2025 tiene secciones que el modelo debe poder alimentar. Dos hallazgos:

**El anexo sale del sistema tal cual.** Fotografías con su coordenada y su hora, más el detalle del
checklist ítem por ítem. `FOT_Fotografias` y `CHD_ChecklistDetalle` ya lo dan **sin teclear nada**.
Para una preventiva, el checklist **es** la descripción de lo que se hizo.

**Pero el correctivo no cabe en un checklist.** Cuando se repara una avería, el informe pide qué
estaba averiado y qué repuesto se usó, y eso no sale de una lista de sí/no. Dos salidas, las dos
baratas:

- Reactivar `Diagnostico` y `Repuestos_Utilizados`, condicionados al tipo de la **orden**. La
  expresión es `[OTID].[Tipo]`, no `[Tipo]`: `MAN_Mantenimientos` no tiene `Tipo` —se retiró porque
  el tipo es de la orden, no de la ejecución—. **Y esa expresión no se puede escribir hasta que la
  Fase B convierta `OTID` en `Ref`**: hoy es texto y no se desreferencia.
- O que el correctivo use un **formulario propio** con esas preguntas — más coherente con la capa de
  tareas de la sección 3, y no cuesta columnas.

**Se elige la segunda.** Reactivar columnas crea dos sitios que dicen lo mismo: `Requiere_Repuesto`
se retiró porque «se cubre con `MotivoPendienteID` = Falta de repuesto», y devolver
`Repuestos_Utilizados` dejaría dos registros del mismo hecho sin forma de saber cuál miente. Un
formulario propio para el correctivo no duplica nada y encaja en la capa de tareas.

**Lo que no cambia:** los tres campos siguen marcados como retirados y **siguen presentes en la
hoja**. Eso ya era así —la Fase A no borra nada— y no es una decisión nueva. Se confirma, no se
revierte.

**Y dos patrones vistos en el informe de Neiva–Girardot**, que **no son huecos del Sisga** hasta que
operación lo confirme:

- Su Tabla 1 es una matriz **unidad funcional × tipo de equipo**, y allí las UF se subdividen
  —2,1 · 2,2 · 4,1 · 4,2—. `UNF_UnidadesFuncionales` es plana. **¿Las UF del Sisga se subdividen?**
- Incluye un tipo **`ILUMINACION`** que no está en nuestros 24. En el Plan Maestro del Sisga no
  aparece. **¿El Sisga mantiene iluminación, o no es de su alcance?**

---

## 12. Lo que NO cambia

Conviene decirlo, porque llevamos once rondas de revisión sobre la Fase B y sigue siendo válida.

El cableado de referencias, el geofencing, el filtro por zona, el histórico que no se borra, la
cadena de evidencia y las 17 pruebas de `PRUEBA-002` **valen igual**. Todo eso opera sobre activos
que sí son puntos en el mapa, que son la mayoría y los que más órdenes generan.

Lo que este documento añade es **una capa entre el tipo y el trabajo**, y **una jerarquía de
ubicación**. Se retiran dos columnas que estaban mal colocadas. Nada de lo construido se tira.

---

## 13. Preguntas abiertas

Ninguna se puede responder desde los documentos. Los siete están leídos: lo que sigue aquí es lo que
hay que preguntar en operación.

1. **El inventario real del Sisga.** Trabajamos con 355 activos de un maestro «muy similar», no el
   de este corredor. Todo el dimensionamiento —1.916 órdenes al año, los 5,7 años de cuota— cuelga
   de ahí. **Es el vacío más grande que queda**, y la plantilla de 355 activos sintéticos no lo
   cierra: son códigos del Plan Maestro con coordenadas inventadas, no el registro del corredor.
2. **¿Cuántas estructuras** —puentes, viaductos— tienen paso de fibra, y están inventariadas?
3. **¿El mantenimiento de fibra se programa por tramo o por ruta completa?** De ahí salen 1.200
   órdenes al año o 2.
4. **¿Las 600 cajas existen en algún inventario** —Excel, plano, GIS— o hay que levantarlas?
5. **¿Un tipo de equipo tiene siempre las mismas tareas**, o varían por unidad funcional?
6. **La sede de Bogotá**, fuera del corredor: ¿UF vacía o UF administrativa?
7. **¿El Sisga tiene SLA contractuales propios?** Los plazos de la sección 9 son de otro corredor.
8. **¿Quién puede dar el aviso de una correctiva?** ETRA lo restringe a operadores autorizados.
9. **¿Hay almacén de repuestos gestionado**, o los repuestos se anotan en texto libre?
10. **`PRUEBA MENSUAL CON INTERVENTORÍA`**: ¿la firma el interventor en la app, o basta registrar
    que asistió? `FIR_Firmas` existe, pero ninguna tarea sabe exigir firma de un tercero.
