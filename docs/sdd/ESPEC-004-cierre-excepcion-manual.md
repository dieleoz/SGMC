# ESPEC-004 — Cierre con excepción por GPS: de fórmula inexistente a marca del técnico

**Tercera versión. Reescrita el 2026-08-11 aplicando la vara nueva de `CLAUDE.md` §7.18.** No toca
`scripts/modelo_objetivo.py`, el Sheets de producción ni el editor de AppSheet.

## 0. Qué cambió desde la versión anterior, y una limitación que hay que declarar antes de todo

**La versión anterior (`81118aa`, 798 líneas) recibió una segunda pasada del arquitecto con quince
hallazgos** (`ESTADO.md` §0, `CLAUDE.md` §7.4). **Su texto literal no quedó guardado como artefacto
en el repositorio**: solo sobreviven su número y su tema general, en prosa, en `ESTADO.md` y
`CLAUDE.md`. No hay un `docs/sdd/*.md` ni un `git log` con el detalle punto por punto — se
comprobó buscando **el dictamen** —no la cadena `ESPEC-004`, que sí devuelve commits y de la que
`git show 81118aa:...` recupera las 798 líneas de la versión anterior íntegras— en todo el árbol y en
el historial. El único `DICTAMEN_*.md` del repositorio no menciona `ESPEC-004`. Lo que no existe es el
**texto de los quince hallazgos**; el documento que juzgaron sí está.

Frente a eso, esta reescritura no simula reclasificar un texto que no existe. Hace el trabajo
equivalente: **vuelve a verificar cada afirmación de la versión anterior contra el archivo, hoy**, y
aplica la vara de `CLAUDE.md` §7.18 — *un hallazgo bloquea solo si nombra qué se rompe en
producción* — a lo que encuentra. El resultado (qué sobrevive, qué se degrada a nota o a riesgo
aceptado, y por qué) está en el **§8**, al final, porque solo tiene sentido después de leer el
estado real que el resto del documento levanta.

**Lo que se movió bajo los pies del documento, en concreto:**

- **`ESPEC-005` ya no es un supuesto: está aplicada y cerrada.** La versión anterior abría con
  *"Supuesto que gobierna todo este documento: `ESPEC-005` va primero"*. Hoy `OTID` y `PlanID` son
  `UNIQUEID()`, con `Key` marcada, cotejado en el editor con recarga en duro y transcripción literal
  (`docs/sdd/ACTA-005-pruebas.md`, `P-09`). El fixture de `PRUEBA-004` deja de construirse sobre una
  condicional (§2.2).
- **`ESPEC-006` cerró el 2026-08-11** con cuatro riesgos aceptados y nombrados (§8 de ese
  documento). Es el molde que sigue esta reescritura para su propio §8.
- **`docs/sdd/ACTA-006-cotejo-y-supuesto.md` midió dos cosas**, en vez de declararlas: las nueve
  columnas de `OT_OrdenesTrabajo` están cotejadas contra el editor, y **una columna virtual `App
  formula` con `Show?` activo sí se lee por la API** — medido sobre `PAR_Parametros`, no razonado.
  Ninguna de las dos toca `MAN_Mantenimientos` de forma directa, pero la segunda cambia lo que se
  puede dar por sabido en el resto del pipeline: **una virtual leída por API deja de ser un límite
  documental fijo**, hay que decir explícitamente que no se probó contra `CierreConExcepcion` (§2.5).
- **`scripts/inferencia.py` no es evidencia de estado.** Clasifica columnas por quién consigue el
  tipo, no si alguien ya pasó por el editor — la API v2 devuelve filas, no esquema. Fue el hallazgo 2
  del dictamen de `ESPEC-006`; esta versión no lo repite en ningún punto donde la anterior sí lo
  hacía (§2.5, §2.7).

## 1. Qué se quiere y por qué

`RG-02` inicializa `MAN_Mantenimientos.Precision_GPS` con `USERLOCATIONACCURACY()`. Esa función **no
existe en AppSheet**: lo reportó el editor al intentar escribirla y lo confirma la página oficial de
captura de GPS (§2.1). `RG-19` compara `Precision_GPS` contra `PAR_Parametros.UMBRAL_GPS` para
calcular `CierreConExcepcion`; como `Precision_GPS` nunca se puebla, esa comparación es siempre
`número > blanco` (`FALSE`). `RG-03` exige `MotivoExcepcion` solo si `CierreConExcepcion = TRUE`, y
como eso nunca ocurre, **`MotivoExcepcion` no se le pide nunca a nadie**.

La decisión que este documento permite tomar: **¿puede un técnico, alguna vez, dejar constancia
auditable de que cerró con el GPS deficiente?** Hoy la respuesta de diseño es no.

