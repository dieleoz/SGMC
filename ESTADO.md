# Dónde vamos y qué falta

**Lea esto primero.** Es el mapa de todo lo demás: **lo que está abierto**.

**Qué es el sistema —qué resuelve, de qué se compone, el modelo, las decisiones que gobiernan el
diseño, qué se puede comprobar y qué no, y sus límites— está en
[`docs/SISTEMA.md`](docs/SISTEMA.md), en presente.** Aquí
no se repite: aquí solo va lo que falta.

> **Cuál es la aplicación y cuál la hoja lo dice `python scripts/sistema.py`, y nada más**, que
> también nombra las superadas con el motivo por el que dejaron de serlo. **Si un enlace no es uno
> de los dos que declara ese script, no es este sistema.**
>
> **Nada de lo retirado del árbol de trabajo se perdió.** La etiqueta
> `antes-de-la-limpieza-2026-08-10` devuelve el repositorio entero tal como estaba:
>
> ```bash
> git checkout antes-de-la-limpieza-2026-08-10
> ```

## En una frase

**La hoja de datos está terminada. Las 28 tablas y las 39 referencias están puestas y auditadas.
`ESPEC-005` es el primer dictamen del pipeline que pasó el gate y ya está aplicada al modelo y al
editor: las 8 claves llevan `UNIQUEID()` y las dos columnas virtuales `Etiqueta` están creadas.
`ESPEC-004` y `ESPEC-006` pasaron el gate, se aplicaron al modelo el 2026-08-11 (`ORDEN-004`,
`ORDEN-006`) — `RG-02`, `RG-19`, `RG-08` y `RG-12` se retiraron, ya no existen; `RG-37` y `RG-38` las
reemplazan; `Precision_GPS` se retiró del modelo — y les falta la mitad que vive en el editor:
ninguno de los tres bots por evento está creado, `Automation > Bots` sigue vacío hoy.
`ESPEC-007` está aprobada con riesgos aceptados, y sigue sin aplicar: falta `ORDEN-007`.
`ESPEC-008` está **aprobada con riesgos aceptados** (2026-08-11), con sus ocho condiciones
aplicadas y ampliada a `NOV_Novedades`. Falta su `ORDEN-008`. El guion de lo que queda por hacer a mano, paso a paso,
está en [`docs/LO_QUE_SE_HACE_A_MANO.md`](docs/LO_QUE_SE_HACE_A_MANO.md).**

```
FASE A   hoja generada, 28 tablas, 210 columnas          CERRADA
FASE B   39 referencias, auditor en 0 correcciones       CERRADA
FASE C   21 configurables · 9 cotejadas · 0 imposibles   EN CURSO
CLAVES   8 con UNIQUEID(): las 8 puestas, Key marcada, verificadas a ojo   EN CURSO
TIPOS    106 columnas a mano · unas 24 de 28 tablas con tipos corregidos   EN CURSO
LABEL    Label movido de la clave a la columna legible en unas 14 tablas · las 2 columnas
         virtuales Etiqueta creadas, con Show? y Label puestos             EN CURSO
BOTS     Automation > Bots vacío, ningún bot creado · 3 por evento sin empezar
         (RG-06, RG-10, RG-07 el último) · RG-37/RG-38 por cablear (no son bots)  ABIERTO
```

**Las cifras de arriba se leen distinto según su origen.** `21 configurables` son las **21 reglas**
que declara hoy el modelo, y se rederivan, no se citan —`ESPEC-004`/`ORDEN-004` retiraron `RG-02` y
`RG-19`, que eran las que no podían funcionar—. Las de `CLAVES`, `TIPOS`, `LABEL` y `BOTS` en cambio
son **lecturas a ojo del editor de hoy** —no hay comando que las recupere, la API v2 devuelve filas,
no esquema (`scripts/lectura_de_vuelta.py`)—, transcritas aunque coincidan con lo esperado. `18` y
`2` de la nota siguiente son una cosa distinta: el **objetivo** que declara el modelo, no lo que ya
se hizo en el editor —cuántas columnas *deberían* llevar `Label` según `scripts/modelo_objetivo.py`,
sea cual sea el progreso de hoy—, y esas sí salen de `inferencia.py`:

```bash
python scripts/validar_modelo.py     # Tablas 28 | Columnas 210 | Referencias 39 | Reglas 21
python scripts/inferencia.py         # a mano 106 · nombre 17 · contenido 87
python -c "import sys;sys.path.insert(0,'scripts');from inferencia import etiquetas_pendientes as e;p=e();print(len(p),'destinos ·',sum(1 for x in p if x[1]),'con Label')"
```

## 0. Los frentes abiertos, todos

Es lo que faltaba: **una sola tabla con todo lo que está a medias.** Si algo no está aquí, no está
abierto.

