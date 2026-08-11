# ESPEC-005 — Generador de `OTID` y `PlanID`, y su etiqueta ante el técnico

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.Etiqueta, PLA_PlanMantenimiento.Etiqueta -->
<!-- D-03 compara Tabla.Columna contra MODELO, y Etiqueta a propósito NUNCA entra en MODELO: es
     una columna virtual declarada solo en REGLAS (RG-35/RG-36, §4). Citarla en prosa como
     Tabla.Columna es legítimo -es como se documenta una virtual-, no un hueco del modelo. -->

**Rehecha el 2026-08-10 tras bloqueo del arquitecto.** La versión anterior recibió catorce
hallazgos. Tres eran defectos de código y ya están aplicados en el repositorio, fuera de esta
especificación: `V-11` de `validar_modelo.py` ahora recorre también las columnas (no solo
`REGLAS`), los pasos de `docs/PROMPT_CABLEADO.md` se numeran solos, y `scripts/capacidad.py`
deriva el número de activos de `ACT_Activos` en vez de traerlo escrito a mano. Los once restantes
—incluida una condición que cambia el diseño de `Etiqueta`— se atienden en esta versión, verificada
de nuevo contra el archivo en cada punto, no reescrita desde la memoria de la anterior.

## 1. Qué se quiere y por qué

Las ocho tablas transaccionales (`OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `CHK_Checklists`,
`CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `NOV_Novedades`, `PLA_PlanMantenimiento`)
llegaron vacías a AppSheet. Sobre una tabla vacía, AppSheet exige un `Initial value` antes de dejar
marcar `Key`, o se queda con `_RowNumber`. Para seis de las ocho eso está resuelto: pertenecen a
`CLAVE_GENERADA` en `scripts/modelo_objetivo.py` y basta con declarar `Initial value = UNIQUEID()`.

`OT_OrdenesTrabajo.OTID` y `PLA_PlanMantenimiento.PlanID` no. Son claves legibles con prefijo
(`OT-0001`, `PLA-001`), están en `CLAVE_LEGIBLE`, y el modelo no declara quién escribe ese valor.
Eso no es un hueco cosmético: `RG-10` (bot que crea una orden de seguimiento cuando
`RequiereSegundaVisita = TRUE`) y `RG-12` (bot programado que genera las órdenes de la semana desde
el plan) **crean filas en `OT_OrdenesTrabajo` sin asignar `OTID`**. Una fila sin clave, AppSheet la
descarta sin avisar. La decisión que esta especificación permite tomar es: **quién escribe `OTID` y
`PlanID`, para que marcar `Key` sobre esas dos columnas deje de estar bloqueado y para que los
dos bots dejen de crear filas huérfanas.**

De los dos bots, ninguno está cableado hoy — y eso importa para no exagerar la urgencia (§6). Según
`ESTADO.md:56`: *"Los 5 bots | 3 se pueden poner; `RG-10` y `RG-12` no | `ESPEC-005`"*. El bloqueo
es exactamente el que resuelve esta especificación: nadie puede configurar `RG-10` en
`Automation > Bots` mientras `OTID` no tenga una forma de generarse, porque la primera fila que
cree se perdería sin avisar y no habría manera de comprobar el bot. El riesgo es real pero
**prospectivo**: se activa el día que, después de esta especificación, alguien cablee `RG-10` en el
editor y un técnico marque una segunda visita — no antes.

### Por qué no basta con sembrar una fila de ejemplo

Se propuso sembrar una fila en las ocho tablas vacías para que AppSheet infiera bien claves y tipos.
El arquitecto ya lo rechazó con dos argumentos, y los dos siguen de pie después de mirar el archivo:

- Sembrar `FOT_Fotografias` y `FIR_Firmas` fabrica evidencia dentro de un sistema cuyo propósito es
  que la evidencia sea difícil de falsificar. El propio `SDD_PIPELINE_SGMC.md` (§5.1, Higiene de los
  datos de prueba) ya documenta el costo real de esto: `CHK_Checklists` tuvo una fila con
  `TecnicoID = "Santiago Moreno"` y `FechaInicio = "NOW()"` como texto literal, sin marca `TEST` y
  sin fecha de retiro. La hoja vigente está vacía "y es la primera vez que eso pasa". Reabrirlo
  reproduce el hallazgo que ese párrafo existe para evitar.
- Que las ocho tablas estén vacías es lo que hace que corregir tipos y claves hoy no cueste nada; con
  una fila dentro, cada corrección posterior pasa a ser una migración.

Hay un tercer argumento, verificado en el archivo y no solo de principio: **sembrar no hace falta
para lo que se le pediría.** `docs/PROMPT_CABLEADO.md`, sección *"Paso 2 — Las claves de las 8
tablas que llegaron vacías"* (los números de sección de este documento **se regeneran** cada vez
que cambia el modelo — ver §12 de esta especificación sobre por qué aquí se cita por título y no por
línea), ya documenta que basta con declarar `Initial value = UNIQUEID()` **sobre la tabla vacía**
para que AppSheet deje marcar `Key`: *"AppSheet no te va a dejar marcar `Key` sin más. Sobre una
tabla vacía exige que la columna tenga un `Initial value` que genere la clave; si no, asume que las
filas nuevas nacerían sin identificador y se aferra a `_RowNumber`. Así que primero el valor,
después la casilla."* Esto ya se sigue con seis tablas sin necesitar una sola fila de datos.
Extender el mismo mecanismo a `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` (§3) logra lo mismo sin
sembrar nada y sin ninguno de los dos costos de arriba. No hay una forma acotada de sembrar que
valga la pena: la alternativa sin sembrar ya funciona y ya está en uso.

### Clase de cambio: "migrar después cuesta", y con fecha de caducidad

Esta especificación se justifica en parte porque las dos tablas están vacías hoy y corregirlas no
cuesta nada. Eso es cierto **solo hasta el primer dato real**. Lo que esta versión añade, que la
anterior no decía, es que esa fecha de caducidad **no es al final del despliegue: es el primer
fixture de `PRUEBA-005`.** En cuanto esa tanda cree la primera fila de prueba en `OT_OrdenesTrabajo`
(§3.4 y §6 más abajo), la ventana barata se cierra **para siempre** en esa tabla — incluida la
limpieza del propio fixture, que por diseño no vuelve a dejarla en cero (§6, y `PRUEBA-005` §1.2).
Cualquier otro cambio de estructura sobre `OT_OrdenesTrabajo` o `PLA_PlanMantenimiento` que se
plantee después de `PRUEBA-005` ya no puede argumentar "la tabla está vacía, no cuesta nada": hay
que decirlo así en cualquier especificación futura que las toque, para no repetir el argumento del
§1 sobre una premisa que dejó de ser cierta sin que nadie lo anunciara.

