# PRUEBA-005 — Pruebas de aceptación de ESPEC-005

**Rehecha el 2026-08-10, junto con `ESPEC-005`, tras bloqueo del arquitecto.** Once hallazgos se
atienden aquí; los tres de código ya estaban aplicados en el repositorio antes de esta versión
(ver cabecera de `ESPEC-005`). El cambio de mayor alcance es que `Etiqueta` pasó de ser una `App
formula` sobre columna real a una **columna virtual**, y eso reescribe buena parte de la Familia A:
lo que la versión anterior predecía que iba a fallar (`P-07`), ahora se verificó que pasa; lo que
predecía que había que regenerar la hoja (`P-03`), ahora se verificó que no hace falta.

**Escrita antes de que `ORDEN-005` exista.** Nada de lo que sigue se aplicó al repositorio real ni
al modelo en vivo. Los comandos marcados «automática» sí se corrieron —de solo lectura contra la
aplicación, o sobre una copia temporal fuera del repositorio para predecir el resultado exacto— y
sus salidas están citadas literalmente. Los que requieren la app están descritos para cuando el
ejecutor los corra, no ejecutados aquí.

| | |
|---|---|
| Cubre | [`ESPEC-005-clave-otid-planid.md`](ESPEC-005-clave-otid-planid.md): `OTID` y `PlanID` pasan de `CLAVE_LEGIBLE` a `CLAVE_GENERADA` (`Initial value = UNIQUEID()`); `Etiqueta` como columna **virtual** en `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` (`App formula` vía `RG-35`/`RG-36`, `Label`) |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Volcado hoy con `python scripts/sistema.py` |
| Reglas que esta tanda tiene que probar | `RG-35` y `RG-36`, nuevas, declaradas como `REGLA` de columna virtual — a diferencia de la versión anterior, ya no hay un hallazgo de "regla sin declarar": eso es precisamente lo que `P-07` verifica que se resolvió. `RG-10` y `RG-12` dejan de crear filas huérfanas. `RG-07` (bot de correo) se ve afectado como efecto colateral — ver precondición de la Familia B |
| Innegociables | `P-01`, `P-03`, `P-04`, `P-07`, `P-09`, `P-11`, `P-12`, `P-13`, `P-14` |

## 0. Los cinco puntos del encargo, y dónde se prueban cada uno

| # | Punto del encargo | Prueba(s) |
|---|---|---|
| 1 | Un bot crea una orden y esa orden EXISTE | `P-11` |
| 2 | La prueba negativa | `P-12` (con su alcance real declarado explícitamente: solo mide filas, no correos — ver la nota dentro de `P-12`) |
| 3 | `Key` queda en la columna, no en `_RowNumber`, sin sembrar | `P-09` |
| 4 | La columna `Etiqueta` escribe (para el técnico) | `P-15` (Label visible) y `P-07` (dónde queda documentada su fórmula) |
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
Coincide con `BD/Modelo_Datos_PLANTILLA.xlsx` leído por `openpyxl` (mismo conteo que `ESPEC-005`
§2.1). La instantánea se borró después de leerla, siguiendo la higiene de `SDD_PIPELINE_SGMC.md`
§5.1.

**Las dos tablas que este cambio toca están en cero, y las cuatro de las que su fixture depende
—`ACT_Activos`, `USR_Usuarios`, `EOT_EstadosOrden`, `FRE_Frecuencias`— ya tienen datos reales.** El
fixture entra, reutilizando las cuatro tablas pobladas sin tocarlas, y creando únicamente filas
nuevas en `OT_OrdenesTrabajo`, `MAN_Mantenimientos` y `PLA_PlanMantenimiento`.

**Y esta vez, con una consecuencia que la versión anterior no declaraba: el fixture cierra la
ventana barata para siempre** (`ESPEC-005` §1, §3.4, §6). La limpieza de este fixture **no borra las
filas** (ver `P-13`): las marca `Activo = FALSE`. Después de esta tanda, `OT_OrdenesTrabajo`,
`MAN_Mantenimientos` y `PLA_PlanMantenimiento` **nunca vuelven a tener 0 filas**. Cualquier
especificación futura que toque su estructura tiene que asumir eso, no "tabla vacía, no cuesta
nada".

**Diferencia con el fixture de `PRUEBA-004`:** ahí la clave de la orden se podía escribir a mano
(`OTID = TEST-OT-004A`) porque `OTID` no tenía `Initial value` todavía. **Aquí ya no.** Tras
`ORDEN-005`, `OTID` y `PlanID` los genera `UNIQUEID()` y su valor no se elige. La marca `TEST` va en
`Observaciones` donde existe (`OT_OrdenesTrabajo`, `MAN_Mantenimientos`); `PLA_PlanMantenimiento` no
tiene esa columna, y su fila de prueba se identifica por el `UNIQUEID()` que devuelve el `diff` de
`instantanea.py` entre el guardado inmediatamente anterior y el inmediatamente posterior a crearla —
nunca por ser "la única fila que existe" (`ESPEC-005` §6; ver `P-17`).

### 1.2 `validar_modelo.py`, `verificar_faseA.py`, `verificar_datos.py`, hoy

```
$ python scripts/validar_modelo.py
Tablas: 28 | Columnas: 211 | Referencias: 39 | Reglas: 21
ERRORES: ninguno
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
11 avisos: [G-01] SED_Sedes.UnidadFuncionalID, [G-04] x8 tablas vacias (OT_OrdenesTrabajo con
12 columnas, PLA_PlanMantenimiento con 7 — no 13 y 8: ver P-08), [G-03] PAR_Parametros.Valor,
[G-05] ACT_Activos.SedeID
DATOS COHERENTES: 0 obligatorias vacias sin motivo, 0 referencias huerfanas
```
Los dos `F-11` de arriba son exactamente los que `ESPEC-005` §2.3 dice que van a dejar de tener
nada que decidir en cuanto las dos tablas entren en `CLAVE_GENERADA` — es lo que prueba `P-04`.

### 1.3 `CLAVE_LEGIBLE`, `CLAVE_GENERADA` y `REGLAS`, contadas hoy

