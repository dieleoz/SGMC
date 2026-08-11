# ESPEC-006 — `RG-08` y `RG-12` dejan de ser bots programados

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.EstaVencida -->
<!-- D-03 compara Tabla.Columna contra MODELO, y EstaVencida a propósito NUNCA entra en MODELO:
     es una columna virtual declarada solo en REGLAS (RG-37, §4), siguiendo el mismo mecanismo
     que RG-35/RG-36 de ESPEC-005. Citarla en prosa como Tabla.Columna es legítimo -es como se
     documenta una virtual-, no un hueco del modelo. -->

**No aplicada.** Este documento es del especificador. No toca `scripts/modelo_objetivo.py`, el
Sheets de producción ni el editor de AppSheet. Escrita contra el commit `9188b25`. Hay un ejecutor
cerrando `ESPEC-005` en paralelo; ninguno de los archivos que edita esa especificación
(`ESPEC-005-clave-otid-planid.md`, `ORDEN-005-*`, `ACTA-005-*`) se toca aquí.

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

**Hallazgo colateral, no autoritativo: un artefacto superado contradice el dato vigente.**
`scripts/faseA_sheets.gs` —el guion de Google Apps Script de cuando la Fase A era trabajo manual
sobre el Sheets, antes de que `generar_plantilla.py` la generara del modelo— declara la misma fila
`Vencida` con `EsFinal = false`, no `true`. Ese archivo no está referenciado desde ningún otro
script del repositorio (`grep -rl faseA_sheets scripts/ docs/` no devuelve nada) y `SDD_PIPELINE_SGMC.md`
ya declara superada la Fase A manual. No se usa como fuente: el dato vigente es el de arriba, en
las dos fuentes que sí gobiernan la aplicación hoy. Se deja constancia porque es exactamente el
tipo de documento que, si alguien lo lee sin saber que está superado, produce una afirmación falsa
sobre el sistema — la patología que este proyecto existe para evitar.

### 2.3 Ningún otro estado library da salida a una orden vencida

```bash
python -c "
import sys;sys.path.insert(0,'scripts')
from modelo_objetivo import REGLAS
print([r['id'] for r in REGLAS if r['tabla']=='OT_OrdenesTrabajo'])
"
```
```
['RG-35', 'RG-08', 'RG-14', 'RG-05', 'RG-07']
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

**Los generadores de expresiones — aquí sí hay un defecto real, no cosmético, verificado
ejecutándolos.** `scripts/generar_reconstruccion.py` y `scripts/generar_prompt_cableado.py`
detectan una columna virtual con la condición `r["tipo"] == "App formula" and r.get("columna") ==
"(tabla)"`, y **los dos asumen que toda regla que cumple esa condición es la etiqueta `Label` y la
llaman `Etiqueta` de forma literal**:

```
scripts/generar_reconstruccion.py:
    w("> ... se llama **`Etiqueta`**, lleva esa expresión en su `App formula`, y después
    >  **`Show?` activo** y **`Label` marcado**.")

scripts/generar_prompt_cableado.py:
    for _t, _e in sorted(_virtuales):
        w("| `%s` | **`Etiqueta`** | `%s` |" % (_t, _e))
    ... instruye marcar Show? y Label sobre esa fila.
```

Esto es correcto hoy porque las dos únicas reglas con esa forma son `RG-35` y `RG-36`, y las dos
son, en efecto, la etiqueta `Etiqueta`. **Declarar `EstaVencida` con la misma forma —`App formula`
sobre `columna="(tabla)"`, que es la única forma que `V-10` acepta para una columna virtual (§4)—
hace que estos dos generadores digan, al regenerarse, que `EstaVencida` "se llama `Etiqueta`" y que
hay que marcarla `Label`.** Es falso en los dos puntos: no se llama `Etiqueta` y no debe ser
`Label` — ya hay una `Label` en esa tabla, puesta por `RG-35`, y `Label` solo puede haber una
(`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, sección de la propia regla, cita a Google ya incorporada
en `ESPEC-005` §2.5). Verificado leyendo el código de los dos generadores completo, no solo el
fragmento: ninguno de los dos consulta el nombre real de la columna virtual en ningún otro sitio,
porque hasta hoy nunca hizo falta — solo existía un caso.

