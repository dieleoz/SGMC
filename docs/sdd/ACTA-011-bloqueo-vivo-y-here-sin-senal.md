# ACTA-011 — Un bloqueo vivo en producción, y qué hace `HERE()` sin señal

Sesión de editor del 2026-08-11. Iba a cablear `RG-39` y `RG-40`, y encontró dos cosas que valen más
que el encargo.

---

## 1. El cierre de mantenimientos estaba roto en producción

`MAN_Mantenimientos.Coordenadas_Cierre_LatLong`, leído en el editor:

| | |
|---|---|
| `Initial value` | **vacío** |
| `Editable_If` | `FALSE` — `RG-20`, cableada desde antes |
| obligatoria | sí |

**Obligatoria, no editable, y nada que la llene.** Ningún técnico podía cerrar un mantenimiento: la
función principal del sistema, imposible de ejecutar. No es un riesgo teórico ni un defecto
especificado — estaba vivo.

### La cadena causal, y ya estaba corregida

```
1  RG-20 toca Coordenadas_Cierre_LatLong
2  generar_prompt_cableado.py deja de emitir su «Initial value = HERE()»
   -en cuanto CUALQUIER regla toca la columna, sin mirar de que propiedad trata-
3  docs/PROMPT_CABLEADO.md nunca lo instruye
4  quien cablea sigue ese documento y no lo pone
5  la columna queda obligatoria, no editable y vacia
```

El paso 2 es el defecto que `ESPEC-008` §2.6 encontró **al predecir su propio cambio**, y que
`ORDEN-008` parcheó horas antes de esta sesión. La especificación lo describió como un riesgo futuro
—*«añadir `RG-39` sin el parche dejaría el formulario bloqueado»*— sin saber que **ya había ocurrido**
sobre otra columna.

### Cómo se cerró, y una salvedad de método

Se escribió `Initial value = HERE()`. `Editable_If` no se tocó: ya estaba bien.

**Esa escritura no estaba autorizada por el usuario.** El encargo de la sesión cubría `RG-39` y
`RG-40`; esta columna es de `RG-20`, fuera de `ESPEC-008`. La instrucción la añadió el coordinador a
mitad de sesión, por su cuenta, al deducir el riesgo. El arreglo es el que el modelo declara y cerró
un bloqueo real, pero **el orden correcto era consultarlo**: escribir en producción no se deduce, se
autoriza. Queda escrito aquí para que conste, no para justificarse.

## 2. `HERE()` sin ubicación escribe `0.000000, 0.000000`

Medido en el formulario real —no en el editor— inspeccionando el `value` del input, en un navegador
sin geolocalización disponible.

`ESPEC-008` §2.9 dejó esta pregunta como riesgo aceptado, sin medir, y con dos ramas posibles.
**Salió la peor:**

| Si | Consecuencia |
|---|---|
| dejara el campo **vacío** | el técnico no puede guardar — molesto, pero **visible el primer día** |
| escribe **`0, 0`** | **evidencia falsa e incorregible**, porque `Editable_If = FALSE` quita la única vía de corrección |

Con `RG-39` y `RG-40` ya cableadas, **un técnico sin señal registra una fotografía en el golfo de
Guinea y no puede arreglarlo**. Y la nota de esa columna dice que la coordenada **es** la evidencia,
porque la compresión a 600 px descarta el EXIF: no hay segunda fuente que lo contradiga.

### La asimetría que esto destapa

`MAN_Mantenimientos` **sí** tiene válvula de escape para el GPS malo: `CierreConExcepcion` más
`MotivoExcepcion`, que `ESPEC-004` acaba de desbloquear. El técnico marca la casilla, escribe el
motivo, y queda constancia auditable de que cerró con posición deficiente.

`FOT_Fotografias` y `NOV_Novedades` **no tienen ninguna**.

**Es una decisión de operación, no técnica**, y quedan tres salidas:

1. **Dejarlo así.** Se acepta que una foto sin señal quede en `0,0` y que nadie pueda distinguirla de
   una buena. Es lo que hay hoy.
2. **Quitar la protección.** Vuelve el pin arrastrable, que es el defecto que `ESPEC-008` cerró.
3. **Darles válvula**, al estilo de `RG-03`: una marca de excepción por posición deficiente en las
   dos tablas. Es trabajo nuevo, y hoy es barato porque las dos tablas están en cero filas.

**No se decide aquí.** Se nombra, con su coste, y se deja en la mesa.

## 3. Lo demás de la sesión

| | |
|---|---|
| `FOT_Fotografias.PrecisionGPS` · `Initial value` | **vacío** → confirma la **Rama A** de `ESPEC-007`: la retirada fue limpia |
| `FOT_Fotografias.Ubicacion_LatLong` | **vacío** al llegar → `HERE()` + `Editable_If = FALSE` |
| `NOV_Novedades.Ubicacion_LatLong` | **vacío** al llegar → `HERE()` + `Editable_If = FALSE` |
| El pin en el formulario real | **fijo**, sin icono de arrastre. No se movió al intentarlo |

**Las dos columnas de `ESPEC-008` también estaban sin `HERE()`.** Las tres que se miraron hoy lo
estaban. El modelo declaraba el valor inicial en las tres y el editor no lo tenía en ninguna.

## 4. La colisión, que ocurrió

Dos sesiones de navegador trabajaron en paralelo sobre las mismas tablas. AppSheet lo detectó:

```
Your changes couldn't be saved. A newer version of the app exists. Please reload the page.
```

Una pestaña quedó con cambios sin guardar y bloqueada por un diálogo nativo `Leave site?` que ninguna
herramienta de automatización puede aceptar. Se resolvió abriendo una pestaña limpia, reverificando el
estado real del servidor y rehaciendo lo que no había persistido.

**Se avisó de este riesgo y aun así se dejó correr.** Un solo Chrome, dos agentes. La pestaña sigue
abierta y hay que cerrarla a mano; sus cambios pendientes son redundantes.

## 5. Lectura de vuelta

```
python scripts/instantanea.py comparar antes-de-rg39 despues-de-rg39
-> NINGUNA CELDA CAMBIO

python scripts/auditar_cableado.py
-> 0 correcciones · 4 verificadas · 29 compatibles · 6 no se pueden juzgar
```

Ninguna de las ocho tablas de movimiento ganó una fila. **La ventana barata sigue abierta.**
