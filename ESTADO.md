# Dónde vamos y qué falta

**Lea esto primero.** Es el mapa de todo lo demás.

**Punto de partida fijado el 2026-08-10.** El repositorio se limpió ese día: se retiró todo lo que
describía aplicaciones y hojas superadas. Lo que queda describe **un solo sistema**.

## El sistema

```
Aplicación   SISGA_-323965761-26-08-10
             https://www.appsheet.com/template/appdef?appId=d180a1b5-19ca-448e-a44c-f985396dce12

Datos        Modelo_Datos_10082026   ·   Hoja de cálculo de Google
             https://docs.google.com/spreadsheets/d/1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0
```

> **Si un enlace no es uno de esos dos, no es este sistema.** Entre el 6 y el 10 de agosto hubo
> cinco aplicaciones y tres hojas. Las superadas están en `scripts/sistema.py`, nombradas y con el
> motivo por el que dejaron de serlo, para poder reconocerlas y descartarlas de un vistazo.
>
> **Nada de lo retirado se perdió.** La etiqueta `antes-de-la-limpieza-2026-08-10` devuelve el
> repositorio entero tal como estaba:
>
> ```bash
> git checkout antes-de-la-limpieza-2026-08-10
> ```

## En una frase

**La hoja de datos está terminada y verificada. La aplicación tiene las 28 tablas dadas de alta y
nada más: falta cablearla entera.**

---

## 1. Qué está hecho

### La hoja de datos

`Modelo_Datos_10082026` sale generada del modelo, no heredada de nada.

```
28 pestañas de datos más _LEEME · 205 columnas · ninguna de sobra
ACT_Activos        368 activos, un solo inventario, códigos SOS-001 / SWIT-001
TIP_TiposActivo     27 tipos, con radio de cierre poblado en los 27
FRM_Formularios     27 formularios, uno por tipo
FRM_Preguntas      333 preguntas, los 27 checklists con contenido
LST_ValoresLista   108 valores, ningún desplegable vacío
Sin registros de prueba · FASE A CERRADA, 52 comprobaciones
```

Se rehace entera con un comando y **se reproduce**: dos ejecuciones seguidas dan las 29 pestañas
idénticas, celda por celda.

```bash
python scripts/generar_plantilla.py
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

### El modelo

`scripts/modelo_objetivo.py` es la fuente única: **28 tablas, 205 columnas, 39 referencias, 20
reglas.** De ahí se generan el diccionario, el manual de despliegue, la guía funcional y la lista de
reposición de expresiones. Nada de eso se escribe a mano.

### La aplicación

**Las 28 tablas dadas de alta sobre la hoja limpia**, y el 2026-08-10 se empezó a poner al día su
esquema tras cambiar la hoja. `SED_Sedes` ya tiene sus 10 columnas regeneradas.

> **Subir el Excel arregla la hoja, no la aplicación.** Son dos sitios distintos. El Excel fija
> columnas y datos; **el tipo de cada columna, la clave y las referencias viven en el esquema de
> AppSheet**, que se infiere de los datos y hay que corregir a mano.
>
> Lo que se ve al abrir el editor, en una sola tabla: `SedeID` tipada `Number` cuando el modelo dice
> `Text`, `Ubicacion` como `Text` cuando es una coordenada, `UnidadFuncionalID` como `Number` cuando
> es una referencia, y **`TramoINVIAS` como `Number` porque el único valor cargado es `5607`** — el
> día que alguien escriba `55CN03` no cabrá.

---

## 2. Qué falta

**La aplicación se reconstruyó desde cero el 2026-08-10, así que el cableado de la anterior no
sirve: se repone entero.** No es una lista de retoques, es el procedimiento completo.

| # | Qué | Dónde está escrito |
|---|---|---|
| 1 | **Las 39 referencias**, con `IsPartOf` en las cuatro que lo llevan | [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md), ficha por tabla |
| 2 | **Las 21 reglas**: geofencing, umbral de GPS, `Editable_If`, los bots | [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](docs/sdd/RECONSTRUCCION_EXPRESIONES.md), expresión completa |
| 3 | **Los dos filtros de seguridad**: activos por unidad funcional, órdenes por técnico | Ídem |
| 4 | **Las cuatro marcas de tiempo** como `ChangeTimestamp` del servidor | Ídem |
| 5 | **Retirar `Deletes`** en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` | Ídem |
| 6 | **Correr `PRUEBA-003`** | [`docs/sdd/PRUEBA-003-despliegue.md`](docs/sdd/PRUEBA-003-despliegue.md) |

