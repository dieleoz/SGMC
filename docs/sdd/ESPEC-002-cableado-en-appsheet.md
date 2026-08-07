# ESPEC-002 — Cableado de referencias en AppSheet

Fase B. Es la que convierte el modelo en un sistema: hasta aquí hay una hoja de cálculo ordenada, y
al terminar hay referencias reales, geofencing y navegación entre tablas.

| | |
|---|---|
| Dónde se aplica | Editor de AppSheet, aplicación `SGMC-886843353` |
| Quién | Agente de navegador, o una persona. No hay API en el plan actual |
| Precede | `ESPEC-001`, `ESPEC-001B` y `ESPEC-001C`, cerradas (`ACTA-002`) |
| Pruebas | `PRUEBA-002` |
| Versión 2 | Reescrita el 2026-08-07 tras el veredicto BLOQUEA del arquitecto, 16 hallazgos |

---

## 1. Verificación previa, obligatoria

La Fase A está cerrada. Constancia en `ACTA-002`, verificada sobre **`BD/Modelo de Datos (7).xlsx`**,
descarga del Sheets de producción del 2026-08-07:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (7).xlsx"
-> CONFORMES (43), AVISOS (6), FASE A CERRADA
```

**Vuelve a correrlo antes de empezar, sobre la descarga más reciente.** La hoja la editan dos
personas más, y los archivos anteriores ya no pasan: `Modelo de Datos (6).xlsx` da hoy
`FASE A INCOMPLETA` porque el verificador se endureció después.

### Lo que ya está resuelto y NO hay que tocar

Estos tres fueron bloqueantes y **están corregidos**. Si el ejecutor intenta «arreglarlos» otra vez,
rompe datos correctos:

| Antes | Ahora |
|---|---|
| `CHK.MantenimientoID` guardaba `OT-0001`, una orden | Resuelve contra `MAN_Mantenimientos` |
| `LST_ValoresLista.PreguntaID` guardaba el texto `Estado encontrado` | Vale `SOS001` en las 4 filas |
| Faltaban `FechaBaja` y `MotivoBaja` | Presentes en `ACT_Activos` |

### Lo que sigue abierto y condiciona los pasos

| Hecho verificado | Consecuencia |
|---|---|
| `TIP_TiposActivo.RadioGeofencingKm` está **vacío en los 18 tipos** | RG-01 no puede usarlo. Ver bloque 4 |
| `OT_OrdenesTrabajo.Activo` está **vacía en las 6 filas** | Tiparla `Yes/No` sin poblarla deja las 6 órdenes como inactivas. Ver 5.1 |
| `MAN_Mantenimientos` tiene **2 filas**, no 0 | Son de prueba y desechables, pero la premisa «no arrastra nada» ya no es literal |
| `USR_Usuarios.UsuarioID` mezcla 10 numéricos y uno de texto (`3aa202ee`) | Si la clave se tipa `Number`, esa fila queda con clave inválida |
| `OT.ActivoID` guarda texto (`'2'`) y `ACT.ActivoID` números (`2.0`) | La referencia solo resuelve si ambas se tipan igual |

---

## 2. La regla que gobierna toda la fase

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

1. **Primero la clave del destino, después quien la apunta.**
2. **Una conversión `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave.** Las
   demás quedan huérfanas y en silencio.
3. **Se valida en el Asistente de Expresiones, no ejercitando la aplicación.**

---

## 3. Antes de tocar nada

1. **Respaldo del Sheets:** `SGMC_backup_2026-08-07_antes_cableado_FaseA`. Si han pasado días, otro.
2. **Punto de restauración: versión `1.000238`.** No hay que guardar nada; AppSheet versiona solo.
3. **Avisar a las dos cuentas con permiso de edición.** La reversión solo es limpia si nadie escribe.
4. **Inventariar los nombres viejos.** Buscar en el editor cada vista, fórmula o acción que cite:
   `Numero_OT`, `Activo` como vínculo al activo, `Tecnico`, `SupervidorID`, `Estado`, `MttoID`,
   `Tecnico_Asignado`, **`EstadoID`** y **`SedeID`**. Las dos últimas se ven ya en las acciones
   `View Ref (EstadoID)` y `View Ref (SedeID)` de `ACT_Activos`. Se reparan en el bloque 5.
