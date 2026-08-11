# Encargo de cableado de la aplicación

**Autocontenido. Cópialo íntegro desde la línea siguiente.**

**Generado** por `scripts/generar_prompt_cableado.py`. No editar a mano: las listas salen de
`scripts/modelo_objetivo.py`.

---

Vas a cablear la aplicación **`_SISGA_-323965761`** de Google AppSheet. Las 28 tablas ya están dadas de alta
sobre la hoja `Modelo_Datos_10082026`, y los datos ya están cargados. **No hay que subir ningún Excel ni tocar la
hoja**: todo lo que sigue vive dentro del editor.

```
https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e
```

> Si ese enlace da 404, entra por el listado de `https://www.appsheet.com` y abre `_SISGA_-323965761`.

### Dónde está cada cosa en el editor

Los nombres de las reglas **no son** los nombres de los controles. Ahí es donde se pierde
la gente, y ahí se coló más de un error del 2026-08-10.

| Lo que dice el encargo | Dónde está en pantalla |
|---|---|
| `Valid_If` | Data Validity > Valid If — y el mensaje va en `Invalid value error`, justo debajo |
| `Required_If` | Data Validity > Require? — **no es una casilla que se marque**: hay que pulsar el icono `=` que hay al lado para escribir la expresion. El 2026-08-10 acabo escrita en `Valid If`, que la habria vuelto imposible de guardar |
| `App formula` | Auto Compute > App formula — **escribe en la hoja** |
| `Initial value` | Auto Compute > Initial value — solo se aplica a filas NUEVAS; el usuario puede cambiarla despues salvo que `Editable?` lo impida |
| `Editable_If` | Update Behavior > Editable? — el icono `=` al lado de la casilla |
| `Label` | Display > Label — exige que `Show?` este activo, y solo puede haber UNA por tabla |
| `Key` | la casilla `Key` en la lista de columnas, no dentro del panel — sobre una tabla VACIA, AppSheet no deja marcarla si la columna no tiene `Initial value` que genere la clave |
| `Security Filter` | Data > Tables > <tabla> > Table settings > Security > Security filter |
| `Are updates allowed` | Data > Tables > <tabla> > Table settings — tres casillas: `Updates`, `Adds`, `Deletes` |

**Dentro del panel de una columna**, las secciones van en este orden:

- **`Show?`** — si la columna se ve en la aplicacion
- **`Type`** — el tipo. Es un <select> nativo del navegador
- **`Type Details`** — lo que depende del tipo: `Source table` de una Ref, los valores de un Enum, la longitud de un Text
- **`Data Validity`** — **`Valid If`**, **`Invalid value error`** y **`Require?`**
- **`Auto Compute`** — **`App formula`**, **`Initial value`** y `Suggested values`
- **`Update Behavior`** — **`Editable?`** -que es donde vive `Editable_If`- y `Reset on edit?`
- **`Display`** — **`Label`**, `Display name` y `Description`
- **`Other Properties`** — `Searchable`, `Scannable`, `NFC` y `Sensitive data`

### Antes de leer nada: recarga en duro

Si el editor muestra «A newer version of the app exists», recarga en duro con Ctrl+Shift+R ANTES de leer ningun tipo. Lo que hay en pantalla puede ser cache, y un cotejo sobre cache reporta tipos falsos con toda la confianza del mundo.

### Los bots

`Automation > Bots` → `Create a new Bot`, y tres partes:

  Event       la tabla + `Data change type`: Adds, Updates, Adds and Updates.
              O `Schedule` si es programado, con su cadencia
  Condition   una expresion que decide si sigue
  Step        `Add a step` → lo que hace

**La trampa del `Step`.** Si lo que hace es ANADIR UNA FILA a otra tabla, no se
configura dentro del bot: AppSheet interpreta que quieres generar un documento y
pide plantilla PDF y valores de retorno. Van dos sitios, en este orden:

  1. `Data > Actions` → `Add Action`
       For a record of this table  = la tabla de origen
       Do this = **Data: add a new row to another table using values from this row**
       Table to add to = la tabla destino, y los valores de cada columna

  2. `Automation > Bots` → tu bot → `Add a step` → **`Run a data action`**,
     y eliges la que acabas de crear

### Cómo saber que quedó guardado