## 2. Estado actual verificado

Todo lo siguiente se leyó de `scripts/modelo_objetivo.py` (el modelo, fuente única) y de
`BD/Modelo_Datos_PLANTILLA.xlsx` (el volcado local), reverificado el 2026-08-10. Según
`python scripts/sistema.py`, la aplicación vigente es `_SISGA_-323965761` sobre la hoja
`Modelo_Datos_10082026`, y ese volcado es hoy el mismo archivo mientras nadie edite el Sheets
directamente. Donde se cita la aplicación en vivo (§2.8), se dice explícitamente: es lectura por
API, no del volcado.

### 2.1 Las ocho tablas están vacías hoy — y de dónde sale esa afirmación, con cuidado

```
python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True)
for t in ['OT_OrdenesTrabajo','PLA_PlanMantenimiento','MAN_Mantenimientos','CHK_Checklists',
          'CHD_ChecklistDetalle','FOT_Fotografias','FIR_Firmas','NOV_Novedades']:
    ws = wb[t]
    n = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if any(c not in (None,'') for c in r))
    print(t, n)
"
```
Salida: las ocho en `0`.

**Esta salida, por sí sola, no prueba nada sobre el estado real de la aplicación.** El comando lee
`BD/Modelo_Datos_PLANTILLA.xlsx`, el volcado local, y ese archivo es **ciego por diseño** a estas
ocho tablas: `generar_plantilla.py` las vacía en cada pasada porque son registros de movimiento y la
plantilla es lo que recibe el funcional. `scripts/lectura_de_vuelta.py` lo declara explícitamente en
`VOLCADO_CIEGO_A` — *"Una fila creada en la APLICACION -un fixture de prueba, una orden real- nunca
llega a ese archivo. Cualquier comprobacion que espere verla ahi no puede dispararse jamas, y pasa en
verde por no ejercitarse."* Es decir: este comando daría `0` en las ocho **aunque la aplicación en
vivo tuviera filas reales**, porque nunca las mira.

La afirmación de la que sí depende esta especificación —que las ocho están en cero **hoy, en la
aplicación**, no solo en su volcado— se apoya en `PRUEBA-005` §1.1, que lee por API con
`python scripts/instantanea.py guardar prueba-005-partida` y confirma `0` en las tres tablas que
importan para el fixture (`OT_OrdenesTrabajo`, `PLA_PlanMantenimiento`, `MAN_Mantenimientos`)
contra la aplicación viva, no contra el archivo. Las dos verificaciones coinciden hoy, pero por
motivos distintos y con instrumentos distintos: una es estructural (el generador vacía a propósito),
la otra es una medición (la API no tiene nada que devolver todavía). Confundirlas sería apoyar una
especificación sobre producción en un comando que no puede refutarla.

### 2.2 `python scripts/validar_modelo.py` hoy

```
Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 21
ERRORES: ninguno
AVISOS (3):
  [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
APTO PARA DESPLEGAR
```

`V-06` confirma algo que reutilizo en el §3: **nada referencia `PLA_PlanMantenimiento`**. Ningún
`Ref` de las 28 tablas apunta a ella (`grep ref="PLA_PlanMantenimiento" scripts/modelo_objetivo.py`
no devuelve nada). `OT_OrdenesTrabajo`, en cambio, sí es destino: `MAN_Mantenimientos.OTID` y
`OT_OrdenesTrabajo.OTOrigenID` (autorreferencia) apuntan a ella, dos referencias.

### 2.3 `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"` hoy

```
AVISOS (4):
  [F-01] OT_OrdenesTrabajo.Activo sigue existiendo (...)
  [F-04] 14 columnas siguen pendientes de retipar a Ref (...)
  [F-11] OT_OrdenesTrabajo esta vacia en la hoja: no se puede decidir si su clave es legible.
  [F-11] PLA_PlanMantenimiento esta vacia en la hoja: no se puede decidir si su clave es legible.
FASE A CERRADA
```

`F-11` se salta precisamente en las dos tablas que esta especificación resuelve, porque su lógica
(`scripts/verificar_faseA.py:264-306`) exime del todo a `CLAVE_GENERADA` y compara contra
`CLAVE_LEGIBLE` a las demás. Moverlas a `CLAVE_GENERADA` (§3) hace que este aviso deje de tener nada
que decidir, en vez de resolverlo con datos que no existen. **Verificado por simulación sobre una
copia temporal del repositorio con los siete cambios de §4 aplicados**: los dos `F-11` desaparecen y
no aparece ningún `F-02` nuevo — ver §3.2 sobre por qué no aparece ninguno.

### 2.4 Ningún `Ref`, `valid_if`, `formula` ni `valor_inicial` del modelo compara `OTID` o `PlanID`
contra un literal

```
grep -n '\[OTID\]\|"OT-\|OT-0001\|\[PlanID\]\|"PLA-' scripts/modelo_objetivo.py
```
Las únicas apariciones de `[OTID]` son dereferencias (`[OTID].[ActivoID]...`, dos veces, en `RG-01`
y en el `valid_if` de `Coordenadas_Cierre_LatLong`), y una nota de comentario. `PlanID` no aparece
comparado contra nada. `validar_modelo.py` (V-17) solo dispara sobre patrones del tipo
`[Columna] = "literal"` con la columna **sin** un punto después —una dereferencia como
`[OTID].[ActivoID]` queda excluida por el `(?!\s*\.\s*\[)` de la propia expresión regular—. Es
decir: **hoy nada se rompe en `validar_modelo.py` si `OTID` deja de ser legible**, porque nada lo
compara como si lo fuera.

Aparte, `RG-08` (`AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`) compara
`[EstadoOrdenID].[EsFinal]`, no `[EstadoOrdenID]` a secas ni `[OTID]`. Es una dereferencia sobre
`EOT_EstadosOrden` —que sí está en `CLAVE_ES_LA_PALABRA`, y ahí es legítimo comparar contra un
literal ("Cerrada", "Asignada")—, y no toca en absoluto la legibilidad de `OTID`. `CLAVE_LEGIBLE`
(cómo se ve la clave) y `CLAVE_ES_LA_PALABRA` (contra cuáles literales es legítimo comparar) son
listas distintas a propósito, y hoy contienen: `CLAVE_ES_LA_PALABRA = {EOT_EstadosOrden,
FRM_Formularios, PAR_Parametros, SEN_Sentidos}` — ni `OT_OrdenesTrabajo` ni `PLA_PlanMantenimiento`
están ahí, así que esta especificación no toca esa lista.

