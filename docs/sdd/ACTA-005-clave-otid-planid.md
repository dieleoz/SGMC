# ACTA-005 — Qué quedó realmente en el repositorio tras `ORDEN-005`

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.Etiqueta, PLA_PlanMantenimiento.Etiqueta -->
<!-- D-03 compara Tabla.Columna contra MODELO, y Etiqueta a propósito NUNCA entra en MODELO: es
     una columna virtual declarada solo en REGLAS (RG-35/RG-36). Mismo criterio que ESPEC-005. -->

**Fecha de este acta:** 2026-08-11. **Cubre:** [`ORDEN-005`](ORDEN-005-clave-otid-planid.md), sobre
[`ESPEC-005`](ESPEC-005-clave-otid-planid.md) y [`PRUEBA-005`](PRUEBA-005-clave-otid-planid.md).

## -1. Hallazgo de esta sesión: el repositorio se modificó en vivo mientras se escribía esta acta —
léase antes que el resto

**Este repositorio no estaba quieto durante esta tarea.** Mientras se redactaban `ORDEN-005` y las
ediciones de `ESPEC-005`/`PRUEBA-005`, aparecieron commits nuevos en `git log` con marca de tiempo de
minutos antes de cada comprobación (`47acef8`, 09:20:30, verificado contra un reloj del sistema en
09:22:33). Uno de ellos empaquetó, **sin que esta sesión ejecutara `git add` ni `git commit` en
ningún momento**, las ediciones de esta tarea (`ESPEC-005`, `PRUEBA-005`, el archivo nuevo
`ORDEN-005`) junto con cambios ajenos a esta orden: una instantánea de 17.293 líneas
(`BD/instantaneas/despues-de-la-ventana.json`), y modificaciones a `docs/PROMPT_CABLEADO.md`,
`docs/PROMPT_EXPRESIONES.md`, `docs/ENCARGO_VENTANA.md` y `scripts/navegacion_editor.py`, con un
mensaje de commit que describe trabajo real contra el editor de AppSheet (columnas virtuales creadas,
54 tipos cotejados, un bug de caché del editor) que **esta sesión no ejecutó**. Después de eso,
`git status` siguió mostrando más archivos tocados por fuera de esta tarea (`MAP.md`, `README.md`, un
`../SISTEMA.md` nuevo), en los minutos siguientes.

**Lectura correcta de esto:** hay una sesión de ejecución distinta y activa, trabajando sobre el
mismo repositorio al mismo tiempo que esta, probablemente aplicando de verdad la Familia B de
`PRUEBA-005` contra la aplicación (lo que en §5 de esta acta se describe como "pendiente" según lo
que esta sesión pudo verificar por su cuenta). **Esta acta no puede ni debe intentar reconciliar esa
actividad**: no es el encargo que abrió esta tarea, esta sesión no la ejecutó ni la puede verificar
con sus propios comandos, y forzar una narrativa conjunta sería exactamente el tipo de "reporte sin
verificación propia" que este proyecto ya arrastra. Lo que sí hace esta acta: dejar constancia clara
de que existió, y de que **las ediciones de esta tarea terminaron dentro de un commit que esta sesión
no autorizó ni ejecutó**, aunque el contenido de esas ediciones —verificado línea por línea contra el
commit (`git show 47acef8 -- docs/sdd/ESPEC-005-...md` y `docs/sdd/PRUEBA-005-...md`)— es exactamente
el texto que esta sesión escribió, sin alteración.

**Consecuencia práctica:** los cuatro verificadores se corrieron de nuevo *después* de este hallazgo,
contra el estado ya mezclado (§6), y siguen en verde. Pero el estado de "qué falta en el editor de
AppSheet" que describe §5 puede estar ya desactualizado por la actividad de esa otra sesión — no se
verificó de nuevo contra la aplicación en vivo dentro de esta tarea, porque hacerlo sin coordinación
sería exactamente "improvisar sobre producción". **Se recomienda, antes de dar este frente por
cerrado, confirmar con quien tenga acceso a la sesión concurrente qué aplicó de verdad, y cotejarlo
contra §5 de esta acta.**

