# ESPEC-009 — Proteger la identidad de quién ejecuta, con `Editable_If`

## 0. Por qué este documento es corto, y en qué se diferencia de `ESPEC-008`

El mecanismo es el mismo que `RG-20`/`RG-39`/`RG-40`: una regla hermana `Editable_If = FALSE` por
columna. Lo que cambia respecto de `ESPEC-008` son dos cosas, verificadas y no supuestas:

1. **El generador ya no está roto.** `ESPEC-008` §2.6 encontró que `generar_prompt_cableado.py`
   dejaba de citar el `Initial value` de una columna en cuanto cualquier regla la tocaba, y
   `ORDEN-008` lo corrigió el mismo día. El §2.6 de este documento repite la prueba —con las cuatro
   columnas de esta especificación, no con la de `ESPEC-008`— y confirma que el parche sigue
   funcionando: no hace falta tocar ningún generador.
2. **Aquí sí hay una decisión de diseño**, y el §1 la resuelve verificando, no suponiendo: existen
   **dos** columnas llamadas `TecnicoID` en el modelo, una en `OT_OrdenesTrabajo` y otra en
   `MAN_Mantenimientos`, y solo la segunda es el defecto de esta especificación. Confundirlas sería
   congelar la asignación de la orden en vez de (o además de) la ejecución.

## 1. Qué se quiere y por qué

Cuatro columnas resuelven **quién hizo algo** con una expresión que llama a `USEREMAIL()`, y ninguna
tiene `Editable_If`. Verificado con el comando exacto del encargo, contra
`scripts/modelo_objetivo.py`, el archivo fuente (no contra el volcado ni contra producción: esto es
estructura del modelo, no dato):

```
$ python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;[print(t,c['nombre'],c.get('tipo'),'editable=',c.get('editable'),'|',c.get('valor_inicial')) for t in MODELO for c in MODELO[t]['columnas'] if 'USEREMAIL' in str(c.get('valor_inicial'))]"
MAN_Mantenimientos TecnicoID Ref editable= None | LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")
MAN_Mantenimientos UsuarioRegistro Text editable= None | USEREMAIL()
NOV_Novedades UsuarioID Ref editable= None | LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")
FOT_Fotografias Usuario Text editable= None | USEREMAIL()
```

Un `Initial value` se evalúa una sola vez, al abrir el formulario, y después es editable por
defecto —el mismo hecho que sostiene `RG-20`/`RG-39`/`RG-40`, verificado con cita oficial en
`docs/BASE_CONOCIMIENTO_APPSHEET.md` §1-3—. Dos de las cuatro son `Ref` a `USR_Usuarios`: un campo
`Ref` se rinde como un selector de las filas de la tabla referenciada, no como texto libre —
comportamiento estándar de AppSheet para el tipo `Ref`, consistente con cómo se han visto y descrito
los `Ref` ya cableados de este proyecto (`ACTA-004`, `ACTA-010`), pero **sin cita oficial propia en
`docs/BASE_CONOCIMIENTO_APPSHEET.md`** — a diferencia de la afirmación sobre `LatLong` como pin
arrastrable (§10), esta no está contrastada contra la fuente en este repositorio. Se declara así, no
como un hecho con cita.

**Lo que se rompe en producción, verificado que nada lo impide (§2.4, §2.5):** un técnico abre el
mantenimiento, elige a otro técnico en el desplegable `TecnicoID`, y la ejecución queda atribuida a
un compañero. Con un toque, no tecleando un correo — esa es la razón verificada por la que las dos
columnas `Ref` son más explotables que las dos `Text`, no una opinión: elegir de una lista cuesta un
gesto, escribir un correo ajeno de memoria y sin errores cuesta más y deja más rastro de intención.

**La decisión que este documento SÍ tiene, a diferencia de `ESPEC-008`:** si `MAN_Mantenimientos.
TecnicoID` deja de ser editable, ¿queda bloqueada la reasignación de un técnico a una orden? La
respuesta, verificada en el §2.7 y no supuesta, es **no**: existe una columna distinta,
`OT_OrdenesTrabajo.TecnicoID`, que es la que gobierna la asignación, no lleva `USEREMAIL()`, no está
en el alcance de este documento y sigue exactamente igual de editable después de aplicarlo. Las dos
columnas comparten nombre y no comparten mecanismo ni propósito.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

```
$ python scripts/sistema.py
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Estructura verificada contra `scripts/modelo_objetivo.py`, el archivo fuente. Población verificada
contra producción por API, sin escribir ningún archivo (§2.3): las cuatro columnas de esta
especificación viven en tres de las ocho tablas de movimiento que el volcado vacía por diseño
(`CLAUDE.md` §7.15), así que el volcado por sí solo no basta para decir "vacía de verdad".

### 2.1 El defecto, con el comando exacto del encargo

Ya mostrado en el §1. Ninguna de las cuatro tiene `editable=False` en su `col()`, y confirmado que
ninguna regla `Editable_If` las cubre hoy:

```
$ python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;print([(r['id'],r['tabla'],r.get('columna')) for r in REGLAS if r['tipo']=='Editable_If'])"
[('RG-20', 'MAN_Mantenimientos', '(varias)'), ('RG-39', 'FOT_Fotografias', 'Ubicacion_LatLong'), ('RG-40', 'NOV_Novedades', 'Ubicacion_LatLong')]
```

`RG-20`, `RG-39` y `RG-40` cubren posición (geofencing, coordenadas). Ninguna cubre identidad.

### 2.2 Dos clases de riesgo, verificadas por tipo y por obligatoriedad, no por opinión

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
for t,n in [('MAN_Mantenimientos','TecnicoID'),('NOV_Novedades','UsuarioID'),
            ('MAN_Mantenimientos','UsuarioRegistro'),('FOT_Fotografias','Usuario')]:
    c = [x for x in MODELO[t]['columnas'] if x['nombre']==n][0]
    print(t, n, c['tipo'], 'obligatoria=', c.get('obligatoria'), 'ref=', c.get('ref'))
"
MAN_Mantenimientos TecnicoID Ref obligatoria= True ref= USR_Usuarios
NOV_Novedades UsuarioID Ref obligatoria= True ref= USR_Usuarios
MAN_Mantenimientos UsuarioRegistro Text obligatoria= None ref= None
FOT_Fotografias Usuario Text obligatoria= None ref= None
```