### 2.5 `Etiqueta`: por qué es una columna VIRTUAL y no una `App formula` sobre columna real

Esta es la condición que cambia el diseño de la versión anterior, y se resuelve aquí con cinco
verificaciones separadas, no con una afirmación.

**Primero, la incógnita que el arquitecto marcó como no asumible: ¿puede un `Label` ser una columna
virtual?** `docs/BASE_CONOCIMIENTO_APPSHEET.md` no tiene ninguna línea sobre `Label`
(`grep -i label docs/BASE_CONOCIMIENTO_APPSHEET.md` — cero resultados). Se verificó contra la
documentación oficial de Google, no se adoptó como supuesto:

> «You can create a row label containing values from two or more columns as follows: Add a virtual
> column to the table. In the App formula field of the virtual column, enter a `CONCATENATE()`
> expression that combines appropriate column values to form the row label. For example:
> `CONCATENATE([First label column], ", ", [Second label column])`. Disable the `Label?` property
> for any existing row label column. Enable the `Label?` property of the virtual column.»

— [Add row labels](https://support.google.com/appsheet/answer/10106376), AppSheet Help (consultado
2026-08-10). No es solo "se puede": **es el mecanismo que Google documenta como la forma correcta**
de componer una etiqueta a partir de dos o más columnas. `CONCATENATE()` queda verificado como la
función a usar, no diferido.

Con eso resuelto, `Etiqueta` se declara como **columna virtual**, siguiendo el molde que
`docs/sdd/ESPEC-003-modelo-de-dominio.md:985-1002` fijó para `MinutosRelojParado` y su `RG-29` (esa
especificación sigue bloqueada y `RG-29` no existe aún en `scripts/modelo_objetivo.py`; lo que se
reutiliza aquí es el patrón de diseño, no una dependencia de que se aplique primero). Esto resuelve
cinco hallazgos de golpe:

1. **No escribe en la hoja, así que no viola R-6** (`CLAUDE.md:207`, *"un dato se alcanza por
   referencia o se guarda, nunca las dos cosas"*). Con `App formula` sobre columna real, renombrar
   un activo dejaría etiquetas viejas en las órdenes ya sincronizadas mientras la referencia resuelve
   al nombre nuevo: dos copias diciendo cosas distintas. Con columna virtual, `Etiqueta` se recalcula
   en cada sincronización y nunca queda un valor viejo guardado.
2. **La valida `V-11`, y ahora por la única vía que existe para una columna virtual.** `V-11` ya
   recorre columnas además de `REGLAS` (fix aplicado, ver cabecera de este documento), pero una
   columna virtual **no se declara en `MODELO`** (punto 4 más abajo), así que no hay ningún
   `c["formula"]` que recorrer para ella. La única forma de que `V-11` la vea es que esté declarada
   como `REGLA` — no es una garantía redundante, es la única puerta que queda abierta. Verificado en
   §3.2.
3. **Las virtuales tienen papelera, así que es reversible.** `docs/BASE_CONOCIMIENTO_APPSHEET.md:212`:
   *"Y las columnas reales no se pueden borrar una a una. Solo las virtuales tienen papelera: las
   demás vienen de la hoja y AppSheet no ofrece esa opción."* Si `Etiqueta` resulta mal cableada, se
   borra desde la papelera de columnas virtuales sin necesitar un `Delete and re-add the table`.
4. **No obliga a tocar el Sheets de producción.** `verificar_faseA.py` (`F-02`) exige que toda
   columna del modelo exista en la hoja; una columna que nunca entra en `MODELO` nunca dispara esa
   exigencia. Verificado por simulación (§3.2): ni antes ni después de declarar `Etiqueta` aparece
   ningún `F-02`, y `generar_plantilla.py` no necesita correr — nadie tiene que acordarse de meter la
   columna en `Modelo_Datos_10082026` a mano, y ningún verificador lo habría notado si se le
   olvidaba.
5. **Aparece sola en `RECONSTRUCCION_EXPRESIONES.md` y `PROMPT_EXPRESIONES.md`.** Ambos generadores
   iteran `REGLAS`, no `col(..., formula=...)`. Verificado por simulación en §3.2 y en `PRUEBA-005`
   `P-07`.

### 2.6 Un hallazgo cruzado: `ROADMAP.md` y el modelo no dicen lo mismo sobre `Adds` en `OT_OrdenesTrabajo`

`scripts/modelo_objetivo.py` declara `RG-14` como `tabla="OT_OrdenesTrabajo"`, `expresion="Updates,
Adds"`, sin condición. `docs/MANUAL_DESPLIEGUE.md` y `docs/PROMPT_CABLEADO.md`, ambos generados de
ese mismo modelo, instruyen `Adds sí` para `OT_OrdenesTrabajo`. `docs/ROADMAP.md` §4.5, reverificado
hoy:

```
grep -n "Creación de órdenes desde la app" docs/ROADMAP.md
```
```
346:| Creación de órdenes desde la app | **Desbloqueada, pendiente de aplicar.** El motivo del
aplazamiento era que OTID hacía de clave y de etiqueta legible a la vez; ESPEC-005 lo separa —clave
con UNIQUEID(), columna Etiqueta aparte— y RG-14 ya declara Updates, Adds. (...)
```

Ya no dice lo que la versión anterior de esta especificación señalaba como desactualizado
("Aplazada, no descartada"): alguien lo corrigió por la vía rápida del §6 del pipeline, tal como esa
versión anticipaba. No hace falta ninguna acción sobre `ROADMAP.md` en esta especificación.

### 2.7 Escala: por qué una convención de 4 dígitos no resiste — y por qué eso es un argumento secundario

```
python scripts/capacidad.py
```
`scripts/capacidad.py` ya no trae el literal `34` que envejeció en silencio (fix aplicado, ver
cabecera): deriva los activos de `ACT_Activos` y hoy da 368. El escenario "Hoy" con 368 activos
produce 5.299 mantenimientos/año; el escenario "Inventario del Plan Maestro" (355 activos, el número
que citan `CONTEXTO_OPERACION.md` y la plantilla) da 5.112/año. Con cualquiera de los dos, una clave
`OT-0001` de 4 dígitos (rango 9.999) se agota en menos de 2 años:

```
python3 -c "
mtto = 5112  # Plan Maestro, scripts/capacidad.py
print('4 digitos: %.2f anios' % (9999/mtto))
print('5 digitos: %.2f anios' % (99999/mtto))
"
```
```
4 digitos: 1.96 anios
5 digitos: 19.56 anios
```

**Esto es un argumento secundario, y se declara así a propósito.** Un dígito más multiplica el
margen por diez —de "menos de 2 años" a "casi 20"— porque el agotamiento de un contador de ancho
fijo se resuelve trivialmente ensanchando el formato. No es un argumento que se sostenga solo: si
la única razón para abandonar la clave legible fuera el agotamiento, la respuesta correcta sería
`OT-00001` con cinco dígitos, no `UNIQUEID()`. **El argumento que sí se sostiene solo, y es el único
necesario, es la concurrencia** (§3.1): un `Initial value` calculado en el dispositivo no tiene
forma de coordinarse entre dos técnicos sin señal, ni entre `RG-10` y un técnico creando una
correctiva a la vez, y eso no lo arregla ningún número de dígitos. Se conserva el dato de escala
como contexto, no como coargumento de peso equivalente.

### 2.8 `auditar_cableado.py`: las dos referencias hacia `OT_OrdenesTrabajo` están hoy "miradas a ojo", no medidas — y eso es un riesgo para el cambio de clave

Corrido en vivo hoy contra la aplicación (lectura, `Action: Find`, no escribe nada):

```
python scripts/auditar_cableado.py
```
```
De las 39 referencias declaradas:
     4 VERIFICADAS: la aplicacion nombra la columna
    29 compatibles, no atribuidas
     6 NO SE PUEDEN JUZGAR: su tabla destino esta vacia
     - MAN_Mantenimientos.OTID -> OT_OrdenesTrabajo mirada el 2026-08-10 por Diego, en el editor
     - OT_OrdenesTrabajo.OTOrigenID -> OT_OrdenesTrabajo mirada el 2026-08-10 por Diego, en el editor
```

Dos cosas verificadas aquí, no una sola. **Uno:** `OT_OrdenesTrabajo` está entre las tablas cuya
tabla destino está vacía, así que el script **no puede medir** si las dos referencias que la
apuntan (`MAN_Mantenimientos.OTID`, `OT_OrdenesTrabajo.OTOrigenID`) están bien cableadas — es
exactamente la limitación que su propio código documenta: *"La columna virtual vive en el DESTINO.
Si el destino esta vacio, la API no devuelve ninguna fila y por tanto ningun nombre de columna: de
esas referencias este script NO PUEDE DECIR NADA."* **Dos, y es el hallazgo nuevo:** el propio
script registra que esas dos referencias **ya fueron miradas y configuradas en el editor**, con
fecha de hoy (`CONFIRMADAS_A_OJO`, `scripts/auditar_cableado.py:82-88`) — es decir, **el paso de
"Las 39 referencias" ya se ejecutó para estas dos, antes de que el paso de la clave (esta
especificación) se aplique.**

Eso importa porque `docs/BASE_CONOCIMIENTO_APPSHEET.md:156-165` cita la documentación oficial:

> «En el editor puedes seleccionar una clave distinta para la tabla, pero antes es importante
> considerar si la tabla está siendo referenciada. **Esas referencias se romperán.**»

— [Troubleshoot AppSheet databases](https://support.google.com/appsheet/answer/14255794?hl=en)

Hoy, sin `Initial value`, AppSheet no deja marcar `Key` en `OTID` y la tabla queda de hecho sobre
`_RowNumber`. Cuando `ORDEN-005` declare `Initial value = UNIQUEID()` y marque `Key = OTID`, **eso
es literalmente seleccionar una clave distinta para la tabla** — el escenario exacto de la cita. Las
dos referencias que ya están configuradas (miradas a ojo, no medidas) están en riesgo de romperse
justo por eso, y como su destino sigue vacío durante `PRUEBA-005` hasta el fixture (§3.4), **nadie lo
va a poder medir hasta que existan filas**. Esto se traduce en dos puntos de acción, no en una
alarma sin salida: reconfirmar a ojo las dos referencias inmediatamente después de marcar `Key`
(§6, y `PRUEBA-005` `P-09`), y correr `auditar_cableado.py` **de verdad** —con medición, no a
ojo— en cuanto el fixture de `PRUEBA-005` deje filas en `OT_OrdenesTrabajo` (`PRUEBA-005` `P-14`).
Es la única forma de que esta afirmación deje de ser "miradas a ojo" y pase a ser medida.

## 3. Qué cambia exactamente

| Tabla | Columna | Antes | Después | Nota |
|---|---|---|---|---|
| `OT_OrdenesTrabajo` | `OTID` | `Text`, `pk=True`, sin `Initial value`, en `CLAVE_LEGIBLE` | `Text`, `pk=True`, sin `Initial value` declarado en el modelo (igual que las seis de `CLAVE_GENERADA` hoy), sale de `CLAVE_LEGIBLE`, entra en `CLAVE_GENERADA` | En Fase B se declara `Initial value = UNIQUEID()` en el editor |
| `PLA_PlanMantenimiento` | `PlanID` | `Text`, `pk=True`, sin `Initial value`, en `CLAVE_LEGIBLE` | Igual tratamiento que `OTID`: sale de `CLAVE_LEGIBLE`, entra en `CLAVE_GENERADA` | Sin bot creador y sin ninguna referencia entrante (§2.2), el riesgo es menor, pero la plataforma no ofrece un tercer mecanismo distinto (§3.1) |
| `OT_OrdenesTrabajo` | `Etiqueta` (nueva, **columna VIRTUAL**, no de `MODELO`) | No existe | Virtual, `App formula` declarada como `RG-35` en `REGLAS`, `columna="(tabla)"`. Expresión: `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` | Reemplaza, para el técnico, lo que `OTID` dejaba de poder ofrecer como identificador legible. Se marca `Label` en Fase C. Ver §3.2 |
| `PLA_PlanMantenimiento` | `Etiqueta` (nueva, **columna VIRTUAL**) | No existe | Virtual, `App formula` declarada como `RG-36`. Expresión: `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` | Para operación, que hoy vería `PlanID` como identificador por defecto y dejará de poder |

### 3.1 Por qué `UNIQUEID()` y no las otras dos opciones, para ambas claves

**Opción descartada: una fórmula que componga la clave (prefijo + fecha + consecutivo).** Se
descarta por la concurrencia, y solo por eso —el agotamiento (§2.7) es un argumento secundario que
por sí solo no bastaría—. `docs/BASE_CONOCIMIENTO_APPSHEET.md`, tabla "Limitaciones arquitectónicas
de fondo": *"Offline-first: consistencia eventual. Todo contador o secuencia compite consigo
mismo."* `RG-29`, en el modelo de dominio bloqueado (`ESPEC-003`), existe explícitamente para evitar
el mismo patrón: *"la ausencia de transacciones basta por sí sola para descartar el contador
acumulado"*. Un consecutivo calculado por `Initial value` (que se evalúa en el dispositivo, no en el
servidor, §7) no tiene forma de coordinarse entre dos técnicos sin señal, ni entre el bot `RG-10` y
un técnico creando una correctiva a la vez.

**Opción descartada: que la escriba quien crea la orden a mano.** No cubre el caso que destapó esta
especificación: `RG-10` y `RG-12` crean filas sin que haya un humano tecleando nada en ese instante.
Para `PlanID` esto sería técnicamente viable —nadie más que operación crea filas en
`PLA_PlanMantenimiento`, no hay bot— pero se descarta por consistencia con la razón de fondo y
porque no hay ganancia real: nada lo compara contra un literal (§2.4) y nadie lo ve en un
desplegable (§2.2).

**Opción elegida: `UNIQUEID()`.** Lo que se pierde: la clave deja de ser legible en las dos tablas.
Es una pérdida real —es justo lo que dispara el problema del §3.2—, pero es el mecanismo que las
otras seis tablas transaccionales ya usan sin incidentes.

### 3.2 Cómo se identifica una orden ante el técnico si `OTID` deja de ser legible — el mecanismo completo, verificado

`scripts/inferencia.py:174-178` (hoy, antes de `ORDEN-005`) declara `OT_OrdenesTrabajo` en
`SIN_ETIQUETA_NATURAL` con el motivo "una orden se identifica por su número y su fecha". Ese motivo
deja de sostenerse en cuanto el número es un `UNIQUEID()`. La resolución, verificada por simulación
completa sobre una copia temporal del repositorio (no aplicada al repositorio real):

1. **`OT_OrdenesTrabajo` sale de `SIN_ETIQUETA_NATURAL`** en `scripts/inferencia.py`.
2. **Se declaran `RG-35` y `RG-36` en `REGLAS`** (§4), con `columna="(tabla)"` y `tipo="App
   formula"`, siguiendo el molde de `RG-29`. **No se añade ninguna columna a `MODELO["OT_OrdenesTrabajo"]["columnas"]`
   ni a `MODELO["PLA_PlanMantenimiento"]["columnas"]`.**
3. **`etiqueta_de()` no puede encontrar una columna virtual recorriendo `MODELO`**, porque una
   virtual no vive ahí a propósito (punto 2). Añadir `"Etiqueta"` a la tupla `ETIQUETAS` —el plan de
   la versión anterior— **no habría funcionado**: se verificó ejecutando el código, y
   `etiqueta_de('OT_OrdenesTrabajo')` seguía devolviendo `None` con ese cambio solo, porque
   `ETIQUETAS` se compara contra `MODELO[tabla]["columnas"]`, no contra `REGLAS`. La corrección real
   es un diccionario nuevo y explícito:
   ```python
   ETIQUETA_VIRTUAL = {
       "OT_OrdenesTrabajo": "Etiqueta",
       "PLA_PlanMantenimiento": "Etiqueta",
   }
   ```
   y `etiqueta_de()` lo consulta primero, antes de mirar `SIN_ETIQUETA_NATURAL` o `ETIQUETAS`. Se
   declara a mano, no se deriva de `REGLAS`, porque una `REGLA` no lleva el nombre de la columna que
   crea (`columna="(tabla)"` no dice "Etiqueta"). Verificado tras el cambio:
   ```
   OT Etiqueta
   PLA Etiqueta
   MAN None
   CHK None
   ```
4. En Fase B/C, la columna virtual `Etiqueta` se crea en *Data > Columns > Add virtual column*, con
   la expresión de `RG-35`/`RG-36`, y se marca `Label`, reemplazando la instrucción vigente de
   `docs/PROMPT_CABLEADO.md` que hoy dice "ninguna: la clave la identifica, y está decidido así".

**Verificado que no hace falta tocar la hoja en ningún punto de esta cadena.** `verificar_faseA.py`
sobre la copia simulada, con los cambios de `modelo_objetivo.py` e `inferencia.py` aplicados y **sin
regenerar la hoja**, no muestra ningún `F-02` — a diferencia de lo que habría pasado con el diseño
anterior (`App formula` sobre columna real, que si habría exigido regenerar). Los dos `F-11` de
`OT_OrdenesTrabajo`/`PLA_PlanMantenimiento` desaparecen igual, porque dependen de `CLAVE_GENERADA`,
no de `Etiqueta`. `FASE A CERRADA` en la primera corrida.

No se toca `MAN_Mantenimientos` ni `CHK_Checklists`, que también están en `SIN_ETIQUETA_NATURAL`:
sus motivos nunca prometieron que la propia clave fuera legible, y ya están en `CLAVE_GENERADA`
desde antes de esta especificación.

### 3.3 La sintaxis exacta de `Etiqueta`, verificada, con un margen que sí queda para Fase C

A diferencia de la versión anterior, `CONCATENATE()` ya no es una incógnita diferida: es la función
que la documentación oficial de Google recomienda para este caso exacto (§2.5). La expresión
propuesta:

- `OT_OrdenesTrabajo.Etiqueta` (`RG-35`): `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])`
- `PLA_PlanMantenimiento.Etiqueta` (`RG-36`): `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])`

Las dos se verificaron con `validar_modelo.py` sobre la copia simulada: `V-11` navega
`[ActivoID].[Nombre]` sin error (`ActivoID` es `Ref` a `ACT_Activos`, que tiene `Nombre`), y
`[FrecuenciaID].[Nombre]` igual contra `FRE_Frecuencias`. Lo que **sí** queda abierto para Fase C,
con el proceso existente (`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` / `docs/PROMPT_EXPRESIONES.md`),
es el detalle de presentación: el separador exacto (aquí `" - "`, provisional, mismo tratamiento que
el umbral provisional de `RG-19`) y si `FechaProgramada` necesita `TEXT()` para un formato de fecha
legible en vez del que AppSheet use por defecto al concatenar un `Date`. Eso no bloquea nada de esta
especificación: es ajuste de redacción sobre una expresión que ya resuelve, cablea y valida.

### 3.4 Ruta de reversión, escrita antes del primer paso destructivo

Ningún paso de esta especificación es destructivo mientras las dos tablas sigan vacías: declarar
`Initial value` y marcar `Key` sobre una tabla sin filas no tiene nada que perder, y se deshace
desmarcando `Key` y borrando el `Initial value`. **El primer paso irreversible es el primer
`UNIQUEID()` que se escribe en una fila real** — el primero que crea `PRUEBA-005` (§3, hallazgo de
esta versión) o el primero que crea un técnico en producción, lo que ocurra antes.

A partir de ahí:

- **Las filas que `UNIQUEID()` ya creó no se pueden convertir a una clave legible sin una migración.**
  `UNIQUEID()` no tiene relación con el orden de creación ni con el activo; no hay fórmula que derive
  `OT-0001` de una cadena aleatoria ya escrita. Revertir a clave legible después de este punto exige
  reescribir la clave de cada fila existente **y** cada `Ref` que la apunte (`MAN_Mantenimientos.OTID`,
  `OT_OrdenesTrabajo.OTOrigenID`), a mano o con un script de migración que hoy no existe.
- **Si además hace falta un `Delete and re-add the table`** —porque la estructura de columnas quedó
  en un estado que `Regenerate` no puede fusionar, el mismo escenario que ya obligó a reconstruir la
  aplicación una vez (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §11, `docs/COMUNICACION_PROPIETARIO_APP.md`)—,
  **eso solo lo puede ejecutar el propietario de la aplicación**: *"Quien crea la aplicacion es su
  propietario (...) un coautor no puede dar de alta tablas"* (`docs/MANUAL_DESPLIEGUE.md`, sección
  «Paso 1 — Crear la aplicacion» — citado por título, no por línea, porque es un documento generado y
  sus líneas se mueven: ver §8), y `Add data` está reservado a esa cuenta
  (`docs/BASE_CONOCIMIENTO_APPSHEET.md:228-229`). Hoy la
  propietaria de la hoja de producción es la Concesión (`CLAUDE.md` §2.1); quién es exactamente el
  propietario de la aplicación `_SISGA_-323965761` no está verificado desde el repositorio — hay que
  mirarlo en AppSheet, no inferirlo. `Delete and re-add` además borra toda la configuración de esa
  tabla en el editor (referencias, `Label`, `Valid_If`, filtros), y obliga a recablearla entera desde
  `RECONSTRUCCION_EXPRESIONES.md`.