```
$ python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M
print(len(M.CLAVE_LEGIBLE)); print(len(M.CLAVE_GENERADA)); print(len(M.REGLAS))"
22
6
21
```
Después de `ORDEN-005`: `CLAVE_LEGIBLE` en 20, `CLAVE_GENERADA` en 8, `REGLAS` en 23 (21 + `RG-35` +
`RG-36`). Es lo que `P-01` y `P-02` comprueban.

### 1.4 `docs/ROADMAP.md` §4.5 — comprobado hoy, y ya no es un riesgo

Ya se corrigió, fuera de esta prueba y de esta especificación:

```
$ grep -n "Creación de órdenes desde la app" docs/ROADMAP.md
346:| Creación de órdenes desde la app | **Desbloqueada, pendiente de aplicar.** (...)
```
No hace falta ninguna prueba sobre este punto.

### 1.5 `auditar_cableado.py`, corrido en vivo hoy — el hallazgo que `ESPEC-005` §2.8 abre

```
$ python scripts/auditar_cableado.py
0 correcciones en el editor
De las 39 referencias: 4 VERIFICADAS, 29 compatibles no atribuidas, 6 NO SE PUEDEN JUZGAR
  - MAN_Mantenimientos.OTID -> OT_OrdenesTrabajo mirada el 2026-08-10 por Diego, en el editor
  - OT_OrdenesTrabajo.OTOrigenID -> OT_OrdenesTrabajo mirada el 2026-08-10 por Diego, en el editor
```
Las dos referencias hacia `OT_OrdenesTrabajo` están **miradas a ojo, no medidas**, porque su destino
sigue vacío. Esta tanda es la primera vez que va a haber filas ahí para medirlas de verdad — es lo
que prueba `P-14`, y es la razón por la que `auditar_cableado.py` entra en esta tanda y no aparecía
en ninguna versión anterior de `PRUEBA-005`.

## 2. Pruebas

### Familia A — Modelo (Python), automáticas

Todas corridas hoy contra una copia temporal de `scripts/` y `docs/` fuera del repositorio (no sobre
el repositorio real), con los cambios de `ESPEC-005` §4 aplicados a mano sobre esa copia. El
repositorio real queda sin tocar.

#### P-01 — El modelo todavía tiene lo que `ESPEC-005` manda mover (hoy falla; TDD real) — INNEGOCIABLE