`scripts/generar_prompt_expresiones.py` tiene un defecto distinto, también verificado en el código:
la sección *"La trampa: un bot que AÑADE UNA FILA se hace en dos sitios"* dice literalmente
`w("Afecta a `RG-10` y a `RG-12`, que son los dos que crean órdenes.")` y filtra con
`r["id"] in ("RG-10", "RG-12")` — un identificador citado a mano, no derivado. Si `RG-12`
desaparece de `REGLAS` (§4), esa frase sigue imprimiéndose con un identificador que ya no existe en
el modelo, y la propia sección dejaría de ser cierta para el mecanismo que sustituye a `RG-12`: el
reemplazo no es un bot, así que **no** se configura en dos sitios (`Data > Actions` +
`Automation > Bots`) — se configura solo en `Data > Actions`, y se expone en una vista (§4). Este
generador necesita, además de dejar de citar `RG-12`, una sección nueva para el mecanismo de
`RG-38` que no hable de bots.

**Los tres defectos son de código, no de diseño, y su arreglo es trabajo del ejecutor (`ORDEN-006`),
no de esta especificación** — el mismo tratamiento que `ESPEC-005` dio a los defectos de código que
encontró en `V-11`, `PROMPT_CABLEADO.md` y `capacidad.py` (ver la cabecera de ese documento). Se
listan con el detalle necesario para que la orden no tenga que volver a investigarlos (§6).

## 3. Qué cambia exactamente

| Mecanismo | Antes | Después | Nota |
|---|---|---|---|
| Marcar una orden vencida | `RG-08`, `Bot programado` sobre `OT_OrdenesTrabajo.EstadoOrdenID`. Mueve la orden al estado `Vencida`, que es final | `RG-37`, `App formula` sobre columna **VIRTUAL** `EstaVencida` (`Yes/No`) en `OT_OrdenesTrabajo`. Misma expresión exacta: `AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`. No escribe, no mueve el estado, se recalcula en cada sincronización | El estado de la orden no cambia solo. `EstaVencida` es una lectura, no una decisión |
| Generar las órdenes de la semana desde el plan | `RG-12`, `Bot programado` sobre `PLA_PlanMantenimiento`. Condición `[ProximaFecha] <= TODAY() + 7` | `RG-38`, `Accion` (nuevo tipo) sobre `PLA_PlanMantenimiento`. Una vista/slice con la condición `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)`, más una acción `Data: add a new row to another table using values from this row` que el supervisor pulsa —individualmente o en bloque— y crea la fila en `OT_OrdenesTrabajo` | El disparo pasa de automático a manual. Ver §3.2 para el mapeo de columnas |
| Estado `Vencida` en `EOT_EstadosOrden` | Fila con `QuienCambia = Sistema`, `EsFinal = Y` | Se conserva la fila y `EsFinal = Y`. Cambia el dato `QuienCambia`, de `Sistema` a `Supervisor` | Ver §3.1. Es un cambio de **dato**, no de columna |

### 3.1 Qué pasa con `Vencida` como estado — la pregunta central de este documento

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

### 3.2 El mapeo de columnas de la acción de `RG-38`, verificado columna por columna contra el modelo

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

### 3.3 Qué se pierde con cada alternativa, y quién se queda con lo que falta

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
                  "cerrar. No tiene historico: si la orden se cierra tarde, vuelve a FALSE y no "
                  "queda marca de que estuvo vencida (ver ESPEC-006 3.3).")),
dict(id="RG-38", tabla="PLA_PlanMantenimiento", columna="(tabla)",
     tipo="Accion", cubre="Plan de mantenimiento",
     expresion="AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)",
     descripcion=("Reemplaza a RG-12. La expresion de arriba es la condicion de una vista/slice "
                  "'Vence en 7 dias' sobre esta tabla -no una regla de columna-. Sobre esa vista "
                  "se expone una accion 'Data: add a new row to another table using values from "
                  "this row' (Data > Actions), que el supervisor pulsa -individual o en bloque, "
                  "ver Actions: The Essentials, seccion Bulk actions- y crea la fila en "
                  "OT_OrdenesTrabajo. Mapeo de columnas verificado en ESPEC-006 3.2. No usa "
                  "Automation > Bots: no hay Event ni Schedule, es invocacion explicita del "
                  "usuario. No requiere plan de pago (ver ESPEC-006 2.1: la restriccion "
                  "verificada contra la fuente oficial es sobre bots con Schedule event, no "
                  "sobre acciones invocadas por el usuario).")),
