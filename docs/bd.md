# Diccionario de datos — As-Built

**Generado automáticamente** por `scripts/generar_diccionario_bd.py` desde
`Modelo_Datos_PLANTILLA.xlsx`. No editar a mano.

Describe **lo que la hoja tiene hoy**, no lo que debería tener. El modelo objetivo está en
`ARQUITECTURA_OBJETIVO_SGMC.md`; aquí se marca la distancia entre uno y otro.

La versión anterior de este documento decía «24 hojas» cuando había 32, apuntaba a un Excel
maestro de hace tres días y describía columnas renombradas. Por eso ahora se genera: **la única
forma de que mienta es que mienta el archivo**.

| | |
|---|---|
| Backend de producción | Google Sheets `Modelo_Datos_10082026` |
| Aplicación | AppSheet `_SISGA_-323965761` |
| Archivo leído | `Modelo_Datos_PLANTILLA.xlsx` |
| Hojas | **29** |
| Filas con datos | **1007** |
| Generado el | 2026-08-11 |

---

## 1. Qué falta para llegar al modelo objetivo

| Concepto | Cuántos | Dónde se resuelve |
|---|---|---|
| Columnas que siguen siendo `Text` y deben ser `Ref` | **14** | Fase B, `ESPEC-002` |
| Columnas marcadas como retiradas que siguen en la hoja | **49** | Pasada posterior, con datos ya migrados |
| Columnas presentes sin decidir todavía | **0** | Decisión de operación |
| **Total a ocultar al dar de alta las tablas** | **49** | `MANUAL_DESPLIEGUE.md`, anexo |
| Tablas marcadas como retiradas que siguen en la hoja | 0 | Idem |
| Tablas del modelo objetivo que ya existen | 28 de 28 | — |

**Ninguna de esas columnas se borra todavía a propósito.** La Fase A no borra nada: borrar es lo
único que un respaldo no vuelve gratis.

## 2. Inventario de hojas

| Hoja | Columnas | Filas | En el modelo objetivo |
|---|---|---|---|
| `_LEEME` | 1 | 54 | No figura |
| `SED_Sedes` | 9 | 6 | Sí |
| `UNF_UnidadesFuncionales` | 7 | 4 | Sí · **nueva** |
| `ROL_Roles` | 4 | 4 | Sí |
| `USR_Usuarios` | 9 | 11 | Sí |
| `ASG_AsignacionZona` | 4 | 4 | Sí · **nueva** |
| `TIP_TiposActivo` | 8 | 27 | Sí |
| `EST_Activo` | 4 | 4 | Sí |
| `EOT_EstadosOrden` | 6 | 7 | Sí · **nueva** |
| `MOT_MotivosPendiente` | 4 | 5 | Sí · **nueva** |
| `PAR_Parametros` | 6 | 3 | Sí · **nueva** |
| `FRE_Frecuencias` | 4 | 8 | Sí |
| `CAL_Calzadas` | 3 | 3 | Sí |
| `SEN_Sentidos` | 3 | 2 | Sí |
| `ACT_Activos` | 20 | 368 | Sí |
| `OT_OrdenesTrabajo` | 12 | 0 | Sí |
| `MAN_Mantenimientos` | 23 | 0 | Sí |
| `NOV_Novedades` | 9 | 0 | Sí · **nueva** |
| `PLA_PlanMantenimiento` | 7 | 0 | Sí · **nueva** |
| `FAL_ModosFalla` | 6 | 5 | Sí · **nueva** |
| `FOT_Fotografias` | 8 | 0 | Sí |
| `FIR_Firmas` | 5 | 0 | Sí |
| `CHK_Checklists` | 7 | 0 | Sí |
| `CHD_ChecklistDetalle` | 9 | 0 | Sí |
| `FRM_Formularios` | 5 | 27 | Sí |
| `FRM_Secciones` | 4 | 14 | Sí |
| `FRM_Preguntas` | 17 | 333 | Sí |
| `TPR_TiposRespuesta` | 3 | 10 | Sí |
| `LST_ValoresLista` | 5 | 108 | Sí |

## 3. Parámetros calibrables

Umbrales que el administrador ajusta **en la hoja**, sin abrir el editor de AppSheet. Un
número escondido dentro de una expresión no se puede calibrar.

| Parámetro | Valor en la hoja | Unidad | Declarado en el modelo | Quién lo lee |
|---|---|---|---|---|
| `UMBRAL_GPS` | 40 | m | 40 | — |
| `RADIO_GEOFENCING_KM` | 1 | km | 1.0 | RG-01 |
| `DISTANCIA_ESCANEO_CIERRE_KM` | 0.5 | km | 0.5 | RG-13 |