**El orden del 5 no es opcional.** Se marca `IsPartOf` en cuatro referencias, y eso es borrado en
cascada: borrar un mantenimiento se lleva sus fotografías, su firma y su checklist. Solo es seguro
porque el mantenimiento nunca se borra, y eso es lo que hace quitar `Deletes`.

**Antes de nada, dos comprobaciones que solo se pueden hacer ahora**, recién dadas de alta las
tablas, y que después salen carísimas:

- **Ninguna clave compuesta.** AppSheet combina dos columnas cuando no encuentra una única. Contra
  una clave compuesta **no resuelve ninguna referencia** y falla el bloque entero sin decir por qué.
  Deben ser 28 claves simples, todas `Text`.
- **Ninguna tabla dos veces.** Es el fallo propio de dar de alta una por una: aparece
  `OT_OrdenesTrabajo_1` o `Copy of…`. Con dos tablas sobre la misma pestaña **las referencias se
  reparten y la mitad de las filas parece desaparecer, sin error**.

Y una de cuenta: **28 tablas, no 29.** `_LEEME` es la pestaña de instrucciones y no se da de alta.

### Lo que no desbloquea ningún cableado

**Las coordenadas no son reales.** Ninguno de los 368 activos tiene su posición levantada en campo:
están calculadas sobre el trazado del corredor. Hasta cargarlas, la comprobación de distancia al
cerrar **no significa nada**. Es la decisión D-01 y es el bloqueo del piloto.

**Y 288 de las 333 preguntas son borrador.** Llevan `[BORRADOR: validar con operacion]` en su ayuda.
Buscar esa marca en la hoja dice exactamente qué queda por revisar, y el día que no aparezca
ninguna, el banco de preguntas está cerrado. Las 45 restantes —SOS, CCTV y PMVF— ya estaban
acordadas.

---

## 3. El entregable de datos

**`BD/Modelo_Datos_PLANTILLA.xlsx`** es lo que recibe el funcional, y es el mismo archivo que está
publicado como `Modelo_Datos_10082026`.

**Viene autocompletado a propósito:** cada columna trae un valor con el formato correcto para que se
corrija en vez de adivinarlo. La primera pestaña, `_LEEME`, dice en qué formato va cada cosa —la
coordenada, la fecha, el decimal— y qué columnas hay que completar.

**El principio es de operación: entregamos la estructura; el dato real lo pone quien lo conoce.**

### Lo que sí está anclado en fuente

**Las cuatro unidades funcionales son las del contrato**, Apéndice Técnico 1, Tabla 3:

```
UF1  Sisga - Machetá - Manta - Guateque                      50,01 km
UF2  Guateque - Garagoa - Macanal                            22,00 km
UF3  Macanal - Santa María                                   17,80 km
UF4  Santa María - Cachipay - San Luis de Gaceno - Aguaclara 47,36 km
```

**No son cuartos iguales**, que es como estaban repartidas hasta el 2026-08-10. Al corregirlo
resultó que **113 de los 368 activos estaban en la unidad funcional equivocada**. Importa porque
`RG-04` filtra por UF: cada técnico habría visto un conjunto de activos que no es el suyo, y nada lo
habría detectado, porque la referencia resolvía.

> **Y el contrato prueba una carencia del modelo que hasta ahora era una sospecha: un PR no
> identifica un punto.** El corredor **atraviesa tres rutas de INVÍAS**, no una — `55CN03` del
> PR0+0+000 al PR6+194, `5607` del PR7+146 al PR46+080 y `5608` del PR0+000 al PR92+048.
>
> **Hay dos puntos distintos llamados «PR 0+000»**: el arranque en El Sisga sobre la `55CN03` y
> Guateque sobre la `5608`, separados por unos 50 km. Un técnico enviado al «PR 0+000» no sabe a
> cuál de los dos.
>
> Lo resuelve declarar la ruta, o el **PK**, que es lineal y continuo en todo el corredor. Están
> declaradas como columnas propuestas `ACT_Activos.PK` y `ACT_Activos.TramoINVIAS`, sin implementar:
> es cambio de modelo y pasa por especificación.

### Quince túneles, y un tercio de la UF3 bajo tierra

El contrato los lista con su PR de entrada y salida —tablas 13, 19 y 20—. Son **7.224 metros**, y
no están repartidos: **la UF3 tiene once túneles que suman 6.000 de sus 17.800 metros**. Un tercio
de ese tramo va bajo tierra, con `El Polvorín` de 1.649 m como el más largo.

