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

En *Data > Tables*, para `OT_OrdenesTrabajo` y `MAN_Mantenimientos`, en **Are updates allowed**:

```
Updates  si        Adds  si        Deletes  NO
```

**Por qué va primero y no después.** El paso 2 marca `IsPartOf` en 4 referencias, y eso es
**borrado en cascada**: borrar un mantenimiento se lleva sus fotografías, su firma y su
checklist. Eso solo es seguro porque el mantenimiento nunca se borra. **La cascada existe desde
el momento en que se marca la primera; la protección tiene que estar puesta ya.**

## Paso 2 — Las 39 referencias

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

## Paso 3 — Los tipos que no se infieren

### Las 4 marcas de tiempo del servidor

Tipo **`ChangeTimestamp`**. AppSheet no lo infiere nunca: llegan como texto.

- `MAN_Mantenimientos.FechaHoraRegistro`
- `NOV_Novedades.FechaHora`
- `FOT_Fotografias.FechaHora`
- `FIR_Firmas.FechaHora`

**Por qué importa.** `ChangeTimestamp` la escribe el servidor. Un `Initial value = NOW()` lo pone
el teléfono, y el usuario puede cambiar la hora del teléfono. Sin esto, **la hora de cada
fotografía y de cada firma no prueba nada**, que es justo lo que el sistema existe para sostener.

### Los 12 desplegables

Tipo `Enum`, y **los valores exactos**. No los deduzcas ni los traduzcas: son estos.

| Tabla | Columna | Valores |
|---|---|---|
| `TIP_TiposActivo` | `Categoria` | `ITS` · `Electrico` · `Comunicaciones` · `TI` |
| `EOT_EstadosOrden` | `QuienCambia` | `Sistema` · `Tecnico` · `Supervisor` |
| `ACT_Activos` | `Criticidad` | `Alta` · `Media` · `Baja` |
| `ACT_Activos` | `MotivoBaja` | `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` |
| `OT_OrdenesTrabajo` | `Tipo` | `Preventivo` · `Correctivo` |
| `MAN_Mantenimientos` | `OrigenApertura` | `QR` · `Lista` |
| `NOV_Novedades` | `Tipo` | `Activo no inventariado` · `Falla detectada` |
| `NOV_Novedades` | `Estado` | `Reportada` · `Aceptada` · `Descartada` |
| `FAL_ModosFalla` | `Criticidad` | `Alta` · `Media` · `Baja` |
| `FOT_Fotografias` | `Tipo` | `Antes` · `Despues` · `Novedad` |
| `FIR_Firmas` | `TipoFirma` | `Tecnico` |
| `CHD_ChecklistDetalle` | `RespuestaLista` | **sin declarar en el modelo. Pregunta antes de inventarlos** |

### Las 6 coordenadas

Deberían haber entrado ya como `LatLong`, porque su nombre lleva la palabra que AppSheet
reconoce. **Compruébalas igual**, y si alguna salió `Text`, cámbiala: `DISTANCE()` no funciona
sobre texto.

- `SED_Sedes.Ubicacion_LatLong`
- `ACT_Activos.Ubicacion_LatLong`
- `MAN_Mantenimientos.UbicacionEscaneo_LatLong`
- `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`
- `NOV_Novedades.Ubicacion_LatLong`
- `FOT_Fotografias.Ubicacion_LatLong`

## Paso 4 — Las 21 reglas

Están **enteras y sin cortar** en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md),
con su tabla, su columna y su tipo —`Valid_If`, `Initial value`, `App formula`, bot—. Cópialas de
ahí. **No las escribas de memoria ni las adaptes.**

La que más se olvida es **RG-19**, el umbral de GPS con su `OR(ISBLANK(...))`: sin ese `ISBLANK`,
si alguien borra la fila del parámetro **todos los cierres salen limpios y nadie se entera**.

## Paso 5 — Comprobar, y aquí está lo que solo se puede ver ahora

**Las 6 tablas que llegaron vacías eligieron su clave a ciegas**, porque AppSheet la infiere de
los datos y no había. Y son justo las que generan clave con `UNIQUEID()`, es decir alfanumérica:
**si alguna quedó `Number`, cada fila que cree un técnico se perderá sin aviso.**

- `CHD_ChecklistDetalle`
- `CHK_Checklists`
- `FIR_Firmas`
- `FOT_Fotografias`
- `MAN_Mantenimientos`
- `NOV_Novedades`

Abre cada una y confirma que su clave es **`Text`**.

Después, las pruebas de [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).

## Qué reportar al terminar

1. **Cuántas referencias pusiste**, y si alguna no te dejó.
2. **Las 4 de `IsPartOf`**, y confirmación de que `MAN_Mantenimientos.OTID` quedó DESMARCADA.
3. **`Deletes` retirado** en las dos tablas.
4. **Las claves de las 6 tablas vacías**: qué tipo tenía cada una.
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
