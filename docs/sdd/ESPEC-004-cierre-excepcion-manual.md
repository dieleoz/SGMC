# ESPEC-004 — Cierre con excepción por GPS: de fórmula inexistente a marca del técnico

**Rehecha el 2026-08-10 tras bloqueo del arquitecto.** El dictamen trajo doce condiciones; una ya
estaba aplicada en el modelo (el arreglo de `RG-19`, ver §2.2) y las otras once se atienden aquí,
cada una con el comando que la verifica. Nada de lo que sigue está aplicado en `modelo_objetivo.py`
ni en el editor.

**Supuesto que gobierna todo este documento: `ESPEC-005` va primero.** `ESTADO.md` ya lo fija así
—`OTID` deja de poder teclearse en cuanto `ESPEC-005` lo convierte en `UNIQUEID()`, y si este
documento se aplicara antes, `PRUEBA-004` montaría su fixture sobre una clave que va a dejar de
existir—. Todo lo que sigue asume `ORDEN-005` ya aplicada: modelo, hoja regenerada y las dos claves
(`OTID`, `PlanID`) cableadas en el editor como `CLAVE_GENERADA`.

## 1. Qué se quiere y por qué

`RG-02` inicializa `MAN_Mantenimientos.Precision_GPS` con `USERLOCATIONACCURACY()`. Esa función
**no existe en AppSheet**: lo reportó el editor al intentar escribirla (`Can't find function
"USERLOCATIONACCURACY"`) y lo confirmo hoy de forma independiente contra la página oficial de
captura de GPS — ver §2.1. `RG-19` compara `Precision_GPS` contra `PAR_Parametros.UMBRAL_GPS` para
calcular `CierreConExcepcion`; como `Precision_GPS` nunca se puebla, esa comparación es siempre
`número > blanco`, que en AppSheet evalúa `FALSE`. `RG-03` exige `MotivoExcepcion` solo si
`CierreConExcepcion = TRUE`, y como esa condición nunca se cumple, **`MotivoExcepcion` no se le pide
nunca a nadie**, sin importar cuán mala sea la posición registrada.

La decisión que este documento permite tomar es concreta: **¿puede un técnico, alguna vez, dejar
constancia auditable de que cerró con el GPS deficiente?** Hoy la respuesta de diseño es no.

**Y hay que decir, desde aquí y sin diluirlo, cuál es el riesgo que este documento en realidad
gestiona.** No es que un técnico marque la excepción quien no debería: no puede falsear dónde
estuvo —`RG-01` lo sigue comprobando por distancia, y `HERE()` sobre `Coordenadas_Cierre_LatLong`
sigue sin ser editable, ver §3—. **El riesgo real es el que cierra con GPS malo y NO marca la
casilla.** Ese cierre queda indistinguible de uno con buena señal, hoy y después de este documento,
porque nada obliga a marcar: la casilla es una autodeclaración, no una medición. Y es un riesgo que
existe con o sin `ESPEC-004`: sin este documento, la casilla ni siquiera se puede usar; con él, se
puede usar, pero usarla sigue siendo voluntario. La sección 2.12 nombra esta exposición con detalle
y la sección 6 dice quién la vigila y con qué cadencia, porque una casilla que depende solo de que
alguien la marque, sin lector y sin contraste, es decoración si nadie la revisa.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

Según `python scripts/sistema.py`, hoy el sistema vigente es:

```
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026  (Google Sheets, fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Este documento verifica contra el volcado local con `openpyxl` y contra `scripts/modelo_objetivo.py`
como fuente del diseño. No se leyó producción de nuevo para esta reescritura: los conteos de filas
de §2.3 se retomaron de la comprobación más reciente (`PRUEBA-004` §1.1, `PRUEBA-005` §1.1, ambas
del mismo día), y coinciden con el volcado local corrido hoy.

### 2.1 `USERLOCATIONACCURACY()` no existe, y la página oficial dice algo más que eso

Verificado hoy contra la página oficial de captura de GPS de AppSheet:

```
$ curl -s "https://support.google.com/appsheet/answer/10106789" -A "Mozilla/5.0" | ...
```

> «There are four ways to capture the GPS location in a form: [1] LatLong column con App Formula
> `HERE()` ... [2] LatLong column con Initial Value `HERE()` ... [3] You can manually capture the
> current location. The input field for a LatLong column has a clickable icon that lets you
> capture the device's current GPS location. [...] with each button press the app will try to
> obtain the most accurate current location it can for up to 30 seconds or until an estimated
> accuracy of 10m is reached. This method offers the highest accuracy and displays an estimate of
> the accuracy (in meters) within the app. [4] Additionally, you can explicitly type in a LatLong
> value.»
>
> «"Wifi location data typically includes information such as MAC address, relative signal
> strength... GPS location includes ... Since the actual location capture mechanisms are device
> dependent, maximum available accuracy may vary ... As such, a consistently high accuracy cannot
> be guaranteed. **The manual capture mode of the LatLong input provides the highest available
> accuracy and is recommended over use of the `HERE()` function in cases where high accuracy is
> especially important.**»

— [Capture GPS location](https://support.google.com/appsheet/answer/10106789), AppSheet Help,
consultado el 2026-08-10 y de nuevo hoy para esta reescritura, misma URL.

Confirma tres cosas:

1. No hay ninguna función equivalente a `USERLOCATIONACCURACY()` bajo otro nombre para guardar la
   precisión en una columna.
2. La app **sí muestra** al técnico una estimación de precisión en metros, pero **solo en pantalla,
   durante la captura manual**, y nada en la documentación dice que ese número se pueda asignar a
   una columna. Es la base del rechazo de la "mejora" de §3.
3. **AppSheet mismo recomienda la captura manual por encima de `HERE()` cuando la precisión
   importa** — y este sistema, en `Coordenadas_Cierre_LatLong`, hace justo lo contrario: usa
   `HERE()` como `Initial value` y lo deja `Editable_If = FALSE` (`RG-20`) precisamente para que el
   técnico no pueda tocar el pin. **Este documento mantiene esa decisión** — el residuo se explica
   en §3, "Sobre la mejora propuesta": la captura manual gana precisión a cambio de volver
   arrastrable el pin que sostiene todo el geofencing (`RG-01`), y `RG-20` existe exactamente para
   impedir eso. La cita de AppSheet no cambia esa cuenta; solo confirma que el sistema paga un costo
   de precisión, a sabiendas, a cambio de no reabrir ese agujero.

No recorrí la lista completa de funciones de expresión de AppSheet — así que esta verificación se
apoya en la página canónica de captura de GPS más el error literal del editor. Lo declaro como dos
fuentes independientes y consistentes, no como una enumeración exhaustiva.

### 2.2 La cadena está configurada y no puede dispararse — y el diagnóstico del `RG-19` doble se corrige aquí

`scripts/modelo_objetivo.py`, columnas de `MAN_Mantenimientos` (verificado hoy, línea 337-342):

```python
col("Precision_GPS", "Number", valor_inicial="USERLOCATIONACCURACY()", editable=False),
col("CierreConExcepcion", "Yes/No",
    formula=('OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), '
          '[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))'),
    nota="Se calcula, no se edita (RG-19). El umbral vive en PAR_Parametros"),
