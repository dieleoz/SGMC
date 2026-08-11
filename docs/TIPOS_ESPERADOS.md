# Qué tipo debe tener cada columna

**Generado** por `scripts/generar_tipos_esperados.py`. No editar a mano.

---

Esta lista existe porque **ningún script del repositorio puede comprobarla**. La API v2 de
AppSheet devuelve **filas, no esquema**: no hay forma de preguntarle de qué tipo es una columna.
Se mira en `Data > Columns`, columna por columna, contra esto.

## Por qué AppSheet se equivoca, y cómo

Infiere el tipo de **dos** señales, y aquí las dos fallan:

- **Sin contenido cae en `Text`.** Ocho tablas llegaron vacías, así que sus columnas enteras se
  tiparon a ciegas. En las tablas pobladas pasa igual con cada columna vacía.
- **Con contenido, el nombre puede mandar sobre el dato.** Es la señal que aprovechamos al
  renombrar a `_LatLong` — y que mordió al revés: **`Precision_GPS` salió `LatLong`** porque su
  nombre lleva `GPS`, cuando son los metros de precisión, un `Number`.

> **Lo que cuesta no mirarlo.** `RG-03` quedó puesta y bien escrita —`[CierreConExcepcion] = TRUE`
> en `Required_If`— sobre una columna que AppSheet tipó `Text`. Comparar texto contra el booleano
> `TRUE` es **siempre falso y no da error**: el motivo de excepción no se pide nunca, y el técnico
> cierra con excepción sin justificar. La regla existe, está bien redactada, y no hace nada.

## Empieza por estas 88

Son las que AppSheet tuvo que adivinar. **El resto también hay que mirarlo**, pero si el tiempo
es poco, aquí está donde se concentra el error.