## 4. Detalle por hoja

Leyenda del estado de cada columna:

- **Pendiente `Ref`** — sigue siendo texto y debe pasar a referencia en la Fase B.
- **Retirada** — marcada para eliminar, todavía presente a propósito.
- **Renombrada** — su nombre actual viene de otro anterior; se indica cuál.
- **Fuera del modelo** — está en la hoja y el modelo objetivo no la contempla.

### `_LEEME`

*No figura en el modelo objetivo.*

1 columnas · 54 filas · clave: `28 pestanas de datos mas esta, con la estructura exacta que espera la aplicacion.`, `NO anada ni quite columnas: la aplicacion las lee por nombre.`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `PLANTILLA DE DATOS - SGMC` | — | **Fuera del modelo** |

### `SED_Sedes`

Edificaciones del corredor: CCO, peajes y basculas. Cada una esta al lado de la via, en un PR concreto, y por tanto dentro de una unidad funcional. Es el PADRE DE UBICACION del equipo bajo techo: un servidor, un NAS o una impresora no estan en un punto de la via, estan DENTRO de un edificio, y de el heredan donde estan.

9 columnas · 6 filas · clave: `SED-001`, `SED-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SedeID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Ciudad` | Text |  |
| 4 | `UnidadFuncionalID` | Ref → `UNF_UnidadesFuncionales` |  |
| 5 | `PR` | Text |  |
| 6 | `TramoINVIAS` | Text |  |
| 7 | `PK` | Text |  |
| 8 | `Ubicacion_LatLong` | LatLong |  |
| 9 | `Activo` | Yes/No |  |

### `UNF_UnidadesFuncionales`

Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque son dos conceptos distintos que el modelo anterior mezclaba en una sola columna, dejando usuarios y activos en conjuntos disjuntos.

7 columnas · 4 filas · clave: `UNF-01`, `UNF-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `UnidadFuncionalID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `PKInicial` | Text |  |
| 4 | `PKFinal` | Text |  |
| 5 | `PRInicial` | Text |  |
| 6 | `PRFinal` | Text |  |
| 7 | `Activo` | Yes/No |  |

### `ROL_Roles`

Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta.

4 columnas · 4 filas · clave: `ROL-01`, `ROL-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `RolID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Descripcion` | Text | Antes `Descripción`. AppSheet resuelve por nombre literal: la tilde obliga a escribirla en cada expresion. |
| 4 | `Activo` | Yes/No |  |

### `USR_Usuarios`

Personas del sistema. El correo resuelve la sesion contra USEREMAIL().

9 columnas · 11 filas · clave: `USR-001`, `USR-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `UsuarioID` | Text · **PK** | Antes `usuarioID`. Produccion la escribe en minuscula inicial. AppSheet resuelve por nombre literal. |
| 2 | `Nombres` | Text |  |
| 3 | `Correo` | Email |  |
| 4 | `Cargo` | Text |  |
| 5 | `Iniciales` | Text |  |
| 6 | `RolID` | Ref → `ROL_Roles` | **Pendiente `Ref`** hacia `ROL_Roles` (hoy `Number`) |
| 7 | `Telefono` | Phone |  |
| 8 | `FechaIngreso` | Date |  |
| 9 | `Activo` | Yes/No | Antes `Estado`. Convencion: todas las tablas usan Activo como bandera. |

### `ASG_AsignacionZona`

Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: un tecnico puede tener varias, de modo que la relacion es de muchos a muchos y no cabe como columna en USR_Usuarios.

4 columnas · 4 filas · clave: `ASG-01`, `ASG-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `AsignacionID` | Text · **PK** |  |
| 2 | `UsuarioID` | Ref → `USR_Usuarios` |  |
| 3 | `UnidadFuncionalID` | Ref → `UNF_UnidadesFuncionales` |  |
| 4 | `Activo` | Yes/No |  |

### `TIP_TiposActivo`

Taxonomia de activos. Determina que checklist abre la aplicacion.

8 columnas · 27 filas · clave: `TIP-001`, `TIP-002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `TipoActivoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Categoria` | Enum |  |
| 4 | `FormularioID` | Ref → `FRM_Formularios` | **Pendiente `Ref`** hacia `FRM_Formularios` (hoy `Text`) |
| 5 | `TieneQR` | Yes/No |  |
| 6 | `RequiereGPS` | Yes/No |  |
| 7 | `RadioGeofencingKm` | Decimal |  |
| 8 | `Activo` | Yes/No |  |

### `EST_Activo`

Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado.

