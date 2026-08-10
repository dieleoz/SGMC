> # Documento historico. NO SE APLICA.
>
> Baja de activos y datos de prueba. **Ejecutado**, `ACTA-003`.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# Prompt para el agente que trabaja sobre la hoja — ESPEC-001C

**Autocontenido a propósito.** El agente que lo recibe trabaja dentro del Google Sheets y no tiene
acceso a este repositorio, así que todos los datos van inline. Cópialo íntegro desde la línea
siguiente.

---

Vas a aplicar cambios sobre este Google Sheets. Ya aplicaste dos tandas anteriores y salieron bien.
Esta es la última antes de configurar AppSheet.

## Dos reglas que gobiernan todo lo que sigue

**AppSheet resuelve las columnas por nombre literal**, y una referencia guarda **el valor de la
clave de la tabla destino**. De ahí:

**1. Cuando crees un catálogo, su clave debe ser el valor que los datos existentes ya guardan.** No
un identificador nuevo y ordenado.

> En la tanda anterior se creó `EOT_EstadosOrden` con claves `1..7` mientras
> `OT_OrdenesTrabajo.EstadoOrdenID` guardaba `Asignada`, `Cerrada` y `Suspendida`. Se veía impecable
> y habría dejado las 6 órdenes huérfanas al cablear. Hubo que rehacerlo.

**2. Renombrar un encabezado no cambia lo que el dato significa.**

> `CHK_Checklists.OTID` se renombró a `MantenimientoID` y su fila siguió guardando `OT-0001`, que es
> una **orden**, no un mantenimiento.

**No inventes identificadores.** Usa los que ya existen: órdenes `OT-0001` a `OT-0006`, técnicos `3`
a `6`, formulario `FRM_SOS`, preguntas `SOS001` a `SOS015`, activos `1` a `34`, motivos `MOT-01` a
`MOT-05`, estados de activo `1` a `4`.

## Reglas de trabajo

- **No borres ninguna columna.** Solo se añaden, salvo el borrado de la fila indicado en el paso 1.
- **Toda fila de prueba lleva el prefijo `TEST-` en su primera columna.** Es lo que permite borrarlas
  todas juntas después. Esta hoja ya arrastró basura de prueba que entró sin marca.
- Encabezados **sin tildes y sin espacios**, con las mayúsculas exactas.
- Si algo no coincide con lo que dice este documento, **para y dilo**. No improvises: lo que
  escribas se valida después contra un modelo.

---

## Paso 1. Borrar una fila

En `CHK_Checklists`, borrar la fila con `ChecklistID = d02d8a3d`. Su `MantenimientoID` guarda
`OT-0001`, que es una orden y no un mantenimiento. Se sustituye en el paso 5.

## Paso 2. Añadir columnas

Al final de cada hoja, respetando el nombre exacto:

| Hoja | Columnas a añadir |
|---|---|
| `ACT_Activos` | `Criticidad`, `FechaBaja`, `MotivoBaja` |
| `OT_OrdenesTrabajo` | `Tipo` |
| `FOT_Fotografias` | `Tipo`, `Ubicacion`, `PrecisionGPS`, `FechaHora` |
| `FIR_Firmas` | `FechaHora` |
| `FRM_Preguntas` | `Version` |
| `CAL_Calzadas` | `Activo` |
| `SEN_Sentidos` | `Activo` |
| `TPR_TiposRespuesta` | `Activo` |
| `FAL_ModosFalla` | `TipoActivoID`, `Componente`, `Criticidad`, `Activo` |
| `NOV_Novedades` | `UsuarioID`, `Tipo`, `Descripcion`, `Ubicacion`, `Fotografia`, `ActivoID`, `Estado`, `FechaHora` |
| `PLA_PlanMantenimiento` | `PlanID`, `ActivoID`, `FrecuenciaID`, `UltimaEjecucion`, `ProximaFecha`, `ResponsableID`, `Activo` |

Las cuatro de `FOT_Fotografias` son la cadena de evidencia del sistema, no higiene: sin coordenada y
hora por fotografía no hay prueba de que alguien estuvo donde dice.

En `CAL_Calzadas`, `SEN_Sentidos` y `TPR_TiposRespuesta`, poner `Activo = TRUE` en todas las filas
existentes.

## Paso 3. Baja del activo 34

En `ACT_Activos`, fila con `ActivoID = 34` (`SUBE-001`):