| Frente | Estado | Espera a |
|---|---|---|
| **`ESPEC-005`** · claves `OTID` y `PlanID` | **APLICADA AL MODELO Y AL EDITOR.** Primer dictamen que pasa el gate. `CLAVE_LEGIBLE` 22→20, `CLAVE_GENERADA` 6→8, reglas 21→23 con `RG-35` y `RG-36`. Las 8 claves con `UNIQUEID()` y las 2 columnas virtuales `Etiqueta` (`Show?`/`Label`) están puestas en el editor, verificadas a ojo | Nada de lo propio. Sigue abierto crear órdenes desde la app hasta que los 3 bots por evento y los filtros de seguridad estén cableados |
| **`ESPEC-004`** · `CierreConExcepcion` manual | **APROBADA CON RIESGOS ACEPTADOS** (tercera versión) y **APLICADA AL MODELO** por `ORDEN-004` el 2026-08-11. `RG-02` y `RG-19` se retiraron —ya no existen—, `Precision_GPS` se retiró del modelo. En el editor: `Type Yes/No` confirmado, `Description` escrita a mano. **Pendiente la mitad del editor** | Quitar la `App formula` de `CierreConExcepcion` en `Data > Columns`, resolver `MotivoExcepcion` (`Required_If` vs `Valid_If`) y ejecutar `PRUEBA-004` `P-40` a `P-45`. Ver [`ORDEN-004`](docs/sdd/ORDEN-004-cierre-excepcion-manual.md) §6 |
| **`ESPEC-006`** · reemplazo de los bots programados | **CERRADA con cuatro riesgos aceptados** (tercera pasada de arquitecto) y **APLICADA AL MODELO** por `ORDEN-006` el 2026-08-11. `RG-08` y `RG-12` se retiraron —ya no existen— | Cablear `RG-37`/`RG-38` en el editor (fila de abajo) |
| **`ESPEC-007`** · retirar `FOT_Fotografias.PrecisionGPS` | **APROBADA CON RIESGOS ACEPTADOS el 2026-08-11**, primera pasada de arquitecto. **No aplicada al modelo**: falta `ORDEN-007` | Ejecutar `ORDEN-007` sobre `scripts/modelo_objetivo.py` |
| **`ESPEC-008`** | **APROBADA CON RIESGOS ACEPTADOS** (2026-08-11), ocho condiciones aplicadas, ampliada a `NOV_Novedades` con `RG-40` | `ORDEN-008`. Su parche de `generar_prompt_cableado.py` va **en el mismo commit** que el cambio de modelo |
| `RG-02` · `RG-19` · `RG-08` · `RG-12` | **Retiradas del modelo, no existen.** `RG-03` ya no depende de las dos primeras: solo le falta el cableado de rutina en el editor, igual que el resto | — |
| Las **8 claves** con `UNIQUEID()` | **Las 8 puestas** en el editor, con `Key` marcada, verificadas a ojo | Nada. Ya está |
| Los **106 tipos** de columna | En curso. **Unas 24 de las 28 tablas** con tipos corregidos en la sesión del editor | Nada. Es mecánico |
| El **`Label`**: 18 por marcar (objetivo del modelo) + 2 virtuales | Label movido de la clave a la columna legible en **unas 14 tablas**. **Las 2 columnas virtuales `Etiqueta` están creadas**, con `Show?` y `Label` puestos | Nada. Ya se puede |
| Los **3 bots por evento** (`RG-06`, `RG-07`, `RG-10`) | **Sin empezar.** `Automation > Bots` está vacío, verificado dos veces (`docs/sdd/ACTA-004-lecturas-editor.md` §4ter). `RG-10` ya no está bloqueado: `OTID` y `PlanID` se generan solos | Nada. Ya se puede. `RG-07` se crea el último, porque manda correo real |
| `RG-37` (columna virtual `EstaVencida`) y `RG-38` (vista + acción) | **Reemplazan a `RG-08` y `RG-12`** (`ESPEC-006`/`ORDEN-006`, 2026-08-11): esos dos bots programados no corrían en la cuenta gratuita. Ninguno de los dos es un bot: `RG-37` es una columna virtual sobre `OT_OrdenesTrabajo`, `RG-38` es una vista más una acción sobre `PLA_PlanMantenimiento` que pulsa el supervisor. **Sin cablear en el editor** | Nada. Ya se puede |
| **Crear órdenes desde la aplicación** | **Desbloqueado por `ESPEC-005`, ya aplicada al editor.** Las órdenes se siguen creando en el Sheets **saltándose todas las validaciones** hasta que la app pueda crearlas | Los 3 bots por evento y los filtros de seguridad |
| Los **2 `Security Filter`** | Van **los últimos**: al ponerlos, la API deja de ver esa tabla y los dos instrumentos mecánicos se quedan ciegos (`lectura_de_vuelta.FILTROS_AL_FINAL`) | Todo lo anterior |
| **`MAN_Mantenimientos.OTID`** | **Ya es `Ref → OT_OrdenesTrabajo` en el modelo, y no hay nada que decidir.** Su propia nota lo dice: *«Era `Text`. Ese solo hecho impedia todo el geofencing»*. Lo decidido el 2026-08-07 fue lo contrario —**no** marcarlo `IsPartOf`—, para que borrar una orden no borre su ejecución. Lo abierto es otra cosa: **el auditor no puede comprobar que esté puesto en el editor**, porque `OT_OrdenesTrabajo` está vacía y el método necesita filas en el destino. Sale como `NO SE PUEDEN JUZGAR` | Nada que decidir. Se **mira** en el editor |
| **Las coordenadas reales** | 368 derivadas del `PK`, **ninguna medida en campo**, y **las 368 distintas entre sí** — lo que las hace peores que inútiles: una coordenada única para todos dejaría el geofencing **decorativo** y pasaría siempre; 368 puntos sintéticos distintos hacen que **el técnico esté en el activo real y el sistema le diga que no**. Rechaza cierres legítimos, que es peor que no comprobar nada | Operación. **Es el bloqueo del piloto** |
| **288 de 333 preguntas** en borrador | Marcadas `[BORRADOR: validar con operacion]` | Operación |
| `D-04` y `SED_Sedes.UnidadFuncionalID` | Avisos que **pasan a fallo el 2026-08-31** | Operación |

**Lo que no depende de nosotros son las tres últimas**, y son las que de verdad impiden arrancar.
Lo demás es trabajo.

### El primer fixture cierra una ventana, y no se vuelve a abrir

Lo pide el arquitecto y no puede quedarse solo en su dictamen:

> **A partir del primer fixture de prueba, `OT_OrdenesTrabajo`, `MAN_Mantenimientos` y
> `PLA_PlanMantenimiento` dejan de estar en cero para siempre.**

Hoy las tres están vacías, y una tabla vacía es el único momento en que un cambio de tipo o de clave
**no arrastra ni una fila**. En cuanto entre la primera, cualquier conversión pasa a tener que
migrar datos, y eso deja de ser gratis.

**Lo que se lleva por delante es `MAN_Mantenimientos.OTID`.** El modelo ya lo declara `Ref` a
`OT_OrdenesTrabajo`; **el editor lo sigue teniendo `Text`**, y mientras esté `Text` no hay
referencia real y toda la cadena `[OTID].[ActivoID].[…]` del geofencing no existe. Es la conversión
que `ESPEC-003` deja pendiente.

**Si esa conversión se va a hacer, se hace antes del primer fixture.** No es una preferencia de
orden: después hay que resolver a mano cada valor de `OTID` ya escrito, y ninguna de las dos
comprobaciones mecánicas —`auditar_cableado.py` e `instantanea.py`— avisa de que la ventana se
cerró.

### El volcado local es CIEGO a las ocho tablas de movimiento

**`generar_plantilla.py` las vacía a propósito** cada vez que corre: son registros de prueba, y la
plantilla es lo que recibe el funcional. Está declarado en `scripts/lectura_de_vuelta.py` como
`VOLCADO_CIEGO_A`, y son las ocho de `CLAVE_GENERADA`:

```
OT_OrdenesTrabajo · MAN_Mantenimientos · CHK_Checklists · CHD_ChecklistDetalle
FOT_Fotografias   · FIR_Firmas         · NOV_Novedades  · PLA_PlanMantenimiento
```

**La consecuencia anula pruebas enteras.** `verificar_faseA.py` y `verificar_datos.py` leen
`BD/Modelo_Datos_PLANTILLA.xlsx` por defecto. Una fila creada **en la aplicación** —un fixture, una
orden real— **nunca llega a ese archivo**. Cualquier comprobación que espere verla ahí **no puede
dispararse jamás**, y pasa en verde por no ejercitarse. Lo encontró el arquitecto sobre `PRUEBA-004`:
dos de sus pruebas eran imposibles.

**Para mirar datos de movimiento, `python scripts/instantanea.py`**, que lee por API; o se descarga
el Sheets a un archivo aparte y se le pasa por argumento al verificador. El volcado sirve para
estructura y catálogos, no para esto.

### ¿Esto es replicable?

**La hoja sí.** Se rehace con un comando, y `verificar_reproducible.py` demuestra que dos pasadas
dan las 29 pestañas idénticas celda por celda. No hay que conservarla: se genera.

```bash
python scripts/generar_plantilla.py
```

**La aplicación no automáticamente, y no puede serlo:** la API v2 de AppSheet devuelve filas, no
esquema, así que no hay forma de escribir tipos, claves, etiquetas ni expresiones desde un script.
Se reconstruye a mano siguiendo tres documentos, y **todo lo que se tocó en el editor el 2026-08-10
está escrito en alguno de los tres**: las claves con `UNIQUEID()`, los tipos, el `Label`, los
`Editable_If`, los `Security Filter`, la estructura de los bots y el patrón de dos pasos para los
que añaden filas.

> **Lo que hay que decir y no está probado:** ese procedimiento **nunca se ha ejecutado entero desde
> cero**. Se fue escribiendo mientras se arreglaba, así que describe lo que hicimos, no lo que se
> comprobó que funciona seguido de principio a fin. La única forma de saberlo es reconstruir una
> aplicación nueva a partir de los tres documentos y comparar. Hasta entonces, «replicable» es una
> intención razonada, no un hecho verificado.

### El orden de las dos especificaciones: se cumplió, y `ESPEC-005` ya pasó

**`ESPEC-005` iba primero, y fue.** Motivo: `PRUEBA-004` monta su fixture sobre claves `OTID`
tecleadas a mano, y `ESPEC-005` las convierte en `UNIQUEID()`. Al revés, el fixture habría quedado
inconstruible y habría habido que reescribir la tanda de pruebas dos veces.

**Es el primer dictamen del pipeline que pasa el gate.** El arquitecto verificó la cita de Google
que sostiene el diseño —*«Add a virtual column… enter a `CONCATENATE()` expression»*—, reprodujo el
diseño en una copia, corrompió la expresión a propósito y comprobó que `V-11` la caza.

Lo que cambió en el modelo, y se cuenta con un comando:

```bash
python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(len(M.CLAVE_LEGIBLE),len(M.CLAVE_GENERADA),len(M.REGLAS))"
# 20 8 21 — hoy. Cuando ESPEC-005 se aplicó, este comando daba 20 8 23; RG-35 y RG-36 siguen
# vivas, pero ORDEN-004/ORDEN-006 (2026-08-11) retiraron RG-02, RG-19, RG-08 y RG-12 y añadieron
# RG-37/RG-38, así que el total volvió a bajar a 21 por un camino distinto
```

| | Antes de `ESPEC-005` | Tras `ESPEC-005` | Hoy (tras `ORDEN-004`/`ORDEN-006`) |
|---|---|---|---|
| `CLAVE_LEGIBLE` | 22 | 20 — salen `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` | **20**, sin cambio |
| `CLAVE_GENERADA` | 6 | 8 — entran las dos, con `UNIQUEID()` | **8**, sin cambio |
| `REGLAS` | 21 | 23 — entran `RG-35` y `RG-36` | **21** — salen `RG-02`, `RG-19`, `RG-08`, `RG-12`; entran `RG-37`, `RG-38` |