```

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
  especificación) la lee. Cambiar el dato de la fila `Vencida` (§3.1, §6) no le da efecto: sigue
  siendo, como hoy, un dato descriptivo que nadie hace cumplir. Imponerla es el trabajo que
  `ESPEC-003` ya reserva con `RG-23`/`RG-24`, bloqueada.
- **Corregir los tres generadores** (`generar_reconstruccion.py`, `generar_prompt_cableado.py`,
  `generar_prompt_expresiones.py`) que §2.8 encontró rotos. Se documenta el defecto exacto y la
  causa para que la orden de ejecución no tenga que volver a investigarlo, pero el cambio de código
  es de la orden, no de esta especificación — mismo reparto que `ESPEC-005` hizo con sus propios
  defectos de código encontrados en el camino.
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

- **Los tres generadores rotos (§2.8) tienen que corregirse antes de regenerar `PROMPT_CABLEADO.md`,
  `RECONSTRUCCION_EXPRESIONES.md` o `PROMPT_EXPRESIONES.md`, o esos documentos van a instruir mal
  al ejecutor de la Fase C.** Concretamente: `generar_reconstruccion.py` y
  `generar_prompt_cableado.py` deben filtrar sus secciones de "columna virtual = Label" por
  `r.get("es_label")` en vez de por la forma `tipo == "App formula" and columna == "(tabla)"`, y
  usar `r.get("nombre_virtual", "Etiqueta")` en vez del literal `"Etiqueta"` para el resto de
  columnas virtuales sin `es_label`. `generar_prompt_expresiones.py` debe dejar de citar `RG-12`
  por id fijo en su sección de bots que crean filas, y necesita una sección nueva, separada de "los
  bots", que explique `Data > Actions` sin el paso de `Automation > Bots` para `RG-38`. Ninguno de
  los tres cambios toca `scripts/modelo_objetivo.py`; son correcciones de código en los
  generadores, verificadas y localizadas en §2.8.
- **`ResponsableID` opcional contra `TecnicoID` obligatoria (§3.2).** La acción de `RG-38` falla al
  validar si se ejecuta sobre una fila de `PLA_PlanMantenimiento` sin `ResponsableID`. No hay
  ninguna regla que lo exija hoy. Operación tiene que mantenerlo poblado, o se necesita una
  `Required_If` nueva — no incluida aquí porque cambiaría el comportamiento de captura del plan,
  fuera del alcance de esta especificación.
- **El dato `QuienCambia = Supervisor` en la fila `Vencida` de `EOT_EstadosOrden` es un cambio de
  dato, no de estructura, y no lo controla ningún generador.** `generar_plantilla.py` preserva el
  contenido de las tablas de catálogo entre pasadas (comentario `ORIGEN = SALIDA` en el propio
  script, verificado en el código) y solo completa filas que falten — no reescribe una fila que ya
  existe. El cambio hay que aplicarlo a mano, en las dos superficies que hoy coinciden: la fila de
  `BD/Modelo_Datos_PLANTILLA.xlsx` y la fila equivalente del Sheets de producción
  `Modelo_Datos_10082026`. Es un cambio de Fase A (la hoja), gate ligero: se verifica leyendo de
  vuelta, igual que cualquier otro dato.
- **Dependencia de `ESPEC-005`.** `RG-37` y `RG-38` crean o podrían crear filas en
  `OT_OrdenesTrabajo`, y esa tabla depende de que `OTID` tenga `Initial value = UNIQUEID()` para no
  descartar filas sin clave en silencio (`ESPEC-005`, aplicada al modelo el 2026-08-10; falta la
  mitad que vive en el editor, según `docs/ENCARGO_VENTANA.md`). Esta especificación no crea ese
  riesgo: lo hereda, y no se puede cablear `RG-38` en el editor hasta que esa mitad esté puesta,
  igual que ya vale para `RG-10`.
- **Qué pasa el día que se contrate el plan de pago.** No hay vuelta atrás automática ni conviene
  que la haya. `RG-37` sigue siendo estrictamente mejor que un bot programado con el mismo
  propósito **incluso en el plan de pago**, porque el defecto que corrige (`Vencida` bloqueando el
  cierre) no depende del licenciamiento — es un defecto de diseño del ciclo de estados, verificado
  en §2.2 sin relación con §2.1. Reintroducir un bot programado que escriba `Vencida` reintroduciría
  ese defecto con o sin plan pagado. Para `RG-38`, la pregunta sí depende del licenciamiento: con
  plan de pago, generar automáticamente las órdenes de la semana vuelve a ser técnicamente posible,
  pero el argumento de fondo de §3.3 —que alguien decida generar las órdenes, en un sistema cuyo
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