| Columna | Valor |
|---|---|
| `EstadoActivoID` | `4` |
| `FechaBaja` | `2026-08-07` |
| `MotivoBaja` | `Obsolescencia` |

Se elige el 34 porque no tiene ninguna orden asociada. Es un escenario de prueba del ciclo de baja.

## Paso 4. Corregir `LST_ValoresLista`

Sus 4 filas guardan en `PreguntaID` el texto `Estado encontrado`. Reemplazar ese texto por la clave
**`SOS001`** en las cuatro filas.

## Paso 5. Poblar datos de prueba

### Sobre el formato de las coordenadas

Escríbelas exactamente así, igual que `ACT_Activos.Ubicacion`:

```
4.728512, -74.114531
```

Grados decimales, coma y espacio, como texto. **No lo "normalices"**: un espacio de más o de menos
puede romper la comparación de distancias.

Conviene que sepas que es un supuesto: en toda la hoja **no hay ni una sola coordenada capturada por
la aplicación**. Las cuatro columnas que podrían tenerla están vacías, y la única que existe la cargó
una persona. Se confirmará más adelante capturando una desde la app.

### `MAN_Mantenimientos` — dos filas

Las columnas no listadas se dejan vacías.

| Columna | Fila 1 | Fila 2 |
|---|---|---|
| `MantenimientoID` | `TEST-MTTO-001` | `TEST-MTTO-002` |
| `OTID` | `OT-0001` | `OT-0003` |
| `TecnicoID` | `4` | `5` |
| `FechaHoraInicio` | `2026-08-07 08:00:00` | `2026-08-07 10:30:00` |
| `FechaHoraFin` | `2026-08-07 09:15:00` | `2026-08-07 11:00:00` |
| `OrigenApertura` | `Lista` | `Lista` |
| `UbicacionEscaneo` | `4.728512, -74.114531` | `4.728512, -74.114531` |
| `FechaHoraEscaneo` | `2026-08-07 08:00:00` | `2026-08-07 10:30:00` |
| `EstadoActivoID` | `1` | `3` |
| `Coordenadas_Cierre` | `4.728512, -74.114531` | `4.650000, -74.100000` |
| `Precision_GPS` | `8` | `45` |
| `CierreConExcepcion` | `FALSE` | `TRUE` |
| `MotivoExcepcion` | *(vacío)* | `Prueba de excepcion por GPS deficiente` |
| `RequiereSegundaVisita` | `FALSE` | `TRUE` |
| `MotivoPendienteID` | *(vacío)* | `MOT-01` |
| `AprobadoSupervisor` | `TRUE` | `FALSE` |
| `Observaciones` | `Fila de prueba. Cierre dentro de rango.` | `Fila de prueba. Cierre a 9 km: debe ser rechazado.` |
| `Activo` | `TRUE` | `TRUE` |

**La segunda fila cierra a nueve kilómetros del activo, y es deliberado.** Los 34 activos comparten
la misma coordenada, así que con estas dos se puede comprobar la regla de geofencing: una tiene que
pasar y la otra tiene que ser rechazada. Sin la segunda no hay forma de distinguir «la regla
funciona» de «la regla no se aplica». **No la corrijas para que coincida.**

### `FOT_Fotografias` — tres filas

`Archivo` se deja vacío: una imagen no se puede poblar desde la hoja.

| `FotoID` | `MantenimientoID` | `Tipo` | `Ubicacion` | `PrecisionGPS` | `FechaHora` | `Usuario` |
|---|---|---|---|---|---|---|
| `TEST-FOT-001` | `TEST-MTTO-001` | `Antes` | `4.728512, -74.114531` | `8` | `2026-08-07 08:05:00` | `santiago.moreno@concesiondelsisga.com.co` |
| `TEST-FOT-002` | `TEST-MTTO-001` | `Despues` | `4.728512, -74.114531` | `7` | `2026-08-07 09:10:00` | `santiago.moreno@concesiondelsisga.com.co` |
| `TEST-FOT-003` | `TEST-MTTO-001` | `Novedad` | `4.728512, -74.114531` | `9` | `2026-08-07 09:12:00` | `santiago.moreno@concesiondelsisga.com.co` |

### `FIR_Firmas` — una fila

| `FirmaID` | `MantenimientoID` | `TipoFirma` | `Imagen` | `FechaHora` |
|---|---|---|---|---|
| `TEST-FIR-001` | `TEST-MTTO-001` | `Tecnico` | *(vacío)* | `2026-08-07 09:14:00` |

### `CHK_Checklists` — una fila