col("MotivoExcepcion", "LongText", nota="Obligatorio si CierreConExcepcion es verdadero"),
```

Y `REGLAS` (`RG-02`, `Initial value`; `RG-03`, `Required_If`; `RG-19`, `App formula`, línea
1171-1186), con la **misma** expresión con `OR(ISBLANK(...), ...)` que la columna.

**Esto ya no está roto por duplicación.** Hasta hace poco, `RG-19` estaba declarada dos veces con
expresiones distintas: la columna traía `[Precision_GPS] > LOOKUP(...)` sin guarda, y `REGLAS` traía
el `OR(ISBLANK(...), ...)` con guarda. `RECONSTRUCCION_EXPRESIONES.md` toma la expresión de
`REGLAS`, así que el ejecutor habría cableado la versión **con** guarda aunque la columna dijera
otra cosa — una divergencia que nadie habría notado hasta comparar los dos sitios a mano. Existe
`scripts/validar_modelo.py`, comprobación `V-18` (líneas 235-275), escrita explícitamente para que
esto no pueda volver a pasar: compara la expresión de cada regla contra la de la columna que declara
el mismo mecanismo, y falla si divergen. Verificado hoy:

```
$ python scripts/validar_modelo.py
ERRORES: ninguno
```

Sin ningún `V-18` en la lista — las dos declaraciones de `RG-19` coinciden hoy.

**Y hay que decir con precisión qué corrige la guarda `ISBLANK`, porque el diagnóstico anterior no
era exacto sin ella.** Con la guarda, `RG-19` no es "siempre falsa": es falsa **mientras exista la
fila `UMBRAL_GPS` en `PAR_Parametros`**. Si esa fila se borrara —hay al menos dos cuentas con
permiso de edición sobre el Sheets, según el propio comentario de `scripts/validar_modelo.py:250-251`—,
`LOOKUP(...)` devolvería blanco, `ISBLANK` sería `TRUE`, el `OR` completo sería `TRUE`, y
`CierreConExcepcion` saldría `TRUE` en **todos** los cierres, sin que nadie lo pidiera. Es el mismo
patrón de falla que el propio `RG-19` describe para `RG-16` en su propia nota: "falla hacia el lado
seguro" cuando el umbral no se puede leer no es gratis — es seguro en el sentido de "no deja pasar
un cierre sospechoso sin marcar", pero **inunda** el sistema de excepciones si la fila desaparece,
lo que en la práctica tampoco es inocuo: un supervisor que vea el 100% de los cierres marcados como
excepción dejaría de poder usar la marca para nada. La corrección del `RG-19` doble sigue en pie tal
como está: el arreglo es correcto. Lo que se precisa aquí es que "arreglado" no significa "sin
condición": significa "correcto mientras la fila `UMBRAL_GPS` exista", y esa fila **no está
protegida contra borrado** por ninguna regla de este modelo. Esto no es una razón para bloquear este
documento — la App formula ya falla del lado más ruidoso posible, y de hecho es en última instancia
irrelevante en cuanto §3 retire `RG-19` por completo—, pero era un hallazgo que había que declarar
con precisión y no se había hecho.

### 2.3 `MAN_Mantenimientos` y `OT_OrdenesTrabajo` están vacías en los dos modelos

Volcado local, hoy:

```
MAN_Mantenimientos 0
OT_OrdenesTrabajo 0
```

Coincide con la última lectura de producción registrada (`PRUEBA-004` y `PRUEBA-005`, ambas del
2026-08-10, instantánea `28 tablas · 953 filas en total` con las dos en cero). No hay ninguna fila
histórica que migrar ni que se vea afectada por retirar una columna: la cadena rota nunca ha
producido un solo cierre con excepción real.

### 2.4 `PAR_Parametros.UMBRAL_GPS` coincide en los dos modelos

Volcado local:

```
('UMBRAL_GPS', 'Umbral de GPS deficiente', 40, 'm', 'Error del satelite...', 'TRUE')
```

Producción (lectura previa, `PRUEBA-004` §2.4 de la versión anterior): `{'ParametroID': 'UMBRAL_GPS',
'Nombre': 'Umbral de GPS deficiente', 'Valor': '40', 'Unidad': 'm', 'Activo': 'Y'}`.

### 2.5 `RG-13` y `RG-18` no tienen dónde vivir en el editor — y son dos, no una, y las demás usan once propiedades, no ocho

Verificado hoy contra `scripts/modelo_objetivo.py`:

```
$ python -c "
import sys; sys.path.insert(0,'scripts')
import modelo_objetivo as M
tipos = {}
for r in M.REGLAS:
    tipos.setdefault(r['tipo'], []).append(r['id'])
for t, ids in sorted(tipos.items()):
    print(t, ids)
print('TOTAL tipos distintos:', len(tipos))
"
App formula ['RG-11', 'RG-19', 'RG-16']
Are updates allowed ['RG-14', 'RG-15']
Bot ['RG-06', 'RG-07', 'RG-10']
Bot programado ['RG-08', 'RG-12']
Doctrina de reportes ['RG-18']
Editable_If ['RG-20']
Initial value ['RG-02', 'RG-09']
Required_If ['RG-03', 'RG-17']
Security Filter ['RG-04', 'RG-05']
Valid_If ['RG-01', 'RG-34']
Verificacion de evidencia ['RG-13']
TOTAL tipos distintos: 11
```

**Son once propiedades distintas de `tipo`, no ocho**, y **dos de las 21 reglas no tienen mecanismo
real de AppSheet detrás**, no una:

- **`RG-13`**, `tipo="Verificacion de evidencia"` (línea 1154). Compara
  `UbicacionEscaneo_LatLong` contra `Coordenadas_Cierre_LatLong`. `docs/PROMPT_CABLEADO.md` no la
  cita en ningún paso (`grep -n "RG-13" docs/PROMPT_CABLEADO.md` sin resultados), y su entrada,
  `UbicacionEscaneo_LatLong`, solo se llena cuando `OrigenApertura = QR`
  (`scripts/modelo_objetivo.py:327-329`), fuera de alcance desde el 2026-08-07
  (`SDD_PIPELINE_SGMC.md` §8). No se resuelve aquí — ver §5.
- **`RG-18`**, `tipo="Doctrina de reportes"` (línea 1203). Su propia `expresion` lo dice: *"Ver
  descripcion: es una prohibicion, no una expresion a configurar"*. Es una regla de **cómo se
  construyen los reportes** ("no filtrar los históricos por la bandera `Activo` del padre"), no una
  configuración de columna ni un bot: no hay reportes construidos (`D-12` abierta), así que hoy no
  hay nada que configurar ni que viole la prohibición. No se resuelve aquí — es un frente de
  `D-12`, no de `ESPEC-004`.

Ninguna de las dos compensa la pérdida de detección de precisión de `ESPEC-004`, y las dos quedan
exactamente igual de inertes después de este documento que antes: no era su objeto y sigue sin
serlo.

### 2.6 El hallazgo colateral: `Ubicacion_LatLong`, y a quién acusa de verdad

La versión anterior de este documento afirmó que `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (líneas 92,
149) decía que `ACT_Activos.Ubicacion_LatLong` está vacía en las 368 filas. **Es falso, y se
verifica leyendo la línea exacta:**

```
$ sed -n '149p' docs/ALCANCE_Y_SUPUESTOS_SGMC.md
| D-01 | Las coordenadas reales. `ACT_Activos.Ubicacion_LatLong` está poblada en las 368 con
valores distintos, **derivados del `PK` sobre el trazado del corredor: ninguna se midió en
campo**. `RG-01` compara contra un punto inventado, así que el geofencing puede estar
perfectamente cableado y **no significar nada**. (...)
```

Dice literalmente **lo contrario** de lo que la versión anterior le atribuía: la columna está
**poblada**, con 368 valores distintos, sintéticos y derivados del `PK`. El problema real de `D-01`
no es que esté vacía — es que ninguno de esos 368 valores se midió en campo.

