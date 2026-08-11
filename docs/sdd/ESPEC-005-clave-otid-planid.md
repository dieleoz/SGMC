# ESPEC-005 — Generador de `OTID` y `PlanID`, y su etiqueta ante el técnico

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

De los dos bots, uno ya es un riesgo activo hoy y no uno teórico: `RG-10` es un bot por evento (tipo
`Bot`, no `Bot programado`), y los bots por evento sí corren en el plan gratuito. Lo que no corre son
los programados (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §6), y `RG-12` lo dice en su propia
descripción: "REQUIERE PLAN PAGADO". En cuanto la aplicación esté desplegada y un técnico marque
una segunda visita, `RG-10` intentará crear la orden y fallará en silencio si esta especificación no
se resuelve antes.

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
para lo que se le pediría.** `docs/PROMPT_CABLEADO.md` (líneas 76-78) ya documenta, para las seis
tablas de `CLAVE_GENERADA`, que basta con declarar `Initial value = UNIQUEID()` **sobre la tabla
vacía** para que AppSheet deje marcar `Key`: "AppSheet no te va a dejar marcar `Key` sin más. Sobre
una tabla vacía exige que la columna tenga un `Initial value` que genere la clave (...) así que
primero el valor, después la casilla." Esto ya se sigue con seis tablas sin necesitar una sola fila
de datos. Extender el mismo mecanismo a `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` (§3) logra lo
mismo sin sembrar nada y sin ninguno de los dos costos de arriba. No hay una forma acotada de
sembrar que valga la pena: la alternativa sin sembrar ya funciona y ya está en uso.

## 2. Estado actual verificado

Todo lo siguiente se leyó de `scripts/modelo_objetivo.py` (el modelo, fuente única) y de
`BD/Modelo_Datos_PLANTILLA.xlsx` (el volcado local). Según `python scripts/sistema.py`, ese volcado
es hoy el mismo archivo que corre en producción (`Modelo_Datos_10082026`) mientras nadie edite el
Sheets directamente; no se leyó el Sheets de producción en esta especificación.

### 2.1 Las ocho tablas están vacías hoy, en el volcado local

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
Salida: las ocho en `0`. Coincide con `BD/instantaneas/antes-de-fase-c.json`, que registra el mismo
`0` para las mismas ocho tablas.

### 2.2 `python scripts/validar_modelo.py` hoy

