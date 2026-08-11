# Lo que se hace a mano

Esto no es `docs/MANUAL_DESPLIEGUE.md` (cómo se despliega de cero) ni `docs/ENCARGO_VENTANA.md` (lo
urgente antes de poblar). Es la lista de lo que **ningún comando puede hacer ni verificar**: la API
v2 de AppSheet devuelve filas, no esquema — no hay forma de preguntarle de qué tipo es una columna,
qué expresión tiene, quién puede editarla o cuál lleva `Label` (`docs/BASE_CONOCIMIENTO_APPSHEET.md`
§14, `scripts/lectura_de_vuelta.py`). Todo eso se mira a ojo, en el editor, o no se mira.

Reunido de `docs/sdd/ESPEC-004-cierre-excepcion-manual.md` §8, `docs/sdd/ESPEC-006-reemplazo-bots-programados.md`
§8, `docs/sdd/PRUEBA-005-clave-otid-planid.md` (Familias B y D), `docs/sdd/PRUEBA-006-reemplazo-bots-programados.md`
(Familia B), `docs/sdd/PRUEBA-003-despliegue.md` (`P-23` a `P-27`, `P-29`, `P-32`, `P-33`),
`docs/sdd/ACTA-004-lecturas-editor.md`, `docs/sdd/ACTA-006-cotejo-y-supuesto.md`,
`docs/ENCARGO_VENTANA.md`, `docs/TIPOS_ESPERADOS.md`, `scripts/navegacion_editor.py` (dónde está cada
control) y `scripts/lectura_de_vuelta.py` (qué se comprueba y qué no). No repite el contenido de esos
documentos: extrae de cada uno solo lo que exige mano.

Ordenado por **cuándo se hace**. Ejecuta de arriba abajo.

---

## 0. Cuatro hechos de hoy, antes de tocar nada

1. **No existe ningún bot en la aplicación.** `Automation > Bots` está vacío —comprobado dos veces
   con recarga en duro, `docs/sdd/ACTA-004-lecturas-editor.md` §4ter—. El modelo declara cinco
   reglas de tipo bot y ninguna está creada. De esas cinco, **dos no hay que crearlas nunca como
   bot**: `RG-08` y `RG-12` son `Bot programado`, y en la cuenta gratuita en la que corre hoy
   `_SISGA_-323965761` un bot con evento `Schedule` **no se ejecuta nunca**, aunque quede configurado
   sin un solo error (cita textual contra la fuente oficial, `docs/BASE_CONOCIMIENTO_APPSHEET.md` §6).
   `docs/sdd/ESPEC-006-reemplazo-bots-programados.md` las reemplaza por una columna virtual (`RG-37`)
   y una vista más una acción (`RG-38`) — Fase 6 y Fase 8 de este documento, no un bot.
2. **`RG-07` manda correo real** a `ivan.salcedo@concesiondelsisga.com.co`, una dirección
   corporativa, en cuanto se añade **cualquier** fila en `OT_OrdenesTrabajo` — la cree un técnico con
   el botón `+`, el bot `RG-10`, o (cuando exista) la acción de `RG-38`. Se crea el último de los tres
   bots reales, y se desactiva antes de cualquier fixture de prueba (Fase 6).
3. **El icono `=` no es un visor: es un conmutador.** Junto a `Editable?` o `Require?`, pulsarlo sobre
   un campo booleano lo convierte a expresión **vacía**, y al guardar la aplicación entera deja de
   cargar. Ocurrió el 2026-08-11 sobre `CierreConExcepcion`, con este texto exacto:

   ```
   Column Name 'CierreConExcepcion' in Schema 'MAN_Mantenimientos_Schema' of Column Type 'Yes/No'
   has an invalid Editable_If constraint '='. Empty expression

   The _SISGA_-323965761 app did not load successfully.
   version 1.000111 is not runnable --- please contact the app creator.
   ```

   Para saber si un campo trae expresión, **no se pulsa el icono**: se mira si aparece resaltado. Si
   se activa por accidente, se sale con la **`X`** del campo de expresión —nunca `Ctrl+Z`, que no
   deshace el cambio de modo— y se confirma que `SAVE` vuelve a gris antes de seguir
   (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §18).