| Columna | Tipo | Obligatoria | Clase | Por qué |
|---|---|---|---|---|
| `MAN_Mantenimientos.TecnicoID` | `Ref` | Sí | **1 — urgente** | Desplegable de un toque, y bloquea el formulario si `Editable_If` se pone sin `Initial value` (§2.9) |
| `NOV_Novedades.UsuarioID` | `Ref` | Sí | **1 — urgente** | Igual que la anterior |
| `MAN_Mantenimientos.UsuarioRegistro` | `Text` | No | **2 — mismo defecto, menor severidad** | Exige teclear un correo ajeno; si queda vacía y congelada no bloquea nada porque no es obligatoria |
| `FOT_Fotografias.Usuario` | `Text` | No | **2 — mismo defecto, menor severidad, pero sin respaldo** | Igual que la anterior, y **es la única columna de identidad que tiene `FOT_Fotografias`**: a diferencia de `MAN_Mantenimientos`, no existe una `Usuario_ID` de tipo `Ref` que la respalde |

Las cuatro comparten el defecto exacto —`USEREMAIL()`/`LOOKUP(USEREMAIL(),...)` como `Initial value`,
sin `Editable_If`— y el mismo remedio. La clase solo cambia **la severidad si el `Initial value` no
está cableado en el editor** (§2.9), no si hay que protegerlas: las cuatro se protegen, con el mismo
mecanismo, verificado más abajo que cuesta lo mismo aplicarlo a las cuatro que a dos.

### 2.3 Las tres tablas en cero filas — verificado contra producción, sin escribir ningún archivo

```
$ python scripts/verificar_app.py
...
FOT_Fotografias                   0        0
MAN_Mantenimientos                0        0
NOV_Novedades                     0        0
...
LA APLICACION VE EXACTAMENTE LO QUE EL REPOSITORIO DECLARA
```

`verificar_app.py` es de solo lectura (usa únicamente la acción `Find` de la API, verificado con
`grep -n "open(\|json.dump\|write(" scripts/verificar_app.py`, sin resultado de escritura de
archivo) — no se tocó `BD/instantaneas/`. Las tres tablas de esta especificación están en cero filas
en producción, no solo en el volcado. No hay ninguna fila real que dependa de este cambio, y no hace
falta migrar nada.

### 2.4 El parámetro `editable` del `col()` sigue siendo documental — mismo hallazgo que `ESPEC-008` §2.4, reconfirmado

```
$ grep -n '\["editable"\]\|\.get(.editable.)' scripts/*.py
scripts/generar_guia_funcional.py:442:         if c.get("editable") is False]
scripts/modelo_objetivo.py:33:def col(nombre, tipo, **kw):
```

La única lectura en tiempo de ejecución de `editable` fuera de `modelo_objetivo.py` está en
`generar_guia_funcional.py`, y es un conteo derivado (§2.8), no una instrucción de cableado. **Lo que
efectivamente cablea la instrucción de `Editable_If` para el ejecutor sigue siendo `REGLAS`**, exacto
mismo hallazgo que `ESPEC-008` §2.4 verificó para `Ubicacion_LatLong`. Las dos cosas —`editable=False`
en el `col()` y una regla en `REGLAS`— se declaran juntas en el §4, por el mismo motivo.

### 2.5 Ninguna otra columna del modelo usa `USEREMAIL()` — barrido completo, y el caso que parece pero no es

El comando del §1 ya es el barrido completo: no hay una quinta columna con `USEREMAIL()` en ningún
lado del modelo. Pero hay una columna que **comparte nombre** con una de las cuatro y que un lector
apurado podría confundir:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
for c in MODELO['OT_OrdenesTrabajo']['columnas']:
    if c['nombre'] in ('TecnicoID','SupervisorID','CerradaPor'):
        print(c['nombre'], c['tipo'], 'valor_inicial=', c.get('valor_inicial'), 'editable=', c.get('editable'))
"
TecnicoID Ref valor_inicial= None editable= None
SupervisorID Ref valor_inicial= None editable= None
CerradaPor Ref valor_inicial= None editable= None
```

`OT_OrdenesTrabajo.TecnicoID` **no** lleva `USEREMAIL()`: no tiene ningún `valor_inicial`. Es una
columna que alguien —hoy, la acción `RG-38` que crea la orden desde el plan— rellena a mano o por
mapeo explícito, no una que se autoatribuye a quien abre el formulario. **No es el mismo defecto, y
no entra en esta especificación** (desarrollado en el §2.7).

### 2.6 El generador de cableado, ya parcheado por `ORDEN-008`, sigue citando el `Initial value` de las cuatro — verificado, no supuesto

`ESPEC-008` §2.6 encontró que `generar_prompt_cableado.py` dejaba de citar el `Initial value` de una
columna en cuanto **cualquier** regla la tocaba. `ORDEN-008` lo corrigió el mismo día: el filtro
compara ahora por `(tabla, columna, tipo_de_propiedad)`, no solo por `(tabla, columna)`:

```
$ grep -n "_MAPA_TIPO_REGLA\|_cubiertas_por_tipo" scripts/generar_prompt_cableado.py
327:_MAPA_TIPO_REGLA = {"valor_inicial": "Initial value", "formula": "App formula", "valid_if": "Valid_If"}
329:_cubiertas_por_tipo = {(r["tabla"], r.get("columna"), r["tipo"]) for r in REGLAS}
```

Se predijo el cambio de este documento (§4) sobre una copia de `scripts/` y `docs/` fuera del
repositorio (mismo método que `PRUEBA-004`, `PRUEBA-007`, `PRUEBA-008`), y se regeneró
`docs/PROMPT_CABLEADO.md`. **Antes**, sobre el repositorio real, sin ningún cambio:

```
$ grep -n "TecnicoID\|UsuarioID\|UsuarioRegistro\|Usuario\b" docs/PROMPT_CABLEADO.md
...
490:| `FOT_Fotografias` | `Usuario` | `Initial value` | `USEREMAIL()` |
508:| `MAN_Mantenimientos` | `TecnicoID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
509:| `MAN_Mantenimientos` | `UsuarioRegistro` | `Initial value` | `USEREMAIL()` |
514:| `NOV_Novedades` | `UsuarioID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
```

**Después**, sobre la copia con `RG-41` a `RG-44` (§4) aplicadas, las cuatro filas siguen ahí, sin
cambiar de línea ni de contenido:

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`TecnicoID\`\|^| \`MAN_Mantenimientos\` | \`UsuarioRegistro\`\|^| \`NOV_Novedades\` | \`UsuarioID\`\|^| \`FOT_Fotografias\` | \`Usuario\`" docs/PROMPT_CABLEADO.md
490:| `FOT_Fotografias` | `Usuario` | `Initial value` | `USEREMAIL()` |
508:| `MAN_Mantenimientos` | `TecnicoID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
509:| `MAN_Mantenimientos` | `UsuarioRegistro` | `Initial value` | `USEREMAIL()` |
514:| `NOV_Novedades` | `UsuarioID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
```