```
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
que decidir, en vez de resolverlo con datos que no existen.

### 2.4 Ningún `Ref`, `valid_if`, `formula` ni `valor_inicial` del modelo compara `OTID` o `PlanID`
contra un literal

```
grep -n '\[OTID\]\|"OT-\|OT-0001\|\[PlanID\]\|"PLA-' scripts/modelo_objetivo.py
```
Las únicas apariciones de `[OTID]` son dereferencias (`[OTID].[ActivoID]...`, dos veces, en `RG-01`
y en el `valid_if` de `Coordenadas_Cierre_LatLong`), y una nota de comentario. `PlanID` no aparece
comparado contra nada. `validar_modelo.py` (V-17, líneas 175-224) solo dispara sobre patrones del
tipo `[Columna] = "literal"` con la columna **sin** un punto después —una dereferencia como
`[OTID].[ActivoID]` queda excluida por el `(?!\s*\.\s*\[)` de la propia expresión regular—. Es
decir: **hoy nada se rompe en `validar_modelo.py` si `OTID` deja de ser legible**, porque nada lo
compara como si lo fuera.

Aparte, `RG-08` (`AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`) compara
`[EstadoOrdenID].[EsFinal]`, no `[EstadoOrdenID]` a secas ni `[OTID]`. Es una dereferencia sobre
`EOT_EstadosOrden` —que sí está en `CLAVE_ES_LA_PALABRA`, y ahí es legítimo comparar contra un
literal ("Cerrada", "Asignada")—, y no toca en absoluto la legibilidad de `OTID`. Se verificó para
no confundir las dos listas: `CLAVE_LEGIBLE` (`scripts/modelo_objetivo.py:816-847`, cómo se ve la
clave) y `CLAVE_ES_LA_PALABRA` (`scripts/modelo_objetivo.py:882-884`, contra cuáles literales es
legítimo comparar) son listas distintas a propósito, y hoy contienen: `CLAVE_ES_LA_PALABRA =
{EOT_EstadosOrden, FRM_Formularios, PAR_Parametros, SEN_Sentidos}` — ni `OT_OrdenesTrabajo` ni
`PLA_PlanMantenimiento` están ahí, así que esta especificación no toca esa lista.

### 2.5 `SIN_ETIQUETA_NATURAL` y la etiqueta de las tablas destino de referencia

```
python -c "
import sys; sys.path.insert(0,'scripts')
from inferencia import etiquetas_pendientes
for t,e,n in etiquetas_pendientes(): print(t,e,n)
"
```
Salida (extracto relevante):
```
MAN_Mantenimientos None 3
OT_OrdenesTrabajo None 2
CHK_Checklists None 1
```
`OT_OrdenesTrabajo` es destino de 2 referencias y no tiene columna de etiqueta: hoy AppSheet usaría
la propia clave como `Label` por defecto (`scripts/inferencia.py:153-168`), y
`scripts/inferencia.py:174-178` lo declara a propósito en `SIN_ETIQUETA_NATURAL`, con el motivo "una
orden se identifica por su número y su fecha". Ese motivo asume que el número (`OTID`) es legible.
`docs/PROMPT_CABLEADO.md` (líneas 372-393, el paso de `Label`) lo confirma como instrucción vigente:
para `OT_OrdenesTrabajo` dice literalmente "ninguna: la clave la identifica, y está decidido así".
`PLA_PlanMantenimiento` no está en `SIN_ETIQUETA_NATURAL` ni en la tabla de `Label` de
`PROMPT_CABLEADO.md`, porque no es destino de ninguna referencia (§2.2): nadie la selecciona en un
desplegable hoy.

### 2.6 Un hallazgo cruzado: `ROADMAP.md` y el modelo no dicen lo mismo sobre `Adds` en `OT_OrdenesTrabajo`

`scripts/modelo_objetivo.py` declara `RG-14` como `tabla="OT_OrdenesTrabajo"`, `expresion="Updates,
Adds"` (línea 1212-1216), sin condición. `docs/MANUAL_DESPLIEGUE.md` y `docs/PROMPT_CABLEADO.md`,
ambos generados de ese mismo modelo, instruyen `Adds sí` para `OT_OrdenesTrabajo`.

`docs/ROADMAP.md` §4.5 (editado el 2026-08-10, más tarde que el último cambio a
`scripts/modelo_objetivo.py` según la fecha del archivo) dice lo contrario, en una tabla que el
propio documento declara cerrada y no reabierta: *"Creación de órdenes desde la app — Aplazada, no
descartada. `OT_OrdenesTrabajo` no admite `Adds` mientras `OTID` haga de clave y de etiqueta legible
a la vez."* Y `docs/MODELO_EVOLUCION_FASE_2.md` (documento marcado "Propuesta", no vigente) repite la
misma idea: "si el piloto incluye correctivo, CU-02 deja de estar diferido y `OT_OrdenesTrabajo`
necesita `Adds`. Hoy está aplazado."

Según el propio `docs/SDD_PIPELINE_SGMC.md`, "cuando una especificación y `modelo_objetivo.py`
discrepan, manda el modelo": `RG-14` es lo vigente, y `ROADMAP.md` está desactualizado en ese punto.
No es una contradicción activa sobre la aplicación en vivo —`docs/PROMPT_CABLEADO.md` ordena resolver
primero la clave (su Paso 1, líneas 76-96, "Y estas 2, PARA") y solo después llegar al paso de
`Are updates allowed`, así que en la práctica nadie llega a habilitar `Adds` sobre `OT_OrdenesTrabajo`
sin pasar antes por el bloqueo que esta especificación resuelve—, pero si esta especificación se
aplica y nadie corrige `ROADMAP.md`, ese documento seguirá afirmando que la creación de órdenes desde
la app sigue aplazada cuando ya no lo estará. Se deja dicho aquí porque **es exactamente el patrón
que este proyecto ya pagó una vez** (documentos que describen otro documento y no el archivo), y la
corrección de `ROADMAP.md` es una corrección de redacción que va por la vía rápida del §6 del
pipeline, no por esta especificación.

### 2.7 Escala: por qué una convención de 4 dígitos no resiste, aparte de la concurrencia

```
python scripts/capacidad.py
```
El escenario "Hoy" del script está desactualizado: declara 34 activos (`scripts/capacidad.py:16`),
y `ACT_Activos` tiene hoy 368 filas pobladas —misma consulta del §2.1, aplicada a `ACT_Activos` en
vez de a las ocho tablas vacías—. Se deja como hallazgo aparte; no se corrige en esta especificación,
que no toca `scripts/capacidad.py`. El escenario más cercano a 368 activos es "Plan Maestro" (355 activos):
5.112 mantenimientos/año, y por tanto una `OT_OrdenesTrabajo` de **25.560 filas a 5 años**. Una
clave `OT-0001` de 4 dígitos agota su rango (9.999) en menos de 2 años a ese ritmo. Esto es
independiente del problema de concurrencia del §3: aunque no hubiera dos dispositivos escribiendo a
la vez, un contador de ancho fijo tiene fecha de caducidad calculable, y ninguna de las tres
opciones de generación evaluadas la evita salvo dejar de ser legible.

## 3. Qué cambia exactamente

| Tabla | Columna | Antes | Después | Nota |
|---|---|---|---|---|
| `OT_OrdenesTrabajo` | `OTID` | `Text`, `pk=True`, sin `Initial value`, en `CLAVE_LEGIBLE` | `Text`, `pk=True`, sin `Initial value` declarado en el modelo (igual que las seis de `CLAVE_GENERADA` hoy), sale de `CLAVE_LEGIBLE`, entra en `CLAVE_GENERADA` | En Fase B se declara `Initial value = UNIQUEID()` en el editor, siguiendo el mismo mecanismo ya usado para las seis tablas de `CLAVE_GENERADA` (`docs/PROMPT_CABLEADO.md` líneas 80-87) |
| `PLA_PlanMantenimiento` | `PlanID` | `Text`, `pk=True`, sin `Initial value`, en `CLAVE_LEGIBLE` | Igual tratamiento que `OTID`: sale de `CLAVE_LEGIBLE`, entra en `CLAVE_GENERADA` | Sin bot creador y sin ninguna referencia entrante (§2.2), el riesgo es menor, pero la plataforma no ofrece un tercer mecanismo distinto para generarla (§3.1) |
| `OT_OrdenesTrabajo` | `Etiqueta` (nueva) | No existe | `Text`, columna nueva, `formula` (App formula) que compone un texto identificable a partir de `[ActivoID].[Nombre]` y `[FechaProgramada]` | Reemplaza, para el técnico, lo que `OTID` dejaba de poder ofrecer como identificador legible. Ver §3.2 |
| `PLA_PlanMantenimiento` | `Etiqueta` (nueva) | No existe | `Text`, columna nueva, `formula` que compone un texto identificable a partir de `[ActivoID].[Nombre]` y `[FrecuenciaID].[Nombre]` | Para operación, que hoy vería `PlanID` como identificador por defecto y dejará de poder |

### 3.1 Por qué `UNIQUEID()` y no las otras dos opciones, para ambas claves

**Opción descartada: una fórmula que componga la clave (prefijo + fecha + consecutivo).** Se
descarta por dos razones ya documentadas en este mismo proyecto, no por una preferencia nueva:

- **Concurrencia.** `docs/BASE_CONOCIMIENTO_APPSHEET.md`, tabla "Limitaciones arquitectónicas de
  fondo": *"Offline-first: consistencia eventual. Todo contador o secuencia compite consigo mismo.
  Es la razón de que `OT_OrdenesTrabajo` perdiera `Adds`"* (esa frase concreta está superada, §2.6,
  pero la razón de fondo —consistencia eventual sin transacciones— no lo está). `RG-29`, en el
  modelo de dominio bloqueado (`ESPEC-003`), existe explícitamente para evitar el mismo patrón:
  *"la ausencia de transacciones basta por sí sola para descartar el contador acumulado"*. Un
  consecutivo calculado por `Initial value` (que se evalúa en el dispositivo, no en el servidor,
  §7) no tiene forma de coordinarse entre dos técnicos sin señal, ni entre el bot `RG-10` y un
  técnico creando una correctiva a la vez.
