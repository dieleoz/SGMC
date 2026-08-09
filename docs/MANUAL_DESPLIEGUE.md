# Manual de despliegue — SGMC sobre AppSheet

**Para quien construye la aplicacion.** De cero a desplegada.

> **Manual por rol, no por persona.** Quien lo ejecuta es el **Funcional**: perfil que configura
> AppSheet, sin necesidad de programar. Escrito para poder replicarlo en otro contrato.

| | |
|---|---|
| Sistema | Gestion de Mantenimiento en Campo |
| Plataforma | Google AppSheet sobre Google Sheets |
| Fuente del modelo | `scripts/modelo_objetivo.py`. Este manual se genera de ahi |
| Tablas | **28** |
| Referencias | **38** |
| Reglas | **20** |

## Por que este manual existe

La primera version de esta aplicacion se construyo, y despues el modelo de datos se corrigio **en
la hoja**: columnas renombradas, tablas nuevas, campos retirados. **No hubo forma de que AppSheet
lo recogiera.**

Dos limites de la plataforma, los dos verificados, explican por que:

**`Regenerate` fusiona, no reemplaza.** Su documentacion dice que combina la informacion nueva con
la existente e intenta mantener las columnas que ya estan. Sirve para anadir una columna; con un
esquema muy divergente **impide converger**. El propio AppSheet indica la salida: *Delete and
re-add the table*.

**AppSheet ignora las pestanas ocultas, y no avisa.** Ocho pestanas del libro estaban ocultas y
cargaban 24 tablas de 32, sin un solo mensaje.

**Por debajo de cierto umbral se repara; por encima se reconstruye.** Este manual es el camino de
reconstruir, que resulto ser mas rapido y mas limpio.

---

## Paso 0 — Antes de abrir AppSheet

**Comprobar la hoja.** Si algo esta mal aqui, todo lo demas hereda el error.

```bash
python scripts/verificar_faseA.py "BD/<archivo>.xlsx"
```

Tiene que decir **`FASE A CERRADA`**. Si dice otra cosa, no siga.

**Y mirar las pestanas ocultas**, que es lo que mas cuesta descubrir despues:

```bash
python -c "import openpyxl;wb=openpyxl.load_workbook('BD/<archivo>.xlsx',read_only=True);print([n for n in wb.sheetnames if wb[n].sheet_state!='visible'])"
```

Tiene que devolver **una lista vacia**. Si hay pestanas ocultas, mostrarlas en Google Sheets —
*Ver → Hojas ocultas*— antes de continuar. **`F-18` de la verificacion tambien lo detecta.**

## Paso 1 — Crear la aplicacion

En AppSheet: **Create → App → Start with existing data**, y elegir el Google Sheets.

**Fuente: el documento de Google Sheets, no un archivo subido.** Si se sube un `.xlsx`, la
aplicacion queda leyendo una foto fija y nada se sincroniza.

**Quien crea la aplicacion es su propietario.** Conviene que sea la cuenta que va a operarla: un
coautor no puede dar de alta tablas, y todo este manual consiste en eso.

## Paso 2 — Dar de alta las 28 tablas

*Data → `+` → Add data*, una por una. **En este orden**, que no es alfabetico: cada nivel apunta a
tablas cuyas claves quedaron fijadas antes.

**1. Catalogos**

```
  ROL_Roles                · SED_Sedes                · UNF_UnidadesFuncionales
  CAL_Calzadas             · SEN_Sentidos             · FRE_Frecuencias
  EST_Activo               · EOT_EstadosOrden         · MOT_MotivosPendiente
  TPR_TiposRespuesta       · PAR_Parametros
```

**2. Formularios**

```
  FRM_Formularios          · FRM_Secciones            · FRM_Preguntas
  LST_ValoresLista
```

**3. Maestras**

```
  TIP_TiposActivo          · USR_Usuarios             · ASG_AsignacionZona
  FAL_ModosFalla
```

**4. Activos**

```
  ACT_Activos
```

**5. Ordenes**

```
  OT_OrdenesTrabajo        · PLA_PlanMantenimiento    · NOV_Novedades
```

**6. Ejecucion**

```
  MAN_Mantenimientos       · CHK_Checklists           · CHD_ChecklistDetalle
  FOT_Fotografias          · FIR_Firmas
```

### Las que NO se dan de alta

Estan en la hoja y el modelo las retira:

| Pestana | Por que |
|---|---|
| `FRM_CCTV` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_PMVF` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_SOS` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `GPS` | Duplica Coordenadas_Cierre y Precision_GPS de MAN_Mantenimientos. Nunca recibio un registro. |
| `SEC_Secciones` | Duplicada con FRM_Secciones. Se consolida en una sola. |

