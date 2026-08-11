# PRUEBA-008 — Pruebas de aceptación de ESPEC-008

**Sin fixture.** `FOT_Fotografias` está en cero filas, verificado tanto en el volcado como en
producción por API (`ESPEC-008` §2.3): no hay ningún flujo con datos que ejercitar. Todas las
pruebas de esta tanda son estructurales.

**Nada de lo que sigue se aplicó al repositorio real, al Sheets ni al editor.** Los comandos
marcados «predicho sobre copia» se corrieron contra una copia de `scripts/` y `docs/` fuera del
repositorio, con los cambios de `ESPEC-008` §4 aplicados solo ahí — mismo método que `PRUEBA-004`,
`PRUEBA-005` y `PRUEBA-007`. La copia se borró después de leerla.

| | |
|---|---|
| Cubre | [`ESPEC-008-proteger-ubicacion-fotografias.md`](ESPEC-008-proteger-ubicacion-fotografias.md): proteger `FOT_Fotografias.Ubicacion_LatLong` con `editable=False` + `RG-39`, y corregir el generador que el §2.6 encontró roto |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Confirmado con `python scripts/sistema.py` |
| Reglas que esta tanda prueba | `RG-39`, nueva. No repite `RG-20`: sigue cubierta por `PRUEBA-004` |
| Innegociables | `P-69`, `P-72` |

## 1. Estado de partida, para que `P-69` tenga con qué compararse

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 21
Tablas retiradas: 5  |  Campos retirados de MAN: 14
------------------------------------------------------------------------------
ERRORES: ninguno

AVISOS (3) - revisar, no bloquean: [V-06] x2, [V-14]
==============================================================================
APTO PARA DESPLEGAR
```

Corrido contra el repositorio real, hoy, sin ningún cambio de `ESPEC-008` aplicado. `Reglas: 21` es
la cifra que `P-69` tiene que subir a `22`; `Columnas: 210` es la cifra que **no** debe moverse —a
diferencia de `PRUEBA-007`, este cambio no retira ni añade ninguna columna física, solo un parámetro
sobre una que ya existe.

## P-69 — El modelo sube a 22 reglas, sin errores, con los mismos avisos (innegociable)

**Predicho sobre copia**, con `ESPEC-008` §4 aplicado (el `editable=False` del `col()` y el `dict`
de `RG-39`, sin el parche del generador — ese lo prueba `P-72` aparte):

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 210  |  Referencias: 39  |  Reglas: 22
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

**Pasa si:** `Columnas: 210` (sin cambio), `Reglas: 22` (sube de 21), `ERRORES: ninguno` —en
particular sin `V-10`, que dispararía si `RG-39` apuntara a una tabla o columna que no existe—, y los
tres avisos son exactamente los tres que ya existían antes de este cambio.

**Cómo se distingue el fallo:** si `RG-39` se escribe con un error de tipeo en `tabla` o `columna`
(por ejemplo `Ubicacion_Latlong`, minúscula de más), `validar_modelo.py` termina con `ERRORES: 1` y
el mensaje nombra la regla y la ruta exacta que no existe. No hay forma de que este error pase
inadvertido.

## P-70 — La consulta exacta del encargo, antes y después (positiva)

**Predicho sobre copia**, replicando literalmente el comando que `ESPEC-008` §2.1 corrió contra el
repositorio real:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,REGLAS
print([(t,c['nombre']) for t in MODELO for c in MODELO[t]['columnas'] if c.get('editable') is False])
print([(r['id'],r['tabla'],r.get('columna')) for r in REGLAS if r['tipo']=='Editable_If'])
"
[('MAN_Mantenimientos', 'UbicacionEscaneo_LatLong'), ('MAN_Mantenimientos', 'FechaHoraEscaneo'), ('MAN_Mantenimientos', 'Coordenadas_Cierre_LatLong'), ('FOT_Fotografias', 'Ubicacion_LatLong')]
[('RG-20', 'MAN_Mantenimientos', '(varias)'), ('RG-39', 'FOT_Fotografias', 'Ubicacion_LatLong')]
```

**Pasa si:** `('FOT_Fotografias', 'Ubicacion_LatLong')` aparece en la primera lista y
`('RG-39', 'FOT_Fotografias', 'Ubicacion_LatLong')` en la segunda. **Antes** de aplicar el cambio, la
misma consulta sobre el repositorio real no trae ninguna de las dos (transcrito en `ESPEC-008` §2.1);
se corren las dos, no solo una, para que el contraste sea la prueba y no una lectura suelta.

