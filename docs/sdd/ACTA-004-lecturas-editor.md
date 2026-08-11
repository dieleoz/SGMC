# ACTA-004 — Lo que el editor tenía de verdad en `MAN_Mantenimientos`

Cinco lecturas a ojo, con `Ctrl+Shift+R` previo, el 2026-08-11. Las pidió el arquitecto al aprobar
`ESPEC-004`, para cerrar su único bloqueante midiéndolo en vez de estimarlo.

Se transcriben aunque coincidan con lo esperado. **No hay comando que las recupere**: la API v2
devuelve filas, no esquema. Esta anotación es la única evidencia que va a existir.

---

## 1. Las cinco lecturas

| Columna · campo | Lo que había |
|---|---|
| `CierreConExcepcion` · `Type` | **`Yes/No`** |
| `CierreConExcepcion` · `Editable_If` | vacío — `Editable?` en `TRUE` por defecto, sin expresión |
| `CierreConExcepcion` · `Description` | vacío |
| `Precision_GPS` · `Type` | `Number` |
| `Precision_GPS` · `Initial value` | **vacío** |
| `Coordenadas_Cierre_LatLong` · `Editable_If` | `FALSE` |
| `UbicacionEscaneo_LatLong` · `Editable_If` | `FALSE` |
| `FechaHoraEscaneo` · `Editable_If` | `FALSE` |
| `MotivoExcepcion` · `Type` | `LongText` |
| `MotivoExcepcion` · `Required_If` | `[CierreConExcepcion] = TRUE` |

## 2. Lo que cierra

**El bloqueante de `ESPEC-004` no existía.** El riesgo aceptado 1 de su §8 decía: *si
`CierreConExcepcion` salió `Text`, un técnico marcará la casilla y el formulario guardará sin
pedirle el motivo*. Está en `Yes/No`. La comparación con `TRUE` es válida.

**`Precision_GPS` no trae `Initial value`.** Nadie cableó `USERLOCATIONACCURACY()` pese al bloqueo,
así que **se confirma la Rama A** de `ESPEC-004` §2.10: la columna queda huérfana, sin fórmula y sin
uso. La reversión es limpia. La Rama B —`Delete and re-add`, que «se lleva por delante todo lo demás
cableado en ella»— no hace falta.

Esto es exactamente lo que el arquitecto pidió: el documento llegó a estimar la Rama A en §2.10 y la
B en §7, que son contrarias y la B es la destructiva. **Se retiró la estimación y se midió.**

## 3. Lo que se escribió, y por qué a mano

`CierreConExcepcion` · `Description`:

```
¿La app no alcanzó buena precisión al capturar la posición de cierre? Marque si es así.
```

Va a mano porque **ningún generador del repositorio emite `Description`**: el `nota=` de una columna
no lo consume nadie (`grep -rn 'get("nota")' scripts/*.py` solo devuelve `generar_reconstruccion.py`,
y sobre `REGLAS`). Era un refinamiento adoptado en `ESPEC-004` §2.13 que nadie iba a poner. Persistió
tras recarga en duro.

## 4. Lo que esta acta NO cierra

**No se leyó el `App formula` de `CierreConExcepcion`**, y es la lectura que decide el fondo:

- Si trae la expresión de `RG-19`, la columna **se calcula sola** y el técnico no puede marcarla,
  por mucho que `Editable?` esté en `TRUE` — una `App formula` gana sobre editable. Y como
  `Precision_GPS` está siempre vacía, esa fórmula da siempre `FALSE`.
- Si está vacía, la casilla ya es libre, `RG-03` ya funciona y media `ESPEC-004` estaba hecha sin
  que nadie lo supiera.

El encargo de esta sesión pedía `Type`, `Editable_If` y `Description`, y **omitió el campo que
importaba**. Queda para la sesión siguiente. Se registra el hueco en vez de taparlo: un acta que
solo cuenta lo que salió bien es la clase de informe que este proyecto ya tiene cuatro.

## 4bis. El hueco, cerrado en la sesión siguiente: `RG-19` **sí** está viva

Leído del DOM sin activar el icono `=`, para no repetir el incidente de §5. `App formula` de
`CierreConExcepcion`:

```
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

Coincide **letra por letra** con `RG-19`. `Initial value`: vacío.

**Así que el defecto está vivo entero.** La columna se autocalcula, y una `App formula` gana sobre
`Editable?`: el técnico **no puede marcar la casilla** aunque `Editable?` esté en `TRUE`. `ESPEC-004`
no describía un riesgo hipotético.

### En qué valor se queda, que no es un detalle

La sesión que la leyó razonó que `ISBLANK(...)` es `TRUE` y por tanto el `OR` da `TRUE` siempre. **Es
al revés**, y se comprueba con los datos:

```
PAR_Parametros -> ParametroID='UMBRAL_GPS', Valor='40'
```

El parámetro **existe y vale 40**, así que `ISBLANK` da `FALSE`. Y `[Precision_GPS] > 40` con
`Precision_GPS` siempre vacía da `FALSE`. Luego `OR(FALSE, FALSE)` = **`FALSE` siempre**.

La diferencia importa más de lo que parece:

| Si diera | Lo que pasaría |
|---|---|
| `TRUE` siempre | el motivo se pide **en todos los cierres** — molesto, y **visible** el primer día |
| `FALSE` siempre | **no se pide nunca**, y nadie se entera — que es el defecto real |

## 4ter. No existe ningún bot en la aplicación

`Automation > Bots` muestra el estado vacío de AppSheet: *«Create bots to add automation to your
project»*, sin una sola fila. Verificado dos veces con recarga en duro.

El modelo declara **cinco** reglas de tipo bot —`RG-06`, `RG-07`, `RG-10` (por evento) y `RG-08`,
`RG-12` (programados)—. **Ninguna está creada.**

No es «activo vs desactivado»: es que la automatización no existe. Y tiene tres consecuencias que
tocan documentos vigentes:

- **`RG-07` no puede desactivarse antes de un fixture porque no está.** `PRUEBA-005` §1.5 y
  `PRUEBA-006` lo fijan como precondición común —*«sin desactivarlo, dispara hasta 3 correos reales a
  `ivan.salcedo@concesiondelsisga.com.co`, una dirección corporativa»*—. Ese riesgo **no existe hoy**,
  y la precondición se cae sola. Es una buena noticia que hay que escribir, porque quien lea esas
  pruebas hoy buscará un bot que no va a encontrar y no sabrá si lo borró alguien.
- **`RG-10` tampoco existe**, y `PRUEBA-005` `P-11`/`P-12` prueban justo que crea (o no crea) una
  orden de seguimiento. Esas dos pruebas no pueden pasar hoy por una razón distinta de la que
  declaran.
- **`RG-08` y `RG-12` no estaban puestos.** `ESPEC-006` los reemplaza porque **en la cuenta gratuita
  no se ejecutan nunca**; resultó que además nunca se llegaron a crear. No cambia su decisión —el
  motivo del reemplazo sigue en pie— pero sí su coste: no hay nada que retirar.

Es otra factura del mismo patrón: **el repositorio declara atributos que decide la plataforma.** El
modelo dice «cinco bots» y eso no los crea. Lo mismo que pasó con los 107 tipos y con las 8 claves.

## 5. Incidente — la app dejó de cargar durante la sesión

Al pulsar el **icono de fórmula (`=`)** junto a `Editable?` de `CierreConExcepcion` para comprobar
si traía expresión, AppSheet lo convirtió en una **expresión vacía**, y al guardar:

```
Column Name 'CierreConExcepcion' in Schema 'MAN_Mantenimientos_Schema' of Column Type 'Yes/No'
has an invalid Editable_If constraint '='. Empty expression

The _SISGA_-323965761 app did not load successfully.
version 1.000111 is not runnable --- please contact the app creator.
```

Se reparó dentro de la misma sesión —reabrir `Editable?`, salir con la `X` del campo de expresión,
guardar— y se verificó tras recarga en duro que quedó como casilla booleana limpia, sin fórmula
residual, y que la `Description` seguía puesta.

**Lo que deja escrito: inspeccionar no es gratis.** El icono `=` no es un visor, es un conmutador de
modo, y sobre un campo booleano lo deja en un estado que AppSheet considera inválido. Para leer si un
campo tiene expresión, **no se pulsa** — se mira si el icono aparece resaltado. Y si se activa por
accidente, se sale con la **`X`**, no con `Ctrl+Z`, comprobando que el `SAVE` vuelve a gris.

## 6. Lectura de vuelta

```
python scripts/instantanea.py comparar antes-de-man despues-de-man
-> NINGUNA CELDA CAMBIO
```

Con la matización que corresponde: `MAN_Mantenimientos` tiene **0 filas**, así que no hay celdas que
puedan moverse. Los dos cambios de esta sesión son metadatos de esquema, y un contraste de filas no
los ve **por construcción**. El verde aquí no prueba lo mismo que en una tabla poblada.


## 7. Una discrepancia sin resolver, anotada en vez de elegida

Sobre `MAN_Mantenimientos.MotivoExcepcion`, dos sesiones distintas leyeron cosas distintas:

| Sesión | Leyó |
|---|---|
| lecturas de §1 | `Required_If` = `[CierreConExcepcion] = TRUE` |
| lectura de §4bis | `Valid_If` = `[CierreConExcepcion] = TRUE` |

No es lo mismo. `Required_If` **obliga** a rellenar el motivo cuando la casilla está marcada, que es
lo que `RG-03` quiere. `Valid_If` con esa expresión diría que el motivo **solo es válido** si la
casilla está marcada — semantica distinta, y si estuviera en `Valid_If` en vez de en `Required_If`,
`RG-03` no obligaría a nada.

Puede que estén las dos, o que una de las dos lecturas confundiera el campo del panel. **No se elige
aquí cuál es**: se anota, y se resuelve mirando los dos campos en la misma pantalla y a la vez. Entra
en la cola de editor.
