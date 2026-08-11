# Encargo de las expresiones — Fase C

**Autocontenido. Cópialo íntegro desde la línea siguiente.**

**Generado** por `scripts/generar_prompt_expresiones.py`. No editar a mano: las expresiones y
las cadenas de referencias salen de `scripts/modelo_objetivo.py`.

---

Vas a poner **21 reglas** en la aplicación **`_SISGA_-323965761`** de Google AppSheet.
Las 39 referencias son el paso anterior. **Este documento no sabe si están puestas** —sale del
modelo, así que describe el destino—. Compruébalo antes de empezar:

```bash
python scripts/auditar_cableado.py
```

Si no sale con **0 correcciones**, para: una expresión con puntos sobre una referencia sin cablear
falla, y el error te va a mandar a mirar la expresión en vez del cableado.

```
https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e
```

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


## Lo primero, porque ya salió mal tres veces

**Una expresión con puntos no falla por estar mal escrita. Falla porque un salto de su cadena no
está cableado.**

El error de AppSheet lo dice literalmente. Cuando `RG-01` daba
`Can't find column "RadioGeofencingKm" in table "SED_Sedes"`, no había que buscar otro nombre
de columna: había que ver por qué la cadena aterrizaba en `SED_Sedes`. Y era que
`ACT_Activos.TipoActivoID` apuntaba a la tabla de sedes.

> **NO reescribas una expresión para que el error desaparezca.** Se propusieron dos veces dos
> arreglos que parecían razonables: sustituir el radio por un `LOOKUP` a `PAR_Parametros`, y
> quitar un salto de la cadena. El primero habría colapsado en un solo número los **tres radios**
> distintos —1,5 km para la fibra óptica, 0,05 km para un poste SOS—, y el segundo apunta a una
> columna que no existe. Ninguno de los dos da error: dejan el cierre en campo **aceptando lo que
> debe rechazar**.

Si una expresión falla, mira la tabla que nombra el error y búscala en la columna **«atraviesa»**
de la tabla de abajo. Ahí está el salto roto.

## Lo segundo: en qué tabla estás

El mismo nombre es **clave** en una tabla y **referencia** en otra. `EstadoActivoID` es la clave
de `EST_Activo` y la referencia hacia ella en `ACT_Activos`. Editarlo en la tabla equivocada
produce esto:

```
Column Name 'EstadoActivoID' in Schema 'EST_Activo_Schema'
contains a cyclical table reference to 'EST_Activo'.
```

Ya pasó el 2026-08-10. **Antes de tocar una columna, comprueba en qué tabla estás.** Cada regla
de abajo dice la suya, y no es negociable: la misma columna en otra tabla es otra cosa.

## Las 21 reglas

Cada una: entra a la **tabla**, abre la **columna**, y pon la expresión en la **propiedad** que
dice. Las que **escriben en la hoja** van al final a propósito.

