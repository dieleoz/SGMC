# Prompt para el agente que trabaja sobre la hoja — ESPEC-001C

Cópialo tal cual al agente que tiene acceso al Google Sheets.

---

Vas a aplicar cambios sobre el Google Sheets de producción del SGMC (Sistema de Gestión de
Mantenimiento en Campo, Concesión Transversal del Sisga). Ya aplicaste dos tandas anteriores sobre
este mismo documento y salieron bien. Esta es la última antes de configurar AppSheet.

## Contexto que necesitas para no repetir un error que ya ocurrió

**AppSheet resuelve las columnas por nombre literal**, y una referencia guarda **el valor de la
clave de la tabla destino**. De ahí salen las dos reglas que gobiernan todo lo que vas a hacer:

**1. Cuando crees un catálogo nuevo, su clave debe ser el valor que los datos existentes ya
guardan.** No un identificador nuevo y ordenado.

> En la tanda anterior se creó `EOT_EstadosOrden` con claves `1..7` mientras
> `OT_OrdenesTrabajo.EstadoOrdenID` guardaba `Asignada`, `Cerrada` y `Suspendida`. Se veía
> impecable en la hoja, y habría dejado las 6 órdenes huérfanas en cuanto se cablearan las
> referencias. Hubo que rehacerlo. `UNF_UnidadesFuncionales` se hizo bien —claves 7 a 10, las que
> ya usaba `ACT_Activos`— y por eso las 34 filas de activos siguieron resolviendo solas.

**2. Renombrar un encabezado no cambia lo que el dato significa.**

> `CHK_Checklists.OTID` se renombró a `MantenimientoID`, pero su única fila sigue guardando
> `OT-0001`, que es el identificador de una **orden**, no de un **mantenimiento**. Esa fila hay que
> borrarla, no renombrarla.

**No inventes identificadores.** Usa exactamente los que ya existen: órdenes `OT-0001` a `OT-0006`,
técnicos `3` a `6`, formulario `FRM_SOS`, preguntas `SOS001` a `SOS015`, activos `1` a `34`,
motivos `MOT-01` a `MOT-05`.

## Reglas de trabajo

- **No borres ninguna columna.** Solo se añaden columnas y filas, salvo el borrado explícito de la
  fila `d02d8a3d` que se indica abajo.
- **Toda fila de prueba lleva el prefijo `TEST-` en su primera columna.** Sin excepción: es lo que
  permite borrarlas todas juntas después. Este documento ya arrastró basura de prueba que entró sin
  marca y acabó siendo una tarea de limpieza.
- Los encabezados van **sin tildes y sin espacios**, con las mayúsculas exactas.
- Si un encabezado o un valor no coincide con lo que describe la especificación, **para y dilo**.
  No improvises: el modelo se valida automáticamente contra lo que escribas.

## Qué tienes que hacer

Está todo detallado, tabla por tabla y celda por celda, en el documento
**`docs/sdd/ESPEC-001C-baja-de-activos-y-datos-de-prueba.md`** del repositorio. Son cinco bloques:

1. **Borrar la fila `d02d8a3d`** de `CHK_Checklists`. Su `MantenimientoID` guarda `OT-0001`, que es
   una orden, no un mantenimiento.
2. **Añadir columnas que faltan** en 9 tablas. Las cuatro de `FOT_Fotografias` —`Tipo`,
   `Ubicacion`, `PrecisionGPS`, `FechaHora`— son la cadena de evidencia del sistema, no higiene.
3. **Baja de activos:** añadir `FechaBaja` y `MotivoBaja` a `ACT_Activos`, y retirar el activo
   `34` (`SUBE-001`) como escenario de prueba. Se elige ese porque no tiene ninguna orden asociada.
4. **Poblar los datos de prueba** en `MAN_Mantenimientos` (2), `FOT_Fotografias` (3),
   `FIR_Firmas` (1), `CHK_Checklists` (1), `CHD_ChecklistDetalle` (15) y `NOV_Novedades` (1); más
   los catálogos `FAL_ModosFalla` (5) y `PLA_PlanMantenimiento` (3), que van **sin** prefijo porque
   son datos reales.
5. **Corregir `LST_ValoresLista`:** sus 4 filas guardan en `PreguntaID` el texto
   `Estado encontrado` en lugar de una clave. Poner `SOS001` en las cuatro.

## Sobre las coordenadas: es un supuesto, no un hecho

Escribe las coordenadas exactamente en este formato, el mismo de `ACT_Activos.Ubicacion`:

```
4.728512, -74.114531
```

Grados decimales, coma y espacio, como texto. **No lo cambies ni lo "normalices"**: quítale o
añádele un espacio y `DISTANCE()` puede dejar de comparar bien.

Conviene que sepas por qué es un supuesto: **en todo el sistema no hay ni una sola coordenada
capturada por la aplicación.** Las cuatro columnas que podrían tenerla están vacías. La única que
existe la cargó una persona. Se confirmará capturando una coordenada real desde la app en la fase
siguiente, y si el formato difiere habrá que reescribir estas filas. No es culpa tuya si pasa.

## Un detalle que no es un descuido

En `MAN_Mantenimientos`, la fila `TEST-MTTO-001` cierra en `4.728512, -74.114531` y la fila
`TEST-MTTO-002` cierra en `4.650000, -74.100000`, a unos nueve kilómetros.

**Es deliberado.** Los 34 activos comparten la primera coordenada, así que con estas dos filas se
puede probar la regla de geofencing de inmediato: una tiene que pasar y la otra tiene que ser
rechazada. Sin la segunda no hay forma de saber si la regla funciona o si simplemente no se aplica.

No las «corrijas» para que coincidan.

## Cuando termines

Descarga el libro —*Archivo → Descargar → Microsoft Excel*—, guárdalo en la carpeta `BD/` del
proyecto y avisa. Se verifica con:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir `FASE A CERRADA` con 0 fallos. **No declares el trabajo cerrado por tu cuenta**: en
las dos tandas anteriores se reportó como cerrado y la verificación encontró 19 fallos la primera
vez y 23 la segunda. No es reproche, es que una hoja de 31 pestañas no se puede autoverificar de
memoria. Deja que lo diga el script.

Si algo no cuadra con lo que describe la especificación, dilo antes de aplicarlo.