**El riesgo que este documento en realidad gestiona no es que alguien marque la excepción sin
deberlo** — no puede falsear dónde estuvo: `RG-01` sigue comprobando la distancia, y `HERE()` sobre
`Coordenadas_Cierre_LatLong` sigue sin ser editable (`RG-20`). **Es el técnico que cierra con GPS
malo y NO marca la casilla.** Ese cierre queda indistinguible de uno con buena señal, con o sin este
documento, porque la casilla es una autodeclaración, no una medición. Sin `ESPEC-004` la casilla ni
siquiera se puede usar; con ella, se puede usar, pero usarla sigue siendo voluntario. §2.14 nombra
esa exposición con precisión y §6 dice quién la vigila mientras no exista un reporte que la
contraste.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

```
$ python scripts/sistema.py
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026 (fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Verificado hoy contra el volcado local (`openpyxl`, `data_only=True`) y contra
`scripts/modelo_objetivo.py`. No se leyó producción de nuevo por API en esta reescritura para las
tablas de catálogo (coinciden con el volcado, que es el mismo archivo mientras nadie edite el Sheets
a mano); para las ocho tablas de movimiento, que el volcado vacía por diseño (`CLAUDE.md` §7.15), se
cita `docs/sdd/ACTA-006-cotejo-y-supuesto.md` §3, del 2026-08-11, que sí las leyó por API.

### 2.1 `USERLOCATIONACCURACY()` no existe

> «There are four ways to capture the GPS location in a form: [1] `HERE()` como App Formula ...
> [2]... como Initial Value ... [3] captura manual, con un ícono que muestra la precisión en metros
> ... [4] escribirlo a mano. **The manual capture mode of the LatLong input provides the highest
> available accuracy and is recommended over use of the `HERE()` function in cases where high
> accuracy is especially important.**»

— [Capture GPS location](https://support.google.com/appsheet/answer/10106789), AppSheet Help,
consultado el 2026-08-10. Ninguna de las cuatro formas guarda la precisión mostrada en pantalla en
una columna. **Nota de higiene documental, degradada a nota en §8:** esta cita vive solo en este
documento; `docs/BASE_CONOCIMIENTO_APPSHEET.md` no la indexa —comprobado, `grep -c
"10106789\|USERLOCATIONACCURACY" docs/BASE_CONOCIMIENTO_APPSHEET.md` da `0`—. No cambia si la
función existe o no; sí significa que quien busque esta verificación en el sitio donde el proyecto
dice que vive el conocimiento de plataforma no la va a encontrar.

**Este documento mantiene `HERE()` con `Editable_If = FALSE`** (§3, "Sobre la mejora rechazada"): la
captura manual gana precisión a cambio de volver arrastrable el pin que sostiene el geofencing
(`RG-01`), y `RG-20` existe para impedir eso.

### 2.2 `ESPEC-005` ya está aplicada — deja de ser una condición para pasar a ser un hecho

```
$ python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(len(M.CLAVE_LEGIBLE),len(M.CLAVE_GENERADA),len(M.REGLAS))"
20 8 23
```

`OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` están en `CLAVE_GENERADA`, con `RG-35`/`RG-36`
(columnas virtuales `Etiqueta`) declaradas. En el editor, cotejado con recarga en duro:

```
OTID / PlanID:  Initial value = UNIQUEID()  ·  Key: marcado  ·  App formula: vacío
```

— `docs/sdd/ACTA-005-pruebas.md`, `P-09`, transcripción literal del 2026-08-11. El fixture de
`PRUEBA-004` (Familia C) se construye sobre este hecho, no sobre una condicional: **ninguna clave se
teclea**, se lee de vuelta después de crear cada fila (ya así en la versión anterior, §1.3 de
`PRUEBA-004`; lo que cambia aquí es que deja de estar detrás de un supuesto).

**Lo que esto resuelve, y ya no hace falta explicar en dos ramas:** la versión anterior dedicaba
media página (su §2.9, punto 3) a un riesgo de secuencia — que `verificar_faseA.py` certificara en
falso `OT_OrdenesTrabajo` como clave legible si se corría contra un `modelo_objetivo.py` que aún no
reflejara `ORDEN-005`. Verificado hoy que el riesgo ya no aplica, porque no hay dos versiones del
archivo en juego:

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx" | grep F-11
(sin salida — ningún F-11 sobre OT_OrdenesTrabajo ni PLA_PlanMantenimiento)
```

### 2.3 `RG-19` sigue declarada una sola vez, con guarda — `V-18` en 0 errores

```
$ python scripts/validar_modelo.py
Tablas: 28 | Columnas: 211 | Referencias: 39 | Reglas: 23
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14]
APTO PARA DESPLEGAR
```

Sin ningún `V-18` en la lista: la columna y `REGLAS` coinciden en la expresión
`OR(ISBLANK(LOOKUP("UMBRAL_GPS", ...)), [Precision_GPS] > LOOKUP("UMBRAL_GPS", ...))`. El `ISBLANK`
hace que, si alguien borra la fila `UMBRAL_GPS` de `PAR_Parametros`, la excepción salga `TRUE` en
todos los cierres en vez de en ninguno — un riesgo real hoy, pero **queda sin objeto en cuanto §3
retire `RG-19` por completo**: no se declara como acción de este documento, se declara para que
quede escrito por qué no hace falta declararla.

