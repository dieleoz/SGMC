# ORDEN-005 — Ejecución de `ESPEC-005` (`OTID`/`PlanID` a `UNIQUEID()`, `Etiqueta` virtual)

<!-- verificar_documentos: ignorar OT_OrdenesTrabajo.Etiqueta, PLA_PlanMantenimiento.Etiqueta -->
<!-- D-03 compara Tabla.Columna contra MODELO, y Etiqueta a propósito NUNCA entra en MODELO: es
     una columna virtual declarada solo en REGLAS (RG-35/RG-36). Mismo criterio que ESPEC-005. -->

## 0. Nota de proceso — léase antes que nada

**Esta orden se escribe después de que el cambio que autoriza ya estaba aplicado.** El orden
correcto del pipeline (`docs/SDD_PIPELINE_SGMC.md` §3) es Especificador → Verificador → Arquitecto →
**Ejecutor** (que produce esta misma `ORDEN-NNN` **antes** de tocar nada) → Probador. Lo que ocurrió
aquí fue: Especificador → Verificador → Arquitecto (`PASA CON CONDICIONES`) → **se aplicó
directamente el cambio de modelo, sin que existiera `ORDEN-005`, sin `ACTA-005` y sin lanzar al
ejecutor** — commit `8e7ccef` (`ESPEC-005 APLICADA: OTID y PlanID pasan a UNIQUEID, con etiqueta
virtual`), el 2026-08-10/11. Quien lo aplicó fue el mismo especificador/arquitecto de sesión, no el
ejecutor, y sin la orden que este documento debería haber sido primero.

**Es la segunda vez que esto pasa en el proyecto.** La primera está documentada en
[`ESTADO.md`](../../ESTADO.md): *"Nada se aplica hasta que el arquitecto lo tumbe o lo deje pasar. Es
la regla que nos saltamos el 2026-08-10 por la mañana, y costó un dictamen de veinte observaciones."*
Esa vez el costo fue un dictamen inflado por partir de un estado no verificado. Esta vez el costo es
distinto: el cambio de modelo en sí resultó correcto (verificado en `ACTA-005`), pero **siete
condiciones del propio dictamen del arquitecto —las de redacción, no las de código— quedaron sin
aplicar durante el tiempo en que el repositorio ya decía "aplicada"**, hasta que esta orden y el acta
que la acompaña las cierran.

**Esta orden no autoriza retroactivamente lo ya hecho.** Lo documenta, con la misma exigencia de
verificación que si fuera a autorizarlo ahora, y dice explícitamente qué de lo que un `ORDEN-NNN`
normal cubriría **no se hizo y sigue sin autorización**: todo lo que vive en el editor de AppSheet y
en el Sheets de producción (§4).

## 1. Las tres firmas, verificadas en este momento

