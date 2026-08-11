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

## 4. La lectura de vuelta — acta cerrada

```
antes-de-la-ventana  ->  despues-de-la-ventana
NINGUNA CELDA CAMBIO.
```

Cotejar los tipos no escribió en los datos. Importaba comprobarlo: en este proyecto una conversión a
`Enum` ya reescribió una celda añadiéndole un espacio al final.

```
0 correcciones en el editor
De las 39 referencias declaradas:
     4 VERIFICADAS · 29 compatibles no atribuidas · 6 NO SE PUEDEN JUZGAR
```

### Las seis siguen sin poder juzgarse, y el propio auditor lo dice mejor que nadie

La sesión que hizo el cotejo concluyó que *«las 6 referencias que no se pueden juzgar son
exactamente las que acabamos de revisar a ojo, así que estamos cubiertos al 100%»*. **El auditor
advierte literalmente de lo contrario, en su propia salida:**

```
Las 6 se miraron en el editor. Eso NO las vuelve verificadas: una
lectura visual no es una medicion, y por eso se guarda con fecha.
Para MEDIRLAS: sembrar una fila en la tabla destino y volver a correr.
```

La distinción no es pedantería: **mirada** y **verificada** son dos niveles distintos de confianza,
y el registro guarda la fecha y el nombre precisamente porque una lectura visual caduca y una
medición no. Este cotejo **renueva** esas seis lecturas al 2026-08-11 y añade lo que faltaba
—`MAN_Mantenimientos.OTID` es `Ref` y sin `Is a part of`—, pero **no las convierte en medidas**.

Medirlas cuesta exactamente lo que cuesta cerrar la ventana barata: sembrar una fila en la tabla
destino. Es la decisión que sigue siendo del usuario.
