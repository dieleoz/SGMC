# Reconstruccion de la capa de expresiones — lista de reposicion

**Generado de `scripts/modelo_objetivo.py`.** Es lo que tiene que existir cuando termine el
borrado y la regeneracion. No se inventa nada: son las 20 reglas que ya pasaron el arquitecto.

## Por que existe esta lista

La Fase A renombro columnas en la hoja mientras AppSheet guardaba definiciones con los nombres
viejos. Toda expresion que citaba `Activo`, `Estado`, `Fecha Programada`, `Numero_OT`,
`SupervidorID`, `Tecnico`, `Fecha_Cierre` o `Cerrada_Por` quedo rota, y como una tabla invalida
invalida a las que la referencian, los errores salen encadenados.

La salida es borrar la capa de expresiones y rehacerla. **Pero borrar sin lista deja una app que
despliega y nadie sabe que perdio.** Esto es la lista.

## 1. Los ocho nombres que rompen todo

Busque estos en cualquier formula, `Show_If`, `Valid_If` o `REF_ROWS`. Si aparecen, estan mal:

| Nombre viejo | Nombre correcto |
|---|---|
| `Numero_OT` | `OTID` |
| `Activo` | `ActivoID` |
| `Tecnico` | `TecnicoID` |
| `SupervidorID` | `SupervisorID` |
| `Fecha Programada` | `FechaProgramada` |
| `Estado` | `EstadoOrdenID` |
| `Fecha_Cierre` | `FechaCierre` |
| `Cerrada_Por` | `CerradaPor` |
| `EstadoID` | `EstadoActivoID` |
| `SedeID` | `UnidadFuncionalID` |
| `usuarioID` | `UsuarioID` |
| `Estado` | `Activo` |
| `MttoID` | `MantenimientoID` |
| `Tecnico_Asignado` | `TecnicoID` |
| `Fecha_Hora_Inicio` | `FechaHoraInicio` |
| `Fecha_Hora_Fin` | `FechaHoraFin` |
| `Requiere_Segunda_Visita` | `RequiereSegundaVisita` |
| `Motivo_Pendiente` | `MotivoPendienteID` |
| `Aprobado_Supervisor` | `AprobadoSupervisor` |
| `Usuario_Registro` | `UsuarioRegistro` |
| `Fecha_Hora_Registro` | `FechaHoraRegistro` |
| `OTID` | `MantenimientoID` |
| `Observaciones` | `Observacion` |
| `ListaID` | `ValorListaID` |
| `Descripción` | `Descripcion` |
| `Descripción` | `Descripcion` |
| `Versión` | `Version` |

**Cuidado con `Activo`:** en `OT_OrdenesTrabajo` existen HOY las dos. `ActivoID` es la referencia
al activo; `Activo` es la bandera Si/No. Una formula que diga `Activo` **no dara error** y
apuntara a la bandera. Es el fallo silencioso que aviso V-14.

## 2. Las 20 reglas que hay que reponer

| # | Tabla | Columna | Tipo | Expresion |
|---|---|---|---|---|
| RG-01 | `MAN_Mantenimientos` | `Coordenadas_Cierre` | Valid_If | `DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[Tipo...` |
| RG-02 | `MAN_Mantenimientos` | `Precision_GPS` | Initial value | `USERLOCATIONACCURACY()` |
| RG-03 | `MAN_Mantenimientos` | `MotivoExcepcion` | Required_If | `[CierreConExcepcion] = TRUE` |
| RG-04 | `ACT_Activos` | `(tabla)` | Security Filter | `IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[C...` |
| RG-05 | `OT_OrdenesTrabajo` | `(tabla)` | Security Filter | `OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())` |
| RG-06 | `MAN_Mantenimientos` | `(tabla)` | Bot | `[EstadoActivoID].[GeneraAlerta] = TRUE` |
| RG-07 | `OT_OrdenesTrabajo` | `(tabla)` | Bot | `Adds` |
| RG-08 | `OT_OrdenesTrabajo` | `EstadoOrdenID` | Bot programado | `AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())` |
| RG-09 | `CHK_Checklists` | `VersionFormulario` | Initial value | `[FormularioID].[Version]` |
| RG-11 | `PLA_PlanMantenimiento` | `ProximaFecha` | App formula | `[UltimaEjecucion] + [FrecuenciaID].[Dias]` |
| RG-12 | `PLA_PlanMantenimiento` | `(tabla)` | Bot programado | `[ProximaFecha] <= TODAY() + 7` |
| RG-13 | `MAN_Mantenimientos` | `(tabla)` | Verificacion de evidencia | `DISTANCE([UbicacionEscaneo], [Coordenadas_Cierre]) <= 0.5` |
| RG-20 | `MAN_Mantenimientos` | `(varias)` | Editable_If | `FALSE` |
| RG-19 | `MAN_Mantenimientos` | `CierreConExcepcion` | App formula | `OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_G...` |
| RG-16 | `ACT_Activos` | `Activo` | App formula | `[EstadoActivoID].[Nombre] <> "Retirado"` |
| RG-17 | `ACT_Activos` | `FechaBaja` | Required_If | `[EstadoActivoID].[Nombre] = "Retirado"` |
| RG-18 | `ACT_Activos` | `(tabla)` | Doctrina de reportes | `Ver descripcion: es una prohibicion, no una expresion a configurar` |
| RG-14 | `OT_OrdenesTrabajo` | `(tabla)` | Are updates allowed | `Updates, Adds` |
| RG-15 | `MAN_Mantenimientos` | `(tabla)` | Are updates allowed | `Updates, Adds` |
| RG-10 | `MAN_Mantenimientos` | `(tabla)` | Bot | `[RequiereSegundaVisita] = TRUE` |

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

