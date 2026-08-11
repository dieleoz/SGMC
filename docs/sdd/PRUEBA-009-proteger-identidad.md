# PRUEBA-009 — Pruebas de aceptación de ESPEC-009

**Sin fixture.** `MAN_Mantenimientos`, `NOV_Novedades` y `FOT_Fotografias` están en cero filas,
verificado contra producción por API sin escribir ningún archivo (`ESPEC-009` §2.3,
`python scripts/verificar_app.py`): no hay ningún flujo con datos que ejercitar. Todas las pruebas
de esta tanda son estructurales.

**Nada de lo que sigue se aplicó al repositorio real, al Sheets ni al editor.** Los comandos marcados
«predicho sobre copia» se corrieron contra una copia de `scripts/` y `docs/` fuera del repositorio,
con los cambios de `ESPEC-009` §4 aplicados solo ahí — mismo método que `PRUEBA-004`, `PRUEBA-007` y
`PRUEBA-008`. Las copias se borraron después de leerlas.

| | |
|---|---|
| Cubre | [`ESPEC-009-proteger-identidad.md`](ESPEC-009-proteger-identidad.md): proteger `MAN_Mantenimientos.TecnicoID`, `NOV_Novedades.UsuarioID`, `MAN_Mantenimientos.UsuarioRegistro` y `FOT_Fotografias.Usuario` con `editable=False` + `RG-41` a `RG-44` |
| Contra cuál sistema | `_SISGA_-323965761` sobre `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`), volcado en `BD/Modelo_Datos_PLANTILLA.xlsx`. Confirmado con `python scripts/sistema.py` |
| Reglas que esta tanda prueba | `RG-41`, `RG-42`, `RG-43`, `RG-44`, nuevas. No repite `RG-20`/`RG-39`/`RG-40`: ya cubiertas por `PRUEBA-004`/`PRUEBA-008` |
| Innegociables | `P-76`, `P-79`, `P-80` |

## 1. Estado de partida, para que `P-76` tenga con qué compararse

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 23
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

Corrido contra el repositorio real, hoy, sin ningún cambio de `ESPEC-009` aplicado. `Reglas: 23` es
la cifra que `P-76` tiene que subir a `27`; `Columnas: 209` es la cifra que **no** debe moverse: este
cambio no retira ni añade ninguna columna física, solo un parámetro sobre cuatro que ya existen.

## P-76 — El modelo sube a 27 reglas, sin errores, con los mismos avisos (innegociable)

**Predicho sobre copia**, con `ESPEC-009` §4 aplicado íntegro (los cuatro `editable=False` y los
cuatro `dict` de `RG-41` a `RG-44`):

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 209  |  Referencias: 39  |  Reglas: 27
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

**Pasa si:** `Columnas: 209` (sin cambio), `Reglas: 27` (sube de 23), `ERRORES: ninguno` —en
particular sin `V-10`, que dispararía si alguna de las cuatro reglas apuntara a una tabla o columna
que no existe—, y los tres avisos son exactamente los tres que ya existían antes de este cambio.

**Cómo se distingue el fallo:** si `RG-41` a `RG-44` se escriben con un error de tipeo en `tabla` o
`columna` (por ejemplo `Tecnicoid`, minúscula de más), `validar_modelo.py` termina con `ERRORES: 1` y
el mensaje nombra la regla y la ruta exacta que no existe.

## P-77 — La consulta exacta del encargo, antes y después (positiva)

**Predicho sobre copia**, replicando literalmente el comando que `ESPEC-009` §1 corrió contra el
repositorio real:

```
$ python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;[print(t,c['nombre'],c.get('tipo'),'editable=',c.get('editable'),'|',c.get('valor_inicial')) for t in MODELO for c in MODELO[t]['columnas'] if 'USEREMAIL' in str(c.get('valor_inicial'))]"
MAN_Mantenimientos TecnicoID Ref editable= False | LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")
MAN_Mantenimientos UsuarioRegistro Text editable= False | USEREMAIL()
NOV_Novedades UsuarioID Ref editable= False | LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")
FOT_Fotografias Usuario Text editable= False | USEREMAIL()
```