- **Qué comprueba:** que `OTID` y `PlanID` siguen en `CLAVE_LEGIBLE` y fuera de `CLAVE_GENERADA`,
  que `REGLAS` no tiene `RG-35` ni `RG-36`, que ninguna de las dos tablas tiene una columna llamada
  `Etiqueta` en `MODELO` (**tiene que seguir sin tenerla incluso después de `ORDEN-005`**: es
  virtual, nunca entra en `MODELO` — ver la nota bajo el bloque), que `SIN_ETIQUETA_NATURAL` sigue
  citando `OT_OrdenesTrabajo`, y que `inferencia.py` no tiene todavía ningún `ETIQUETA_VIRTUAL`.
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
  ids = {r["id"] for r in M.REGLAS}
  if "RG-35" in ids: fallos.append("RG-35 ya existe")
  if "RG-36" in ids: fallos.append("RG-36 ya existe")
  cols_ot = {c["nombre"] for c in M.MODELO["OT_OrdenesTrabajo"]["columnas"]}
  cols_pla = {c["nombre"] for c in M.MODELO["PLA_PlanMantenimiento"]["columnas"]}
  if "Etiqueta" in cols_ot: fallos.append("OT ya tiene Etiqueta en MODELO (no deberia, es virtual)")
  if "Etiqueta" in cols_pla: fallos.append("PLA ya tiene Etiqueta en MODELO (no deberia, es virtual)")
  if "OT_OrdenesTrabajo" not in I.SIN_ETIQUETA_NATURAL: fallos.append("OT ya salio de SIN_ETIQUETA_NATURAL")
  if hasattr(I, "ETIQUETA_VIRTUAL"): fallos.append("ETIQUETA_VIRTUAL ya existe en inferencia.py")
  print("FALLA:" if fallos else "PASA: 0 fallos")
  for f in fallos: print("  -", f)
  EOF
  ```
- **Resultado — hoy, 2026-08-10, corrido de verdad:**
  ```
  PASA: 0 fallos
  ```
  («PASA» significa «el estado previo al cambio se confirma intacto», la lectura correcta antes de
  `ORDEN-005`.)
- **Resultado esperado — después de `ORDEN-005`:** el mismo script, con cada condición invertida
  (**salvo las dos de `Etiqueta` en `MODELO`, que tienen que seguir en negativo**: la columna es
  virtual y no debe aparecer nunca ahí, ni antes ni después), tiene que dar `PASA: 0 fallos`.
  Verificado por simulación hoy contra una copia temporal: con los cambios aplicados, `RG-35` y
  `RG-36` existen en `REGLAS`, `Etiqueta` sigue ausente de `MODELO` en las dos tablas,
  `SIN_ETIQUETA_NATURAL` ya no cita `OT_OrdenesTrabajo`, y `ETIQUETA_VIRTUAL` existe con las dos
  entradas.
- **Cómo se distingue el fallo:** si después de `ORDEN-005` `Etiqueta` aparece en `MODELO`, es una
  señal de que se implementó como `App formula` sobre columna real en vez de virtual —el defecto de
  diseño que el arquitecto bloqueó—, no un progreso.

#### P-02 — `validar_modelo.py` en 0 errores, con las cifras exactas

- **Qué comprueba:** que mover dos tablas de lista y añadir dos reglas no rompe nada, y que
  `Columnas` **no sube** (a diferencia de lo que predecía la versión anterior con `Etiqueta` como
  columna real).
- **Precondición:** `ORDEN-005` aplicada.
- **Acción:** `python scripts/validar_modelo.py`
- **Resultado esperado, verificado por simulación hoy:**
  ```
  Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
  ERRORES: ninguno
  AVISOS (3): [V-06] x2, [V-14] — los mismos de siempre, ninguno nuevo
  APTO PARA DESPLEGAR
  ```
  **`Columnas` se queda en 211**, no sube a 213: es la prueba automática de que `Etiqueta` nunca
  entró en `MODELO`. `Reglas` sube de 21 a 23.
- **Cómo se distingue el fallo:** si `Columnas` sube a 213, `Etiqueta` se implementó como columna
  real de `MODELO`, no virtual — el mismo defecto que marca `P-01`. Si aparece un `V-17` nuevo, algo
  tocó por error una comparación legítima contra `EOT_EstadosOrden`, `FRM_Formularios`,
  `PAR_Parametros` o `SEN_Sentidos`.

#### P-03 — `V-11` cazando `RG-35`/`RG-36` mal escritas — INNEGOCIABLE, resuelve el hallazgo de diseño

- **Qué comprueba:** que declarar `Etiqueta` como `REGLA` (y no como columna de `MODELO`) es lo que
  garantiza que una expresión mal escrita se valide. No es una comprobación redundante con `V-11`
  ya recorriendo columnas (fix aplicado antes de esta versión): como `Etiqueta` **nunca** es una
  columna de `MODELO`, no hay ningún `c["formula"]` para esa columna que `V-11` pueda recorrer por
  esa vía. La única puerta que la valida es que esté en `REGLAS`.
- **Precondición:** `ORDEN-005` aplicada tal como dice `ESPEC-005` §4.
- **Acción — corrida de verdad, no simulada, sobre la copia temporal:**
  ```bash
  # 1. Confirmar que el modelo con RG-35/RG-36 correctas pasa limpio
  python scripts/validar_modelo.py   # baseline: 0 errores

  # 2. Corromper a mano RG-35: [ActivoID].[Nombre] -> [Activo].[Nombre]
  #    (Activo SI existe en OT_OrdenesTrabajo, pero es Yes/No, no Ref: R-7,
  #    "cuidado con el nombre reutilizado")
  python - <<'EOF'
  p = "scripts/modelo_objetivo.py"
  s = open(p, encoding="utf-8").read()
  s = s.replace(
      'CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])',
      'CONCATENATE([Activo].[Nombre], " - ", [FechaProgramada])')
  open(p, "w", encoding="utf-8").write(s)
  EOF
  python scripts/validar_modelo.py
  ```
- **Resultado — verificado hoy, corrida real sobre la copia temporal:**
  ```
  ERRORES (1) - el modelo no se puede desplegar asi:
    x [V-11] RG-35: no se puede desreferenciar OT_OrdenesTrabajo.Activo, es Yes/No y no Ref
  NO APTO: corrige los errores
  ```
  Restaurada la expresión correcta, `validar_modelo.py` vuelve a `ERRORES: ninguno`, verificado en
  la misma corrida.
- **Cómo se distingue el fallo:** si esta corrupción **no** produce un error —por ejemplo, porque
  alguien implementó `Etiqueta` como columna de `MODELO` con `formula=` en vez de como `REGLA`, y el
  recorrido de columnas de `V-11` sí la ve pero por una ruta distinta a la que `ESPEC-005` declaró—,
  hay que revisar cómo quedó declarada antes de continuar: el punto de esta prueba es que la
  detección dependa de estar en `REGLAS`, no de cualquier otra vía.

#### P-04 — `verificar_faseA.py` vuelve a `FASE A CERRADA` sin tocar la hoja — INNEGOCIABLE

- **Qué comprueba:** lo contrario de lo que predecía la versión anterior de esta prueba. Ahí, `P-03`
  esperaba un `F-02` ("faltan columnas del modelo") antes de regenerar la hoja, y que ese `F-02`
  desapareciera después de correr `generar_plantilla.py`. **Con `Etiqueta` como columna virtual, eso
  no pasa: no hace falta regenerar la hoja en ningún momento**, porque una columna virtual nunca es
  una de las columnas que `F-02` exige encontrar en el archivo.
- **Precondición:** `ORDEN-005` aplicada sobre `scripts/modelo_objetivo.py` e `inferencia.py`. **La
  hoja NO se toca.**
- **Acción:** `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"`
- **Resultado, verificado hoy por simulación (sin regenerar nada):**
  ```
  AVISOS (2): [F-01] OT_OrdenesTrabajo.Activo (esperado), [F-04] 14 columnas pendientes de Ref
  FASE A CERRADA
  ```
  Ningún `F-02` en ningún momento. Los dos `F-11` de hoy (§1.2) desaparecen, porque `CLAVE_GENERADA`
  los exime — no porque la hoja cambiara.
- **Cómo se distingue el fallo:** si aparece un `F-02` mencionando `Etiqueta`, alguien la declaró
  como columna de `MODELO` en vez de virtual — señal exacta del defecto de diseño que el arquitecto
  bloqueó, y la misma señal que da `P-01`/`P-02` por otra vía. Tres pruebas independientes cazando el
  mismo error no es redundancia: es que el error es precisamente el que costó catorce hallazgos la
  vez pasada.

#### P-05 — `verificar_reproducible.py` sigue reproducible

- **Qué comprueba:** que `CLAVE_GENERADA`/`CLAVE_LEGIBLE` no introducen una fuente de variación entre
  dos pasadas del generador de la hoja. Como `Etiqueta` no toca `generar_plantilla.py` (no usa
  `CLAVE_GENERADA` ni `CLAVE_LEGIBLE`, verificado con `grep -n "CLAVE_GENERADA\|CLAVE_LEGIBLE"
  scripts/generar_plantilla.py`, sin resultados), esta prueba en rigor no ejercita nada nuevo de
  `Etiqueta`, pero se conserva como control de no regresión sobre el generador de la hoja.
- **Precondición:** `ORDEN-005` aplicada.
- **Acción:** `python scripts/verificar_reproducible.py`
- **Resultado esperado, verificado por simulación hoy:** `REPRODUCIBLE: las 29 pestanas salen
  identicas`, sin diferencias.
- **Cómo se distingue el fallo:** alguna pestaña sale distinta entre las dos pasadas.

