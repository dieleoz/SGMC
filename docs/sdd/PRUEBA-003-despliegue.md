# PRUEBA-003 — Aceptación del despliegue

**Las pruebas del despliegue reconstruido.** `PRUEBA-002` medía convertir 15 columnas en una
aplicación existente; esto mide construir una aplicación de cero.

| | |
|---|---|
| Cubre | `docs/MANUAL_DESPLIEGUE.md`, los 10 pasos, y el encargo generado [`../PROMPT_CABLEADO.md`](../PROMPT_CABLEADO.md), que es lo que se ejecuta en el editor |
| Sustituye a | `PRUEBA-002` en lo que ya no aplica. Nueve de sus 19 se conservan íntegras |
| Innegociables | `P-05`, `P-09`, `P-12`, `P-16` y **`P-27`** |
| Revisado | **2026-08-10.** Las pruebas no cambian; **lo que citan sí**: claves alfanuméricas, columnas de coordenada con sufijo `_LatLong`, 39 referencias y una hoja que ya no tiene ninguna columna de más |

## 1. Qué queda de PRUEBA-002

| Prueba | Veredicto | Motivo |
|---|---|---|
| `P-03` claves correctas | **Vale, y gana peso** | Antes medía claves ya fijadas; ahora **las 28 se eligen de cero, y todas son alfanuméricas con prefijo** —`ACT-0001`, `TIP-001`, `UNF-01`—. Una clave que AppSheet tipe `Number` **descarta sin avisar** las filas de texto |
| `P-04` formato de coordenada | **Vale, y ahora tiene una pista de nombre** | Independiente del procedimiento. Las seis columnas de coordenada llevan `_LatLong` en el nombre justo para que el tipo entre solo: `Ubicacion_LatLong`, `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong` |
| `P-05` la cadena de referencias | **Vale, e insuficiente** | Probaba 1 cadena sobre 15 conversiones. Ahora son **39**. Necesita a `P-25` al lado |
| `P-06` estados de las órdenes | **Vale** | Quitar la frase «no debería ocurrir»: ahora sí puede, la referencia es nueva |
| `P-08` cierre en rango | **Vale** | |
| `P-09` cierre fuera de rango | **Vale** | Innegociable, intacta |
| `P-10` filtro por zona | **Vale** | Le falta su caso negativo, que ya le faltaba |
| `P-12` lectura de vuelta | **Vale, y gana peso** | Con el esquema nuevo, la sincronización es lo único que no se infiere: hay que verlo |
| `P-16` baja de activos | **Vale** | Su fixture vive en la hoja y sobrevive |
| `P-19` columnas no editables | **Vale, y sube de riesgo** | `Editable_If` se repone desde cero en las cuatro |
| `P-01` estructura llegó | **Reescribir** | Sus discriminadores ya no pueden ocurrir. El fallo nuevo es leer la pestaña equivocada — ver `P-28` |
| `P-02` las ocho tablas nuevas | **Reescribir** | Ahora se dan de alta las 28. La versión actual daría verde con 20 ausentes |
| `P-07` navegación padre-hijo | **Reescribir** | Lo que la hace funcionar son las virtuales `Related`, y eso no lo mide — ver `P-24` |
| `P-11` el histórico no se borra | **Reescribir** | `Are updates allowed` vuelve al valor por defecto en las 28, no en dos |
| `P-17` la baja exige fecha | **Reescribir** | **Solo tiene el caso negativo.** No distingue un `Required_If` bien escrito de uno constante `TRUE` |
| `P-18` GPS deficiente | **Reescribir** | **Sin lectura de vuelta**, y RG-19 es una `App formula` que escribe — ver `P-31` |
| `P-13` vistas reparadas | **Sobra** | Mide un daño que ya no puede producirse. Sustituida por `P-23` |

## 2. Tres contradicciones a resolver antes de ejecutar nada

Están verificadas contra el archivo. **Con el ejecutor trabajando bien, harían fallar pruebas
innegociables.**

> **Repasadas contra el archivo el 2026-08-09. Dos siguen abiertas y una está cerrada.** Cada una
> lleva debajo su estado y el comando con el que se comprobó.

