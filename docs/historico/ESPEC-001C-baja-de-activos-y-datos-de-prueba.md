> # Documento historico. NO SE APLICA.
>
> Última pasada a mano sobre el Sheets de la aplicación `SGMC-886843353`: baja de activos, doctrina
> de reportes históricos y poblado de prueba. **Se ejecutó y se cerró** el 2026-08-07 (`ACTA-002`).
> Esa aplicación se abandonó el 2026-08-09 y **la hoja ya no se prepara a mano: se genera del
> modelo**, con `scripts/generar_hoja_limpia.py`.
>
> Lo que decidió sigue vivo, pero **en el modelo, no aquí**: `FechaBaja` y `MotivoBaja` en
> `ACT_Activos`, y las reglas RG-16, RG-17 y RG-18 en `scripts/modelo_objetivo.py`. La lista de
> expresiones vigente es [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](../sdd/RECONSTRUCCION_EXPRESIONES.md).
>
> Se conserva por trazabilidad: explica por qué se decidió lo que hay hoy.
> **El estado vigente está en [`ESTADO.md`](../../ESTADO.md).**

# ESPEC-001C — Baja de activos y poblado completo de prueba

Última pasada sobre la hoja antes de la Fase B. Deja el Sheets **completo y ejercitable**: con el
ciclo de baja de activos modelado y con datos de prueba en todas las tablas del ciclo, de modo que
la Fase B se pueda verificar de extremo a extremo sin esperar al levantamiento de campo.

| | |
|---|---|
| Dónde se aplica | Google Sheets de producción, `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc` |
| Precede | `ESPEC-001` y `ESPEC-001B`, cerradas y verificadas (`ACTA-001`) |
| Verificación | `python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"` |
| Respaldo | `SGMC_backup_2026-08-07_antes_cableado_FaseA` |

---

## 1. El huérfano que queda de la Fase A

`CHK_Checklists.d02d8a3d` tiene **`MantenimientoID = 'OT-0001'`**.

La columna se renombró de `OTID` a `MantenimientoID`, pero **el valor sigue siendo el de una orden
de trabajo**. Renombrar un encabezado no cambia lo que el dato significa. Al convertirla a `Ref`
contra `MAN_Mantenimientos` —que tiene 0 filas— esa fila queda huérfana en silencio.

Es el mismo defecto que `OTID` lleva meses causando, en su tercera variante en tres días.

**Corrección:** borrar la fila `d02d8a3d` de `CHK_Checklists`. Es residuo del mismo ensayo que
produjo `CHK001`: tiene 1 de 15 preguntas contestadas, `Finalizado = FALSE` y ninguna evidencia
asociada. En su lugar se crea `TEST-CHK-001`, correctamente enlazada, en la sección 4.

---

## 2. Baja de activos

### 2.1 Dos columnas nuevas en `ACT_Activos`

| Columna | Tipo | Contenido |
|---|---|---|
| `FechaBaja` | Date | Cuándo se dio de baja. Vacía mientras el activo esté vigente |
| `MotivoBaja` | Enum | `Obsolescencia`, `Dano irreparable`, `Robo o vandalismo`, `Reemplazo`, `Retiro por obra` |

Sin `FechaBaja`, el histórico no puede explicar por qué un activo dejó de recibir mantenimiento, y
esa es exactamente la pregunta que hace la interventoría.

### 2.2 `Activo` deja de editarse a mano

`EST_Activo` ya tiene el estado `Retirado`, y además existe la bandera `Activo`. **Son dos formas de
decir lo mismo, y algún día se contradirán sin que nadie sepa cuál manda.**

En la Fase B, `ACT_Activos.Activo` pasa a ser una fórmula (RG-16):

```
[EstadoActivoID] <> "Retirado"
```

En la hoja la columna se queda como está. Lo que cambia es que **nadie la escribe**: se deriva.

### 2.3 La doctrina de reportes, que es lo que de verdad importa (RG-18)

> **Un reporte histórico filtra por la fecha y el estado de la TRANSACCIÓN, nunca por el estado
> actual del activo padre.**

Si un reporte histórico filtra por `[ActivoID].[Activo] = TRUE`, al dar de baja un activo
**desaparecen retroactivamente todos sus mantenimientos pasados**. El informe del año anterior
cambia solo, un año después, y muestra menos trabajo del que se hizo.

