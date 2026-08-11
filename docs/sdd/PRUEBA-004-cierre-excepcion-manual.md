# PRUEBA-004 — Pruebas de aceptación de ESPEC-004

**Escrita antes de que ORDEN-004 exista.** Nada de lo que sigue se ejecutó contra el modelo, la
hoja ni el editor: los comandos marcados «automática» sí se corrieron —son de solo lectura o
comprueban archivos ya escritos— y sus salidas están citadas literalmente. Los que requieren la app
están descritos para cuando el ejecutor los corra, no ejecutados aquí.

| | |
|---|---|
| Cubre | [`ESPEC-004-cierre-excepcion-manual.md`](ESPEC-004-cierre-excepcion-manual.md): retirar `RG-02`/`Precision_GPS`, retirar `RG-19`, dejar `CierreConExcepcion` editable por el técnico, `RG-03` sin cambios |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (fileId `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Volcado hoy con `python scripts/sistema.py`, no copiado de una tanda anterior |
| Reglas que esta tanda tiene que probar y `PRUEBA-003` no cubre | `RG-02` retirada, `RG-19` retirada, el tipo real de `CierreConExcepcion` (`S-30`), el límite exacto de `RG-20` |
| Innegociables | `P-06`, `P-07`, `P-08`, `P-09` |

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
USR_Usuarios         11
EST_Activo           4
EOT_EstadosOrden     7
PAR_Parametros       3
```

Coincide con el volcado local (`openpyxl`, `BD/Modelo_Datos_PLANTILLA.xlsx`): `MAN_Mantenimientos`
y `OT_OrdenesTrabajo` en 1 fila de encabezado y cero de datos, el resto igual. Los dos modelos
coinciden; no hubo que resolver ninguna discrepancia. La instantánea se borró después de leerla,
siguiendo la higiene que ya sigue `ESPEC-004` §2.0.

**`OT_OrdenesTrabajo` en cero es un dato nuevo que `ESPEC-004` no cita** —solo habla de
`MAN_Mantenimientos`— y cambia el tamaño del fixture: no basta con una fila de `MAN`, hace falta
también su orden.

### 1.2 El fixture: entra en la prueba, no se aplaza

**Criterio:** entra. Aplazar la creación de la fila de `MAN_Mantenimientos` aplazaría la única
prueba capaz de demostrar que `RG-03` vuelve a disparar, que es el objeto entero de `ESPEC-004`.
Repetir aquí el patrón que este documento existe para cortar —declarar conforme un mecanismo que
nunca se ejercitó— sería exactamente el defecto original.

Y es un fixture **acotado, no abierto**: la cadena de arrastre se detiene en dos filas nuevas.

```
ACT_Activos          368 filas  →  se reutiliza una existente, no se crea ninguna
USR_Usuarios          11 filas  →  se reutilizan dos existentes (un técnico, un supervisor)
EST_Activo             4 filas  →  se reutiliza una existente
EOT_EstadosOrden       7 filas  →  se reutiliza una existente
OT_OrdenesTrabajo      0 filas  →  SE CREAN dos, marcadas TEST
MAN_Mantenimientos     0 filas  →  SE CREAN dos, una por cada OT
```

No arrastra activo, técnico ni estado nuevos porque esas cuatro tablas **ya tienen datos reales**
que sirven sin tocarlos. Si alguna de las cuatro estuviera también vacía, el criterio cambiaría: ahí
sí tocaría decidir aplazar, porque poblar un catálogo entero para probar una casilla ya no es un
fixture acotado.

**El borrado va en esta misma prueba, no en otra**, siguiendo la regla de higiene de
`SDD_PIPELINE_SGMC.md` §5.1: es el último paso de `P-08`.

### 1.3 El fixture elegido

| Campo | Valor | Por qué |
|---|---|---|
| `ActivoID` | `ACT-0001` (`SOS-001`, `TipoActivoID=TIP-001`, radio `0.05` km, `Ubicacion_LatLong = 5.099798, -73.718568`) | Existe, `Activo=TRUE`, coordenada poblada (ver 1.4) |
| Técnico | `USR-002` (Ivan Salcedo, `RolID=ROL-03` Técnico, `Activo=TRUE`) | Rol correcto, correo real: `ivan.salcedo@concesiondelsisga.com.co` |
| Supervisor | `USR-006` (Fernand Bolivar, `RolID=ROL-02` Supervisor) | Rol correcto |
| `EstadoOrdenID` | `En ejecucion` | Estado previo razonable a un cierre |
| `EstadoActivoID` (del `MAN`) | `EST-01` Operativo | Cierre normal, no una baja |
| `OTID` positiva | `TEST-OT-004A` | Prefijo `TEST` en la clave, numerada con este `PRUEBA` |
| `OTID` negativa | `TEST-OT-004B` | Ídem, fila separada para no mezclar los dos casos en una sola orden |

`MAN_Mantenimientos.MantenimientoID` **no se puede fijar a mano**: está en `CLAVE_GENERADA`
(`scripts/modelo_objetivo.py:887`), así que la aplicación le asigna `UNIQUEID()` en cuanto el
técnico abre el mantenimiento contra la orden. La marca `TEST` no puede ir en esa clave; va en
`Observaciones`: `"TEST — PRUEBA-004, borrar tras P-08"`. Es la adaptación de la regla de higiene a
una tabla de clave generada, y coincide con lo que ya declara el propio modelo sobre estas seis
tablas (`scripts/modelo_objetivo.py:849-859`).

### 1.4 `Ubicacion_LatLong` está poblada, al revés de lo que dicen dos documentos vigentes

Ya lo señaló `ESPEC-004` §2.6 sin corregirlo por no ser su objeto: `ACT_Activos.Ubicacion_LatLong`
está poblada en las 368 filas, y tanto `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (S-30, líneas 108, 133)
como `Manuales/MANUAL_DE_USUARIO.md` (recuadro «Antes de usar este manual», y §3.5) siguen diciendo
que está vacía. Lo confirmo de nuevo aquí porque **esta prueba depende del hecho, no de la cita**:

```
ACT-0001  Ubicacion_LatLong = 5.099798, -73.718568
```

Sigue sin ser el objeto de este documento corregir los dos archivos; queda registrado porque, si se
lee cualquiera de los dos antes que esto, llevan a construir el fixture como si no hubiera
coordenada que usar.

### 1.5 El obstáculo real: `RG-01` no se evita, se satisface por construcción

`Coordenadas_Cierre_LatLong` tiene `Initial value = HERE()` y quedará `Editable_If = FALSE`
(`RG-20`, que esta prueba no toca — ver `P-10`): en el formulario real, el pin **no es
arrastrable**, así que no hay manera de teclear la coordenada del activo a mano. Si quien ejecuta la
prueba no está físicamente en el corredor, `HERE()` capturará su ubicación real, casi con certeza a
más de 50 m del activo, y `RG-01` rechazará el cierre antes de llegar a `RG-03` — el defecto que
`ESPEC-004` §6 ya advertía.

**La solución no depende de estar cerca del activo, sino de que la distancia sea exactamente cero**,
que satisface `DISTANCE(...) <= [RadioGeofencingKm]` para cualquier radio positivo, y los 27 tipos
lo tienen (mínimo `0.05`, ninguno en `0`). Se logra sustituyendo lo que el navegador entrega a
`HERE()`:

```
Chrome DevTools → More tools → Sensors → Location → Custom
Latitud:  5.099798
Longitud: -73.718568
```

**Esto es una técnica de prueba de navegador, no un comportamiento de AppSheet**, y no está citada
en `BASE_CONOCIMIENTO_APPSHEET.md`: no hay verificación de que `HERE()` en este despliegue concreto
lea la geolocalización simulada del navegador en vez de la del dispositivo real o de un proxy de
red. **Se declara como técnica a probar, no como hecho confirmado.** Si no funciona, el método de
reserva es ejecutar la prueba físicamente junto a `ACT-0001` (`PK 00+100`), y si tampoco es viable
en la fecha de ejecución, `P-06` y `P-07` pasan a `BLOQUEADA POR` con esa causa — no se inventa una
tercera vía que toque `Coordenadas_Cierre_LatLong` o `RG-01`, porque eso es exactamente lo que
`ESPEC-004` §3 rechazó.

### 1.6 El tipo de `CierreConExcepcion` — el hallazgo que más pesa en esta tanda

`docs/ALCANCE_Y_SUPUESTOS_SGMC.md`, entrada `S-30` (líneas 244-274), ya lo dejó verificado el
2026-08-10: de las 10 columnas `Yes/No` en tablas sin una sola fila, **`CierreConExcepcion` es una
de ellas y salió `Text`** al inferir sobre una tabla vacía. Con la columna `Text`,
`[CierreConExcepcion] = TRUE` en `RG-03` compara texto contra el booleano `TRUE`, que **es siempre
falso y no da error** — es el modo de fallo por el que el encargo que originó `ESPEC-004` pidió
verificar esto por nombre.

`ESPEC-004` §3 y §4 no dicen nada sobre corregir este tipo: describen el estado objetivo de
`CierreConExcepcion` como «`Yes/No`, sin fórmula, editable», dando por hecho el tipo que `S-30` ya
encontró mal. **Si nadie lo retipa en `Data > Columns` al cablear esta tabla, `ESPEC-004` se aplica
entera y el defecto que vino a corregir —`RG-03` sin efecto— sigue exactamente igual**, ahora por el
tipo en vez de por el `Precision_GPS` en blanco. Es la razón de que `P-11` sea, junto con `P-06` y
`P-07`, innegociable.

## 2. Pruebas

### Familia A — Modelo (Python), automáticas

Corren contra `scripts/modelo_objetivo.py` y compañía. No requieren API ni editor.

#### P-01 — El modelo todavía tiene lo que `ESPEC-004` manda retirar (hoy falla; es la regla que precede al cambio)

- **Qué comprueba:** que `Precision_GPS`, `RG-02`, `RG-19` y la fórmula de `CierreConExcepcion`
  siguen vivos en `scripts/modelo_objetivo.py` **antes** de `ORDEN-004`, y que la comprobación es
  capaz de verlo — la regla que tiene que fallar primero, en el único punto del pipeline que admite
  TDD de verdad.
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
    - CierreConExcepcion todavia tiene formula: '[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")'
    - RG-02 sigue en REGLAS
    - RG-19 sigue en REGLAS
    - RG-20 todavia menciona Precision_GPS en su descripcion
    - Precision_GPS no esta en CAMPOS_RETIRADOS['MAN_Mantenimientos']
  ```
  Corrido hoy, 2026-08-10, y es exactamente esta salida — no una paráfrasis.
- **Resultado esperado — DESPUÉS de `ORDEN-004`:** `PASA: 0 fallos`.
- **Cómo se distingue el fallo:** si tras `ORDEN-004` el script sigue listando algo, `ESPEC-004` §4
  no se aplicó completa — por ejemplo, se borró la columna pero no la entrada de
  `CAMPOS_RETIRADOS`, o se quitó la fórmula pero `RG-19` sigue en la lista `REGLAS`. Cualquier línea
  de la lista es, por sí sola, un cambio a medias.

#### P-02 — `validar_modelo.py` sigue en 0 errores

- **Qué comprueba:** que retirar `Precision_GPS` no deja huérfana la entrada `"Precision del GPS"`
  de `COBERTURA` (`scripts/validar_modelo.py:249`) — el riesgo que `ESPEC-004` §2.7 y §6 marcan como
  dependencia dura de orden.
- **Precondición:** `ORDEN-004` aplicada, incluyendo el punto de §4 que dice quitar esa entrada de
  `COBERTURA`.
- **Acción:** `python scripts/validar_modelo.py`
- **Resultado esperado:** `ERRORES: ninguno` y `APTO PARA DESPLEGAR`, igual que hoy
  (verificado: `Tablas: 28 | Columnas: 211 | Referencias: 39 | Reglas: 21`, 3 avisos, ninguno sobre
  `Precision_GPS` ni `V-13`). Tras `ORDEN-004`: `Reglas: 19` (se van `RG-02` y `RG-19`) y
  `Columnas: 210` (se va `Precision_GPS`).
- **Cómo se distingue el fallo:** aparece `[V-13] El flujo 'Precision del GPS' necesita
  MAN_Mantenimientos.Precision_GPS, que no existe` — significa que se editó `modelo_objetivo.py`
  pero no `validar_modelo.py`, exactamente el escenario que `ESPEC-004` §6 declara como riesgo.

#### P-03 — `verificar_datos.py` (`G-05`) no seguiría citando un defecto ya cerrado como si siguiera abierto

- **Qué comprueba:** que el comentario de cabecera de `G-05` (`scripts/verificar_datos.py:213-214`,
  hoy: *"RG-19 compara Precision_GPS, que nadie puebla porque la función que la poblaría no existe
  en AppSheet"*) se actualiza o se sustituye por un ejemplo vigente, tal como pide `ESPEC-004` §4
  último punto.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:**
  ```bash
  grep -n "RG-19" scripts/verificar_datos.py
  python scripts/verificar_datos.py
  ```
- **Resultado esperado:** el `grep` no encuentra `RG-19` citada como ejemplo del defecto que `G-05`
  persigue (puede seguir apareciendo en un comentario que diga explícitamente «corregido con
  `ESPEC-004`», que no es el mismo caso). La ejecución sigue en `DATOS COHERENTES`, sin que `G-05`
  produzca ningún aviso nuevo achacable a este cambio.
- **Cómo se distingue el fallo:** el `grep` devuelve la línea original sin ninguna nota de que el
  caso se cerró — el ejemplo pasaría a describir, en presente, algo que ya no es cierto, que es
  precisamente el patrón que este proyecto ya pagó con `bd.md` y el Excel.

#### P-04 — `verificar_faseA.py` ya no cruza `Precision_GPS` contra una fórmula retirada

- **Qué comprueba:** que el bloque `F-12`/`F-13` (`scripts/verificar_faseA.py:307-387`), que asume
  que `RG-19` sigue siendo una `App formula` viva, se retira — como pide `ESPEC-004` §4.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:**
  ```bash
  grep -n "Precision_GPS\|RG-19" scripts/verificar_faseA.py
  python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
  ```
- **Resultado esperado:** el `grep` no devuelve nada del bloque `F-12` (puede seguir citando
  `RADIO_GEOFENCING_KM` bajo `F-13`, que no depende de `RG-19`). La ejecución de `verificar_faseA.py`
  llega a `FASE A CERRADA` sin ningún `F-12`.
- **Cómo se distingue el fallo:** el bloque sigue presente y compara `Precision_GPS` —columna que ya
  no existe— contra `CierreConExcepcion`: el script revienta con un `KeyError`/`IndexError` al no
  encontrar la columna en la hoja, o peor, calla porque `"Precision_GPS" in h` da `False` y el
  bloque entero se salta en silencio sin que nadie note que quedó código muerto.

#### P-05 — `generar_diccionario_bd.py` ya no atribuye `UMBRAL_GPS` a `RG-19`

- **Qué comprueba:** que `lectores["UMBRAL_GPS"]` (`scripts/generar_diccionario_bd.py:159`) deja de
  decir `"RG-19"`, como pide `ESPEC-004` §4.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:**
  ```bash
  grep -n 'lectores = ' -A 2 scripts/generar_diccionario_bd.py
  python scripts/generar_diccionario_bd.py
  grep -n "UMBRAL_GPS" docs/bd.md
  ```
- **Resultado esperado:** `lectores` ya no tiene la clave `"UMBRAL_GPS"` (queda sin lector, como ya
  le pasa a `RADIO_GEOFENCING_KM`), y `docs/bd.md` regenerado muestra `UMBRAL_GPS` con la columna
  «Quién lo lee» en `—`.
- **Cómo se distingue el fallo:** `docs/bd.md` sigue diciendo `RG-19` en esa fila — un documento
  **generado** afirmando que una regla retirada lee un parámetro, que es la misma clase de mentira
  que motivó reescribir `generar_diccionario_bd.py` en primer lugar.

### Familia B — Configuración (AppSheet), no automáticas: ejercicio de la app

**Cómo se lee de vuelta: NADIE, salvo quien la ejecuta.** No hay comando: `Required_If` y
`Editable_If` no viajan por la API (`scripts/lectura_de_vuelta.py`). Se cierran documentando lo que
se vio, literal.

**Precondición común a `P-06` y `P-07`:** `ORDEN-004` aplicada; `OTID`, `TecnicoID`,
`EstadoOrdenID` cableados en `OT_OrdenesTrabajo`; `OTID`, `TecnicoID`, `EstadoActivoID` cableados en
`MAN_Mantenimientos`; `RG-01` puesta; sesión iniciada con una cuenta cuyo correo coincide con una
fila de `USR_Usuarios` (`ivan.salcedo@concesiondelsisga.com.co` / `USR-002`), para que
`TecnicoID` de `MAN_Mantenimientos` resuelva por `LOOKUP(USEREMAIL()...)`; geolocalización del
navegador fijada en `5.099798, -73.718568` (§1.5).

#### P-06 — Positiva: el técnico marca la excepción y el sistema le exige el motivo — INNEGOCIABLE

- **Qué comprueba:** que `RG-03` (`Required_If = [CierreConExcepcion] = TRUE`) bloquea el guardado
  cuando la casilla está marcada y `MotivoExcepcion` sigue vacío, y que deja guardar en cuanto se
  escribe el motivo. Es la mitad que faltaba desde que `Precision_GPS` nunca llegó a poblarse.
- **Precondición:** la común de la Familia B, más una orden nueva `OTID = TEST-OT-004A` con
  `ActivoID = ACT-0001`, `TecnicoID = USR-002`, `SupervisorID = USR-006`, `Tipo = Correctivo`,
  `FechaProgramada` = hoy, `EstadoOrdenID = En ejecucion`.
- **Acción:** abrir `TEST-OT-004A` en el formulario del técnico, iniciar el mantenimiento,
  `EstadoActivoID = EST-01`, marcar `Cierre con excepción`, **intentar guardar sin escribir el
  motivo**, y luego escribir `"PRUEBA-004 — cobertura deficiente simulada"` en `Motivo de excepción`
  y guardar de nuevo. `Observaciones = "TEST — PRUEBA-004, borrar tras P-08"`.
- **Resultado esperado:** el primer intento **no guarda** y el formulario señala `MotivoExcepcion`
  como pendiente. El segundo intento guarda y la orden pasa a `En revision` o al estado que
  corresponda tras el cierre.
- **Cómo se distingue el fallo:** el primer intento guarda igual. Si eso pasa,
  `CierreConExcepcion` no está resolviendo a `TRUE` cuando el desplegable/casilla está marcada —
  el escenario exacto de `S-30` (`P-11` lo diagnostica) — o `RG-03` no se cableó.

#### P-07 — Negativa: el técnico NO marca la excepción y el sistema le deja guardar sin motivo

- **Qué comprueba:** que `Required_If` no se volvió una obligación constante. Sin esta prueba, un
  `Required_If` que pidiera el motivo **siempre** pasaría `P-06` sin que nadie lo notara — el defecto
  que `P-30` de `PRUEBA-003` ya identificó como el que casi siempre falta.
- **Precondición:** la común de la Familia B, más `OTID = TEST-OT-004B`, mismos datos que
  `TEST-OT-004A` salvo la clave.
- **Acción:** abrir `TEST-OT-004B`, `EstadoActivoID = EST-01`, **no** marcar `Cierre con excepción`,
  dejar `Motivo de excepción` en blanco, guardar. `Observaciones = "TEST — PRUEBA-004, borrar tras
  P-08"`.
- **Resultado esperado:** guarda sin que el formulario pida nada sobre `MotivoExcepcion`.
- **Cómo se distingue el fallo:** el formulario bloquea el guardado pidiendo el motivo aunque la
  casilla esté sin marcar. Sería el error contrario a `ESPEC-004`: convertiría el cierre normal, que
  es la inmensa mayoría de los casos, en imposible de guardar sin justificar algo que no ocurrió.

### Familia C — Datos (Sheets), automática

#### P-08 — Lectura de vuelta: qué quedó escrito en la hoja — INNEGOCIABLE

- **Qué comprueba:** que lo que la app dijo que guardó **llegó al Sheets**, con el valor correcto en
  las dos filas, y que no escribió en ninguna celda que no debía — la clase de comprobación que este
  proyecto exige después de `P-33`/`RG-16`: una `App formula` o un cierre de formulario pueden tocar
  más de lo que se ve en pantalla.
- **Precondición:** `P-06` y `P-07` ejecutadas.
- **Acción:**
  ```bash
  # ANTES de P-06/P-07 (tomar al empezar la Familia B):
  python scripts/instantanea.py guardar antes-prueba-004
  # ... se ejecutan P-06 y P-07 ...
  python scripts/instantanea.py guardar despues-prueba-004
  python scripts/instantanea.py comparar antes-prueba-004 despues-prueba-004
  ```
  Y, como segunda vía de lectura —independiente de la API de AppSheet, directa sobre el archivo—,
  abrir `Modelo_Datos_10082026` (`fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) con el
  conector de Drive y localizar las dos filas por `TEST-OT-004A` / `TEST-OT-004B` en las pestañas
  `MAN_Mantenimientos` y `OT_OrdenesTrabajo`.
- **Resultado esperado:**
  - Aparecen exactamente **dos filas nuevas** en `OT_OrdenesTrabajo` (`TEST-OT-004A`,
    `TEST-OT-004B`) y **dos filas nuevas** en `MAN_Mantenimientos`, cada una con su `OTID`
    correspondiente.
  - En la fila ligada a `TEST-OT-004A`: `CierreConExcepcion` vale `Y`/`TRUE` y `MotivoExcepcion`
    contiene el texto escrito en `P-06`.
  - En la fila ligada a `TEST-OT-004B`: `CierreConExcepcion` vale `N`/`FALSE` (o blanco) y
    `MotivoExcepcion` está vacío.
  - **Ninguna de las dos filas tiene la clave `Precision_GPS`** — la columna ya no existe, así que
    la API no puede devolverla bajo ningún nombre.
  - **Ninguna otra celda de ninguna otra tabla cambió** entre las dos instantáneas.
  - Las dos lecturas —API y Drive— coinciden en los cuatro puntos anteriores.
- **Cómo se distingue el fallo:** cualquier celda de las 953+4 filas fuera de las dos nuevas aparece
  en el `comparar`, o `CierreConExcepcion`/`MotivoExcepcion` en la hoja no coinciden con lo que se
  vio en pantalla al guardar (la app mostró éxito pero la hoja quedó con el valor viejo o vacío), o
  la clave `Precision_GPS` sigue apareciendo en la fila —la columna sobrevivió en la hoja aunque se
  retiró del modelo—, o la lectura por Drive discrepa de la lectura por API —indicio de que el
  Sheets tiene una fila que la app todavía no sincronizó, o viceversa.

**Cierre del fixture, en esta misma prueba:** una vez confirmados los cuatro puntos, borrar las dos
filas de `MAN_Mantenimientos` y las dos de `OT_OrdenesTrabajo` por API (`Action: Delete`, con
`scripts/appsheet_api.py`, sobre las claves `TEST-OT-004A`/`TEST-OT-004B` y las dos claves
`UNIQUEID()` que devolvió `P-08`). Es la excepción que el propio `appsheet_api.py` prevé al advertir
sobre `Delete`: el histórico que no se borra es el de mantenimientos reales, no el de un fixture
marcado `TEST` que esta misma prueba creó y tiene la obligación de retirar. Confirmar con una
tercera instantánea (`despues-de-borrar`) que las dos tablas vuelven a 0 filas.

### Familia D — Configuración (AppSheet), cotejo a ojo

**Cómo se lee de vuelta: NADIE, salvo quien la ejecuta.** El tipo de columna y `Editable_If` no
viajan por la API. Se copian del editor literalmente.

#### P-09 — El caso del tipo: `CierreConExcepcion` es `Yes/No`, no `Text` — INNEGOCIABLE

- **Qué comprueba:** exactamente el riesgo de §1.6. Si `CierreConExcepcion` quedó `Text` al inferir
  sobre la tabla vacía (`S-30`), `P-06` y `P-07` pueden parecer que pasan por una razón equivocada:
  un `Required_If` sobre una columna `Text` puede comportarse de forma inconsistente según cómo
  AppSheet dibuje el control, y aunque pareciera funcionar en el formulario, `[CierreConExcepcion] =
  TRUE` seguiría comparando texto contra booleano y sería falso siempre — el defecto de `S-30`
  reencarnado.
- **Precondición:** `ORDEN-004` aplicada y la tabla cableada en el editor.
- **Acción:** en el editor de AppSheet, *Data > Columns > `MAN_Mantenimientos` > `CierreConExcepcion`*.
  Copiar literalmente el valor del desplegable **Type**.
- **Resultado esperado:** `Yes/No`.
- **Cómo se distingue el fallo:** el desplegable dice `Text`. No hay comando que lo detecte solo;
  por eso esta prueba existe con este nombre y no como una línea suelta dentro de `P-06`. Si sale
  `Text`, hay que retiparla a mano en el editor **antes** de dar por buena ninguna otra prueba de
  esta tanda — es la corrección que `ESPEC-004` da por hecha sin decirlo.

#### P-10 — `RG-20` cubre tres columnas, no cuatro, y `CierreConExcepcion` no es una de ellas

- **Qué comprueba:** el límite exacto que `ESPEC-004` §3 pide, en el sentido correcto: que
  `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong` y `FechaHoraEscaneo` quedan
  `Editable_If = FALSE`, y que `CierreConExcepcion` **no** — porque si `RG-20` se aplicara «por
  seguridad» a las cuatro por costumbre (eran cuatro hasta ayer), el técnico no podría marcar la
  casilla nunca y `P-06` fallaría por una razón distinta a la que se está probando, confundiendo el
  diagnóstico.
- **Precondición:** `ORDEN-004` aplicada y `RG-20` cableada.
- **Acción:** en *Data > Columns* de `MAN_Mantenimientos`, abrir cada una de las cuatro columnas y
  copiar literalmente el contenido del campo `Editable_If`:
  `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo`, `CierreConExcepcion`.
- **Resultado esperado:** las tres primeras muestran `FALSE`; `CierreConExcepcion` muestra el campo
  **vacío** (sin expresión, editable por defecto).
- **Cómo se distingue el fallo:** `CierreConExcepcion` también trae `FALSE` — la casilla quedaría
  gris en el formulario, imposible de marcar, y `P-06` fallaría en el primer paso sin que el mensaje
  de error diga por qué; se leería como un fallo de `RG-03` cuando el defecto real está en `RG-20`.

#### P-11 — `Precision_GPS` no existe en ningún sitio del editor

- **Qué comprueba:** que la columna se retiró de verdad, no que dejó de citarse en `REGLAS`.
  Complementa la comprobación mecánica de `P-08` (que solo puede ver que la API no la devuelve)
  mirando el origen: si la columna sigue en la hoja o en la tabla de AppSheet aunque nadie la
  referencie, sigue siendo una trampa para la próxima persona que la encuentre y la use.
- **Precondición:** `ORDEN-004` aplicada.
- **Acción:** en *Data > Columns* de `MAN_Mantenimientos`, confirmar que no aparece ninguna fila
  `Precision_GPS`. En el formulario de captura, confirmar que no hay ningún campo de precisión GPS
  visible al técnico.
- **Resultado esperado:** ausente en las dos superficies.
- **Cómo se distingue el fallo:** la columna sigue en *Data > Columns* marcada `Show = FALSE` o
  similar — retirada de la vista pero no de la tabla, que deja viva la `Initial value` rota y el
  riesgo de que alguien la reactive sin saber que nunca funcionó.

## 3. Pruebas bloqueadas

- **La vista del supervisor que cuenta cierres con excepción por técnico y por activo**
  (`Manuales/MANUAL_DE_USUARIO.md` §3.4: *"El supervisor ve cuántos cierres con excepción tiene cada
  técnico y cada activo"*). **BLOQUEADA POR `D-12`**: el modelo no declara vistas ni *slices*, y
  `ESPEC-004` §5 dice explícitamente que no la construye. No hay nada que ejercitar todavía.
- **`RG-13`** (contrastar dónde se escaneó con dónde se cerró). No se escribe prueba: `ESPEC-004` §5
  la deja fuera de alcance a propósito, sin propiedad real de AppSheet que la aloje, y su entrada
  (`UbicacionEscaneo_LatLong`) no se puebla mientras el QR siga fuera de alcance
  (`SDD_PIPELINE_SGMC.md` §8). Escribir una prueba aquí validaría un mecanismo que nadie va a cablear
  con este cambio.
- **`P-06`/`P-07` en su forma de app**, si la técnica de §1.5 (geolocalización simulada por
  DevTools) no funciona contra este despliegue y no es viable ejecutar la prueba físicamente en el
  corredor en la fecha disponible. **BLOQUEADA POR** falta de un método verificado para satisfacer
  `RG-01` sin tocar `Coordenadas_Cierre_LatLong`. Si esto ocurre, se declara en el acta del probador
  con la fecha en que se intentó, no se calla ni se sustituye por una prueba distinta que no pruebe
  lo mismo.

**Consecuencia para `PRUEBA-003`, que no se resuelve en este documento:** sus pruebas `P-30` (mide
`RG-02` y, de paso, plantea la forma correcta de probar `RG-03`) y `P-31` («Lectura de vuelta de
`RG-19`») quedan **superadas** en cuanto `ORDEN-004` se aplica: las dos reglas que miden ya no van a
existir. `PRUEBA-003` necesita una nota que lo diga cuando esta tanda cierre — no se edita aquí
porque no es el objeto de este `ESPEC`, pero dejarlo sin decir repetiría el patrón de `bd.md` y el
Excel: dos documentos describiendo sistemas distintos y nadie lo nota.

## 4. Criterio de cierre

**Tienen que pasar todas menos las que queden `BLOQUEADA POR` en el momento de ejecutar**, y en
concreto:

- `P-01` a `P-05` (Familia A) son la condición de entrada: si alguna falla, `ORDEN-004` está
  incompleta y no tiene sentido seguir con las siguientes.
- `P-06`, `P-07`, `P-08` y `P-09` son innegociables. Sin las cuatro, no hay evidencia de que un
  técnico pueda, alguna vez, dejar constancia auditable de un cierre con GPS deficiente — la
  pregunta que abre `ESPEC-004` §1 sigue sin respuesta aunque el modelo esté limpio.
- `P-10` y `P-11` cierran los dos límites explícitos de `ESPEC-004` §3: que `RG-20` no se llevó por
  delante `CierreConExcepcion`, y que `Precision_GPS` no sobrevive a medias.
- Las pruebas de la sección 3 se cierran **declarando** su bloqueo, no ejecutándolas a la fuerza.

Si `P-09` sale `Text`, ninguna prueba de la Familia B ni C cuenta como pasada aunque el formulario
se haya comportado bien en pantalla: hay que retipar y repetir `P-06` a `P-08` desde cero, porque el
comportamiento visto pudo deberse al tipo equivocado y no a `RG-03`.