**C-1 — CERRADA el 2026-08-10.** Estuvo abierta mientras convivieron dos hojas: una con el radio
poblado y otra con la columna vacía, y la misma expresión era correcta en una y desastrosa en la
otra. Contra vacío, RG-01 compara con blanco y **rechaza también el cierre legítimo**, con lo que
`P-08` y `P-09` fallarían las dos y la tanda dejaría de discriminar.

**Ya no hay dos hojas.** La vigente trae el radio poblado en sus 27 tipos, así que RG-01 va en su
variante por tipo, sin alternativa. Comprobado con:

```bash
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

**C-2 — CERRADA el 2026-08-10, y a favor del modelo.** Estuvo abierta mientras `modelo_objetivo.py`
RG-14 decía `"Updates, Adds"` y `ESPEC-002` §7 exigía que el botón de añadir **no apareciera** en
`OT_OrdenesTrabajo`. **El documento que sostenía el otro lado ya no existe**: `ESPEC-002` se retiró
en la limpieza del 2026-08-10, y la instrucción vigente se genera del modelo, no se escribe:

```
Updates  si        Adds  si        Deletes  NO
```

Eso es lo que dice el paso 1 de [`../PROMPT_CABLEADO.md`](../PROMPT_CABLEADO.md) para
`OT_OrdenesTrabajo` y `MAN_Mantenimientos`, y coincide con RG-14 y RG-15. **Lo que se retira es
`Deletes`, no `Adds`**, y esa distinción es la decisión central del sistema: una orden no se borra,
se anula con `Activo = FALSE`, que deja traza de que existió.

**Consecuencia para `P-11`:** su criterio de cierre es que el botón de **borrar** no aparezca en las
dos tablas. Si la prueba se ejecuta esperando que tampoco aparezca el de **añadir**, fallará sobre
una configuración correcta. Se comprueba volcando la fuente:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print([(r['id'],r['tabla'],r['expresion']) for r in M.REGLAS if r['tipo']=='Are updates allowed'])"
```

