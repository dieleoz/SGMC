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
| `NOV_Novedades` | `Fotografia` | `Image` |  |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | `ChangeTimestamp` | **Marca del servidor.** AppSheet no lo infiere nunca |
| `FOT_Fotografias` | `FechaHora` | `ChangeTimestamp` | **Sin esto la hora de la fotografia no prueba nada** |
| `FIR_Firmas` | `FechaHora` | `ChangeTimestamp` | Idem para la firma |
| `NOV_Novedades` | `FechaHora` | `ChangeTimestamp` |  |

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

**Nota sobre `OT_OrdenesTrabajo.OTOrigenID`**, que sale en el nivel 5: apunta a su propia tabla,
para encadenar una orden derivada con la que la origino. **Dejela para el final del nivel.**

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
| `CHD_ChecklistDetalle` | `TipoRespuestaID` | `TPR_TiposRespuesta` | Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| `CHK_Checklists` | `ActivoID` | `ACT_Activos` | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| `OT_OrdenesTrabajo` | `FormularioID` | `FRM_Formularios` | El formulario lo determina el tipo del activo, no la orden. |

**Son 3, derivadas del archivo y no escritas a mano.** Estan tambien en la ficha de cada tabla,
marcadas como TRAMPA.

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

> **Supuesto sin verificar, y es el peor modo de fallo del sistema.** No hay pagina oficial que
> confirme si AppSheet evalua un `Valid_If` sobre una columna con `Editable_If = FALSE`. **Si no lo
> evalua, la regla parece funcionar por no ejercitarse nunca.** Se detecta asi: pruebe un cierre
> cercano y uno lejano. **Si los dos salen aceptados, sospeche de esto antes que del radio.**

**Excepcion por GPS deficiente** — en `MAN_Mantenimientos.CierreConExcepcion`:

```
App formula:
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")),
   [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

**El `ISBLANK` no sobra.** Sin el, borrar la fila del parametro hace que **todos los cierres
salgan limpios y nadie se entere**. Con el, si el umbral no se puede leer el cierre se marca como
excepcional: falla hacia el lado seguro. Es la forma exacta del defecto de RG-16.

```
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

### Retirar el borrado — sin esto el `IsPartOf` es peligroso

*Data → Tables → [tabla] → Are updates allowed*:

```
OT_OrdenesTrabajo    Updates si · Adds si · Deletes NO
MAN_Mantenimientos   Updates si · Adds si · Deletes NO
```

**Es la otra mitad del paso 5.** Marcar `IsPartOf` en cuatro referencias crea **borrado en
cascada**: borrar un mantenimiento se lleva sus fotografias, su firma y su checklist.

