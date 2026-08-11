# ACTA-010 — Las ocho tablas de la ventana, cotejadas una por una

Sesión de editor del 2026-08-11. Se recorrieron las **ocho tablas de movimiento** columna por columna
contra `docs/ENCARGO_VENTANA.md`, y **las ocho salieron conformes**.

Se registra aquí porque **no hay comando que lo recupere**: la API v2 devuelve filas, no esquema. Sin
esta acta, ese trabajo no deja rastro y el siguiente que pregunte «¿están bien los tipos?» tendrá que
volver a mirarlo entero.

---

## 1. Lo que se cotejó

| Tabla | Resultado |
|---|---|
| `CHD_ChecklistDetalle` | conforme |
| `CHK_Checklists` | conforme |
| `FIR_Firmas` | conforme |
| `FOT_Fotografias` | conforme, **con `Is a part of` en `MantenimientoID`** y los tres valores de `Tipo` |
| `MAN_Mantenimientos` | conforme, 14 columnas |
| `NOV_Novedades` | conforme, `UsuarioID` **sin** `Is a part of` |
| `OT_OrdenesTrabajo` | conforme, **más la virtual `Etiqueta` con su `CONCATENATE(...)`** |
| `PLA_PlanMantenimiento` | conforme |

## 2. Los dos hallazgos que valen más que el resto

### `MAN_Mantenimientos.OTID` **es `Ref`**, y sin `Is a part of`

Era la pregunta abierta. `auditar_cableado.py` la daba como **`NO SE PUEDEN JUZGAR`** —una de las
seis— porque su tabla destino, `OT_OrdenesTrabajo`, está vacía y el método de referencias necesita
filas en el destino para atribuir.

**Ahora está confirmada a ojo**, que es la única vía que quedaba. Con eso:

- La cadena de geofencing `[OTID].[ActivoID].[Ubicacion_LatLong]` **existe de verdad en el editor**,
  no solo en el modelo. Su nota decía *«Era `Text`. Ese solo hecho impedía todo el geofencing»*.
- **`Is a part of` está sin marcar**, que es la decisión del 2026-08-07: borrar una orden **no** debe
  borrar su ejecución, porque la ejecución es el registro histórico y sobrevive a su orden.

Las referencias en `NO SE PUEDEN JUZGAR` bajan a cinco por cotejo, no por medición. Sigue sin haber
comando que lo compruebe.

### La cascada de la evidencia, confirmada en el editor

`FOT_Fotografias.MantenimientoID` **sí** tiene `Is a part of`, y `NOV_Novedades.UsuarioID` **no**. Los
dos coinciden con el modelo.

Que la primera lo tenga es lo que `docs/HALLAZGOS_ABIERTOS.md` registra: borrar un mantenimiento
borraría sus fotografías. Está neutralizado dentro de la aplicación porque `RG-15` retira `Deletes`
de `MAN_Mantenimientos` —no hay botón que borre—, y el residuo real, borrado a mano en el Sheets, no
se arregla quitando `IsPartOf`: un borrado en la hoja no dispara cascada, deja huérfanos.

## 3. Lo que este cotejo NO hace, y conviene decirlo

**No cierra la ventana barata.** La sesión que lo hizo escribió *«si esta pasa en verde, cerramos la
ventana barata para siempre»*, y es al revés:

```
cotejar          gratis, repetible, no consume nada
la primera fila  cierra la ventana PARA SIEMPRE
```

Las ocho tablas siguen en **cero filas**. La ventana sigue abierta, y corregir un tipo sigue costando
un clic. Confundir las dos cosas haría creer que ya no queda nada que perder, justo cuando es cuando
más hay.

**Y no sustituye a `inferencia.clasificar()`, ni al revés.** Ese comando seguirá diciendo que hay
columnas «a mano» después de esta acta, porque responde *qué columnas necesitan mano* y no *en cuáles
ya pasó alguien*. No es una contradicción: es que ninguna de las dos preguntas se puede contestar con
la otra.

## 4. Lo que queda pendiente de esta misma sesión

La comparación de instantáneas y el auditor, que la sesión declaró lanzados y sin salida todavía. **El
acta no está cerrada hasta que se peguen los dos.** Un cotejo sin lectura de vuelta no descarta que
alguna conversión de tipo haya escrito en los datos — ya pasó en este proyecto: una conversión a
`Enum` reescribió una celda añadiéndole un espacio al final.
