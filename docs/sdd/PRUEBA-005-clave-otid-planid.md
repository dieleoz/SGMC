# PRUEBA-005 — Pruebas de aceptación de ESPEC-005

**Escrita antes de que `ORDEN-005` exista.** Nada de lo que sigue se ejecutó contra el modelo, la
hoja ni el editor. Los comandos marcados «automática» sí se corrieron —son de solo lectura, o
corren sobre una copia temporal fuera del repositorio para predecir el resultado exacto— y sus
salidas están citadas literalmente. Los que requieren la app están descritos para cuando el
ejecutor los corra, no ejecutados aquí. No se tocó `scripts/modelo_objetivo.py` ni ningún otro
archivo del repositorio.

| | |
|---|---|
| Cubre | [`ESPEC-005-clave-otid-planid.md`](ESPEC-005-clave-otid-planid.md): `OTID` y `PlanID` pasan de `CLAVE_LEGIBLE` a `CLAVE_GENERADA` (`Initial value = UNIQUEID()`), columna `Etiqueta` nueva en `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` (`App formula`, `Label`) |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Volcado hoy con `python scripts/sistema.py`, no copiado de una tanda anterior |
| Reglas que esta tanda tiene que probar | Ninguna regla de `REGLAS` cambia de expresión. Lo que cambia es que `RG-10` y `RG-12` dejan de crear filas huérfanas, y aparece un hallazgo: las dos `App formula` de `Etiqueta` **no tienen `REGLA` propia** en el diseño de `ESPEC-005` §4 — ver `P-07` |
| Innegociables | `P-01`, `P-06`, `P-07`, `P-09`, `P-11`, `P-12`, `P-13` |

## 0. Los cinco puntos del encargo, y dónde se prueban cada uno

| # | Punto del encargo | Prueba(s) |
|---|---|---|
| 1 | Un bot crea una orden y esa orden EXISTE | `P-11` |
| 2 | La prueba negativa | `P-12` (y su justificación, más abajo) |
| 3 | `Key` queda en la columna, no en `_RowNumber`, sin sembrar | `P-09` |
| 4 | La columna `Etiqueta` escribe | `P-13` (sobre cuántas filas) y `P-07` (dónde queda documentada su fórmula, o no) |
| 5 | `OT_OrdenesTrabajo` admite creación desde la app | `P-10` |

## 1. Estado de partida

### 1.1 Filas de las tablas implicadas, hoy, contra la aplicación viva

```
$ python scripts/instantanea.py guardar prueba-005-partida
Guardada: BD/instantaneas/prueba-005-partida.json
28 tablas · 953 filas en total
```
```
OT_OrdenesTrabajo    0
PLA_PlanMantenimiento 0
MAN_Mantenimientos   0
ACT_Activos          368
USR_Usuarios         11
EOT_EstadosOrden     7
FRE_Frecuencias      8
```
Coincide con `BD/Modelo_Datos_PLANTILLA.xlsx` leído por `openpyxl` (mismo conteo que
`ESPEC-005` §2.1). La instantánea se borró después de leerla, siguiendo la higiene de
`SDD_PIPELINE_SGMC.md` §5.1: no queda ningún archivo de prueba en el repositorio por este paso.

**Las dos tablas que este cambio toca están en cero, y las cuatro de las que su fixture depende
—`ACT_Activos`, `USR_Usuarios`, `EOT_EstadosOrden`, `FRE_Frecuencias`— ya tienen datos reales.**
Es la misma situación que resolvió `PRUEBA-004` §1.2, y el criterio es el mismo: **el fixture
entra**, reutilizando las cuatro tablas pobladas sin tocarlas, y creando únicamente filas nuevas en
`OT_OrdenesTrabajo` y `MAN_Mantenimientos` — nunca en las cuatro reutilizadas. Aplazar la creación
de esas filas aplazaría exactamente la prueba que el encargo llama «la que de verdad importa»
(`P-11`): sin una orden real creada por `RG-10`, no hay evidencia de que el mecanismo funcione,
solo de que el modelo describe uno.

**Diferencia con el fixture de `PRUEBA-004`, y por qué importa:** ahí la clave de la orden se podía
escribir a mano (`OTID = TEST-OT-004A`) porque `OTID` no tenía `Initial value` todavía. **Aquí ya
no.** Tras `ORDEN-005`, `OTID` y `PlanID` los genera `UNIQUEID()` y su valor no se elige. La marca
`TEST` no puede ir en la clave; va en `Observaciones` (`OT_OrdenesTrabajo` la tiene). La
identificación y el borrado posterior del fixture se hacen por ese campo, nunca por la clave — ver
`P-13`.

### 1.2 `validar_modelo.py`, `verificar_faseA.py`, `verificar_datos.py`, hoy

```
$ python scripts/validar_modelo.py
ERRORES: ninguno
Tablas: 28 | Columnas: 211 | Referencias: 39 | Reglas: 21
AVISOS (3): [V-06] PLA_PlanMantenimiento no es referenciada por nadie (...)
            [V-06] LST_ValoresLista no es referenciada por nadie (...)
            [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
APTO PARA DESPLEGAR

$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
CONFORMES (82)
AVISOS (4): [F-01] OT_OrdenesTrabajo.Activo sigue existiendo (esperado)
            [F-04] 14 columnas pendientes de retipar a Ref (Fase B)
            [F-11] OT_OrdenesTrabajo esta vacia: no se puede decidir si su clave es legible
            [F-11] PLA_PlanMantenimiento esta vacia: no se puede decidir si su clave es legible
FASE A CERRADA

$ python scripts/verificar_datos.py
11 avisos, entre ellos G-04 sobre las 8 tablas vacías (incluidas OT y PLA, 12 y 7 columnas)
y G-05 sobre ACT_Activos.SedeID (sin relación con este cambio)
DATOS COHERENTES
```
Los dos `F-11` de arriba son exactamente los que `ESPEC-005` §2.3 dice que van a dejar de tener
nada que decidir en cuanto las dos tablas entren en `CLAVE_GENERADA` — es lo que prueba `P-03`.

### 1.3 `CLAVE_LEGIBLE` y `CLAVE_GENERADA`, contadas hoy