**A diferencia de `ESPEC-008`, esta especificación no necesita ningún parche de código.** El parche
de `ORDEN-008` ya cubre este caso porque compara por tipo de propiedad, no por columna: da igual que
sea `Editable_If` o `Valid_If` lo que se le añada a la columna, el `Initial value` se sigue listando.
`PRUEBA-009` lo verifica como prueba de no regresión, no como un parche pendiente.

### 2.7 `OT_OrdenesTrabajo.TecnicoID` es la asignación; `MAN_Mantenimientos.TecnicoID` es la ejecución — verificado, no supuesto

Son dos columnas distintas, en dos tablas distintas, con dos mecanismos distintos:

| | `OT_OrdenesTrabajo.TecnicoID` | `MAN_Mantenimientos.TecnicoID` |
|---|---|---|
| Qué representa | A quién se le **asigna** la orden | Quién la **ejecutó**, autoatribuido |
| `valor_inicial` | Ninguno | `LOOKUP(USEREMAIL(),...)` |
| Cómo se llena hoy | La acción de `RG-38` la mapea desde `PLA_PlanMantenimiento.ResponsableID` al crear la orden (verificado en `ESPEC-006` §3.3), o se edita a mano en el formulario de la orden | Se autorrellena con quien abre el formulario de mantenimiento |
| `Editable_If` hoy | Ninguno — y esta especificación no le pone ninguno | Ninguno — y esta especificación **sí** le pone `RG-41` |
| `Are updates allowed` de la tabla | `RG-14`: `Updates, Adds` (verificado, §2.5) | No aplica a esta columna, es una regla de tabla en `OT_OrdenesTrabajo` |

**La pregunta del §1 queda resuelta, no supuesta: un supervisor sigue pudiendo reasignar una orden a
otro técnico después de aplicar esta especificación**, porque el campo que gobierna la asignación no
es ninguno de los cuatro que este documento toca. `RG-14` sigue permitiendo `Updates` sobre
`OT_OrdenesTrabajo`, y ninguna regla nueva de este documento la restringe.

**Lo que sí cambia, y es el propósito:** una vez que existe una fila de `MAN_Mantenimientos` —es
decir, una vez que alguien abrió el formulario y empezó a ejecutar—, quién queda registrado como
`TecnicoID` de esa ejecución deja de poder tocarse desde el desplegable. Si la persona que abrió el
formulario no es la persona asignada en `OT_OrdenesTrabajo.TecnicoID` —un compañero cubre una
visita, por ejemplo—, `MAN_Mantenimientos.TecnicoID` capturará correctamente a quien de verdad la
ejecutó, que es exactamente lo que la columna dice ser (`alias_justificado="Rol: quien ejecuta"`,
`scripts/modelo_objetivo.py:320`). Eso no es el defecto: el defecto es que hoy, además de capturarlo
bien al abrir, cualquiera puede cambiarlo después a cualquier otro nombre de la lista.

**No existe, y esta especificación no la crea, ninguna regla que compare
`MAN_Mantenimientos.TecnicoID` contra `OT_OrdenesTrabajo.TecnicoID`** para avisar si difieren. Sería
una decisión de producto nueva —si un compañero cubre una visita, ¿es eso una anomalía que reportar,
o una práctica normal que no hace falta señalar?— y queda fuera de alcance (§5).

### 2.8 Nueve columnas no editables tras este cambio, en tres tablas — verificado con el conteo dinámico que ya existe

`generar_guia_funcional.py` cuenta las columnas `editable=False` en tiempo de ejecución, no a mano
(corregido tras el incidente que documenta su propio comentario, líneas 432-440: un literal fijo
decía "las cuatro de captura" cuando eran tres, y luego habría dicho "tres" cuando `ESPEC-008` las
subió a cinco). Predicho sobre la misma copia del §2.6:

```
$ python scripts/generar_guia_funcional.py
$ grep -n "Las no editables" docs/GUIA_IMPLEMENTACION_FUNCIONAL.md
383:| Las no editables | `Editable_If = FALSE`. Hoy son 9, en 3 tablas: `FOT_Fotografias`, `MAN_Mantenimientos`, `NOV_Novedades` |
```

Antes de este cambio, ese mismo comando devuelve **5**, en las mismas tres tablas (`RG-20` cubre tres
columnas de `MAN_Mantenimientos`, `RG-39` una de `FOT_Fotografias`, `RG-40` una de `NOV_Novedades`).
Sube en 4, uno por cada regla nueva. No hace falta editar este generador.

`generar_manual_despliegue.py:837` tiene, en cambio, un literal fijo —"en `MAN_Mantenimientos`,
`Editable_If = FALSE` en las tres columnas de captura"— que nombra explícitamente
`Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong` y `FechaHoraEscaneo`. Se verificó que **sigue
siendo correcto** después de este cambio, porque esas tres siguen siendo exactamente las columnas de
captura geoespacial de esa tabla; `TecnicoID` y `UsuarioRegistro` son de identidad, no de captura, y
el texto no pretende ser exhaustivo sobre todas las columnas `editable=False` del modelo:

```
$ python scripts/generar_manual_despliegue.py
$ grep -n "No editables" docs/MANUAL_DESPLIEGUE.md
803:**No editables** — en `MAN_Mantenimientos`, `Editable_If = FALSE` en las tres columnas de
```

Se deja verificado y no se toca, para que quien aplique esta especificación no tenga que
redescubrirlo ni tema haber roto ese texto.

### 2.9 La pregunta honesta: ¿el editor ya tiene el `Initial value` de estas cuatro columnas puesto?

**No se sabe, y es el riesgo más caro de este documento.** El incidente reciente sobre
`FOT_Fotografias.Ubicacion_LatLong` —declaraba `HERE()` en el modelo y el editor lo tenía **vacío**,
por el mismo defecto de generador que corrigió `ORDEN-008`— confirma que "el modelo lo declara" y "el
editor lo tiene" son dos hechos distintos que hay que medir por separado. No hay, en ningún acta de
`docs/sdd/`, una lectura de `Data > Columns` sobre `TecnicoID`, `UsuarioID`, `UsuarioRegistro` ni
`Usuario`:

```
$ grep -n "TecnicoID\|UsuarioRegistro" docs/CORRECCIONES_CABLEADO.md docs/sdd/ACTA-004-lecturas-editor.md docs/sdd/ACTA-010-cotejo-ocho-tablas.md
(sin resultado en ninguno de los tres)
```