| # | Regla | Tabla | Columna | Propiedad | Atraviesa |
|---|---|---|---|---|---|
| 1 | `RG-01` | `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | `Valid_If` | `OT_OrdenesTrabajo` → `ACT_Activos` · `OT_OrdenesTrabajo` → `ACT_Activos` → `TIP_TiposActivo` |
| 2 | `RG-03` | `MAN_Mantenimientos` | `MotivoExcepcion` | `Required_If` | — |
| 3 | `RG-13` | `MAN_Mantenimientos` | `(tabla)` | `Verificacion de evidencia` | — |
| 4 | `RG-14` | `OT_OrdenesTrabajo` | `(tabla)` | `Are updates allowed` | — |
| 5 | `RG-15` | `MAN_Mantenimientos` | `(tabla)` | `Are updates allowed` | — |
| 6 | `RG-17` | `ACT_Activos` | `FechaBaja` | `Required_If` | `EST_Activo` |
| 7 | `RG-18` | `ACT_Activos` | `(tabla)` | `Doctrina de reportes` | — |
| 8 | `RG-20` | `MAN_Mantenimientos` | `(varias)` | `Editable_If` | — |
| 9 | `RG-34` | `ACT_Activos` | `UnidadFuncionalID` | `Valid_If` | `SED_Sedes` |
| 10 | `RG-02` | `MAN_Mantenimientos` | `Precision_GPS` | `Initial value` | — |
| 11 | `RG-06` | `MAN_Mantenimientos` | `(tabla)` | `Bot` | `EST_Activo` |
| 12 | `RG-07` | `OT_OrdenesTrabajo` | `(tabla)` | `Bot` | — |
| 13 | `RG-08` | `OT_OrdenesTrabajo` | `EstadoOrdenID` | `Bot programado` | `EOT_EstadosOrden` |
| 14 | `RG-09` | `CHK_Checklists` | `VersionFormulario` | `Initial value` | `FRM_Formularios` |
| 15 | `RG-10` | `MAN_Mantenimientos` | `(tabla)` | `Bot` | — |
| 16 | `RG-11` | `PLA_PlanMantenimiento` | `ProximaFecha` | `App formula` | `FRE_Frecuencias` |
| 17 | `RG-12` | `PLA_PlanMantenimiento` | `(tabla)` | `Bot programado` | — |
| 18 | `RG-16` | `ACT_Activos` | `Activo` | `App formula` | `EST_Activo` |
| 19 | `RG-19` | `MAN_Mantenimientos` | `CierreConExcepcion` | `App formula` | — |
| 20 | `RG-04` | `ACT_Activos` | `(tabla)` | `Security Filter` | `USR_Usuarios` |
| 21 | `RG-05` | `OT_OrdenesTrabajo` | `(tabla)` | `Security Filter` | `USR_Usuarios` · `USR_Usuarios` |

> Las de `App formula`, `Initial value` y las de tipo bot **escriben**. Ponerlas antes de haber
> comprobado las demás significa soltarlas sobre el inventario entero sin saber qué escriben.
>
> **Y los dos `Security Filter` van los últimos de todos.** En cuanto entran, la API deja de
> devolver las filas de esa tabla —llama sin usuario, así que `USEREMAIL()` queda en blanco— y
> ni `instantanea.py` ni `auditar_cableado.py` pueden volver a comprobar nada ahí. Ponerlos
> antes es apagar la luz de la habitación en la que estás trabajando.

## Los 5 bots no van en una columna, y esto es lo que faltaba

Las otras 16 se ponen en una propiedad de una columna o de una tabla. **Un bot no.** Vive en
`Automation > Bots` —el icono del rayo— y tiene tres partes, no una expresión suelta:

```
Event       cuando se dispara:  la tabla + Adds / Updates / Adds and Updates,
                                o Schedule si es programado
