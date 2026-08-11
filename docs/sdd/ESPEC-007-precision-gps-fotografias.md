# ESPEC-007 — `FOT_Fotografias.PrecisionGPS`: retirar una función inexistente que nadie lee

## 0. Por qué este documento es corto, y por qué eso es la conclusión y no un atajo

`ESPEC-004` resolvió el mismo síntoma —`USERLOCATIONACCURACY()`, que no existe en AppSheet— sobre
`MAN_Mantenimientos.Precision_GPS`, y le hicieron falta 488 líneas porque esa columna alimentaba una
cadena de tres reglas (`RG-02` → `RG-19` → `RG-03`) que dejaba a `MotivoExcepcion` sin pedirse nunca.
Aquí no hay cadena: se verifica en el §2.2 que **ninguna regla del modelo lee
`FOT_Fotografias.PrecisionGPS`**. No hay nada que se rompa aguas abajo porque no hay aguas abajo.
Lo único que decide este documento es si algo *debería* leerla — no lo hay, §7 — y cómo se declara
su retiro. El §2.6 muestra que ni siquiera hace falta editar un generador aparte de
`scripts/modelo_objetivo.py`: los tres documentos que hoy instruyen a cablear la función inexistente
la citan por un bucle genérico sobre `valor_inicial`, y dejan de citarla solos en cuanto se quita de
ahí.

## 1. Qué se quiere y por qué

`scripts/modelo_objetivo.py:427` declara `FOT_Fotografias.PrecisionGPS` con
`valor_inicial="USERLOCATIONACCURACY()"`. Esa función no existe en AppSheet — verificado en
`ESPEC-004` §2.1 contra la página oficial de captura de GPS de AppSheet Help, consultada el
2026-08-10 — así que la columna nunca se va a poblar. La decisión que este documento permite tomar:
**¿hace falta que algo lea esa columna, o se retira?** La respuesta, verificada en §2, es que hoy no
la lee nada, y §7 argumenta por qué tampoco debería.

Sin este documento, el modelo sigue instruyendo a quien cablee el editor a escribir una función que
el propio editor va a rechazar, y tres documentos generados van a seguir repitiendo esa instrucción
cada vez que se regeneren.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

```
$ python scripts/sistema.py
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026 (fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Verificado contra el volcado local (`openpyxl`) y contra `scripts/modelo_objetivo.py`. No se leyó
producción por API para este documento: `FOT_Fotografias` es una de las ocho tablas de movimiento
que el volcado vacía por diseño (`CLAUDE.md` §7.15), pero su **estructura** —qué columnas tiene el
modelo, no qué filas trae la hoja— no depende de esa lectura, y el §2.7 cita en su lugar el estado
del editor que ya midieron `ACTA-004` y `docs/CORRECCIONES_CABLEADO.md`.

### 2.1 `USERLOCATIONACCURACY()` no existe — y lo que este documento NO puede verificar por sí mismo

Que la función no existe está verificado por `ESPEC-004` §2.1 contra la documentación oficial de
AppSheet, y no se repite la cita aquí. Lo que el encargo de esta especificación añade es que **el
editor la rechazó al intentar escribirla sobre `FOT_Fotografias.PrecisionGPS`**, con el mensaje
`Can't find function "USERLOCATIONACCURACY"`. **Eso se reporta aquí como dicho por el ejecutor de la
sesión anterior, no como verificado por este documento**: no existe en el repositorio ninguna acta ni
transcripción con esa cadena literal —

```
$ grep -rn "Can't find function" . --include=*.md
(sin resultado)
```

— así que no hay artefacto que lo sostenga más allá del reporte de quien lo vio en pantalla. No
cambia la conclusión (la función ya está descartada por la cita oficial, independientemente de si el
editor la rechazó una vez o cien), pero si en algún momento hace falta citar el rechazo del editor
como hecho, hace falta una transcripción nueva — mismo criterio que `ACTA-004` aplicó al tipo de
`CierreConExcepcion`.

