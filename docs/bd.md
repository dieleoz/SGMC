# Diccionario de datos — As-Built

**Generado automáticamente** por `scripts/generar_diccionario_bd.py` desde
`Modelo de Datos (9).xlsx`. No editar a mano.

Describe **lo que la hoja tiene hoy**, no lo que debería tener. El modelo objetivo está en
`ARQUITECTURA_OBJETIVO_SGMC.md`; aquí se marca la distancia entre uno y otro.

La versión anterior de este documento decía «24 hojas» cuando había 32, apuntaba a un Excel
maestro de hace tres días y describía columnas renombradas. Por eso ahora se genera: **la única
forma de que mienta es que mienta el archivo**.

| | |
|---|---|
| Backend de producción | Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc` |
| Aplicación | AppSheet `SGMC-886843353` |
| Hojas | **32** |
| Filas con datos | **259** |
| Generado el | 2026-08-07 |

---

## 1. Qué falta para llegar al modelo objetivo

| Concepto | Cuántos | Dónde se resuelve |
|---|---|---|
| Columnas que siguen siendo `Text` y deben ser `Ref` | **15** | Fase B, `ESPEC-002` |
| Columnas marcadas como retiradas que siguen en la hoja | **45** | Pasada posterior, con datos ya migrados |
| Tablas marcadas como retiradas que siguen en la hoja | 4 | Idem |
| Tablas del modelo objetivo que ya existen | 28 de 28 | — |

**Ninguna de esas columnas se borra todavía a propósito.** La Fase A no borra nada: borrar es lo
único que un respaldo no vuelve gratis.

## 2. Inventario de hojas

| Hoja | Columnas | Filas | En el modelo objetivo |
|---|---|---|---|
| `ACT_Activos` | 17 | 34 | Sí |
| `CAL_Calzadas` | 3 | 2 | Sí |
| `EST_Activo` | 4 | 4 | Sí |
| `FRE_Frecuencias` | 4 | 8 | Sí |
| `SED_Sedes` | 4 | 10 | Sí |
| `SEN_Sentidos` | 3 | 2 | Sí |
| `TIP_TiposActivo` | 8 | 18 | Sí |
| `USR_Usuarios` | 11 | 11 | Sí |
| `ROL_Roles` | 4 | 4 | Sí |
| `OT_OrdenesTrabajo` | 15 | 6 | Sí |
| `MAN_Mantenimientos` | 36 | 2 | Sí |
| `FRM_Formularios` | 6 | 18 | Sí |
| `FRM_Preguntas` | 18 | 15 | Sí |
| `TPR_TiposRespuesta` | 3 | 10 | Sí |
| `FRM_SOS` | 11 | 15 | **Se retira.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_CCTV` | 11 | 15 | **Se retira.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_PMVF` | 11 | 15 | **Se retira.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_Secciones` | 4 | 14 | Sí |
| `LST_ValoresLista` | 5 | 4 | Sí |
| `FIR_Firmas` | 5 | 1 | Sí |
| `FOT_Fotografias` | 9 | 3 | Sí |
| `CHK_Checklists` | 22 | 1 | Sí |
| `GPS` | 8 | 0 | **Se retira.** Duplica Coordenadas_Cierre y Precision_GPS de MAN_Mantenimientos. Nunca recibio un registro. |
| `CHD_ChecklistDetalle` | 21 | 15 | Sí |
| `UNF_UnidadesFuncionales` | 5 | 4 | Sí · **nueva** |
| `EOT_EstadosOrden` | 6 | 7 | Sí · **nueva** |
| `ASG_AsignacionZona` | 4 | 4 | Sí · **nueva** |
| `MOT_MotivosPendiente` | 4 | 5 | Sí · **nueva** |
| `FAL_ModosFalla` | 6 | 5 | Sí · **nueva** |
| `NOV_Novedades` | 9 | 1 | Sí · **nueva** |
| `PLA_PlanMantenimiento` | 7 | 3 | Sí · **nueva** |
| `PAR_Parametros` | 6 | 3 | Sí · **nueva** |

