# Base de conocimiento de AppSheet — comportamiento verificado contra la fuente

Base de conocimiento propia del proyecto. Cada afirmación sobre **cómo se comporta AppSheet** lleva
su cita textual, su URL oficial y **qué regla o especificación del SGMC sostiene**.

## Por qué existe

Este proyecto exige verificar contra el archivo antes de afirmar nada (`CLAUDE.md` §3). Durante
cinco rondas de revisión **esa regla se aplicó solo a los datos**. Todo lo que las especificaciones
decían sobre el comportamiento de la plataforma —que un `Ref` guarda la clave, que una `App formula`
escribe, que el *Regenerate* fija claves solo— salía de la memoria de quien lo escribió.

El arquitecto tampoco lo cubría: verifica contra `BD/*.xlsx`, no contra Google. Era un punto ciego
del pipeline, y de él salieron dos correcciones que ninguna otra comprobación habría encontrado
(puntos 4 y 5).

## Cómo se usa

**Antes de escribir una regla, un tipo o un paso que dependa del comportamiento de AppSheet, se
busca aquí.** Si no está, se busca la página oficial y se añade. Si no se encuentra, se declara como
supuesto en la tabla del final — nunca se afirma de memoria.

Para añadir una entrada: cita textual, URL, y **qué sostiene**. Sin la tercera columna la entrada no
sirve para planificar.

---

## Índice cruzado

| # | Comportamiento | Qué sostiene en el SGMC | Estado |
|---|---|---|---|
| 1 | Un `Ref` guarda la clave del destino | **R-1**, `CLAVE_LEGIBLE`, V-17, todo el orden del cableado | Confirmado |
| 2 | Una `App formula` escribe en la hoja al modificar la fila | Gravedad de **RG-16**, segunda parte de **P-16** | Confirmado |
| 3 | La clave va en `Initial value`, nunca en `App formula` | `ESPEC-002` §4.3, los seis `UNIQUEID()` | Confirmado |
| 4 | *Regenerate* elige la clave solo, y puede **componerla** | Fusión de los bloques 1 y 2 en `ESPEC-002` §4 | Confirmado |
| 5 | *Regenerate* añade **columnas virtuales** | Corrige **P-01** | Confirmado |
| 6 | Los bots programados no corren sin plan de pago ni app desplegada | **D-B**, exclusiones de `ESPEC-002` §7, **P-15** | Confirmado |
| 7 | Una referencia rota se marca con `!` | Matiza **R-4**: no es del todo silenciosa | Confirmado |
| 8 | Cambiar la clave de una tabla **rompe** las referencias que la apuntan | `ESPEC-002` §4.2, el orden clave-antes-que-referencia | Confirmado |
| 9 | `DISTANCE()` devuelve **kilómetros** | **RG-01**, el `<= 1.0`, **P-08** y **P-09** | Confirmado |
| 10 | `LatLong` son grados decimales; el espacio tras la coma no es significativo | Formato de las filas `TEST-`, **P-04** | Confirmado |
| 11 | *Regenerate* **fusiona**, no reemplaza: conserva las columnas viejas | Explica por que la Fase B no era cablear 15 columnas | Confirmado |
| 12 | AppSheet **ignora las pestañas ocultas** de un libro | Explica por qué solo cargaban 24 de 32 tablas | Confirmado en la práctica |

---

## 1. Un `Ref` guarda la clave del destino

> «Un `Ref` siempre guarda el valor de la columna clave de la fila referenciada. Por ejemplo, si el
> valor de la clave de una fila de Customers es `Ann Adams`, el campo `Ref` de la fila de Orders
> contendrá el valor `Ann Adams`. La copia del valor de la clave en la columna `Ref` permite al
> sistema recuperar sin ambigüedad la fila correcta de la tabla referenciada.»

