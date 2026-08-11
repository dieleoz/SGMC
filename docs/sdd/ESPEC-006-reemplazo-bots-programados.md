# ESPEC-006 — `RG-08` y `RG-12` dejan de ser bots programados

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.EstaVencida, DRY_RUN -->
<!-- D-03 compara Tabla.Columna contra MODELO, y EstaVencida a propósito NUNCA entra en MODELO:
     es una columna virtual declarada solo en REGLAS (RG-37, §4), siguiendo el mismo mecanismo
     que RG-35/RG-36 de ESPEC-005. Citarla en prosa como Tabla.Columna es legítimo -es como se
     documenta una virtual-, no un hueco del modelo.
     DRY_RUN no es una tabla: es la bandera booleana de scripts/faseA_sheets.gs (§2.2). D-01 la
     detecta como candidata a tabla por el patrón MAYUSCULAS_Palabra; se ignora aquí, a proposito. -->

**No aplicada.** Este documento es del especificador. No toca `scripts/modelo_objetivo.py`, el
Sheets de producción ni el editor de AppSheet.

**Rehecha el 2026-08-11 tras bloqueo del arquitecto.** La versión anterior recibió diez hallazgos.
Tres eran defectos de código míos y ya están aplicados en el repositorio, fuera de esta
especificación (commit `f790c91`): la heurística *"toda columna virtual `App formula` sobre
`(tabla)` se llama `Etiqueta` y lleva `Label`"* —que la versión anterior de este documento ya había
encontrado y corregido en `generar_reconstruccion.py` y `generar_prompt_cableado.py`, en el mismo
commit que la introdujo (`0d3d641`)— seguía viva en un **tercer** generador que nadie había mirado,
`generar_encargo_ventana.py`, y con `RG-37` declarada habría emitido dos filas llamadas `Etiqueta`
sobre la misma tabla; ahora los tres consultan `inferencia.py`
(`columnas_virtuales()`/`etiquetas_virtuales()`) en vez de suponerlo de la forma de la regla.
Además, `generar_prompt_expresiones.py` deja de clasificar una columna virtual entre las que
escriben en la hoja (`_escribe()`); y el conteo de `CLAUDE.md` §7.17 cuenta etiquetas virtuales, no
toda columna `App formula`. Los siete restantes son de documento y se atienden aquí, cada uno con el
comando que lo verifica, no reescrito desde la memoria de la versión anterior.

**Lo que cambió desde el bloqueo, y afloja una de las siete condiciones.** `P-09` de `PRUEBA-005`
—la que deja `OTID` y `PlanID` con `Initial value = UNIQUEID()` y `Key` marcada— se ejecutó y se
registró en `docs/sdd/ACTA-005-pruebas.md` (commit `7a6e750`), con transcripción literal del
editor. Sigue habiendo un ejecutor trabajando en paralelo sobre `ESPEC-005`/`PRUEBA-005`; ninguno de
esos archivos (`ESPEC-005-clave-otid-planid.md`, `ORDEN-005-*`, `ACTA-005-*`) se toca aquí, se leen
solo para verificar lo que ya está registrado.

## 1. Qué se quiere y por qué

Dos de las 23 reglas del modelo son bots programados, y en la cuenta gratuita en la que corre hoy
`_SISGA_-323965761` **no se ejecutan nunca**, sin importar cuántas veces se configuren bien
(§2.1). Uno de los dos, además, tiene un segundo defecto independiente del plan de licenciamiento:
**si algún día se ejecutara, movería la orden a un estado que le impide al técnico cerrarla**
(§2.2). Esta especificación decide, para los dos, un mecanismo que sí funciona en esta cuenta hoy,
y de paso corrige el segundo defecto, que seguiría existiendo aunque se comprara el plan de pago
mañana mismo.

La decisión que esto permite tomar: **cómo se marca una orden vencida y cómo se generan las
órdenes de la semana, sin depender de un bot programado que nunca corre.** `docs/ROADMAP.md`
(sección «`Vencida` es un estado FINAL, así que una orden que se pasa de fecha no puede cerrarse»)
ya lo dejó escrito el 2026-08-11: *"Está pendiente de decidir con operación, y la decisión va antes
de poner `RG-08`"*. Esta especificación es esa decisión, tomada por el método vigente de este
proyecto —construir bajo supuestos y no esperar respuesta (`docs/ALCANCE_Y_SUPUESTOS_SGMC.md` §1)—,
no una consulta abierta.

## 2. Estado actual verificado

Todo lo siguiente se leyó de `scripts/modelo_objetivo.py` (el modelo, fuente única),
`BD/instantaneas/antes-de-fase-c.json` y `BD/Modelo_Datos_PLANTILLA.xlsx` (el volcado local).
Según `python scripts/sistema.py`, hoy la aplicación vigente es `_SISGA_-323965761` sobre la hoja
`Modelo_Datos_10082026`, y ese volcado es el mismo archivo mientras nadie edite el Sheets
directamente — no hay evidencia en el repositorio de que se haya editado a mano desde que se
generó, y `EOT_EstadosOrden` no es una de las tablas que operación completa manualmente (es
catálogo cerrado, no dato transaccional). Donde este documento se apoya en algo que solo puede
verse en el editor de AppSheet y no en el archivo, se dice explícitamente.

### 2.1 `RG-08` y `RG-12` son bots programados, y la cuenta es gratuita

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;[print(r['id'],'|',r['tipo'],'|',r['tabla'],'|',r['columna']) for r in REGLAS if 'Bot' in r['tipo']]"
```
```
RG-06 | Bot | MAN_Mantenimientos | (tabla)
RG-07 | Bot | OT_OrdenesTrabajo | (tabla)
RG-08 | Bot programado | OT_OrdenesTrabajo | EstadoOrdenID
RG-12 | Bot programado | PLA_PlanMantenimiento | (tabla)
RG-10 | Bot | MAN_Mantenimientos | (tabla)
```

De los cinco bots, dos —`RG-08` y `RG-12`, exactamente los dos que preguntan sobre este
documento— son `Bot programado`. `docs/BASE_CONOCIMIENTO_APPSHEET.md` §6 lo documenta con tres
citas textuales, con URL, contra la fuente oficial:

> «Puedes configurar estas funciones, **pero no se ejecutarán como esperas**.»

> «Si tu aplicación no está desplegada o no estás en un plan de pago, tu bot no se ejecutará en el
> horario indicado. **Sin embargo, puedes invocarlo pulsando `Test`.**»

> «En cuentas gratuitas, al ejecutar un bot con evento programado, los correos se envían **solo al
> propietario de la app**.»

— [Use AppSheet for free](https://support.google.com/appsheet/answer/10104499?hl=en) ·
[Understand bot scheduling and retry](https://support.google.com/appsheet/answer/11547468?hl=en)

Se recontrastó hoy contra la fuente, no se copió de memoria: se descargó
`https://support.google.com/appsheet/answer/10104499?hl=en` y contiene, literal:

> «A subset of features, such as sending emails or triggering bots with schedule events using
> AppSheet automation, are not fully supported until you purchase a subscription. That is, you can
> configure these features, but they won't execute as expected.»

Coincide con la cita ya registrada en la base de conocimiento del proyecto. **`RG-08` y `RG-12` se
pueden configurar enteros, sin un solo error, y no van a hacer nada** mientras la cuenta siga en el
plan gratuito. Es la forma exacta del defecto que `CLAUDE.md` §7.13 nombra: una regla puesta, bien
escrita, que no hace nada.

### 2.2 `Vencida` tiene `EsFinal = Y`, y bloquea el cierre — verificado en dos fuentes, no una

```bash
python -c "
import json
with open('BD/instantaneas/antes-de-fase-c.json', encoding='utf-8') as f:
    data = json.load(f)
for r in data['EOT_EstadosOrden']:
    print(r['EstadoOrdenID'], '| EsFinal=', r['EsFinal'], '| QuienCambia=', r['QuienCambia'])
"
```
```
Programada    | EsFinal= N | QuienCambia= Sistema
Asignada      | EsFinal= N | QuienCambia= Supervisor
En ejecucion  | EsFinal= N | QuienCambia= Tecnico
En revision   | EsFinal= N | QuienCambia= Tecnico
Cerrada       | EsFinal= Y | QuienCambia= Supervisor
Suspendida    | EsFinal= N | QuienCambia= Supervisor
Vencida       | EsFinal= Y | QuienCambia= Sistema
```

Y contra el volcado local, la misma tabla, para confirmar que las dos fuentes dicen lo mismo hoy:

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True)
for r in wb['EOT_EstadosOrden'].iter_rows(values_only=True):
    print(r)