5. **Buscar filtros por la bandera `Activo` del activo.** Cualquier vista, slice o reporte que use
   `[ActivoID].[Activo]` o equivalente sobre datos históricos. Es RG-18, y con RG-16 corregida deja
   de ser hipotético: el activo 34 pasará a `Activo = FALSE`.

---

## 4. BLOQUE 1 — Estructura y claves. Van juntas, no separadas

**No se puede hacer *Regenerate* y parar.** Al dar de alta una tabla o regenerarla, **AppSheet fija
una clave por su cuenta e infiere referencias contra ella**. Eso ya ocurrió: las acciones
`View Ref (CalzadaID)`, `View Ref (EstadoID)` y `View Ref (SedeID)` sobre `ACT_Activos` existen
porque AppSheet las creó solo.

Terminar el bloque tras el *Regenerate* deja exactamente el estado que hay que evitar: tablas con la
clave adivinada y referencias automáticas colgando de ella.

**Cómo elige AppSheet, según su documentación** (verificado el 2026-08-07, ver
`docs/PLATAFORMA_APPSHEET_VERIFICADO.md`):

> Examina las columnas **de izquierda a derecha** buscando una con valores únicos y la convierte en
> clave. **Si ninguna sirve, examina pares de columnas y las combina en una clave compuesta.**

**La clave compuesta es el peligro que hay que vigilar**, y no estaba documentado hasta hoy: contra
una clave de dos columnas **ninguna referencia del bloque 3 resolverá**. Si al leer una tabla en 4.2
la clave aparece como combinación, hay que corregirla antes de seguir.

Y las referencias las infiere **por coincidencia de nombre** —«si Orders tiene una columna
`Customer Name` y la clave de Customers es `Name`, se asume `Ref`»—, que es exactamente por qué
existen `View Ref (SedeID)` y `View Ref (EstadoID)` con los nombres viejos.

### 4.1 Regenerar y dar de alta