**No borre esas pestanas de la hoja.** Tres de ellas guardan bancos de preguntas que todavia no se
han migrado.

## Paso 3 — Las claves, todas `Text`

*Data → Columns* de cada tabla. **Una sola casilla `KEY`**, sobre la columna correcta, tipo
**`Text`**.

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

**`Text` sin excepcion, y hay un caso que lo justifica.** `USR_Usuarios.UsuarioID` tiene un valor
alfanumerico entre otros numericos. Si AppSheet infiere `Number`, esa fila se queda sin clave
valida y ese usuario **deja de existir para el sistema**.

**Si ve dos casillas `KEY` marcadas, o la clave aparece como combinacion de dos columnas,
corrijalo antes de seguir.** Contra una clave compuesta no resuelve ninguna referencia, y el
sintoma es que falla todo el paso 5 sin decir por que.

### Clave automatica para las filas nuevas

Estas 6 tablas crean filas desde la aplicacion. Sin esto, no sabe que identificador poner:

| Tabla | Columna | `Initial value` |
|---|---|---|
| `CHD_ChecklistDetalle` | `DetalleID` | `UNIQUEID()` |
| `CHK_Checklists` | `ChecklistID` | `UNIQUEID()` |
| `FIR_Firmas` | `FirmaID` | `UNIQUEID()` |
| `FOT_Fotografias` | `FotoID` | `UNIQUEID()` |
| `MAN_Mantenimientos` | `MantenimientoID` | `UNIQUEID()` |
| `NOV_Novedades` | `NovedadID` | `UNIQUEID()` |

## Paso 4 — Los tipos que AppSheet no adivina

Todo llega de una hoja, asi que entra como texto o numero.

| Tabla | Columna | Tipo | |
|---|---|---|---|
| `ACT_Activos` | `Ubicacion` | `LatLong` | Sobre ella se calcula la distancia al activo |
| `ACT_Activos` | `FechaBaja` | `Date` |  |
| `ACT_Activos` | `Activo` | `Yes/No` |  |
| `MAN_Mantenimientos` | `Coordenadas_Cierre` | `LatLong` | **La mas importante.** DISTANCE() no funciona sobre texto |
| `MAN_Mantenimientos` | `UbicacionEscaneo` | `LatLong` |  |
| `MAN_Mantenimientos` | `Precision_GPS` | `Number` |  |
| `MAN_Mantenimientos` | `CierreConExcepcion` | `Yes/No` |  |
| `MAN_Mantenimientos` | `OrigenApertura` | `Enum` | Valores: `QR`, `Lista` |
| `OT_OrdenesTrabajo` | `Tipo` | `Enum` | Valores: `Preventivo`, `Correctivo` |
| `FOT_Fotografias` | `Ubicacion` | `LatLong` |  |
| `FOT_Fotografias` | `Archivo` | `Image` |  |
| `FIR_Firmas` | `Imagen` | `Signature` |  |
| `NOV_Novedades` | `Ubicacion` | `LatLong` |  |

## Paso 5 — Las 38 referencias

> **Cuidado con las listas de otros documentos.** `ESPEC-002` lista **15**, y es correcto para lo
> que norma: convertir una aplicacion existente donde otras 23 ya estaban puestas. **Construyendo
> desde cero no sobrevive ninguna.** Si al terminar cuenta 15, siguio la lista equivocada.

Una referencia de AppSheet **guarda el valor de la clave de la tabla destino**. De ahi que el orden
importe: primero la clave del destino, despues quien la apunta.

**2. Formularios**

```
 1  FRM_Preguntas.FormularioID         -> FRM_Formularios
 2  FRM_Preguntas.SeccionID            -> FRM_Secciones
 3  FRM_Preguntas.TipoRespuestaID      -> TPR_TiposRespuesta
 4  LST_ValoresLista.PreguntaID        -> FRM_Preguntas
```

**3. Maestras**

```
 5  TIP_TiposActivo.FormularioID       -> FRM_Formularios
 6  USR_Usuarios.RolID                 -> ROL_Roles
 7  USR_Usuarios.SedeID                -> SED_Sedes
 8  ASG_AsignacionZona.UsuarioID       -> USR_Usuarios
 9  ASG_AsignacionZona.UnidadFuncionalID -> UNF_UnidadesFuncionales
10  FAL_ModosFalla.TipoActivoID        -> TIP_TiposActivo
```

**4. Activos**

```
11  ACT_Activos.TipoActivoID           -> TIP_TiposActivo
12  ACT_Activos.UnidadFuncionalID      -> UNF_UnidadesFuncionales
13  ACT_Activos.CalzadaID              -> CAL_Calzadas
14  ACT_Activos.SentidoID              -> SEN_Sentidos
15  ACT_Activos.EstadoActivoID         -> EST_Activo
16  ACT_Activos.FrecuenciaID           -> FRE_Frecuencias
```