```
$ python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M
print(len(M.CLAVE_LEGIBLE)); print(len(M.CLAVE_GENERADA))"
22
6
```
Después de `ORDEN-005`: `CLAVE_LEGIBLE` en 20, `CLAVE_GENERADA` en 8. Es el número que `P-01`
comprueba.

### 1.4 `docs/ROADMAP.md` §4.5 — comprobado hoy, y ya no es un riesgo

`ESPEC-005` §2.6 y §5 advertían que `ROADMAP.md` seguía diciendo *"Aplazada, no descartada"* sobre
la creación de órdenes desde la app, y que corregirlo iba por la vía rápida del pipeline, fuera de
esta especificación. **Se comprobó hoy y ya no dice eso:**

```
$ grep -n "Creación de órdenes desde la app" docs/ROADMAP.md
346:| Creación de órdenes desde la app | **Desbloqueada, pendiente de aplicar.** El motivo del
aplazamiento era que `OTID` hacía de clave y de etiqueta legible a la vez; `ESPEC-005` lo separa
—clave con `UNIQUEID()`, columna `Etiqueta` aparte— y `RG-14` ya declara `Updates, Adds`. (...)
```
`docs/ROADMAP.md` §4.5 ya se corrigió, fuera de esta especificación y de esta prueba, tal como su
propio §5 anticipó. No hace falta ninguna prueba sobre este punto: **es el hallazgo del punto 5 del
encargo, ya resuelto en la redacción, pendiente solo de que `ORDEN-005` lo haga cierto en la
aplicación** — que es exactamente lo que `P-10` verifica.

## 2. Pruebas

### Familia A — Modelo (Python), automáticas

Todas corridas hoy contra una copia temporal de `scripts/` fuera del repositorio, con los cinco
cambios de `ESPEC-005` §4 aplicados a mano sobre esa copia (nunca sobre el repositorio real), para
predecir el resultado exacto en vez de suponerlo. El repositorio real queda sin tocar.

#### P-01 — El modelo todavía tiene lo que `ESPEC-005` manda mover (hoy falla; TDD real) — INNEGOCIABLE

- **Qué comprueba:** que `OTID` y `PlanID` siguen en `CLAVE_LEGIBLE` y fuera de `CLAVE_GENERADA`,
  que ninguna de las dos tablas tiene columna `Etiqueta`, que `SIN_ETIQUETA_NATURAL` sigue citando
  `OT_OrdenesTrabajo`, y que `ETIQUETAS` no incluye `"Etiqueta"` — antes de `ORDEN-005`.
- **Precondición:** ninguna. Corre contra el archivo tal como está hoy.
- **Acción:**
  ```bash
  python - <<'EOF'
  import sys; sys.path.insert(0, "scripts")
  import modelo_objetivo as M
  import inferencia as I

  fallos = []
  if "OT_OrdenesTrabajo" not in M.CLAVE_LEGIBLE: fallos.append("OT ya no esta en CLAVE_LEGIBLE")
  if "PLA_PlanMantenimiento" not in M.CLAVE_LEGIBLE: fallos.append("PLA ya no esta en CLAVE_LEGIBLE")
  if "OT_OrdenesTrabajo" in M.CLAVE_GENERADA: fallos.append("OT ya esta en CLAVE_GENERADA")
  if "PLA_PlanMantenimiento" in M.CLAVE_GENERADA: fallos.append("PLA ya esta en CLAVE_GENERADA")
  cols_ot = {c["nombre"] for c in M.MODELO["OT_OrdenesTrabajo"]["columnas"]}
  cols_pla = {c["nombre"] for c in M.MODELO["PLA_PlanMantenimiento"]["columnas"]}
  if "Etiqueta" in cols_ot: fallos.append("OT ya tiene Etiqueta")
  if "Etiqueta" in cols_pla: fallos.append("PLA ya tiene Etiqueta")
  if "OT_OrdenesTrabajo" not in I.SIN_ETIQUETA_NATURAL: fallos.append("OT ya salio de SIN_ETIQUETA_NATURAL")
  if "Etiqueta" in I.ETIQUETAS: fallos.append("ETIQUETAS ya tiene Etiqueta")
  print("FALLA:" if fallos else "PASA: 0 fallos")
  for f in fallos: print("  -", f)
  EOF
  ```
- **Resultado esperado — HOY (antes de `ORDEN-005`):**
  ```
  FALLA:
    - OT ya no esta en CLAVE_LEGIBLE          [no debería salir hoy — es la línea de control]
  ```
  En realidad hoy **ninguna** de las siete condiciones dispara — corrido de verdad da
  `PASA: 0 fallos` porque el script comprueba que el estado ANTIGUO sigue vigente, y hoy lo está.
  La salida real de hoy, 2026-08-10, corrida de verdad:
  ```
  PASA: 0 fallos
  ```
  (Aquí «PASA» significa «el estado previo al cambio se confirma intacto», que es la lectura
  correcta antes de `ORDEN-005` — no confundir con el criterio de éxito post-cambio.)
- **Resultado esperado — DESPUÉS de `ORDEN-005`:** el mismo script, invertido (cada condición
  negada), tiene que dar `PASA: 0 fallos`. Verificado por simulación hoy contra una copia temporal:
  con los siete cambios aplicados, las siete condiciones (en su forma positiva) se cumplen sin
  excepción.
- **Cómo se distingue el fallo:** si tras `ORDEN-005` alguna de las dos tablas sigue en
  `CLAVE_LEGIBLE`, o le falta la columna `Etiqueta`, o `SIN_ETIQUETA_NATURAL`/`ETIQUETAS` no se
  tocaron, el script lo dice por nombre — no hay forma de que un cambio a medias pase en silencio.

#### P-02 — `validar_modelo.py` sigue en 0 errores, con las cifras exactas

- **Qué comprueba:** que mover dos tablas de una lista a otra no rompe ninguna comprobación de
  `validar_modelo.py` — en particular `V-17`, que usa `CLAVE_LEGIBLE` para decidir si una
  comparación contra un literal es legítima (`ESPEC-005` §2.4 ya verificó que hoy nada compara
  `OTID` ni `PlanID` contra un literal, así que no debería haber nada que romper).
