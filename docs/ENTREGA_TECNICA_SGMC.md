# Entrega tecnica — reconstruccion del SGMC en AppSheet

**Este es el documento de entrada.** Dice que hay, en que estado, y el paso a paso para
terminarlo. Todo lo demas son anexos.

| | |
|---|---|
| Sistema | Gestion de Mantenimiento en Campo · Concesion Transversal del Sisga |
| Backend | Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc` |
| Fuente del modelo | `scripts/modelo_objetivo.py` — **unica**. Los documentos se generan de ahi |
| Fecha | 2026-08-09 |

## Lo primero, en tres frases

**La hoja esta bien y la aplicacion esta desfasada.** El modelo de datos se corrigio en el
Sheets —27 columnas renombradas, 8 tablas nuevas, 45 campos retirados— y AppSheet conserva
todavia el esquema anterior.

**No se arregla con `Regenerate`.** La documentacion de AppSheet dice que al regenerar *combina*
la informacion nueva con la existente y **mantiene las columnas viejas**. Lo comprobamos: la tabla
de ordenes sobrevivio a varios `Regenerate` con sus nombres de antes.

**El procedimiento es borrar cada tabla y volver a darla de alta**, y despues reponer la capa de
expresiones desde una lista escrita. Lo indica el propio AppSheet: *Delete and re-add the table
to create the column structure*.

---

## 1. Que leer, y en que orden

| # | Documento | Para que |
|---|---|---|
| 1 | [`FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md) | Que hace el sistema, para quien y por que. **Su §6 es el registro de decisiones**: una sola forma por proposito |
| 2 | [`bd.md`](bd.md) | Diccionario de datos As-Built. **Generado del archivo**: la unica forma de que mienta es que mienta la hoja |
| 3 | [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) | La lista de reposicion: 27 nombres viejos, 20 reglas, 28 claves, 15 retipados |
| 4 | [`sdd/ESPEC-002-cableado-en-appsheet.md`](sdd/ESPEC-002-cableado-en-appsheet.md) | El detalle del cableado de referencias, con sus 17 pruebas |
| 5 | [`BASE_CONOCIMIENTO_APPSHEET.md`](BASE_CONOCIMIENTO_APPSHEET.md) | 11 comportamientos de la plataforma verificados contra la fuente, con su URL |
| 6 | [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md) | Como se mantiene el corredor de verdad. De donde sale el modelo |

**Si solo lee uno, que sea el 3.** Es la lista contra la que se valida el trabajo.

## 2. El modelo de datos

**28 tablas.** La fuente es `scripts/modelo_objetivo.py`; este inventario sale de ahi.

### Catalogos

| Tabla | Columnas | Proposito |
|---|---|---|
| `ASG_AsignacionZona` · **nueva** | 4 | Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: un tecnico puede tener varias... |
| `CAL_Calzadas` | 3 | Calzadas del corredor. |
| `EOT_EstadosOrden` · **nueva** | 6 | Ciclo de vida de la orden segun el supuesto D-06. Declararlo como catalogo, y no como texto libre, es l... |
| `EST_Activo` | 4 | Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado. |
| `FAL_ModosFalla` · **nueva** | 6 | Taxonomia de fallas por tipo de activo. Sin clasificar la falla no hay ingenieria de mantenimiento posi... |
| `FRE_Frecuencias` | 4 | Periodicidad del mantenimiento preventivo. |
| `MOT_MotivosPendiente` · **nueva** | 4 | Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no tiene donde declarar por que... |
| `PAR_Parametros` · **nueva** | 6 | Umbrales que el administrador ajusta con las pruebas de campo, sin tocar la configuracion de la aplicac... |
| `ROL_Roles` | 4 | Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta. |
| `SED_Sedes` | 4 | Sedes fisicas donde trabaja el personal: CCO, peajes y basculas. |
| `SEN_Sentidos` | 3 | Sentidos de circulacion. |
| `TIP_TiposActivo` | 8 | Taxonomia de activos. Determina que checklist abre la aplicacion. |
| `UNF_UnidadesFuncionales` · **nueva** | 5 | Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque son dos conceptos distintos ... |
| `USR_Usuarios` | 10 | Personas del sistema. El correo resuelve la sesion contra USEREMAIL(). |

### Maestras

| Tabla | Columnas | Proposito |
|---|---|---|
| `ACT_Activos` | 17 | Inventario de los activos del corredor. Es el eje del sistema. |

### Transaccionales

| Tabla | Columnas | Proposito |
|---|---|---|
| `MAN_Mantenimientos` | 23 | Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia. |
| `NOV_Novedades` · **nueva** | 9 | Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de programacion. Supuesto D-08. ... |
| `OT_OrdenesTrabajo` | 12 | Trabajo programado o levantado sobre un activo. |
| `PLA_PlanMantenimiento` · **nueva** | 7 | Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al sistema en gestion de man... |