## 4. Las 15 columnas que pasan a `Ref`

| Tabla | Columna | Hoy | `Ref` a |
|---|---|---|---|
| `MAN_Mantenimientos` | `OTID` | Text | `OT_OrdenesTrabajo` |
| `ACT_Activos` | `TipoActivoID` | Number | `TIP_TiposActivo` |
| `ACT_Activos` | `CalzadaID` | Number | `CAL_Calzadas` |
| `ACT_Activos` | `SentidoID` | Number | `SEN_Sentidos` |
| `ACT_Activos` | `FrecuenciaID` | Number | `FRE_Frecuencias` |
| `CHK_Checklists` | `FormularioID` | Text | `FRM_Formularios` |
| `CHD_ChecklistDetalle` | `ChecklistID` | Text | `CHK_Checklists` |
| `CHD_ChecklistDetalle` | `PreguntaID` | Text | `FRM_Preguntas` |
| `USR_Usuarios` | `RolID` | Number | `ROL_Roles` |
| `USR_Usuarios` | `SedeID` | Number | `SED_Sedes` |
| `TIP_TiposActivo` | `FormularioID` | Text | `FRM_Formularios` |
| `LST_ValoresLista` | `PreguntaID` | Text | `FRM_Preguntas` |
| `FRM_Preguntas` | `FormularioID` | Text | `FRM_Formularios` |
| `FRM_Preguntas` | `SeccionID` | Number | `FRM_Secciones` |
| `FRM_Preguntas` | `TipoRespuestaID` | Number | `TPR_TiposRespuesta` |

## 5. Lo que NO se repone

Columnas retiradas del modelo. Siguen en la hoja a proposito, pero **su expresion se vacia** y
no se vuelve a escribir:

| Tabla | Columna | Por que |
|---|---|---|
| `ACT_Activos` | `SedeID` | Se sustituye por UnidadFuncionalID. Mezclar donde trabaja la persona con donde esta el activo es lo que dejo a los usuarios en la sede 1 y a los activos en las sedes 7 a 10, es decir en conjuntos disjuntos. |
| `CHD_ChecklistDetalle` | `Orden` | Se alcanza por [PreguntaID].[Orden]. |
| `CHD_ChecklistDetalle` | `TipoRespuestaID` | Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| `CHD_ChecklistDetalle` | `PreguntaActual` | Estado de la interfaz, no dato. |
| `CHD_ChecklistDetalle` | `EstadoPregunta` | Redundante con Contestada. |
| `CHD_ChecklistDetalle` | `TotalPreguntas` | No es del detalle sino del encabezado, y ademas se cuenta. |
| `CHD_ChecklistDetalle` | `RespuestaFecha` | Fuera de alcance: ninguna pregunta usa tipo fecha. |
| `CHD_ChecklistDetalle` | `RespuestaHora` | Fuera de alcance: ninguna pregunta usa tipo hora. |
| `CHD_ChecklistDetalle` | `RespuestaFoto` | Sustituido por FOT_Fotografias. |
| `CHD_ChecklistDetalle` | `RespuestaFirma` | Sustituido por FIR_Firmas. |
| `CHD_ChecklistDetalle` | `RespuestaGPS` | La coordenada es del mantenimiento y de cada fotografia. |
| `CHD_ChecklistDetalle` | `FechaRespuesta` | Se deriva del ChangeTimestamp del mantenimiento. |
| `CHD_ChecklistDetalle` | `Activo` | El detalle es parte de su checklist: no se desactiva por separado. |
| `CHK_Checklists` | `ActivoID` | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| `CHK_Checklists` | `TecnicoID` | Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato de prueba dejo 'Santiago Moreno' en lugar de un identificador. |
| `CHK_Checklists` | `Observaciones` | La observacion es de la ejecucion o de la respuesta, no del encabezado. |
| `CHK_Checklists` | `FechaCreacion` | Redundante con FechaInicio. |
| `CHK_Checklists` | `Estado` | Sustituido por Finalizado, que produccion ya tiene. |
| `CHK_Checklists` | `GPSInicio` | La coordenada es del mantenimiento y de cada fotografia, no del checklist. |
| `CHK_Checklists` | `GPSFin` | Idem. |
| `CHK_Checklists` | `FirmaTecnico` | Sustituido por FIR_Firmas. |
| `CHK_Checklists` | `FirmaSupervisor` | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `CHK_Checklists` | `PDF` | El informe se genera al enviarlo, no se almacena en la fila. |
| `CHK_Checklists` | `FechaEnvioCorreo` | Es traza del bot, no del checklist. |
| `CHK_Checklists` | `Activo` | El checklist es parte de su mantenimiento: no se desactiva por separado. |
| `CHK_Checklists` | `PreguntaActual` | Estado de la interfaz, no dato. Se deriva de las respuestas. |
| `CHK_Checklists` | `TotalPreguntas` | Se cuenta de FRM_Preguntas. |
| `CHK_Checklists` | `Porcentaje` | Se calcula. Guardarlo permite que contradiga al detalle. |
| `MAN_Mantenimientos` | `ActivoID` | El activo se alcanza por [OTID].[ActivoID]. Guardarlo tambien aqui permite que la ejecucion diga un activo y su orden diga otro, y no hay forma de saber cual miente. Existe en el Excel local; AppSheet confirmo que en produccion no esta. |
| `MAN_Mantenimientos` | `Imagen_Inicio` | Sustituido por FOT_Fotografias con Tipo=Antes. |
| `MAN_Mantenimientos` | `Imagen_Final` | Sustituido por FOT_Fotografias con Tipo=Despues. |
| `MAN_Mantenimientos` | `Firma_Tecnico` | Sustituido por FIR_Firmas. |
| `MAN_Mantenimientos` | `Firma_Supervisor` | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `MAN_Mantenimientos` | `Localizacion` | Ambiguo y redundante con Coordenadas_Cierre. |
| `MAN_Mantenimientos` | `Diagnostico` | Se responde en el checklist, no en campo libre. |
| `MAN_Mantenimientos` | `Trabajo_Realizado` | Se responde en el checklist. |
| `MAN_Mantenimientos` | `Repuestos_Utilizados` | Gestion de repuestos esta fuera de alcance. |
| `MAN_Mantenimientos` | `Requiere_Repuesto` | Se cubre con MotivoPendienteID = Falta de repuesto. |
| `MAN_Mantenimientos` | `Duracion_Minutos` | Se calcula de FechaHoraInicio y FechaHoraFin. |
| `MAN_Mantenimientos` | `Tipo` | El tipo es de la orden, no de la ejecucion. |
| `MAN_Mantenimientos` | `Fecha` | Redundante con FechaHoraInicio. |
| `MAN_Mantenimientos` | `Estado_Intervencion` | Redundante con el estado de la orden. |
| `OT_OrdenesTrabajo` | `FormularioID` | El formulario lo determina el tipo del activo, no la orden. |
| `OT_OrdenesTrabajo` | `Motivo_Cierre` | Se tipifica en MOT_MotivosPendiente desde la ejecucion. |
| `OT_OrdenesTrabajo` | `Informe_Final` | Se genera del mantenimiento y su checklist, no se transcribe. |

---
*Generado. Para actualizarlo, cambie `modelo_objetivo.py` y vuelva a ejecutar el generador.*