**`RG-35` y `RG-36` no son columnas de la hoja: son columnas VIRTUALES llamadas `Etiqueta`**, que
AppSheet calcula y no se guardan en el Sheets. Por eso no están en `MODELO` —`F-02` no las exige, no
tocan la hoja— y viven solo en `REGLAS`, declaradas aparte en `inferencia.ETIQUETA_VIRTUAL`. Se
probó meter `Etiqueta` en la tupla `ETIQUETAS` y **no funciona**: `etiqueta_de()` solo mira `MODELO`.

```
RG-35  OT_OrdenesTrabajo     CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])
RG-36  PLA_PlanMantenimiento CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])
```

**Y eso desbloquea crear órdenes desde la aplicación**, que hoy se siguen haciendo en el Sheets
saltándose todas las validaciones. Lo que falta para cobrarlo es la mitad que vive en el editor:
crear las dos columnas virtuales, marcarles `Show?` y marcarles `Label`. El encargo lo trae
[`docs/PROMPT_CABLEADO.md`](docs/PROMPT_CABLEADO.md), paso 5.

### La decisión que ya se cerró: `ESPEC-004`, tercera versión, aplicada

| | Qué pasó | Qué queda |
|---|---|---|
| [`ESPEC-004`](docs/sdd/ESPEC-004-cierre-excepcion-manual.md) · **APROBADA CON RIESGOS ACEPTADOS, APLICADA AL MODELO** | `RG-02` usaba `USERLOCATIONACCURACY()`, que **no existe en AppSheet**: `Precision_GPS` nunca se poblaba, `RG-19` comparaba blanco y `RG-03` no pedía nunca el motivo. `ORDEN-004` (2026-08-11) retiró `RG-02` y `RG-19` del modelo y retiró `Precision_GPS`; `CierreConExcepcion` pasa a ser una casilla que marca el técnico | Cablear en el editor: quitar la `App formula` de `CierreConExcepcion`, resolver `MotivoExcepcion` y ejecutar `PRUEBA-004` `P-40` a `P-45` |

**Segunda pasada del arquitecto: quince hallazgos, después una tercera versión bajo la vara de
`CLAUDE.md` §7.18.** La primera versión recibió doce condiciones y se rehizo con las once que
faltaban; la versión rehecha volvió con quince; la tercera pasó con dos hallazgos que sobreviven
como bloqueantes de editor y un riesgo aceptado. Aplicada en `modelo_objetivo.py` por `ORDEN-004`;
**el editor sigue pendiente** (§6 de esa orden).

**Nada se aplica hasta que el arquitecto lo tumbe o lo deje pasar.** Es la regla que nos saltamos el
2026-08-10 por la mañana, y costó un dictamen de veinte observaciones. `ESPEC-005` fue el primer
dictamen en pasar el gate; `ESPEC-004` y `ESPEC-006` lo pasaron después, el 2026-08-11, y las tres
ya están aplicadas al modelo.

> **Lo que bloquea el piloto no ha cambiado en todo el día:** las 368 coordenadas se derivan del
> `PK` sobre el trazado y **ninguna se midió en campo**. El geofencing puede quedar perfecto y estar
> midiendo distancias a puntos inventados.

---

## 1. Qué está hecho

### La hoja de datos

`Modelo_Datos_10082026` sale generada del modelo, no heredada de nada.

```
28 pestañas de datos más _LEEME · 210 columnas · ninguna de sobra
ACT_Activos        368 activos, un solo inventario, códigos SOS-001 / SWIT-001
TIP_TiposActivo     27 tipos, con radio de cierre poblado en los 27
FRM_Formularios     27 formularios, uno por tipo
FRM_Preguntas      333 preguntas, los 27 checklists con contenido
LST_ValoresLista   108 valores, ningún desplegable vacío
Sin registros de prueba · FASE A CERRADA, 82 conformes y 4 avisos
```

Se rehace entera con un comando y **se reproduce**: dos ejecuciones seguidas dan las 29 pestañas
idénticas, celda por celda.