## 0. El fallo de proceso, de frente

**`ESPEC-005` se aplicó al modelo el 2026-08-10/11 (commit `8e7ccef`) sin que existiera todavía
`ORDEN-005` ni este acta, y sin pasar por el ejecutor.** No es un atajo válido ni una interpretación
generosa del pipeline: `docs/SDD_PIPELINE_SGMC.md` §3 y §4 son explícitos en que el paso 4
(ejecutor, que produce `ORDEN-NNN` **antes** de tocar producción o el modelo) no arranca sin la
orden. Es la **segunda vez** que este proyecto se salta un paso del pipeline — la primera está en
`ESTADO.md`: *"Es la regla que nos saltamos el 2026-08-10 por la mañana, y costó un dictamen de
veinte observaciones."*

Este acta no encubre el orden real de los hechos. Lo que sigue documenta, verificado con comando,
**qué quedó en el repositorio**, no en qué orden se debería haber hecho.

## 1. Qué se aplicó al modelo — verificado ahora, no de memoria

```
$ python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as m;print(len(m.CLAVE_LEGIBLE),len(m.CLAVE_GENERADA),len(m.REGLAS))"
20 8 23
```
Antes de `ESPEC-005` (commit `43b0666` y anteriores): `22 6 21`. Coincide exactamente con lo que
`ESPEC-005` §4 y `PRUEBA-005` §1.3 predijeron.

