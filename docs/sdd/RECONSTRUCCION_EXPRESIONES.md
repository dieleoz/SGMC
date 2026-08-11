# Reconstruccion de la capa de expresiones — lista de reposicion

**Generado de `scripts/modelo_objetivo.py`.** Es lo que tiene que existir en la aplicacion.
**Ninguna expresion esta truncada**: se copian y se pegan enteras.

## 1. Los nombres viejos, y por que la lista NO se aplica en bloque

La Fase A renombro columnas en la hoja. Toda expresion que cite un nombre viejo quedo rota.

> **Cuidado: cinco de estos nombres siguen VIVOS en otras tablas.** El mapeo solo vale **tabla por
> tabla**. Un buscar-y-reemplazar global rompe `SED_Sedes` y `MAN_Mantenimientos`.

| Tabla | Nombre viejo | Nombre correcto | Aviso |
|---|---|---|---|
| `ACT_Activos` | `EstadoID` | `EstadoActivoID` |  |
| `CHD_ChecklistDetalle` | `Observaciones` | `Observacion` | **Sigue vivo en `ACT_Activos`, `OT_OrdenesTrabajo`, `MAN_Mantenimientos`** |
| `CHK_Checklists` | `OTID` | `MantenimientoID` | **Sigue vivo en `OT_OrdenesTrabajo`, `MAN_Mantenimientos`** |
| `FRM_Formularios` | `Descripción` | `Descripcion` |  |
| `FRM_Formularios` | `Versión` | `Version` |  |
| `LST_ValoresLista` | `ListaID` | `ValorListaID` |  |
| `MAN_Mantenimientos` | `Aprobado_Supervisor` | `AprobadoSupervisor` |  |
| `MAN_Mantenimientos` | `Fecha_Hora_Fin` | `FechaHoraFin` |  |
| `MAN_Mantenimientos` | `Fecha_Hora_Inicio` | `FechaHoraInicio` |  |
| `MAN_Mantenimientos` | `Fecha_Hora_Registro` | `FechaHoraRegistro` |  |
| `MAN_Mantenimientos` | `Motivo_Pendiente` | `MotivoPendienteID` |  |
| `MAN_Mantenimientos` | `MttoID` | `MantenimientoID` |  |
| `MAN_Mantenimientos` | `Requiere_Segunda_Visita` | `RequiereSegundaVisita` |  |
| `MAN_Mantenimientos` | `Tecnico_Asignado` | `TecnicoID` |  |
| `MAN_Mantenimientos` | `Usuario_Registro` | `UsuarioRegistro` |  |
| `OT_OrdenesTrabajo` | `Activo` | `ActivoID` | **Sigue vivo en `SED_Sedes`, `UNF_UnidadesFuncionales`, `ROL_Roles`** |
| `OT_OrdenesTrabajo` | `Cerrada_Por` | `CerradaPor` |  |
| `OT_OrdenesTrabajo` | `Estado` | `EstadoOrdenID` | **Sigue vivo en `NOV_Novedades`** |
| `OT_OrdenesTrabajo` | `Fecha Programada` | `FechaProgramada` |  |
| `OT_OrdenesTrabajo` | `Fecha_Cierre` | `FechaCierre` |  |
| `OT_OrdenesTrabajo` | `Numero_OT` | `OTID` |  |
| `OT_OrdenesTrabajo` | `SupervidorID` | `SupervisorID` |  |
| `OT_OrdenesTrabajo` | `Tecnico` | `TecnicoID` |  |
| `ROL_Roles` | `Descripción` | `Descripcion` |  |
| `USR_Usuarios` | `Estado` | `Activo` | **Sigue vivo en `NOV_Novedades`** |
| `USR_Usuarios` | `usuarioID` | `UsuarioID` |  |

**El caso que mas engana:** en `OT_OrdenesTrabajo` conviven `ActivoID` —la referencia al activo—
y `Activo` —la bandera Si/No—. Una formula que diga `Activo` **no da error**: apunta a la bandera
y devuelve lista vacia.

## 2. Las 23 reglas, con su expresion completa

### RG-01 — `MAN_Mantenimientos` · `Coordenadas_Cierre_LatLong`

**Tipo:** Valid_If · cubre RF-012

```
DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
```

> Impide cerrar lejos del activo, con radio por tipo. La ruta atraviesa dos referencias, de ahi que cablearlas sea el primer paso de todo.