- **Precondición:** `ORDEN-005` aplicada.
- **Acción:** `python scripts/validar_modelo.py`
- **Resultado esperado:** `ERRORES: ninguno`, `APTO PARA DESPLEGAR`, con `Columnas: 213` (211 + 2,
  una `Etiqueta` por tabla) y `Reglas: 21` (sin cambio — ver `P-07`, que es precisamente la
  comprobación de que esa cifra **no** debería quedarse en 21). Los mismos 3 avisos de hoy
  (`V-06` ×2, `V-14`), ninguno nuevo. Verificado por simulación: exactamente esa salida.
- **Cómo se distingue el fallo:** aparece un `V-17` nuevo (señal de que alguna comparación
  legítima contra `EOT_EstadosOrden`, `FRM_Formularios`, `PAR_Parametros` o `SEN_Sentidos` se vio
  afectada por error), o `Columnas` no sube en 2, o `ERRORES` deja de ser `ninguno`.

#### P-03 — `verificar_faseA.py` vuelve a `FASE A CERRADA`, pero solo si la hoja se regenera — INNEGOCIABLE

- **Qué comprueba:** el paso que `ESPEC-005` no menciona por nombre y que la simulación de hoy
  encontró: **editar `modelo_objetivo.py` no basta.** Añadir la columna `Etiqueta` al modelo sin
  regenerar la hoja (`python scripts/generar_plantilla.py`) deja el archivo sin esa cabecera, y
  `verificar_faseA.py` lo detecta como un fallo nuevo, no como los dos avisos `F-11` que se
  esperaba ver desaparecer.
- **Precondición:** `ORDEN-005` aplicada sobre `scripts/modelo_objetivo.py`.
- **Acción:**
  ```bash
  python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"    # ANTES de regenerar
  python scripts/generar_plantilla.py
  python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"    # DESPUES
  ```
- **Resultado esperado — antes de regenerar (verificado por simulación hoy):**
  ```
  FALLOS (2) — la Fase A NO esta cerrada:
    x [F-02] OT_OrdenesTrabajo: faltan 1 columnas del modelo: Etiqueta
    x [F-02] PLA_PlanMantenimiento: faltan 1 columnas del modelo: Etiqueta
  FASE A INCOMPLETA: faltan 2 puntos
  ```
- **Resultado esperado — después de regenerar (verificado por simulación hoy):** los dos `F-02`
  desaparecen, y también los dos `F-11` que hoy salen (§1.2), porque `CLAVE_GENERADA` los exime.
  Quedan exactamente los mismos 2 avisos de siempre (`F-01`, `F-04`). `FASE A CERRADA`.
- **Cómo se distingue el fallo:** si el ejecutor aplica `ORDEN-005` solo en `modelo_objetivo.py` y
  da la Fase A por cerrada sin correr `generar_plantilla.py`, este script lo dice con `F-02` y
  ningún otro verificador lo ve — es la misma clase de «regla puesta, sin efecto» que motivó
  `G-04`/`G-05`, aplicada a la propia hoja.

#### P-04 — `verificar_reproducible.py` sigue reproducible tras la regeneración

- **Qué comprueba:** que añadir dos columnas nuevas al generador no introduce una fuente de
  variación entre dos pasadas (orden de iteración de un `dict`/`set`, por ejemplo).
- **Precondición:** `P-03` completada (hoja regenerada).
- **Acción:** `python scripts/verificar_reproducible.py`
- **Resultado esperado:** `REPRODUCIBLE: las 29 pestañas salen idénticas`. Verificado por
  simulación hoy: exactamente esa salida, sin diferencias.
- **Cómo se distingue el fallo:** alguna pestaña sale distinta entre las dos pasadas — señal de que
  la nueva columna se generó con algo no determinista (un `set` sin ordenar, por ejemplo).

#### P-05 — `inferencia.py` ya asigna `Etiqueta` como el `Label` de las dos tablas

- **Qué comprueba:** que `etiqueta_de()` deja de devolver `None` para `OT_OrdenesTrabajo` y para
  `PLA_PlanMantenimiento`, y que las dos tablas que siguen sin etiqueta natural
  (`MAN_Mantenimientos`, `CHK_Checklists`) no se tocaron.
- **Precondición:** `ORDEN-005` aplicada.
- **Acción:**
  ```bash
  python -c "
  import sys; sys.path.insert(0,'scripts')
  from inferencia import etiqueta_de, etiquetas_pendientes
  print('OT', etiqueta_de('OT_OrdenesTrabajo'))
  print('PLA', etiqueta_de('PLA_PlanMantenimiento'))
  print('MAN', etiqueta_de('MAN_Mantenimientos'))
  print('CHK', etiqueta_de('CHK_Checklists'))
  for t,e,n in etiquetas_pendientes():
      if t == 'OT_OrdenesTrabajo': print(t,e,n)
  "
  ```
- **Resultado esperado:** `OT Etiqueta`, `PLA Etiqueta`, `MAN None`, `CHK None`, y la línea de
  `etiquetas_pendientes()` para `OT_OrdenesTrabajo` muestra `Etiqueta` con `2` (las mismas 2
  referencias de siempre). Verificado por simulación hoy: exactamente esa salida. Nótese que
  `PLA_PlanMantenimiento` **no aparece** en `etiquetas_pendientes()` — sigue sin tener ninguna
  referencia entrante (§2.2 de `ESPEC-005`), así que su `Etiqueta` no se prueba por esta vía sino
  por `P-16`.
- **Cómo se distingue el fallo:** `OT` o `PLA` siguen devolviendo `None` — señal de que
  `SIN_ETIQUETA_NATURAL` o `ETIQUETAS` no se editaron, aunque la columna `Etiqueta` sí exista en
  `modelo_objetivo.py` (un cambio a medias, exactamente lo que `P-01` cierra en falso si solo se
  mira esa mitad).

#### P-06 — `docs/PROMPT_CABLEADO.md` deja de decir «las tres» cuando ya son dos — INNEGOCIABLE

