# Prompt para el agente de la hoja — pestaña `PAR_Parametros`

Autocontenido. Cópialo íntegro desde la línea siguiente. Es un cambio pequeño: una pestaña nueva
con tres filas, y **no se toca ninguna celda de las que ya existen**.

---

Vas a añadir **una pestaña nueva** al Google Sheets del SGMC. Es el único cambio: no borres nada, no
renombres nada, no modifiques ninguna fila existente.

## Por qué

Varias reglas de la aplicación dependen de umbrales numéricos —cuántos metros de error GPS se
consideran un cierre dudoso, cuántos kilómetros de radio admite el geofencing—. Hoy esos números
irían escritos dentro de las expresiones, y **un número escondido en una expresión no se puede
calibrar**: hay que abrir el editor de AppSheet, encontrarlo y arriesgarse a romper la regla.

Poniéndolos en una tabla, el administrador los ajusta **en una celda** después de las pruebas de
campo. Es lo que se pide.

## Qué hacer

Crear una pestaña llamada exactamente **`PAR_Parametros`**, con estos encabezados en la fila 1, sin
tildes y con las mayúsculas exactas:

```
ParametroID    Nombre    Valor    Unidad    Descripcion    Activo
```

Y estas tres filas:

| `ParametroID` | `Nombre` | `Valor` | `Unidad` | `Descripcion` | `Activo` |
|---|---|---|---|---|---|
| `UMBRAL_GPS` | Umbral de GPS deficiente | `40` | `m` | Error del satélite por encima del cual el cierre se marca como excepcional. Un móvil es preciso a unos 5 m a cielo abierto; 40 deja margen para montaña y estructuras | `TRUE` |
| `RADIO_GEOFENCING_KM` | Radio de geofencing provisional | `1.0` | `km` | Distancia máxima al activo para poder cerrar, mientras no se defina un radio por tipo de activo | `TRUE` |
| `DISTANCIA_ESCANEO_CIERRE_KM` | Distancia máxima entre escaneo y cierre | `0.5` | `km` | Si el técnico escaneó en un punto y cerró en otro más lejano, se señala en el reporte. No bloquea | `TRUE` |

**`Valor` tiene que quedar como número, no como texto.** Si la celda queda alineada a la izquierda,
Google la está tratando como texto y las reglas no podrán compararla.

## Lo que NO hay que hacer

- **No cambies `Precision_GPS` de `TEST-MTTO-002`.** Vale `45` y está bien: con el umbral en 40, esa
  fila queda correctamente marcada como cierre con excepción. Si en algún documento viste un `65`,
  está desactualizado.
- No toques ninguna otra pestaña.

## Cuando termines

Descarga el libro —*Archivo → Descargar → Microsoft Excel*—, guárdalo en la carpeta `BD/` del
proyecto y avisa con el nombre del archivo. Se verifica con:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir `FASE A CERRADA`. **No lo des por cerrado tú**: en las tandas anteriores se reportó
como cerrado y la verificación encontró fallos. Deja que lo diga el script.
