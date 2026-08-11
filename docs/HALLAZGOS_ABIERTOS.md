# Hallazgos abiertos

**Esto no es una especificación y no pasa por el pipeline.** Es la lista de lo que sabemos que está
mal o sin resolver, **y que no merece un documento propio**.

Existe porque hasta hoy todo hallazgo tenía dos destinos: convertirse en especificación, o perderse.
El primero hace que las especificaciones crezcan sin control; el segundo hace que el trabajo de
mirar se tire a la basura. Esta lista es el tercero.

**Regla de entrada.** Un hallazgo se convierte en especificación **solo si nombra qué se rompe en
producción** —«un técnico hará X y pasará Y»— y además exige una decisión de diseño. Si nombra la
rotura pero el arreglo ya está resuelto en otro sitio, se amplía la especificación que ya lo
resuelve. Si no nombra ninguna rotura, se queda aquí.

**Cada entrada trae su comando.** Sin comando no se puede saber si sigue abierta, y una lista que no
se puede verificar envejece igual que una cifra escrita a mano.

---

## La cascada de borrado de `MAN_Mantenimientos`

`FOT_Fotografias.MantenimientoID` lleva `es_parte_de=True`, así que borrar un mantenimiento borraría
en cascada sus fotografías. Y no es solo esa tabla: son **cuatro hijas** —`FOT_Fotografias`,
`FIR_Firmas`, `CHK_Checklists`, y `CHD_ChecklistDetalle` como nieta—.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;print([(t,c['nombre'],c['ref']) for t in MODELO for c in MODELO[t]['columnas'] if c.get('es_parte_de')])"
```

**Por qué no es una especificación, y no es por prioridad.** `RG-15` ya retira `Deletes` de
`MAN_Mantenimientos`, y su propia descripción lo dice: *«Protegido aqui arriba, el IsPartOf de FOT,
FIR y CHK nunca llega a dispararse»*. Dentro de la aplicación **no hay botón que borre** una fila
padre.

El residuo real es otro: **borrado a mano en el Sheets**, que dos cuentas tienen permiso para hacer.
Y ahí retirar `IsPartOf` **no arregla nada**, porque un borrado en la hoja no dispara cascada
ninguna: deja huérfanos. Tendría coste sin beneficio.

Queda aquí porque en un sistema cuyo propósito es que la evidencia sea difícil de falsificar, esto
se decide por escrito aunque la decisión sea «no se toca».

## `docs/PROMPT_CABLEADO.md` no es reproducible byte a byte

Su tabla de etiquetas ordena los empates de forma inestable, así que dos regeneraciones seguidas
producen diffs distintos sin que nada haya cambiado.

```bash
python scripts/generar_prompt_cableado.py && git diff --stat docs/PROMPT_CABLEADO.md
```

**Consecuencia práctica:** cualquier orden que regenere ese documento va a traer líneas de diff
espurias. Hay que avisarlo en la orden, para que no se lean como efecto del cambio.

No rompe nada en producción. Rompe la confianza en el `diff`, que es peor de lo que suena cuando el
método entero se apoya en leer de vuelta.

## `HERE()` sin señal escribe `0, 0` — MEDIDO, y salió la peor rama

**Ya no es una duda: está medido** (`docs/sdd/ACTA-011`). En el formulario real, con la
geolocalización no disponible, `HERE()` escribe el literal `0.000000, 0.000000`. **No deja el campo
vacío.**

De las dos ramas que `ESPEC-008` §2.9 planteó, salió la mala:

| Si | Consecuencia |
|---|---|
| dejara el campo vacío | el técnico no puede guardar — molesto, pero **visible el primer día** |
| escribe `0, 0` | **evidencia falsa e incorregible**: `Editable_If = FALSE` quita la única vía de corrección |

Con `RG-39` y `RG-40` ya cableadas, un técnico sin señal **registra una fotografía en el golfo de
Guinea y no puede arreglarlo**. Y esa coordenada **es** la evidencia: la compresión a 600 px descarta
el EXIF, no hay segunda fuente.

**Sigue abierto porque es una decisión de operación, no técnica.** `MAN_Mantenimientos` tiene válvula
de escape —`CierreConExcepcion` más `MotivoExcepcion`—; `FOT_Fotografias` y `NOV_Novedades` no tienen
ninguna. Tres salidas, con su coste, en `ACTA-011` §2: dejarlo, quitar la protección, o darles
válvula. La tercera es barata **hoy**, con las dos tablas en cero filas.

## ~~Qué pasa si `HERE()` no está disponible~~ — contestado arriba

_Lo que sigue es la entrada original, de cuando era una duda sin medir._


Sin señal, o con la ubicación denegada en el dispositivo, no está fijado si `HERE()` deja el campo
**vacío** o escribe **`0, 0`**. No hay página oficial que lo diga y no lo hemos medido.

Importa porque `ESPEC-008` propone `Editable_If = FALSE` sobre esas columnas, y eso **elimina la
única vía de corrección**: con el campo vacío y obligatorio, el técnico no puede guardar; con `0, 0`,
queda una evidencia falsa e incorregible.

**Es medible barato**, en la misma sesión de editor: abrir el formulario con la ubicación denegada y
mirar. Está en la tabla de supuestos sin verificar de `docs/BASE_CONOCIMIENTO_APPSHEET.md`.

## No hay comando que diga qué tipos quedaron pendientes en el editor

`inferencia.clasificar()` responde *qué columnas necesitan mano*, no *en cuáles ya pasó alguien*. La
API devuelve filas, no esquema.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from inferencia import clasificar;print({k:len(v) for k,v in clasificar().items()})"
```