`ACTA-010` §1 dice `MAN_Mantenimientos, conforme, 14 columnas` y `NOV_Novedades, conforme, UsuarioID
sin Is a part of` — pero ese cotejo verificó **tipos** y `Is a part of`, no el contenido del `Initial
value` de cada columna, que es un campo distinto en el editor (`Auto Compute > Initial value`, no
`Data > Columns` en su vista de lista). No es evidencia de que `LOOKUP(USEREMAIL(),...)` esté puesto.

**Y mientras se escribía este documento, dejó de ser una duda teórica: `docs/sdd/ACTA-011` (sesión de
editor del 2026-08-11, en paralelo a esta investigación) midió exactamente este riesgo sobre otras
tres columnas del modelo, y salió mal en las tres.**

```
$ grep -n "Initial value" docs/sdd/ACTA-011-bloqueo-vivo-y-here-sin-senal.md | head -5
| `Initial value` | **vacío** |
| `FOT_Fotografias.PrecisionGPS` · `Initial value` | **vacío** → confirma la **Rama A** de `ESPEC-007`: la retirada fue limpia |
| `FOT_Fotografias.Ubicacion_LatLong` | **vacío** al llegar → `HERE()` + `Editable_If = FALSE` |
| `NOV_Novedades.Ubicacion_LatLong` | **vacío** al llegar → `HERE()` + `Editable_If = FALSE` |
```

`MAN_Mantenimientos.Coordenadas_Cierre_LatLong` —obligatoria, `Editable_If = FALSE` desde `RG-20`,
protegida desde `ESPEC-004`/`ORDEN-004`— tenía el `Initial value` **vacío** en el editor de
producción, pese a que el modelo lo declara. `ACTA-011` §1 lo dice sin adornos: *«Obligatoria, no
editable, y nada que la llene. Ningún técnico podía cerrar un mantenimiento: la función principal
del sistema, imposible de ejecutar. No es un riesgo teórico ni un defecto especificado — estaba
viva.»* La causa es el mismo defecto de generador que `ESPEC-008` §2.6 encontró y `ORDEN-008`
corrigió (§2.6 de este documento), pero el corte ya había ocurrido antes del parche: la instrucción
nunca llegó a `docs/PROMPT_CABLEADO.md`, y quien cableó el editor siguió el documento tal cual.

**El resultado agregado de esa sesión: de las tres columnas con `valor_inicial` declarado que se
miraron el 2026-08-11, las tres lo tenían vacío en el editor** —`Coordenadas_Cierre_LatLong`,
`PrecisionGPS` (retirada, así que su vacío confirma la Rama A limpia de `ESPEC-007`, no es una
rotura) y `Ubicacion_LatLong` de `FOT_Fotografias` y de `NOV_Novedades`—. `docs/HALLAZGOS_ABIERTOS.md`
ya lo generaliza: *«De las 3 [obligatorias y no editables] del bloqueo duro, las tres se miraron el
2026-08-11 y las tres estaban mal.»*

**Esto no demuestra que `TecnicoID`, `UsuarioID`, `UsuarioRegistro` y `Usuario` estén igual de
vacíos en el editor — nadie los ha mirado (siguen sin aparecer en ningún acta, verificado arriba).
Pero cambia lo que es razonable esperar.** Antes de `ACTA-011`, "no se sabe" era un vacío de
información neutral. Con un precedente de 3 de 3 sobre columnas del mismo mecanismo —`Initial value`
puesto en el modelo, nunca confirmado contra el editor—, la hipótesis de trabajo razonable es que el
editor **tampoco** tiene puesto el `LOOKUP(USEREMAIL(),...)` de `TecnicoID`/`UsuarioID` ni el
`USEREMAIL()` de `UsuarioRegistro`/`Usuario`, no lo contrario.

**Por qué esto es más grave aquí que en `ESPEC-008`, y ahora con precedente medido, no solo
argumentado:** dos de las cuatro columnas —`TecnicoID` y `UsuarioID`— son `obligatoria=True`, igual
que `Coordenadas_Cierre_LatLong` lo era cuando quedó bloqueada en producción. Si el editor no tiene
el `Initial value` puesto y se aplica `Editable_If = FALSE` de todos modos, la columna queda
**obligatoria, no editable y vacía**, y **ningún técnico puede guardar un mantenimiento ni una
novedad** — el mismo bloqueo que `ACTA-011` §1 encontró ya ocurrido, no un riesgo hipotético, sobre
dos formularios centrales de la operación. Las otras dos —`UsuarioRegistro` y `Usuario`— no son
obligatorias: si les falta el `Initial value`, el resultado es un campo vacío y congelado, no un
formulario bloqueado.

**El orden de cableado, por tanto, no es una preferencia: es la condición para no repetir, por
tercera y cuarta vez, un bloqueo que ya ocurrió una vez y que no fue teórico.** Leer primero `Auto
Compute > Initial value` de las cuatro columnas; si falta, ponerlo antes que `Update Behavior >
Editable?`. Y con una salvedad de método que `ACTA-011` §1 deja escrita para quien haga esa sesión:
**escribir un `Initial value` en el editor de producción es una escritura, no una lectura, y no se
autoriza por deducción** —en `ACTA-011` la hizo el coordinador de la sesión sin que el encargo la
cubriera, y aunque cerró un bloqueo real, el propio acta registra que el orden correcto era
consultarlo primero—. Se resuelve en la misma sesión de editor ya encolada por `ORDEN-004` §6,
`ORDEN-006` §6, `ESPEC-007` §5-§6 y `ESPEC-008` §6/`PRUEBA-008` `P-75`, con autorización explícita
para escribir, no solo para leer.

### 2.10 `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` sí propaga `descripcion` — el hallazgo abierto está superado, verificado

`docs/HALLAZGOS_ABIERTOS.md` registra hoy que `generar_reconstruccion.py` no lee
`r["descripcion"]`, con `grep -c descripcion scripts/generar_reconstruccion.py` → `0` como evidencia.
Se repitió el comando contra el repositorio real, hoy:

```
$ grep -c descripcion scripts/generar_reconstruccion.py
4
```

**El hallazgo está superado: alguien lo corrigió después de escribirlo, sin actualizar la entrada.**
Se confirmó además contra la fuente, no solo contra el conteo:

```
$ grep -A6 "RG-39" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
### RG-39 — `FOT_Fotografias` · `Ubicacion_LatLong`
...
> Mismo mecanismo que RG-20: HERE() es Initial value, no App formula, y un Initial value SI es
  editable. ... CABLEAR DESPUES del Initial value = HERE() ... ESPEC-008.
```