| Tabla | Columna | Debe ser | Reglas que la usan | Por qué pudo salir mal |
|---|---|---|---|---|
| `SED_Sedes` | `PK` | **`Text`** | — | la columna está **vacía en las 6 filas** |
| `SED_Sedes` | `Ubicacion_LatLong` | **`LatLong`** | — | la columna está **vacía en las 6 filas** |
| `TIP_TiposActivo` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a **LatLong**, y no lo es |
| `EST_Activo` | `GeneraAlerta` | **`Yes/No`** | `RG-06` | la columna está **vacía en las 4 filas** |
| `ACT_Activos` | `PR` | **`Text`** | — | la columna está **vacía en las 368 filas** |
| `ACT_Activos` | `TramoINVIAS` | **`Text`** | — | la columna está **vacía en las 368 filas** |
| `ACT_Activos` | `SedeID` | **`Ref`** | `RG-34` | la columna está **vacía en las 368 filas** |
| `ACT_Activos` | `Criticidad` | **`Enum`** | — | la columna está **vacía en las 368 filas** |
| `OT_OrdenesTrabajo` | `OTID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `ActivoID` | **`Ref`** | `RG-01`, `RG-35` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `TecnicoID` | **`Ref`** | `RG-05` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `SupervisorID` | **`Ref`** | `RG-05` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `Tipo` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `FechaProgramada` | **`DateTime`** | `RG-35`, `RG-37` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | **`Ref`** | `RG-37` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `OTOrigenID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `Observaciones` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `FechaCierre` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `CerradaPor` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `OT_OrdenesTrabajo` | `Activo` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `MantenimientoID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `OTID` | **`Ref`** | `RG-01` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `TecnicoID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `FechaHoraInicio` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `FechaHoraFin` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `OrigenApertura` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `UbicacionEscaneo_LatLong` | **`LatLong`** | `RG-13` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `FechaHoraEscaneo` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `EstadoActivoID` | **`Ref`** | `RG-06` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | **`LatLong`** | `RG-01`, `RG-13` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `CierreConExcepcion` | **`Yes/No`** | `RG-03` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `MotivoExcepcion` | **`LongText`** | `RG-03` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `RequiereSegundaVisita` | **`Yes/No`** | `RG-10` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `MotivoPendienteID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `ModoFallaID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `Observaciones` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `AprobadoSupervisor` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `FechaAprobacion` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `ObservacionRechazo` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `UsuarioRegistro` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | **`ChangeTimestamp`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato; su nombre dispara la inferencia a **Date o DateTime**, y no lo es |
| `MAN_Mantenimientos` | `Activo` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `NovedadID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `UsuarioID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `Tipo` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `Descripcion` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `Ubicacion_LatLong` | **`LatLong`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `Fotografia` | **`Image`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `ActivoID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `Estado` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `NOV_Novedades` | `FechaHora` | **`ChangeTimestamp`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato; su nombre dispara la inferencia a **Date o DateTime**, y no lo es |
| `PLA_PlanMantenimiento` | `PlanID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `ActivoID` | **`Ref`** | `RG-36` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | **`Ref`** | `RG-11`, `RG-36` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `UltimaEjecucion` | **`Date`** | `RG-11` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `ProximaFecha` | **`Date`** | `RG-11`, `RG-38` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `ResponsableID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `PLA_PlanMantenimiento` | `Activo` | **`Yes/No`** | `RG-38` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `FotoID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `MantenimientoID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `Tipo` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `Archivo` | **`Image`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `Ubicacion_LatLong` | **`LatLong`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FOT_Fotografias` | `FechaHora` | **`ChangeTimestamp`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato; su nombre dispara la inferencia a **Date o DateTime**, y no lo es |
| `FOT_Fotografias` | `Usuario` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FIR_Firmas` | `FirmaID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FIR_Firmas` | `MantenimientoID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FIR_Firmas` | `TipoFirma` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FIR_Firmas` | `Imagen` | **`Signature`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FIR_Firmas` | `FechaHora` | **`ChangeTimestamp`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato; su nombre dispara la inferencia a **Date o DateTime**, y no lo es |
| `CHK_Checklists` | `ChecklistID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `MantenimientoID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `FormularioID` | **`Ref`** | `RG-09` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `VersionFormulario` | **`Number`** | `RG-09` | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `FechaInicio` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `FechaFin` | **`DateTime`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHK_Checklists` | `Finalizado` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `DetalleID` | **`Text`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `ChecklistID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `PreguntaID` | **`Ref`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `RespuestaTexto` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `RespuestaNumero` | **`Decimal`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `RespuestaBoolean` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `RespuestaLista` | **`Enum`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `Contestada` | **`Yes/No`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `CHD_ChecklistDetalle` | `Observacion` | **`LongText`** | — | la tabla llegó **vacía**: el tipo se eligió sin un solo dato |
| `FRM_Preguntas` | `VisibleSi` | **`Text`** | — | la columna está **vacía en las 333 filas** |
| `FRM_Preguntas` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a **LatLong**, y no lo es |

> **La columna «reglas que la usan» es la que ordena el trabajo.** Una columna con el tipo mal y
> sin ninguna regla encima molesta al usuario. Una columna con el tipo mal y una regla encima
> **rompe la regla en silencio**, que es lo que no se puede permitir.

## Todas, tabla por tabla

### `ACT_Activos` — 368 filas

| Columna | Tipo | |
|---|---|---|
| `ActivoID` | **`Text`** | **clave** |
| `CodigoActivo` | **`Text`** | obligatoria |
| `Nombre` | **`Text`** | obligatoria |
| `TipoActivoID` | **`Ref`** | → `TIP_TiposActivo` · obligatoria |
| `UnidadFuncionalID` | **`Ref`** | → `UNF_UnidadesFuncionales` · obligatoria |
| `PR` | **`Text`** |  |
| `CalzadaID` | **`Ref`** | → `CAL_Calzadas` |
| `SentidoID` | **`Ref`** | → `SEN_Sentidos` |
| `Ubicacion_LatLong` | **`LatLong`** | obligatoria |
| `PK` | **`Text`** |  |
| `TramoINVIAS` | **`Text`** |  |
| `SedeID` | **`Ref`** | → `SED_Sedes` |
| `EstadoActivoID` | **`Ref`** | → `EST_Activo` · obligatoria |
| `CodigoQR` | **`Text`** |  |
| `FrecuenciaID` | **`Ref`** | → `FRE_Frecuencias` |
| `Criticidad` | **`Enum`** | valores: `Alta` · `Media` · `Baja` |
| `FechaBaja` | **`Date`** |  |
| `MotivoBaja` | **`Enum`** | valores: `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` |
| `Activo` | **`Yes/No`** |  |
| `Observaciones` | **`LongText`** |  |

### `ASG_AsignacionZona` — 4 filas

| Columna | Tipo | |
|---|---|---|
| `AsignacionID` | **`Text`** | **clave** |
| `UsuarioID` | **`Ref`** | → `USR_Usuarios` · obligatoria |
| `UnidadFuncionalID` | **`Ref`** | → `UNF_UnidadesFuncionales` · obligatoria |
| `Activo` | **`Yes/No`** |  |

### `CAL_Calzadas` — 3 filas

| Columna | Tipo | |
|---|---|---|
| `CalzadaID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `CHD_ChecklistDetalle` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `DetalleID` | **`Text`** | **clave** |
| `ChecklistID` | **`Ref`** | → `CHK_Checklists` · obligatoria |
| `PreguntaID` | **`Ref`** | → `FRM_Preguntas` · obligatoria |
| `RespuestaTexto` | **`LongText`** |  |
| `RespuestaNumero` | **`Decimal`** |  |
| `RespuestaBoolean` | **`Yes/No`** |  |
| `RespuestaLista` | **`Enum`** |  |
| `Contestada` | **`Yes/No`** |  |
| `Observacion` | **`LongText`** |  |