- **Techo de escala.** §2.7: un consecutivo de ancho fijo agota su rango en menos de dos años al
  ritmo del inventario actual, y ensancharlo no resuelve la concurrencia, solo pospone el problema.

**Opción descartada: que la escriba quien crea la orden a mano.** No cubre el caso que destapó esta
especificación: `RG-10` (bot por evento, ya elegible en el plan gratuito) y `RG-12` (bot programado)
crean filas sin que haya un humano tecleando nada en ese instante. Una solución que dependa de que
alguien escriba el valor deja a los dos bots exactamente donde están hoy: creando filas sin clave.
Para `PlanID` esto sería técnicamente viable —nadie más que operación crea filas en
`PLA_PlanMantenimiento`, no hay bot— pero se descarta por consistencia con la razón de fondo
(consistencia eventual sin transacciones) y porque no hay ganancia real: nada lo compara contra un
literal (§2.4) y nadie lo ve en un desplegable (§2.2), así que la legibilidad de `PlanID` no paga
por sí sola el riesgo de un contador manual.

**Opción elegida: `UNIQUEID()`.** Lo que se pierde: la clave deja de ser legible en las dos tablas.
Es una pérdida real y no gratis —es justo lo que dispara el problema del §3.2—, pero es la única de
las tres que no tiene ya un modo de fallo documentado en este proyecto, y es el mecanismo que las
otras seis tablas transaccionales ya usan sin incidentes, verificado en `scripts/modelo_objetivo.py`
(`CLAVE_GENERADA`, líneas 886-893) y en `docs/PROMPT_CABLEADO.md` (líneas 80-87).