4. **Un tipo mal no solo deja una regla decorativa — falsea lo que la API devuelve.** Comparar `Text`
   contra el booleano `TRUE` es siempre falso y no da error (el defecto que tenía `RG-03` sobre
   `CierreConExcepcion`). Y por separado: `USR_Usuarios.Telefono` tipada `Number` en vez de `Phone`
   hacía que la API devolviera `'57321654987'` en vez de `'+57321654987'` — **el mismo dato, leído
   distinto según el tipo** (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §17). Cualquier lectura de vuelta
   por API —`instantanea.py`, `auditar_cableado.py`— solo es confiable si los tipos de abajo ya están
   confirmados. Por eso el cotejo de tipos va primero.

## 1. Reglas que valen para toda la sesión

- **Antes de leer ningún tipo: `Ctrl+Shift+R`.** Si el editor muestra «A newer version of the app
  exists», lo que hay en pantalla puede ser caché. Una sesión anterior leyó las nueve columnas de
  `OT_OrdenesTrabajo` como `Text` cuando ya estaban puestas — era caché, y se rehízo el cotejo
  (`docs/sdd/ACTA-006-cotejo-y-supuesto.md` §1).
- **El botón `SAVE` de la cabecera pasa de gris a AZUL cuando el editor recoge un cambio, y vuelve a
  gris al guardar.** Si sigue gris, el cambio no llegó al modelo interno y se pierde al recargar.
- **Si AppSheet muestra un error, ese error describe algo real.** Se copia el texto exacto y se para
  — no se reintenta a ciegas.
- **Ningún paso se cierra sin decir cómo se lee de vuelta.** La mayoría de los pasos de este
  documento no tienen comando (`scripts/lectura_de_vuelta.py`, categorías `tipos`, `expresiones`,
  `permisos`, `etiqueta`: las cuatro dicen **«No hay comando»**, literal). Donde no lo hay, se cierra
  copiando literalmente lo que se ve, **aunque coincida con lo esperado** — «coincide» no es
  evidencia, el texto sí.

## 2. Orden de ejecución

| # | Fase | Pantalla | ¿Tiene comando de verificación? |
|---|---|---|---|
| 1 | Columnas virtuales `Etiqueta` (`RG-35`/`RG-36`) | `Data > Columns > TABLA` | No (`Show?`/`Label`); el valor, una vez hay filas, sí |
| 2 | Cotejo de tipos, tabla por tabla | `Data > Columns > TABLA` | No |
| 3 | Expresiones de cada regla (`Valid_If`, `Required_If`, `App formula`, `Initial value`, `Editable_If`) | `Data > Columns > TABLA` | No |
| 4 | `Description` de `CierreConExcepcion` — **ya hecho** | `Data > Columns > MAN_Mantenimientos` | No |
| 5 | `Key` en `OTID`/`PlanID` — **ya hecho** | Lista de columnas de `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` | No |
| 6 | Columna virtual `EstaVencida` (`RG-37`) — condicional | `Data > Columns > OT_OrdenesTrabajo` | No (el valor sí se lee por API, medido) |
| 7 | Bots: `RG-06`, `RG-10`, y **`RG-07` último** | `Automation > Bots` | No |
| 8 | `Data > Actions` de `RG-10` | `Data > Actions` | No (la configuración); sí, indirecto, el resultado |
| 9 | Vista + acción de `RG-38` — condicional | `Data > Slices`, `Data > Actions` | No (la configuración); sí, indirecto, el resultado |
| 10 | `EOT_EstadosOrden.QuienCambia` (`Vencida`, `Programada`) — condicional | Hoja local y Sheets de producción | **Sí** |
| 11 | Inventario de vistas/slices/acciones/filtros | `UX > Views`, `Data > Slices`, `Behavior > Actions` | No |
| 12 | `Are updates allowed` por tabla | `Data > Tables > TABLA > Table settings` | No |
| 13 | Security Filters `RG-04`/`RG-05` — **los últimos, siempre** | `Data > Tables > TABLA > Table settings > Security` | No directo (efecto indirecto observable) |
| — | **Punto sin retorno**: primera fila real en cualquiera de las 8 tablas de movimiento | La aplicación misma | Ver Fase 14 |