**5. Ordenes**

```
17  OT_OrdenesTrabajo.ActivoID         -> ACT_Activos
18  OT_OrdenesTrabajo.TecnicoID        -> USR_Usuarios
19  OT_OrdenesTrabajo.SupervisorID     -> USR_Usuarios
20  OT_OrdenesTrabajo.EstadoOrdenID    -> EOT_EstadosOrden
21  OT_OrdenesTrabajo.OTOrigenID       -> OT_OrdenesTrabajo
22  OT_OrdenesTrabajo.CerradaPor       -> USR_Usuarios
23  PLA_PlanMantenimiento.ActivoID     -> ACT_Activos
24  PLA_PlanMantenimiento.FrecuenciaID -> FRE_Frecuencias
25  PLA_PlanMantenimiento.ResponsableID -> USR_Usuarios
26  NOV_Novedades.UsuarioID            -> USR_Usuarios
27  NOV_Novedades.ActivoID             -> ACT_Activos
```

**6. Ejecucion**

```
28  MAN_Mantenimientos.OTID            -> OT_OrdenesTrabajo
29  MAN_Mantenimientos.TecnicoID       -> USR_Usuarios
30  MAN_Mantenimientos.EstadoActivoID  -> EST_Activo
31  MAN_Mantenimientos.MotivoPendienteID -> MOT_MotivosPendiente
32  MAN_Mantenimientos.ModoFallaID     -> FAL_ModosFalla
33  CHK_Checklists.MantenimientoID     -> MAN_Mantenimientos   IsPartOf = TRUE
34  CHK_Checklists.FormularioID        -> FRM_Formularios
35  CHD_ChecklistDetalle.ChecklistID   -> CHK_Checklists   IsPartOf = TRUE
36  CHD_ChecklistDetalle.PreguntaID    -> FRM_Preguntas
37  FOT_Fotografias.MantenimientoID    -> MAN_Mantenimientos   IsPartOf = TRUE
38  FIR_Firmas.MantenimientoID         -> MAN_Mantenimientos   IsPartOf = TRUE
```

**Y la ultima, aparte:**

```
39  OT_OrdenesTrabajo.OTOrigenID        -> OT_OrdenesTrabajo
```

Apunta a su propia tabla, para encadenar una orden derivada con la que la origino. Dejela para el
final.

### `IsPartOf` va marcado en cuatro, y en ninguna mas

```
FOT_Fotografias.MantenimientoID    -> MAN_Mantenimientos
FIR_Firmas.MantenimientoID         -> MAN_Mantenimientos
CHK_Checklists.MantenimientoID     -> MAN_Mantenimientos
CHD_ChecklistDetalle.ChecklistID   -> CHK_Checklists
```

**`MAN_Mantenimientos.OTID` va DESMARCADO, y es deliberado.** Con `IsPartOf`, borrar una orden
borraria su ejecucion, sus fotografias y su firma **en cascada**. En un sistema cuyo proposito es
que la evidencia sea dificil de falsificar, eso se decide, no se hereda de un ejemplo.

### Despues de cada conversion

**Mire si aparecieron celdas en blanco donde habia valores.** Convertir a `Ref` conserva solo las
filas cuyo valor coincide con la clave del destino; las demas quedan huerfanas **sin mensaje de
error**.

## Paso 6 — Tres columnas que AppSheet convierte solo, y estan mal

Son columnas muertas que siguen en la hoja **y se llaman igual que la clave de otra tabla**.
AppSheet infiere referencias por coincidencia de nombre, asi que las convierte sin que nadie se lo
pida.

| Tabla | Columna | Adonde apunta sola | Por que esta mal |
|---|---|---|---|
| `CHK_Checklists` | `ActivoID` | `ACT_Activos` | El checklist cuelga del mantenimiento, no del activo |
| `CHD_ChecklistDetalle` | `TipoRespuestaID` | `TPR_TiposRespuesta` | El tipo de respuesta lo da la pregunta |
| `OT_OrdenesTrabajo` | `FormularioID` | `FRM_Formularios` | El formulario lo determina el tipo del activo |

**Dejelas en `Text` y desmarque `Show?`.** Si se quedan como `Ref`, dibujan rutas de navegacion
que el modelo prohibe y aparecen en la aplicacion como si fueran buenas.

Un aviso del tipo *was set to be unsearchable because it is Hidden* es **normal**: confirma que la
columna quedo oculta.

## Paso 7 — Las reglas