### 2.2 Ninguna regla del modelo lee `PrecisionGPS` — la diferencia real con `ESPEC-004`

```
$ python -c "
import sys; sys.path.insert(0,'scripts')
import modelo_objetivo as M
print([r['id'] for r in M.REGLAS if r.get('tabla')=='FOT_Fotografias'])
"
[]
```

**Ninguna regla declarada toca `FOT_Fotografias`, ni por `PrecisionGPS` ni por ninguna otra
columna.** Esto es lo que separa este caso del de `MAN_Mantenimientos.Precision_GPS`: ahí `RG-19`
comparaba el valor en blanco contra `PAR_Parametros.UMBRAL_GPS` y volvía inerte a `RG-03`, así que un
técnico podía cerrar con GPS malo sin que el sistema se lo pidiera nunca marcar. Aquí no hay ninguna
regla que dependa del valor: la columna simplemente nunca se llena y nada la consulta. El final de
trayecto es una columna huérfana, no una cadena rota.

### 2.3 `FOT_Fotografias` en cero filas

```
$ python -c "
import openpyxl
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
ws = wb['FOT_Fotografias']
rows = list(ws.iter_rows(values_only=True))
print('encabezado', rows[0])
print('filas de datos', len(rows) - 1)
"
encabezado ('FotoID', 'MantenimientoID', 'Tipo', 'Archivo', 'Ubicacion_LatLong', 'PrecisionGPS', 'FechaHora', 'Usuario')
filas de datos 0
```

No hay ninguna fotografía real que dependa de cómo quede esta columna. No hace falta migrar nada.

### 2.4 El encargo citaba cinco documentos; solo tres instruyen cablear la función — verificado, no copiado

El encargo de esta especificación enumeraba `docs/ARQUITECTURA_OBJETIVO_SGMC.md:577`,
`docs/MANUAL_DESPLIEGUE.md:1214`, `docs/PROMPT_CABLEADO.md:490`, `docs/TIPOS_ESPERADOS.md:96,247` y
`docs/bd.md:433`. Se verificó cada uno, no se dio por bueno:

```
$ grep -rn "USERLOCATIONACCURACY" docs/ scripts/ Manuales/
docs/ARQUITECTURA_OBJETIVO_SGMC.md:577:| `PrecisionGPS` | Number |  |  |  | Valor inicial: `USERLOCATIONACCURACY()` |
docs/MANUAL_DESPLIEGUE.md:1214:| `PrecisionGPS` | `Number` | `Initial value` = `USERLOCATIONACCURACY()` |
docs/PROMPT_CABLEADO.md:490:| `FOT_Fotografias` | `PrecisionGPS` | `Initial value` | `USERLOCATIONACCURACY()` |
(y las líneas de MAN_Mantenimientos.Precision_GPS que ya cubrió ESPEC-004, sin relación con FOT)
```

`docs/TIPOS_ESPERADOS.md:96,247` y `docs/bd.md:433` **no citan la fórmula**: dicen que
`PrecisionGPS` es `Number`, que es correcto y no hay que tocarlo — son el defecto de tipo que ya
corrigió la Tanda 2 de hoy (`LatLong` → `Number`, §2.5), un hallazgo distinto sin relación con la
función inexistente. Contarlos entre los documentos que "cablean lo imposible" habría sido inflar el
alcance sin verificarlo: son tres documentos, no cinco.

### 2.5 El tipo `Number` de `PrecisionGPS` ya está corregido, y este documento no depende de él

`docs/TIPOS_ESPERADOS.md:96` deja escrito que `PrecisionGPS` salió `LatLong` en la inferencia
automática por llevar `GPS` en el nombre, cuando el dato son metros — corregido a `Number` en la
Tanda 2 de hoy. No afecta esta decisión: §3 y §4 retiran la columna, así que su tipo deja de importar
en cuanto `ORDEN-004`-equivalente se aplique. Se deja anotado para que nadie lo persiga por su
cuenta, igual que hizo `ESPEC-004` §2.8 con el mismo hallazgo sobre `Precision_GPS` de `MAN`.

