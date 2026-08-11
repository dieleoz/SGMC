# ORDEN-004 — Ejecución de `ESPEC-004` (cierre con excepción manual: `RG-02`/`RG-19` retiradas, `RG-03` desbloqueada)

## 1. Las cuatro firmas, verificadas en este momento

| | |
|---|---|
| Cubre | [`ESPEC-004-cierre-excepcion-manual.md`](ESPEC-004-cierre-excepcion-manual.md) y [`PRUEBA-004-cierre-excepcion-manual.md`](PRUEBA-004-cierre-excepcion-manual.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — confirmado vigente con `python scripts/sistema.py` al escribir esta orden, mismo resultado que cuando se escribió `ESPEC-004`/`ACTA-004` |

1. **Especificación.** `ESPEC-004`, tercera versión, reescrita el 2026-08-11 aplicando la vara de
   `CLAUDE.md` §7.18. Cierra su §8 con dos hallazgos que sobreviven como bloqueantes (el tipo de
   `CierreConExcepcion` y los ocho scripts de §2.9) y un riesgo aceptado (el tipo no verificado en
   el momento de aprobar).
2. **Pruebas.** `PRUEBA-004`, ajustada el mismo día contra la tercera versión de `ESPEC-004`.
   `P-34` a `P-39` (Familia A) se ejecutan en esta orden, de verdad, sobre el repositorio real —no
   simuladas—. `P-40` a `P-62` (Familias B, C, D) siguen sin ejecutarse: exigen el editor de
   AppSheet, que esta orden no toca (§4).
3. **Arquitecto.** Veredicto **APROBADA CON RIESGOS ACEPTADOS**, commit `e8befce`. La condición que
   el arquitecto marcó como la única que de verdad decide si la especificación funciona —el `Type`
   de `MAN_Mantenimientos.CierreConExcepcion`— se cerró **midiendo, no escribiendo**:
   [`ACTA-004-lecturas-editor.md`](ACTA-004-lecturas-editor.md) transcribe, con `Ctrl+Shift+R`
   previo, que es `Yes/No`. La misma acta, en su §4bis, midió lo que la primera sesión había
   dejado sin leer: **`RG-19` sí está viva**, puesta letra por letra como `App formula` sobre
   `CierreConExcepcion`. El defecto que `ESPEC-004` describe está confirmado, no hipotético.
4. **Gate objetivo**, corrido en este momento, antes de tocar nada:
   ```
   $ python scripts/validar_modelo.py
   Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
   ERRORES: ninguno
   AVISOS (3): [V-06] x2, [V-14]
   APTO PARA DESPLEGAR
   ```
   0 errores, línea base contra la que se compara §5.

## 2. Un hecho medido hoy que cambia el procedimiento de §3

`ACTA-004` §2 confirma la **Rama A** de `ESPEC-004` §2.10: `Precision_GPS` no trae `Initial value`
en el editor. Nadie llegó a cablear `USERLOCATIONACCURACY()` pese al bloqueo. Consecuencia directa
para esta orden:

- **Retirar `Precision_GPS` del modelo no exige tocar el editor de AppSheet.** La columna queda
  huérfana en la hoja —sin fórmula, sin uso—, y `ESPEC-004` §2.10 y `PRUEBA-004` `P-45` declaran
  eso explícitamente **no un fallo**. La Rama B (`Delete and re-add` de la tabla) queda descartada
  para esta ejecución.
- **No se borra `Precision_GPS` de la hoja de producción** (prohibido también por el encargo de
  esta sesión). Sigue existiendo como columna huérfana hasta que alguien haga *Delete and re-add*
  de `MAN_Mantenimientos` por otro motivo.

## 3. Qué se aplicó, en orden, y qué devolvió cada paso

### 3.1 `scripts/modelo_objetivo.py` (§4 de `ESPEC-004`)

- **`MODELO["MAN_Mantenimientos"]["columnas"]`**: se eliminó `Precision_GPS`. `CierreConExcepcion`
  perdió su `formula=`; queda `Yes/No` libre, con una `nota` que explica el mecanismo nuevo y
  remite a `ESPEC-004`.
- **`CAMPOS_RETIRADOS["MAN_Mantenimientos"]["Precision_GPS"]`**: añadida, con el motivo de §2.9 de
  `ESPEC-004` y la nota de que retirarla del esquema de AppSheet exige *Delete and re-add* solo si
  la tabla ya estaba cableada con `Initial value` puesto (Rama B) — no es el caso medido en
  `ACTA-004`.
- **`REGLAS`**: eliminados los `dict` de `RG-02` y `RG-19`. Los identificadores no se reutilizan —
  quedan como huecos numéricos, mismo precedente que fija `ESPEC-006` §4 después. `RG-20` pasó a
  cubrir tres columnas (`Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong`,
  `FechaHoraEscaneo`), no cuatro; se reescribió su `descripcion`.
- **`PARAMETROS["UMBRAL_GPS"]`**: reescrita su descripción siguiendo el precedente de
  `RADIO_GEOFENCING_KM` — ninguna regla la lee desde esta orden, queda como referencia para el
  juicio del técnico.
- **`DECISIONES`**: la entrada "Cierre sin GPS válido" no cambió de lado; su `por_qué` ahora dice
  que el valor lo pone el técnico, no una fórmula, y nombra la exposición de `ESPEC-004` §2.14.

**Verificado y verificado de nuevo:**
```
$ python -c "
import sys; sys.path.insert(0, 'scripts')
import modelo_objetivo as M
fallos = []
cols = {c['nombre'] for c in M.MODELO['MAN_Mantenimientos']['columnas']}
if 'Precision_GPS' in cols: fallos.append('Precision_GPS sigue en columnas')
cce = next(c for c in M.MODELO['MAN_Mantenimientos']['columnas'] if c['nombre'] == 'CierreConExcepcion')
if cce.get('formula'): fallos.append('CierreConExcepcion todavia tiene formula')
ids = {r['id'] for r in M.REGLAS}
if 'RG-02' in ids: fallos.append('RG-02 sigue en REGLAS')
if 'RG-19' in ids: fallos.append('RG-19 sigue en REGLAS')
rg20 = next(r for r in M.REGLAS if r['id'] == 'RG-20')
if 'Precision_GPS' in rg20['descripcion']: fallos.append('RG-20 todavia menciona Precision_GPS')
if 'Precision_GPS' not in M.CAMPOS_RETIRADOS.get('MAN_Mantenimientos', {}): fallos.append('falta CAMPOS_RETIRADOS')
print('FALLA:' if fallos else 'PASA: 0 fallos')
for f in fallos: print(' -', f)
"
PASA: 0 fallos
```
Esto es `P-34` de `PRUEBA-004`, invertida como se esperaba tras la orden.

### 3.2 `validar_modelo.py` — `P-35`

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 21
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14] (los tres preexistentes, ninguno nuevo)
APTO PARA DESPLEGAR
```
`Reglas` baja de 23 a 21 (se van `RG-02` y `RG-19`), `Columnas` de 211 a 210 (se va
`Precision_GPS`). Coincide exactamente con lo previsto en `PRUEBA-004` `P-35`. Antes de editar
`COBERTURA["Precision del GPS"]` en `validar_modelo.py:323`, el gate daba `[V-13] El flujo
'Precision del GPS' necesita MAN_Mantenimientos.Precision_GPS, que no existe` — confirmado
reproduciendo el fallo antes de corregirlo, no solo citado.

### 3.3 Los ocho scripts de §2.9 de `ESPEC-004` que dicen «Editar»

| Script | Qué se cambió |
|---|---|
| `scripts/validar_modelo.py:323` | Se retiró la entrada `"Precision del GPS"` de `COBERTURA` (comentario explicando por qué) |
| `scripts/generar_prompt_expresiones.py:330-357` | La sección "Dos que hoy NO se pueden poner" se reescribió: `RG-02` y `RG-19` ya no existen, y se añadió la instrucción nueva para `RG-03` (confirmar `Type`, fijar `Description`) |
| `scripts/generar_guia_funcional.py:383,389-403` | "cuatro columnas no editables" pasa a "tres"; la sección 7.2 ("El umbral de GPS, entero") se reescribió para describir la marca del técnico, no el cálculo automático |
| `scripts/generar_manual_despliegue.py:837-867` | Mismo tratamiento: "cuatro columnas" → "tres", sección de la excepción reescrita |
| `scripts/generar_diccionario_bd.py:159` | `lectores["UMBRAL_GPS"]` retirado del diccionario (ya no tiene lector) |
| `scripts/verificar_faseA.py:307-386` | El bloque `F-12` (cruce `Precision_GPS`×`CierreConExcepcion`) se retiró entero. `F-13` (validación general de `PAR_Parametros`) se conservó, sin la lógica de adopción específica de `UMBRAL_GPS` que solo servía a `F-12` |
| `scripts/generar_encargo_ventana.py:141` | La fila fija que decía `RG-02, RG-19, RG-03 → ESPEC-004 está bloqueada` ahora nombra solo `RG-03` y dice que **entra** |
| `scripts/verificar_datos.py:210-227` | El comentario de cabecera de `G-05` sustituyó el ejemplo `RG-19` (retirado) por `RG-13`/`UbicacionEscaneo_LatLong`, que sigue abierto |

**Verificación, `P-37` (el bloque `F-12`/`F-13` se retira):**
```
$ grep -n "Precision_GPS\|RG-19" scripts/verificar_faseA.py
(sin resultado en el bloque de reglas; solo comentarios historicos)
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
... FASE A CERRADA, sin F-12, sin F-11 sobre OT_OrdenesTrabajo/PLA_PlanMantenimiento
```
(exit code 0, confirmado con `echo $?` tras la corrida — ver §5)

**Verificación, `P-38` (diccionario ya no atribuye `UMBRAL_GPS` a `RG-19`):**
```
$ python scripts/generar_diccionario_bd.py && grep -n "UMBRAL_GPS" docs/bd.md
79:| `UMBRAL_GPS` | 40 | m | 40 | — |
```
Columna «Quién lo lee» en `—`, como pedía la prueba.

**Verificación, `P-39` (los generadores no instruyen a cablear algo retirado):**
```
$ grep -n "Precision_GPS\|USERLOCATIONACCURACY\|RG-02\b\|RG-19\b" docs/PROMPT_EXPRESIONES.md docs/GUIA_IMPLEMENTACION_FUNCIONAL.md docs/MANUAL_DESPLIEGUE.md docs/PROMPT_CABLEADO.md
```
Todas las líneas que devuelve son menciones históricas explícitamente marcadas como retiradas
(`RG-02 ya no existe`, `RG-19 también se retiró`, etc.), ninguna instruye a poner
`USERLOCATIONACCURACY()` ni la `App formula` de `RG-19` como vigente. Ninguna de las tres cuenta ya
"cuatro columnas no editables". `docs/PROMPT_CABLEADO.md` no tiene el párrafo de `RG-19`: se
comprobó con `python -c "import sys;sys.path.insert(0,'scripts');import inferencia"`, sin error —
`generar_prompt_cableado.py` deriva de `REGLAS` en tiempo de ejecución y `RG-19` ya no está.

### 3.4 Documentos "a mano" de `ESPEC-004` §4

- **`docs/ALCANCE_Y_SUPUESTOS_SGMC.md`**, D-04, líneas 108 y 133: ya no dice "CERRADA en el
  mecanismo" sobre algo que nunca funcionó. Ahora dice que el automático (`RG-19`) nunca funcionó y
  fue sustituido por la marca del técnico.
- **`docs/FUNCIONAL_SGMC.md`** §6.4 (fila de la tabla de "una sola forma por propósito"): reescrita
  para decir que el valor lo pone el técnico, no una fórmula, y por qué la fórmula automática nunca
  funcionó.
- **`Manuales/MANUAL_DE_USUARIO.md`** §3.4 y §5.4: reescritas. §3.4 deja de decir que el supervisor
  "ve cuántos cierres con excepción tiene cada técnico" —ese reporte no existe, `D-12` sigue
  abierta— y lo sustituye por la revisión manual de `Observaciones`/`Motivo de excepción` que
  `ESPEC-004` §6 adopta como paliativo. §5.4 deja de implicar que el umbral se compara solo:
  ninguna regla lo lee.

### 3.5 Documentos generados, re-emitidos

```
python scripts/generar_diccionario_bd.py
python scripts/generar_doc_arquitectura.py
python scripts/generar_manual_despliegue.py
python scripts/generar_prompt_cableado.py
python scripts/generar_prompt_expresiones.py
python scripts/generar_reconstruccion.py
python scripts/generar_reglas_datos.py
python scripts/generar_tipos_esperados.py
python scripts/generar_guia_funcional.py
python scripts/generar_encargo_ventana.py
```
Los diez corrieron sin error. Los tres documentos "no editar" de §2.9
(`generar_tipos_esperados.py`, `scripts/inferencia.py`, `generar_prompt_cableado.py`) se
regeneraron/importaron solos, sin edición, y salieron limpios.

`BD/Modelo_Datos_PLANTILLA.xlsx` se regeneró como efecto colateral de `verificar_reproducible.py`
(que genera dos veces para comparar) — no está en la lista de "documentos generados" de `ESPEC-004`
§4, pero mantenerlo desincronizado del modelo real (con una columna fantasma) sería la misma clase
de cifra envejecida que esta orden existe para evitar. Se acepta el cambio, verificado reproducible
(§5).

## 4. Qué NO se aplicó, y por qué

- **No se tocó el editor de AppSheet ni el Sheets de producción.** Prohibido por el encargo de esta
  sesión. `Precision_GPS` sigue existiendo como columna huérfana en `MAN_Mantenimientos` — es la
  Rama A de `ESPEC-004` §2.10, confirmada por `ACTA-004`, y no es un fallo.
- **No se ejecutaron `P-40` a `P-62` de `PRUEBA-004`** (Familias B, C, D): exigen sesión de
  navegador contra el editor y contra el Sheets — cablear `RG-03` sin `RG-19`, confirmar `Type` de
  `CierreConExcepcion` en `Data > Columns`, fijar su `Description`, y ejercitar el formulario con
  el fixture de `PRUEBA-004` §1.3. Quedan en la cola de sesiones de navegador (§6).
- **No se retipa nada en el editor.** `ACTA-004` §1 ya midió que `CierreConExcepcion` es `Yes/No`
  (no `Text`), así que el riesgo aceptado 1 de `ESPEC-004` §8 está cerrado — no hay nada que
  retipar. Lo que sigue pendiente es un paso de configuración, no de corrección: dejar el campo
  `Editable?` libre otra vez ahora que la `App formula` de `RG-19` (que `ACTA-004` §4bis encontró
  viva) se retira, y fijar `Description`.
- **No se tocaron `ESTADO.md`, `MAP.md`, `CLAUDE.md`, `docs/ROADMAP.md`,
  `docs/CONTEXTO_OPERACION.md` ni `docs/INDICACIONES_POR_ROL.md`**, aunque los seis siguen citando
  `RG-02`/`RG-19`/`Precision_GPS` como si `ESPEC-004` siguiera bloqueada. Ninguno está en la lista
  de `ESPEC-004` §4 ("Documentos generados que se re-emiten" / "A mano, no generados"). Tocarlos
  habría sido "tocar algo que la orden no menciona" — se deja registrado aquí en vez de
  extender el alcance sin autorización. **Van a envejecer mal hasta que alguien los actualice.**
- **No se resolvieron `RG-13` ni `RG-18`** (`ESPEC-004` §5, fuera de alcance desde antes).
- **No se construyó ningún reporte** (`D-12` sigue abierta). El paliativo de `ESPEC-004` §6/§7 —el
  supervisor revisa `Observaciones`/`Motivo de excepción` uno por uno— quedó documentado en el
  manual (§3.4 de arriba), no implementado como mecanismo.
- **No se cerró `PRUEBA-003` `P-09`** (`ESPEC-004` §2.12): sigue sin acta de ejecución en el
  repositorio. `P-40`/`P-41` de `PRUEBA-004` no van a contar como evidencia hasta que se cierre.

## 5. Verificación de cierre

Los ocho verificadores, corridos en este orden, contra el estado tras aplicar `ORDEN-004` (antes de
empezar `ORDEN-006`):

```
$ python scripts/validar_modelo.py; echo "EXIT=$?"
Tablas: 28 | Columnas: 210 | Referencias: 39 | Reglas: 21
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14]
APTO PARA DESPLEGAR
EXIT=0

