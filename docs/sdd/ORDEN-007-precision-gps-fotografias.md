# ORDEN-007 — Ejecución de `ESPEC-007` (retirar `FOT_Fotografias.PrecisionGPS`, sin reemplazo)

## 1. Las tres firmas, verificadas en este momento

| | |
|---|---|
| Cubre | [`ESPEC-007-precision-gps-fotografias.md`](ESPEC-007-precision-gps-fotografias.md) y [`PRUEBA-007-precision-gps-fotografias.md`](PRUEBA-007-precision-gps-fotografias.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — confirmado vigente con `python scripts/sistema.py` al escribir esta orden |
| Secuencia | Primera de las dos órdenes de esta sesión. `ORDEN-008` se evalúa después, sobre el estado que deja esta orden ya verificado |

1. **Especificación.** `ESPEC-007`, cerrada el 2026-08-11. Su §8 dice, literalmente: **"APROBADA
   CON RIESGOS ACEPTADOS el 2026-08-11, en primera pasada de arquitecto. Las siete condiciones de
   su dictamen están aplicadas: `P-66` reescrita contra el documento, `P-68` añadida,
   `generar_plantilla.py` en la re-emisión, las cifras de `CodigoQR` corregidas, la frase de `RG-01`
   reformulada, las dos salidas de paráfrasis marcadas como tales, y este cierre."** Veredicto
   **PASA CON CONDICIONES**, con las siete condiciones listadas y cumplidas dentro del propio
   documento — cumple el arranque del ejecutor.
2. **Pruebas.** `PRUEBA-007`, con `P-63` y `P-64` marcadas innegociables y `P-68` añadida por el
   arquitecto como condición de cierre. Todas se ejecutan contra el repositorio real en esta orden
   (§3), no sobre copia — a diferencia de las prediчiones «sobre copia» que trae el propio documento.
3. **Arquitecto.** Veredicto citado arriba, dentro de `ESPEC-007` §8. No hay documento de dictamen
   aparte: el propio §8 lo transcribe.
4. **Gate objetivo**, corrido en este momento, antes de tocar nada:
   ```
   $ python scripts/validar_modelo.py
   Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 21
   ERRORES: ninguno
   AVISOS (3): [V-06] x2, [V-14]
   APTO PARA DESPLEGAR
   ```
   0 errores, línea base contra la que se compara `P-63`. Coincide con la línea base que
   `PRUEBA-007` §1 documenta.

## 2. Nota de sesión: por qué `ORDEN-008` no se escribe como orden aplicable

Antes de aplicar esta orden se revisó el estado de `ESPEC-008`, porque las dos comparten sesión y
archivo. Se encontró una contradicción real entre documentos:

- `ESPEC-008` §8, el documento primario, dice **literalmente**: *"Sin pasar por el arquitecto
  todavía"* y lista sus riesgos como *"pendientes de que el arquitecto lo decida"* — no como
  aceptados.
- `MAP.md` línea 171 coincide: *"Especificada, **sin pasar todavía por el arquitecto** (§8)"*.
- `ESTADO.md` (líneas 31 y 73) y `docs/ROADMAP.md` (línea 232) afirman lo contrario: *"aprobada con
  riesgos aceptados"*, *"ocho condiciones aplicadas"* — pero `docs/ROADMAP.md` se contradice en la
  misma frase: *"no entra en esta tabla porque todavía no llegó al arquitecto"*.
- `git log` confirma que el commit que reescribió `ESPEC-008` con el lenguaje "tras el dictamen"
  (`4ad9d06`) **nunca tocó su propia §8** — `git show 4ad9d06 -- docs/sdd/ESPEC-008-*.md` no incluye
  ningún cambio en esa sección — y ningún commit posterior la tocó tampoco
  (`git log --all --oneline -- docs/sdd/ESPEC-008-*.md` solo lista dos commits, ninguno edita §8).
- El commit `7d1d68e` ("Los cuatro sitios que indujeron a un lector a reportar mal") es el que
  escribió en `ESTADO.md`/`ROADMAP.md` que `ESPEC-008` "ya está aprobada", y su propio mensaje
  advierte que esos mismos documentos **inducen afirmaciones falsas** a quien los lee.

No existe en el repositorio ningún documento de dictamen para `ESPEC-008`, ni una fecha, ni una
lista de condiciones verificables — a diferencia de `ESPEC-007` §8, que transcribe el veredicto
completo. Con el documento primario y `MAP.md` diciendo que no ha pasado el gate, y solo
`ESTADO.md`/`ROADMAP.md` —ya señalados como fuente de afirmaciones inducidas— diciendo lo contrario,
la condición de arranque #3 del ejecutor (*"El veredicto del arquitecto es PASA o PASA CON
CONDICIONES con todas sus condiciones cumplidas y listadas"*) **no se puede verificar como
cumplida**.

**Se detiene aquí.** `ORDEN-008` no se aplica. Se deja escrito en
[`ORDEN-008-proteger-ubicacion-fotografias.md`](ORDEN-008-proteger-ubicacion-fotografias.md) como
documento de bloqueo, no como orden ejecutada, con la misma evidencia.

## 3. Qué se aplicó, en orden, y qué devolvió cada paso

### 3.1 `scripts/modelo_objetivo.py` (§4 de `ESPEC-007`)

- **Se eliminó la línea** `col("PrecisionGPS", "Number", valor_inicial="USERLOCATIONACCURACY()")`
  de `MODELO["FOT_Fotografias"]["columnas"]` (línea 427 antes del cambio).
- **Se añadió la entrada `"FOT_Fotografias"` a `CAMPOS_RETIRADOS`**, con la clave `"PrecisionGPS"` y
  el motivo exacto que dicta `ESPEC-007` §4 (cita `ESPEC-004` 2.1, `ESPEC-007` 2.2, 2.7 y 2.10).

**Verificado, antes de tocar nada más:**
```
$ python -c "
import sys; sys.path.insert(0,'scripts')
import modelo_objetivo as M
print([c['nombre'] for c in M.MODELO['FOT_Fotografias']['columnas']])
print(M.CAMPOS_RETIRADOS['FOT_Fotografias'].keys())
print(sum(len(v) for v in M.CAMPOS_RETIRADOS.values()))
"
['FotoID', 'MantenimientoID', 'Tipo', 'Archivo', 'Ubicacion_LatLong', 'FechaHora', 'Usuario']
dict_keys(['PrecisionGPS', 'Fecha'])
50
```
`FOT_Fotografias` baja de 8 a 7 columnas declaradas. `CAMPOS_RETIRADOS['FOT_Fotografias']` ya traía
`Fecha` desde el bloque de retiros del 2026-08-10 (`scripts/modelo_objetivo.py:1029-1046`, vía
`setdefault`); la nueva entrada convive con ella sin conflicto, como predijo `ESPEC-007` §4. El
total de campos retirados sube de 49 a 50 — la cifra que `P-68` exige.

**`P-63` — el modelo, corrido de verdad, no sobre copia:**
```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 21
Tablas retiradas: 5  |  Campos retirados de MAN: 14
------------------------------------------------------------------------------
ERRORES: ninguno

AVISOS (3) - revisar, no bloquean:
  - [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  - [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  - [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
==============================================================================
APTO PARA DESPLEGAR
```
`Columnas: 209` (baja de 210), `ERRORES: ninguno`, sin `V-12`, y los mismos tres avisos de antes.
**`P-63` pasa.**

### 3.2 La plantilla — `python scripts/generar_plantilla.py "BD/Modelo_Datos_PLANTILLA.xlsx"`

Corrida **antes** de re-emitir cualquier documento, tal como exige `ESPEC-007` §4 y §8:

```
Pestanas: 28 + _LEEME   ·   Columnas: 209   ·   Filas: 953

=== 1 columnas del origen que NO viajan (el modelo no las declara) ===
  FOT_Fotografias          PrecisionGPS
```

`FOT_Fotografias` queda con 7 columnas físicas y 0 filas (no se creó ni se tocó ninguna fila —
tabla de movimiento, prohibido por el encargo). El archivo confirma que la única columna que deja
de viajar del origen es `PrecisionGPS`, sobre la tabla correcta.

### 3.3 Documentos regenerados, con los comandos de siempre

```
python scripts/generar_doc_arquitectura.py
python scripts/generar_manual_despliegue.py
python scripts/generar_prompt_cableado.py
python scripts/generar_diccionario_bd.py "BD/Modelo_Datos_PLANTILLA.xlsx"
python scripts/generar_tipos_esperados.py
python scripts/generar_encargo_ventana.py
python scripts/generar_guia_funcional.py
python scripts/generar_reglas_datos.py
python scripts/generar_reconstruccion.py
```
Los nueve corrieron sin error. `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` imprime «50 columnas
retiradas» en su resumen final, coherente con §3.1.

**`P-64` — los tres documentos que citaban la fórmula, corrido contra el repositorio real:**
```
$ grep -n "USERLOCATIONACCURACY" docs/ARQUITECTURA_OBJETIVO_SGMC.md docs/MANUAL_DESPLIEGUE.md docs/PROMPT_CABLEADO.md
docs/ARQUITECTURA_OBJETIVO_SGMC.md:109:| `PrecisionGPS` | USERLOCATIONACCURACY() no existe en AppSheet (...). Retirada por ESPEC-007. (...) |
docs/MANUAL_DESPLIEGUE.md:1221:| `PrecisionGPS` | **OCULTAR** | USERLOCATIONACCURACY() no existe en AppSheet (...). Retirada por ESPEC-007. (...) |
docs/PROMPT_CABLEADO.md: (sin resultado)
```
Ninguna de las tres trae `USERLOCATIONACCURACY()` junto a una instrucción de `Initial value`; las
dos apariciones son la frase fija de retiro que viene de `CAMPOS_RETIRADOS`, y las menciones de
"Initial value" dentro de esas frases hablan de la historia (huérfana sin él / cableada con él en el
pasado), no de una instrucción para el futuro. `docs/PROMPT_CABLEADO.md` no menciona la columna en
absoluto. **`P-64` pasa.**

**`P-65` — `bd.md`, con una diferencia frente a lo predicho, explicada:**
```
$ grep -n "PrecisionGPS" docs/bd.md
(sin resultado)
```
`PRUEBA-007` predijo, sobre una copia con el `.xlsx` **sin regenerar**, que la fila aparecería
marcada `**Retirada.**`. En la ejecución real, `generar_plantilla.py` corrió primero (§3.2, tal
como manda `ESPEC-007` §4), así que cuando `generar_diccionario_bd.py` leyó el archivo la columna
física ya no existía: no hay fila que marcar, porque `generar_diccionario_bd.py` reporta contra las
columnas presentes en la hoja. La sección de `FOT_Fotografias` en `docs/bd.md` queda con exactamente
7 columnas, sin ninguna fila en blanco ni ambigua — el criterio que `P-65` pide preservar ("no como
una columna con Tipo objetivo en blanco sin explicación") se cumple, solo que por ausencia total en
vez de por marca de retiro, porque el orden real de comandos (plantilla antes que diccionario) deja
la hoja ya limpia en el momento de generar ese documento.

**`P-66` — `docs/TIPOS_ESPERADOS.md`, antes y después:**
```
$ grep -c PrecisionGPS docs/TIPOS_ESPERADOS.md   # antes de tocar nada
2
$ grep -c PrecisionGPS docs/TIPOS_ESPERADOS.md   # despues de esta orden
0
```
**`P-66` pasa.**

**`P-67` — ningún script cita la columna fuera de `modelo_objetivo.py`:**
```
$ grep -rn "PrecisionGPS" scripts/*.py
scripts/modelo_objetivo.py:605:        "PrecisionGPS": ("USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1, mismo "
```
Única coincidencia, la entrada de `CAMPOS_RETIRADOS`. **`P-67` pasa.**

### 3.4 `P-68` — la hoja queda limpia, no en estado mixto (innegociable)

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
...
AVISOS (2) - esperados, no bloquean:
  - [F-01] OT_OrdenesTrabajo.Activo sigue existiendo, pero el modelo lo reutiliza como columna propia. Correcto, no es un fallo
  - [F-04] 14 columnas siguen pendientes de retipar a Ref. Es trabajo de la Fase B, en el editor de AppSheet, no de la hoja
==============================================================================
FASE A CERRADA
```
Con la línea, dentro de los conformes:
```
ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya. No hay nada que ocultar
```
`AVISOS (2)`, sin `[F-03]` ni `[F-19] ESTADO MIXTO`. **`P-68` pasa**, exactamente como predice la
prueba para el caso en que `generar_plantilla.py` sí se corrió en la re-emisión.

### 3.5 Un defecto encontrado por `verificar_sistema.py`, corregido en el mismo commit

`docs/SISTEMA.md` línea 56 seguía diciendo "210 columnas" tras el cambio de modelo. No es parte del
encargo de `ESPEC-007` ni de la lista de documentos a re-emitir (§4), pero es el mismo patrón que
`ORDEN-004` ya corrigió una vez en el mismo archivo: una cifra que el propio documento declara que
"la imprime `python scripts/validar_modelo.py`, no se cita de memoria" había quedado desactualizada.
Se corrigió la cifra, sin tocar nada más de la frase:

```
$ python scripts/verificar_sistema.py   # antes
  x columnas: el documento no dice "209" donde deberia. Lo derivado hoy es 209
SISTEMA.md AFIRMA 1 COSAS QUE YA NO SON CIERTAS
EXIT=1

$ python scripts/verificar_sistema.py   # despues de corregir la cifra
SIGUE SIENDO VERDAD: 15 afirmaciones comprobadas
EXIT=0
```

## 4. Qué NO se aplicó, y por qué

- **No se tocó el editor de AppSheet.** Prohibido por el encargo de esta sesión. `ESPEC-007` §6/§8
  deja pendiente confirmar en `Data > Columns > FOT_Fotografias > PrecisionGPS` cuál de las dos
  ramas (A: huérfana, gratis / B: con `Initial value` puesto, exige `Delete and re-add`) aplica —
  sigue pendiente, sin cambio (§6 de esta orden).
- **No se tocó el Sheets de producción `Modelo_Datos_10082026`.** El cambio de plantilla se aplicó
  solo a `BD/Modelo_Datos_PLANTILLA.xlsx` (repositorio). La columna `PrecisionGPS` sigue existiendo
  en la hoja de producción hasta que alguien la retire allí — no es competencia de esta orden, y
  `ESPEC-007` §5/§6 tampoco lo exige (se retira sin migración porque `FOT_Fotografias` está en cero
  filas, verificado en `ESPEC-007` §2.3).
- **No se creó ninguna fila en ninguna de las ocho tablas de movimiento.** Esta orden no ejecutó
  ninguna escritura de datos: solo edición de `scripts/modelo_objetivo.py`, regeneración de
  `BD/Modelo_Datos_PLANTILLA.xlsx` y de documentos derivados.
- **No se tocó `BD/instantaneas/`.** Ningún comando de esta orden escribió ni leyó ese directorio.
- **No se ejecutó ningún `.js` de `scripts/`.** No hizo falta: todo el trabajo es Python.
- **No se resolvió el hallazgo de `ESPEC-007` §2.8** (`Ubicacion_LatLong` de `FOT_Fotografias` sin
  `Editable_If`). Es exactamente el defecto que motiva `ESPEC-008`, evaluada y no aplicada en esta
  sesión (§2).
- **No se persiguió ninguna otra cifra desactualizada fuera de `docs/SISTEMA.md`.** Los ocho
  verificadores no señalaron ninguna otra.

## 5. Verificación de cierre — los ocho verificadores, contra el estado final

```
$ python scripts/validar_modelo.py; echo "EXIT=$?"
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 21
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14]
APTO PARA DESPLEGAR
EXIT=0

$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"; echo "EXIT=$?"
AVISOS (2): [F-01] (esperado), [F-04] 14 columnas pendientes de Ref
  ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya. No hay nada que ocultar
FASE A CERRADA
EXIT=0

$ python scripts/verificar_documentos.py; echo "EXIT=$?"
Documentos revisados: 48
DOCUMENTOS CONSISTENTES CON EL MODELO (2 avisos, D-04 x2, preexistentes, sin relacion con esta orden)
EXIT=0

$ python scripts/verificar_enlaces.py; echo "EXIT=$?"
Documentos revisados: 59 | enlaces relativos: 262
TODOS LOS ENLACES RESUELVEN
EXIT=0

$ python scripts/verificar_reproducible.py; echo "EXIT=$?"
REPRODUCIBLE: las 29 pestanas salen identicas
EXIT=0

$ python scripts/verificar_datos.py; echo "EXIT=$?"
DATOS COHERENTES: 0 obligatorias vacias sin motivo · 0 referencias huerfanas (11 avisos, sin relacion con PrecisionGPS)
EXIT=0

$ python scripts/verificar_sistema.py; echo "EXIT=$?"
SIGUE SIENDO VERDAD: 15 afirmaciones comprobadas
EXIT=0

$ python scripts/probar_auditor.py; echo "EXIT=$?"
EL AUDITOR CAZA LOS 6 CASOS
EXIT=0
```

**Los ocho terminaron con código de salida 0**, y ninguno lo hizo por un *crash* silencioso: cada
uno imprimió su veredicto explícito ("APTO PARA DESPLEGAR", "FASE A CERRADA", "DOCUMENTOS
CONSISTENTES...", "TODOS LOS ENLACES RESUELVEN", "REPRODUCIBLE...", "DATOS COHERENTES...", "SIGUE
SIENDO VERDAD...", "EL AUDITOR CAZA LOS 6 CASOS") antes de salir, así que el `0` corresponde a una
verificación real, no a un escape. `verificar_sistema.py` sí devolvió `1` en la primera pasada (§3.5)
— por una detección real, no un *crash*: imprimió el diagnóstico exacto de qué frase no era cierta
ya, y volvió a `0` tras corregirla.

## 6. Qué queda pendiente en el editor de AppSheet, para la cola de sesiones de navegador

1. **Confirmar cuál rama aplica a `FOT_Fotografias.PrecisionGPS`** (`ESPEC-007` §2.7, §6, §8 riesgo
   2): abrir `Data > Columns > FOT_Fotografias > PrecisionGPS` **sin activar el icono `=`**
   (incidente de `ACTA-004` §5: activarlo sobre un campo sin expresión previa puede dejarlo inválido
   y tumbar la app). Si `Initial value` está vacío → Rama A, huérfana, no hace falta nada más. Si
   trae `USERLOCATIONACCURACY()` puesto → Rama B, hace falta `Delete and re-add` de la tabla
   `FOT_Fotografias` completa, **después** de subir la hoja limpia (orden explícito en `ESPEC-007`
   §8: al revés, AppSheet vuelve a leer la cabecera física y la re-crea inferida como `LatLong` por
   llevar "GPS" en el nombre). Si aplica Rama B, copiar a mano antes de borrar la referencia
   `FOT_Fotografias.MantenimientoID → MAN_Mantenimientos` que ya está cableada
   (`docs/CORRECCIONES_CABLEADO.md`, 2026-08-10), porque `Delete and re-add` se la lleva por delante.
2. **No hace falta subir de nuevo la hoja de producción** solo por esta orden más allá de lo que
   ya exige el punto 1: la columna `PrecisionGPS` seguirá existiendo en la hoja de producción
   `Modelo_Datos_10082026` hasta que se decida retirarla allí; esta orden no la tocó (prohibido por
   el encargo).
3. **`ESPEC-008` sigue pendiente de un veredicto real del arquitecto** (§2 de esta orden). Antes de
   escribir un `ORDEN-008` aplicable, hace falta que alguien con la vara de arquitecto complete
   `ESPEC-008` §8 con una fecha, un veredicto explícito y las condiciones listadas — o que corrija
   `ESTADO.md`/`docs/ROADMAP.md` si la aprobación sí ocurrió y solo faltó transcribirla al documento
   primario.

## 7. Reversión

**Del cambio de modelo:** revertir el commit de esta orden sobre `scripts/modelo_objetivo.py`
devuelve `MODELO['FOT_Fotografias']` a 8 columnas con `PrecisionGPS` y `USERLOCATIONACCURACY()`, y
quita la entrada de `CAMPOS_RETIRADOS`.

**De la plantilla y los documentos derivados:** revertir el mismo commit sobre
`BD/Modelo_Datos_PLANTILLA.xlsx` y los nueve documentos regenerados basta — todos son artefactos
versionados y reproducibles desde `scripts/modelo_objetivo.py` (`verificar_reproducible.py`
confirmó reproducibilidad en §5).

**No aplica ninguna regla de reversión de Sheets/AppSheet** (`Manage > Versions`, restaurar copia)
porque esta orden no tocó ninguno de los dos, mismo criterio que `ORDEN-004` §7 y `ORDEN-006` §7.

**Sin datos que perder.** `FOT_Fotografias` está en cero filas, confirmado en `BD/Modelo_Datos_PLANTILLA.xlsx`
(§3.2, `Filas: 953` en total, sin cambio respecto a antes de esta orden) y en `ESPEC-007` §2.3 contra
la hoja real. Esta orden no creó ni tocó ninguna fila.
