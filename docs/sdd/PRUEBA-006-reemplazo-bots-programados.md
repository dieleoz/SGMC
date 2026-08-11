# PRUEBA-006 — Pruebas de aceptación de ESPEC-006

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.EstaVencida -->
<!-- D-03 compara Tabla.Columna contra MODELO, y EstaVencida a propósito NUNCA entra en MODELO:
     es una columna virtual declarada solo en REGLAS (RG-37), siguiendo el mismo mecanismo que
     RG-35/RG-36 de ESPEC-005 y el mismo criterio que ya usa PRUEBA-005 para Etiqueta. Citarla en
     prosa como Tabla.Columna es legítimo, no un hueco del modelo. -->

**Escrita antes de que `ORDEN-006` exista.** Nada de lo que sigue se aplicó al repositorio real, al
Sheets de producción ni al editor de AppSheet. Los comandos marcados «corrida real» sí se
ejecutaron —de solo lectura contra la aplicación viva, o sobre una copia temporal de `scripts/` y
`docs/` fuera del repositorio, para predecir el resultado exacto de `ORDEN-006`— y sus salidas están
citadas literalmente, no supuestas. Los que requieren crear datos en la app están descritos para
cuando el ejecutor los corra, con los cinco campos completos, pero no ejecutados aquí.