- **El punto exacto en que la ventana deja de ser limpia es el primer fixture, no el fin del
  despliegue** (§1). Después de `PRUEBA-005`, `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` nunca
  vuelven a estar en `0` filas por diseño (la limpieza usa `Activo = FALSE`, no `Delete` — §6,
  `PRUEBA-005` `P-13`), así que cualquier reversión posterior a ese punto ya no es "tabla vacía, no
  cuesta nada": es una migración sobre datos reales, aunque estén marcados `TEST` e inactivos.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, salvo el punto marcado aparte:

- **`CLAVE_LEGIBLE`**: se retiran `"OT_OrdenesTrabajo"` y `"PLA_PlanMantenimiento"` del conjunto.
  Queda con 20 tablas (hoy 22).
- **`CLAVE_GENERADA`**: se añaden `"OT_OrdenesTrabajo"` y `"PLA_PlanMantenimiento"` al conjunto.
  Queda con 8 tablas (hoy 6).
- **`CLAVE_ES_LA_PALABRA`**: no se toca. Ninguna de las dos tablas está ni debe estar ahí (§2.4).
- **`REGLAS`**: se añaden dos entradas nuevas, siguiendo el molde de `RG-29`
  (`docs/sdd/ESPEC-003-modelo-de-dominio.md:985-1002`). Los identificadores `RG-35`/`RG-36` se
  eligen para no colisionar con los que `ESPEC-003` ya reserva (`RG-21` a `RG-33`, verificado con
  `grep -on "RG-[0-9]\+" docs/sdd/ESPEC-003-modelo-de-dominio.md`) ni con `RG-34`, ya aplicado en
  `scripts/modelo_objetivo.py`:
  ```python
  dict(id="RG-35", tabla="OT_OrdenesTrabajo", columna="(tabla)",
       tipo="App formula", cubre="Identificacion legible ante el tecnico",
       expresion='CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])',
       descripcion="Etiqueta, columna VIRTUAL (no en MODELO: F-02 no la exige, no toca la hoja). "
                   "Reemplaza a OTID como Label ahora que OTID es UNIQUEID()."),
  dict(id="RG-36", tabla="PLA_PlanMantenimiento", columna="(tabla)",
       tipo="App formula", cubre="Identificacion legible ante operacion",
       expresion='CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])',
       descripcion="Etiqueta, columna VIRTUAL. Mismo mecanismo que RG-35."),
  ```
  **No se añade ninguna columna a `MODELO["OT_OrdenesTrabajo"]["columnas"]` ni a
  `MODELO["PLA_PlanMantenimiento"]["columnas"]`.** Esta es la diferencia central con la versión
  bloqueada, y la que resuelve el hallazgo de diseño del arquitecto (§2.5).