$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"; echo "EXIT=$?"
AVISOS (2): [F-01] (esperado), [F-04] 14 columnas pendientes de Ref (Fase B)
FASE A CERRADA
EXIT=0

$ python scripts/verificar_documentos.py; echo "EXIT=$?"
Documentos revisados: 40
DOCUMENTOS CONSISTENTES CON EL MODELO (2 avisos, ambos D-04 preexistentes sin relacion con esta orden)
EXIT=0

$ python scripts/verificar_enlaces.py; echo "EXIT=$?"
Documentos revisados: 51 | enlaces relativos: 235
TODOS LOS ENLACES RESUELVEN
EXIT=0

$ python scripts/verificar_reproducible.py; echo "EXIT=$?"
REPRODUCIBLE: las 29 pestanas salen identicas
EXIT=0

$ python scripts/verificar_datos.py; echo "EXIT=$?"
DATOS COHERENTES: 0 obligatorias vacias sin motivo, 0 referencias huerfanas (11 avisos, ninguno sobre RG-02/RG-19/Precision_GPS)
EXIT=0

$ python scripts/verificar_sistema.py; echo "EXIT=$?"
(tras corregir docs/SISTEMA.md: "211 columnas, 23 reglas" -> "210 columnas, 21 reglas")
SIGUE SIENDO VERDAD: 14 afirmaciones comprobadas
EXIT=0