```
$ python -c "import sys;sys.path.insert(0,'scripts');from inferencia import etiqueta_de;print('OT',etiqueta_de('OT_OrdenesTrabajo'));print('PLA',etiqueta_de('PLA_PlanMantenimiento'));print('MAN',etiqueta_de('MAN_Mantenimientos'));print('CHK',etiqueta_de('CHK_Checklists'))"
OT Etiqueta
PLA Etiqueta
MAN None
CHK None
```
`ETIQUETA_VIRTUAL` existe y `etiqueta_de()` la consulta antes que `SIN_ETIQUETA_NATURAL`, exactamente
como manda `ESPEC-005` §3.2 punto 3. `MAN_Mantenimientos` y `CHK_Checklists` siguen sin etiqueta,
sin cambio: **hecho y verificado**.

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
ERRORES: ninguno
AVISOS (3): [V-06] PLA_PlanMantenimiento no es referenciada por nadie ·
            [V-06] LST_ValoresLista no es referenciada por nadie ·
            [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
APTO PARA DESPLEGAR
```
`Columnas` se queda en 211 (no sube a 213): confirma que `Etiqueta` nunca entró en `MODELO`, tal
como exige el diseño de columna virtual. **Hecho y verificado.**

## 2. Lo contraintuitivo: la hoja de datos NO cambió

```
$ python -c "import subprocess,io,openpyxl;a=subprocess.run(['git','show','43b0666:BD/Modelo_Datos_PLANTILLA.xlsx'],capture_output=True).stdout;A=openpyxl.load_workbook(io.BytesIO(a),read_only=True,data_only=True);B=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True);print(len(A.sheetnames),'pestanas | mismos nombres:',A.sheetnames==B.sheetnames,'|',sum(1 for n in A.sheetnames if [tuple(r) for r in A[n].iter_rows(values_only=True)]!=[tuple(r) for r in B[n].iter_rows(values_only=True)]),'con contenido distinto')"
29 pestanas | mismos nombres: True | 0 con contenido distinto
```
`43b0666` es el commit inmediatamente anterior a `ESPEC-005` (el mismo que cita `ROADMAP.md`).
**Corrida de nuevo en esta sesión, mismo resultado: 29 pestañas, las mismas, cero con contenido
distinto.** La razón, verificada contra el modelo: `RG-35` y `RG-36` son columnas **virtuales** — no
existen en `MODELO["OT_OrdenesTrabajo"]["columnas"]` ni en
`MODELO["PLA_PlanMantenimiento"]["columnas"]` (confirmado en §1) — y `CLAVE_LEGIBLE`/`CLAVE_GENERADA`
describen el comportamiento del **editor** de AppSheet (qué `Initial value` declarar, si se puede
marcar `Key`), no una transformación de datos. No hay ninguna `App formula` sobre columna real que
hubiera escrito en el Sheets. **Hecho y verificado**, con el comando de arriba.

## 3. Efecto colateral: `F-11` dejó de disparar sobre dos tablas

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
...
AVISOS (2) — esperados, no bloquean:
  - [F-01] OT_OrdenesTrabajo.Activo sigue existiendo, pero el modelo lo reutiliza como columna propia. Correcto, no es un fallo
  - [F-04] 14 columnas siguen pendientes de retipar a Ref. Es trabajo de la Fase B, en el editor de AppSheet, no de la hoja
FASE A CERRADA
```
Antes de `ESPEC-005` (`PRUEBA-005` §1.2) había **cuatro** avisos: los mismos `F-01`/`F-04` más dos
`F-11` (*"OT_OrdenesTrabajo esta vacia: no se puede decidir si su clave es legible"*, y lo mismo para
`PLA_PlanMantenimiento`). Ahora son dos. La razón, verificada en `scripts/verificar_faseA.py:264-306`:
`F-11` exime del todo a las tablas en `CLAVE_GENERADA`, y las dos acaban de entrar ahí (§1). **Es
correcto** —su clave será aleatoria en cuanto exista la primera fila—, pero es **una comprobación
menos**: que la clave de esas dos tablas esté bien puesta en el editor ya no lo dice ningún
verificador automático de la hoja; solo se ve a ojo o con `auditar_cableado.py` una vez existan filas
(`PRUEBA-005` `P-14`). **Hecho y verificado**, con el comando de arriba.

## 4. Las condiciones de documento — aplicadas y verificadas, una por una

| # | Condición | Dónde quedó | Verificación |
|---|---|---|---|
| 3 | `RG-05` no aplicado durante la tanda; `P-14` única oportunidad | `ESPEC-005` §6 (párrafo nuevo tras el bullet de `auditar_cableado.py`); `PRUEBA-005` `P-14` (precondición + párrafo final) | `grep -n "RG-05" docs/sdd/ESPEC-005-clave-otid-planid.md docs/sdd/PRUEBA-005-clave-otid-planid.md` da resultados en ambos (antes de esta orden, cero) |
| 4 | Retirar `python scripts/sistema.py` como volcado | `PRUEBA-005`, fila «Contra cuál sistema» y cierre de `P-13` | `grep -n "no descarga nada" docs/sdd/PRUEBA-005-clave-otid-planid.md` → 2 apariciones |
| 5 | Citar `instantanea.py`/`VOLCADO_CIEGO_A`, no solo el volcado local | `ESPEC-005` §2.1, reescrita | `grep -n "VOLCADO_CIEGO_A" docs/sdd/ESPEC-005-clave-otid-planid.md` → 1 aparición |
| 6 | `P-15`: `Show?` activo + `Label?` desactivado | `PRUEBA-005` `P-15` | `grep -n "Label?" docs/sdd/PRUEBA-005-clave-otid-planid.md` → apariciones en `P-15` y `P-17` |
| 7 | `P-17`: marcar `Label` sobre `PLA_PlanMantenimiento.Etiqueta` | `PRUEBA-005` `P-17`, paso 1 nuevo | Lectura directa de `P-17`: paso 1 de la acción marca `Label` antes de crear el fixture |
| 8 | Cita a `MANUAL_DESPLIEGUE.md` por título, no por línea; documento sumado a la lista de generados | `ESPEC-005` §3.4 y §8 | `grep -n "174-175" docs/sdd/ESPEC-005-clave-otid-planid.md` → 0 resultados (antes, 1); `grep -n "MANUAL_DESPLIEGUE.md.*generad" docs/sdd/ESPEC-005-clave-otid-planid.md` → presente en §8 |
| 9 | `P-13`: reactivar `RG-07` sin comando, cierre a ojo | `PRUEBA-005` `P-13`, último punto | Lectura directa: el punto dice explícitamente "No hay comando..." y qué copiar |
| 10 | `P-07`: sustituir el `6` literal por el criterio declarado | `PRUEBA-005` `P-07` | Lectura directa: nuevo bullet "Criterio de paso" antes del resultado observado, y nota final de que un conteo distinto de 6 no es, por sí solo, un fallo |

**Nota de cuenta:** el encargo que abrió esta orden presenta estas condiciones como "siete" pero las
enumera en ocho puntos (numerados 3 a 10, sin que exista en el repositorio la lista original de diez
del arquitecto para cotejar la numeración). Este acta no fuerza la cuenta a siete: se aplicaron y se
verifican **las ocho** de la tabla de arriba. Si la intención original era que dos de ellas
compartieran un solo número en el dictamen del arquitecto, no cambia lo que se aplicó ni cómo se
verificó.

Además, fuera de la lista numerada: **`ESPEC-005` ya no se contradice con el repositorio real.** La
frase "no aplicada al repositorio real" (antes en la resolución de §3.2) se corrigió con una nota que
dice cuándo se aplicó y remite a esta orden. Verificado:
```
$ grep -n "no aplicada al repositorio real" docs/sdd/ESPEC-005-clave-otid-planid.md
372:"no aplicada al repositorio real". Eso dejó de ser cierto el 2026-08-10: los cambios de este §3.2 y
```
La única aparición que queda es dentro de la propia corrección, citando la frase vieja para explicar
por qué se corrigió — no una afirmación vigente.

## 5. Lo que NO se hizo — pendiente, sin ambigüedad

**El Sheets de producción y el editor de AppSheet no se tocaron en ningún momento de esta sesión.**
Coincide con lo que `ROADMAP.md` y `ESTADO.md` ya declaraban ("PENDIENTE EN EL EDITOR",
"Pendiente la mitad del editor") y esta acta no lo cambia:

- `Initial value = UNIQUEID()` y `Key` sobre `OT_OrdenesTrabajo.OTID` y `PLA_PlanMantenimiento.PlanID`
  — **pendiente**.
- Las dos columnas virtuales `Etiqueta` (crear, `Show?`, `Label`, desmarcar la etiqueta anterior) —
  **pendiente**.
- `RG-10`, `RG-12`, botón `+` de creación de órdenes — **pendiente** (`RG-12` además bloqueada por el
  plan gratuito, `ESPEC-005` §5).
- `auditar_cableado.py` medido de verdad sobre `OT_OrdenesTrabajo` con filas (`P-14`) — **pendiente**,
  y sigue siendo la única oportunidad futura mientras `RG-05` no se aplique (§4, condición 3).
- `RG-04`/`RG-05` (Security Filters) — **pendiente**, van los últimos.
- Bots `RG-07` desactivar/reactivar alrededor del fixture — **pendiente**, no aplica todavía porque
  no hay fixture.

Nada de esto lo autoriza `ORDEN-005` (§4 de esa orden). Sigue esperando una ejecución futura contra
la aplicación, con el encargo de [`docs/PROMPT_CABLEADO.md`](../PROMPT_CABLEADO.md).

**Aparte, y sin relación con esta orden:** `git status` muestra `BD/Modelo_Datos_PLANTILLA.xlsx`
modificado sin commit, de una sesión anterior a esta. Verificado que la diferencia es solo de
metadatos del contenedor `.zip`, cero contenido de celda distinto:
```
$ git diff --stat -- BD/Modelo_Datos_PLANTILLA.xlsx
 BD/Modelo_Datos_PLANTILLA.xlsx | Bin 80653 -> 80657 bytes
$ python -c "...comparación celda a celda contra HEAD..."
29 29 mismos nombres: True
con contenido distinto: []
```
No se tocó ni se hizo `commit` de este archivo en esta sesión, siguiendo la instrucción de no aplicar
nada nuevo al modelo ni a la hoja.

## 6. Verificación final de los cuatro verificadores

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14] x1 — preexistentes, no relacionados con esta orden
APTO PARA DESPLEGAR
```

```
$ python scripts/verificar_documentos.py
Documentos revisados: 32
Tablas del modelo: 28 | propuestas: 10 | retiradas: 5
Decisiones de una sola forma: 13
  - [D-04] ACT_Activos.FrecuenciaID se descarto y sigue viva. Se retira antes del 2026-08-31
  - [D-04] TIP_TiposActivo.FormularioID se descarto y sigue viva. Se retira antes del 2026-08-31
