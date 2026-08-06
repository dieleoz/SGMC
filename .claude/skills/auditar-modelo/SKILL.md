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

Hay dos fuentes y no coinciden:

| Fuente | Qué es | Cómo se lee |
|---|---|---|
| Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc` | **El que corre la app.** Manda ante discrepancia | Conector de Google Drive, `read_file_content` |
| `BD/Modelo de Datos (2).xlsx` | Registro local paralelo | `openpyxl` |

Ninguno es superconjunto del otro. Nunca copies uno sobre el otro sin decisión explícita: se
destruye trabajo.

## Procedimiento

### 1. Lee producción primero

Con el conector de Google Drive, `read_file_content` sobre el `fileId` de arriba. Si el conector
no está disponible, dilo y detente: **no sustituyas producción por el Excel local sin advertirlo**.

Revisa de paso `get_file_metadata`: si `modifiedTime` es reciente, alguien acaba de tocar el
backend y cualquier hallazgo previo puede haber caducado.

### 2. Lee el Excel local

```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook(r'BD/Modelo de Datos (2).xlsx', read_only=True, data_only=True)
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

- `MAN_Mantenimientos`: ¿tiene `Coordenadas_Cierre` y `Precision_GPS`? En producción no las tiene,
  y sin ellas RF-011 y RF-012 no pueden ni configurarse.
- `ACT_Activos.Ubicacion`: ¿cuántas coordenadas **distintas** hay? Si es una sola, el geofencing es
  inoperante por mucho que la fórmula esté bien.
- `TIP_TiposActivo.FormularioID`: ¿está poblado en los 18 tipos? Sin él no hay checklist dinámico.
- `SedeID`: ¿se intersecan los valores de `USR_Usuarios` y los de `ACT_Activos`? Si no, el Security
  Filter deja a cada técnico con cero activos.
- `FRM_Preguntas`: ¿cuántos de los 18 formularios tienen banco de preguntas? Las hojas planas
  `FRM_SOS`, `FRM_CCTV` y `FRM_PMVF` son una arquitectura paralela y **no** alimentan el motor.
- Integridad referencial: `CHK.OTID` y `MAN.OTID` contra las claves reales de `OT_OrdenesTrabajo`,
  que son `Numero_OT` con valores tipo `OT-0001`, no `OTID`.
- Tablas vacías: `MAN_Mantenimientos`, `FOT_Fotografias`, `FIR_Firmas` y `GPS`. Mientras sigan sin
  registros, el ciclo de mantenimiento nunca se ha ejecutado y nada está probado.
- Datos de prueba sin limpiar: nombres donde deberían ir identificadores, `NOW()` como texto.

## Lo que la lectura de datos NO puede decirte

Ni el Sheets ni la API de AppSheet exponen la **configuración**: expresiones `Valid_If`, Security
Filters, `IsPartOf`, tipos de columna ni bots. Para verificar eso hay que entrar al editor de
AppSheet por navegador. Si un hallazgo depende de la configuración, márcalo como **no verificado**
en lugar de suponerlo.

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

```
https://www.appsheet.com/Template/AppDef?appName=SGMC-886843353
```

La ruta con `appId` devuelve 404; usa `appName`. Antes de tocar el editor, confirma que exista una
copia de respaldo de la aplicación: *Regenerate Structure* advierte explícitamente que no se puede
deshacer.

## Al terminar

Actualiza `docs/AUDITORIA_PLAN_Y_ROADMAP.md` con lo encontrado, y `CLAUDE.md` si cambia el estado
real. Deja constancia del comando y de la salida con que cerraste cada hallazgo.