**Antes de pegarla, compruebe que el radio esta poblado.** Esta regla desreferencia
`TIP_TiposActivo.RadioGeofencingKm`. **Si esa columna esta vacia, la comparacion se hace
contra blanco y rechaza tambien el cierre legitimo**: fallarian las dos pruebas del par,
la que debe aceptar y la que debe rechazar, y la tanda dejaria de discriminar.

```bash
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

En la hoja vigente estan **poblados los 27**, con 0.05 km en 18 · 0.1 km en 8 · 1.5 km en 1. Un literal en su lugar -por ejemplo `<= 1.0`- hace que el sistema pruebe "estas en el corredor" en vez de "estas frente al equipo", que es su proposito.

### RG-35 — `OT_OrdenesTrabajo` · `(tabla)`

**Tipo:** App formula · cubre Identificacion legible ante el tecnico

> **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con
> *Data > Columns > `Add virtual column`*, se llama **`Etiqueta`**, y lleva esa expresión
> en su `App formula`.
> 
> Y además **`Show?` activo** y **`Label` marcado**. Si la tabla ya tenía otra
> columna con `Label`, se desmarca primero: solo puede haber una.

```
CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])
```

> Etiqueta, columna VIRTUAL (no en MODELO: F-02 no la exige, no toca la hoja). Reemplaza a OTID como Label ahora que OTID es UNIQUEID().

### RG-36 — `PLA_PlanMantenimiento` · `(tabla)`

**Tipo:** App formula · cubre Identificacion legible ante operacion

> **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con
> *Data > Columns > `Add virtual column`*, se llama **`Etiqueta`**, y lleva esa expresión
> en su `App formula`.
> 
> Y además **`Show?` activo** y **`Label` marcado**. Si la tabla ya tenía otra
> columna con `Label`, se desmarca primero: solo puede haber una.

```
CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])
```

> Etiqueta, columna VIRTUAL. Mismo mecanismo que RG-35.

### RG-34 — `ACT_Activos` · `UnidadFuncionalID`

**Tipo:** Valid_If · cubre RF-002

```
OR(ISBLANK([SedeID]), [UnidadFuncionalID] = [SedeID].[UnidadFuncionalID])
```

> El equipo bajo techo hereda donde esta de su edificacion. Sin esta regla la unidad funcional se guardaria en dos sitios -en el activo y en su sede- y podrian decir cosas distintas sin que nada protestara. Con ella hay un solo sitio donde mirar: si el activo tiene sede, manda la sede.

### RG-03 — `MAN_Mantenimientos` · `MotivoExcepcion`

**Tipo:** Required_If · cubre D-04

```
[CierreConExcepcion] = TRUE
```

> Si el tecnico cierra con excepcion por GPS deficiente, debe justificarlo por escrito.

### RG-04 — `ACT_Activos` · `(tabla)`

**Tipo:** Security Filter · cubre RF-004

```
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))
```

> Cada tecnico descarga solo los activos de las unidades funcionales que tiene asignadas. Controla el volumen de sincronizacion, no solo la visibilidad.

### RG-05 — `OT_OrdenesTrabajo` · `(tabla)`

**Tipo:** Security Filter · cubre RF-004

```
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

> El tecnico ve sus ordenes; el supervisor, las que supervisa.

### RG-06 — `MAN_Mantenimientos` · `(tabla)`

**Tipo:** Bot · cubre RF-016

```
[EstadoActivoID].[GeneraAlerta] = TRUE
```

> Envia correo con informe PDF al CCO y al supervisor cuando el activo queda fuera de servicio.

### RG-07 — `OT_OrdenesTrabajo` · `(tabla)`

**Tipo:** Bot · cubre RF-003

```
Adds
```

> Notifica por correo al tecnico cuando se le asigna una orden.

### RG-37 — `OT_OrdenesTrabajo` · `(tabla)`

**Tipo:** App formula · cubre D-06

> **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con
> *Data > Columns > `Add virtual column`*, se llama **`EstaVencida`**, y lleva esa expresión
> en su `App formula`.

```
AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())
```

