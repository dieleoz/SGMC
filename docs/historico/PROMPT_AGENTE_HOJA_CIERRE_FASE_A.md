> # Documento historico. NO SE APLICA.
>
> Cierre de la Fase A. **Ejecutado**, `ACTA-003`.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# Prompt para el agente de la hoja — cierre definitivo de la Fase A

Autocontenido. Cópialo íntegro desde la línea siguiente.

Reúne **las cuatro ediciones que quedan** sobre el Google Sheets. Se hacen todas en una sola pasada
porque después no se vuelve a tocar la hoja: lo siguiente es configurar AppSheet.

---

Vas a hacer cuatro cambios en el Google Sheets del SGMC. Son los últimos antes de configurar la
aplicación.

## Reglas de trabajo

- **No borres ninguna fila ni ninguna columna.** Solo se añade una pestaña y se rellenan celdas.
- **No cambies `Precision_GPS` de `TEST-MTTO-002`.** Vale `45` y **está bien**. Si en algún
  documento antiguo viste un `65`, está desactualizado.
- Encabezados **sin tildes y sin espacios**, con las mayúsculas exactas.
- Si algo no coincide con lo que dice este documento, **para y dilo** antes de aplicarlo.

---

## 1. Pestaña nueva: `PAR_Parametros`

Varias reglas de la aplicación dependen de umbrales numéricos. Si esos números van escritos dentro
de las expresiones, **no se pueden calibrar**: hay que abrir el editor de AppSheet, encontrarlos y
arriesgarse a romper la regla. En una tabla son una celda que el administrador ajusta tras las
pruebas de campo.

Crea una pestaña llamada exactamente **`PAR_Parametros`**, con estos encabezados en la fila 1:

```
ParametroID    Nombre    Valor    Unidad    Descripcion    Activo
```

Y estas tres filas:

| `ParametroID` | `Nombre` | `Valor` | `Unidad` | `Descripcion` | `Activo` |
|---|---|---|---|---|---|
| `UMBRAL_GPS` | Umbral de GPS deficiente | `40` | `m` | Error del satélite por encima del cual el cierre se marca como excepcional. Un móvil es preciso a unos 5 m a cielo abierto; 40 deja margen para montaña y estructuras | `TRUE` |
| `RADIO_GEOFENCING_KM` | Radio de geofencing provisional | `1.0` | `km` | Distancia máxima al activo para poder cerrar, mientras no se defina un radio por tipo de activo | `TRUE` |
| `DISTANCIA_ESCANEO_CIERRE_KM` | Distancia máxima entre escaneo y cierre | `0.5` | `km` | Si el técnico escaneó en un punto y cerró en otro más lejano, se señala en el reporte. No bloquea | `TRUE` |

**`Valor` tiene que quedar como número, no como texto.** Si la celda sale alineada a la izquierda,
Google la está tratando como texto y las reglas no podrán compararla.

## 2. `OT_OrdenesTrabajo.Activo` — poner `TRUE` en las 6 filas

Esa columna está **vacía en las seis órdenes**. En la aplicación se va a tipar como `Yes/No`, y
**AppSheet lee un blanco como falso**: las seis órdenes quedarían marcadas como inactivas.

Además, la aplicación va a perder el botón de borrar —el histórico no se borra, se desactiva— y
`Activo = FALSE` pasa a ser la única vía de anular una orden. Sin poblar esta columna, se quitaría
el borrado sin que exista el sustituto.

Poner **`TRUE`** en las 6 filas.

## 3. `EST_Activo.Activo` — poner `TRUE` en las 4 filas

Mismo caso: está vacía en las cuatro. Y es el catálogo de estados del que dependen las reglas de
baja de activos, así que un desplegable vacío ahí las deja sin funcionar.

Poner **`TRUE`** en las 4 filas.

## 4. `ACT_Activos` fila 34 — poner `Activo` en `FALSE`

El activo `34` (`SUBE-001`) está **`Retirado`**: tiene `EstadoActivoID = 4` y `FechaBaja`. Pero su
columna `Activo` dice `TRUE`, así que la fila se contradice consigo misma.

En la aplicación, esa columna pasará a calcularse sola desde el estado. Mientras tanto, la hoja debe
decir lo mismo que dirá la fórmula.

Poner **`FALSE`** en `Activo` de la fila cuyo `ActivoID` es `34`. **No toques su `EstadoActivoID` ni
su `FechaBaja`**, ni ninguna otra fila de esa tabla: las otras 33 se quedan en `TRUE`.

---

## Cuando termines

Descarga el libro —*Archivo → Descargar → Microsoft Excel*—, guárdalo en la carpeta `BD/` del
proyecto y avisa con el nombre del archivo. Se verifica con:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir **`FASE A CERRADA`** con 0 fallos.

**No lo des por cerrado tú.** En las tandas anteriores se reportó como cerrado y la verificación
encontró 19 fallos la primera vez y 23 la segunda. No es reproche: una hoja de 32 pestañas no se
puede autoverificar de memoria. Deja que lo diga el script.