### `CHK_Checklists` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `ChecklistID` | **`Text`** | **clave** |
| `MantenimientoID` | **`Ref`** | → `MAN_Mantenimientos` · obligatoria |
| `FormularioID` | **`Ref`** | → `FRM_Formularios` · obligatoria |
| `VersionFormulario` | **`Number`** | obligatoria |
| `FechaInicio` | **`DateTime`** |  |
| `FechaFin` | **`DateTime`** |  |
| `Finalizado` | **`Yes/No`** |  |

### `EOT_EstadosOrden` — 7 filas

| Columna | Tipo | |
|---|---|---|
| `EstadoOrdenID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Orden` | **`Number`** |  |
| `QuienCambia` | **`Enum`** | valores: `Sistema` · `Tecnico` · `Supervisor` |
| `EsFinal` | **`Yes/No`** |  |
| `Activo` | **`Yes/No`** |  |

### `EST_Activo` — 4 filas

| Columna | Tipo | |
|---|---|---|
| `EstadoActivoID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `GeneraAlerta` | **`Yes/No`** |  |
| `Activo` | **`Yes/No`** |  |

### `FAL_ModosFalla` — 5 filas

| Columna | Tipo | |
|---|---|---|
| `ModoFallaID` | **`Text`** | **clave** |
| `TipoActivoID` | **`Ref`** | → `TIP_TiposActivo` · obligatoria |
| `Nombre` | **`Text`** | obligatoria |
| `Componente` | **`Text`** |  |
| `Criticidad` | **`Enum`** | valores: `Alta` · `Media` · `Baja` |
| `Activo` | **`Yes/No`** |  |

### `FIR_Firmas` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `FirmaID` | **`Text`** | **clave** |
| `MantenimientoID` | **`Ref`** | → `MAN_Mantenimientos` · obligatoria |
| `TipoFirma` | **`Enum`** | obligatoria · valores: `Tecnico` |
| `Imagen` | **`Signature`** | obligatoria |
| `FechaHora` | **`ChangeTimestamp`** |  |

### `FOT_Fotografias` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `FotoID` | **`Text`** | **clave** |
| `MantenimientoID` | **`Ref`** | → `MAN_Mantenimientos` · obligatoria |
| `Tipo` | **`Enum`** | obligatoria · valores: `Antes` · `Despues` · `Novedad` |
| `Archivo` | **`Image`** | obligatoria |
| `Ubicacion_LatLong` | **`LatLong`** | obligatoria |
| `FechaHora` | **`ChangeTimestamp`** |  |
| `Usuario` | **`Text`** |  |

### `FRE_Frecuencias` — 8 filas

| Columna | Tipo | |
|---|---|---|
| `FrecuenciaID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Dias` | **`Number`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `FRM_Formularios` — 27 filas

| Columna | Tipo | |
|---|---|---|
| `FormularioID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Descripcion` | **`Text`** |  |
| `Version` | **`Number`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `FRM_Preguntas` — 333 filas

| Columna | Tipo | |
|---|---|---|
| `PreguntaID` | **`Text`** | **clave** |
| `FormularioID` | **`Ref`** | → `FRM_Formularios` · obligatoria |
| `SeccionID` | **`Ref`** | → `FRM_Secciones` · obligatoria |
| `Orden` | **`Number`** | obligatoria |
| `Pregunta` | **`Text`** | obligatoria |
| `TipoRespuestaID` | **`Ref`** | → `TPR_TiposRespuesta` · obligatoria |
| `Obligatoria` | **`Yes/No`** |  |
| `ValorMinimo` | **`Decimal`** |  |
| `ValorMaximo` | **`Decimal`** |  |
| `Unidad` | **`Text`** |  |
| `Ayuda` | **`Text`** |  |
| `VisibleSi` | **`Text`** |  |
| `RequiereFoto` | **`Yes/No`** |  |
| `Version` | **`Number`** |  |
| `RequiereGPS` | **`Yes/No`** |  |
| `RequiereFirma` | **`Yes/No`** |  |
| `Activo` | **`Yes/No`** |  |

### `FRM_Secciones` — 14 filas

| Columna | Tipo | |
|---|---|---|
| `SeccionID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Orden` | **`Number`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `LST_ValoresLista` — 108 filas

| Columna | Tipo | |
|---|---|---|
| `ValorListaID` | **`Text`** | **clave** |
| `PreguntaID` | **`Ref`** | → `FRM_Preguntas` · obligatoria |
| `Valor` | **`Text`** | obligatoria |
| `Orden` | **`Number`** |  |
| `Activo` | **`Yes/No`** |  |

### `MAN_Mantenimientos` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `MantenimientoID` | **`Text`** | **clave** |
| `OTID` | **`Ref`** | → `OT_OrdenesTrabajo` · obligatoria |
| `TecnicoID` | **`Ref`** | → `USR_Usuarios` · obligatoria |
| `FechaHoraInicio` | **`DateTime`** | obligatoria |
| `FechaHoraFin` | **`DateTime`** |  |
| `OrigenApertura` | **`Enum`** | valores: `QR` · `Lista` |
| `UbicacionEscaneo_LatLong` | **`LatLong`** |  |
| `FechaHoraEscaneo` | **`DateTime`** |  |
| `EstadoActivoID` | **`Ref`** | → `EST_Activo` · obligatoria |
| `Coordenadas_Cierre_LatLong` | **`LatLong`** | obligatoria |
| `CierreConExcepcion` | **`Yes/No`** |  |
| `MotivoExcepcion` | **`LongText`** |  |
| `RequiereSegundaVisita` | **`Yes/No`** |  |
| `MotivoPendienteID` | **`Ref`** | → `MOT_MotivosPendiente` |
| `ModoFallaID` | **`Ref`** | → `FAL_ModosFalla` |
| `Observaciones` | **`LongText`** |  |
| `AprobadoSupervisor` | **`Yes/No`** |  |
| `FechaAprobacion` | **`DateTime`** |  |
| `ObservacionRechazo` | **`LongText`** |  |
| `UsuarioRegistro` | **`Text`** |  |
| `FechaHoraRegistro` | **`ChangeTimestamp`** |  |
| `Activo` | **`Yes/No`** |  |

### `MOT_MotivosPendiente` — 5 filas

| Columna | Tipo | |
|---|---|---|
| `MotivoPendienteID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `GeneraSeguimiento` | **`Yes/No`** |  |
| `Activo` | **`Yes/No`** |  |