Por eso `ESTADO.md` dice «unas 24 de 28 tablas» y no las nombra: nombrarlas sería inventar. La única
evidencia de qué se tocó son las actas de `docs/sdd/`.

Es el mismo límite que hace que **11 de los 13 pasos** de `docs/LO_QUE_SE_HACE_A_MANO.md` no tengan
ningún verificador.

## ~~`RECONSTRUCCION_EXPRESIONES.md` no propagaba la explicación de ninguna regla~~ — corregido

**Lo destapó `ORDEN-008` y se arregló el mismo día.** Se deja escrito porque el modo de fallo es
instructivo: `generar_reconstruccion.py` emitía el campo `nota` de cada regla, y **ninguna de las 23
reglas tiene `nota`** —todas usan `descripcion`—. Ese bloque **no se ejecutó nunca desde que existe**,
y el documento jamás llegó a explicar una sola regla.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;print('nota:',sum(1 for r in REGLAS if r.get('nota')),'descripcion:',sum(1 for r in REGLAS if r.get('descripcion')))"
```

**Por qué importó justo ahora:** la condición 1 del dictamen de `ESPEC-008` exigía meter la
instrucción *«cablear DESPUÉS del `Initial value`»* dentro de `descripcion` **para que llegara a quien
cablea** — y quien cablea lee justo este documento. La condición se aplicó, el texto se escribió, y
**no llegaba a su destino**. La regla salía como *«Tipo: `Editable_If` · `FALSE`»* y nada más.

Es el patrón de siempre en su versión más fina: **algo configurado, bien escrito, sin error, y sin
efecto**. Y esta vez el que no tenía efecto era el arreglo.

## `RG-06` y `RG-10` están creados y no pueden funcionar como están declarados

Los dos bots se crearon en el editor el 2026-08-11 (`docs/sdd/ACTA-009`) con su tabla, su evento y su
condición. **Los dos quedaron incompletos, y por el mismo motivo: el modelo no declara lo que
AppSheet exige para guardarlos.**

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;[print(r['id'],'|',r['expresion'],'|',r['descripcion']) for r in REGLAS if r['id'] in ('RG-06','RG-10')]"
```

| | Qué dice el modelo | Qué falta |
|---|---|---|
| `RG-06` | *«Envia correo con informe PDF al CCO y al supervisor»* | **Quién es el CCO** y con qué expresión se resuelve el supervisor |
| `RG-10` | *«Genera una orden de seguimiento enlazada mediante `OTOrigenID`»* | **El mapeo de columnas.** AppSheet lo exige literalmente: `The data action ... does not define a column to set` |

**No se completaron a ojo, y está bien.** Inventar un destinatario o un mapeo es decidir por
operación en una pantalla, sin registro. `RG-38` sí pudo cablearse porque `ESPEC-006` §3.3 fija su
mapeo columna por columna; estos dos no tienen equivalente.

**Por qué está aquí y no es una especificación.** No nombra una rotura: son dos reglas que **no
funcionan todavía**, no dos reglas que hagan daño. Y el contenido que falta no es una decisión de
diseño —es un dato que operación tiene o no tiene—. Cuando se sepa quién es el CCO, se escriben las
dos expresiones y se cablean; hasta entonces, especificarlo sería escribir alrededor del hueco.

Con una salvedad que sí conviene tener presente: **`RG-10` es la que crea la orden de seguimiento**, y
`PRUEBA-005` `P-11` y `P-12` prueban justo que la crea o no la crea. Esas dos pruebas no pueden pasar
hoy por una razón distinta de la que declaran.