| | |
|---|---|
| Cubre | [`ESPEC-006-reemplazo-bots-programados.md`](ESPEC-006-reemplazo-bots-programados.md): `RG-37` (columna virtual `EstaVencida` en `OT_OrdenesTrabajo`) reemplaza a `RG-08`; `RG-38` (vista + acción en `PLA_PlanMantenimiento`) reemplaza a `RG-12`; `EOT_EstadosOrden.QuienCambia` de la fila `Vencida` pasa de `Sistema` a `Supervisor` |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`, volcado con `python scripts/sistema.py` hoy — no descarga nada, solo confirma los identificadores vigentes) |
| Reglas que esta tanda prueba | `RG-37` y `RG-38`, nuevas. `RG-08` y `RG-12` quedan como huecos numéricos, no se prueba que "ya no estén": eso lo cubre `P-46` |
| Innegociables | `P-46`, `P-47`, `P-49`, `P-50`, `P-51`, `P-52`, `P-53`, `P-54`, `P-59`, `P-60` |

## 0. Los cinco puntos del encargo, y dónde se prueban

| # | Punto del encargo | Prueba(s) |
|---|---|---|
| 1 | `RG-37` positiva y negativa | `P-51` (positiva), `P-52` y `P-53` (negativas: fecha futura y ya cerrada) |
| 2 | `RG-37` NO impide cerrar | `P-55` |
| 3 | `RG-38` crea filas, y qué escribe / no toca | `P-56` (positiva, bloqueada), `P-57` (negativa, bloqueada) |
| 4 | El caso del tipo: `EstaVencida` como `Text` | `P-54` |
| 5 | `EOT_EstadosOrden.QuienCambia` llega a la hoja y a la aplicación | `P-58` y `P-59` |
| — | Los dos generadores corregidos (commit `0d3d641`) tratan bien a `RG-37` | `P-49` y `P-50` |

## 1. Estado de partida

### 1.1 El modelo, hoy — corrida real, no simulada

```bash
$ python -c "
import sys;sys.path.insert(0,'scripts')
from modelo_objetivo import REGLAS
ids=[r['id'] for r in REGLAS]
print(len(REGLAS))
print('RG-08' in ids, 'RG-12' in ids, 'RG-37' in ids, 'RG-38' in ids)
"
23
True True False False
```

`RG-08` y `RG-12` siguen en `REGLAS`. `RG-37` y `RG-38` no existen todavía en ningún documento del
repositorio (`ESPEC-006` §2.4 ya lo verificó por `grep`). Este es el estado que `P-46` confirma como
punto de partida.

### 1.2 Las filas de las tablas implicadas — corrida real contra la aplicación viva, hoy

```bash
$ python scripts/instantanea.py guardar prueba-006-partida
Guardada: BD/instantaneas/prueba-006-partida.json
28 tablas · 953 filas en total
```
```
OT_OrdenesTrabajo      0
PLA_PlanMantenimiento  0
MAN_Mantenimientos     0
EOT_EstadosOrden       7
USR_Usuarios           11
ACT_Activos            368
FRE_Frecuencias        8
```
Y, dentro de `EOT_EstadosOrden`, la fila que este cambio toca — leída por API, no del `.xlsx`:
```
Vencida | EsFinal= Y | QuienCambia= Sistema
```
Coincide exactamente con lo que `ESPEC-006` §2.2 documenta contra las dos fuentes locales. La
instantánea se borró después de leerla (`rm BD/instantaneas/prueba-006-partida.json`), siguiendo la
higiene de `SDD_PIPELINE_SGMC.md` §5.1.

**Las dos tablas que `RG-37`/`RG-38` tocan siguen en cero.** Y no es la primera vez que se cuenta:
`ESPEC-005`/`PRUEBA-005` ya diseñaron un fixture para las mismas dos tablas, y **ese fixture nunca se
ejecutó.** `ACTA-005-pruebas.md` lo dice explícito: de sus 17 pruebas, 9 —toda la Familia B, C y D,
`P-09` a `P-17`— quedaron `NO EJECUTADA` por falta de acceso al editor en ese contexto, y el resumen
lo resume en una tabla: `8 pasan, 0 fallan, 0 bloqueadas, 9 no ejecutadas`. El conteo de filas de
arriba, hecho hoy, lo confirma de forma independiente: si el fixture de `PRUEBA-005` se hubiera
corrido, `OT_OrdenesTrabajo` no estaría en cero. **La ventana barata de las dos tablas sigue
abierta**, pero con una condición que `§1.4` desarrolla: no se sabe desde aquí si el editor ya tiene
`OTID`/`PlanID` con `Initial value = UNIQUEID()` y `Key` marcada (`P-09` de `PRUEBA-005`), porque eso
no viaja por la API.

### 1.3 `validar_modelo.py`, `verificar_faseA.py`, hoy

```bash
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
ERRORES: ninguno
AVISOS (3): [V-06] PLA_PlanMantenimiento no es referenciada (...), [V-06] LST_ValoresLista (...),
            [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
APTO PARA DESPLEGAR
```
Línea base contra la que se compara `P-47`.

### 1.4 Qué hay realmente cableado en el editor hoy — corrida real, no supuesta

```bash
$ python scripts/auditar_cableado.py
0 correcciones en el editor
De las 39 referencias: 4 VERIFICADAS, 29 compatibles no atribuidas, 6 NO SE PUEDEN JUZGAR
  - MAN_Mantenimientos.OTID -> OT_OrdenesTrabajo (mirada a ojo el 2026-08-10, no medida)
  - OT_OrdenesTrabajo.OTOrigenID -> OT_OrdenesTrabajo (mirada a ojo el 2026-08-10, no medida)
  - (más cuatro hacia tablas vacías: CHD, CHK, FIR, FOT sobre MAN_Mantenimientos/CHK_Checklists)
```
Hay wiring parcial (33 de 39 referencias tienen al menos `Ref` puesto), pero **esta prueba no puede
confirmar desde aquí si `OTID` tiene `Initial value = UNIQUEID()` ni si `Key` está marcada**: ninguno
de los dos viaja por la API (`lectura_de_vuelta.py`, categoría `expresiones`). Es la misma
incertidumbre de `§1.2`, medida por un instrumento distinto y con el mismo resultado: no se sabe.
Esto fija la precondición de la Familia B (`§2.2`).

### 1.5 A qué instrumento se lee cada tabla — para que ninguna prueba se dispare contra el sitio ciego

`generar_plantilla.py` vacía a propósito `OT_OrdenesTrabajo`, `MAN_Mantenimientos` y
`PLA_PlanMantenimiento` en cada pasada (`VOLCADO_CIEGO_A`, `scripts/lectura_de_vuelta.py`). **Ninguna
prueba de esta tanda que toque esas tres tablas lee `BD/Modelo_Datos_PLANTILLA.xlsx`.** Se lee con
`python scripts/instantanea.py` (API) o descargando el Sheets de producción a un `.xlsx` aparte. La
única prueba que sí lee `BD/Modelo_Datos_PLANTILLA.xlsx` es `P-58`, y es sobre `EOT_EstadosOrden`,
que es catálogo y sí sobrevive entre pasadas.

## 2. Pruebas

### Familia A — Modelo (Python) y generadores, automáticas — corridas reales sobre copia temporal

Todas corridas hoy contra una copia de `scripts/` y `docs/` fuera del repositorio, con los cambios de
`ESPEC-006` §4 aplicados a mano sobre esa copia. El repositorio real queda sin tocar.

#### P-46 — El modelo todavía no tiene `RG-37`/`RG-38` (hoy falla; TDD real) — INNEGOCIABLE

- **Qué comprueba:** que el estado de partida es el que `ESPEC-006` describe, antes de que nadie
  toque nada. Es la prueba que después de `ORDEN-006` tiene que invertirse.
- **Precondición:** ninguna. Corre contra el archivo tal como está hoy.
- **Acción:**
  ```bash
  python -c "
  import sys;sys.path.insert(0,'scripts')
  from modelo_objetivo import REGLAS
  ids=[r['id'] for r in REGLAS]
  print(len(REGLAS))
  print('RG-08' in ids, 'RG-12' in ids, 'RG-37' in ids, 'RG-38' in ids)
  "
  ```
- **Resultado — hoy, corrido de verdad:** `23` / `True True False False` (ver `§1.1`).
- **Resultado esperado — después de `ORDEN-006`:** `23` / `False False True True`. El total **no
  sube a 25**: se retiran dos y se añaden dos, y `RG-08`/`RG-12` quedan como huecos numéricos, no se
  reutilizan (`ESPEC-006` §4, precedente de `ESPEC-004` con `RG-02`/`RG-19`).
- **Cómo se distingue el fallo:** si el conteo sube a 25, alguien dejó `RG-08`/`RG-12` en `REGLAS`
  además de añadir las nuevas — el modelo tendría dos mecanismos compitiendo por el mismo estado.

#### P-47 — `validar_modelo.py` y `verificar_faseA.py`, con las cifras exactas — INNEGOCIABLE

- **Qué comprueba:** que sustituir dos bots por una columna virtual y una acción no cambia ni una
  columna del modelo (`EstaVencida` nunca entra en `MODELO`) ni exige regenerar la hoja.
- **Precondición:** `ORDEN-006` aplicada sobre `scripts/modelo_objetivo.py`. La hoja NO se toca.
- **Acción:**
  ```bash
  python scripts/validar_modelo.py
  python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
  ```
- **Resultado, verificado hoy por simulación real sobre la copia temporal:**
  ```
  Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
  ERRORES: ninguno
  AVISOS (3): los mismos tres de siempre, ninguno nuevo
  APTO PARA DESPLEGAR

  AVISOS (2): [F-01] OT_OrdenesTrabajo.Activo (esperado), [F-04] 14 columnas pendientes de Ref
  FASE A CERRADA
  ```
  **`Columnas` se queda en 211** (no sube a 212): la prueba automática de que `EstaVencida` nunca
  entró en `MODELO`. **`Reglas` se queda en 23**, no sube a 25 (`P-46`). Ningún `F-02` en
  `verificar_faseA.py`: `EstaVencida` no es una de las columnas que esa regla busca en la hoja.
- **Cómo se distingue el fallo:** `Columnas` sube a 212 → `EstaVencida` se declaró como columna real
  del modelo, no virtual. Aparece un `F-02` mencionando `EstaVencida` → mismo defecto, cazado por un
  instrumento distinto.

#### P-48 — `V-11` detecta una `RG-37` mal escrita — confirma que declararla como `REGLA` la valida

- **Qué comprueba:** que la única puerta que valida la expresión de `RG-37` es estar en `REGLAS`
  (`columna="(tabla)"`, mismo molde que `RG-35`/`RG-36`), no una comparación paralela contra una
  columna de `MODELO` que no existe.
- **Precondición:** `ORDEN-006` aplicada, `validar_modelo.py` en 0 errores como línea base.
- **Acción — corrida real sobre la copia temporal:**
  ```bash
  python - <<'EOF'
  p = "scripts/modelo_objetivo.py"
  s = open(p, encoding="utf-8").read()
  old = 'expresion="AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())",'
  new = 'expresion="AND([EstadoOrden].[EsFinal] = FALSE, [FechaProgramada] < TODAY())",'
  open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
  EOF
  python scripts/validar_modelo.py
  ```
- **Resultado — corrida real hoy:**
  ```
  ERRORES (1) - el modelo no se puede desplegar asi:
    x [V-11] RG-37: 'EstadoOrden' no existe en OT_OrdenesTrabajo (ruta EstadoOrden.EsFinal)
  NO APTO: corrige los errores
  ```
  Restaurada la expresión correcta, `validar_modelo.py` vuelve a `ERRORES: ninguno` — confirmado en
  la misma corrida.
- **Cómo se distingue el fallo:** si la corrupción **no** produce error, `RG-37` no está siendo
  recorrida por `V-11` — señal de que quedó declarada de otra forma que la que `ESPEC-006` §4 fija.

#### P-49 — `generar_reconstruccion.py`: `RG-37` sale con su nombre, sin instrucción de `Label` — INNEGOCIABLE

- **Qué comprueba:** el defecto que `ESPEC-006` §2.8 encontró y que el commit `0d3d641` ya corrigió —
  que el generador asumía que toda columna virtual se llama `Etiqueta` y lleva `Label`. `RG-37` es la
  primera columna virtual que **no** es etiqueta, y es la prueba de que la corrección (`nombre_virtual`,
  `es_label`) funciona con un caso real, no solo con los dos que ya existían.
- **Precondición:** `ORDEN-006` aplicada. Generadores ya corregidos (commit `0d3d641`, verificado
  antes de escribir esta prueba).
- **Acción — corrida real sobre la copia temporal:**
  ```bash
  python scripts/generar_reconstruccion.py
  grep -n "RG-37" -A6 docs/sdd/RECONSTRUCCION_EXPRESIONES.md
  ```
- **Resultado, corrida real hoy** — bloque tal cual quedó escrito en `RECONSTRUCCION_EXPRESIONES.md`:

  ~~~
  ### RG-37 — `OT_OrdenesTrabajo` · `(tabla)`

  **Tipo:** App formula · cubre D-06

  > **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con
  > *Data > Columns > `Add virtual column`*, se llama **`EstaVencida`**, y lleva esa expresión
  > en su `App formula`.

  ```
  AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())
  ```
  ~~~

  Se llama **`EstaVencida`**, no `Etiqueta`. **No aparece ninguna línea sobre `Show?`/`Label`** —esa
  línea sí sale para `RG-35`/`RG-36`, que tienen `es_label=True`; `RG-37` no lo tiene, y el generador
  filtra por `r.get("es_label")`, verificado leyendo el código antes de correrlo.
- **Cómo se distingue el fallo:** si el bloque dice `se llama **Etiqueta**`, o incluye la línea de
  `Show?`/`Label` para `RG-37`, el defecto que `ESPEC-006` §2.8 documentó sigue vivo pese al commit
  `0d3d641` — hay que revisar si la corrección se deshizo.

#### P-50 — `generar_prompt_cableado.py`: `RG-37` no entra en la tabla de `Label` a marcar — INNEGOCIABLE

- **Qué comprueba:** el mismo defecto que `P-49`, en el segundo generador. Su «Paso 5 — La etiqueta
  de cada tabla» filtra las columnas virtuales por `r.get("es_label")` antes de listar cuáles hay que
  crear con `Show?`/`Label`; `RG-38` (tipo `Accion`, no `App formula`) tampoco debe aparecer ahí.
- **Precondición:** igual que `P-49`.
- **Acción — corrida real sobre la copia temporal:**
  ```bash
  python scripts/generar_prompt_cableado.py
  grep -n "RG-37\|RG-38\|EstaVencida" docs/PROMPT_CABLEADO.md
  ```
- **Resultado, corrida real hoy:**
  ```
  274:| `EOT_EstadosOrden` | `EsFinal` | **`Yes/No`** | `RG-37` | ...
  280:| `OT_OrdenesTrabajo` | `EstadoOrdenID` | **`Ref`** → `EOT_EstadosOrden` | `RG-37` | ...
  283:| `PLA_PlanMantenimiento` | `Activo` | **`Yes/No`** | `RG-38` | ...
  ```
  Las tres apariciones son de la tabla de tipos del Paso 4 (`RG-37`/`RG-38` como la regla que
  necesita esa columna **real** bien tipada), no del Paso 5. **Ni `RG-37` ni `RG-38` aparecen en la
  tabla `| Tabla | Referencias que la apuntan | Label |` del Paso 5** — se confirmó leyendo el
  documento completo generado, no solo el `grep`: esa tabla lista 20 filas, todas de columnas
  `es_label=True` reales (`RG-35`/`RG-36` entre ellas, como `OT_OrdenesTrabajo` → `Etiqueta`).
- **Cómo se distingue el fallo:** `RG-37` o `RG-38` aparecen en la tabla del Paso 5 con `Label`
  marcado — instruiría al ejecutor a marcar `Label` sobre una columna que no lo es, desplazando el
  `Label` legítimo (`Etiqueta`, puesto por `RG-35`) y dejando el desplegable de `OT_OrdenesTrabajo`
  sin etiqueta legible.

### Familia B — Configuración (AppSheet) y datos, ejercicio real de la app: el fixture

**Decisión sobre el fixture, y el criterio — se pide explícitamente en el encargo de esta tanda.**
`OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` siguen en cero (`§1.2`), y cualquier prueba de `RG-37`
o `RG-38` con datos reales exige crear filas ahí, lo que cierra la ventana barata para siempre —
igual que ya advirtió `ESPEC-005`/`PRUEBA-005` sobre las mismas dos tablas. La decisión no es la
misma para las dos reglas:

- **`RG-37` entra en esta tanda.** Es de solo lectura: no escribe en `OT_OrdenesTrabajo`, no depende
  de que `OTID` tenga `Initial value = UNIQUEID()` ni `Key` marcada — lee `EstadoOrdenID` y
  `FechaProgramada`, dos columnas que ya tienen wiring parcial hoy (`§1.4`). Su fixture se escribe
  completo (`P-51` a `P-55`, `P-61`), listo para que el ejecutor lo corra en cuanto `RG-37` esté
  cableada en el editor.
- **`RG-38` se aplaza.** No por pereza: por una dependencia que `ESPEC-006` §6 ya declara y que esta
  prueba no puede saltarse. La acción de `RG-38` es `Data: add a new row to another table using
  values from this row` sobre `OT_OrdenesTrabajo`, y **no se puede cablear en el editor hasta que
  `OTID` tenga `Initial value = UNIQUEID()` puesto** — la misma condición que ya vale para `RG-10`.
  Esa condición es exactamente `P-09` de `PRUEBA-005`, y `§1.2`/`§1.4` de este documento confirman
  que sigue `NO EJECUTADA`. `RG-38` (`P-56`, `P-57`, `P-62`) se escribe completa, con los cinco
  campos, y se marca `BLOQUEADA POR` esa dependencia (`§3`).
- **Recomendación de secuencia, no una prueba:** cuando la dependencia de `RG-38` se resuelva
  (`PRUEBA-005` `P-09`), conviene ejecutar en la misma sesión de editor el fixture de `RG-37` de esta
  tanda y el de `PRUEBA-005` — los dos exigen la misma sesión de `USR-002`, la misma desactivación de
  `RG-07`, y los dos van a cerrar la misma ventana de las mismas dos tablas. Ejecutarlos por separado
  duplica el costo de sesión sin necesidad.

**Precondición común a toda la Familia B:**

1. `RG-37` cableada en el editor: columna virtual `EstaVencida` (`Yes/No`), `App formula` con la
   expresión de `RG-37`, `Show?` activo (sin esto la columna no se lee por API — es la vía por la
   que `P-51` a `P-54` la leen de vuelta).
2. Sesión iniciada como `USR-002` (`ivan.salcedo@concesiondelsisga.com.co`, técnico, `ROL-03`,
   confirmado hoy contra `USR_Usuarios`).
3. **`RG-07` (bot, `OT_OrdenesTrabajo`, evento `Adds`) se desactiva antes de crear la primera fila.**
   Esta tanda crea 3 filas en `OT_OrdenesTrabajo` (`P-51`, `P-52`, `P-53`) más una fila en
   `MAN_Mantenimientos` (`P-55`): sin desactivarlo, dispara hasta 3 correos reales a
   `ivan.salcedo@concesiondelsisga.com.co`, una dirección corporativa, sobre órdenes marcadas `TEST`.
   Se desactiva en `Automation > Bots` → `RG-07` → `Disable`, y se reactiva en `P-60`, último paso de
   esta tanda. Misma cita que usa `PRUEBA-005`: *"You can disable the bot... Then, re-enable it"* —
   [Bots: The Essentials](https://support.google.com/appsheet/answer/11432969?hl=en).
4. **Identificación del fixture, en dos caminos posibles, porque no se sabe desde aquí si `OTID`
   admite escritura hoy (`§1.4`):** si el campo `OTID` del formulario acepta texto, se teclea
   `TEST-OT-006A`/`B`/`C`; si ya está de solo lectura (`ORDEN-005` aplicada primero), la fila se
   identifica por `Observaciones` conteniendo `"PRUEBA-006"` y por el `diff` de `instantanea.py`,
   igual que `PRUEBA-005` §1.1 hace para su propio fixture. Ningún resultado de esta prueba depende
   de que la clave sea un literal.

#### P-51 — `RG-37` positiva: orden vencida ("fecha pasada y sin cerrar", tal cual pide el encargo)

- **Qué comprueba:** que una orden con `FechaProgramada` pasada y `EstadoOrdenID` no final sale
  `EstaVencida = Y`.
- **Precondición:** Familia B, precondición común.
- **Acción:** en `OT_OrdenesTrabajo`, `+`: `ActivoID = ACT-0001`, `TecnicoID = USR-002`,
  `SupervisorID = USR-006`, `Tipo = Correctivo`, `FechaProgramada` = hoy − 3 días, `EstadoOrdenID =
  Asignada`, `Observaciones = "TEST — PRUEBA-006, borrar tras P-60 (fixture A, RG-37 positiva)"`.
  `SAVE`. Fixture identificado como **A**.
  ```bash
  python scripts/instantanea.py guardar prueba-006-antes-fixture
  # crear fixture A en la app
  python scripts/instantanea.py guardar prueba-006-despues-A
  python scripts/instantanea.py comparar prueba-006-antes-fixture prueba-006-despues-A
  ```
- **Resultado esperado:** el `comparar` muestra una fila nueva en `OT_OrdenesTrabajo`, y su columna
  `EstaVencida` es `Y` (leída vía API, con el mismo formato `Y`/`N` que ya usa `EOT_EstadosOrden.EsFinal`
  hoy, §1.2). Ninguna otra tabla cambia.
- **Cómo se distingue el fallo:** `EstaVencida` sale `N`, vacía, o no aparece en absoluto en el `Find`
  — esta última señal indica que `Show?` no está activo (precondición 1, no cableada).

#### P-52 — `RG-37` negativa: fecha futura — INNEGOCIABLE

- **Qué comprueba:** que una orden con `FechaProgramada` futura, aunque no esté cerrada, **no** sale
  vencida. Sin este caso, una expresión que devolviera `TRUE` siempre pasaría `P-51` igual.
- **Precondición:** `P-51` completada.
- **Acción:** igual que `P-51`, `FechaProgramada` = hoy + 10 días, `Observaciones = "TEST —
  PRUEBA-006, borrar tras P-60 (fixture B, RG-37 negativa: fecha futura)"`. Fixture **B**.
  ```bash
  python scripts/instantanea.py guardar prueba-006-despues-B
  python scripts/instantanea.py comparar prueba-006-despues-A prueba-006-despues-B
  ```
