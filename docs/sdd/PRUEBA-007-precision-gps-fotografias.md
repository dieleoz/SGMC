# PRUEBA-007 — Pruebas de aceptación de ESPEC-007

**Sin fixture.** `FOT_Fotografias` está en cero filas (`ESPEC-007` §2.3) y ninguna regla la lee
(`ESPEC-007` §2.2): no hay ningún flujo que ejercitar con datos, así que crear filas de prueba
gastaría la ventana barata de las ocho tablas de movimiento sin comprobar nada que una fila no
ejercitaría. Todas las pruebas de esta tanda son estructurales.

**Nada de lo que sigue se aplicó al repositorio real, al Sheets ni al editor.** Los comandos
marcados «predicho sobre copia» se corrieron contra una copia de `scripts/` y de
`BD/Modelo_Datos_PLANTILLA.xlsx` fuera del repositorio, con la edición de `ESPEC-007` §4 aplicada
solo ahí — mismo método que `PRUEBA-004` y `PRUEBA-005` usaron para predecir sin tocar el
original. La copia se borró después de leerla.

> **Cuánto vale cada salida citada, dicho sin adornos.** La cabecera anterior decía que «su salida
> se cita literalmente», y en `P-64` y `P-65` **no era cierto**: el motivo que emiten los
> generadores es el texto largo de §4 completo, no el resumen citado, y los números de línea
> dependen de dónde se inserte la entrada en `CAMPOS_RETIRADOS` —al principio dan 70 y 1221; al
> final, 146 y 1221; la prueba decía 95 y 1199—. Esas dos salidas son **paráfrasis**, y así quedan
> marcadas en su propio apartado. Las demás sí son literales.
>
> Se corrige en vez de re-correrse porque el número de línea **no es lo que la prueba comprueba**:
> comprobar una posición exacta la haría fallar por reordenar una lista, que es ruido. Lo que se
> comprueba es que la entrada exista y que el documento deje de citar la función.

| | |
|---|---|
| Cubre | [`ESPEC-007-precision-gps-fotografias.md`](ESPEC-007-precision-gps-fotografias.md): retirar `FOT_Fotografias.PrecisionGPS` y declararla en `CAMPOS_RETIRADOS` |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Confirmado con `python scripts/sistema.py` |
| Reglas que esta tanda prueba | Ninguna: `ESPEC-007` §2.2 verificó que ninguna regla toca `FOT_Fotografias`. Lo que se prueba es que el modelo queda consistente y que los generadores dejan de emitir la instrucción imposible |
| Innegociables | `P-63`, `P-64` |

## P-63 — El modelo queda con 209 columnas y sin errores (innegociable)

**Predicho sobre copia**, con la edición de `ESPEC-007` §4 aplicada:

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 21
Tablas retiradas: 5  |  Campos retirados de MAN: 14
------------------------------------------------------------------------------
ERRORES: ninguno