Las fases 6, 9 y 10 son condicionales a que `docs/sdd/ESPEC-006-reemplazo-bots-programados.md`
(`ORDEN-006`) ya se haya aplicado a `scripts/modelo_objetivo.py`. Se comprueba así, y hay que volver a
correrlo antes de ejecutar esas fases, porque el modelo puede cambiar entre la escritura de este
documento y su lectura:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;ids=[r['id'] for r in REGLAS];print('RG-37' in ids, 'RG-38' in ids)"
```

Corrido tras aplicar `ORDEN-006` (2026-08-11): **`True True`** — `RG-37` y `RG-38` **ya están en el
modelo**, así que las fases 6, 9 y 10 **sí aplican**. Y sobre los otros dos, el mismo comando devuelve
**`RG-08 False, RG-12 False`**: están retirados. **No los crees como bot** — ya no existen ni en el
modelo ni en el editor, y en la cuenta gratuita un bot programado no se ejecuta nunca.

> Este párrafo decía `False False` cuando se escribió, unas horas antes de que `ORDEN-006`
> aterrizara. **Corre el comando tú mismo antes de estas tres fases** en vez de fiarte de esta línea:
> el modelo cambia más deprisa que el documento, y por eso la condición se escribió como comando y
> no como afirmación.

## 3. Detalle, fase por fase

### Fase 1 — Columnas virtuales `Etiqueta`

Ya están declaradas en el modelo (verificado hoy: `'RG-35' in ids` y `'RG-36' in ids` dan `True`).
Existen porque `OTID` y `PlanID` pasaron a `UNIQUEID()`: una orden ya no se llama `OT-0042` sino un
identificador alfanumérico sin significado, y sin etiqueta el técnico vería eso en cada desplegable.

**Pantalla:** `Data > Columns > OT_OrdenesTrabajo`, botón `Add virtual column`. Repetir en
`PLA_PlanMantenimiento`.

**Qué escribir**, literal desde `modelo_objetivo.py`:

| Tabla | Nombre | `App formula` |
|---|---|---|
| `OT_OrdenesTrabajo` | `Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` |
| `PLA_PlanMantenimiento` | `Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` |

Además, en la misma columna: **`Show?` activo** (sin esto AppSheet no la acepta como `Label`) y
**`Label` marcado** — si la tabla ya tenía otra columna con `Label` (típicamente `OTID`/`PlanID`),
**desmarcarla primero**: solo puede haber una por tabla.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta, para `Show?`/`Label` — no viajan por la
API. Se transcribe el estado de las dos casillas, y el de la columna vieja. El **valor** que calcula
la fórmula sí se puede leer por API, pero solo una vez existan filas: se abre un desplegable que
referencie la tabla y se copia el texto de una opción; con datos reales, `instantanea.py` también lo
trae en la fila.

### Fase 2 — Cotejo de tipos

**Por qué antes que nada más:** un tipo mal falsea la lectura de todo lo que viene después (§0,
punto 4).

**Pantalla:** `Data > Columns > TABLA`, columna por columna, sección `Type` del panel (es un
`<select>` nativo del navegador). Contra qué se compara: `docs/TIPOS_ESPERADOS.md` (generado, no se
edita a mano).

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta. Se transcribe el `Type` literal aunque
coincida con lo esperado.

**Cuánto falta hoy**, medido, no estimado:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from inferencia import clasificar;print(len(clasificar()['a mano']))"
```