> EstaVencida, columna VIRTUAL (Yes/No), no en MODELO: F-02 no la exige, no toca la hoja. Reemplaza a RG-08. Misma condicion exacta que tenia el bot programado, pero como lectura que se recalcula en cada sincronizacion: no escribe, no mueve el estado, y el tecnico que llega tarde sigue pudiendo cerrar. Su consumidor: una vista 'Ordenes vencidas' sobre esta tabla, condicion [EstaVencida] = TRUE, visible para el rol Supervisor (ver ESPEC-006 3.2). No tiene historico: si la orden se cierra tarde, vuelve a FALSE y no queda marca de que estuvo vencida, y la vista deja de listarla (ver ESPEC-006 3.4).

### RG-09 — `CHK_Checklists` · `VersionFormulario`

**Tipo:** Initial value · cubre D-11

```
[FormularioID].[Version]
```

> Congela la version del formulario con que se respondio, para comparar historico.

### RG-11 — `PLA_PlanMantenimiento` · `ProximaFecha`

**Tipo:** App formula · cubre Plan de mantenimiento

```
[UltimaEjecucion] + [FrecuenciaID].[Dias]
```

> Calcula cuando vuelve a tocar el preventivo de ese activo.

### RG-38 — `PLA_PlanMantenimiento` · `(tabla)`

**Tipo:** Accion · cubre Plan de mantenimiento

```
AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)
```

> Reemplaza a RG-12. La expresion de arriba es la condicion de una vista/slice 'Vence en 7 dias' sobre esta tabla -no una regla de columna-. Sobre esa vista se expone una accion 'Data: add a new row to another table using values from this row' (Data > Actions), que el supervisor pulsa -individual o en bloque, ver Actions: The Essentials, seccion Bulk actions- y crea la fila en OT_OrdenesTrabajo. Mapeo de columnas verificado en ESPEC-006 3.3. No usa Automation > Bots: no hay Event ni Schedule, es invocacion explicita del usuario. No requiere plan de pago (ver ESPEC-006 2.1: la restriccion verificada contra la fuente oficial es sobre bots con Schedule event, no sobre acciones invocadas por el usuario).

### RG-13 — `MAN_Mantenimientos` · `(tabla)`

**Tipo:** Verificacion de evidencia · cubre Prueba de presencia

```
DISTANCE([UbicacionEscaneo_LatLong], [Coordenadas_Cierre_LatLong]) <= 0.5
```

> Contrasta donde escaneo con donde cerro. Una diferencia grande indica que escaneo en un sitio y cerro en otro. No bloquea: se reporta.

### RG-20 — `MAN_Mantenimientos` · `(varias)`

**Tipo:** Editable_If · cubre Prueba de presencia

```
FALSE
```

> Sobre Coordenadas_Cierre, UbicacionEscaneo y FechaHoraEscaneo (tres columnas desde ESPEC-004/ORDEN-004: Precision_GPS se retiro del modelo, ver CAMPOS_RETIRADOS). SIN ESTO EL GEOFENCING ES DECORATIVO: HERE() es Initial value, no App formula, y un Initial value SI es editable. Coordenadas_Cierre es un LatLong, que en un formulario AppSheet dibuja como un pin arrastrable sobre un mapa, y la ubicacion del activo esta visible en la app: el tecnico arrastra el pin encima del activo y RG-01 valida sin protestar. La regla se cumplia y la presencia no quedaba probada.

### RG-16 — `ACT_Activos` · `Activo`

**Tipo:** App formula · cubre Baja de activos

```
[EstadoActivoID].[Nombre] <> "Retirado"
```

> La bandera se deriva del estado, no se edita. La comparacion va contra [Nombre] y NO contra la columna a secas: EstadoActivoID es un Ref y un Ref guarda la CLAVE del destino, que aqui vale 1 a 4. Comparar la clave con la cadena 'Retirado' es siempre cierto, y como esto es una App formula, ESCRIBE: pondria Activo=TRUE sobre el activo dado de baja. EST_Activo ya tiene el estado Retirado; mantener ademas una bandera independiente es el mismo dato en dos sitios, y algun dia diran cosas distintas sin forma de saber cual miente.

### RG-17 — `ACT_Activos` · `FechaBaja`

**Tipo:** Required_If · cubre Baja de activos

```
[EstadoActivoID].[Nombre] = "Retirado"
```

> Contra [Nombre], no contra la clave. Si se retira un activo hay que decir cuando. Un historico que no puede explicar por que un activo dejo de recibir mantenimiento no es defendible.

### RG-18 — `ACT_Activos` · `(tabla)`