Condition   una expresion que decide si sigue
Step        lo que hace
```

La tabla de arriba da el **Event** en la columna de la expresión y la **Condition** en el detalle.
El `Step` lo dice la descripción de cada regla.

### La trampa: un bot que AÑADE UNA FILA se hace en dos sitios

Si el `Step` es *añadir una fila a otra tabla*, **no se configura dentro del bot**. AppSheet
interpreta que quieres generar un documento y te pide una plantilla PDF y valores de retorno, y
ahí es donde se atasca todo el mundo.

El orden es este:

1. **`Data > Actions` → `Add Action`.** Ahí se define *qué fila se crea y con qué valores*:
   `For a record of this table` = la tabla de origen, y `Do this` = **`Data: add a new row to
   another table using values from this row`**.
2. **`Automation > Bots` → tu bot → `Add a step` → `Run a data action`**, y eliges la que
   acabas de crear.

Afecta a `RG-10` y a `RG-12`, que son los dos que crean órdenes.

> **Y un aviso que vale más que el procedimiento:** un bot que crea filas en `OT_OrdenesTrabajo`
> tiene hoy un problema abierto. `OTID` es clave legible y **nadie la genera**, así que la fila
> nacería sin identificador y AppSheet la descarta sin decir nada. Está en el pipeline. **No
> pongas `RG-10` ni `RG-12` en producción hasta que se resuelva.**

## Las expresiones, enteras

**Cópialas de aquí. No las escribas de memoria ni las adaptes.**

### RG-01 — `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`

**Valid_If** · cubre `RF-012`

```
DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
```

Impide cerrar lejos del activo, con radio por tipo. La ruta atraviesa dos referencias, de ahi que cablearlas sea el primer paso de todo.

Atraviesa **3 referencias distintas**:

- `MAN_Mantenimientos.OTID` → `OT_OrdenesTrabajo`
- `OT_OrdenesTrabajo.ActivoID` → `ACT_Activos`
- `ACT_Activos.TipoActivoID` → `TIP_TiposActivo`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-03 — `MAN_Mantenimientos.MotivoExcepcion`

**Required_If** · cubre `D-04`

```
[CierreConExcepcion] = TRUE
```

Si el tecnico cierra con excepcion por GPS deficiente, debe justificarlo por escrito.

### RG-13 — `MAN_Mantenimientos.(tabla)`

**Verificacion de evidencia** · cubre `Prueba de presencia`

```
DISTANCE([UbicacionEscaneo_LatLong], [Coordenadas_Cierre_LatLong]) <= 0.5
```

Contrasta donde escaneo con donde cerro. Una diferencia grande indica que escaneo en un sitio y cerro en otro. No bloquea: se reporta.

### RG-14 — `OT_OrdenesTrabajo.(tabla)`

**Are updates allowed** · cubre `Evidencia defendible`

```
Updates, Adds
```

Se retira Deletes. Una orden no se borra: se anula con Activo = FALSE, que deja traza de que existio. Si el boton no esta, no hay accidente posible.

### RG-15 — `MAN_Mantenimientos.(tabla)`

**Are updates allowed** · cubre `Evidencia defendible`

```
Updates, Adds
```

Se retira Deletes. Es la decision central del sistema: la ejecucion es la prueba de que alguien estuvo frente al equipo. Protegido aqui arriba, el IsPartOf de FOT, FIR y CHK nunca llega a dispararse. Nota: esto protege DENTRO de la app; nadie impide borrar la fila a mano en el Sheets, donde hay dos cuentas con permiso de edicion.

### RG-17 — `ACT_Activos.FechaBaja`

**Required_If** · cubre `Baja de activos`

```
[EstadoActivoID].[Nombre] = "Retirado"
```

Contra [Nombre], no contra la clave. Si se retira un activo hay que decir cuando. Un historico que no puede explicar por que un activo dejo de recibir mantenimiento no es defendible.

Atraviesa **1 referencia**:

- `ACT_Activos.EstadoActivoID` → `EST_Activo`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-18 — `ACT_Activos.(tabla)`

**Doctrina de reportes** · cubre `Baja de activos`

```
Ver descripcion: es una prohibicion, no una expresion a configurar
```

NO filtrar los reportes historicos por la bandera Activo del activo padre. Un reporte HISTORICO filtra por la fecha y el estado de la TRANSACCION, nunca por el estado actual del activo padre. Filtrar por [ActivoID].[Activo] hace que al dar de baja un activo desaparezcan retroactivamente todos sus mantenimientos pasados: el informe del ano anterior cambia solo y muestra menos trabajo del que se hizo. Ante interventoria eso no parece un filtro mal puesto, parece que el mantenimiento nunca se ejecuto.

### RG-20 — `MAN_Mantenimientos.(varias)`

**Editable_If** · cubre `Prueba de presencia`

```
FALSE
```

Sobre Coordenadas_Cierre, Precision_GPS, UbicacionEscaneo y FechaHoraEscaneo. SIN ESTO EL GEOFENCING ES DECORATIVO: HERE() y USERLOCATIONACCURACY() son Initial value, no App formula, y un Initial value SI es editable. Coordenadas_Cierre es un LatLong, que en un formulario AppSheet dibuja como un pin arrastrable sobre un mapa, y la ubicacion del activo esta visible en la app: el tecnico arrastra el pin encima del activo y RG-01 valida sin protestar. La regla se cumplia y la presencia no quedaba probada.

### RG-34 — `ACT_Activos.UnidadFuncionalID`

**Valid_If** · cubre `RF-002`

```
OR(ISBLANK([SedeID]), [UnidadFuncionalID] = [SedeID].[UnidadFuncionalID])
```

El equipo bajo techo hereda donde esta de su edificacion. Sin esta regla la unidad funcional se guardaria en dos sitios -en el activo y en su sede- y podrian decir cosas distintas sin que nada protestara. Con ella hay un solo sitio donde mirar: si el activo tiene sede, manda la sede.

Atraviesa **1 referencia**:

- `ACT_Activos.SedeID` → `SED_Sedes`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-02 — `MAN_Mantenimientos.Precision_GPS`

**Initial value** · cubre `RF-011`

```
USERLOCATIONACCURACY()
```

Registra el error del satelite en metros, para distinguir un cierre legitimo de uno dudoso.

### RG-06 — `MAN_Mantenimientos.(tabla)`

**Bot** · cubre `RF-016`

```
[EstadoActivoID].[GeneraAlerta] = TRUE
```

Envia correo con informe PDF al CCO y al supervisor cuando el activo queda fuera de servicio.

Atraviesa **1 referencia**:

- `MAN_Mantenimientos.EstadoActivoID` → `EST_Activo`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-07 — `OT_OrdenesTrabajo.(tabla)`

**Bot** · cubre `RF-003`

```
Adds
```

Notifica por correo al tecnico cuando se le asigna una orden.

### RG-08 — `OT_OrdenesTrabajo.EstadoOrdenID`

**Bot programado** · cubre `D-06`

```
AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())
```

Marca como Vencida la orden cuya fecha programada paso sin cerrarse.

Atraviesa **1 referencia**:

- `OT_OrdenesTrabajo.EstadoOrdenID` → `EOT_EstadosOrden`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-09 — `CHK_Checklists.VersionFormulario`

**Initial value** · cubre `D-11`

```
[FormularioID].[Version]
```

Congela la version del formulario con que se respondio, para comparar historico.

Atraviesa **1 referencia**:

- `CHK_Checklists.FormularioID` → `FRM_Formularios`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-10 — `MAN_Mantenimientos.(tabla)`

**Bot** · cubre `D-07`

```
[RequiereSegundaVisita] = TRUE
```

Genera una orden de seguimiento enlazada a la original mediante OTOrigenID.

### RG-11 — `PLA_PlanMantenimiento.ProximaFecha`

**App formula** · cubre `Plan de mantenimiento`

```
[UltimaEjecucion] + [FrecuenciaID].[Dias]
```

Calcula cuando vuelve a tocar el preventivo de ese activo.

Atraviesa **1 referencia**:

- `PLA_PlanMantenimiento.FrecuenciaID` → `FRE_Frecuencias`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-12 — `PLA_PlanMantenimiento.(tabla)`

**Bot programado** · cubre `Plan de mantenimiento`

```
[ProximaFecha] <= TODAY() + 7
```

Genera las ordenes de la semana a partir del plan y notifica al tecnico responsable. REQUIERE PLAN PAGADO: en el gratuito los bots programados no se ejecutan.

### RG-16 — `ACT_Activos.Activo`

**App formula** · cubre `Baja de activos`

```
[EstadoActivoID].[Nombre] <> "Retirado"
```

La bandera se deriva del estado, no se edita. La comparacion va contra [Nombre] y NO contra la columna a secas: EstadoActivoID es un Ref y un Ref guarda la CLAVE del destino, que aqui vale 1 a 4. Comparar la clave con la cadena 'Retirado' es siempre cierto, y como esto es una App formula, ESCRIBE: pondria Activo=TRUE sobre el activo dado de baja. EST_Activo ya tiene el estado Retirado; mantener ademas una bandera independiente es el mismo dato en dos sitios, y algun dia diran cosas distintas sin forma de saber cual miente.

Atraviesa **1 referencia**:

- `ACT_Activos.EstadoActivoID` → `EST_Activo`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-19 — `MAN_Mantenimientos.CierreConExcepcion`

**App formula** · cubre `D-04`

```
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