AVISOS (3) - revisar, no bloquean:
  - [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  - [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  - [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
==============================================================================
APTO PARA DESPLEGAR
```

**Pasa si:** `Columnas: 209` (baja de 210, §1 de abajo), `ERRORES: ninguno` —en particular, sin
`V-12`, que dispararía si `PrecisionGPS` quedara en `CAMPOS_RETIRADOS` y también viva en `MODELO`—, y
los tres avisos son exactamente los tres que ya existían antes de este cambio (ninguno nuevo).

## P-64 — Los tres documentos que citaban la fórmula dejan de citarla, sin editarlos (innegociable)

**Salida paráfrasis, no literal** (ver la nota de cabecera): se cita el sentido, no el texto exacto ni el número de línea.

**Predicho sobre copia**, regenerando los tres con los comandos de siempre:

```
$ grep -n "PrecisionGPS" docs/ARQUITECTURA_OBJETIVO_SGMC.md
95:| `PrecisionGPS` | USERLOCATIONACCURACY() no existe en AppSheet. Retirada por ESPEC-007. |

$ grep -n "PrecisionGPS" docs/MANUAL_DESPLIEGUE.md
1199:| `PrecisionGPS` | **OCULTAR** | USERLOCATIONACCURACY() no existe en AppSheet. Retirada por ESPEC-007. |

$ grep -n "PrecisionGPS" docs/PROMPT_CABLEADO.md
(sin resultado)
```

**Pasa si:** ninguna de las tres salidas contiene `USERLOCATIONACCURACY()` junto a
`Initial value`/`Valor inicial` — la única aparición aceptable es dentro de la frase fija "no existe
en AppSheet. Retirada por..." que viene del texto de `CAMPOS_RETIRADOS`, no de una instrucción de
cablear. `PROMPT_CABLEADO.md` no debe mencionar la columna en absoluto, porque solo lista columnas
vivas con expresión pendiente.

## P-65 — `bd.md` marca la columna como retirada, sin ambigüedad con lo que hay en la hoja física

**Salida paráfrasis, no literal** (ver la nota de cabecera): se cita el sentido, no el texto exacto ni el número de línea.

**Predicho sobre copia**, con el `.xlsx` real copiado aparte (la hoja física todavía trae 8
columnas: retirar del modelo no borra la columna de la hoja, `ESPEC-007` §2.7):

```
$ python scripts/generar_diccionario_bd.py "BD/Modelo_Datos_PLANTILLA.xlsx"
...
| 6 | `PrecisionGPS` | — | **Retirada.** USERLOCATIONACCURACY() no existe en AppSheet. Retirada por ESPEC-007. |
```

**Pasa si:** la fila aparece marcada `Retirada` con el motivo, y no como una columna con `Tipo
objetivo` en blanco sin explicación — que sería indistinguible de una columna sin decidir.

## P-66 — `docs/TIPOS_ESPERADOS.md` deja de mencionar la columna

**Se mide sobre el DOCUMENTO, no sobre la salida del generador.** La versión anterior de esta
prueba hacía `grep` sobre el *stdout* de `generar_tipos_esperados.py`, que solo imprime `Generado:
...` y un resumen: **nunca contiene un nombre de columna**, así que daba `0` tanto con el cambio como
sin él. **No podía fallar**, y una prueba que no puede fallar no prueba nada — ocupa el sitio de la
que sí comprobaría.

```
$ grep -c PrecisionGPS docs/TIPOS_ESPERADOS.md
```

**Pasa si:** devuelve **`2` antes** de aplicar y **`0` después**. Se demuestra corriendo las dos, no
una. La columna deriva de `MODELO` en tiempo de ejecución (`ESPEC-007` §2.6); si sigue apareciendo
después, algo quedó hardcodeado y hay que investigarlo antes de cerrar esta tanda.

## P-67 — Ningún script sigue citando la columna por nombre, fuera de `modelo_objetivo.py`

**Predicho sobre copia**, tras aplicar `ESPEC-007` §4:

```
$ grep -rn "PrecisionGPS" scripts/*.py
scripts/modelo_objetivo.py:<línea de CAMPOS_RETIRADOS>: "PrecisionGPS": ("USERLOCATIONACCURACY..."
```

**Pasa si:** la única coincidencia es la entrada de `CAMPOS_RETIRADOS` en `scripts/modelo_objetivo.py`
— ninguna declaración de columna viva, y ningún otro script.

## Lo que esta tanda NO prueba, y por qué

- **No prueba que `FOT_Fotografias` en el editor de AppSheet quede sin la columna.** Eso depende de
  cuál rama de `ESPEC-007` §2.7 aplique, y ninguna de las dos se puede confirmar sin sesión de
  navegador. Se deja como dependencia de ejecución en `ESPEC-007` §6, con la comprobación de cinco
  minutos que hace falta antes de dar esto por cerrado.
- **No prueba ningún flujo con datos.** No hay fixture: no hay ninguna regla ni ningún flujo que una
  fila de `FOT_Fotografias` ejercite de forma distinta con o sin esta columna (`ESPEC-007` §2.2).
- **No repite las pruebas de `PRUEBA-004`.** `MAN_Mantenimientos.Precision_GPS` es una columna
  distinta, ya cubierta por esa tanda.

## 1. Estado de partida, para que `P-63` tenga con qué compararse

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 21
Tablas retiradas: 5  |  Campos retirados de MAN: 14
------------------------------------------------------------------------------
ERRORES: ninguno

AVISOS (3) - revisar, no bloquean: [V-06] x2, [V-14]
==============================================================================
APTO PARA DESPLEGAR
```

Corrido contra el repositorio real, hoy, sin ningún cambio de `ESPEC-007` aplicado. `Columnas: 210`
es la cifra que `P-63` tiene que bajar a `209`.

## P-68 — La hoja queda limpia, no en estado mixto (innegociable)

Esta prueba existe porque **la tanda anterior no la tenía y el arquitecto encontró lo que dejaba
pasar**: retirar la columna de `MODELO` sin regenerar la plantilla deja el archivo con la cabecera
física todavía puesta, y `verificar_faseA.py` lo detecta como el estado que su propio comentario
declara el malo.

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

**Pasa si:** termina en **`AVISOS (2)`** —los dos preexistentes, `F-01` y `F-04`— y trae la línea:

```
ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya
```

**Cómo se distingue el fallo, y es concreto:** si se omite
`python scripts/generar_plantilla.py "BD/Modelo_Datos_PLANTILLA.xlsx"` de la re-emisión de §4, sale
**`AVISOS (4)`** con estas dos de más:

```
[F-03] FOT_Fotografias conserva 1 columnas marcadas como retiradas: PrecisionGPS
[F-19] ESTADO MIXTO: ... quedan 1 en la hoja y 49 ya no estan
```

**Esta prueba falla de verdad**, y falla exactamente por la omisión que la motiva. Es la diferencia
entre una prueba y una afirmación.
