# ESPEC-008 — Proteger `FOT_Fotografias.Ubicacion_LatLong` con `Editable_If`

## 0. Por qué este documento es corto, y por qué eso es la conclusión y no un atajo

El mecanismo que hace falta ya existe, ya está **cableado y verificado por lectura de vuelta** en
producción —no *probado*: `MAN_Mantenimientos` tiene 0 filas, así que nunca se guardó una por ese
formulario (§2.3)— y no exige ninguna decisión de
producto: `RG-20` resolvió exactamente este defecto para tres columnas de `MAN_Mantenimientos` en
`ESPEC-004`/`ORDEN-004`, y `ACTA-004` §1 confirma que `Coordenadas_Cierre_LatLong.Editable_If` **ya
está en `FALSE` en el editor de producción**. Aquí no hay que inventar el candado, hay que ponerlo en
la segunda cerradura que quedó sin él. El §2.5 verifica que ninguna otra columna de `FOT_Fotografias`
está en la misma situación, y el §2.6 encuentra el único obstáculo real: un generador que, al añadir
la regla, deja de emitir la instrucción de `Initial value` para la misma columna — un defecto de
código preexistente que este documento no introduce pero que expone y que hay que corregir antes de
regenerar `docs/PROMPT_CABLEADO.md`, o el remedio deja el formulario de fotografías inutilizable.

## 1. Qué se quiere y por qué

`scripts/modelo_objetivo.py:424` declara `FOT_Fotografias.Ubicacion_LatLong` como `LatLong`,
obligatoria, con `HERE()` como `Initial value`, y **sin ningún parámetro `editable=False` ni ninguna
regla `Editable_If` que la cubra** — verificado en el §2.1 con el comando exacto del encargo. Un
`Initial value` se evalúa una sola vez y después es editable por defecto: en un formulario de
AppSheet, un `LatLong` sin `Editable_If` se dibuja como un pin arrastrable sobre un mapa. La nota de
la propia columna dice que esa coordenada **es** la evidencia, porque la compresión a 600 px descarta
el EXIF de la fotografía — no hay una segunda fuente que la contradiga si alguien la mueve.

La decisión que este documento permite tomar: **¿se cierra esa vía de edición, con el mismo mecanismo
que ya cierra la de `MAN_Mantenimientos`, o se deja abierta?** No hay una alternativa de producto que
evaluar — que la evidencia no se pueda mover a mano es el propósito del sistema, no una preferencia —,
así que lo único que decide este documento es **cómo se declara** el cierre y **qué más se rompe** al
declararlo (§2.6).

Sin este documento, cualquier fotografía que entre a `FOT_Fotografias` puede registrarse con una
coordenada distinta de donde se tomó, sin que ninguna regla lo impida ni lo señale.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

```
$ python scripts/sistema.py
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026 (fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Estructura verificada contra `scripts/modelo_objetivo.py` y contra el volcado local. Población
verificada además contra producción por API (§2.3), no solo contra el volcado — `FOT_Fotografias` es
una de las ocho tablas que `generar_plantilla.py` vacía por diseño (`CLAUDE.md` §7.15), así que el
volcado sale vacío la escriba quien la escriba; solo la lectura por API distingue "vacía de verdad" de
"vacía porque el instrumento no puede ver lo que hay".

**`ESPEC-007` está aprobada con riesgos aceptados pero no aplicada** (no existe `ORDEN-007` ni
`ACTA-007` en `docs/sdd/`, comprobado listando el directorio): `scripts/modelo_objetivo.py` todavía
declara `FOT_Fotografias.PrecisionGPS` con `valor_inicial="USERLOCATIONACCURACY()"`, `RG-20` todavía
cubre tres columnas y `REGLAS` todavía tiene 21 entradas. Este documento se verifica contra ese
estado, el real, no contra el que `ESPEC-007` propone.

### 2.1 El defecto, verificado con el comando del encargo

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,REGLAS
print([(t,c['nombre']) for t in MODELO for c in MODELO[t]['columnas'] if c.get('editable') is False])
print([(r['id'],r['tabla'],r.get('columna')) for r in REGLAS if r['tipo']=='Editable_If'])
"
[('MAN_Mantenimientos', 'UbicacionEscaneo_LatLong'), ('MAN_Mantenimientos', 'FechaHoraEscaneo'), ('MAN_Mantenimientos', 'Coordenadas_Cierre_LatLong')]
[('RG-20', 'MAN_Mantenimientos', '(varias)')]
```

`FOT_Fotografias.Ubicacion_LatLong` no aparece en ninguna de las dos listas. `RG-20` es la única
regla `Editable_If` del modelo y cubre solo tres columnas, las tres de `MAN_Mantenimientos`. Ninguna
columna de `FOT_Fotografias` lleva `editable=False` en su `col()`:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
for c in MODELO['FOT_Fotografias']['columnas']:
    print(c['nombre'], c['tipo'], 'obligatoria=', c.get('obligatoria'), 'valor_inicial=', c.get('valor_inicial'), 'editable=', c.get('editable'))
"
FotoID Text obligatoria= None valor_inicial= None editable= None
MantenimientoID Ref obligatoria= True valor_inicial= None editable= None
Tipo Enum obligatoria= True valor_inicial= None editable= None
Archivo Image obligatoria= True valor_inicial= None editable= None
Ubicacion_LatLong LatLong obligatoria= True valor_inicial= HERE() editable= None
PrecisionGPS Number obligatoria= None valor_inicial= USERLOCATIONACCURACY() editable= None
FechaHora ChangeTimestamp obligatoria= None valor_inicial= None editable= None
Usuario Text obligatoria= None valor_inicial= None editable= None
```

`Ubicacion_LatLong` es la única columna de la tabla con `HERE()` como `Initial value` sobre un tipo
`LatLong`. En el editor de AppSheet un `LatLong` así declarado se dibuja como un pin arrastrable
(`docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` §7.1, mismo mecanismo documentado para `RG-20`), y nada en el
modelo impide moverlo.

### 2.2 `RG-20`, leída completa, para no reinventar lo que ya explica

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS
r = next(x for x in REGLAS if x['id']=='RG-20')
print(r['tabla'], r['columna'], r['tipo'], repr(r['expresion']))
print(r['descripcion'])
"
MAN_Mantenimientos (varias) Editable_If 'FALSE'
Sobre Coordenadas_Cierre, UbicacionEscaneo y FechaHoraEscaneo (tres columnas desde ESPEC-004/ORDEN-004:
Precision_GPS se retiro del modelo, ver CAMPOS_RETIRADOS). SIN ESTO EL GEOFENCING ES DECORATIVO:
HERE() es Initial value, no App formula, y un Initial value SI es editable. Coordenadas_Cierre es un
LatLong, que en un formulario AppSheet dibuja como un pin arrastrable sobre un mapa, y la ubicacion
del activo esta visible en la app: el tecnico arrastra el pin encima del activo y RG-01 valida sin
protestar. La regla se cumplia y la presencia no quedaba probada.
```