**El boton `SAVE` de la cabecera pasa de gris a AZUL** cuando el editor recoge un
cambio, y vuelve a gris al guardar. Ese ciclo -gris, azul, gris- es la senal.

Si sigue gris, **el cambio no llego al modelo interno** y se pierde al recargar.
No basta con haber cambiado el valor del control.


## Cómo cambiar un tipo sin morir a base de clics

Los desplegables de la columna `TYPE` en *Data > Columns* son **`<select>` nativos del
navegador**, no widgets propios de AppSheet. Se pueden asignar de forma determinista.

**Y la parte que no es obvia: cambiar el valor del control NO basta.** Hay que confirmar que la
aplicación lo recogió, y la señal es que **el botón `SAVE` de la cabecera pasa de gris a azul**.
Si sigue gris, el cambio no llegó al modelo interno del editor y se pierde al recargar. Después
de guardar vuelve a gris: ese ciclo —gris, azul, gris— es lo que hay que ver en cada tabla.

**Guarda al terminar cada tabla, no al final.** La interfaz deja de protegerte cuando la
automatizas: un valor equivocado aplicado en serie se aplica en serie.

## Paso 1 — Retirar el borrado. ANTES que las referencias

**Cómo se lee de vuelta: NADIE, salvo tú.**

**No hay comando.** Are updates allowed no viaja por la API, y la API ademas tiene MAS permisos que la aplicacion -se salta el Deletes retirado-, asi que probar por ahi diria que se puede borrar cuando la app no deja.

Por eso este paso se cierra **copiando literalmente lo que ves**, incluso
cuando coincida. «Coincide» no es evidencia; el texto sí.

En *Data > Tables*, para `OT_OrdenesTrabajo` y `MAN_Mantenimientos`, en **Are updates allowed**:

```
Updates  si        Adds  si        Deletes  NO
```

**Por qué va primero y no después.** El paso 2 marca `IsPartOf` en 4 referencias, y eso es
**borrado en cascada**: borrar un mantenimiento se lleva sus fotografías, su firma y su
checklist. Eso solo es seguro porque el mantenimiento nunca se borra. **La cascada existe desde
el momento en que se marca la primera; la protección tiene que estar puesta ya.**

## Paso 2 — Las claves de las 8 tablas que llegaron vacías

**Sin un solo dato, AppSheet elige la clave a ciegas — y elige `_RowNumber`.** Contra una
clave que no es la declarada, ninguna referencia resuelve de forma estable, y el error que
acaba dando es este:

```
That Table or Slice uses RowNumber as a key which is not a stable key.
```

En *Data > Columns*, marca **`Key`** en la columna que dice la tabla y **desmarca `_RowNumber`**:

| Tabla | `Key` | ¿AppSheet avisará? |
|---|---|---|
| `CHD_ChecklistDetalle` | **`DetalleID`** | **no. Nadie la referencia, así que falla en silencio** |
| `CHK_Checklists` | **`ChecklistID`** | sí, 1 referencias la apuntan |
| `FIR_Firmas` | **`FirmaID`** | **no. Nadie la referencia, así que falla en silencio** |
| `FOT_Fotografias` | **`FotoID`** | **no. Nadie la referencia, así que falla en silencio** |
| `MAN_Mantenimientos` | **`MantenimientoID`** | sí, 3 referencias la apuntan |
| `NOV_Novedades` | **`NovedadID`** | **no. Nadie la referencia, así que falla en silencio** |
| `OT_OrdenesTrabajo` | **`OTID`** | sí, 2 referencias la apuntan |
| `PLA_PlanMantenimiento` | **`PlanID`** | **no. Nadie la referencia, así que falla en silencio** |

**AppSheet no te va a dejar marcar `Key` sin más.** Sobre una tabla vacía exige que la columna
tenga un `Initial value` que genere la clave; si no, asume que las filas nuevas nacerían sin
identificador y se aferra a `_RowNumber`. Así que primero el valor, después la casilla:

En estas 8, `Initial value` = **`UNIQUEID()`**, y luego marca `Key`:

- `CHD_ChecklistDetalle.DetalleID`
- `CHK_Checklists.ChecklistID`
- `FIR_Firmas.FirmaID`
- `FOT_Fotografias.FotoID`
- `MAN_Mantenimientos.MantenimientoID`
- `NOV_Novedades.NovedadID`
- `OT_OrdenesTrabajo.OTID`
- `PLA_PlanMantenimiento.PlanID`