DOCUMENTOS CONSISTENTES CON EL MODELO (2 avisos)
```
0 fallos. Los dos avisos `D-04` son preexistentes (fecha límite 2026-08-31), no relacionados con esta
orden.

```
$ python scripts/verificar_enlaces.py
Documentos revisados: 43 | enlaces relativos: 21X
TODOS LOS ENLACES RESUELVEN
```
Incluye los enlaces nuevos de `ORDEN-005` y `ACTA-005` hacia `ESPEC-005`/`PRUEBA-005` y viceversa,
que antes de crear estos dos archivos aparecían como rotos (verificado en esta misma sesión, antes de
escribir `ACTA-005`: 4 enlaces rotos por la ausencia de los archivos).

```
$ python scripts/verificar_datos.py
DATOS COHERENTES: 0 obligatorias vacias sin motivo · 0 referencias huerfanas
11 avisos
```
Los 11 avisos son los mismos de `PRUEBA-005` §1.2, preexistentes, ninguno nuevo.

**Las cuatro verificaciones: hecho y verificado con los comandos de arriba, corridos en esta sesión,
después de escribir `ORDEN-005` y este acta.**

## 7. Qué queda sin hacer, resumido

- **Toda la Familia B, C y D de `PRUEBA-005`** (`P-09` a `P-17`): pendiente de una ejecución real
  contra el editor de AppSheet y el Sheets de producción. No es responsabilidad de esta orden ni de
  este acta cerrarlas; queda explícito en `ORDEN-005` §4.
- **La numeración original de las diez condiciones del arquitecto** no está en el repositorio como
  documento aparte; esta acta trabaja con el contenido de cada condición, no con un número que no se
  puede cotejar (§4, nota de cuenta).
- **El binario `BD/Modelo_Datos_PLANTILLA.xlsx` modificado sin commit**, de una sesión anterior a
  esta, sin contenido distinto verificado (§5). No se decide aquí si se hace `commit`: es una
  decisión fuera del alcance de esta orden.
- **Confirmar contra la sesión concurrente** qué de la Familia B ya aplicó de verdad, antes de tratar
  §5 de esta acta como la última palabra (§-1).

**Sobre `commit`/`push`:** esta sesión no ejecutó ninguno de los dos, siguiendo la instrucción con la
que se abrió este encargo. **Pero, como registra §-1, las ediciones de `ESPEC-005`, `PRUEBA-005` y el
archivo `ORDEN-005` terminaron dentro del commit `47acef8`, hecho por una sesión distinta y sin que
esta lo pidiera.** Esta acta (`ACTA-005-clave-otid-planid.md`) sigue sin `commit` al cerrarse. No se
intentó deshacer `47acef8` ni separar sus cambios: hacerlo arriesgaría borrar trabajo real de esa
otra sesión (la instantánea de 17.293 líneas, los cambios de `scripts/navegacion_editor.py` y de los
tres encargos generados) que esta tarea no tiene forma de verificar ni de reproducir.
