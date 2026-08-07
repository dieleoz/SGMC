# ESPEC-002 — Cableado de referencias en AppSheet

Fase B. Es la que convierte el modelo en un sistema: hasta aquí hay una hoja de cálculo ordenada,
y al terminar hay referencias reales, geofencing y navegación entre tablas.

| | |
|---|---|
| Dónde se aplica | Editor de AppSheet, aplicación `SGMC-886843353` |
| Quién | Agente de navegador, o una persona. No hay API en el plan actual |
| Precede | `ESPEC-001` y **`ESPEC-001B`**, ambas cerradas |
| Estado | **BLOQUEADA.** Ver sección 1 |

---

## 1. Por qué está bloqueada ahora mismo

`python scripts/verificar_faseA.py "BD/Modelo de Datos (4).xlsx"` devuelve **19 fallos**. Dos de
ellos impiden empezar, y no por formalismo:

**`EOT_EstadosOrden` tiene claves numéricas `1..7`, y `OT_OrdenesTrabajo.EstadoOrdenID` guarda
`Asignada`, `Cerrada` y `Suspendida`.** Si se ejecuta el paso 5 de esta especificación con eso sin
corregir, las 6 órdenes quedan huérfanas y AppSheet no avisa. Se descubriría semanas después, igual
que se descubrió lo de `OTID`.

**`ASG_AsignacionZona` está vacía.** El Security Filter del paso 7 dejaría a cada técnico con cero
activos, y parecería un fallo de la regla cuando sería falta de datos.

No empieces esta fase hasta que la verificación imprima `FASE A CERRADA`.

---

## 2. La regla que gobierna toda la fase

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

De ahí las tres reglas de orden, y por eso los pasos van en el orden en que van:

1. **Primero la clave del destino, después quien la apunta.**
2. **Una conversión `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave.** Las
   demás quedan huérfanas y en silencio.
3. **Se valida en el Asistente de Expresiones, no ejercitando la aplicación.** Es más rápido, más
   barato y no depende de que haya datos.

---

## 3. Antes de tocar nada

1. **Respaldo del Sheets:** ya existe, `SGMC_backup_2026-08-07_antes_cableado_FaseA`. Si han pasado
   días, haz otro.
2. **Versión de la aplicación:** *Manage → Versions → Save a version*, con la nota
   `antes de cablear referencias`.
3. **Avisar a quien pueda editar** durante la ventana: el propietario del documento y la cuenta del
   cliente. La reversión solo es limpia si nadie más escribe.
4. **Buscar `Numero_OT` en el editor** y anotar cada vista, fórmula o acción que lo cite. Esa
   columna ya no existe: ahora se llama `OTID`, y todo lo que la citaba está roto desde la Fase A.

---

## 4. Paso 1 — Regenerate Structure

*Data → Tables →* sobre cada tabla *→ Regenerate Structure*.

Sin este paso las columnas existen en la hoja y la aplicación no las ve, **y todo lo demás falla en
silencio**. Es el error que ya ocurrió una vez en este proyecto.

Tablas a regenerar: `ACT_Activos`, `OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `USR_Usuarios`,
`EST_Activo`, `TIP_TiposActivo`, `CHK_Checklists`, `CHD_ChecklistDetalle`, `FOT_Fotografias`,
`FIR_Firmas`, `FRM_Preguntas`, `FRM_Formularios`, `LST_ValoresLista`, `ROL_Roles`, `CAL_Calzadas`,
`SEN_Sentidos`, `TPR_TiposRespuesta`.

Y **añadir como tablas nuevas** las siete que la Fase A creó, que AppSheet todavía no conoce:
`UNF_UnidadesFuncionales`, `ASG_AsignacionZona`, `EOT_EstadosOrden`, `MOT_MotivosPendiente`,
`FAL_ModosFalla`, `NOV_Novedades`, `PLA_PlanMantenimiento`.

**Verificación del paso:** cada tabla muestra el número de columnas que tiene la hoja.
`MAN_Mantenimientos` debe mostrar 36.

## 5. Paso 2 — Fijar las claves

*Data → Columns →* marcar la casilla **KEY**, y que sea la única.

| Tabla | Clave |
|---|---|
| `ACT_Activos` | `ActivoID` |
| `OT_OrdenesTrabajo` | `OTID` |
| `MAN_Mantenimientos` | `MantenimientoID` |
| `USR_Usuarios` | `UsuarioID` |
| `EST_Activo` | `EstadoActivoID` |
| `UNF_UnidadesFuncionales` | `UnidadFuncionalID` |
| `EOT_EstadosOrden` | `EstadoOrdenID` |
| `MOT_MotivosPendiente` | `MotivoPendienteID` |
| `CHK_Checklists` | `ChecklistID` |
| `CHD_ChecklistDetalle` | `DetalleID` |