`RG-20.expresion` es el literal `"FALSE"`, y `RG-20.tabla` es una cadena única
(`"MAN_Mantenimientos"`) — el esquema de `REGLAS` ata cada entrada a **una** tabla. Confirmado en
`scripts/validar_modelo.py:130`, la comprobación `V-10`:

```
$ grep -n "columna.*not in" scripts/validar_modelo.py
    elif r["columna"] not in ("(tabla)", "(varias)"):
```

`r["tabla"]` se usa como valor único en todo `validar_modelo.py` (línea 128: `if r["tabla"] not in
MODELO`), nunca como colección. **Extender literalmente `RG-20` para que además cubra
`FOT_Fotografias` no encaja en el esquema**: la vía que sí encaja, y que ya usan `RG-01`/`RG-16`/etc.
para "una tabla, una columna, un mecanismo compartido", es una regla hermana con la misma expresión y
el mismo tipo. Se declara así en el §4.

### 2.3 `FOT_Fotografias` en cero filas — verificado en el volcado y en producción

```
$ python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
ws = wb['FOT_Fotografias']
rows = list(ws.iter_rows(values_only=True))
print('encabezado', rows[0]); print('filas de datos', len(rows)-1)
"
encabezado ('FotoID', 'MantenimientoID', 'Tipo', 'Archivo', 'Ubicacion_LatLong', 'PrecisionGPS', 'FechaHora', 'Usuario')
filas de datos 0
```

Y contra producción, por API, no contra el volcado (`CLAUDE.md` §7.15: el volcado vacía las ocho
tablas de movimiento por diseño, así que por sí solo no basta para afirmar "vacía de verdad"):

```
$ python scripts/instantanea.py guardar chequeo-espec008
Guardada: BD/instantaneas/chequeo-espec008.json
28 tablas · 953 filas en total

$ python -c "
import json
d = json.load(open('BD/instantaneas/chequeo-espec008.json', encoding='utf-8'))
for t in ['FOT_Fotografias','NOV_Novedades','FIR_Firmas','MAN_Mantenimientos']:
    print(t, len(d[t]))
"
FOT_Fotografias 0
NOV_Novedades 0
FIR_Firmas 0
MAN_Mantenimientos 0
```

Las cuatro tablas de evidencia/ejecución están en cero filas en producción hoy, no solo en el
volcado. El fichero de la instantánea se borró después de leerlo; no forma parte de este documento.
No hay ninguna fotografía real que dependa de este cambio, y no hace falta migrar nada.

### 2.4 El parámetro `editable` de `col()` es documental: la protección real la produce `REGLAS`

```
$ grep -rln "editable" scripts/*.py
scripts/generar_guia_funcional.py
scripts/generar_manual_despliegue.py
scripts/modelo_objetivo.py
```

Ningún generador lee `c.get("editable")` en tiempo de ejecución — se comprobó con
`grep -rn '\["editable"\]\|\.get(.editable.)' scripts/*.py`, sin resultado fuera de
`modelo_objetivo.py`. Las dos apariciones en `generar_guia_funcional.py` y
`generar_manual_despliegue.py` son **texto fijo** ("en las tres columnas de captura..."), no un bucle
sobre la propiedad. **Lo que efectivamente cablea la instrucción de `Editable_If` para el ejecutor es
`REGLAS`** —`PROMPT_CABLEADO.md`, `PROMPT_EXPRESIONES.md`, `RECONSTRUCCION_EXPRESIONES.md` y
`ARQUITECTURA_OBJETIVO_SGMC.md` derivan de ahí, verificado en el §2.6 de `ESPEC-007` para el mismo
patrón—, así que declarar solo `editable=False` en el `col()` sin una regla en `REGLAS` no generaría
ninguna instrucción de cableado. Las dos cosas se declaran juntas en el §4, igual que ya conviven hoy
en las tres columnas de `MAN_Mantenimientos` (`editable=False` en el `col()` **y** `RG-20` en
`REGLAS`, comprobado en el §2.1).

### 2.5 Ninguna otra columna de `FOT_Fotografias`, y solo una tabla hermana, están en la misma situación

Barrido completo de todas las columnas `LatLong` del modelo:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
for t in MODELO:
    for c in MODELO[t]['columnas']:
        if c['tipo']=='LatLong':
            print(t, c['nombre'], 'valor_inicial=', c.get('valor_inicial'), 'editable=', c.get('editable'), 'obligatoria=', c.get('obligatoria'))
