# PRUEBA-002 — Pruebas de aceptación de ESPEC-002

Qué tiene que ocurrir para dar por bueno el cableado de la Fase B. **Escrito antes de ejecutar**,
que es lo único que impide medir el resultado con la vara que convenga después.

No es TDD: AppSheet no tiene framework de pruebas y su API REST exige plan Core. Son pruebas de
aceptación, y se llaman por su nombre.

| | |
|---|---|
| Cubre | `ESPEC-002` |
| Estado de partida | Hoja cerrada y verificada, `ACTA-004`. **59 conformes**, 0 fallos |
| Punto de restauración | AppSheet versión `1.000238`; Sheets `SGMC_backup_2026-08-07_antes_cableado_FaseA` |

## 1. Estado de partida

Verificado el 2026-08-07 sobre **`BD/Modelo de Datos (11).xlsx`**, la última **descarga del Sheets
de producción**, con la hoja cerrada en contenido y en formato (`ACTA-004`, 59 conformes y 0
fallos). No es el Excel local histórico, que describe otro modelo:

| Tabla | Filas | Relevancia |
|---|---|---|
| `ACT_Activos` | 34 | Las 34 con `Ubicacion = 4.728512, -74.114531`, en Bogotá |
| `OT_OrdenesTrabajo` | 6 | Estados `Asignada`, `Cerrada`, `Suspendida` |
| `MAN_Mantenimientos` | 2 | `TEST-MTTO-001` en rango y con 8 m de GPS; `TEST-MTTO-002` a 8,89 km y con 45 m |
| `ASG_AsignacionZona` | 4 | Técnicos 3 a 6 contra unidades 7 a 10 |
| `FOT` / `FIR` / `CHK` / `CHD` | 3 / 1 / 1 / 15 | Cadena de evidencia poblada |

`python scripts/validar_modelo.py` devuelve 0 errores.

---

## 2. Pruebas

### P-01 — La estructura llegó a la aplicación

- **Qué comprueba:** que *Regenerate Structure* leyó la hoja actual y no una versión en caché.
- **Precondición:** paso 1 de `ESPEC-002` ejecutado.
- **Acción:** en *Data > Columns*, contar las columnas **reales** de `MAN_Mantenimientos`. Las
  virtuales se cuentan aparte: la documentación oficial confirma que *Regenerate Structure*
  **añade columnas virtuales por su cuenta**, del tipo `Related FOT_Fotografias`.
- **Resultado esperado:** **36 reales**, más las virtuales que AppSheet haya añadido, anotadas.
- **Cómo se distingue el fallo:** 27 reales significa que no regeneró. **Más de 36 reales** son
  definiciones fantasma que sobrevivieron —`MttoID`, `Tecnico_Asignado`, `EstadoID`, `SedeID`— y hay
  que retirarlas; **no confundirlas con las virtuales**, que son legítimas. Menos de 36 y distinto
  de 27, que la hoja cambió sin que nadie lo registrara.

### P-02 — Las siete tablas nuevas existen en la app

- **Acción:** *Data > Tables*, buscar `UNF_UnidadesFuncionales`, `ASG_AsignacionZona`,
  `EOT_EstadosOrden`, `MOT_MotivosPendiente`, `FAL_ModosFalla`, `NOV_Novedades`,
  `PLA_PlanMantenimiento` y **`PAR_Parametros`**.
- **Resultado esperado:** las **ocho**, con el número de columnas que tiene cada hoja.
- **Cómo se distingue el fallo:** con siete no se sigue. La que falte rompe una referencia del
  bloque 3, y si falta `PAR_Parametros` **RG-19 ni siquiera se puede guardar**: su `LOOKUP()` no
  resolvería.

### P-03 — Las claves son las correctas

- **Acción:** *Data > Columns*, revisar la casilla `KEY` en las **27 tablas** de la sección 4.2 de
  `ESPEC-002`, comprobando nombre **y tipo**. Todas las claves van `Text`.
- **Después de forzar el tipo, contar filas:** `ACT_Activos` 34, `USR_Usuarios` 11,
  `OT_OrdenesTrabajo` 6. Forzar el tipo de una clave es la operación que más silenciosamente pierde
  filas: si el recuento baja, la conversión dejó huérfanas.
