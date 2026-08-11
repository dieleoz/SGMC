---
name: auditar-modelo
description: Audita el modelo de datos del SGMC leyendo el backend de producción en Google Sheets y el Excel local, y reporta divergencias y bloqueantes. Úsala antes de afirmar cualquier cosa sobre el estado del sistema, antes de configurar algo en AppSheet, y cuando alguien reporte una subsanación como cerrada.
---

# Auditar el modelo de datos del SGMC

Este proyecto arrastra dos problemas crónicos: subsanaciones reportadas como cerradas que no lo
estaban, y **dos modelos de datos que divergen**. Esta skill existe para no volver a caer en
ninguno de los dos.

## Regla que gobierna todo

**No declares nada conforme por reporte. Verifícalo contra el archivo, y di contra cuál.**

Hay dos fuentes y pueden no coincidir:

| Fuente | Qué es | Cómo se lee |
|---|---|---|
| El Google Sheets que declare `python scripts/sistema.py` como `HOJA_ID` | **El que corre la app.** Manda ante discrepancia | Conector de Google Drive, `read_file_content` |
| El volcado que declare ese mismo script como `VOLCADO` (hoy, `BD/Modelo_Datos_PLANTILLA.xlsx`) | Registro local. **Ciego a ocho tablas** — ver abajo | `openpyxl` |
| La aplicación en vivo | La única que ve las filas de movimiento | `python scripts/instantanea.py` |

### El volcado local es CIEGO a las ocho tablas de movimiento, y no lo dice al abrirlo

**`generar_plantilla.py` las vacía a propósito** cada vez que corre: son registros de prueba y la
plantilla es lo que recibe el funcional. Están declaradas en `scripts/lectura_de_vuelta.py` como
`VOLCADO_CIEGO_A`:

```
OT_OrdenesTrabajo · MAN_Mantenimientos · CHK_Checklists · CHD_ChecklistDetalle
FOT_Fotografias   · FIR_Firmas         · NOV_Novedades  · PLA_PlanMantenimiento
```

**Nunca uses el volcado para mirar datos de movimiento.** Una fila creada en la aplicación —un
fixture, una orden real— **nunca llega a ese archivo**, así que ahí saldrán las ocho vacías **aunque
la aplicación tenga filas**. Reportar «`MAN_Mantenimientos` está vacía, luego el ciclo nunca se
ejecutó» leyendo el volcado es un hallazgo **falso por construcción**, y ni `verificar_faseA.py` ni
`verificar_datos.py` lo desmienten: los dos leen ese mismo archivo por defecto.

**Para esas ocho tablas hay exactamente dos fuentes válidas:** el Sheets de producción por el
conector, o `python scripts/instantanea.py`, que lee por API. El volcado sirve para **estructura y
catálogos**, no para población de movimiento. Si informas de una de las ocho, di con cuál de las dos
la miraste.

**No copies el `fileId` ni la ruta de una auditoría anterior.** Este sistema se reconstruyó tres
veces en cuatro días, y `scripts/sistema.py` es el único sitio que no envejece: lista también las
aplicaciones y hojas superadas, con el motivo, para reconocerlas si aparecen citadas en otro
documento.

Mientras la hoja publicada sea exactamente la plantilla generada por `scripts/generar_plantilla.py`
son el mismo archivo. Dejan de serlo en cuanto operación empiece a completar el Sheets a mano, y
ahí es donde esta auditoría vuelve a tener trabajo real que hacer. Nunca copies uno sobre el otro
sin decisión explícita: se destruye trabajo.

## Procedimiento

### 1. Lee producción primero

Con el conector de Google Drive, `read_file_content` sobre el `HOJA_ID` de `scripts/sistema.py`. Si
el conector no está disponible, dilo y detente: **no sustituyas producción por el volcado local sin
advertirlo**.

Revisa de paso `get_file_metadata`: si `modifiedTime` es reciente, alguien acaba de tocar el
backend y cualquier hallazgo previo puede haber caducado.

### 2. Lee el volcado local — para estructura, no para movimiento

El recuento de filas que imprime este comando **no significa nada en las ocho tablas de
`VOLCADO_CIEGO_A`**, que salen marcadas para que no se te olvide:

```bash
python -c "
import sys, openpyxl
sys.path.insert(0, 'scripts')
from lectura_de_vuelta import VOLCADO_CIEGO_A
wb = openpyxl.load_workbook(r'BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
for n in wb.sheetnames:
    ws = wb[n]
    hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1)) if c.value]
    ciega = '  <-- CIEGA: el volcado la vacia por diseno, mira instantanea.py' if n in VOLCADO_CIEGO_A else ''
    print(f'{n:22s} cols={len(hdr):2d} filas~{ws.max_row-1}{ciega}')
"
```

### 3. Contrasta y reporta

Para cada hallazgo, indica siempre **en cuál de las dos fuentes lo verificaste**. Un hallazgo sin
esa marca no sirve.

## Qué comprobar siempre

Distingue **estructura** de **población**: que exista la columna no significa que tenga datos, y
que la tabla exista no significa que el flujo se haya ejercitado.

- `MAN_Mantenimientos`: ¿tiene `Coordenadas_Cierre_LatLong` y `Precision_GPS`? Verificado el 2026-08-10
  contra `scripts/modelo_objetivo.py`: hoy sí están, en las 28 tablas del modelo y en la hoja
  generada de él. Si una hoja que estés auditando no las trae, es la hoja la que quedó atrás, no la
  regla la que cambió.
- `ACT_Activos.Ubicacion_LatLong`: ¿cuántas coordenadas **distintas** hay? Si es una sola, el geofencing es
  inoperante por mucho que la fórmula esté bien. En `BD/Modelo_Datos_PLANTILLA.xlsx`, 34 de los 368
  activos comparten la coordenada `4.728512, -74.114531` (Bogotá): son de fixture, no del terreno.
- `TIP_TiposActivo.FormularioID`: ¿está poblado en **todas** las filas? Sin él no hay checklist
  dinámico. **Cuenta las filas del archivo que estés auditando, no des por hecho cuántas son:** el
  catálogo vigente son 27 tipos (`scripts/catalogo_tipos.py`); si encuentras 18, es una hoja
  superada, no la de hoy.
- Security Filter: ¿se intersecan los `UnidadFuncionalID` de `ACT_Activos` con los que
  `ASG_AsignacionZona` asigna a cada `UsuarioID`? Si no, el filtro deja a ese técnico con cero
  activos. **No lo compruebes por `SedeID`**: esa columna vive en `USR_Usuarios` —dónde trabaja la
  persona— y `ACT_Activos` no la tiene; es exactamente la confusión que `CLAUDE.md` §6 (RG-04)
  señala como la que dejó usuarios y activos en conjuntos disjuntos.
- `FRM_Preguntas`: ¿cuántas filas de `FRM_Formularios` tienen banco de preguntas, sobre el total de
  esa misma hoja? El catálogo vigente son 27 formularios, uno por tipo, con las 333 preguntas
  cargadas — 45 acordadas (SOS, CCTV, PMVF) y el resto con la marca `[BORRADOR: validar con
  operacion]` de `scripts/banco_preguntas.py`. Buscar esa marca dice qué queda por revisar.
- Integridad referencial: `CHK_Checklists` **no lleva `OTID`** sino `MantenimientoID`, referencia a
  `MAN_Mantenimientos`. Y desde `ESPEC-005`, **`OT_OrdenesTrabajo.OTID` y
  `PLA_PlanMantenimiento.PlanID` ya no son claves legibles**: las genera `UNIQUEID()`, así que
  `CLAVE_LEGIBLE` son **20** tablas y `CLAVE_GENERADA` **8**. Comparar un `Ref` a una de esas ocho
  contra un literal de texto es **siempre** un error. Vuelca `scripts/modelo_objetivo.py` antes de
  asumir cuál es la clave de cada tabla: ya cambió más de una vez en este proyecto.
- **Y eso te dejó dos comprobaciones menos, que es lo que hay que saber al leer el verde.** `F-11` de
  `verificar_faseA.py` —la que comprueba que las listas de claves dicen la verdad sobre la hoja—
  **exime a `CLAVE_GENERADA` a propósito**, así que desde `ESPEC-005` **ya no mira
  `OT_OrdenesTrabajo` ni `PLA_PlanMantenimiento`**. Antes sí las recorría, y sobre la plantilla —que
  las trae vacías— emitía su aviso de «está vacía en la hoja: no se puede decidir». Hoy ni eso: pasa
  de largo en silencio. **Es correcto** —sus claves serán aleatorias en cuanto la aplicación cree la
  primera fila, y meterlas en `CLAVE_LEGIBLE` apagaría `V-17`—, pero **no lo reportes como que `F-11`
  las aprobó**: no las miró. Se comprueba de un vistazo:

  ```bash
  python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,CLAVE_GENERADA;print('F-11 evalua',len([t for t in MODELO if t not in CLAVE_GENERADA]),'tablas y exime',len(CLAVE_GENERADA),'|',sorted(CLAVE_GENERADA))"
  ```

  La forma es la de `CLAUDE.md` §7.15: **una comprobación que deja de dispararse pasa en verde por no
  ejercitarse**, y el verde se lee igual. Si vas a decir que la clave de esas dos está bien, la miras
  en el editor.