Ante interventoría eso no parece un filtro mal puesto: **parece que el mantenimiento nunca se
ejecutó**.

| Tipo de reporte | ¿Sale el activo dado de baja? |
|---|---|
| Operativos: pendientes, programadas, inventario, disponibilidad del mes | No |
| Históricos: ejecutados en 2025, evidencias, cumplimiento del año pasado | **Sí, obligatoriamente** |

### 2.4 Escenario de prueba de la baja

Retirar **`ActivoID = 34`** (`SUBE-001`, Subestación Eléctrica 001). Se elige porque **no tiene
ninguna orden de trabajo asociada**, así que la prueba no altera nada existente.

| Columna | Valor |
|---|---|
| `EstadoActivoID` | `4` (Retirado) |
| `FechaBaja` | `2026-08-07` |
| `MotivoBaja` | `Obsolescencia` |

Reversible con una celda: devolver `EstadoActivoID` a `1`.

---

## 3. Columnas que faltan para que el ciclo funcione

`verificar_faseA.py` las señala. Las de `FOT_Fotografias` no son higiene: **son la cadena de
evidencia**, y sin ellas el sistema no cumple su propósito.

| Tabla | Columnas a añadir |
|---|---|
| `ACT_Activos` | `Criticidad`, `FechaBaja`, `MotivoBaja` |
| `OT_OrdenesTrabajo` | `Tipo` |
| `FOT_Fotografias` | `Tipo`, `Ubicacion`, `PrecisionGPS`, `FechaHora` |
| `FIR_Firmas` | `FechaHora` |
| `FRM_Preguntas` | `Version` |
| `CAL_Calzadas`, `SEN_Sentidos`, `TPR_TiposRespuesta` | `Activo` |
| `FAL_ModosFalla` | `TipoActivoID`, `Componente`, `Criticidad`, `Activo` |
| `NOV_Novedades` | `UsuarioID`, `Tipo`, `Descripcion`, `Ubicacion`, `Fotografia`, `ActivoID`, `Estado`, `FechaHora` |
| `PLA_PlanMantenimiento` | `PlanID`, `ActivoID`, `FrecuenciaID`, `UltimaEjecucion`, `ProximaFecha`, `ResponsableID`, `Activo` |

---

## 3.1 El formato de la coordenada: lo que NO se puede verificar todavía

Antes de escribir una sola coordenada de prueba hay que decir esto, porque es una suposición y no
un hecho.

**No existe ni una sola coordenada capturada por la aplicación en todo el sistema.** Verificado el
2026-08-07:

| Dónde podría haber una | Filas con dato |
|---|---|
| `MAN_Mantenimientos.Coordenadas_Cierre` y `UbicacionEscaneo` | 0 |
| `FOT_Fotografias.Ubicacion` | 0 |
| `GPS.Latitud` y `GPS.Longitud` | 0 |
| `CHK_Checklists.GPSInicio` y `GPSFin` | 0 |

La única coordenada del sistema es `ACT_Activos.Ubicacion`, con el valor literal
`'4.728512, -74.114531'` —cadena de texto, grados decimales, coma y espacio— repetido en los 34
activos. **La cargó una persona, no la aplicación.**

Y el modelo actual arrastra **tres representaciones distintas** de lo mismo, ninguna ejercitada:
una cadena única (`Ubicacion`), dos columnas numéricas separadas (`GPS.Latitud` y `GPS.Longitud`,
tabla que se retira) y un par más (`GPSInicio`, `GPSFin`).

### Qué se hace mientras tanto

Se usa el formato de `ACT_Activos.Ubicacion`, **y no por costumbre**: `DISTANCE()` tiene que
comparar `Coordenadas_Cierre` contra `Ubicacion`, así que necesariamente comparten formato. Es la
evidencia más fuerte disponible.

```
4.728512, -74.114531
```

**Pero queda declarado como supuesto, no como hecho.** La confirmación es el primer paso de la Fase
B, y está añadida a `ESPEC-002`: tipar la columna como `LatLong`, capturar **una** coordenada real
desde la aplicación, leer el Sheets de vuelta y comparar el literal. Si difiere —en separador,
precisión o espaciado— se reescriben las coordenadas de las filas de prueba antes de seguir.

No es un formalismo: si el formato no coincide, `DISTANCE()` no falla con un error claro. Devuelve
un resultado y la regla de geofencing parece funcionar cuando no lo hace.

## 4. Datos de prueba