> **Solo 3 de las 8 avisan.** AppSheet protesta cuando una tabla referenciada tiene clave
> inestable; de las que nadie referencia no dice nada. Hazlas las 8 de una vez, o las cinco
> restantes se descubrirán de una en una, cuando alguien intente usarlas.

## Paso 3 — Las 39 referencias

**Cómo se lee de vuelta:**

```bash
python scripts/auditar_cableado.py
```

Lee las columnas virtuales inversas de la tabla destino. Con ' By ' prueba la columna; sin ' By ' solo prueba que hay una referencia a esa tabla. Y no ve nada si el destino esta vacio.

Para cada una: *Data > Columns > la tabla > la columna > `TYPE` = `Ref`*, y en las propiedades de
la columna, **`Source table`** = la tabla destino.

**Ninguna se crea sola.** AppSheet infiere `Ref` por parecido entre el nombre de la columna y el
de una tabla, y las nuestras llevan prefijo —`UNF_UnidadesFuncionales`, no `UnidadFuncional`—,
así que el parecido se rompe. Hay que ponerlas las 39.

> **Cuántas faltan hoy, este documento no lo sabe.** Sale del modelo, así que describe el destino
> y no el estado: seguirá diciendo 39 el día que estén las 39 puestas. Antes de empezar, pregúntaselo
> a la aplicación:
>
> ```bash
> python scripts/auditar_cableado.py
> ```
>
> Emite [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md) con **lo que quede pendiente**, y
> distingue tres cosas que es fácil confundir: la que está mal, la que falta, y la que **no se
> puede ver** porque su tabla destino está vacía. Dar por buena una referencia que nadie ha
> mirado es como se llegó a tener `TipoActivoID` apuntando a la tabla de sedes.

| Tabla | Columna | `Source table` | `IsPartOf` |
|---|---|---|---|
| `SED_Sedes` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `USR_Usuarios` | `RolID` | `ROL_Roles` | no |
| `ASG_AsignacionZona` | `UsuarioID` | `USR_Usuarios` | no |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `TIP_TiposActivo` | `FormularioID` | `FRM_Formularios` | no |
| `ACT_Activos` | `TipoActivoID` | `TIP_TiposActivo` | no |
| `ACT_Activos` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | no |
| `ACT_Activos` | `CalzadaID` | `CAL_Calzadas` | no |
| `ACT_Activos` | `SentidoID` | `SEN_Sentidos` | no |
| `ACT_Activos` | `SedeID` | `SED_Sedes` | no |
| `ACT_Activos` | `EstadoActivoID` | `EST_Activo` | no |
| `ACT_Activos` | `FrecuenciaID` | `FRE_Frecuencias` | no |
| `OT_OrdenesTrabajo` | `ActivoID` | `ACT_Activos` | no |
| `OT_OrdenesTrabajo` | `TecnicoID` | `USR_Usuarios` | no |
| `OT_OrdenesTrabajo` | `SupervisorID` | `USR_Usuarios` | no |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | `EOT_EstadosOrden` | no |
| `OT_OrdenesTrabajo` | `OTOrigenID` | `OT_OrdenesTrabajo` | no |
| `OT_OrdenesTrabajo` | `CerradaPor` | `USR_Usuarios` | no |
| `MAN_Mantenimientos` | `OTID` | `OT_OrdenesTrabajo` | no |
| `MAN_Mantenimientos` | `TecnicoID` | `USR_Usuarios` | no |
| `MAN_Mantenimientos` | `EstadoActivoID` | `EST_Activo` | no |
| `MAN_Mantenimientos` | `MotivoPendienteID` | `MOT_MotivosPendiente` | no |
| `MAN_Mantenimientos` | `ModoFallaID` | `FAL_ModosFalla` | no |
| `NOV_Novedades` | `UsuarioID` | `USR_Usuarios` | no |
| `NOV_Novedades` | `ActivoID` | `ACT_Activos` | no |
| `PLA_PlanMantenimiento` | `ActivoID` | `ACT_Activos` | no |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | `FRE_Frecuencias` | no |
| `PLA_PlanMantenimiento` | `ResponsableID` | `USR_Usuarios` | no |
| `FAL_ModosFalla` | `TipoActivoID` | `TIP_TiposActivo` | no |
| `FOT_Fotografias` | `MantenimientoID` | `MAN_Mantenimientos` | **SÍ** |
| `FIR_Firmas` | `MantenimientoID` | `MAN_Mantenimientos` | **SÍ** |
| `CHK_Checklists` | `MantenimientoID` | `MAN_Mantenimientos` | **SÍ** |
| `CHK_Checklists` | `FormularioID` | `FRM_Formularios` | no |
| `CHD_ChecklistDetalle` | `ChecklistID` | `CHK_Checklists` | **SÍ** |
| `CHD_ChecklistDetalle` | `PreguntaID` | `FRM_Preguntas` | no |
| `FRM_Preguntas` | `FormularioID` | `FRM_Formularios` | no |
| `FRM_Preguntas` | `SeccionID` | `FRM_Secciones` | no |
| `FRM_Preguntas` | `TipoRespuestaID` | `TPR_TiposRespuesta` | no |
| `LST_ValoresLista` | `PreguntaID` | `FRM_Preguntas` | no |