- Tablas de movimiento sin registros: **compruébalo por API o en el Sheets, nunca en el volcado.**
  Las ocho de `VOLCADO_CIEGO_A` salen vacías ahí siempre. Si lo confirmas contra la fuente buena y
  siguen sin filas, entonces sí: el ciclo de mantenimiento nunca se ha ejecutado y nada está
  probado.
- **Y si están vacías, dilo con la consecuencia que tiene:** una tabla vacía es el último momento en
  que un cambio de tipo o de clave **no arrastra ni una fila**. `MAN_Mantenimientos.OTID` está
  declarada `Ref` en el modelo y **sigue `Text` en el editor** —conversión pendiente de
  `ESPEC-003`—, y mientras sea `Text` **no hay referencia real**: toda la cadena
  `[OTID].[ActivoID].[…]` del geofencing no existe. **El primer fixture cierra esa ventana** —para
  las **ocho**, no solo para las tres que se nombran al hablar del geofencing— y no vuelve a abrirse:
  son transaccionales. Lo que hay que hacer dentro de ella está reunido y generado en
  `docs/ENCARGO_VENTANA.md`; la regla que lo gobierna, en `CLAUDE.md` §7.17. **Si en una auditoría
  encuentras las ocho todavía vacías, eso no es un pendiente: es el activo que queda por gastar, y se
  reporta como tal.**
- Datos de prueba sin limpiar: nombres donde deberían ir identificadores, `NOW()` como texto.

## Lo que la lectura de datos NO puede decirte

Ni el Sheets ni la API de AppSheet exponen la **configuración**: expresiones `Valid_If`, Security
Filters, `IsPartOf`, tipos de columna ni bots. Para verificar eso hay que entrar al editor de
AppSheet por navegador. Si un hallazgo depende de la configuración, márcalo como **no verificado**
en lugar de suponerlo.

**Con una excepción, y conviene conocer sus límites: las referencias sí se pueden leer, de lado.**
Al definir una `Ref`, AppSheet crea en la tabla **destino** una columna virtual `Related <Origen>`
—o `Related <Origen> By <Columna>` si hay varias entre el mismo par—, y esos nombres **sí viajan en
las filas**. `python scripts/auditar_cableado.py` reconstruye el grafo con eso.

Tres límites que hay que respetar al citarlo:

- **Sin ` By `, la columna no está probada.** AppSheet solo nombra la tabla, y atribuir la columna
  exige preguntárselo al modelo, que es lo que se quería verificar. El script las llama
  *compatibles no atribuidas* y **no debes sumarlas a las verificadas**: esa suma inflada ya se
  publicó una vez.
- **Si la tabla destino está vacía, no se puede decir nada.** No están bien ni mal. Confundir «no lo
  puedo ver» con «está bien» es como se llegó al informe de «39/39 asignadas» con cinco rotas.
- **El método es más fuerte cuando el cableado está mal.** Varias referencias al mismo destino
  obligan a desambiguar con ` By `; cuando todo está bien, deja de nombrar la columna. Es decir:
  **no sirve para confirmar una corrección recién hecha.** Eso se mira en el editor.

**Lección del 2026-08-10, y es la que más veces se ha repetido: una regla puede estar puesta, bien
escrita, sin dar un solo error, y no hacer nada.** Tres casos el mismo día, cada uno por un motivo
distinto: el **tipo** de su columna (`RG-03`, `Text` comparado contra el booleano `TRUE`), el **dato**
de la columna que lee (`RG-06`, con `GeneraAlerta` vacía en los cuatro estados) y una **función que
no existe** (`RG-02`, `USERLOCATIONACCURACY()`).