**Pasa si:** las cuatro filas traen `editable= False`. **Antes** de aplicar el cambio, la misma
consulta sobre el repositorio real trae las cuatro con `editable= None` (transcrito en `ESPEC-009`
§1); se corren las dos, no solo una, para que el contraste sea la prueba y no una lectura suelta.

## P-78 — Solo estas cuatro columnas quedan `editable=False` en todo el modelo (negativa)

**Qué discrimina:** que el cambio se aplicó exactamente a las cuatro columnas del encargo, ni una
menos ni una de más — el modo de fallo contrario al que motivó esta especificación, y el mismo tipo
de prueba que `PRUEBA-008` `P-71` usó para `FOT_Fotografias`, aquí extendido a todo el modelo porque
esta especificación toca tres tablas, no una.

**Predicho sobre copia**, con `ESPEC-009` §4 aplicado:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO
print(sorted([(t,c['nombre']) for t in MODELO for c in MODELO[t]['columnas'] if c.get('editable') is False]))
"
[('FOT_Fotografias', 'Ubicacion_LatLong'), ('FOT_Fotografias', 'Usuario'), ('MAN_Mantenimientos', 'Coordenadas_Cierre_LatLong'), ('MAN_Mantenimientos', 'FechaHoraEscaneo'), ('MAN_Mantenimientos', 'TecnicoID'), ('MAN_Mantenimientos', 'UbicacionEscaneo_LatLong'), ('MAN_Mantenimientos', 'UsuarioRegistro'), ('NOV_Novedades', 'Ubicacion_LatLong'), ('NOV_Novedades', 'UsuarioID')]
```

**Pasa si:** la lista tiene exactamente **9** entradas: las 3 de `RG-20` + las 2 de `RG-39`/`RG-40`
(ya existentes, verificadas por `PRUEBA-004`/`PRUEBA-008`) + las 4 nuevas de esta tanda. Ninguna
columna fuera de esas nueve debe aparecer — en particular, ninguna de `OT_OrdenesTrabajo`,
`ACT_Activos`, `SED_Sedes` ni `USR_Usuarios`.

**Cómo se distingue el fallo:** si alguien, al aplicar `ESPEC-009` §4, marca por error una columna
de más —por ejemplo `SupervisorID` o `CerradaPor` de `OT_OrdenesTrabajo`, que también son `Ref` a
`USR_Usuarios`—, esta lista lo muestra de inmediato: aparecería una décima entrada donde el conteo
exige nueve.

## P-79 — `OT_OrdenesTrabajo.TecnicoID` queda intacta, y su tabla también (innegociable)

**Qué discrimina:** esta es la prueba central del documento. `ESPEC-009` §1 y §2.7 dependen de que
la columna de asignación, que comparte nombre con una de las cuatro protegidas, **no** se toque. Si
alguien la confunde y la congela también, un supervisor deja de poder reasignar una orden — la
rotura que `ESPEC-009` §1 verificó que no ocurre, y que esta prueba comprueba que sigue sin ocurrir
después de aplicar el cambio.

**Predicho sobre copia**, con `ESPEC-009` §4 aplicado:

```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,REGLAS
for c in MODELO['OT_OrdenesTrabajo']['columnas']:
    print(c['nombre'], 'editable=', c.get('editable'), 'valor_inicial=', c.get('valor_inicial'))