**C-3 — CERRADA el 2026-08-09.** `RECONSTRUCCION_EXPRESIONES.md` §4 lista **las 39** —eran 38 en los
documentos escritos antes del 2026-08-10, así que una cifra `38` en prosa vigente está atrasada—, con
el aviso de que las 15 de `ESPEC-002`
eran las que faltaban en la aplicación anterior. `ESPEC-002` está retirado del repositorio. **Ya no
hay documento vigente que mande cablear 15**, y el que manda hoy es
[`../PROMPT_CABLEADO.md`](../PROMPT_CABLEADO.md), generado del modelo. La cifra se deriva:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sum(1 for d in M.MODELO.values() for c in d['columnas'] if c.get('ref')))"
```

## 3. Las pruebas nuevas

### P-21 — Ninguna clave quedó compuesta

**Qué demuestra.** Que AppSheet no combinó dos columnas al dar de alta. Contra una clave compuesta
**no resuelve ninguna referencia**, y el síntoma es que falla todo el bloque sin decir por qué.

**Y ahora el riesgo es mayor que cuando se escribió esta prueba.** Entonces las tablas de
movimiento traían una fila de ensayo, y con una fila cualquier columna parece única. **Hoy están
vacías a propósito**: se retiraron los registros de prueba del entregable. Sobre una pestaña sin
datos AppSheet no tiene con qué distinguir una columna única, así que **es justo donde va a
componer**.

Las ocho a vigilar, que son las que llegan sin filas:

```
OT_OrdenesTrabajo · MAN_Mantenimientos · CHK_Checklists · CHD_ChecklistDetalle
FOT_Fotografias   · FIR_Firmas         · NOV_Novedades  · PLA_PlanMantenimiento
```

**Cómo se ejecuta.** Después de dar de alta cada una de esas ocho, mirar la casilla `KEY`: si hay
dos marcadas o aparece como combinación, **corregir antes de pasar a la siguiente**, poniendo la
clave que declara el modelo. Criterio final: 28 claves simples, todas `Text`.

> **Y hay un segundo defecto que se ve en la misma pantalla, sobre esas mismas tablas vacías.** Seis
> de las ocho generan su clave con `UNIQUEID()`, es decir **alfanumérica**: `CHD_ChecklistDetalle`,
> `CHK_Checklists`, `FIR_Firmas`, `FOT_Fotografias`, `MAN_Mantenimientos` y `NOV_Novedades`. Sin
> filas de las que inferir, AppSheet elige el tipo a ciegas, y **si alguna quedó `Number`, cada fila
> que cree un técnico se perderá sin decirlo** — que es exactamente lo que le pasó al usuario que
> desapareció el 2026-08-10. Mientras se mira la casilla `KEY`, mírese también el `TYPE`: `Text` en
> las seis.
>
> Las otras dos, `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento`, llegan vacías pero **con clave
> legible** —`OT-0001`, `PLA-001`—, y `F-11` se salta su comprobación por falta de filas. Lo dice en
> su salida, y conviene leerlo:
>
> ```bash
> python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
> ```

### P-22 — Las tablas son 28, ninguna dada de alta dos veces

**Qué demuestra.** Que no quedó una tabla duplicada. Es el modo de fallo específico de dar de alta
una por una: si algo se repite, AppSheet crea `OT_OrdenesTrabajo_1` o `Copy of ...`. **Con dos tablas
sobre la misma pestaña, las referencias se reparten entre las dos y la mitad de las filas parece
desaparecer, sin error.**

**Cómo se ejecuta.** Contar en *Data → Tables*: deben ser 28. Ningún sufijo `_1`, `(2)`, `Copy of`.
Cada tabla apuntando a una pestaña distinta. Y comprobar que **no** están `GPS`, `SEC_Secciones`,
`FRM_SOS`, `FRM_CCTV` ni `FRM_PMVF`.

### P-23 — Inventario de vistas, slices, acciones y filtros

**Qué demuestra.** Que no falta ninguna pieza de configuración. Hoy **no existe en el repositorio un
inventario de vistas ni de slices**, así que si se pierde una, no hay contra qué compararla.

**Cómo se ejecuta.** Al terminar el paso 8, recorrer *UX → Views*, *Data → Slices*,
*Behavior → Actions* y el *Security Filter* de cada tabla. Anotar nombre, tabla y **expresión
completa**. Eso pasa a ser la línea base del sistema.

**Y sobre esa lista:** ninguna vista, slice ni reporte filtra por `[ActivoID].[Activo]` — es RG-18, y
es lo único que se rescata de `P-13`.

### P-24 — Las columnas virtuales `Related` se crearon

**Qué demuestra.** Que la navegación padre-hijo existe. Las crea AppSheet al poner una referencia, y
son lo que hace funcionar `P-07`.

**Cuántas, derivado del modelo:** las **39 referencias producen 39 virtuales, repartidas sobre 20
tablas destino**. Las que más importan:

| Tabla destino | Esperadas |
|---|---|
| `USR_Usuarios` | **7** — `ASG`, `OT` ×3, `MAN`, `NOV`, `PLA` |
| `MAN_Mantenimientos` | 3 — `FOT`, `FIR`, `CHK`, las tres con `IsPartOf` |
| `ACT_Activos` | 3 — `OT`, `NOV`, `PLA` |
| `FRM_Formularios` | 3 — `TIP`, `CHK`, `FRM_Preguntas` |
| `UNF_UnidadesFuncionales` | 3 — `SED`, `ASG`, `ACT` |
| `OT_OrdenesTrabajo` | 2 — `MAN` y la autorreferencia |
| `SED_Sedes` | **1 — `ACT_Activos.SedeID`.** Es fácil de dar por inexistente, porque documentos anteriores al 2026-08-10 dicen que esa columna estaba retirada |

El reparto entero se vuelca, no se cita:

```bash
python -c "import sys,collections;sys.path.insert(0,'scripts');import modelo_objetivo as M;c=collections.Counter(x['ref'] for d in M.MODELO.values() for x in d['columnas'] if x.get('ref'));print(sum(c.values()),'virtuales en',len(c),'tablas');print(c.most_common())"
```

**El caso que engaña: `USR_Usuarios`.** Tres virtuales apuntan a `OT_OrdenesTrabajo` por columnas
distintas —`TecnicoID`, `SupervisorID`, `CerradaPor`— y AppSheet las nombra igual o casi. Hay que
abrir las tres y leer el segundo argumento del `REF_ROWS`. **Si solo hay una, faltan dos y el
supervisor no ve sus órdenes.**

### P-25 — Las 39 referencias existen y resuelven

**Innegociable acompañante de `P-05`**, porque una muestra de 1 sobre 39 ya no autoriza a suponer el
resto.

**Cómo se ejecuta.** Volcar la lista **contra la fuente, no contra un documento**:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;[print(t+'.'+c['nombre'],'->',c['ref'],'IsPartOf' if c.get('es_parte_de') else '') for t,d in M.MODELO.items() for c in d['columnas'] if c.get('ref')]"
```