"
SED_Sedes Ubicacion_LatLong valor_inicial= None editable= None obligatoria= None
ACT_Activos Ubicacion_LatLong valor_inicial= None editable= None obligatoria= True
MAN_Mantenimientos UbicacionEscaneo_LatLong valor_inicial= None editable= False obligatoria= None
MAN_Mantenimientos Coordenadas_Cierre_LatLong valor_inicial= HERE() editable= False obligatoria= True
NOV_Novedades Ubicacion_LatLong valor_inicial= HERE() editable= None obligatoria= True
FOT_Fotografias Ubicacion_LatLong valor_inicial= HERE() editable= None obligatoria= True
```

Solo seis columnas `LatLong` existen en todo el modelo. Se agrupan en tres clases, y solo una
comparte el defecto de `FOT_Fotografias`:

| Columna | Clase | ¿Misma situación? |
|---|---|---|
| `SED_Sedes.Ubicacion_LatLong`, `ACT_Activos.Ubicacion_LatLong` | Dato de catálogo. Grupo `Catalogos`, sin `valor_inicial`: lo teclea o lo pega un administrador una vez, al dar de alta la sede o el activo — no hay `HERE()` capturando "dónde estoy ahora", así que no hay pin arrastrable que proteja de un técnico en campo | **No.** Distinto propósito: es un dato maestro que se corrige, no una evidencia que se congela |
| `MAN_Mantenimientos.UbicacionEscaneo_LatLong`, `MAN_Mantenimientos.Coordenadas_Cierre_LatLong` | Ya protegidas por `RG-20` (§2.1, §2.2) | **N/A — ya resuelto** |
| `NOV_Novedades.Ubicacion_LatLong` | `HERE()` como `Initial value`, `obligatoria=True`, sin `editable` ni regla — **idéntico patrón al de `FOT_Fotografias.Ubicacion_LatLong`** | **Sí, verificado.** Decisión de alcance en el §5 |
| `FOT_Fotografias.Ubicacion_LatLong` | El defecto de este documento | — |

`NOV_Novedades` es la tabla de "hallazgos del técnico en ruta" (`scripts/modelo_objetivo.py:359-378`)
y también lleva una columna `Fotografia` (`Image`, obligatoria) — mismo argumento de compresión que
`FOT_Fotografias.Archivo`, aunque su `nota=` no lo escribe explícitamente. Es el mismo defecto, con el
mismo remedio. **Se decide dejarlo fuera de esta especificación** (§5): el encargo, el nombre del
archivo y el §1 de este documento acotan "fotografías"; `NOV_Novedades` es una tabla distinta, con su
propio flujo, y mezclarla aquí sería ampliar el alcance sin que el título del documento lo declare.
Queda nombrado, verificado y con su comando de comprobación escrito, para que no haya que
redescubrirlo.

### 2.6 Un generador dejaría de instruir el `Initial value` de la misma columna — verificado con el cambio predicho sobre copia

Se predijo el cambio del §4 sobre una copia de `scripts/` y `docs/` fuera del repositorio (mismo
método que `PRUEBA-004`, `PRUEBA-005` y `PRUEBA-007`), y se regeneró `docs/PROMPT_CABLEADO.md`.
**Antes** de aplicar nada, la fila existe:

```
$ python scripts/generar_prompt_cableado.py   # sobre el repositorio real, sin ningun cambio
$ grep -n "FOT_Fotografias.*Initial value\|Initial value.*FOT_Fotografias" docs/PROMPT_CABLEADO.md
491:| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
```

**Después** de añadir solo `RG-39` (§4) a la copia y regenerar, la fila desaparece:

```
$ grep -n "FOT_Fotografias.*Ubicacion_LatLong" docs/PROMPT_CABLEADO.md   # sobre la copia, con RG-39 aplicada
(sin resultado en la seccion de Initial value; solo quedan PrecisionGPS y Usuario)
```

La causa está en `scripts/generar_prompt_cableado.py:327-331`:

```python
_huerfanas = [(t, c["nombre"], k, c[k])
              for t in MODELO for c in MODELO[t]["columnas"]
              for k in ("valor_inicial", "formula", "valid_if")
              if c.get(k) and (t, c["nombre"]) not in {(r["tabla"], r.get("columna"))
                                                       for r in REGLAS}]
```

El filtro descarta una columna de la lista de "expresiones huérfanas" en cuanto **cualquier** regla
de `REGLAS` toca esa `(tabla, columna)` — sin importar de qué **propiedad** trata esa regla. `RG-39`
es `Editable_If`, una propiedad distinta de `Initial value`, pero el código no distingue: al existir
`RG-39` sobre `(FOT_Fotografias, Ubicacion_LatLong)`, la comprensión de conjunto deja de listar el
`Initial value = HERE()` de esa misma columna, que **no** tiene ninguna regla propia que lo documente
en otro sitio.

**Esto no lo introduce esta especificación: ya está roto hoy**, sobre la columna que `RG-20` protege.
Se comprobó contra el repositorio real, sin ningún cambio:

```
$ grep -n "Coordenadas_Cierre_LatLong" docs/PROMPT_CABLEADO.md
378:- `MAN_Mantenimientos.Coordenadas_Cierre_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
```

**No hay ninguna fila que diga `Coordenadas_Cierre_LatLong | Initial value | HERE()`** en
`docs/PROMPT_CABLEADO.md` hoy, pese a que la columna sí lo lleva declarado
(`scripts/modelo_objetivo.py:335`) — `RG-01` (`Valid_If`) y `RG-20` (`Editable_If`) ya bastan para
que el filtro la excluya. La razón por la que esto no ha causado un incidente todavía:
`docs/MANUAL_DESPLIEGUE.md` sí la documenta, en una tabla distinta que recorre **todas** las columnas
de cada tabla sin depender de `REGLAS` (`scripts/generar_manual_despliegue.py:1127-1129`):

```
$ grep -n "Coordenadas_Cierre_LatLong" docs/MANUAL_DESPLIEGUE.md
1321:| `Coordenadas_Cierre_LatLong` | `LatLong` | `Initial value` = `HERE()` |
```

Esa tabla no depende de `REGLAS` y sí seguirá listando `FOT_Fotografias.Ubicacion_LatLong` aunque
exista `RG-39` — verificado sobre la misma copia:

```
$ python scripts/generar_manual_despliegue.py   # sobre la copia, con RG-39 aplicada
$ grep -n "^| \`Ubicacion_LatLong\`" docs/MANUAL_DESPLIEGUE.md
| `Ubicacion_LatLong` | `LatLong` | `Initial value` = `HERE()` |
```

**Hay una red de seguridad, pero no es la que el propio `PROMPT_CABLEADO.md` dice ser.** El texto que
antecede a la tabla de expresiones huérfanas afirma: *"Si no se ponen aquí, no las pone nadie"*
(`scripts/generar_prompt_cableado.py:340`). Es falso para `Coordenadas_Cierre_LatLong` desde que
existe `RG-20`, y sería falso también para `Ubicacion_LatLong` de `FOT_Fotografias` en cuanto exista
`RG-39`, salvo que se corrija. La corrección exacta, verificada sobre la misma copia:

```python
_MAPA_TIPO_REGLA = {"valor_inicial": "Initial value", "formula": "App formula",
                    "valid_if": "Valid_If"}
_cubiertas_por_tipo = {(r["tabla"], r.get("columna"), r["tipo"]) for r in REGLAS}
_huerfanas = [(t, c["nombre"], k, c[k])
              for t in MODELO for c in MODELO[t]["columnas"]
              for k in ("valor_inicial", "formula", "valid_if")
              if c.get(k) and (t, c["nombre"], _MAPA_TIPO_REGLA[k]) not in _cubiertas_por_tipo]
```

Con este cambio, sobre la misma copia con `RG-39` ya aplicada, la fila de `Ubicacion_LatLong` vuelve:

```
$ grep -n "^| \`FOT_Fotografias\` | \`Ubicacion_LatLong\`" docs/PROMPT_CABLEADO.md
491:| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
```

Y la de `Coordenadas_Cierre_LatLong` reaparece también, como efecto colateral correcto:

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`Coordenadas_Cierre_LatLong\`" docs/PROMPT_CABLEADO.md
506:| `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | `Initial value` | `HERE()` |
```

**Este defecto de código no se corrige aquí.** Es trabajo del ejecutor (`ORDEN-008`), el mismo
reparto que `ESPEC-005` y `ESPEC-006` dieron a los defectos de generador que encontraron por el
camino (`ESPEC-006` §2.8, §5, §6): la especificación lo documenta con el detalle necesario para que
la orden no tenga que volver a investigarlo, y la corrección de código se aplica junto con el cambio
de modelo, antes de regenerar `docs/PROMPT_CABLEADO.md`.

### 2.7 El hallazgo heredado: borrar una orden borra sus fotografías

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
c = [x for x in MODELO['FOT_Fotografias']['columnas'] if x['nombre']=='MantenimientoID'][0]
print(c)
"
{'nombre': 'MantenimientoID', 'tipo': 'Ref', 'ref': 'MAN_Mantenimientos', 'obligatoria': True, 'es_parte_de': True}
```

`es_parte_de=True` es lo que en AppSheet se marca como `Is a part of`: borrar una fila de
`MAN_Mantenimientos` borra en cascada sus filas hijas de `FOT_Fotografias`. **Esto es heredado, no lo
introduce esta especificación** — `es_parte_de=True` está en el modelo desde antes de este documento,
y no tiene relación de mecanismo con `Editable_If` ni con `HERE()`. Pero en un sistema cuyo propósito
es que la evidencia sea difícil de falsificar, que la evidencia se pueda hacer desaparecer borrando su
padre es la misma familia de problema, y no se puede dejar sin nombrar solo porque no es el defecto
que motivó este documento.

**Pero está más neutralizado de lo que esta sección llegó a decir, y quitar `IsPartOf` no lo
arreglaría.** `RG-15` ya retira `Deletes` de `MAN_Mantenimientos`, y su propia descripción lo dice:
*«Protegido aqui arriba, el IsPartOf de FOT, FIR y CHK nunca llega a dispararse»*. Dentro de la
aplicación **no hay botón que borre** una fila padre. El residuo real es otro: **borrado a mano en
el Sheets**, que dos cuentas tienen permiso para hacer — y un borrado en la hoja **no dispara
cascada ninguna**: deja huérfanos. Retirar `IsPartOf` tendría coste sin beneficio.

Y son **cuatro** hijos, no uno: `FOT_Fotografias`, `FIR_Firmas`, `CHK_Checklists`, y
`CHD_ChecklistDetalle` como nieta.

**No merece documento propio.** Queda en `docs/HALLAZGOS_ABIERTOS.md`, con su comando.

### 2.8 Un hallazgo tangencial, verificado y fuera de alcance: la identidad tampoco está protegida

> **Corregido tras el dictamen: son cuatro columnas en tres tablas, no dos en dos.** Y las dos que
> faltaban son **las más explotables**, porque son `Ref` —un desplegable— y no texto:
> `MAN_Mantenimientos.TecnicoID` y `NOV_Novedades.UsuarioID`, las dos con
> `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` como valor inicial y `editable=None`.
> Lo que se rompe: *un técnico abre el mantenimiento, elige a otro técnico en el desplegable, y la
> ejecución queda atribuida a un compañero.* Se hace con un toque. **Va a `ESPEC-009`**, porque a
> diferencia del pin sí tiene una decisión de diseño detrás: si `TecnicoID` deja de ser editable,
> hay que decir quién la asigna.

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
for t in MODELO:
    for c in MODELO[t]['columnas']:
        if c.get('valor_inicial')=='USEREMAIL()':
            print(t, c['nombre'], 'editable=', c.get('editable'))
