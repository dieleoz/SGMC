# Evolución del modelo de datos — Fase 2

Lo que el modelo actual no representa, descubierto al leer el **plan de mantenimiento real** de la
Concesión. No es una lista de mejoras: son huecos de dominio, y cada uno tiene detrás un documento
o una conversación con operación.

**Esto no invalida la Fase B.** Ver la sección 9.

| | |
|---|---|
| Estado | Backlog de modelo. Ninguna pieza es todavía una especificación ejecutable |
| Origen | `contexto/`, aportado el 2026-08-07 |
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
| Tipos | 18 | **24** |
| Postes SOS | 3 | **54** |
| Switches capa 2 | 0 | **142** |
| Fibra troncal | 1 fila | **137 km**, ~600 cajas |

Los 34 son **3 de cada tipo**: una muestra sintética. El piloto corre sobre el 10% del parque.

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
PLA_Plan         = activo × tarea, con su propia próxima fecha
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
- Aparece **`EST_Estructuras`**: puentes y viaductos por los que pasa la fibra y que exigen revisión
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

### El radio de geofencing deja de ser deuda

`TIP_TiposActivo.RadioGeofencingKm` se creó por tipo de activo y está vacío en los 18. Aquí es
donde hace falta:

| Tipo | Radio |
|---|---|
| Poste SOS, cámara | 50 m |
| **Tramo de fibra** | **1,5 km** |

Sin él, o el poste admite 1 km —y no prueba nada— o el tramo rechaza cierres legítimos.

**El precio, dicho claro:** un radio de 1,5 km confirma que el técnico estaba en ese tramo del
corredor, no que estuviera trabajando en la fibra. Un trabajo lineal no admite la misma prueba que
uno puntual. Lo que conserva su valor son las fotografías con coordenada propia.

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

Calculado con `scripts/capacidad.py` y con el volumen real del plan.

**La sincronización se degrada.** AppSheet degrada por encima de **~50.000 filas por tabla**:

```
CHD_ChecklistDetalle:  28.740 filas/año  →  143.700 a 5 años   (casi el triple)
```

No es opcional archivar por año. Y eso **sin** contar las mediciones de 48 hilos.

**El almacenamiento se agota antes que la retención.** Con inventario real, la cuota de 15 GB de la
cuenta personal que hoy posee el backend **se agota en 4,1 años**, antes de los 5 de retención
exigida.

Esto da número a **D-A** (propiedad del backend) y **D-B** (plan de licenciamiento), enviadas a
Dirección como decisiones abstractas. Un «hace falta plan de pago» pesa poco; «la cuota se agota
antes de la retención contractual» decide.

---

## 9. El correctivo: lo más grande que falta

Fuente: `2-MANTENIMIENTO.pdf` §6 y §7. Detalle en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md) §3.

**Hoy `OT_OrdenesTrabajo` tiene `FechaCreacion` y `FechaCierre`.** Eso da una duración total, y la
duración total no es ninguna de las dos cosas que se miden en un contrato de mantenimiento:

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
OT_OrdenesTrabajo gana   CriticidadID · HoraAviso · HoraInicioTrabajos · RelojParadoMin
                          NivelAtencion (N1 · N2 · N3)  ← para el escalado
CRI_Criticidad     nuevo  catálogo con los plazos, para no enterrarlos en una expresión
```

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

- Reactivar `Diagnostico` y `Repuestos_Utilizados` con `Required_If [Tipo] = "Correctivo"`.
- O que el correctivo use un **formulario propio** con esas preguntas — más coherente con la capa de
  tareas de la sección 3, y no cuesta columnas.

**Consecuencia inmediata sobre la Fase A:** `Diagnostico`, `Trabajo_Realizado` y
`Repuestos_Utilizados` están hoy en `CAMPOS_RETIRADOS` de `MAN_Mantenimientos`. **No se borran.**
Borrarlas y volver a necesitarlas es cambiar la base después de producción, que es justo lo que hay
que evitar.

**Otros dos huecos que abre el informe:**

- Su Tabla 1 es una matriz **unidad funcional × tipo de equipo**, y las UF se subdividen —2,1 · 2,2 ·
  4,1 · 4,2—. `UNF_UnidadesFuncionales` es plana.
- Incluye un tipo **`ILUMINACION`** que no está en nuestros 18.

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
   de este corredor. Todo el dimensionamiento —1.916 órdenes al año, los 4,1 años de cuota— cuelga
   de ahí. **Es el vacío más grande que queda.**
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