$ python scripts/probar_auditor.py; echo "EXIT=$?"
EL AUDITOR CAZA LOS 6 CASOS
EXIT=0
```

**`verificar_sistema.py` falló primero** (`EXIT=1`, dos afirmaciones ya no ciertas: "211 columnas"
y "23 reglas") porque `docs/SISTEMA.md` citaba las cifras anteriores a esta orden. Se corrigió la
frase (no las cifras sueltas) en `docs/SISTEMA.md` línea 56, y se corrió de nuevo: `EXIT=0`. Queda
como evidencia de que el gate no se maquilló — el fallo real se vio, se corrigió la causa, se
volvió a correr.

## 6. Qué queda pendiente en el editor de AppSheet, para la cola de sesiones de navegador

En el orden que manda `SDD_PIPELINE_SGMC.md` (limpieza → Sheets → *Regenerate* → tipos/claves →
referencias → reglas → verificación), lo que falta de `ESPEC-004`/`PRUEBA-004`:

1. **Quitar la `App formula` de `CierreConExcepcion`.** `ACTA-004` §4bis confirmó que `RG-19` sigue
   puesta, letra por letra. Hay que abrir `Data > Columns > MAN_Mantenimientos > CierreConExcepcion`
   y vaciar el campo `App formula` (con la `X`, no con `Ctrl+Z` — ver el incidente de `ACTA-004` §5).
2. **Resolver la discrepancia de `ACTA-004` §7**: `MotivoExcepcion` — ¿`Required_If` o `Valid_If`?
   Dos sesiones leyeron cosas distintas. Hay que mirar los dos campos en la misma pantalla.
3. **Confirmar que `Description` de `CierreConExcepcion` sigue puesta** tras quitar la `App formula`
   (ya se escribió y se verificó una vez en `ACTA-004` §3, pero conviene recotejar después de tocar
   el campo contiguo).
4. Ejecutar `PRUEBA-004` `P-40` a `P-45` (Familias B, C, D): el fixture de §1.3, con la técnica de
   spoofing de GPS de §1.5, y el discriminador de `PRUEBA-003` `P-09` (pendiente, punto separado).
5. **`PRUEBA-003` `P-09`** (cierre fuera de rango) sobre este despliegue — precondición de todo lo
   anterior, sin acta en el repositorio.

## 7. Reversión

**Del cambio de modelo (esta orden):** revertir el commit de esta orden sobre
`scripts/modelo_objetivo.py` y los ocho scripts de §3.3 devuelve `REGLAS`/`MODELO`/`CAMPOS_RETIRADOS`
a 23/211/13. Como la hoja de producción no se tocó (§4), no hay nada que restaurar en Sheets ni en
AppSheet: revertir el commit basta.

**No aplica ninguna regla de reversión de Sheets/AppSheet** (`Manage > Versions`, restaurar copia)
porque esta orden no tocó ninguno de los dos, siguiendo el mismo criterio que `ORDEN-005` §6.
