# ACTA-009 — El cableado de `RG-37`, `RG-38` y los dos bots

Sesión de editor del 2026-08-11, con `Ctrl+Shift+R` previo. Cuatro encargos, los cuatro ejecutados.
**Ninguna celda cambió** y ninguna de las ocho tablas de movimiento ganó una fila: la ventana barata
sigue abierta.

Se transcribe todo aunque coincida con lo esperado. **No hay comando que lo recupere**: la API v2
devuelve filas, no esquema.

---

## 1. `MAN_Mantenimientos.CierreConExcepcion` — la `App formula` fuera

Traía esto, que es `RG-19`, retirada del modelo por `ORDEN-004`:

```
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

**Borrada.** Confirmado tras recarga en duro: el campo sigue en blanco, la columna sigue `Yes/No`, la
app carga sin error.

**Con esto el defecto que motivó `ESPEC-004` queda cerrado en el editor.** Mientras esa fórmula
estuviera, la columna se autocalculaba y una `App formula` gana sobre `Editable?`: el técnico **no
podía** marcar la casilla. Y como `Precision_GPS` está siempre vacía, daba `FALSE` siempre, así que
el motivo de excepción no se pedía nunca. Ahora la casilla es del técnico.

### La discrepancia entre dos sesiones, resuelta

`ACTA-004` §7 dejó anotado que dos sesiones leyeron cosas distintas sobre `MotivoExcepcion`. Se
miraron **los dos campos a la vez**:

| Campo | Lo que hay |
|---|---|
| `Require?` (`Required_If`) | `[CierreConExcepcion] = TRUE` |
| `Valid If` | **vacío** |

Está en `Required_If`, que es donde `RG-03` la quiere. La lectura que dijo `Valid_If` era errónea. No
se movió nada.

## 2. `RG-37` — la columna virtual `EstaVencida`

Creada sobre `OT_OrdenesTrabajo`:

```
AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())
```

`Show?` **activo**. `Label` **sin marcar** — la tabla conserva `Etiqueta` como su único `Label`. Tipo
inferido: `Yes/No`.

Reemplaza al bot programado `RG-08`, que no se ejecutaba nunca. Es **solo lectura**: no escribe, no
mueve el estado, y el técnico que llega tarde sigue pudiendo cerrar la orden — que era el defecto del
bot al que sustituye.

## 3. `RG-38` — la vista y la acción

**Slice `Vence en 7 dias`** sobre `PLA_PlanMantenimiento`:

```
AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)
```

**Acción `Generar Orden desde Plan`**, tipo `Data: add a new row to another table using values from
this row`, destino `OT_OrdenesTrabajo`. El mapeo tal como quedó:

| Columna de `OT_OrdenesTrabajo` | Valor |
|---|---|
| `ActivoID` | `[ActivoID]` |
| `TecnicoID` | `[ResponsableID]` |
| `SupervisorID` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `Tipo` | `"Preventivo"` |
| `FechaProgramada` | `[ProximaFecha]` |
| `EstadoOrdenID` | `"Programada"` |

`OTID` no se mapeó: conserva su `Initial value = UNIQUEID()`. `OTOrigenID`, `Observaciones`,
`FechaCierre` y `CerradaPor` quedaron en blanco.

**`ESPEC-006` §3.3 dejaba abierto si haría falta un `TEXT()` para pasar de `Date` a `DateTime`.** No
hizo falta: AppSheet validó en verde, sin error ni advertencia en ningún punto. Supuesto cerrado.

## 4. Los dos bots — creados, y los dos incompletos por el mismo motivo

`Automation > Bots` estaba **vacío**. Ahora tiene dos. Los dos quedaron a medias, y **no por un fallo
de la sesión sino porque el modelo no declara lo que AppSheet exige**.

| | `RG-06` | `RG-10` |
|---|---|---|
| Tabla | `MAN_Mantenimientos` | `MAN_Mantenimientos` |
| Evento | `Adds` + `Updates` | `Adds` + `Updates` |
| Condición | `[EstadoActivoID].[GeneraAlerta] = TRUE` | `[RequiereSegundaVisita] = TRUE` |
| Qué falta | **los destinatarios** | **el mapeo de columnas** |

`Deletes` quedó deshabilitado solo en los dos, con el mensaje `Table does not have Deletes
permission` — que es `RG-15` funcionando.

**Lo que AppSheet pidió, literal, sobre `RG-10`:**

```
The data action 'Crear orden de seguimiento Action - 1' does not define a column to set
```

Ninguno de los dos se completó a ojo, y está bien que no. `RG-06` dice *«Envia correo con informe PDF
al CCO y al supervisor»* y el modelo **no dice quién es el CCO** ni con qué expresión se resuelve el
supervisor. `RG-10` dice *«Genera una orden de seguimiento enlazada mediante `OTOrigenID`»* y el
modelo **no trae el mapeo**, a diferencia de `RG-38`, cuyo `ESPEC-006` §3.3 lo fija columna por
columna. Inventarlos habría sido decidir por operación en una pantalla.

Los dos quedan en `docs/HALLAZGOS_ABIERTOS.md`.

## 5. El aviso que invalida una precaución de todo el proyecto

Al guardar `RG-06`:

```
The account is free. All emails are therefore being sent to the app creator.
This email should have gone To 'dieleoz@gmail.com' CC'ed to '' and BCC'ed to ''
```

**En esta cuenta ningún correo de bot puede llegar a una dirección corporativa.** `PRUEBA-005` §1.5 y
`PRUEBA-006` fijaban como precondición común desactivar `RG-07` antes de cualquier fixture, porque
*«dispara hasta 3 correos reales a `ivan.salcedo@concesiondelsisga.com.co`»*. Ese riesgo no existe
mientras el plan sea gratuito. Desarrollado en `docs/BASE_CONOCIMIENTO_APPSHEET.md` §19, **incluido
lo que NO invalida**.

## 6. Lectura de vuelta

```
python scripts/instantanea.py comparar antes-de-cablear despues-de-cablear
-> NINGUNA CELDA CAMBIO

python scripts/auditar_cableado.py
-> 0 correcciones · 4 verificadas · 29 compatibles · 6 no se pueden juzgar
```

Las seis que no se pueden juzgar son preexistentes: su tabla destino está vacía. Ninguna tiene
relación con lo cableado hoy.

**Y la matización que corresponde**, la misma de `ACTA-004` §6: casi todo lo de esta sesión es
metadato de esquema, y un contraste de filas no lo ve **por construcción**. El verde aquí prueba que
no se escribió en los datos, no que la configuración sea correcta. Eso lo prueba la transcripción de
arriba, y nada más.