### Evidencias

| Tabla | Columnas | Proposito |
|---|---|---|
| `FIR_Firmas` | 5 | Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor valida aprobando en el portal... |
| `FOT_Fotografias` | 8 | Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. Se elige tabla hija y se... |

### Checklist

| Tabla | Columnas | Proposito |
|---|---|---|
| `CHD_ChecklistDetalle` | 9 | Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su texto: sin eso no hay compara... |
| `CHK_Checklists` | 7 | Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la inspeccion es parte de la eje... |

### Formularios

| Tabla | Columnas | Proposito |
|---|---|---|
| `FRM_Formularios` | 5 | Registro maestro de los 18 checklists, uno por tipo de activo. |
| `FRM_Preguntas` | 15 | Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, FRM_CCTV y FRM_PMVF, que er... |
| `FRM_Secciones` | 4 | Agrupacion de preguntas dentro del formulario. |
| `LST_ValoresLista` | 5 | Opciones de las preguntas de tipo lista. |
| `TPR_TiposRespuesta` | 3 | Tipo de dato esperado en cada respuesta. |

### Como se regenera la documentacion

```bash
python scripts/generar_diccionario_bd.py "BD/Modelo de Datos (N).xlsx"
```

**Nada se documenta a mano.** El diccionario anterior decia 24 hojas cuando habia 32 y describia
columnas renombradas dos dias antes. Por eso se genera.

## 3. El procedimiento, paso a paso

### Antes de empezar

1. **Respaldo del Sheets.** Nombrelo con la fecha.
2. **Anote la version actual de la app.** Es el punto de retorno.
3. **Que nadie use la aplicacion ni edite la hoja** mientras dure. La reversion solo es limpia si
   nadie escribe.
4. **Descargue la hoja a `BD/`** y ejecute la verificacion de partida:

```bash
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"   # debe decir FASE A CERRADA
python scripts/validar_modelo.py                                  # debe dar 0 errores
```

### Paso 1 — Limpieza

Borre de AppSheet las tablas que el modelo ya no contempla: `GPS`, `SEC_Secciones` y las
`FRM_SOS` / `FRM_CCTV` / `FRM_PMVF` individuales.

**Borrar la tabla en AppSheet no borra la hoja.** El dato se queda.

> **Ojo con `FRM_CCTV` y `FRM_PMVF`:** tienen 15 preguntas cada una que **nunca se migraron** a
> `FRM_Preguntas`, que solo tiene las 15 de `FRM_SOS`. Son 30 preguntas que hay que migrar antes
> o despues. No es bloqueante, pero no se puede olvidar.

### Paso 2 — Borrar y volver a dar de alta cada tabla

**Una por una.** Si AppSheet infiere mal una clave, hay que saber en cual.

```
menu triple punto -> Delete        +  -> Add data -> la hoja -> la pestana
```

**Y sin parar entre las dos.** Mientras la tabla no existe, todo lo que la referencia grita mas
fuerte: es ruido temporal.

**El orden importa: de abajo hacia arriba.** Una tabla con errores desaparece para las que la
referencian, asi que empezando por arriba parece que no se avanza.

```
1. Catalogos      CAL_Calzadas · SEN_Sentidos · EST_Activo · FRE_Frecuencias
                  TPR_TiposRespuesta · ROL_Roles · SED_Sedes · UNF_UnidadesFuncionales
                  EOT_EstadosOrden · MOT_MotivosPendiente · FAL_ModosFalla · PAR_Parametros
2. Formularios    FRM_Formularios · FRM_Secciones · FRM_Preguntas · LST_ValoresLista
3. Maestras       TIP_TiposActivo · USR_Usuarios · ASG_AsignacionZona
4. Activos        ACT_Activos
5. Ordenes        OT_OrdenesTrabajo · PLA_PlanMantenimiento · NOV_Novedades
6. Ejecucion      MAN_Mantenimientos · CHK_Checklists · CHD_ChecklistDetalle
                  FOT_Fotografias · FIR_Firmas
```

### Paso 3 — Las claves, en la misma sesion

**Esto es lo unico que no se puede recuperar despues.** Al dar de alta una tabla, AppSheet elige
clave por su cuenta: examina las columnas de izquierda a derecha y, **si ninguna le sirve, combina
dos en una clave compuesta**. Contra una clave compuesta no resuelve ninguna referencia.