- **Resultado esperado:** una fila nueva en `OT_OrdenesTrabajo`, `EstaVencida = N`.
- **Cómo se distingue el fallo:** `EstaVencida` sale `Y` con fecha futura — la comparación
  `[FechaProgramada] < TODAY()` no se está evaluando, o se invirtió el signo.

#### P-53 — `RG-37` negativa: orden ya cerrada — INNEGOCIABLE

- **Qué comprueba:** que una orden en el estado final `Cerrada`, aunque su fecha ya pasó, **no** sale
  vencida — la otra mitad del caso negativo que pide el encargo ("una ya cerrada"), aislada de si
  alguien la cerró tarde o a tiempo: aquí se crea directamente en `Cerrada`.
- **Precondición:** `P-52` completada.
- **Acción:** igual que `P-51`, `FechaProgramada` = hoy − 3 días, **`EstadoOrdenID = Cerrada`** desde
  la creación, `Observaciones = "TEST — PRUEBA-006, borrar tras P-60 (fixture C, RG-37 negativa: ya
  cerrada)"`. Fixture **C**.
  ```bash
  python scripts/instantanea.py guardar prueba-006-despues-C
  python scripts/instantanea.py comparar prueba-006-despues-B prueba-006-despues-C
  ```
- **Resultado esperado:** una fila nueva, `EstaVencida = N`, pese a que `FechaProgramada` está en el
  pasado — porque `EstadoOrdenID.EsFinal = TRUE` invalida la primera mitad del `AND`.
