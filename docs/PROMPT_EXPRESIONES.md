# Encargo de las expresiones — Fase C

**Autocontenido. Cópialo íntegro desde la línea siguiente.**

**Generado** por `scripts/generar_prompt_expresiones.py`. No editar a mano: las expresiones y
las cadenas de referencias salen de `scripts/modelo_objetivo.py`.

---

Vas a poner **21 reglas** en la aplicación **`_SISGA_-323965761`** de Google AppSheet.
Las 39 referencias ya están cableadas. Esto es lo que va encima.

```
https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e
```

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
| 3 | `RG-04` | `ACT_Activos` | `(tabla)` | `Security Filter` | `USR_Usuarios` |
| 4 | `RG-05` | `OT_OrdenesTrabajo` | `(tabla)` | `Security Filter` | `USR_Usuarios` · `USR_Usuarios` |
| 5 | `RG-13` | `MAN_Mantenimientos` | `(tabla)` | `Verificacion de evidencia` | — |
| 6 | `RG-14` | `OT_OrdenesTrabajo` | `(tabla)` | `Are updates allowed` | — |
| 7 | `RG-15` | `MAN_Mantenimientos` | `(tabla)` | `Are updates allowed` | — |
| 8 | `RG-17` | `ACT_Activos` | `FechaBaja` | `Required_If` | `EST_Activo` |
| 9 | `RG-18` | `ACT_Activos` | `(tabla)` | `Doctrina de reportes` | — |
| 10 | `RG-20` | `MAN_Mantenimientos` | `(varias)` | `Editable_If` | — |
| 11 | `RG-34` | `ACT_Activos` | `UnidadFuncionalID` | `Valid_If` | `SED_Sedes` |
| 12 | `RG-02` | `MAN_Mantenimientos` | `Precision_GPS` | `Initial value` | — |
| 13 | `RG-06` | `MAN_Mantenimientos` | `(tabla)` | `Bot` | `EST_Activo` |
| 14 | `RG-07` | `OT_OrdenesTrabajo` | `(tabla)` | `Bot` | — |
| 15 | `RG-08` | `OT_OrdenesTrabajo` | `EstadoOrdenID` | `Bot programado` | `EOT_EstadosOrden` |
| 16 | `RG-09` | `CHK_Checklists` | `VersionFormulario` | `Initial value` | `FRM_Formularios` |
| 17 | `RG-10` | `MAN_Mantenimientos` | `(tabla)` | `Bot` | — |
| 18 | `RG-11` | `PLA_PlanMantenimiento` | `ProximaFecha` | `App formula` | `FRE_Frecuencias` |
| 19 | `RG-12` | `PLA_PlanMantenimiento` | `(tabla)` | `Bot programado` | — |
| 20 | `RG-16` | `ACT_Activos` | `Activo` | `App formula` | `EST_Activo` |
| 21 | `RG-19` | `MAN_Mantenimientos` | `CierreConExcepcion` | `App formula` | — |

> Las de `App formula`, `Initial value` y las de tipo bot **escriben**. Ponerlas antes de haber
> comprobado las demás significa soltarlas sobre el inventario entero sin saber qué escriben.

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