> **Las 4 de `IsPartOf` y la que NO lo lleva.**
>
> - `FOT_Fotografias.MantenimientoID` hacia `MAN_Mantenimientos`
> - `FIR_Firmas.MantenimientoID` hacia `MAN_Mantenimientos`
> - `CHK_Checklists.MantenimientoID` hacia `MAN_Mantenimientos`
> - `CHD_ChecklistDetalle.ChecklistID` hacia `CHK_Checklists`
>
> **`MAN_Mantenimientos.OTID` va DESMARCADO.** Es la trampa de este paso: parece que debería
> llevarlo por simetría con las otras, y no. Con `IsPartOf`, borrar una orden se llevaría el
> mantenimiento entero y con él toda su evidencia.

## Paso 4 — Los tipos. **Las 210, no una lista de excepciones**

**Este paso se llamaba «los tipos que no se infieren» y enumeraba 61 columnas.** Era una lista
blanca de excepciones sobre un default que se presumía bueno: las otras 150 se daban por
correctas por omisión. La plataforma garantiza lo contrario, y el precio fue `RG-03` —bien
escrita, bien colocada— sobre una columna que AppSheet tipó `Text` cuando el modelo dice
`Yes/No`. Comparar texto contra el booleano `TRUE` es **siempre falso y no da error**: el motivo
de excepción no se pide nunca. La regla existe y es decorativa.

Y el «qué reportar» cerraba el bucle en falso —«cualquier tipo distinto del que dice este
documento»—: **nadie puede reportar una diferencia contra un valor que nunca se le dio.**

### Las 106 que NADIE pone si no las pones tú

Ningún contenido de la hoja las produce, o su propio nombre empuja a AppSheet al tipo
equivocado. **Están ordenadas por las reglas que dependen de cada una**, que es lo que ordena el
trabajo: una columna mal tipada sin regla encima molesta al usuario; con una regla encima
**rompe la regla en silencio**.