*Data > Tables > [tabla] > Regenerate Structure* sobre: `ACT_Activos`, `OT_OrdenesTrabajo`,
`MAN_Mantenimientos`, `USR_Usuarios`, `EST_Activo`, `TIP_TiposActivo`, `CHK_Checklists`,
`CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `FRM_Preguntas`, `FRM_Formularios`,
`FRM_Secciones`, `LST_ValoresLista`, `ROL_Roles`, `SED_Sedes`, `CAL_Calzadas`, `SEN_Sentidos`,
`FRE_Frecuencias`, `TPR_TiposRespuesta`.

**Añadir como tablas nuevas** las siete que la Fase A creó: `UNF_UnidadesFuncionales`,
`ASG_AsignacionZona`, `EOT_EstadosOrden`, `MOT_MotivosPendiente`, `FAL_ModosFalla`, `NOV_Novedades`,
`PLA_PlanMantenimiento`.

### 4.2 Leer qué clave fijó AppSheet, y corregirla

Tabla por tabla en *Data > Columns*: **anotar qué columna quedó marcada como `KEY`** y compararla
con esta tabla. El tipo importa tanto como el nombre.

| Tabla | Clave | Tipo | Nota |
|---|---|---|---|
| `ACT_Activos` | `ActivoID` | `Text` | La hoja guarda números. Forzar `Text`, o `OT.ActivoID` —que guarda texto— no resolverá |
| `OT_OrdenesTrabajo` | `OTID` | `Text` | `OT-0001` |
| `MAN_Mantenimientos` | `MantenimientoID` | `Text` | |
| `USR_Usuarios` | `UsuarioID` | `Text` | **Obligatorio `Text`.** Hay un valor `3aa202ee` entre diez numéricos |
| `EST_Activo` | `EstadoActivoID` | `Text` | |
| `ROL_Roles` | `RolID` | `Text` | |
| `SED_Sedes` | `SedeID` | `Text` | |
| `TIP_TiposActivo` | `TipoActivoID` | `Text` | |
| `CAL_Calzadas` | `CalzadaID` | `Text` | |
| `SEN_Sentidos` | `SentidoID` | `Text` | Valores `SA`, `AS` |
| `FRE_Frecuencias` | `FrecuenciaID` | `Text` | |
| `UNF_UnidadesFuncionales` | `UnidadFuncionalID` | `Text` | Valores 7 a 10 |
| `ASG_AsignacionZona` | `AsignacionID` | `Text` | Tabla nueva. RG-04 la recorre |
| `EOT_EstadosOrden` | `EstadoOrdenID` | `Text` | Valores `Asignada`, `Cerrada`… |
| `MOT_MotivosPendiente` | `MotivoPendienteID` | `Text` | |
| `FAL_ModosFalla` | `ModoFallaID` | `Text` | Tabla nueva y destino de `MAN.ModoFallaID` |
| `CHK_Checklists` | `ChecklistID` | `Text` | |
| `CHD_ChecklistDetalle` | `DetalleID` | `Text` | |
| `FRM_Formularios` | `FormularioID` | `Text` | |
| `FRM_Preguntas` | `PreguntaID` | `Text` | |
| `FRM_Secciones` | `SeccionID` | `Text` | |
| `TPR_TiposRespuesta` | `TipoRespuestaID` | `Text` | |
| `LST_ValoresLista` | `ValorListaID` | `Text` | |
| `NOV_Novedades` | `NovedadID` | `Text` | |
| `PLA_PlanMantenimiento` | `PlanID` | `Text` | |
| `FOT_Fotografias` | `FotoID` | `Text` | Se le asigna `UNIQUEID()` en 4.3: sin clave declarada quedaría a lo que adivine AppSheet |
| `FIR_Firmas` | `FirmaID` | `Text` | Igual |

**Todas `Text`, y no por comodidad:** es la convención del modelo y evita que AppSheet infiera
`Number` sobre una columna con un valor alfanumérico y deje esa fila con clave inválida. Es la regla
R-4 aplicada a las claves.

Una sola casilla `KEY` por tabla. Si hay dos, quitar la sobrante.

### 4.3 Generación de clave para las filas nuevas

Sin esto, P-04, P-08 y P-12 no se pueden ejecutar: la aplicación no sabría qué identificador poner
al crear un registro.

| Tabla | Columna | `Initial value` |
|---|---|---|
| `MAN_Mantenimientos` | `MantenimientoID` | `UNIQUEID()` |
| `FOT_Fotografias` | `FotoID` | `UNIQUEID()` |
| `FIR_Firmas` | `FirmaID` | `UNIQUEID()` |
| `CHK_Checklists` | `ChecklistID` | `UNIQUEID()` |
| `CHD_ChecklistDetalle` | `DetalleID` | `UNIQUEID()` |
| `NOV_Novedades` | `NovedadID` | `UNIQUEID()` |

**Supuesto declarado, no verificado:** que `UNIQUEID()` no colisiona entre dispositivos que trabajan
**sin conexión**. No se ha encontrado la página oficial que lo garantice. Importa porque es el
argumento por el que `OT_OrdenesTrabajo` pierde `Adds`. Ver la tabla final de
`docs/BASE_CONOCIMIENTO_APPSHEET.md`.

**Verificación del bloque 1:** `MAN_Mantenimientos` muestra **36 columnas**. Cada tabla tiene una
sola clave, la de la tabla anterior, con su tipo. Un número **mayor** que 36 significa definiciones
de columna fantasma que sobrevivieron al *Regenerate* —`MttoID`, `Tecnico_Asignado`— y hay que
retirarlas.

---

## 5. BLOQUE 2 — Tipos que no son referencia

Independientes entre sí, no pueden romper nada.

| Tabla | Columna | Tipo |
|---|---|---|
| `ACT_Activos` | `Ubicacion` | `LatLong` |
| `ACT_Activos` | `FechaBaja` | `Date` |
| `ACT_Activos` | `Activo` | `Yes/No` |
| `MAN_Mantenimientos` | `Coordenadas_Cierre`, `UbicacionEscaneo` | `LatLong` |
| `MAN_Mantenimientos` | `Precision_GPS` | `Number` |
| `MAN_Mantenimientos` | `FechaHoraInicio`, `FechaHoraFin`, `FechaHoraEscaneo`, `FechaAprobacion` | `DateTime` |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | `ChangeTimestamp` |
| `MAN_Mantenimientos` | `OrigenApertura` | `Enum`: `QR`, `Lista` |
| `MAN_Mantenimientos` | `CierreConExcepcion`, `RequiereSegundaVisita`, `AprobadoSupervisor`, `Activo` | `Yes/No`. `CierreConExcepcion` la calcula RG-19: no la edita nadie |
| `OT_OrdenesTrabajo` | `Activo` | `Yes/No` |
| `OT_OrdenesTrabajo` | `Tipo` | `Enum`: `Preventivo`, `Correctivo`. **Vacía en las 6 filas: deuda declarada.** No la marques obligatoria o las 6 órdenes quedan incompletas |
| `FOT_Fotografias` | `Archivo` | `Image`, calidad baja 600 px |
| `FOT_Fotografias` | `Ubicacion` | `LatLong` |
| `FIR_Firmas` | `Imagen` | `Signature` |
| `TIP_TiposActivo` | `RadioGeofencingKm` | `Decimal` |

### 5.0 `Editable_If = FALSE` en las cuatro columnas de captura. **Antes que ninguna regla**

| Tabla | Columna | `Editable_If` |
|---|---|---|
| `MAN_Mantenimientos` | `Coordenadas_Cierre` | `FALSE` |
| `MAN_Mantenimientos` | `Precision_GPS` | `FALSE` |
| `MAN_Mantenimientos` | `UbicacionEscaneo` | `FALSE` |
| `MAN_Mantenimientos` | `FechaHoraEscaneo` | `FALSE` |

**Sin esto el geofencing es decorativo, y es la razón de ser del sistema.** `HERE()` y
`USERLOCATIONACCURACY()` son `Initial value`, **no `App formula`**, y un valor inicial **sí lo puede
editar el usuario**. `Coordenadas_Cierre` es un `LatLong`: en un formulario AppSheet lo dibuja como
un **pin arrastrable sobre un mapa**, y la ubicación del activo está visible en la propia
aplicación. El técnico arrastra el pin encima del activo y **RG-01 valida sin protestar**.

La regla se cumpliría y la presencia no quedaría probada. Es RG-20.

Si `Coordenadas_Cierre` queda como `Text`, `DISTANCE()` no opera y el bloque 4 falla sin explicar
por qué.

### 5.1 Precondiciones de datos — SE HACEN EN LA HOJA, NO AQUÍ

`OT.Activo` está **vacía en las 6 filas**. Tipada como `Yes/No`, un blanco se lee como falso: las
seis órdenes quedarían inactivas.

Tres columnas tienen que estar pobladas **antes** de tipar nada, y las tres son ediciones del
Google Sheets, no configuración de AppSheet. Van en la misma pasada que la pestaña
`PAR_Parametros`, con el prompt de `docs/prompts/PROMPT_AGENTE_HOJA_CIERRE_FASE_A.md`.

| Qué | Por qué antes |
|---|---|
| `OT_OrdenesTrabajo.Activo = TRUE` en las 6 filas | Tipada `Yes/No`, un blanco se lee como falso: las 6 órdenes quedarían inactivas. Y RG-14 retira el borrado dejando `Activo = FALSE` como única vía de anulación: se quitaría el borrado sin que exista el sustituto |
| `EST_Activo.Activo = TRUE` en las 4 filas | Es el catálogo del que dependen RG-16 y RG-17 |
| `ACT_Activos.Activo = FALSE` en la fila 34 | Está `Retirado` y la columna dice `TRUE`. RG-16 la calculará `FALSE`; la hoja debe decir lo mismo antes |

**`verificar_faseA.py` no dará `FASE A CERRADA` hasta que estén las cuatro.** Ese es el gate de
entrada a esta fase.

**`ACT_Activos.Activo` se contradirá consigo misma si no se toca.** La hoja guarda el texto `TRUE`
en las 34 filas, incluida la 34, que está `Retirado` y tiene `FechaBaja`. Con RG-16 como
`App formula`, la aplicación calculará `FALSE` y el Sheets seguirá diciendo `TRUE` hasta que alguien
escriba esa fila. **Poner `FALSE` en `ACT_Activos.Activo` de la fila 34**, en la misma pasada. Es
una celda.

**`EST_Activo.Activo` está en la misma situación:** vacía en sus 4 filas. Hoy no la usa ninguna
regla, pero es el catálogo del que dependen RG-16 y RG-17, y un `Valid_If` de catálogo sobre
`[Activo] = TRUE` dejaría el desplegable de estados vacío. **Poner `TRUE` en las 4 filas**, en la
misma pasada.

### 5.2 Confirmar el formato de la coordenada

En todo el sistema **no hay ni una coordenada capturada por la aplicación**. El formato de las filas
de prueba es un supuesto, tomado de que `DISTANCE()` compara contra `ACT_Activos.Ubicacion`.

1. Con `Coordenadas_Cierre` tipada `LatLong`, crear un registro desde la aplicación dejando que
   `HERE()` capture.
2. Leer el Sheets de vuelta y comparar el literal con `4.728512, -74.114531`.

**Plan B, y hay que preverlo:** un agente de navegador **no tiene GPS**. `HERE()` sin permiso de
ubicación devuelve blanco o una posición por IP. Si la captura no es viable:

- O la hace una persona desde un móvil.
- O se declara el formato como **supuesto verificado** —`4.728512, -74.114531`, coma y espacio, el
  que ya usan las 34 filas de `ACT_Activos`—, se anota en el acta y se sigue.

Lo que **no** vale es dar el formato por confirmado sin ninguna de las dos.

---

## 6. BLOQUE 3 — Las referencias, de abajo hacia arriba

Cada bloque referencia tablas cuyas claves se fijaron en el bloque 1.

### 6.1 Contra catálogos

| Tabla | Columna | `Ref` a |
|---|---|---|
| `USR_Usuarios` | `RolID` | `ROL_Roles` |
| `USR_Usuarios` | `SedeID` | `SED_Sedes` |
| `ACT_Activos` | `TipoActivoID` | `TIP_TiposActivo` |
| `ACT_Activos` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` |
| `ACT_Activos` | `EstadoActivoID` | `EST_Activo` |
| `ACT_Activos` | `CalzadaID` | `CAL_Calzadas` |
| `ACT_Activos` | `SentidoID` | `SEN_Sentidos` |
| `ACT_Activos` | `FrecuenciaID` | `FRE_Frecuencias` |
| `TIP_TiposActivo` | `FormularioID` | `FRM_Formularios` |
| `ASG_AsignacionZona` | `UsuarioID` | `USR_Usuarios` |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | `UNF_UnidadesFuncionales` |