| Tabla | Clave | Tipo |
|---|---|---|
| `ACT_Activos` | `ActivoID` | `Text` |
| `ASG_AsignacionZona` | `AsignacionID` | `Text` |
| `CAL_Calzadas` | `CalzadaID` | `Text` |
| `CHD_ChecklistDetalle` | `DetalleID` | `Text` |
| `CHK_Checklists` | `ChecklistID` | `Text` |
| `EOT_EstadosOrden` | `EstadoOrdenID` | `Text` |
| `EST_Activo` | `EstadoActivoID` | `Text` |
| `FAL_ModosFalla` | `ModoFallaID` | `Text` |
| `FIR_Firmas` | `FirmaID` | `Text` |
| `FOT_Fotografias` | `FotoID` | `Text` |
| `FRE_Frecuencias` | `FrecuenciaID` | `Text` |
| `FRM_Formularios` | `FormularioID` | `Text` |
| `FRM_Preguntas` | `PreguntaID` | `Text` |
| `FRM_Secciones` | `SeccionID` | `Text` |
| `LST_ValoresLista` | `ValorListaID` | `Text` |
| `MAN_Mantenimientos` | `MantenimientoID` | `Text` |
| `MOT_MotivosPendiente` | `MotivoPendienteID` | `Text` |
| `NOV_Novedades` | `NovedadID` | `Text` |
| `OT_OrdenesTrabajo` | `OTID` | `Text` |
| `PAR_Parametros` | `ParametroID` | `Text` |
| `PLA_PlanMantenimiento` | `PlanID` | `Text` |
| `ROL_Roles` | `RolID` | `Text` |
| `SED_Sedes` | `SedeID` | `Text` |
| `SEN_Sentidos` | `SentidoID` | `Text` |
| `TIP_TiposActivo` | `TipoActivoID` | `Text` |
| `TPR_TiposRespuesta` | `TipoRespuestaID` | `Text` |
| `UNF_UnidadesFuncionales` | `UnidadFuncionalID` | `Text` |
| `USR_Usuarios` | `UsuarioID` | `Text` |

**Todas `Text`, sin excepcion.** El caso que lo justifica es `USR_Usuarios.UsuarioID`: tiene un
valor `3aa202ee` entre diez numericos. Si AppSheet infiere `Number`, esa fila queda sin clave
valida y su usuario deja de existir para el sistema.

**Una sola casilla `KEY` por tabla.** Si quedan dos, quite la sobrante.

### Paso 4 — Generacion de clave para filas nuevas

Sin esto la aplicacion no sabe que identificador poner al crear un registro.

| Tabla | Columna | `Initial value` |
|---|---|---|
| `MAN_Mantenimientos` | `MantenimientoID` | `UNIQUEID()` |
| `FOT_Fotografias` | `FotoID` | `UNIQUEID()` |
| `FIR_Firmas` | `FirmaID` | `UNIQUEID()` |
| `CHK_Checklists` | `ChecklistID` | `UNIQUEID()` |
| `CHD_ChecklistDetalle` | `DetalleID` | `UNIQUEID()` |
| `NOV_Novedades` | `NovedadID` | `UNIQUEID()` |

### Paso 5 — Las referencias

**15 columnas pasan de texto o numero a `Ref`.** Primero la clave del destino, despues quien la
apunta.

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