## 3. Parámetros calibrables

Umbrales que el administrador ajusta **en la hoja**, sin abrir el editor de AppSheet. Un
número escondido dentro de una expresión no se puede calibrar.

| Parámetro | Valor en la hoja | Unidad | Declarado en el modelo | Quién lo lee |
|---|---|---|---|---|
| `UMBRAL_GPS` | 40.0 | m | 40 | RG-19 |
| `RADIO_GEOFENCING_KM` | 1.0 | km | 1.0 | RG-01 |
| `DISTANCIA_ESCANEO_CIERRE_KM` | 0.5 | km | 0.5 | RG-13 |

## 4. Detalle por hoja

Leyenda del estado de cada columna:

- **Pendiente `Ref`** — sigue siendo texto y debe pasar a referencia en la Fase B.
- **Retirada** — marcada para eliminar, todavía presente a propósito.
- **Renombrada** — su nombre actual viene de otro anterior; se indica cuál.
- **Fuera del modelo** — está en la hoja y el modelo objetivo no la contempla.

### `ACT_Activos`

Inventario de los activos del corredor. Es el eje del sistema.

17 columnas · 34 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ActivoID` | Text · **PK** |  |
| 2 | `CodigoActivo` | Text |  |
| 3 | `Nombre` | Text |  |
| 4 | `TipoActivoID` | Ref → `TIP_TiposActivo` | **Pendiente `Ref`** hacia `TIP_TiposActivo` (hoy `Number`) |
| 5 | `UnidadFuncionalID` | Ref → `UNF_UnidadesFuncionales` | Antes `SedeID`. Guarda 7 a 10, que en SED_Sedes son UF1 a UF4, es decir unidades funcionales y no sedes. La tabla ya mezclaba los dos conceptos; esto solo lo hace explicito. |
| 6 | `PR` | Text |  |
| 7 | `CalzadaID` | Ref → `CAL_Calzadas` | **Pendiente `Ref`** hacia `CAL_Calzadas` (hoy `Number`) |
| 8 | `Ubicacion` | LatLong |  |
| 9 | `EstadoActivoID` | Ref → `EST_Activo` | Antes `EstadoID`. La referencia se llama como la clave destino. |
| 10 | `CodigoQR` | Text |  |
| 11 | `SentidoID` | Ref → `SEN_Sentidos` | **Pendiente `Ref`** hacia `SEN_Sentidos` (hoy `Number`) |
| 12 | `Activo` | Yes/No |  |
| 13 | `FrecuenciaID` | Ref → `FRE_Frecuencias` | **Pendiente `Ref`** hacia `FRE_Frecuencias` (hoy `Number`) |
| 14 | `Observaciones` | LongText |  |
| 15 | `Criticidad` | Enum |  |
| 16 | `FechaBaja` | Date |  |
| 17 | `MotivoBaja` | Enum |  |

### `CAL_Calzadas`

Calzadas del corredor.

3 columnas · 2 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `CalzadaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `EST_Activo`

Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado.

4 columnas · 4 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `EstadoActivoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `GeneraAlerta` | Yes/No |  |
| 4 | `Activo` | Yes/No |  |

### `FRE_Frecuencias`

Periodicidad del mantenimiento preventivo.

4 columnas · 8 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FrecuenciaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Dias` | Number |  |
| 4 | `Activo` | Yes/No |  |

### `SED_Sedes`

Sedes fisicas donde trabaja el personal: CCO, peajes y basculas.