```bash
python scripts/generar_plantilla.py
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

> **El archivo local ya está en 210; la hoja de producción `Modelo_Datos_10082026` todavía no.**
> `ORDEN-004` (2026-08-11) retiró `Precision_GPS` de `scripts/modelo_objetivo.py` y regeneró
> `BD/Modelo_Datos_PLANTILLA.xlsx` —confirmado: ya no trae esa columna—, pero **no tocó el Sheets de
> producción**, por prohibición explícita de la sesión. Ahí `Precision_GPS` sigue existiendo como
> columna huérfana (211), hasta que alguien haga *Delete and re-add* de `MAN_Mantenimientos` por otro
> motivo. Los dos archivos no coinciden hoy, y es esperado, no un error.

### El modelo

`scripts/modelo_objetivo.py` es la fuente única: **28 tablas, 210 columnas, 39 referencias, 21
reglas.** De ahí se generan el diccionario, el manual de despliegue, la guía funcional y la lista de
reposición de expresiones. Nada de eso se escribe a mano.

**Fueron 23 reglas mientras `ESPEC-005` (que añadió `RG-35` y `RG-36`) estuvo aplicada sin
`ESPEC-004`/`ESPEC-006`.** El 2026-08-11, `ORDEN-004` retiró `RG-02` y `RG-19`, y `ORDEN-006` retiró
`RG-08` y `RG-12` y añadió `RG-37` y `RG-38`: el total volvió a 21, por una composición distinta a
la de antes de `ESPEC-005`. La cifra la imprime `python scripts/validar_modelo.py` en su primera
línea; no se cita de memoria.

### La aplicación

**Las 28 tablas dadas de alta sobre la hoja definitiva**, con las claves alfanuméricas ya puestas.
Comprobado por API el 2026-08-10: las 28 responden, **ninguna de más ni de menos**, y cada una ve
exactamente las columnas que el modelo declara más el `_RowNumber` que añade AppSheet.

> **Lo que esa comprobación demuestra y lo que no.** La API devuelve **filas de datos**, así que
> prueba que las tablas existen, que la estructura llegó y que las claves entraron como texto
> —`ACT-0001`, `TIP-001`, `UNF-01`—. **No devuelve tipos**: que `Ubicacion_LatLong` sea `LatLong` y
> no `Text` solo se ve abriendo `Data > Columns` en el editor.

> **Subir el Excel arregla la hoja, no la aplicación.** Son dos sitios distintos. El Excel fija
> columnas y datos; **el tipo de cada columna, la clave y las referencias viven en el esquema de
> AppSheet**, que se infiere de los datos y hay que corregir a mano.
>
> Eso ya se corrigió tabla por tabla, pero el mecanismo sigue vivo: **`TramoINVIAS` se tipa `Number`
> mientras el único valor cargado sea `5607`**, y el día que operación escriba `55CN03` no cabrá.

### Lo que dejó la sesión del editor

**Sesión del 2026-08-10, cuatro horas de navegador:**

```
CLAVES     las 6 con UNIQUEID()          ya estaban
TIPOS      22 de las 28 tablas           hechas
ETIQUETAS  esas mismas 22 tablas         hechas
           UNF_UnidadesFuncionales · USR_Usuarios   sin terminar
BOTS       los 5                          sin empezar
```

**Un solo cambio en los datos en toda esa sesión, y era el esperado:**
`ACT_Activos[ACT-0034].FechaBaja` perdió la hora al pasar de `DateTime` a `Date`.

> Que cuatro horas de tocar el esquema produzcan **un** cambio de dato es el resultado bueno, no el
> aburrido: significa que los tipos se corrigieron sin reescribir el inventario por debajo. Y lo
> sabemos porque `instantanea.py` compara celda a celda contra una foto previa — sin eso, esta
> frase sería una impresión.

**Sesión del 2026-08-11, sobre la anterior:**

```
CLAVES     las 8 con UNIQUEID(), las 8   Key marcada, verificadas a ojo
TIPOS      unas 24 de las 28 tablas      con tipos corregidos
LABEL      unas 14 tablas                con Label movido de la clave a la columna legible
           2 columnas virtuales Etiqueta creadas, con Show? y Label
DESCRIPTION  CierreConExcepcion          escrita a mano (ningún generador la emite)
BOTS       ninguno creado                Automation > Bots vacío, verificado dos veces
```

**La lectura de vuelta de esta sesión salió limpia: los datos no cambiaron.**
`docs/sdd/ACTA-006-cotejo-y-supuesto.md` §3 compara dos instantáneas y el resultado es
`NINGUNA CELDA CAMBIO`. `auditar_cableado.py` sigue en **0 correcciones**.

**Y dejó dos hallazgos que van más allá de esta sesión**, escritos en
[`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) §17 y §18: un tipo mal
puesto no solo deja una regla decorativa, **falsea lo que la API devuelve** — `USR_Usuarios.Telefono`
tipada `Number` le comía el `+` del indicativo, y la API lo devolvía sin que nadie escribiera nada
distinto—; y el icono `=` junto a `Editable?`/`Require?` **no es un visor, es un conmutador**: pulsado
sobre un campo booleano lo deja con expresión vacía y **tumbó la aplicación entera** durante una
sesión cuyo encargo era de solo lectura. El detalle operativo de los dos, y cómo evitarlos, está en
[`docs/LO_QUE_SE_HACE_A_MANO.md`](docs/LO_QUE_SE_HACE_A_MANO.md) §0.

#### `RespuestaLista` es un `Enum` sin catálogo, y se resolvió con `Allow other values`

`CHD_ChecklistDetalle.RespuestaLista` está declarada `Enum` y **el modelo no le declara lista de
valores a propósito**: su contenido depende de la pregunta, y las opciones viven en
`LST_ValoresLista`, una fila por valor y por pregunta. No hay un conjunto fijo que declarar.

**AppSheet lo rechazaba**: un `Enum` sin valores no se deja guardar. Se resolvió activando
**`Allow other values`**, que es exactamente lo que corresponde a un dominio abierto.

**Queda escrito porque es una decisión de diseño, no un apaño.** Quien encuentre esa columna sin
lista y sin esta nota va a suponer que falta poblarla, y va a inventarse los valores — que es
precisamente lo que ya pasó una vez con un `Enum` de este repositorio.

---

## 2. Qué falta

**La aplicación se reconstruyó desde cero el 2026-08-10, así que el cableado de la anterior no
sirve: se repone entero.** No es una lista de retoques, es el procedimiento completo.

> **Ningún documento de esta tabla sabe cuánto está hecho, y no es un descuido: todos salen del
> modelo, así que describen el destino.** El estado lo tiene la aplicación y se le pregunta con
> `scripts/auditar_cableado.py`. Lo aprendimos caro: el informe de cableado del 2026-08-10 decía
> «39/39 asignadas» y de las que se podían mirar, cinco estaban mal —`TipoActivoID` apuntaba a la
> tabla de sedes, y tres columnas de texto se habían vuelto referencia—. La API respondía 28/28 y
> `validar_modelo.py` daba APTO. Es la regla **R-04**: *preguntar «apunta a algo» nunca contesta
> «apunta a lo correcto»*.