print('reglas de OT_OrdenesTrabajo:', sorted([(r['id'], r['tipo']) for r in REGLAS if r['tabla']=='OT_OrdenesTrabajo']))
"
OTID editable= None valor_inicial= None
ActivoID editable= None valor_inicial= None
TecnicoID editable= None valor_inicial= None
SupervisorID editable= None valor_inicial= None
Tipo editable= None valor_inicial= None
FechaProgramada editable= None valor_inicial= None
EstadoOrdenID editable= None valor_inicial= None
OTOrigenID editable= None valor_inicial= None
Observaciones editable= None valor_inicial= None
FechaCierre editable= None valor_inicial= None
CerradaPor editable= None valor_inicial= None
Activo editable= None valor_inicial= TRUE
reglas de OT_OrdenesTrabajo: [('RG-05', 'Security Filter'), ('RG-07', 'Bot'), ('RG-14', 'Are updates allowed'), ('RG-35', 'App formula'), ('RG-37', 'App formula')]
```

**Pasa si:** ninguna columna de `OT_OrdenesTrabajo` trae `editable= False`, `TecnicoID` sigue sin
`valor_inicial`, y la lista de reglas de esa tabla es exactamente la misma que antes de aplicar
`ESPEC-009` —cinco reglas, ninguna `Editable_If`—, en particular que `RG-14` siga declarando
`Updates, Adds` (verificado también sin cambios: `expresion='Updates, Adds'`, sin tocar).

**Cómo se distingue el fallo:** si `ESPEC-009` §4 se aplicara por error sobre
`OT_OrdenesTrabajo.TecnicoID` en vez de (o además de) `MAN_Mantenimientos.TecnicoID`, esta columna
aparecería con `editable= False` y una sexta regla `Editable_If` en la lista de `OT_OrdenesTrabajo`.
No hay forma de que ese error pase inadvertido.

## P-80 — El generador ya parchado sigue citando el `Initial value` de las cuatro (no regresión, innegociable)

**Esta prueba demuestra que el cambio de `ESPEC-009` no necesita ningún parche de código, y que si
alguien revirtiera el de `ORDEN-008` el problema volvería** — la misma disciplina que `PRUEBA-008`
`P-72` fijó para no repetir una prueba que no puede fallar (`PRUEBA-007` `P-66`).

**Paso 1 — antes de tocar nada, sobre el repositorio real:**

```
$ python scripts/generar_prompt_cableado.py
$ grep -n "^| \`MAN_Mantenimientos\` | \`TecnicoID\` | \`Initial value\`" docs/PROMPT_CABLEADO.md
508:| `MAN_Mantenimientos` | `TecnicoID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
```

**Paso 2 — predicho sobre una copia distinta, con `RG-41` aplicada Y revirtiendo el parche de
`ORDEN-008` a la versión previa** (`_cubiertas = {(r["tabla"], r.get("columna")) for r in REGLAS}`,
sin distinguir por tipo de propiedad — el código que `ESPEC-008` §2.6 documentó como roto):

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`TecnicoID\` | \`Initial value\`" docs/PROMPT_CABLEADO.md
(sin resultado)
```

> Esto demuestra que la prueba **sí puede fallar**: si `ORDEN-008` no se hubiera aplicado, o alguien
> revirtiera su parche por error en un cambio posterior, esta misma fila desaparecería al aplicar
> `ESPEC-009` sin que nadie lo avisara — exactamente el defecto que `ESPEC-008` §2.6 encontró y
> corrigió, aquí usado para confirmar que la corrección sigue vigente.