| | |
|---|---|
| Cubre | [`ESPEC-005-clave-otid-planid.md`](ESPEC-005-clave-otid-planid.md) y [`PRUEBA-005-clave-otid-planid.md`](PRUEBA-005-clave-otid-planid.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — confirmado vigente con `python scripts/sistema.py` al escribir esta orden |

1. **Especificación.** `ESPEC-005`, rehecha el 2026-08-10 tras el primer bloqueo del arquitecto
   (catorce hallazgos en la versión anterior). Verificada de nuevo contra el archivo en cada punto,
   según su propia cabecera.
2. **Pruebas.** `PRUEBA-005`, rehecha el mismo día junto con `ESPEC-005`. `P-01` a `P-08`
   (Familia A) corridas de verdad sobre copia temporal antes de esta orden; `P-09` a `P-17`
   (Familias B, C, D) descritas para cuando se ejecuten contra la aplicación — **no ejecutadas
   todavía**, ver §4.
3. **Arquitecto.** Veredicto `PASA CON CONDICIONES`, **diez condiciones**. No existe en el
   repositorio un documento de dictamen aparte con las diez numeradas: lo que sí queda trazado es el
   mensaje del commit `8e7ccef`, que lista tres de ellas por ser "las que eran de mis generadores", y
   el encargo con el que se abrió esta orden, que trae el contenido de las siete restantes. Esta
   orden no reconstruye una numeración original que no está en el repositorio: describe cada
   condición por su contenido y por dónde se cerró.
   - **Tres condiciones de código**, ya aplicadas junto con el modelo (commit `8e7ccef`, antes de
     esta orden) y verificadas de nuevo aquí (§2.2):
     1. `docs/PROMPT_CABLEADO.md` (generado por `scripts/generar_prompt_cableado.py`) instruye crear
        la columna virtual antes de marcar `Label`, con su `App formula`, y con `Show?` activo y
        `Label?` desmarcado en la columna anterior — sección «Antes de marcar nada: 2 de esas
        etiquetas hay que crearlas».
     2. `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` (generado por `scripts/generar_reconstruccion.py`)
        ya no solo emite el identificador y la expresión de `RG-35`/`RG-36`: dice que es columna
        virtual, su nombre, y que lleva `Label` — sección «RG-35 — `OT_OrdenesTrabajo` · `(tabla)`».
     3. La misma instrucción de Show?+Label de la condición 1 alcanza también a
        `PLA_PlanMantenimiento.Etiqueta` en esa sección de `docs/PROMPT_CABLEADO.md` — aunque
        `PLA_PlanMantenimiento` no aparezca en la tabla-resumen derivada de
        `etiquetas_pendientes()` (§3, condición de documento correspondiente en `PRUEBA-005`).
   - **Siete/ocho condiciones de documento** — el encargo que abrió esta orden las presenta como
     "siete" pero las enumera en ocho puntos (numerados 3 a 10); esta orden no fuerza la cuenta a
     siete donde el propio encargo lista ocho, y dice cuántas aplicó de verdad: **ocho**, ver §3. No
     estaban aplicadas cuando `8e7ccef` se hizo, y **esta orden es la que las aplica**, sobre
     `ESPEC-005` y `PRUEBA-005`.
4. **Gate objetivo**, corrido en este momento, no cuando se aprobó:
   ```
   $ python scripts/validar_modelo.py
   Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
   ERRORES: ninguno
   AVISOS (3): [V-06] PLA_PlanMantenimiento no es referenciada por nadie ·
               [V-06] LST_ValoresLista no es referenciada por nadie ·
               [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID' (...)
   APTO PARA DESPLEGAR
   ```
   0 errores. Los tres avisos son preexistentes y no relacionados con esta orden (`PLA` y `LST` como
   puntos de entrada, y el renombre `Activo`→`ActivoID` que espera Fase B).

## 2. Qué se aplicó, y cuándo — lo ya hecho, fuera de orden

### 2.1 El cambio de modelo (commit `8e7ccef`, 2026-08-10/11)

Sobre `scripts/modelo_objetivo.py`:

- `CLAVE_LEGIBLE`: `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` salen del conjunto (22 → 20).
- `CLAVE_GENERADA`: las mismas dos entran (6 → 8).
- `REGLAS`: se añaden `RG-35` (`OT_OrdenesTrabajo`, `App formula`, columna virtual `Etiqueta`,
  `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])`) y `RG-36` (`PLA_PlanMantenimiento`,
  mismo mecanismo, `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])`) — 21 → 23.
- Ninguna columna nueva en `MODELO["OT_OrdenesTrabajo"]["columnas"]` ni en
  `MODELO["PLA_PlanMantenimiento"]["columnas"]`: `Etiqueta` es virtual y nunca entra ahí, exactamente
  como manda `ESPEC-005` §3.2.

Sobre `scripts/inferencia.py`:

- `SIN_ETIQUETA_NATURAL` pierde la entrada `"OT_OrdenesTrabajo"`.
- Se añade `ETIQUETA_VIRTUAL = {"OT_OrdenesTrabajo": "Etiqueta", "PLA_PlanMantenimiento": "Etiqueta"}`.
- `etiqueta_de()` consulta `ETIQUETA_VIRTUAL` antes que `SIN_ETIQUETA_NATURAL`/`ETIQUETAS`.

Esto es exactamente lo que `ESPEC-005` §4 manda. Verificación literal en `ACTA-005`.

### 2.2 Las tres condiciones de código, verificadas de nuevo aquí

```
$ grep -n "RG-35" -A8 docs/sdd/RECONSTRUCCION_EXPRESIONES.md | head -9
67:### RG-35 — `OT_OrdenesTrabajo` · `(tabla)`
...
71:> **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con
72:> *Data > Columns > `Add virtual column`*, se llama **`Etiqueta`**, lleva esa expresión
73:> en su `App formula`, y después **`Show?` activo** y **`Label` marcado**. (...)
```
```
$ grep -n "PLA_PlanMantenimiento" docs/PROMPT_CABLEADO.md | sed -n '1,3p'
132:| `PLA_PlanMantenimiento` | **`PlanID`** | **no. Nadie la referencia (...)** |
...
431:| `PLA_PlanMantenimiento` | **`Etiqueta`** | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` |
```
La sección «Antes de marcar nada» de `docs/PROMPT_CABLEADO.md` instruye `Show?`+`Label` para las
**dos** filas de esa tabla (`OT_OrdenesTrabajo` y `PLA_PlanMantenimiento`), no solo para la que
aparece después en la tabla-resumen derivada de `etiquetas_pendientes()`. Las tres condiciones de
código: **hecho y verificado**, con los comandos de arriba.

## 3. Las condiciones de documento — aplicadas por esta orden

Sobre `ESPEC-005` y `PRUEBA-005`, en este mismo cambio de repositorio, antes de cerrar esta orden:

| # (según el encargo) | Qué pedía | Dónde quedó |
|---|---|---|
| 3 | `RG-05` no puede estar aplicado durante la tanda; `P-14` es la única oportunidad de medir `MAN_Mantenimientos.OTID`/`OT_OrdenesTrabajo.OTOrigenID` | `ESPEC-005` §6 (nuevo párrafo sobre `RG-05`/`FILTROS_AL_FINAL`); `PRUEBA-005` `P-14` (precondición ampliada + párrafo de cierre) |
| 4 | Retirar `python scripts/sistema.py` como forma de volcar | `PRUEBA-005`, fila «Contra cuál sistema» y `P-13` |
| 5 | Citar `instantanea.py` (API) como fuente de «las ocho en cero», o declarar el volcado local ciego | `ESPEC-005` §2.1, reescrita con la cita de `VOLCADO_CIEGO_A` y la remisión a `PRUEBA-005` §1.1 |
| 6 | `P-15` añade `Show?` activo y `Label?` desactivado | `PRUEBA-005` `P-15`, acción en dos pasos numerados con la cita de Google |
| 7 | `P-17` incluye marcar `Label` sobre `PLA_PlanMantenimiento.Etiqueta` | `PRUEBA-005` `P-17`, nuevo paso 1 de la acción |
| 8 | Citar `MANUAL_DESPLIEGUE.md` por título, no por línea; sumarlo a la lista de generados | `ESPEC-005` §3.4 (cita corregida) y §8 (documento añadido a la lista) |
| 9 | `P-13`: reactivar `RG-07` no tiene comando, se cierra copiando el estado del bot | `PRUEBA-005` `P-13`, último punto del cierre del fixture |
| 10 | `P-07`: sustituir el `6` literal por «las tres salidas no vacías» | `PRUEBA-005` `P-07`, criterio de paso reescrito antes del resultado observado |

Y, fuera de la lista numerada del encargo pero exigido por la coherencia del propio documento:
`ESPEC-005` deja de decir de sí misma que «no está aplicada al repositorio real» (antes en la
resolución de §3.2); ahora dice cuándo se aplicó y remite a esta orden y a `ACTA-005`.

Verificación de que ninguna de estas ediciones rompió los verificadores automáticos, en §5 y en
`ACTA-005`.

## 4. Qué NO autoriza ni aplica esta orden

**El Sheets de producción y el editor de AppSheet no se tocan.** Nada de lo siguiente está hecho, y
esta orden no lo autoriza: sigue pendiente de una ejecución futura, separada, que siga el orden de
operaciones del ejecutor (respaldo → limpieza → Sheets → `Regenerate Structure` → tipos y claves →
referencias → reglas → verificación):

- Declarar `Initial value = UNIQUEID()` y marcar `Key` en `OT_OrdenesTrabajo.OTID` y
  `PLA_PlanMantenimiento.PlanID` (`PRUEBA-005` `P-09`).
- Crear las columnas virtuales `Etiqueta` en las dos tablas, marcar `Show?` y `Label`, desmarcar
  `Label?` de la columna anterior (`P-15`, `P-17`).
- Probar `RG-10`, `RG-12` y el botón `+` de creación de órdenes (`P-10`, `P-11`, `P-12`).
- Reconfirmar a ojo y luego medir con `auditar_cableado.py` las dos referencias hacia
  `OT_OrdenesTrabajo` (`P-14`) — **antes** de aplicar `RG-05` (§3, condición 3).
- Aplicar los `Security Filter` `RG-04`/`RG-05` — van los últimos, según `ESTADO.md`.
- Desactivar/reactivar `RG-07` alrededor del fixture.

El encargo para esa ejecución futura ya existe y no cambia con esta orden:
[`docs/PROMPT_CABLEADO.md`](../PROMPT_CABLEADO.md), pasos 2 y 5.

## 5. Verificación de cierre

Comandos corridos al cerrar esta orden (salida completa en `ACTA-005`, no repetida aquí):

- `python scripts/validar_modelo.py` — 0 errores.
- `python scripts/verificar_documentos.py` — 0 fallos.
- `python scripts/verificar_enlaces.py` — 0 enlaces rotos (incluye los de esta orden y de
  `ACTA-005` hacia `ESPEC-005`/`PRUEBA-005` y viceversa).
- `python scripts/verificar_datos.py` — 0 obligatorias vacías sin motivo, 0 referencias huérfanas.

## 6. Reversión

**De lo aplicado al modelo (commit `8e7ccef`):** `git revert 8e7ccef` sobre `scripts/modelo_objetivo.py`
y `scripts/inferencia.py` devuelve `CLAVE_LEGIBLE`/`CLAVE_GENERADA`/`REGLAS` a 22/6/21 y retira
`ETIQUETA_VIRTUAL`. Como la hoja de datos no cambió (`ACTA-005` §2), no hay nada que restaurar en
Sheets ni en AppSheet para esta parte: revertir el commit basta.

**De las ediciones de documento de esta orden:** son commits de texto sobre `ESPEC-005` y
`PRUEBA-005`; revertir el commit correspondiente basta, sin efecto sobre producción.

**No aplica ninguna de las reglas de reversión de Sheets/AppSheet** (`Manage > Versions`, restaurar
copia) porque esta orden no tocó ninguno de los dos.
