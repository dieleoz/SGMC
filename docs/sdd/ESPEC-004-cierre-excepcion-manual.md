# ESPEC-004 — Cierre con excepción por GPS: de fórmula inexistente a marca del técnico

## 1. Qué se quiere y por qué

`RG-02` inicializa `MAN_Mantenimientos.Precision_GPS` con `USERLOCATIONACCURACY()`. Esa función
**no existe en AppSheet**: lo reportó el editor al intentar escribirla (`Can't find function
"USERLOCATIONACCURACY"`) y lo confirmo hoy de forma independiente contra la página oficial de
captura de GPS — ver §2. `RG-19` compara `Precision_GPS` contra `PAR_Parametros.UMBRAL_GPS` para
calcular `CierreConExcepcion`; como `Precision_GPS` nunca se puebla, esa comparación es siempre
`número > blanco`, que en AppSheet evalúa `FALSE`. `RG-03` exige `MotivoExcepcion` solo si
`CierreConExcepcion = TRUE`, y como esa condición nunca se cumple, **`MotivoExcepcion` no se le pide
nunca a nadie**, sin importar cuán mala sea la posición registrada.

Tres reglas están escritas, documentadas y (según `ESTADO.md`) pendientes de cablear en el editor
— es decir, todavía no se ha gastado el paso caro sobre esto. La decisión que este documento
permite tomar es concreta: **¿puede un técnico, alguna vez, dejar constancia auditable de que cerró
con el GPS deficiente?** Hoy la respuesta de diseño es no, aunque nadie lo hubiera notado hasta
intentar cablear la primera de las tres.

Esto no es una construcción nueva: es la corrección de una regla que el propio proyecto ya sabía
que estaba rota. `scripts/verificar_datos.py` trae desde hoy una comprobación nueva, `G-05`, escrita
explícitamente para cazar este caso (cita textual en su código, ver §2): *"RG-19 compara
Precision_GPS, que nadie puebla porque la función que la poblaría no existe en AppSheet"*.

## 2. Estado actual verificado

### 2.0 Contra cuál modelo

Según `python scripts/sistema.py`, hoy el sistema vigente es:

```
Aplicacion  _SISGA_-323965761
Datos       Modelo_Datos_10082026  (Google Sheets, fileId 1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
Volcado     BD/Modelo_Datos_PLANTILLA.xlsx
```

Este documento verifica **contra los dos**, y lo indica en cada punto: el volcado local con
`openpyxl`, y producción con `python scripts/instantanea.py guardar <nombre>` (usa la API v2 de
AppSheet, acción `Find`, contra la aplicación `_SISGA_-323965761`). Los dos coincidieron en todo lo
que se comprobó aquí; no hubo que resolver ninguna discrepancia.

> Nota de método: las dos instantáneas que tomé para escribir este documento
> (`prueba-espec-004.json`, `chk-act-activos.json`) se borraron después de leerlas, siguiendo la
> higiene de no dejar artefactos de verificación sueltos en `BD/instantaneas/`.

### 2.1 `USERLOCATIONACCURACY()` no existe

Verificado hoy contra la página oficial de captura de GPS de AppSheet:

```
$ curl -s "https://support.google.com/appsheet/answer/10106789" -A "Mozilla/5.0" | ...
```

> «There are four ways to capture the GPS location in a form: [1] LatLong column con App Formula
> `HERE()` ... [2] LatLong column con Initial Value `HERE()` ... [3] You can manually capture the
> current location. The input field for a LatLong column has a clickable icon that lets you
> capture the device's current GPS location. [...] with each button press the app will try to
> obtain the most accurate current location it can for up to 30 seconds or until an estimated
> accuracy of 10m is reached. **This method offers the highest accuracy and displays an estimate
> of the accuracy (in meters) within the app.** [4] Additionally, you can explicitly type in a
> LatLong value.»