Marca el cierre como excepcional cuando el error del satelite supera el umbral. Sin ella la columna existe y nadie la puebla: un cierre con 45 m de error seria indistinguible de uno con 8 m, y ahi se cae la cadena de evidencia. EL UMBRAL ES UN PARAMETRO, no un numero en la expresion: se calibra con las pruebas de campo y lo ajusta el administrador en una celda, sin abrir el editor. FALLA DE FORMA RUIDOSA: si el umbral no se puede leer, el OR con ISBLANK marca el cierre COMO EXCEPCIONAL. Sin eso, borrar la fila del parametro haria que todos los cierres saliesen limpios y nadie se enterase, que es la forma exacta del defecto de RG-16. Provisional 40 m, unas ocho veces la precision tipica de un movil a cielo abierto (4,9 m segun GPS.gov) y deja margen para montana y estructuras. D-04 decia 50; se baja a 40 tras comprobar que 45 m ya es nueve veces la norma.

### RG-04 — `ACT_Activos.(tabla)`

**Security Filter** · cubre `RF-004`

```
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))
```

Cada tecnico descarga solo los activos de las unidades funcionales que tiene asignadas. Controla el volumen de sincronizacion, no solo la visibilidad.

Atraviesa **1 referencia**:

- `ASG_AsignacionZona.UsuarioID` → `USR_Usuarios`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

