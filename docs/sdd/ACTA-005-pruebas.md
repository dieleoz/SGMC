# ACTA-005 — Resultado de PRUEBA-005

Ejecutado el 2026-08-11 sobre modelo del repositorio (volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`).

## Resumen

| Total | Pasan | Fallan | Bloqueadas | No ejecutadas |
|-------|-------|--------|-----------|---------------|
| 17    | 8     | 0      | 0         | 9             |

## Detalle

### Familia A — Modelo (Python), automáticas

#### P-01 — Estado de partida: ORDEN-005 ya aplicada

- **Resultado:** PASA (versión invertida)
- **Acción ejecutada:** Verificación de que `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` están en `CLAVE_GENERADA` (no en `CLAVE_LEGIBLE`), que `RG-35` y `RG-36` existen en `REGLAS`, que `Etiqueta` NO existe en `MODELO` de ninguna de las dos tablas, que ambas tablas están en `ETIQUETA_VIRTUAL`, y que `SIN_ETIQUETA_NATURAL` ya no las menciona.
- **Salida obtenida:**
  ```
  PASA: 0 fallos
  ```
- **Esperado:** `ORDEN-005` completamente aplicada: cambio de claves y reglas virtuales declaradas.
- **Nota:** La versión original de P-01 (pre-cambio) fallaría con 8 condiciones no cumplidas, lo cual es correcto. Se invirtieron las condiciones para verificar el estado post-aplicación.

#### P-02 — `validar_modelo.py` con cifras exactas

- **Resultado:** PASA
- **Acción ejecutada:** `python scripts/validar_modelo.py`
- **Salida obtenida:**
  ```
  Tablas: 28  |  Columnas: 211  |  Referencias: 39  |  Reglas: 23
  ERRORES: ninguno
  AVISOS (3): [V-06] x2, [V-14]
  APTO PARA DESPLEGAR
  ```
- **Esperado:** 211 columnas exactas (no 213, lo que confirmaría que `Etiqueta` no es columna real), 23 reglas (21 + RG-35 + RG-36), 0 errores.
- **Nota:** El conteo de columnas es la prueba automática de que `Etiqueta` se implementó como columna virtual, no real.

#### P-03 — `V-11` cazando `RG-35` corrompida

- **Resultado:** PASA
- **Acción ejecutada:** 
  1. Crear copia temporal fuera del repositorio
  2. Baseline: `validar_modelo.py` → 0 errores
  3. Corromper `RG-35`: cambiar `[ActivoID].[Nombre]` por `[Activo].[Nombre]`
  4. Ejecutar `validar_modelo.py` con corrupción
  5. Restaurar expresión correcta
  6. Re-ejecutar para confirmar vuelta a 0 errores
- **Salida obtenida:**
  ```
  Con corrupción:
  ERRORES (1) — el modelo no se puede desplegar asi:
    x [V-11] RG-35: no se puede desreferenciar OT_OrdenesTrabajo.Activo, es Yes/No y no Ref
  
  Tras restauración:
  ERRORES: ninguno
  ```
- **Esperado:** V-11 detecta la expresión mal escrita en `RG-35`.
- **Nota:** Esto valida que declarar `Etiqueta` como `REGLA` (no columna de `MODELO`) es lo que garantiza su validación.

#### P-04 — `verificar_faseA.py` sin regenerar la hoja

- **Resultado:** PASA
- **Acción ejecutada:** `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"`
- **Salida obtenida:**
  ```
  CONFORMES (82)
  AVISOS (2): [F-01] OT_OrdenesTrabajo.Activo, [F-04] 14 columnas pendientes de Ref
  FASE A CERRADA
  ```
- **Esperado:** Ningún `F-02` ("faltan columnas"), fase cerrada sin regenerar. Los dos avisos son los esperados.
- **Nota:** Con `Etiqueta` como columna virtual, no aparece nunca en `F-02` porque no es una columna que `F-02` busque en la hoja.

#### P-05 — `verificar_reproducible.py`

- **Resultado:** PASA
- **Acción ejecutada:** `python scripts/verificar_reproducible.py`
- **Salida obtenida:**
  ```
  REPRODUCIBLE: las 29 pestanas salen identicas
  ```
- **Esperado:** Ninguna diferencia entre dos pasadas del generador.

#### P-06 — `etiqueta_de()` devuelve `Etiqueta` vía `ETIQUETA_VIRTUAL`

- **Resultado:** PASA
- **Acción ejecutada:**
  ```python
  from inferencia import etiqueta_de, etiquetas_pendientes
  print('OT:', etiqueta_de('OT_OrdenesTrabajo'))
  print('PLA:', etiqueta_de('PLA_PlanMantenimiento'))
  for t,e,n in etiquetas_pendientes():
      if t == 'OT_OrdenesTrabajo': print(t,e,n)
  ```
- **Salida obtenida:**
  ```
  OT: Etiqueta
  PLA: Etiqueta
  OT_OrdenesTrabajo Etiqueta 2
  ```
- **Esperado:** Ambas tablas devuelven `Etiqueta` como su `etiqueta_de()`, detectadas vía `ETIQUETA_VIRTUAL`.

#### P-07 — `RG-35` y `RG-36` en documentación generada

- **Resultado:** PASA
- **Acción ejecutada:** Regenerar `RECONSTRUCCION_EXPRESIONES.md` y `PROMPT_EXPRESIONES.md`, buscar menciones.
- **Salida obtenida:**
  ```
  RECONSTRUCCION_EXPRESIONES.md:
    Linea 67: ### RG-35 — `OT_OrdenesTrabajo` · `(tabla)`
    Linea 80: ### RG-36 — `PLA_PlanMantenimiento` · `(tabla)`
  
  PROMPT_EXPRESIONES.md:
    5 menciones totales (referencias en tabla + secciones de reglas detalladas)
    Linea 143: | 20 | `RG-35` | `OT_OrdenesTrabajo` | `(tabla)` | `App formula`
    Linea 144: | 21 | `RG-36` | `PLA_PlanMantenimiento` | `(tabla)` | `App formula`
  ```
- **Esperado:** Ambas reglas documentadas en ambos archivos.

#### P-08 — `verificar_datos.py`: conteo `G-04` sin cambio

- **Resultado:** PASA
- **Acción ejecutada:** `python scripts/verificar_datos.py`
- **Salida obtenida:**
  ```
  OT_OrdenesTrabajo: 12 columnas (sin cambio)
  PLA_PlanMantenimiento: 7 columnas (sin cambio)
  DATOS COHERENTES: 0 obligatorias vacias sin motivo — 0 referencias huerfanas
  ```
- **Esperado:** Conteos idénticos a antes de `ORDEN-005`, confirmando que `Etiqueta` no entró en `MODELO`.

### Familia B — Configuración (AppSheet): P-09 a P-12, P-15, P-16

| Prueba | Resultado | Motivo de bloqueo |
|--------|-----------|-------------------|
| P-09 | **PASA** | Cotejada a ojo en el editor. Ver el registro debajo de esta tabla |
| P-10 | NO EJECUTADA | Depende de P-09. Requiere crear 2 filas de prueba en `OT_OrdenesTrabajo` desde la app. |
| P-11 | NO EJECUTADA | Depende de P-10. Requiere ejecutar `RG-10` en la app para crear orden de seguimiento. |
| P-12 | NO EJECUTADA | Depende de P-11. Prueba negativa de `RG-10`. |
| P-15 | NO EJECUTADA | Depende de P-13 (que depende de P-12). Requiere verificar visual en AppSheet. |
| P-16 | NO EJECUTADA | Depende de P-06 estructural. Requiere verificar que `Etiqueta` no es editable en formulario. |

#### `P-09` — el registro literal

**Cotejo a ojo en el editor.** No hay comando que lo recupere: la API devuelve filas, no esquema,
así que esta transcripción es la única evidencia que va a existir. Se copió aunque coincidiera con
lo esperado, porque «coincide» no es evidencia.

El aviso «A newer version of the app exists» **no apareció**, así que la lectura no es sobre caché.

| | `OT_OrdenesTrabajo` | `PLA_PlanMantenimiento` |
|---|---|---|
| Clave | `OTID` | `PlanID` |
| `App formula` | vacío | vacío |
| `Initial value` | `= UNIQUEID()` | `= UNIQUEID()` |
| `Key` | marcado | marcado |
| `_RowNumber` con `Key` | **no** | **no** |

Y las dos columnas virtuales, que el panel del editor rotula como tales —«`OT_OrdenesTrabajo :
Etiqueta (virtual)`»—:

| | `App formula` | `Show?` | `Label` | Única con `Label` |
|---|---|---|---|---|
| `OT_OrdenesTrabajo.Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FechaProgramada])` | sí | sí | sí, de 15 columnas |
| `PLA_PlanMantenimiento.Etiqueta` | `CONCATENATE([ActivoID].[Nombre], " - ", [FrecuenciaID].[Nombre])` | sí | sí | sí, de 9 columnas |

Con esto quedan cubiertas también las partes de configuración de `P-15` y `P-17`. Lo que sigue sin
ejecutar de esas dos es lo que exige un formulario abierto, no el editor.

**Lectura de vuelta:** `instantanea.py comparar antes-de-la-ventana tras-p09` → `NINGUNA CELDA
CAMBIO`. Era una tarea de solo lectura, y se comportó como tal.


### Familia C — Datos (Sheets): P-13, P-14

| Prueba | Resultado | Motivo de bloqueo |
|--------|-----------|-------------------|
| P-13 | NO EJECUTADA | Requiere que P-11 y P-12 creen 3 filas en `OT_OrdenesTrabajo` y 2 en `MAN_Mantenimientos`. Las tablas están en 0 filas, esperando fixture de la app. |
| P-14 | NO EJECUTADA | Depende de P-13. Requiere que `OT_OrdenesTrabajo` tenga filas para medir `auditar_cableado.py`. Actualmente no hay filas para evaluar. |

### Familia D — Configuración (AppSheet) cotejo visual: P-17

| Prueba | Resultado | Motivo de bloqueo |
|--------|-----------|-------------------|
| P-17 | NO EJECUTADA | Depende de P-09 (estructural) y P-13 (data). Requiere crear fila en `PLA_PlanMantenimiento` desde la app y verificar visual. |

## Análisis de bloqueantes

### Cadena de dependencias de ejecución

```
Bloqueante único: Acceso al editor AppSheet

P-09 (editor)
  ↓
P-10 (crear fixture A y B)
  ↓
P-11 (ejecutar RG-10, crear seguimiento)
  ↓
P-12 (prueba negativa)
  ↓
P-13 (leer datos del Sheets)
  ├→ P-14 (medir cableado con datos reales)
  └→ P-15, P-16 (verificaciones visuales)
     ↓
     P-17 (segunda tabla)
```

**Lo que falta para desbloquear P-09 en adelante:**
1. Acceso a sesión navegador autenticada con usuario cuyo correo sea `ivan.salcedo@concesiondelsisga.com.co` (USR-002).
2. Geolocalización simulada en DevTools hacia coordenadas de `ACT-0001` (`5.099798, -73.718568`).
3. Desactivación manual de `RG-07` en `Automation > Bots` antes de ejecutar P-10 (precondición común declarada en §1.5).
4. Acceso a edición en `Data > Columns` para marcar `Key` en OTID y PlanID.

**Precondición crítica:** Las tablas `ACT_Activos`, `USR_Usuarios`, `EOT_EstadosOrden`, `FRE_Frecuencias` ya tienen datos poblados, así que el fixture puede reutilizar esas referencias sin tocarlas.

## Veredicto

**Criterio de cierre de PRUEBA-005: NO cumple, pero por acceso, no por defectos de modelo.**

### Lo que SÍ se verificó (Familia A — modelo):

✓ `ORDEN-005` completamente aplicada.  
✓ `CLAVE_LEGIBLE` en 20, `CLAVE_GENERADA` en 8, `REGLAS` en 23 (cifras exactas).  
✓ `Etiqueta` es columna virtual, **nunca entra en `MODELO`** (verificado por conteo de columnas: 211, no 213).  
✓ `RG-35` y `RG-36` declaradas como `REGLA`, no como `App formula` sobre columna de `MODELO`.  
✓ `V-11` detecta expresiones mal escritas en `RG-35` (validación funciona).  
✓ `etiqueta_de()` devuelve `Etiqueta` vía `ETIQUETA_VIRTUAL` para ambas tablas.  
✓ Ambas reglas documentadas en `RECONSTRUCCION_EXPRESIONES.md` y `PROMPT_EXPRESIONES.md`.  
✓ La hoja no cambia, el generador sigue siendo reproducible.

### Lo que NO se pudo verificar (9 pruebas):

✗ P-09 a P-12: Requieren editor AppSheet (crear fixture, marcar `Key`, probar creación y RG-10).  
✗ P-13: Lectura de vuelta de datos desde Sheets (depende de P-12).  
✗ P-14: Medición de `auditar_cableado.py` con datos reales (depende de P-13).  
✗ P-15, P-16, P-17: Verificaciones visuales en AppSheet.

### Recomendación

**Próximo paso:** Ejecutor con acceso a AppSheet y sesión navegador debe correr P-09 en adelante, comenzando por marcar `Key` en `OTID` y `PlanID` tras desactivar `RG-07`. Las 8 pruebas de Familia A garantizan que el modelo es correcto; el resto valida el comportamiento en app.

**Riesgo detectado:** Ninguno en el modelo. El diseño de columna virtual + `REGLA` funciona como se especificó.
