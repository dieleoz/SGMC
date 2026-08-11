# PRUEBA-004 — Pruebas de aceptación de ESPEC-004

**Renumerada el 2026-08-10 tras el bloqueo del arquitecto.** Usaba `P-01`..`P-11`, y colisionaba: dos
`P-09` distintos existían a la vez —uno en `PRUEBA-003`, otro aquí—, los dos declarados
«innegociables». `PRUEBA-003` ya arrancaba en `P-21` por la misma razón; esta tanda arranca en
**`P-34`**, el primer número libre después de `PRUEBA-003` (hasta `P-33`).

**Escrita antes de que `ORDEN-004` exista.** Nada de lo que sigue se ejecutó contra el modelo, la
hoja ni el editor: los comandos marcados «automática» sí se corrieron —son de solo lectura, o
corren sobre una copia de `scripts/` y del volcado fuera del repositorio para predecir el resultado
exacto— y sus salidas están citadas literalmente. Los que requieren la app están descritos para
cuando el ejecutor los corra, no ejecutados aquí.

**Supuesto que gobierna esta tanda entera, heredado de `ESPEC-004`: `ORDEN-005` ya está aplicada.**
`OTID` y `PlanID` generan su clave con `UNIQUEID()`, no se teclean. El fixture de esta tanda se
construye enteramente sin literales de clave — ver §1.3.