- **Cómo se distingue el fallo:** `EstaVencida` sale `Y` — la expresión no está desreferenciando
  `EsFinal` correctamente, o el `AND` se volvió un `OR`.

#### P-54 — El caso del tipo: `EstaVencida` devuelve `Y`/`N`, no `Text` — INNEGOCIABLE

- **Qué comprueba, con el método que ya cazó el mismo defecto una vez.** `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`
  `S-30` documenta que la API devuelve el literal `Y`/`N` para una columna `Yes/No`, y devuelve el
  contenido crudo para una `Text` — y que `MAN_Mantenimientos.CierreConExcepcion` salió `Text` una
  vez, en silencio, dejando `RG-03` sin efecto porque comparar texto contra el booleano `TRUE` es
  siempre falso y no da error. `EstaVencida` es virtual y nueva, así que no hay ningún `F-XX` de
  `verificar_faseA.py` que la vaya a mirar nunca — nunca entra en `MODELO` (`P-47`). Esta es la única
  prueba de esta tanda que puede cazar que quedó `Text` en el editor.
- **Precondición:** `P-51`, `P-52` y `P-53` completadas (reutiliza los fixtures A, B y C).
- **Acción:**
  ```bash
  python -c "
  import json
  a = json.load(open('BD/instantaneas/prueba-006-despues-A.json', encoding='utf-8'))
  c = json.load(open('BD/instantaneas/prueba-006-despues-C.json', encoding='utf-8'))
  fA = [r for r in a['OT_OrdenesTrabajo'] if 'fixture A' in (r.get('Observaciones') or '')][0]
  fC = [r for r in c['OT_OrdenesTrabajo'] if 'fixture C' in (r.get('Observaciones') or '')][0]
  print('A (esperado vencida):', repr(fA.get('EstaVencida')))
  print('C (esperado NO vencida):', repr(fC.get('EstaVencida')))
  "
  ```