### 2.4 `MAN_Mantenimientos` y `OT_OrdenesTrabajo` siguen en cero

```
$ python -c "import openpyxl;wb=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',data_only=True,read_only=True); [print(t, len([r for r in wb[t].iter_rows(min_row=2,values_only=True) if r[0]])) for t in ('MAN_Mantenimientos','OT_OrdenesTrabajo')]"
MAN_Mantenimientos 0
OT_OrdenesTrabajo 0
```

Coincide con `docs/sdd/ACTA-006-cotejo-y-supuesto.md` §3, que sí leyó producción por API el
2026-08-11: *"Las ocho tablas de movimiento siguen en cero. La ventana barata sigue abierta."* No
hay ninguna fila histórica que migrar ni que se vea afectada por retirar una columna.

### 2.5 `PAR_Parametros.UMBRAL_GPS` sin cambios — y el hallazgo de `ACTA-006` no lo alcanza

```
$ python -c "..."
{'ParametroID': 'UMBRAL_GPS', 'Nombre': 'Umbral de GPS deficiente', 'Valor': 40, 'Unidad': 'm',
 'Descripcion': 'Error del satelite...', 'Activo': 'TRUE'}
```

`ACTA-006` §2 midió que una columna virtual `App formula` con `Show?` activo **sí** se lee por la
API, sobre `PAR_Parametros` — no sobre `MAN_Mantenimientos` ni sobre `CierreConExcepcion`. No se
extiende aquí ese resultado a este documento: `CierreConExcepcion` no es una columna virtual
—guardaba una `App formula` que este documento retira, no la conserva—, así que el hallazgo de
`ACTA-006` es relevante para el proyecto en general (informa qué se puede medir barato) pero no
cambia ningún hecho verificado sobre `RG-02`/`RG-03`/`RG-19`.

### 2.6 `RG-13` y `RG-18`, fuera de alcance — sin cambios

`RG-13` (`Verificacion de evidencia`) no tiene mecanismo de AppSheet detrás y su entrada,
`UbicacionEscaneo_LatLong`, solo se llena con `OrigenApertura = QR`, fuera de alcance desde
2026-08-07. `RG-18` (`Doctrina de reportes`) es una prohibición sobre reportes que no existen
(`D-12`). Ninguna de las dos se resuelve aquí (§5).

### 2.7 El hallazgo que más pesa: `CierreConExcepcion` puede seguir `Text`, y sigue sin comprobarse

```
$ grep -n "S-30" -A 25 docs/ALCANCE_Y_SUPUESTOS_SGMC.md | sed -n '1,25p'
```

`S-30` (2026-08-10, `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`): de 38 columnas `Yes/No` del modelo, **10
están en tablas sin una sola fila** y no se pudieron confirmar por contenido. `CierreConExcepcion` es
una de ellas y **salió `Text`** al inferir sobre la tabla vacía. Con `Text`,
`[CierreConExcepcion] = TRUE` compara texto contra el booleano `TRUE` — siempre falso, sin error.

**Esto es exactamente el defecto que este documento existe para corregir, sobreviviendo por otra
vía.** Si nadie retipa la columna en `Data > Columns` al cablear `MAN_Mantenimientos`, `ESPEC-004` se
aplica entera —`Precision_GPS` retirada, `RG-02`/`RG-19` fuera, `RG-03` disponible— y `RG-03` sigue
sin disparar nunca, ahora por el tipo en vez de por el dato en blanco. **Un técnico marcará la
casilla, y el formulario guardará sin pedirle el motivo.** Nombra la rotura en producción con
precisión: es bloqueante bajo la vara de §7.18, y se mantiene como tal (era `P-43`, innegociable, en
la versión anterior de `PRUEBA-004`; sigue siéndolo).

**No se puede comprobar desde este documento.** El tipo vive en el editor de AppSheet y la API v2
devuelve filas, no esquema — no hay comando. **Es la comprobación de cinco minutos que falta, y es la
única de todo este documento que un agente sin acceso al editor no puede cerrar**: abrir `Data >
Columns` de `MAN_Mantenimientos`, columna `CierreConExcepcion`, leer `Type`. Si dice `Yes/No`, este
riesgo se cierra sin tocar nada más; si dice `Text`, hay que retiparla antes de dar por buena
cualquier prueba de esta tanda. Se declara como supuesto refutable en §7, no como hecho.

### 2.8 `Precision_GPS` salió `LatLong` en la inferencia — y no importa, porque se retira

```
$ grep -n "Precision_GPS" docs/TIPOS_ESPERADOS.md
63:| MAN_Mantenimientos | Precision_GPS | Number | RG-02, RG-19 | ... su nombre dispara la
    inferencia a LatLong, y no lo es
```