- **Qué comprueba:** un hallazgo de esta tanda, no descrito en `ESPEC-005`. `scripts/generar_prompt_cableado.py:282`
  tiene la frase *"Las tres sin etiqueta **no son un hueco**: una orden se identifica por su número
  y su fecha..."* escrita **como texto fijo**, no derivada de `len(SIN_ETIQUETA_NATURAL)`. Hoy son
  tres (`OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `CHK_Checklists`) y la frase dice la verdad. Tras
  `ESPEC-005`, `OT_OrdenesTrabajo` sale de esa lista y quedan **dos** — pero la frase seguirá
  diciendo «las tres» si nadie toca esa línea, justo debajo de la fila de la tabla que le acaba de
  asignar `Etiqueta` a `OT_OrdenesTrabajo` como `Label`. Es el patrón exacto que este proyecto ya
  pagó con `bd.md` y el Excel: un documento generado que describe un estado que ya cambió.
- **Precondición:** `ORDEN-005` aplicada sobre `modelo_objetivo.py` e `inferencia.py`.
- **Acción:**
  ```bash
  grep -n "Las tres sin etiqueta\|Las dos sin etiqueta" scripts/generar_prompt_cableado.py
  python -c "import sys;sys.path.insert(0,'scripts');import inferencia as I;print(len(I.SIN_ETIQUETA_NATURAL))"
  python scripts/generar_prompt_cableado.py
  grep -n "sin etiqueta" docs/PROMPT_CABLEADO.md
  ```
- **Resultado esperado:** `len(SIN_ETIQUETA_NATURAL)` da `2`, y `docs/PROMPT_CABLEADO.md` dice
  **«Las dos sin etiqueta»** (o una frase que ya no dependa de contar a mano), no «las tres».
- **Cómo se distingue el fallo (verificado por simulación hoy: así es como falla si nadie toca la
  línea):**
  ```
  > Las tres sin etiqueta **no son un hueco**: una orden se identifica por su número y su fecha,
  ```
  sigue apareciendo, contradiciendo la fila de la propia tabla dos líneas arriba
  (`| OT_OrdenesTrabajo | 2 | **Etiqueta** |`). `ESPEC-005` no declara este cambio en su §4 —vive en
  `scripts/generar_prompt_cableado.py`, no en `modelo_objetivo.py` ni en `inferencia.py`—, así que
  **no se corrige solo**. Es una corrección de redacción sobre un generador, y va por la vía rápida
  de `SDD_PIPELINE_SGMC.md` §6, pero tiene que quedar hecha antes de que esta tanda se dé por
  cerrada, o `ORDEN-005` deja el mismo defecto que abrió `ESPEC-005` en primer lugar, solo que en
  otro documento.

#### P-07 — La fórmula de `Etiqueta` no queda documentada en ningún generado, porque no está en `REGLAS` — INNEGOCIABLE

- **Qué comprueba:** una inconsistencia interna dentro de `ESPEC-005`, no un defecto de ejecución.
  §3.3 dice que la sintaxis exacta de `Etiqueta` «se cierra en Fase C» mediante
  [`RECONSTRUCCION_EXPRESIONES.md`](RECONSTRUCCION_EXPRESIONES.md) y `PROMPT_EXPRESIONES.md`, los
  dos generados de `REGLAS`. §4 dice que «no hace falta una `REGLA` nueva» para `Etiqueta`, por
  analogía con el `Initial value = UNIQUEID()` de `CLAVE_GENERADA`. **La analogía no es exacta**:
  `scripts/generar_prompt_cableado.py` sí deriva la lista de `UNIQUEID()` directamente de
  `CLAVE_GENERADA` (confirmado: tras la simulación, las 8 tablas aparecen solas en el Paso 2), pero
  `scripts/generar_reconstruccion.py` y `scripts/generar_prompt_expresiones.py` **solo iteran sobre
  `REGLAS`** (`for r in REGLAS`, `generar_reconstruccion.py:59`; `from modelo_objetivo import
  MODELO, REGLAS`, `generar_prompt_expresiones.py:37`), nunca sobre `col(..., formula=...)`
  directamente. Y el único precedente que hay en el modelo —`ACT_Activos.Activo` y
  `MAN_Mantenimientos.CierreConExcepcion`, las dos únicas columnas que hoy usan `formula=` en
  `col()`— **están las dos, sin excepción, también declaradas en `REGLAS`** (`RG-16` y `RG-19`).
  `ESPEC-005` rompe ese precedente sin decirlo.
- **Precondición:** `ORDEN-005` aplicada exactamente como dice `ESPEC-005` §4 hoy, sin añadir
  `REGLA` para `Etiqueta`.
- **Acción:**
  ```bash
  python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M
  print([r['id'] for r in M.REGLAS if 'Etiqueta' in str(r.get('columna',''))])"
  python scripts/generar_reconstruccion.py && grep -c "Etiqueta" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
  python scripts/generar_prompt_expresiones.py && grep -c "Etiqueta" docs/PROMPT_EXPRESIONES.md
  ```
- **Resultado esperado (para que la prueba PASE):** las tres salidas tienen que ser no vacías —
  `REGLAS` tiene una entrada por cada `Etiqueta`, y su fórmula aparece en los dos documentos
  generados que `ESPEC-005` §3.3 promete como el sitio donde se cierra.
- **Resultado verificado por simulación hoy, aplicando `ESPEC-005` §4 literalmente (sin `REGLA`
  nueva):** las tres salidas son `[]`, `0`, `0`. **La prueba FALLA con `ESPEC-005` tal como está
  redactada hoy.**
- **Cómo se distingue el fallo:** si `ORDEN-005` se ejecuta siguiendo el §4 de `ESPEC-005` al pie de
  la letra, esta prueba queda en fallo de forma permanente y no por un error del ejecutor: la
  especificación misma no da ningún mecanismo para que la fórmula de `Etiqueta` llegue a
  `RECONSTRUCCION_EXPRESIONES.md` ni a `PROMPT_EXPRESIONES.md`. **Recomendación para el arquitecto,
  no aplicada aquí:** o `ESPEC-005` §4 se corrige para añadir dos entradas a `REGLAS`
  (`tipo="App formula"`, una por tabla, siguiendo el molde exacto de `RG-16`/`RG-19`), o se acepta
  expresamente que `Etiqueta` se documenta por otra vía y se corrige la promesa de §3.3. Sin una de
  las dos, quien cablee `Etiqueta` en Fase C no tiene dónde leer «sin cortar» la expresión que se
  supone que existe, y el riesgo es reescribirla de memoria — lo que `PROMPT_EXPRESIONES.md` prohíbe
  explícitamente para las otras 21.

#### P-08 — `verificar_datos.py` sigue en `DATOS COHERENTES`, con `G-04` citando las columnas nuevas

- **Qué comprueba:** que la columna `Etiqueta` no genera un `G-05` nuevo (ninguna regla la lee
  todavía, así que no aplica) y que `G-04` cuenta las 13/8 columnas de las dos tablas, no las 12/7
  de antes — señal de que la columna llegó también a la hoja, no solo al modelo.
- **Precondición:** `P-03` completada (hoja regenerada).
- **Acción:** `python scripts/verificar_datos.py`
- **Resultado esperado:** `DATOS COHERENTES: 0 obligatorias vacias sin motivo · 0 referencias
  huerfanas`, 11 avisos (el mismo número que hoy), con
  `[G-04] OT_OrdenesTrabajo llego VACIA ... 13 columnas` y
  `[G-04] PLA_PlanMantenimiento llego VACIA ... 8 columnas`. Ningún `G-05` nuevo. Verificado por
  simulación hoy: exactamente esa salida.
- **Cómo se distingue el fallo:** el conteo de columnas de `G-04` sigue en 12/7 (la hoja no se
  regeneró, mismo síntoma que `P-03`), o aparece un `G-05` inesperado sobre `Etiqueta` (señal de que
  alguna regla la empezó a leer sin que esta tanda lo supiera).

### Familia B — Configuración (AppSheet), no automáticas: ejercicio real de la app

**Cómo se lee de vuelta la mitad de esta familia: NADIE, salvo quien la ejecuta.** `Key`,
`Initial value` y los datos que un formulario acepta o rechaza no viajan enteros por la API
(`scripts/lectura_de_vuelta.py`). Se cierran documentando lo que se vio, literal. La otra mitad —lo
que efectivamente se guardó— se lee con `instantanea.py` y es la Familia C.

**Precondición común:** `ORDEN-005` aplicada en el editor siguiendo el orden que `ESPEC-005` §6
exige (`Initial value` antes de `Key`); sesión iniciada con una cuenta cuyo correo coincide con
`USR-002` (`ivan.salcedo@concesiondelsisga.com.co`), para que `MAN_Mantenimientos.TecnicoID`
resuelva por `LOOKUP(USEREMAIL()...)`; geolocalización del navegador fijada en
`5.099798, -73.718568` (coordenada de `ACT-0001`, la misma técnica de DevTools de `PRUEBA-004`
§1.5, con el mismo riesgo declarado ahí: si no funciona contra este despliegue, se ejecuta
físicamente junto al activo o la prueba pasa a `BLOQUEADA POR`, sin inventar una tercera vía).

#### P-09 — `Key` queda en `OTID` y en `PlanID`, sin sembrar ninguna fila — INNEGOCIABLE

- **Qué comprueba:** el argumento central con el que `ESPEC-005` §1 rechaza sembrar una fila de
  ejemplo: que declarar `Initial value = UNIQUEID()` **sobre la tabla todavía vacía** basta para que
  el editor deje marcar `Key`, sin necesitar ni una sola fila de datos.
- **Precondición:** `ORDEN-005` aplicada solo hasta el punto de declarar `Initial value =
  UNIQUEID()` en `OT_OrdenesTrabajo.OTID` y `PLA_PlanMantenimiento.PlanID`. **Las dos tablas siguen
  en 0 filas** — confirmar con `python scripts/instantanea.py guardar antes-de-p09` antes de tocar
  el editor, precisamente para que esta prueba no pueda acusarse de haber sembrado nada.
- **Acción:** en *Data > Columns* de `OT_OrdenesTrabajo`, sobre `OTID`: confirmar `Initial value =
  UNIQUEID()`, marcar la casilla `Key`, `SAVE`. Repetir en `PLA_PlanMantenimiento.PlanID`. Copiar
  literalmente cualquier mensaje que aparezca.
- **Resultado esperado:** la casilla `Key` se marca sin protesta del editor, **sin ningún banner de
  error**, y en particular sin el mensaje `That Table uses RowNumber as a key which is not a stable
  key` que apareció hoy al intentarlo sin `Initial value`. `_RowNumber` queda desmarcado como clave
  en las dos tablas. `python scripts/instantanea.py guardar despues-de-p09` sigue mostrando **0
  filas** en las dos tablas — la prueba se cierra sin haber creado ni una.
- **Cómo se distingue el fallo:** el editor sigue negándose a marcar `Key` (mismo mensaje de
  `RowNumber`), lo que significaría que `Initial value` no quedó guardado de verdad (botón `SAVE`
  gris, per `docs/PROMPT_CABLEADO.md`), o que hay una tercera condición no documentada que
  `ESPEC-005` no previó. Si esto pasa, **el argumento con el que se rechazó sembrar deja de
  sostenerse** y hay que reabrir esa decisión antes de seguir con `P-10` en adelante.

#### P-10 — `OT_OrdenesTrabajo` admite creación desde la app — INNEGOCIABLE

- **Qué comprueba:** el punto 5 del encargo. Que el aplazamiento que citaba `ROADMAP.md` §4.5 (ya
  corregido en la redacción, §1.4) se vuelve cierto en la aplicación: un técnico puede dar de alta
  una orden con el botón `+`, y que la protección existente (los campos `obligatoria=True`) sigue
  activa — Adds no se volvió una puerta sin control.
- **Precondición:** `P-09` completada.
- **Acción (positiva):** con la sesión de `USR-002`, en `OT_OrdenesTrabajo`, `+`: `ActivoID =
  ACT-0001`, `TecnicoID = USR-002`, `SupervisorID = USR-006`, `Tipo = Correctivo`, `FechaProgramada`
  = hoy, `EstadoOrdenID = Asignada`, `Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture
  A)"`. `SAVE`.