#### P-06 — `inferencia.py` asigna `Etiqueta` vía `ETIQUETA_VIRTUAL`, no vía `ETIQUETAS`

- **Qué comprueba:** que `etiqueta_de()` deja de devolver `None` para `OT_OrdenesTrabajo` y
  `PLA_PlanMantenimiento`, por el mecanismo correcto. **Se verificó primero que el mecanismo de la
  versión anterior no funciona**: añadir `"Etiqueta"` a la tupla `ETIQUETAS` sin más, y `etiqueta_de`
  seguía devolviendo `None`, porque esa tupla se compara contra `MODELO[tabla]["columnas"]` y
  `Etiqueta` nunca vive ahí. El mecanismo correcto (`ESPEC-005` §3.2, §4) es un diccionario nuevo,
  `ETIQUETA_VIRTUAL`, consultado antes que `SIN_ETIQUETA_NATURAL`/`ETIQUETAS`.
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
- **Resultado, verificado hoy por ejecución real sobre la copia temporal:**
  ```
  OT Etiqueta
  PLA Etiqueta
  MAN None
  CHK None
  OT_OrdenesTrabajo Etiqueta 2
  ```
  `PLA_PlanMantenimiento` no aparece en `etiquetas_pendientes()` — sigue sin ninguna referencia
  entrante (§2.2 de `ESPEC-005`); se prueba por `P-17`, no por esta vía.
- **Cómo se distingue el fallo:** `OT` o `PLA` siguen devolviendo `None` — señal de que
  `ETIQUETA_VIRTUAL` no se creó o `etiqueta_de()` no la consulta primero.

#### P-07 — `RECONSTRUCCION_EXPRESIONES.md` y `PROMPT_EXPRESIONES.md` documentan `Etiqueta` — INNEGOCIABLE

- **Qué comprueba:** exactamente lo que la versión anterior de esta prueba predecía que **iba a
  fallar** con el diseño de `App formula` sobre columna real y `REGLA` opcional. Con el diseño
  corregido —`Etiqueta` como columna virtual, declarada **solo** como `REGLA` (`RG-35`/`RG-36`, con
  `columna="(tabla)"`, molde de `RG-29`)—, esto deja de ser una promesa incumplida: `REGLAS` es
  justamente por donde iteran los dos generadores (`for r in REGLAS`, `generar_reconstruccion.py:59`;
  `from modelo_objetivo import MODELO, REGLAS`, `generar_prompt_expresiones.py:37`), así que no hace
  falta ningún mecanismo adicional.
- **Precondición:** `ORDEN-005` aplicada exactamente como dice `ESPEC-005` §4.
- **Acción, corrida de verdad sobre la copia temporal:**
  ```bash
  python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M
  print([r['id'] for r in M.REGLAS if 'Etiqueta' in r.get('descripcion','') and r['id'] in ('RG-35','RG-36')])"
  python scripts/generar_reconstruccion.py && grep -n "RG-35\|RG-36" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
  python scripts/generar_prompt_expresiones.py && grep -c "RG-35\|RG-36" docs/PROMPT_EXPRESIONES.md
  ```
- **Resultado, corrida de verdad hoy:**
  ```
  ['RG-35', 'RG-36']
  227:### RG-35 — `OT_OrdenesTrabajo` · `(tabla)`
  235:### RG-36 — `PLA_PlanMantenimiento` · `(tabla)`
  6
  ```
  Las tres salidas son no vacías. `docs/PROMPT_EXPRESIONES.md` incluye, para cada una, su tabla, su
  tipo (`App formula`), su expresión completa y la ruta de referencia que atraviesa
  (`OT_OrdenesTrabajo.ActivoID → ACT_Activos`, y para `RG-36` también `→ FRE_Frecuencias`),
  igual que las otras 21 reglas — **la prueba PASA**, al revés de lo que predecía la versión
  anterior.
- **Cómo se distingue el fallo:** si alguna de las tres salidas queda vacía, `Etiqueta` se declaró
  fuera de `REGLAS` (por ejemplo, como `formula=` de una columna de `MODELO`), reproduciendo el
  defecto que esta versión de `ESPEC-005` existe para evitar.

#### P-08 — `verificar_datos.py`: `G-04` NO sube de 12/7 columnas — confirma que `Etiqueta` nunca toca la hoja

- **Qué comprueba lo contrario de lo que la versión anterior afirmaba.** La versión anterior de
  `P-08` esperaba que el conteo de `G-04` subiera de 12/7 a 13/8 tras regenerar la hoja, y el
  arquitecto marcó que ese criterio no discrimina nada: `verificar_datos.py` cuenta
  `len(MODELO[t]["columnas"])`, que es el modelo, no la hoja. **Con el diseño corregido el punto es
  distinto y más fuerte: el conteo no debe subir nunca**, porque `Etiqueta` jamás entra en `MODELO`.
  Esta prueba verifica esa ausencia, no una presencia.