Para cada renglón: tipo `Ref`, tabla destino correcta, e `Is a part of` marcado **solo** en las
cuatro. Mirar el indicador `!` de referencia rota, que no se anuncia: hay que ir a buscarlo.

### P-26 — Ninguna expresión repuesta cita un nombre viejo

**Aviso sobre la lista que hay que usar.** Es la de `RECONSTRUCCION_EXPRESIONES.md` §1, «Los nombres
viejos, y por qué la lista NO se aplica en bloque», que **se genera del modelo y hoy tiene 26
renglones**. La cifra se lee del documento, no de aquí. Y **el mapeo solo es válido tabla por
tabla**: cinco de esos nombres siguen vivos en otra tabla, y son estos:

```
Activo        → ActivoID        en OT   ...pero Activo es la bandera legítima en 23 tablas
Estado        → EstadoOrdenID   en OT   ...pero Estado sigue vivo en NOV_Novedades
Estado        → Activo          en USR  ...el mismo nombre viejo, otro destino, otra tabla
OTID          → MantenimientoID en CHK  ...pero OTID es correcto en OT y en MAN
Observaciones → Observacion     en CHD  ...pero sigue vivo en ACT, OT y MAN
```

**Un buscar-y-reemplazar global rompe `SED_Sedes` y `MAN_Mantenimientos`.**

> **Corregido el 2026-08-10: esta prueba citaba un renglón `SedeID → retirada en ACT`, y hoy es al
> revés.** `ACT_Activos.SedeID` **existe** —es el recinto bajo techo donde vive el equipo— y la que
> se retiró es `USR_Usuarios.SedeID`, la del usuario. `SedeID` sigue siendo además la clave de
> `SED_Sedes`, así que el nombre aparece ahora en tres papeles distintos y **ninguno es un renombrado
> pendiente**: no se toca ninguno de los tres.

### P-28 — El recuento de columnas reales coincide con la hoja

**Sustituye a `P-01`.** Al dar de alta desde la hoja, el número de columnas es determinista: es el
número de encabezados.

**Recalculado contra la hoja vigente el 2026-08-10: cuadra en las 28 de 28, con cero columnas de
más y cero de menos.** Antes cuadraba en 24, y las cuatro que no eran el hallazgo de esta prueba.
**El hallazgo se cerró solo, y no por haberlo atendido**: la hoja dejó de heredarse y pasó a
generarse del modelo, así que no puede tener una columna que el modelo no declare.

La prueba **no sobra por eso, cambia de sentido**: dejó de buscar columnas huérfanas y pasa a ser la
comprobación de que el esquema que AppSheet leyó es el que la hoja tiene. Se ejecuta así, y el
criterio de cierre es `TOTAL 0`:

```bash
python - <<'EOF'
import sys, openpyxl
sys.path.insert(0, 'scripts')
import modelo_objetivo as M
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
total = 0
for t, d in M.MODELO.items():
    hdr = [c.value for c in next(wb[t].iter_rows(min_row=1, max_row=1)) if c.value]
    mod = {c['nombre'] for c in d['columnas']}
    sobra = [h for h in hdr if h not in mod]
    falta = [m for m in mod if m not in hdr]
    if sobra or falta:
        total += len(sobra) + len(falta)
        print(t, 'sobra', sobra, 'falta', falta)
print('TOTAL', total)
EOF
```

> **Y dos de aquellas seis nunca fueron huérfanas: `FRM_Preguntas.RequiereGPS` y
> `FRM_Preguntas.RequiereFirma` son columnas vivas del modelo**, y estaban en esta tabla por error.
> Importa porque circuló una instrucción de ocultar 49 columnas que las incluía, y ocultarlas habría
> quitado del formulario dos campos que el sistema usa. Es el mismo patrón de siempre: **una lista
> escrita a mano se desvía del modelo**.
>
> Las que sí quedaron sin decidir son cuatro —`USR_Usuarios.UltimaSincronizacion`,
> `FOT_Fotografias.Fecha`, `FRM_Formularios.Orden` y `FRM_Preguntas.ValorDefecto`—, viven en
> `COLUMNAS_SIN_DECIDIR` y las avisa la regla `D-06`. **`FOT_Fotografias.Fecha` sigue mereciendo
> mirada**: el sistema guarda fecha y coordenada por fotografía, y el modelo llama a la suya
> `FechaHora`. Ninguna de las cuatro está ya en la hoja, así que **no van a aparecer en el editor**;
> lo que queda de ellas es la decisión, no la columna.