Hoy (2026-08-11) da `106` — vuelve a correr este comando antes de empezar: el modelo está cambiando
mientras se escribe este documento y la cifra se mueve con él. Esa cuenta incluye catálogos ya
poblados además de las ocho tablas de movimiento; el reparto tabla por tabla:

```bash
python -c "
import sys;sys.path.insert(0,'scripts')
from inferencia import clasificar
import collections
c = collections.Counter(t for t, col, m in clasificar()['a mano'])
for t in sorted(c): print(t, c[t])
"
```

**Ya cerrado:** las 9 columnas de `OT_OrdenesTrabajo` — transcritas letra por letra en
`docs/sdd/ACTA-006-cotejo-y-supuesto.md` §1 (2026-08-11, con `Ctrl+Shift+R` previo), incluida
`EstadoOrdenID → Ref EOT_EstadosOrden`, de la que depende la desreferencia de `RG-37` (Fase 6).

### Fase 3 — Expresiones de cada regla

Ninguna de las cinco viaja por la API bajo ninguna forma (`scripts/lectura_de_vuelta.py`, categoría
`expresiones`: «Valid_If, App formula, Initial value, Editable_If y los Security Filter no viajan por
la API. Se copian del editor LITERALMENTE, sin resumir ni corregir»).

**Dónde vive cada una en pantalla — no es donde dice su nombre** (`scripts/navegacion_editor.py`):

| Lo que declara `modelo_objetivo.py` | Dónde está en pantalla |
|---|---|
| `Valid_If` | `Data Validity > Valid If` — el mensaje va en `Invalid value error`, justo debajo |
| `Required_If` | `Data Validity > Require?` — **no es una casilla que se marque**: hay que pulsar el icono `=` de al lado para escribir la expresión |
| `App formula` | `Auto Compute > App formula` — **escribe en la hoja** |
| `Initial value` | `Auto Compute > Initial value` — solo se aplica a filas nuevas |
| `Editable_If` | `Update Behavior > Editable?` — el icono `=` al lado de la casilla |

**Riesgo ya materializado una vez:** el 2026-08-10 la condición de `RG-03` (`Required_If`) acabó
escrita en `Valid If`, lo que la habría vuelto imposible de guardar.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta. Se copia literal cada campo, contra la
expresión declarada en `scripts/modelo_objetivo.py` (o su volcado, regenerable con
`python scripts/generar_prompt_expresiones.py`). `python scripts/validar_modelo.py` valida que la
expresión **declarada en el modelo** esté bien escrita — no confirma que el editor la tenga igual.

### Fase 4 — `Description` de `CierreConExcepcion` (ya hecha)

Adoptada en `docs/sdd/ESPEC-004-cierre-excepcion-manual.md` §2.13, escrita el 2026-08-11
(`docs/sdd/ACTA-004-lecturas-editor.md` §3). Ningún generador emite `Description`: era un
refinamiento que nadie iba a poner si no se hacía a mano.

**Pantalla:** `Data > Columns > MAN_Mantenimientos > CierreConExcepcion > Display > Description`.

**Texto exacto:**

```
¿La app no alcanzó buena precisión al capturar la posición de cierre? Marque si es así.
```

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta — sin comando. Confirmado que persiste
tras recarga en duro (`ACTA-004` §3). Se re-verifica a ojo si en el futuro se pulsa
`Regenerate Structure`.

### Fase 5 — `Key` en `OTID` y `PlanID` (ya hecha)

**Pantalla:** primero `Auto Compute > Initial value = UNIQUEID()` en cada columna; **después**, la
casilla `Key` en la **lista de columnas** (no dentro del panel) — sobre una tabla vacía, AppSheet no
deja marcar `Key` si la columna no tiene un `Initial value` que genere la clave. El orden importa.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta. Ya cerrado y transcrito literal en
`docs/sdd/ACTA-005-pruebas.md` (`P-09`): `Initial value = UNIQUEID()`, `Key` marcado, `_RowNumber`
sin `Key`, en las dos tablas. La lectura de vuelta de datos (que no mide esto, mide si se escribió
algo) dio `NINGUNA CELDA CAMBIO`.