- **`RENOMBRADOS`, `CAMPOS_RETIRADOS`, `RETIRADAS`**: no se tocan. No hay renombre, ni retiro de
  columna, ni tabla que se retire.

**Fuera de `scripts/modelo_objetivo.py`, un cambio necesario y declarado aparte a propósito:**
`scripts/inferencia.py`:
- `SIN_ETIQUETA_NATURAL`: se retira `"OT_OrdenesTrabajo"`.
- Se añade un diccionario nuevo, `ETIQUETA_VIRTUAL = {"OT_OrdenesTrabajo": "Etiqueta",
  "PLA_PlanMantenimiento": "Etiqueta"}`.
- `etiqueta_de()` consulta `ETIQUETA_VIRTUAL` antes que `SIN_ETIQUETA_NATURAL` o `ETIQUETAS` (§3.2).
- **No se toca `ETIQUETAS`.** El plan de la versión anterior —añadir `"Etiqueta"` a esa tupla— se
  verificó por ejecución y no funciona para una columna virtual (§3.2, punto 3): se corrige aquí en
  vez de repetirse.

No es `modelo_objetivo.py` porque la etiqueta de una columna nunca vivió ahí: vive en
`scripts/inferencia.py` desde que ese archivo se creó.

## 5. Qué NO cubre esta especificación

- **El separador exacto y el formato de fecha de `Etiqueta`.** Se deja para Fase C (§3.3), con el
  proceso que ya existe. Costaría poco añadirlo después: es un ajuste de redacción sobre una
  expresión que ya resuelve, cablea y valida.
