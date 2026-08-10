> # Documento historico. NO SE APLICA.
>
> Instructivo de la Fase B. **Lo sustituye `docs/MANUAL_DESPLIEGUE.md`**, que trae la ficha de las 28 tablas, y `docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md` para lo que falta.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# Prompt para el agente de AppSheet — cablear la app nueva

Autocontenido. Cópialo íntegro desde la línea siguiente.

> **Nota de alcance, 2026-08-09.** Este prompt sustituye al anterior, que listaba **15 referencias**.
> Esas 15 eran correctas para **convertir la aplicación existente**, donde otras 23 ya estaban
> puestas. La aplicación se reconstruyó desde cero, así que **no hay ninguna heredada: son 38**.
> `ESPEC-002` sigue siendo válida para lo que norma; lo que le faltaba era declarar desde qué punto
> de partida.

---

Vas a terminar de configurar una aplicación de **Google AppSheet** recién creada sobre una hoja de
cálculo. La aplicación se llama **SISGA** y su fuente es el libro **`Modelo_Datos_09082026`**.

Las tablas ya están dadas de alta. Tu trabajo es **poner los tipos y las referencias**. No creas
tablas, no borras columnas, no cambias datos.

## Lo único que tienes que entender antes de empezar

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

De ahí salen tres reglas:

1. **Primero la clave del destino, después quien la apunta.** Por eso la lista va en orden y hay que
   respetarlo.
2. **Convertir a `Ref` conserva solo las filas cuyo valor coincide con la clave del destino.** Las
   demás quedan huérfanas **sin mensaje de error**: la celda se queda en blanco. *(Ya se midió sobre
   estos datos: no hay ninguna huérfana. Aun así, mira si aparecen blancos.)*
3. **Se valida en el Asistente de Expresiones, no ejercitando la aplicación.**

## Paso 1 — Las claves, todas `Text`

En *Data > Columns* de cada tabla: **una sola casilla `KEY` marcada**, sobre la columna correcta, y
su tipo en **`Text`**.

```
ACT_Activos ActivoID          ASG_AsignacionZona AsignacionID    CAL_Calzadas CalzadaID
CHD_ChecklistDetalle DetalleID CHK_Checklists ChecklistID        EOT_EstadosOrden EstadoOrdenID
EST_Activo EstadoActivoID     FAL_ModosFalla ModoFallaID         FIR_Firmas FirmaID
FOT_Fotografias FotoID        FRE_Frecuencias FrecuenciaID       FRM_Formularios FormularioID
FRM_Preguntas PreguntaID      FRM_Secciones SeccionID            LST_ValoresLista ValorListaID
MAN_Mantenimientos MantenimientoID  MOT_MotivosPendiente MotivoPendienteID
NOV_Novedades NovedadID       OT_OrdenesTrabajo OTID             PAR_Parametros ParametroID
PLA_PlanMantenimiento PlanID  ROL_Roles RolID                    SED_Sedes SedeID
SEN_Sentidos SentidoID        TIP_TiposActivo TipoActivoID       TPR_TiposRespuesta TipoRespuestaID
UNF_UnidadesFuncionales UnidadFuncionalID  USR_Usuarios UsuarioID
```

**`Text` sin excepción.** El caso que lo justifica es `USR_Usuarios.UsuarioID`: tiene un valor
`3aa202ee` entre diez numéricos. Si AppSheet infiere `Number`, esa fila se queda sin clave válida y
ese usuario deja de existir para el sistema.

**Si ves dos casillas `KEY` marcadas, o la clave aparece como combinación de columnas, corrígelo
antes de seguir.** Contra una clave compuesta no resuelve ninguna referencia.

## Paso 2 — Los tipos que AppSheet no adivina

Vienen de una hoja, así que llegan como texto o número.

| Tabla | Columna | Tipo |
|---|---|---|
| `ACT_Activos` | `Ubicacion` | `LatLong` |
| `ACT_Activos` | `FechaBaja` | `Date` |
| `ACT_Activos` | `Activo` | `Yes/No` |
| `MAN_Mantenimientos` | `Coordenadas_Cierre` | `LatLong` |
| `MAN_Mantenimientos` | `UbicacionEscaneo` | `LatLong` |
| `MAN_Mantenimientos` | `Precision_GPS` | `Number` |
| `MAN_Mantenimientos` | `CierreConExcepcion` | `Yes/No` |
| `MAN_Mantenimientos` | `OrigenApertura` | `Enum` — valores `QR`, `Lista` |
| `OT_OrdenesTrabajo` | `Tipo` | `Enum` — valores `Preventivo`, `Correctivo` |
| `FOT_Fotografias` | `Ubicacion` | `LatLong` |
| `FOT_Fotografias` | `Archivo` | `Image` |
| `FIR_Firmas` | `Imagen` | `Signature` |
| `NOV_Novedades` | `Ubicacion` | `LatLong` |