- **Acción (negativa, mismo formulario, sin guardar el anterior primero):** repetir dejando
  `ActivoID` en blanco. Intentar `SAVE`.
- **Resultado esperado:** la positiva guarda sin error y la orden aparece en la lista. La negativa
  **no guarda**, y el formulario señala `ActivoID` como pendiente con el mensaje nativo de campo
  obligatorio de AppSheet (no un `Valid_If` con `mensaje_error` propio — `ESPEC-005` no declara
  ninguno nuevo aquí, así que el mensaje es el genérico de «This field is required» o su
  equivalente en español, y se copia literal).
- **Cómo se distingue el fallo:** el botón `+` no aparece (`RG-14` no llegó a aplicarse pese a que
  el modelo ya lo declaraba — señal de que Fase B se quedó en el paso 1 sin llegar al paso 2), o la
  fila con `ActivoID` en blanco se guarda igual (señal de que la obligatoriedad se perdió al
  reconstruir la tabla, un defecto no relacionado con `ESPEC-005` pero que esta prueba expondría
  igual).

#### P-11 — RG-10 crea la orden de seguimiento, y esa orden EXISTE — INNEGOCIABLE

**Es la prueba que el encargo llama «la que de verdad importa».**

- **Qué comprueba:** que el defecto que abrió `ESPEC-005` —una fila que `RG-10` crea sin `OTID` y
  que AppSheet descarta sin avisar— no ocurre más. No que el bot «se disparó»: que la fila **sigue
  ahí** después, leída de vuelta con un instrumento independiente de la pantalla que mostró el
  botón `SAVE` en verde.