- **Corregir `docs/ROADMAP.md` §4.5.** Ya no hace falta: se verificó hoy (§2.6) que ya está
  corregido, fuera de esta especificación.
- **Si `RG-12` se activa.** Sigue bloqueado por el plan gratuito (D-B), independientemente de que
  esta especificación resuelva quién genera `PlanID`.
- **Renumerar o citar `OT-0001` en ningún reporte u oficio existente.** No hay ninguno: las ocho
  tablas están vacías (§2.1).
- **`MAN_Mantenimientos.OTID` y `OT_OrdenesTrabajo.OTOrigenID`** siguen siendo `Ref` a
  `OT_OrdenesTrabajo` sin ningún cambio de declaración: guardan la clave del destino (`UNIQUEID()`
  en vez de `OT-0001`). Lo que sí cubre esta especificación es el riesgo de que el cambio de clave
  rompa su configuración ya puesta en el editor (§2.8, §6) — eso se verifica, no se redeclara.
- **Añadir `Etiqueta` a `docs/BASE_CONOCIMIENTO_APPSHEET.md` como entrada sobre `Label`.** La cita de
  Google que resuelve §2.5 se usa aquí, pero incorporarla como entrada permanente de esa base de
  conocimiento es un cambio de otro documento, fuera de esta especificación, y va por la vía rápida
  del §6 del pipeline si alguien lo considera necesario.