4 columnas · 10 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SedeID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Ciudad` | Text |  |
| 4 | `Activo` | Yes/No |  |

### `SEN_Sentidos`

Sentidos de circulacion.

3 columnas · 2 filas · clave: `SA`, `AS`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SentidoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `TIP_TiposActivo`

Taxonomia de activos. Determina que checklist abre la aplicacion.

8 columnas · 18 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `TipoActivoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Categoria` | Enum |  |
| 4 | `Activo` | Yes/No |  |
| 5 | `TieneQR` | Yes/No |  |
| 6 | `RequiereGPS` | Yes/No |  |
| 7 | `FormularioID` | Ref → `FRM_Formularios` | **Pendiente `Ref`** hacia `FRM_Formularios` (hoy `Text`) |
| 8 | `RadioGeofencingKm` | Decimal |  |

### `USR_Usuarios`

Personas del sistema. El correo resuelve la sesion contra USEREMAIL().

11 columnas · 11 filas · clave: `2.0`, `3.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `UsuarioID` | Text · **PK** | Antes `usuarioID`. Produccion la escribe en minuscula inicial. AppSheet resuelve por nombre literal. |
| 2 | `Nombres` | Text |  |
| 3 | `Correo` | Email |  |
| 4 | `Cargo` | Text |  |
| 5 | `Iniciales` | Text |  |
| 6 | `RolID` | Ref → `ROL_Roles` | **Pendiente `Ref`** hacia `ROL_Roles` (hoy `Number`) |
| 7 | `SedeID` | Ref → `SED_Sedes` | **Pendiente `Ref`** hacia `SED_Sedes` (hoy `Number`) |
| 8 | `Activo` | Yes/No | Antes `Estado`. Convencion: todas las tablas usan Activo como bandera. |
| 9 | `Telefono` | Phone |  |
| 10 | `FechaIngreso` | Date |  |
| 11 | `UltimaSincronizacion` | — | **Fuera del modelo** |

### `ROL_Roles`

Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta.

4 columnas · 4 filas · clave: `2.0`, `3.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `RolID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Descripcion` | Text | Antes `Descripción`. AppSheet resuelve por nombre literal: la tilde obliga a escribirla en cada expresion. |
| 4 | `Activo` | Yes/No |  |

### `OT_OrdenesTrabajo`

Trabajo programado o levantado sobre un activo.

15 columnas · 6 filas · clave: `OT-0001`, `OT-0002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `OTID` | Text · **PK** | Antes `Numero_OT`. La clave se llamaba distinto de la referencia que la apunta. Ese solo desajuste produjo el checklist huerfano d02d8a3d. |
| 2 | `ActivoID` | Ref → `ACT_Activos` | Antes `Activo`. Guarda enteros que son ActivoID (2, 26, 5, 9, 27, 3). Es la referencia al activo, con nombre que parece una bandera. |
| 3 | `TecnicoID` | Ref → `USR_Usuarios` | Antes `Tecnico`. Guarda enteros que son UsuarioID. |
| 4 | `FechaProgramada` | DateTime | Antes `Fecha Programada`. Los espacios en el nombre obligan a citarlo. |
| 5 | `EstadoOrdenID` | Ref → `EOT_EstadosOrden` | Antes `Estado`. Pasa de texto libre a referencia contra EOT_EstadosOrden. |
| 6 | `Observaciones` | LongText |  |
| 7 | `FormularioID` | — | **Retirada.** El formulario lo determina el tipo del activo, no la orden. |
| 8 | `SupervisorID` | Ref → `USR_Usuarios` | Antes `SupervidorID`. Error de escritura en el encabezado de produccion. |
| 9 | `FechaCierre` | DateTime | Antes `Fecha_Cierre`. Convencion de nombres. |
| 10 | `CerradaPor` | Ref → `USR_Usuarios` | Antes `Cerrada_Por`. Convencion de nombres. |
| 11 | `Motivo_Cierre` | — | **Retirada.** Se tipifica en MOT_MotivosPendiente desde la ejecucion. |
| 12 | `Informe_Final` | — | **Retirada.** Se genera del mantenimiento y su checklist, no se transcribe. |
| 13 | `OTOrigenID` | Ref → `OT_OrdenesTrabajo` |  |
| 14 | `Activo` | Yes/No |  |
| 15 | `Tipo` | Enum |  |

### `MAN_Mantenimientos`

Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia.