**Va antes que cualquier referencia.** Una referencia creada contra una tabla cuya clave todavía no
está fijada resuelve contra otra columna, y no lo dice.

## 6. Paso 3 — Los tipos que no son referencia

Se hacen primero porque son independientes entre sí y no pueden romper nada.

| Tabla | Columna | Tipo |
|---|---|---|
| `ACT_Activos` | `Ubicacion` | `LatLong` |
| `MAN_Mantenimientos` | `Coordenadas_Cierre`, `UbicacionEscaneo` | `LatLong` |
| `MAN_Mantenimientos` | `Precision_GPS` | `Number` |
| `MAN_Mantenimientos` | `FechaHoraInicio`, `FechaHoraFin`, `FechaHoraEscaneo`, `FechaAprobacion` | `DateTime` |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | `ChangeTimestamp` |
| `MAN_Mantenimientos` | `OrigenApertura` | `Enum`: `QR`, `Lista` |
| `MAN_Mantenimientos` | `CierreConExcepcion`, `RequiereSegundaVisita`, `AprobadoSupervisor` | `Yes/No` |
| `FOT_Fotografias` | `Archivo` | `Image`, calidad baja 600 px |
| `FOT_Fotografias` | `Ubicacion` | `LatLong` |
| `FIR_Firmas` | `Imagen` | `Signature` |
| `TIP_TiposActivo` | `RadioGeofencingKm` | `Decimal` |

Si `Coordenadas_Cierre` queda como `Text`, `DISTANCE()` no opera y el paso 8 falla sin explicar por
qué.

## 7. Paso 4 — Las referencias, de abajo hacia arriba

**El orden es obligatorio**: cada bloque referencia tablas cuyas claves ya se fijaron en el bloque
anterior.

### 4.1 Contra catálogos

| Tabla | Columna | `Ref` a |
|---|---|---|
| `USR_Usuarios` | `RolID` | `ROL_Roles` |
| `USR_Usuarios` | `SedeID` | `SED_Sedes` |
| `ACT_Activos` | `TipoActivoID` | `TIP_TiposActivo` |
| `ACT_Activos` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` |
| `ACT_Activos` | `EstadoActivoID` | `EST_Activo` |
| `ACT_Activos` | `CalzadaID` | `CAL_Calzadas` |
| `ACT_Activos` | `SentidoID` | `SEN_Sentidos` |
| `ACT_Activos` | `FrecuenciaID` | `FRE_Frecuencias` |
| `TIP_TiposActivo` | `FormularioID` | `FRM_Formularios` |
| `ASG_AsignacionZona` | `UsuarioID` | `USR_Usuarios` |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` |

### 4.2 La orden de trabajo

| Columna | `Ref` a | Nota |
|---|---|---|
| `ActivoID` | `ACT_Activos` | Guarda 2, 26, 5, 9, 27, 3. Resuelven |
| `TecnicoID` | `USR_Usuarios` | |
| `SupervisorID` | `USR_Usuarios` | |
| `EstadoOrdenID` | `EOT_EstadosOrden` | **Solo si `ESPEC-001B` está aplicada** |
| `OTOrigenID` | `OT_OrdenesTrabajo` | Autorreferencia |

### 4.3 El mantenimiento — el retipado que desbloquea todo

| Columna | `Ref` a | Nota |
|---|---|---|
| `OTID` | `OT_OrdenesTrabajo` | **Era `Text`. Es el defecto raíz del sistema.** La tabla tiene 0 filas, así que la conversión no arrastra dato alguno |
| `TecnicoID` | `USR_Usuarios` | |
| `EstadoActivoID` | `EST_Activo` | |
| `MotivoPendienteID` | `MOT_MotivosPendiente` | |
| `ModoFallaID` | `FAL_ModosFalla` | |

**Sobre `Is a part of` en `MAN_Mantenimientos.OTID`: decidir antes de marcarlo.** Marcarlo implica
que **borrar una orden borre su ejecución, sus fotografías y sus firmas**. En un sistema cuyo
propósito es que la evidencia sea difícil de falsificar, eso se decide a conciencia. Si no hay
decisión tomada, **déjalo sin marcar**: se puede activar después, y desactivarlo no devuelve lo
borrado.

### 4.4 Evidencias y checklist