| Tabla | Columna | `TYPE` | Reglas | Por qué no se consigue sola |
|---|---|---|---|---|
| `ACT_Activos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-16`, `RG-17` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04`, `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-01`, `RG-35` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | `RG-11`, `RG-36` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Activo` | **`Yes/No`** | `RG-16` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `ACT_Activos` | `SedeID` | **`Ref`** → `SED_Sedes` | `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `Activo` | **`Yes/No`** | `RG-04` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHK_Checklists` | `FormularioID` | **`Ref`** → `FRM_Formularios` | `RG-09` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `EsFinal` | **`Yes/No`** | `RG-37` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `EST_Activo` | `GeneraAlerta` | **`Yes/No`** | `RG-06` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `CierreConExcepcion` | **`Yes/No`** | `RG-03` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-06` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoExcepcion` | **`LongText`** | `RG-03` | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OTID` | **`Ref`** → `OT_OrdenesTrabajo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `RequiereSegundaVisita` | **`Yes/No`** | `RG-10` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | **`Ref`** → `EOT_EstadosOrden` | `RG-37` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `SupervisorID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `Activo` | **`Yes/No`** | `RG-38` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `PLA_PlanMantenimiento` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-36` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `SED_Sedes` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `CalzadaID` | **`Ref`** → `CAL_Calzadas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Criticidad` | **`Enum`** · valores: `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `MotivoBaja` | **`Enum`** · valores: `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `ACT_Activos` | `SentidoID` | **`Ref`** → `SEN_Sentidos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CAL_Calzadas` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `ChecklistID` | **`Ref`** → `CHK_Checklists` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `Contestada` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `Observacion` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHD_ChecklistDetalle` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `RespuestaBoolean` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `RespuestaLista` | **`Enum`** | — | el contenido no declara el conjunto de valores permitidos |
| `CHD_ChecklistDetalle` | `RespuestaTexto` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHK_Checklists` | `Finalizado` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHK_Checklists` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `EOT_EstadosOrden` | `QuienCambia` | **`Enum`** · valores: `Sistema` · `Tecnico` · `Supervisor` | — | el contenido no declara el conjunto de valores permitidos |
| `EST_Activo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FAL_ModosFalla` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FAL_ModosFalla` | `Criticidad` | **`Enum`** · valores: `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `FAL_ModosFalla` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FIR_Firmas` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FIR_Firmas` | `Imagen` | **`Signature`** | — | igual que Image |
| `FIR_Firmas` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FIR_Firmas` | `TipoFirma` | **`Enum`** · valores: `Tecnico` | — | el contenido no declara el conjunto de valores permitidos |
| `FOT_Fotografias` | `Archivo` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `FOT_Fotografias` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FOT_Fotografias` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FOT_Fotografias` | `PrecisionGPS` | **`Number`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `FOT_Fotografias` | `Tipo` | **`Enum`** · valores: `Antes` · `Despues` · `Novedad` | — | el contenido no declara el conjunto de valores permitidos |
| `FRE_Frecuencias` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Formularios` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `FormularioID` | **`Ref`** → `FRM_Formularios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `Obligatoria` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereFirma` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereFoto` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `FRM_Preguntas` | `SeccionID` | **`Ref`** → `FRM_Secciones` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `TipoRespuestaID` | **`Ref`** → `TPR_TiposRespuesta` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Secciones` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `LST_ValoresLista` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `LST_ValoresLista` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `AprobadoSupervisor` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `MAN_Mantenimientos` | `ModoFallaID` | **`Ref`** → `FAL_ModosFalla` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoPendienteID` | **`Ref`** → `MOT_MotivosPendiente` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `ObservacionRechazo` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OrigenApertura` | **`Enum`** · valores: `QR` · `Lista` | — | el contenido no declara el conjunto de valores permitidos |
| `MAN_Mantenimientos` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MOT_MotivosPendiente` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MOT_MotivosPendiente` | `GeneraSeguimiento` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `NOV_Novedades` | `ActivoID` | **`Ref`** → `ACT_Activos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `NOV_Novedades` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `NOV_Novedades` | `Estado` | **`Enum`** · valores: `Reportada` · `Aceptada` · `Descartada` | — | el contenido no declara el conjunto de valores permitidos |
| `NOV_Novedades` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `NOV_Novedades` | `Fotografia` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `NOV_Novedades` | `Tipo` | **`Enum`** · valores: `Activo no inventariado` · `Falla detectada` | — | el contenido no declara el conjunto de valores permitidos |
| `NOV_Novedades` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `OT_OrdenesTrabajo` | `CerradaPor` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `OTOrigenID` | **`Ref`** → `OT_OrdenesTrabajo` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `OT_OrdenesTrabajo` | `Tipo` | **`Enum`** · valores: `Preventivo` · `Correctivo` | — | el contenido no declara el conjunto de valores permitidos |
| `PAR_Parametros` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `PAR_Parametros` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `PLA_PlanMantenimiento` | `ResponsableID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ROL_Roles` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `SED_Sedes` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `SEN_Sentidos` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TIP_TiposActivo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TIP_TiposActivo` | `Categoria` | **`Enum`** · valores: `ITS` · `Electrico` · `Comunicaciones` · `TI` | — | el contenido no declara el conjunto de valores permitidos |
| `TIP_TiposActivo` | `FormularioID` | **`Ref`** → `FRM_Formularios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `TIP_TiposActivo` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `TIP_TiposActivo` | `TieneQR` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TPR_TiposRespuesta` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `UNF_UnidadesFuncionales` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `USR_Usuarios` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `USR_Usuarios` | `RolID` | **`Ref`** → `ROL_Roles` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |

### Las 17 que el NOMBRE consigue

Deberían haber entrado bien porque su nombre lleva la palabra que AppSheet reconoce.
**Compruébalas igual**: es una heurística, no una garantía.

- `ACT_Activos.FechaBaja` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `ACT_Activos.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `CHK_Checklists.FechaFin` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `CHK_Checklists.FechaInicio` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `FOT_Fotografias.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `MAN_Mantenimientos.Coordenadas_Cierre_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `MAN_Mantenimientos.FechaAprobacion` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraEscaneo` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraFin` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraInicio` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.UbicacionEscaneo_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `NOV_Novedades.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `OT_OrdenesTrabajo.FechaCierre` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `OT_OrdenesTrabajo.FechaProgramada` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `PLA_PlanMantenimiento.ProximaFecha` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `SED_Sedes.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `USR_Usuarios.FechaIngreso` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)

**Cómo se lee de vuelta: NADIE, salvo tú.**

**No hay comando.** La API v2 devuelve filas, no esquema: no hay forma de preguntarle de que tipo es una columna. Se cotejan contra TIPOS_ESPERADOS.md, y lo que quede escrito es la unica evidencia.

Por eso este paso se cierra **copiando literalmente lo que ves**, incluso
cuando coincida. «Coincide» no es evidencia; el texto sí.

### Las 87 que dependen del contenido

AppSheet debería acertar leyendo los valores — **cuando los hay**. Las de una tabla vacía no
tienen contenido que leer, así que estas también hay que mirarlas ahí. La lista completa, tabla
por tabla, está en [`TIPOS_ESPERADOS.md`](TIPOS_ESPERADOS.md).

> **El caso que desarma la confianza en el contenido:** `SED_Sedes.TramoINVIAS` tenía un valor
> real y representativo, `5607`, y AppSheet la tipó **`Number`**. El modelo dice `Text`, y el día
> que operación escriba `55CN03` no cabrá. Tener el dato correcto no basta.

## Paso 5 — La etiqueta de cada tabla, que no la declaraba nadie

**Cómo se lee de vuelta: NADIE, salvo tú.**

**No hay comando.** El Label es lo que el tecnico ve en los desplegables. Se mira en Data > Columns, una por tabla.

Por eso este paso se cierra **copiando literalmente lo que ves**, incluso
cuando coincida. «Coincide» no es evidencia; el texto sí.

`Label` es la columna que **representa una fila en las listas y en los desplegables**. No estaba
en el modelo ni en ningún documento: la elegía AppSheet, y elige la primera columna de texto, que
casi siempre es la clave.

No rompe nada, y por eso nadie lo miraba. Lo que pasa es que el técnico abre el desplegable para
asignar una orden y ve **`USR-001`, `USR-004`** en vez de los nombres.

### Antes de marcar nada: 2 de esas etiquetas **hay que crearlas**

No son columnas de la hoja. Son **columnas virtuales**: las calcula AppSheet y no se guardan
en el Sheets. Es lo que Google documenta para una etiqueta compuesta de varias columnas.

En *Data > Columns > la tabla*, **`Add virtual column`**, y así:

| Tabla | Nombre | `App formula` |
|---|---|---|
| `OT_OrdenesTrabajo` | **`Etiqueta`** | `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` |
| `PLA_PlanMantenimiento` | **`Etiqueta`** | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` |