| # | Qué | Dónde está escrito |
|---|---|---|
| 1 | **Las 39 referencias**, con `IsPartOf` en las cuatro que lo llevan | [`docs/PROMPT_CABLEADO.md`](docs/PROMPT_CABLEADO.md) — el encargo. Cuántas faltan **hoy**: `python scripts/auditar_cableado.py` |
| 2 | **Las 21 reglas**: geofencing, umbral de GPS, `Editable_If`, los bots, las 2 etiquetas virtuales | [`docs/PROMPT_EXPRESIONES.md`](docs/PROMPT_EXPRESIONES.md) — el encargo de la Fase C, con la cadena de referencias que atraviesa cada una. **Dónde está cada control en pantalla**: `python scripts/navegacion_editor.py` |
| 3 | **Los dos filtros de seguridad**: activos por unidad funcional, órdenes por técnico | Ídem |
| 4 | **Las cuatro marcas de tiempo** como `ChangeTimestamp` del servidor | Ídem |
| 5 | **Retirar `Deletes`** en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` | Ídem |
| 6 | **Los tipos de columna**: AppSheet adivinó los de las 8 tablas vacías, y una regla sobre una columna mal tipada no da error, no hace nada | [`docs/TIPOS_ESPERADOS.md`](docs/TIPOS_ESPERADOS.md) |
| 7 | **Correr `PRUEBA-003`** | [`docs/sdd/PRUEBA-003-despliegue.md`](docs/sdd/PRUEBA-003-despliegue.md) |

**El orden del 5 no es opcional.** Se marca `IsPartOf` en cuatro referencias, y eso es borrado en
cascada: borrar un mantenimiento se lleva sus fotografías, su firma y su checklist. Solo es seguro
porque el mantenimiento nunca se borra, y eso es lo que hace quitar `Deletes`.

**Antes de nada, dos comprobaciones que solo se pueden hacer ahora**, recién dadas de alta las
tablas, y que después salen carísimas:

- **Ninguna clave compuesta.** AppSheet combina dos columnas cuando no encuentra una única. Contra
  una clave compuesta **no resuelve ninguna referencia** y falla el bloque entero sin decir por qué.
  Deben ser 28 claves simples, todas `Text`.
- **Ninguna tabla dos veces.** Es el fallo propio de dar de alta una por una: aparece
  `OT_OrdenesTrabajo_1` o `Copy of…`. Con dos tablas sobre la misma pestaña **las referencias se
  reparten y la mitad de las filas parece desaparecer, sin error**.

Y una de cuenta: **28 tablas, no 29.** `_LEEME` es la pestaña de instrucciones y no se da de alta.

### Lo que no desbloquea ningún cableado

**Las coordenadas no son reales.** Ninguno de los 368 activos tiene su posición levantada en campo:
están calculadas sobre el trazado del corredor. Hasta cargarlas, la comprobación de distancia al
cerrar **no significa nada**. Es la decisión D-01 y es el bloqueo del piloto.

**Y 288 de las 333 preguntas son borrador.** Llevan `[BORRADOR: validar con operacion]` en su ayuda.
Buscar esa marca en la hoja dice exactamente qué queda por revisar, y el día que no aparezca
ninguna, el banco de preguntas está cerrado. Las 45 restantes —SOS, CCTV y PMVF— ya estaban
acordadas.

---

## 3. El entregable de datos

**`BD/Modelo_Datos_PLANTILLA.xlsx`** es lo que recibe el funcional, y es el mismo archivo que está
publicado como `Modelo_Datos_10082026`.

**Viene autocompletado a propósito:** cada columna trae un valor con el formato correcto para que se
corrija en vez de adivinarlo. La primera pestaña, `_LEEME`, dice en qué formato va cada cosa —la
coordenada, la fecha, el decimal— y qué columnas hay que completar.

**El principio es de operación: entregamos la estructura; el dato real lo pone quien lo conoce.**

### Lo que sí está anclado en fuente

**Las cuatro unidades funcionales son las del contrato**, Apéndice Técnico 1, Tabla 3:

```
UF1  Sisga - Machetá - Manta - Guateque                      50,01 km
UF2  Guateque - Garagoa - Macanal                            22,00 km
UF3  Macanal - Santa María                                   17,80 km
UF4  Santa María - Cachipay - San Luis de Gaceno - Aguaclara 47,36 km
```

**No son cuartos iguales**, que es como estaban repartidas hasta el 2026-08-10. Al corregirlo
resultó que **107 de los 368 activos estaban en la unidad funcional equivocada**. Importa porque
`RG-04` filtra por UF: cada técnico habría visto un conjunto de activos que no es el suyo, y nada lo
habría detectado, porque la referencia resolvía.

> **Y el contrato prueba una carencia del modelo que hasta ahora era una sospecha: un PR no
> identifica un punto.** El corredor **atraviesa tres rutas de INVÍAS**, no una — `55CN03` del
> PR0+0+000 al PR6+194, `5607` del PR7+146 al PR46+080 y `5608` del PR0+000 al PR92+048.
>
> **Hay dos puntos distintos llamados «PR 0+000»**: el arranque en El Sisga sobre la `55CN03` y
> Guateque sobre la `5608`, separados por unos 50 km. Un técnico enviado al «PR 0+000» no sabe a
> cuál de los dos.
>
> Lo resuelve declarar la ruta, o el **PK**, que es lineal y continuo en todo el corredor. Están
> declaradas como columnas propuestas `ACT_Activos.PK` y `ACT_Activos.TramoINVIAS`, sin implementar:
> es cambio de modelo y pasa por especificación.

### Quince túneles, y un tercio de la UF3 bajo tierra

El contrato los lista con su PR de entrada y salida —tablas 13, 19 y 20—. Son **7.224 metros**, y
no están repartidos: **la UF3 tiene once túneles que suman 6.000 de sus 17.800 metros**. Un tercio
de ese tramo va bajo tierra, con `El Polvorín` de 1.649 m como el más largo.

> **Dentro de un túnel el GPS no fija posición, y `RG-01` comprueba la distancia al activo al
> cerrar.** Todo equipo dentro de un túnel **falla esa comprobación siempre**, por diseño y no por
> avería.
>
> Hoy eso se manejaría como excepción caso por caso, y el supervisor vería a un técnico acumulando
> cierres con excepción **sin saber que es el túnel y no el técnico**. Está declarada la tabla
> `TUN_Tuneles` en `PROPUESTAS`, sin especificar.

Y el contrato apunta otra cosa: **la ventilación de los túneles figura como `N/A`** y lo único que
exige es iluminación. Si no hay ventilación ni detección de incendios, esos túneles no aportan los
activos que cabría esperar — pero **falta leer la página 27**, donde continúa la tabla de los cinco
últimos.

**Y el contrato da el dato que a `SED_Sedes` le faltaba:** el peaje de Machetá está en el
**PR27+240 de la Ruta 5607**, cobro bidireccional, unidad funcional 1. El de San Luis de Gaceno
aparece en el mapa del contrato marcado como **peaje nuevo**, sin fila de tabla ni abscisa: está
proyectado, no construido. `SED_Sedes` los lista como si los dos existieran.

### Por qué el catálogo tiene 27 tipos y el Plan Maestro 18 familias

**No son la misma lista, y que los dos números fueran 18 lo escondía.** `TIP_TiposActivo` decide
**qué checklist ve el técnico**; las familias del Plan Maestro son **cómo operación cuenta los
equipos**. Nueve familias no tenían tipo propio y colgaban del de otra cosa: la impresora heredaba
el checklist del NAS, el portátil el del servidor, el carril de peaje el de la báscula.

Eran **78 activos de 355 con el checklist equivocado**, y ningún verificador lo veía porque
`TipoActivoID` resolvía contra una fila que existe. `scripts/catalogo_tipos.py` lo cierra como
fuente única, con `comprobar()`, que falla si dos familias comparten tipo o si un tipo se queda sin
radio.

---

## 4. Qué leer, según lo que necesite

| Si necesita | Lea |
|---|---|
| **Saber qué le toca a usted** | [`docs/INDICACIONES_POR_ROL.md`](docs/INDICACIONES_POR_ROL.md) |
| **Cablear la aplicación** | [`docs/PROMPT_CABLEADO.md`](docs/PROMPT_CABLEADO.md) — el encargo entero, generado del modelo: las 39 referencias con su destino, los tipos y el orden |
| **Qué queda por hacer a mano, paso a paso** | [`docs/LO_QUE_SE_HACE_A_MANO.md`](docs/LO_QUE_SE_HACE_A_MANO.md) — 13 pasos, 11 sin ningún comando que los verifique. Es el guion de quien va al editor |
| **Cambiar algo del modelo** | [`docs/REGLAS_DEL_MODELO_DE_DATOS.md`](docs/REGLAS_DEL_MODELO_DE_DATOS.md) — las diez reglas del motor, con el fallo del que salió cada una y quién la hace cumplir |
| **Construir la aplicación** | [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md) — diez pasos y una ficha por tabla, columna por columna |
| **La expresión exacta de una regla** | [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) — las 21 sin cortar |
| **Dónde está ese control en el editor** | `python scripts/navegacion_editor.py` — el nombre de la regla **no es** el nombre del control |
| **Quién comprueba lo que acabo de hacer** | `python scripts/lectura_de_vuelta.py` — y si contesta «a ojo», es que no hay comando |
| **Probar que funciona** | [`docs/sdd/PRUEBA-003-despliegue.md`](docs/sdd/PRUEBA-003-despliegue.md) |
| **Qué hace el sistema y para quién** | [`docs/FUNCIONAL_SGMC.md`](docs/FUNCIONAL_SGMC.md) |
| **La estructura de datos real** | [`docs/bd.md`](docs/bd.md), generado del archivo |
| **Cómo se comporta AppSheet, con la cita oficial** | [`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) |
| **Con qué supuestos se construye** | [`docs/ALCANCE_Y_SUPUESTOS_SGMC.md`](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) |
| **El orden de implementación** | [`docs/ROADMAP.md`](docs/ROADMAP.md) |