4 columnas · 4 filas · clave: `EST-01`, `EST-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `EstadoActivoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `GeneraAlerta` | Yes/No |  |
| 4 | `Activo` | Yes/No |  |

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

### `MOT_MotivosPendiente`

Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no tiene donde declarar por que no pudo terminar, fuerza un cierre falso.

4 columnas · 5 filas · clave: `MOT-01`, `MOT-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `MotivoPendienteID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `GeneraSeguimiento` | Yes/No |  |
| 4 | `Activo` | Yes/No |  |

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

### `FRE_Frecuencias`

Periodicidad del mantenimiento preventivo.

4 columnas · 8 filas · clave: `FRE-01`, `FRE-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FrecuenciaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Dias` | Number |  |
| 4 | `Activo` | Yes/No |  |

### `CAL_Calzadas`

Calzadas del corredor.

3 columnas · 3 filas · clave: `CAL-01`, `CAL-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `CalzadaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `SEN_Sentidos`

Sentidos de circulacion.

3 columnas · 2 filas · clave: `SA`, `AS`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SentidoID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `ACT_Activos`

Inventario de los activos del corredor. Es el eje del sistema.

20 columnas · 368 filas · clave: `ACT-0001`, `ACT-0002`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ActivoID` | Text · **PK** |  |
| 2 | `CodigoActivo` | Text |  |
| 3 | `Nombre` | Text |  |
| 4 | `TipoActivoID` | Ref → `TIP_TiposActivo` | **Pendiente `Ref`** hacia `TIP_TiposActivo` (hoy `Number`) |
| 5 | `UnidadFuncionalID` | Ref → `UNF_UnidadesFuncionales` |  |
| 6 | `PR` | Text |  |
| 7 | `CalzadaID` | Ref → `CAL_Calzadas` | **Pendiente `Ref`** hacia `CAL_Calzadas` (hoy `Number`) |
| 8 | `SentidoID` | Ref → `SEN_Sentidos` | **Pendiente `Ref`** hacia `SEN_Sentidos` (hoy `Number`) |
| 9 | `Ubicacion_LatLong` | LatLong |  |
| 10 | `PK` | Text |  |
| 11 | `TramoINVIAS` | Text |  |
| 12 | `SedeID` | Ref → `SED_Sedes` |  |
| 13 | `EstadoActivoID` | Ref → `EST_Activo` | Antes `EstadoID`. La referencia se llama como la clave destino. |
| 14 | `CodigoQR` | Text |  |
| 15 | `FrecuenciaID` | Ref → `FRE_Frecuencias` | **Pendiente `Ref`** hacia `FRE_Frecuencias` (hoy `Number`) |
| 16 | `Criticidad` | Enum |  |
| 17 | `FechaBaja` | Date |  |
| 18 | `MotivoBaja` | Enum |  |
| 19 | `Activo` | Yes/No |  |
| 20 | `Observaciones` | LongText |  |

### `OT_OrdenesTrabajo`

Trabajo programado o levantado sobre un activo.

12 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `OTID` | Text · **PK** | Antes `Numero_OT`. La clave se llamaba distinto de la referencia que la apunta. Ese solo desajuste produjo el checklist huerfano d02d8a3d. |
| 2 | `ActivoID` | Ref → `ACT_Activos` | Antes `Activo`. Guarda enteros que son ActivoID (2, 26, 5, 9, 27, 3). Es la referencia al activo, con nombre que parece una bandera. |
| 3 | `TecnicoID` | Ref → `USR_Usuarios` | Antes `Tecnico`. Guarda enteros que son UsuarioID. |
| 4 | `SupervisorID` | Ref → `USR_Usuarios` | Antes `SupervidorID`. Error de escritura en el encabezado de produccion. |
| 5 | `Tipo` | Enum |  |
| 6 | `FechaProgramada` | DateTime | Antes `Fecha Programada`. Los espacios en el nombre obligan a citarlo. |
| 7 | `EstadoOrdenID` | Ref → `EOT_EstadosOrden` | Antes `Estado`. Pasa de texto libre a referencia contra EOT_EstadosOrden. |
| 8 | `OTOrigenID` | Ref → `OT_OrdenesTrabajo` |  |
| 9 | `Observaciones` | LongText |  |
| 10 | `FechaCierre` | DateTime | Antes `Fecha_Cierre`. Convencion de nombres. |
| 11 | `CerradaPor` | Ref → `USR_Usuarios` | Antes `Cerrada_Por`. Convencion de nombres. |
| 12 | `Activo` | Yes/No |  |

### `MAN_Mantenimientos`

Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia.

23 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `MantenimientoID` | Text · **PK** | Antes `MttoID`. La clave no seguia la convencion <Prefijo>ID legible. |
| 2 | `OTID` | Ref → `OT_OrdenesTrabajo` | **Pendiente `Ref`** hacia `OT_OrdenesTrabajo` (hoy `Text`) |
| 3 | `TecnicoID` | Ref → `USR_Usuarios` | Antes `Tecnico_Asignado`. Pasa a referencia contra USR_Usuarios. |
| 4 | `FechaHoraInicio` | DateTime | Antes `Fecha_Hora_Inicio`. Convencion de nombres. |
| 5 | `FechaHoraFin` | DateTime | Antes `Fecha_Hora_Fin`. Convencion de nombres. |
| 6 | `OrigenApertura` | Enum |  |
| 7 | `UbicacionEscaneo_LatLong` | LatLong |  |
| 8 | `FechaHoraEscaneo` | DateTime |  |
| 9 | `EstadoActivoID` | Ref → `EST_Activo` |  |
| 10 | `Coordenadas_Cierre_LatLong` | LatLong |  |
| 11 | `Precision_GPS` | — | **Retirada.** USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1): la columna nunca se poblaba, RG-19 comparaba siempre numero > blanco y RG-03 no pedia MotivoExcepcion nunca. Retirada por ESPEC-004/ORDEN-004. Si MAN_Mantenimientos ya estaba dada de alta en el editor con esta columna sin usar (Rama A, ESPEC-004 2.10), retirarla del modelo no la borra de la hoja: queda huerfana, sin Initial value y sin uso, y eso no es un fallo (ACTA-004; PRUEBA-004 P-45). Si ya estaba cableada con Initial value puesto (Rama B), hace falta Delete and re-add de la tabla completa (ESPEC-004 2.10). |
| 12 | `CierreConExcepcion` | Yes/No |  |
| 13 | `MotivoExcepcion` | LongText |  |
| 14 | `RequiereSegundaVisita` | Yes/No | Antes `Requiere_Segunda_Visita`. Convencion de nombres. |
| 15 | `MotivoPendienteID` | Ref → `MOT_MotivosPendiente` | Antes `Motivo_Pendiente`. Pasa a referencia contra MOT_MotivosPendiente. |
| 16 | `ModoFallaID` | Ref → `FAL_ModosFalla` |  |
| 17 | `Observaciones` | LongText |  |
| 18 | `AprobadoSupervisor` | Yes/No | Antes `Aprobado_Supervisor`. Convencion de nombres. |
| 19 | `FechaAprobacion` | DateTime |  |
| 20 | `ObservacionRechazo` | LongText |  |
| 21 | `UsuarioRegistro` | Text | Antes `Usuario_Registro`. Convencion de nombres. |
| 22 | `FechaHoraRegistro` | ChangeTimestamp | Antes `Fecha_Hora_Registro`. Convencion de nombres. |
| 23 | `Activo` | Yes/No |  |

### `NOV_Novedades`

Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de programacion. Supuesto D-08. Sin esta via los hallazgos se pierden o acaban en WhatsApp, que es lo que el sistema viene a reemplazar.

9 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `NovedadID` | Text · **PK** |  |
| 2 | `UsuarioID` | Ref → `USR_Usuarios` |  |
| 3 | `Tipo` | Enum |  |
| 4 | `Descripcion` | LongText |  |
| 5 | `Ubicacion_LatLong` | LatLong |  |
| 6 | `Fotografia` | Image |  |
| 7 | `ActivoID` | Ref → `ACT_Activos` |  |
| 8 | `Estado` | Enum |  |
| 9 | `FechaHora` | ChangeTimestamp |  |

### `PLA_PlanMantenimiento`

Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al sistema en gestion de mantenimiento y no en un registro de formularios: de aqui salen las ordenes, en lugar de crearlas a mano una por una.

7 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `PlanID` | Text · **PK** |  |
| 2 | `ActivoID` | Ref → `ACT_Activos` |  |
| 3 | `FrecuenciaID` | Ref → `FRE_Frecuencias` |  |
| 4 | `UltimaEjecucion` | Date |  |
| 5 | `ProximaFecha` | Date |  |
| 6 | `ResponsableID` | Ref → `USR_Usuarios` |  |
| 7 | `Activo` | Yes/No |  |

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

### `FOT_Fotografias`

Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. Se elige tabla hija y se retiran los campos de imagen embebidos en MAN.

8 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FotoID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` |  |
| 3 | `Tipo` | Enum |  |
| 4 | `Archivo` | Image |  |
| 5 | `Ubicacion_LatLong` | LatLong |  |
| 6 | `PrecisionGPS` | Number |  |
| 7 | `FechaHora` | ChangeTimestamp |  |
| 8 | `Usuario` | Text |  |