36 columnas · 2 filas · clave: `TEST-MTTO-001`, `TEST-MTTO-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `MantenimientoID` | Text · **PK** | Antes `MttoID`. La clave no seguia la convencion <Prefijo>ID legible. |
| 2 | `OTID` | Ref → `OT_OrdenesTrabajo` | **Pendiente `Ref`** hacia `OT_OrdenesTrabajo` (hoy `Text`) |
| 3 | `TecnicoID` | Ref → `USR_Usuarios` | Antes `Tecnico_Asignado`. Pasa a referencia contra USR_Usuarios. |
| 4 | `Fecha` | — | **Retirada.** Redundante con FechaHoraInicio. |
| 5 | `FechaHoraInicio` | DateTime | Antes `Fecha_Hora_Inicio`. Convencion de nombres. |
| 6 | `FechaHoraFin` | DateTime | Antes `Fecha_Hora_Fin`. Convencion de nombres. |
| 7 | `Duracion_Minutos` | — | **Retirada.** Se calcula de FechaHoraInicio y FechaHoraFin. |
| 8 | `Tipo` | — | **Retirada.** El tipo es de la orden, no de la ejecucion. |
| 9 | `Diagnostico` | — | **Retirada.** Se responde en el checklist, no en campo libre. |
| 10 | `Trabajo_Realizado` | — | **Retirada.** Se responde en el checklist. |
| 11 | `Repuestos_Utilizados` | — | **Retirada.** Gestion de repuestos esta fuera de alcance. |
| 12 | `Requiere_Repuesto` | — | **Retirada.** Se cubre con MotivoPendienteID = Falta de repuesto. |
| 13 | `RequiereSegundaVisita` | Yes/No | Antes `Requiere_Segunda_Visita`. Convencion de nombres. |
| 14 | `MotivoPendienteID` | Ref → `MOT_MotivosPendiente` | Antes `Motivo_Pendiente`. Pasa a referencia contra MOT_MotivosPendiente. |
| 15 | `Estado_Intervencion` | — | **Retirada.** Redundante con el estado de la orden. |
| 16 | `Localizacion` | — | **Retirada.** Ambiguo y redundante con Coordenadas_Cierre. |
| 17 | `Imagen_Inicio` | — | **Retirada.** Sustituido por FOT_Fotografias con Tipo=Antes. |
| 18 | `Imagen_Final` | — | **Retirada.** Sustituido por FOT_Fotografias con Tipo=Despues. |
| 19 | `Observaciones` | LongText |  |
| 20 | `Firma_Tecnico` | — | **Retirada.** Sustituido por FIR_Firmas. |
| 21 | `Firma_Supervisor` | — | **Retirada.** El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| 22 | `AprobadoSupervisor` | Yes/No | Antes `Aprobado_Supervisor`. Convencion de nombres. |
| 23 | `UsuarioRegistro` | Text | Antes `Usuario_Registro`. Convencion de nombres. |
| 24 | `FechaHoraRegistro` | ChangeTimestamp | Antes `Fecha_Hora_Registro`. Convencion de nombres. |
| 25 | `Activo` | Yes/No |  |
| 26 | `Coordenadas_Cierre` | LatLong |  |
| 27 | `Precision_GPS` | Number |  |
| 28 | `OrigenApertura` | Enum |  |
| 29 | `UbicacionEscaneo` | LatLong |  |
| 30 | `FechaHoraEscaneo` | DateTime |  |
| 31 | `EstadoActivoID` | Ref → `EST_Activo` |  |
| 32 | `CierreConExcepcion` | Yes/No |  |
| 33 | `MotivoExcepcion` | LongText |  |
| 34 | `ModoFallaID` | Ref → `FAL_ModosFalla` |  |
| 35 | `FechaAprobacion` | DateTime |  |
| 36 | `ObservacionRechazo` | LongText |  |

### `FRM_Formularios`

Registro maestro de los 18 checklists, uno por tipo de activo.

6 columnas · 18 filas · clave: `FRM_SOS`, `FRM_CCTV`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FormularioID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Descripcion` | Text | Antes `Descripción`. Idem. |
| 4 | `Orden` | — | **Fuera del modelo** |
| 5 | `Version` | Number | Antes `Versión`. Idem. |
| 6 | `Activo` | Yes/No |  |