**Tipo:** Doctrina de reportes · cubre Baja de activos

```
Ver descripcion: es una prohibicion, no una expresion a configurar
```

> NO filtrar los reportes historicos por la bandera Activo del activo padre. Un reporte HISTORICO filtra por la fecha y el estado de la TRANSACCION, nunca por el estado actual del activo padre. Filtrar por [ActivoID].[Activo] hace que al dar de baja un activo desaparezcan retroactivamente todos sus mantenimientos pasados: el informe del ano anterior cambia solo y muestra menos trabajo del que se hizo. Ante interventoria eso no parece un filtro mal puesto, parece que el mantenimiento nunca se ejecuto.

### RG-14 — `OT_OrdenesTrabajo` · `(tabla)`

**Tipo:** Are updates allowed · cubre Evidencia defendible

```
Updates, Adds
```

> Se retira Deletes. Una orden no se borra: se anula con Activo = FALSE, que deja traza de que existio. Si el boton no esta, no hay accidente posible.

### RG-15 — `MAN_Mantenimientos` · `(tabla)`

**Tipo:** Are updates allowed · cubre Evidencia defendible

```
Updates, Adds
```

> Se retira Deletes. Es la decision central del sistema: la ejecucion es la prueba de que alguien estuvo frente al equipo. Protegido aqui arriba, el IsPartOf de FOT, FIR y CHK nunca llega a dispararse. Nota: esto protege DENTRO de la app; nadie impide borrar la fila a mano en el Sheets, donde hay dos cuentas con permiso de edicion.

### RG-10 — `MAN_Mantenimientos` · `(tabla)`

**Tipo:** Bot · cubre D-07

```
[RequiereSegundaVisita] = TRUE
```

> Genera una orden de seguimiento enlazada a la original mediante OTOrigenID.

### RG-39 — `FOT_Fotografias` · `Ubicacion_LatLong`

**Tipo:** Editable_If · cubre Prueba de presencia

```
FALSE
```

> Mismo mecanismo que RG-20: HERE() es Initial value, no App formula, y un Initial value SI es editable. Sin esto la coordenada de la fotografia se dibuja como un pin arrastrable y la evidencia queda donde el tecnico quiera dejarla, no donde tomo la foto. CABLEAR DESPUES del Initial value = HERE(): al reves la columna queda obligatoria, no editable y vacia, y ningun tecnico puede guardar una fotografia. ESPEC-008.

### RG-40 — `NOV_Novedades` · `Ubicacion_LatLong`

**Tipo:** Editable_If · cubre Prueba de presencia

```
FALSE
```

> Igual que RG-39, sobre la novedad en vez de la fotografia. Sin esto un tecnico registra una novedad en ruta, arrastra el pin y el hallazgo queda georreferenciado donde el quiera. CABLEAR DESPUES del Initial value = HERE(). ESPEC-008.

## 3. Las claves, todas `Text`

| Tabla | Clave |
|---|---|
| `ACT_Activos` | `ActivoID` |
| `ASG_AsignacionZona` | `AsignacionID` |
| `CAL_Calzadas` | `CalzadaID` |
| `CHD_ChecklistDetalle` | `DetalleID` |
| `CHK_Checklists` | `ChecklistID` |
| `EOT_EstadosOrden` | `EstadoOrdenID` |
| `EST_Activo` | `EstadoActivoID` |
| `FAL_ModosFalla` | `ModoFallaID` |
| `FIR_Firmas` | `FirmaID` |
| `FOT_Fotografias` | `FotoID` |
| `FRE_Frecuencias` | `FrecuenciaID` |
| `FRM_Formularios` | `FormularioID` |
| `FRM_Preguntas` | `PreguntaID` |
| `FRM_Secciones` | `SeccionID` |
| `LST_ValoresLista` | `ValorListaID` |
| `MAN_Mantenimientos` | `MantenimientoID` |
| `MOT_MotivosPendiente` | `MotivoPendienteID` |
| `NOV_Novedades` | `NovedadID` |
| `OT_OrdenesTrabajo` | `OTID` |
| `PAR_Parametros` | `ParametroID` |
| `PLA_PlanMantenimiento` | `PlanID` |
| `ROL_Roles` | `RolID` |
| `SED_Sedes` | `SedeID` |
| `SEN_Sentidos` | `SentidoID` |
| `TIP_TiposActivo` | `TipoActivoID` |
| `TPR_TiposRespuesta` | `TipoRespuestaID` |
| `UNF_UnidadesFuncionales` | `UnidadFuncionalID` |
| `USR_Usuarios` | `UsuarioID` |