**Convertir `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave del destino.**
Las demas quedan huerfanas **sin mensaje de error**: la celda se queda en blanco. Despues de cada
conversion, mire si aparecieron blancos donde habia valores.

**Se valida en el Asistente de Expresiones, no ejercitando la aplicacion.** La que sostiene el
geofencing es esta:

```
[OTID].[ActivoID].[Ubicacion]
```

Si el asistente la rechaza, pare.

### Paso 6 — Reponer las reglas

**20 reglas.** Estan en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md)
§2 con su expresion completa. Aqui solo el mapa:

| # | Tabla | Columna | Tipo |
|---|---|---|---|
| RG-01 | `MAN_Mantenimientos` | `Coordenadas_Cierre` | Valid_If |
| RG-02 | `MAN_Mantenimientos` | `Precision_GPS` | Initial value |
| RG-03 | `MAN_Mantenimientos` | `MotivoExcepcion` | Required_If |
| RG-04 | `ACT_Activos` | `(tabla)` | Security Filter |
| RG-05 | `OT_OrdenesTrabajo` | `(tabla)` | Security Filter |
| RG-06 | `MAN_Mantenimientos` | `(tabla)` | Bot |
| RG-07 | `OT_OrdenesTrabajo` | `(tabla)` | Bot |
| RG-08 | `OT_OrdenesTrabajo` | `EstadoOrdenID` | Bot programado |
| RG-09 | `CHK_Checklists` | `VersionFormulario` | Initial value |
| RG-11 | `PLA_PlanMantenimiento` | `ProximaFecha` | App formula |
| RG-12 | `PLA_PlanMantenimiento` | `(tabla)` | Bot programado |
| RG-13 | `MAN_Mantenimientos` | `(tabla)` | Verificacion de evidencia |
| RG-20 | `MAN_Mantenimientos` | `(varias)` | Editable_If |
| RG-19 | `MAN_Mantenimientos` | `CierreConExcepcion` | App formula |
| RG-16 | `ACT_Activos` | `Activo` | App formula |
| RG-17 | `ACT_Activos` | `FechaBaja` | Required_If |
| RG-18 | `ACT_Activos` | `(tabla)` | Doctrina de reportes |
| RG-14 | `OT_OrdenesTrabajo` | `(tabla)` | Are updates allowed |
| RG-15 | `MAN_Mantenimientos` | `(tabla)` | Are updates allowed |
| RG-10 | `MAN_Mantenimientos` | `(tabla)` | Bot |

**Cuatro no se pueden ejecutar en el plan gratuito** — las de tipo Bot y Bot programado. Se dejan
escritas y se activan cuando se decida el licenciamiento.

### Paso 7 — Verificar

**No se declara cerrado por el reporte de quien lo hizo.** Este proyecto tiene tres cierres
reportados que no resistieron la comprobacion contra el archivo, y las tres veces lo paro un
script.

```bash
python scripts/validar_modelo.py                                  # el modelo consigo mismo
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"   # el modelo contra la hoja
python scripts/verificar_documentos.py                            # la prosa contra el modelo
```

Y las **17 pruebas de aceptacion** de [`sdd/PRUEBA-002-cableado-en-appsheet.md`](sdd/PRUEBA-002-cableado-en-appsheet.md),
con sus cuatro innegociables: `P-05`, `P-09`, `P-12` y `P-16`.

## 4. Lo que NO cabe en el plan gratuito

No es mas adelante: es **no en el plan actual**. Solo cambia con la decision de licenciamiento.

| Lo que se querria | Por que no |
|---|---|
| Generacion automatica de las ordenes del mes | Los procesos programados no se ejecutan |
| Aviso al supervisor de que hay trabajo por recibir | Lo mismo |
| Integracion con el SCADA para abrir correctivas | Sin plan Core no hay API REST |
| Atributos distintos por tipo de equipo | El backend es una hoja: no hay esquema dinamico |
| Que una escritura directa en la hoja respete las validaciones | Imposible por diseno |

**Y el volumen:** AppSheet degrada por encima de ~50.000 filas por tabla. Con el inventario real
`CHD_ChecklistDetalle` llega a 143.700 filas en cinco anos. **Archivar por ano no es opcional.**

## 5. Lo que viene despues, y no esta construido

**9 tablas propuestas**, especificadas en `ESPEC-003` y pendientes de que su bloqueo se levante:

| Tabla | Para que |
|---|---|
| `CER_Certificaciones` | Catalogo de certificaciones: alturas, electricista, electronico, ayudante, SISO |
| `CRI_Criticidad` | Criticidad de una correctiva y sus plazos de respuesta y resolucion, para no enterrar los num... |
| `ETR_Estructuras` | Puentes y viaductos por los que pasa la fibra y que exigen revision propia |
| `EVT_EventosOrden` | Transiciones de estado de la orden, solo-anadir. De aqui salen los tiempos de respuesta y res... |
| `MED_MedicionesHilo` | Los 48 hilos de una medicion de ODF. Hija del checklist, como FOT_Fotografias y FIR_Firmas |
| `PAU_Pausas` | Pausas y reanudaciones de una orden. Tabla hija solo-anadir: el reloj parado se DERIVA con SU... |
| `ROL_Requeridos` | Que rol exige cada tarea. Los doce roles ya estan en ROL_Roles; lo que falta es colgarlos de ... |
| `TAR_Tareas` | Un tipo de equipo tiene VARIAS tareas, cada una con su periodicidad y su formulario. Hoy la p... |
| `USR_Certificaciones` | Usuario x certificacion, con vigencia. Un certificado de alturas caduca, y eso es una regla c... |

**La mas importante es `TAR_Tareas`.** Hoy el modelo asume que un activo tiene *una* frecuencia y
un tipo tiene *un* formulario. En la operacion real un poste SOS tiene prueba semanal, prueba
mensual con interventoria y mantenimiento trimestral. **La periodicidad es de la tarea, no del
activo.**

## 6. Reglas de trabajo del proyecto

Estan en `CLAUDE.md`. Las tres que mas han evitado desastres:

**No se declara nada conforme por reporte. Se verifica contra el archivo, y se dice contra cual.**

**Quien aplica un cambio no toca la comprobacion que lo mide.** Si una validacion estorba, se
endurece o se sustituye por la inversa; no se retira.

**Una sola forma por proposito.** Antes de proponer un mecanismo, se comprueba si ya existe uno
—`FUNCIONAL_SGMC.md` §6—. Si el nuevo es mejor, se retira el viejo en el mismo cambio.

---
*Documento generado de `scripts/modelo_objetivo.py`. Para actualizarlo, cambie el modelo y vuelva*
*a generar.*