### 3.2 Cómo se identifica una orden ante el técnico si `OTID` deja de ser legible

`scripts/inferencia.py:174-178` declara `OT_OrdenesTrabajo` en `SIN_ETIQUETA_NATURAL` con el motivo
"una orden se identifica por su número y su fecha". Ese motivo deja de sostenerse en cuanto el
número es un `UNIQUEID()`. La resolución propuesta:

1. `OT_OrdenesTrabajo` sale de `SIN_ETIQUETA_NATURAL` en `scripts/inferencia.py`.
2. Se añade la columna `Etiqueta` (§3, tabla) a `OT_OrdenesTrabajo` en `MODELO`, con una `App
   formula` que combine el nombre del activo y la fecha programada — la misma idea que sostenía el
   motivo retirado ("su número y su fecha"), sustituyendo el número por el activo, que es lo que de
   verdad identifica una orden para quien la mira en una lista.
3. `ETIQUETAS` en `scripts/inferencia.py` (línea 169, hoy `("Nombre", "Nombres", "Pregunta",
   "Descripcion")`) gana un quinto nombre, `"Etiqueta"`, para que `etiqueta_de()` la reconozca sin
   necesitar un caso especial por tabla. Se verificó que ninguna de las 28 tablas usa hoy ese nombre
   de columna (`grep -n '"Etiqueta"' scripts/modelo_objetivo.py` no devuelve nada), así que añadirlo
   no reclasifica ninguna columna existente.