**Tres reglas no se pueden poner hoy, y no son las mismas de antes.** `RG-02`, `RG-19` y `RG-03`
dependen de `USERLOCATIONACCURACY()`, que **no existe en AppSheet**: espera a `ESPEC-004`, que sigue
**BLOQUEADA** —segunda pasada, quince hallazgos—. **`RG-10` y `RG-12` ya no están bloqueadas**:
`ESPEC-005` está aplicada al modelo y `OTID`/`PlanID` se generan solos. No las reportes como
esperando a nadie.

**De `ESPEC-005` queda la mitad que vive en el editor**, y es lo que hay que ir a mirar: las dos
**columnas virtuales** `Etiqueta` de `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` (`RG-35`,
`RG-36`), con `Show?` activo y `Label` marcado. **No las busques en la hoja ni en `MODELO`**: una
columna virtual la calcula AppSheet y no se guarda en el Sheets, así que vive solo en `REGLAS` y en
`inferencia.ETIQUETA_VIRTUAL`. Que no aparezca en el volcado **no es un hallazgo**.

Antes de reportar una regla como puesta, corre `python scripts/verificar_datos.py`: su comprobación
**G-05** cruza el alcance real de las **23** reglas contra los datos y dice cuáles leen una columna
vacía, y **G-04** avisa de las tablas tipadas a ciegas. No cubren los otros dos casos —el tipo vive
en el editor, la función es un hecho de la plataforma—, así que esos se miran.

**El alcance de una regla se pregunta a `python scripts/alcance_reglas.py`, no al nombre de la
columna.** Atribuir por nombre suelto daba 94 columnas «con regla» donde hay **39 de 211**: como
`[Activo]` está en `RG-04` y en `RG-16`, las 23 columnas llamadas `Activo` cargaban con las dos.

**Y antes de decir que algo «está sin poner», comprueba que alguien pueda verlo.** `python
scripts/lectura_de_vuelta.py` dice, por clase de cambio, quién lo lee de vuelta: **`referencias`,
`datos` y `estructura` tienen comando; `tipos`, `expresiones`, `permisos` y `etiqueta` no tiene
nadie**. Un hallazgo sobre una de esas cuatro solo se cierra **copiando literalmente lo que ves en
el editor** — «coincide» no es evidencia. Y `python scripts/navegacion_editor.py` dice dónde mirar:
el nombre de la regla **no es** el del control (`Required_If` es `Require?`, y no es una casilla).

**Lección del 2026-08-06.** Que dos tablas compartan un nombre de columna no significa que estén
relacionadas. En este proyecto, la cadena Activo → Orden → Mantenimiento existía en el diccionario
de datos, en los diagramas y en todos los documentos, pero en la aplicación `OTID` estaba tipada
como `Text`: no había ninguna referencia real. **Una relación solo existe si la columna es de tipo
`Ref` en AppSheet.** Verifícalo en el editor antes de escribir cualquier expresión que
desreferencie con la notación `[Columna].[Otra]`.

Atajo para comprobar una expresión sin romper nada: ábrela en el Asistente de Expresiones del
editor y lee el error. Valida contra el esquema real y es la forma más rápida de descubrir que una
relación que dabas por hecha no existe.

## Cómo entrar al editor

La URL vigente es la que `python scripts/sistema.py` declara como `APP_URL` — usa el `appId`, no un
`appName` copiado de una aplicación anterior: cada reconstrucción cambia los dos. Antes de tocar el
editor, confirma que exista una copia de respaldo de la aplicación: *Regenerate Structure* advierte
explícitamente que no se puede deshacer.

## Al terminar

Actualiza `ESTADO.md` con lo encontrado, y `CLAUDE.md` solo si cambia una **regla**, no el estado.
Deja constancia del comando y de la salida con que cerraste cada hallazgo — **y de si el hallazgo
salió del volcado o de la fuente en vivo**, porque en las ocho tablas de movimiento eso decide si el
hallazgo existe.

Y deja los cuatro en verde antes de cerrar:

```bash
python scripts/validar_modelo.py
python scripts/verificar_documentos.py
python scripts/verificar_enlaces.py
python scripts/verificar_datos.py
```

El dictamen del 2026-08-06 que antes se actualizaba aquí, y sus hallazgos `B-01` a `B-14`, salieron
del árbol de trabajo en la limpieza del 2026-08-10. Se recuperan con
`git checkout antes-de-la-limpieza-2026-08-10`; no los cites como vigentes sin comprobarlos de
nuevo contra el modelo de hoy, que ya no es el que auditaban.