"
MAN_Mantenimientos UsuarioRegistro editable= None
FOT_Fotografias Usuario editable= None
```

Ni `MAN_Mantenimientos.UsuarioRegistro` ni `FOT_Fotografias.Usuario` llevan `editable=False`: un
técnico podría, en teoría, editar a mano el correo que identifica quién tomó la fotografía. **No es
el mismo defecto que el de este documento**: `Usuario` es `Text`, no `LatLong` — no se dibuja como pin
arrastrable, se edita tecleando, y el riesgo es de **identidad** (quién lo hizo), no de **posición**
(dónde se hizo). Y aparece igual en `MAN_Mantenimientos` que en `FOT_Fotografias`, así que no es un
defecto exclusivo de esta tabla ni de "fotografías": es un patrón del modelo entero. Se nombra aquí
para que quede escrito y no se pierda, y se deja fuera (§5): mezclar un problema de identidad dentro
de un documento titulado "proteger ubicación" sería ampliar el alcance sin que el título lo declare.

### 2.9 La pregunta honesta: ¿basta `Editable_If = FALSE`, o hace falta que la columna se recalcule?

**Basta, y aquí está el porqué verificado, no supuesto.** `Editable_If = FALSE` congela el valor que
`HERE()` evaluó **una sola vez**, en el instante en que se creó esa fila — es decir, cuando el técnico
abrió el formulario para añadir esa fotografía concreta. Lo que garantiza:

- **Que nadie edite esa coordenada después de creada la fila**, ni arrastrando el pin ni de ninguna
  otra forma. Es exactamente el propósito: la evidencia queda donde `HERE()` la puso al crearse, no
  donde alguien decida después.
- **Que cada fotografía capture su propia posición.** `FOT_Fotografias` no reutiliza una fila: cada
  fotografía —de las 3 a 6 que exige el Supuesto D-10 (`scripts/modelo_objetivo.py:415`)— es un
  registro nuevo, así que `HERE()` se evalúa una vez **por fotografía**, no una vez por formulario o
  por mantenimiento. No hace falta ningún "recálculo" adicional entre fotos: cada una ya dispara su
  propia captura al crearse.

Lo que **no** garantiza, y que este documento no resuelve porque no es una decisión de producto que
le toque:

- **Que la lectura de `HERE()` sea precisa.** No hay ninguna medida de calidad de señal sobre esta
  columna — `PrecisionGPS` está descartada por inexistente (`ESPEC-007`) y no hay ninguna otra. Un
  `HERE()` con mala señal se congela igual de firme que uno bueno.
  - **Que la coordenada corresponda al instante exacto de disparar la cámara**, y no al instante de
  abrir el formulario. Si el técnico abre el formulario, camina unos metros y entonces toma la foto,
  `HERE()` ya se evaluó al abrir. Es el comportamiento estándar de `Initial value` en AppSheet —no
  hay forma de volver a dispararlo dentro del mismo alta sin usar `App formula`, que **sí** escribiría
  en la hoja en cada edición y es justo lo que el modelo evita a propósito para este tipo de dato
  (mismo criterio que `RG-16` documenta para no usar `App formula` donde el valor debe fijarse una vez
  y no recalcularse, `scripts/modelo_objetivo.py:1217-1226`).
- **Que las fotografías de un mismo mantenimiento coincidan entre sí en coordenada.** No es un
  defecto: cada `HERE()` es independiente y es correcto que varíen ligeramente si el técnico se movió
  alrededor del activo entre una foto y otra.
- **Qué pasa si `HERE()` no está disponible** —sin señal, o con la ubicación denegada en el
  dispositivo—. Esta rama faltaba, y la señaló el arquitecto: **`Editable_If = FALSE` elimina
  también la única vía de corrección**. Si `HERE()` deja el campo vacío, la columna es obligatoria y
  **el técnico no puede guardar la fotografía**; si escribe `0, 0`, queda una evidencia falsa **e
  incorregible**. No hay página en `docs/BASE_CONOCIMIENTO_APPSHEET.md` que fije cuál de las dos
  ocurre, así que entra en su tabla de supuestos sin verificar.

  **Y la asimetría que hay que decir:** `MAN_Mantenimientos` tiene válvula de escape para el GPS
  malo —`CierreConExcepcion` más `MotivoExcepcion`, que `ESPEC-004` acaba de desbloquear—.
  `FOT_Fotografias` **no tendría ninguna**. Se acepta porque es medible barato en la misma sesión
  de editor —abrir el formulario con la ubicación denegada y mirar— y porque la alternativa
  —dejar el pin arrastrable— es peor: hoy la evidencia se puede mover **siempre**, no solo cuando
  falla el GPS.

No se propone ningún `Valid_If` que compare esta coordenada contra la del cierre del mantenimiento
(el equivalente de `RG-01` para fotografías). Sería una decisión de producto nueva —con qué margen,
contra qué punto de referencia si hay varias fotos por visita— y el §1 ya estableció que esta
especificación no la toma. Queda nombrado en el §5.

## 3. Qué cambia exactamente

| Tabla.Columna | Estado actual | Estado objetivo |
|---|---|---|
| `FOT_Fotografias.Ubicacion_LatLong` | `LatLong`, obligatoria, `Initial value = HERE()`, sin `Editable_If` | Igual, más `editable=False` en el `col()` y cubierta por una regla `Editable_If = FALSE` nueva |

Ninguna otra columna, tabla ni referencia cambia. `FOT_Fotografias` sigue con 8 columnas (o 7, si
`ESPEC-007` se aplica antes — sin relación con este cambio, §6). `REGLAS` pasa de 21 a 22 entradas.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, dos puntos, más una corrección de código fuera del modelo:

- **`MODELO["FOT_Fotografias"]["columnas"]`** (línea 424): añadir `editable=False` al `col()` de
  `Ubicacion_LatLong`:

  ```python
  col("Ubicacion_LatLong", "LatLong", obligatoria=True, valor_inicial="HERE()",
      editable=False,
      nota="Coordenada de CADA fotografia. La compresion a 600 px descarta el EXIF, "
           "asi que la geolocalizacion debe guardarse como dato, no confiarse a la imagen"),
  ```

- **`REGLAS`**: añadir una entrada nueva, `RG-39` (siguiente identificador libre: el máximo hoy es
  `RG-38`, comprobado con `sorted(int(r['id'].split('-')[1]) for r in REGLAS)` → `... 37, 38`). Se
  declara como regla hermana de `RG-20`, no como su extensión, porque el esquema de `REGLAS` ata cada
  entrada a una sola tabla (§2.2):

  ```python
  dict(id="RG-39", tabla="FOT_Fotografias", columna="Ubicacion_LatLong",
       tipo="Editable_If", cubre="Prueba de presencia",
       expresion="FALSE",
       descripcion=("Mismo mecanismo que RG-20: HERE() es Initial value, no App formula, y un "
                    "Initial value SI es editable. Sin esto la coordenada de la fotografia se "
                    "dibuja como un pin arrastrable y la evidencia queda donde el tecnico quiera "
                    "dejarla, no donde tomo la foto. CABLEAR DESPUES del Initial value = HERE(): "
                    "al reves la columna queda obligatoria, no editable y vacia, y ningun "
                    "tecnico puede guardar una fotografia. ESPEC-008.")),
  ```

  **La instrucción de orden va dentro de `descripcion`, y no es un detalle de estilo.** `RG-39`
  llega a quien cablea a través de `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, y allí aparece como
  *«Tipo: `Editable_If` · `FALSE`»*: si la advertencia vive solo en §6 de este documento, el
  operador la pega en `Update Behavior > Editable?`, no toca `Initial value` porque **ese**
  documento no lo menciona, y si estaba vacío **ningún técnico puede volver a guardar una
  fotografía**. El campo `descripcion` se propaga solo a los tres documentos generados; la prosa de
  una especificación, no.

  No se modifica el `dict` de `RG-20`: sigue cubriendo exactamente las mismas tres columnas de
  `MAN_Mantenimientos` que hoy.