**Regla dura: toda fila de prueba lleva el prefijo `TEST-` en su clave.** Se borran todas juntas
cuando dejen de hacer falta. `CHK_Checklists` ya arrastró basura de prueba que entró sin marca y
acabó siendo tarea de limpieza; esta regla existe para no fabricar la siguiente.

Las claves usadas deben ser las que ya existen: `OT-0001`, `OT-0003`, técnicos `4` y `5`,
`FRM_SOS`, preguntas `SOS001` a `SOS015`. **Escribirlas con la forma final es lo que impide que la
conversión a `Ref` de la Fase B las deje huérfanas.**

### 4.1 `MAN_Mantenimientos` — dos filas, y una debe fallar

Aquí está el truco que permite probar el geofencing **sin esperar a las coordenadas reales (D-01)**.
Los 34 activos comparten `4.728512, -74.114531`. Si una fila cierra en ese punto y otra a nueve
kilómetros, la regla RG-01 se puede validar hoy mismo: una pasa y la otra tiene que ser rechazada.

| Columna | `TEST-MTTO-001` | `TEST-MTTO-002` |
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
| `CierreConExcepcion` | `FALSE` | `TRUE` · **calculada por RG-19**: `45 > 40`. El umbral vive en `PAR_Parametros`, no en la expresión |
| `MotivoExcepcion` | vacío | `Prueba de excepcion por GPS deficiente` |
| `RequiereSegundaVisita` | `FALSE` | `TRUE` |
| `MotivoPendienteID` | vacío | `MOT-01` |
| `AprobadoSupervisor` | `TRUE` | `FALSE` |
| `Observaciones` | `Fila de prueba. Cierre dentro de rango.` | `Fila de prueba. Cierre a 9 km: RG-01 debe rechazarlo.` |
| `Activo` | `TRUE` | `TRUE` |

Las columnas retiradas —`Fecha`, `Tipo`, `Diagnostico`, `Trabajo_Realizado`, etc.— se dejan vacías.

### 4.2 `FOT_Fotografias` — tres filas

`Archivo` se deja **vacío**: una imagen no se puede poblar desde la hoja. La cadena de evidencia se
prueba con la coordenada y la hora, que sí son datos.

| `FotoID` | `MantenimientoID` | `Tipo` | `Ubicacion` | `PrecisionGPS` | `FechaHora` | `Usuario` |
|---|---|---|---|---|---|---|
| `TEST-FOT-001` | `TEST-MTTO-001` | `Antes` | `4.728512, -74.114531` | `8` | `2026-08-07 08:05:00` | `santiago.moreno@concesiondelsisga.com.co` |
| `TEST-FOT-002` | `TEST-MTTO-001` | `Despues` | `4.728512, -74.114531` | `7` | `2026-08-07 09:10:00` | `santiago.moreno@concesiondelsisga.com.co` |
| `TEST-FOT-003` | `TEST-MTTO-001` | `Novedad` | `4.728512, -74.114531` | `9` | `2026-08-07 09:12:00` | `santiago.moreno@concesiondelsisga.com.co` |

### 4.3 `FIR_Firmas` — una fila

| `FirmaID` | `MantenimientoID` | `TipoFirma` | `Imagen` | `FechaHora` |
|---|---|---|---|---|
| `TEST-FIR-001` | `TEST-MTTO-001` | `Tecnico` | vacío | `2026-08-07 09:14:00` |

### 4.4 `CHK_Checklists` — una fila

Antes: **borrar `d02d8a3d`** (sección 1).

| Columna | Valor |
|---|---|
| `ChecklistID` | `TEST-CHK-001` |
| `MantenimientoID` | `TEST-MTTO-001` |
| `FormularioID` | `FRM_SOS` |
| `VersionFormulario` | `1` |
| `FechaInicio` | `2026-08-07 08:10:00` |
| `FechaFin` | `2026-08-07 09:05:00` |
| `Finalizado` | `TRUE` |

Las 15 columnas retiradas se dejan vacías.

### 4.5 `CHD_ChecklistDetalle` — quince filas

Una por pregunta de `FRM_SOS`. Todas con `ChecklistID = TEST-CHK-001` y `Contestada = TRUE`.