La descripción sí aparece. Esto importa para este documento porque `RG-41` a `RG-44` (§4) llevan la
misma instrucción "CABLEAR DESPUES del Initial value" dentro de `descripcion`, con el mismo
razonamiento que `ESPEC-008` §4 fijó: **si la advertencia solo viviera en la prosa de esta
especificación, no llegaría a quien cablea.** Verificado con la copia del §2.6:

```
$ grep -A9 "### RG-41" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
### RG-41 — `MAN_Mantenimientos` · `TecnicoID`
...
> LOOKUP(USEREMAIL(),...) es Initial value ... CABLEAR DESPUES del Initial value = LOOKUP(...) ...
  No congela OT_OrdenesTrabajo.TecnicoID ... ESPEC-009.
```

Llega. Se corrige la entrada de `docs/HALLAZGOS_ABIERTOS.md` (fuera de `docs/sdd/`, no forma parte
de las dos entregas de esta especificación) marcándola resuelta, con este mismo comando.

## 3. Qué cambia exactamente

| Tabla.Columna | Estado actual | Estado objetivo |
|---|---|---|
| `MAN_Mantenimientos.TecnicoID` | `Ref` a `USR_Usuarios`, obligatoria, `Initial value = LOOKUP(USEREMAIL(),...)`, sin `Editable_If` | Igual, más `editable=False` en el `col()` y cubierta por `RG-41` |
| `NOV_Novedades.UsuarioID` | `Ref` a `USR_Usuarios`, obligatoria, `Initial value = LOOKUP(USEREMAIL(),...)`, sin `Editable_If` | Igual, más `editable=False` en el `col()` y cubierta por `RG-42` |
| `MAN_Mantenimientos.UsuarioRegistro` | `Text`, no obligatoria, `Initial value = USEREMAIL()`, sin `Editable_If` | Igual, más `editable=False` en el `col()` y cubierta por `RG-43` |
| `FOT_Fotografias.Usuario` | `Text`, no obligatoria, `Initial value = USEREMAIL()`, sin `Editable_If` | Igual, más `editable=False` en el `col()` y cubierta por `RG-44` |

Ninguna otra columna, tabla ni referencia cambia. `OT_OrdenesTrabajo.TecnicoID` **no** se toca (§2.7).
`REGLAS` pasa de 23 a 27 entradas. Ninguna tabla gana ni pierde columnas: `MODELO` sigue en 209
columnas.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, en dos puntos. No hace falta editar ningún generador (§2.6).

- **`MODELO["MAN_Mantenimientos"]["columnas"]`** (línea 320-321): añadir `editable=False` al `col()`
  de `TecnicoID`:

  ```python
  col("TecnicoID", "Ref", ref="USR_Usuarios", obligatoria=True, alias_justificado="Rol: quien ejecuta",
      valor_inicial='LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")', editable=False),
  ```

- **`MODELO["MAN_Mantenimientos"]["columnas"]`** (línea 354): añadir `editable=False` al `col()` de
  `UsuarioRegistro`:

  ```python
  col("UsuarioRegistro", "Text", valor_inicial="USEREMAIL()", editable=False),
  ```

- **`MODELO["NOV_Novedades"]["columnas"]`** (línea 367-368): añadir `editable=False` al `col()` de
  `UsuarioID`:

  ```python
  col("UsuarioID", "Ref", ref="USR_Usuarios", obligatoria=True,
      valor_inicial='LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")', editable=False),
  ```

- **`MODELO["FOT_Fotografias"]["columnas"]`** (línea 431): añadir `editable=False` al `col()` de
  `Usuario`:

  ```python
  col("Usuario", "Text", valor_inicial="USEREMAIL()", editable=False),
  ```