- **Resultado esperado:** una sola clave por tabla, y la que dice la especificación.
- **Cómo se distingue el fallo:** dos claves marcadas, la clave en otra columna, o la clave tipada
  `Number`. **Es la prueba más silenciosa de todas:** una referencia contra una tabla con la clave
  mal fijada resuelve contra otra columna sin decirlo. Vigila en particular `USR_Usuarios.UsuarioID`
  —si AppSheet la infiere `Number`, la fila `3aa202ee` queda con clave inválida— y que
  `ACT_Activos.ActivoID` sea `Text`, porque `OT.ActivoID` guarda texto y si no coinciden la
  referencia no resuelve.

### P-04 — El formato de la coordenada, confirmado y no supuesto

- **Qué comprueba:** que lo que escribe `HERE()` coincide con lo que guarda `ACT_Activos.Ubicacion`.
  Hoy es un supuesto: no hay ni una coordenada capturada por la app en todo el sistema.
- **Precondición:** `Coordenadas_Cierre` tipada como `LatLong`.
- **Acción:** crear un registro desde la aplicación dejando que `HERE()` capture, y leer el Sheets
  de vuelta con el conector de Drive.
- **Resultado esperado:** un literal con la misma forma que `4.728512, -74.114531` — separador,
  espaciado y decimales comparables.
- **Cómo se distingue el fallo:** cualquier otra forma. **Si difiere, `DISTANCE()` no da error:
  devuelve un número y la regla parece funcionar sin funcionar.** Hay que reescribir las
  coordenadas de las filas `TEST-` antes de seguir.
- **Plan B, obligatorio si el ejecutor es un agente de navegador:** ese agente **no tiene GPS**.
  `HERE()` sin permiso de ubicación devuelve blanco o una posición por IP, que no confirma nada.
  En ese caso, o la captura la hace una persona desde un móvil, o **se declara el formato como
  supuesto verificado** —`4.728512, -74.114531`, el que ya usan las 34 filas de `ACT_Activos`— se
  anota en el acta y se sigue. Dar el formato por confirmado sin ninguna de las dos no vale.

### P-05 — La cadena de referencias existe

- **Qué comprueba:** el defecto raíz del sistema, el que lleva meses abierto.
- **Acción:** en el Asistente de Expresiones, sobre `MAN_Mantenimientos`, escribir
  `[OTID].[ActivoID].[Ubicacion]`.
- **Resultado esperado:** resuelve sin error.
- **Cómo se distingue el fallo:** `Invalid dereference. Column OTID is not a Ref` significa que la
  conversión no quedó. Es el mensaje exacto que este proyecto lleva meses recibiendo.

### P-06 — Los estados de las órdenes resuelven

- **Acción:** abrir las 6 órdenes en la vista previa.
- **Resultado esperado:** las 6 muestran su estado, ninguna en blanco.
- **Cómo se distingue el fallo:** un estado vacío es una fila huérfana. Con las claves de
  `EOT_EstadosOrden` corregidas en `ESPEC-001B` no debería ocurrir; si ocurre, algo se deshizo.

### P-07 — La navegación padre-hijo funciona

- **Acción:** abrir una orden en la vista previa.
- **Resultado esperado:** el activo se muestra como **enlace navegable**, y al pulsarlo se abre su
  ficha.
- **Cómo se distingue el fallo:** si sigue viéndose el número `2`, la referencia no quedó.

### P-08 — POSITIVA: el cierre en rango se acepta

- **Precondición:** RG-01 configurada.
- **Acción:** abrir `TEST-MTTO-001`, cuyo `Coordenadas_Cierre` es `4.728512, -74.114531`, e
  intentar guardar.
- **Resultado esperado:** se guarda sin error.
- **Cómo se distingue el fallo:** si lo rechaza, la regla está invertida o el radio mal puesto.

### P-09 — NEGATIVA: el cierre fuera de rango se rechaza. **La prueba que importa**

- **Qué comprueba:** que la validación **existe**. Una regla de geofencing que nunca ha rechazado
  un cierre no está probada, solo escrita.
- **Acción:** abrir `TEST-MTTO-002`, cuyo `Coordenadas_Cierre` es `4.650000, -74.100000`, a
  **8,89 km** del activo, e intentar guardar.
- **Resultado esperado:** **rechazado**, con el texto exacto
  `Ubicación fuera de rango: debe estar junto al activo para cerrar.`