### 2.6 Los tres documentos de §2.4 se regeneran solos — no hace falta editar ningún generador

```
$ grep -n "valor_inicial" scripts/generar_doc_arquitectura.py
178:            if c.get("valor_inicial"):
179:                nota = (nota + ". " if nota else "") + f"Valor inicial: `{c['valor_inicial']}`"

$ grep -n "valor_inicial" scripts/generar_manual_despliegue.py
1127:        if c.get("valor_inicial"):
1128:            acc.append("`Initial value` = `%s`" % c["valor_inicial"])

$ grep -n "valor_inicial" scripts/generar_prompt_cableado.py
329:              for k in ("valor_inicial", "formula", "valid_if")
333:    _NOMBRE = {"valor_inicial": "Initial value", "formula": "App formula",
```

Los tres bucles recorren `MODELO[t]["columnas"]` y emiten `valor_inicial` para **cualquier** columna
que lo tenga — no hay ninguna línea que cite `PrecisionGPS` ni `USERLOCATIONACCURACY()` como texto
fijo. En cuanto `scripts/modelo_objetivo.py:427` deje de declarar `valor_inicial`, los tres dejan de
emitir esa fila la próxima vez que se regeneren, sin tocarlos. Es el mismo patrón que `ESPEC-004`
§2.9 documentó para `generar_tipos_esperados.py` e `inferencia.py`: deriva del modelo en tiempo de
ejecución, no hay copia que editar.

```
$ grep -n "PrecisionGPS" scripts/*.py
scripts/modelo_objetivo.py:427:            col("PrecisionGPS", "Number", valor_inicial="USERLOCATIONACCURACY()"),
```

Es la única aparición del nombre de la columna en todo `scripts/`. `docs/ENCARGO_VENTANA.md`,
`docs/bd.md` y `docs/TIPOS_ESPERADOS.md` la citan (§2.4) pero sin la fórmula, así que tampoco
necesitan edición: seguirán diciendo `Number` — que sigue siendo correcto, salvo que dejarán de
listarla en cuanto se regeneren, porque la columna ya no existirá.

**Conclusión: un solo archivo cambia, `scripts/modelo_objetivo.py`, en dos puntos (§4).** Ningún
generador ni verificador necesita edición.

### 2.7 `FOT_Fotografias` ya tiene una referencia cableada en el editor — Rama A o B, sin confirmar

```
$ grep -n "FOT_Fotografias" docs/CORRECCIONES_CABLEADO.md
| `FOT_Fotografias.MantenimientoID` | `MAN_Mantenimientos` | el 2026-08-10 por Diego, en el editor |
```

La tabla no está intacta en el editor: su referencia a `MAN_Mantenimientos` ya se puso a mano el
2026-08-10 (`ACTA-004`). Eso no dice nada sobre si `PrecisionGPS` llegó a tener un `Initial value`
puesto — el reporte de §2.1 sugiere que no, porque el editor lo habría rechazado —, pero no hay
lectura de `Data > Columns` que lo confirme, igual que `ESPEC-004` §2.10 dejó sin confirmar cuál de
sus dos ramas aplicaba a `MAN_Mantenimientos.Precision_GPS`. Se declara como supuesto en §7 y se
resuelve con la misma comprobación de cinco minutos, en la misma sesión de editor.

### 2.8 Un hallazgo fuera de alcance, anotado y no perseguido