- **Precondición:** `ORDEN-005` aplicada. No hace falta regenerar la hoja (`P-04`).
- **Acción:** `python scripts/verificar_datos.py`
- **Resultado esperado, verificado por simulación hoy:** exactamente el mismo bloque de 11 avisos
  que hoy (§1.2), sin cambio alguno —**`OT_OrdenesTrabajo` sigue en 12 columnas, `PLA_PlanMantenimiento`
  en 7`**—, porque `Etiqueta` no está ni en `MODELO` ni en la hoja. El propio script, en su versión
  de hoy, ya lo dice de forma expresa para cada `G-04`: *"OJO: este archivo la vacia POR DISENO, asi
  que aqui saldra vacia aunque la aplicacion tenga filas. Para mirarla de verdad, instantanea.py"* —
  confirmando independientemente que `G-04` nunca fue ni puede ser la vía para verificar una columna
  de la hoja o del editor.
- **Cómo se distingue el fallo:** si el conteo sube a 13/8, `Etiqueta` se coló en `MODELO` como
  columna real — la misma señal que ya cazan `P-01`, `P-02` y `P-04`.

### Familia B — Configuración (AppSheet), no automáticas: ejercicio real de la app

**Cómo se lee de vuelta la mitad de esta familia: NADIE, salvo quien la ejecuta.** `Key`,
`Initial value`, `Label` y los datos que un formulario acepta o rechaza no viajan enteros por la API.
Se cierran documentando lo que se vio, literal.

**Precondición común, ampliada frente a la versión anterior:**

1. `ORDEN-005` aplicada en el editor siguiendo el orden de `ESPEC-005` §6 (`Initial value` antes de
   `Key`).
2. Sesión iniciada con una cuenta cuyo correo coincide con `USR-002`
   (`ivan.salcedo@concesiondelsisga.com.co`, verificado hoy contra `USR_Usuarios`), para que
   `MAN_Mantenimientos.TecnicoID` resuelva por `LOOKUP(USEREMAIL()...)`. Geolocalización del
   navegador fijada en `5.099798, -73.718568` (coordenada de `ACT-0001`, misma técnica de
   `PRUEBA-004` §1.5, mismo riesgo declarado ahí).
3. **Nuevo: `RG-07` (bot, `OT_OrdenesTrabajo`, evento `Adds`, notifica por correo al técnico
   asignado) se desactiva antes del primer paso de esta familia que cree una fila en
   `OT_OrdenesTrabajo`.** Es un hallazgo de esta tanda, ausente de toda versión anterior: `RG-07`
   dispara con **cualquier** fila nueva en `OT_OrdenesTrabajo`, la cree un técnico con el botón `+`
   (`P-10`) o el bot `RG-10` (`P-11`). Sin desactivarlo, esta tanda dispara **3 correos reales** —dos
   por `P-10` (`TEST-OT-005A`, `TEST-OT-005B`) y uno por la orden que crea `RG-10` en `P-11`— a
   `ivan.salcedo@concesiondelsisga.com.co`, una dirección corporativa, sobre órdenes marcadas `TEST`.
   Se desactiva en `Automation > Bots` → seleccionar `RG-07` → `Disable`, y se reactiva al cerrar el
   fixture (`P-13`, último paso). Cita: *"You can disable the bot to temporarily stop the automation.
   Then, re-enable it"* — [Bots: The Essentials](https://support.google.com/appsheet/answer/11432969?hl=en),
   AppSheet Help.

#### P-09 — `Key` queda en `OTID` y en `PlanID`, sin sembrar ninguna fila — y las dos referencias hacia `OT_OrdenesTrabajo` sobreviven al cambio — INNEGOCIABLE

- **Qué comprueba, en dos partes:**
  1. El argumento central con el que `ESPEC-005` §1 rechaza sembrar una fila de ejemplo: que
     declarar `Initial value = UNIQUEID()` sobre la tabla todavía vacía basta para que el editor deje
     marcar `Key`, sin necesitar ni una sola fila de datos.
  2. **Nuevo, resuelve `ESPEC-005` §2.8/§6.** Cambiar la clave de `OT_OrdenesTrabajo` (de
     `_RowNumber` implícito a `OTID`) es, según la documentación oficial, exactamente el escenario en
     que "esas referencias se romperán". Hoy `MAN_Mantenimientos.OTID` y `OT_OrdenesTrabajo.OTOrigenID`
     ya están configuradas como `Ref` a `OT_OrdenesTrabajo` (confirmado a ojo, `auditar_cableado.py`
     hoy, §1.5). Esta prueba tiene que confirmar que siguen así **después** de marcar `Key`.
- **Precondición:** `ORDEN-005` aplicada solo hasta declarar `Initial value = UNIQUEID()` en
  `OT_OrdenesTrabajo.OTID` y `PLA_PlanMantenimiento.PlanID`. **Las dos tablas siguen en 0 filas** —
  confirmar con `python scripts/instantanea.py guardar antes-de-p09` antes de tocar el editor.
- **Acción:**
  1. En *Data > Columns* de `OT_OrdenesTrabajo`, sobre `OTID`: confirmar `Initial value =
     UNIQUEID()`, marcar `Key`, `SAVE`. Repetir en `PLA_PlanMantenimiento.PlanID`. Copiar
     literalmente cualquier mensaje que aparezca.
  2. **Inmediatamente después**, sin cerrar el editor: abrir `MAN_Mantenimientos.OTID` y
     `OT_OrdenesTrabajo.OTOrigenID`, y confirmar a ojo que `Type` sigue en `Ref` y `Source table`
     sigue en `OT_OrdenesTrabajo`. Copiar literal lo que se ve. (No hay forma de medir esto por API
     mientras la tabla siga vacía — eso lo cierra `P-14`.)
- **Resultado esperado:** la casilla `Key` se marca sin protesta del editor, **sin ningún banner de
  error**, y en particular sin el mensaje `That Table uses RowNumber as a key which is not a stable
  key` que aparece hoy al intentarlo sin `Initial value`. `_RowNumber` queda desmarcado como clave en
  las dos tablas. `python scripts/instantanea.py guardar despues-de-p09` sigue mostrando **0 filas**
  en las dos tablas. Las dos referencias del punto 2 siguen configuradas como `Ref` a
  `OT_OrdenesTrabajo` sin cambio visible.
- **Cómo se distingue el fallo:** el editor sigue negándose a marcar `Key` (mismo mensaje de
  `RowNumber`) — el argumento con el que se rechazó sembrar deja de sostenerse y hay que reabrir esa
  decisión. O bien, tras marcar `Key`, `MAN_Mantenimientos.OTID` u `OT_OrdenesTrabajo.OTOrigenID`
  aparecen sin `Source table`, o convertidas de vuelta a `Text` — la confirmación de que el cambio de
  clave sí rompió las referencias, tal como advierte la cita oficial. En ese caso hay que
  reconfigurarlas antes de seguir con `P-10`.

#### P-10 — `OT_OrdenesTrabajo` admite creación desde la app — INNEGOCIABLE

- **Qué comprueba:** el punto 5 del encargo. Que un técnico puede dar de alta una orden con el botón
  `+`, y que la protección existente (`ActivoID` obligatorio) sigue activa.
- **Precondición:** `P-09` completada. **`RG-07` desactivado** (precondición común, punto 3).
- **Acción (positiva):** con la sesión de `USR-002`, en `OT_OrdenesTrabajo`, `+`: `ActivoID =
  ACT-0001`, `TecnicoID = USR-002`, `SupervisorID = USR-006`, `Tipo = Correctivo`, `FechaProgramada`
  = hoy, `EstadoOrdenID = Asignada`, `Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture
  A)"`. `SAVE`. Repetir para una segunda orden, `Observaciones = "TEST — PRUEBA-005, borrar tras
  P-13 (fixture B)"`.