- **Cómo se distingue el fallo:** dos formas, y ambas cuentan como fallo:
  1. Lo acepta. La regla no se aplica.
  2. Lo rechaza con un error genérico de AppSheet. La regla existe pero el mensaje no guía al
     técnico, que es medio requisito.

### P-10 — El filtro por zona devuelve algo

- **Precondición:** RG-04 configurada, `ASG_AsignacionZona` con sus 4 filas.
- **Acción:** en *Preview app as*, usar el correo de un técnico —por ejemplo
  `santiago.moreno@concesiondelsisga.com.co`, usuario 4, unidad 8— y abrir la lista de activos.
- **Resultado esperado:** **más de cero** activos, y solo los de su unidad funcional.
- **Cómo se distingue el fallo:** cero activos es el bloqueante B-03 sin resolver. Los 34 significa
  que el filtro no se aplica.

### P-11 — El histórico no se puede borrar, y la asimetría es la prueba

- **Precondición:** RG-14 y RG-15 configuradas.
- **Acción:** abrir una orden y un mantenimiento en la vista previa.
- **Resultado esperado**, y son tres cosas distintas:

  | Tabla | Borrar | Añadir |
  |---|---|---|
  | `OT_OrdenesTrabajo` | **No aparece** | **No aparece** |
  | `MAN_Mantenimientos` | **No aparece** | **Sí aparece** |

- **Alcance de lo que demuestra:** que la acción no está **en la aplicación**. Quien tenga acceso al
  Sheets borra la fila igual: el backend es una hoja de cálculo y no impone nada. Esta prueba no
  puede demostrar lo contrario, y conviene no leerla como si lo hiciera.
- **Supuesto declarado:** que retirar `Deletes` oculta la acción en **todas** las vistas. No se ha
  encontrado la página oficial que lo garantice; recórrelas.
- **Cómo se distingue el fallo:** si el botón de borrar está, la puerta trasera sigue abierta.
  Pero ojo con la otra mitad: **si `MAN_Mantenimientos` pierde también `Adds`, P-04 y P-12 quedan
  inejecutables**, porque no habría forma de crear un registro desde la aplicación. La asimetría no
  es un descuido: es lo que hay que demostrar.

### P-12 — LECTURA DE VUELTA: el dato llegó al Sheets

- **Qué comprueba:** que sincronizó. **La aplicación puede mostrar un registro guardado que no
  llegó al backend**, y sin esta prueba no hay forma de saberlo.