Varias pueden estar **ya** como `Ref` con el nombre viejo. Comprobar antes de crear.

### 6.2 La orden de trabajo

| Columna | `Ref` a | Nota |
|---|---|---|
| `ActivoID` | `ACT_Activos` | Guarda texto `'2'`, `'26'`… Solo resuelve si `ACT.ActivoID` es `Text` |
| `TecnicoID` | `USR_Usuarios` | |
| `SupervisorID` | `USR_Usuarios` | Mezcla `8.0` y `'8'`. Verificar que las 6 resuelvan |
| `EstadoOrdenID` | `EOT_EstadosOrden` | Las 6 resuelven, verificado |
| `OTOrigenID` | `OT_OrdenesTrabajo` | Autorreferencia. Vacía hoy |

### 6.3 El mantenimiento — el retipado que desbloquea todo

| Columna | `Ref` a | Nota |
|---|---|---|
| `OTID` | `OT_OrdenesTrabajo` | **Era `Text`: el defecto raíz del sistema.** Las 2 filas de prueba resuelven contra `OT-0001` y `OT-0003` |
| `TecnicoID` | `USR_Usuarios` | |
| `EstadoActivoID` | `EST_Activo` | |
| `MotivoPendienteID` | `MOT_MotivosPendiente` | |
| `ModoFallaID` | `FAL_ModosFalla` | Vacía hoy |