## ~~`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` no propaga `descripcion` — la advertencia de `RG-39`/`RG-40` no llega por ese canal~~ — corregido

**Superado. Verificado al investigar `ESPEC-009` (2026-08-11):**

```bash
grep -c descripcion scripts/generar_reconstruccion.py
```

Devuelve `4`, no `0`. `generar_reconstruccion.py` ya lee `r["descripcion"]`, y
`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` ya muestra el bloque citado de `RG-39` y `RG-40` completo,
con la frase «CABLEAR DESPUES del Initial value» incluida — comprobado con
`grep -A6 "RG-39" docs/sdd/RECONSTRUCCION_EXPRESIONES.md`. Alguien lo corrigió después de escribir la
entrada de abajo, sin actualizarla. Se deja el texto original íntegro porque el modo de fallo —una
entrada de hallazgo que envejece sin que nadie la revise— es tan instructivo como el hallazgo mismo.

---

### El texto original, ya superado

`ESPEC-008` §4 afirma: *«El campo `descripcion` se propaga solo a los tres documentos generados; la
prosa de una especificación, no»* — y usa esa propagación como el motivo para poner la instrucción
«CABLEAR DESPUES del Initial value» dentro de `descripcion` en vez de solo en la prosa de la
especificación. **Es descripción incompleta de lo que hace el código, verificada al aplicar
`ORDEN-008`:**

```bash
grep -rn '"descripcion"' scripts/generar_*.py
```

Solo dos generadores leen `r["descripcion"]`: `generar_doc_arquitectura.py` (→
`docs/ARQUITECTURA_OBJETIVO_SGMC.md`) y `generar_prompt_expresiones.py` (→
`docs/PROMPT_EXPRESIONES.md`). **`generar_reconstruccion.py` no lo hace** — comprobado con
`grep -c descripcion scripts/generar_reconstruccion.py` → `0`. Y `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`
es, según el propio §4 de `ESPEC-008`, **el documento que nombra como canal del riesgo**: *«`RG-39`
llega a quien cablea a través de `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`, y allí aparece como «Tipo:
`Editable_If` · `FALSE`»»*. Verificado tras aplicar `ORDEN-008`:

```bash
grep -A6 "RG-39" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
```

Sigue mostrando solo `Tipo` y la expresión `FALSE`, sin ninguna mención a `Initial value` — exactamente
el riesgo que `ESPEC-008` §4 describe, sin cerrar, para el documento que el propio §4 nombra como el
peligroso. La instrucción sí llega por `PROMPT_EXPRESIONES.md` y `ARQUITECTURA_OBJETIVO_SGMC.md`
(verificado, ambos la traen completa), así que el riesgo está parcialmente mitigado, no del todo
abierto.

**Por qué no se corrige en `ORDEN-008`.** El único cambio de código que `ESPEC-008` autoriza es
`scripts/generar_prompt_cableado.py:327-331` (§4, verificado con diff). Tocar
`generar_reconstruccion.py` no está en ese alcance, y `ORDEN-008` no puede ampliar lo que el
arquitecto aprobó. Queda aquí para que la corrección —añadir la misma línea `w(r["descripcion"])` que
ya usan los otros dos generadores, condicionada a que exista— se decida con su propia especificación
o se sume a la próxima que toque `generar_reconstruccion.py`.

## El modelo declara `valor_inicial` y el editor puede no tenerlo

**Tres de tres columnas miradas el 2026-08-11 lo tenían vacío** (`docs/sdd/ACTA-011`), pese a que el
modelo declara su valor en las tres. Una de ellas —`MAN_Mantenimientos.Coordenadas_Cierre_LatLong`—
estaba **bloqueando el cierre de mantenimientos en producción**.