### `FRM_Preguntas`

Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, FRM_CCTV y FRM_PMVF, que eran una arquitectura paralela con otro esquema.

18 columnas · 15 filas · clave: `SOS001`, `SOS002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `PreguntaID` | Text · **PK** |  |
| 2 | `FormularioID` | Ref → `FRM_Formularios` | **Pendiente `Ref`** hacia `FRM_Formularios` (hoy `Text`) |
| 3 | `SeccionID` | Ref → `FRM_Secciones` | **Pendiente `Ref`** hacia `FRM_Secciones` (hoy `Number`) |
| 4 | `Orden` | Number |  |
| 5 | `Pregunta` | Text |  |
| 6 | `TipoRespuestaID` | Ref → `TPR_TiposRespuesta` | **Pendiente `Ref`** hacia `TPR_TiposRespuesta` (hoy `Number`) |
| 7 | `Obligatoria` | Yes/No |  |
| 8 | `ValorMinimo` | Decimal |  |
| 9 | `ValorMaximo` | Decimal |  |
| 10 | `Unidad` | Text |  |
| 11 | `Ayuda` | Text |  |
| 12 | `Activo` | Yes/No |  |
| 13 | `VisibleSi` | Text |  |
| 14 | `RequiereFoto` | Yes/No |  |
| 15 | `RequiereGPS` | — | **Fuera del modelo** |
| 16 | `RequiereFirma` | — | **Fuera del modelo** |
| 17 | `ValorDefecto` | — | **Fuera del modelo** |
| 18 | `Version` | Number |  |

### `TPR_TiposRespuesta`

Tipo de dato esperado en cada respuesta.

3 columnas · 10 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `TipoRespuestaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `FRM_SOS`

**Se retira del modelo.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.

11 columnas · 15 filas · clave: `FRM_SOS`, `FRM_SOS`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FormularioID` | — | **Fuera del modelo** |
| 2 | `Orden` | — | **Fuera del modelo** |
| 3 | `SeccionID` | — | **Fuera del modelo** |
| 4 | `Pregunta` | — | **Fuera del modelo** |
| 5 | `TipoRespuestaID` | — | **Fuera del modelo** |
| 6 | `Obligatoria` | — | **Fuera del modelo** |
| 7 | `ValorMinimo` | — | **Fuera del modelo** |
| 8 | `ValorMaximo` | — | **Fuera del modelo** |
| 9 | `Unidad` | — | **Fuera del modelo** |
| 10 | `Ayuda` | — | **Fuera del modelo** |
| 11 | `Activo` | — | **Fuera del modelo** |

### `FRM_CCTV`

**Se retira del modelo.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.

11 columnas · 15 filas · clave: `FRM_CCTV`, `FRM_CCTV`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FormularioID` | — | **Fuera del modelo** |
| 2 | `Orden` | — | **Fuera del modelo** |
| 3 | `Sección` | — | **Fuera del modelo** |
| 4 | `Pregunta` | — | **Fuera del modelo** |
| 5 | `TipoRespuestaID` | — | **Fuera del modelo** |
| 6 | `Obligatoria` | — | **Fuera del modelo** |
| 7 | `ValorMinimo` | — | **Fuera del modelo** |
| 8 | `ValorMaximo` | — | **Fuera del modelo** |
| 9 | `Unidad` | — | **Fuera del modelo** |
| 10 | `Ayuda` | — | **Fuera del modelo** |
| 11 | `Activo` | — | **Fuera del modelo** |

### `FRM_PMVF`

**Se retira del modelo.** Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira.

11 columnas · 15 filas · clave: `FRM_PMVF`, `FRM_PMVF`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FormularioID` | — | **Fuera del modelo** |
| 2 | `Orden` | — | **Fuera del modelo** |
| 3 | `Sección` | — | **Fuera del modelo** |
| 4 | `Pregunta` | — | **Fuera del modelo** |
| 5 | `TipoRespuestaID` | — | **Fuera del modelo** |
| 6 | `Obligatoria` | — | **Fuera del modelo** |
| 7 | `ValorMinimo` | — | **Fuera del modelo** |
| 8 | `ValorMaximo` | — | **Fuera del modelo** |
| 9 | `Unidad` | — | **Fuera del modelo** |
| 10 | `Ayuda` | — | **Fuera del modelo** |
| 11 | `Activo` | — | **Fuera del modelo** |

### `FRM_Secciones`

Agrupacion de preguntas dentro del formulario.

4 columnas · 14 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SeccionID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Orden` | Number |  |
| 4 | `Activo` | Yes/No |  |