`docs/TIPOS_ESPERADOS.md` documenta que `Precision_GPS` es candidata a tiparse `LatLong` en el editor
por llevar `GPS` en el nombre, cuando el dato son metros (`Number`). **Esta especificación no depende
de ese tipo**: §3 y §4 retiran la columna por completo, así que sea cual sea el tipo que AppSheet le
haya asignado hoy en el editor —si es que llegó a cablearse—, deja de tener consecuencia en cuanto
`ORDEN-004` se aplique. Se deja escrito explícitamente para que nadie tenga que perseguir esta duda
por su cuenta: **el riesgo de `TIPOS_ESPERADOS.md` sobre `Precision_GPS` es real como hecho histórico
y queda sin objeto como riesgo de este documento.**

### 2.9 Once scripts tocan este cambio, no seis — recontado hoy, y por dos nombres distintos

```
$ grep -rln "Precision_GPS" scripts/*.py
generar_guia_funcional.py · generar_manual_despliegue.py · generar_prompt_cableado.py ·
generar_prompt_expresiones.py · generar_tipos_esperados.py · inferencia.py · modelo_objetivo.py ·
validar_modelo.py · verificar_datos.py · verificar_faseA.py
```

Nueve, más `modelo_objetivo.py` que se edita directo (§4). **Y una búsqueda por un solo término no
alcanza**: `generar_diccionario_bd.py` no aparece en ese `grep` porque nombra el mecanismo por la
*regla* (`"RG-19"`, dentro de `lectores["UMBRAL_GPS"]`), no por la *columna* — el mismo modo de
fallo que el propio `generar_prompt_cableado.py` ya documenta en su código (fila de abajo). **Doce
scripts en total** (los nueve del `grep`, más `generar_diccionario_bd.py`, más `modelo_objetivo.py`
editado directo), no los seis que contó la versión anterior.

| Archivo | Acción |
|---|---|
| `generar_prompt_expresiones.py:335,340-341` | **Editar.** Sección "Dos que hoy NO se pueden poner": le dice al ejecutor que configure `Precision_GPS` sin `Initial value` — el peor caso, instruye a cablear algo que este documento retira |
| `generar_guia_funcional.py:383,395` | **Editar.** Cuenta "cuatro columnas no editables" (pasan a tres) y cita la `App formula` completa de `RG-19` |
| `generar_manual_despliegue.py:841,858` | **Editar.** Mismo tratamiento |
| `generar_diccionario_bd.py:159` (`lectores["UMBRAL_GPS"] = "RG-19"`) | **Editar.** `docs/bd.md` seguiría atribuyendo un lector inexistente |
| `validar_modelo.py:323` (`COBERTURA["Precision del GPS"]`) | **Editar.** Sin editar, `V-13` falla tras retirar la columna |
| `verificar_faseA.py:307-386` (bloque `F-12`/`F-13`) | **Editar.** Cruza `Precision_GPS` contra `CierreConExcepcion` asumiendo `RG-19` viva |
| `generar_encargo_ventana.py:141` | **Editar — el que faltaba.** Emite con texto **fijo** la fila `« RG-02, RG-19, RG-03 → ESPEC-004 está bloqueada »` en `docs/ENCARGO_VENTANA.md` (línea 158). Un `grep Precision_GPS` no lo encuentra: cita las **reglas**. Tras `ORDEN-004` esa fila debe nombrar solo `RG-03` y decir que **entra**, no que está bloqueada — si no, el encargo del editor seguirá diciendo a quien lo lea que no toque justo lo que este documento acaba de desbloquear |
| `verificar_datos.py:218` (comentario de cabecera de `G-05`) | **Editar.** Cita `RG-19` como ejemplo vigente del defecto que `G-05` persigue; sustituir por uno abierto (`RG-06`/`GeneraAlerta` ya sirve) |
| `generar_tipos_esperados.py` | **No editar.** Cita el hecho histórico ("`Precision_GPS` salió `LatLong` el 2026-08-10 estando su tabla vacía"), deriva de `MODELO` dinámicamente, desaparece sola |
| `inferencia.py` (`GATILLOS_NOMBRE`) | **No editar.** Mismo hecho histórico, sostiene una regla general (`gps` → `LatLong`) útil para columnas futuras |
| `generar_prompt_cableado.py:362-368` | **No editar — hallazgo nuevo.** Nombra `RG-19` buscándola en `REGLAS` en tiempo de ejecución (`next(r for r in REGLAS if r["id"]=="RG-19")`), no con texto fijo: el propio comentario del archivo ya explica por qué —un barrido por `grep Precision_GPS` no la habría encontrado, porque cita la *regla*, no la *columna*—. Retirada `RG-19`, este bloque deja de emitirse solo |

### 2.10 Retirar `Precision_GPS` del editor: procedimiento, no debate