**`MAN_Mantenimientos.OTID` va SIN `Is a part of`.** Decidido el 2026-08-07: marcarlo haría que
borrar una orden borrase su ejecución, y con ella las fotografías, las firmas y el checklist. La
ejecución es el registro histórico y sobrevive a su orden.

### 6.4 Evidencias, checklist y formularios

| Tabla | Columna | `Ref` a | `IsPartOf` |
|---|---|---|---|
| `FOT_Fotografias` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `FIR_Firmas` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `CHK_Checklists` | `MantenimientoID` | `MAN_Mantenimientos` | Sí |
| `CHK_Checklists` | `FormularioID` | `FRM_Formularios` | No |
| `CHD_ChecklistDetalle` | `ChecklistID` | `CHK_Checklists` | Sí |
| `CHD_ChecklistDetalle` | `PreguntaID` | `FRM_Preguntas` | No |
| `FRM_Preguntas` | `FormularioID` | `FRM_Formularios` | No |
| `FRM_Preguntas` | `SeccionID` | `FRM_Secciones` | No |
| `FRM_Preguntas` | `TipoRespuestaID` | `TPR_TiposRespuesta` | No |
| `LST_ValoresLista` | `PreguntaID` | `FRM_Preguntas` | No |

**Aplazadas a `ESPEC-003`:** las 5 referencias de `NOV_Novedades` y `PLA_PlanMantenimiento`
(`NOV.UsuarioID`, `NOV.ActivoID`, `PLA.ActivoID`, `PLA.FrecuenciaID`, `PLA.ResponsableID`).
Verificado que las 5 **resuelven** contra sus destinos, así que no son incorrectas — pero son 5
columnas más en un editor caro y frágil, y no desbloquean ni el geofencing ni la navegación ni el
filtro por zona. La instrucción vigente es que funcione primero. Lo mismo con
`FAL_ModosFalla.TipoActivoID`, que tampoco entra en 6.1.