**`Coordenadas_Cierre` es la más importante.** Sobre ella se monta el geofencing, y `DISTANCE()` no
funciona si la columna es texto.

## Paso 3 — Las 38 referencias, en este orden

El orden no es arbitrario: cada nivel apunta a tablas cuyas claves quedaron fijadas antes.

### Nivel 1 — Formularios

```
FRM_Preguntas.FormularioID        -> FRM_Formularios
FRM_Preguntas.SeccionID           -> FRM_Secciones
FRM_Preguntas.TipoRespuestaID     -> TPR_TiposRespuesta
LST_ValoresLista.PreguntaID       -> FRM_Preguntas
```

### Nivel 2 — Maestras

```
TIP_TiposActivo.FormularioID      -> FRM_Formularios
USR_Usuarios.RolID                -> ROL_Roles
USR_Usuarios.SedeID               -> SED_Sedes
ASG_AsignacionZona.UsuarioID      -> USR_Usuarios
ASG_AsignacionZona.UnidadFuncionalID -> UNF_UnidadesFuncionales
FAL_ModosFalla.TipoActivoID       -> TIP_TiposActivo
```

### Nivel 3 — Activos

```
ACT_Activos.TipoActivoID          -> TIP_TiposActivo
ACT_Activos.UnidadFuncionalID     -> UNF_UnidadesFuncionales
ACT_Activos.CalzadaID             -> CAL_Calzadas
ACT_Activos.SentidoID             -> SEN_Sentidos
ACT_Activos.EstadoActivoID        -> EST_Activo
ACT_Activos.FrecuenciaID          -> FRE_Frecuencias
```

### Nivel 4 — Órdenes

```
OT_OrdenesTrabajo.ActivoID        -> ACT_Activos
OT_OrdenesTrabajo.TecnicoID       -> USR_Usuarios
OT_OrdenesTrabajo.SupervisorID    -> USR_Usuarios
OT_OrdenesTrabajo.EstadoOrdenID   -> EOT_EstadosOrden
OT_OrdenesTrabajo.CerradaPor      -> USR_Usuarios
PLA_PlanMantenimiento.ActivoID    -> ACT_Activos
PLA_PlanMantenimiento.FrecuenciaID -> FRE_Frecuencias
PLA_PlanMantenimiento.ResponsableID -> USR_Usuarios
NOV_Novedades.UsuarioID           -> USR_Usuarios
NOV_Novedades.ActivoID            -> ACT_Activos
```

### Nivel 5 — Ejecución

```
MAN_Mantenimientos.OTID           -> OT_OrdenesTrabajo     IsPartOf = FALSE
MAN_Mantenimientos.TecnicoID      -> USR_Usuarios
MAN_Mantenimientos.EstadoActivoID -> EST_Activo
MAN_Mantenimientos.MotivoPendienteID -> MOT_MotivosPendiente
MAN_Mantenimientos.ModoFallaID    -> FAL_ModosFalla
CHK_Checklists.MantenimientoID    -> MAN_Mantenimientos     IsPartOf = TRUE
CHK_Checklists.FormularioID       -> FRM_Formularios
CHD_ChecklistDetalle.ChecklistID  -> CHK_Checklists         IsPartOf = TRUE
CHD_ChecklistDetalle.PreguntaID   -> FRM_Preguntas
FOT_Fotografias.MantenimientoID   -> MAN_Mantenimientos     IsPartOf = TRUE
FIR_Firmas.MantenimientoID        -> MAN_Mantenimientos     IsPartOf = TRUE
```

### Y la última, aparte

```
OT_OrdenesTrabajo.OTOrigenID      -> OT_OrdenesTrabajo
```

Apunta a su propia tabla, para encadenar una orden derivada con la que la originó. Déjala para el
final.

## `IsPartOf` va marcado en cuatro, y en ninguna más