## P-71 — Ninguna otra columna de `FOT_Fotografias` queda tocada (negativa)

**Qué discrimina:** que el cambio se aplicó solo a `Ubicacion_LatLong`, no a la tabla entera por
error de alcance —el modo de fallo contrario al que motivó esta especificación.

**Predicho sobre copia**, con `ESPEC-008` §4 aplicado:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,REGLAS
for c in MODELO['FOT_Fotografias']['columnas']:
    print(c['nombre'], 'editable=', c.get('editable'))
print('reglas de FOT:', [(r['id'], r['columna']) for r in REGLAS if r['tabla']=='FOT_Fotografias'])
"
FotoID editable= None
MantenimientoID editable= None
Tipo editable= None
Archivo editable= None
Ubicacion_LatLong editable= False
PrecisionGPS editable= None
FechaHora editable= None
Usuario editable= None
reglas de FOT: [('RG-39', 'Ubicacion_LatLong')]
```

**Pasa si:** de las ocho columnas, solo `Ubicacion_LatLong` trae `editable= False`, y
`FOT_Fotografias` tiene exactamente una regla, `RG-39`, sobre exactamente esa columna.

**Cómo se distingue el fallo:** si alguien, al aplicar `ESPEC-008` §4, copia y pega mal y marca por
ejemplo `Archivo` o `Tipo` como `editable=False` también, esta lista lo muestra de inmediato — y esas
dos columnas **deben** seguir editables: `Archivo` es la foto misma, no una coordenada, y `Tipo`
(`Antes`/`Después`/`Novedad`) lo elige el técnico a propósito.

## P-72 — El generador deja de citar `Initial value`, y el parche lo repara (innegociable)

**Esta prueba existe porque el arquitecto acaba de cazar una prueba que no podía fallar** (nota de
cabecera de `PRUEBA-007` sobre su propio `P-66`). Esta no repite ese error: se corre **con** y **sin**
el parche del §2.6, y las dos salidas son distintas y verificables — si algún día dejaran de serlo,
la prueba fallaría de verdad, no en apariencia.

**Paso 1 — antes de tocar nada, sobre el repositorio real:**

```
$ python scripts/generar_prompt_cableado.py
$ grep -n "FOT_Fotografias.*Ubicacion_LatLong\|Ubicacion_LatLong.*FOT_Fotografias" docs/PROMPT_CABLEADO.md
491:| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
```

**Paso 2 — predicho sobre copia, con `RG-39` aplicado y SIN el parche del generador:**

```
$ grep -n "FOT_Fotografias.*Ubicacion_LatLong" docs/PROMPT_CABLEADO.md
(sin resultado en la tabla de Initial value; solo quedan PrecisionGPS y Usuario)
```

**Paso 3 — predicho sobre la misma copia, aplicando además el parche exacto de `ESPEC-008` §2.6/§4:**

```
$ grep -n "^| \`FOT_Fotografias\` | \`Ubicacion_LatLong\`" docs/PROMPT_CABLEADO.md
491:| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
```

**Pasa si:** el Paso 1 y el Paso 3 traen la fila y el Paso 2 no la trae. **Esta prueba falla de
verdad** si `ORDEN-008` aplica `RG-39` sin el parche: el Paso 2 es literalmente lo que queda en el
repositorio real en ese caso, y `P-72` lo detecta comparando contra el Paso 1, no adivinándolo.

**Efecto colateral que también se comprueba, porque el parche es general y no específico de esta
columna:**

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`Coordenadas_Cierre_LatLong\`" docs/PROMPT_CABLEADO.md
(antes del parche: sin resultado, pese a que la columna SÍ tiene Initial value = HERE() declarado)
(despues del parche: 506:| `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | `Initial value` | `HERE()` |)
```

**Esto no lo prueba `PRUEBA-004` ni ningún otro documento existente**: el defecto es anterior a
`ESPEC-008` y nadie lo había escrito como caso de prueba. Se deja registrado aquí porque es donde se
encontró (`ESPEC-008` §2.6), no porque sea competencia de esta tanda mantenerlo — si `PRUEBA-004` se
vuelve a tocar por otro motivo, debería incorporar esta fila también.

## P-73 — `docs/MANUAL_DESPLIEGUE.md` no depende del defecto de `P-72` (positiva, red de seguridad)

**Predicho sobre copia**, con `RG-39` aplicado y **sin** el parche del generador — para comprobar que
esta tabla, a diferencia de la de `PROMPT_CABLEADO.md`, no se ve afectada:

```
$ python scripts/generar_manual_despliegue.py
$ grep -n "^| \`Ubicacion_LatLong\`" docs/MANUAL_DESPLIEGUE.md
| `Ubicacion_LatLong` | `LatLong` | `Initial value` = `HERE()` |
```

**Pasa si:** la fila aparece con `Initial value = HERE()` incluso sin el parche de `P-72` aplicado
— confirma que `docs/MANUAL_DESPLIEGUE.md:1127-1129` recorre todas las columnas sin depender de
`REGLAS`, y por tanto sigue siendo una referencia completa aunque `PROMPT_CABLEADO.md` no lo sea
todavía.

## P-74 — La hoja no cambia (`verificar_faseA.py`, sin regresión)

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

**Predicho sobre copia**, con `ESPEC-008` §4 aplicado, sin regenerar la plantilla (`ESPEC-008` §4
argumenta que no hace falta: `editable` no tiene representación física en el Excel):

```
AVISOS (2) - esperados, no bloquean:
  - [F-01] OT_OrdenesTrabajo.Activo sigue existiendo, pero el modelo lo reutiliza como columna propia. Correcto, no es un fallo
  - [F-04] 14 columnas siguen pendientes de retipar a Ref. Es trabajo de la Fase B, en el editor de AppSheet, no de la hoja