— [Capture GPS location](https://support.google.com/appsheet/answer/10106789), AppSheet Help,
consultado el 2026-08-10.

Esa página es la referencia canónica de "cómo se captura una ubicación" en AppSheet y **no menciona
ninguna función que devuelva o guarde la precisión**. Confirma dos cosas a la vez:

1. No hay ninguna función equivalente a `USERLOCATIONACCURACY()` bajo otro nombre para esta
   finalidad.
2. La app **sí muestra** al técnico una estimación de precisión en metros, pero **solo en pantalla,
   durante la captura manual**, y nada en la documentación dice que ese número se pueda asignar a
   una columna. Es la base del rechazo de la "mejora" en §3.

No recorrí la lista completa de funciones de expresión de AppSheet — la página del generador de
listas devolvió contenido renderizado por cliente, no apto para `curl` — así que esta verificación
se apoya en la página canónica de captura de GPS más el error literal del editor que reportó quien
encargó este documento. Lo declaro como lo que es: dos fuentes independientes y consistentes, no una
enumeración exhaustiva.

### 2.2 La cadena está configurada y no puede dispararse nunca

`scripts/modelo_objetivo.py`, columnas de `MAN_Mantenimientos` (líneas 335-342):

```python
col("Precision_GPS", "Number", valor_inicial="USERLOCATIONACCURACY()", editable=False),
col("CierreConExcepcion", "Yes/No",
    formula='[Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")',
    nota="Se calcula, no se edita (RG-19). El umbral vive en PAR_Parametros"),
col("MotivoExcepcion", "LongText", nota="Obligatorio si CierreConExcepcion es verdadero"),
```

Y `REGLAS` (líneas 1111-1118, 1170-1186): `RG-02` (`Initial value`), `RG-03` (`Required_If`),
`RG-19` (`App formula`), tal como las describe la sección 1.

### 2.3 `MAN_Mantenimientos` está vacía en los dos modelos

Volcado local:

```
MAN_Mantenimientos filas totales (incl encabezado): 1
```

Producción, vía `instantanea.py`:

```
MAN_Mantenimientos filas: 0
```

No hay ninguna fila histórica que migrar ni que se vea afectada por retirar una columna. Esto
también significa que **la cadena rota nunca ha producido un solo cierre con excepción real**: no
se pierde un mecanismo que funcionaba, se corrige uno que nunca llegó a ejercitarse.

### 2.4 `PAR_Parametros.UMBRAL_GPS` coincide en los dos modelos

Volcado local:

```
('UMBRAL_GPS', 'Umbral de GPS deficiente', 40, 'm', 'Error del satelite...', 'TRUE')
```

Producción:

```
{'ParametroID': 'UMBRAL_GPS', 'Nombre': 'Umbral de GPS deficiente', 'Valor': '40', 'Unidad': 'm', 'Activo': 'Y'}
```

### 2.5 `RG-13` no tiene dónde vivir en el editor, y aunque lo tuviera no compensaría nada

`RG-13` está declarada con `tipo="Verificacion de evidencia"` (`scripts/modelo_objetivo.py:1154`).
Las otras 20 reglas usan siempre una de ocho propiedades reales de AppSheet: `Valid_If`,
`Required_If`, `Initial value`, `App formula`, `Bot`, `Bot programado`, `Security Filter`, `Are
updates allowed`, `Editable_If`. `"Verificacion de evidencia"` no es ninguna de ellas.

`docs/PROMPT_CABLEADO.md` — el encargo de cableado autocontenido, vigente — tiene un paso por cada
mecanismo real (Paso 2 referencias, Paso 3 tipos, Paso 4 etiqueta, Paso 5 las 21 reglas remitiendo a
`RECONSTRUCCION_EXPRESIONES.md`). En ninguno de ellos aparece la cadena `RG-13`:

```
$ grep -n "RG-13" docs/PROMPT_CABLEADO.md
(sin resultados)
```

Coincide con lo que reportó quien encargó este documento tras revisar el editor: no existe como
columna ni como bot. Es una regla escrita en tres documentos generados y en `modelo_objetivo.py`
que nunca se tradujo en un mecanismo de AppSheet.

Y aunque se implementara, **no compensaría la pérdida de detección de precisión**: `RG-13` compara
`UbicacionEscaneo_LatLong` contra `Coordenadas_Cierre_LatLong` (distancia entre dónde se escaneó y
dónde se cerró), una señal distinta de "el GPS tenía mala precisión". Su entrada,
`UbicacionEscaneo_LatLong`, solo se llena cuando `OrigenApertura = QR`
(`scripts/modelo_objetivo.py:327-329`), y el QR está **fuera de alcance desde el 2026-08-07**
(`SDD_PIPELINE_SGMC.md §8`); el valor inicial de `OrigenApertura` es `Lista`
(`scripts/modelo_objetivo.py:324`). Hoy `UbicacionEscaneo_LatLong` no se va a poblar nunca, así que
`RG-13`, si se cableara tal cual, caería en el mismo defecto que `G-05` ya persigue: una regla
configurada que lee una columna vacía.

### 2.6 Un hallazgo colateral, verificado y relevante para las pruebas de este cambio

`docs/ALCANCE_Y_SUPUESTOS_SGMC.md` (líneas 92, 149) afirma que `ACT_Activos.Ubicacion_LatLong` está
**vacía en las 368 filas**. Verificado hoy, está **poblada en las 368**, en el volcado y en
producción:

```
ACT_Activos filas: 368  Ubicacion_LatLong pobladas: 368
SOS-001 5.099798, -73.718568
SOS-002 5.098955, -73.714034
...
```

`docs/README.md` ya lo tiene al día: son puntos **sintéticos, derivados del PK** sobre el eje de la
vía (`scripts/generar_plantilla.py:260-287`), no coordenadas levantadas (`D-01` sigue abierta). El
archivo `.xlsx` es más nuevo (21:35) que `ALCANCE_Y_SUPUESTOS_SGMC.md` (20:31), así que ese
documento quedó desactualizado en ese punto por una regeneración posterior. No lo corrijo aquí —no
es el objeto de este `ESPEC`— pero lo señalo porque afecta directamente cómo se puede probar este
cambio: ver §6.

### 2.7 Lo que rompe si se retira `Precision_GPS` sin tocar nada más

Tres puntos objetivos, con archivo y línea, que **tienen** que cambiar junto con el modelo o dejan
de decir la verdad:

| Archivo | Qué depende de `Precision_GPS` |
|---|---|
| `scripts/validar_modelo.py:249` | `COBERTURA["Precision del GPS"] = ("MAN_Mantenimientos", "Precision_GPS")`. Si la columna se retira y esta entrada no, `V-13` falla y `validar_modelo.py` deja de dar 0 errores — el único gate objetivo del pipeline |
| `scripts/verificar_faseA.py:307-386` (bloque `F-12`/`F-13`) | Cruza fila por fila `Precision_GPS` contra `CierreConExcepcion` asumiendo que `RG-19` sigue siendo una `App formula`. Sin la fórmula, ese cruce no tiene sentido: hay que retirarlo, no dejarlo comparando contra una regla que ya no existe |
| `scripts/generar_diccionario_bd.py:159` | `lectores = {"UMBRAL_GPS": "RG-19", ...}`. Con `RG-19` retirada, `docs/bd.md` seguiría atribuyéndole un lector que ya no existe |

## 3. Qué cambia exactamente

| Tabla.Columna / elemento | Estado actual | Estado objetivo |
|---|---|---|
| `MAN_Mantenimientos.Precision_GPS` | `Number`, `Initial value = USERLOCATIONACCURACY()`, `editable=False` | **Retirada.** No hay ninguna forma de poblarla en AppSheet hoy |
| `MAN_Mantenimientos.CierreConExcepcion` | `Yes/No`, `App formula` (`RG-19`), no editable de hecho | `Yes/No`, sin fórmula, editable por el técnico como una casilla de verificación ordinaria |
| `MAN_Mantenimientos.MotivoExcepcion` | `LongText`, `Required_If = [CierreConExcepcion] = TRUE` (`RG-03`) | **Sin cambios.** `Required_If` lee el valor actual de la casilla, no cómo llegó ahí |
| `RG-02` (Initial value) | Activa en `REGLAS` | **Retirada.** La columna que inicializaba desaparece |
| `RG-19` (App formula) | Activa en `REGLAS` | **Retirada.** No hay expresión que calcular |
| `RG-03` (Required_If) | Activa en `REGLAS` | Sin cambios |
| `RG-20` (Editable_If FALSE) | Cubre `Coordenadas_Cierre_LatLong`, `Precision_GPS`, `UbicacionEscaneo_LatLong`, `FechaHoraEscaneo` | Cubre las mismas **tres** columnas restantes. Se retira `Precision_GPS` de la lista porque la columna desaparece. **Las otras tres NO se tocan** — ver el rechazo explícito de la "mejora" más abajo |
| `PAR_Parametros.UMBRAL_GPS` (fila) | Descripción dice "Error del satélite... (RG-19)" | **Se conserva la fila.** Se reescribe la descripción: ya no la lee ninguna regla; es la cifra de referencia que el técnico usa para su propio juicio, y que el manual de usuario reproduce a mano |
| `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`, `docs/FUNCIONAL_SGMC.md §6.4`, `Manuales/MANUAL_DE_USUARIO.md §3.4 y §5.4` | Describen o presuponen una comparación automática | Se ajustan a mano — no se regeneran solos — para que digan que la marca es un juicio del técnico. Ver §4 |

### Sobre la "mejora" propuesta — se rechaza

Se propuso poner `Coordenadas_Cierre_LatLong` en captura manual (editable) en vez de `HERE()`, para
que el técnico vea la precisión en pantalla antes de decidir. **No es segura tal como está
planteada, y no debe adoptarse.**

`RG-20` existe, con esas mayúsculas en su propia descripción
(`scripts/modelo_objetivo.py:1159-1169`), precisamente para impedir que `Coordenadas_Cierre_LatLong`
sea editable: *"Coordenadas_Cierre es un LatLong, que en un formulario AppSheet dibuja como un pin
arrastrable sobre un mapa, y la ubicación del activo está visible en la app: el técnico arrastra el
pin encima del activo y RG-01 valida sin protestar."* El control de "capturar con la precisión más
alta" (el ícono que muestra los metros en pantalla, confirmado en §2.1) vive **dentro del mismo
control editable** que el pin arrastrable. AppSheet no ofrece un botón de "capturar con precisión"
independiente de que el campo sea editable: son la misma superficie. Hacer editable
`Coordenadas_Cierre_LatLong` para ganar el dato en pantalla **reabre exactamente el agujero que
`RG-20` se escribió para cerrar** — y lo reabre en el control que sostiene todo el geofencing
(`RG-01`), no en un lugar menor.

La ganancia que se buscaba —mostrarle al técnico un número en pantalla para que decida con
criterio— no requiere tocar `Coordenadas_Cierre_LatLong`. Se pierde en este documento sin más: hoy
no hay ninguna forma de dar esa información al técnico dentro de la app sin volver editable un campo
protegido. Se compensa con la cifra fija comunicada por fuera de la app: el manual ya dice "espere
unos segundos... si la precisión sigue siendo insuficiente, marque" (§4), que es una instrucción de
comportamiento, no una lectura de pantalla verificada.

## 4. Cómo se declara en el modelo

Todo en `scripts/modelo_objetivo.py`:

- **`MODELO["MAN_Mantenimientos"]["columnas"]`**: eliminar la entrada de `Precision_GPS` (línea
  338). Quitar el argumento `formula=...` de la entrada de `CierreConExcepcion` (línea 339-341); la
  columna queda como `col("CierreConExcepcion", "Yes/No", nota="El técnico la marca cuando el GPS
  no da la precisión suficiente. Criterio de referencia: PAR_Parametros.UMBRAL_GPS. Antes se
  calculaba con RG-19 y USERLOCATIONACCURACY(), que no existe en AppSheet; ver ESPEC-004")`.
- **`CAMPOS_RETIRADOS["MAN_Mantenimientos"]`**: añadir `"Precision_GPS":` con un motivo en el mismo
  estilo que las demás entradas de esa tabla, por ejemplo: *"USERLOCATIONACCURACY() no existe en
  AppSheet — el editor lo rechaza y la documentación oficial de captura de GPS (Capture GPS
  location, support.google.com/appsheet/answer/10106789) no ofrece ninguna función equivalente. La
  columna quedó siempre en blanco y RG-19, que la comparaba, nunca se disparó. Retirada con
  ESPEC-004; CierreConExcepcion pasa a marcarla el técnico."*
- **`REGLAS`**: eliminar los `dict` de `RG-02` (líneas 1111-1114) y `RG-19` (líneas 1170-1186). En
  el `dict` de `RG-20` (líneas 1159-1169), quitar `Precision_GPS` de la lista de columnas que cubre
  y de su texto explicativo (que hoy la nombra junto con `HERE()` y
  `USERLOCATIONACCURACY()`).
- **`PARAMETROS`**: **no se retira** `UMBRAL_GPS`. Se reescribe su descripción (línea 762-766)
  siguiendo el precedente literal de `RADIO_GEOFENCING_KM` en la misma estructura (línea 767-771,
  *"RG-01 NO lo lee... Se conserva porque un umbral escondido en una expresión no se puede calibrar
  sin abrir el editor"*): *"Ninguna regla la lee desde el 2026-08-10 (ESPEC-004): RG-19 se retiró
  porque USERLOCATIONACCURACY() no existe en AppSheet. Se conserva como el criterio que el manual
  de usuario comunica al técnico para su propio juicio, y que el administrador ajusta aquí sin abrir
  el editor — aunque hoy ese ajuste no se propaga solo al manual, hay que actualizarlo a mano."*
- **`DECISIONES`**: la entrada *"Cierre sin GPS válido"* (línea 1057-1059) no cambia de lado — sigue
  siendo `CierreConExcepcion` + `MotivoExcepcion` contra "nota libre en Observaciones" — pero su
  `por_qué` debe añadir que el valor de `CierreConExcepcion` ahora lo pone el técnico y no una
  fórmula, y remitir a este `ESPEC-004`.

Consecuencias fuera de `modelo_objetivo.py`, que el ejecutor tiene que aplicar en el mismo cambio
para que el pipeline siga siendo objetivo (detalle y motivo en §2.7):

- `scripts/validar_modelo.py:249` — quitar la entrada `"Precision del GPS"` de `COBERTURA`.
- `scripts/verificar_faseA.py:307-386` — retirar el bloque `F-12`/`F-13` que cruza `Precision_GPS`
  contra `CierreConExcepcion`.
- `scripts/generar_diccionario_bd.py:159` — quitar `"UMBRAL_GPS": "RG-19"` de `lectores` (queda sin
  lector, como ya le pasa a `RADIO_GEOFENCING_KM`).
- `scripts/verificar_datos.py:205-221` — el comentario de cabecera de `G-05` cita este caso por su
  nombre como ejemplo del defecto que la comprobación persigue. Con la corrección aplicada, ese
  ejemplo describiría un defecto ya cerrado como si siguiera abierto; hay que anotarlo como
  corregido o sustituirlo por otro ejemplo vigente. La lógica de `G-05` en sí no cambia: sigue
  siendo genérica sobre cualquier columna que una regla lea y esté vacía.

Documentos **generados**, que se re-emiten con los comandos de siempre y no se editan a mano:
`docs/bd.md`, `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`,
`docs/PROMPT_CABLEADO.md`, `docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`.

Documentos **no generados** que sí hay que tocar a mano, porque describen el mecanismo en prosa:

- `docs/ALCANCE_Y_SUPUESTOS_SGMC.md`, filas de `D-04` (líneas 108, 133): ya no puede decir "CERRADA
  en el mecanismo" sobre algo que nunca funcionó; debe decir que se corrigió con `ESPEC-004` y cómo.
  De paso, esas líneas conviven con el hallazgo de §2.6 de este documento sobre `Ubicacion_LatLong`,
  que también quedó desactualizado — no es tema de este `ESPEC`, pero queda dicho para quien lo
  corrija.
- `docs/FUNCIONAL_SGMC.md §6.4`: el "por qué" de la fila 6.4 sigue siendo válido (una excepción
  tiene que ser contable, no un texto). Añadir que quien la marca es el técnico, no una fórmula.
- `Manuales/MANUAL_DE_USUARIO.md §3.4 y §5.4`: es el documento que menos hay que tocar. Su texto ya
  dice *"marque `Cierre con excepción`"* como una acción del técnico — coincide con este `ESPEC`, no
  con la fórmula rota. Ajustar solo las dos frases que insinúan una comparación automática ("El
  umbral de precisión no está escondido en el código: lo ajusta el administrador en la tabla de
  parámetros"), para que quede claro que el umbral es una referencia para el juicio del técnico y no
  algo que el sistema evalúe por sí solo.

## 5. Qué NO cubre esta especificación

- **No resuelve `RG-13`.** Queda exactamente tan inerte como hoy: sin propiedad real de AppSheet
  que la aloje, y con su entrada (`UbicacionEscaneo_LatLong`) sin poder poblarse mientras el QR siga
  fuera de alcance. Implementarla —probablemente como un bot que genere un reporte periódico, dado
  que su propia descripción dice "no bloquea: se reporta"— es una decisión de diseño aparte, con su
  propio `ESPEC`, y depende de que se reabra la decisión sobre el QR.
- **No resuelve `D-01`.** Las coordenadas de `ACT_Activos` son sintéticas, derivadas del PK, no
  levantadas en campo. Con 18 de los 27 tipos a 0,05 km de radio, `RG-01` puede seguir rechazando
  cierres legítimos por esa razón, independiente de todo lo que corrige este documento.
- **No construye ningún reporte.** `MANUAL_DE_USUARIO.md §3.4` promete que "el supervisor ve cuántos
  cierres con excepción tiene cada técnico y cada activo"; esa vista no existe (`D-12` sigue
  abierta, el modelo no declara vistas ni slices). Este documento no la crea.
- **No inventa una función de AppSheet que no existe.** No hay, hoy, ninguna forma de capturar la
  precisión del GPS en una columna dentro de esta plataforma. Si AppSheet la añade en el futuro,
  reabrir esta decisión es legítimo y barato: la columna se puede volver a declarar.
- **No crea una estructura formal de "reglas retiradas"** en `modelo_objetivo.py`, paralela a
  `RETIRADAS` / `CAMPOS_RETIRADOS`. La traza de `RG-02` y `RG-19` queda en este documento, en la
  entrada actualizada de `DECISIONES`, y en el hueco numérico que dejan al desaparecer — que es
  exactamente cómo ya conviven en el modelo los identificadores `RG-21` a `RG-33`: propuestos en
  `ESPEC-003`, bloqueados, y ausentes de `REGLAS` sin que eso rompa nada. Si en el futuro se decide
  que hace falta un registro formal, es una mejora aparte, no un requisito de este cambio.

## 6. Riesgos y dependencias

- **Dependencia dura de orden**: `scripts/validar_modelo.py` (`V-13`, línea 249) y
  `scripts/verificar_faseA.py` (`F-12`/`F-13`, líneas 307-386) tienen que actualizarse en el mismo
  cambio que `modelo_objetivo.py`, o el único gate objetivo del pipeline deja de dar 0 errores por
  una razón que no tiene que ver con el fondo del cambio. Está detallado con archivo y línea en §4.
- **Riesgo si no se aprueba a tiempo**: `ESTADO.md` dice que la Fase C —cablear las 21 reglas en el
  editor— está activa y es el frente que sigue. Si alguien cablea `RG-02` antes de que este
  documento se apruebe, va a repetir el error que ya reportó el editor. El costo de este documento
  es bajo precisamente porque interviene antes de ese paso caro.
- **No hay datos que migrar**: `MAN_Mantenimientos` tiene 0 filas en producción y en el volcado
  (§2.3). Retirar `Precision_GPS` no descarta ningún historial.
- **La prueba de aceptación va a tropezar con `RG-01`, no con este cambio**: para probar en el
  formulario real que la casilla y el motivo funcionan, hace falta guardar una fila de
  `MAN_Mantenimientos`, y eso exige que `RG-01` (`Valid_If`) resuelva a `TRUE` primero. Con
  coordenadas sintéticas derivadas del PK y radios de 0,05 km en 18 tipos, eso no está garantizado
  (§2.6). Quien escriba `PRUEBA-004` va a necesitar aislar la prueba de la casilla de la prueba del
  geofencing — por ejemplo, eligiendo o fabricando una fila `TEST` de `ACT_Activos` cuyo punto
  sintético caiga dentro del radio con margen, marcada para borrarse después, siguiendo la regla de
  higiene de datos de prueba del pipeline.
- **Riesgo de sincronización manual aceptado**: al conservar `PAR_Parametros.UMBRAL_GPS` sin que
  ninguna regla la lea, el número que ve el técnico en el manual puede desincronizarse del que el
  administrador ajuste en la hoja, porque nada los mantiene iguales automáticamente. Se acepta
  porque el precedente (`RADIO_GEOFENCING_KM`) ya vive con ese mismo riesgo desde antes de este
  documento, y la alternativa —retirar el parámetro— dejaría al manual citando una cifra que no
  existe en ningún sitio del sistema.
- **Lo que este cambio no puede arreglar solo**: aunque `CierreConExcepcion` quede bien marcable, la
  detección sigue dependiendo por completo de que el técnico sea honesto. No hay ninguna
  comprobación cruzada que note un cierre con GPS malo que nadie marcó. Ver el análisis completo en
  §3 y su reencuadre en la sección siguiente.

## 7. Supuestos adoptados

- **Se adopta la propuesta del encargo**: retirar `RG-02`/`Precision_GPS`, convertir
  `CierreConExcepcion` en una casilla editable por el técnico, dejar `RG-03` sin cambios. Es la
  única de las cuatro alternativas planteadas que no exige algo que AppSheet no ofrece hoy:
  - *Autoreportar la precisión leyéndola en pantalla* se descarta: pide al técnico transcribir un
    número que no se puede verificar después, y crea exactamente el mismo patrón que ya le costó
    caro a este proyecto con `CodigoQR` — un campo con apariencia de dato duro que en realidad nadie
    puede contrastar.
  - *Derivar la excepción de que `RG-01` rechace el cierre* se descarta: `RG-01` es un `Valid_If`,
    que bloquea el guardado del lado del cliente sin dejar ningún evento del que un `Bot` o una
    `App formula` puedan partir. No encontré, ni en `BASE_CONOCIMIENTO_APPSHEET.md` ni en la
    documentación citada en este mismo documento, ningún mecanismo de AppSheet que dispare una
    acción a partir de una validación rechazada. Lo declaro como ausencia verificada por lo que no
    aparece en las fuentes revisadas, no como una negación explícita de una fuente que lo descarte
    por nombre.
  - *Dejarlo muerto y documentado* se descarta: perpetuaría exactamente el patrón que `G-05` existe
    para cazar, y dejaría `RG-03` — bien escrita — pidiendo un motivo que nunca se activa.
- **Se adopta rechazar la "mejora" de volver editable `Coordenadas_Cierre_LatLong`**, por las
  razones de §3: reabre el agujero que `RG-20` cierra a propósito, en la columna que sostiene todo
  el geofencing.
- **Se adopta conservar `PAR_Parametros.UMBRAL_GPS`** como cifra de referencia sin lector, siguiendo
  el precedente ya existente de `RADIO_GEOFENCING_KM`, en vez de retirarla.
- **Se adopta no crear una estructura `REGLAS_RETIRADAS`** en `modelo_objetivo.py`. La traza basta
  con este documento, la entrada de `DECISIONES` y el hueco numérico, siguiendo el patrón que ya
  existe con `RG-21` a `RG-33`.
- **Se adopta que `RG-13` queda fuera de alcance** de este `ESPEC`. No se cablea, no se resuelve su
  `tipo` inexistente. Si se retoma el escaneo por QR, necesita su propia especificación.
- **Se adopta que lo que se pierde es menor de lo que parece**, porque nunca hubo nada que perder en
  la práctica: la cadena automática jamás se disparó sobre una fila real (`MAN_Mantenimientos` tiene
  cero filas en producción). Lo que cambia es que, de aquí en adelante, la única defensa contra un
  cierre con mala señal es que el técnico lo diga. Eso no es nuevo: ya era así de facto. Lo que sí es
  nuevo, y hay que decirlo sin suavizarlo, es que **ahora existe un camino real para que lo diga**, y
  antes no lo había.