| Tabla | Columna | `Ref` a | `IsPartOf` |
|---|---|---|---|
| `FOT_Fotografias` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `FIR_Firmas` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `CHK_Checklists` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `CHK_Checklists` | `FormularioID` | `FRM_Formularios` | No |
| `CHD_ChecklistDetalle` | `ChecklistID` | `CHK_Checklists` | Sí |
| `CHD_ChecklistDetalle` | `PreguntaID` | `FRM_Preguntas` | No |
| `FRM_Preguntas` | `FormularioID` | `FRM_Formularios` | No |
| `FRM_Preguntas` | `SeccionID` | `FRM_Secciones` | No |
| `FRM_Preguntas` | `TipoRespuestaID` | `TPR_TiposRespuesta` | No |
| `LST_ValoresLista` | `PreguntaID` | `FRM_Preguntas` | No |

**Cuidado con `LST_ValoresLista.PreguntaID`:** sus 4 filas guardan el **texto** `Estado encontrado`,
no una clave. Convertirla a `Ref` las deja huérfanas a las cuatro. O se corrigen los valores primero,
o se deja como `Text` y se anota como deuda.

**Verificación del paso 4, y es la que importa de toda la fase.** En el Asistente de Expresiones,
sobre `MAN_Mantenimientos`:

```
[OTID].[ActivoID].[Ubicacion]
```

Debe resolver sin error. **Es la prueba de que la cadena existe**, y lo que este proyecto no ha
tenido nunca.

## 8. Paso 5 — Las reglas

Ahora sí, y no antes, porque todas dependen de las referencias.

**RG-01, geofencing de cierre**, sobre `MAN_Mantenimientos.Coordenadas_Cierre`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
Invalid text:   Ubicación fuera de rango: debe estar junto al activo para cerrar.
```

Mientras `RadioGeofencingKm` esté vacío en los 18 tipos, usar el literal `1.0` y anotarlo como
provisional. Poblarlo es mejor: una subestación y un poste SOS no admiten la misma tolerancia.

**RG-02:** `Precision_GPS`, valor inicial `USERLOCATIONACCURACY()`.

**RG-03:** `MotivoExcepcion`, `Required_If` = `[CierreConExcepcion] = TRUE`.

**RG-04, Security Filter** sobre `ACT_Activos`:

```
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))
```

**RG-05, Security Filter** sobre `OT_OrdenesTrabajo`:

```
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

**RG-09:** `CHK_Checklists.VersionFormulario`, valor inicial `[FormularioID].[Version]`.

Las demás reglas del modelo —RG-06 a RG-08 y RG-10 a RG-13— son bots. **Los bots programados no se
ejecutan en el plan gratuito**, así que se configuran pero no funcionarán hasta que se decida D-B.

## 9. Paso 6 — Reparar lo que rompió el renombrado

Corregir cada vista, fórmula y acción anotada en el punto 3.4 que citaba `Numero_OT`, `Activo`,
`Tecnico`, `SupervidorID`, `Estado`, `MttoID` o `Tecnico_Asignado`.

## 10. Criterio de cierre

1. `[OTID].[ActivoID].[Ubicacion]` resuelve en el Asistente de Expresiones.
2. Abrir una orden muestra el activo como **enlace navegable**, no como el número `2`.
3. Las 6 órdenes muestran su estado resuelto contra `EOT_EstadosOrden`, ninguna en blanco.
4. Con la cuenta de un técnico, `ACT_Activos` devuelve **más de cero** activos.
5. Una fila escrita **desde la aplicación** llega a `MAN_Mantenimientos` con valor en
   `Coordenadas_Cierre` y `Precision_GPS`, verificada leyendo el Sheets.
6. Un intento de cierre lejos del activo se rechaza **con el mensaje escrito**, no con un error
   genérico.

**El punto 6 no va a pasar todavía, y conviene saberlo antes de intentarlo.** Los 34 activos
comparten la coordenada `4.728512, -74.114531`, que está en Bogotá. Mientras siga así, todo cierre
en la vía queda fuera de rango y todo cierre en Bogotá queda dentro. El cableado es condición
necesaria del geofencing; las coordenadas reales (D-01) son la otra mitad.

## 11. Cuándo detenerse

Detenerse no es fallar. Seguir a ciegas sí.

- Un paso no produce el efecto esperado **dos veces seguidas**.
- La pantalla no coincide con lo que esta especificación describe.
- Hay que tocar algo que no está aquí.

En todos los casos: parar, documentar qué se hizo, qué se esperaba y qué se vio, y devolver el
control. **No improvisar sobre producción.**

## 12. Reversión

1. AppSheet: *Manage → Versions*, restaurar la versión guardada en el punto 3.2.
2. Sheets: restaurar desde `SGMC_backup_2026-08-07_antes_cableado_FaseA`.
3. Anotar en qué paso falló y con qué mensaje **antes** de reintentar.