> **Dentro de un túnel el GPS no fija posición, y `RG-01` comprueba la distancia al activo al
> cerrar.** Todo equipo dentro de un túnel **falla esa comprobación siempre**, por diseño y no por
> avería.
>
> Hoy eso se manejaría como excepción caso por caso, y el supervisor vería a un técnico acumulando
> cierres con excepción **sin saber que es el túnel y no el técnico**. Está declarada la tabla
> `TUN_Tuneles` en `PROPUESTAS`, sin especificar.

Y el contrato apunta otra cosa: **la ventilación de los túneles figura como `N/A`** y lo único que
exige es iluminación. Si no hay ventilación ni detección de incendios, esos túneles no aportan los
activos que cabría esperar — pero **falta leer la página 27**, donde continúa la tabla de los cinco
últimos.

**Y el contrato da el dato que a `SED_Sedes` le faltaba:** el peaje de Machetá está en el
**PR27+240 de la Ruta 5607**, cobro bidireccional, unidad funcional 1. El de San Luis de Gaceno
aparece en el mapa del contrato marcado como **peaje nuevo**, sin fila de tabla ni abscisa: está
proyectado, no construido. `SED_Sedes` los lista como si los dos existieran.

### Por qué el catálogo tiene 27 tipos y el Plan Maestro 18 familias

**No son la misma lista, y que los dos números fueran 18 lo escondía.** `TIP_TiposActivo` decide
**qué checklist ve el técnico**; las familias del Plan Maestro son **cómo operación cuenta los
equipos**. Nueve familias no tenían tipo propio y colgaban del de otra cosa: la impresora heredaba
el checklist del NAS, el portátil el del servidor, el carril de peaje el de la báscula.

Eran **78 activos de 355 con el checklist equivocado**, y ningún verificador lo veía porque
`TipoActivoID` resolvía contra una fila que existe. `scripts/catalogo_tipos.py` lo cierra como
fuente única, con `comprobar()`, que falla si dos familias comparten tipo o si un tipo se queda sin
radio.

---

## 4. Qué leer, según lo que necesite

| Si necesita | Lea |
|---|---|
| **Saber qué le toca a usted** | [`docs/INDICACIONES_POR_ROL.md`](docs/INDICACIONES_POR_ROL.md) |
| **Construir la aplicación** | [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md) — diez pasos y una ficha por tabla, columna por columna |
| **La expresión exacta de una regla** | [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) — las 21 sin cortar |
| **Probar que funciona** | [`docs/sdd/PRUEBA-003-despliegue.md`](docs/sdd/PRUEBA-003-despliegue.md) |
| **Qué hace el sistema y para quién** | [`docs/FUNCIONAL_SGMC.md`](docs/FUNCIONAL_SGMC.md) |
| **La estructura de datos real** | [`docs/bd.md`](docs/bd.md), generado del archivo |
| **Cómo se comporta AppSheet, con la cita oficial** | [`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) |
| **Con qué supuestos se construye** | [`docs/ALCANCE_Y_SUPUESTOS_SGMC.md`](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) |
| **El orden de implementación** | [`docs/ROADMAP.md`](docs/ROADMAP.md) |

---

## 5. Los cuatro verificadores

Ninguno sustituye a otro, y **lo único que ha funcionado en este proyecto es lo mecánico**.

```bash
python scripts/validar_modelo.py        # el modelo consigo mismo. Gate del pipeline
python scripts/verificar_faseA.py       # el modelo contra la hoja descargada
python scripts/verificar_documentos.py  # la prosa contra el modelo
python scripts/verificar_enlaces.py     # que todo enlace entre documentos resuelve
```

---

## 6. Lo que costó la semana, para no repetirlo

**AppSheet ignora las pestañas ocultas.** Ocho catálogos ocultos hacían que cargara 24 tablas de 32,
sin un solo mensaje, mientras nuestra verificación decía que todo estaba bien porque `openpyxl` sí
las lee. Lo caza `F-18`.

**`Regenerate` fusiona, no reemplaza.** Conserva las columnas viejas a propósito. Con un esquema muy
divergente impide converger, y por eso se reconstruyó en vez de reparar.

**Una referencia que resuelve puede apuntar a lo que no es.** Pasó dos veces: el inventario
sintético reescribió 34 activos reales, y nueve familias vieron el checklist de otro equipo. Las dos
veces la comprobación de huérfanos daba verde. Los verificadores contestan «apunta a algo», nunca
«apunta a lo correcto».

**Una instrucción que exige criterio se ejecuta mal.** «Oculte las columnas retiradas» produjo que
se cableara una trampa como referencia y que alguien se inventara los valores de un `Enum`. Por eso
los documentos llevan la lista completa, generada, sin nada que deducir.