### `FIR_Firmas`

Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor valida aprobando en el portal, no firmando.

5 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FirmaID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` |  |
| 3 | `TipoFirma` | Enum |  |
| 4 | `Imagen` | Signature |  |
| 5 | `FechaHora` | ChangeTimestamp |  |

### `CHK_Checklists`

Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la inspeccion es parte de la ejecucion.

7 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ChecklistID` | Text · **PK** |  |
| 2 | `MantenimientoID` | Ref → `MAN_Mantenimientos` | Antes `OTID`. Cambia de padre: el checklist cuelga de la ejecucion, no de la orden. La inspeccion es parte de ejecutar. |
| 3 | `FormularioID` | Ref → `FRM_Formularios` | **Pendiente `Ref`** hacia `FRM_Formularios` (hoy `Text`) |
| 4 | `VersionFormulario` | Number |  |
| 5 | `FechaInicio` | DateTime |  |
| 6 | `FechaFin` | DateTime |  |
| 7 | `Finalizado` | Yes/No |  |

### `CHD_ChecklistDetalle`

Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su texto: sin eso no hay comparacion historica posible.

9 columnas · 0 filas · clave: vacía

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `DetalleID` | Text · **PK** |  |
| 2 | `ChecklistID` | Ref → `CHK_Checklists` | **Pendiente `Ref`** hacia `CHK_Checklists` (hoy `Text`) |
| 3 | `PreguntaID` | Ref → `FRM_Preguntas` | **Pendiente `Ref`** hacia `FRM_Preguntas` (hoy `Text`) |
| 4 | `RespuestaTexto` | LongText |  |
| 5 | `RespuestaNumero` | Decimal |  |
| 6 | `RespuestaBoolean` | Yes/No |  |
| 7 | `RespuestaLista` | Enum |  |
| 8 | `Contestada` | Yes/No |  |
| 9 | `Observacion` | LongText | Antes `Observaciones`. Singular: es la observacion de una respuesta, no de la tabla. |