Y después, en esa misma columna virtual: **`Show?` activo** —sin eso AppSheet no acepta que
sea etiqueta— y **`Label` marcado**. Si la tabla ya tenía otra columna con `Label`,
**desmárcala primero**: solo puede haber una.

En *Data > Columns*, marca la casilla **`Label`** de estas columnas:

| Tabla | Referencias que la apuntan | `Label` |
|---|---|---|
| `USR_Usuarios` | 7 | **`Nombres`** |
| `ACT_Activos` | 3 | **`Nombre`** |
| `FRM_Formularios` | 3 | **`Nombre`** |
| `MAN_Mantenimientos` | 3 | *ninguna: la clave la identifica, y está decidido así* |
| `UNF_UnidadesFuncionales` | 3 | **`Nombre`** |
| `OT_OrdenesTrabajo` | 2 | **`Etiqueta`** |
| `FRE_Frecuencias` | 2 | **`Nombre`** |
| `FRM_Preguntas` | 2 | **`Pregunta`** |
| `EST_Activo` | 2 | **`Nombre`** |
| `TIP_TiposActivo` | 2 | **`Nombre`** |
| `MOT_MotivosPendiente` | 1 | **`Nombre`** |
| `EOT_EstadosOrden` | 1 | **`Nombre`** |
| `TPR_TiposRespuesta` | 1 | **`Nombre`** |
| `SED_Sedes` | 1 | **`Nombre`** |
| `CAL_Calzadas` | 1 | **`Nombre`** |
| `ROL_Roles` | 1 | **`Nombre`** |
| `SEN_Sentidos` | 1 | **`Nombre`** |
| `FRM_Secciones` | 1 | **`Nombre`** |
| `CHK_Checklists` | 1 | *ninguna: la clave la identifica, y está decidido así* |
| `FAL_ModosFalla` | 1 | **`Nombre`** |