### `LST_ValoresLista`

Opciones de las preguntas de tipo lista.

5 columnas · 4 filas · clave: `1.0`, `2.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ValorListaID` | Text · **PK** | Antes `ListaID`. La clave se llamaba distinto de la convencion. Detectado el 2026-08-07 al verificar la Fase A, no antes. |
| 2 | `PreguntaID` | Ref → `FRM_Preguntas` | **Pendiente `Ref`** hacia `FRM_Preguntas` (hoy `Text`) |
| 3 | `Valor` | Text |  |
| 4 | `Orden` | Number |  |
| 5 | `Activo` | Yes/No |  |

### `FIR_Firmas`

Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor valida aprobando en el portal, no firmando.

5 columnas · 1 filas · clave: `TEST-FIR-001`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FirmaID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` |  |
| 3 | `TipoFirma` | Enum |  |
| 4 | `Imagen` | Signature |  |
| 5 | `FechaHora` | ChangeTimestamp |  |

### `FOT_Fotografias`

Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. Se elige tabla hija y se retiran los campos de imagen embebidos en MAN.

9 columnas · 3 filas · clave: `TEST-FOT-001`, `TEST-FOT-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FotoID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` |  |
| 3 | `Archivo` | Image |  |
| 4 | `Fecha` | — | **Fuera del modelo** |
| 5 | `Usuario` | Text |  |
| 6 | `Tipo` | Enum |  |
| 7 | `Ubicacion` | LatLong |  |
| 8 | `PrecisionGPS` | Number |  |
| 9 | `FechaHora` | ChangeTimestamp |  |

### `CHK_Checklists`

Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la inspeccion es parte de la ejecucion.

22 columnas · 1 filas · clave: `TEST-CHK-001`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ChecklistID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` | Antes `OTID`. Cambia de padre: el checklist cuelga de la ejecucion, no de la orden. La inspeccion es parte de ejecutar. |
| 3 | `FormularioID` | Ref → `FRM_Formularios` | **Pendiente `Ref`** hacia `FRM_Formularios` (hoy `Text`) |
| 4 | `ActivoID` | — | **Retirada.** Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| 5 | `TecnicoID` | — | **Retirada.** Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato de prueba dejo 'Santiago Moreno' en lugar de un identificador. |
| 6 | `FechaCreacion` | — | **Retirada.** Redundante con FechaInicio. |
| 7 | `FechaInicio` | DateTime |  |
| 8 | `FechaFin` | DateTime |  |
| 9 | `Estado` | — | **Retirada.** Sustituido por Finalizado, que produccion ya tiene. |
| 10 | `GPSInicio` | — | **Retirada.** La coordenada es del mantenimiento y de cada fotografia, no del checklist. |
| 11 | `GPSFin` | — | **Retirada.** Idem. |
| 12 | `FirmaTecnico` | — | **Retirada.** Sustituido por FIR_Firmas. |
| 13 | `FirmaSupervisor` | — | **Retirada.** El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| 14 | `PDF` | — | **Retirada.** El informe se genera al enviarlo, no se almacena en la fila. |
| 15 | `FechaEnvioCorreo` | — | **Retirada.** Es traza del bot, no del checklist. |
| 16 | `Observaciones` | — | **Retirada.** La observacion es de la ejecucion o de la respuesta, no del encabezado. |
| 17 | `Activo` | — | **Retirada.** El checklist es parte de su mantenimiento: no se desactiva por separado. |
| 18 | `PreguntaActual` | — | **Retirada.** Estado de la interfaz, no dato. Se deriva de las respuestas. |
| 19 | `TotalPreguntas` | — | **Retirada.** Se cuenta de FRM_Preguntas. |
| 20 | `Porcentaje` | — | **Retirada.** Se calcula. Guardarlo permite que contradiga al detalle. |
| 21 | `Finalizado` | Yes/No |  |
| 22 | `VersionFormulario` | Number |  |

