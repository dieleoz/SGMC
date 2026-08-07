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

## 9. Lo que NO cambia

Conviene decirlo, porque llevamos once rondas de revisión sobre la Fase B y sigue siendo válida.

El cableado de referencias, el geofencing, el filtro por zona, el histórico que no se borra, la
cadena de evidencia y las 17 pruebas de `PRUEBA-002` **valen igual**. Todo eso opera sobre activos
que sí son puntos en el mapa, que son la mayoría y los que más órdenes generan.

Lo que este documento añade es **una capa entre el tipo y el trabajo**, y **una jerarquía de
ubicación**. Se retiran dos columnas que estaban mal colocadas. Nada de lo construido se tira.

---

## 10. Preguntas abiertas

Ninguna se puede responder desde los documentos:

1. **¿Cuántas estructuras** —puentes, viaductos— tienen paso de fibra, y están inventariadas?
2. **¿El mantenimiento de fibra se programa por tramo o por ruta completa?** De ahí salen 1.200
   órdenes al año o 2.
3. **¿Las 600 cajas existen en algún inventario** —Excel, plano, GIS— o hay que levantarlas?
4. **¿Un tipo de equipo tiene siempre las mismas tareas**, o varían por unidad funcional?
5. **La sede de Bogotá**, fuera del corredor: ¿UF vacía o UF administrativa?