4. En Fase B/C, la columna `Etiqueta` se marca `Label` en el editor, reemplazando la instrucción
   vigente de `docs/PROMPT_CABLEADO.md` (línea 381) que hoy dice "ninguna: la clave la identifica".
   `PLA_PlanMantenimiento` gana su propia `Etiqueta` por el mismo mecanismo, sin necesitar tocar
   `SIN_ETIQUETA_NATURAL` porque nunca estuvo declarada ahí (§2.2): es un vacío no declarado, no una
   decisión que se reabra.

No se toca `MAN_Mantenimientos` ni `CHK_Checklists`, que también están en `SIN_ETIQUETA_NATURAL`:
sus motivos ("se identifica por su orden y su hora", "se identifica por su mantenimiento") nunca
prometieron que la propia clave fuera legible —las dos ya están en `CLAVE_GENERADA` desde antes de
esta especificación—, así que no hay nada que corregir ahí.

### 3.3 La sintaxis exacta de `Etiqueta` no se cierra aquí

Esta especificación describe **qué** debe componer la fórmula, no la escribe carácter por carácter
contra el editor en vivo. `docs/BASE_CONOCIMIENTO_APPSHEET.md` no tiene una entrada verificada sobre
la sintaxis exacta de concatenación de texto en AppSheet, y el propio proyecto ya tiene un proceso
para esto —`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` y `docs/PROMPT_EXPRESIONES.md`, que reconstruyen
cada expresión "sin cortar" contra la aplicación real—. La expresión final de `Etiqueta` se cierra
en esa misma Fase C, no en esta especificación (ver §5 y §7).

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, salvo el punto marcado aparte:

- **`CLAVE_LEGIBLE`** (líneas 816-847): se retiran `"OT_OrdenesTrabajo"` y
  `"PLA_PlanMantenimiento"` del conjunto.
- **`CLAVE_GENERADA`** (líneas 886-893): se añaden `"OT_OrdenesTrabajo"` y
  `"PLA_PlanMantenimiento"` al conjunto. Queda con ocho tablas en vez de seis.
- **`CLAVE_ES_LA_PALABRA`**: no se toca. Ninguna de las dos tablas está ni debe estar ahí (§2.4).
- **`MODELO["OT_OrdenesTrabajo"]["columnas"]`**: se añade `col("Etiqueta", "Text", formula=<pendiente
  de Fase C>, nueva=True, nota="Identifica la orden ante el técnico ahora que OTID es UNIQUEID();
  compone activo y fecha programada")`, después de `EstadoOrdenID` y antes de `OTOrigenID` (por
  legibilidad del bloque, no por dependencia).
- **`MODELO["PLA_PlanMantenimiento"]["columnas"]`**: se añade `col("Etiqueta", "Text",
  formula=<pendiente de Fase C>, nueva=True, nota="Identifica el plan ante operación; compone activo
  y frecuencia")`.
- **`RETIPADOS`, `RENOMBRADOS`, `CAMPOS_RETIRADOS`, `RETIRADAS`, `REGLAS`**: no se tocan. No hay
  renombre, ni retiro de columna, ni tabla que se retire, y no hace falta una `REGLA` nueva: el
  `Initial value = UNIQUEID()` de las seis tablas de `CLAVE_GENERADA` tampoco está declarado como
  `REGLA` — vive en la pertenencia al conjunto y se documenta en `docs/PROMPT_CABLEADO.md` y
  `docs/MANUAL_DESPLIEGUE.md`, generados de ese mismo conjunto. Extender `OT_OrdenesTrabajo` y
  `PLA_PlanMantenimiento` a `CLAVE_GENERADA` basta para que esos dos documentos, al regenerarse,
  incluyan las dos tablas en su tabla de "Clave automática para las filas nuevas" sin más cambios.