### `GPS`

**Se retira del modelo.** Duplica Coordenadas_Cierre y Precision_GPS de MAN_Mantenimientos. Nunca recibio un registro.

8 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `GPSID` | — | **Fuera del modelo** |
| 2 | `MantenimientoID` | — | **Fuera del modelo** |
| 3 | `Latitud` | — | **Fuera del modelo** |
| 4 | `Longitud` | — | **Fuera del modelo** |
| 5 | `Precisión` | — | **Fuera del modelo** |
| 6 | `Altitud` | — | **Fuera del modelo** |
| 7 | `Proveedor` | — | **Fuera del modelo** |
| 8 | `FechaHora` | — | **Fuera del modelo** |

### `CHD_ChecklistDetalle`

Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su texto: sin eso no hay comparacion historica posible.

21 columnas · 15 filas · clave: `TEST-CHD-001`, `TEST-CHD-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `DetalleID` | Text · **PK** |  |
| 2 | `ChecklistID` | Ref → `CHK_Checklists` | **Pendiente `Ref`** hacia `CHK_Checklists` (hoy `Text`) |
| 3 | `PreguntaID` | Ref → `FRM_Preguntas` | **Pendiente `Ref`** hacia `FRM_Preguntas` (hoy `Text`) |
| 4 | `Orden` | — | **Retirada.** Se alcanza por [PreguntaID].[Orden]. |
| 5 | `TipoRespuestaID` | — | **Retirada.** Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| 6 | `PreguntaActual` | — | **Retirada.** Estado de la interfaz, no dato. |
| 7 | `EstadoPregunta` | — | **Retirada.** Redundante con Contestada. |
| 8 | `TotalPreguntas` | — | **Retirada.** No es del detalle sino del encabezado, y ademas se cuenta. |
| 9 | `RespuestaTexto` | LongText |  |
| 10 | `RespuestaNumero` | Decimal |  |
| 11 | `RespuestaBoolean` | Yes/No |  |
| 12 | `RespuestaLista` | Enum |  |
| 13 | `RespuestaFecha` | — | **Retirada.** Fuera de alcance: ninguna pregunta usa tipo fecha. |
| 14 | `RespuestaHora` | — | **Retirada.** Fuera de alcance: ninguna pregunta usa tipo hora. |
| 15 | `RespuestaFoto` | — | **Retirada.** Sustituido por FOT_Fotografias. |
| 16 | `RespuestaFirma` | — | **Retirada.** Sustituido por FIR_Firmas. |
| 17 | `RespuestaGPS` | — | **Retirada.** La coordenada es del mantenimiento y de cada fotografia. |
| 18 | `Contestada` | Yes/No |  |
| 19 | `FechaRespuesta` | — | **Retirada.** Se deriva del ChangeTimestamp del mantenimiento. |
| 20 | `Observacion` | LongText | Antes `Observaciones`. Singular: es la observacion de una respuesta, no de la tabla. |
| 21 | `Activo` | — | **Retirada.** El detalle es parte de su checklist: no se desactiva por separado. |

### `UNF_UnidadesFuncionales`

Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque son dos conceptos distintos que el modelo anterior mezclaba en una sola columna, dejando usuarios y activos en conjuntos disjuntos.

5 columnas · 4 filas · clave: `7.0`, `8.0`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `UnidadFuncionalID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `PRInicial` | Text |  |
| 4 | `PRFinal` | Text |  |
| 5 | `Activo` | Yes/No |  |

### `EOT_EstadosOrden`

Ciclo de vida de la orden segun el supuesto D-06. Declararlo como catalogo, y no como texto libre, es lo que permite medir cumplimiento.