- **Acción (negativa, mismo formulario, sin guardar antes):** repetir dejando `ActivoID` en blanco.
  Intentar `SAVE`.
- **Resultado esperado:** las dos positivas guardan sin error y aparecen en la lista **con `Etiqueta`
  ya visible** (aunque su cableado formal se prueba en `P-15`, esta es la primera vez que hay una
  fila real para verla). La negativa no guarda, y el formulario señala `ActivoID` como pendiente con
  el mensaje nativo de campo obligatorio.
- **Cómo se distingue el fallo:** el botón `+` no aparece (`RG-14` no se aplicó), o la fila con
  `ActivoID` en blanco se guarda igual.

#### P-11 — `RG-10` crea la orden de seguimiento, y esa orden EXISTE — INNEGOCIABLE

**Es la prueba que el encargo llama «la que de verdad importa».**

- **Qué comprueba:** que el defecto que abrió `ESPEC-005` —una fila que `RG-10` crea sin `OTID` y
  que AppSheet descarta sin avisar— no ocurre más, leído de vuelta con un instrumento independiente
  de la pantalla.
- **Precondición:** `P-10` completada. **Y, no cubierta por `ESPEC-005`:** `RG-10` cableada de
  verdad como `Bot` con su `Data > Actions` asociada, mapeando los campos obligatorios de la orden de
  seguimiento además de `OTOrigenID`. `RG-07` sigue desactivado.
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-antes-rg10
  ```
  En la app: abrir `TEST-OT-005A`, iniciar un mantenimiento, `EstadoActivoID = EST-01`, cerrar con
  `Coordenadas_Cierre_LatLong` capturada en `5.099798, -73.718568`, marcar `RequiereSegundaVisita =
  TRUE`, `Observaciones = "TEST — PRUEBA-005, borrar tras P-13 (fixture A)"`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-005-despues-rg10
  python scripts/instantanea.py comparar prueba-005-antes-rg10 prueba-005-despues-rg10
  ```
- **Resultado esperado:** el `comparar` muestra **dos** cambios de fila: `MAN_Mantenimientos` gana la
  fila que se acaba de cerrar, y **`OT_OrdenesTrabajo` gana una fila nueva que nadie creó a mano**,
  con `OTOrigenID` igual a la clave de `TEST-OT-005A`, `OTID` no vacío y distinto de cualquier
  literal escrito en esta prueba. Ninguna otra tabla cambia.
- **Cómo se distingue el fallo:** el `comparar` muestra solo el cambio en `MAN_Mantenimientos` y
  ninguno en `OT_OrdenesTrabajo` — el defecto original, ahora demostrado con datos.

#### P-12 — `RG-10` NO crea nada cuando la condición es falsa — INNEGOCIABLE

**La prueba negativa del punto 2 del encargo.**

- **Qué comprueba, y qué NO comprueba — precisado frente a la versión anterior.** Comprueba que la
  condición `[RequiereSegundaVisita] = TRUE` se evalúa de verdad y no crea una fila cuando es falsa,
  usando `instantanea.py comparar`, que solo ve **filas de la hoja**. Lo que esta prueba **no puede
  comprobar, y no hay que afirmar que comprueba**, es que no ocurrió ningún otro efecto: en
  particular, no puede decir si `RG-07` habría disparado un correo — la API no ve bots ejecutados,
  solo su resultado en la hoja. Es precisamente por eso que `RG-07` se desactiva para toda la
  familia (precondición común, punto 3) en vez de confiar en que esta prueba lo detectaría si no se
  desactivara.
- **Precondición:** `P-11` completada. Existe `TEST-OT-005B` (creada en `P-10`).
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-antes-manB
  ```
  En la app: abrir `TEST-OT-005B`, iniciar mantenimiento, `EstadoActivoID = EST-01`, cerrar con la
  misma coordenada de `ACT-0001`, **dejar `RequiereSegundaVisita` en `FALSE`**, `Observaciones =
  "TEST — PRUEBA-005, borrar tras P-13 (fixture B)"`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-005-despues-manB
  python scripts/instantanea.py comparar prueba-005-antes-manB prueba-005-despues-manB
  ```
- **Resultado esperado:** el `comparar` muestra **un solo** cambio de fila —la nueva fila de
  `MAN_Mantenimientos`—, y **es un cambio de fila, no de "todo lo que pasó"**: `OT_OrdenesTrabajo` no
  gana ninguna fila por esta acción, y esa es toda la afirmación que esta prueba sostiene.
- **Cómo se distingue el fallo:** aparece una fila nueva en `OT_OrdenesTrabajo` con `OTOrigenID`
  apuntando a `TEST-OT-005B` — señal de que `RG-10` se dispara con cualquier actualización, no con la
  condición declarada.

### Familia C — Datos (Sheets) y cableado, automática

#### P-13 — Lectura de vuelta completa, y cierre del fixture SIN `Delete` — INNEGOCIABLE

- **Qué comprueba:** que lo que la app mostró como guardado llegó al Sheets, que la `App formula` de
  `Etiqueta` escribió sobre las tres filas que existen en `OT_OrdenesTrabajo` (`TEST-OT-005A`,
  `TEST-OT-005B`, la de `RG-10`) y sobre ninguna otra tabla, y que la lectura por API y la lectura
  directa del archivo coinciden.