- **`RG-40`, sobre `NOV_Novedades.Ubicacion_LatLong`**, idéntica salvo la tabla, y su `col()` con
  `editable=False`:

  ```python
  dict(id="RG-40", tabla="NOV_Novedades", columna="Ubicacion_LatLong",
       tipo="Editable_If", cubre="Prueba de presencia",
       expresion="FALSE",
       descripcion=("Igual que RG-39, sobre la novedad en vez de la fotografia. Sin esto un "
                    "tecnico registra una novedad en ruta, arrastra el pin y el hallazgo queda "
                    "georreferenciado donde el quiera. CABLEAR DESPUES del Initial value = "
                    "HERE(). ESPEC-008.")),
  ```

  **Entró después del dictamen, y conviene decir por qué.** Este documento la había dejado fuera
  por el título —«fotografías»—, y el arquitecto la señaló como *«el único de los tres aplazados
  que nombra la misma rotura que motivó la especificación»*. Es el mismo defecto, el mismo
  mecanismo y el mismo arreglo: **una regla más, cero decisiones nuevas.** Escribir una `ESPEC-009`
  para repetir el argumento con otro nombre de tabla habría sido crecimiento sin contenido.

- **`scripts/generar_prompt_cableado.py:327-331`** (código, no modelo): corregir el filtro de
  "expresiones huérfanas" para que compare por propiedad, no solo por columna — el cambio exacto y
  verificado está en el §2.6. **Tiene que aplicarse en el mismo commit que el cambio de modelo, antes
  de regenerar `docs/PROMPT_CABLEADO.md`** (§6): si se regenera sin corregirlo, ese documento deja de
  instruir el `Initial value = HERE()` de `Ubicacion_LatLong`, y de paso también deja de instruirlo
  para `Coordenadas_Cierre_LatLong` (que ya lo tenía perdido, §2.6).

No se toca `CAMPOS_RETIRADOS`, `RETIRADAS`, `RETIPADOS`, `RENOMBRADOS`, `PARAMETROS` ni `DECISIONES`:
no se retira ni se retipa ninguna columna, y esto no es una decisión de rediseño de dominio como las
que registra `DECISIONES` — es la aplicación del mismo mecanismo que `RG-20` ya fijó, a una columna
que quedó fuera la primera vez.