`LST_ValoresLista.PreguntaID` vale `SOS001` en sus 4 filas y **resuelve**. Va como `Ref`, sin
excepciones ni deuda pendiente.

La cascada de `IsPartOf` es inofensiva **porque el mantenimiento nunca se borra** (RG-15).

> **Y no hay transacciones.** Un mantenimiento, sus fotografías, su firma y su checklist son
> escrituras de filas **independientes**. Una sincronización parcial deja la cadena de evidencia
> incompleta y **nada la revierte**. No es corregible en esta fase: se declara como límite conocido.

**Verificación del bloque 3, y es la que importa de toda la fase.** En el Asistente de Expresiones,
sobre `MAN_Mantenimientos`:

```
[OTID].[ActivoID].[Ubicacion]
```

Debe resolver sin error. Es la prueba de que la cadena existe.

---

## 7. BLOQUE 4 — Las reglas

**RG-01, geofencing**, sobre `MAN_Mantenimientos.Coordenadas_Cierre`. `RadioGeofencingKm` está
**vacío en los 18 tipos**, así que la expresión que se pega es esta, con el literal:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= 1.0
Invalid text:   Ubicación fuera de rango: debe estar junto al activo para cerrar.
```

Si se pega la variante con `[TipoActivoID].[RadioGeofencingKm]` sobre la columna vacía, el `<=`
compara contra blanco y **rechaza también el cierre legítimo**: P-08 y P-09 fallarían las dos y la
tanda dejaría de discriminar.

La versión con radio por tipo entra cuando se pueblen los 18. Queda anotado como deuda.

**RG-02:** `Precision_GPS`, `Initial value` = `USERLOCATIONACCURACY()`.

**RG-03:** `MotivoExcepcion`, `Required_If` = `[CierreConExcepcion] = TRUE`.

**RG-19:** `MAN_Mantenimientos.CierreConExcepcion`, `App formula`:

```
[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")
```

> **El umbral es un parámetro, no un número en la expresión.** Vive en `PAR_Parametros` y el
> administrador lo ajusta en una celda tras las pruebas de campo, sin abrir el editor ni arriesgarse
> a romper la regla. Provisional: **40 m**.
>
> El número sale de un dato, no de una impresión: un móvil con GPS es preciso a unos **4,9 m a
> cielo abierto** ([GPS.gov](https://www.gps.gov/gps-accuracy)), y empeora en montaña y cerca de
> estructuras — que es el corredor. 40 m deja unas ocho veces de margen. D-04 decía 50; se baja al
> comprobar que 45 m ya es nueve veces la norma.
>
> Sin esta regla la columna existe y **nadie la puebla**: un cierre con 45 m de error sería
> indistinguible de uno con 8 m. Al ser `App formula` el técnico no puede desmarcarla, **y por
> RG-20 tampoco puede editar el `Precision_GPS` que la decide**.

**RG-04, Security Filter** sobre `ACT_Activos`:

```
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))
```

> **El Security Filter no es confidencialidad.** Es control de acceso **en la app** y, sobre todo,
> **arquitectura de rendimiento**: sin él cada técnico se descarga el inventario entero al
> dispositivo. Quien tenga el enlace del Sheets ve todas las filas igualmente.

**RG-05, Security Filter** sobre `OT_OrdenesTrabajo`:

```
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