### P-29 — El filtro de seguridad de las órdenes muerde

**RG-05 no tiene ninguna prueba hoy.** `P-10` cubre RG-04 y nada cubre RG-05.

**Cómo se ejecuta.** *Preview app as* con el correo de un técnico: ve las órdenes donde es técnico o
supervisor, **y ninguna otra**. Repetir con un usuario que no figure en ninguna: esperado **cero**.

**Y la trampa:** RG-05 desreferencia `[TecnicoID].[Correo]`. Si esa referencia quedó como texto, el
filtro **no da error: devuelve vacío y el técnico se queda sin trabajo en pantalla.**

### P-30 — Las tres reglas que nadie mide

**RG-02** `Precision_GPS` con `USERLOCATIONACCURACY()`: exigir que no llegue vacía. Si lo ejecuta un
agente sin GPS, se marca **NO EJECUTADA**, no PASA.

**RG-03** `MotivoExcepcion` obligatorio cuando hay excepción: probar que **no deja guardar** sin
motivo cuando `CierreConExcepcion = TRUE`, **y que sí deja** cuando es FALSE. Sin ese segundo paso no
se distingue de un `Required_If` constante — el mismo defecto que `P-17`.

**RG-09** `VersionFormulario`: crear un checklist y comprobar que se puebla con la versión del
formulario. Si `CHK.FormularioID` quedó texto, la expresión no resuelve y **la columna queda vacía
sin error**.

### P-31 — Lectura de vuelta de RG-19

**Qué demuestra.** Que `CierreConExcepcion` se **escribe** en la hoja, no solo se pinta. Es una
`App formula`, y una `App formula` materializa su valor al guardar.

**Cómo se ejecuta.** Con `UMBRAL_GPS = 40`, abrir el registro de prueba de 45 m y guardar. Leer la
hoja: la celda debe valer **TRUE**. Repetir con el de 8 m: **FALSE**. Si en la hoja siguen como
estaban mientras la vista previa mostraba otra cosa, **la marca de excepción es decorativa**.

---

## 4. P-27 — Barrido de fallos silenciosos

**La quinta innegociable, y la que nadie había escrito.**

Las otras cuatro detectan fallos ruidosos: una expresión que no resuelve, un cierre que no se
rechaza, una fila que no llega. **P-27 es la única que mira los fallos que un despliegue verde no
distingue de un acierto.**

### La causa raíz, y por qué dejó de existir

**El procedimiento da de alta cada tabla leyendo la hoja.** Mientras la hoja arrastró 47 columnas
que el modelo no declara, esas columnas volvían al esquema como columnas reales y **toda expresión
que las citara resolvía** — incluidas tres cuyo nombre coincide con la clave de otra tabla, que
AppSheet convertía en referencia por su cuenta.

> **Cerrado el 2026-08-10 al construir sobre la hoja limpia.** Esas columnas **ya no existen en el
> archivo**, así que no hay nada que ocultar ni ninguna trampa que deshacer. Se comprueba con
> `verificar_faseA.py`, cuya regla `F-19` distingue tres estados: **están las 44** —la hoja
> heredada—, no está ninguna —la limpia, que es la vigente— o **están algunas**, que es el
> peligroso, porque entonces la documentación generada manda ocultar columnas que ya no existen.
>
> **La cifra de arriba, «47», era correcta y hoy son 48**, porque `USR_Usuarios.SedeID` pasó a
> `CAMPOS_RETIRADOS` ese día. Y no sale de una sola estructura: son **44** declaradas más **4** que
> nadie ha decidido. **Nunca se cita de memoria** —dos caminos daban 43 y 47, y el desacuerdo
> señalaba un hueco real en el modelo—:
>
> ```bash
> python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sum(len(v) for v in M.CAMPOS_RETIRADOS.values()),'+',len(M.COLUMNAS_SIN_DECIDIR))"
> ```
>
> **Los once casos de abajo se conservan.** No describen un riesgo vivo: describen **qué clase de
> fallo hay que buscar**, y esa clase —una referencia que resuelve contra lo que no es— volvió a
> aparecer dos veces con otro disfraz.