- **Resultado esperado:** `A` es exactamente el string `'Y'` y `C` es exactamente el string `'N'` —
  el mismo formato que ya se verificó para `EOT_EstadosOrden.EsFinal` en `§1.2`. **Cualquier otro
  literal es el defecto**, no una variante aceptable: ni `'TRUE'`/`'FALSE'`, ni `'true'`/`'false'`,
  ni `'1'`/`'0'`, ni una cadena vacía.
- **Cómo se distingue el fallo:** si `A` devuelve algo distinto de `'Y'` (por ejemplo `'true'`), la
  columna quedó `Text` en el editor — la expresión sigue siendo lógicamente correcta (por eso `P-51`
  a `P-53` podrían parecer que "funcionan" si solo se mira si el valor es truthy en un cotejo a ojo
  descuidado), pero cualquier `Valid_If`/`Security Filter` futuro que compare `[EstaVencida] = TRUE`
  fallaría siempre y en silencio — exactamente la forma del defecto de `CierreConExcepcion` (`S-30`).

#### P-55 — `RG-37` NO impide cerrar — el defecto que tenía `RG-08` — INNEGOCIABLE

- **Qué comprueba:** el punto 2 del encargo. Con `RG-08`, una orden que pasaba de fecha se movía a
  `Vencida` (`EsFinal = Y`) automáticamente, y el técnico que llegaba tarde ya no podía registrar el
  mantenimiento — el estado bloqueaba el cierre antes de que la evidencia se capturara. Con `RG-37`,
  el fixture **A** (`P-51`, 3 días vencido, `EstadoOrdenID` sigue en `Asignada`) demuestra que el
  técnico **todavía puede** abrir y cerrar esa orden con normalidad.
- **Precondición:** `P-54` completada (para no perder la lectura de `EstaVencida = Y` de `A` antes de
  cerrarla).
