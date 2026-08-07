# ACTA-003 — Cierre de la hoja

**La Fase A queda cerrada de forma definitiva el 7 de agosto de 2026.** La hoja no se vuelve a tocar
desde Google Sheets: todo lo que sigue ocurre dentro del editor de AppSheet.

| | |
|---|---|
| Archivo verificado | `BD/Modelo de Datos (9).xlsx` |
| Resultado | **`FASE A CERRADA`** — 0 fallos |
| Cubre | La pestaña `PAR_Parametros` y las tres precondiciones de datos de `ESPEC-002` §5.1 |

## 1. Lo aplicado, verificado contra el archivo

| Cambio | Comprobación |
|---|---|
| `PAR_Parametros` | 3 filas exactas, encabezados correctos, **ninguna fila inventada**. `Valor` guardado como número (`float`), no como texto |
| `OT_OrdenesTrabajo.Activo` | `TRUE` en las 6 filas |
| `EST_Activo.Activo` | `TRUE` en las 4 filas |
| `ACT_Activos` fila 34 | `Activo = FALSE`, y las otras 33 siguen en `TRUE` |
| `MAN_Mantenimientos.TEST-MTTO-002` | `Precision_GPS = 45`, **sin tocar** |

Ese último era el punto más frágil del encargo: había un `65` en documentos que yo había escrito y
nunca aplicado, y era exactamente el tipo de cosa que un asistente «corrige» por iniciativa propia.
Llegó intacto.

## 2. Dos alucinaciones, y las dos se detuvieron donde debían

**El asistente de la hoja inventó el contenido de `PAR_Parametros`** en el primer intento: creó una
pestaña de configuración genérica con parámetros que nadie pidió —`MaxDiasPendiente`, un correo de
administración— y **omitió `Valor`, `Unidad` y `Descripcion`**, que son las tres columnas que el
modelo exige.

No se detectó leyendo su informe, que describía el trabajo como hecho. Se detectó porque
`verificar_faseA.py` dijo:

```
x [F-02] PAR_Parametros: faltan 3 columnas del modelo: Valor, Unidad, Descripcion
```

Es la tercera vez en dos días que un reporte de cierre no resiste la comprobación contra el archivo,
y la tercera vez que el script lo para. La regla de `CLAUDE.md` §3 no es celo heredado: es lo único
que ha funcionado.

## 3. Incidente de método, y por qué esta vez el resultado fue mejor

**Se modificaron `modelo_objetivo.py` y `verificar_faseA.py` durante la aplicación**, que es
justamente lo que `CLAUDE.md` §3 prohíbe: quien aplica un cambio no toca la comprobación que lo
mide. Revisados los dos diffs, **ninguno relaja nada**:

- **`CLAVE_LEGIBLE` gana `PAR_Parametros`.** Es correcto y es **corrección de una omisión mía**: sus
  claves son `UMBRAL_GPS` y compañía, texto legible, así que F-11 fallaba con razón. Cuando declaré
  la tabla olvidé declararla también aquí.
- **Se añadieron F-14 y F-15**, que comprueban `OT_OrdenesTrabajo.Activo`, `EST_Activo.Activo` y la
  fila 34. Eso es **endurecer**: nadie las había codificado, y sin ellas el cierre dependía de que
  alguien mirase.

**El método siguió siendo el equivocado y el resultado fue estrictamente mejor.** Ambas cosas son
ciertas y conviene no elegir solo una. Lo que hace que esto sea aceptable no es que acertara: es que
el diff era pequeño, aditivo y revisable, y que se revisó línea a línea antes de aceptarlo.

## 4. Estado de la hoja

32 pestañas. Todo el cableado de referencias sigue pendiente: **15 columnas continúan como `Text`
donde deben ser `Ref`**, y 43 columnas marcadas como retiradas siguen presentes a propósito — la
Fase A no borra nada.

## 5. Lo que sigue

**Fase B**, `docs/sdd/ESPEC-002-cableado-en-appsheet.md`. Está **bloqueada** por el séptimo veredicto
del arquitecto, pendiente de que revise las correcciones de la última ronda: `Editable_If` sobre las
cuatro columnas de captura (RG-20), la parametrización del umbral (RG-19 con `PAR_Parametros`), y
las tres garantías que la especificación daba por absolutas y solo valen en la capa de aplicación.
