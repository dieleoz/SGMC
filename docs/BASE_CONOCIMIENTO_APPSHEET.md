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

Sostiene el orden de `ESPEC-002`: **primero la clave del destino, después quien la apunta** (R-3).
El bloque 1 fija las 27 claves antes de que el bloque 3 cree una sola referencia, precisamente por
esto.

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
| **Que AppSheet evalúe un `Valid_If` sobre una columna con `Editable_If = FALSE`** | **RG-01 sobre `Coordenadas_Cierre`**, y con ella **P-09**, que es innegociable | RG-20 hace la columna no editable y RG-01 pone su validación encima. Si no se evalúa, **la regla parece funcionar por no ejercitarse nunca**: P-09 pasaría sin probar nada. Es el peor modo de fallo posible y no hay página oficial que lo aclare |