> Las 2 sin etiqueta **no son un hueco**: se identifican por su clave y su fecha. Está
> decidido, no olvidado.

## Paso 6 — Las 49 expresiones que no son reglas, y por eso no salen en ningún otro sitio

El modelo las declara en la columna, **sin `REGLA` propia**. Y los documentos de expresiones
—`RECONSTRUCCION_EXPRESIONES.md` y `PROMPT_EXPRESIONES.md`— se generan recorriendo `REGLAS`,
así que **ninguna aparece ahí**. Si no se ponen aquí, no las pone nadie.

La mayoría son `TRUE` en columnas `Activo`, y saltárselas solo deja el valor en blanco. Pero
las hay que sostienen la evidencia: quién registró un mantenimiento, dónde y con quién se tomó
una fotografía. Esas nacen vacías y nadie lo nota.

| Tabla | Columna | Propiedad | Expresión |
|---|---|---|---|
| `ASG_AsignacionZona` | `Activo` | `Initial value` | `TRUE` |
| `CAL_Calzadas` | `Activo` | `Initial value` | `TRUE` |
| `CHD_ChecklistDetalle` | `Contestada` | `Initial value` | `FALSE` |
| `CHK_Checklists` | `FechaInicio` | `Initial value` | `NOW()` |
| `CHK_Checklists` | `Finalizado` | `Initial value` | `FALSE` |
| `EOT_EstadosOrden` | `Activo` | `Initial value` | `TRUE` |
| `EOT_EstadosOrden` | `EsFinal` | `Initial value` | `FALSE` |
| `EST_Activo` | `Activo` | `Initial value` | `TRUE` |
| `EST_Activo` | `GeneraAlerta` | `Initial value` | `FALSE` |
| `FAL_ModosFalla` | `Activo` | `Initial value` | `TRUE` |
| `FOT_Fotografias` | `PrecisionGPS` | `Initial value` | `USERLOCATIONACCURACY()` |
| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
| `FOT_Fotografias` | `Usuario` | `Initial value` | `USEREMAIL()` |
| `FRE_Frecuencias` | `Activo` | `Initial value` | `TRUE` |
| `FRM_Formularios` | `Activo` | `Initial value` | `TRUE` |
| `FRM_Formularios` | `Version` | `Initial value` | `1` |
| `FRM_Preguntas` | `Activo` | `Initial value` | `TRUE` |
| `FRM_Preguntas` | `Obligatoria` | `Initial value` | `TRUE` |
| `FRM_Preguntas` | `RequiereFirma` | `Initial value` | `FALSE` |
| `FRM_Preguntas` | `RequiereFoto` | `Initial value` | `FALSE` |
| `FRM_Preguntas` | `RequiereGPS` | `Initial value` | `FALSE` |
| `FRM_Preguntas` | `Version` | `Initial value` | `1` |
| `FRM_Secciones` | `Activo` | `Initial value` | `TRUE` |
| `LST_ValoresLista` | `Activo` | `Initial value` | `TRUE` |
| `MAN_Mantenimientos` | `Activo` | `Initial value` | `TRUE` |
| `MAN_Mantenimientos` | `AprobadoSupervisor` | `Initial value` | `FALSE` |
| `MAN_Mantenimientos` | `FechaHoraInicio` | `Initial value` | `NOW()` |
| `MAN_Mantenimientos` | `OrigenApertura` | `Initial value` | `Lista` |
| `MAN_Mantenimientos` | `RequiereSegundaVisita` | `Initial value` | `FALSE` |
| `MAN_Mantenimientos` | `TecnicoID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `MAN_Mantenimientos` | `UsuarioRegistro` | `Initial value` | `USEREMAIL()` |
| `MOT_MotivosPendiente` | `Activo` | `Initial value` | `TRUE` |
| `MOT_MotivosPendiente` | `GeneraSeguimiento` | `Initial value` | `TRUE` |
| `NOV_Novedades` | `Estado` | `Initial value` | `Reportada` |
| `NOV_Novedades` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
| `NOV_Novedades` | `UsuarioID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `OT_OrdenesTrabajo` | `Activo` | `Initial value` | `TRUE` |
| `PAR_Parametros` | `Activo` | `Initial value` | `TRUE` |
| `PLA_PlanMantenimiento` | `Activo` | `Initial value` | `TRUE` |
| `ROL_Roles` | `Activo` | `Initial value` | `TRUE` |
| `SED_Sedes` | `Activo` | `Initial value` | `TRUE` |
| `SEN_Sentidos` | `Activo` | `Initial value` | `TRUE` |
| `TIP_TiposActivo` | `Activo` | `Initial value` | `TRUE` |
| `TIP_TiposActivo` | `RadioGeofencingKm` | `Initial value` | `0.2` |
| `TIP_TiposActivo` | `RequiereGPS` | `Initial value` | `TRUE` |
| `TIP_TiposActivo` | `TieneQR` | `Initial value` | `TRUE` |
| `TPR_TiposRespuesta` | `Activo` | `Initial value` | `TRUE` |
| `UNF_UnidadesFuncionales` | `Activo` | `Initial value` | `TRUE` |
| `USR_Usuarios` | `Activo` | `Initial value` | `TRUE` |