- **Corregir el mensaje genérico de `docs/PROMPT_EXPRESIONES.md`** ("`App formula` (...) escribe en
  la hoja"), que deja de ser universalmente cierto en cuanto existen `App formula` sobre columnas
  virtuales. Verificado por simulación: `RG-35` y `RG-36` aparecen bajo esa afirmación general aunque
  no escriban nada. Se deja anotado como hallazgo en §6, no se corrige aquí: es una frase de un
  generador, y su descripción individual de `RG-35`/`RG-36` ya aclara que son virtuales.

## 6. Riesgos y dependencias

- **Orden dentro de Fase B.** `Initial value` se declara antes de marcar `Key`, no al revés. Si el
  ejecutor invierte el orden sobre estas dos tablas nuevas, reproduce el mismo síntoma que abrió esta
  especificación (`_RowNumber` como clave).
- **`RG-10` es un riesgo prospectivo, no uno ya activo hoy** (corregido frente a la versión anterior,
  que lo daba por "vivo"). `ESTADO.md:56` es explícito: `RG-10` **no está cableado** —no se puede
  poner en el editor mientras esta especificación no se resuelva—. El riesgo se activa el día que,
  después de `ORDEN-005`, alguien configure `RG-10` en `Automation > Bots` y un técnico marque una
  segunda visita antes de que esa configuración exista. No antes.
- **Cambiar la clave de `OT_OrdenesTrabajo` puede romper las dos referencias que ya están
  configuradas en el editor** (§2.8). Es un riesgo verificado, no hipotético: `auditar_cableado.py`
  confirma hoy que `MAN_Mantenimientos.OTID` y `OT_OrdenesTrabajo.OTOrigenID` ya se miraron y
  configuraron el 2026-08-10, antes de que `OTID` tenga su `Initial value`. Después de marcar `Key`
  en Fase B, hay que **reabrir esas dos columnas en el editor y reconfirmar a ojo que `Source table`
  sigue siendo `OT_OrdenesTrabajo`** (no hay forma de medirlo por API mientras la tabla siga vacía).
  En cuanto `PRUEBA-005` deje filas reales en `OT_OrdenesTrabajo`, correr `auditar_cableado.py` de
  verdad para convertir esa confirmación visual en una medición.
- **`RG-05` (Security Filter sobre `OT_OrdenesTrabajo`) no puede estar aplicado mientras dure esta
  tanda, y eso no es una preferencia de orden: es la única forma de que la medición de arriba pueda
  hacerse alguna vez.** `scripts/lectura_de_vuelta.py` (`FILTROS_AL_FINAL`) documenta, con el
  precedente ya ocurrido de `RG-04` sobre `ACT_Activos`, que un `Security Filter` se evalúa con
  `USEREMAIL()` en blanco cuando la API llama sin usuario, y la API pasa a devolver **cero filas** de
  esa tabla — no porque estén filtradas por error, sino porque el filtro hace exactamente su trabajo
  también contra el instrumento de lectura. En cuanto `RG-05` se ponga en el editor,
  `auditar_cableado.py` deja de poder ver `OT_OrdenesTrabajo` y las dos referencias que la apuntan
  (`MAN_Mantenimientos.OTID`, `OT_OrdenesTrabajo.OTOrigenID`) vuelven a caer en "NO SE PUEDEN JUZGAR"
  — **para siempre**, no de forma temporal: no hay ventana posterior en la que la API vuelva a ver
  esa tabla sin usuario. `ESTADO.md` ya fija que los dos `Security Filter` (`RG-04` y `RG-05`) "van
  los últimos", después de todo lo demás, precisamente por esto. **`P-14` de `PRUEBA-005` es, por lo
  tanto, la única oportunidad que va a existir de medir esas dos referencias**: antes de `ORDEN-005`
  no hay filas que medir (§2.8), y después de aplicar `RG-05` no hay instrumento que pueda volver a
  mirar. Si `P-14` se salta o se corre después de aplicar `RG-05`, esas dos referencias quedan
  confirmadas solo "a ojo" —como hoy— de manera permanente.
- **`RG-07` (bot, `OT_OrdenesTrabajo`, evento `Adds`, notifica por correo al técnico) dispara con
  cada fila nueva, la cree un técnico o un bot.** No está mencionado en ninguna versión anterior de
  esta especificación ni de `PRUEBA-005`, y **cualquier fixture de prueba que cree filas en
  `OT_OrdenesTrabajo` —incluida la orden que crea `RG-10` al probarse— dispara un correo real** a la
  dirección corporativa del técnico asignado, con el asunto de una orden marcada `TEST`. Es reversible:
  *"You can disable the bot to temporarily stop the automation. Then, re-enable it"* — [Bots: The
  Essentials](https://support.google.com/appsheet/answer/11432969?hl=en), AppSheet Help. `RG-07`
  debe desactivarse (`Automation > Bots` → seleccionar → `Disable`) antes de crear la primera orden
  de prueba, y reactivarse al cerrar el fixture. Ver `PRUEBA-005`, precondición común de la Familia B
  y `P-13`.
- **La ventana barata se cierra con el primer fixture, no al final del despliegue** (§1, §3.4). A
  partir de la primera fila que cree `PRUEBA-005`, `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento`
  dejan de estar vacías **para siempre**, porque la limpieza del fixture usa `Activo = FALSE` y no
  `Delete` (punto siguiente). Cualquier especificación futura que toque la estructura de estas dos
  tablas ya no puede argumentar que corregirlas no cuesta nada.
- **La limpieza del fixture no puede usar `Delete`.** `RG-14` y `RG-15` retiran `Deletes` de
  `OT_OrdenesTrabajo` y `MAN_Mantenimientos` precisamente porque el histórico no se borra —"se anula
  con `Activo = FALSE`, que deja traza de que existió"—, y `scripts/appsheet_api.py` expone `Delete`
  sin esa protección: su propia cabecera dice *"expone Delete contra datos de produccion, y la regla
  del proyecto es que el historico no se borra. Antes de usarlo, decidir si se queda"*, una decisión
  que sigue sin tomarse. `PRUEBA-005` no toma esa decisión por esta especificación: **evita el
  problema entero usando solo `Action: Edit` con `Activo = FALSE`**, nunca `Delete`, sobre las filas
  de prueba (`OT_OrdenesTrabajo`, `MAN_Mantenimientos` y `PLA_PlanMantenimiento`, las tres con columna
  `Activo`). `PLA_PlanMantenimiento` no tiene ninguna columna de texto libre para marcar `TEST` (no
  tiene `Observaciones`), así que su fila de prueba se identifica por el `UNIQUEID()` que devuelve el
  `diff` de `instantanea.py` entre el guardado inmediatamente anterior y el inmediatamente posterior
  a crearla —no por ser "la única fila que existe", que deja de ser cierto si algo falla a mitad de
  la tanda.
- **Depende de que `docs/PROMPT_CABLEADO.md`, `docs/MANUAL_DESPLIEGUE.md`,
  `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` y `docs/PROMPT_EXPRESIONES.md` se regeneren** después de
  este cambio, o seguirán describiendo un modelo que ya cambió. Es autoejecutable —son generados, no
  se editan a mano— pero solo si alguien corre el comando; queda para la orden de ejecución.
- **El mensaje genérico "`App formula` (...) escribe en la hoja" de `docs/PROMPT_EXPRESIONES.md`
  deja de ser cierto para `RG-35`/`RG-36`.** No es un defecto que bloquee nada —la descripción
  individual de cada regla generada sí aclara que son columnas virtuales, verificado en §2.5—, pero
  quien ejecute Fase C debe leer la descripción de cada regla, no solo la tabla general de "dónde
  está cada cosa en el editor".

## 7. Supuestos adoptados

1. **Que AppSheet evalúa el `Initial value` de una columna también cuando la fila la crea un bot
   (`RG-10`, `RG-12`), igual que cuando la crea un formulario de usuario.** No hay una cita verificada
   de esto en `docs/BASE_CONOCIMIENTO_APPSHEET.md`. Se adopta como supuesto porque (a) es el
   comportamiento que `docs/PROMPT_CABLEADO.md` ya asume para las seis tablas de `CLAVE_GENERADA`
   sin que nadie lo haya cuestionado, y (b) la documentación oficial dice que el `Initial value` "se
   asigna una vez, al crear el registro" sin distinguir el origen de esa creación. Si resulta falso,
   es el riesgo más caro de esta especificación (§6).
2. **Que `UNIQUEID()` no colisiona entre dos dispositivos sin conexión.** `docs/BASE_CONOCIMIENTO_APPSHEET.md`
   lo declara expresamente sin verificar contra la fuente oficial. Se adopta igual porque, de las tres
   opciones evaluadas en §3.1, es la única sin un modo de fallo ya documentado en este proyecto.
3. **Que "operación" no comparte el perfil de concurrencia offline de un técnico de campo.** Sale
   del enunciado de este encargo, no de un conteo verificado de usuarios ni de dispositivos.
4. **El nombre de columna `Etiqueta`.** No había convención previa para una columna de este tipo en
   una tabla transaccional. Se adopta porque no colisiona con ningún nombre existente
   (`grep -n '"Etiqueta"' scripts/modelo_objetivo.py` no devuelve nada) y describe sin ambigüedad su
   propósito.
5. **Que basta con dos referencias para decidir que `OT_OrdenesTrabajo` necesita una `Etiqueta`
   explícita con más urgencia que `PLA_PlanMantenimiento`, con cero.** Se adopta como criterio de
   priorización, no como regla general: las dos reciben la misma columna `Etiqueta` de todas formas.
6. **El separador `" - "` y el formato sin `TEXT()` de `FechaProgramada` en `RG-35`, y de `RG-36`
   sin ajuste adicional.** Es una expresión de trabajo, válida y verificada contra `V-11`, pero su
   presentación final se cierra en Fase C con `RECONSTRUCCION_EXPRESIONES.md` (§3.3). No es una
   incógnita sin verificar como `Label`+virtual (§2.5): es un detalle de redacción pendiente de
   pulir, no una pregunta abierta sobre si el mecanismo funciona.

**Lo que ya no es un supuesto en esta versión:** que una columna virtual pueda ser `Label`. Se
verificó contra la documentación oficial de Google (§2.5) y se retira de la lista de incógnitas.

## 8. Nota de método: cómo se cita este documento a `docs/PROMPT_CABLEADO.md`

`docs/PROMPT_CABLEADO.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, `docs/PROMPT_EXPRESIONES.md` y
**`docs/MANUAL_DESPLIEGUE.md`** son **generados**: sus números de línea se mueven cada vez que el
modelo cambia, y sus números de paso se derivan de recuentos (`len(REGLAS)`, `len(SIN_ETIQUETA_NATURAL)`,
etc.) que también cambian. `docs/MANUAL_DESPLIEGUE.md` lo genera `scripts/generar_manual_despliegue.py`
igual que los otros tres se generan por su script correspondiente; se añade a esta lista en esta misma
versión porque §3.4 lo citaba por línea (`:174-175`) y esa cita ya se corrigió a título de sección
(«Paso 1 — Crear la aplicacion»). Toda cita a estos cuatro documentos en esta especificación se hace
**por título de sección**, nunca por número de línea. Donde la versión anterior citaba líneas (76-78,
80-87, 372-393), esas líneas ya no corresponden a lo citado —verificado hoy: la cita textual del §1
existe, pero en otra línea y dentro de otro paso ("Paso 2", no "Paso 1")—. El contenido citado se
revisó contra el archivo actual en cada punto de este documento; el número de línea nunca se usó como
identificador.