Si en el futuro se añaden tablas a `CLAVE_GENERADA` (hoy 8:
`python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sorted(M.CLAVE_GENERADA))"`),
repetir esta fase respetando el mismo orden.

### Fase 6 — Columna virtual `EstaVencida` (`RG-37`) — condicional

Comprobar primero que aplica (§2). Si `'RG-37' in ids` da `True`:

**Pantalla:** `Data > Columns > OT_OrdenesTrabajo > Add virtual column`.

**Qué escribir:** nombre `EstaVencida`, tipo `Yes/No`, `App formula`:

```
AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())
```

`Show?` activo. **No lleva `Label`** — no es una etiqueta, es un cálculo; si se marca por error, se
desplaza el `Label` legítimo (`Etiqueta`, Fase 1) y el desplegable de `OT_OrdenesTrabajo` se queda
sin etiqueta legible.

**Cómo se sabe que quedó:** el **valor** calculado sí se lee por API — está medido, no supuesto:
`docs/sdd/ACTA-006-cotejo-y-supuesto.md` §2 creó una virtual de prueba sobre `PAR_Parametros` y la
API la devolvió en la fila. Pero el **texto exacto** de la `App formula`, carácter por carácter, no
viaja: un espacio de más o un `<=` en vez de `<` no lo cazaría ninguna prueba con datos, solo la
transcripción literal contra el texto de arriba.

Su consumidor (declarado dentro de la misma regla, no aparte): una vista `"Órdenes vencidas"` sobre
`OT_OrdenesTrabajo`, condición `[EstaVencida] = TRUE`, visible para el rol Supervisor, de solo
lectura.

### Fase 7 — Bots

**Pantalla:** `Automation > Bots` → `Create a new Bot`. Tres partes: `Event` (tabla + tipo de cambio,
o `Schedule`), `Condition`, `Step`.

**Se crean tres, en este orden, con la expresión literal que declara el modelo:**

| Orden | Bot | Tabla | `Condition` | Qué hace |
|---|---|---|---|---|
| 1 | `RG-06` | `MAN_Mantenimientos`, evento `Adds`/`Updates` | `[EstadoActivoID].[GeneraAlerta] = TRUE` | Envía correo con informe PDF al CCO y al supervisor cuando el activo queda fuera de servicio |
| 2 | `RG-10` | `MAN_Mantenimientos`, evento `Adds`/`Updates` | `[RequiereSegundaVisita] = TRUE` | Genera una orden de seguimiento enlazada a la original mediante `OTOrigenID` — ver Fase 8, el `Step` no se configura dentro del bot |
| 3 | `RG-07` | `OT_OrdenesTrabajo`, evento `Adds` | (sin condición: dispara con cualquier fila nueva) | Notifica por correo al técnico asignado — **manda correo real**, se crea último |

**No se crean como bot:** `RG-08` (`OT_OrdenesTrabajo`, `Bot programado`) ni `RG-12`
(`PLA_PlanMantenimiento`, `Bot programado`) — mientras sigan declaradas con ese tipo en el modelo
(§2). Un bot con evento `Schedule` en esta cuenta se puede configurar entero, sin error, y no va a
ejecutarse nunca.

**La trampa del `Step` de `RG-10`, y de `RG-38` cuando aplique:** si lo que el bot hace es AÑADIR UNA
FILA a otra tabla, no se configura dentro del bot — AppSheet interpreta que se quiere generar un
documento y pide plantilla PDF. Va en dos sitios, en este orden: 1) `Data > Actions` → `Add Action`
(`Do this = Data: add a new row to another table using values from this row`) — Fase 8; 2)
`Automation > Bots` → el bot → `Add a step` → `Run a data action`, eligiendo la acción recién creada.