**Fuera de `scripts/modelo_objetivo.py`, un cambio necesario y declarado aparte a propósito:**
`scripts/inferencia.py` — `SIN_ETIQUETA_NATURAL` (retirar `"OT_OrdenesTrabajo"`) y `ETIQUETAS`
(añadir `"Etiqueta"`). No es `modelo_objetivo.py` porque la etiqueta de una columna nunca vivió ahí:
vive en `scripts/inferencia.py` desde que ese archivo se creó, para las mismas 20 tablas destino de
referencia (§2.2 de este documento, y el docstring del propio archivo). Tratar esto como "cambio de
diseño que se edita solo en modelo_objetivo.py" sería inventar una regla que el repositorio no tiene:
la pertenencia declarada hoy es que `inferencia.py` consume `MODELO` y decide la etiqueta, no que
`modelo_objetivo.py` decida la etiqueta directamente.

## 5. Qué NO cubre esta especificación

- **La sintaxis exacta de la fórmula `Etiqueta`.** Se deja para Fase C, con el mismo proceso que ya
  existe (`RECONSTRUCCION_EXPRESIONES.md` / `PROMPT_EXPRESIONES.md`). Costaría poco añadirlo después:
  es una fórmula de columna nueva sobre una tabla vacía, sin datos que migrar.
- **Corregir `docs/ROADMAP.md` §4.5** (§2.6). Es una corrección de redacción sobre un documento, no
  toca el Sheets, el editor ni `modelo_objetivo.py`, así que va por la vía rápida del §6 del
  pipeline, no por esta especificación ni por el arquitecto. Costaría una frase.
- **Si `RG-12` se activa.** Sigue bloqueado por el plan gratuito (D-B), independientemente de que
  esta especificación resuelva quién genera `OTID`. El día que se contrate el plan pagado, `RG-12`
  empezará a crear filas usando el mismo `UNIQUEID()` que esta especificación deja declarado; no hace
  falta volver a decidir nada.
- **Renumerar o citar `OT-0001` en ningún reporte u oficio existente.** No hay ninguno: las ocho
  tablas están vacías (§2.1). Si algún documento de otro frente cita esa convención como ejemplo, no
  se toca aquí.
- **`MAN_Mantenimientos.OTID` y `OT_OrdenesTrabajo.OTOrigenID`** siguen siendo `Ref` a
  `OT_OrdenesTrabajo` sin ningún cambio: guardan la clave del destino (`UNIQUEID()` en vez de
  `OT-0001`), que es exactamente el comportamiento que `docs/BASE_CONOCIMIENTO_APPSHEET.md` §1
  documenta para un `Ref`. No hay nada que redeclarar en las referencias.
- **El resto de las 17 tablas de `LABEL... ABIERTO`** que cita `ESTADO.md`. Esta especificación
  resuelve la etiqueta de `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` porque nace del mismo
  problema de clave; las demás son un frente aparte, ya cubierto por el paso de `Label` de
  `docs/PROMPT_CABLEADO.md`.

## 6. Riesgos y dependencias

- **Orden dentro de Fase B.** `Initial value` se declara antes de marcar `Key`, no al revés — es el
  mismo orden que ya usan las seis tablas de `CLAVE_GENERADA`, y `docs/PROMPT_CABLEADO.md` ya lo dice
  explícitamente ("primero el valor, después la casilla"). Si el ejecutor invierte el orden sobre
  estas dos tablas nuevas, reproduce el mismo síntoma que abrió esta especificación (`_RowNumber`
  como clave).
- **`RG-10` es un riesgo vivo, no solo documentado.** Es un bot por evento, elegible en el plan
  gratuito. Si la aplicación se despliega y algún técnico marca `RequiereSegundaVisita = TRUE` antes
  de que `OTID` tenga `Initial value = UNIQUEID()` declarado en el editor, el bot crea una fila sin
  clave y AppSheet la descarta sin avisar — la orden de seguimiento simplemente no existe y nadie lo
  sabe hasta que alguien busque una orden que debería estar.