| `DetalleID` | `PreguntaID` | Respuesta |
|---|---|---|
| `TEST-CHD-001` | `SOS001` | `RespuestaLista` = `Operativo` |
| `TEST-CHD-002` | `SOS002` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-003` | `SOS003` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-004` | `SOS004` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-005` | `SOS005` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-006` | `SOS006` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-007` | `SOS007` | `RespuestaNumero` = `24.5` |
| `TEST-CHD-008` | `SOS008` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-009` | `SOS009` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-010` | `SOS010` | `RespuestaBoolean` = `TRUE` |
| `TEST-CHD-011` | `SOS011` | `RespuestaBoolean` = `FALSE` |
| `TEST-CHD-012` | `SOS012` | `RespuestaTexto` = `Prueba de extremo a extremo.` |
| `TEST-CHD-013` | `SOS013` | `Contestada` = `TRUE`, resto vacío |
| `TEST-CHD-014` | `SOS014` | `Contestada` = `TRUE`, resto vacío |
| `TEST-CHD-015` | `SOS015` | `Contestada` = `FALSE` |

`SOS007` con `24.5` está dentro del rango declarado en `FRM_Preguntas` (10 a 30 V). Sirve para
comprobar que la validación por rango no rechaza un valor legítimo.

### 4.6 `FAL_ModosFalla` — cinco filas, sin prefijo

Es un catálogo, no una transacción: se queda.

| `ModoFallaID` | `TipoActivoID` | `Nombre` | `Componente` | `Criticidad` |
|---|---|---|---|---|
| `FAL-01` | `1` | `Bateria descargada` | `Banco de baterias` | `Alta` |
| `FAL-02` | `1` | `Auricular dañado` | `Auricular` | `Media` |
| `FAL-03` | `2` | `Lente sucio u obstruido` | `Lente` | `Media` |
| `FAL-04` | `2` | `Perdida de comunicacion` | `Enlace` | `Alta` |
| `FAL-05` | `3` | `Modulo LED apagado` | `Panel LED` | `Alta` |

### 4.7 `PLA_PlanMantenimiento` — tres filas, sin prefijo

| `PlanID` | `ActivoID` | `FrecuenciaID` | `UltimaEjecucion` | `ProximaFecha` | `ResponsableID` |
|---|---|---|---|---|---|
| `PLA-001` | `1` | `4` | `2026-07-15` | `2026-08-14` | `4` |
| `PLA-002` | `2` | `4` | `2026-07-20` | `2026-08-19` | `4` |
| `PLA-003` | `4` | `6` | `2026-06-01` | `2026-08-30` | `5` |

### 4.8 `NOV_Novedades` — una fila

| `NovedadID` | `UsuarioID` | `Tipo` | `Descripcion` | `Ubicacion` | `ActivoID` | `Estado` | `FechaHora` |
|---|---|---|---|---|---|---|---|
| `TEST-NOV-001` | `4` | `Falla detectada` | `Poste con gabinete forzado. Fila de prueba.` | `4.728512, -74.114531` | `2` | `Reportada` | `2026-08-07 09:20:00` |

### 4.9 `LST_ValoresLista` — corregir los valores existentes

Sus 4 filas guardan en `PreguntaID` el **texto** `Estado encontrado`, no una clave. Convertirla a
`Ref` en la Fase B las dejaría huérfanas a las cuatro.

**Poner `PreguntaID = SOS001`** en las cuatro filas. `SOS001` es «Estado encontrado», la única de
tipo Lista (`TipoRespuestaID = 2`).

---

## 5. Criterio de cierre

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir **`FASE A CERRADA`** con 0 fallos, incluidas las comprobaciones nuevas de que
`CHK_Checklists.MantenimientoID`, `CHD_ChecklistDetalle.ChecklistID`, `FOT_Fotografias` y
`FIR_Firmas` resuelven contra sus padres.

Para reverificar: *Archivo → Descargar → Microsoft Excel*, guardar en `BD/` y correr el comando.

## 6. Cómo se borra todo esto después

Filtrar por el prefijo `TEST-` en la primera columna y borrar las filas de `MAN_Mantenimientos`,
`FOT_Fotografias`, `FIR_Firmas`, `CHK_Checklists`, `CHD_ChecklistDetalle` y `NOV_Novedades`.
En ese orden: primero los hijos, después los padres.

Los catálogos `FAL_ModosFalla` y `PLA_PlanMantenimiento` **no se borran**: son datos reales, no
pruebas. Y `ActivoID = 34` vuelve a `EstadoActivoID = 1` si se quiere revertir la baja.