`FOT_Fotografias.Ubicacion_LatLong` no está cubierta por ninguna regla `Editable_If`: `RG-20` es la
única regla de ese tipo en el modelo y solo cubre tres columnas de `MAN_Mantenimientos`
(`Coordenadas_Cierre_LatLong`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo`). Ni la columna en el
`col()` (línea 424) lleva el parámetro `editable=False` que sí llevan esas tres. Esto no lo motivó
esta especificación ni lo resuelve: se deja anotado en §5 para que quede escrito, no para tocarlo
aquí — es exactamente el criterio que `ORDEN-004` §4 aplicó a `docs/CONTEXTO_OPERACION.md`: tocar
algo que el encargo no menciona sería extender el alcance sin autorización.

## 3. Qué cambia exactamente

| Tabla.Columna | Estado actual | Estado objetivo |
|---|---|---|
| `FOT_Fotografias.PrecisionGPS` | `Number`, `Initial value = USERLOCATIONACCURACY()` | **Retirada del modelo** |

Ninguna otra columna, referencia ni regla cambia. `FOT_Fotografias` pasa de 8 a 7 columnas.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`, dos puntos:

- **`MODELO["FOT_Fotografias"]["columnas"]`** (línea 427): eliminar la línea
  `col("PrecisionGPS", "Number", valor_inicial="USERLOCATIONACCURACY()")`.
- **`CAMPOS_RETIRADOS`**: añadir la primera entrada de esta tabla —hoy no existe
  `CAMPOS_RETIRADOS["FOT_Fotografias"]`—:

  ```python
  "FOT_Fotografias": {
      "PrecisionGPS": ("USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1, mismo "
                       "hallazgo que Precision_GPS de MAN_Mantenimientos). Ninguna regla la leia "
                       "(ESPEC-007 2.2): a diferencia de MAN, no habia cadena que romper. Retirada "
                       "por ESPEC-007. Si FOT_Fotografias ya tenia esta columna con Initial value "
                       "puesto en el editor, hace falta Delete and re-add de la tabla completa "
                       "(mismo procedimiento de ESPEC-004 2.10); si quedo huerfana sin usar, no hace "
                       "falta nada (ESPEC-007 2.7, sin confirmar cual rama aplica)."),
  },
  ```

No se toca `REGLAS` (§2.2: ninguna la declaraba), ni `PARAMETROS`, ni `DECISIONES` (no hay una
decisión de dominio registrada sobre esta columna). No se toca ningún script generador ni verificador
(§2.6).

**Documentos que se re-emiten** con los comandos de siempre, una vez editado `modelo_objetivo.py`:
`docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`, `docs/PROMPT_CABLEADO.md`,
`docs/bd.md`, `docs/TIPOS_ESPERADOS.md`, `docs/ENCARGO_VENTANA.md`, `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`. Ninguno necesita
edición manual previa: se regeneran limpios en cuanto la columna deja de estar en `MODELO`.

## 5. Qué NO cubre esta especificación

- **No decide si algún reporte futuro (`D-12`) debería cruzar la calidad de posición de una
  fotografía contra el cierre de su mantenimiento.** Si `D-12` alguna vez lo pide, es un documento
  aparte: hoy no hay ningún requisito que lo pida (§7).
  - **No resuelve el hallazgo de §2.8** (`Ubicacion_LatLong` de `FOT_Fotografias` sin
  `Editable_If`). Queda anotado, no corregido.
- **No confirma en el editor cuál de las dos ramas de §2.7 aplica.** Necesita sesión de navegador.
- **No repite ni reabre nada de `ESPEC-004`.** `MAN_Mantenimientos.Precision_GPS` y su cadena de
  reglas son un documento distinto, ya aplicado por `ORDEN-004`.
- **No inventa una función de AppSheet que no existe.** Si la plataforma añade alguna forma de
  escribir en una columna la precisión que muestra en pantalla, reabrir esta decisión es legítimo y
  barato — la tabla sigue en cero filas hoy (§2.3).

## 6. Riesgos y dependencias

- **Ninguna dependencia de otra especificación.** No hace falta que `ESPEC-004`, `ESPEC-005` ni
  `ESPEC-006` estén en ningún estado particular: esta columna no comparte regla ni tabla con
  ninguna de ellas.
- **Rama A o B sin confirmar (§2.7).** Si `PrecisionGPS` llegó a tener un `Initial value` puesto en
  el editor (Rama B), retirarla del modelo no la borra de la hoja y hace falta `Delete and re-add`
  de `FOT_Fotografias` completa — se lleva por delante la referencia a `MAN_Mantenimientos` que ya
  se cableó el 2026-08-10 (§2.7), así que copiar ese estado a mano antes de borrar es obligatorio si
  aplica esta rama. Se confirma con `Data > Columns > FOT_Fotografias > PrecisionGPS`, cinco minutos,
  en la misma sesión que la comprobación pendiente de `ORDEN-004` §4 sobre `CierreConExcepcion` —
  no hace falta abrir el editor dos veces por esto.
- **Sin datos que migrar** (§2.3). Revertir esta especificación, en cualquier momento antes de la
  primera fila real de `FOT_Fotografias`, cuesta reponer una línea en `MODELO` y borrar una entrada
  de `CAMPOS_RETIRADOS`.

## 7. Supuestos adoptados

- **Se adopta que ninguna regla necesita leer la precisión de una fotografía individual.** La
  calidad de posición que gobierna el cierre de un mantenimiento ya la exige `RG-01`
  (`DISTANCE(...) <= RadioGeofencingKm`) sobre `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`, y la
  excepción por GPS deficiente en el cierre ya tiene mecanismo declarado (`CierreConExcepcion` +
  `MotivoExcepcion`, `ESPEC-004`). Una fotografía es evidencia de lo que se ve, no una segunda
  medición de posición: si la del cierre pasó el geofencing, la foto que acompaña a ese mismo
  mantenimiento no necesita una calificación de precisión propia. **Qué lo rompe:** que operación
  decida que necesita distinguir, fotografía por fotografía, cuáles se tomaron con señal deficiente
  —por ejemplo para una auditoría legal de evidencia—. **Qué tan barato es reabrirlo si se rompe:**
  la tabla sigue en cero filas (§2.3), así que reabrir es declarar de nuevo la columna, sin ningún
  dato que reconciliar.
- **Se adopta NO dejar la columna sin `Initial value`, como alternativa evaluada y rechazada.** Un
  campo `Number` visible en el formulario de captura de fotos, sin nada que lo llene, es la misma
  trampa que ya costó cara con `ACT_Activos.CodigoQR` (33 de 368 valores autocompletados por la
  plantilla, 335 en blanco, ninguno un código real — `README.md` prólogo): invita a que un técnico
  transcriba a mano un número que cree recordar de la pantalla, y ese número nadie lo puede
  contrastar después. Se rechaza por el mismo criterio que `ESPEC-004` §2.13 rechazó pedir el número
  transcrito para `MAN_Mantenimientos`.
- **Se adopta NO poblarla con un mecanismo que sí exista, porque no existe ninguno.** Las cuatro
  formas de captura de GPS que documenta AppSheet (`ESPEC-004` §2.1) no guardan en una columna la
  precisión que muestran en pantalla durante la captura manual. La única forma de obtener un número
  real sería pedir la transcripción manual, que el punto anterior ya rechaza.
- **Se adopta retirar la columna en vez de las otras dos alternativas**, por ser la única que no
  exige algo que AppSheet no ofrece ni fabrica un campo que nadie va a poder llenar de verdad.
- **Se adopta que el hallazgo de §2.8 (`Ubicacion_LatLong` sin `Editable_If`) queda fuera de esta
  especificación.** No lo motivó el encargo de este documento, y tocarlo sería extender el alcance
  sin autorización.
- **No se estima aquí cuál rama de §2.7 es la más probable.** Se decide mirando el editor, con el
  mismo criterio que `ESPEC-004` §7 fijó para su propia ambigüedad de rama: la lectura del editor
  manda, no una probabilidad escrita de antemano.
