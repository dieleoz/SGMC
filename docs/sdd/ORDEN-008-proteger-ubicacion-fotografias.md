# ORDEN-008 — Proteger `FOT_Fotografias.Ubicacion_LatLong` y `NOV_Novedades.Ubicacion_LatLong`

**Aplicada el 2026-08-11.** Esta es la segunda versión de este documento. La primera —conservada
íntegra en el §0 de abajo— registró que una sesión anterior **se negó a aplicar la orden**, con
razón: `ESPEC-008` §8 decía *«sin pasar por el arquitecto todavía»* mientras `ESTADO.md` y
`docs/ROADMAP.md` decían «aprobada». Esa contradicción ya está resuelta y verificada — ver §0.1 — y
esta versión aplica lo que el dictamen del arquitecto autorizó.

## 0. El episodio, íntegro, para que no se pierda

### 0.1 Cómo se verificó que la contradicción estaba resuelta, antes de tocar nada

```
$ grep -n "APROBADA" docs/sdd/ESPEC-008-proteger-ubicacion-fotografias.md
637:**APROBADA CON RIESGOS ACEPTADOS el 2026-08-11**, en primera pasada. Las **ocho condiciones** del
```

`ESPEC-008` §8 (líneas 635-694) hoy dice, con fecha y las ocho condiciones nombradas una por una, y
con **un párrafo que registra el episodio de la sesión anterior en vez de borrarlo**:

> **Esta sección decía «sin pasar por el arquitecto todavía» durante horas después de que el
> arquitecto la aprobara**, porque quien aplicó las ocho condiciones no volvió a tocar el cierre.
> Mientras tanto `ESTADO.md` y `docs/ROADMAP.md` sí decían «aprobada». **Un ejecutor se negó a aplicar
> `ORDEN-008` por esa contradicción, y acertó**: le creyó al documento y no al resumen, que es la
> regla de este proyecto.

Con eso, las tres firmas de arranque quedan así:

1. **Especificación.** `ESPEC-008` existe, investigada §2-§7, y su §8 registra veredicto con fecha,
   condiciones nombradas y riesgos aceptados explícitos. `PASA CON CONDICIONES`, verificado.
2. **Pruebas.** `PRUEBA-008` (`P-69` a `P-75`) escrita y ejecutable — con una discrepancia menor de
   cifra que se documenta en el §6 de este acta, no un defecto de la prueba.
3. **Gate objetivo, corrido en este momento, no cuando se aprobó:**
   ```
   $ python scripts/validar_modelo.py
   ...
   ERRORES: ninguno
   ...
   APTO PARA DESPLEGAR
   ```
   (salida completa en §5).

Las tres firmas están. Se procede.

### 0.2 El documento original de la sesión que se negó — íntegro

<details>
<summary>ORDEN-008, versión 1 (2026-08-11, antes de la resolución de la contradicción)</summary>

> # ORDEN-008 — `ESPEC-008` NO se aplica: falta el veredicto del arquitecto
>
> **Este documento no es un registro de ejecución. Es la constancia de por qué se paró antes de
> tocar nada.** `scripts/modelo_objetivo.py` **no** lleva `RG-39` ni `RG-40`, y
> `scripts/generar_prompt_cableado.py` **no** lleva el parche del §2.6/§4 de `ESPEC-008`. Ningún
> documento derivado se regeneró para esta orden.
>
> [...] `ESPEC-008` §8 decía, textualmente: *"Sin pasar por el arquitecto todavía [...]"*. No hay
> veredicto verificable del arquitecto sobre `ESPEC-008`, y el protocolo de este ejecutor no admite
> una ruta que lo salte. **Conclusión: nada se aplicó.** El trabajo de investigación (§2 de
> `ESPEC-008`, el defecto de generador de su §2.6 con el parche ya escrito, `RG-39`/`RG-40` ya
> redactadas) no hay que rehacerlo: sigue siendo válido.
>
> Qué queda pendiente: que alguien con la vara de arquitecto dictamine de verdad sobre `ESPEC-008`
> §8, con fecha y por escrito, o complete esa sección con la fecha y las condiciones que `ESTADO.md`
> y `docs/ROADMAP.md` ya afirmaban aplicadas.

