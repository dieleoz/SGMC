---
name: cablear-referencias
description: Cablea o modifica una referencia entre tablas del SGMC — convertir una columna Text en Ref, renombrar una clave, cambiar el padre de una tabla hija. Úsala antes de tocar cualquier tipo de columna en el Sheets o en AppSheet, y siempre que alguien proponga una fórmula con desreferencia [A].[B].[C].
---

# Cablear una referencia en el SGMC

Este proyecto documentó durante meses una fórmula de geofencing que nunca funcionó. La causa no fue
la fórmula: fue que `MAN_Mantenimientos.OTID` es `Text` y no `Ref`, de modo que la desreferencia era
imposible. Nadie lo detectó porque nadie comprobó la cadena antes de escribirla.

Esta skill existe para que eso no se repita.

## La regla de la que se deriva todo

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

Léela otra vez antes de seguir. Casi todos los errores de esta clase salen de ignorarla:

- Renombrar y retipar no son dos tareas. Si la clave se llama `Numero_OT` y quien la apunta se llama
  `OTID`, la conversión no tiene contra qué resolver.
- El orden importa. Primero la clave del destino, después quien la apunta.
- Una conversión `Text` a `Ref` conserva **solo** las filas cuyo valor coincide con la clave. Las
  demás quedan huérfanas, y AppSheet no lo anuncia.

## Antes de proponer nada: cuatro comprobaciones

Ninguna es opcional, y las cuatro se hacen contra el archivo, no contra la memoria ni contra la
documentación.

### 1. ¿Contra cuál de los dos modelos estás mirando?

El Excel local y el Sheets de producción **son modelos distintos**. Declara cuál leíste antes de
afirmar nada. Ejemplo real: `MAN_Mantenimientos.ActivoID` existe en el Excel y no en producción.

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo de Datos (2).xlsx', read_only=True)
ws = wb['NOMBRE_TABLA']
print([c.value for c in next(ws.iter_rows(min_row=1,max_row=1))])
"
```

Para producción, el conector de Google Drive con
`fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.

### 2. ¿Cuál es la clave real del destino?

No la deduzcas del nombre. `OT_OrdenesTrabajo` no tiene columna `OTID`: su clave es `Numero_OT`,
con valores `OT-0001`. Otras tablas la referencian como `OTID`. Ese desajuste produjo el checklist
huérfano `d02d8a3d`.

### 3. ¿Los valores actuales resuelven contra esa clave?

Es la comprobación que decide si la conversión es limpia o deja huérfanos. Cuenta cuántos valores
de la columna origen **no** existen en la clave destino. Si el número no es cero, la conversión
tiene un paso previo de limpieza.

### 4. ¿Cuántas filas hay en juego?

Determina el costo, y a veces el calendario. `MAN_Mantenimientos` tiene 0 filas: convertir `OTID`
hoy no arrastra ningún dato. Después de poblar, la misma conversión obliga a migrar y reconciliar.
Cuando encuentres una tabla vacía cuya referencia está mal tipada, dilo: es la ventana barata.

## Cómo se declara el cambio

**El diseño se edita en un solo sitio.** Nunca escribas el mapeo de migración solo en un documento:
se declara en `scripts/modelo_objetivo.py`, en una de estas dos estructuras.

| Estructura | Cuándo | Qué declara |
|---|---|---|
| `RETIPADOS` | La columna conserva el nombre y cambia de tipo | tipo actual, tipo objetivo, tabla destino, motivo |
| `RENOMBRADOS` | La columna cambia de nombre | nombre objetivo y por qué |

Si la columna no existe hoy, márcala con `nueva=True` en su definición. Una referencia que no cae
en ninguno de los tres casos es una que nadie va a crear el día de la migración, y la validación te
lo dirá.

Flujo obligatorio, sin atajos:

```
1. editar  scripts/modelo_objetivo.py
2. correr  python scripts/validar_modelo.py        -> debe dar 0 errores
3. correr  python scripts/generar_doc_arquitectura.py
```

Las reglas que te van a frenar:

| Regla | Comprueba |
|---|---|
| V-05 | La referencia se llama como la clave destino, o declara un alias justificado |
| V-11 | La ruta `[A].[B].[C]` es navegable: cada salto intermedio es `Ref` |
| V-14 | El renombrado aterriza en una columna que existe. Avisa si reutiliza el nombre viejo |
| V-15 | Toda referencia declara de dónde sale: renombrado, retipado o columna nueva |
| V-16 | Lo retipado coincide en tipo y destino con lo que declara el modelo |
| V-17 | Ninguna expresión compara una columna `Ref` contra un literal de texto, **salvo que el destino esté en `CLAVE_LEGIBLE`** |

**V-11 es la que habría ahorrado meses.** Comprueba lo que AppSheet comprueba, sin abrir AppSheet.

## Trampas conocidas

Cada una costó tiempo real en este proyecto.

**El nombre reutilizado.** `OT_OrdenesTrabajo.Activo` guarda hoy el identificador del activo; en el
modelo objetivo `Activo` es la bandera `Yes/No` de todas las tablas. Renombra la vieja **antes** de
crear la nueva, o el Sheets queda con dos columnas iguales y AppSheet resuelve una sin decir cuál.