### RG-05 — `OT_OrdenesTrabajo.(tabla)`

**Security Filter** · cubre `RF-004`

```
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

El tecnico ve sus ordenes; el supervisor, las que supervisa.

Atraviesa **2 referencias distintas**:

- `OT_OrdenesTrabajo.TecnicoID` → `USR_Usuarios`
- `OT_OrdenesTrabajo.SupervisorID` → `USR_Usuarios`

Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,
no en la expresión.

## Cómo se comprueba, y por qué depende de ti

**Cómo se lee de vuelta: NADIE, salvo tú.**

**No hay comando.** Valid_If, App formula, Initial value, Editable_If y los Security Filter no viajan por la API. Se copian del editor LITERALMENTE, sin resumir ni corregir: un espacio al final o una tilde de mas rompen la comparacion y no dan error.

Por eso este paso se cierra **copiando literalmente lo que ves**, incluso
cuando coincida. «Coincide» no es evidencia; el texto sí.

## Dos que hoy NO se pueden poner, y hay que saberlo antes de intentarlo

**`RG-02` es imposible tal como está declarada.** Usa `USERLOCATIONACCURACY()`, y esa función
**no existe en AppSheet**: la plataforma no expone la precisión del GPS al motor de expresiones.
La captura manual sí muestra al técnico los metros en pantalla, pero ese número no se puede
guardar en una columna. Deja `Precision_GPS` con tipo `Number` y **sin `Initial value`**.

Y arrastra dos más, así que no las des por buenas aunque las pongas:

```
RG-02   Precision_GPS = USERLOCATIONACCURACY()       no existe -> nunca se puebla
RG-19   CierreConExcepcion = Precision_GPS > umbral   blanco > numero -> siempre falso
RG-03   MotivoExcepcion obligatorio si excepcion      nunca se pide
```

Tres reglas bien configuradas y el mecanismo entero inerte. **Está pendiente de decidir** si
`CierreConExcepcion` pasa a ser una casilla que marca el técnico; hasta entonces, ponlas y no las
cuentes como funcionando.

> Es el patrón del día: una regla puede estar puesta, bien escrita, sin dar un solo error, y no
> hacer nada. Pasó por el tipo (`RG-03`), por el dato (`RG-06`, con `GeneraAlerta` vacía) y aquí
> por una función que no existe. `python scripts/verificar_datos.py` caza el segundo caso —G-05—;
> los otros dos solo se ven mirando.

## Al terminar

Antes de dar por buena ninguna:

```bash
python scripts/auditar_cableado.py      # que las 39 referencias sigan donde estaban
python scripts/validar_modelo.py        # que ninguna regla compare un Ref con un literal
```

La segunda existe por un motivo concreto. Comparar una columna `Ref` con un texto —
`[EstadoActivoID] <> "Retirado"`— **es siempre falso y no da error**: la referencia guarda
`EST-04`, no la palabra. Hay que escribir `[EstadoActivoID].[Nombre]`.

Reporta: qué reglas pusiste, cuáles dieron error y **con qué texto exacto**, y qué tabla nombraba
cada error. Ese texto es el diagnóstico, no un estorbo.

## Lo que NO debes hacer

- **No reescribas una expresión para silenciar un error.** Es la regla de arriba y es la que más
  veces se ha roto.
- **No pruebes expresiones escribiéndolas dentro de una columna.** Se prueban en el Asistente de
  Expresiones, que solo evalúa, y se cierra **sin dar a `Done`**.
- **No cambies ninguna referencia.** Están puestas y auditadas. Si una está mal, se reporta.
- **No publiques.** Ninguna coordenada está levantada en campo: se derivan del PK sobre el
  trazado, así que la comprobación de distancia todavía no significa nada en la vía.