**RG-09:** `CHK_Checklists.VersionFormulario`, `Initial value` = `[FormularioID].[Version]`.

**RG-16:** `ACT_Activos.Activo`, `App formula` = `[EstadoActivoID].[Nombre] <> "Retirado"`.

**RG-17:** `ACT_Activos.FechaBaja`, `Required_If` = `[EstadoActivoID].[Nombre] = "Retirado"`.

> **La comparación va contra `[Nombre]`, no contra la columna a secas.** `EstadoActivoID` es un
> `Ref` y **un `Ref` guarda la clave del destino**, que en `EST_Activo` vale `1` a `4`; el texto
> `Retirado` vive en `Nombre`. Escrito `[EstadoActivoID] <> "Retirado"`, RG-16 es **siempre cierta**
> — y al ser una `App formula` **escribe**: repondría `Activo = TRUE` sobre el activo 34, deshaciendo
> en silencio la baja que dejó `ESPEC-001C`. La regla **V-17** de `validar_modelo.py` detiene ahora
> esta clase de error.

**RG-14 y RG-15 — el histórico no se borra.** En *Data > Tables >*, en **Are updates allowed**:

| Tabla | Se deja | Se retira |
|---|---|---|
| `MAN_Mantenimientos` | `Updates`, `Adds` | `Deletes` |
| `OT_OrdenesTrabajo` | `Updates` | `Deletes` **y `Adds`** |

**Por qué también `Adds` en la orden.** `OTID` sigue la convención legible `OT-0001`, y ninguna
tabla del paso 4.3 le asigna `UNIQUEID()` porque eso rompería esa convención. Un contador del tipo
`COUNT(...)+1` **compite consigo mismo**: esta aplicación opera offline y sincroniza después, así
que dos técnicos sin señal generarían el mismo número. Dejar `Adds` sin generación de clave produce
órdenes con `OTID` en blanco.

Mientras no se decida el generador, **las órdenes se crean en el Sheets**. Queda anotado como deuda
y es trabajo de una `ESPEC-003`.

**Solo después de haber poblado `OT.Activo = TRUE` en las 6 órdenes** (paso 5.1).

> **Dónde se cumple esta garantía, y dónde no.** Retirar `Deletes` protege **dentro de la
> aplicación**. Nadie impide que alguien borre la fila a mano en el Sheets, y hay **dos cuentas con
> permiso de edición**. El backend es una hoja de cálculo: no impone unicidad, ni tipos, ni
> integridad referencial, de modo que **toda garantía de este documento vive en la capa de
> aplicación**. Lo que el sistema puede ofrecer es que **falsificar cueste más que hacer el trabajo,
> no que sea imposible**. Es el propósito declarado del proyecto y conviene no prometer más.

**RG-18 — prohibición, no configuración.** No se «activa»: es lo que **no** hay que hacer.

> **Un reporte o una vista NUNCA filtra el histórico por la bandera `Activo` del activo padre.**

Hasta ahora el peligro estaba dormido, porque RG-16 mal escrita era siempre cierta y ningún activo
llegaba a `Activo = FALSE`. **Con RG-16 corregida, el activo 34 pasará a `FALSE`** — y cualquier
vista que filtre por `[ActivoID].[Activo] = TRUE` hará desaparecer retroactivamente todos sus
mantenimientos pasados. Corregir RG-16 es lo que vuelve urgente a RG-18.

Por eso los puntos **3.4 y 3.5** del inventario y el bloque 5 incluyen **buscar ese filtro en las
vistas que ya existen**, y P-13 lo comprueba.

### Las reglas que NO entran en esta fase, y por qué

Agruparlas todas como «bots» sería inexacto y llevaría a configurar cosas que no pueden funcionar:

| Regla | Qué es | Por qué no entra |
|---|---|---|
| RG-08, RG-12 | **Bot programado** | En el plan gratuito los procesos programados **no se ejecutan**. Decisión D-B |
| RG-06, RG-07, RG-10 | **Bot por evento** | Dependen del mismo plan. Se configuran cuando se resuelva D-B |
| RG-11 | **`App formula`**, no un bot | Usa `[FrecuenciaID].[Dias]`, y `PLA_PlanMantenimiento.FrecuenciaID` está **aplazada a `ESPEC-003`**. Va con ella |
| RG-13 | **Verificación de evidencia**, no un bot | Se excluye **por alcance, no por falta de dato**: `MAN.UbicacionEscaneo` está poblada en las 2 filas y en `TEST-MTTO-002` la distancia escaneo-cierre es 8,88 km, así que discriminaría hoy mismo. Pero es un contraste que **se reporta y no bloquea**, y pertenece a los reportes |