### Los once casos

**Familia A — el nombre viejo con significado nuevo**

| # | Trampa | Qué devuelve |
|---|---|---|
| A1 | `OT_OrdenesTrabajo.Activo` | Era la referencia al activo; ahora es la bandera `Yes/No`. `REF_ROWS("OT_OrdenesTrabajo","Activo")` devuelve **lista vacía**; `[OTID].[Activo]` devuelve `TRUE` constante |

**Familia B — la columna muerta que sigue resolviendo**

| # | Columna | Por qué es trampa | Camino correcto |
|---|---|---|---|
| B1 | `CHK_Checklists.ActivoID` | **Se llama como la clave de `ACT_Activos`: AppSheet la convierte en `Ref` sola** | `[MantenimientoID].[OTID].[ActivoID]` |
| B2 | `CHK_Checklists.TecnicoID` | Guarda `Santiago Moreno` — un nombre, no un identificador. Resuelve y devuelve una persona escrita a mano | `[MantenimientoID].[TecnicoID]` |
| B3 | `CHD_ChecklistDetalle.TipoRespuestaID` | **Se llama como la clave de `TPR_TiposRespuesta`: `Ref` automática** | `[PreguntaID].[TipoRespuestaID]` |
| B4 | `CHD_ChecklistDetalle.Orden` | `Orden` existe vivo en cuatro tablas más | `[PreguntaID].[Orden]` |
| B5 | `OT_OrdenesTrabajo.FormularioID` | **`Ref` automática** hacia una tabla de la que la orden ya no debe colgar | El formulario lo da el tipo del activo |
| B6 | `CHK_Checklists.Estado` | Sustituido por `Finalizado`. `Estado` sigue vivo en `NOV_Novedades` | `[Finalizado]` |
| B7 | `CHK_Checklists.Observaciones` | Sigue vivo en `ACT`, `OT` y `MAN`; en `CHD` el nuevo es `Observacion`, en singular | La observación es de la ejecución |
| B8 | `CHK_Checklists.Activo` | `Activo` es bandera legítima en **23** tablas, así que parece normal | El checklist no se desactiva aparte |
| B9 | `CHD_ChecklistDetalle.Activo` | Idéntico | Idéntico |
| B10 | `MAN_Mantenimientos.Tipo` | `Tipo` sigue vivo en `OT`, `NOV` y `FOT` | `[OTID].[Tipo]` |

**Tres son peores que los demás: B1, B3 y B5.** No requieren que nadie se equivoque escribiendo —
**AppSheet los crea como `Ref` por su cuenta**, porque infiere por coincidencia de nombre. Cada uno
fabrica además una virtual `Related` que contamina `P-24`.

**Familia C — la comparación constante.** Un `Ref` guarda la clave; compararlo con un literal no da
error y devuelve siempre lo mismo. Y si vive en una `App formula`, **escribe** ese resultado. Es lo
que motivó V-17.

**Y aquí hay que releer con cuidado, porque el 2026-08-10 la excepción se volvió la norma.** Con
todas las claves pasadas a texto legible, **`CLAVE_LEGIBLE` tiene hoy 22 entradas** —las 22 tablas
pobladas— y `CLAVE_GENERADA` las 6 vacías. `V-17` exceptúa por diseño a las de `CLAVE_LEGIBLE`
(`R-10`), así que **la comparación contra literal deja de ser un error en 22 tablas y el validador
deja de avisar en ellas**. `[EstadoOrdenID] = "Cerrada"` es correcto; `[EstadoActivoID] = "Retirado"`
no lo es, porque el texto vive en `Nombre`. La distinción hay que hacerla leyendo, no esperando el
aviso.