**El dato guardado dos veces.** Si el activo se alcanza por `[OTID].[ActivoID]`, no lo guardes
además en la ejecución. Dos copias del mismo dato permiten que digan cosas distintas, y no hay
forma de saber cuál miente.

**`IsPartOf` es un borrado en cascada.** Marcarlo sobre `MAN_Mantenimientos.OTID` significa que
borrar una orden borra su ejecución, sus fotografías y sus firmas. En un sistema cuyo propósito es
que la evidencia sea difícil de falsificar, eso se decide, no se hereda del ejemplo.

**El encabezado renombrado con el dato viejo.** Renombrar una columna **no cambia lo que el dato
significa**. `CHK_Checklists.OTID` pasó a llamarse `MantenimientoID` y su fila siguió guardando
`OT-0001`, que es una orden. La columna dice una cosa, el dato dice otra, y solo se nota al
convertir a `Ref`. **Después de cada renombrado, comprueba que los valores resuelvan contra la nueva
clave destino.**

**El catálogo nuevo con claves nuevas.** Al crear un catálogo para una columna que ya tiene datos,
la clave debe ser **el valor que esos datos ya guardan**, no un identificador ordenado. Ocurrió el
2026-08-07: `EOT_EstadosOrden` se creó con `1..7` mientras la orden guardaba `Asignada` y `Cerrada`.
Se ve impecable en la hoja y deja las 6 órdenes huérfanas al cablear. La misma tarde,
`UNF_UnidadesFuncionales` se hizo bien —claves 7 a 10, las que ya usaba `ACT_Activos`— y las 34
filas siguieron resolviendo solas.

**Comparar un `Ref` contra un literal legible.** Un `Ref` guarda la **clave** del destino, no su
nombre. `[EstadoActivoID] <> "Retirado"` sobre una `EST_Activo` con claves `1..4` es **siempre
cierto** — y si la expresión es una `App formula`, **escribe** ese resultado constante sobre los
datos. Ocurrió el 2026-08-07: RG-16 habría repuesto `Activo = TRUE` sobre el activo recién dado de
baja, deshaciendo la Fase A en silencio. Se escribe `[EstadoActivoID].[Nombre]`. La regla **V-17**
lo detiene ahora, porque **V-11 era ciega a esto**: solo comprueba cadenas de más de un salto.

**Pero no toda comparación contra un literal está mal, y ahí estuvo el segundo error.** Si el
catálogo tiene la clave legible, la palabra **es** la clave: `[EstadoOrdenID] = "Cerrada"` es
correcto, porque `ESPEC-001B` construyó `EOT_EstadosOrden` así a propósito siguiendo R-8. La primera
versión de V-17 prohibía la clase entera y daba falso positivo sobre esa regla, contradiciendo la
doctrina del propio proyecto. Por eso existe `CLAVE_LEGIBLE` en `modelo_objetivo.py`, **derivada del
dato y no de una impresión**: lista las 15 tablas cuya clave es texto legible. Si una tabla cambia
de clave numérica a legible, se actualiza ahí.

**El texto como clave ajena.** `CHD_ChecklistDetalle` referenciaba la pregunta por su **enunciado**.
Corregir una tilde rompía la agrupación histórica. Si ves una columna que guarda texto legible y
hace de clave, es un defecto, no una comodidad.

**Renombrar la clave rompe las vistas.** Antes de renombrar, busca el nombre viejo en el editor de
AppSheet y anota dónde aparece. Después de *Regenerate Structure*, corrige cada aparición.

## Cómo entregar el trabajo

El agente no tiene acceso al editor de AppSheet ni al Sheets de producción. Lo que produce es una
especificación que un operador humano aplica. Por tanto:

1. **Pasos numerados y ordenados**, con el porqué del orden cuando no sea obvio.
2. **Una verificación por paso**, con la salida esperada. No «verificar que quedó bien», sino qué
   comando o qué expresión, y qué debe devolver.
3. **Ruta de reversión** antes del primer paso destructivo.
4. **Criterio de cierre**, y si algo va a impedir que se cumpla, dilo por adelantado. El geofencing
   no pasará su prueba mientras los 34 activos compartan una coordenada en Bogotá: decirlo después
   de que alguien lo intente es hacerle perder la tarde.

Marca cada punto como **hecho y verificado**, con qué comando lo verificaste, o como **pendiente de
aplicar**. No hay estado intermedio: este proyecto arrastra un historial de subsanaciones reportadas
como cerradas que no lo estaban.

## Verificar lo que otro aplicó

Cuando el cambio lo aplique otra persona u otro asistente, **no cierres por su reporte**. Exporta el
Sheets a `.xlsx` —*Archivo → Descargar → Microsoft Excel*, guardar en `BD/`— y corre:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Compara encabezado por encabezado contra `modelo_objetivo.py`. La primera vez que se usó, sobre un
trabajo reportado como «100% cerrado y validado», encontró 23 fallos.

## Regla final

Si no puedes mostrar la salida de una comprobación, no lo declares conforme. Una referencia que
«debería» resolver es exactamente lo que este proyecto documentó durante meses.