**Documentos que se re-emiten** con los comandos de siempre, una vez editados
`scripts/modelo_objetivo.py` y `scripts/generar_prompt_cableado.py`: `docs/ARQUITECTURA_OBJETIVO_SGMC.md`,
`docs/MANUAL_DESPLIEGUE.md`, `docs/PROMPT_CABLEADO.md`, `docs/PROMPT_EXPRESIONES.md`,
`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, `docs/REGLAS_DEL_MODELO_DE_DATOS.md`. Todos derivan de
`REGLAS` en tiempo de ejecución (verificado uno a uno en el §2.6 y en la cabecera de este documento);
ninguno necesita edición manual de contenido, más allá de la corrección de código ya señalada.

**No hace falta regenerar `BD/Modelo_Datos_PLANTILLA.xlsx`.** Este cambio no añade, retira ni retipa
ninguna columna física: `editable=False` y las reglas `Editable_If` no tienen representación en la
cabecera del Excel — verificado que ni `scripts/generar_plantilla.py` ni `scripts/verificar_faseA.py`
mencionan la palabra "editable" en ningún sitio (`grep -n "editable" scripts/generar_plantilla.py
scripts/verificar_faseA.py`, sin resultado). Confirmado corriendo `verificar_faseA.py` sobre la copia
con el cambio aplicado: mismos `AVISOS (2)` que sin él (§6, evidencia completa en `PRUEBA-008`).

## 5. Qué NO cubre esta especificación

- **No protege `NOV_Novedades.Ubicacion_LatLong`.** Tiene el mismo defecto, verificado en el §2.5,
  con el mismo remedio disponible. Queda fuera porque el encargo, el título de este documento y su
  §1 acotan "fotografías"; `NOV_Novedades` es una tabla y un flujo distintos ("hallazgos del técnico
  en ruta"). Si se decide protegerla, es una especificación pequeña y ya investigada: mismo patrón
  `col(editable=False)` + regla hermana de `RG-20`/`RG-39`, sin decisión de producto pendiente.
- **No protege `SED_Sedes.Ubicacion_LatLong` ni `ACT_Activos.Ubicacion_LatLong`.** Verificado en el
  §2.5 que no comparten el defecto: son datos de catálogo sin `Initial value = HERE()`, no evidencia
  capturada en campo.
- **No protege la identidad de quién sube la evidencia** (`FOT_Fotografias.Usuario`,
  `MAN_Mantenimientos.UsuarioRegistro`, §2.8). Es un problema distinto —edición de texto, no arrastre
  de un pin— y afecta a `MAN_Mantenimientos` igual que a `FOT_Fotografias`, así que no es un asunto de
  "fotografías" tampoco.
- **No resuelve que borrar una orden borre en cascada sus fotografías**
  (`FOT_Fotografias.MantenimientoID` con `es_parte_de=True`, §2.7). Es heredado, no lo introduce este
  documento, y su remedio es una decisión de diseño distinta a la de este documento.
- **No añade ningún `Valid_If` que compare la coordenada de la fotografía contra la del cierre del
  mantenimiento** (el equivalente de `RG-01` para evidencia fotográfica, §2.9). Sería una decisión de
  producto nueva, no la extensión mecánica de un candado ya decidido.
- **No corrige el generador dentro de esta especificación.** El defecto del §2.6 se documenta con el
  detalle y el parche exactos para que la orden de ejecución (`ORDEN-008`) no tenga que
  reinvestigarlo, pero el cambio de código es de la orden, no de esta especificación — mismo reparto
  que `ESPEC-005` y `ESPEC-006` dieron a los defectos de generador que encontraron en el camino.
- **No confirma en el editor qué trae hoy `Ubicacion_LatLong` de `FOT_Fotografias`.**
  `docs/CORRECCIONES_CABLEADO.md` solo registra que se cableó la referencia a `MAN_Mantenimientos` el
  2026-08-10; no dice nada sobre si esta columna ya tiene algo puesto. Necesita sesión de navegador
  (§6).
- **No repite ni reabre `ESPEC-004` ni `ESPEC-007`.** No hay dependencia entre ellas y esta
  especificación (§6).

## 6. Riesgos y dependencias

- **El defecto de generador del §2.6 tiene que corregirse en el mismo commit que el cambio de
  modelo, antes de regenerar `docs/PROMPT_CABLEADO.md`.** Si no se corrige: ese documento deja de
  instruir `Initial value = HERE()` para `Ubicacion_LatLong`. Si el ejecutor sigue el documento tal
  cual y solo cablea `Editable_If = FALSE`, la columna queda **obligatoria, no editable y sin ningún
  valor que la llene** — el formulario de fotografías no se podría guardar nunca, un bloqueo peor que
  el defecto que este documento viene a cerrar. El parche exacto está verificado y listo en el §2.6 y
  el §4; aplicarlo cuesta cuatro líneas.
- **No se sabe si `Ubicacion_LatLong` ya tiene algo cableado en el editor de producción.** A
  diferencia de `RG-20` sobre `MAN_Mantenimientos` (confirmado en `ACTA-004` §1: `Editable_If =
  FALSE` ya puesto), no existe ninguna lectura del editor sobre esta columna de `FOT_Fotografias`.
  `docs/CORRECCIONES_CABLEADO.md` solo registra la referencia `MantenimientoID → MAN_Mantenimientos`
  cableada el 2026-08-10; nada sobre `Ubicacion_LatLong`. **Antes de tocar nada en el editor**, la
  sesión de navegador debe leer `Data > Columns > FOT_Fotografias > Ubicacion_LatLong`: si `Initial
  value` ya trae `HERE()`, solo falta poner `Editable_If`; si está vacío, hay que poner las dos cosas
  en el mismo paso, en el orden Initial value primero, Editable_If después — poner `Editable_If =
  FALSE` antes de que `Initial value` tenga algo dejaría el campo obligatorio inutilizable desde el
  primer momento, el mismo riesgo del punto anterior pero causado a mano en vez de por el generador.
- **No depende de `ESPEC-004` ni de `ESPEC-007`.** Se verificó aplicando solo el cambio de este
  documento sobre una copia: `validar_modelo.py` da `210` columnas y `22` reglas, sin errores nuevos,
  con exactamente los mismos tres avisos que hoy (evidencia completa en `PRUEBA-008`). Si `ESPEC-007`
  se aplica antes o después, `FOT_Fotografias` pasa de 8 a 7 columnas por la retirada de
  `PrecisionGPS`, sin relación de mecanismo con `RG-39`.
- **Sin datos que migrar** (§2.3). Revertir esta especificación, en cualquier momento antes de la
  primera fila real de `FOT_Fotografias`, cuesta quitar una entrada de `REGLAS` y un parámetro de un
  `col()`.
- **Qué se rompe si el supuesto del §2.9 fuera falso:** si alguna vez se necesita distinguir,
  fotografía por fotografía, la calidad de la señal con que se tomó —una auditoría legal de
  evidencia, por ejemplo—, hoy no hay ningún dato que lo permita (`PrecisionGPS` está descartada,
  `ESPEC-007`). No es una regresión de este documento: ya era así antes, y sigue siéndolo después.

## 7. Supuestos adoptados

- **Se adopta declarar `RG-39` como regla hermana de `RG-20`, no como su extensión.** El esquema de
  `REGLAS` ata cada entrada a una sola tabla (§2.2, verificado en `validar_modelo.py:128-133`).
  **Qué lo rompe:** que `REGLAS` cambie de esquema para admitir una lista de `(tabla, columna)` por
  entrada. **Qué tan barato es reabrirlo:** fusionar `RG-20` y `RG-39` en una sola entrada, si ese
  esquema llega a existir, es un cambio de forma sin cambio de comportamiento — ambas reglas ya
  comparten `tipo` y `expresion` literales.
- **Se adopta que `Editable_If = FALSE` es suficiente y que no hace falta ningún mecanismo de
  recálculo** (§2.9), porque cada fotografía es una fila nueva y `HERE()` se evalúa una vez por fila,
  no una vez por tabla ni por sesión. **Qué lo rompe:** que AppSheet reutilice una fila parcialmente
  completada entre sesiones —un borrador— de forma que reabrirla no vuelva a evaluar `Initial value`.
  **Qué tan barato es comprobarlo:** un fixture de una sola fila, abrir el formulario, cerrarlo sin
  guardar, reabrirlo y mirar si la coordenada cambió — cae dentro de la misma sesión de editor que ya
  hace falta para el punto siguiente, no exige una ventana aparte.
- **Se adopta no verificar en esta especificación si `Ubicacion_LatLong` ya tiene algo cableado en
  producción** (§6). **Qué lo rompe:** que sí lo tenga y el orden de cableado importe (mismo patrón
  de advertencia que `ESPEC-007` §8 dejó escrito para `PrecisionGPS`, aplicado aquí en sentido
  inverso: aquí el riesgo es poner `Editable_If` antes que `Initial value`, no al revés). **Qué tan
  barato es cerrarlo:** una lectura de `Data > Columns`, en la misma sesión ya encolada.
- **Se adopta que el defecto de generador del §2.6 se corrige en código, en `ORDEN-008`, no aquí.**
  Mismo criterio que `ESPEC-005` y `ESPEC-006` aplicaron a los defectos de generador que encontraron
  por el camino. **Qué lo rompe:** que alguien regenere `docs/PROMPT_CABLEADO.md` sin aplicar antes
  el parche del §2.6 — el documento quedaría dando una instrucción incompleta sin decirlo, exactamente
  el patrón que este mismo documento vino a evitar en otro sitio. **Qué tan barato es evitarlo:** el
  parche son cuatro líneas, ya escritas y verificadas (§2.6).
- **Se adopta que `NOV_Novedades.Ubicacion_LatLong`, la identidad sin proteger y la cascada de borrado
  (§2.5, §2.7, §2.8) quedan fuera de esta especificación**, por acotar el alcance al título del
  documento. **Qué lo rompe:** que se decida que "proteger evidencia" es una directriz única que debe
  aplicarse de una vez a las cuatro cosas. **Qué tan barato es reabrirlo:** cada uno ya está
  verificado, nombrado y con su comando de comprobación escrito en este documento — no hace falta
  redescubrir nada, solo decidir tratarlo.

---

## 8. Cierre — qué se acepta como riesgo, y qué no entra aquí

**APROBADA CON RIESGOS ACEPTADOS el 2026-08-11**, en primera pasada. Las **ocho condiciones** del
dictamen están aplicadas: la instrucción de orden dentro del campo `descripcion` de `RG-39` y
`RG-40`, `P-73` acotado a la sección de `FOT_Fotografias`, `P-72` con patrón anclado y salidas
literales, la rama de `HERE()` no disponible en §2.9, §2.8 corregido a 4 columnas en 3 tablas, §2.7
corregido citando `RG-15`, §0 rebajado de «probado» a «cableado y leído de vuelta», y el literal de
`generar_guia_funcional.py`. **Y ampliada a `NOV_Novedades` con `RG-40`** por recomendación expresa
del dictamen: es el mismo defecto, el mismo mecanismo y el mismo arreglo.

> **Esta sección decía «sin pasar por el arquitecto todavía» durante horas después de que el
> arquitecto la aprobara**, porque quien aplicó las ocho condiciones no volvió a tocar el cierre.
> Mientras tanto `ESTADO.md` y `docs/ROADMAP.md` sí decían «aprobada». **Un ejecutor se negó a aplicar
> `ORDEN-008` por esa contradicción, y acertó**: le creyó al documento y no al resumen, que es la
> regla de este proyecto. Queda escrito porque es el modo de fallo más barato de cometer —aplicar lo
> que un dictamen pide y olvidar registrar que el dictamen existió— y el gate solo funciona si el
> propio documento lleva su veredicto.

### Riesgos aceptados

1. **El defecto de generador del §2.6 es real, verificado y no es cosmético.** Si `ORDEN-008` aplica
   `RG-39` sin el parche de `generar_prompt_cableado.py`, el resultado no es un documento
   desactualizado: es un formulario de fotografías que no se puede guardar nunca, porque
   `Ubicacion_LatLong` quedaría obligatoria, no editable y sin ningún valor que la llene. **Por qué se
   propone aceptar el riesgo de proceder de todos modos:** el parche está escrito, verificado con
   diff de antes y después (§2.6), y cuesta cuatro líneas — no es una investigación pendiente, es un
   paso de la orden que ya tiene su texto.
2. **No se sabe si `Ubicacion_LatLong` de `FOT_Fotografias` ya tiene algo cableado en el editor.** A
   diferencia de `PrecisionGPS` (`ESPEC-007`, retiro de una columna con ambigüedad Rama A/B) esta es
   la situación inversa: **añadir** protección a una columna cuyo estado de cableado hoy no está
   leído. **Por qué no bloquea escribir esta especificación:** es una lectura, no una decisión de
   diseño, y el orden correcto para la sesión de editor ya queda escrito (§6): `Initial value`
   primero, `Editable_If` después. **Qué lo cierra:** la misma sesión de navegador que ya está en la
   cola por otras pendientes (`ORDEN-004` §6, `ORDEN-006` §6, `ESPEC-007` §5-§6).
3. **El supuesto del §2.9 —que `Editable_If = FALSE` no necesita ningún recálculo porque cada
   fotografía es una fila nueva— no se verificó en un fixture real**, solo se razonó desde cómo
   AppSheet evalúa `Initial value` según su documentación y el comportamiento ya observado de `RG-20`
   en producción (`ACTA-004`). **Por qué se propone aceptar:** el caso que lo rompería —una fila
   borrador reutilizada entre sesiones— no tiene evidencia de que ocurra en este sistema, y
   comprobarlo cuesta la misma sesión de editor ya encolada, no una ventana aparte.

### Lo que NO entra aquí, y queda nombrado para quien decida el siguiente paso

**`NOV_Novedades.Ubicacion_LatLong` tiene, verificado en el §2.5, el mismo defecto exacto:** `HERE()`
como `Initial value`, obligatoria, sin `editable` ni regla que la cubra. El remedio ya está
investigado —mismo patrón `col(editable=False)` más una regla hermana de `RG-20`/`RG-39`— y no exige
ninguna decisión de producto nueva. No se convierte en `ESPEC-009` aquí porque esta es, según el
encargo, la última especificación prevista de esta tanda; queda con su comando de verificación
escrito (§2.5) para que abrir esa especificación, si se decide, no cueste una investigación nueva.

**La identidad de quién sube la evidencia tampoco está protegida** (§2.8): `FOT_Fotografias.Usuario`
y `MAN_Mantenimientos.UsuarioRegistro` son editables pese a llevar `USEREMAIL()`. Es un defecto de
otra familia —edición de texto, no arrastre de un pin— y toca a dos tablas, no solo a fotografías.
Queda nombrado, no perseguido.

**Borrar una orden sigue borrando en cascada sus fotografías** (`FOT_Fotografias.MantenimientoID` con
`es_parte_de=True`, §2.7). Es heredado, no lo introduce este documento ni lo resuelve: decidir si
`MantenimientoID` debe dejar de ser `IsPartOf` —con el costo de que entonces habría que borrar la
evidencia a mano en dos sitios— es una decisión de diseño distinta a la de este documento, y merece
la suya propia si alguna vez se prioriza.