==============================================================================
FASE A CERRADA
```

**Pasa si:** `AVISOS (2)`, idénticos a los que trae el repositorio real hoy sin este cambio — ningún
`[F-03]` ni `[F-19] ESTADO MIXTO`. A diferencia de `PRUEBA-007` `P-68`, aquí **no** hace falta
regenerar `BD/Modelo_Datos_PLANTILLA.xlsx`: si esta prueba fallara con avisos nuevos, significaría que
el supuesto de `ESPEC-008` §4 —que `editable` no toca la hoja física— es falso, y habría que
investigar antes de cerrar esta tanda.

## P-75 — Lectura de vuelta: qué tiene que verse en el editor (lectura de vuelta, pendiente de sesión de navegador)

**No se puede ejecutar sin sesión de navegador.** Se deja escrita para que quien la ejecute no tenga
que decidir qué mirar.

- **Precondición:** `ORDEN-008` aplicada al modelo, generador parcheado, `RG-39` cableada.
- **Acción:** en `Data > Columns > FOT_Fotografias > Ubicacion_LatLong`, leer **sin activar el icono
  `=`** —incidente ya documentado en `ACTA-004` §5: activarlo sobre un campo sin expresión previa
  puede dejarlo en un estado inválido y tumbar la app— el campo `Update Behavior > Editable?` y el
  campo `Auto Compute > Initial value`.
- **Resultado esperado:** `Editable?` resaltado como con expresión, con `FALSE` dentro; `Initial
  value` con `HERE()`.
- **Cómo se distingue el fallo:** si `Editable?` está en `TRUE` sin expresión, `RG-39` no llegó a
  cablearse y el defecto original sigue abierto. Si `Initial value` está vacío, se aplicó
  `Editable_If` sin `Initial value` —el riesgo nombrado en `ESPEC-008` §6— y el formulario de
  fotografías está roto: hay que revertir `Editable_If` a `TRUE` en el editor antes de que cualquier
  técnico intente subir una fotografía.
- **Segunda comprobación, en el mismo formulario, no en `Data > Columns`:** abrir el formulario de
  alta de una fotografía nueva (`Add a new FOT_Fotografias`) y confirmar que el mapa de
  `Ubicacion_LatLong` **muestra un pin fijo, sin el ícono de arrastre**, a diferencia de como se ve
  hoy `Coordenadas_Cierre_LatLong` en `MAN_Mantenimientos` **antes** de `RG-20` (que ya no se puede
  reproducir, porque `RG-20` está aplicada) — la comparación visual de referencia es la captura que
  documenta `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` §7.1 para el mismo mecanismo.

## Lo que esta tanda NO prueba, y por qué

- **No prueba `NOV_Novedades.Ubicacion_LatLong`.** `ESPEC-008` §5 la deja fuera de alcance a
  propósito; no hay cambio que probar.
- **No prueba ningún flujo con datos reales.** No hay fixture: `FOT_Fotografias` está en cero filas
  en producción, no solo en el volcado (`ESPEC-008` §2.3).
- **No repite `PRUEBA-004` ni `PRUEBA-007`.** `RG-20` y el retiro de `PrecisionGPS` son cambios
  distintos, ya cubiertos por esas tandas.
- **No prueba el `Valid_If` de geofencing sobre fotografías.** No existe: `ESPEC-008` §2.9 decide no
  proponerlo.
