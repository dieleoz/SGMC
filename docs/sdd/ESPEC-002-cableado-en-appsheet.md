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

---

## 4. BLOQUE 1 — Estructura y claves. Van juntas, no separadas

**No se puede hacer *Regenerate* y parar.** Al dar de alta una tabla o regenerarla, **AppSheet fija
una clave por su cuenta e infiere referencias contra ella**. Eso ya ocurrió: las acciones
`View Ref (CalzadaID)`, `View Ref (EstadoID)` y `View Ref (SedeID)` sobre `ACT_Activos` existen
porque AppSheet las creó solo.

Terminar el bloque tras el *Regenerate* deja exactamente el estado que hay que evitar: tablas con la
clave adivinada y referencias automáticas colgando de ella.

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
| `MAN_Mantenimientos` | `CierreConExcepcion`, `RequiereSegundaVisita`, `AprobadoSupervisor`, `Activo` | `Yes/No` |
| `OT_OrdenesTrabajo` | `Activo` | `Yes/No` |
| `OT_OrdenesTrabajo` | `Tipo` | `Enum`: `Preventivo`, `Correctivo`. **Vacía en las 6 filas: deuda declarada.** No la marques obligatoria o las 6 órdenes quedan incompletas |
| `FOT_Fotografias` | `Archivo` | `Image`, calidad baja 600 px |
| `FOT_Fotografias` | `Ubicacion` | `LatLong` |
| `FIR_Firmas` | `Imagen` | `Signature` |
| `TIP_TiposActivo` | `RadioGeofencingKm` | `Decimal` |

Si `Coordenadas_Cierre` queda como `Text`, `DISTANCE()` no opera y el bloque 4 falla sin explicar
por qué.

### 5.1 Poblar `OT_OrdenesTrabajo.Activo` ANTES de seguir

`OT.Activo` está **vacía en las 6 filas**. Tipada como `Yes/No`, un blanco se lee como falso: las
seis órdenes quedarían inactivas.

**En el Sheets, poner `TRUE` en las 6 filas.** Se hace antes de configurar RG-14, porque esa regla
retira el borrado y deja `Activo = FALSE` como única vía de anulación. Retirar el borrado sin que
exista el sustituto deja la orden sin forma de anularse.

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

**RG-04, Security Filter** sobre `ACT_Activos`:

```
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))
```

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

### Las reglas que NO entran en esta fase, y por qué

Agruparlas todas como «bots» sería inexacto y llevaría a configurar cosas que no pueden funcionar:

| Regla | Qué es | Por qué no entra |
|---|---|---|
| RG-08, RG-12 | **Bot programado** | En el plan gratuito los procesos programados **no se ejecutan**. Decisión D-B |
| RG-06, RG-07, RG-10 | **Bot por evento** | Dependen del mismo plan. Se configuran cuando se resuelva D-B |
| RG-11 | **`App formula`**, no un bot | Usa `[FrecuenciaID].[Dias]`, y `PLA_PlanMantenimiento.FrecuenciaID` está **aplazada a `ESPEC-003`**. Va con ella |
| RG-13 | **Verificación de evidencia**, no un bot | `DISTANCE([UbicacionEscaneo], [Coordenadas_Cierre]) <= 0.5`. No necesita ninguna referencia y sí podría entrar, pero es un contraste que **se reporta y no bloquea**: pertenece a los reportes, que son otro frente |

RG-11 es el caso que importa: **aplazar una referencia arrastra la regla que la usa.** Si se
configurase RG-11 con `FrecuenciaID` todavía como texto, la fórmula no resolvería y `ProximaFecha`
quedaría en blanco sin decir por qué.

---

## 8. BLOQUE 5 — Reparar lo que rompió el renombrado

Corregir cada vista, fórmula y acción anotada en el punto 3.4 que citara `Numero_OT`, `Activo` como
vínculo al activo, `Tecnico`, `SupervidorID`, `Estado`, `MttoID`, `Tecnico_Asignado`, `EstadoID` o
`SedeID`.

Es la misma lista que comprueba `PRUEBA-002` P-13.

---

## 9. Criterio de cierre

El de `PRUEBA-002`: **pasan P-01 a P-13**. P-14 y P-15 quedan bloqueadas por D-01 y D-B.

Tres son innegociables: **P-05** (la cadena resuelve), **P-09** (el cierre a 8,89 km es rechazado
con el mensaje escrito) y **P-12** (el dato llegó al Sheets, no solo a la pantalla).

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
2. **Excepción: solo las filas creadas durante la ventana.** La única prueba que **crea** es P-04;
   P-08 edita una fila que ya existe y P-12 solo lee. Esas filas nuevas se reconocen por su clave
   `UNIQUEID()` —una cadena aleatoria, no un `TEST-`— y como RG-15 retira el borrado **se eliminan a
   mano en el Sheets**.

   **`TEST-MTTO-001` y sus 20 hijos NO se tocan.** Son datos de la Fase A, certificados en
   `ACTA-002`: 3 fotografías, 1 firma, 1 checklist y 15 detalles. Son la cadena de evidencia
   poblada, no residuo de esta fase.
3. Restaurar el respaldo del Sheets **no** es reversión de la Fase B: tiraría también toda la Fase A.
   Solo se usa si algo corrompe los datos, no la configuración.
4. Anotar en qué paso falló y con qué mensaje **antes** de reintentar.