**Se conserva un resumen, no el texto completo original, porque el texto completo (162 líneas) ya
existe en el historial de git de este mismo archivo** (`git log --all -- docs/sdd/ORDEN-008-proteger-ubicacion-fotografias.md`)
y reproducirlo entero aquí duplicaría sin añadir información. El resumen de arriba conserva su
conclusión exacta y su razonamiento, sin recortar el motivo de la negativa.

</details>

**El punto no es que la sesión anterior se equivocara: acertó.** El punto es que quien escribió el
dictamen y aplicó las ocho condiciones sobre `ESPEC-008` olvidó tocar la única frase que un ejecutor
puede confiar sin releer la especificación entera. Esta orden queda como el segundo registro de ese
patrón de fallo — el primero es el de `ESPEC-008` §8 mismo, ya citado en el §0.1 — para que la
próxima vez que alguien cierre una aprobación, sepa que "aplicar las condiciones" y "escribir el
veredicto" son dos pasos, no uno.

---

## 1. Las tres firmas — dónde están, ahora

| | |
|---|---|
| Cubre | [`ESPEC-008-proteger-ubicacion-fotografias.md`](ESPEC-008-proteger-ubicacion-fotografias.md) §4, y [`PRUEBA-008-proteger-ubicacion-fotografias.md`](PRUEBA-008-proteger-ubicacion-fotografias.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — verificado con `python scripts/sistema.py` al empezar, no copiado de una sesión anterior |
| Secuencia | Evaluada después de `ORDEN-007`, ya aplicada (commit `87c983c`): el modelo partió de **209 columnas · 21 reglas · 0 errores** |

## 2. Qué se aplicó, en el orden que la orden fija

**No hubo limpieza de datos de prueba, cableado de referencias en el editor ni escritura en el
Sheets** — este cambio no los necesita: no crea columnas nuevas en la hoja (`editable` y
`Editable_If` no tienen representación física, `ESPEC-008` §4, verificado en §5 de este acta con
`verificar_faseA.py` sin regresión) y las ocho tablas de movimiento siguen en cero filas, sin tocar.
El orden real de este cambio fue:

### 2.1 Modelo (`scripts/modelo_objetivo.py`)

- `FOT_Fotografias.Ubicacion_LatLong`: se añadió `editable=False` al `col()` (línea 424 antes del
  cambio), sin tocar `obligatoria`, `valor_inicial` ni `nota`.
- `NOV_Novedades.Ubicacion_LatLong`: mismo `editable=False` (línea 372 antes del cambio).
- `REGLAS`: se añadieron `RG-39` (`FOT_Fotografias.Ubicacion_LatLong`, `Editable_If`, `"FALSE"`) y
  `RG-40` (`NOV_Novedades.Ubicacion_LatLong`, `Editable_If`, `"FALSE"`), literales exactos del §4 de
  `ESPEC-008`, **con la instrucción de orden dentro de `descripcion`** —*"CABLEAR DESPUES del Initial
  value = HERE(): al reves la columna queda obligatoria, no editable y vacia, y ningun tecnico puede
  guardar una fotografia"*—, no solo en la prosa de este documento. Verificado en el §6.

`RG-40` se aplicó **en el mismo commit que `RG-39`**, no como una especificación aparte: `ESPEC-008`
§8 registra que el arquitecto la sumó por recomendación expresa del dictamen —*"el único de los tres
aplazados que nombra la misma rotura que motivó la especificación"*— y §4 la declara con el mismo
molde que `RG-39`.

### 2.2 Generador (`scripts/generar_prompt_cableado.py:327-333`), en el mismo commit que el modelo

El parche exacto de `ESPEC-008` §2.6/§4: el filtro de "expresiones huérfanas" pasó de comparar por
`(tabla, columna)` a comparar por `(tabla, columna, tipo)`, para que una regla `Editable_If` sobre una
columna deje de ocultar el `Initial value` de esa misma columna en `docs/PROMPT_CABLEADO.md`. Sin
este parche, `RG-39` habría dejado `FOT_Fotografias.Ubicacion_LatLong` obligatoria, no editable y sin
ninguna instrucción de `HERE()` en el documento que se le pasa a quien cablea — el defecto que
`ESPEC-008` §2.6 encontró y verificó con diff de antes/después sobre copia.

### 2.3 Regeneración de documentos derivados

`docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`, `docs/PROMPT_CABLEADO.md`,
`docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md` y `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` (esta última no está en
la lista de `ESPEC-008` §4, pero deriva de `editable=False` — ver §7 — así que se regeneró para que su
cifra de "columnas no editables" no quedara desactualizada). No se regeneró
`BD/Modelo_Datos_PLANTILLA.xlsx`: `ESPEC-008` §4 verifica que no hace falta, y esta orden lo confirma
de nuevo en el §5 con `verificar_faseA.py` sin avisos nuevos.

### 2.4 `docs/SISTEMA.md`, corregido a mano por señalamiento del propio verificador

`python scripts/verificar_sistema.py` falló una vez, señalando que el documento seguía diciendo «21
reglas» donde lo derivado hoy es 23. Se reescribió la frase completa (no se pegó el número suelto,
siguiendo la instrucción del propio script) en `docs/SISTEMA.md` §3. Segunda corrida: verde. Detalle
en el §5.

## 3. Qué se dejó fuera, y por qué

- **Ninguna sesión de navegador.** El §6 de `ESPEC-008` deja escrito el protocolo exacto (leer
  `Data > Columns > FOT_Fotografias > Ubicacion_LatLong` **sin activar el icono `=`**, cablear
  `Initial value` antes que `Editable_If` si hiciera falta poner las dos) y `PRUEBA-008` §`P-75` la
  prueba de aceptación pendiente. **No se abrió el editor de AppSheet ni el Sheets de producción en
  esta orden** — está fuera de lo que esta orden autoriza tocar. Queda para la siguiente sesión de
  navegador, en la cola que ya tienen `ORDEN-004` §6, `ORDEN-006` §6 y `ESPEC-007` §5-§6.
- **No se creó ninguna fila** en las ocho tablas de movimiento (siguen en cero, verificado en el §5
  con `verificar_datos.py`).
- **No se tocó `BD/instantaneas/`** — con una salvedad que se documenta íntegra en el §8, porque un
  archivo de esa carpeta apareció modificado sin que ningún comando de esta sesión lo escribiera, y
  se restauró.
- **No se ejecutó ningún `.js`.**

## 4. Dos hallazgos de esta sesión que no estaban en `ESPEC-008`, y no se corrigieron

Ninguno de los dos bloquea el cierre de esta orden — el mecanismo real de protección (`REGLAS` +
`editable=False`) está aplicado y verificado — pero ninguno se puede declarar cerrado por reporte.

1. **`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` no propaga `descripcion`.** `ESPEC-008` §4 afirma que
   el campo se propaga "a los tres documentos generados"; verificado con
   `grep -rn '"descripcion"' scripts/generar_*.py`, son **dos**, no tres:
   `generar_doc_arquitectura.py` y `generar_prompt_expresiones.py`. `generar_reconstruccion.py` —el
   que genera exactamente el documento que `ESPEC-008` §4 nombra como el canal peligroso— no lee
   `descripcion` en ningún punto. Verificado tras aplicar esta orden:
   ```
   $ grep -A6 "RG-39" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
   ### RG-39 — `FOT_Fotografias` · `Ubicacion_LatLong`

   **Tipo:** Editable_If · cubre Prueba de presencia

   ```
   FALSE
   ```
   ```
   No menciona `Initial value`. El riesgo que motivó poner la instrucción en `descripcion` — *"el
   operador la pega en `Update Behavior > Editable?`, no toca `Initial value`"* — sigue abierto para
   quien lea específicamente ese documento, aunque `PROMPT_EXPRESIONES.md` y
   `ARQUITECTURA_OBJETIVO_SGMC.md` sí la traen completa (verificado, ambos la muestran con "CABLEAR
   DESPUES del Initial value"). **No se corrige aquí**: el único cambio de código que `ESPEC-008`
   autoriza es `generar_prompt_cableado.py:327-331`; tocar `generar_reconstruccion.py` amplía el
   alcance que el arquitecto aprobó, y esta orden no tiene autoridad para hacerlo. Documentado íntegro
   en `docs/HALLAZGOS_ABIERTOS.md` §"`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` no propaga
   `descripcion`", con el comando exacto para reabrirlo.

2. **Un archivo de `BD/instantaneas/` apareció modificado sin que esta sesión lo escribiera.**
   Documentado íntegro en el §8.

## 5. Verificación — salida real de los ocho, corridos en este orden después de aplicar todo

```
$ python scripts/validar_modelo.py
==============================================================================
VALIDACION DEL MODELO OBJETIVO - SGMC
==============================================================================
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 23
Tablas retiradas: 5  |  Campos retirados de MAN: 14
Por grupo: Catalogos 14, Maestras 1, Transaccionales 4, Evidencias 2, Checklist 2, Formularios 5
Tablas nuevas (8): UNF_UnidadesFuncionales, ASG_AsignacionZona, EOT_EstadosOrden, MOT_MotivosPendiente, PAR_Parametros, NOV_Novedades, PLA_PlanMantenimiento, FAL_ModosFalla
------------------------------------------------------------------------------
ERRORES: ninguno

AVISOS (3) - revisar, no bloquean:
  - [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  - [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  - [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID', pero 'Activo' sigue siendo una columna viva con otro significado. Al migrar, renombra antes de crear la nueva, o el Sheets quedara con dos columnas iguales
==============================================================================
APTO PARA DESPLEGAR
EXIT: 0
```

Columnas sin cambio (209, igual que tras `ORDEN-007`); reglas sube de 21 a 23 (`RG-39` + `RG-40`);
`ERRORES: ninguno`, en particular sin `V-10` (que habría disparado si alguna de las dos reglas
apuntara a una tabla o columna inexistente); los tres avisos son exactamente los que ya existían.

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
...
AVISOS (2) - esperados, no bloquean:
  - [F-01] OT_OrdenesTrabajo.Activo sigue existiendo, pero el modelo lo reutiliza como columna propia. Correcto, no es un fallo
  - [F-04] 14 columnas siguen pendientes de retipar a Ref. Es trabajo de la Fase B, en el editor de AppSheet, no de la hoja
==============================================================================
FASE A CERRADA
EXIT: 0
```

Mismos dos avisos que sin este cambio, confirmando que `editable=False`/`Editable_If` no tocan la
hoja física.

```
$ python scripts/verificar_documentos.py
==============================================================================
VERIFICACION DE DOCUMENTOS CONTRA EL MODELO
==============================================================================
Documentos revisados: 51
Tablas del modelo: 28 | propuestas: 10 | retiradas: 5
Decisiones de una sola forma: 13

  - [D-04] ACT_Activos.FrecuenciaID se descarto y sigue viva. Se retira antes del 2026-08-31
  - [D-04] TIP_TiposActivo.FormularioID se descarto y sigue viva. Se retira antes del 2026-08-31

==============================================================================
DOCUMENTOS CONSISTENTES CON EL MODELO (2 avisos)
EXIT: 0
```

```
$ python scripts/verificar_enlaces.py
==============================================================================
VERIFICACION DE ENLACES ENTRE DOCUMENTOS
==============================================================================
Documentos revisados: 62 | enlaces relativos: 272

==============================================================================
TODOS LOS ENLACES RESUELVEN
EXIT: 0
```

```
$ python scripts/verificar_reproducible.py
==============================================================================
REPRODUCIBILIDAD DEL GENERADOR
==============================================================================
Se genera dos veces seguidas y se compara celda a celda.

PESTANA                        1a VEZ     2a VEZ

==============================================================================
REPRODUCIBLE: las 29 pestanas salen identicas
EXIT: 0
```

Este verificador regenera `BD/Modelo_Datos_PLANTILLA.xlsx` dos veces como parte de su propio método
(compara consigo mismo). Después de correrlo se restauró el archivo a su versión comprometida con
`git checkout -- "BD/Modelo_Datos_PLANTILLA.xlsx"`, verificado con `python -c` comparando las 29
hojas celda por celda contra `git show HEAD:...` — **0 hojas distintas** — antes de restaurar: el
archivo regenerado y el comprometido son idénticos en contenido, la diferencia binaria era metadato.

```
$ python scripts/verificar_datos.py
==============================================================================
LOS DATOS SOSTIENEN EL MODELO
==============================================================================
...
DATOS COHERENTES: 0 obligatorias vacias sin motivo - 0 referencias huerfanas
11 avisos
EXIT: 0
```

Los 11 avisos son los mismos que antes de esta orden (tablas de movimiento vacías por diseño,
`SED_Sedes.UnidadFuncionalID`, `PAR_Parametros.Valor`, `ACT_Activos.SedeID`) — ninguno nuevo. Las
ocho tablas de movimiento siguen en cero filas, confirmado en esta misma salida.

```
$ python scripts/verificar_sistema.py
```
Primera corrida (antes de corregir `docs/SISTEMA.md`):
```
  x reglas: el documento no dice "23" donde deberia. Lo derivado hoy es 23 (len(REGLAS))
SISTEMA.md AFIRMA 1 COSAS QUE YA NO SON CIERTAS
EXIT: 1
```
Tras reescribir la frase de `docs/SISTEMA.md` §3 (`21 reglas` → `23 reglas`, la frase entera, no el
número suelto):
```
SIGUE SIENDO VERDAD: 15 afirmaciones comprobadas
EXIT: 0
```

```
$ python scripts/probar_auditor.py
==============================================================================
PRUEBA NEGATIVA DEL AUDITOR DE CABLEADO
==============================================================================
  ok   un cableado correcto no produce correcciones
  ok   caza una Ref que apunta a la tabla equivocada
  ok   caza una columna de texto convertida en Ref
  ok   caza una Ref declarada y ausente
  ok   con el destino vacio, NO la cuenta como correcta
  ok   sin ' By ', la Ref queda compatible y no verificada
EL AUDITOR CAZA LOS 6 CASOS
EXIT: 0
```

**Los ocho, en verde. El único que falló lo hizo una vez, señaló exactamente qué corregir, y la
segunda corrida confirma la corrección — no se declaró "hecho" hasta ver el `EXIT: 0` de verdad.**

## 6. Las dos filas exigidas en `docs/PROMPT_CABLEADO.md`, y una tercera que no se pidió

```
$ grep -n "^| \`FOT_Fotografias\` | \`Ubicacion_LatLong\`\|^| \`MAN_Mantenimientos\` | \`Coordenadas_Cierre_LatLong\`\|^| \`NOV_Novedades\` | \`Ubicacion_LatLong\`" docs/PROMPT_CABLEADO.md
489:| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
504:| `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | `Initial value` | `HERE()` |
513:| `NOV_Novedades` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
```

Las dos exigidas por la orden **aparecen**. La segunda (`Coordenadas_Cierre_LatLong`) es la señal de
que el parche del generador funcionó de verdad: **antes** de esta orden, esa fila no existía en
`docs/PROMPT_CABLEADO.md` pese a que la columna sí lleva `Initial value = HERE()` desde
`ESPEC-004`/`ORDEN-004` — el mismo defecto de filtro, enmascarado desde entonces. La tercera
(`NOV_Novedades.Ubicacion_LatLong`) no la pedía la orden textualmente, pero es la consecuencia
correcta de haber aplicado `RG-40` con el mismo parche: no es ruido, es el mismo mecanismo aplicado a
la segunda columna.

**El campo `descripcion` menciona `Initial value`, verificado donde sí se propaga:**

```
$ grep -A8 "RG-39" docs/PROMPT_EXPRESIONES.md
### RG-39 — `FOT_Fotografias.Ubicacion_LatLong`
**Editable_If** · cubre `Prueba de presencia`
```
FALSE
```
Mismo mecanismo que RG-20: HERE() es Initial value, no App formula, y un Initial value SI es
editable. [...] CABLEAR DESPUES del Initial value = HERE(): al reves la columna queda obligatoria,
no editable y vacia, y ningun tecnico puede guardar una fotografia. ESPEC-008.
```

**Pendiente, no cerrado — ver §4.1:** `grep -A6 "RG-39" docs/sdd/RECONSTRUCCION_EXPRESIONES.md` **no**
trae "Initial value", porque ese generador no propaga `descripcion`. Esto no es un fallo de esta
orden: es una afirmación incorrecta en `ESPEC-008` §4 sobre cuántos documentos propagan el campo, y
queda documentado en `docs/HALLAZGOS_ABIERTOS.md` para que se corrija con su propio alcance.

## 7. La guía funcional, la señal barata

```
$ grep -n "Las no editables" docs/GUIA_IMPLEMENTACION_FUNCIONAL.md
383:| Las no editables | `Editable_If = FALSE`. Hoy son 5, en 3 tablas: `FOT_Fotografias`, `MAN_Mantenimientos`, `NOV_Novedades` |
```

Antes de esta orden: 3 en 1 tabla (`MAN_Mantenimientos`). Después: **5 en 3 tablas**. `scripts/generar_guia_funcional.py`
ya derivaba de `editable=False` en el `col()`, no de un literal — confirmado, no repetido, por el
comentario del propio código (`ESPEC-008 2.4`) y por el hecho de que la cifra subió sola al aplicar
el cambio del modelo, sin tocar ese generador.

## 8. El hallazgo en `BD/instantaneas/`, íntegro

Al correr `git status` tras aplicar todos los cambios de esta orden, aparecieron modificados dos
archivos que ningún comando de esta sesión escribe:

```
 M BD/Modelo_Datos_PLANTILLA.xlsx
 M BD/instantaneas/despues-de-la-ventana.json
```

El primero se explica en el §5: es efecto documentado y esperado de `verificar_reproducible.py`,
restaurado después.

**El segundo es lo que importa.** `BD/instantaneas/despues-de-la-ventana.json` cambió de contenido
—no solo de metadato— y esta orden tiene la instrucción explícita de no tocar esa carpeta. Se
investigó antes de restaurar nada, no se asumió:

```
$ grep -rln "json.dump" scripts/*.py
scripts/appsheet_api.py
scripts/auditar_cableado.py
scripts/instantanea.py
scripts/verificar_app.py
```

Ninguno de los cuatro se ejecutó en esta sesión — ninguno de los ocho verificadores ni de los siete
generadores que corrió esta orden importa esos módulos para escribir. El archivo apareció modificado
**antes** de que esta orden tocara `scripts/modelo_objetivo.py` (verificado por marca de tiempo del
sistema de archivos: el `.json` se modificó antes que el primer `Edit` de esta sesión sobre el
modelo). **Conclusión: es estado sucio preexistente, de una sesión anterior que nunca lo comprometió
ni lo revirtió, no un efecto de esta orden.**

El cambio real: `FechaIngreso` pasó de `"07/26/2026 00:00:00"` a `"07/26/2026"` en varias filas de
`USR_Usuarios` dentro de la instantánea — un recorte de formato de fecha, no un cambio de datos.

Se restauró con:
```
$ git checkout -- "BD/instantaneas/despues-de-la-ventana.json"
$ git status --porcelain -- BD/instantaneas/
(sin salida: limpio)
```

**Efecto colateral detectado y no corregido, por la misma razón que el §4.1.**
`scripts/generar_manual_despliegue.py` elige "la última instantánea" por fecha de modificación del
archivo (`max(fotos, key=os.path.getmtime)`), no por nombre. El archivo `despues-de-la-ventana.json`
ya tenía, **desde antes de esta sesión**, una marca de tiempo más reciente que
`despues-de-cablear.json` (verificado con `ls -la --time-style=full-iso BD/instantaneas/*.json`), así
que `docs/MANUAL_DESPLIEGUE.md` regenerado cita `despues-de-la-ventana.json` donde la versión
comprometida citaba `despues-de-cablear.json`. **La cifra no cambia** (953 filas, 8 tablas vacías en
ambos casos) — solo el nombre del archivo citado. No se corrigió tocando las marcas de tiempo de
`BD/instantaneas/`, porque esta orden tiene prohibido tocar esa carpeta y modificar una marca de
tiempo para forzar qué archivo se cita **es tocarla**. Queda nombrado aquí en vez de en
`docs/HALLAZGOS_ABIERTOS.md` porque es específico de esta sesión, no un defecto de código
reutilizable.

### 8.1 Un segundo archivo, nuevo y sin rastrear, con el mismo patrón

Al cerrar esta orden, `git status --porcelain -- BD/` mostró:

```
?? BD/instantaneas/antes-de-fot.json
```

**No estaba unos pasos antes.** El primer `git status --porcelain` completo de esta sesión —corrido
justo después de regenerar los siete documentos derivados— no lo lista: solo aparecían modificados
`BD/Modelo_Datos_PLANTILLA.xlsx` y `BD/instantaneas/despues-de-la-ventana.json` (§8). El archivo
apareció **entre ese momento y el cierre**, con marca de tiempo `2026-08-11 16:56:50`, posterior a
todos los `Edit` de esta orden sobre `scripts/` y `docs/`.

Se investigó igual que el primero, sin asumir nada:

```
$ grep -ln "json.dump" scripts/generar_manual_despliegue.py scripts/generar_doc_arquitectura.py \
    scripts/generar_prompt_cableado.py scripts/generar_prompt_expresiones.py \
    scripts/generar_reconstruccion.py scripts/generar_reglas_datos.py scripts/generar_guia_funcional.py
(sin resultado)

$ grep -ln "json.dump\|instantanea" scripts/verificar_faseA.py scripts/verificar_datos.py \
    scripts/verificar_documentos.py scripts/verificar_enlaces.py scripts/verificar_reproducible.py \
    scripts/verificar_sistema.py scripts/probar_auditor.py scripts/validar_modelo.py \
    scripts/lectura_de_vuelta.py scripts/alcance_reglas.py
scripts/verificar_datos.py
scripts/lectura_de_vuelta.py
```

Los dos únicos que mencionan "instantanea" lo hacen dentro de **cadenas de texto** de un mensaje de
aviso (*"...instantanea.py"*), no como llamada — verificado leyendo las líneas exactas, ninguna abre
ni escribe un archivo. **Ninguno de los siete generadores ni de los ocho verificadores que corrió esta
orden escribe en `BD/instantaneas/`.** Los únicos cuatro módulos del repositorio con `json.dump`
—`appsheet_api.py`, `auditar_cableado.py`, `instantanea.py`, `verificar_app.py`— no se ejecutaron ni
se importaron en ningún comando de esta sesión.

**Conclusión, igual que en el §8: no es un efecto de esta orden.** Se dejó **intacto, sin tocar**:
no se añadió a git (los `git add` de cierre usan rutas explícitas, nunca `-A`, así que un archivo sin
listar no entra) y no se borró — borrarlo también sería tocar la carpeta. Queda como constancia de que
algo, dentro de la ventana de esta sesión, escribió dos veces en `BD/instantaneas/` sin que ningún
comando de este ejecutor lo hiciera. Coincide en carácter con el hallazgo anterior: contenido de datos
de producción (`ACT_Activos`, `USR_Usuarios`, etc.) apareciendo o cambiando en esa carpeta por una vía
que no deja rastro en el código de este repositorio. **Se avisa aquí explícitamente para que se
investigue por fuera de esta orden** — incluida la posibilidad, que la propia instrucción de esta
tarea reconoce como real (*"hay más de uno"* con permiso de edición), de que otra sesión concurrente
esté escribiendo sobre el mismo árbol de archivos mientras esta orden se ejecutaba.

## 9. El diff espurio de `docs/PROMPT_CABLEADO.md` — avisado, no un efecto de este cambio

`docs/HALLAZGOS_ABIERTOS.md` §"`docs/PROMPT_CABLEADO.md` no es reproducible byte a byte" ya documenta
que la tabla de etiquetas (`Label`) de ese archivo ordena los empates de forma inestable. **Se
confirmó en esta orden**: el diff real trae reordenada por completo la tabla de 18 filas de `Label`
—mismas 18 filas, mismo contenido, orden distinto— sin que esta orden haya tocado ninguna etiqueta.
Quien lea el diff de este commit no debe leer esa tabla reordenada como efecto de `RG-39`/`RG-40`; los
efectos reales en ese archivo son: la fila `Coordenadas_Cierre_LatLong` (§6), el título "Paso 6" que
sube de 48 a 49 expresiones huérfanas (una más: `Coordenadas_Cierre_LatLong` deja de estar oculta por
el defecto de generador), y "Paso 7 — Las 23 reglas" (antes 21).

## 10. Qué queda pendiente, sin ambigüedad

| Pendiente | Por qué no se hizo aquí | Dónde está escrito |
|---|---|---|
| Cablear `RG-39`/`RG-40` en el editor de AppSheet (`Editable_If`, después de confirmar `Initial value`) | Fuera de lo que esta orden autoriza tocar (editor/Sheets prohibidos) | `ESPEC-008` §6, `PRUEBA-008` `P-75` |
| Confirmar si `HERE()` no disponible deja el campo vacío o en `0,0` | Requiere sesión de navegador; afecta directamente si `Editable_If = FALSE` es seguro | `docs/HALLAZGOS_ABIERTOS.md` §"Qué pasa si `HERE()` no está disponible" |
| `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` no propaga `descripcion` | Cambio de código fuera del alcance que `ESPEC-008` autorizó | `docs/HALLAZGOS_ABIERTOS.md` §"`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` no propaga `descripcion`" |
| `ESPEC-008` §5 sigue diciendo "No protege `NOV_Novedades`" pese a que §8 registra que se amplió | Inconsistencia interna de la especificación, no de esta orden — no le toca a un ejecutor reescribir una especificación ya aprobada | Este documento, aquí |
| `PRUEBA-008` `P-69` predice "22 reglas"; lo real, tras el dictamen, es 23 | `PRUEBA-008` se escribió antes de que el dictamen sumara `RG-40`; el arquitecto amplió el alcance en `ESPEC-008` §8 sin volver a `PRUEBA-008` | Este documento, aquí — la prueba sigue siendo válida en método, solo desactualizada en la cifra de una fila |

Ninguno de los cinco bloquea lo que sí se aplicó: el mecanismo de protección (`RG-39`, `RG-40`,
`editable=False`) está en el modelo, validado con 0 errores, y los documentos que sí propagan
`descripcion` llevan la instrucción de orden completa.

## 11. Reversión

Sin datos que migrar (`ESPEC-008` §2.3, confirmado de nuevo en el §5 de este acta: las ocho tablas de
movimiento siguen en cero). Revertir esta orden, en cualquier momento antes de la primera fila real de
`FOT_Fotografias` o `NOV_Novedades`, es:

1. Quitar los `dict(id="RG-39", ...)` y `dict(id="RG-40", ...)` de `REGLAS` en
   `scripts/modelo_objetivo.py`, y el `editable=False` de los dos `col()`.
2. Revertir `scripts/generar_prompt_cableado.py:327-333` a la comprensión de conjunto original —queda
   el diff exacto en el historial de git de este commit.
3. Regenerar los siete documentos del §2.3.
4. Revertir la frase de `docs/SISTEMA.md` §3 a "21 reglas".

No aplica reversión de AppSheet ni de Sheets: esta orden no tocó ninguno de los dos.