`docs/BASE_CONOCIMIENTO_APPSHEET.md` §11: *Regenerate* funde con lo existente y no borra columnas
reales una por una; la salida oficial es *"Delete and re-add the table"*. Cuál de las dos ramas
aplica se decide mirando el editor en el momento de ejecutar, no aquí:

| Rama | Cuándo | Qué hacer |
|---|---|---|
| **A** — `MAN_Mantenimientos` no llegó a su Paso 6 de cableado (bloqueada precisamente en `RG-02`/`RG-19`/`RG-03`, que es lo que dice `ESTADO.md` hoy) | Más probable | No hace falta borrar nada: `Precision_GPS` queda huérfana sin `Initial value` y sin uso. Es ruido visual, no una regla activa |
| **B** — la tabla ya avanzó más allá (tipos, referencias, `Editable_If`, `Label` puestos, solo faltaba este bloque) | Si alguien ya cableó el resto mientras esperaba `ESPEC-004` | `Delete` y volver a dar de alta la tabla completa. **Se lleva por delante todo lo demás cableado en ella**: copiar a mano el estado de cada columna antes de borrar (no hay comando de lectura de vuelta), repetir el Paso 1 a 5 de `docs/PROMPT_CABLEADO.md` para esa tabla, comparar contra la copia al terminar |

### 2.11 El fixture de `PRUEBA-004` despierta `G-04`/`G-05` — esperado, no regresión

Con las dos filas del fixture insertadas (`PRUEBA-004`, Familia C), `G-04` deja de avisar sobre
`MAN_Mantenimientos`/`OT_OrdenesTrabajo` (deja de estar vacía) sin que eso confirme ningún tipo — hay
que seguir cotejando `Data > Columns` a mano. Y `G-05` emite un aviso nuevo y legítimo sobre
`UbicacionEscaneo_LatLong`/`RG-13` (vacía porque `OrigenApertura = Lista`, no un defecto de este
documento). Los dos efectos están verificados por simulación en la versión anterior y siguen válidos
sin cambios en esta reescritura; el detalle completo queda en `PRUEBA-004` §1 y no se repite aquí.

### 2.12 El discriminador de `RG-01` sigue sin verificar, y su precondición sigue sin ejecutarse

No hay página oficial que confirme si AppSheet evalúa un `Valid_If` sobre una columna con
`Editable_If = FALSE`. Si no lo evalúa, cualquier cierre se guardaría sin comprobar distancia, y las
pruebas de esta tanda (`P-40`/`P-41`) pasarían por una razón que nada tiene que ver con `RG-03`. El
discriminador ya existe en el proyecto: `PRUEBA-003`, `P-09` (cierre fuera de rango, innegociable) —
si un cierre lejano se acepta igual que uno cercano, el `Valid_If` no se está evaluando.

```
$ ls docs/sdd/ | grep -i "ACTA-003"
(sin resultado)
```

**`P-09` de `PRUEBA-003` no tiene acta de ejecución en el repositorio hoy.** No es un hallazgo de
diseño de este documento — es una dependencia de ejecución de `PRUEBA-004`, ya declarada como
precondición en su §1.5, y sigue sin cumplirse. Se deja como dependencia en §6, no como bloqueante de
esta especificación: `ESPEC-004` no necesita que `P-09` se haya corrido para estar bien diseñada;
`PRUEBA-004` sí lo necesita para que sus resultados cuenten como evidencia.

### 2.13 La pregunta contestable — adoptada, costo cero

`MotivoExcepcion` es libre y `CierreConExcepcion` hoy es una casilla sin más contexto que su nombre:
el manual, no la app, le dice al técnico en prosa que la marque si la precisión es mala. Se adopta
fijar la `Description` de `CierreConExcepcion` en el editor —propiedad estándar de AppSheet, texto
de ayuda bajo el campo— con la pregunta explícita: *"¿La app no alcanzó buena precisión al capturar
la posición de cierre? Marque si es así."* No cambia el esquema, no toca `RG-03`, y convierte una
instrucción muda en una pregunta declarada como juicio del técnico, no como medición. Se sigue
rechazando pedir el número transcrito (mismo patrón que costó caro con `CodigoQR`: un dato que nadie
puede contrastar después).

### 2.14 El riesgo residual, nombrado sin diluir

- El técnico que marca la excepción sin necesitarla no es el riesgo: no puede falsear su posición.
- **El técnico que cierra con GPS malo y no marca es el riesgo real.** Nada lo detecta —`RG-01` mide
  distancia, no calidad de señal—, y la marca depende enteramente de que decida ponerla.
- Quien edite directo en el Sheets se salta `RG-03` entero: `Required_If` es una regla de formulario,
  no existe en la hoja de cálculo.
- La garantía que este documento entrega vive **solo en la aplicación**, con sesión de técnico. Fuera
  de ese camino no hay ninguna constancia, auditable o no.