RG-11 es el caso que importa: **aplazar una referencia arrastra la regla que la usa.** Si se
configurase RG-11 con `FrecuenciaID` todavía como texto, la fórmula no resolvería y `ProximaFecha`
quedaría en blanco sin decir por qué.

---

## 8. BLOQUE 5 — Reparar lo que rompió el renombrado

Corregir cada vista, fórmula y acción anotada en el punto 3.4 que citara `Numero_OT`, `Activo` como
vínculo al activo, `Tecnico`, `SupervidorID`, `Estado`, `MttoID`, `Tecnico_Asignado`, `EstadoID` o
`SedeID`.

**Y retirar todo filtro por `[ActivoID].[Activo]` sobre datos históricos** (RG-18, punto 3.5).

Es la misma lista que comprueba `PRUEBA-002` P-13.

---

## 9. Criterio de cierre

El de `PRUEBA-002`: **pasan P-01 a P-13 y P-16 a P-18, las dieciséis.** P-14 y P-15 quedan fuera,
bloqueadas por D-01 y D-B.

**Cuatro son innegociables**, y si alguna de las cuatro falla la Fase B no se cierra por muchas de
las otras que pasen:

- **P-05** — la cadena `[OTID].[ActivoID].[Ubicacion]` resuelve. Es el defecto raíz.
- **P-09** — el cierre a 8,89 km es rechazado, con el mensaje escrito.
- **P-12** — el dato llegó al Sheets, no solo a la pantalla.
- **P-16** — RG-16 calcula y **escribe** bien la baja del activo 34.

---

## 10. Cuándo detenerse

- Un paso no produce el efecto esperado **dos veces seguidas**.
- La pantalla no coincide con lo que describe esta especificación.
- Hay que tocar algo que no está aquí.

Parar, documentar qué se hizo, qué se esperaba y qué se vio, y devolver el control. **No improvisar
sobre producción.**

---

## 11. Reversión

**La Fase B solo toca la definición de la aplicación, no el Sheets.** Por tanto:

1. **Restaurar la versión `1.000238` en *Manage > Versions* es la reversión completa de esta fase**,
   siempre que nadie haya escrito en el Sheets durante la ventana.
2. **Filas creadas durante la ventana.** La única prueba que **crea** filas es P-04; P-08 edita una
   que ya existe y P-12 solo lee. Esas filas nuevas se reconocen por su clave
   `UNIQUEID()` —una cadena aleatoria, no un `TEST-`— y como RG-15 retira el borrado **se eliminan a
   mano en el Sheets**.

   **`TEST-MTTO-001` y sus 20 hijos NO se tocan.** Son datos de la Fase A, certificados en
   `ACTA-002`: 3 fotografías, 1 firma, 1 checklist y 15 detalles. Son la cadena de evidencia
   poblada, no residuo de esta fase.

3. **Escrituras sobre `ACT_Activos` fila 34, que es dato maestro y no de prueba.** Dos pruebas la
   tocan y hay que devolverla como estaba:

   | Prueba | Qué escribe | Cómo se restituye |
   |---|---|---|
   | P-16 | Guarda la fila para forzar el recálculo de la `App formula`, tocando `Observaciones` | Devolver `Observaciones` a su valor anterior. **Anótalo antes de tocarlo** |
   | P-17 | Vacía `FechaBaja` en el formulario | La rama que pasa **no persiste nada**: AppSheet rechaza el guardado y se cancela. Si la regla falla y llega a guardar, devolver `FechaBaja = 2026-08-07` |

   Ninguna de las dos cambia el `EstadoActivoID`, así que el activo 34 sigue `Retirado` en todo
   momento.
4. Restaurar el respaldo del Sheets **no** es reversión de la Fase B: tiraría también toda la Fase A.
   Solo se usa si algo corrompe los datos, no la configuración.
5. Anotar en qué paso falló y con qué mensaje **antes** de reintentar.