**Con las 6 tablas de `UNIQUEID()` el riesgo original sigue intacto, y peor:** llegan sin ninguna
fila, así que no hay ni siquiera una clave que mirar, y **desde la primera fila que cree la
aplicación serán cadenas aleatorias**. Una regla que compare contra un literal ahí pasaría la prueba
y dejaría de funcionar en producción.

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sorted(M.CLAVE_GENERADA))"
```

### Cómo se ejecuta

**Paso 1 — demostrar que la trampa existe.** En el Asistente, escribir la expresión tramposa.

**El resultado esperado es que la ACEPTE.** Ese es el punto: queda documentado que un despliegue
verde no distingue la expresión correcta de la trampa. Se anota con su salida literal.

**Paso 2 — demostrar que nadie cayó.** Recorrer las 21 reglas, las slices y las virtuales, y
comprobar que ninguna cita los once nombres **sobre la tabla del caso**.

**Paso 3 — dejar la columna inerte.** Tipo `Text` —hay que **deshacer la inferencia automática en
B1, B3 y B5**—, sin fórmula ni validación, y `Show? = FALSE`.

**Criterio de cierre.** Los once documentados en el paso 1, cero apariciones en el paso 2, los once
inertes en el paso 3.

> **Si el paso 1 se salta, la prueba no vale.** Sin ver la trampa aceptada, no se sabe si el paso 2
> pasó por diligencia o por casualidad. Es la regla del proyecto de reintroducir el defecto para
> probar la regla.

---

## 5. Las tres clases, y quién no las trae

`CLAUDE.md` exige positiva, negativa y lectura de vuelta.

**De las 19 de `PRUEBA-002`, una sola trae las tres: `P-16`.** Y no por casualidad — se escribió
después de que alguien señalara que RG-16 se había corregido sin prueba.

**Catorce de diecinueve no leen el Sheets en ningún momento.** Toda la tanda se apoya en tres pruebas
para saber si algo salió de la pantalla.

Tres déficits que importan más que el recuento:

- **`P-17` no tiene positiva**, así que no prueba lo que dice. Un `Required_If` constante `TRUE`
  daría el mismo resultado. Es el defecto simétrico del que motivó `P-16`, sobre la regla de al lado.
- **`P-18` no tiene lectura de vuelta** y RG-19 escribe. Ver `P-31`.
- **`P-10` no tiene negativa ejecutada.** Falta probar con un usuario sin asignación y exigir cero.

## 6. Qué es ejecutable sin plan de pago

**Automatizable contra el archivo, y es lo más barato y lo menos usado:** el pre-vuelo de claves, el
recuento de columnas por tabla —`P-28`, que ya trae su comando—, el inventario de las once trampas, y
el volcado de **las 39** y de las virtuales esperadas. **Merece un `scripts/verificar_reposicion.py`**
que falle con código distinto de cero — y que **no lo escriba quien ejecute el despliegue**.

> **Y hay un verificador nuevo desde el 2026-08-10 que no sustituye a este pero conviene conocer:**
> `python scripts/verificar_reproducible.py`, que genera la plantilla dos veces y compara celda a
> celda. Nació de un defecto que **pasó los otros cuatro verificadores**, porque todos miran un
> archivo y aquel solo existía entre dos ejecuciones: la resiembra de claves duplicó las seis
> edificaciones de `SED_Sedes`, y cada pasada habría añadido seis más. Si `P-28` sale con columnas
> de más, mírese este antes que el editor.

**Manual y barato: el Asistente de Expresiones.** `P-05`, `P-25`, `P-27` paso 1. Es el instrumento
más rentable del proyecto.

**Manual y caro: recorrer el editor.** `P-21`, `P-22`, `P-24`, `P-26`, `P-28` y sobre todo `P-23`.

**No ejecutable por un agente, y hay que decirlo así:** `P-04` y `RG-02` sin un móvil real —se
declaran **NO EJECUTADAS**, no PASA—. Y `P-09` sigue colgando de un supuesto sin verificar: **si
AppSheet evalúa un `Valid_If` sobre una columna con `Editable_If = FALSE`**. Es el peor modo de fallo
del sistema, porque la regla parecería funcionar por no ejercitarse nunca. **Si `P-08` y `P-09` salen
las dos aceptadas, sospeche de eso antes que del radio.**

---

*Deriva del dictamen del probador sobre `PRUEBA-002` y el manual de despliegue. Las contradicciones*
*de la sección 2 se resuelven en la fuente —`modelo_objetivo.py`— antes de ejecutar.*