"
```
```
('EstadoOrdenID', 'Nombre', 'Orden', 'QuienCambia', 'EsFinal', 'Activo')
('Programada', 'Programada', 1, 'Sistema', 'FALSE', 'TRUE')
('Asignada', 'Asignada', 2, 'Supervisor', 'FALSE', 'TRUE')
('En ejecucion', 'En ejecucion', 3, 'Tecnico', 'FALSE', 'TRUE')
('En revision', 'En revision', 4, 'Tecnico', 'FALSE', 'TRUE')
('Cerrada', 'Cerrada', 5, 'Supervisor', 'TRUE', 'TRUE')
('Suspendida', 'Suspendida', 6, 'Supervisor', 'FALSE', 'TRUE')
('Vencida', 'Vencida', 7, 'Sistema', 'TRUE', 'TRUE')
```

Coinciden. De los siete estados hay **dos finales**: `Cerrada` y `Vencida`. La afirmación del
encargo se confirma tal cual: `RG-08` (`AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] <
TODAY())`) movería la orden a `Vencida`, y `Vencida` es terminal. Un estado terminal, en este
modelo, no tiene ninguna transición declarada que saque a la orden de ahí — no hay fila `Devuelta`
ni ninguna regla que reabra un estado con `EsFinal = TRUE`. El técnico que ejecuta el mantenimiento
después de que su orden pasó a `Vencida` no tiene dónde registrar lo que hizo.

**Hallazgo colateral, no autoritativo: un artefacto superado contradice el dato vigente, y hay que
decidir si se queda en el árbol.** `scripts/faseA_sheets.gs` —el guion de Google Apps Script de
cuando la Fase A era trabajo manual sobre el Sheets, antes de que `generar_plantilla.py` la
generara del modelo— declara la misma fila `Vencida` con `EsFinal = false`, no `true`. Ese archivo
no está referenciado desde ningún otro script del repositorio, verificado hoy de nuevo:

```bash
grep -rl faseA_sheets scripts/ docs/ MAP.md README.md CLAUDE.md
```
Sin salida, salvo este propio documento. `SDD_PIPELINE_SGMC.md` ya declara superada la Fase A
manual.

**Se queda, no se retira**, y no por descuido: sus primeras veinte líneas son un banner
`RETIRADO EL 2026-08-07` que explica por qué no tiene trabajo pendiente (la Fase A se cerró a mano,
`ACTA-002`) y por qué se conserva —"registro de método: el patrón `DRY_RUN`, tener el borrado de
los datos de prueba en el mismo archivo que los crea, y la verificación separada del que aplica"—,
verificado leyendo el encabezado completo del archivo antes de escribir esto. Retirarlo borraría ese
registro sin ganar nada: cero referencias significa que ningún generador ni ningún documento vigente
lo lee, así que su dato obsoleto no puede propagarse en silencio — solo puede leerlo quien abra el
archivo directamente, y quien lo haga se encuentra primero con el banner de retiro. No se usa como
fuente en ningún punto de este documento: el dato vigente es el de arriba, en las dos fuentes que sí
gobiernan la aplicación hoy. Se deja esta constancia, y ahora esta decisión explícita, porque es
exactamente el tipo de documento que, si alguien lo lee sin saber que está superado, produce una
afirmación falsa sobre el sistema — la patología que este proyecto existe para evitar.

### 2.3 Ningún otro estado library da salida a una orden vencida

```bash
python -c "
import sys;sys.path.insert(0,'scripts')
from modelo_objetivo import REGLAS
print([r['id'] for r in REGLAS if r['tabla']=='OT_OrdenesTrabajo'])
"
```
```
['RG-35', 'RG-05', 'RG-07', 'RG-08', 'RG-14']
```

Ninguna es una transición de reapertura. `RG-14` es `Are updates allowed` (`Updates, Adds`, sin
`Deletes`), `RG-05` es el filtro de seguridad, `RG-07` es el bot de aviso al asignar. La única regla
sobre `EstadoOrdenID` es la propia `RG-08`. Confirma lo que `docs/ROADMAP.md` ya adelantaba: de las
tres salidas que nombra —que `Vencida` deje de ser final, que exista una transición de reapertura,
o que el vencimiento sea una marca y no un estado— **ninguna está construida hoy**.

### 2.4 Los identificadores libres, verificados por rango completo

```bash
grep -on "RG-[0-9]\+" scripts/modelo_objetivo.py | cut -d: -f2 | sort -t- -k2 -n -u
```
```
RG-01 RG-02 RG-03 RG-04 RG-05 RG-06 RG-07 RG-08 RG-09 RG-10 RG-11 RG-12 RG-13
RG-14 RG-15 RG-16 RG-17 RG-18 RG-19 RG-20 RG-34 RG-35 RG-36
```

23 identificadores, sin huecos hasta `RG-20`, y luego `RG-34` a `RG-36` (aplicados por `ESPEC-005`
el 2026-08-10). `RG-21` a `RG-33` no aparecen: `docs/sdd/ESPEC-003-modelo-de-dominio.md` los
reserva completos, verificado en su propio texto:

```bash
grep -on "RG-[0-9]\+" docs/sdd/ESPEC-003-modelo-de-dominio.md | cut -d: -f2 | sort -t- -k2 -n -u | head -20
```
```
RG-01 RG-02 RG-03 RG-04 RG-05 RG-06 RG-07 RG-08 RG-09 RG-10 RG-11 RG-12 RG-13
RG-14 RG-15 RG-16 RG-17 RG-18 RG-19 RG-20 RG-21 RG-22 RG-23 RG-24 RG-25 RG-26
RG-27 RG-28 RG-29 RG-30 RG-31 RG-32 RG-33 RG-34
```

`RG-21` a `RG-33` están reservados y esa especificación sigue **bloqueada** (14 condiciones sin
resolver, `MAP.md`); no se tocan. `RG-37` y `RG-38` no aparecen en ningún documento del repositorio:

```bash
grep -rln "RG-37\|RG-38" scripts/ docs/
```
Sin salida. Son los identificadores más bajos libres, y los que esta especificación usa (§4).

### 2.5 `validar_modelo.py` hoy

```bash
python scripts/validar_modelo.py
```
```
Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
ERRORES: ninguno
AVISOS (3):
  [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
APTO PARA DESPLEGAR
```

Línea base contra la que se compara §6.

### 2.6 Las dos tablas siguen vacías, así que el cambio no toca ningún dato transaccional

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True)
for t in ['OT_OrdenesTrabajo','PLA_PlanMantenimiento']:
    ws = wb[t]
    n = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if any(c not in (None,'') for c in r))
    print(t, n)
"
```
```
OT_OrdenesTrabajo 0
PLA_PlanMantenimiento 0
```

Igual que en `ESPEC-005` §2.1, esto no prueba el estado de la aplicación en vivo —el volcado es
ciego a las ocho tablas de movimiento por diseño (`scripts/lectura_de_vuelta.py`,
`VOLCADO_CIEGO_A`)—, pero acota lo que hay que perder si algo sale mal: ninguna fila real.

### 2.7 Volumen que tendría que absorber el mecanismo de `RG-12`, por orden de magnitud

```bash
python scripts/capacidad.py
```
```
Hoy: 368 activos  ->  5,299 mantenimientos al anio
```

Con el 20% de correctivos que asume `capacidad.py`, unos 4.239 preventivos/año, del orden de 80 a
90 por semana en el escenario de hoy (368 activos). Es una cota de orden de magnitud, no una
medición: `PLA_PlanMantenimiento` está vacía (§2.6), así que el número real de filas cuya
`ProximaFecha` cae en una semana dada no se puede contar hoy. Se usa en §3 para valorar qué se
pierde con un botón manual frente a un disparador automático.

### 2.8 Qué tocan los tres consumidores que el encargo señala, verificado en cada uno

**`validar_modelo.py`, `V-18`.** Compara la expresión de una regla en `REGLAS` contra la propiedad
de la misma columna en `MODELO`, pero **solo para los tipos `Valid_If`, `App formula` e `Initial
value`** (`_PROPIEDAD = {"Valid_If": "valid_if", "App formula": "formula", "Initial value":
"valor_inicial"}`). `RG-08` es `Bot programado`, tipo que no está en ese diccionario:
`_PROPIEDAD.get(r["tipo"])` da `None` y el bucle hace `continue` antes de comparar nada. **`V-18`
nunca comprobó `RG-08` contra nada**, así que retirarla no le quita ninguna comprobación que
estuviera activa. Verificado leyendo el bloque completo de `V-18` en `scripts/validar_modelo.py`.

**`alcance_reglas.py`.** `columnas_de()` solo añade `(tabla, columna)` de forma directa cuando
`regla["columna"]` no es `"(tabla)"` ni `"(varias)"` (línea `if regla.get("columna") and
regla["columna"] not in ("(tabla)", "(varias)")`). El resto de columnas que atribuye salen de
recorrer la expresión. La expresión de `RG-08` —`AND([EstadoOrdenID].[EsFinal] = FALSE,
[FechaProgramada] < TODAY())`— se conserva sin cambios en la regla nueva (§4), así que **el
recorrido de la expresión atribuye las mismas columnas que hoy**: `OT_OrdenesTrabajo.EstadoOrdenID`,
`EOT_EstadosOrden.EsFinal` y `OT_OrdenesTrabajo.FechaProgramada`. Verificado ejecutando
`columnas_de()` a mano sobre las dos formas de la regla (con `columna="EstadoOrdenID"` y con
`columna="(tabla)"`): el conjunto de columnas atribuidas no cambia; lo que cambia es qué `id` de
regla aparece junto a ellas en `por_columna()` cuando se regenere el reporte.

**Los generadores de expresiones — la versión anterior de este documento encontró aquí un defecto
real, no cosmético, y lo corrigió en dos generadores en el mismo commit que la introdujo. El
arquitecto encontró que la corrección no alcanzaba a un tercero.**

```bash
grep -n "es_label\|nombre_virtual" scripts/generar_reconstruccion.py scripts/generar_prompt_cableado.py
```
```
scripts/generar_reconstruccion.py:75:        _nombre = r.get("nombre_virtual", "(sin nombre declarado)")
scripts/generar_reconstruccion.py:80:        if r.get("es_label"):
scripts/generar_prompt_cableado.py:291:_virtuales = [(r["tabla"], r.get("nombre_virtual", "?"), r["expresion"]) for r in REGLAS
scripts/generar_prompt_cableado.py:293:              and r.get("es_label")]
```

`generar_reconstruccion.py` y `generar_prompt_cableado.py` ya no detectan la etiqueta por la forma de
la regla (`App formula` sobre `"(tabla)"`): preguntan por `es_label`, el campo que este mismo
documento propone en §4. **Esto se corrigió en el commit `0d3d641`, el que autoría por primera vez
esta especificación** —verificado con `git show 0d3d641 --stat`: toca esos dos archivos y no toca
`generar_encargo_ventana.py`—, así que cuando el arquitecto revisó la primera versión de este
documento, el código ya estaba corregido en esos dos sitios; el defecto seguía descrito en prosa como
pendiente porque la prosa no se había vuelto a mirar contra el código antes de someterla.

**El arquitecto encontró que la misma heurística seguía viva en un tercer generador que nadie había
señalado.** `generar_encargo_ventana.py` seguía detectando por la forma y, con `RG-37` declarada,
habría emitido **dos filas llamadas `Etiqueta`** sobre `OT_OrdenesTrabajo`, una con la expresión de
`RG-37`. Corregido en el commit `f790c91`, verificado hoy: ahora consulta
`inferencia.etiquetas_virtuales(REGLAS)`, leyendo `scripts/generar_encargo_ventana.py` línea a línea
—la lista `virtuales` sale de esa función, no de una condición sobre `tipo`/`columna`—.

**Queda uno, dentro de `scripts/generar_prompt_expresiones.py`, verificado hoy leyendo el archivo
completo.** La sección *"La trampa: un bot que AÑADE UNA FILA se hace en dos sitios"* sigue
imprimiendo, literal:

```bash
grep -n 'Afecta a\|RG-10.*RG-12' scripts/generar_prompt_expresiones.py
```
```
254:w("Afecta a `RG-10` y a `RG-12`, que son los dos que crean órdenes.")
261:_crean = sorted({r["id"] for r in REGLAS
263:                 ) or r["id"] in ("RG-10", "RG-12")})
```

La línea 254 es un literal escrito a mano, no derivado de `REGLAS`: si `RG-12` desaparece del modelo
(§4), sigue imprimiéndose con un identificador que ya no existe. `_crean` (261-263) sí deriva de
`REGLAS`, así que ese cálculo se corrige solo en cuanto `RG-12` desaparezca — el problema es solo la
línea 254. Y falta la sección que el reemplazo necesita: el mecanismo de `RG-38` no es un bot, así
que **no** se configura en dos sitios (`Data > Actions` + `Automation > Bots`) — se configura solo en
`Data > Actions`, y se expone en una vista (§4). Este generador necesita **dos correcciones dentro
del mismo archivo**: dejar de citar `RG-10`/`RG-12` a mano en la línea 254, y una sección nueva,
separada de "los bots", que explique `Data > Actions` sin el paso de `Automation > Bots` para
`RG-38`.

**El defecto restante es de código, no de diseño, y su arreglo es trabajo del ejecutor (`ORDEN-006`),
no de esta especificación** — el mismo tratamiento que `ESPEC-005` dio a los defectos de código que
encontró en `V-11`, `PROMPT_CABLEADO.md` y `capacidad.py` (ver la cabecera de ese documento), y que
esta misma especificación ya recibió una vez (commit `f790c91`). Se lista con el detalle necesario
para que la orden no tenga que volver a investigarlo (§6).

### 2.9 La ventana barata: qué se cerró con `P-09` y qué sigue abierto

`CLAUDE.md` §7.17 la nombra: ocho tablas —`VOLCADO_CIEGO_A`— están en cero filas, y esa vacuidad es
lo único que hace que corregir un tipo o una clave cueste un clic en vez de una migración. Cualquier
fixture de esta especificación tiene que decidir con esa cuenta a la vista, no después.

**`P-09` de `PRUEBA-005` ya se ejecutó y quedó registrada, con transcripción literal, no un
«coincide».**

```bash
sed -n '144,168p' docs/sdd/ACTA-005-pruebas.md
```
```
#### `P-09` — el registro literal

**Cotejo a ojo en el editor.** No hay comando que lo recupere: la API devuelve filas, no esquema,
así que esta transcripción es la única evidencia que va a existir. Se copió aunque coincidiera con
lo esperado, porque «coincide» no es evidencia.

El aviso «A newer version of the app exists» **no apareció**, así que la lectura no es sobre caché.

| | `OT_OrdenesTrabajo` | `PLA_PlanMantenimiento` |
|---|---|---|
| Clave | `OTID` | `PlanID` |
| `App formula` | vacío | vacío |
| `Initial value` | `= UNIQUEID()` | `= UNIQUEID()` |
| `Key` | marcado | marcado |
| `_RowNumber` con `Key` | **no** | **no** |

Y las dos columnas virtuales, que el panel del editor rotula como tales —«`OT_OrdenesTrabajo :
Etiqueta (virtual)`»—:

| | `App formula` | `Show?` | `Label` | Única con `Label` |
|---|---|---|---|---|
| `OT_OrdenesTrabajo.Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` | sí | sí | sí, de 15 columnas |
| `PLA_PlanMantenimiento.Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` | sí | sí | sí, de 9 columnas |
```

`OTID` y `PlanID` tienen `Initial value = UNIQUEID()` y `Key` marcada; `_RowNumber` no la tiene; y
las dos columnas virtuales `Etiqueta` están con `Show?` y `Label` activos, únicas de su tabla. Es la
condición que el mapeo de columnas de `RG-38` necesita para poder cablearse (§3.3) y que la propia
`ESPEC-005` §7.1 ya asumía.

**Y fue de solo lectura, verificado con dos instrumentos, no uno.** El acta lo dice —*"Lectura de
vuelta: `instantanea.py comparar antes-de-la-ventana tras-p09` → NINGUNA CELDA CAMBIO"*— y se
reconfirma hoy, corriendo el mismo comando otra vez sobre las instantáneas que quedaron en el
repositorio:

```bash
python scripts/instantanea.py comparar antes-de-la-ventana tras-p09
```
```
NINGUNA CELDA CAMBIO.
```

```bash
python -c "
import json
d = json.load(open('BD/instantaneas/tras-p09.json', encoding='utf-8'))
for t in ['OT_OrdenesTrabajo','MAN_Mantenimientos','CHK_Checklists','CHD_ChecklistDetalle',
          'FOT_Fotografias','FIR_Firmas','NOV_Novedades','PLA_PlanMantenimiento']:
    print(t, len(d.get(t, [])))
"
```
```
OT_OrdenesTrabajo 0
MAN_Mantenimientos 0
CHK_Checklists 0
CHD_ChecklistDetalle 0
FOT_Fotografias 0
FIR_Firmas 0
NOV_Novedades 0
PLA_PlanMantenimiento 0
```

**Las ocho tablas siguen en cero.** La ventana barata sigue abierta — `P-09` la usó y no la cerró.

**Lo que `P-09` no cierra es el resto de `ENCARGO_VENTANA.md`.** De las 54 columnas que ese encargo
lista como pendientes de cotejo «a mano» en las ocho tablas, 9 son de `OT_OrdenesTrabajo`, y siguen
pendientes hoy — verificado con el mismo instrumento que las contó por primera vez, no con el
`ENCARGO_VENTANA.md` citado de memoria:

```bash
python -c "
import sys;sys.path.insert(0,'scripts')
from inferencia import clasificar
for t,c,m in clasificar()['a mano']:
    if t=='OT_OrdenesTrabajo': print(c['nombre'])
"
```
```
ActivoID
TecnicoID
SupervisorID
Tipo
EstadoOrdenID
OTOrigenID
Observaciones
CerradaPor
Activo
```

`EstadoOrdenID` está entre las nueve, y de ella depende la desreferencia `[EstadoOrdenID].[EsFinal]`
de la propia `RG-37`: si el `Ref` no está confirmado, la regla no puede leer `EsFinal` y el fixture
de §6 fallaría por un motivo que no tiene nada que ver con la expresión que se está probando. Esto
fija, como precondición y no como recomendación de secuencia, lo que `PRUEBA-006` exige antes de la
primera fila de cualquier fixture que toque `OT_OrdenesTrabajo` (§6).

## 3. Qué cambia exactamente

| Mecanismo | Antes | Después | Nota |
|---|---|---|---|
| Marcar una orden vencida | `RG-08`, `Bot programado` sobre `OT_OrdenesTrabajo.EstadoOrdenID`. Mueve la orden al estado `Vencida`, que es final | `RG-37`, `App formula` sobre columna **VIRTUAL** `EstaVencida` (`Yes/No`) en `OT_OrdenesTrabajo`. Misma expresión exacta: `AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`. No escribe, no mueve el estado, se recalcula en cada sincronización | El estado de la orden no cambia solo. `EstaVencida` es una lectura, no una decisión. Su consumidor: §3.2 |
| Generar las órdenes de la semana desde el plan | `RG-12`, `Bot programado` sobre `PLA_PlanMantenimiento`. Condición `[ProximaFecha] <= TODAY() + 7` | `RG-38`, `Accion` (nuevo tipo) sobre `PLA_PlanMantenimiento`. Una vista/slice con la condición `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)`, más una acción `Data: add a new row to another table using values from this row` que el supervisor pulsa —individualmente o en bloque— y crea la fila en `OT_OrdenesTrabajo` | El disparo pasa de automático a manual. Ver §3.3 para el mapeo de columnas |
| Estado `Vencida` en `EOT_EstadosOrden` | Fila con `QuienCambia = Sistema`, `EsFinal = Y` | Se conserva la fila y `EsFinal = Y`. Cambia el dato `QuienCambia`, de `Sistema` a `Supervisor` | Ver §3.1. Es un cambio de **dato**, no de columna |
| Estado `Programada` en `EOT_EstadosOrden` | Fila con `QuienCambia = Sistema` | Se conserva la fila. Cambia el dato `QuienCambia`, de `Sistema` a `Supervisor` | Ver §3.1. Mismo argumento que `Vencida`, misma superficie de aplicación (§6) |

### 3.1 Qué pasa con `Vencida` y con `Programada` como estados — la pregunta central de este documento

**No sobra.** Se conserva como una de las siete filas de `EOT_EstadosOrden`, pero cambia lo que
significa. Hoy es una consecuencia automática del paso del tiempo, escrita por `Sistema`. Sin
`RG-08`, nadie la escribe nunca de forma automática, así que dejarla con `QuienCambia = Sistema`
sería exactamente el defecto que este proyecto ya pagó una vez: **un campo lleno que describe algo
que ya no ocurre** (`ACT_Activos.CodigoQR`, citado en las instrucciones de este agente, es el
precedente). Se adopta un significado distinto y se declara así, no se deja flotando:

**`Vencida` pasa de ser una marca automática de retraso a ser una decisión del supervisor de que
una orden no se va a ejecutar y se cierra sin trabajo hecho.** Es una disposición final distinta de
las otras dos que ya existen: `Cerrada` es "se hizo el trabajo", `Suspendida` es "se pausó y puede
reanudarse", y `Vencida` pasa a ser "no se va a hacer, y alguien lo decidió". Con esa lectura,
**`EsFinal = Y` es correcto** — es exactamente lo que se espera de una disposición final tomada por
una persona — y lo que hay que corregir no es la columna, es el dato `QuienCambia`, que debe decir
`Supervisor`, no `Sistema`, porque ya no hay ningún mecanismo automático que la escriba.

Esto resuelve, sin necesidad de un octavo estado, la pregunta que `docs/ROADMAP.md` dejaba abierta
con tres salidas: no hace falta que `Vencida` deje de ser final (se queda final, con otro dueño), ni
hace falta una transición de reapertura (una orden vencida por decisión del supervisor no se
reabre; si el trabajo se retoma, se hace desde una orden nueva, igual que cualquier otro trabajo no
planeado). La tercera salida —que el vencimiento sea una marca y no un estado— es la que resuelve
`RG-37` para el caso que sí necesitaba dejar de ser un estado: el aviso de que una orden abierta
está tarde.

**Esto es un supuesto de diseño, declarado como tal en §7**, porque nadie de operación lo ha
confirmado. Es corregible: si operación decide que una orden vencida sí debe poder reabrirse, la
fila y el dato quedan igual y lo que cambia es una regla nueva de reapertura, no esta.

**El mismo argumento se aplica a `Programada`, y el dictamen lo señaló porque esta especificación
no lo había nombrado.** Hoy la fila `Programada` de `EOT_EstadosOrden` también dice
`QuienCambia = Sistema` (§2.2). Antes de `RG-38`, era correcto: `RG-12`, el bot semanal, dejaba la
orden nueva en `Programada` sin que nadie la tocara. Tras `RG-38`, quien deja una orden en
`Programada` es **un supervisor pulsando la acción** —el mapeo de §3.3 fija
`EstadoOrdenID = "Programada"` como el literal que esa acción escribe, y la acción no se dispara
sola: la dispara una persona—. Dejarlo en `Sistema` sería, con el mismo argumento que ya se usó para
`Vencida`, *"un campo lleno que describe algo que ya no ocurre"* — y sería incoherente aplicar ese
argumento a una fila del catálogo y no a la otra.

**Lo único que lo sostiene en parte es `RG-10`.** Sigue siendo un `Bot` por evento —no un
`Bot programado`, así que sí corre en la cuenta gratuita (§2.1)— y crea una orden de seguimiento
cuando `RequiereSegundaVisita = TRUE`. Es, en sentido estricto, un mecanismo automático que también
podría dejar una orden en `Programada`. Pero el modelo no declara qué `EstadoOrdenID` le pone esa
orden —no hay `Initial value` ni un `Step` documentado en `REGLAS` para `RG-10` más allá del
disparador (`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, sección de la propia regla)—, así que no hay
en el archivo ninguna evidencia de que aterrice en `Programada` y no, por ejemplo, directamente en
`Asignada` —una orden de seguimiento nace ya sabiendo a qué técnico corresponde, que es
precisamente la condición para saltarse `Programada`—. **No hay ninguna prueba documental de que
`RG-10` sea hoy la razón por la que `Programada` dice `Sistema`.**

**Se decide: `QuienCambia` de `Programada` pasa de `Sistema` a `Supervisor`, igual que `Vencida`.**
El único mecanismo de esta especificación cuyo literal para esa columna está verificado en el
archivo (§3.3) es humano. Si en el futuro se confirma que `RG-10` también deja órdenes en
`Programada`, eso no revierte la decisión: seguiría siendo cierto que el camino *principal* hacia
`Programada` —el volumen semanal del plan, del orden de 80 a 90 órdenes (§2.7), frente a las
excepcionales de segunda visita— pasó a ser una decisión de una persona, y `QuienCambia` documenta
quién decide, no una lista de todo lo que técnicamente podría escribir la columna: ninguna otra fila
del catálogo lo hace así tampoco (`Asignada` dice `Supervisor` aunque un técnico con permisos de
edición pudiera, en teoría, tocarla a mano).

### 3.2 Dónde ve el supervisor que una orden está vencida — el consumidor de `EstaVencida`

`RG-38` declara su vista dentro de su propia descripción (§4): el supervisor abre `"Vence en 7
días"` sobre `PLA_PlanMantenimiento` y ahí pulsa la acción. `RG-37`, en la versión anterior de este
documento, declaraba una columna y nada más — ni vista, ni slice, ni aviso, ni reporte. Es
exactamente el molde de `CLAUDE.md` §7.13 que esta misma especificación le reprocha a `RG-08`: una
regla puesta, bien escrita, que no hace nada, porque nadie la mira.

**Se declara un consumidor mínimo, con el mismo mecanismo que ya usa `RG-38` para su propia vista —
no se modela como una `REGLA` aparte, porque `REGLAS` no tiene un `tipo` para vistas y no hace falta
crear uno para una sola fila.** Sobre `OT_OrdenesTrabajo`, una vista `"Órdenes vencidas"` con la
condición `[EstaVencida] = TRUE`, visible para el rol Supervisor. Es de solo lectura: no añade
ningún botón ni ninguna acción, solo hace visible lo que `EstaVencida` ya calcula. Se declara dentro
de la propia descripción de `RG-37` en `scripts/modelo_objetivo.py` (§4), no como una regla nueva.

**Esto no cierra el punto por completo, y se dice así.** No hay histórico (§3.4: si la orden se
cierra tarde, `EstaVencida` vuelve a `FALSE` y la vista deja de listarla) y no hay aviso activo —el
supervisor tiene que abrir la vista, nada le notifica—. Es la misma limitación que ya tiene `RG-38`
sin un octavo mecanismo que avise por correo, y no se resuelve aquí: **el alcance de esta
especificación es que la información exista y sea visible bajo demanda, no que empuje una
notificación.** Si eso hace falta, es una especificación futura sobre `RG-07` o un bot nuevo, no
esta.

### 3.3 El mapeo de columnas de la acción de `RG-38`, verificado columna por columna contra el modelo

```bash
python -c "
import sys;sys.path.insert(0,'scripts')
from modelo_objetivo import MODELO
for c in MODELO['PLA_PlanMantenimiento']['columnas']:
    print(c['nombre'], c.get('tipo'), c.get('ref') or '', 'obligatoria' if c.get('obligatoria') else '')
print('---')
for c in MODELO['OT_OrdenesTrabajo']['columnas']:
    print(c['nombre'], c.get('tipo'), c.get('ref') or '', 'obligatoria' if c.get('obligatoria') else '')
"
```
```
PlanID Text  
ActivoID Ref ACT_Activos obligatoria
FrecuenciaID Ref FRE_Frecuencias obligatoria
UltimaEjecucion Date 
ProximaFecha Date  obligatoria
ResponsableID Ref USR_Usuarios
Activo Yes/No 
---
OTID Text  
ActivoID Ref ACT_Activos obligatoria
TecnicoID Ref USR_Usuarios obligatoria
SupervisorID Ref USR_Usuarios obligatoria
Tipo Enum  obligatoria
FechaProgramada DateTime  obligatoria
EstadoOrdenID Ref EOT_EstadosOrden obligatoria
OTOrigenID Ref OT_OrdenesTrabajo 
Observaciones LongText 
FechaCierre DateTime 
CerradaPor Ref USR_Usuarios 
Activo Yes/No 
```

`OT_OrdenesTrabajo` exige `ActivoID`, `TecnicoID`, `SupervisorID`, `Tipo`, `FechaProgramada` y
`EstadoOrdenID`. `OTID` no necesita mapeo: `ESPEC-005` ya la resolvió con `Initial value =
UNIQUEID()`, que se dispara igual cuando la fila la crea una acción que cuando la crea un
formulario (mismo supuesto que `ESPEC-005` §7.1 ya adopta, no uno nuevo). El mapeo propuesto,
columna por columna:

| Columna de `OT_OrdenesTrabajo` | Valor en `Set these columns` | De dónde sale |
|---|---|---|
| `ActivoID` | `[ActivoID]` | Copia directa de la fila de `PLA_PlanMantenimiento` |
| `TecnicoID` | `[ResponsableID]` | Ya existe en `PLA_PlanMantenimiento`, `Ref` a `USR_Usuarios` |
| `SupervisorID` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` | **No es un mecanismo nuevo**: es la expresión literal que ya usa `NOV_Novedades.UsuarioID` como `Initial value` en el modelo aplicado hoy, para resolver quién es el usuario que dispara la acción |
| `Tipo` | `"Preventivo"` | Literal. Coherente con que el plan solo genera preventivos |
| `FechaProgramada` | `[ProximaFecha]` | `Date` en el origen, `DateTime` en el destino. AppSheet admite la conversión; el formato exacto (si hace falta `TEXT()` o una hora por defecto) es un detalle de presentación, mismo tratamiento que `ESPEC-005` §3.3 dio al separador de `Etiqueta` |
| `EstadoOrdenID` | `"Programada"` | Literal contra la clave del catálogo. Legítimo: `EOT_EstadosOrden` está en `CLAVE_ES_LA_PALABRA` |

`OTOrigenID`, `Observaciones`, `FechaCierre` y `CerradaPor` se dejan en blanco: no aplican a una
orden recién creada.

**Riesgo verificado, no supuesto: `ResponsableID` es opcional en `PLA_PlanMantenimiento` y
`TecnicoID` es obligatoria en `OT_OrdenesTrabajo`.** Si una fila del plan no tiene `ResponsableID`
poblado, la acción fallaría al validar el campo requerido del destino. Se declara en §6, no se
resuelve aquí: exige que operación mantenga `ResponsableID` poblado en cada fila de
`PLA_PlanMantenimiento` que se vaya a usar con esta acción, y hoy nada lo obliga (no hay
`Required_If` sobre esa columna).

### 3.4 Qué se pierde con cada alternativa, y quién se queda con lo que falta

**`RG-37` (columna virtual en vez de bot programado).**
- Se pierde el registro histórico de que una orden **estuvo** vencida en algún momento. Si la
  orden se cierra tarde, `EstaVencida` vuelve a `FALSE` en cuanto `EstadoOrdenID.EsFinal` pasa a
  verdadero, y no queda ninguna marca de que hubo un retraso. Esto es exactamente el precio que ya
  anticipaba el encargo: "un reporte no puede decir 'estaba vencida el día X'". **Lo asume
  operación**, y solo importa si D-13 (indicadores de cumplimiento e interventoría) llega a
  necesitar ese dato — hoy D-13 sigue abierta (`docs/ALCANCE_Y_SUPUESTOS_SGMC.md` §3.3), así que no
  hay ningún consumidor que dependa de él todavía. Es coherente con `RG-18`, que ya prohíbe filtrar
  el histórico por la bandera actual del padre: aquí el argumento es el mismo un nivel más arriba.
  Si D-13 lo necesita, la solución no es esta regla: es una columna que **sí** escriba la primera
  vez que se detecta el retraso (un `App formula` sobre una columna real, o un evento), y eso es
  una especificación futura, no esta.
- Se gana que la señal está siempre al día (se recalcula en cada sincronización, no al día
  siguiente de que corriera un bot que en esta cuenta no corre nunca) y que no bloquea el cierre.

**`RG-38` (vista + acción en vez de bot programado).**
- Se pierde la generación automática. **Alguien decide**, cada semana, cuándo pulsar el botón. Si
  nadie lo pulsa esa semana, no se generan órdenes y nada avisa de que no se generaron —no hay
  ningún mecanismo, ni en esta especificación ni en el modelo, que note la ausencia de una
  ejecución manual—. **Lo asume el supervisor**, y es un costo operativo real: por orden de
  magnitud (§2.7), entre 80 y 90 preventivos por semana en el escenario de hoy con 368 activos.
  Seleccionar y confirmar ese volumen a mano, aunque sea con una acción en bloque, no es gratis en
  tiempo del supervisor, y crece con el inventario.
- Se gana trazabilidad de intención: en un sistema cuyo propósito es que la evidencia sea
  defendible, que las órdenes de la semana las genere una persona que lo decide dista de ser un
  consuelo menor —es el argumento de fondo del encargo, y se sostiene—: hoy, si `RG-12` fallara en
  silencio (por ejemplo, por quedarse sin plan de pago un mes y nadie notarlo, precisamente el
  escenario documentado en §2.1), nadie lo vería hasta que faltaran órdenes. Con la acción manual,
  la ausencia de órdenes tiene siempre una causa localizable: nadie la pulsó.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, en `REGLAS`. No se toca `MODELO`, `RENOMBRADOS`,
`CAMPOS_RETIRADOS`, `RETIRADAS`, `CLAVE_LEGIBLE` ni `CLAVE_GENERADA`: ninguna tabla ni columna real
cambia.

**Se retiran los dos `dict` de `RG-08` y `RG-12` de `REGLAS`.** Siguiendo el precedente de
`ESPEC-004` con `RG-02`/`RG-19` (*"se elimina el `dict`... en el hueco numérico que dejan... al
desaparecer"*), los identificadores `RG-08` y `RG-12` no se reutilizan: quedan como huecos en la
numeración, y el hueco documenta que ahí hubo un mecanismo descartado, no un olvido.

**Se añaden `RG-37` y `RG-38`:**

```python
dict(id="RG-37", tabla="OT_OrdenesTrabajo", columna="(tabla)",
     tipo="App formula", cubre="D-06",
     expresion="AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())",
     nombre_virtual="EstaVencida",
     descripcion=("EstaVencida, columna VIRTUAL (Yes/No), no en MODELO: F-02 no la exige, no "
                  "toca la hoja. Reemplaza a RG-08. Misma condicion exacta que tenia el bot "
                  "programado, pero como lectura que se recalcula en cada sincronizacion: no "
                  "escribe, no mueve el estado, y el tecnico que llega tarde sigue pudiendo "
                  "cerrar. Su consumidor: una vista 'Ordenes vencidas' sobre esta tabla, "
                  "condicion [EstaVencida] = TRUE, visible para el rol Supervisor (ver "
                  "ESPEC-006 3.2). No tiene historico: si la orden se cierra tarde, vuelve a "
                  "FALSE y no queda marca de que estuvo vencida, y la vista deja de listarla "
                  "(ver ESPEC-006 3.4).")),
dict(id="RG-38", tabla="PLA_PlanMantenimiento", columna="(tabla)",
     tipo="Accion", cubre="Plan de mantenimiento",
     expresion="AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)",
     descripcion=("Reemplaza a RG-12. La expresion de arriba es la condicion de una vista/slice "
                  "'Vence en 7 dias' sobre esta tabla -no una regla de columna-. Sobre esa vista "
                  "se expone una accion 'Data: add a new row to another table using values from "
                  "this row' (Data > Actions), que el supervisor pulsa -individual o en bloque, "
                  "ver Actions: The Essentials, seccion Bulk actions- y crea la fila en "
                  "OT_OrdenesTrabajo. Mapeo de columnas verificado en ESPEC-006 3.3. No usa "
                  "Automation > Bots: no hay Event ni Schedule, es invocacion explicita del "
                  "usuario. No requiere plan de pago (ver ESPEC-006 2.1: la restriccion "
                  "verificada contra la fuente oficial es sobre bots con Schedule event, no "
                  "sobre acciones invocadas por el usuario).")),
```

**Dato, no regla: las filas `Vencida` y `Programada` de `EOT_EstadosOrden` cambian `QuienCambia` a
`Supervisor` (§3.1).** Esto no se declara en `REGLAS` —`QuienCambia` no lo lee ninguna regla, es
descriptivo (§5)— ni en `MODELO` —la columna ya existe y su tipo no cambia—. Es un cambio de
**contenido** de una tabla de catálogo, y se aplica y se verifica como tal: a mano, en las dos
superficies que hoy coinciden, con el gate ligero de Fase A (§6).

**Se añade el campo `es_label=True` a los `dict` de `RG-35` y `RG-36`** (ya aplicados por
`ESPEC-005`), sin tocar ninguna otra propiedad de esas dos entradas. Es la marca mínima que permite
a los generadores (§6) distinguir "esta columna virtual es la etiqueta de la fila y debe marcarse
`Label`" de "esta columna virtual es otra cosa" — hoy esa distinción no existe en el modelo y los
dos generadores la infieren, mal, de que la columna sea `App formula` sobre `columna="(tabla)"`
(§2.8). Sin este campo, `RG-37` se confundiría con una tercera etiqueta.

**`V-10` de `validar_modelo.py` acepta `columna="(tabla)"` sin exigir que la columna exista en
`MODELO`** (`elif r["columna"] not in ("(tabla)", "(varias)")`, verificado en el código): es la
misma vía que ya usan `RG-35` y `RG-36`, y la que ya empleaba, sin aplicarse todavía, `RG-29` de
`ESPEC-003` para `MinutosRelojParado`. `RG-38` usa la misma vía aunque no sea una columna sino una
acción, porque `V-10` solo exige que la tabla exista y que la columna sea `(tabla)`, `(varias)` o
un nombre real — no exige que el `tipo` de la regla sea uno de los ya conocidos, y `"Accion"` es un
`tipo` nuevo, verificado por lectura completa de `validar_modelo.py`: ningún `V-` restringe el
universo de valores de `tipo` a una lista cerrada. Ya hay precedente de tipos libres no
column-céntricos en `REGLAS` hoy: `RG-18` es `"Doctrina de reportes"` y su propia expresión dice
"Ver descripcion: es una prohibicion, no una expresion a configurar".

## 5. Qué NO cubre esta especificación

- **El octavo estado, `Devuelta`.** Sigue pendiente en `docs/ROADMAP.md` y en `ESPEC-003`
  (`RG-30`). No tiene relación de mecanismo con lo que aquí se decide: es un estado nuevo, no un
  cambio de quién escribe uno existente.
- **Que `QuienCambia` se imponga con una regla.** Hoy ninguna de las 23 (25 tras esta
  especificación) la lee. Cambiar el dato de las filas `Vencida` y `Programada` (§3.1, §6) no le da
  efecto: sigue siendo, como hoy, un dato descriptivo que nadie hace cumplir. Imponerla es el
  trabajo que `ESPEC-003` ya reserva con `RG-23`/`RG-24`, bloqueada.
- **Un histórico o un aviso activo para `EstaVencida`.** §3.2 declara una vista de solo lectura,
  visible bajo demanda; no incluye correo, notificación push ni una columna que recuerde que la
  orden estuvo vencida después de cerrarse tarde. Es la misma decisión que ya tomó `RG-18` sobre no
  filtrar histórico por la bandera actual del padre, un nivel más arriba (§3.4).
- **Corregir el generador que sigue roto** (`generar_prompt_expresiones.py`, §2.8: la línea que cita
  `RG-10`/`RG-12` a mano, y la sección que falta para `Data > Actions` sin bots). Los otros dos
  generadores con la misma heurística —`generar_reconstruccion.py` y `generar_prompt_cableado.py`—
  ya estaban corregidos desde que se autoría esta especificación (commit `0d3d641`), y el tercero
  (`generar_encargo_ventana.py`) se corrigió después de que el arquitecto lo encontrara (commit
  `f790c91`), verificado en §2.8; ninguno de los tres vuelve a mandarse aquí. Se documenta el
  defecto restante con el detalle necesario para que la orden de ejecución no tenga que volver a
  investigarlo, pero el cambio de código es de la orden, no de esta especificación — mismo reparto
  que `ESPEC-005` hizo con sus propios defectos de código encontrados en el camino.
- **Actualizar `docs/ROADMAP.md`, `docs/FUNCIONAL_SGMC.md` §4 y `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`
  D-06** para que dejen de describir `Vencida` como escrita por `Sistema` y `RG-08`/`RG-12` como
  bots pendientes de plan de pago. Es una corrección de redacción derivada de una decisión ya
  tomada aquí — va por la vía rápida del §6 de `SDD_PIPELINE_SGMC.md` una vez esta especificación
  se apruebe, igual que `ESPEC-005` §2.6 encontró que `ROADMAP.md` ya se había corregido así.
- **Ejercitar la acción de `RG-38` con datos reales.** `PLA_PlanMantenimiento` está vacía (§2.6);
  no hay ninguna fila sobre la que probarla hasta que exista un fixture, que es trabajo del
  verificador (`PRUEBA-006`), no de esta especificación.
- **Decidir si `Vencida` admite reapertura.** §3.1 adopta que no, como supuesto. Si el campo lo
  desmiente, es una especificación nueva y pequeña: una fila de transición, no un rediseño.

## 6. Riesgos y dependencias

- **El generador que sigue roto (§2.8) tiene que corregirse antes de regenerar
  `PROMPT_EXPRESIONES.md`, o ese documento va a instruir mal al ejecutor de la Fase C.**
  `generar_prompt_expresiones.py` necesita dos correcciones dentro del mismo archivo: dejar de citar
  `RG-10`/`RG-12` a mano en la línea de *"Afecta a `RG-10` y a `RG-12`"*, y añadir una sección nueva,
  separada de "los bots", que explique `Data > Actions` sin el paso de `Automation > Bots` para
  `RG-38`. No toca `scripts/modelo_objetivo.py`; es una corrección de código en el generador,
  verificada y localizada en §2.8. Los otros dos generadores con la misma heurística que esta
  especificación había encontrado (`generar_reconstruccion.py`, `generar_prompt_cableado.py`) ya
  estaban corregidos desde que se autoría esta especificación (commit `0d3d641`), y el tercero que el
  arquitecto encontró (`generar_encargo_ventana.py`) se corrigió después (commit `f790c91`); no se
  listan aquí de nuevo.
- **Antes de la primera fila de cualquier fixture que toque `OT_OrdenesTrabajo`: `P-09` cerrada y
  las 9 columnas de esa tabla en `ENCARGO_VENTANA.md` cotejadas — las dos, precondición, no
  secuencia recomendada (§2.9).** `P-09` ya está cerrada, registrada con transcripción literal en
  `docs/sdd/ACTA-005-pruebas.md` (commit `7a6e750`): `OTID` y `PlanID` tienen
  `Initial value = UNIQUEID()` y `Key` marcada. **El cotejo de las 9 columnas también está cerrado**,
  con transcripción literal en `docs/sdd/ACTA-006-cotejo-y-supuesto.md` §1 y con `Ctrl+Shift+R`
  previo —una sesión anterior vio esas mismas nueve como `Text` cuando ya estaban puestas, y era
  caché—: las nueve coinciden con lo esperado, incluida `EstadoOrdenID → Ref EOT_EstadosOrden`, de
  la que depende la desreferencia `[EstadoOrdenID].[EsFinal]` de la propia `RG-37`. Sin ese cotejo,
  un fixture que probara `RG-37` no habría distinguido "la regla está mal" de "el `Ref` no está
  confirmado", y habría apuntado al sitio equivocado.

  **`inferencia.clasificar()` las sigue listando como pendientes, y no es una contradicción.**
  Clasifica por **quién consigue el tipo** —responde *«esta columna necesita mano»*— y no tiene forma
  de saber si esa mano ya pasó: la API devuelve filas, no esquema. La evidencia de estado es el
  acta, no el clasificador. Tomar el uno por el otro fue el hallazgo 2 del dictamen.

- **`ResponsableID` opcional contra `TecnicoID` obligatoria (§3.3).** La acción de `RG-38` falla al
  validar si se ejecuta sobre una fila de `PLA_PlanMantenimiento` sin `ResponsableID`. No hay
  ninguna regla que lo exija hoy. Operación tiene que mantenerlo poblado, o se necesita una
  `Required_If` nueva — no incluida aquí porque cambiaría el comportamiento de captura del plan,
  fuera del alcance de esta especificación.
- **El dato `QuienCambia = Supervisor` en las filas `Vencida` y `Programada` de `EOT_EstadosOrden`
  es un cambio de dato, no de estructura, y no lo controla ningún generador.** Son **dos** filas,
  no una: §3.1 decide las dos con el mismo argumento. `generar_plantilla.py` preserva el contenido
  de las tablas de catálogo entre pasadas (comentario `ORIGEN = SALIDA` en el propio script,
  verificado en el código) y solo completa filas que falten — no reescribe una fila que ya existe.
  El cambio hay que aplicarlo a mano, en las dos superficies que hoy coinciden: las dos filas de
  `BD/Modelo_Datos_PLANTILLA.xlsx` y las dos filas equivalentes del Sheets de producción
  `Modelo_Datos_10082026`. Es un cambio de Fase A (la hoja), gate ligero: se verifica leyendo de
  vuelta, igual que cualquier otro dato — y con dos filas en vez de una, la lectura de vuelta tiene
  que confirmar las dos, no solo la que se mire primero.
- **La ruta de reversión, para la parte que no la tiene.** El punto anterior (`QuienCambia`) se
  revierte con un `UPDATE` de una celda si hace falta: es dato de catálogo, sin costo. **Poblar
  `OT_OrdenesTrabajo` y `MAN_Mantenimientos` con el fixture de `PRUEBA-006` no tiene esa reversión.**
  Las dos son dos de las ocho tablas de `VOLCADO_CIEGO_A` (§2.9, `CLAUDE.md` §7.17): mientras estén
  en cero, corregir un tipo o una clave mal puesta cuesta un clic; en cuanto entra la primera fila,
  cuesta una migración, y ese precio no baja después. `PRUEBA-006` `P-60` cierra su fixture marcando
  `Activo = FALSE`, **nunca `Action: Delete`** —la misma política que ya fijó `PRUEBA-005` §2—, así
  que después de `P-60` las dos tablas **no vuelven a cero**: la ventana se cerró, y cerrarla con
  cuidado no es lo mismo que no cerrarla. No hay manera de deshacer eso una vez ejecutado.

  **Por qué se acepta gastarlo ahora, y no después.** El defecto que esta especificación existe
  para corregir —`RG-08` movía la orden a un estado terminal y le impedía al técnico cerrarla
  (§2.2)— no se puede dar por corregido sin ejercitarlo: `P-55` es la única prueba que demuestra que
  `RG-37` no reproduce ese defecto, y no hay forma de correr `P-55` sin que exista al menos una
  orden real, cerrada, en `OT_OrdenesTrabajo` y `MAN_Mantenimientos`. El costo es acotado y se paga
  una sola vez —3 filas en `OT_OrdenesTrabajo`, 1 en `MAN_Mantenimientos` (`PRUEBA-006` §2)—, y se
  paga **después**, no antes, de que la precondición de arriba (`P-09` y el cotejo de los 9 tipos)
  esté cumplida: así el error que sale caro después de cerrar la ventana —un tipo mal puesto en
  `EstadoOrdenID`— ya se descartó cuando todavía costaba un clic. La alternativa —no probar `RG-37`
  con datos reales— dejaría la especificación entera apoyada en que la lectura de la expresión es
  correcta a ojo, que es exactamente el modo de fallo que documentó la fórmula de geofencing que
  nunca funcionó (instrucciones de este agente).
- **Dependencia de `ESPEC-005`, en lo que sigue sin resolver.** `RG-38` crea filas en
  `OT_OrdenesTrabajo` mediante una acción, y esa acción no se puede cablear en el editor hasta que
  `OTID` tenga `Initial value = UNIQUEID()` puesto — condición que `P-09` ya cumplió (arriba). Lo
  que `ESPEC-005`/`PRUEBA-005` no ha cerrado todavía es el resto de su propio fixture (`P-10` a
  `P-17`, `ACTA-005-pruebas.md`: 9 de 17 siguen `NO EJECUTADA`), y esta especificación no depende de
  eso — depende solo de `P-09`, ya satisfecha.
- **Qué pasa el día que se contrate el plan de pago.** No hay vuelta atrás automática ni conviene
  que la haya. `RG-37` sigue siendo estrictamente mejor que un bot programado con el mismo
  propósito **incluso en el plan de pago**, porque el defecto que corrige (`Vencida` bloqueando el
  cierre) no depende del licenciamiento — es un defecto de diseño del ciclo de estados, verificado
  en §2.2 sin relación con §2.1. Reintroducir un bot programado que escriba `Vencida` reintroduciría
  ese defecto con o sin plan pagado. Para `RG-38`, la pregunta sí depende del licenciamiento: con
  plan de pago, generar automáticamente las órdenes de la semana vuelve a ser técnicamente posible,
  pero el argumento de fondo de §3.4 —que alguien decida generar las órdenes, en un sistema cuyo
  propósito es la trazabilidad, no es un consuelo menor— no depende del precio de la cuenta. La
  decisión de volver a un disparador automático, si se toma, es una especificación nueva que
  compare explícitamente "automático con dueño verificable" contra "automático sin dueño", no un
  regreso simple a `RG-12`.
- **`RG-07` sigue disparando correo real por cada fila nueva en `OT_OrdenesTrabajo`**, la cree un
  técnico, `RG-10`, o ahora la acción de `RG-38`. Nada de esto es nuevo —ya lo documenta
  `docs/ROADMAP.md`—, pero la acción de `RG-38` multiplica el número de filas creadas de una sola
  vez si el supervisor la ejecuta en bloque sobre varias decenas de planes, así que cualquier
  fixture de prueba de `RG-38` hereda la misma precondición que `PRUEBA-005`: desactivar `RG-07`
  antes de crear filas de prueba.

## 7. Supuestos adoptados

1. **Que `Vencida` deja de significar "el sistema detectó un retraso" y pasa a significar "el
   supervisor decidió que esta orden no se va a ejecutar"** (§3.1). No lo ha confirmado operación.
   Se adopta porque es la única lectura que conserva `EsFinal = Y` como correcta sin inventar un
   octavo estado ni una transición de reapertura, y porque es reversible barato: si se desmiente,
   el costo es una fila de transición nueva, no una migración.
2. **Que una acción invocada explícitamente por el usuario ("Data-change action") no está sujeta a
   la misma restricción de plan gratuito que un bot con evento `Schedule`.** Verificado por
   triangulación contra tres fuentes oficiales, no una sola: (a) «Actions: The Essentials»
   (`support.google.com/appsheet/answer/10107706`) describe la invocación explícita del usuario y
   la invocación en la nube vía «automation bots» como dos rutas distintas del mismo sistema de
   acciones, sin mencionar ninguna restricción de licencia para la primera; (b) «Use AppSheet for
   free» (`support.google.com/appsheet/answer/10104499`) nombra explícitamente lo que no funciona
   sin plan de pago —enviar correos y bots con evento de horario— y no nombra las acciones; (c) la
   página de precios de AppSheet (`about.appsheet.com/pricing`) agrupa **"Automate data changes...
   on a schedule"** dentro de las funciones **avanzadas** (de pago), separado de las funciones
   básicas de captura y publicación de la app, que sí están disponibles en el nivel gratuito. No es
   una cita textual única y cerrada como las de `BASE_CONOCIMIENTO_APPSHEET.md` §6 —por eso se
   declara aquí como supuesto y no como confirmado—, pero las tres fuentes apuntan en la misma
   dirección y ninguna la contradice. Si resulta falso, `RG-38` se queda sin mecanismo funcional en
   esta cuenta, igual que `RG-12` hoy, y habría que reabrir esta especificación.
3. **Que `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` resuelve al supervisor que
   pulsa la acción, y no a alguien distinto.** No es un supuesto nuevo: es la misma expresión que
   ya usa `NOV_Novedades.UsuarioID` como `Initial value`, aplicada al modelo. Se hereda su
   verificación, no se repite.
4. **Que `ResponsableID` de `PLA_PlanMantenimiento` es, en la práctica, un técnico y no un equipo o
   un rol.** Es el supuesto que ya trae la columna en el modelo (`alias_justificado="Rol: tecnico
   habitual"`); esta especificación lo reutiliza sin cuestionarlo, porque cuestionarlo es una
   decisión de otra especificación.
5. **El nombre `EstaVencida`.** No colisiona con ninguna columna existente
   (`grep -n '"EstaVencida"' scripts/modelo_objetivo.py` no devuelve nada) y describe sin
   ambigüedad una lectura booleana, siguiendo la convención `Es*` ya usada en `EsFinal`.
6. **El nombre del tipo `"Accion"`, sin acento, en `REGLAS`.** Sigue la convención ASCII que ya usan
   `"Verificacion de evidencia"` y otros tipos existentes en el mismo diccionario, no una decisión
   de estilo nueva.
7. **Que una columna virtual `App formula` con `Show?` activo se lee por la API — medido, ya no es
   supuesto.** De él dependían cuatro pruebas (`P-51` a `P-54`), que leen `EstaVencida` con
   `instantanea.py`, que es la API. Estaba anotado como supuesto porque lo confirmado era otra cosa:
   que las virtuales **inversas de una `Ref`** (`Related <Tabla>`) viajan en las filas
   (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §16). De una `App formula` corriente no había ni cita ni
   observación en todo el repositorio.

   **Se midió en vez de razonarse**, sobre `PAR_Parametros` —3 filas, fuera de las ocho tablas de
   movimiento, así que la prueba no cerró ninguna ventana— y las columnas virtuales sí tienen
   papelera. Acta en `docs/sdd/ACTA-006-cotejo-y-supuesto.md` §2. Lo que devolvió la API:

   ```
   ['Activo', 'Descripcion', 'Nombre', 'ParametroID', 'PruebaVirtual', 'Unidad', 'Valor', '_RowNumber']
   ```

   **`PruebaVirtual` aparece.** Las cuatro pruebas son ejecutables, y el fixture de tres filas de
   `OT_OrdenesTrabajo` ya no se gasta sobre una apuesta. La salida degradada que este supuesto
   proveía —cotejar a ojo y bajar la prueba de *verificada* a *mirada*— deja de hacer falta.

   Se deja escrito porque medirlo costó cinco minutos y equivocarse costaba la ventana entera. Es
   la forma que debería tener cualquier supuesto que se pueda medir barato.

8. **Que `QuienCambia = Supervisor` es correcto para `Programada` aunque `RG-10` (bot por evento,
   §2.1) también pueda crear órdenes.** Desarrollado en §3.1: el modelo no declara qué
   `EstadoOrdenID` deja `RG-10` en la orden que crea, así que no hay evidencia documental de que
   aterrice en `Programada`. Si se confirma que sí, el supuesto no se revierte solo por eso —ver
   §3.1 para el argumento completo—, pero sería una razón para reabrir la pregunta con datos reales
   en vez de con lo que dice el archivo.

---

## 8. Cierre — qué se acepta como riesgo y qué queda cerrado

**Esta especificación se cierra en su tercera pasada de arquitecto, por la regla de `CLAUDE.md`
§7.18**, y no porque no queden objeciones: quedan, y aquí están con nombre. La regla dice que **un
hallazgo bloquea solo si nombra qué se rompe en producción**, y que a la tercera pasada lo que
sobreviva se escribe como riesgo aceptado en vez de dar otra vuelta.

Las tres pasadas costaron 911 líneas de reescritura. La cuarta habría costado otro tanto para
mover prosa, mientras la única pregunta con consecuencia real —¿de qué tipo es `EstadoOrdenID`?—
seguía sin que nadie abriera el editor. El propio arquitecto lo dijo al bloquear:

> *No hagas una cuarta ronda de reescritura sobre estas 911 líneas. Cierra primero la condición 1
> —una sesión de editor, con recarga en duro y transcripción— porque es un hecho del mundo, no de
> documento.*

### Lo que se cerró midiendo, no escribiendo

| | Cómo |
|---|---|
| Las 9 columnas de `OT_OrdenesTrabajo` | `ACTA-006` §1 — editor, `Ctrl+Shift+R`, transcripción literal |
| El supuesto 7, la virtual por API | `ACTA-006` §2 — `PruebaVirtual` sobre `PAR_Parametros`, y aparece |
| `clasificar()` como evidencia de estado | Retirado: clasifica quién consigue el tipo, no si ya se hizo |
| El dueño de la precondición | Cerrado aquí, no delegado a `PRUEBA-006` |

### Riesgos aceptados — 2026-08-11

1. **La prosa de esta especificación es larga y en partes redundante.** Tres reescrituras dejaron
   argumentos repetidos entre §2.9, §6 y §7. Nadie va a leer 911 líneas de corrido. **Se acepta**
   porque acortarla es reescribir, y reescribir es lo que esta regla existe para parar. Si alguien
   la resume algún día, que sea al ejecutarla, con lo aprendido.

2. **`RG-38` decide una ventana de 7 días sin haber preguntado a operación.** Es el método
   declarado del proyecto (`ALCANCE_Y_SUPUESTOS_SGMC.md` §1) y está escrito como supuesto
   refutable. **Se acepta.** Lo que romperá si está mal es visible y barato: el supervisor verá que
   la acción no se le ofrece cuando la esperaba, y el número se cambia en un campo.

3. **`QuienCambia = Supervisor` para `Programada` puede quedar mal si `RG-10` deja ahí sus
   órdenes** (supuesto 8). **Se acepta**: es un dato en dos filas de `EOT_EstadosOrden`, se cambia
   sin migración, y hoy no hay forma de saberlo sin ejecutar `RG-10`.

4. **Nueve de las diecisiete pruebas no se han ejecutado**, incluida `P-55` — la que demostraría
   que una orden vencida **sí se puede cerrar**, que es la razón de ser de este documento. No están
   bloqueadas: están **esperando la decisión de gastar la ventana barata**. **Se acepta como riesgo
   explícito**, y es el que más importa nombrar: dentro de un mes esto se leerá como «estaba
   probado» si nadie lo escribe. No lo estaba. Está especificado y validado; no ejecutado.

### Qué significa que esté cerrada

Que entra en la fase 0 —**especificada y validada, no ejecutada**— y que no vuelve al arquitecto.
Lo siguiente que le pase será una `ORDEN-006` y un ejecutor, o nada.