---

## 5. Los seis verificadores

Ninguno sustituye a otro, y **lo único que ha funcionado en este proyecto es lo mecánico**.

```bash
python scripts/validar_modelo.py         # el modelo consigo mismo. Gate del pipeline
python scripts/verificar_faseA.py        # el modelo contra la hoja descargada
python scripts/verificar_documentos.py   # la prosa contra el modelo
python scripts/verificar_enlaces.py      # que todo enlace entre documentos resuelve
python scripts/verificar_reproducible.py # que generar dos veces dé lo mismo
python scripts/verificar_datos.py        # el único que abre el archivo de datos
```

**`verificar_reproducible.py` nació de lo que los otros no pueden ver.** Al resembrar las claves, el
generador dejó de ser idempotente: la garantía de catálogo buscaba las filas por clave, la resiembra
cambiaba esa clave, y en la pasada siguiente las volvía a añadir. `SED_Sedes` acabó con las seis
edificaciones **duplicadas**, y cada ejecución habría añadido seis más.

Pasó todos los demás: el modelo era coherente, la Fase A cerraba, la prosa cuadraba y los enlaces
resolvían. **Todos miran un archivo, y ese defecto solo existe entre dos ejecuciones.**

### Lo que se añadió después, y qué agujero tapa cada uno