[References between tables](https://support.google.com/appsheet/answer/10106510?hl=en)

Es la afirmación más cargada del proyecto: de ella salen R-1, el orden de los pasos, `CLAVE_LEGIBLE`
y la regla V-17. **Hasta el 2026-08-07 nadie la había contrastado.**

## 2. Una `App formula` escribe en la hoja

> «Las columnas con app formulas son útiles para valores que deben calcularse siempre (aparecen
> como solo lectura para el usuario). **Cuando los cambios se sincronizan de vuelta a la hoja, el
> valor calculado se guarda en la celda correspondiente.**»

> «Cuando se abre un formulario **o cuando la fila se modifica por otro mecanismo**, todas las app
> formulas de la fila se recalculan y sus valores se actualizan.»

> «Las app formulas y los valores iniciales pueden hacer cambios **incluso cuando una columna está
> configurada como no editable**.»

[Define app formulas and initial values](https://support.google.com/appsheet/answer/10106437?hl=en)

Sostiene por qué RG-16 mal escrita era crítica y no cosmética. Y confirma que **P-16 necesita su
segunda parte**: la fórmula se materializa al modificar la fila, de modo que mirar la vista previa no
demuestra qué queda guardado.

## 3. La clave se declara en `Initial value`, nunca en `App formula`

> «El valor de la clave debe asignarse una vez, al crear el registro, y permanecer constante durante
> toda su vida. Por eso **debes especificar el valor de la clave en `Initial Value` y nunca en
> `App Formula`**.»

[Define app formulas and initial values](https://support.google.com/appsheet/answer/10106437?hl=en)

Confirma `ESPEC-002` §4.3.

## 4. *Regenerate Structure* elige la clave solo, y puede componerla

> «AppSheet examina cada columna de la hoja **de izquierda a derecha**, buscando una que contenga
> valores únicos, y si la encuentra la convierte en la clave. **Si ninguna columna sirve, examina
> pares de columnas** de izquierda a derecha buscando un par con valores únicos, y si lo encuentra
> **combinará las columnas para crear una clave compuesta**.»

> «Cuando creas la app inicialmente **o cuando regeneras la estructura de una tabla**, AppSheet
> intentará inferir referencias entre tablas automáticamente. Por ejemplo, si Customers tiene `Name`
> como clave y Orders tiene una columna llamada `Customer Name`, se asume que es una columna `Ref`.»

[What is a key?](https://support.google.com/appsheet/answer/10106672?hl=en) ·
[References between tables](https://support.google.com/appsheet/answer/10106510?hl=en)

Confirma que los bloques 1 y 2 **no se pueden separar**. Y aporta un peligro que no estaba en ninguna
especificación: **la clave compuesta**. Contra una clave de dos columnas, ninguna referencia del
bloque 3 resolverá.

Explica también las acciones `View Ref (SedeID)` y `View Ref (EstadoID)` que aparecieron en el
editor: la inferencia es **por coincidencia de nombre**, y los nombres viejos aún estaban.

## 5. *Regenerate Structure* añade columnas virtuales

> «A veces AppSheet **añadirá columnas virtuales automáticamente**, típicamente cuando una tabla se
> añade por primera vez a la app, **o cuando se regenera la estructura de la tabla**.»

[Use virtual columns](https://support.google.com/appsheet/answer/10106758?hl=en)

**Corrigió P-01.** El criterio decía «`MAN_Mantenimientos` debe mostrar 36 columnas» y «más de 36
son definiciones fantasma». Falso: pueden ser virtuales legítimas del tipo
`Related FOT_Fotografias`. Se cuentan las **reales**, y las virtuales aparte.

## 6. Bots programados y plan gratuito

> «Puedes configurar estas funciones, **pero no se ejecutarán como esperas**.»

> «**Si tu aplicación no está desplegada** o no estás en un plan de pago, tu bot no se ejecutará en
> el horario indicado. **Sin embargo, puedes invocarlo pulsando `Test`.**»

> «En cuentas gratuitas, al ejecutar un bot con evento programado, los correos se envían **solo al
> propietario de la app**.»

[Use AppSheet for free](https://support.google.com/appsheet/answer/10104499?hl=en) ·
[Understand bot scheduling and retry](https://support.google.com/appsheet/answer/11547468?hl=en)

Sostiene **D-B**, ya enviada a Dirección. Dos matices que no teníamos: depende también de que la app
esté **desplegada**, y **los bots sí se pueden ejercitar a mano** con `Test`.

## 7. Una referencia rota se marca

> «Cuando los valores seleccionados no coinciden con la columna clave referenciada, resultan
> **referencias rotas (indicadas con un icono `!`)**.»

[Add references between tables](https://support.google.com/appsheet/answer/12798217?hl=en)

**Matiza R-4.** Las especificaciones dicen que una conversión `Text` a `Ref` deja huérfanas las
filas «en silencio». No es exacto: AppSheet **sí marca** la referencia rota con un indicador. Lo que
sigue siendo cierto es que no detiene la conversión ni informa de cuántas filas quedaron así, y que
el indicador hay que ir a mirarlo.

## 8. Cambiar la clave rompe las referencias que la apuntan

> «En el editor puedes seleccionar una clave distinta para la tabla, pero antes es importante
> considerar si la tabla está siendo referenciada. **Esas referencias se romperán.**»

[Troubleshoot AppSheet databases](https://support.google.com/appsheet/answer/14255794?hl=en)

Sostiene R-3: **primero la clave del destino, después quien la apunta.** Las claves de las 28 tablas
se fijan antes de crear una sola de las 39 referencias, precisamente por esto. Las dos cifras salen
de `scripts/modelo_objetivo.py`, no de una especificación: cuando discrepan, manda el modelo.

## 9. `DISTANCE()` devuelve kilómetros

> «`DISTANCE()` devuelve la distancia directa en línea recta entre dos ubicaciones, **en kilómetros
> (km)**, como valor `Decimal`. Multiplica por `0.621371` para millas.»

[DISTANCE()](https://support.google.com/appsheet/answer/11587699?hl=en)

Confirma que el `<= 1.0` de **RG-01** son kilómetros, y que los 8,89 km de `TEST-MTTO-002` caen
fuera del radio con margen. Sostiene **P-08** y **P-09**.

## 10. Formato `LatLong`

> «Una columna `LatLong` guarda una latitud y una longitud (como `48.5564, -122.3421`).» Y: «puedes
> escribir explícitamente un valor `LatLong`, como `46.34,-32.34`.»

[Column data types](https://support.google.com/appsheet/answer/10106435?hl=en) ·
[HERE()](https://support.google.com/appsheet/answer/10107405?hl=en)

Grados decimales. **El segundo ejemplo va sin espacio tras la coma**, así que el espacio no parece
significativo — lo que relaja, sin eliminarla, la advertencia de `ESPEC-001C` sobre no «normalizar»
el formato. `HERE()` devuelve un `LatLong` tal como lo reporta el dispositivo.

---

## 11. *Regenerate Structure* fusiona, no reemplaza

**Verificado el 2026-08-09**, contra la documentación oficial y contra el propio mensaje de error de
la aplicación.

> «Cuando regeneras una tabla que reside en una hoja de Google Sheets o de Excel, AppSheet lee y
> analiza el contenido de esa hoja para determinar el nombre y el tipo de cada columna. **Sin
> embargo, AppSheet combina la información nueva con la que ya exista para la columna e intenta
> mantener el nombre y el tipo de las columnas existentes.**»
>
> — [Add, reorder, or delete columns](https://support.google.com/appsheet/answer/10106675), AppSheet Help

**Consecuencia:** una columna que desapareció de la hoja **no desaparece del esquema**. AppSheet la
conserva a propósito, para no destruir la configuración que tenga encima.

Es una ayuda razonable cuando el cambio es pequeño. **Cuando el esquema divergió mucho, se convierte
en el problema**: `OT_OrdenesTrabajo` sobrevivió a varios *Regenerate* con sus ocho nombres de antes
de la Fase A —`Numero_OT`, `Tecnico`, `Estado`, `Fecha Programada`, `SupervidorID`, `Fecha_Cierre`,
`Cerrada_Por` y un `Activo` de tipo `Ref`— mientras la hoja tenía ya `OTID`, `ActivoID`,
`TecnicoID`, `EstadoOrdenID` y `SupervisorID`.

**Y las columnas reales no se pueden borrar una a una.** Solo las virtuales tienen papelera: las
demás vienen de la hoja y AppSheet no ofrece esa opción.

**La salida la dice el propio AppSheet**, literalmente, al intentar refrescar:

> «Tables must specify a column structure. For some reason, the app definition has been corrupted.
> It may also be possible that you left your column structure in an inconsistent state. **Delete and
> re-add the table to create the column structure.**»

### Qué sostiene

**Que `ESPEC-002` describía mal la Fase B.** Decía «convertir 15 columnas a `Ref`», y el trabajo real
es **borrar cada tabla y volver a darla de alta**, más reponer después la capa de expresiones desde
`RECONSTRUCCION_EXPRESIONES.md`.

**Y explica el bloqueo de permisos como algo estructural, no accesorio.** Si el procedimiento pasa
por dar de alta tablas, **una cuenta coautora no puede ejecutar la Fase B en absoluto**: `Add data`
está reservado al propietario. No es un obstáculo que se rodee con maña.

**Cómo acabó, el 2026-08-09.** No se reparó tabla por tabla: **se creó una aplicación nueva**,
`SISGA`, sobre la misma estructura de datos, y funcionó a la primera. Lo que llevaba dos días
atascado se resolvió en una tarde. Y el número cambió con ella: **las 15 columnas eran las que
faltaban en la aplicación vieja, donde otras 23 ya estaban puestas; sobre una nueva no sobrevive
ninguna y son 38.** Toda lista derivada tiene que declarar de qué punto de partida sale.

## 12. AppSheet ignora las pestañas ocultas

**Verificado el 2026-08-09, en la práctica.** Al crear una aplicación sobre el libro, AppSheet
ofreció **24 tablas de 32**. Las ocho que faltaban estaban marcadas como ocultas:

```
ACT_Activos · USR_Usuarios · TIP_TiposActivo · ROL_Roles
SED_Sedes · CAL_Calzadas · SEN_Sentidos · FRE_Frecuencias
```

**Son el núcleo del modelo.** Sin ellas no hay activos, ni usuarios, ni catálogos, y ninguna
referencia hacia ellas se puede configurar: no aparecen en el desplegable de *Source table*.

**Y no avisa.** La tabla simplemente no está en la lista de *Add data*. Quien busque `ROL_Roles` en
el desplegable concluirá que el problema es suyo.

### Lo que esto delató de nuestras propias comprobaciones

**`verificar_faseA.py` declaró `FASE A CERRADA` dos veces sobre un libro con esas ocho ocultas.**
`openpyxl` las lee sin distinción, así que el script veía las 32 y cerraba la fase mientras AppSheet
veía 24.

Es el mismo modo de fallo que F-17: **la comprobación pasaba porque medía lo que no era.** Se
detecta con `sheet_state`, que `openpyxl` expone y nadie miraba.

Cerrado con **F-18**, probada en los dos sentidos: falla sobre el libro con ocultas, pasa sobre el
corregido.

### Y explica hacia atrás

El 2026-08-08, al abrir *Add data* en la aplicación original, las sugerencias eran `FRM_SOS`,
`FRM_CCTV`, `FRM_PMVF`, `GPS` y `UNF_UnidadesFuncionales` — **ninguna de las ocho ocultas**. La
señal estaba delante y se leyó como un problema de permisos.

## Limitaciones arquitectónicas de fondo

No son comportamientos que se puedan citar de una página: son consecuencias de que **el backend sea
una hoja de cálculo y no una base de datos**. Condicionan el diseño más que cualquier detalle de
sintaxis.

| Limitación | Consecuencia |
|---|---|
| **El Sheets no impone restricciones.** Ni unicidad, ni tipos, ni integridad referencial | Toda garantía vive en la capa de aplicación. Quien escriba directamente en la hoja se salta `Valid_If`, `Required_If` y las referencias. **Hay dos cuentas con permiso de edición**, así que esto es arquitectura y no gobierno |
| **No hay transacciones** | Un mantenimiento, sus fotografías y su firma son escrituras separadas. Una sincronización parcial deja la cadena de evidencia incompleta y nada la revierte |
| **Offline-first: consistencia eventual** | Todo contador o secuencia compite consigo mismo. Es la razón de que `OT_OrdenesTrabajo` perdiera `Adds` |
| **La sincronización baja la tabla al dispositivo** | El Security Filter es arquitectura de rendimiento, no solo control de acceso |
| **Las imágenes van al Drive del propietario** | Cuota y propiedad de un tercero. Decisión D-A |
| **Sin plan Core no hay API REST** | Ni integración ni pruebas automatizadas. De ahí que `PRUEBA-002` sean pruebas de aceptación y no TDD |

**La consecuencia que más se olvida:** «el histórico no se borra» (RG-14, RG-15) se cumple **en la
aplicación**. Alguien con acceso al Sheets borra la fila y no hay nada que lo impida. Lo que el
sistema puede ofrecer es que falsificar cueste más que hacer el trabajo, no que sea imposible.

## Lo que sigue SIN verificar contra la fuente

Se declara, no se afirma. Es lo que puede morder después.

| Afirmación | Dónde se usa | Por qué importa |
|---|---|---|
| El formato exacto que escribe `HERE()` en la hoja, dígito a dígito | **P-04** | No hay ninguna coordenada capturada por la app en todo el sistema. El punto 10 confirma el tipo, no el literal exacto |
| Que retirar `Deletes` en *Are updates allowed* oculta la acción en **todas** las vistas | **RG-14**, **RG-15**, **P-11** | Es la decisión central sobre el histórico. Si alguna vista conserva el borrado, la puerta trasera sigue abierta |
| Que `UNIQUEID()` no colisiona entre dispositivos **sin conexión** | `ESPEC-002` §4.3 y la retirada de `Adds` en `OT` | Es el argumento por el que las órdenes se crean en el Sheets. Si `UNIQUEID()` fuera seguro offline, esa decisión se podría revisar |
| Cuántas filas quedan huérfanas tras una conversión `Text` a `Ref`, y si se informa | **R-4** | El punto 7 confirma que se marcan, no que se cuenten |
| **Que AppSheet evalúe un `Valid_If` sobre una columna con `Editable_If = FALSE`** | **RG-01 sobre `Coordenadas_Cierre_LatLong`**, y con ella **P-09**, que es innegociable | RG-20 hace la columna no editable y RG-01 pone su validación encima. Si no se evalúa, **la regla parece funcionar por no ejercitarse nunca**: P-09 pasaría sin probar nada. Es el peor modo de fallo posible y no hay página oficial que lo aclare |

---

## 13. AppSheet infiere el tipo de cada columna de los datos, no de la hoja

**Comprobado en el editor el 2026-08-10**, sobre `SED_Sedes` recién regenerada:

| Columna | Lo que AppSheet infirió | Lo que declara el modelo |
|---|---|---|
| `SedeID` | `Number` | `Text`, y es la clave |
| `UnidadFuncionalID` | `Number` | `Ref` a `UNF_UnidadesFuncionales` |
| `TramoINVIAS` | `Number` | `Text` |
| `Ubicacion` | `Text` | `LatLong` |

**Lo que esto significa en la práctica: subir el Excel arregla la hoja, no la aplicación.** Son dos
sitios. El Excel fija qué columnas hay y qué datos tienen; **el tipo de cada una, cuál es la clave y
qué es una referencia viven en el esquema de AppSheet**, que se infiere leyendo los datos. Reimportar
no lo corrige, porque la inferencia vuelve a ser la misma sobre los mismos datos.

**El caso que mejor lo ilustra es `TramoINVIAS`.** Los tramos de INVÍAS del corredor son `55CN03`,
`5607` y `5608`: dos parecen números y uno no. Como el único valor cargado hoy es `5607`, AppSheet
la tipa `Number` — y el día que operación escriba `55CN03`, no cabe.

Es el mismo mecanismo que `F-20` caza en las claves, aplicado a cualquier columna. **La diferencia
es que en la clave se pierde la fila entera y en silencio; aquí se pierde un valor.**

### De dónde sale la inferencia, según la documentación oficial

> «AppSheet infers the types of columns from the column header names as well as from the content of
> the rows.»
> — [Effective use of column headers](https://support.google.com/appsheet/answer/10099523), consultado el 2026-08-10

Las palabras que disparan cada tipo son concretas:

| Tipo | Qué lo dispara en el nombre de la cabecera |
|---|---|
| `Ref` | «A column header whose name is similar to another table already in the app» |
| `LatLong` | `latlong`, `geolocation` |
| `Date` | `birthday`, `dob`, `day`, `month`, `year` |
| `Image` | `image`, `picture`, `photo` y sus plurales |
| `Yes/No` | cabecera terminada en `?`, o que empieza por `has` o `is` |

**Ninguna columna de este modelo usa esas palabras**, y de ahí salen dos consecuencias que llevaban
meses sin explicación:

**Ninguna de las 39 referencias se crea sola.** AppSheet infiere `Ref` por parecido con el nombre de
una tabla, y nuestras tablas llevan prefijo —`UNF_UnidadesFuncionales`, no `UnidadFuncional`—, así
que el parecido se rompe. Es el coste de la convención de prefijos **y a la vez su protección**.

**Y explica las tres trampas.** `CHK_Checklists.ActivoID`, `OT_OrdenesTrabajo.FormularioID` y
`CHD_ChecklistDetalle.TipoRespuestaID` se convertían solas en `Ref` porque su nombre **sí** se
parecía a la clave de otra tabla. No era un capricho de la plataforma: era esta regla, funcionando
sobre columnas retiradas.

### Lo que la documentación NO dice

**No ofrece ninguna forma de forzar el tipo desde la hoja.** Lo que dice es que se cambia en
*Data > Columns* con el desplegable, y que para cambios de estructura se modifica el origen y se
regenera. Que formatear la columna como texto plano en Google Sheets fuerce el tipo `Text`
**es un supuesto no verificado**: no aparece en la documentación consultada.

---

## 14. Cómo averiguar el tipo de una columna sin abrir el editor, y hasta dónde vale

**La API v2 devuelve filas, no esquema.** No hay endpoint que diga si una columna es `Text`, `Ref`
o `LatLong`. Eso deja una pregunta sin respuesta barata: las tablas que llegan **vacías** no le dan
a AppSheet ningún dato del que inferir la clave, así que la elige a ciegas — y son justo las seis
que generan clave con `UNIQUEID()`, es decir alfanumérica.

**Si esa clave quedó `Number`, cada fila que cree un técnico se pierde.** Como se perdió un usuario
el 2026-08-10.

### La prueba de sondeo

Se insertó por API una fila con clave alfanumérica en cada una de las ocho tablas de movimiento
—`TEST-OT-999`, `TEST-MAN-999`…— y las ocho fueron aceptadas.

**Qué establece:** si la columna estuviera tipada `Number`, un valor con letras debería fallar la
validación. Que lo acepte es evidencia fuerte de que quedó `Text`.

**Dónde está el hueco, y hay que decirlo:** no está verificado si la API valida el tipo en un `Add`
o si escribe directo a la hoja. Si escribe directo, la aceptación solo prueba que la fila llegó al
Sheets, no que la columna sea `Text`.

**Cómo se cierra:** leyendo la fila **de vuelta** con `Find` antes de borrarla. Si la clave regresa
literal, la columna la aceptó y la conserva. Si vuelve vacía, coercionada, o la fila no aparece, es
`Number`. Eso convierte «lo aceptó» en «lo aceptó y lo conserva», que es lo que importa.

**La comprobación definitiva sigue siendo `Data > Columns`.** El sondeo sirve cuando no se puede
abrir el editor, no en su lugar.

### La advertencia que va con la técnica

**La prueba escribe y borra en producción, y la API tiene más permisos que la aplicación.**

El modelo manda retirar `Deletes` de `OT_OrdenesTrabajo` y `MAN_Mantenimientos` porque hay cuatro
referencias con `IsPartOf` y borrar un mantenimiento se llevaría en cascada sus fotografías, su
firma y su checklist. **La API no ve esa protección: borra igual.**

Sondear una tabla vacía es inocuo. Hacerlo sobre una con histórico es exactamente el modo de fallo
contra el que el sistema entero está diseñado.

---

## 15. Los desplegables de tipo del editor son controles nativos

**Comprobado el 2026-08-10** en `Data > Columns` de `_SISGA_-323965761`: los selectores de la columna
`TYPE` son elementos `<select>` del navegador, no widgets propios de AppSheet. Se comprobó
enumerándolos desde la consola: diez columnas, diez `<select>`, cada uno con la lista completa de
tipos —`Address`, `App`, `ChangeCounter`, `ChangeLocation`, `ChangeTimestamp`, `Color`, `Date`,
`DateTime`…— como `<option>`.

**Por qué importa.** El cableado de esta aplicación son 39 referencias, 4 `IsPartOf`, 12 `Enum`, 4
`ChangeTimestamp` y una decena de tipos sueltos. Hacerlo a base de clics sobre una interfaz que se
redibuja es lento y, peor, **un clic que cae medio píxel fuera cambia la fila de al lado sin que se
note**. Contra un control nativo se puede asignar el valor y disparar su evento, que es
determinista.

### La señal de que el cambio se registró

Cambiar el valor del `<select>` **no basta**: hay que confirmar que la aplicación lo recogió, no solo
que el control se ve distinto. **La señal es que el botón `SAVE` de la cabecera pasa de gris a
azul.** Si sigue gris, el cambio no llegó al modelo interno del editor y se perderá al recargar.

Después de guardar, `SAVE` vuelve a gris. Ese ciclo —gris, azul, gris— es lo que hay que ver.

### Lo que esto no autoriza

**No sustituye a comprobar.** Al terminar cada tabla hay que releer la columna `TYPE` de arriba
abajo contra la ficha del anexo del manual, exactamente igual que si se hubiera hecho a mano. La
automatización quita los clics, no la verificación.

Y va con su riesgo propio: **la interfaz deja de protegerte**. Un valor equivocado aplicado en serie
se aplica en serie. Por eso conviene ir tabla por tabla y guardar en cada una, en vez de encadenar
las 28 y descubrir el error al final.