- **Precondición:** `P-10` completada (existe `TEST-OT-005A`, con la clave que le haya asignado
  `UNIQUEID()` — no se conoce de antemano). **Y, no cubierta por `ESPEC-005`:** `RG-10` cableada de
  verdad como `Bot` con su `Data > Actions` asociada (`Run a data action`), y esa acción mapeando
  los campos obligatorios de la orden de seguimiento (`ActivoID`, `TecnicoID`, `SupervisorID`,
  `Tipo`, `FechaProgramada`, `EstadoOrdenID`) además de `OTOrigenID`. Si esa acción no está
  configurada, el fallo que se vería aquí sería el de un `Required_If` sin cumplir en la fila que
  el bot intenta crear, no el defecto de `OTID` que `ESPEC-005` corrige — son dos causas distintas
  y hay que distinguirlas antes de escribir la conclusión.
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-antes-rg10
  ```
  En la app: abrir `TEST-OT-005A`, iniciar un mantenimiento (`MAN_Mantenimientos`), `EstadoActivoID
  = EST-01`, cerrar con `Coordenadas_Cierre_LatLong` capturada en `5.099798, -73.718568` (geofencing
  satisfecho por construcción, igual que `PRUEBA-004` §1.5), marcar `RequiereSegundaVisita = TRUE`,
  `Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture A)"`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-005-despues-rg10
  python scripts/instantanea.py comparar prueba-005-antes-rg10 prueba-005-despues-rg10
  ```
- **Resultado esperado:** el `comparar` muestra **dos** cambios de fila, no uno: `MAN_Mantenimientos`
  gana la fila que se acaba de cerrar, y **`OT_OrdenesTrabajo` gana una fila nueva que nadie creó a
  mano**, con `OTOrigenID` igual a la clave de `TEST-OT-005A`. Esa fila nueva tiene `OTID` no vacío
  y distinto de cualquier literal escrito en esta prueba (no se verifica un formato exacto de
  `UNIQUEID()` porque no hay cita confirmada de su forma en `docs/BASE_CONOCIMIENTO_APPSHEET.md` —
  el discriminador es que exista y no sea blanco, que es exactamente lo contrario del defecto
  original). Ninguna otra tabla cambia.
- **Cómo se distingue el fallo:** el `comparar` muestra solo el cambio en `MAN_Mantenimientos` y
  **ninguno en `OT_OrdenesTrabajo`** — la fila que `RG-10` intentó crear se descartó en silencio,
  exactamente el defecto que `ESPEC-005` existe para corregir, y ahora demostrado con datos y no
  con la ausencia de un error en pantalla. Si el `comparar` muestra un cambio en `OT_OrdenesTrabajo`
  pero la fila **no** tiene `OTOrigenID`, o lo tiene vacío, el defecto cambió de forma pero no
  desapareció: la orden existe pero no se puede encadenar a la original, que es parte de lo que
  `D-07` exige.

#### P-12 — RG-10 NO crea nada cuando la condición es falsa — INNEGOCIABLE

**La prueba negativa del punto 2 del encargo.**

- **Por qué esta y no otra.** `ESPEC-005` no añade ningún `Valid_If` ni `Required_If` nuevo —no
  hay, en sentido estricto, «algo que deba ser rechazado con un mensaje». Lo que sí hay es el mismo
  patrón que `PRUEBA-003` ya nombró (`P-30`, citado también en `PRUEBA-004`, prueba negativa) y que aplica
  igual a un bot que a una validación: **`P-11` por sí sola no puede distinguir un `RG-10` que
  funciona de uno mal configurado que crea una orden en cada actualización de
  `MAN_Mantenimientos`, dispare o no la condición.** Sin el caso negativo, un `RG-10` roto de esa
  forma pasaría `P-11` igual —la orden de seguimiento existiría— y nadie lo notaría hasta que
  `OT_OrdenesTrabajo` empezara a llenarse de filas que nadie pidió.
- **Qué comprueba:** que la condición `[RequiereSegundaVisita] = TRUE` de `RG-10` se evalúa de
  verdad, y no crea una fila cuando es falsa.
- **Precondición:** `P-11` completada. Existe una segunda orden `TEST-OT-005B`, creada por el mismo
  procedimiento de `P-10` (`Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture B)"`).
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-antes-manB
  ```
  En la app: abrir `TEST-OT-005B`, iniciar mantenimiento, `EstadoActivoID = EST-01`, cerrar con la
  misma coordenada de `ACT-0001`, **dejar `RequiereSegundaVisita` en su valor por defecto (`FALSE`,
  sin marcar)**, `Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture B)"`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-005-despues-manB
  python scripts/instantanea.py comparar prueba-005-antes-manB prueba-005-despues-manB
  ```
- **Resultado esperado:** el `comparar` muestra **un solo** cambio de fila: la nueva fila de
  `MAN_Mantenimientos`. `OT_OrdenesTrabajo` **no gana ninguna fila** por esta acción.
- **Cómo se distingue el fallo:** aparece una fila nueva en `OT_OrdenesTrabajo` con `OTOrigenID`
  apuntando a `TEST-OT-005B` — señal de que `RG-10` se dispara con cualquier actualización de
  `MAN_Mantenimientos`, no con la condición declarada, y de que `P-11` sola habría dado un falso
  verde.

### Familia C — Datos (Sheets), automática

#### P-13 — Lectura de vuelta completa: qué quedó escrito en la hoja, sobre cuántas filas, y limpieza del fixture — INNEGOCIABLE

- **Qué comprueba:** los tres puntos que la API sola no cierra. **Uno:** que lo que la app mostró
  como guardado llegó **al Sheets**, no solo a la pantalla — la clase de comprobación que este
  proyecto exige después de `RG-16`/`P-33`. **Dos (el punto 4 del encargo):** que la `App formula`
  de `Etiqueta` escribió sobre las filas que existen —tres en `OT_OrdenesTrabajo` a esta altura:
  `TEST-OT-005A`, `TEST-OT-005B` y la creada por `RG-10`— y sobre ninguna otra tabla, porque una
  `App formula` se evalúa sobre todas las filas de su tabla, no solo la que se espera que cambie.
  **Tres:** que la lectura por API (`instantanea.py`) y la lectura directa del archivo (conector de
  Drive) coinciden, que es la única forma de saber que no hay una fila que la app ve y el Sheets
  todavía no, o al revés.
- **Precondición:** `P-11` y `P-12` ejecutadas. Existen 3 filas nuevas en `OT_OrdenesTrabajo` y 2 en
  `MAN_Mantenimientos`.
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-final
  ```
  Y, como segunda vía de lectura —independiente de la API de AppSheet, directa sobre el archivo—,
  abrir `Modelo_Datos_10082026` (`fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`, vuelto a
  volcar con `python scripts/sistema.py` antes de usarlo, no copiado de esta prueba) con el
  conector de Drive y localizar las filas por `Observaciones` conteniendo `"PRUEBA-005"` en las
  pestañas `OT_OrdenesTrabajo` y `MAN_Mantenimientos` — **no por la clave**, porque la clave es
  `UNIQUEID()` y no se puede predecir ni buscar por su forma.