## Paso 7 — Las 21 reglas

Están **enteras y sin cortar** en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md),
con su tabla, su columna y su tipo —`Valid_If`, `Initial value`, `App formula`, bot—. Cópialas de
ahí. **No las escribas de memoria ni las adaptes.**


## Paso 8 — Comprobar, y aquí está lo que solo se puede ver ahora

**Las 8 tablas que llegaron vacías eligieron su clave a ciegas**, porque AppSheet la infiere de
los datos y no había. Y son justo las que generan clave con `UNIQUEID()`, es decir alfanumérica:
**si alguna quedó `Number`, cada fila que cree un técnico se perderá sin aviso.**

- `CHD_ChecklistDetalle`
- `CHK_Checklists`
- `FIR_Firmas`
- `FOT_Fotografias`
- `MAN_Mantenimientos`
- `NOV_Novedades`
- `OT_OrdenesTrabajo`
- `PLA_PlanMantenimiento`

Abre cada una y confirma que su clave es **`Text`**.

Después, las pruebas de [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).

## Qué reportar al terminar

1. **Cuántas referencias pusiste**, y si alguna no te dejó.
2. **Las 4 de `IsPartOf`**, y confirmación de que `MAN_Mantenimientos.OTID` quedó DESMARCADA.
3. **`Deletes` retirado** en las dos tablas.
4. **Las claves de las 8 tablas vacías**: qué tipo tenía cada una.
5. **Cualquier tipo que encontraras distinto** del que dice este documento. Eso es un hallazgo,
   no un estorbo: significa que la inferencia hizo algo que no esperábamos.

## Lo que NO debes hacer

- **No subas ningún Excel ni toques la hoja.** El dato está bien; lo que falta es configuración.
- **No pruebes expresiones escribiéndolas dentro de una columna.** Se prueban en el Asistente de
  Expresiones, que solo evalúa, y se cierra **sin dar a `Done`**. Escribir una expresión dentro de
  una columna la convierte en configuración activa: ya ocurrió una vez y dejó una `App formula`
  escribiendo coordenadas dentro de una columna retirada.
- **No borres ninguna columna.**
- **No publiques.** Ninguna de las coordenadas de los activos es real, así que en campo la
  comprobación de distancia no significa nada todavía.
