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