- **Precondición:** `P-11` y `P-12` ejecutadas. Existen 3 filas nuevas en `OT_OrdenesTrabajo` y 2 en
  `MAN_Mantenimientos`.
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-final
  ```
  Y, como segunda vía de lectura, abrir `Modelo_Datos_10082026` con el conector de Drive (vuelto a
  volcar con `python scripts/sistema.py` antes de usarlo) y localizar las filas por `Observaciones`
  conteniendo `"PRUEBA-005"` — nunca por la clave.
- **Resultado esperado:**
  - Exactamente 3 filas nuevas en `OT_OrdenesTrabajo` y 2 en `MAN_Mantenimientos`.
  - Las 3 filas de `OT_OrdenesTrabajo` tienen `Etiqueta` no vacía, distinta de su propio `OTID`, y
    conteniendo el nombre del activo — el contenido exacto se coteja contra la fórmula cerrada en
    `ESPEC-005` §3.3 (`CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])`, salvo el
    separador/formato de fecha que Fase C pueda ajustar).
  - Ninguna otra fila ni tabla cambió.
  - La lectura por API y por Drive coinciden.

**Cierre del fixture, en esta misma prueba — reescrito frente a la versión anterior, sin `Delete`:**

`scripts/appsheet_api.py` expone `Delete`, pero su propia cabecera advierte que esa decisión no está
tomada y que el histórico del proyecto no se borra (`ESPEC-005` §6). `RG-14`/`RG-15` retiraron
`Deletes` de la app precisamente por esto. **Esta prueba nunca invoca `Action: Delete`.** En su
lugar:

```bash
python - <<'EOF'
import sys; sys.path.insert(0, "scripts")
from appsheet_api import ejecutar_accion

# Claves reales: las que devolvio instantanea.py en el diff de P-11/P-12/P-10,
# no un literal (no hay ninguno: son UNIQUEID()).
for tabla, clave_col, claves in [
    ("OT_OrdenesTrabajo", "OTID", ["<clave-A>", "<clave-B>", "<clave-RG10>"]),
    ("MAN_Mantenimientos", "MantenimientoID", ["<clave-manA>", "<clave-manB>"]),
]:
    filas = [{clave_col: c, "Activo": False} for c in claves]
    ejecutar_accion(tabla, "Edit", filas=filas)
