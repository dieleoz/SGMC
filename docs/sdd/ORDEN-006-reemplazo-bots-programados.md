# ORDEN-006 — Ejecución de `ESPEC-006` (`RG-08`/`RG-12` retiradas, reemplazadas por `RG-37`/`RG-38`)

## 1. Las tres firmas, verificadas en este momento

| | |
|---|---|
| Cubre | [`ESPEC-006-reemplazo-bots-programados.md`](ESPEC-006-reemplazo-bots-programados.md) y [`PRUEBA-006-reemplazo-bots-programados.md`](PRUEBA-006-reemplazo-bots-programados.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — confirmado vigente con `python scripts/sistema.py` al escribir esta orden |
| Secuencia | Aplicada **después** de `ORDEN-004` en la misma sesión, sobre el repositorio ya con `ORDEN-004` cerrada y verificada (`docs/sdd/ORDEN-004-cierre-excepcion-manual.md`) |

1. **Especificación.** `ESPEC-006`, cerrada el 2026-08-11 en su tercera pasada de arquitecto, bajo
   la vara de `CLAUDE.md` §7.18. Su §8 cierra con cuatro riesgos aceptados y nombrados (prosa
   redundante, ventana de `RG-38` sin confirmar con operación, `QuienCambia` de `Programada` bajo
   supuesto 8, y nueve de diecisiete pruebas sin ejecutar).
2. **Pruebas.** `PRUEBA-006`, rehecha el mismo día. La Familia A (`P-46` a `P-50`) se ejecuta en
   esta orden, de verdad, contra el repositorio real. La Familia B (`P-51` a `P-57`, `P-61`,
   `P-62`) sigue **EJECUTABLE, a la espera de gastar la ventana** — exige el editor de AppSheet y
   crear filas reales en `OT_OrdenesTrabajo`/`PLA_PlanMantenimiento`, que esta orden no toca (§4).
   La Familia C (`P-58`, parte local) se ejecuta aquí sobre `BD/Modelo_Datos_PLANTILLA.xlsx`; su
   contraparte de producción (`P-59`) queda pendiente.
3. **Arquitecto.** Veredicto **CERRADA con cuatro riesgos aceptados** (§8 de `ESPEC-006`). No
   vuelve al arquitecto: *"Lo siguiente que le pase será una `ORDEN-006` y un ejecutor, o nada"*.
4. **Gate objetivo**, corrido en este momento, sobre el estado que dejó `ORDEN-004`:
   ```
   $ python scripts/validar_modelo.py
   Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 21
   ERRORES: ninguno
   AVISOS (3): [V-06] x2, [V-14]
   APTO PARA DESPLEGAR
   ```
   0 errores, línea base contra la que se compara §5.

## 2. Un hecho medido que abarata esta orden, confirmado de nuevo

`ACTA-004` §4ter (medido durante la sesión de `ORDEN-004`, no repetido aquí): `Automation > Bots`
está vacío en el editor — ningún bot de los cinco que el modelo declaraba llegó a crearse. Consecuencia
directa: **retirar `RG-08` y `RG-12` no tiene contrapartida en el editor.** No hay nada que
desmontar en `Automation > Bots`. Esta orden solo cambia `scripts/modelo_objetivo.py` y el dato de
`EOT_EstadosOrden`; no hay ningún bot programado que desactivar primero.

## 3. Qué se aplicó, en orden, y qué devolvió cada paso

### 3.1 `scripts/modelo_objetivo.py` (§4 de `ESPEC-006`)

- **Se retiraron los `dict` de `RG-08` y `RG-12`** de `REGLAS`. Los identificadores no se
  reutilizan — quedan como huecos numéricos, mismo precedente que `ESPEC-004` fijó con
  `RG-02`/`RG-19` (aplicado por `ORDEN-004`, antes en esta misma sesión).
- **Se añadió `RG-37`** (`OT_OrdenesTrabajo`, `App formula` sobre columna **virtual**
  `EstaVencida`, `columna="(tabla)"`, sin `es_label`): misma expresión exacta que tenía `RG-08`
  como bot, `AND([EstadoOrdenID].[EsFinal] = FALSE, [FechaProgramada] < TODAY())`. No escribe, no
  mueve el estado.
- **Se añadió `RG-38`** (`PLA_PlanMantenimiento`, tipo nuevo `"Accion"`, `columna="(tabla)"`):
  expresión `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)` como condición de una vista/slice
  "Vence en 7 días", con la acción de `Data > Actions` descrita en su `descripcion` y el mapeo de
  columnas de `ESPEC-006` §3.3.
- **No se tocó `MODELO`, `RENOMBRADOS`, `CAMPOS_RETIRADOS`, `CLAVE_LEGIBLE` ni `CLAVE_GENERADA`**:
  ninguna tabla ni columna real cambia, tal como manda `ESPEC-006` §4.
- **`es_label=True` en `RG-35`/`RG-36`** ya estaba aplicado desde antes de esta orden (commit
  `0d3d641`/`f790c91`, verificado con `git log -S`) — no fue necesario tocarlo de nuevo.
- **Comentario de `CLAVE_GENERADA`** (línea junto a `OT_OrdenesTrabajo`/`PLA_PlanMantenimiento`)
  actualizado: citaba `RG-10 y RG-12`; ahora cita `RG-10` y "la acción de `RG-38` (antes `RG-12`)".

**Verificado, `P-46`:**
```
$ python -c "
import sys;sys.path.insert(0,'scripts')
from modelo_objetivo import REGLAS
ids=[r['id'] for r in REGLAS]
print(len(REGLAS))
print('RG-08' in ids, 'RG-12' in ids, 'RG-37' in ids, 'RG-38' in ids)
"
21
False False True True
```
El total se queda en 21 (no sube): se retiran dos, se añaden dos. **Difiere del `23`/`25` que
`PRUEBA-006` cita como línea base** porque esta orden corre *después* de `ORDEN-004` en la misma
sesión (que ya había bajado `REGLAS` de 23 a 21 retirando `RG-02`/`RG-19`) — la aritmética del
delta (−2, +2) es la misma, el punto de partida no.

### 3.2 `EOT_EstadosOrden.QuienCambia` — dato, no esquema (§3.1 y §6 de `ESPEC-006`)

Cambiado directamente en `BD/Modelo_Datos_PLANTILLA.xlsx` (archivo del repositorio, no el Sheets de
producción) con `openpyxl`, localizando las filas por `EstadoOrdenID` y no por número de fila:

```
$ python -c "... cambia QuienCambia de 'Vencida' y 'Programada' a 'Supervisor' ..."
('Programada', 'Sistema', 'Supervisor')
('Vencida', 'Sistema', 'Supervisor')
```

**Leído de vuelta, celda por celda, antes de declararlo hecho:**
```
$ python -c "... vuelca EOT_EstadosOrden entera ..."
('EstadoOrdenID', 'Nombre', 'Orden', 'QuienCambia', 'EsFinal', 'Activo')
('Programada', 'Programada', 1, 'Supervisor', 'FALSE', 'TRUE')
('Asignada', 'Asignada', 2, 'Supervisor', 'FALSE', 'TRUE')
('En ejecucion', 'En ejecucion', 3, 'Tecnico', 'FALSE', 'TRUE')
('En revision', 'En revision', 4, 'Tecnico', 'FALSE', 'TRUE')
('Cerrada', 'Cerrada', 5, 'Supervisor', 'TRUE', 'TRUE')
('Suspendida', 'Suspendida', 6, 'Supervisor', 'FALSE', 'TRUE')
('Vencida', 'Vencida', 7, 'Supervisor', 'TRUE', 'TRUE')
```
Exactamente las siete filas de `ESPEC-006` §3.1/§6, con las dos diferencias que pide `PRUEBA-006`
`P-58`, `EsFinal` sin cambiar en ninguna, y ninguna otra celda tocada. **Esto es `P-58` completa**
(la superficie local). `P-59` (la superficie de producción — Sheets de `Modelo_Datos_10082026`) no
se ejecutó: esta orden no toca producción (§4).

**Por qué es seguro editar el `.xlsx` local directamente:** `generar_plantilla.py` usa
`ORIGEN = SALIDA` por defecto (lee su propia salida) y "la garantía de catálogo solo COMPLETA filas
nuevas" (comentario del propio script, línea ~269) — no reescribe una fila de catálogo que ya
existe. Confirmado corriendo `verificar_reproducible.py` después del cambio: regenera dos veces y
las dos salen con `QuienCambia = Supervisor` en las dos filas, así que el valor sobrevive a la
regeneración y no es un artefacto de una sola pasada.

### 3.3 Generadores — verificados uno por uno contra el mecanismo (`inferencia.columnas_virtuales()`/`etiquetas_virtuales()`, no la forma de la regla)

| Consumidor | Qué se verificó | Resultado |
|---|---|---|
| `verificar_documentos.py` (`D-03`) | Usa `inferencia.columnas_virtuales()` para `_VIRTUALES`; captura `RG-37` automáticamente (tipo `App formula`, columna `(tabla)`), sin editar el script | `EstaVencida` exenta de `D-03` sin cambios de código |
| `generar_reconstruccion.py` | Filtra `Show?`/`Label` por `es_label`; `RG-37` no lo tiene | `P-49`: se llama **`EstaVencida`**, sin línea de `Show?`/`Label` (`RG-35`/`RG-36` sí la llevan) |
| `generar_prompt_cableado.py` | Mismo filtro por `es_label` en su Paso 5 | `P-50`: `RG-37`/`RG-38` aparecen en "Paso 4 — Los tipos" (columnas reales que desreferencian), **no** en "Paso 5 — La etiqueta de cada tabla" |
| `generar_encargo_ventana.py` | Usa `inferencia.etiquetas_virtuales()` para el Paso 1 | "Las 2 columnas virtuales `Etiqueta`" — sigue en 2, no 3: `EstaVencida` no es `Etiqueta` |
| `validar_modelo.py` (`V-11`, `V-10`) | `V-11` recorre `REGLAS` sin filtrar por tipo — corrompida la expresión de `RG-37`, detecta el error | `P-48`, confirmado y restaurado (ver §3.4) |
| `alcance_reglas.py` | `columnas_de()` solo añade directo si `columna` no es `(tabla)`/`(varias)`; el resto sale de recorrer la expresión | Sin cambios necesarios (ya lo verificó `ESPEC-006` §2.8 por lectura de código) |

**`generar_prompt_expresiones.py` — el generador que sí necesitaba edición** (`ESPEC-006` §2.8/§6):

1. La línea `w("Afecta a \`RG-10\` y a \`RG-12\`...")` **ya no existía como literal fijo** al
   llegar a esta orden: el commit `18cf528` (autoría de la propia `ESPEC-006`, anterior a esta
   ejecución) ya la había sustituido por una lista derivada de `REGLAS` (`_crean`). Verificado
   leyendo el archivo antes de tocar nada — no hizo falta repetir ese cambio.
2. **Lo que sí faltaba, y se añadió en esta orden:** una sección nueva, separada de "los bots",
   que explica `Data > Actions` sin pasar por `Automation > Bots` para toda regla de tipo
   `"Accion"` (hoy solo `RG-38`, derivado de `REGLAS` — no de un id fijo, para que una segunda
   acción futura la recoja sola). Tres pasos: crear el slice con la condición, crear la acción con
   el mapeo de `ESPEC-006` §3.3, y una advertencia explícita de que **no hay paso 3 en
   `Automation > Bots`**.

**Verificación, `P-39`-equivalente para `RG-10`/`RG-12`:**
```
$ grep -n "RG-10.*RG-12\|Afecta a \`RG-10\` y a \`RG-12\`" docs/PROMPT_EXPRESIONES.md scripts/generar_prompt_expresiones.py
(sin resultado; los dos usos restantes son comentarios historicos del propio script)
$ grep -n "Afecta a" docs/PROMPT_EXPRESIONES.md
Afecta a `RG-10`, que es la que crea órdenes.
```

### 3.4 `validar_modelo.py` — `P-48`

```
$ cp scripts/modelo_objetivo.py /tmp/backup.py
$ python - # sustituye [EstadoOrdenID] por [EstadoOrden] en la expresion de RG-37
$ python scripts/validar_modelo.py
ERRORES (1) - el modelo no se puede desplegar asi:
  x [V-11] RG-37: 'EstadoOrden' no existe en OT_OrdenesTrabajo (ruta EstadoOrden.EsFinal)
$ cp /tmp/backup.py scripts/modelo_objetivo.py
$ python scripts/validar_modelo.py
ERRORES: ninguno
```
Confirma que declarar `RG-37` como `REGLA` (no como columna de `MODELO`) es suficiente para que
`V-11` la valide — mismo patrón que `PRUEBA-005` `P-03` ya estableció para `RG-35`.

### 3.5 `verificar_faseA.py` — `P-47`

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
AVISOS (2): [F-01] OT_OrdenesTrabajo.Activo (esperado), [F-04] 14 columnas pendientes de Ref
FASE A CERRADA
```
Ningún `F-02` menciona `EstaVencida`: la columna virtual no entró en `MODELO`, así que ningún
verificador de esquema la busca en la hoja — confirmado, no solo esperado por diseño.

### 3.6 Documentos generados, re-emitidos

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
Los diez corrieron sin error, con `Reglas: 21` en todos los que citan la cifra.

### 3.7 Documentos "a mano" (§5 de `ESPEC-006`, «vía rápida» tras el cierre)

`ESPEC-006` §5 no los aplica ella misma pero los señala como corrección de redacción derivada de
una decisión ya tomada, "una vez esta especificación se apruebe" — que es exactamente el momento en
que corre esta orden:

- **`docs/FUNCIONAL_SGMC.md` §4**: la tabla `QuienCambia` (`Programada → Sistema`, `Vencida →
  Sistema`) se reescribió a `Supervisor` en las dos, con un recuadro nuevo explicando que `RG-08`
  nunca corrió (bots programados no se ejecutan en la cuenta gratuita) y que `Vencida` pasó a ser
  una decisión del supervisor, no una consecuencia automática.
- **`docs/ALCANCE_Y_SUPUESTOS_SGMC.md` D-06**: la fila de la tabla de decisiones se amplió para
  decir que `Vencida` ya no es automática y por qué.
- **`docs/ROADMAP.md`**: varias menciones puntuales corregidas — el recuadro "Los 5 bots" (ahora
  "Los 3 bots por evento, y los dos programados que se retiraron", con nota de resolución antes y
  después del análisis histórico, que se conserva); la tabla "Espera / Deja sin poder ponerse" con
  columna `Estado` nueva marcando `ESPEC-004` y `ESPEC-006` como **Aplicada**; los conteos "23
  reglas"/"5 bots"/"2 columnas virtuales"/"10 reglas desreferencian" corregidos a los valores que
  hoy imprime el comando correspondiente (21 / 3 por evento + 1 acción / 3 / 12).

## 4. Qué NO se aplicó, y por qué

- **No se tocó el editor de AppSheet.** Prohibido por el encargo de esta sesión, y sin
  contrapartida que desmontar de todas formas (§2): `Automation > Bots` está vacío.
- **No se tocó el Sheets de producción `Modelo_Datos_10082026`.** El cambio de `QuienCambia` se
  aplicó solo a `BD/Modelo_Datos_PLANTILLA.xlsx` (repositorio). `PRUEBA-006` `P-59` (la lectura de
  vuelta contra producción) queda pendiente — es la mitad del punto 5 del encargo de `ESPEC-006`
  que esta orden no cierra.
- **No se creó ninguna fila en `OT_OrdenesTrabajo`, `MAN_Mantenimientos` ni
  `PLA_PlanMantenimiento`.** Esta orden no ejecutó ninguna acción de escritura contra la aplicación
  ni contra el Sheets — no hay ruta por la que hubiera podido crear una fila ahí. `PRUEBA-006`
  `P-51` a `P-57`, `P-61`, `P-62` (Familia B, toda ella) quedan **EJECUTABLES, a la espera de la
  decisión de gastar la ventana barata** (`ESPEC-006` §8, riesgo aceptado 4) — no ejecutadas por
  esta orden. Ver §7 sobre cómo se sabe si la ventana sigue abierta.
- **No se cableó `RG-37` ni `RG-38` en el editor.** Sin eso, `EstaVencida` no existe como columna
  virtual real y la acción de `RG-38` no existe como botón: son solo texto en `REGLAS` hasta que
  alguien abra `Data > Columns`/`Data > Actions`.
- **No se confirmó con operación la ventana de 7 días de `RG-38`** (`ESPEC-006` §8, riesgo
  aceptado 2) ni el supuesto sobre `RG-10`/`Programada` (riesgo aceptado 3). Siguen como supuestos
  refutables, sin acción de esta orden.
- **No se tocó `scripts/faseA_sheets.gs`.** `ESPEC-006` §2.2 ya decidió conservarlo con su banner
  de retiro, sin referencias vivas; esta orden no reabre esa decisión.
- **No se persiguió cada mención residual de "23 reglas" o "5 bots" en todo el repositorio.** Se
  corrigieron las de `docs/ROADMAP.md`, `docs/FUNCIONAL_SGMC.md` y
  `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (§3.7, con mandato explícito de `ESPEC-006` §5). Otros
  documentos que citen cifras antiguas de `REGLAS` (`ESTADO.md`, `MAP.md`, `CLAUDE.md`,
  `docs/CONTEXTO_OPERACION.md`, `docs/INDICACIONES_POR_ROL.md`) no están en esa lista y no se
  tocaron — mismo criterio de disciplina de alcance que `ORDEN-004` §4.

## 5. Verificación de cierre

Los ocho verificadores, corridos en este orden, contra el estado final (`ORDEN-004` + `ORDEN-006`
aplicadas):

```
$ python scripts/validar_modelo.py; echo "EXIT=$?"
Tablas: 28 | Columnas: 210 | Referencias: 39 | Reglas: 21
ERRORES: ninguno
AVISOS (3): [V-06] x2, [V-14]
APTO PARA DESPLEGAR
EXIT=0

$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"; echo "EXIT=$?"
AVISOS (2): [F-01] (esperado), [F-04] 14 columnas pendientes de Ref
FASE A CERRADA
EXIT=0

$ python scripts/verificar_documentos.py; echo "EXIT=$?"
Documentos revisados: 41
DOCUMENTOS CONSISTENTES CON EL MODELO (2 avisos, ambos D-04 preexistentes, sin relacion con esta orden)
EXIT=0

$ python scripts/verificar_enlaces.py; echo "EXIT=$?"
Documentos revisados: 52 | enlaces relativos: 238
TODOS LOS ENLACES RESUELVEN
EXIT=0

$ python scripts/verificar_reproducible.py; echo "EXIT=$?"
REPRODUCIBLE: las 29 pestanas salen identicas (incluye la EOT_EstadosOrden con QuienCambia=Supervisor)
EXIT=0

$ python scripts/verificar_datos.py; echo "EXIT=$?"
DATOS COHERENTES: 0 obligatorias vacias sin motivo, 0 referencias huerfanas (11 avisos, ninguno sobre RG-08/RG-12/EstaVencida)
EXIT=0

$ python scripts/verificar_sistema.py; echo "EXIT=$?"
SIGUE SIENDO VERDAD: 15 afirmaciones comprobadas
EXIT=0

$ python scripts/probar_auditor.py; echo "EXIT=$?"
EL AUDITOR CAZA LOS 6 CASOS
EXIT=0
```

**Ninguno de los ocho falló esta vez** — a diferencia de `ORDEN-004`, donde `verificar_sistema.py`
sí detectó una cifra desactualizada (`docs/SISTEMA.md`). Para `ORDEN-006`, `docs/SISTEMA.md` ya
decía "210 columnas, 21 reglas" (corregido durante `ORDEN-004`) y esta orden no cambia ninguna de
las dos cifras (retira 2 reglas, añade 2), así que no había nada que `verificar_sistema.py` pudiera
cazar aquí. Se corrió igual, sin dar por sentado que seguiría en verde.

## 6. Qué queda pendiente en el editor de AppSheet, para la cola de sesiones de navegador

En el orden que manda `SDD_PIPELINE_SGMC.md`:

1. **Cablear `RG-37`.** `Data > Columns > OT_OrdenesTrabajo > Add virtual column`, nombre
   `EstaVencida`, tipo `Yes/No`, `App formula` con la expresión de `RG-37` (copiarla literal de
   `docs/PROMPT_EXPRESIONES.md`, no de memoria), `Show?` activo.
2. **Crear la vista "Órdenes vencidas"** sobre `OT_OrdenesTrabajo`, condición
   `[EstaVencida] = TRUE`, visible para el rol Supervisor (`ESPEC-006` §3.2).
3. **Cablear `RG-38`:** `Data > Slices` con la vista "Vence en 7 días" sobre
   `PLA_PlanMantenimiento` (condición `AND([Activo] = TRUE, [ProximaFecha] <= TODAY() + 7)`),
   después `Data > Actions` con la acción de `Set these columns` (mapeo de `ESPEC-006` §3.3). **No**
   se pasa por `Automation > Bots`.
4. **Aplicar `QuienCambia = Supervisor`** en las filas `Vencida` y `Programada` de
   `EOT_EstadosOrden` en el Sheets de producción `Modelo_Datos_10082026` — ya aplicado en el
   `.xlsx` local (§3.2), pendiente en producción. Es la mitad que falta de `PRUEBA-006` `P-59`.
5. **Precondición antes de crear cualquier fixture:** desactivar `RG-07` (`Automation > Bots` →
   `RG-07` → `Disable`) para no disparar correos reales a `ivan.salcedo@concesiondelsisga.com.co`,
   y reactivarlo al terminar (`PRUEBA-006` `P-60`, último paso).
6. **Ejecutar `PRUEBA-006` `P-51` a `P-62`** (Familia B y las de cotejo a ojo de Familia D): el
   fixture de tres filas en `OT_OrdenesTrabajo` (positiva `RG-37`, dos negativas), una fila en
   `MAN_Mantenimientos` (cierre de la positiva, `P-55`, la prueba de mayor peso: confirma que
   `EstaVencida` no bloquea el cierre), y el ejercicio de la acción de `RG-38` sobre
   `PLA_PlanMantenimiento`. **Esto gasta la ventana barata para siempre** — `OT_OrdenesTrabajo` y
   `MAN_Mantenimientos` dejan de estar en cero en cuanto se ejecuta.
7. **`PRUEBA-006` `P-59`**: confirmar por API y por Drive que `QuienCambia = Supervisor` llegó a
   producción, en las dos filas.

## 7. Reversión

**Del cambio de modelo (esta orden):** revertir el commit de esta orden sobre
`scripts/modelo_objetivo.py` y los generadores de §3.3 devuelve `REGLAS` a 21 con `RG-08`/`RG-12`
en vez de `RG-37`/`RG-38`.

**Del dato de `EOT_EstadosOrden.QuienCambia`:** revertir el commit basta para el `.xlsx` local
—es un archivo versionado—. Como el Sheets de producción no se tocó (§4), no hay nada que revertir
ahí.

**No aplica ninguna regla de reversión de Sheets/AppSheet** (`Manage > Versions`, restaurar copia)
porque esta orden no tocó ninguno de los dos, mismo criterio que `ORDEN-004` §7 y `ORDEN-005` §6.

**Sin datos que perder, hasta donde este repositorio puede verlo sin tocar producción.** Las tres
tablas de movimiento que este cambio afecta (`OT_OrdenesTrabajo`, `MAN_Mantenimientos`,
`PLA_PlanMantenimiento`) están en cero en `BD/Modelo_Datos_PLANTILLA.xlsx`, confirmado con
`openpyxl` en esta sesión — pero ese archivo vacía esas tablas **por diseño**
(`VOLCADO_CIEGO_A`, `scripts/lectura_de_vuelta.py`) sea cual sea el estado real de producción, así
que no es evidencia de producción. La evidencia de producción es `docs/sdd/ACTA-005-pruebas.md`
(`P-09`) y `docs/sdd/ESPEC-006-reemplazo-bots-programados.md` §2.9, que sí leyeron por API el
2026-08-11 y encontraron las ocho tablas de `VOLCADO_CIEGO_A` en cero — anterior a esta orden, que
no creó ninguna fila y por tanto no cambia ese hecho, pero que tampoco lo remidió por API. Quien
ejecute §6 debería confirmarlo de nuevo con `python scripts/instantanea.py` antes de gastar la
ventana, no asumirlo de esta acta.