Ninguna de estas comprobaciones estaba escrita en ningún documento hasta ahora.

| | Qué mira | El agujero que tapa |
|---|---|---|
| **`V-18`** en `validar_modelo.py` | Una regla declarada **dos veces con expresiones distintas** —una en la columna, otra en `REGLAS`— | `RG-19` lo estaba **y nadie lo veía**. La columna decía `[Precision_GPS] > LOOKUP(…)` y `REGLAS` decía `OR(ISBLANK(LOOKUP(…)), …)`. `RECONSTRUCCION_EXPRESIONES` —lo que el ejecutor teclea— toma la de `REGLAS`. Sin la guarda la regla es falsa siempre; con ella, falsa **solo mientras exista el parámetro**, y hay dos cuentas con permiso de edición sobre el Sheets |
| **`V-11` ahora recorre también las columnas** | Toda expresión del modelo, venga de `REGLAS` **o del `formula` / `valid_if` / `valor_inicial` de una columna** | Antes solo miraba `REGLAS`, así que una expresión escrita en una columna **no se validaba en absoluto**. El arquitecto metió en una columna la peor expresión posible —desreferenciar un `Yes/No` y nombrar una columna que no existe— y el validador respondió `APTO PARA DESPLEGAR`. La misma dentro de `REGLAS` daba dos errores |
| **`G-04`** en `verificar_datos.py` | Tablas que llegaron **vacías y tipadas a ciegas**: AppSheet eligió el tipo de sus columnas sin un solo dato | Son las 8 de movimiento. Y el aviso dice en voz alta que **este archivo las vacía por diseño**, así que salen vacías aunque la aplicación tenga filas |
| **`G-05`** en `verificar_datos.py` | Reglas que **leen una columna vacía**, cruzando el alcance real contra los datos | Es como se caza `RG-06`: bien escrita, sin error, y `GeneraAlerta` vacía en los cuatro estados. Hoy señala `ACT_Activos.SedeID`, de la que depende `RG-34` |

Y tres instrumentos que no son verificadores pero declaran lo que nadie declaraba:

| | Qué declara |
|---|---|
| **`scripts/lectura_de_vuelta.py`** | Por clase de cambio, **quién lo comprueba**: `referencias`, `datos` y `estructura` tienen comando; **`tipos`, `expresiones`, `permisos` y `etiqueta` no tiene nadie**. Tres con comando, **cuatro a ojo** — y las cuatro son justo las que sobrevivieron a tres informes de «hecho». Un paso sin comprobación declarada se lee como comprobado |
| **`scripts/navegacion_editor.py`** | El **mapa de clics** del editor. Los nombres de las reglas **no son los de los controles**: `Required_If` se llama **`Require?`** y **no es una casilla que se marque** —hay que pulsar el icono `=` de al lado—. El 2026-08-10 acabó escrita en `Valid If` |
| **`scripts/alcance_reglas.py`** | Qué columnas toca **de verdad** cada regla, **con su tabla**. Son **39 de las 210**. Atribuyendo por nombre suelto salían **94**: como `[Activo]` aparece en `RG-04` y en `RG-16`, las **23 columnas llamadas `Activo`** de 23 tablas distintas salían con esas dos reglas encima. Y eso no es cosmética: esa atribución **ordena el trabajo del ejecutor**, así que inflarla convierte la prioridad en ruido |

```bash
python scripts/lectura_de_vuelta.py   # quién lee de vuelta cada cosa, y quién no
python scripts/navegacion_editor.py   # dónde está cada control en pantalla
python scripts/alcance_reglas.py      # 39 de 210, con su tabla
```

---

## 6. Lo que costó la semana, para no repetirlo

**AppSheet ignora las pestañas ocultas.** Ocho catálogos ocultos hacían que cargara 24 tablas de 32,
sin un solo mensaje, mientras nuestra verificación decía que todo estaba bien porque `openpyxl` sí
las lee. Lo caza `F-18`.

**`Regenerate` fusiona, no reemplaza.** Conserva las columnas viejas a propósito. Con un esquema muy
divergente impide converger, y por eso se reconstruyó en vez de reparar.

**Una referencia que resuelve puede apuntar a lo que no es.** Pasó dos veces: el inventario
sintético reescribió 34 activos reales, y nueve familias vieron el checklist de otro equipo. Las dos
veces la comprobación de huérfanos daba verde. Los verificadores contestan «apunta a algo», nunca
«apunta a lo correcto».

**Una instrucción que exige criterio se ejecuta mal.** «Oculte las columnas retiradas» produjo que
se cableara una trampa como referencia y que alguien se inventara los valores de un `Enum`. Por eso
los documentos llevan la lista completa, generada, sin nada que deducir.

**Un tipo mal no solo deja una regla decorativa: falsea lo que la API devuelve.** `USR_Usuarios.Telefono`
tipada `Number` le comía el `+` del indicativo a la lectura — el dato en la hoja estaba bien desde el
principio, lo que cambió fue lo que el lector truncaba. Un contraste de instantáneas que compara
contra la foto anterior, no contra la hoja, puede archivar esto como «diferencia benigna» sin verla.
Detalle completo en [`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) §17.

**El icono `=` no es un visor, es un conmutador.** Junto a `Editable?` o `Require?`, pulsarlo sobre un
campo booleano lo convierte a expresión vacía, y al guardar **la aplicación entera deja de cargar** —
no la columna, la app—, incluso durante una sesión cuyo encargo era de solo lectura. Se sale con la
`X` del campo de expresión, nunca con `Ctrl+Z`. Detalle completo en
[`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) §18.