- **Acción:** tras P-08, leer `MAN_Mantenimientos` en producción con el conector de Drive,
  `fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.
- **Resultado esperado:** la fila con valor en `Coordenadas_Cierre`, `Precision_GPS`,
  `UbicacionEscaneo` y `FechaHoraEscaneo`. **Las cuatro con dato, no vacías.** Es la otra mitad de
  RG-20: `Editable_If = FALSE` impide que el técnico las toque, pero hay que demostrar que el
  `Initial value` **sigue capturando**. Si además dejaran de escribirse, el geofencing se quedaría
  sin dato y la regla validaría contra vacío.
- **Cómo se distingue el fallo:** si la app lo muestra y el Sheets no lo tiene, hay un problema de
  sincronización que ninguna otra prueba detecta.

### P-13 — Las vistas rotas quedaron reparadas

- **Acción:** recorrer las vistas de la aplicación y el panel de errores del editor.
- **Resultado esperado:** ninguna referencia a `Numero_OT`, `Activo` como vínculo al activo,
  `Tecnico`, `SupervidorID`, `Estado`, `MttoID`, `Tecnico_Asignado`, `EstadoID` ni `SedeID`. Es la
  misma lista del punto 3.4 y del bloque 5 de `ESPEC-002`: si divergen, el ejecutor repara una cosa
  y el probador mide otra.
- **Y ninguna vista, slice o reporte filtra por `[ActivoID].[Activo]`** sobre datos históricos
  (RG-18). Con RG-16 corregida el activo 34 pasa a `Activo = FALSE`, así que un filtro así haría
  desaparecer sus mantenimientos pasados de los informes.
- **Cómo se distingue el fallo:** cualquier vista que cite un nombre viejo. La app lleva rota desde
  la Fase A y esto es lo que la devuelve a funcionar.

---

### P-18 — POSITIVA Y NEGATIVA: el cierre con GPS deficiente se marca solo (RG-19)

- **Qué comprueba:** que `CierreConExcepcion` se calcula y no se edita. Sin ella, un cierre con
  error de satélite alto es indistinguible de uno bueno.
- **Precondición:** RG-19 configurada leyendo el umbral de `PAR_Parametros` con `LOOKUP()`, y
  `UMBRAL_GPS = 40` en esa tabla. `Precision_GPS` tipada `Number`.
- **Acción:** abrir en la vista previa `TEST-MTTO-001` (8 m) y `TEST-MTTO-002` (45 m).
- **Resultado esperado:** el primero `FALSE`, el segundo **`TRUE`**. Y en ninguno de los dos el
  técnico puede modificar la casilla: una `App formula` es de solo lectura para el usuario.
- **Cómo se distingue el fallo:** si los dos salen igual, la fórmula no se aplicó o `Precision_GPS`
  quedó como `Text` y la comparación numérica no opera. Si la casilla es editable, no se configuró
  como `App formula` sino como valor inicial, y el técnico podría desmarcar su propia excepción.
- **Prueba del parámetro:** cambiar `UMBRAL_GPS` a `50` en `PAR_Parametros` y comprobar que
  `TEST-MTTO-002` pasa a `FALSE` sin tocar la aplicación. Devolverlo a `40`. Es lo que demuestra que
  el administrador puede calibrarlo con las pruebas de campo sin abrir el editor.

### P-19 — Las columnas de captura no se pueden editar (RG-20)

- **Qué comprueba:** el hallazgo más grave de las ocho rondas de revisión. `HERE()` y
  `USERLOCATIONACCURACY()` son `Initial value`, no `App formula`, y **un valor inicial sí se puede
  editar**. Sin RG-20, el técnico arrastra el pin del mapa encima del activo y RG-01 valida sin
  protestar: la regla se cumple y la presencia no queda probada.
- **Precondición:** RG-20 configurada, `Editable_If = FALSE` en las cuatro columnas.
- **Acción:** abrir un mantenimiento en el formulario de la vista previa.
- **Resultado esperado:** `Coordenadas_Cierre`, `Precision_GPS`, `UbicacionEscaneo` y
  `FechaHoraEscaneo` se muestran **sin control de edición**.
- **Cómo se distingue el fallo, y es concreto:** en `Coordenadas_Cierre` **no debe aparecer el pin
  arrastrable sobre el mapa**, solo el valor. Si el pin está, la columna es editable y el geofencing
  es decorativo.
- **La otra mitad la comprueba P-12:** que las cuatro sigan llegando **con dato** al Sheets. No
  editable y sin capturar sería igual de inútil.

### P-16 — POSITIVA Y NEGATIVA: la baja de activos se deriva bien (RG-16)

- **Qué comprueba:** la regla que motivó el tercer bloqueo. `ACT_Activos.Activo` se calcula desde el
  estado y **no** se edita. El fixture ya está servido: 33 activos en `Operativo` y **el 34 en
  `Retirado`**.
- **Precondición:** RG-16 configurada como `App formula` = `[EstadoActivoID].[Nombre] <> "Retirado"`.
- **Acción:** abrir en la vista previa el activo `34` y cualquiera de los otros 33.
- **Resultado esperado:** el 34 muestra `Activo` en **FALSE**; los demás, en **TRUE**.
- **Cómo se distingue el fallo:** si el 34 sale `TRUE`, la comparación va contra la clave y no
  contra `[Nombre]` — el defecto exacto del 2026-08-07.
- **Segunda parte, obligatoria: demostrar que ESCRIBE bien.** Lo anterior prueba que la fórmula
  *muestra* bien, no que *escriba* bien, y una `App formula` de AppSheet materializa su valor **al
  guardar la fila**. Que la celda ya valga `FALSE` no prueba nada: la puso a mano el paso 5.1.
  1. **Guardar** el activo 34 desde la aplicación. Basta con tocar `Observaciones`.
  2. **Leer `ACT_Activos` de vuelta** en producción con el conector de Drive.
  3. `Activo` de la fila 34 debe seguir en **`FALSE`**.
- **Cómo se distingue este fallo:** si al guardar se repone a `TRUE`, la fórmula está deshaciendo la
  baja en cada escritura. Es exactamente el daño que motivó el tercer bloqueo, y sin este paso la
  prueba no lo vería.

### P-17 — La baja exige fecha (RG-17)

- **Precondición:** RG-17 configurada como `Required_If` = `[EstadoActivoID].[Nombre] = "Retirado"`.
- **Acción:** **sobre el activo 34, que ya está `Retirado`** — no se cambia el estado de ningún
  otro—, **vaciar `FechaBaja` en el formulario de la aplicación**, no en el Sheets, e intentar
  guardar.
- **Resultado esperado:** **no deja guardar** hasta rellenar `FechaBaja`.
- **Restitución:** si la regla funciona, **no hace falta**. AppSheet rechaza el guardado, se sale
  con *Cancelar* y **nada persiste**: por eso el vaciado va en el formulario y no en la hoja. La
  restitución solo aplica a la rama de fallo —si llegó a guardar—, y entonces se devuelve
  `FechaBaja = 2026-08-07`.
- **Se ejecuta la última de la tanda**, como cinturón: si algo la interrumpe, no arrastra a las
  demás.
- **Cómo se distingue el fallo:** si guarda con la fecha vacía, la condición nunca se cumple —mismo
  defecto que P-16— y el histórico no podrá explicar por qué el activo dejó de recibir
  mantenimiento.

> **Por qué sobre el 34 y no sobre otro.** Retirar un activo cualquiera para probar escribiría sobre
> un dato maestro que no es de prueba, y si la tanda se interrumpe a medias queda un activo retirado
> por error, con `Activo = FALSE` calculado por RG-16 y su histórico expuesto a RG-18. El 34 ya está
> dado de baja: solo se toca una fecha, y se restituye.

---

## 3. Pruebas bloqueadas

### P-14 — Geofencing con coordenadas reales · **BLOQUEADA POR D-01**

Los 34 activos comparten `4.728512, -74.114531`, que está en Bogotá y no en el corredor. Cualquier
cierre real en la vía quedará fuera de rango y cualquier cierre en Bogotá quedará dentro.

**No es un fallo de la Fase B.** P-08 y P-09 demuestran que **la regla funciona**; esta demostraría
que **el dato es correcto**, y para eso hace falta el levantamiento de campo.

### P-15 — Reglas fuera de alcance · **NO SE PRUEBAN EN ESTA FASE**

| Regla | Qué es | Por qué no se prueba |
|---|---|---|
| RG-08, RG-12 | Bot programado | No se ejecutan solas en el plan gratuito ni sin app desplegada. **Su lógica sí se puede ejercitar a mano con `Test`** en Automation > Bots. D-B |
| RG-06, RG-07, RG-10 | Bot por evento | Mismo plan |
| RG-11 | `App formula` | Usa `[FrecuenciaID].[Dias]`, referencia aplazada a `ESPEC-003` |
| RG-13 | Verificación de evidencia | Excluida por alcance, no por falta de dato |

La clasificación es la de `ESPEC-002` §7, y **no son todas bots**: RG-11 es una `App formula` que
depende de una referencia aplazada, y RG-13 una verificación de evidencia excluida por alcance.
Si esta lista y la de `ESPEC-002` divergen, el ejecutor configura una cosa y el probador mide otra.


---

## 4. Criterio de cierre

**Deben pasar P-01 a P-13 y P-16 a P-19, las diecisiete.** P-14 y P-15 quedan bloqueadas por decisiones ajenas a esta
fase.

**Cuatro** son innegociables, y conviene decir por qué antes de que alguien proponga cerrar sin ellas:

- **P-05**, porque es el defecto raíz. Sin la cadena no hay sistema, solo formularios.
- **P-09**, porque una validación que nunca ha rechazado nada no está probada. Es la única prueba
  que distingue «la regla funciona» de «la regla no se aplica».
- **P-12**, porque sin lectura de vuelta no hay constancia de que el dato salió de la pantalla.
- **P-16**, porque corregir una regla y no probarla deja el arreglo sin constancia. Es el bucle que
  `ACTA-002` §3 dejó por escrito, y RG-16 **escribe** sobre los datos.

Si alguna de las **cuatro** falla, la Fase B **no se cierra**, por muchas de las otras que pasen.