Eso solo es seguro **porque el mantenimiento nunca se borra**, y eso es exactamente lo que hace
quitar `Deletes`. Configurar el `IsPartOf` sin esto deja la cascada abierta.

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
[`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).

## Paso 10 — Publicar

> **Antes de publicar, lea esto.** Los 34 activos de la hoja comparten **una sola coordenada**,
> `4.728512, -74.114531`, que esta en Bogota y no en el corredor. Con el radio de 1 km, la
> aplicacion **rechaza todo cierre hecho en via y acepta todo cierre hecho en Bogota**.
>
> **No es un defecto de la configuracion: faltan las coordenadas reales**, que es la decision
> D-01. Publicar antes de cargarlas entrega un sistema donde ningun tecnico puede cerrar una
> orden, y se descubre con el tecnico delante.

*Manage → Deploy → Run deployment check*, y despues **Move app to Deployed state**.

**Antes de publicar, si existe una aplicacion anterior sobre la misma hoja, despubliquela.** Dos
aplicaciones sobre un backend sin integridad referencial es una fuente de corrupcion silenciosa:
la vieja conserva permisos de anadir y borrar que el modelo nuevo ya no concede.

## Reversion — hasta donde se puede volver atras

**Todo lo anterior al paso 10 se puede abandonar sin coste.** La aplicacion no esta publicada y
nadie la usa: se borra y se empieza de nuevo. La hoja no se toca en ningun paso salvo el 0.

**El paso 0 SI escribe en la hoja** al mostrar las pestanas ocultas. Antes de empezar, haga una
copia fechada del documento. Es el unico punto de restauracion del dato.

**El punto de no retorno es el paso 10**, y no por publicar: por **despublicar la aplicacion
anterior**. Si el *deployment check* falla despues, la vieja ya no esta en servicio. Compruebe
todo el paso 9 **antes** de despublicar nada.

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
---

# Anexo — Ficha de cada tabla

**Columna por columna, sin nada que deducir.** Esta es la referencia contra la que se configura y
contra la que se valida. Si una columna no aparece aqui, no deberia estar visible en la app.

Leyenda:

- **CLAVE** — casilla `KEY` marcada, tipo `Text`
- **`Ref` -> Tabla** — tipo `Ref` con esa tabla como *Source table*
- **IsPartOf** — ademas, casilla `Is a part of` marcada
- **OCULTAR** — retirada del modelo: tipo `Text`, `Show?` desmarcado, sin formula
- **TRAMPA** — AppSheet la convierte a `Ref` sola por coincidencia de nombre. **Deshagalo**
- **SIN DECIDIR** — esta en la hoja y el modelo no la declara

## `ACT_Activos`

Inventario de los activos del corredor. Es el eje del sistema.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ActivoID` | `Text` | **CLAVE** |
| `CodigoActivo` | `Text` |  |
| `Nombre` | `Text` |  |
| `TipoActivoID` | `Ref` | `Ref` -> `TIP_TiposActivo` · IsPartOf desmarcado |
| `UnidadFuncionalID` | `Ref` | `Ref` -> `UNF_UnidadesFuncionales` · IsPartOf desmarcado |
| `PR` | `Text` |  |
| `CalzadaID` | `Ref` | `Ref` -> `CAL_Calzadas` · IsPartOf desmarcado |
| `SentidoID` | `Ref` | `Ref` -> `SEN_Sentidos` · IsPartOf desmarcado |
| `Ubicacion` | `LatLong` |  |
| `EstadoActivoID` | `Ref` | `Ref` -> `EST_Activo` · IsPartOf desmarcado |
| `CodigoQR` | `Text` |  |
| `FrecuenciaID` | `Ref` | `Ref` -> `FRE_Frecuencias` · IsPartOf desmarcado |
| `Criticidad` | `Enum` | Valores: `Alta` · `Media` · `Baja. Pondera la disponibilidad de D-13` |
| `FechaBaja` | `Date` |  |
| `MotivoBaja` | `Enum` | Valores: `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` |
| `Activo` | `Yes/No` |  |
| `Observaciones` | `LongText` |  |

## `ASG_AsignacionZona`

Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: un tecnico puede tener varias, de modo que la relacion es de muchos a muchos y no cabe como columna en USR_Usuarios.

| Columna | Tipo | Que hacer |
|---|---|---|
| `AsignacionID` | `Text` | **CLAVE** |
| `UsuarioID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `UnidadFuncionalID` | `Ref` | `Ref` -> `UNF_UnidadesFuncionales` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `CAL_Calzadas`

Calzadas del corredor.

| Columna | Tipo | Que hacer |
|---|---|---|
| `CalzadaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `CHD_ChecklistDetalle`

Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su texto: sin eso no hay comparacion historica posible.

| Columna | Tipo | Que hacer |
|---|---|---|
| `DetalleID` | `Text` | **CLAVE** |
| `ChecklistID` | `Ref` | `Ref` -> `CHK_Checklists` · **IsPartOf** |
| `PreguntaID` | `Ref` | `Ref` -> `FRM_Preguntas` · IsPartOf desmarcado |
| `RespuestaTexto` | `LongText` |  |
| `RespuestaNumero` | `Decimal` |  |
| `RespuestaBoolean` | `Yes/No` |  |
| `RespuestaLista` | `Enum` |  |
| `Contestada` | `Yes/No` | `Initial value` = `FALSE` |
| `Observacion` | `LongText` |  |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Activo` | **OCULTAR** | El detalle es parte de su checklist: no se desactiva por separado. |
| `EstadoPregunta` | **OCULTAR** | Redundante con Contestada. |
| `FechaRespuesta` | **OCULTAR** | Se deriva del ChangeTimestamp del mantenimiento. |
| `Orden` | **OCULTAR** | Se alcanza por [PreguntaID].[Orden]. |
| `PreguntaActual` | **OCULTAR** | Estado de la interfaz, no dato. |
| `RespuestaFecha` | **OCULTAR** | Fuera de alcance: ninguna pregunta usa tipo fecha. |
| `RespuestaFirma` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `RespuestaFoto` | **OCULTAR** | Sustituido por FOT_Fotografias. |
| `RespuestaGPS` | **OCULTAR** | La coordenada es del mantenimiento y de cada fotografia. |
| `RespuestaHora` | **OCULTAR** | Fuera de alcance: ninguna pregunta usa tipo hora. |
| `TipoRespuestaID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `TPR_TiposRespuesta`** | Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| `TotalPreguntas` | **OCULTAR** | No es del detalle sino del encabezado, y ademas se cuenta. |

## `CHK_Checklists`

Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la inspeccion es parte de la ejecucion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ChecklistID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `VersionFormulario` | `Number` |  |
| `FechaInicio` | `DateTime` | `Initial value` = `NOW()` |
| `FechaFin` | `DateTime` |  |
| `Finalizado` | `Yes/No` | `Initial value` = `FALSE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Activo` | **OCULTAR** | El checklist es parte de su mantenimiento: no se desactiva por separado. |
| `ActivoID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `ACT_Activos`** | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| `Estado` | **OCULTAR** | Sustituido por Finalizado, que produccion ya tiene. |
| `FechaCreacion` | **OCULTAR** | Redundante con FechaInicio. |
| `FechaEnvioCorreo` | **OCULTAR** | Es traza del bot, no del checklist. |
| `FirmaSupervisor` | **OCULTAR** | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `FirmaTecnico` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `GPSFin` | **OCULTAR** | Idem. |
| `GPSInicio` | **OCULTAR** | La coordenada es del mantenimiento y de cada fotografia, no del checklist. |
| `Observaciones` | **OCULTAR** | La observacion es de la ejecucion o de la respuesta, no del encabezado. |
| `PDF` | **OCULTAR** | El informe se genera al enviarlo, no se almacena en la fila. |
| `Porcentaje` | **OCULTAR** | Se calcula. Guardarlo permite que contradiga al detalle. |
| `PreguntaActual` | **OCULTAR** | Estado de la interfaz, no dato. Se deriva de las respuestas. |
| `TecnicoID` | **OCULTAR** | Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato de prueba dejo 'Santiago Moreno' en lugar de un identificador. |
| `TotalPreguntas` | **OCULTAR** | Se cuenta de FRM_Preguntas. |

## `EOT_EstadosOrden`

Ciclo de vida de la orden segun el supuesto D-06. Declararlo como catalogo, y no como texto libre, es lo que permite medir cumplimiento.

| Columna | Tipo | Que hacer |
|---|---|---|
| `EstadoOrdenID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Orden` | `Number` |  |
| `QuienCambia` | `Enum` | Valores: `Sistema` · `Tecnico` · `Supervisor` |
| `EsFinal` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `EST_Activo`

Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado.

| Columna | Tipo | Que hacer |
|---|---|---|
| `EstadoActivoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `GeneraAlerta` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FAL_ModosFalla`

Taxonomia de fallas por tipo de activo. Sin clasificar la falla no hay ingenieria de mantenimiento posible: no se puede calcular tiempo medio entre fallas, ni saber que componente falla mas, ni pasar de correctivo a predictivo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ModoFallaID` | `Text` | **CLAVE** |
| `TipoActivoID` | `Ref` | `Ref` -> `TIP_TiposActivo` · IsPartOf desmarcado |
| `Nombre` | `Text` |  |
| `Componente` | `Text` |  |
| `Criticidad` | `Enum` | Valores: `Alta` · `Media` · `Baja` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FIR_Firmas`

Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor valida aprobando en el portal, no firmando.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FirmaID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `TipoFirma` | `Enum` | Valores: `Tecnico` |
| `Imagen` | `Signature` |  |
| `FechaHora` | `ChangeTimestamp` |  |

## `FOT_Fotografias`

Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. Se elige tabla hija y se retiran los campos de imagen embebidos en MAN.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FotoID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `Tipo` | `Enum` | Valores: `Antes` · `Despues` · `Novedad` |
| `Archivo` | `Image` |  |
| `Ubicacion` | `LatLong` | `Initial value` = `HERE()` |
| `PrecisionGPS` | `Number` | `Initial value` = `USERLOCATIONACCURACY()` |
| `FechaHora` | `ChangeTimestamp` |  |
| `Usuario` | `Text` | `Initial value` = `USEREMAIL()` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Fecha` | **OCULTAR** · SIN DECIDIR | El modelo no la declara |

## `FRE_Frecuencias`

Periodicidad del mantenimiento preventivo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FrecuenciaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Dias` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FRM_Formularios`

Registro maestro de los 18 checklists, uno por tipo de activo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FormularioID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Descripcion` | `Text` |  |
| `Version` | `Number` | `Initial value` = `1` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FRM_Preguntas`

Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, FRM_CCTV y FRM_PMVF, que eran una arquitectura paralela con otro esquema.

| Columna | Tipo | Que hacer |
|---|---|---|
| `PreguntaID` | `Text` | **CLAVE** |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `SeccionID` | `Ref` | `Ref` -> `FRM_Secciones` · IsPartOf desmarcado |
| `Orden` | `Number` |  |
| `Pregunta` | `Text` |  |
| `TipoRespuestaID` | `Ref` | `Ref` -> `TPR_TiposRespuesta` · IsPartOf desmarcado |
| `Obligatoria` | `Yes/No` | `Initial value` = `TRUE` |
| `ValorMinimo` | `Decimal` |  |
| `ValorMaximo` | `Decimal` |  |
| `Unidad` | `Text` |  |
| `Ayuda` | `Text` |  |
| `VisibleSi` | `Text` |  |
| `RequiereFoto` | `Yes/No` | `Initial value` = `FALSE` |
| `Version` | `Number` | `Initial value` = `1` |
| `RequiereGPS` | `Yes/No` | `Initial value` = `FALSE` |
| `RequiereFirma` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FRM_Secciones`

Agrupacion de preguntas dentro del formulario.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SeccionID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Orden` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `LST_ValoresLista`

Opciones de las preguntas de tipo lista.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ValorListaID` | `Text` | **CLAVE** |
| `PreguntaID` | `Ref` | `Ref` -> `FRM_Preguntas` · IsPartOf desmarcado |
| `Valor` | `Text` |  |
| `Orden` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `MAN_Mantenimientos`

Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia.

| Columna | Tipo | Que hacer |
|---|---|---|
| `MantenimientoID` | `Text` | **CLAVE** |
| `OTID` | `Ref` | `Ref` -> `OT_OrdenesTrabajo` · IsPartOf desmarcado |
| `TecnicoID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado · `Initial value` = `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `FechaHoraInicio` | `DateTime` | `Initial value` = `NOW()` |
| `FechaHoraFin` | `DateTime` |  |
| `OrigenApertura` | `Enum` | Valores: `QR o Lista. Abrir por lista no prueba presencia; se marca para poder exigir QR donde importe y para medir cuantos cierres carecen de escaneo` · `Initial value` = `QR` |
| `UbicacionEscaneo` | `LatLong` |  |
| `FechaHoraEscaneo` | `DateTime` |  |
| `EstadoActivoID` | `Ref` | `Ref` -> `EST_Activo` · IsPartOf desmarcado |
| `Coordenadas_Cierre` | `LatLong` | `Initial value` = `HERE()` |
| `Precision_GPS` | `Number` | `Initial value` = `USERLOCATIONACCURACY()` |
| `CierreConExcepcion` | `Yes/No` |  |
| `MotivoExcepcion` | `LongText` |  |
| `RequiereSegundaVisita` | `Yes/No` | `Initial value` = `FALSE` |
| `MotivoPendienteID` | `Ref` | `Ref` -> `MOT_MotivosPendiente` · IsPartOf desmarcado |
| `ModoFallaID` | `Ref` | `Ref` -> `FAL_ModosFalla` · IsPartOf desmarcado |
| `Observaciones` | `LongText` |  |
| `AprobadoSupervisor` | `Yes/No` | `Initial value` = `FALSE` |
| `FechaAprobacion` | `DateTime` |  |
| `ObservacionRechazo` | `LongText` |  |
| `UsuarioRegistro` | `Text` | `Initial value` = `USEREMAIL()` |
| `FechaHoraRegistro` | `ChangeTimestamp` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Diagnostico` | **OCULTAR** | Se responde en el checklist, no en campo libre. |
| `Duracion_Minutos` | **OCULTAR** | Se calcula de FechaHoraInicio y FechaHoraFin. |
| `Estado_Intervencion` | **OCULTAR** | Redundante con el estado de la orden. |
| `Fecha` | **OCULTAR** | Redundante con FechaHoraInicio. |
| `Firma_Supervisor` | **OCULTAR** | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `Firma_Tecnico` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `Imagen_Final` | **OCULTAR** | Sustituido por FOT_Fotografias con Tipo=Despues. |
| `Imagen_Inicio` | **OCULTAR** | Sustituido por FOT_Fotografias con Tipo=Antes. |
| `Localizacion` | **OCULTAR** | Ambiguo y redundante con Coordenadas_Cierre. |
| `Repuestos_Utilizados` | **OCULTAR** | Gestion de repuestos esta fuera de alcance. |
| `Requiere_Repuesto` | **OCULTAR** | Se cubre con MotivoPendienteID = Falta de repuesto. |
| `Tipo` | **OCULTAR** | El tipo es de la orden, no de la ejecucion. |
| `Trabajo_Realizado` | **OCULTAR** | Se responde en el checklist. |

## `MOT_MotivosPendiente`

Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no tiene donde declarar por que no pudo terminar, fuerza un cierre falso.

| Columna | Tipo | Que hacer |
|---|---|---|
| `MotivoPendienteID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `GeneraSeguimiento` | `Yes/No` | `Initial value` = `TRUE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `NOV_Novedades`

Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de programacion. Supuesto D-08. Sin esta via los hallazgos se pierden o acaban en WhatsApp, que es lo que el sistema viene a reemplazar.

| Columna | Tipo | Que hacer |
|---|---|---|
| `NovedadID` | `Text` | **CLAVE** |
| `UsuarioID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado · `Initial value` = `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `Tipo` | `Enum` | Valores: `Activo no inventariado` · `Falla detectada` |
| `Descripcion` | `LongText` |  |
| `Ubicacion` | `LatLong` | `Initial value` = `HERE()` |
| `Fotografia` | `Image` |  |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `Estado` | `Enum` | Valores: `Reportada` · `Aceptada` · `Descartada` · `Initial value` = `Reportada` |
| `FechaHora` | `ChangeTimestamp` |  |

## `OT_OrdenesTrabajo`

Trabajo programado o levantado sobre un activo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `OTID` | `Text` | **CLAVE** |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `TecnicoID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `SupervisorID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Tipo` | `Enum` | Valores: `Preventivo` · `Correctivo` |
| `FechaProgramada` | `DateTime` |  |
| `EstadoOrdenID` | `Ref` | `Ref` -> `EOT_EstadosOrden` · IsPartOf desmarcado |
| `OTOrigenID` | `Ref` | `Ref` -> `OT_OrdenesTrabajo` · IsPartOf desmarcado |
| `Observaciones` | `LongText` |  |
| `FechaCierre` | `DateTime` |  |
| `CerradaPor` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `FormularioID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `FRM_Formularios`** | El formulario lo determina el tipo del activo, no la orden. |
| `Informe_Final` | **OCULTAR** | Se genera del mantenimiento y su checklist, no se transcribe. |
| `Motivo_Cierre` | **OCULTAR** | Se tipifica en MOT_MotivosPendiente desde la ejecucion. |

## `PAR_Parametros`

Umbrales que el administrador ajusta con las pruebas de campo, sin tocar la configuracion de la aplicacion. Existe porque un numero magico escondido en una expresion no se puede calibrar: hay que abrir el editor, encontrarlo y arriesgarse a romper la regla. Aqui es una celda.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ParametroID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Valor` | `Decimal` |  |
| `Unidad` | `Text` |  |
| `Descripcion` | `LongText` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `PLA_PlanMantenimiento`

Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al sistema en gestion de mantenimiento y no en un registro de formularios: de aqui salen las ordenes, en lugar de crearlas a mano una por una.

| Columna | Tipo | Que hacer |
|---|---|---|
| `PlanID` | `Text` | **CLAVE** |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `FrecuenciaID` | `Ref` | `Ref` -> `FRE_Frecuencias` · IsPartOf desmarcado |
| `UltimaEjecucion` | `Date` |  |
| `ProximaFecha` | `Date` |  |
| `ResponsableID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `ROL_Roles`

Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta.

| Columna | Tipo | Que hacer |
|---|---|---|
| `RolID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Descripcion` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `SED_Sedes`

Sedes fisicas donde trabaja el personal: CCO, peajes y basculas.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SedeID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Ciudad` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `SEN_Sentidos`

Sentidos de circulacion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SentidoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `TIP_TiposActivo`

Taxonomia de activos. Determina que checklist abre la aplicacion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `TipoActivoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Categoria` | `Enum` | Valores: `ITS` · `Electrico` · `Comunicaciones` · `TI` |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `TieneQR` | `Yes/No` | `Initial value` = `TRUE` |
| `RequiereGPS` | `Yes/No` | `Initial value` = `TRUE` |
| `RadioGeofencingKm` | `Decimal` | `Initial value` = `0.2` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `TPR_TiposRespuesta`

Tipo de dato esperado en cada respuesta.

| Columna | Tipo | Que hacer |
|---|---|---|
| `TipoRespuestaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `UNF_UnidadesFuncionales`

Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque son dos conceptos distintos que el modelo anterior mezclaba en una sola columna, dejando usuarios y activos en conjuntos disjuntos.

| Columna | Tipo | Que hacer |
|---|---|---|
| `UnidadFuncionalID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `PRInicial` | `Text` |  |
| `PRFinal` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `USR_Usuarios`

Personas del sistema. El correo resuelve la sesion contra USEREMAIL().

| Columna | Tipo | Que hacer |
|---|---|---|
| `UsuarioID` | `Text` | **CLAVE** |
| `Nombres` | `Text` |  |
| `Correo` | `Email` |  |
| `Cargo` | `Text` |  |
| `Iniciales` | `Text` |  |
| `RolID` | `Ref` | `Ref` -> `ROL_Roles` · IsPartOf desmarcado |
| `SedeID` | `Ref` | `Ref` -> `SED_Sedes` · IsPartOf desmarcado |
| `Telefono` | `Phone` |  |
| `FechaIngreso` | `Date` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `UltimaSincronizacion` | **OCULTAR** · SIN DECIDIR | El modelo no la declara |