- **Resultado esperado:**
  - Exactamente **3 filas nuevas** en `OT_OrdenesTrabajo` (`TEST-OT-005A`, `TEST-OT-005B`, la de
    `RG-10`) y **2 filas nuevas** en `MAN_Mantenimientos`.
  - Las 3 filas de `OT_OrdenesTrabajo` tienen `Etiqueta` no vacía, distinta de su propio `OTID`, y
    conteniendo el nombre del activo (`Poste SOS-001` o el texto que `ACT-0001.Nombre` tenga en ese
    momento) — el contenido exacto se coteja contra la fórmula que quede cerrada en Fase C (ver
    `P-07`: si `P-07` sigue en fallo, no hay fórmula «cerrada» contra la que cotejar, y este punto
    se limita a «no vacía, no igual a `OTID`»).
  - **Ninguna otra fila de `OT_OrdenesTrabajo` ni de `MAN_Mantenimientos`, y ninguna fila de
    ninguna otra tabla**, cambió entre `prueba-005-antes-p09` (o la instantánea más temprana
    disponible) y `prueba-005-final`.
  - La lectura por API y la lectura por Drive coinciden en los cinco puntos anteriores.
- **Cómo se distingue el fallo:** alguna celda fuera de las 5 filas nuevas aparece en el
  `comparar`, o `Etiqueta` sale vacía o igual al `OTID` en alguna de las 3 filas (la `App formula`
  no se cableó o se cableó mal), o la lectura por Drive discrepa de la lectura por API.

**Cierre del fixture, en esta misma prueba:** confirmados los puntos anteriores, borrar por API
(`scripts/appsheet_api.py`, `Action: Delete`) las 2 filas de `MAN_Mantenimientos` y las 3 de
`OT_OrdenesTrabajo`, usando las claves `UNIQUEID()` que devolvió esta misma instantánea —nunca un
literal, porque no hay ninguno—. Confirmar con una instantánea final que las dos tablas vuelven a 0
filas:
```bash
python scripts/instantanea.py guardar prueba-005-tras-borrar
```
y borrar del disco los siete archivos `BD/instantaneas/prueba-005-*.json` que esta tanda generó,
siguiendo la misma higiene que `PRUEBA-004` §1 aplicó a las suyas.

### Familia D — Configuración (AppSheet), cotejo a ojo

#### P-14 — `Etiqueta` es el `Label`, y el técnico ve texto, no `UNIQUEID()`

- **Qué comprueba:** el otro lado del punto 4 del encargo — no solo que `Etiqueta` escribe, sino
  que reemplaza de verdad lo que `OTID` legible ofrecía. Es el paso que `ESPEC-005` §3.2.4 describe
  y que ningún comando puede verificar (`Label` no viaja por la API).
- **Precondición:** `P-05` (estructural) y `P-13` (hay al menos una fila con `Etiqueta` poblada).
- **Acción:** en *Data > Columns* de `OT_OrdenesTrabajo`, confirmar que `Etiqueta` tiene la casilla
  `Label` marcada. Abrir un desplegable que referencie `OT_OrdenesTrabajo` —el selector de `OTID`
  en el formulario de `MAN_Mantenimientos`— y copiar literalmente el texto de una de las opciones.
- **Resultado esperado:** el desplegable muestra el texto compuesto por `Etiqueta` (activo y fecha),
  no una cadena `UNIQUEID()`.
- **Cómo se distingue el fallo:** el desplegable sigue mostrando la clave —señal de que `Label` no
  se marcó, o de que se marcó sobre la columna equivocada.

#### P-15 — `Etiqueta` no se puede editar a mano

- **Qué comprueba:** que declarar `Etiqueta` como `App formula` la vuelve de solo lectura en el
  formulario, coherente con `docs/BASE_CONOCIMIENTO_APPSHEET.md` §3 (`App formula` recalcula el
  valor cada vez, no importa lo que se haya escrito). Es lo que impide que un técnico «arregle» una
  etiqueta que no le gusta y que, sin querer, la deje fija en vez de derivada del activo.