La versión anterior también citaba `PRUEBA-004` §1.4 (líneas 108, 133) como refuerzo de la
acusación. Verificado hoy:

```
$ sed -n '108p;133p' docs/ALCANCE_Y_SUPUESTOS_SGMC.md
| D-04 | GPS deficiente | Cierre con excepción: motivo escrito, fotografía, marca y aviso al
supervisor. Umbral 50 m | **CERRADA en el mecanismo, con 40 m y no 50** |
| D-04 | `MAN_Mantenimientos.CierreConExcepcion` y `MotivoExcepcion`, con `RG-03` y `RG-19`. (...)
```

Las dos son sobre `D-04`, el mecanismo de cierre con excepción — **ninguna de las dos habla de
`Ubicacion_LatLong`**. Citar esas líneas como evidencia de que el documento dice que la coordenada
está vacía repite el error una vez, no lo corrige: es exactamente el patrón que este proyecto existe
para cortar, aplicado dentro del propio documento que existe para cortarlo.

**El documento que sí está desactualizado, y solo él, es `Manuales/MANUAL_DE_USUARIO.md`, en tres
puntos:**

```
$ sed -n '46p;168p;266p' Manuales/MANUAL_DE_USUARIO.md
| Coordenadas de los activos | **No hay ninguna.** `ACT_Activos.Ubicacion_LatLong` está **vacía
en las 368 filas** de la hoja vigente. Las que hubo eran calculadas sobre el trazado, no medidas,
y se perdieron al renombrar la columna el 2026-08-10 |
> Y aunque estuviera cableado, **el activo no tiene coordenada**: `Ubicacion_LatLong` está vacía en
> **Estado, contra `BD/Modelo_Datos_PLANTILLA.xlsx`:** de los 368 activos, el **PK** está poblado en
los 368; **PR**, **tramo de INVÍAS**, **sede** y **coordenada** están **vacíos en los 368**.
```

Las tres afirman que `Ubicacion_LatLong` está vacía. **No lo está**: está poblada en las 368,
verificado hoy contra el volcado y ya confirmado también en `docs/README.md` (§6, "la columna ya no
está vacía"). El manual quedó desactualizado en un punto que el propio repositorio ya corrigió en
otro lado. No es objeto central de `ESPEC-004` corregir esto, pero como `MANUAL_DE_USUARIO.md` ya se
edita por otra razón en este mismo cambio (§4), se cierra de paso: es más barato corregirlo aquí que
dejarlo abierto para otro documento que quizá nunca llegue a tocar esas líneas.

### 2.7 Lo que rompe si se retira `Precision_GPS` sin tocar nada más — y son seis generadores, no tres

**Tres archivos** dependen de `Precision_GPS`/`RG-19` de forma que un cambio a medias los deja
mintiendo, y **se regeneran o se editan sin más consecuencia** que la de estar bien hechos:

| Archivo | Qué depende | Acción |
|---|---|---|
| `scripts/validar_modelo.py:249` | `COBERTURA["Precision del GPS"] = ("MAN_Mantenimientos", "Precision_GPS")`. Si la columna se retira y esta entrada no, `V-13` falla | Editar a mano: quitar la entrada |
| `scripts/verificar_faseA.py:307-386` (bloque `F-12`/`F-13`) | Cruza `Precision_GPS` contra `CierreConExcepcion` asumiendo que `RG-19` sigue viva | Editar a mano: retirar el bloque |
| `scripts/generar_diccionario_bd.py:159` | `lectores = {"UMBRAL_GPS": "RG-19", ...}`. Con `RG-19` retirada, `docs/bd.md` seguiría atribuyéndole un lector inexistente | Editar a mano: quitar la clave |

**Y hay otros cinco archivos que nombran literalmente `Precision_GPS` en su código y que la versión
anterior de este documento no mencionó — son generadores, y tres de ellos necesitan edición de
código, no solo re-ejecución:**

```
$ grep -rln "Precision_GPS" scripts/*.py
scripts/generar_guia_funcional.py
scripts/generar_manual_despliegue.py
scripts/generar_prompt_expresiones.py
scripts/generar_tipos_esperados.py
scripts/inferencia.py
scripts/modelo_objetivo.py
scripts/validar_modelo.py
scripts/verificar_datos.py
scripts/verificar_faseA.py
```

**Tres necesitan edición de código porque describen `RG-02`/`RG-19` con texto fijo (`w("...")`), no
derivado de `MODELO`/`REGLAS`. Regenerarlos sin editarlos primero produce documentos que instruyen
al ejecutor a cablear algo que ya no existe:**

- **`scripts/generar_prompt_expresiones.py:293-310`** — la sección completa "Dos que hoy NO se
  pueden poner" queda obsoleta entera: enumera `RG-02` y `RG-19` como imposibles y **le dice
  textualmente al ejecutor**:
  ```
  guardar en una columna. Deja `Precision_GPS` con tipo `Number` y **sin `Initial value`**.
  ```
  Es el peor caso citado en el dictamen: **el encargo generado le diría al ejecutor que configure
  una columna que este documento retira.** Hay que borrar toda la sección (líneas 293-311) y
  sustituirla por una nota breve: `RG-02` y `RG-19` se retiraron con `ESPEC-004`; `RG-03` ya se
  puede poner sobre `CierreConExcepcion` como una columna ordinaria.
- **`scripts/generar_guia_funcional.py:383,395`** — "Lo mismo en `Precision_GPS`,
  `UbicacionEscaneo_LatLong` y `FechaHoraEscaneo`" (línea 383, tiene que quedar en dos columnas, no
  tres) y cita completa de la `App formula` de `RG-19` con `[Precision_GPS]` (línea 395, hay que
  quitar la sección "7.2 El umbral de GPS, entero" o reescribirla para describir la marca manual).
- **`scripts/generar_manual_despliegue.py:841,858`** — la lista de las "cuatro columnas de captura"
  no editables (línea 841: `Coordenadas_Cierre_LatLong · Precision_GPS · UbicacionEscaneo_LatLong ·
  FechaHoraEscaneo`) tiene que quedar en tres, y la misma cita completa de `RG-19` (línea 858) hay
  que quitarla o reescribirla igual que en `generar_guia_funcional.py`.

**Dos NO necesitan edición**, verificado leyendo el contexto de cada mención:

- **`scripts/generar_tipos_esperados.py:14,113`** cita `Precision_GPS` como ejemplo **histórico** de
  por qué el nombre de una columna puede mandar sobre el dato ("Precision_GPS salió LatLong el
  2026-08-10 estando su tabla VACÍA"). Es un hecho que ya ocurrió y sigue siendo cierto después de
  este documento; no instruye a nadie a configurar nada hoy. La tabla de columnas sospechosas del
  propio documento se deriva dinámicamente de `MODELO` (`for t in MODELO: for c in
  MODELO[t]["columnas"]`), así que en cuanto `Precision_GPS` salga del modelo, deja de aparecer ahí
  sin tocar el script.
- **`scripts/inferencia.py:79`** cita el mismo hecho histórico como evidencia del gatillo `gps` →
  `LatLong` en `GATILLOS_NOMBRE`. Mismo argumento: describe una observación pasada que sigue siendo
  cierta y sostiene una regla general útil para futuras columnas con `gps` en el nombre.

**En total: seis scripts de la familia generadora tocados por este cambio** —
`generar_diccionario_bd.py` (ya citado antes), `generar_guia_funcional.py`,
`generar_manual_despliegue.py`, `generar_prompt_expresiones.py` (edición de código, los cuatro), más
`generar_tipos_esperados.py` e `inferencia.py` (sin edición, se regeneran solos y siguen diciendo la
verdad). `validar_modelo.py`, `verificar_faseA.py` y `verificar_datos.py` no son generadores; son
verificadores, y están tratados aparte en la tabla de arriba y en §2.9.

### 2.8 Retirar `Precision_GPS` no cabe en la plataforma tal como está especificado hoy — la columna ya existe en el editor

`docs/BASE_CONOCIMIENTO_APPSHEET.md` §11, verificado hoy:

> «Cuando regeneras una tabla que reside en una hoja de Google Sheets o de Excel, AppSheet lee y
> analiza el contenido de esa hoja para determinar el nombre y el tipo de cada columna. **Sin
> embargo, AppSheet combina la información nueva con la que ya exista para la columna e intenta
> mantener el nombre y el tipo de las columnas existentes.**»
>
> «**Y las columnas reales no se pueden borrar una a una.** Solo las virtuales tienen papelera: las
> demás vienen de la hoja y AppSheet no ofrece esa opción.»
>
> «Tables must specify a column structure. (...) **Delete and re-add the table to create the column
> structure.**»

Esto no es un riesgo futuro: **es el estado de hoy.** `ESTADO.md` confirma que **las 28 tablas ya
están dadas de alta en la aplicación** ("Las 28 tablas dadas de alta sobre la hoja definitiva (...)
Comprobado por API el 2026-08-10: las 28 responden"), lo que incluye `MAN_Mantenimientos`. Una tabla
dada de alta expone en `Data > Columns` **todas** las columnas de su pestaña, cableadas o no —
`Precision_GPS` ya está ahí hoy, como columna real sin `Initial value` configurado, esperando la
Fase C que `ESTADO.md` marca "en curso". Quitar la columna de `modelo_objetivo.py` y regenerar la
hoja hace que su cabecera desaparezca del Excel, pero **no la retira del esquema de AppSheet**: por
la cita de arriba, sobrevive como columna huérfana apuntando a un encabezado que ya no existe.

**El procedimiento real, en dos ramas según cuánto se haya cableado ya `MAN_Mantenimientos` cuando
se aplique esta especificación:**

**Rama A — si `MAN_Mantenimientos` todavía no llegó a su Paso 6 de `docs/PROMPT_CABLEADO.md`
("Reportar al terminar") por estar bloqueada precisamente en `RG-02`/`RG-19`/`RG-03`** (que es lo
que hoy dice `ESTADO.md`: *"`RG-02` · `RG-19` · `RG-03` — No se pueden poner — Espera a
`ESPEC-004`"*): en ese caso, no hace falta borrar nada. `Precision_GPS` existe como columna huérfana
sin configurar, y basta con **nunca configurarla** — el ejecutor edita `modelo_objetivo.py` (§4),
regenera la hoja, y en el editor deja la columna `Precision_GPS` tal como está: sin `Initial value`,
sin uso. AppSheet la sigue mostrando en `Data > Columns` como columna huérfana (por el mismo
comportamiento de "fusiona, no reemplaza"), pero eso no bloquea nada: es ruido visual, no una
regla activa. Se anota en §4 como una deuda menor, no un bloqueante.

**Rama B — si para cuando se aplique esta especificación `MAN_Mantenimientos` ya avanzó más allá de
lo que `ESTADO.md` describe hoy** (por ejemplo, si alguien ya puso el resto de tipos, referencias,
`Editable_If` y Label de esa tabla mientras esperaba a que se resolviera `ESPEC-004`, dejando solo
`Precision_GPS`/`RG-02`/`RG-19`/`RG-03` pendientes — que es exactamente el estado más probable, dado
que `PROMPT_CABLEADO.md` avanza tabla por tabla y no columna por columna): entonces sí hace falta
borrar y volver a dar de alta `MAN_Mantenimientos` para que `Precision_GPS` desaparezca de verdad del
esquema. **Eso destruye todo lo demás que ya estuviera cableado en esa tabla**, no solo
`Precision_GPS`: la clave, los tipos, las cinco referencias salientes
(`OTID`, `TecnicoID`, `EstadoActivoID`, `MotivoPendienteID`, `ModoFallaID`), el `Editable_If` de
`Coordenadas_Cierre_LatLong`/`UbicacionEscaneo_LatLong`/`FechaHoraEscaneo`, el `Label`, y las tres
referencias entrantes con `IsPartOf` (`FOT_Fotografias`, `FIR_Firmas`, `CHK_Checklists` →
`MAN_Mantenimientos`), que tendrían que volver a marcarse desde el lado de esas tres tablas.

**Procedimiento de la Rama B, en orden:**

1. Antes de borrar, **copiar a mano del editor** el estado de cada columna de `MAN_Mantenimientos`
   (tipo, `Initial value`, `Valid_If`, `Required_If`, `Editable_If`, `App formula`, `Label`) — no
   hay comando que lo lea de vuelta (`docs/BASE_CONOCIMIENTO_APPSHEET.md`, "Cómo se lee de vuelta:
   NADIE"). Es la única forma de saber, después, si la reconstrucción quedó igual.
2. Aplicar `ORDEN-004` a `modelo_objetivo.py` (§4) y regenerar la hoja
   (`python scripts/generar_plantilla.py`), para que la pestaña `MAN_Mantenimientos` ya no tenga la
   columna `Precision_GPS` cuando se vuelva a dar de alta.
3. En el editor: `Delete` sobre la tabla `MAN_Mantenimientos`, y volver a añadirla desde la misma
   pestaña.
4. Repetir el encargo completo de `docs/PROMPT_CABLEADO.md` para esa única tabla: Paso 1 (`Are
   updates allowed`), Paso 2 (`Key`), Paso 2 — 39 referencias (solo las que tocan `MAN_Mantenimientos`,
   ocho saltos), Paso 3bis (tipos), Paso 4 (`Label`), Paso 5 (las expresiones y las reglas que le
   tocan, ahora sin `RG-02`/`RG-19` y con `RG-03` finalmente disponible sobre una columna editable).
   Volver a marcar `IsPartOf` en las tres referencias entrantes.
5. Comparar contra la copia del paso 1: todo lo que no sea `Precision_GPS`/`RG-02`/`RG-19` tiene que
   quedar exactamente igual que antes de borrar. Cualquier diferencia es un defecto de la
   reconstrucción, no un cambio deseado por este documento.

**Cuál rama aplica se decide en el momento, mirando el editor — no aquí.** Este documento no da por
supuesto que la Rama A es la que va a ocurrir; el estado de hoy (`ESTADO.md`) hace pensar que la
tabla está más cerca de la Rama B que de la A, porque los tres bloqueantes que cita son
específicamente `RG-02`/`RG-19`/`RG-03` y no "toda la tabla sin tocar". Se declara la rama más cara
explícitamente para que nadie la descubra en el momento, mirando fijo un mensaje de "Delete and
re-add the table" sin saber que ya está previsto.

### 2.9 Qué despierta el fixture de `PRUEBA-004`: tres efectos verificados por simulación, no supuestos

`PRUEBA-004` necesita crear dos filas reales (una con `CierreConExcepcion = TRUE`, una con `FALSE`)
en `MAN_Mantenimientos` y `OT_OrdenesTrabajo` para probar `RG-03`. Esas dos tablas, hoy vacías, pasan
a tener contenido, y **eso despierta comprobaciones que hoy están dormidas por falta de filas**. Se
verificó cada una simulando el escenario completo sobre una copia de `scripts/` y
`BD/Modelo_Datos_PLANTILLA.xlsx` fuera del repositorio, nunca sobre el repositorio real.

**1. `G-04` se apaga en las dos tablas del fixture, sin que ningún tipo quede confirmado.**
`scripts/verificar_datos.py` salta su aviso de "tabla vacía, tipada a ciegas" en cuanto la tabla deja
de estar vacía (`if not filas: ... continue`). Verificado: con las dos filas del fixture insertadas,
`G-04` deja de mencionar `MAN_Mantenimientos` y `OT_OrdenesTrabajo` en su salida — **no porque sus
211 columnas restantes se hayan confirmado en el editor, sino porque dos filas creadas por la
aplicación bastan para que el script deje de mirar la tabla.** No es un defecto de `G-04` — su
propósito es señalar tablas sin dato con qué inferir, y ahora sí lo hay —, pero es una trampa para
quien lea la salida de `verificar_datos.py` después del fixture y la lea como "los tipos de estas
dos tablas ya están bien": no lo dice. Sigue haciendo falta cotejar `Data > Columns` a mano
(`docs/TIPOS_ESPERADOS.md`), como ya pedía `ESTADO.md` antes del fixture.

**2. `G-05` despierta con un aviso nuevo, legítimo, que no es una regresión.** Antes del fixture,
`G-05` no dice nada sobre las columnas de `MAN_Mantenimientos` porque la tabla entera está vacía
(`if not filas: continue # tabla vacia: ya lo cuenta G-04`). Con las dos filas del fixture pobladas
(`OTID`, `TecnicoID`, `EstadoActivoID`, `Coordenadas_Cierre_LatLong`, `CierreConExcepcion`,
`Observaciones`, pero **no** `UbicacionEscaneo_LatLong`, que sigue vacía porque `OrigenApertura =
Lista`), verificado hoy:

```
! [G-05] MAN_Mantenimientos.UbicacionEscaneo_LatLong esta vacia en las 2 filas y de ella depende
  RG-13. La regla queda configurada y sin efecto: no da error, no hace nada
```

Es exactamente el caso de `RG-13` que §2.5 ya declaró fuera de alcance: `UbicacionEscaneo_LatLong`
no se llena mientras el QR siga fuera de alcance, con fixture o sin él. **Este aviso nuevo es
esperado y no delata ningún defecto de `ESPEC-004`.** Hace falta decirlo explícitamente porque, si
nadie lo anticipa, alguien va a leerlo como una regresión que introdujo este cambio y va a perder
tiempo investigando algo ya cerrado.

**3. `F-11` puede certificar en falso `OT_OrdenesTrabajo` como "clave legible" si el orden se
invierte — riesgo de secuencia, no del diseño.** `verificar_faseA.py` exime de `F-11` a toda tabla
que esté en `CLAVE_GENERADA` (`if tabla in CLAVE_GENERADA: continue`), sin mirar su contenido. Tras
`ORDEN-005` (que `ESPEC-004` da por aplicada, ver la nota de apertura), `OT_OrdenesTrabajo` está en
`CLAVE_GENERADA`, así que `F-11` queda en silencio total sobre ella, con o sin fixture — verificado
por simulación con el modelo ya corregido: ningún `F-11` menciona `OT_OrdenesTrabajo`.

**Pero si `verificar_faseA.py` se corre contra un estado en que `modelo_objetivo.py` todavía NO
tiene `OT_OrdenesTrabajo` en `CLAVE_GENERADA`** — por ejemplo, si alguien crea el fixture de
`PRUEBA-004` sobre la aplicación real (que ya tiene `OTID` generándose con `UNIQUEID()` por
`ORDEN-005`) pero corre el verificador contra una copia de `modelo_objetivo.py` que aún no refleja
ese cambio —, ocurre lo que `ESPEC-005` existe para revertir. Verificado por simulación:

```
$ python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
  ok OT_OrdenesTrabajo: clave legible, coherente con CLAVE_LEGIBLE
```

`_clave_es_legible()` solo comprueba que el valor sea una cadena no puramente numérica — un
`UNIQUEID()` de AppSheet (una cadena hexadecimal) pasa esa prueba igual que `OT-0001` la pasaría.
**`F-11` no distingue una clave legible de una clave aleatoria que por casualidad no es un número
puro.** Si `CLAVE_GENERADA` no está al día en el código que se ejecuta, `F-11` certifica
"coherente con `CLAVE_LEGIBLE`" sobre exactamente la columna que `ESPEC-005` decidió que ya no lo
es — un falso positivo que tapa la discrepancia en vez de señalarla.

**Consecuencia para el orden de ejecución, no para el diseño de `ESPEC-004`:** el fixture de
`PRUEBA-004` no debe crearse hasta que `ORDEN-005` esté completa **en el mismo `modelo_objetivo.py`
que se vaya a usar para verificar** — modelo, hoja regenerada y claves cableadas en el editor. Si en
algún momento `verificar_faseA.py` muestra "`OT_OrdenesTrabajo`: clave legible, coherente con
`CLAVE_LEGIBLE`" después de que `ESPEC-005` se haya aprobado, es la señal de que el código que se
está corriendo no es el que se aplicó — nunca la señal de que la clave volvió a ser legible.

### 2.10 El discriminador que le faltaba a `P-06`: cómo distinguir "`RG-01` validó" de "`RG-01` no se evaluó"

`docs/BASE_CONOCIMIENTO_APPSHEET.md:300` — tabla "Lo que sigue SIN verificar contra la fuente":

> «**Que AppSheet evalúe un `Valid_If` sobre una columna con `Editable_If = FALSE`** | `RG-01` sobre
> `Coordenadas_Cierre_LatLong`, y con ella `P-09`, que es innegociable | `RG-20` hace la columna no
> editable y `RG-01` pone su validación encima. **Si no se evalúa, la regla parece funcionar por no
> ejercitarse nunca**: `P-09` pasaría sin probar nada. Es el peor modo de fallo posible y no hay
> página oficial que lo aclare.»

Esto no es un supuesto sobre `RG-19` ni sobre la geolocalización simulada del navegador (§1.5 de
`PRUEBA-004` sigue siendo la técnica que hace falta para que `RG-01` deje pasar el cierre en las
pruebas de `RG-03`): es el supuesto que sostiene **que las pruebas de esta tanda estén probando
algo**. Si `RG-01` no se evalúa nunca sobre una columna `Editable_If = FALSE`, cualquier cierre se
guardaría sin comprobar la distancia — con la técnica de spoofing funcionando o sin funcionar,
porque la validación que debería fallar si el spoofing fallara nunca se ejecuta. `P-06` y `P-07` de
`PRUEBA-004` pasarían igual, por la razón equivocada, y nadie lo notaría mirando solo el resultado
de esas dos pruebas.

**El discriminador ya existe en el proyecto y no hay que inventarlo:** es el mismo que usa `P-08`
(cierre en rango) y `P-09` (cierre fuera de rango, **innegociable**) de `PRUEBA-003` — un cierre
cercano tiene que pasar y uno lejano tiene que rechazarse; **si los dos pasan, el `Valid_If` no se
está evaluando**, tal como `scripts/generar_manual_despliegue.py:850` ya instruye: *"pruebe un
cierre cercano y uno lejano. Si los dos salen aceptados, sospeche de esto antes que del radio."* Se
añade a `P-06` de `PRUEBA-004` como precondición explícita: no correr `P-06`/`P-07` como evidencia
de nada hasta confirmar que `P-09` de `PRUEBA-003` se ejecutó **sobre este mismo despliegue** (la
aplicación se reconstruyó entera el 2026-08-10, así que una `P-09` de una reconstrucción anterior no
sirve) y que su caso lejano fue **rechazado**. Detalle en `PRUEBA-004`.

### 2.11 La alternativa evaluada: convertir la instrucción en una pregunta contestable, no en un número

Se planteó una alternativa más barata que la ya rechazada en §3 (volver editable
`Coordenadas_Cierre_LatLong`): **no pedir el número, preguntar qué vio el técnico.** El argumento es
correcto en su premisa: el dato que se busca —una estimación de precisión— **ya aparece en pantalla**
durante la captura manual (§2.1), así que no hace falta construir nada para producirlo; lo único que
falta es una pregunta que lo recoja.

**Se evalúa y se adopta una versión mínima, sin tocar el mecanismo.** Hoy, `MotivoExcepcion` es un
`LongText` libre y `CierreConExcepcion` es una casilla sin más contexto que su nombre: el manual (no
la app) es quien le dice al técnico, en prosa, que la marque si la precisión es mala. Eso es
exactamente "una instrucción de comportamiento, no una pregunta contestable" — el defecto que la
alternativa señala. La corrección adoptada no cambia el esquema ni añade columnas ni toca `RG-03`:
**se fija la `Description` de `CierreConExcepcion` en el editor** (una propiedad de columna estándar
de AppSheet, distinta del `Label`, que se muestra como texto de ayuda bajo el campo en el
formulario) para que la casilla deje de ser un flag mudo y pase a formular la pregunta
explícitamente: *"¿La app no alcanzó buena precisión al capturar la posición de cierre? Marque si
es así."* Es gratis, no introduce un dato que parezca duro y no lo sea —sigue siendo un juicio del
técnico, declarado como tal—, y es la traducción directa de "convertir la instrucción en pregunta"
sin repetir el error de `CodigoQR` que motivó rechazar la otra alternativa (pedir el número
transcrito). Se declara en §4 como una línea más del encargo de cableado, no como una regla nueva.

**Se sigue rechazando pedir el número transcrito** (ya evaluado y descartado en la versión anterior
de este documento, §7): un número que nadie puede contrastar después es exactamente el patrón que le
costó caro al proyecto con `CodigoQR`. La pregunta contestable no tiene ese problema porque no
finge ser una medición: es una casilla con una pregunta explícita en vez de implícita.

### 2.12 La exposición real que la versión anterior de este documento no nombraba

Repetido con precisión, porque conviene que quede aparte y no diluido entre los demás hallazgos:

- **El técnico que marca la excepción a voluntad no es el riesgo.** No puede falsear dónde estuvo:
  `RG-01` sigue comprobando la distancia por `DISTANCE()`, y `HERE()` sobre
  `Coordenadas_Cierre_LatLong` sigue sin ser editable (`RG-20`). Marcar la casilla cuando no hacía
  falta es, como mucho, ruido en las estadísticas de excepción — no un fraude sobre la posición.
- **El riesgo real es el técnico que cierra con GPS malo y NO marca.** Nada lo detecta. `RG-01`
  no lo cubre, porque "mala precisión" y "fuera de radio" son fallos distintos: un cierre puede
  estar dentro del radio de geofencing con una posición de baja confianza (el propio texto oficial
  de §2.1 dice que la precisión varía por hardware, red y condiciones locales) y `RG-01` lo deja
  pasar sin más, porque solo mide distancia, no calidad de la señal. La marca depende enteramente de
  que el técnico decida ponerla.
- **Quien escriba directamente en el Sheets se salta `RG-03` entero.** `Required_If` es una regla de
  formulario de AppSheet: no existe en la hoja de cálculo. Una edición directa en
  `Modelo_Datos_10082026` puede dejar `CierreConExcepcion = TRUE` con `MotivoExcepcion` en blanco sin
  que nada lo impida ni lo señale.
- **La especificación anterior prometía "constancia auditable" sin decir dónde se cumple esa
  garantía.** Se cumple **en la aplicación, y solo en la aplicación**: en el formulario de AppSheet,
  con la sesión iniciada por el técnico. Fuera de ese camino —edición directa del Sheets, o
  simplemente el silencio de quien no marca la casilla— no hay ninguna constancia, auditable o no.

Esto no es un defecto nuevo que introduzca `ESPEC-004`: es la superficie de riesgo que queda **una
vez que este documento hace su trabajo**. Antes de `ESPEC-004` la pregunta ni se podía contestar; con
`ESPEC-004`, se puede contestar, pero contestarla sigue siendo voluntario y no hay ningún contraste
automático. Ver §6 para quién vigila esto y con qué cadencia, y §5 para lo que este documento
explícitamente no resuelve.

## 3. Qué cambia exactamente

| Tabla.Columna / elemento | Estado actual | Estado objetivo |
|---|---|---|
| `MAN_Mantenimientos.Precision_GPS` | `Number`, `Initial value = USERLOCATIONACCURACY()`, `editable=False` | **Retirada del modelo.** Ver §2.8 para cómo se retira, de verdad, del editor |
| `MAN_Mantenimientos.CierreConExcepcion` | `Yes/No`, `App formula` (`RG-19`), no editable de hecho | `Yes/No`, sin fórmula, editable por el técnico. `Description` en el editor formulada como pregunta (§2.11) |
| `MAN_Mantenimientos.MotivoExcepcion` | `LongText`, `Required_If = [CierreConExcepcion] = TRUE` (`RG-03`) | **Sin cambios.** `Required_If` lee el valor actual de la casilla, no cómo llegó ahí |
| `RG-02` (Initial value) | Activa en `REGLAS` | **Retirada.** La columna que inicializaba desaparece |
| `RG-19` (App formula) | Activa en `REGLAS` | **Retirada.** No hay expresión que calcular |
| `RG-03` (Required_If) | Activa en `REGLAS` | Sin cambios en la expresión. Ahora sí se puede poner en el editor |
| `RG-20` (Editable_If FALSE) | Cubre `Coordenadas_Cierre_LatLong`, `Precision_GPS`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo` | Cubre las mismas **tres** columnas restantes |
| `PAR_Parametros.UMBRAL_GPS` (fila) | Descripción dice "Error del satelite... (RG-19)" | **Se conserva la fila.** Se reescribe la descripción: ya no la lee ninguna regla; es la cifra de referencia que el técnico usa para su propio juicio |
| `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (D-04), `docs/FUNCIONAL_SGMC.md §6.4`, `Manuales/MANUAL_DE_USUARIO.md §3.4, §5.4 y las tres líneas de §2.6` | Describen o presuponen una comparación automática, y tres líneas del manual dicen que `Ubicacion_LatLong` está vacía | Se ajustan a mano — no se regeneran solos — ver §4 |

### Sobre la "mejora" de volver editable `Coordenadas_Cierre_LatLong` — se rechaza

Se propuso poner `Coordenadas_Cierre_LatLong` en captura manual (editable) en vez de `HERE()`, para
que el técnico vea la precisión en pantalla antes de decidir. **No es segura tal como está
planteada, y no debe adoptarse.**

`RG-20` existe, con esas mayúsculas en su propia descripción, precisamente para impedir que
`Coordenadas_Cierre_LatLong` sea editable: *"Coordenadas_Cierre es un LatLong, que en un formulario
AppSheet dibuja como un pin arrastrable sobre un mapa, y la ubicación del activo está visible en la
app: el técnico arrastra el pin encima del activo y RG-01 valida sin protestar."* El control de
"capturar con la precisión más alta" (el ícono que muestra los metros en pantalla, y que AppSheet
mismo recomienda usar cuando la precisión importa, §2.1) vive **dentro del mismo control editable**
que el pin arrastrable. Hacer editable `Coordenadas_Cierre_LatLong` para ganar el dato en pantalla
**reabre exactamente el agujero que `RG-20` se escribió para cerrar** — y lo reabre en el control que
sostiene todo el geofencing (`RG-01`), no en un lugar menor.

La ganancia que se buscaba —darle al técnico un dato con el que decidir, en vez de una instrucción
muda— se obtiene por §2.11 sin tocar `Coordenadas_Cierre_LatLong`: formulando la pregunta en la
propia casilla.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`:

- **`MODELO["MAN_Mantenimientos"]["columnas"]`**: eliminar la entrada de `Precision_GPS`. Quitar el
  argumento `formula=...` de la entrada de `CierreConExcepcion`; la columna queda como
  `col("CierreConExcepcion", "Yes/No", nota="El técnico la marca cuando la app no le mostró buena
  precisión al capturar el cierre. Criterio de referencia: PAR_Parametros.UMBRAL_GPS. Antes se
  calculaba con RG-19 y USERLOCATIONACCURACY(), que no existe en AppSheet; ver ESPEC-004. Su
  Description en el editor formula la pregunta explícitamente, ver ESPEC-004 §2.11")`.
- **`CAMPOS_RETIRADOS["MAN_Mantenimientos"]`**: añadir `"Precision_GPS":` con motivo: *"
  USERLOCATIONACCURACY() no existe en AppSheet — el editor lo rechaza y la documentación oficial de
  captura de GPS (Capture GPS location, support.google.com/appsheet/answer/10106789) no ofrece
  ninguna función equivalente; esa misma página recomienda la captura manual sobre HERE() cuando la
  precisión importa, y este sistema mantiene HERE() por la razón que RG-20 protege (ver ESPEC-004
  §2.1 y §3). La columna quedó siempre en blanco y RG-19, que la comparaba, nunca se disparó.
  Retirada con ESPEC-004; CierreConExcepcion pasa a marcarla el técnico. Retirar la columna del
  esquema de AppSheet exige Delete-and-re-add de la tabla si ya estaba dada de alta con esta columna
  sin usar — ver ESPEC-004 §2.8."*
- **`REGLAS`**: eliminar los `dict` de `RG-02` y `RG-19`. En el `dict` de `RG-20`, quitar
  `Precision_GPS` de la lista de columnas que cubre y de su texto explicativo.
- **`PARAMETROS`**: **no se retira** `UMBRAL_GPS`. Se reescribe su descripción siguiendo el
  precedente de `RADIO_GEOFENCING_KM`: *"Ninguna regla la lee desde el 2026-08-10 (ESPEC-004):
  RG-19 se retiró porque USERLOCATIONACCURACY() no existe en AppSheet. Se conserva como el criterio
  que el manual de usuario comunica al técnico para su propio juicio, y que el administrador ajusta
  aquí sin abrir el editor — aunque hoy ese ajuste no se propaga solo al manual, hay que actualizarlo
  a mano."*
- **`DECISIONES`**: la entrada *"Cierre sin GPS válido"* no cambia de lado, pero su `por_qué` debe
  añadir que el valor de `CierreConExcepcion` ahora lo pone el técnico y no una fórmula, remitir a
  este `ESPEC-004`, y nombrar la exposición residual de §2.12 con una frase, no en silencio.

**Consecuencias fuera de `scripts/modelo_objetivo.py`, en el mismo cambio (§2.7):**

- `scripts/validar_modelo.py:249` — quitar la entrada `"Precision del GPS"` de `COBERTURA`.
- `scripts/verificar_faseA.py:307-386` — retirar el bloque `F-12`/`F-13`.
- `scripts/generar_diccionario_bd.py:159` — quitar `"UMBRAL_GPS": "RG-19"` de `lectores`.
- `scripts/verificar_datos.py:213-214` — el comentario de cabecera de `G-05` que cita `RG-19` como
  ejemplo vigente del defecto hay que marcarlo como corregido, o sustituirlo por otro ejemplo
  abierto (por ejemplo `RG-06`/`GeneraAlerta`, que el propio comentario ya cita como caso vivo).
- **`scripts/generar_prompt_expresiones.py:293-311`** — editar a mano: borrar la sección "Dos que
  hoy NO se pueden poner" y sustituirla por una nota de una línea (§2.7).
- **`scripts/generar_guia_funcional.py:383,395`** — editar a mano: la cuenta de columnas no
  editables pasa de tres a dos junto a `Coordenadas_Cierre_LatLong`, y la cita de la `App formula` de
  `RG-19` se retira o se sustituye por una descripción de la casilla manual con su `Description`.
- **`scripts/generar_manual_despliegue.py:841,858`** — mismo tratamiento que el anterior.

**`generar_tipos_esperados.py` e `inferencia.py` no se editan** (§2.7): se regeneran solos y siguen
diciendo la verdad, porque citan `Precision_GPS` como hecho histórico, no como instrucción vigente.

**Documentos generados que se re-emiten con los comandos de siempre**, una vez editados los seis
scripts de arriba: `docs/bd.md`, `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`,
`docs/PROMPT_CABLEADO.md`, `docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`, `docs/TIPOS_ESPERADOS.md`, `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md`.

**Documentos no generados que hay que tocar a mano:**

- `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`, filas de `D-04` (líneas 108, 133): ya no puede decir "CERRADA
  en el mecanismo" sobre algo que nunca funcionó; debe decir que se corrigió con `ESPEC-004` y cómo.
- `docs/FUNCIONAL_SGMC.md §6.4`: añadir que quien marca la excepción es el técnico, no una fórmula.
- `Manuales/MANUAL_DE_USUARIO.md §3.4 y §5.4`: ajustar las frases que insinúan una comparación
  automática, para que quede claro que el umbral es una referencia para el juicio del técnico.
- **`Manuales/MANUAL_DE_USUARIO.md`, líneas 46, 168 y 266** (§2.6): corregir las tres afirmaciones de
  que `Ubicacion_LatLong` está vacía. Está poblada en las 368, con valores sintéticos derivados del
  `PK` — sigue sin estar medida en campo (`D-01`), que es lo que sí importa decir. No es objeto
  central de este `ESPEC`, pero se cierra aquí por estar ya editando este mismo archivo.

## 5. Qué NO cubre esta especificación

- **No resuelve `RG-13`ni `RG-18`** (§2.5). `RG-13` sigue sin propiedad real de AppSheet que la aloje
  y sin poder poblarse mientras el QR siga fuera de alcance; `RG-18` es una prohibición sobre cómo se
  construyen reportes que todavía no existen (`D-12`).
- **No resuelve `D-01`.** Las coordenadas de `ACT_Activos` son sintéticas, derivadas del PK. `RG-01`
  puede seguir rechazando cierres legítimos por esa razón, independiente de este documento.
- **No construye ningún reporte.** `D-12` sigue abierta; este documento no la cierra.
- **No detecta el cierre con GPS malo que nadie marca (§2.12).** La única defensa contra ese caso es
  el juicio del técnico y, ahora, la pregunta explícita de §2.11 — no hay contraste automático.
  Construir uno (por ejemplo, un reporte que cruce duración de captura contra hora de cierre, o un
  patrón de cierres consecutivos sin excepción en zonas de mala cobertura conocida) es un frente
  aparte, con su propio `ESPEC`, y no se dimensiona aquí.
- **No impide que alguien escriba directo en el Sheets y se salte `RG-03` entero (§2.12).** Es una
  limitación de arquitectura de AppSheet (`Required_If` no existe fuera del formulario), no algo que
  este documento pueda cerrar.
- **No inventa una función de AppSheet que no existe.** Si AppSheet añade en el futuro una forma de
  leer la precisión del GPS en una columna, reabrir esta decisión es legítimo y barato.
- **No crea una estructura formal de "reglas retiradas"** en `modelo_objetivo.py`. La traza queda en
  este documento, en `DECISIONES`, y en el hueco numérico que dejan `RG-02`/`RG-19` al desaparecer.

## 6. Riesgos y dependencias

### 6.1 Dependencia dura de orden: `ESPEC-005` primero, y en el mismo código que se verifica

No es solo una preferencia de secuencia: es un requisito técnico. `PRUEBA-004` monta su fixture
sobre claves de `OT_OrdenesTrabajo` que `ESPEC-005` convierte en `UNIQUEID()` (§2.9); si el orden se
invierte, el fixture es inconstruible tal como está escrito. Y, verificado por simulación (§2.9),
correr `verificar_faseA.py` contra un `modelo_objetivo.py` que no refleje `ORDEN-005` completa puede
producir un falso positivo (`F-11` certificando `OT_OrdenesTrabajo` como clave legible) que oculta
exactamente el error de secuencia que se cometió.

### 6.2 Dependencia dura dentro del mismo cambio: los seis generadores y los tres verificadores de §2.7

`scripts/validar_modelo.py`, `scripts/verificar_faseA.py`, `scripts/generar_diccionario_bd.py`,
`scripts/generar_prompt_expresiones.py`, `scripts/generar_guia_funcional.py` y
`scripts/generar_manual_despliegue.py` tienen que editarse en el mismo cambio que
`modelo_objetivo.py`, o el pipeline deja de decir la verdad, o peor, instruye al ejecutor a cablear
algo retirado (el caso de `generar_prompt_expresiones.py`, el más caro).

### 6.3 Ruta de reversión — no existía en la versión anterior de este documento

**Punto exacto a partir del cual la reversión deja de ser gratuita: la primera fila de
`MAN_Mantenimientos` donde un técnico guardó `CierreConExcepcion` con intención — TRUE marcado a
propósito, o FALSE dejado sin marcar tras haber abierto el formulario.** Antes de ese punto (el
estado de hoy: 0 filas, §2.3), revertir cuesta lo que cueste deshacer §4 más, si se llegó a la Rama B
de §2.8, repetir el cableado de `MAN_Mantenimientos` una vez más — caro en tiempo, pero sin ninguna
pérdida de dato real, porque no hay ninguno.

**A partir de ese punto, revertir el modelo (volver a poner la `App formula` de `RG-19` sobre
`CierreConExcepcion`) es destructivo, y no de forma hipotética.** Una `App formula` "materializa su
valor al guardar: no pinta la celda, la escribe" — es literalmente lo que demuestra `P-33` de
`PRUEBA-003` sobre `RG-16`, el mismo mecanismo. Si se revierte y luego esa fila se vuelve a guardar
por cualquier motivo —incluida una edición menor de otro campo—, `RG-19` recalcula
`CierreConExcepcion` contra `Precision_GPS` (que sigue en blanco, porque nunca se pudo poblar) y la
fuerza a `FALSE`, **borrando en silencio la marca TRUE que el técnico dejó a propósito.** Si
`MotivoExcepcion` ya tenía texto, queda huérfano: una `LongText` con contenido, sobre una casilla que
ya no dice que hacía falta. El histórico de auditoría de esa fila queda corrompido por la propia
reversión — el defecto exactamente opuesto al que este documento existe para cerrar, y sin que nadie
lo note salvo comparando contra una copia de la fila anterior a la reversión.

**Qué hacer si hay que revertir después de ese punto:** exportar (Drive → descarga o
`scripts/instantanea.py`) todas las filas de `MAN_Mantenimientos` con `CierreConExcepcion` o
`MotivoExcepcion` no vacíos **antes** de tocar el modelo, y aceptar que, tras revertir, esas filas
quedan como registro histórico que no se debe volver a guardar desde el formulario — no hay ningún
mecanismo en este modelo para congelar una fila del recálculo de una `App formula` sin condicionar la
propia fórmula a una fecha de corte, y añadir esa condición sería una regla nueva, no contemplada
aquí.

### 6.4 El riesgo residual de §2.12 necesita dueño y cadencia — no lo tenía

Un control que depende por completo de la autodeclaración del técnico, sin lector automático y sin
contraste, es decoración si nadie lo revisa. `D-12` (los seis reportes propuestos, incluida la vista
de cierres con excepción por técnico y por activo que `MANUAL_DE_USUARIO.md §3.4` ya promete) sigue
abierta, así que hoy no hay ninguna vista que cuente las marcas.

**Se adopta como supuesto de trabajo, hasta que `D-12` entregue esa vista:** el supervisor —el mismo
rol que ya aprueba y cierra cada orden en `EOT_EstadosOrden` (§4.2 del manual)— revisa `Observaciones`
y `MotivoExcepcion` de las órdenes de su unidad funcional al aprobar cada cierre, uno por uno, porque
hoy no hay forma de verlas agregadas. Es una cadencia forzada por la falta de reporte, no la deseada:
en cuanto `D-12` entregue la vista, la revisión pasa a ser periódica (semanal, alineada con el resto
de reportes que `D-13` va a definir) en vez de por cada cierre individual. Se declara el supuesto
explícitamente en §7 para que no quede como un vacío sin dueño.

### 6.5 Lo demás

- **No hay datos que migrar** (§2.3).
- **La prueba de aceptación tropieza con `RG-01`, no con este cambio.** Detallado en `PRUEBA-004`.
- **Riesgo de sincronización manual aceptado en `UMBRAL_GPS`**, igual que el precedente de
  `RADIO_GEOFENCING_KM`.

## 7. Supuestos adoptados

- **Se adopta la propuesta del encargo**: retirar `RG-02`/`Precision_GPS`, convertir
  `CierreConExcepcion` en una casilla editable por el técnico, dejar `RG-03` sin cambios de
  expresión. Sigue siendo la única de las alternativas evaluadas que no exige algo que AppSheet no
  ofrece hoy — ver el detalle en la versión anterior de este documento, no repetido aquí punto por
  punto porque no cambió.
- **Se adopta la pregunta contestable de §2.11** (`Description` de `CierreConExcepcion` formulada
  como pregunta) como refinamiento de costo cero, sin tocar el esquema ni `RG-03`. Se sigue
  rechazando pedir el número transcrito.
- **Se adopta rechazar la "mejora" de volver editable `Coordenadas_Cierre_LatLong`** (§3).
- **Se adopta conservar `PAR_Parametros.UMBRAL_GPS`** sin lector, siguiendo el precedente de
  `RADIO_GEOFENCING_KM`.
- **Se adopta que `RG-13` y `RG-18` quedan fuera de alcance** de este `ESPEC` (§2.5, §5).
- **Se adopta la Rama B de §2.8 como la más probable**, dado el estado que describe `ESTADO.md` hoy,
  y se documenta el procedimiento completo por si ocurre, en vez de dejarlo para improvisar en el
  momento.
- **Se adopta un dueño y una cadencia provisionales para el riesgo residual de §2.12** (§6.4): el
  supervisor, revisando por cierre individual hasta que `D-12` entregue una vista agregada. No es un
  supuesto sobre el sistema, es una decisión operativa que se declara aquí para que no quede sin
  responsable.
- **Se adopta que lo que se pierde es menor de lo que parece**, porque nunca hubo nada que perder en
  la práctica: la cadena automática jamás se disparó sobre una fila real. Lo que cambia, y hay que
  decirlo sin suavizarlo, es que **ahora existe un camino real para que el técnico lo diga**, que la
  única defensa contra un cierre con mala señal sigue siendo que decida decirlo, y que nadie más lo
  contrasta hasta que `D-12` exista.