### `NOV_Novedades` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `NovedadID` | **`Text`** | **clave** |
| `UsuarioID` | **`Ref`** | → `USR_Usuarios` · obligatoria |
| `Tipo` | **`Enum`** | obligatoria · valores: `Activo no inventariado` · `Falla detectada` |
| `Descripcion` | **`LongText`** | obligatoria |
| `Ubicacion_LatLong` | **`LatLong`** | obligatoria |
| `Fotografia` | **`Image`** | obligatoria |
| `ActivoID` | **`Ref`** | → `ACT_Activos` |
| `Estado` | **`Enum`** | valores: `Reportada` · `Aceptada` · `Descartada` |
| `FechaHora` | **`ChangeTimestamp`** |  |

### `OT_OrdenesTrabajo` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `OTID` | **`Text`** | **clave** |
| `ActivoID` | **`Ref`** | → `ACT_Activos` · obligatoria |
| `TecnicoID` | **`Ref`** | → `USR_Usuarios` · obligatoria |
| `SupervisorID` | **`Ref`** | → `USR_Usuarios` · obligatoria |
| `Tipo` | **`Enum`** | obligatoria · valores: `Preventivo` · `Correctivo` |
| `FechaProgramada` | **`DateTime`** | obligatoria |
| `EstadoOrdenID` | **`Ref`** | → `EOT_EstadosOrden` · obligatoria |
| `OTOrigenID` | **`Ref`** | → `OT_OrdenesTrabajo` |
| `Observaciones` | **`LongText`** |  |
| `FechaCierre` | **`DateTime`** |  |
| `CerradaPor` | **`Ref`** | → `USR_Usuarios` |
| `Activo` | **`Yes/No`** |  |