**`RG-07`, la última, con una condición de operación:** antes de crear cualquier fila de prueba en
`OT_OrdenesTrabajo` (un fixture de las Familias B de `PRUEBA-005`/`PRUEBA-006`, o cualquier prueba
manual), se desactiva: `Automation > Bots` → `RG-07` → `Disable`. Se reactiva al terminar:
`Automation > Bots` → `RG-07` → `Enable`.

**Cómo se sabe que quedó — creación y estado `Enable`/`Disable`:** NADIE, salvo quien lo ejecuta. El
estado de un bot no viaja por la API v2. Se cierra copiando literalmente el texto que muestra la
columna de estado de `Automation > Bots` para ese bot, después de pulsar el botón — no basta con decir
«se activó» o «se creó».

### Fase 8 — `Data > Actions` de `RG-10`

**Pantalla:** `Data > Actions` → `Add Action`. `For a record of this table = MAN_Mantenimientos`,
`Do this = Data: add a new row to another table using values from this row`,
`Table to add to = OT_OrdenesTrabajo`, con `OTOrigenID` apuntando a la orden original.

**Un hueco que ningún documento del repositorio cierra, y hay que decidirlo aquí, no inventarlo
antes:** no hay evidencia documental de qué `EstadoOrdenID` debe llevar la orden de seguimiento que
crea `RG-10` — ni un `Initial value` ni un `Step` lo fijan en `scripts/modelo_objetivo.py`
(`docs/sdd/ESPEC-006-reemplazo-bots-programados.md` §3.1 lo señala expresamente: «no hay en el
archivo ninguna evidencia de que aterrice en `Programada`»). Se decide al configurar la acción, y se
deja escrito qué se eligió y por qué —una orden de seguimiento nace ya sabiendo el técnico, así que
`Asignada` es defendible; `Programada` es el valor por defecto del resto del flujo—, para que quien
lea `EOT_EstadosOrden` después no tenga que adivinarlo.

**Cómo se sabe que quedó:** el mapeo de columnas (`Set these columns`) no viaja por la API — se
transcribe literal. El **resultado**, una vez el bot se dispara con datos reales, sí es medible:
`python scripts/instantanea.py comparar <antes> <después>` debe mostrar una fila nueva en
`OT_OrdenesTrabajo` con `OTOrigenID` apuntando a la orden que lo disparó, y ninguna otra tabla
afectada (`docs/sdd/PRUEBA-005-clave-otid-planid.md` `P-11`).

### Fase 9 — Vista + acción de `RG-38` — condicional

Comprobar primero que aplica (§2, `'RG-38' in ids`). Si es `True`:

**Pantalla 1 — `Data > Slices`:** crear `"Vence en 7 días"` sobre `PLA_PlanMantenimiento`, condición:

```
AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)
```

**Pantalla 2 — `Data > Actions`:** `Add Action`, `For a record of this table = PLA_PlanMantenimiento`,
`Do this = Data: add a new row to another table using values from this row`,
`Table to add to = OT_OrdenesTrabajo`. Mapeo exacto, columna por columna:

| Columna de `OT_OrdenesTrabajo` | Valor en `Set these columns` |
|---|---|
| `ActivoID` | `[ActivoID]` |
| `TecnicoID` | `[ResponsableID]` |
| `SupervisorID` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `Tipo` | `"Preventivo"` |
| `FechaProgramada` | `[ProximaFecha]` |
| `EstadoOrdenID` | `"Programada"` |

`OTOrigenID`, `Observaciones`, `FechaCierre` y `CerradaPor` se dejan en blanco. **No se configura en
`Automation > Bots`**: no hay `Event` ni `Schedule`, es una acción que el supervisor pulsa
—individual o en bloque— desde la vista.

**Riesgo a vigilar, no resuelto aquí:** `ResponsableID` es opcional en `PLA_PlanMantenimiento` y
`TecnicoID` es obligatoria en `OT_OrdenesTrabajo`. Si una fila del plan no tiene `ResponsableID`
poblado, la acción falla al validar. No hay `Required_If` que lo evite hoy.