## 4. Las 39 referencias

**Son las del modelo, no las 15 de `ESPEC-002`.** Aquellas eran las que faltaban en la aplicacion
anterior; en una construida de cero no sobrevive ninguna.

| Tabla | Columna | `Ref` a | `IsPartOf` |
|---|---|---|---|
| `ACT_Activos` | `TipoActivoID` | `TIP_TiposActivo` | no |
| `ACT_Activos` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `ACT_Activos` | `CalzadaID` | `CAL_Calzadas` | no |
| `ACT_Activos` | `SentidoID` | `SEN_Sentidos` | no |
| `ACT_Activos` | `SedeID` | `SED_Sedes` | no |
| `ACT_Activos` | `EstadoActivoID` | `EST_Activo` | no |
| `ACT_Activos` | `FrecuenciaID` | `FRE_Frecuencias` | no |
| `ASG_AsignacionZona` | `UsuarioID` | `USR_Usuarios` | no |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `CHD_ChecklistDetalle` | `ChecklistID` | `CHK_Checklists` | **SI** |
| `CHD_ChecklistDetalle` | `PreguntaID` | `FRM_Preguntas` | no |
| `CHK_Checklists` | `MantenimientoID` | `MAN_Mantenimientos` | **SI** |
| `CHK_Checklists` | `FormularioID` | `FRM_Formularios` | no |
| `FAL_ModosFalla` | `TipoActivoID` | `TIP_TiposActivo` | no |
| `FIR_Firmas` | `MantenimientoID` | `MAN_Mantenimientos` | **SI** |
| `FOT_Fotografias` | `MantenimientoID` | `MAN_Mantenimientos` | **SI** |
| `FRM_Preguntas` | `FormularioID` | `FRM_Formularios` | no |
| `FRM_Preguntas` | `SeccionID` | `FRM_Secciones` | no |
| `FRM_Preguntas` | `TipoRespuestaID` | `TPR_TiposRespuesta` | no |
| `LST_ValoresLista` | `PreguntaID` | `FRM_Preguntas` | no |
| `MAN_Mantenimientos` | `OTID` | `OT_OrdenesTrabajo` | no |
| `MAN_Mantenimientos` | `TecnicoID` | `USR_Usuarios` | no |
| `MAN_Mantenimientos` | `EstadoActivoID` | `EST_Activo` | no |
| `MAN_Mantenimientos` | `MotivoPendienteID` | `MOT_MotivosPendiente` | no |
| `MAN_Mantenimientos` | `ModoFallaID` | `FAL_ModosFalla` | no |
| `NOV_Novedades` | `UsuarioID` | `USR_Usuarios` | no |
| `NOV_Novedades` | `ActivoID` | `ACT_Activos` | no |
| `OT_OrdenesTrabajo` | `ActivoID` | `ACT_Activos` | no |
| `OT_OrdenesTrabajo` | `TecnicoID` | `USR_Usuarios` | no |
| `OT_OrdenesTrabajo` | `SupervisorID` | `USR_Usuarios` | no |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | `EOT_EstadosOrden` | no |
| `OT_OrdenesTrabajo` | `OTOrigenID` | `OT_OrdenesTrabajo` | no |
| `OT_OrdenesTrabajo` | `CerradaPor` | `USR_Usuarios` | no |
| `PLA_PlanMantenimiento` | `ActivoID` | `ACT_Activos` | no |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | `FRE_Frecuencias` | no |
| `PLA_PlanMantenimiento` | `ResponsableID` | `USR_Usuarios` | no |
| `SED_Sedes` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `TIP_TiposActivo` | `FormularioID` | `FRM_Formularios` | no |
| `USR_Usuarios` | `RolID` | `ROL_Roles` | no |

## 5. Lo que NO se repone: columnas retiradas

**50 columnas.** Siguen en la hoja a proposito. En la aplicacion: tipo `Text`, `Show?`
desmarcado, sin formula. **No se borran.**