No es un defecto que introduzca este documento: es la superficie que queda una vez que hace su
trabajo. Antes, la pregunta ni se podía contestar; con `ESPEC-004`, se puede, pero contestarla sigue
siendo voluntaria y sin contraste automático (§6).

## 3. Qué cambia exactamente

| Tabla.Columna / elemento | Estado actual | Estado objetivo |
|---|---|---|
| `MAN_Mantenimientos.Precision_GPS` | `Number`, `Initial value = USERLOCATIONACCURACY()`, no editable | **Retirada del modelo** (§2.9, §2.10 para el editor) |
| `MAN_Mantenimientos.CierreConExcepcion` | `Yes/No` en el modelo, `App formula` (`RG-19`), no editable de hecho; **tipo real en el editor sin confirmar, puede ser `Text`** (§2.7) | `Yes/No`, sin fórmula, editable por el técnico. `Description` formulada como pregunta (§2.13) |
| `MAN_Mantenimientos.MotivoExcepcion` | `LongText`, `Required_If = [CierreConExcepcion] = TRUE` (`RG-03`) | Sin cambios. Lee el valor actual de la casilla |
| `RG-02` (Initial value) | Activa | **Retirada** |
| `RG-19` (App formula) | Activa, con guarda `ISBLANK` (§2.3) | **Retirada** |
| `RG-03` (Required_If) | Activa, sin efecto porque `CierreConExcepcion` nunca es `TRUE` | Sin cambios de expresión. Deja de estar inerte |
| `RG-20` (Editable_If FALSE) | Cubre 4 columnas | Cubre 3: `Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo` |
| `PAR_Parametros.UMBRAL_GPS` (fila) | Descripción cita `RG-19` como lector | **Se conserva.** Descripción reescrita: ninguna regla la lee; es la cifra de referencia para el juicio del técnico |
| `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (D-04), `docs/FUNCIONAL_SGMC.md` §6.4, `Manuales/MANUAL_DE_USUARIO.md` §3.4/§5.4 | Describen una comparación automática | Se ajustan a mano (§4) |

### Sobre la mejora rechazada: volver editable `Coordenadas_Cierre_LatLong`

Se evaluó y se rechaza. El control que muestra la precisión en pantalla durante la captura manual es
el mismo control editable que dibuja el pin arrastrable — hacerlo editable para ganar el dato en
pantalla reabre exactamente el agujero que `RG-20` existe para cerrar, en el control que sostiene
todo el geofencing. La ganancia (dato en vez de instrucción muda) se obtiene sin ese costo en §2.13.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`:

- **`MODELO["MAN_Mantenimientos"]["columnas"]`**: eliminar `Precision_GPS`. Quitar `formula=...` de
  `CierreConExcepcion`; queda `col("CierreConExcepcion", "Yes/No", nota="El técnico la marca cuando
  la app no le mostró buena precisión al capturar el cierre. Criterio de referencia:
  PAR_Parametros.UMBRAL_GPS. Antes se calculaba con RG-19 y USERLOCATIONACCURACY(), que no existe en
  AppSheet; ver ESPEC-004. Su Description en el editor formula la pregunta explícitamente, ver
  ESPEC-004 §2.13")`.
- **`CAMPOS_RETIRADOS["MAN_Mantenimientos"]`**: añadir `"Precision_GPS"` con el motivo de §2.9 y una
  nota de que retirarla del esquema de AppSheet exige el procedimiento de §2.10 si la tabla ya estaba
  dada de alta con la columna sin usar.
- **`REGLAS`**: eliminar los `dict` de `RG-02` y `RG-19`. En `RG-20`, quitar `Precision_GPS` de la
  lista de columnas que cubre y de su texto.
- **`PARAMETROS`**: no se retira `UMBRAL_GPS`. Se reescribe su descripción siguiendo el precedente de
  `RADIO_GEOFENCING_KM`: ninguna regla la lee desde `ESPEC-004`; queda como referencia para el manual
  y el juicio del técnico.
- **`DECISIONES`**: la entrada "Cierre sin GPS válido" no cambia de lado; su `por_qué` añade que el
  valor lo pone el técnico y no una fórmula, remite a este documento y nombra la exposición de §2.14.

**En el mismo cambio**, fuera de `modelo_objetivo.py`: los **ocho** archivos de la tabla de §2.9 que
dicen "Editar". Los tres que dicen "No editar" se regeneran solos.

**La `Description` de `CierreConExcepcion` no viaja por ningún generador, y por eso va en el encargo
del editor.** §2.13 adopta fijarla y `P-40` describe al técnico leyéndola en pantalla, pero el `nota=`
de una columna no lo consume nadie (`grep -rn 'get("nota")' scripts/*.py` solo devuelve
`generar_reconstruccion.py`, y sobre `REGLAS`), y ningún script emite `Description`. Sin esto era un
refinamiento adoptado que nadie iba a poner. Se escribe **en la misma pantalla y la misma sesión** que
la lectura del `Type` —coste cero— y `P-44` la coteja literal.