**Paso 3 — predicho sobre la copia de `ESPEC-009` §4, con el generador tal como está hoy en el
repositorio real (ya parcheado por `ORDEN-008`):**

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`TecnicoID\` | \`Initial value\`" docs/PROMPT_CABLEADO.md
508:| `MAN_Mantenimientos` | `TecnicoID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
```

**Pasa si:** el Paso 1 y el Paso 3 traen la fila y el Paso 2 no la trae. **Esta prueba falla de
verdad** si el parche de `ORDEN-008` deja de estar en el repositorio en el momento de aplicar
`ESPEC-009`: el Paso 2 es literalmente lo que quedaría en ese caso.

**Verificado también para las otras tres columnas**, mismo patrón, mismo resultado (presentes antes
y después con el generador parcheado):

```
$ grep -n "^| \`MAN_Mantenimientos\` | \`UsuarioRegistro\` | \`Initial value\`\|^| \`NOV_Novedades\` | \`UsuarioID\` | \`Initial value\`\|^| \`FOT_Fotografias\` | \`Usuario\` | \`Initial value\`" docs/PROMPT_CABLEADO.md
509:| `MAN_Mantenimientos` | `UsuarioRegistro` | `Initial value` | `USEREMAIL()` |
514:| `NOV_Novedades` | `UsuarioID` | `Initial value` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
490:| `FOT_Fotografias` | `Usuario` | `Initial value` | `USEREMAIL()` |
```

## P-81 — `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` propaga la instrucción de orden de `RG-41` (positiva)

**Qué discrimina:** que la advertencia "CABLEAR DESPUES del Initial value", puesta dentro de
`descripcion` (`ESPEC-009` §4), efectivamente llegue al documento que el ejecutor lee para cablear —
y de paso, confirma que la entrada de `docs/HALLAZGOS_ABIERTOS.md` que decía lo contrario está
superada (`ESPEC-009` §2.10).

**Predicho sobre copia**, con `ESPEC-009` §4 aplicado:

```
$ python scripts/generar_reconstruccion.py
$ grep -A9 "### RG-41" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
### RG-41 — `MAN_Mantenimientos` · `TecnicoID`

**Tipo:** Editable_If · cubre Prueba de identidad

```
FALSE
```

> LOOKUP(USEREMAIL(),...) es Initial value, no App formula, y un Initial value SI es editable: TecnicoID se dibuja como desplegable de USR_Usuarios sin filtrar, y con un toque el tecnico logueado puede atribuir la ejecucion a otro companero. CABLEAR DESPUES del Initial value = LOOKUP(...): al reves la columna queda obligatoria, no editable y vacia, y ningun tecnico puede guardar el mantenimiento. No congela OT_OrdenesTrabajo.TecnicoID (asignacion, columna distinta, sin Initial value, fuera de alcance): un supervisor sigue reasignando la orden sin verse afectado por esta regla. ESPEC-009.
```

**Pasa si:** la frase `CABLEAR DESPUES del Initial value` aparece dentro del bloque citado (`> `) de
`RG-41`, no solo en el tipo y la expresión. **Cómo se distingue el fallo:** si
`generar_reconstruccion.py` dejara de leer `descripcion` —la regresión que `docs/HALLAZGOS_ABIERTOS.md`
describía como vigente y que el §2.10 de `ESPEC-009` encontró ya corregida—, el bloque citado no
aparecería en absoluto, solo `**Tipo:** Editable_If · cubre Prueba de identidad` y la expresión.

## P-82 — La hoja no cambia (`verificar_faseA.py`, sin regresión)

**Predicho sobre copia**, con `ESPEC-009` §4 aplicado, sin regenerar la plantilla (`ESPEC-009` §4
argumenta que no hace falta: `editable` no tiene representación física en el Excel):

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
...
AVISOS (2) - esperados, no bloquean:
  - [F-01] OT_OrdenesTrabajo.Activo sigue existiendo, pero el modelo lo reutiliza como columna propia. Correcto, no es un fallo
  - [F-04] 14 columnas siguen pendientes de retipar a Ref. Es trabajo de la Fase B, en el editor de AppSheet, no de la hoja
==============================================================================
FASE A CERRADA
```

**Pasa si:** `AVISOS (2)`, idénticos a los del repositorio real hoy sin este cambio — ningún `[F-03]`
ni `[F-19] ESTADO MIXTO`. Si esta prueba fallara con avisos nuevos, el supuesto de `ESPEC-009` §4 de
que `editable` no toca la hoja física sería falso, y habría que investigar antes de cerrar esta
tanda.