| Tabla | Columna | Por que | |
|---|---|---|---|
| `CHD_ChecklistDetalle` | `Activo` | El detalle es parte de su checklist: no se desactiva por separado. |  |
| `CHD_ChecklistDetalle` | `EstadoPregunta` | Redundante con Contestada. |  |
| `CHD_ChecklistDetalle` | `FechaRespuesta` | Se deriva del ChangeTimestamp del mantenimiento. |  |
| `CHD_ChecklistDetalle` | `Orden` | Se alcanza por [PreguntaID].[Orden]. |  |
| `CHD_ChecklistDetalle` | `PreguntaActual` | Estado de la interfaz, no dato. |  |
| `CHD_ChecklistDetalle` | `RespuestaFecha` | Fuera de alcance: ninguna pregunta usa tipo fecha. |  |
| `CHD_ChecklistDetalle` | `RespuestaFirma` | Sustituido por FIR_Firmas. |  |
| `CHD_ChecklistDetalle` | `RespuestaFoto` | Sustituido por FOT_Fotografias. |  |
| `CHD_ChecklistDetalle` | `RespuestaGPS` | La coordenada es del mantenimiento y de cada fotografia. |  |
| `CHD_ChecklistDetalle` | `RespuestaHora` | Fuera de alcance: ninguna pregunta usa tipo hora. |  |
| `CHD_ChecklistDetalle` | `TipoRespuestaID` | Se alcanza por [PreguntaID].[TipoRespuestaID]. | **TRAMPA -> `TPR_TiposRespuesta`** |
| `CHD_ChecklistDetalle` | `TotalPreguntas` | No es del detalle sino del encabezado, y ademas se cuenta. |  |
| `CHK_Checklists` | `Activo` | El checklist es parte de su mantenimiento: no se desactiva por separado. |  |
| `CHK_Checklists` | `ActivoID` | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. | **TRAMPA -> `ACT_Activos`** |
| `CHK_Checklists` | `Estado` | Sustituido por Finalizado, que produccion ya tiene. |  |
| `CHK_Checklists` | `FechaCreacion` | Redundante con FechaInicio. |  |
| `CHK_Checklists` | `FechaEnvioCorreo` | Es traza del bot, no del checklist. |  |
| `CHK_Checklists` | `FirmaSupervisor` | El supervisor aprueba en el portal, no firma. Supuesto D-10. |  |
| `CHK_Checklists` | `FirmaTecnico` | Sustituido por FIR_Firmas. |  |
| `CHK_Checklists` | `GPSFin` | Idem. |  |
| `CHK_Checklists` | `GPSInicio` | La coordenada es del mantenimiento y de cada fotografia, no del checklist. |  |
| `CHK_Checklists` | `Observaciones` | La observacion es de la ejecucion o de la respuesta, no del encabezado. |  |
| `CHK_Checklists` | `PDF` | El informe se genera al enviarlo, no se almacena en la fila. |  |
| `CHK_Checklists` | `Porcentaje` | Se calcula. Guardarlo permite que contradiga al detalle. |  |
| `CHK_Checklists` | `PreguntaActual` | Estado de la interfaz, no dato. Se deriva de las respuestas. |  |
| `CHK_Checklists` | `TecnicoID` | Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato de prueba dejo 'Santiago Moreno' en lugar de un identificador. |  |
| `CHK_Checklists` | `TotalPreguntas` | Se cuenta de FRM_Preguntas. |  |
| `FOT_Fotografias` | `Fecha` | Duplicaba a FechaHora, que es la que vale como evidencia porque la escribe el servidor. Dos fechas para el mismo hecho invitan a discutir cual manda justo cuando hay que probar algo. Retirada el 2026-08-10. |  |
| `FOT_Fotografias` | `PrecisionGPS` | USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1, mismo hallazgo que Precision_GPS de MAN_Mantenimientos). Ninguna regla la leia (ESPEC-007 2.2): a diferencia de MAN, no habia cadena que romper. Retirada por ESPEC-007. Si FOT_Fotografias ya tenia esta columna con Initial value puesto en el editor, hace falta Delete and re-add de la tabla completa (mismo procedimiento de ESPEC-004 2.10); si quedo huerfana sin usar, no hace falta nada (ESPEC-007 2.7, sin confirmar cual rama aplica). |  |
| `FRM_Formularios` | `Orden` | Ordenaria los formularios en una lista y ninguna vista los ordena. Estaba vacia. Si algun dia se ordenan, se declara entonces con su proposito escrito. Retirada el 2026-08-10. |  |
| `FRM_Preguntas` | `ValorDefecto` | Precargaria la respuesta antes de que el tecnico conteste. En una evidencia eso es peligroso: una respuesta por defecto que nadie toca parece contestada. Retirada el 2026-08-10. |  |
| `MAN_Mantenimientos` | `Diagnostico` | Se responde en el checklist, no en campo libre. |  |
| `MAN_Mantenimientos` | `Duracion_Minutos` | Se calcula de FechaHoraInicio y FechaHoraFin. |  |
| `MAN_Mantenimientos` | `Estado_Intervencion` | Redundante con el estado de la orden. |  |
| `MAN_Mantenimientos` | `Fecha` | Redundante con FechaHoraInicio. |  |
| `MAN_Mantenimientos` | `Firma_Supervisor` | El supervisor aprueba en el portal, no firma. Supuesto D-10. |  |
| `MAN_Mantenimientos` | `Firma_Tecnico` | Sustituido por FIR_Firmas. |  |
| `MAN_Mantenimientos` | `Imagen_Final` | Sustituido por FOT_Fotografias con Tipo=Despues. |  |
| `MAN_Mantenimientos` | `Imagen_Inicio` | Sustituido por FOT_Fotografias con Tipo=Antes. |  |
| `MAN_Mantenimientos` | `Localizacion` | Ambiguo y redundante con Coordenadas_Cierre. |  |
| `MAN_Mantenimientos` | `Precision_GPS` | USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1): la columna nunca se poblaba, RG-19 comparaba siempre numero > blanco y RG-03 no pedia MotivoExcepcion nunca. Retirada por ESPEC-004/ORDEN-004. Si MAN_Mantenimientos ya estaba dada de alta en el editor con esta columna sin usar (Rama A, ESPEC-004 2.10), retirarla del modelo no la borra de la hoja: queda huerfana, sin Initial value y sin uso, y eso no es un fallo (ACTA-004; PRUEBA-004 P-45). Si ya estaba cableada con Initial value puesto (Rama B), hace falta Delete and re-add de la tabla completa (ESPEC-004 2.10). |  |
| `MAN_Mantenimientos` | `Repuestos_Utilizados` | Gestion de repuestos esta fuera de alcance. |  |
| `MAN_Mantenimientos` | `Requiere_Repuesto` | Se cubre con MotivoPendienteID = Falta de repuesto. |  |
| `MAN_Mantenimientos` | `Tipo` | El tipo es de la orden, no de la ejecucion. |  |
| `MAN_Mantenimientos` | `Trabajo_Realizado` | Se responde en el checklist. |  |
| `OT_OrdenesTrabajo` | `FormularioID` | El formulario lo determina el tipo del activo, no la orden. | **TRAMPA -> `FRM_Formularios`** |
| `OT_OrdenesTrabajo` | `Informe_Final` | Se genera del mantenimiento y su checklist, no se transcribe. |  |
| `OT_OrdenesTrabajo` | `Motivo_Cierre` | Se tipifica en MOT_MotivosPendiente desde la ejecucion. |  |
| `USR_Usuarios` | `SedeID` | Retirada el 2026-08-10 para que el modelo diga lo que dice la especificacion. FUNCIONAL_SGMC 6.3 la declara descartada frente a ASG_AsignacionZona: la sede es un edificio y la asignacion es un tramo, y un tecnico puede atender varias unidades funcionales, asi que la relacion es de muchos a muchos y no cabe como columna. RG-04, el filtro de seguridad que decide que activos ve cada tecnico, lee la asignacion y no menciona la sede. El modelo la declaraba Ref obligatoria mientras la spec la daba por descartada: se contradecian, y cablearla habria dejado dos formas de decir donde trabaja alguien. | **TRAMPA -> `SED_Sedes`** |
| `USR_Usuarios` | `UltimaSincronizacion` | Venia de una version anterior y el modelo nunca la uso. La regeneracion del 2026-08-10 la dejo fuera y no se echo en falta. Retirada el 2026-08-10. |  |

**Las 4 marcadas TRAMPA** se llaman igual que la clave de otra tabla, asi que **AppSheet las
convierte a `Ref` sola**. Hay que deshacerlo.

---
*Generado. Para actualizarlo, cambie `modelo_objetivo.py` y vuelva a generar.*