La causa está identificada y corregida (`ORDEN-008` parcheó `generar_prompt_cableado.py`), pero
**quien cableó la app siguió el documento roto**, así que el daño ya estaba hecho y nadie sabe cuánto
alcanza.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;[print('%-24s %-28s %-45s obl=%s ed=%s' % (t,c['nombre'],c['valor_inicial'],bool(c.get('obligatoria')),c.get('editable'))) for t in MODELO for c in MODELO[t]['columnas'] if c.get('valor_inicial')]"
```

**49 columnas declaran `valor_inicial`. Ninguna se puede comprobar por comando** — la API devuelve
filas, no esquema. Hay que mirarlas a ojo, y el orden lo da la gravedad, no el alfabeto:

| Cuántas | Estado | Qué pasa si falta |
|---|---|---|
| **3** | obligatorias **y** no editables | **bloqueo duro**: el formulario no se puede guardar |
| 4 | obligatorias, editables | el técnico lo teclea a mano cada vez |
| 42 | el resto | el campo llega vacío |

De las 3 del bloqueo duro, las tres se miraron el 2026-08-11 y **las tres estaban mal**. De las otras
46, ninguna.

## La cuenta que abre la app **no está en `USR_Usuarios`**, y eso vacía tres expresiones

```bash
python -c "import json,glob,os;f=max(glob.glob('BD/instantaneas/despues-*.json'),key=os.path.getmtime);d=json.load(open(f,encoding='utf-8'));print([r.get('Correo') for r in d['USR_Usuarios']])"
```

Los once usuarios son `@concesiondelsisga.com.co`. **`dieleoz@gmail.com`, que es la cuenta dueña de
la aplicación y con la que se entra al editor, no figura.**

`LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` devuelve **vacío** cuando el correo
logueado no está en esa lista. Y de esa expresión dependen:

| Columna | Obligatoria | Qué pasa si el `LOOKUP` sale vacío |
|---|---|---|
| `MAN_Mantenimientos.TecnicoID` | **sí** | el mantenimiento **no se puede guardar** |
| `NOV_Novedades.UsuarioID` | **sí** | la novedad **no se puede guardar** |
| `MAN_Mantenimientos.UsuarioRegistro` | no | queda en blanco |
| `FOT_Fotografias.Usuario` | no | queda en blanco |

**Y alcanza a algo que se cabló hoy.** La acción de `RG-38` mapea `OT_OrdenesTrabajo.SupervisorID`
—que es **obligatoria**— con ese mismo `LOOKUP`. Si el supervisor que pulsa el botón no está en
`USR_Usuarios`, **la acción falla al validar** y no crea la orden.

### Por qué importa más de lo que parece

`ESPEC-009` propone congelar esas columnas con `Editable_If = FALSE`, y su orden de cableado
—`Initial value` primero— **no protege contra esto**: la expresión puede estar perfectamente puesta
y devolver vacío igual. Es una **segunda vía al mismo bloqueo** que ya nos mordió con
`Coordenadas_Cierre_LatLong`, y por un motivo distinto.

Lo destapó el arquitecto de `ESPEC-009` y se verificó contra los datos el 2026-08-11.

### Qué hacer, y es una decisión, no un arreglo

1. **Añadir el correo de quien prueba a `USR_Usuarios`** — lo más simple, pero mete una cuenta que
   no es un técnico real en la tabla de técnicos.
2. **Probar siempre logueado como un usuario de la lista.** Es lo que `PRUEBA-005` ya hace con
   `USR-002` (`ivan.salcedo@`).
3. **Dar un valor por defecto al `LOOKUP`** para que nunca salga vacío.

Lo urgente no es elegir: es **saberlo antes de congelar nada**, porque después el síntoma es «no se
puede guardar un mantenimiento» y la causa parece el cableado cuando no lo es.

## Si una columna `Signature` se puede capturar sin cobertura

La documentación de offline trata `Image` explícitamente —se captura offline y sincroniza después— y
lista `Video`, `File` y audio como limitados. **No menciona `Signature`.**

Afecta a `FIR_Firmas.Imagen`, que es **la mitad de la cadena de evidencia**: un mantenimiento se cierra
con fotos y con la firma de quien lo recibe. Si la firma no se puede capturar sin cobertura, el cierre
se bloquea en los tramos sin red aunque las fotos sí funcionen.

Es razonable suponer que sí funciona —la firma se dibuja en el dispositivo, no se descarga— **pero es
un supuesto, no una cita**. Se mide sin cobertura, abriendo el formulario de firma. Detalle en
`docs/BASE_CONOCIMIENTO_APPSHEET.md` §22.

## Nadie ha comprobado si el modo offline está activado

`Settings > Offline mode` es una **configuración que hay que activar**, tabla por tabla, y no viene
puesta. **Si no lo está, un técnico sin cobertura no puede trabajar** —aunque su GPS funcione, que
funciona (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §21)—.

En un corredor vial de 137 km, trabajar sin cobertura no es un caso extremo.

**No se puede ver por API**: es configuración, no datos. Se mira en el editor, en esa misma pantalla,
y se anota por tabla —interesan sobre todo las ocho de movimiento, que son las que se llenan en
campo—.

El offline básico **es gratuito**; lo que exige plan Core o superior es `Server caching`, `Delta sync`
y `Quick sync`, o sea la velocidad de sincronización, no la capacidad de trabajar sin red.