### `PAR_Parametros` — 3 filas

| Columna | Tipo | |
|---|---|---|
| `ParametroID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Valor` | **`Decimal`** | obligatoria |
| `Unidad` | **`Text`** |  |
| `Descripcion` | **`LongText`** |  |
| `Activo` | **`Yes/No`** |  |

### `PLA_PlanMantenimiento` — **tabla vacía: todos sus tipos se eligieron a ciegas**

| Columna | Tipo | |
|---|---|---|
| `PlanID` | **`Text`** | **clave** |
| `ActivoID` | **`Ref`** | → `ACT_Activos` · obligatoria |
| `FrecuenciaID` | **`Ref`** | → `FRE_Frecuencias` · obligatoria |
| `UltimaEjecucion` | **`Date`** |  |
| `ProximaFecha` | **`Date`** | obligatoria |
| `ResponsableID` | **`Ref`** | → `USR_Usuarios` |
| `Activo` | **`Yes/No`** |  |

### `ROL_Roles` — 4 filas

| Columna | Tipo | |
|---|---|---|
| `RolID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Descripcion` | **`Text`** |  |
| `Activo` | **`Yes/No`** |  |

### `SED_Sedes` — 6 filas

| Columna | Tipo | |
|---|---|---|
| `SedeID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Ciudad` | **`Text`** |  |
| `UnidadFuncionalID` | **`Ref`** | → `UNF_UnidadesFuncionales` · obligatoria |
| `PR` | **`Text`** |  |
| `TramoINVIAS` | **`Text`** |  |
| `PK` | **`Text`** |  |
| `Ubicacion_LatLong` | **`LatLong`** |  |
| `Activo` | **`Yes/No`** |  |

### `SEN_Sentidos` — 2 filas

| Columna | Tipo | |
|---|---|---|
| `SentidoID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `TIP_TiposActivo` — 27 filas

| Columna | Tipo | |
|---|---|---|
| `TipoActivoID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Categoria` | **`Enum`** | valores: `ITS` · `Electrico` · `Comunicaciones` · `TI` |
| `FormularioID` | **`Ref`** | → `FRM_Formularios` · obligatoria |
| `TieneQR` | **`Yes/No`** |  |
| `RequiereGPS` | **`Yes/No`** |  |
| `RadioGeofencingKm` | **`Decimal`** |  |
| `Activo` | **`Yes/No`** |  |

### `TPR_TiposRespuesta` — 10 filas

| Columna | Tipo | |
|---|---|---|
| `TipoRespuestaID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `Activo` | **`Yes/No`** |  |

### `UNF_UnidadesFuncionales` — 4 filas

| Columna | Tipo | |
|---|---|---|
| `UnidadFuncionalID` | **`Text`** | **clave** |
| `Nombre` | **`Text`** | obligatoria |
| `PKInicial` | **`Text`** |  |
| `PKFinal` | **`Text`** |  |
| `PRInicial` | **`Text`** |  |
| `PRFinal` | **`Text`** |  |
| `Activo` | **`Yes/No`** |  |

### `USR_Usuarios` — 11 filas

| Columna | Tipo | |
|---|---|---|
| `UsuarioID` | **`Text`** | **clave** |
| `Nombres` | **`Text`** | obligatoria |
| `Correo` | **`Email`** | obligatoria |
| `Cargo` | **`Text`** |  |
| `Iniciales` | **`Text`** |  |
| `RolID` | **`Ref`** | → `ROL_Roles` · obligatoria |
| `Telefono` | **`Phone`** |  |
| `FechaIngreso` | **`Date`** |  |
| `Activo` | **`Yes/No`** |  |

## Al terminar

No hay comando que cierre esto. Lo único que se puede hacer es dejar constancia: **anota qué tipo
tenía cada una antes de cambiarla**. Si mañana algo se comporta raro, esa lista es la única forma
de saber si lo tocamos nosotros.

Y lo que sí se puede comprobar después, porque un cambio de tipo puede disparar una escritura:

```bash
python scripts/instantanea.py guardar despues-de-los-tipos
python scripts/instantanea.py comparar antes-de-fase-c despues-de-los-tipos
```