6 columnas · 7 filas · clave: `Programada`, `Asignada`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `EstadoOrdenID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Orden` | Number |  |
| 4 | `QuienCambia` | Enum |  |
| 5 | `EsFinal` | Yes/No |  |
| 6 | `Activo` | Yes/No |  |

### `ASG_AsignacionZona`

Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: un tecnico puede tener varias, de modo que la relacion es de muchos a muchos y no cabe como columna en USR_Usuarios.

4 columnas · 4 filas · clave: `ASG-01`, `ASG-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `AsignacionID` | Text · **PK** |  |
| 2 | `UsuarioID` | Ref → `USR_Usuarios` |  |
| 3 | `UnidadFuncionalID` | Ref → `UNF_UnidadesFuncionales` |  |
| 4 | `Activo` | Yes/No |  |

### `MOT_MotivosPendiente`

Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no tiene donde declarar por que no pudo terminar, fuerza un cierre falso.

4 columnas · 5 filas · clave: `MOT-01`, `MOT-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `MotivoPendienteID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `GeneraSeguimiento` | Yes/No |  |
| 4 | `Activo` | Yes/No |  |

### `FAL_ModosFalla`

Taxonomia de fallas por tipo de activo. Sin clasificar la falla no hay ingenieria de mantenimiento posible: no se puede calcular tiempo medio entre fallas, ni saber que componente falla mas, ni pasar de correctivo a predictivo.

6 columnas · 5 filas · clave: `FAL-01`, `FAL-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ModoFallaID` | Text · **PK** |  |
| 2 | `TipoActivoID` | Ref → `TIP_TiposActivo` |  |
| 3 | `Nombre` | Text |  |
| 4 | `Componente` | Text |  |
| 5 | `Criticidad` | Enum |  |
| 6 | `Activo` | Yes/No |  |

### `NOV_Novedades`

Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de programacion. Supuesto D-08. Sin esta via los hallazgos se pierden o acaban en WhatsApp, que es lo que el sistema viene a reemplazar.

9 columnas · 1 filas · clave: `TEST-NOV-001`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `NovedadID` | Text · **PK** |  |
| 2 | `UsuarioID` | Ref → `USR_Usuarios` |  |
| 3 | `Tipo` | Enum |  |
| 4 | `Descripcion` | LongText |  |
| 5 | `Ubicacion` | LatLong |  |
| 6 | `Fotografia` | Image |  |
| 7 | `ActivoID` | Ref → `ACT_Activos` |  |
| 8 | `Estado` | Enum |  |
| 9 | `FechaHora` | ChangeTimestamp |  |

### `PLA_PlanMantenimiento`

Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al sistema en gestion de mantenimiento y no en un registro de formularios: de aqui salen las ordenes, en lugar de crearlas a mano una por una.

7 columnas · 3 filas · clave: `PLA-001`, `PLA-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `PlanID` | Text · **PK** |  |
| 2 | `ActivoID` | Ref → `ACT_Activos` |  |
| 3 | `FrecuenciaID` | Ref → `FRE_Frecuencias` |  |
| 4 | `UltimaEjecucion` | Date |  |
| 5 | `ProximaFecha` | Date |  |
| 6 | `ResponsableID` | Ref → `USR_Usuarios` |  |
| 7 | `Activo` | Yes/No |  |

### `PAR_Parametros`

Umbrales que el administrador ajusta con las pruebas de campo, sin tocar la configuracion de la aplicacion. Existe porque un numero magico escondido en una expresion no se puede calibrar: hay que abrir el editor, encontrarlo y arriesgarse a romper la regla. Aqui es una celda.

6 columnas · 3 filas · clave: `UMBRAL_GPS`, `RADIO_GEOFENCING_KM`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ParametroID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Valor` | Decimal |  |
| 4 | `Unidad` | Text |  |
| 5 | `Descripcion` | LongText |  |
| 6 | `Activo` | Yes/No |  |

---
*Documento generado. Para actualizarlo, descarga la hoja a `BD/` y ejecuta*
*`python scripts/generar_diccionario_bd.py "BD/Modelo de Datos (N).xlsx"`.*