### `FRM_Formularios`

Registro maestro de los checklists, uno por tipo de activo: 27 en BD/Modelo_Datos_PLANTILLA.xlsx, 18 en la hoja de produccion.

5 columnas · 27 filas · clave: `FRM_SOS`, `FRM_CCTV`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `FormularioID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Descripcion` | Text | Antes `Descripción`. Idem. |
| 4 | `Version` | Number | Antes `Versión`. Idem. |
| 5 | `Activo` | Yes/No |  |

### `FRM_Secciones`

Agrupacion de preguntas dentro del formulario.

4 columnas · 14 filas · clave: `SEC-01`, `SEC-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `SeccionID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Orden` | Number |  |
| 4 | `Activo` | Yes/No |  |

### `FRM_Preguntas`

Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, FRM_CCTV y FRM_PMVF, que eran una arquitectura paralela con otro esquema.

17 columnas · 333 filas · clave: `SOS001`, `SOS002`

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
| 12 | `VisibleSi` | Text |  |
| 13 | `RequiereFoto` | Yes/No |  |
| 14 | `Version` | Number |  |
| 15 | `RequiereGPS` | Yes/No |  |
| 16 | `RequiereFirma` | Yes/No |  |
| 17 | `Activo` | Yes/No |  |

### `TPR_TiposRespuesta`

Tipo de dato esperado en cada respuesta.

3 columnas · 10 filas · clave: `TPR-01`, `TPR-02`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `TipoRespuestaID` | Text · **PK** |  |
| 2 | `Nombre` | Text |  |
| 3 | `Activo` | Yes/No |  |

### `LST_ValoresLista`

Opciones de las preguntas de tipo lista.

5 columnas · 108 filas · clave: `SOS001-1`, `SOS001-2`

| # | Columna | Tipo objetivo | Estado |
|---|---|---|---|
| 1 | `ValorListaID` | Text · **PK** | Antes `ListaID`. La clave se llamaba distinto de la convencion. Detectado el 2026-08-07 al verificar la Fase A, no antes. |
| 2 | `PreguntaID` | Ref → `FRM_Preguntas` | **Pendiente `Ref`** hacia `FRM_Preguntas` (hoy `Text`) |
| 3 | `Valor` | Text |  |
| 4 | `Orden` | Number |  |
| 5 | `Activo` | Yes/No |  |

---
*Documento generado. Para actualizarlo, descarga la hoja a `BD/` y ejecuta*
*`python scripts/generar_diccionario_bd.py "BD/Modelo_Datos_PLANTILLA.xlsx"`.*