Las 20 del modelo. Las expresiones completas estan en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) §2.

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

### Las cuatro que no pueden faltar

**Geofencing** — en `MAN_Mantenimientos.Coordenadas_Cierre`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= 1.0
Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.
Editable_If:    FALSE
```

**El `1.0` es literal a proposito.** El modelo preve un radio por tipo de activo, pero esa columna
esta vacia en los 18 tipos: la version por tipo comparia contra una celda en blanco y **rechazaria
tambien los cierres legitimos**.

**No editables** — en `MAN_Mantenimientos`, `Editable_If = FALSE` en las cuatro columnas de
captura:

```
Coordenadas_Cierre · Precision_GPS · UbicacionEscaneo · FechaHoraEscaneo
```

**Sin esto el geofencing es decorativo:** el tecnico arrastra el pin del mapa y cierra desde donde
quiera. La regla parece funcionar y no prueba nada.

**Excepcion por GPS deficiente** — en `MAN_Mantenimientos.CierreConExcepcion`:

```
App formula:  [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")
```

**Filtros de seguridad** — *Data → Tables → [tabla] → Security Filter*:

```
ACT_Activos:
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID],
   AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))

OT_OrdenesTrabajo:
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

**No son solo control de acceso: son rendimiento.** Sin ellos, cada tecnico se descarga el
inventario entero al telefono.

## Paso 8 — Las vistas

**La mayor parte se construye sola al poner las referencias.** AppSheet crea las columnas
virtuales `Related ...` y con ellas la navegacion padre-hijo: al abrir un mantenimiento se ven sus
fotografias y su firma; al abrir un activo, sus ordenes.

Lo que hay que configurar a mano son las vistas principales:

| Vista | Tipo | Sobre | Nota |
|---|---|---|---|
| Mapa de activos | `Map` | `ACT_Activos` | Columna de mapa: `Ubicacion` |
| Mis ordenes | `Deck` | `OT_OrdenesTrabajo` | Es la pantalla de trabajo del tecnico |
| Mantenimientos | `Table` | `MAN_Mantenimientos` | |

## Paso 9 — Verificar antes de publicar

**No lo de por cerrado usted.** Este proyecto tiene tres cierres reportados que no resistieron la
comprobacion contra el archivo, y las tres veces lo paro un script.

**La cadena navega** — en el Asistente de Expresiones, sobre `MAN_Mantenimientos`:

```
[OTID].[ActivoID].[Ubicacion]
[OTID].[TecnicoID].[Correo]
```

Las dos en verde. Si la primera falla, casi siempre es `OT_OrdenesTrabajo.ActivoID`, que la lista
antigua de 15 no incluia.

**Cuente las referencias.** Las columnas de tipo `Ref` deben sumar **38**.

**Y los tres verificadores del repositorio:**

```bash
python scripts/validar_modelo.py          # el modelo consigo mismo
python scripts/verificar_faseA.py "..."   # el modelo contra la hoja
python scripts/verificar_documentos.py    # la prosa contra el modelo
```

**Ninguno mira la aplicacion.** Para eso estan las pruebas de aceptacion de
[`sdd/PRUEBA-002-cableado-en-appsheet.md`](sdd/PRUEBA-002-cableado-en-appsheet.md).

## Paso 10 — Publicar

*Manage → Deploy → Run deployment check*, y despues **Move app to Deployed state**.

**Antes de publicar, si existe una aplicacion anterior sobre la misma hoja, despubliquela.** Dos
aplicaciones sobre un backend sin integridad referencial es una fuente de corrupcion silenciosa:
la vieja conserva permisos de anadir y borrar que el modelo nuevo ya no concede.

## Lo que NO cabe en el plan gratuito

No es *mas adelante*: es **no en este plan**. Solo cambia con la decision de licenciamiento.

| Lo que se querria | Por que no |
|---|---|
| Generacion automatica de las ordenes del mes | Los procesos programados no se ejecutan |
| Aviso al supervisor de que hay trabajo por recibir | Lo mismo |
| Integracion con sistemas externos | Sin plan Core no hay API REST |
| Atributos distintos por tipo de equipo | El backend es una hoja: no hay esquema dinamico |
| Que una escritura directa en la hoja respete las validaciones | Imposible por diseno |

**Ese ultimo importa mas de lo que parece.** Todas las garantias del sistema viven en la capa de
aplicacion. Quien escriba en la hoja se las salta todas. Lo que el sistema puede ofrecer es que
falsificar cueste mas que hacer el trabajo, no que sea imposible.

---
*Generado de `scripts/modelo_objetivo.py` por `scripts/generar_manual_despliegue.py`.*
*Para actualizarlo, cambie el modelo y vuelva a generar.*