EOF
python scripts/instantanea.py guardar prueba-005-tras-cierre
```
- **Resultado esperado del cierre:** las 5 filas siguen existiendo —`OT_OrdenesTrabajo` y
  `MAN_Mantenimientos` **no vuelven a 0 filas**, y no es un fallo: es el diseño (`ESPEC-005` §3.4,
  §6)—, con `Activo = FALSE`. `Observaciones` se conserva con la marca `TEST`, para que cualquiera
  que las encuentre después sepa qué son.
- **Último paso de esta prueba: reactivar `RG-07`** (`Automation > Bots` → `RG-07` → `Enable`),
  cerrando la precondición común de la Familia B.
- Borrar del disco los archivos `BD/instantaneas/prueba-005-*.json` que esta tanda generó, siguiendo
  la higiene de `PRUEBA-004` §1.
- **Cómo se distingue el fallo:** alguna celda fuera de las 5 filas de prueba aparece en el
  `comparar`, `Etiqueta` sale vacía o igual a la clave en alguna de las 3 filas de `OT_OrdenesTrabajo`,
  o el cierre usó `Delete` en vez de `Edit` con `Activo = FALSE`.

#### P-14 — `auditar_cableado.py`, medido de verdad ahora que `OT_OrdenesTrabajo` tiene filas — INNEGOCIABLE

- **Qué comprueba:** resuelve `ESPEC-005` §2.8/§6. Hoy, con `OT_OrdenesTrabajo` vacía,
  `auditar_cableado.py` no puede medir si `MAN_Mantenimientos.OTID` y `OT_OrdenesTrabajo.OTOrigenID`
  están bien cableadas — solo hay una confirmación visual de antes de `ORDEN-005`
  (`CONFIRMADAS_A_OJO`, fechada 2026-08-10). Esta tanda deja, por primera vez, filas reales en
  `OT_OrdenesTrabajo` (las 3 del fixture, marcadas `Activo = FALSE` pero presentes), así que esta es
  la primera oportunidad de convertir esa confirmación visual en una medición real.
- **Precondición:** `P-13` completada (las 3 filas de `OT_OrdenesTrabajo` existen, `Activo = FALSE`).
- **Acción:** `python scripts/auditar_cableado.py`
- **Resultado esperado:** las dos referencias hacia `OT_OrdenesTrabajo` pasan de "NO SE PUEDEN
  JUZGAR" a **VERIFICADAS** o a alguna de las otras categorías medibles (compatible no atribuida,
  apunta a otra tabla, declarada y ausente, convertida en Ref sin serlo) — cualquiera de esas
  categorías es información nueva que hoy no existe. Si salen **VERIFICADAS**, `P-09` (punto 2) queda
  confirmado con medición, no solo a ojo: el cambio de clave no rompió las referencias. `0
  correcciones` en el resto del cableado, sin cambios respecto a hoy.
- **Cómo se distingue el fallo:** las dos referencias salen como "apuntan a otra tabla",
  "declaradas y ausentes" o "convertidas en Ref sin serlo" — cualquiera de esas tres es la
  confirmación de que cambiar la clave sí rompió lo que estaba configurado, y hay que
  reconfigurarlas antes de dar esta tanda por cerrada.

### Familia D — Configuración (AppSheet), cotejo a ojo

#### P-15 — `Etiqueta` es el `Label`, y el técnico ve texto, no `UNIQUEID()`

- **Qué comprueba:** el punto 4 del encargo. Es el paso que ningún comando puede verificar (`Label`
  no viaja por la API).
- **Precondición:** `P-06` (estructural) y `P-13` (hay filas con `Etiqueta` poblada).
- **Acción:** en *Data > Columns* de `OT_OrdenesTrabajo`, confirmar que la columna virtual `Etiqueta`
  tiene la casilla `Label` marcada. Abrir un desplegable que referencie `OT_OrdenesTrabajo` —el
  selector de `OTID` en el formulario de `MAN_Mantenimientos`— y copiar literalmente el texto de una
  de las opciones.
- **Resultado esperado:** el desplegable muestra el texto compuesto por `Etiqueta` (activo y fecha),
  no una cadena `UNIQUEID()`.
- **Cómo se distingue el fallo:** el desplegable sigue mostrando la clave.

#### P-16 — `Etiqueta` no se puede editar a mano

- **Qué comprueba:** que declarar `Etiqueta` como `App formula` (aunque sea virtual) la vuelve de
  solo lectura en el formulario.
- **Precondición:** `P-06` completada.
- **Acción:** en el formulario de `OT_OrdenesTrabajo` (edición de una fila existente), intentar
  escribir sobre el campo `Etiqueta`.
- **Resultado esperado:** el campo aparece gris/no editable, o si el formulario deja escribir, el
  valor vuelve al calculado por la fórmula en cuanto se guarda — cotejar cuál de los dos ocurre y
  copiarlo literal.
- **Cómo se distingue el fallo:** el valor escrito a mano se guarda y sobrevive a una recarga.

#### P-17 — `PLA_PlanMantenimiento` también admite creación y también tiene `Etiqueta`, identificada sin depender de "es la única fila"

- **Qué comprueba:** el mismo mecanismo que `P-09`/`P-10`/`P-13` pero sobre la segunda tabla, con la
  marca `TEST` resuelta de otra forma: `ESPEC-005` §6 señala que `PLA_PlanMantenimiento` no tiene
  ninguna columna de texto libre, así que "es la única fila que existe" no sirve como discriminador
  —deja de ser cierto si algo falla a mitad de la tanda—.
- **Precondición:** `P-09` completada para `PlanID`.
- **Acción:**
  ```bash
  python scripts/instantanea.py guardar prueba-005-antes-pla
  ```
  Con la sesión de operación (o `USR-002`), en `PLA_PlanMantenimiento`, `+`: `ActivoID = ACT-0001`,
  `FrecuenciaID = FRE-04` (Mensual), `UltimaEjecucion` = hoy menos 30 días, `ResponsableID =
  USR-002`. `SAVE`.
  ```bash
  python scripts/instantanea.py guardar prueba-005-despues-pla
  python scripts/instantanea.py comparar prueba-005-antes-pla prueba-005-despues-pla
  ```
- **Resultado esperado:** el `comparar` identifica **la clave exacta** (`UNIQUEID()`) de la fila
  nueva por el `diff`, no por conteo. `PlanID` no vacío, `ProximaFecha` calculada por `RG-11`,
  `Etiqueta` no vacía y con el nombre del activo y de la frecuencia.
- **Cierre de esta prueba, sin `Delete`:** usando la clave identificada por el `diff`,
  `ejecutar_accion("PLA_PlanMantenimiento", "Edit", filas=[{"PlanID": "<clave>", "Activo": False}])`.
  Confirmar con una instantánea que la fila sigue existiendo, ahora con `Activo = FALSE`.
- **Cómo se distingue el fallo:** la fila no se guarda, se guarda sin `PlanID`, `Etiqueta` queda
  vacía, o el cierre borra la fila en vez de marcarla inactiva.

## 3. Pruebas bloqueadas

- **`RG-12` en ejecución real.** Sigue bloqueada por el plan gratuito (decisión `D-B`). **BLOQUEADA
  POR** la ausencia de plan pagado.
- **`P-11` y `P-12` en su forma de app**, si la técnica de geolocalización simulada por DevTools no
  funciona contra este despliegue y no es viable ejecutar físicamente junto a `ACT-0001`. **BLOQUEADA
  POR** falta de un método verificado para satisfacer `RG-01` sin tocar `Coordenadas_Cierre_LatLong`
  — la misma causa que `PRUEBA-004` ya declaró.
- **El cotejo exacto de texto de `Etiqueta` en `P-13`/`P-15`**, si el separador/formato de fecha no
  se cerró todavía en Fase C (`ESPEC-005` §3.3, §7 supuesto 6). El cotejo se degrada entonces a "no
  vacía, no igual a la clave, contiene el nombre del activo" — un criterio más débil, no un bloqueo
  total: a diferencia de la versión anterior, aquí ya existe una expresión de referencia
  (`CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])`) contra la que comparar, aunque el
  separador final pueda cambiar.

Frente a la versión anterior, **ya no hay ninguna prueba bloqueada por `P-07`**: se verificó que
`P-07` pasa con el diseño corregido (columna virtual + `REGLA`), así que esa condición desapareció.

## 4. Criterio de cierre

**Tienen que pasar todas menos las que queden `BLOQUEADA POR` en el momento de ejecutar**, y en
concreto:

- `P-01` a `P-08` (Familia A) son la condición de entrada: si alguna falla, `ORDEN-005` está
  incompleta. `P-03` en particular (`V-11` cazando la expresión corrompida) es la prueba de que el
  diseño de columna virtual + `REGLA` funciona como se declara en `ESPEC-005`, no solo que se
  declaró.
- `P-09`, `P-11`, `P-12`, `P-13` y `P-14` son innegociables: sin las cinco, no hay evidencia de que un
  técnico o un bot puedan crear una orden que sobreviva **y** de que crear esa orden no rompió el
  cableado que ya estaba puesto (`P-14`, el hallazgo nuevo de esta versión).
- `P-10` cierra el punto 5 del encargo.
- `P-15`, `P-16` y `P-17` cierran los flecos de `Label`, edición manual y la segunda tabla; no son
  innegociables, pero tienen que quedar documentados con el texto literal visto.
- **Antes de dar la tanda por cerrada, confirmar que `RG-07` quedó reactivado** (último paso de
  `P-13`): dejarlo desactivado sería resolver un riesgo de esta prueba creando uno permanente sobre
  producción.
- **A partir del cierre de `P-13`, cualquier especificación futura sobre `OT_OrdenesTrabajo`,
  `MAN_Mantenimientos` o `PLA_PlanMantenimiento` tiene que asumir que ya no están vacías** (`ESPEC-005`
  §1, §3.4): la ventana barata de este cambio se cerró aquí, con estas filas marcadas `Activo =
  FALSE` y `TEST`, no al final del despliegue completo.