- **`REGLAS`**: añadir cuatro entradas nuevas, siguiente identificador libre `RG-41`
  (`sorted(int(r['id'].split('-')[1]) for r in REGLAS)` da `... 39, 40`, verificado en el §2.1 de
  este documento con `RG-40` como último). Se declaran como reglas hermanas de `RG-20`/`RG-39`/
  `RG-40`, no como su extensión, por el mismo motivo que fijó `ESPEC-008` §2.2: el esquema de
  `REGLAS` ata cada entrada a una sola tabla:

  ```python
  dict(id="RG-41", tabla="MAN_Mantenimientos", columna="TecnicoID",
       tipo="Editable_If", cubre="Prueba de identidad",
       expresion="FALSE",
       descripcion=("LOOKUP(USEREMAIL(),...) es Initial value, no App formula, y un Initial "
                    "value SI es editable: TecnicoID se dibuja como desplegable de USR_Usuarios "
                    "sin filtrar, y con un toque el tecnico logueado puede atribuir la ejecucion "
                    "a otro companero. CABLEAR DESPUES del Initial value = LOOKUP(...): al reves "
                    "la columna queda obligatoria, no editable y vacia, y ningun tecnico puede "
                    "guardar el mantenimiento. No congela OT_OrdenesTrabajo.TecnicoID (asignacion, "
                    "columna distinta, sin Initial value, fuera de alcance): un supervisor sigue "
                    "reasignando la orden sin verse afectado por esta regla. ESPEC-009.")),
  dict(id="RG-42", tabla="NOV_Novedades", columna="UsuarioID",
       tipo="Editable_If", cubre="Prueba de identidad",
       expresion="FALSE",
       descripcion=("Mismo mecanismo que RG-41, sobre quien reporta la novedad. Sin esto un "
                    "tecnico elige a otro companero en el desplegable y el hallazgo queda "
                    "atribuido a quien no lo reporto. CABLEAR DESPUES del Initial value = "
                    "LOOKUP(...): la columna es obligatoria, al reves el formulario de "
                    "novedades no se puede guardar. ESPEC-009.")),
  dict(id="RG-43", tabla="MAN_Mantenimientos", columna="UsuarioRegistro",
       tipo="Editable_If", cubre="Prueba de identidad",
       expresion="FALSE",
       descripcion=("Mismo mecanismo que RG-41 sobre un campo de texto en vez de un Ref: "
                    "USEREMAIL() es Initial value y por tanto editable a mano. No es "
                    "obligatoria, asi que si el Initial value no estuviera cableado el riesgo es "
                    "un campo vacio y congelado, no un formulario bloqueado. CABLEAR DESPUES "
                    "del Initial value = USEREMAIL(), mismo orden por consistencia. ESPEC-009.")),
  dict(id="RG-44", tabla="FOT_Fotografias", columna="Usuario",
       tipo="Editable_If", cubre="Prueba de identidad",
       expresion="FALSE",
       descripcion=("Mismo mecanismo que RG-43, sobre quien tomo la fotografia. A diferencia de "
                    "MAN_Mantenimientos, FOT_Fotografias no tiene ninguna columna Ref de "
                    "respaldo: este campo de texto es la unica captura de identidad de la tabla. "
                    "No es obligatoria. CABLEAR DESPUES del Initial value = USEREMAIL(). "
                    "ESPEC-009.")),
  ```

  **La instrucción de orden va dentro de `descripcion`, no solo en esta prosa**, por el motivo que
  `ESPEC-008` §4 fijó y que el §2.10 de este documento reconfirma: `descripcion` se propaga a
  `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, `docs/PROMPT_EXPRESIONES.md` y
  `docs/ARQUITECTURA_OBJETIVO_SGMC.md`; la prosa de una especificación, no.

  No se modifican `RG-20`, `RG-39` ni `RG-40`: siguen cubriendo exactamente las mismas columnas que
  hoy.

No se toca `CAMPOS_RETIRADOS`, `RETIRADAS`, `RETIPADOS`, `RENOMBRADOS`, `PARAMETROS`, `DECISIONES`, ni
ninguna columna ni regla de `OT_OrdenesTrabajo` (§2.7). No se retira ni se retipa ninguna columna:
`MODELO` sigue en 209 columnas.

**Documentos que se re-emiten** con los comandos de siempre, una vez editado
`scripts/modelo_objetivo.py`: `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`,
`docs/PROMPT_CABLEADO.md`, `docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`, `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md`. Todos derivan de
`REGLAS` en tiempo de ejecución (§2.6, §2.8, §2.10); ninguno necesita edición manual de contenido.
`docs/MANUAL_DESPLIEGUE.md` se re-emite igual, aunque su literal fijo de la línea 837 no cambie
(§2.8): regenerarlo no lo rompe, y dejarlo desactualizado frente al resto de documentos sí sería un
defecto.

**No hace falta regenerar `BD/Modelo_Datos_PLANTILLA.xlsx`.** Mismo argumento que `ESPEC-008` §4:
`editable=False` y las reglas `Editable_If` no tienen representación en la cabecera del Excel —
verificado con `grep -n "editable" scripts/generar_plantilla.py scripts/verificar_faseA.py`, sin
resultado — y confirmado corriendo `verificar_faseA.py` sobre la copia con el cambio aplicado: mismos
`AVISOS (2)` que sin él (§2.8, evidencia completa en `PRUEBA-009`).

## 5. Qué NO cubre esta especificación

- **No toca `OT_OrdenesTrabajo.TecnicoID`.** Es la asignación de la orden, no la ejecución del
  mantenimiento; verificado en el §2.7 que es una columna distinta, sin `USEREMAIL()`, sin
  `Editable_If` hoy y sin que este documento le añada ninguno. Un supervisor la sigue editando
  exactamente igual que antes.
- **No añade ninguna regla que compare `MAN_Mantenimientos.TecnicoID` contra
  `OT_OrdenesTrabajo.TecnicoID`** para señalar cuando el que ejecutó no es el que estaba asignado
  (§2.7). Sería una decisión de producto nueva —si eso es una anomalía que reportar o una práctica
  normal—, y esta especificación no la toma.
- **No añade ninguna vía de corrección dentro de la aplicación** para el caso en que la
  autoatribución quede mal —por ejemplo, alguien abre el formulario en el dispositivo de otra
  persona por error—. Se declara como supuesto en el §7, con el mismo criterio que `ESPEC-008`
  aceptó para el GPS no disponible: la corrección, si hace falta, se hace a mano en el Sheets, no en
  la app.
- **No decide si `MAN_Mantenimientos.UsuarioRegistro` debería retirarse en vez de congelarse.** Es
  una columna `Text` que no lee ninguna regla y que duplica, en texto plano, lo que
  `MAN_Mantenimientos.TecnicoID` ya guarda como referencia estructurada (§2.2). Retirarla —como
  `ESPEC-007` hizo con `PrecisionGPS`— sería una decisión de diseño distinta, de menor urgencia que
  proteger la identidad: hoy el defecto es que se puede editar, no que sea redundante. Queda anotado,
  no perseguido.
- **No confirma en el editor si las cuatro columnas ya tienen `Initial value` puesto** (§2.9).
  Necesita sesión de navegador. Es el riesgo más caro de este documento y se declara en el §6, no se
  resuelve aquí.
- **No repite ni reabre `ESPEC-004`, `ESPEC-007` ni `ESPEC-008`.** No hay dependencia de mecanismo ni
  de estado con ninguna de las tres (§6).
- **No corrige `docs/HALLAZGOS_ABIERTOS.md` dentro de `docs/sdd/`.** La corrección del §2.10 se
  aplica sobre `docs/HALLAZGOS_ABIERTOS.md`, que vive fuera de esa carpeta.

## 6. Riesgos y dependencias

**Antes de la lista, el límite de lo que esto garantiza, porque es fácil leerlo de más.**
`Editable_If = FALSE` es una regla de **la capa de aplicación**: impide que un técnico cambie la
identidad **desde la app**. Las dos cuentas con permiso de edición sobre `Modelo_Datos_10082026`
pueden reescribir `TecnicoID` **directamente en el Sheets** y la prueba de identidad desaparece
sin dejar rastro.

La identidad queda **inviolable en la app, no en el backend**. Este documento menciona esa
edición manual más abajo como el **remedio** de una autoatribución equivocada —y lo es—, pero es
también **el agujero de la garantía**, y las dos cosas son la misma puerta. Es el mismo límite que
`ESPEC-004` §2.14 declara para `RG-03`: no se resuelve aquí, se nombra.

- **No se sabe si `TecnicoID`, `UsuarioID`, `UsuarioRegistro` o `Usuario` ya tienen algo cableado en
  el editor de producción** (§2.9). Es el mismo riesgo que `ESPEC-008` §6 nombró para
  `Ubicacion_LatLong`, y ya no es hipotético: `docs/sdd/ACTA-011` midió, el mismo día, tres columnas
  con `valor_inicial` declarado en el modelo y encontró las **tres** vacías en el editor, una de
  ellas —`Coordenadas_Cierre_LatLong`, obligatoria— **bloqueando en producción el cierre de
  mantenimientos**. Sube de "riesgo sin medir" a "riesgo con precedente de 3 de 3", agravado aquí
  porque dos de las cuatro columnas de este documento —`TecnicoID` y `UsuarioID`— son obligatorias
  igual que la que ya se bloqueó: si el `Initial value` falta y se aplica `Editable_If = FALSE` de
  todos modos, el formulario de mantenimiento o el de novedad queda **imposible de guardar**, no solo
  desprotegido. **Antes de tocar nada en el editor**, la sesión de navegador debe leer `Data >
  Columns > [tabla] > [columna] > Auto Compute > Initial value` de las cuatro, en ese orden: primero
  confirmar que el valor está puesto, después aplicar `Update Behavior > Editable?`. Si alguna lo
  tiene vacío, ponerlo antes de congelar esa columna en particular — el resto puede seguir su curso.
  Y con la salvedad de método que `ACTA-011` §1 registró sobre sí misma: escribir un `Initial value`
  en producción es una escritura y se autoriza, no se deduce a mitad de otra sesión.
- **No hay ninguna vía de corrección dentro de la app si la autoatribución queda mal** (§5, §7).
  Aceptado como el mismo tipo de riesgo que `ESPEC-008` aceptó para el GPS no disponible: la reversión
  —quitar `Editable_If` en el editor, o corregir el dato a mano en el Sheets— cuesta lo mismo con o
  sin esta especificación.
- **No depende de `ESPEC-004`, `ESPEC-007` ni `ESPEC-008`.** Se verificó aplicando solo el cambio de
  este documento sobre una copia: `validar_modelo.py` da `209` columnas y `27` reglas, sin errores
  nuevos, con exactamente los mismos tres avisos que hoy (evidencia completa en `PRUEBA-009`). Si
  `ESPEC-007` se aplica antes o después, `FOT_Fotografias` pierde `PrecisionGPS`, sin relación de
  mecanismo con `RG-44`. Si `ESPEC-008` se aplica antes o después, `FOT_Fotografias.Ubicacion_LatLong`
  y `NOV_Novedades.Ubicacion_LatLong` quedan protegidas por `RG-39`/`RG-40`, sin relación de mecanismo
  con `RG-41` a `RG-44`: son columnas distintas en las mismas tablas.
- **Sin datos que migrar** (§2.3, verificado contra producción sin escribir archivo). Revertir esta
  especificación, en cualquier momento antes de la primera fila real de las tres tablas, cuesta quitar
  cuatro entradas de `REGLAS` y cuatro parámetros de cuatro `col()`.
- **Qué se rompe si el supuesto del §7 sobre `OT_OrdenesTrabajo.TecnicoID` fuera falso:** si algún día
  se decide que "quien ejecuta" debe derivarse siempre de "quien está asignado" —en vez de
  autoatribuirse por `LOOKUP(USEREMAIL(),...)`—, el `valor_inicial` correcto de
  `MAN_Mantenimientos.TecnicoID` pasaría a ser algo como `[OTID].[TecnicoID]`, no
  `LOOKUP(USEREMAIL(),...)`. Ese cambio es independiente de si la columna está congelada o no: el
  costo de reabrirlo es el mismo con o sin esta especificación aplicada.

## 7. Supuestos adoptados

- **Que una columna `Ref` se dibuja como un selector desplegable, y por eso es más explotable que
  una `Text`.** Es el supuesto sobre el que descansa toda la jerarquía de este documento —dos
  columnas de clase 1, dos de clase 2— y estaba declarado en la prosa del §1 **sin subir a esta
  tabla**, que es donde se le mira la cara a un supuesto. **Qué lo rompe:** que AppSheet dibuje un
  `Ref` de otra forma en el formulario —un campo de texto con autocompletado, por ejemplo—, en cuyo
  caso las cuatro columnas son igual de explotables y el orden de prioridad da lo mismo. **Qué tan
  barato es reabrirlo:** no cambia la decisión —las cuatro se protegen igual—, solo el argumento de
  por qué dos urgen más. Y **se mide mirando un formulario**, no hay que preguntarle a nadie.

- **Se adopta que `MAN_Mantenimientos.TecnicoID` (ejecución) y `OT_OrdenesTrabajo.TecnicoID`
  (asignación) son conceptos distintos y que esta especificación solo congela el primero.**
  Verificado en el §2.7: mecanismos distintos, sin relación declarada entre ambos. **Qué lo rompe:**
  que el negocio decida que "quien ejecuta" debe heredar siempre de "quien está asignado", en vez de
  autoatribuirse. **Qué tan barato es reabrirlo:** cambiar el `valor_inicial` de
  `MAN_Mantenimientos.TecnicoID`, un cambio de fórmula sin relación con que la columna esté congelada
  o no — el costo es el mismo antes y después de esta especificación.
- **Se adopta que no hace falta ninguna vía de corrección dentro de la aplicación para una
  autoatribución equivocada** (§5, §6), con el mismo criterio que `ESPEC-008` §2.9 aceptó para el GPS
  no disponible. **Qué lo rompe:** que ocurra con frecuencia suficiente como para que editar en el
  Sheets sin dejar traza clara de quién corrigió qué deje de ser aceptable, y haga falta una acción
  auditable dentro de la app. **Qué tan barato es cerrarlo:** las tres tablas están en cero filas
  (§2.3), así que no hay nada que reconciliar; el costo es diseñar la acción, no deshacer datos.
- **Se adopta proteger las cuatro columnas con el mismo mecanismo, en la misma especificación, en vez
  de separar las dos `Ref` (clase 1) de las dos `Text` (clase 2) en dos entregas.** El costo de
  declarar las cuatro reglas es el mismo que declarar dos (§4), y fragmentarlo no reduce el riesgo del
  §2.9, que depende de la sesión de editor, no del número de columnas por especificación. **Qué lo
  rompe:** que la sesión de editor solo alcance a verificar el `Initial value` de dos columnas por
  vez. **Qué tan barato es reabrirlo:** cablear las dos `Ref` primero —mayor severidad si el
  formulario se bloquea— y dejar las dos `Text` para una segunda sesión es válido sin tocar este
  documento ni escribir uno nuevo: las cuatro reglas ya están declaradas y verificadas.
- **Se adopta no decidir aquí si `MAN_Mantenimientos.UsuarioRegistro` debería retirarse por
  redundante** (§5), en vez de congelarse junto con las otras tres. **Qué lo rompe:** que alguien
  priorice reducir columnas muertas del modelo sobre proteger identidad, y decida que retirarla es
  más urgente que congelarla. **Qué tan barato es reabrirlo:** la tabla está en cero filas (§2.3);
  retirarla después de congelarla cuesta lo mismo que retirarla antes, con la diferencia de que si se
  congela primero, revertir es una línea menos que gestionar mientras se decide.

---

## 8. Cierre — qué se acepta como riesgo, y qué no entra aquí

**APROBADA CON RIESGOS ACEPTADOS el 2026-08-11**, en primera pasada. Las **seis condiciones** del
dictamen están aplicadas: el paso 0 de `P-83` —comprobar que el correo de quien prueba esté en
`USR_Usuarios`—, su tercera comprobación reescrita para una tabla en 0 filas, el discriminante
entre las dos causas de un campo vacío, el límite de la garantía en §6, el supuesto del `Ref` como
selector subido a §7, y este cierre.

El arquitecto reprodujo las cuatro afirmaciones de carga por su cuenta —no las leyó—, incluida la
que sostiene el documento entero: que `OT_OrdenesTrabajo.TecnicoID` es otra columna y la
reasignación no se rompe. Y revirtió él mismo el parche de `ORDEN-008` para comprobar que `P-80`
falla de verdad.

### Riesgos aceptados

1. **2026-08-11 — El `LOOKUP` puede devolver vacío aunque el `Initial value` esté perfecto.**
   `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` no encuentra nada si el correo
   logueado no está en la tabla, y entonces `TecnicoID` —obligatoria— queda vacía y congelada: **no
   se puede guardar un mantenimiento**. Es una **segunda vía al mismo bloqueo** que el orden de
   cableado no cubre. Lo encontró el arquitecto y se verificó contra los datos el mismo día: la
   cuenta dueña de la aplicación no estaba en `USR_Usuarios`. **Se acepta** porque `P-83` ahora
   lo comprueba antes de nada y porque añadir un correo cuesta una fila.

2. **2026-08-11 — La garantía vive solo en la aplicación.** Dos cuentas pueden reescribir la
   identidad directamente en el Sheets (§6). Aceptado, no resuelto — mismo criterio que
   `ESPEC-004` §2.14 para `RG-03`.

3. **2026-08-11 — El dato de identidad se guarda dos veces y puede divergir sin arreglo.**
   `MAN.TecnicoID` (`Ref`) y `MAN.UsuarioRegistro` (`Text`) registran el mismo hecho, y congeladas
   las dos pueden separarse de forma permanente **justo cuando el `LOOKUP` falla y `USEREMAIL()`
   no**. El arquitecto lo señaló como argumento **a favor** de conservar `UsuarioRegistro`, contra
   su candidatura a retiro del §5: es el registro en crudo que sobrevive al `LOOKUP` fallido.

4. **2026-08-11 — `FIR_Firmas` no tiene columna de identidad propia.** Quién firmó se deriva por
   `MantenimientoID` → `MAN_Mantenimientos.TecnicoID`, así que **`RG-41` es lo único que protege la
   identidad de la firma**. Se acepta y se nombra: refuerza el cambio y deja el hueco identificado.

5. **2026-08-11 — El `alias_justificado` de `OT_OrdenesTrabajo.TecnicoID` dice «quien ejecuta»** y
   este documento lo trata como «a quién se asigna». El argumento **mecánico** —sin `valor_inicial`,
   sin `Editable_If`, y `RG-38` la mapea desde `PLA_PlanMantenimiento.ResponsableID`— está verificado
   y no depende del alias. Corregir el alias queda para una pasada futura.

### Lo que un dictamen tenía que mirar, y miró

1. **El riesgo del §2.9 es real y tiene precedente medido, no solo argumentado.** `TecnicoID` y
   `UsuarioID` son obligatorias; si su `Initial value` no está cableado en el editor de producción y
   se aplica `Editable_If = FALSE` de todos modos, el formulario de mantenimiento o el de novedad
   queda imposible de guardar — lo que le ocurrió de verdad a `Coordenadas_Cierre_LatLong` el
   2026-08-11, según `docs/sdd/ACTA-011`, con las tres columnas medidas ese día vacías en el editor
   pese a declarar `valor_inicial` en el modelo. La comprobación cuesta una lectura de `Data >
   Columns`, en la misma sesión ya encolada por `ESPEC-008` §6, pero no se ha hecho sobre las cuatro
   columnas de este documento. Dado el precedente de 3 de 3, un dictamen podría considerar que esa
   lectura deja de ser opcional antes de aprobar la aplicación de `RG-41`/`RG-42` en particular.
2. **El supuesto de que basta con no crear ninguna vía de corrección dentro de la app** (§7) no está
   contrastado contra ninguna política de operación escrita: se adopta por el mismo criterio que
   `ESPEC-008` aceptó para el GPS, no porque exista una decisión explícita sobre identidad.
3. **La distinción entre `MAN_Mantenimientos.TecnicoID` y `OT_OrdenesTrabajo.TecnicoID`** (§2.7) es
   la pieza central de este documento: si el dictamen la encuentra insuficiente —por ejemplo, si
   decide que también hace falta una regla que compare ambas columnas—, ese es un alcance mayor que
   el que aquí se propuso, y quedaría para una especificación aparte o para ampliar esta antes de
   aplicarla.
4. **`MAN_Mantenimientos.UsuarioRegistro` es candidata a retiro, no solo a protección** (§5, §7): el
   dictamen podría preferir retirarla en vez de congelarla, dado que ningún consumidor la lee y
   duplica `TecnicoID`.

### Lo que NO entra aquí, y queda nombrado para quien decida el siguiente paso

**No existe ninguna regla que compare `MAN_Mantenimientos.TecnicoID` contra
`OT_OrdenesTrabajo.TecnicoID`** para detectar cuándo quien ejecutó no es quien estaba asignado
(§2.7). Es una decisión de producto —si eso merece señalarse o es una práctica operativa normal— y no
la toma este documento.

**No hay ninguna vía, dentro de la aplicación, para corregir una autoatribución equivocada** una vez
congelada (§5, §6). La corrección, si hace falta, es editar el dato a mano en el Sheets, con las
cuentas que ya tienen ese permiso hoy — el mismo residuo que `docs/HALLAZGOS_ABIERTOS.md` ya nombra
para la cascada de borrado: un cambio a mano en la hoja no queda tan trazado como un cambio dentro de
la aplicación.

**`docs/HALLAZGOS_ABIERTOS.md` tiene una entrada superada** (§2.10): la que dice que
`generar_reconstruccion.py` no propaga `descripcion` ya no es cierta, verificado con
`grep -c descripcion scripts/generar_reconstruccion.py` → `4`. Se corrige en ese archivo, fuera de
`docs/sdd/`, como parte del cierre de esta especificación.