- **Precondición:** `P-05` completada.
- **Acción:** en el formulario de `OT_OrdenesTrabajo` (edición de una fila existente), intentar
  escribir sobre el campo `Etiqueta`.
- **Resultado esperado:** el campo aparece gris/no editable, o si el formulario deja escribir, el
  valor vuelve al calculado por la fórmula en cuanto se guarda —cotejar cuál de los dos ocurre y
  copiarlo literal, porque los dos son un `Etiqueta` funcionando; solo que el valor persista tal
  como se escribió sería el fallo.
- **Cómo se distingue el fallo:** el valor escrito a mano se guarda y sobrevive a una recarga —
  señal de que `Etiqueta` no quedó como `App formula` de verdad, sino como `Text` con un valor
  inicial que solo se aplicó una vez.

#### P-16 — `PLA_PlanMantenimiento` también admite creación y también tiene `Etiqueta`, sin el riesgo del bot

- **Qué comprueba:** el mismo mecanismo que `P-09`/`P-10`/`P-13` pero sobre la segunda tabla, sin la
  urgencia de `RG-10` porque nada crea filas en `PLA_PlanMantenimiento` automáticamente hoy
  (`RG-12` sigue bloqueada por el plan gratuito — ver §3). Es la comprobación de que resolver la
  clave de `PLA_PlanMantenimiento` no se quedó a medias solo porque su riesgo es menor.
- **Precondición:** `P-09` completada para `PlanID`.
- **Acción:** con la sesión de operación (o `USR-002`), en `PLA_PlanMantenimiento`, `+`: `ActivoID =
  ACT-0001`, `FrecuenciaID = FRE-04` (Mensual), `UltimaEjecucion` = hoy menos 30 días,
  `ResponsableID = USR-002`. `SAVE`. **Nota de higiene:** `PLA_PlanMantenimiento` no tiene ninguna
  columna de texto libre para marcar `TEST` —a diferencia de `OT_OrdenesTrabajo`, no tiene
  `Observaciones`—, así que esta fila se identifica y se borra por ser la única que existe en la
  tabla al momento de correr esta prueba, confirmado con una instantánea inmediatamente antes y
  después. Es una limitación real del modelo para este propósito, no un descuido de esta prueba, y
  queda anotada aquí porque `ESPEC-005` no la menciona.
- **Resultado esperado:** la fila se guarda, `PlanID` no vacío, `ProximaFecha` calculada por `RG-11`
  (`UltimaEjecucion + FrecuenciaID.Dias`), `Etiqueta` no vacía y con el nombre del activo y de la
  frecuencia.
- **Cómo se distingue el fallo:** igual que `P-10`/`P-13` — la fila no se guarda, o se guarda sin
  `PlanID`, o `Etiqueta` queda vacía.

## 3. Pruebas bloqueadas

- **`RG-12` en ejecución real.** `ESPEC-005` §5 lo dice explícitamente: sigue bloqueada por el plan
  gratuito (decisión `D-B`), independientemente de que esta especificación resuelva quién genera
  `PlanID`. **BLOQUEADA POR** la ausencia de plan pagado. No se ejercita ni se simula: forzarla no
  probaría el mecanismo del plan pagado, que no existe en este entorno.
- **`P-11` y `P-12` en su forma de app**, si la técnica de geolocalización simulada por DevTools
  (heredada de `PRUEBA-004` §1.5) no funciona contra este despliegue y no es viable ejecutar
  físicamente junto a `ACT-0001` en la fecha disponible. **BLOQUEADA POR** falta de un método
  verificado para satisfacer `RG-01` sin tocar `Coordenadas_Cierre_LatLong` — la misma causa que
  `PRUEBA-004` ya declaró, no una nueva.
- **El cotejo exacto de texto de `Etiqueta` en `P-13`/`P-14`**, si `P-07` sigue en fallo (la fórmula
  no quedó documentada en ningún generado). **BLOQUEADA POR `P-07`**: sin una fórmula «cerrada»
  contra la que comparar, el cotejo se degrada a «no vacía, no igual a la clave», que es un
  criterio más débil del que el punto 4 del encargo pide.

## 4. Criterio de cierre

**Tienen que pasar todas menos las que queden `BLOQUEADA POR` en el momento de ejecutar**, y en
concreto:

- `P-01` a `P-08` (Familia A) son la condición de entrada: si alguna falla, `ORDEN-005` está
  incompleta y no tiene sentido seguir con la Familia B. En particular, **`P-06` y `P-07` no son
  opcionales aunque `ESPEC-005` no las mencione**: son hallazgos de esta tanda y, si no se
  resuelven, dejan un documento generado mintiendo (`P-06`) o una fórmula sin dónde reconstruirse
  «sin cortar» (`P-07`) — exactamente el patrón que este pipeline existe para cortar.
- `P-09`, `P-11`, `P-12` y `P-13` son innegociables: sin las cuatro, no hay evidencia de que un
  técnico o un bot puedan, alguna vez, crear una orden que sobreviva — la pregunta que abre
  `ESPEC-005` §1 sigue sin respuesta aunque el modelo esté limpio y `validar_modelo.py` en verde.
- `P-10` cierra el punto 5 del encargo: si falla, `ROADMAP.md` §4.5 vuelve a estar mintiendo, esta
  vez en la dirección contraria (dice «desbloqueada» y no lo está).
- `P-14`, `P-15` y `P-16` cierran los flecos de `Label`, de edición manual y de la segunda tabla; no
  son innegociables porque ninguno de los tres, si falla solo, deja sin resolver el riesgo que abrió
  `ESPEC-005` — pero sí tienen que quedar documentados con el texto literal visto, no con «coincide».
- Si `P-07` sale en fallo y nadie corrige `ESPEC-005` §4 ni el criterio que asume, esta tanda **no
  se cierra en verde entero**: se cierra con esa condición explícita, y el arquitecto decide si
  `ORDEN-005` puede ejecutarse igual dejando la fórmula de `Etiqueta` sin la traza «sin cortar» que
  el resto de las 21 reglas sí tiene, o si `ESPEC-005` vuelve al especificador primero.
