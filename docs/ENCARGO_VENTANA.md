# Encargo: cerrar la ventana barata

**Autocontenido. Cópialo íntegro desde la línea siguiente.**

**Generado** por `scripts/generar_encargo_ventana.py`. No editar a mano.

---

Trabajas en el editor de AppSheet de **`_SISGA_-323965761`**.

```
https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e
```

## Por qué esto es urgente y lo demás no

**8 tablas están hoy en CERO filas**, y esa vacuidad no es un estado neutro: es lo que hace que
corregir un tipo o una clave cueste **un clic**. Con una sola fila dentro, cada corrección pasa a
ser una migración.

Y el primer registro la cierra **para siempre**: son tablas transaccionales, así que una vez que
entren órdenes y mantenimientos no vuelven a estar vacías nunca.

Todo lo que sigue vive dentro de esa ventana. Lo que no está aquí es porque no.

## Paso 1 — Las 2 columnas virtuales `Etiqueta`

**No son columnas de la hoja.** Son columnas **virtuales**: las calcula AppSheet y no se guardan
en el Sheets. Es lo que Google documenta para una etiqueta compuesta de varias columnas.

Existen porque `OTID` y `PlanID` pasaron a `UNIQUEID()`: una orden ya no se llama `OT-0042` sino
`a3f9c2e1`, y sin etiqueta el técnico vería eso en cada desplegable.

En *Data > Columns > la tabla*, botón **`Add virtual column`**:

| Tabla | Nombre | `App formula` |
|---|---|---|
| `OT_OrdenesTrabajo` | **`Etiqueta`** | `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` |
| `PLA_PlanMantenimiento` | **`Etiqueta`** | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` |

Y en esa misma columna virtual, dos cosas que la documentación de Google prescribe y que es fácil
saltarse:

- **`Show?` activo.** Sin eso AppSheet no acepta que sea etiqueta.
- **`Label` marcado** — y si la tabla ya tenía otra columna con `Label`, **desmárcala primero**.
  Solo puede haber una por tabla.

## Paso 2 — Cotejar 52 tipos, y dejar constancia

**Esto no es para cambiarlos: es para mirarlos.** Lo más probable es que ya estén, porque una
sesión anterior recorrió estas tablas. Pero *reportado* no es *verificado*, y de eso este
proyecto lleva cuatro informes de «hecho» que no lo estaban.

**Anota lo que veas aunque coincida.** No hay comando que lo recupere después: la API de AppSheet
devuelve filas, no esquema. Tu anotación es la única evidencia que va a existir.

### `CHD_ChecklistDetalle` — 7 columnas

| Columna | Debe ser |
|---|---|
| `ChecklistID` | **`Ref`** → `CHK_Checklists` |
| `Contestada` | **`Yes/No`** |
| `Observacion` | **`LongText`** |
| `PreguntaID` | **`Ref`** → `FRM_Preguntas` |
| `RespuestaBoolean` | **`Yes/No`** |
| `RespuestaLista` | **`Enum`** |
| `RespuestaTexto` | **`LongText`** |

### `CHK_Checklists` — 3 columnas

| Columna | Debe ser |
|---|---|
| `Finalizado` | **`Yes/No`** |
| `FormularioID` | **`Ref`** → `FRM_Formularios` |
| `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` |

### `FIR_Firmas` — 4 columnas

| Columna | Debe ser |
|---|---|
| `FechaHora` | **`ChangeTimestamp`** |
| `Imagen` | **`Signature`** |
| `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` |
| `TipoFirma` | **`Enum`** · valores: `Tecnico` |

### `FOT_Fotografias` — 4 columnas

| Columna | Debe ser |
|---|---|
| `Archivo` | **`Image`** |
| `FechaHora` | **`ChangeTimestamp`** |
| `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` |
| `Tipo` | **`Enum`** · valores: `Antes` · `Despues` · `Novedad` |

### `MAN_Mantenimientos` — 14 columnas

| Columna | Debe ser |
|---|---|
| `Activo` | **`Yes/No`** |
| `AprobadoSupervisor` | **`Yes/No`** |
| `CierreConExcepcion` | **`Yes/No`** |
| `EstadoActivoID` | **`Ref`** → `EST_Activo` |
| `FechaHoraRegistro` | **`ChangeTimestamp`** |
| `ModoFallaID` | **`Ref`** → `FAL_ModosFalla` |
| `MotivoExcepcion` | **`LongText`** |
| `MotivoPendienteID` | **`Ref`** → `MOT_MotivosPendiente` |
| `OTID` | **`Ref`** → `OT_OrdenesTrabajo` |
| `ObservacionRechazo` | **`LongText`** |
| `Observaciones` | **`LongText`** |
| `OrigenApertura` | **`Enum`** · valores: `QR` · `Lista` |
| `RequiereSegundaVisita` | **`Yes/No`** |
| `TecnicoID` | **`Ref`** → `USR_Usuarios` |

### `NOV_Novedades` — 7 columnas

| Columna | Debe ser |
|---|---|
| `ActivoID` | **`Ref`** → `ACT_Activos` |
| `Descripcion` | **`LongText`** |
| `Estado` | **`Enum`** · valores: `Reportada` · `Aceptada` · `Descartada` |
| `FechaHora` | **`ChangeTimestamp`** |
| `Fotografia` | **`Image`** |
| `Tipo` | **`Enum`** · valores: `Activo no inventariado` · `Falla detectada` |
| `UsuarioID` | **`Ref`** → `USR_Usuarios` |

### `OT_OrdenesTrabajo` — 9 columnas

| Columna | Debe ser |
|---|---|
| `Activo` | **`Yes/No`** |
| `ActivoID` | **`Ref`** → `ACT_Activos` |
| `CerradaPor` | **`Ref`** → `USR_Usuarios` |
| `EstadoOrdenID` | **`Ref`** → `EOT_EstadosOrden` |
| `OTOrigenID` | **`Ref`** → `OT_OrdenesTrabajo` |
| `Observaciones` | **`LongText`** |
| `SupervisorID` | **`Ref`** → `USR_Usuarios` |
| `TecnicoID` | **`Ref`** → `USR_Usuarios` |
| `Tipo` | **`Enum`** · valores: `Preventivo` · `Correctivo` |

### `PLA_PlanMantenimiento` — 4 columnas

| Columna | Debe ser |
|---|---|
| `Activo` | **`Yes/No`** |
| `ActivoID` | **`Ref`** → `ACT_Activos` |
| `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` |
| `ResponsableID` | **`Ref`** → `USR_Usuarios` |

## Lo que NO entra, y por qué

| | Por qué queda fuera |
|---|---|
| `UNF_UnidadesFuncionales` y `USR_Usuarios` | Tienen filas. Su ventana se cerró hace tiempo, así que pueden esperar |
| Los bots | No dependen de la ventana |
| `RG-04` y `RG-05`, los `Security Filter` | Van **los últimos**. Al ponerlos, la API deja de devolver las filas de esa tabla y ni `auditar_cableado.py` ni `instantanea.py` pueden volver a mirarla |
| `RG-03` | Ya **entra**: `ESPEC-004`/`ORDEN-004` la desbloqueó — `CierreConExcepcion` deja de calcularse sola y pasa a ser una casilla que marca el técnico. `RG-02` y `RG-19` se retiraron del modelo (`RG-02` usaba `USERLOCATIONACCURACY()`, que no existe en AppSheet) |

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


## Antes de empezar y al terminar

```bash
python scripts/instantanea.py guardar antes-de-la-ventana
```

Un cambio de tipo **puede escribir en los datos**. Ya pasó: convertir una columna a `Enum`
reescribió una celda añadiéndole un espacio al final. Sin foto previa no hay vuelta atrás.

Al terminar:

```bash
python scripts/instantanea.py guardar despues-de-la-ventana
python scripts/instantanea.py comparar antes-de-la-ventana despues-de-la-ventana
python scripts/auditar_cableado.py
```

La comparación debe decir **NINGUNA CELDA CAMBIO**, y el auditor **0 correcciones**. Si dicen
otra cosa, para y reporta la salida entera.

## Lo que no puedes hacer

- **No pobles ninguna de las 8 tablas.** Es justo lo que cerraría la ventana.
- **No toques ninguna referencia.** Están puestas: el auditor sale con 0 correcciones. Pero
  «puestas» no es «auditadas» —de las 39, solo unas pocas están **verificadas** y el resto son
  **compatibles no atribuidas**—, así que si ves algo raro, repórtalo en vez de corregirlo.
- **No pongas los `Security Filter`.** Apagan los instrumentos sobre esa tabla.
- **No pulses `Regenerate Structure`.** Fusiona, no reemplaza, y no se deshace.
- **No ejecutes ningún `.js` de `scripts/`.** Son experimentos abandonados que hacen clic a
  ciegas, y son la causa de que cinco columnas acabaran apuntando a la tabla equivocada.
- **No publiques.**
- Si AppSheet muestra un error, **ese error describe algo real**. Reporta el texto exacto y para.

## Qué reportar

1. Las 2 columnas virtuales: si se crearon, con qué `App formula`, y el estado de `Show?` y
   `Label` en cada una.
2. Tabla por tabla, **qué tipo tenía cada columna antes** — aunque no lo cambies.
3. La salida entera de los tres comandos del cierre.

No des una tabla por cerrada sin su comparación.