**Cómo se sabe que quedó:** la condición del slice y el mapeo de la acción no viajan por API — se
transcriben literal (`Data > Slices`, y `Data > Actions` → la acción → `Set these columns`). El
resultado, con datos reales, sí es medible con `instantanea.py`: una sola fila nueva en
`OT_OrdenesTrabajo`, con los valores de la tabla de arriba, y ningún cambio en la fila origen del
plan.

### Fase 10 — `EOT_EstadosOrden.QuienCambia` — condicional

Comprobar primero que aplica (§2, mismo `RG-37`/`RG-38`). Si aplica: dos filas del catálogo
`EOT_EstadosOrden` cambian el dato `QuienCambia` de `Sistema` a `Supervisor` — **`Vencida` y
`Programada`, las dos, con el mismo argumento**: ya no hay ningún mecanismo automático que las
escriba solo. `EsFinal` **no cambia** en ninguna de las dos.

**No es un cambio de esquema, es un cambio de dato**, y se hace en dos superficies que hoy coinciden:

1. `BD/Modelo_Datos_PLANTILLA.xlsx` — edición directa del archivo local, celda `QuienCambia` de las
   filas `Vencida` y `Programada`.
2. El Sheets de producción `Modelo_Datos_10082026` — edición directa en Google Sheets, **no en el
   editor de AppSheet**: `QuienCambia` no lo lee ninguna regla ni la controla ningún generador.

