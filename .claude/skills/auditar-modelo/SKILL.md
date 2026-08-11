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
| El volcado que declare ese mismo script como `VOLCADO` (hoy, `BD/Modelo_Datos_PLANTILLA.xlsx`) | Registro local | `openpyxl` |

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

### 2. Lee el volcado local

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook(r'BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
for n in wb.sheetnames:
    ws = wb[n]
    hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1)) if c.value]
    print(f'{n:22s} cols={len(hdr):2d} filas~{ws.max_row-1}')
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
- Integridad referencial: en el modelo vigente `OT_OrdenesTrabajo` tiene clave `OTID` (Text), y
  `CHK_Checklists` no lleva `OTID` sino `MantenimientoID`, referencia a `MAN_Mantenimientos`.
  Vuelca `scripts/modelo_objetivo.py` antes de asumir cuál es la clave de cada tabla: ya cambió más
  de una vez en este proyecto.
- Tablas vacías: `MAN_Mantenimientos`, `FOT_Fotografias` y `FIR_Firmas`. Mientras sigan sin
  registros, el ciclo de mantenimiento nunca se ha ejecutado y nada está probado.
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

Y hay dos reglas que **no se pueden poner hoy**, así que no las reportes como pendientes de
teclear: `RG-02` usa una función inexistente y `RG-10`/`RG-12` crearían órdenes sin clave. Están en
`ESPEC-004` y `ESPEC-005`, en el pipeline.

Antes de reportar una regla como puesta, corre `python scripts/verificar_datos.py`: su comprobación
**G-05** cruza el alcance real de las 21 reglas contra los datos y dice cuáles leen una columna
vacía. No cubre los otros dos casos —el tipo vive en el editor, la función es un hecho de la
plataforma—, así que esos se miran.

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
Deja constancia del comando y de la salida con que cerraste cada hallazgo.

El dictamen del 2026-08-06 que antes se actualizaba aquí, y sus hallazgos `B-01` a `B-14`, salieron
del árbol de trabajo en la limpieza del 2026-08-10. Se recuperan con
`git checkout antes-de-la-limpieza-2026-08-10`; no los cites como vigentes sin comprobarlos de
nuevo contra el modelo de hoy, que ya no es el que auditaban.