**Documentos generados que se re-emiten** con los comandos de siempre una vez editados esos siete
scripts: `docs/bd.md`, `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`,
`docs/PROMPT_CABLEADO.md`, `docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`, `docs/TIPOS_ESPERADOS.md`, `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md`
y **`docs/ENCARGO_VENTANA.md`**, que es el que lee quien entra al editor y hoy dice que esto está
bloqueado.

**A mano, no generados:** `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (D-04, líneas 108 y 133: ya no puede
decir "CERRADA en el mecanismo" sobre algo que nunca funcionó), `docs/FUNCIONAL_SGMC.md` §6.4 (quien
marca la excepción es el técnico, no una fórmula), `Manuales/MANUAL_DE_USUARIO.md` §3.4 y §5.4 (el
umbral es una referencia para el juicio del técnico, no una comparación automática).

## 5. Qué NO cubre esta especificación

- **No resuelve `RG-13` ni `RG-18`** (§2.6): sin propiedad real de AppSheet la primera, sin reportes
  que construir la segunda (`D-12`).
- **No resuelve `D-01`.** Las coordenadas de `ACT_Activos` son sintéticas, derivadas del `PK`. `RG-01`
  puede seguir rechazando cierres legítimos por esa razón, independiente de este documento.
- **No construye ningún reporte.** `D-12` sigue abierta.
- **No detecta el cierre con GPS malo que nadie marca** (§2.14). La única defensa es el juicio del
  técnico y la pregunta de §2.13, sin contraste automático. Un reporte que lo cruce es un frente
  aparte, con su propio `ESPEC`.
- **No impide escribir directo en el Sheets y saltarse `RG-03`.** Es un límite de arquitectura de
  AppSheet, no algo que este documento pueda cerrar.
- **No inventa una función de AppSheet que no existe.** Si la plataforma añade una forma de leer la
  precisión del GPS en una columna, reabrir esta decisión es legítimo y barato.
- **No retipa `CierreConExcepcion` desde aquí.** Lo hace quien tenga el editor delante (§2.7).

## 6. Riesgos y dependencias

- **La comprobación de tipo de §2.7 es la precondición dura de toda esta tanda.** Si
  `CierreConExcepcion` sale `Text` en el editor, `ESPEC-004` puede aplicarse entera y el defecto que
  vino a corregir sigue vivo. Se verifica en cinco minutos y en un solo lugar: `Data > Columns`.
- **Los siete scripts de §2.9 se editan en el mismo cambio que `modelo_objetivo.py`**, o el pipeline
  instruye a cablear algo retirado (`generar_prompt_expresiones.py` es el caso más caro).
- **`PRUEBA-003` `P-09` sigue sin acta de ejecución** (§2.12): mientras no se corra sobre este
  despliegue, `P-40`/`P-41` de `PRUEBA-004` no cuentan como evidencia de nada por sí solas.
- **Ruta de reversión.** El punto exacto donde deja de ser gratis: la primera fila de
  `MAN_Mantenimientos` donde un técnico guardó `CierreConExcepcion` con intención. Antes de eso
  (hoy: 0 filas, §2.4), revertir cuesta deshacer §4 y, si se llegó a la Rama B de §2.10, repetir el
  cableado — caro, sin pérdida de dato real. **Después de ese punto, revertir es destructivo**: una
  `App formula` materializa su valor al guardar (documentado y probado con `RG-16`/`P-33` de
  `PRUEBA-003`), así que reponer la fórmula de `RG-19` sobre una fila ya guardada por un técnico
  recalcularía `CierreConExcepcion` contra `Precision_GPS` en blanco y **borraría en silencio la
  marca que el técnico dejó a propósito**. Si hay que revertir después de ese punto: exportar antes
  todas las filas con `CierreConExcepcion` o `MotivoExcepcion` no vacíos, y aceptarlas como histórico
  que no se vuelve a guardar desde el formulario.
- **El riesgo residual de §2.14 necesita dueño y cadencia, y no lo tenía.** Se adopta en §7: el
  supervisor revisa `Observaciones`/`MotivoExcepcion` al aprobar cada cierre, uno por uno, hasta que
  `D-12` entregue una vista agregada.
- **Sin datos que migrar** (§2.4). **Riesgo de sincronización manual aceptado en `UMBRAL_GPS`**, igual
  que el precedente de `RADIO_GEOFENCING_KM`.

## 7. Supuestos adoptados

- **Se adopta retirar `RG-02`/`Precision_GPS`**, convertir `CierreConExcepcion` en casilla editable
  por el técnico, y dejar `RG-03` sin cambios de expresión. Es la única alternativa evaluada que no
  exige algo que AppSheet no ofrece hoy.
- **Se adopta la pregunta contestable de §2.13** como refinamiento de costo cero.
- **Se adopta rechazar la mejora de volver editable `Coordenadas_Cierre_LatLong`** (§3).
- **Se adopta conservar `PAR_Parametros.UMBRAL_GPS`** sin lector, precedente de `RADIO_GEOFENCING_KM`.
- **Se adopta que `RG-13` y `RG-18` quedan fuera de alcance** (§2.6, §5).
- **No se estima aquí qué rama es la más probable.** La estimación vive en §2.10 y en un solo sitio:
  este documento llegó a decir A en §2.10 y B en §7, que son contrarias, y B es la destructiva. Lo
  decide **la lectura 4 del encargo de editor** (`Precision_GPS`: si existe, su `Type` e `Initial
  value`), no una probabilidad escrita de antemano
  para `MAN_Mantenimientos`, sin que eso decida cuál aplica realmente: se confirma mirando el editor.
- **Se adopta un dueño y una cadencia provisionales para §2.14**: el supervisor, por cierre
  individual, hasta que `D-12` entregue una vista agregada.
- **Supuesto refutable, y es el que más pesa: `CierreConExcepcion` es `Yes/No` en el editor de
  AppSheet.** Qué lo rompe: que `S-30` tenía razón y salió `Text` al inferir sobre la tabla vacía.
  Cómo se sabe: `Data > Columns > MAN_Mantenimientos > CierreConExcepcion`, leer `Type` — cinco
  minutos, un solo lugar, sin necesidad de ejecutar nada más (§2.7, §6). Si sale `Text`, se retipa
  antes de dar por buena cualquier prueba de `PRUEBA-004`.
- **Se adopta que lo que se pierde es menor de lo que parece**: la cadena automática nunca se disparó
  sobre una fila real. Lo que cambia es que ahora existe un camino real para que el técnico lo diga,
  que sigue dependiendo de que decida decirlo, y que nadie más lo contrasta hasta que `D-12` exista.

## 8. Cierre bajo la vara nueva

**No hay texto literal de los quince hallazgos de la segunda pasada** (§0). Lo que sigue es la
reclasificación del trabajo hecho en esta reescritura contra la vara de `CLAUDE.md` §7.18 — *un
hallazgo bloquea solo si nombra qué se rompe en producción* —, no una lista punto por punto de un
dictamen que no se conservó.

### Lo que sobrevive como bloqueante

1. **El tipo de `CierreConExcepcion` (§2.7).** Nombra la rotura exacta: si sale `Text`, un técnico
   marcará la casilla y el formulario guardará sin pedirle el motivo — el defecto entero sobrevive
   por otra vía. Es la única condición que de verdad decide si esta especificación funciona, y no se
   puede cerrar sin acceso al editor.
2. **Los siete scripts de §2.9 sin editar.** Nombra la rotura: un ejecutor sigue `PROMPT_EXPRESIONES`
   o `PROMPT_CABLEADO` generados sin editar primero esos scripts y configura en el editor una columna
   que este documento retira, o dos verificadores fallan por una `COBERTURA`/bloque huérfano.

### Lo que se degrada a nota, y por qué

- **La cita de GPS sin indexar en `BASE_CONOCIMIENTO_APPSHEET.md` (§2.1).** No cambia ningún hecho
  verificado, solo dónde vive. Nota de higiene documental, no bloqueante.
- **El riesgo de `RG-19` sobre `UMBRAL_GPS` borrada (§2.3).** Real hoy, pero queda sin objeto en
  cuanto `RG-19` se retira con este mismo documento — no hace falta que nadie lo resuelva aparte.
- **El riesgo de secuencia `F-11`/`ORDEN-005` (§2.2).** Era real mientras `ESPEC-005` era un
  supuesto; con `ESPEC-005` aplicada y cerrada, el escenario que lo producía ya no existe.
- **La precisión sobre `Precision_GPS` y `LatLong` (§2.8).** Es un hecho histórico real, pero esta
  especificación retira la columna, así que no hereda el riesgo de tipo de nadie.
- **`PRUEBA-003` `P-09` sin acta (§2.12).** Es una dependencia de ejecución de `PRUEBA-004`, no un
  defecto de diseño de `ESPEC-004`: no bloquea aprobar esta especificación, sí bloquea confiar en
  `P-40`/`P-41` una vez ejecutadas.
- **La extensión y las reescrituras de citas entre versiones.** La versión anterior dedicaba secciones
  enteras a corregir citas erróneas de versiones aún anteriores de sí misma. Es meta-historia del
  documento, no verificación del sistema: se resume en una línea en vez de reconstruirse aquí.

### Riesgo aceptado — 2026-08-11

**No se pudo verificar el tipo de `CierreConExcepcion` en el editor durante esta reescritura**, por
no tener acceso a él. Es la condición 1 de arriba, y queda declarada explícitamente como pendiente en
vez de asumida: quien ejecute `ORDEN-004` la comprueba primero, con el comando de cinco minutos de
§2.7, antes de tocar nada más.