- **Supuesto no verificado sobre bots (§7) es el punto más frágil de esta especificación.** Si
  `Initial value` no se aplicara cuando un bot añade una fila —solo cuando la añade un formulario de
  usuario—, entonces declarar `UNIQUEID()` en el editor no bastaría para `RG-10` ni `RG-12`, y haría
  falta que la propia acción del bot escribiera el valor. Se recomienda que la primera prueba de
  aceptación de la fase siguiente (`PRUEBA-005`) ejercite exactamente esto: disparar `RG-10` de
  verdad y leer si la fila nueva de `OT_OrdenesTrabajo` tiene `OTID` con forma de `UNIQUEID()`.
- **Depende de que `docs/PROMPT_CABLEADO.md` y `docs/MANUAL_DESPLIEGUE.md` se regeneren** después de
  este cambio (`python scripts/generar_prompt_cableado.py`, `python scripts/generar_manual_despliegue.py`),
  o seguirán instruyendo "Y estas 2, PARA" y "ninguna: la clave la identifica" sobre un modelo que ya
  cambió. Esto es autoejecutable — son generados, no se editan a mano — pero solo si alguien corre el
  comando; queda para la orden de ejecución, no para esta especificación.
- **Si esta especificación se aplica y `ROADMAP.md` §4.5 no se corrige (§2.6, §5)**, el repositorio
  vuelve a tener el mismo patrón que costó meses: un documento que describe un estado que ya cambió.
  Se deja advertido explícitamente para que no se repita en silencio.

## 7. Supuestos adoptados

1. **Que AppSheet evalúa el `Initial value` de una columna también cuando la fila la crea un bot
   (`RG-10`, `RG-12`), igual que cuando la crea un formulario de usuario.** No hay una cita verificada
   de esto en `docs/BASE_CONOCIMIENTO_APPSHEET.md`. Se adopta como supuesto porque (a) es el
   comportamiento que `docs/PROMPT_CABLEADO.md` ya asume para las seis tablas de `CLAVE_GENERADA`
   sin que nadie lo haya cuestionado, y (b) la documentación oficial dice que el `Initial value` "se
   asigna una vez, al crear el registro" sin distinguir el origen de esa creación
   (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §3). Si resulta falso, es el riesgo más caro de esta
   especificación (§6) y hay que revisarlo antes de dar por resuelto `RG-10` y `RG-12`.
2. **Que `UNIQUEID()` no colisiona entre dos dispositivos sin conexión.** `docs/BASE_CONOCIMIENTO_APPSHEET.md`
   lo declara expresamente sin verificar contra la fuente oficial ("Lo que sigue SIN verificar contra
   la fuente"). Se adopta igual porque, de las tres opciones evaluadas en §3.1, es la única sin un
   modo de fallo ya documentado en este proyecto.
3. **Que "operación" no comparte el perfil de concurrencia offline de un técnico de campo.** Sale
   del enunciado de este encargo ("`PLA_PlanMantenimiento` no la crea nadie en campo: la puebla
   operación"), no de un conteo verificado de usuarios ni de dispositivos.
4. **El nombre de columna `Etiqueta`.** No había convención previa para una columna de este tipo en
   una tabla transaccional (las columnas que hoy sirven de etiqueta son todas de catálogos:
   `Nombre`, `Nombres`, `Pregunta`, `Descripcion`). Se adopta `Etiqueta` porque no colisiona con
   ningún nombre existente (§3.2) y describe sin ambigüedad su propósito.
5. **Que basta con dos referencias (`docs/PROMPT_CABLEADO.md` línea 65-74) para decidir que
   `OT_OrdenesTrabajo` necesita una `Etiqueta` explícita y que `PLA_PlanMantenimiento`, con cero, no
   la necesita con la misma urgencia.** Se adopta como criterio de priorización, no como regla
   general: `PLA_PlanMantenimiento` recibe la misma columna `Etiqueta` de todas formas (§3), así que
   este supuesto no deja a `PLA_PlanMantenimiento` peor servida, solo explica por qué `OT_OrdenesTrabajo`
   es el caso que de verdad rompía algo hoy.