**Cómo se sabe que quedó:** este es el único paso de todo el documento con comando, porque es dato
de catálogo, no esquema:

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True)
for r in wb['EOT_EstadosOrden'].iter_rows(min_row=2, values_only=True): print(r)
"
python scripts/instantanea.py guardar tras-quiencambia
python -c "
import json
d = json.load(open('BD/instantaneas/tras-quiencambia.json', encoding='utf-8'))
for r in d['EOT_EstadosOrden']: print(r['EstadoOrdenID'], '| EsFinal=', r['EsFinal'], '| QuienCambia=', r['QuienCambia'])
"
```

Las dos vías tienen que mostrar `QuienCambia = Supervisor` en las dos filas, `EsFinal` sin cambiar
(`Y` en `Vencida`, `N` en `Programada`), y coincidir entre sí.

### Fase 11 — Inventario de vistas, slices, acciones y filtros

Hoy **no existe en el repositorio ningún inventario** de esto. Sin él, si se pierde una vista o un
slice, no hay contra qué compararlo.

**Pantalla:** recorrer `UX > Views`, `Data > Slices`, `Behavior > Actions` y el `Security Filter` de
cada tabla (`Data > Tables > TABLA > Table settings > Security`). Anotar nombre, tabla y **expresión
completa** de cada uno. Eso pasa a ser la línea base del sistema.

**Un chequeo específico dentro de este inventario:** ninguna vista, slice ni reporte debe filtrar por
`[ActivoID].[Activo]` — es la doctrina de `RG-18`, y con `RG-16` cableada (`App formula` que
recalcula `ACT_Activos.Activo` según `EstadoActivoID`), un filtro así haría desaparecer en silencio
los mantenimientos de cualquier activo retirado.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta. Sin comando, sin atajo.

### Fase 12 — `Are updates allowed` por tabla

**Pantalla:** `Data > Tables > TABLA > Table settings` — tres casillas: `Updates`, `Adds`, `Deletes`.

**Por qué no basta con la API para esto:** la API tiene **más** permisos que la aplicación —se salta
el `Deletes` retirado de `OT_OrdenesTrabajo` y `MAN_Mantenimientos`—, así que probar por ahí diría
que se puede borrar cuando la app no deja.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta. Se transcribe el estado de las tres
casillas, tabla por tabla.

### Fase 13 — Security Filters (`RG-04`, `RG-05`) — los últimos, siempre

**Pantalla:** `Data > Tables > TABLA > Table settings > Security > Security filter`.

**Por qué van al final, y no es preferencia:** una vez puestos, la API deja de devolver las filas de
esa tabla —llama sin usuario, `USEREMAIL()` queda en blanco, el filtro no deja pasar nada—, y ni
`instantanea.py` ni `auditar_cableado.py` pueden volver a mirarla. Ya ocurrió: al poner `RG-04` sobre
`ACT_Activos`, la API pasó de devolver 368 filas a devolver cero. No se perdió nada, pero los dos
únicos instrumentos mecánicos del proyecto se quedaron ciegos justo en la tabla más grande, para
siempre — no hay forma de deshacerlo salvo quitar el filtro.

**Verificación positiva/negativa, dentro de la propia app** (no hay comando, pero sí un
procedimiento repetible): `Preview app as` con el correo de un técnico — debe ver solo las órdenes
donde es técnico o supervisor. Repetir con un usuario que no figure en ninguna: esperado, cero filas.

**La trampa:** `RG-05` desreferencia `[TecnicoID].[Correo]`. Si esa referencia quedó como texto en
vez de `Ref`, el filtro no da error — devuelve vacío, y el técnico se queda sin trabajo en pantalla.

**Cómo se sabe que quedó:** NADIE, salvo quien lo ejecuta, para la expresión del filtro en sí. El
efecto —que `instantanea.py` y `auditar_cableado.py` dejan de ver la tabla— sí es observable con
comando, pero es un efecto colateral, no una confirmación de que el filtro esté bien escrito.

### Fase 14 — El punto sin retorno

Las ocho tablas de movimiento —`OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `PLA_PlanMantenimiento`,
`CHK_Checklists`, `CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `NOV_Novedades`— están hoy
en cero filas. Comprobar cuántas siguen así, con lectura de solo lectura (no escribe nada, pero
consultarlo no es lo mismo que cerrar la ventana):

```bash
python scripts/instantanea.py guardar antes-de-crear-la-primera-fila
```

**Mientras estén en cero, corregir un tipo o una clave mal puesta cuesta un clic. En cuanto entra la
primera fila —real o de prueba— en cualquiera de las ocho, corregirlo cuesta una migración, y ese
precio no vuelve a bajar nunca.** El proyecto no tiene vía de `Delete` para deshacerlo: `RG-14`/`RG-15`
la retiraron a propósito; cerrar un fixture de prueba se hace marcando `Activo = FALSE`, nunca
borrando.

**Antes de crear esa primera fila en cualquiera de las ocho tablas:** confirmar que las Fases 2
(tipos) y 3 (expresiones) de esa tabla concreta ya están cerradas. Si no, un fallo al probarla con
datos reales no distingue «la regla está mal» de «el tipo o la referencia no estaba confirmado» —el
mismo argumento que `docs/sdd/ESPEC-006-reemplazo-bots-programados.md` §2.9 usó para
`EstadoOrdenID`—.

**Esto no es un paso de configuración: es una decisión.** Este documento no dice cuándo gastarla —
eso depende de qué fixture de prueba (`PRUEBA-005`, `PRUEBA-006`) se decida ejecutar y cuándo—, solo
deja constancia de que, a partir de ahí, no hay vuelta atrás.

---

## 4. Cuenta final

| | Fases | Sin ningún comando de verificación |
|---|---|---|
| Pasos que exigen mano | **13** (Fases 1 a 13; la Fase 14 es una decisión, no un paso de configuración) | **11** |

Los dos únicos pasos con comando de verificación real son los de la Fase 10
(`EOT_EstadosOrden.QuienCambia`), porque son dato de catálogo, no esquema — todo lo demás (columnas
virtuales, tipos, las cinco propiedades de expresión, `Description`, `Key`, bots y su estado,
mapeos de acciones, condiciones de slices, permisos por tabla, filtros de seguridad, el inventario
de vistas) vive en el esquema de AppSheet, y el esquema no viaja por la API v2. Esa es la cifra que
mide el tamaño real del problema: **11 de 13 pasos no tienen ningún instrumento que los lea de
vuelta salvo quien los ejecuta, copiando literalmente lo que ve.**