| | |
|---|---|
| Cubre | [`ESPEC-004-cierre-excepcion-manual.md`](ESPEC-004-cierre-excepcion-manual.md): retirar `RG-02`/`Precision_GPS`, retirar `RG-19`, dejar `CierreConExcepcion` editable por el técnico con `Description` formulada como pregunta, `RG-03` sin cambios de expresión |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (fileId `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Volcado con `python scripts/sistema.py`, no copiado de una tanda anterior |
| Reglas que esta tanda tiene que probar y `PRUEBA-003` no cubre | `RG-02` retirada, `RG-19` retirada, el tipo real de `CierreConExcepcion` (`S-30`), el límite exacto de `RG-20`, que los seis scripts generadores dejaron de citar el mecanismo retirado |
| Innegociables | `P-40`, `P-41`, `P-42`, `P-43` |

## 1. Estado de partida

### 1.1 Las tablas que hacen falta para el fixture

```
$ python scripts/instantanea.py guardar prueba-004-partida
Guardada: BD/instantaneas/prueba-004-partida.json
28 tablas · 953 filas en total
```

```
MAN_Mantenimientos   0
OT_OrdenesTrabajo    0
ACT_Activos          368
USR_Usuarios          11
EST_Activo             4
EOT_EstadosOrden       7
PAR_Parametros          3
```

Coincide con el volcado local (`openpyxl`, `BD/Modelo_Datos_PLANTILLA.xlsx`): `MAN_Mantenimientos`
y `OT_OrdenesTrabajo` en 1 fila de encabezado y cero de datos, el resto igual. La instantánea se
borró después de leerla, siguiendo la higiene que ya sigue `ESPEC-004` §2.0.

**`OT_OrdenesTrabajo` en cero es un dato que `ESPEC-004` no cita por nombre** —solo habla de
`MAN_Mantenimientos`— y cambia el tamaño del fixture: no basta con una fila de `MAN`, hace falta
también su orden. Y, por el supuesto de apertura, **esa orden nace con `OTID = UNIQUEID()`, no con
un literal**: la forma de crearla cambia respecto a lo que esta prueba habría hecho si `ESPEC-005`
no existiera — ver §1.3.

### 1.2 El fixture: entra en la prueba, no se aplaza

**Criterio:** entra. Aplazar la creación de la fila de `MAN_Mantenimientos` aplazaría la única
prueba capaz de demostrar que `RG-03` vuelve a disparar, que es el objeto entero de `ESPEC-004`.

Es un fixture **acotado, no abierto**: la cadena de arrastre se detiene en dos filas nuevas por
tabla.

```
ACT_Activos          368 filas  →  se reutiliza una existente, no se crea ninguna
USR_Usuarios          11 filas  →  se reutilizan dos existentes (un técnico, un supervisor)
EST_Activo              4 filas  →  se reutiliza una existente
EOT_EstadosOrden        7 filas  →  se reutiliza una existente
OT_OrdenesTrabajo       0 filas  →  SE CREAN dos, por el botón `+` de la app (RG-14, ESPEC-005),
                                     marcadas en Observaciones, con OTID = UNIQUEID()
MAN_Mantenimientos      0 filas  →  SE CREAN dos, una por cada OT, con MantenimientoID = UNIQUEID()
```

No arrastra activo, técnico ni estado nuevos porque esas cuatro tablas ya tienen datos reales que
sirven sin tocarlos.

**El borrado va en esta misma prueba**, siguiendo la regla de higiene de `SDD_PIPELINE_SGMC.md`
§5.1: es el último paso de `P-42`.

### 1.3 El fixture elegido — sin ninguna clave tecleada

`SDD_PIPELINE_SGMC.md` §5.1 dice «toda fila de prueba lleva la marca `TEST` **en su clave**». Esa
frase no se puede cumplir literalmente sobre `OT_OrdenesTrabajo` ni sobre `MAN_Mantenimientos`
después de `ESPEC-005`: las dos tienen su clave en `CLAVE_GENERADA`, así que `OTID` y
`MantenimientoID` los asigna `UNIQUEID()` en cuanto se guarda la fila, y no hay ningún campo donde
teclear `TEST-OT-004A`. Es la misma adaptación que ya usa `PRUEBA-005` §1.1 para su propio fixture:
**la marca va en `Observaciones`, la única columna de las dos tablas donde un literal se puede
escribir y buscar después**, y coincide con lo que ya declara el modelo sobre estas tablas
(`scripts/modelo_objetivo.py:849-859`, `CLAVE_GENERADA`).

| Campo | Valor | Por qué |
|---|---|---|
| `ActivoID` | `ACT-0001` (`SOS-001`, `TipoActivoID=TIP-001`, radio `0.05` km, `Ubicacion_LatLong = 5.099798, -73.718568`) | Existe, `Activo=TRUE`, coordenada poblada (§1.4) |
| Técnico | `USR-002` (Ivan Salcedo, `RolID=ROL-03` Técnico) | Rol correcto, correo real: `ivan.salcedo@concesiondelsisga.com.co` |
| Supervisor | `USR-006` (Fernand Bolivar, `RolID=ROL-02` Supervisor) | Rol correcto |
| `EstadoOrdenID` | `Asignada` al crear, `En ejecucion` al abrir el mantenimiento | Ciclo normal de una orden |
| `EstadoActivoID` (del `MAN`) | `EST-01` Operativo | Cierre normal, no una baja |
| Marca de la orden positiva | `Observaciones = "TEST — PRUEBA-004 (positiva), borrar tras P-42"` | Sustituye a la clave tecleada. Se crea con el botón `+` de `OT_OrdenesTrabajo` (`RG-14`, habilitado por `ESPEC-005`), no por API, para ejercitar el mismo camino que usará un supervisor real |
| Marca de la orden negativa | `Observaciones = "TEST — PRUEBA-004 (negativa), borrar tras P-42"` | Fila separada, para no mezclar los dos casos en una sola orden |
| Marca del mantenimiento positivo | `Observaciones = "TEST — PRUEBA-004 (positiva), borrar tras P-42"` | Mismo texto que su orden, para poder cruzarlas al leer de vuelta |
| Marca del mantenimiento negativo | `Observaciones = "TEST — PRUEBA-004 (negativa), borrar tras P-42"` | Ídem |

**Ninguna clave de esta tanda se conoce de antemano.** Se leen de vuelta después de crear cada fila
(§ Familia C), nunca se predicen ni se escriben a mano — es la misma disciplina que usa `PRUEBA-005`
`P-11`/`P-13` para el mismo problema.

### 1.4 `Ubicacion_LatLong` está poblada — verificado de nuevo, y contra quién estaba mal la cita

`ESPEC-004` §2.6 corrigió, en esta misma revisión, una acusación falsa: la versión anterior de este
documento decía que `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` afirmaba que `Ubicacion_LatLong` está vacía.
**Es al revés**: la línea 149 de ese archivo dice, verificado hoy, que está *poblada* en las 368,
con valores sintéticos derivados del `PK`. El documento que sí dice —de forma desactualizada— que
está vacía es `Manuales/MANUAL_DE_USUARIO.md`, en sus líneas 46, 168 y 266, que `ESPEC-004` §4
incluye entre lo que hay que corregir a mano.

Esta prueba depende del hecho, no de qué documento lo dice bien o mal:

```
ACT-0001  Ubicacion_LatLong = 5.099798, -73.718568
```

### 1.5 El obstáculo real: `RG-01` no se evita, se satisface por construcción — y hace falta un discriminador antes de confiar en el resultado

`Coordenadas_Cierre_LatLong` tiene `Initial value = HERE()` y queda `Editable_If = FALSE` (`RG-20`,
que esta prueba no toca — ver `P-44`): en el formulario real, el pin **no es arrastrable**. Si quien
ejecuta la prueba no está físicamente en el corredor, `HERE()` capturará su ubicación real, y `RG-01`
rechazará el cierre antes de llegar a `RG-03`.

**La solución no depende de estar cerca del activo, sino de que la distancia sea exactamente cero**,
que satisface `DISTANCE(...) <= [RadioGeofencingKm]` para cualquier radio positivo. Se logra
sustituyendo lo que el navegador entrega a `HERE()`:

```
Chrome DevTools → More tools → Sensors → Location → Custom
Latitud:  5.099798
Longitud: -73.718568
```

**Esto es una técnica de prueba de navegador, no un comportamiento de AppSheet**, y no está citada en
`BASE_CONOCIMIENTO_APPSHEET.md`. Si no funciona, el método de reserva es ejecutar la prueba
físicamente junto a `ACT-0001` (`PK 00+100`), y si tampoco es viable en la fecha de ejecución, `P-40`
y `P-41` pasan a `BLOQUEADA POR` con esa causa.

**Y antes de confiar en que `P-40`/`P-41` pasaron por la razón correcta, hay un discriminador que
cumplir, citado en `ESPEC-004` §2.10 desde `docs/BASE_CONOCIMIENTO_APPSHEET.md:300`:** no hay página
oficial que confirme que AppSheet evalúa un `Valid_If` sobre una columna con `Editable_If = FALSE`.
Si no lo evalúa, `RG-01` nunca se ejecuta sobre `Coordenadas_Cierre_LatLong`, y **cualquier cierre se
guardaría igual, con la técnica de spoofing funcionando o sin funcionar** — `P-40` y `P-41` pasarían
por una razón que no tiene nada que ver con `RG-03`.

**Precondición añadida, antes de dar por buena esta familia:** confirmar que `P-09` de `PRUEBA-003`
(cierre fuera de rango, **innegociable** en esa tanda) se ejecutó **sobre este mismo despliegue** —la
aplicación se reconstruyó entera el 2026-08-10, así que una `P-09` de una reconstrucción anterior no
sirve— y que su caso lejano fue **rechazado**. Si `P-09` de `PRUEBA-003` no se ha corrido todavía
sobre esta aplicación, o si su resultado no está documentado con la misma disciplina que exige esta
tanda, `P-40`/`P-41` de esta tanda no cuentan como evidencia de nada hasta que se corra: es la misma
comprobación que `scripts/generar_manual_despliegue.py:850` ya instruye —*"pruebe un cierre cercano
y uno lejano. Si los dos salen aceptados, sospeche de esto antes que del radio."*

### 1.6 El tipo de `CierreConExcepcion` — el hallazgo que más pesa en esta tanda

`docs/ALCANCE_Y_SUPUESTOS_SGMC.md`, entrada `S-30`, dejó verificado el 2026-08-10: de las 10
columnas `Yes/No` en tablas sin una sola fila, **`CierreConExcepcion` es una de ellas y salió `Text`**
al inferir sobre una tabla vacía. Con la columna `Text`, `[CierreConExcepcion] = TRUE` en `RG-03`
compara texto contra el booleano `TRUE`, que **es siempre falso y no da error**.

`ESPEC-004` §3 y §4 no dicen nada sobre corregir este tipo: describen el estado objetivo de
`CierreConExcepcion` dando por hecho el tipo que `S-30` ya encontró mal. **Si nadie lo retipa en
`Data > Columns` al cablear esta tabla, `ESPEC-004` se aplica entera y el defecto que vino a
corregir sigue exactamente igual**, ahora por el tipo en vez de por el `Precision_GPS` en blanco. Es
la razón de que `P-43` sea, junto con `P-40`, `P-41` y `P-42`, innegociable.

## 2. Pruebas

### Familia A — Modelo (Python), automáticas

Corren contra `scripts/modelo_objetivo.py` y compañía. No requieren API ni editor.

#### P-34 — El modelo todavía tiene lo que `ESPEC-004` manda retirar (hoy falla; es la regla que precede al cambio)

- **Qué comprueba:** que `Precision_GPS`, `RG-02`, `RG-19` y la fórmula de `CierreConExcepcion`
  siguen vivos en `scripts/modelo_objetivo.py` **antes** de `ORDEN-004`.
- **Precondición:** ninguna. Corre contra el archivo tal como está hoy.
- **Acción:**
  ```bash
  python - <<'EOF'
  import sys; sys.path.insert(0, "scripts")
  import modelo_objetivo as M

  fallos = []
  cols = {c["nombre"] for c in M.MODELO["MAN_Mantenimientos"]["columnas"]}
  if "Precision_GPS" in cols:
      fallos.append("Precision_GPS sigue en la lista de columnas de MAN_Mantenimientos")
  cce = next(c for c in M.MODELO["MAN_Mantenimientos"]["columnas"] if c["nombre"] == "CierreConExcepcion")
  if cce.get("formula"):
      fallos.append("CierreConExcepcion todavia tiene formula: %r" % cce.get("formula"))
  ids = {r["id"] for r in M.REGLAS}
  if "RG-02" in ids: fallos.append("RG-02 sigue en REGLAS")
  if "RG-19" in ids: fallos.append("RG-19 sigue en REGLAS")
  rg20 = next(r for r in M.REGLAS if r["id"] == "RG-20")
  if "Precision_GPS" in rg20["descripcion"]:
      fallos.append("RG-20 todavia menciona Precision_GPS en su descripcion")
  if "Precision_GPS" not in M.CAMPOS_RETIRADOS.get("MAN_Mantenimientos", {}):
      fallos.append("Precision_GPS no esta en CAMPOS_RETIRADOS['MAN_Mantenimientos']")
  print("FALLA:" if fallos else "PASA: 0 fallos")
  for f in fallos: print("  -", f)
  EOF
  ```
- **Resultado esperado — HOY (antes de `ORDEN-004`):**
  ```
  FALLA:
    - Precision_GPS sigue en la lista de columnas de MAN_Mantenimientos
    - CierreConExcepcion todavia tiene formula: 'OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))'
    - RG-02 sigue en REGLAS
    - RG-19 sigue en REGLAS
    - RG-20 todavia menciona Precision_GPS en su descripcion
    - Precision_GPS no esta en CAMPOS_RETIRADOS['MAN_Mantenimientos']
  ```
  Corrido hoy, 2026-08-10, y es exactamente esta salida — la fórmula citada es la que quedó tras el
  arreglo de `RG-19` que `ESPEC-004` §2.2 documenta, no la versión sin `ISBLANK` que citaba una
  versión anterior de esta prueba.
- **Resultado esperado — DESPUÉS de `ORDEN-004`:** `PASA: 0 fallos`.
- **Cómo se distingue el fallo:** si tras `ORDEN-004` el script sigue listando algo, `ESPEC-004` §4
  no se aplicó completa.

#### P-35 — `validar_modelo.py` sigue en 0 errores

- **Qué comprueba:** que retirar `Precision_GPS` no deja huérfana la entrada `"Precision del GPS"`
  de `COBERTURA` (`scripts/validar_modelo.py:249`).
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:** `python scripts/validar_modelo.py`
- **Resultado esperado:** `ERRORES: ninguno` y `APTO PARA DESPLEGAR`. Verificado hoy antes de
  `ORDEN-004`: `Tablas: 28 | Columnas: 211 | Referencias: 39 | Reglas: 21`, 3 avisos, ninguno sobre
  `Precision_GPS` ni `V-13`, ninguno `V-18`. Tras `ORDEN-004`: `Reglas: 19` (se van `RG-02` y
  `RG-19`) y `Columnas: 210` (se va `Precision_GPS`).
- **Cómo se distingue el fallo:** aparece `[V-13] El flujo 'Precision del GPS' necesita
  MAN_Mantenimientos.Precision_GPS, que no existe`.

#### P-36 — `verificar_datos.py` (`G-05`) no seguiría citando un defecto ya cerrado — y aparece un aviso nuevo legítimo que no hay que confundir con una regresión

- **Qué comprueba:** dos cosas, no una. **Primero**, que el comentario de cabecera de `G-05`
  (`scripts/verificar_datos.py:213-214`, hoy cita `RG-19` como ejemplo del defecto que persigue) se
  actualiza o se sustituye por un ejemplo vigente, tal como pide `ESPEC-004` §4. **Segundo**, algo
  que `ESPEC-004` §2.9 verificó por simulación y que la versión anterior de esta prueba no
  contemplaba: en cuanto el fixture de la Familia C exista, `G-05` va a mostrar un aviso **nuevo y
  esperado**, no relacionado con `Precision_GPS`, sobre `UbicacionEscaneo_LatLong`/`RG-13` — hay que
  saber distinguirlo de una regresión antes de que aparezca, no después.
- **Precondición (primera parte):** `ORDEN-004` aplicada, **antes** de crear el fixture.
- **Acción:**
  ```bash
  grep -n "RG-19" scripts/verificar_datos.py
  python scripts/verificar_datos.py
  ```
- **Resultado esperado (antes del fixture):** el `grep` no encuentra `RG-19` citada como ejemplo del
  defecto que `G-05` persigue. La ejecución sigue en `DATOS COHERENTES`, sin ningún `G-05` sobre
  `MAN_Mantenimientos` ni `OT_OrdenesTrabajo` — las dos tablas siguen vacías en este punto, así que
  `G-04` sigue cubriéndolas y `G-05` sigue sin nada que mirar en ellas.
- **Resultado esperado (después del fixture, verificado por simulación en `ESPEC-004` §2.9):**
  ```
  ! [G-05] MAN_Mantenimientos.UbicacionEscaneo_LatLong esta vacia en las 2 filas y de ella depende
    RG-13. La regla queda configurada y sin efecto: no da error, no hace nada
  ```
  Este aviso **es esperado y no es un defecto de `ESPEC-004`**: `UbicacionEscaneo_LatLong` no se
  llena mientras el QR siga fuera de alcance, con fixture o sin él, y `RG-13` ya está fuera de
  alcance de este `ESPEC` (§2.5). No debe registrarse como hallazgo nuevo ni bloquear el cierre de
  esta tanda.
- **Cómo se distingue el fallo:** antes del fixture, el `grep` devuelve la línea original sin
  ninguna nota de cierre. Después del fixture, un `G-05` que mencione `Precision_GPS` (que ya no
  existe como columna, así que no debería poder aparecer) o `RG-02`/`RG-19` (retiradas) sí sería un
  fallo real — el de `UbicacionEscaneo_LatLong`/`RG-13` no lo es.

#### P-37 — `verificar_faseA.py` ya no cruza `Precision_GPS` contra una fórmula retirada

- **Qué comprueba:** que el bloque `F-12`/`F-13` (`scripts/verificar_faseA.py:307-386`) se retira.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:**
  ```bash
  grep -n "Precision_GPS\|RG-19" scripts/verificar_faseA.py
  python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
  ```
- **Resultado esperado:** el `grep` no devuelve nada del bloque `F-12`. La ejecución llega a `FASE A
  CERRADA` sin ningún `F-12`, y sin ningún `F-11` sobre `OT_OrdenesTrabajo`/`PLA_PlanMantenimiento`
  (`ORDEN-005` ya las movió a `CLAVE_GENERADA`, que `F-11` exime).
- **Cómo se distingue el fallo:** el bloque `F-12` sigue presente y compara `Precision_GPS` —columna
  que ya no existe— contra `CierreConExcepcion`. **O**, señal del riesgo de secuencia que `ESPEC-004`
  §2.9 documenta: aparece `[F-11] OT_OrdenesTrabajo: clave legible, coherente con CLAVE_LEGIBLE` —
  eso no es un fallo de `ESPEC-004`, es la prueba de que se está corriendo este script contra un
  `modelo_objetivo.py` que no tiene `ORDEN-005` completa. Si aparece, se detiene esta tanda entera:
  el orden de las dos especificaciones no se cumplió.

#### P-38 — `generar_diccionario_bd.py` ya no atribuye `UMBRAL_GPS` a `RG-19`

- **Qué comprueba:** que `lectores["UMBRAL_GPS"]` (`scripts/generar_diccionario_bd.py:159`) deja de
  decir `"RG-19"`.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:**
  ```bash
  grep -n 'lectores = ' -A 2 scripts/generar_diccionario_bd.py
  python scripts/generar_diccionario_bd.py
  grep -n "UMBRAL_GPS" docs/bd.md
  ```
- **Resultado esperado:** `lectores` ya no tiene la clave `"UMBRAL_GPS"`, y `docs/bd.md` regenerado
  muestra `UMBRAL_GPS` con la columna «Quién lo lee» en `—`.
- **Cómo se distingue el fallo:** `docs/bd.md` sigue diciendo `RG-19` en esa fila.

#### P-39 — Los seis generadores dejaron de instruir un mecanismo retirado — sin esta prueba, la tanda daba verde con documentos generados describiendo una columna que ya no existe

- **Qué comprueba:** el hallazgo de `ESPEC-004` §2.7 que la versión anterior de esta tanda no
  probaba en absoluto: tres scripts (`generar_prompt_expresiones.py`, `generar_guia_funcional.py`,
  `generar_manual_despliegue.py`) citan `Precision_GPS`/`RG-02`/`RG-19` con texto **fijo**, no
  derivado de `MODELO`/`REGLAS`. Regenerarlos sin editarlos produce documentos que le dicen al
  ejecutor que configure algo que `ESPEC-004` acaba de retirar — el peor caso posible para un
  documento generado.
- **Precondición:** `ORDEN-004` aplicada, incluyendo la edición a mano de los tres scripts (§4 de
  `ESPEC-004`).
- **Acción:**
  ```bash
  python scripts/generar_prompt_expresiones.py
  python scripts/generar_guia_funcional.py
  python scripts/generar_manual_despliegue.py
  grep -n "Precision_GPS\|USERLOCATIONACCURACY\|RG-02\b\|RG-19\b" docs/PROMPT_EXPRESIONES.md docs/GUIA_IMPLEMENTACION_FUNCIONAL.md docs/MANUAL_DESPLIEGUE.md
  python scripts/generar_tipos_esperados.py
  python -c "
  import sys; sys.path.insert(0,'scripts')
  import inferencia
  print('inferencia.py importa sin error')
  "
  ```
- **Resultado esperado:** el `grep` devuelve, como mucho, menciones históricas explícitamente
  marcadas como cerradas o superadas (ninguna que instruya a poner `Precision_GPS`, `Initial value =
  USERLOCATIONACCURACY()`, o la `App formula` de `RG-19` como algo vigente); ninguna de las tres
  cuenta ya "cuatro columnas no editables" en `MAN_Mantenimientos` — deben ser tres. Los otros dos
  regeneran sin error (no requieren edición, §2.7 de `ESPEC-004`).
- **Cómo se distingue el fallo:** el `grep` devuelve una línea con `Deja \`Precision_GPS\` con tipo
  \`Number\` y sin \`Initial value\`` (u otra instrucción equivalente): el encargo generado le está
  diciendo al ejecutor que configure una columna retirada. Es el fallo más caro de toda esta tanda,
  porque no se ve en el modelo ni en la app: se ve solo en el texto que alguien va a leer y seguir.

### Familia B — Configuración (AppSheet), no automáticas: ejercicio de la app

**Cómo se lee de vuelta: NADIE, salvo quien la ejecuta.** No hay comando: `Required_If` y
`Editable_If` no viajan por la API. Se cierran documentando lo que se vio, literal.

**Precondición común a `P-40` y `P-41`:** `ORDEN-004` aplicada; `ORDEN-005` aplicada y con `RG-14`
(`Adds`) cableada en `OT_OrdenesTrabajo`; `OTID`, `TecnicoID`, `EstadoOrdenID` cableados en
`OT_OrdenesTrabajo`; `OTID`, `TecnicoID`, `EstadoActivoID` cableados en `MAN_Mantenimientos`; `RG-01`
puesta; **el discriminador de §1.5 cumplido** (`P-09` de `PRUEBA-003` corrida sobre este despliegue,
con el caso lejano rechazado); sesión iniciada con `ivan.salcedo@concesiondelsisga.com.co` /
`USR-002`; geolocalización del navegador fijada en `5.099798, -73.718568` (§1.5).

#### P-40 — Positiva: el técnico marca la excepción y el sistema le exige el motivo — INNEGOCIABLE

- **Qué comprueba:** que `RG-03` bloquea el guardado cuando la casilla está marcada y
  `MotivoExcepcion` sigue vacío, y que deja guardar en cuanto se escribe el motivo.
- **Precondición:** la común de la Familia B, más una orden nueva creada con el botón `+` de
  `OT_OrdenesTrabajo`: `ActivoID = ACT-0001`, `TecnicoID = USR-002`, `SupervisorID = USR-006`, `Tipo
  = Correctivo`, `FechaProgramada` = hoy, `EstadoOrdenID = Asignada`, `Observaciones = "TEST —
  PRUEBA-004 (positiva), borrar tras P-42"`. `SAVE`, y anotar el `OTID` que AppSheet le asignó (no
  se conoce de antemano).
- **Acción:** abrir esa orden en el formulario del técnico, iniciar el mantenimiento,
  `EstadoActivoID = EST-01`, marcar la casilla cuya `Description` ahora pregunta explícitamente
  «¿La app no alcanzó buena precisión al capturar la posición de cierre?» (`ESPEC-004` §2.11),
  **intentar guardar sin escribir el motivo**, y luego escribir `"PRUEBA-004 — cobertura deficiente
  simulada"` en `Motivo de excepción` y guardar de nuevo. `Observaciones = "TEST — PRUEBA-004
  (positiva), borrar tras P-42"`.
- **Resultado esperado:** el primer intento **no guarda** y el formulario señala `MotivoExcepcion`
  como pendiente. El segundo intento guarda.
- **Cómo se distingue el fallo:** el primer intento guarda igual — `CierreConExcepcion` no está
  resolviendo a `TRUE`, el escenario exacto de `S-30` (`P-43` lo diagnostica), o `RG-03` no se
  cableó.

#### P-41 — Negativa: el técnico NO marca la excepción y el sistema le deja guardar sin motivo

- **Qué comprueba:** que `Required_If` no se volvió una obligación constante.
- **Precondición:** la común de la Familia B, más una segunda orden nueva, mismos datos que la de
  `P-40` salvo `Observaciones = "TEST — PRUEBA-004 (negativa), borrar tras P-42"`.
- **Acción:** abrir esa orden, `EstadoActivoID = EST-01`, **no** marcar la casilla, dejar `Motivo de
  excepción` en blanco, guardar. `Observaciones = "TEST — PRUEBA-004 (negativa), borrar tras P-42"`.
- **Resultado esperado:** guarda sin que el formulario pida nada sobre `MotivoExcepcion`.
- **Cómo se distingue el fallo:** el formulario bloquea el guardado pidiendo el motivo aunque la
  casilla esté sin marcar.

### Familia C — Datos (Sheets), automática

#### P-42 — Lectura de vuelta: qué quedó escrito en la hoja, identificado por `Observaciones` y no por la clave — INNEGOCIABLE

- **Qué comprueba:** que lo que la app dijo que guardó **llegó al Sheets**, con el valor correcto en
  las dos filas de `MAN_Mantenimientos` y en las dos de `OT_OrdenesTrabajo`, y que no escribió en
  ninguna celda que no debía. **A diferencia de la versión anterior de esta prueba, ninguna fila se
  localiza por su clave**: `OTID` y `MantenimientoID` son `UNIQUEID()` desde `ESPEC-005`, y no se
  pueden predecir ni teclear — se localizan por el texto de `Observaciones`, siguiendo el mismo
  método que usa `PRUEBA-005` `P-13` para el mismo problema.
- **Precondición:** `P-40` y `P-41` ejecutadas.
- **Acción:**
  ```bash
  # ANTES de P-40/P-41 (tomar al empezar la Familia B):
  python scripts/instantanea.py guardar antes-prueba-004
  # ... se ejecutan P-40 y P-41 ...
  python scripts/instantanea.py guardar despues-prueba-004
  python scripts/instantanea.py comparar antes-prueba-004 despues-prueba-004
  ```
  Y, como segunda vía de lectura, abrir `Modelo_Datos_10082026` con el conector de Drive y localizar
  las cuatro filas —dos en `OT_OrdenesTrabajo`, dos en `MAN_Mantenimientos`— por `Observaciones`
  conteniendo `"PRUEBA-004"`, no por su clave.
- **Resultado esperado:**
  - Aparecen exactamente **dos filas nuevas** en `OT_OrdenesTrabajo` y **dos filas nuevas** en
    `MAN_Mantenimientos`, cada una con `Observaciones` conteniendo `"(positiva)"` o `"(negativa)"`
    según corresponda, y el `MAN` de cada una referenciando el `OTID` (`UNIQUEID()`) de su propia
    orden.
  - En la fila «positiva»: `CierreConExcepcion` vale `Y`/`TRUE` y `MotivoExcepcion` contiene el
    texto escrito en `P-40`.
  - En la fila «negativa»: `CierreConExcepcion` vale `N`/`FALSE` (o blanco) y `MotivoExcepcion` está
    vacío.
  - **Ninguna de las dos filas de `MAN_Mantenimientos` tiene la clave `Precision_GPS`.**
  - **Ninguna otra celda de ninguna otra tabla cambió** entre las dos instantáneas.
  - Las dos lecturas —API y Drive— coinciden en los cinco puntos anteriores.
- **Cómo se distingue el fallo:** cualquier celda fuera de las cuatro filas nuevas aparece en el
  `comparar`, o `CierreConExcepcion`/`MotivoExcepcion` no coinciden con lo que se vio en pantalla, o
  la clave `Precision_GPS` sigue apareciendo en la fila, o la lectura por Drive discrepa de la
  lectura por API.

**Cierre del fixture, en esta misma prueba:** confirmados los cinco puntos, borrar por API
(`scripts/appsheet_api.py`, `Action: Delete`) las dos filas de `MAN_Mantenimientos` y las dos de
`OT_OrdenesTrabajo`, usando las claves `UNIQUEID()` que devolvió esta misma instantánea — nunca un
literal. Confirmar con una tercera instantánea que las dos tablas vuelven a 0 filas, y borrar del
disco los archivos `BD/instantaneas/*prueba-004*.json` que esta tanda generó.

### Familia D — Configuración (AppSheet), cotejo a ojo

#### P-43 — El caso del tipo: `CierreConExcepcion` es `Yes/No`, no `Text` — INNEGOCIABLE

- **Qué comprueba:** exactamente el riesgo de §1.6. Si `CierreConExcepcion` quedó `Text` al inferir
  sobre la tabla vacía (`S-30`), `[CierreConExcepcion] = TRUE` seguiría comparando texto contra
  booleano y sería falso siempre.
- **Precondición:** `ORDEN-004` aplicada y la tabla cableada en el editor.
- **Acción:** en el editor, *Data > Columns > `MAN_Mantenimientos` > `CierreConExcepcion`*. Copiar
  literalmente el valor de **Type**.
- **Resultado esperado:** `Yes/No`.
- **Cómo se distingue el fallo:** el desplegable dice `Text`. Si sale `Text`, hay que retiparla a
  mano **antes** de dar por buena ninguna otra prueba de esta tanda.

#### P-44 — `RG-20` cubre tres columnas, no cuatro, y `CierreConExcepcion` no es una de ellas

- **Qué comprueba:** que `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong` y
  `FechaHoraEscaneo` quedan `Editable_If = FALSE`, y que `CierreConExcepcion` **no**.
- **Precondición:** `ORDEN-004` aplicada y `RG-20` cableada.
- **Acción:** en *Data > Columns* de `MAN_Mantenimientos`, copiar literalmente `Editable_If` de las
  cuatro columnas: `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo`,
  `CierreConExcepcion`.
- **Resultado esperado:** las tres primeras muestran `FALSE`; `CierreConExcepcion` muestra el campo
  **vacío**.
- **Cómo se distingue el fallo:** `CierreConExcepcion` también trae `FALSE` — la casilla quedaría
  gris, imposible de marcar, y `P-40` fallaría en el primer paso sin decir por qué.

#### P-45 — `Precision_GPS` no existe en ningún sitio del editor, y si sobrevive como columna huérfana está declarado y no es un fallo

- **Qué comprueba:** que la columna se retiró de verdad del uso, no solo de `REGLAS`. **A
  diferencia de la versión anterior de esta prueba**, `ESPEC-004` §2.8 ya adelantó que puede quedar
  como columna huérfana en `Data > Columns` si `MAN_Mantenimientos` se dio de alta antes de este
  cambio (Rama A) — eso no es, por sí solo, un fallo: lo es solo si sigue teniendo `Initial value` o
  aparece en el formulario.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:** en *Data > Columns* de `MAN_Mantenimientos`, buscar `Precision_GPS`. Si aparece,
  copiar su `Type` e `Initial value`. En el formulario de captura, confirmar que no hay ningún campo
  de precisión GPS visible al técnico.
- **Resultado esperado — Rama B de `ESPEC-004` §2.8** (se hizo *Delete and re-add* de la tabla):
  `Precision_GPS` ausente por completo de *Data > Columns*.
- **Resultado esperado — Rama A** (nunca se llegó a cablear, se dejó huérfana a propósito):
  `Precision_GPS` puede seguir en *Data > Columns*, pero **sin `Initial value`** (nunca se llegó a
  poner `USERLOCATIONACCURACY()`) y **ausente del formulario de captura** —AppSheet no muestra en el
  formulario una columna que ninguna vista referencia—.
- **Cómo se distingue el fallo:** `Precision_GPS` aparece en *Data > Columns* **con** `Initial value
  = USERLOCATIONACCURACY()` puesto (alguien la cableó pese al bloqueo), o aparece visible en el
  formulario que ve el técnico. Cualquiera de los dos es la trampa que `ESPEC-004` existía para
  cerrar, sobreviviendo a medias.

## 3. Pruebas bloqueadas

- **La vista del supervisor que cuenta cierres con excepción por técnico y por activo**
  (`Manuales/MANUAL_DE_USUARIO.md` §3.4). **BLOQUEADA POR `D-12`**: el modelo no declara vistas ni
  *slices*, y `ESPEC-004` §5 dice explícitamente que no la construye. `ESPEC-004` §6.4 adopta, hasta
  que `D-12` la entregue, un dueño y una cadencia provisionales para ese vacío — no cambia que esta
  prueba siga bloqueada.
- **`RG-13` y `RG-18`.** No se escribe prueba: `ESPEC-004` §5 las deja fuera de alcance a propósito.
- **`P-40`/`P-41` en su forma de app**, si la técnica de §1.5 no funciona contra este despliegue y no
  es viable ejecutar la prueba físicamente en el corredor en la fecha disponible, o si el
  discriminador de §1.5 (`P-09` de `PRUEBA-003` sobre este despliegue) no está disponible. Se
  declara en el acta del probador con la fecha en que se intentó.

**Consecuencia para `PRUEBA-003`, que no se resuelve en este documento:** sus pruebas `P-30` (mide
`RG-02`) y `P-31` («Lectura de vuelta de `RG-19`») quedan **superadas** en cuanto `ORDEN-004` se
aplica. `PRUEBA-003` necesita una nota que lo diga cuando esta tanda cierre — no se edita aquí.

## 4. Criterio de cierre

**Tienen que pasar todas menos las que queden `BLOQUEADA POR` en el momento de ejecutar**, y en
concreto:

- `P-34` a `P-39` (Familia A) son la condición de entrada: si alguna falla, `ORDEN-004` está
  incompleta y no tiene sentido seguir con las siguientes. **`P-37` en particular puede detener toda
  la tanda** si delata un problema de secuencia con `ESPEC-005` (§2.9 de `ESPEC-004`).
- `P-40`, `P-41`, `P-42` y `P-43` son innegociables. Sin las cuatro, no hay evidencia de que un
  técnico pueda, alguna vez, dejar constancia auditable de un cierre con GPS deficiente.
- `P-44` y `P-45` cierran los dos límites explícitos de `ESPEC-004` §3 y §2.8.
- Las pruebas de la sección 3 se cierran **declarando** su bloqueo, no ejecutándolas a la fuerza.
- El aviso nuevo de `G-05` sobre `UbicacionEscaneo_LatLong`/`RG-13` que aparece tras crear el fixture
  (`P-36`) **no cuenta como hallazgo ni bloquea el cierre**: está declarado y explicado por
  adelantado.

Si `P-43` sale `Text`, ninguna prueba de la Familia B ni C cuenta como pasada aunque el formulario se
haya comportado bien en pantalla: hay que retipar y repetir `P-40` a `P-42` desde cero.