Las columnas no listadas se dejan vacías.

| Columna | Valor |
|---|---|
| `ChecklistID` | `TEST-CHK-001` |
| `MantenimientoID` | `TEST-MTTO-001` |
| `FormularioID` | `FRM_SOS` |
| `VersionFormulario` | `1` |
| `FechaInicio` | `2026-08-07 08:10:00` |
| `FechaFin` | `2026-08-07 09:05:00` |
| `Finalizado` | `TRUE` |

### `CHD_ChecklistDetalle` — quince filas

Todas con `ChecklistID = TEST-CHK-001`. `Contestada = TRUE` en todas salvo la última.

| `DetalleID` | `PreguntaID` | Columna de respuesta | Valor | `Contestada` |
|---|---|---|---|---|
| `TEST-CHD-001` | `SOS001` | `RespuestaLista` | `Operativo` | `TRUE` |
| `TEST-CHD-002` | `SOS002` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-003` | `SOS003` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-004` | `SOS004` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-005` | `SOS005` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-006` | `SOS006` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-007` | `SOS007` | `RespuestaNumero` | `24.5` | `TRUE` |
| `TEST-CHD-008` | `SOS008` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-009` | `SOS009` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-010` | `SOS010` | `RespuestaBoolean` | `TRUE` | `TRUE` |
| `TEST-CHD-011` | `SOS011` | `RespuestaBoolean` | `FALSE` | `TRUE` |
| `TEST-CHD-012` | `SOS012` | `RespuestaTexto` | `Prueba de extremo a extremo.` | `TRUE` |
| `TEST-CHD-013` | `SOS013` | *(ninguna)* | *(vacío)* | `TRUE` |
| `TEST-CHD-014` | `SOS014` | *(ninguna)* | *(vacío)* | `TRUE` |
| `TEST-CHD-015` | `SOS015` | *(ninguna)* | *(vacío)* | `FALSE` |

`SOS007` con `24.5` está dentro del rango 10 a 30 V que declara `FRM_Preguntas`. Sirve para
comprobar que un valor legítimo no se rechaza.

### `NOV_Novedades` — una fila

| `NovedadID` | `UsuarioID` | `Tipo` | `Descripcion` | `Ubicacion` | `ActivoID` | `Estado` | `FechaHora` |
|---|---|---|---|---|---|---|---|
| `TEST-NOV-001` | `4` | `Falla detectada` | `Poste con gabinete forzado. Fila de prueba.` | `4.728512, -74.114531` | `2` | `Reportada` | `2026-08-07 09:20:00` |

### `FAL_ModosFalla` — cinco filas, SIN prefijo

Es un catálogo real, no una prueba. `Activo = TRUE` en las cinco.

| `ModoFallaID` | `TipoActivoID` | `Nombre` | `Componente` | `Criticidad` |
|---|---|---|---|---|
| `FAL-01` | `1` | `Bateria descargada` | `Banco de baterias` | `Alta` |
| `FAL-02` | `1` | `Auricular danado` | `Auricular` | `Media` |
| `FAL-03` | `2` | `Lente sucio u obstruido` | `Lente` | `Media` |
| `FAL-04` | `2` | `Perdida de comunicacion` | `Enlace` | `Alta` |
| `FAL-05` | `3` | `Modulo LED apagado` | `Panel LED` | `Alta` |

### `PLA_PlanMantenimiento` — tres filas, SIN prefijo

`Activo = TRUE` en las tres.

| `PlanID` | `ActivoID` | `FrecuenciaID` | `UltimaEjecucion` | `ProximaFecha` | `ResponsableID` |
|---|---|---|---|---|---|
| `PLA-001` | `1` | `4` | `2026-07-15` | `2026-08-14` | `4` |
| `PLA-002` | `2` | `4` | `2026-07-20` | `2026-08-19` | `4` |
| `PLA-003` | `4` | `6` | `2026-06-01` | `2026-08-30` | `5` |

---

## Cuando termines

Descarga el libro: *Archivo → Descargar → Microsoft Excel*, y avisa con el nombre del archivo.

**No declares el trabajo cerrado por tu cuenta.** En las dos tandas anteriores se reportó como
cerrado y una verificación automática encontró 19 fallos la primera vez y 23 la segunda. No es
reproche: una hoja de 31 pestañas no se puede autoverificar de memoria. Deja que lo diga el script.

Si algo no cuadra con lo que dice este documento, dilo **antes** de aplicarlo.