- **Acción:** con la sesión de `USR-002`, abrir el fixture **A**, iniciar un mantenimiento,
  `EstadoActivoID = EST-01`, cerrar con `Coordenadas_Cierre_LatLong` capturada en la coordenada de
  `ACT-0001` (`5.099798, -73.718568`), `Observaciones = "TEST — PRUEBA-006, borrar tras P-60 (cierre
  de fixture A)"`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-006-despues-cierre-A
  python scripts/instantanea.py comparar prueba-006-despues-C prueba-006-despues-cierre-A
  ```
- **Resultado esperado:** el cierre se guarda sin ningún error ni bloqueo del formulario —
  `EstadoOrdenID` del fixture A pasa a `Cerrada`, y `MAN_Mantenimientos` gana una fila nueva. Como
  consecuencia, no como algo que haya que forzar, `EstaVencida` de A se recalcula a `N` en la misma
  lectura (mismo motivo que `P-53`: ya es final).
- **Cómo se distingue el fallo:** el formulario rechaza el cierre, o `EstadoOrdenID` no cambia a
  `Cerrada` — señal de que algo (una `Valid_If` mal escrita, o un `RG-08` que no se retiró) sigue
  tratando la orden como si estuviera en un estado terminal antes de que el técnico actúe.

#### P-56 — `RG-38` positiva: la acción crea la fila, y sólo esa — BLOQUEADA POR PRUEBA-005 `P-09`

- **Qué comprueba:** qué escribe la acción de `RG-38`, sobre qué, y que no toca nada más. El mapeo
  exacto está cerrado en `ESPEC-006` §3.2 y se repite aquí para que esta prueba sea autocontenida.
- **Precondición:** `RG-38` cableada — vista/slice `"Vence en 7 días"` sobre `PLA_PlanMantenimiento`
  con la condición `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)`, y la acción `Data: add a
  new row to another table using values from this row` con el mapeo de `§3.2` de `ESPEC-006`. **Y,
  antes que nada: `OT_OrdenesTrabajo.OTID` con `Initial value = UNIQUEID()` y `Key` marcada** —
  `PRUEBA-005` `P-09`, confirmado `NO EJECUTADA` (`§1.2`, `§1.4`). Sin esto la acción no se puede
  cablear siquiera (`ESPEC-006` §6), así que esta prueba **no puede empezar**.
- **Acción, cuando la precondición se cumpla:** con la sesión de operación (o `USR-002`), crear en
  `PLA_PlanMantenimiento`: `ActivoID = ACT-0001`, `FrecuenciaID = FRE-04` (Mensual, 30 días),
  `UltimaEjecucion` = hoy − 25 días (de modo que `ProximaFecha` calculada por `RG-11` cae en 5 días,
  dentro de la ventana de 7), `ResponsableID = USR-002`, `Activo = TRUE`. Confirmar a ojo que la fila
  aparece en la vista `"Vence en 7 días"`. Pulsar la acción sobre esa fila.
  ```bash
  python scripts/instantanea.py guardar prueba-006-antes-rg38
  # pulsar la accion
  python scripts/instantanea.py guardar prueba-006-despues-rg38
  python scripts/instantanea.py comparar prueba-006-antes-rg38 prueba-006-despues-rg38
  ```
- **Resultado esperado:** el `comparar` muestra **una sola** fila nueva, en `OT_OrdenesTrabajo`, con
  `ActivoID` = el mismo `ACT-0001`, `TecnicoID` = `USR-002` (copiado de `ResponsableID`),
  `SupervisorID` = quien pulsó la acción (vía `LOOKUP(USEREMAIL()...)`), `Tipo = Preventivo` (literal),
  `FechaProgramada` = la `ProximaFecha` del plan, `EstadoOrdenID = Programada` (literal). `OTID` no
  vacío. Ninguna otra fila de `PLA_PlanMantenimiento` cambia — la fila origen sigue igual, la acción
  no la modifica, solo lee de ella.
- **Cómo se distingue el fallo:** aparece más de una fila nueva, o la fila nueva tiene algún campo
  obligatorio vacío (en particular `TecnicoID`, si `ResponsableID` estaba vacío en el plan — riesgo ya
  declarado en `ESPEC-006` §3.2 y §6), o cambió algo en `PLA_PlanMantenimiento` además de lo esperado.

#### P-57 — `RG-38` negativa: fuera de la ventana de 7 días, la acción no se puede disparar — BLOQUEADA POR PRUEBA-005 `P-09`

- **Qué comprueba:** que la condición del slice sí filtra, y no expone la acción sobre cualquier fila
  del plan.
- **Precondición:** igual que `P-56`.
- **Acción:** crear una segunda fila en `PLA_PlanMantenimiento` con `UltimaEjecucion` = hoy (de modo
  que `ProximaFecha` cae en 30 días, fuera de la ventana), mismos `ActivoID`/`FrecuenciaID`/
  `ResponsableID`. Confirmar a ojo, en la vista `"Vence en 7 días"`, que esta fila **no aparece** —
  como control cruzado, el mismo par `(ActivoID, ProximaFecha)` se recalcula en Python con la misma
  condición del slice (`AND(Activo=TRUE, ProximaFecha <= hoy+7)`) para confirmar que el resultado
  esperado no es una lectura optimista.
  ```bash
  python scripts/instantanea.py guardar prueba-006-fila-fuera-ventana
  ```
- **Resultado esperado:** la fila no aparece en la vista, y no hay ningún botón de acción disponible
  sobre ella (no hay acción posible sobre una fila fuera del slice al que está ligada). El
  `instantanea.py` de control confirma que `PLA_PlanMantenimiento` sigue con la fila (existe, no
  desapareció) pero `OT_OrdenesTrabajo` no gana ninguna fila atribuible a ella.
- **Cómo se distingue el fallo:** la fila aparece en la vista, o el botón de acción está disponible
  sobre ella — la condición del slice está mal escrita o no se aplicó.

### Familia C — Datos (Sheets), lectura de vuelta y cierre del fixture

#### P-58 — `EOT_EstadosOrden.QuienCambia` llegó a la hoja (`BD/Modelo_Datos_PLANTILLA.xlsx`)

- **Qué comprueba:** la primera de las dos superficies que `ESPEC-006` §6 exige tocar a mano —la hoja
  local—, y que **solo** cambió esa celda, ninguna otra de las siete filas de `EOT_EstadosOrden`.
- **Precondición:** el ejecutor editó a mano la fila `Vencida` de `EOT_EstadosOrden` en
  `BD/Modelo_Datos_PLANTILLA.xlsx`, cambiando `QuienCambia` de `Sistema` a `Supervisor`. Ningún otro
  valor de esa fila ni de las otras seis se toca.
- **Acción:**
  ```bash
  python -c "
  import openpyxl
  wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True)
  for r in wb['EOT_EstadosOrden'].iter_rows(min_row=2, values_only=True):
      print(r)
  "
  ```
- **Resultado esperado:** exactamente las siete filas de `§2.2` de `ESPEC-006`, con **una sola
  diferencia**: `('Vencida', 'Vencida', 7, 'Supervisor', 'TRUE', 'TRUE')` — `EsFinal` sigue en
  `'TRUE'`, solo cambió `QuienCambia`. Las otras seis filas, carácter por carácter, iguales a las
  citadas en `ESPEC-006` §2.2.
- **Cómo se distingue el fallo:** cualquier otra celda de la tabla cambió (por ejemplo, `EsFinal` de
  `Vencida` pasó a `FALSE`, deshaciendo la decisión de `ESPEC-006` §3.1 en vez de aplicarla), o
  `QuienCambia` sigue en `Sistema`.

#### P-59 — `EOT_EstadosOrden.QuienCambia` llegó a la aplicación — INNEGOCIABLE

- **Qué comprueba:** la segunda superficie, la que de verdad ve el usuario — sin esto, `P-58` solo
  demostraría que el archivo local cambió, no que la app lo hizo. Es la prueba de lectura de vuelta
  de este punto del encargo (§0, punto 5).
- **Precondición:** `P-58` completada, y el ejecutor aplicó el mismo cambio en el Sheets de
  producción `Modelo_Datos_10082026`.
- **Acción, con dos instrumentos independientes:**
  ```bash
  python scripts/instantanea.py guardar prueba-006-quiencambia
  python -c "
  import json
  d = json.load(open('BD/instantaneas/prueba-006-quiencambia.json', encoding='utf-8'))
  for r in d['EOT_EstadosOrden']:
      print(r['EstadoOrdenID'], '| EsFinal=', r['EsFinal'], '| QuienCambia=', r['QuienCambia'])
  "
  ```
  Y, como segunda vía, abrir `Modelo_Datos_10082026` con el conector de Drive —descargando el Sheets
  a un `.xlsx` aparte, no con `python scripts/sistema.py`, que no descarga nada— y leer la misma fila
  a ojo.
- **Resultado esperado:** las dos vías muestran, para `Vencida`: `EsFinal = Y`, `QuienCambia =
  Supervisor`. Las otras seis filas, iguales a `§1.2` de este documento. Las dos vías coinciden entre
  sí.
- **Cómo se distingue el fallo:** la API sigue devolviendo `QuienCambia = Sistema` (el cambio se hizo
  solo en el archivo local, no en el Sheets real — `P-58` pasaría y esta fallaría, la señal exacta de
  que faltó la segunda superficie), o las dos vías no coinciden entre sí.

#### P-60 — Cierre del fixture, sin `Delete`, y reactivación de `RG-07` — INNEGOCIABLE

- **Qué comprueba:** que el fixture de `RG-37` (fixtures A, B, C de `OT_OrdenesTrabajo`, y la fila de
  `MAN_Mantenimientos` de `P-55`) se cierra siguiendo la política vigente del proyecto —la misma que
  fija `PRUEBA-005` §2, `P-13`: **nunca `Action: Delete`**, se marca `Activo = FALSE`—, y que `RG-07`
  queda reactivado.
- **Precondición:** `P-51` a `P-55` ejecutadas. Existen 3 filas en `OT_OrdenesTrabajo` (A, B, C) y 1
  en `MAN_Mantenimientos`.
- **Acción:**
  ```bash
  python - <<'EOF'
  import sys; sys.path.insert(0, "scripts")
  from appsheet_api import ejecutar_accion

  for tabla, clave_col, claves in [
      ("OT_OrdenesTrabajo", "OTID", ["<clave-A>", "<clave-B>", "<clave-C>"]),
      ("MAN_Mantenimientos", "MantenimientoID", ["<clave-manA>"]),
  ]:
      filas = [{clave_col: c, "Activo": False} for c in claves]
      ejecutar_accion(tabla, "Edit", filas=filas)
  EOF
  python scripts/instantanea.py guardar prueba-006-tras-cierre
  ```
  Las claves reales son las que `instantanea.py comparar` devolvió en `P-51`/`P-53`/`P-55` (o los
  literales `TEST-OT-006A/B/C` si `OTID` admitía escritura — `§2.2` precondición 4), nunca un literal
  supuesto.
- **Último paso: reactivar `RG-07`** (`Automation > Bots` → `RG-07` → `Enable`). Sin comando que lo
  lea de vuelta (`lectura_de_vuelta.py`, categoría `expresiones`): se cierra copiando literalmente el
  estado que muestra `Automation > Bots` para `RG-07` tras pulsar `Enable`.
- Borrar del disco `BD/instantaneas/prueba-006-*.json` (higiene, `SDD_PIPELINE_SGMC.md` §5.1).
- **Resultado esperado:** las 4 filas siguen existiendo, con `Activo = FALSE` — `OT_OrdenesTrabajo` y
  `MAN_Mantenimientos` **no vuelven a cero**, y no es un fallo: es la misma decisión ya tomada en
  `PRUEBA-005`. `RG-07` muestra `Enable`/`On` tras el último paso.
- **Cómo se distingue el fallo:** alguna celda fuera de las 4 filas de prueba cambió, el cierre usó
  `Delete` en vez de `Edit` con `Activo = FALSE`, o `RG-07` quedó desactivado al terminar la tanda —
  dejar eso así sería resolver el riesgo de correos de esta prueba creando uno permanente sobre
  producción.

### Familia D — Configuración (AppSheet), cotejo a ojo — sin comando posible

`lectura_de_vuelta.py` declara que 4 de las 7 clases de cambio no tienen comprobación mecánica:
`tipos`, `expresiones`, `permisos`, `etiqueta`. `P-54` ya cubre `tipos` por la vía indirecta de `S-30`
(contenido, no esquema). Lo que sigue es la categoría `expresiones`, que **no tiene ningún atajo**:
un `App formula` no viaja por la API bajo ninguna forma, ni siquiera indirecta.

#### P-61 — La `App formula` de `EstaVencida`, copiada literal del editor

- **Qué comprueba:** que lo que quedó escrito en `Data > Columns > EstaVencida > App formula` es,
  carácter por carácter, la expresión que `RG-37` declara — no una que "hace lo mismo" a ojo. Es la
  prueba que ninguna de `P-51` a `P-55` puede reemplazar: todas ellas confirman el **resultado**, no
  el **texto** de la fórmula, y dos fórmulas distintas pueden coincidir en los tres fixtures de esta
  tanda y diferir en un caso que nadie probó.
- **Precondición:** `RG-37` cableada.
- **Acción:** en *Data > Columns* de `OT_OrdenesTrabajo`, abrir `EstaVencida`, copiar literalmente el
  contenido del campo `App formula`.
- **Resultado esperado:** `AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`,
  carácter por carácter igual a `RG-37` (`ESPEC-006` §4) y a lo que tenía `RG-08` como bot (`ESPEC-006`
  §3, tabla: "Misma expresión exacta").
- **Cómo se distingue el fallo:** cualquier diferencia de carácter — un espacio de más, `<=` en vez
  de `<`, un paréntesis movido. `P-51` a `P-55` no habrían cazado, por ejemplo, `<=` en vez de `<`
  salvo que alguno de los fixtures tuviera `FechaProgramada` exactamente igual a hoy, y ninguno lo
  tiene.

#### P-62 — El mapeo de columnas de la acción de `RG-38`, copiado literal del editor — BLOQUEADA POR PRUEBA-005 `P-09`

- **Qué comprueba:** lo mismo que `P-61`, para la acción de `RG-38`: que `Set these columns` tiene
  exactamente el mapeo de `ESPEC-006` §3.2, no una aproximación que produjo las filas correctas en
  `P-56` por casualidad de los valores usados en ese fixture concreto.
- **Precondición:** igual que `P-56`.
- **Acción:** en `Data > Actions` de `PLA_PlanMantenimiento`, abrir la acción de `RG-38`, copiar
  literalmente la tabla `Set these columns`, y en `Data > Slices`, copiar literalmente la condición
  de la vista `"Vence en 7 días"`.
- **Resultado esperado:** las seis filas de la tabla de `ESPEC-006` §3.2, exactas, y la condición
  `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)`.
- **Cómo se distingue el fallo:** cualquier columna mapeada distinto (en particular
  `SupervisorID`, cuya expresión `LOOKUP(USEREMAIL()...)` es fácil de escribir con el nombre de tabla
  o columna cambiado sin que el editor proteste), o la condición del slice con `<` en vez de `<=`.

## 3. Pruebas bloqueadas

- **`P-56`, `P-57` y `P-62` (todo `RG-38`).** **BLOQUEADA POR** que `OT_OrdenesTrabajo.OTID` no tiene
  todavía `Initial value = UNIQUEID()` ni `Key` marcada en el editor de la aplicación viva —
  `PRUEBA-005` `P-09`, confirmado `NO EJECUTADA` en `ACTA-005-pruebas.md` y en el conteo de filas de
  `§1.2` de este documento. `ESPEC-006` §6 ya declara esta dependencia; esta prueba solo la hereda,
  no la crea. Se desbloquea en cuanto `PRUEBA-005` `P-09` pase.
- **El cotejo exacto del texto de `EstaVencida` (`P-61`) y de la acción de `RG-38` (`P-62`)**, en la
  parte de `P-62`, hereda el mismo bloqueo que `P-56`/`P-57`: no se puede copiar el `Set these
  columns` de una acción que no se puede crear todavía. `P-61` (`RG-37`) no está bloqueada.
- **`RG-12` en ejecución real con plan pagado**, y en general cualquier comparación contra el
  comportamiento del bot que `RG-38` reemplaza: sigue fuera de alcance, igual que ya lo declaró
  `PRUEBA-005` sobre `RG-12`. No se prueba aquí porque no es lo que `ESPEC-006` decide — decide
  reemplazar el bot, no evaluarlo.

## 4. Criterio de cierre

**Tienen que pasar todas las que no estén `BLOQUEADA POR` en el momento de ejecutar**, y en concreto:

- `P-46` y `P-47` son la condición de entrada: si alguna falla, `ORDEN-006` está incompleta o rompió
  algo del modelo que no debía tocar.
- `P-48` confirma que declarar `RG-37` como `REGLA` (no columna de `MODELO`) la deja validada, mismo
  patrón que `PRUEBA-005` `P-03` ya estableció para `RG-35`.
- `P-49` y `P-50` son la condición explícita de esta tanda sobre el commit `0d3d641`: sin ellas, no
  hay evidencia de que la corrección de los generadores sobreviva a un caso real, solo a los dos que
  ya existían.
- `P-51`, `P-52`, `P-53` cierran el punto 1 del encargo (positiva y las dos negativas). Ninguna sola
  basta: `P-51` sin `P-52`/`P-53` no descarta una expresión que devuelva `TRUE` siempre.
- `P-54` cierra el punto 4 (el tipo) y es la única prueba de esta tanda con esa capacidad — no hay
  ninguna otra vía mecánica para detectar `EstaVencida` como `Text`.
- `P-55` cierra el punto 2, el defecto original de `RG-08` que esta especificación existe para
  corregir. Es, junto con `P-54`, la prueba de mayor peso de la tanda.
- `P-58` y `P-59` cierran el punto 5. Las dos son necesarias: `P-58` sin `P-59` deja abierta la
  posibilidad de que el cambio solo se aplicó en el archivo local y nunca llegó a producción.
- `P-60` cierra el fixture y confirma que `RG-07` no quedó desactivado sobre producción — condición
  de cierre no negociable de cualquier tanda que haya tocado `OT_OrdenesTrabajo`.
- `P-61` documenta la fórmula literal; no es innegociable pero tiene que quedar copiada, no resumida.
- `P-56`, `P-57` y `P-62` **no** entran en el criterio de cierre de esta tanda mientras sigan
  bloqueadas. Entran en el criterio de cierre del día en que `PRUEBA-005` `P-09` pase — a partir de
  ahí, son innegociables para dar `RG-38` por probada.
- **A partir del cierre de `P-60`, `OT_OrdenesTrabajo` y `MAN_Mantenimientos` dejan de estar en cero**
  (`PLA_PlanMantenimiento` sigue en cero hasta que `RG-38` se desbloquee): cualquier especificación
  futura sobre esas dos tablas tiene que asumirlo, igual que `PRUEBA-005` §4 ya advirtió para su
  propio fixture.