## P-83 — Lectura de vuelta: qué tiene que verse en el editor (lectura de vuelta, pendiente de sesión de navegador)

**No se puede ejecutar sin sesión de navegador.** Se deja escrita para que quien la ejecute no tenga
que decidir qué mirar, y en el orden que `ESPEC-009` §2.9 y §6 fijan como obligatorio.

- **Precondición:** `ESPEC-009` aplicada al modelo, `RG-41` a `RG-44` cableadas.
- **Paso 1, antes de cambiar nada — leer el `Initial value` de las cuatro, sin activar el icono `=`**
  (incidente ya documentado en `ACTA-004` §5: activarlo sobre un campo sin expresión previa puede
  dejarlo en un estado inválido y tumbar la app):
  - `Data > Columns > MAN_Mantenimientos > TecnicoID > Auto Compute > Initial value` — debe traer
    `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")`.
  - `Data > Columns > NOV_Novedades > UsuarioID > Auto Compute > Initial value` — mismo valor.
  - `Data > Columns > MAN_Mantenimientos > UsuarioRegistro > Auto Compute > Initial value` — debe
    traer `USEREMAIL()`.
  - `Data > Columns > FOT_Fotografias > Usuario > Auto Compute > Initial value` — mismo valor.
  - **Si alguna está vacía**, no aplicar `Editable_If` sobre esa columna todavía: ponerle primero el
    `Initial value` que falte, guardar, y solo entonces continuar con el paso 2 para esa columna.
    `TecnicoID` y `UsuarioID` son obligatorias: aplicar `Editable_If = FALSE` sobre cualquiera de las
    dos sin `Initial value` puesto bloquea el formulario correspondiente por completo.
- **Paso 2 — `Update Behavior > Editable?` de las cuatro** — debe quedar resaltado como con
  expresión, con `FALSE` dentro.
- **Resultado esperado:** las cuatro con `Initial value` puesto y `Editable?` en `FALSE`.
- **Cómo se distingue el fallo:** si `Editable?` está en `TRUE` sin expresión, la regla
  correspondiente no llegó a cablearse y el defecto original sigue abierto en esa columna. Si
  `Initial value` está vacío y `Editable?` ya está en `FALSE`, se aplicó en el orden equivocado —el
  riesgo nombrado en `ESPEC-009` §2.9 y §6— y hay que revertir `Editable_If` a `TRUE` antes de que
  cualquier técnico intente guardar un mantenimiento o una novedad.
- **Tercera comprobación, en el formulario, no en `Data > Columns`:** abrir `Add a new
  MAN_Mantenimientos` y confirmar que `TecnicoID` se ve como el nombre del usuario que abrió el
  formulario, **sin poder tocarse** (a diferencia de como se comportaría hoy, antes de este cambio,
  donde es un desplegable normal). Abrir por separado `Data: OT_OrdenesTrabajo > Edit` sobre una
  orden existente y confirmar que `TecnicoID` **sigue siendo editable** ahí — es la comprobación
  directa de que la reasignación de un supervisor no quedó bloqueada (`ESPEC-009` §2.7, `P-79`).

## Lo que esta tanda NO prueba, y por qué

- **No prueba ningún flujo con datos reales.** No hay fixture: las tres tablas están en cero filas en
  producción, no solo en el volcado (`ESPEC-009` §2.3).
- **No repite `PRUEBA-004` ni `PRUEBA-008`.** `RG-20`, `RG-39` y `RG-40` son cambios distintos, ya
  cubiertos por esas tandas.
- **No prueba ninguna regla que compare `MAN_Mantenimientos.TecnicoID` contra
  `OT_OrdenesTrabajo.TecnicoID`.** No existe: `ESPEC-009` §5 decide no proponerla.
- **No prueba ninguna vía de corrección de una autoatribución equivocada.** No existe: `ESPEC-009` §5
  decide no construirla dentro de esta especificación.
