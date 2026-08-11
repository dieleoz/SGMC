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

## Paso 3 — Los tipos. **Las 211, no una lista de excepciones**

**Este paso se llamaba «los tipos que no se infieren» y enumeraba 61 columnas.** Era una lista
blanca de excepciones sobre un default que se presumía bueno: las otras 150 se daban por
correctas por omisión. La plataforma garantiza lo contrario, y el precio fue `RG-03` —bien
escrita, bien colocada— sobre una columna que AppSheet tipó `Text` cuando el modelo dice
`Yes/No`. Comparar texto contra el booleano `TRUE` es **siempre falso y no da error**: el motivo
de excepción no se pide nunca. La regla existe y es decorativa.

Y el «qué reportar» cerraba el bucle en falso —«cualquier tipo distinto del que dice este
documento»—: **nadie puede reportar una diferencia contra un valor que nunca se le dio.**

### Las 107 que NADIE pone si no las pones tú

Ningún contenido de la hoja las produce, o su propio nombre empuja a AppSheet al tipo
equivocado. **Están ordenadas por las reglas que dependen de cada una**, que es lo que ordena el
trabajo: una columna mal tipada sin regla encima molesta al usuario; con una regla encima
**rompe la regla en silencio**.

| Tabla | Columna | `TYPE` | Reglas | Por qué no se consigue sola |
|---|---|---|---|---|
| `ACT_Activos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-06`, `RG-16`, `RG-17` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-06`, `RG-16`, `RG-17` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `ACT_Activos` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04`, `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04`, `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CAL_Calzadas` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `EOT_EstadosOrden` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `EST_Activo` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FAL_ModosFalla` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRE_Frecuencias` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Formularios` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Preguntas` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Secciones` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `LST_ValoresLista` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `MAN_Mantenimientos` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `MAN_Mantenimientos` | `CierreConExcepcion` | **`Yes/No`** | `RG-03`, `RG-19` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `MAN_Mantenimientos` | `Precision_GPS` | **`Number`** | `RG-02`, `RG-19` | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `MOT_MotivosPendiente` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `OT_OrdenesTrabajo` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `PAR_Parametros` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `PLA_PlanMantenimiento` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `ROL_Roles` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `SED_Sedes` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `SED_Sedes` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04`, `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `SEN_Sentidos` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `TIP_TiposActivo` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `TPR_TiposRespuesta` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `UNF_UnidadesFuncionales` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `USR_Usuarios` | `Activo` | **`Yes/No`** | `RG-04`, `RG-16` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `ACT_Activos` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | `RG-11` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `SedeID` | **`Ref`** → `SED_Sedes` | `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHK_Checklists` | `FormularioID` | **`Ref`** → `FRM_Formularios` | `RG-09` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `EsFinal` | **`Yes/No`** | `RG-08` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `EST_Activo` | `GeneraAlerta` | **`Yes/No`** | `RG-06` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FAL_ModosFalla` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `FormularioID` | **`Ref`** → `FRM_Formularios` | `RG-09` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoExcepcion` | **`LongText`** | `RG-03` | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OTID` | **`Ref`** → `OT_OrdenesTrabajo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `RequiereSegundaVisita` | **`Yes/No`** | `RG-10` | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `MAN_Mantenimientos` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `NOV_Novedades` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `NOV_Novedades` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | **`Ref`** → `EOT_EstadosOrden` | `RG-08` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `SupervisorID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | `RG-11` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `TIP_TiposActivo` | `FormularioID` | **`Ref`** → `FRM_Formularios` | `RG-09` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `CalzadaID` | **`Ref`** → `CAL_Calzadas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Criticidad` | **`Enum`** · valores: `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `MotivoBaja` | **`Enum`** · valores: `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `ACT_Activos` | `SentidoID` | **`Ref`** → `SEN_Sentidos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `ChecklistID` | **`Ref`** → `CHK_Checklists` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `Contestada` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `CHD_ChecklistDetalle` | `Observacion` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHD_ChecklistDetalle` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `RespuestaBoolean` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `CHD_ChecklistDetalle` | `RespuestaLista` | **`Enum`** | — | el contenido no declara el conjunto de valores permitidos |
| `CHD_ChecklistDetalle` | `RespuestaTexto` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHK_Checklists` | `Finalizado` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `CHK_Checklists` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `QuienCambia` | **`Enum`** · valores: `Sistema` · `Tecnico` · `Supervisor` | — | el contenido no declara el conjunto de valores permitidos |
| `FAL_ModosFalla` | `Criticidad` | **`Enum`** · valores: `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `FIR_Firmas` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FIR_Firmas` | `Imagen` | **`Signature`** | — | igual que Image |
| `FIR_Firmas` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FIR_Firmas` | `TipoFirma` | **`Enum`** · valores: `Tecnico` | — | el contenido no declara el conjunto de valores permitidos |
| `FOT_Fotografias` | `Archivo` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `FOT_Fotografias` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FOT_Fotografias` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FOT_Fotografias` | `PrecisionGPS` | **`Number`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `FOT_Fotografias` | `Tipo` | **`Enum`** · valores: `Antes` · `Despues` · `Novedad` | — | el contenido no declara el conjunto de valores permitidos |
| `FRM_Preguntas` | `Obligatoria` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Preguntas` | `RequiereFirma` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Preguntas` | `RequiereFoto` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `FRM_Preguntas` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `FRM_Preguntas` | `SeccionID` | **`Ref`** → `FRM_Secciones` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `TipoRespuestaID` | **`Ref`** → `TPR_TiposRespuesta` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `LST_ValoresLista` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `AprobadoSupervisor` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `MAN_Mantenimientos` | `ModoFallaID` | **`Ref`** → `FAL_ModosFalla` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoPendienteID` | **`Ref`** → `MOT_MotivosPendiente` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `ObservacionRechazo` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OrigenApertura` | **`Enum`** · valores: `QR` · `Lista` | — | el contenido no declara el conjunto de valores permitidos |
| `MOT_MotivosPendiente` | `GeneraSeguimiento` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
| `NOV_Novedades` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `NOV_Novedades` | `Estado` | **`Enum`** · valores: `Reportada` · `Aceptada` · `Descartada` | — | el contenido no declara el conjunto de valores permitidos |
| `NOV_Novedades` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `NOV_Novedades` | `Fotografia` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `NOV_Novedades` | `Tipo` | **`Enum`** · valores: `Activo no inventariado` · `Falla detectada` | — | el contenido no declara el conjunto de valores permitidos |
| `OT_OrdenesTrabajo` | `CerradaPor` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `OTOrigenID` | **`Ref`** → `OT_OrdenesTrabajo` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `OT_OrdenesTrabajo` | `Tipo` | **`Enum`** · valores: `Preventivo` · `Correctivo` | — | el contenido no declara el conjunto de valores permitidos |
| `PAR_Parametros` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `PLA_PlanMantenimiento` | `ResponsableID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `TIP_TiposActivo` | `Categoria` | **`Enum`** · valores: `ITS` · `Electrico` · `Comunicaciones` · `TI` | — | el contenido no declara el conjunto de valores permitidos |
| `TIP_TiposActivo` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `TIP_TiposActivo` | `TieneQR` | **`Yes/No`** | — | supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no esta en la documentacion ni lo hemos observado. Si falla, la columna sale Text y toda comparacion contra TRUE es siempre falsa, sin dar error |
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

### Las 87 que dependen del contenido

AppSheet debería acertar leyendo los valores — **cuando los hay**. Las de una tabla vacía no
tienen contenido que leer, así que estas también hay que mirarlas ahí. La lista completa, tabla
por tabla, está en [`TIPOS_ESPERADOS.md`](TIPOS_ESPERADOS.md).

> **El caso que desarma la confianza en el contenido:** `SED_Sedes.TramoINVIAS` tenía un valor
> real y representativo, `5607`, y AppSheet la tipó **`Number`**. El modelo dice `Text`, y el día
> que operación escriba `55CN03` no cabrá. Tener el dato correcto no basta.

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