```
CHK_Checklists.MantenimientoID    TRUE
CHD_ChecklistDetalle.ChecklistID  TRUE
FOT_Fotografias.MantenimientoID   TRUE
FIR_Firmas.MantenimientoID        TRUE
```

**`MAN_Mantenimientos.OTID` va DESMARCADO, y es deliberado.** Con `IsPartOf`, borrar una orden
borraría su ejecución, sus fotografías y su firma en cascada. En un sistema cuyo propósito es que la
evidencia sea difícil de falsificar, eso se decide, no se hereda de un ejemplo.

## Paso 4 — Tres columnas que AppSheet convierte solo, y están mal

Son columnas muertas que siguen en la hoja y **se llaman igual que la clave de otra tabla**. AppSheet
infiere referencias por coincidencia de nombre, así que las convierte a `Ref` sin que nadie se lo
pida:

```
CHK_Checklists.ActivoID
CHD_ChecklistDetalle.TipoRespuestaID
OT_OrdenesTrabajo.FormularioID
```

**Déjalas en `Text` y desmarca `Show?`.** Si se quedan como `Ref`, crean rutas de navegación que el
modelo prohíbe y aparecen en la aplicación como si fueran buenas.

Un aviso del tipo *«was set to be unsearchable because it is Hidden»* es **normal y correcto**:
confirma que la columna quedó oculta.

## Paso 5 — Las reglas

**Geofencing** — en `MAN_Mantenimientos.Coordenadas_Cierre`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= 1.0
Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.
Editable_If:    FALSE
```

**El `1.0` es literal a propósito.** El modelo prevé un radio por tipo de activo, pero esa columna
está vacía en los 18 tipos: usar la versión por tipo compararía contra una celda en blanco y
**rechazaría también los cierres legítimos**.

**Excepción por GPS deficiente** — en `MAN_Mantenimientos.CierreConExcepcion`:

```
App formula:  [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")
```

**No editable** — en `MAN_Mantenimientos`, pon `Editable_If = FALSE` en las cuatro:

```
Coordenadas_Cierre · Precision_GPS · UbicacionEscaneo · FechaHoraEscaneo
```

Sin esto el geofencing es decorativo: el técnico arrastra el pin del mapa y cierra desde donde
quiera.

**Baja de activos** — en `ACT_Activos.Activo`:

```
App formula:  [EstadoActivoID].[Nombre] <> "Retirado"
```

**Filtros de seguridad** — en *Data > Tables > [tabla] > Security Filter*:

```
ACT_Activos:
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID],
   AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))

OT_OrdenesTrabajo:
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

## Paso 6 — Comprobar

**En el Asistente de Expresiones, sobre `MAN_Mantenimientos`:**

```
[OTID].[ActivoID].[Ubicacion]
```

**Si sale en verde, la cadena navega.** Si lo rechaza, alguna de las tres referencias del camino no
está puesta — casi siempre `OT_OrdenesTrabajo.ActivoID`, que la lista antigua de 15 no incluía.

Y una segunda, que prueba el otro extremo:

```
[OTID].[TecnicoID].[Correo]
```

**Después, cuenta.** En cada tabla, las columnas de tipo `Ref` deben sumar **38** en total. Si salen
15, se siguió la lista antigua.

## Lo que NO debes hacer

- **No crees ni borres tablas.**
- **No borres columnas.** Las que sobran se ocultan con `Show? = FALSE`.
- **No toques `Precision_GPS` del registro `TEST-MTTO-002`.** Vale `45` y está bien: es la fila que
  prueba el rechazo por GPS deficiente.
- **No pongas radios de geofencing por tipo.** Van en otra fase.
- **No modifiques ninguna comprobación para que algo pase.**

## Cuándo pararte

- Una conversión deja filas en blanco que antes tenían valor.
- El Asistente rechaza una desreferencia que debería funcionar.
- AppSheet crea una clave compuesta.
- Cualquier cosa que te obligue a salirte de esta lista.

**Parar a mitad no es un fracaso. Terminar con referencias rotas en silencio, sí.**

## Cuando termines

1. **Reporta las 38 una por una**: cuál pusiste, cuál ya estaba, cuál no pudiste.
2. **Pega el resultado** de las dos expresiones del paso 6.
3. **Di cuántas columnas `Ref` hay en total.** Debe ser 38.
4. **Anota cualquier aviso** que haya salido, con su texto literal.

**No lo des por cerrado tú.** En este proyecto se han reportado tres cierres que no resistieron la
comprobación contra el archivo.
