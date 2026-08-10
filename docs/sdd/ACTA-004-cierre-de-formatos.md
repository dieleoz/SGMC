# ACTA-004 — Cierre de formatos

> **Nota añadida el 2026-08-09. El acta no se corrige: se anota qué resultó falso.**
>
> **Quedaba un noveno punto que `F-16` y `F-17` no podían ver.** `BD/Modelo de Datos (11).xlsx`
> —el archivo que este acta certifica con 59 conformes y 0 fallos— tiene **8 pestañas del modelo
> ocultas**: `ACT_Activos`, `USR_Usuarios`, `TIP_TiposActivo`, `ROL_Roles`, `SED_Sedes`,
> `CAL_Calzadas`, `SEN_Sentidos` y `FRE_Frecuencias`. Comprobado leyendo `sheet_state` del archivo.
>
> **AppSheet ignora las pestañas ocultas y no lo anuncia:** de las 32 solo habría cargado 24, y esas
> ocho no aparecían siquiera en el desplegable de tabla origen. Lo cierra `F-18`, escrita después.
>
> Este acta escribió que **«ningún script leía valores: todos leían fórmulas»**. El defecto de las
> ocultas es el mismo patrón una vuelta más allá: `openpyxl` las lee sin distinción, así que la
> comprobación pasaba midiendo lo que no era.
>
> **Y el `ESPEC-002` que este acta deja pendiente del décimo veredicto nunca se ejecutó.** Se
> autorizó con `ORDEN-002`, la aplicación `SGMC-886843353` se abandonó el 2026-08-09 y se
> reconstruyó desde cero como `SISGA`. No hay `ACTA-005`.
>
> El estado vigente está en [`ESTADO.md`](../../ESTADO.md).

**La hoja queda cerrada en contenido y en formato el 7 de agosto de 2026.** No se toca una celda más
desde Google Sheets.

| | |
|---|---|
| Archivo verificado | `BD/Modelo de Datos (11).xlsx` |
| Resultado | **`FASE A CERRADA`** — 59 conformes, 0 fallos |
| Cubre | Los 8 puntos que detectaron `F-16` y `F-17` |

## 1. Por qué hubo que reabrir una hoja ya cerrada

`ACTA-003` la cerró **en contenido**: todas las columnas presentes, todas las filas pobladas, todas
las referencias resolviendo. Y era cierto.

Lo que ninguna comprobación miraba era **cómo estaban guardados los datos**. Dos reglas nuevas
encontraron ocho puntos:

**F-16 — el mismo valor en dos formatos.** Un `Ref` de AppSheet guarda el valor de la clave del
destino. Pero `ACT_Activos.ActivoID` guardaba `2.0` como **número** y `OT_OrdenesTrabajo.ActivoID`
guardaba `'2'` como **texto**. Al tipar ambas, de cómo convirtiera AppSheet dependía que la
referencia resolviera o quedara rota sin avisar. Y `OT.SupervisorID` tenía `8.0` y `'8'` **en la
misma columna**: unas filas habrían resuelto y otras no.

**F-17 — una columna que no contenía datos.** `TIP_TiposActivo.FormularioID` tenía 18 fórmulas,
`=CONCAT("FRM_",MID(B2,1,4))`, que toman los cuatro primeros caracteres del nombre del tipo.
Funcionaba por casualidad del nombrado: renombrar un tipo de activo habría repuntado en silencio el
checklist que abre la aplicación en campo.

## 2. Lo verificado contra el archivo

| Comprobación | Resultado |
|---|---|
| `ACT_Activos.ActivoID`, `USR_Usuarios.UsuarioID`, `OT.ActivoID`, `OT.SupervisorID`, `MAN.TecnicoID` | Todos `str`, **sin decimales** |
| `3aa202ee` | Intacto. Es el valor que justificaba todo el cambio |
| `TIP_TiposActivo.FormularioID` | **0 fórmulas**, los 18 valores conservados de `FRM_SOS` a `FRM_SUBE` |
| `MAN.Precision_GPS` | `8` y `45`, sin tocar |
| `PAR_Parametros.Valor` | Sigue numérico, que es lo que exige `LOOKUP()` |

El riesgo del cambio era que convertir un número a texto produjera `2.0` en lugar de `2`, y eso
habría roto las referencias igual que antes. No ocurrió.

## 3. Un defecto sistémico que salió por el camino

**Ningún script leía valores: todos leían fórmulas.** Ni `verificar_faseA.py` ni
`generar_diccionario_bd.py` usaban `data_only=True`, así que openpyxl les devolvía el texto de la
fórmula. `TIP_TiposActivo.FormularioID` daba **18 huérfanos** leída en crudo y **0** leída con
valores, y ninguna regla la evaluaba por lo que realmente contenía.

El diccionario As-Built llevaba generándose con `=CONCAT(...)` en esas 18 celdas.

Y la trampa: poner `data_only=True` a secas **habría roto F-17**, porque openpyxl deja de ver la
fórmula. Hacen falta dos libros abiertos del mismo archivo — uno de valores para todas las
comprobaciones, otro de fórmulas solo para F-17. Así queda.

## 4. Método

**Esta vez nadie tocó los scripts de verificación.** En las dos tandas anteriores sí, y aunque los
cambios resultaron legítimos, el bucle era el equivocado. Aquí el diff solo trajo los dos `.xlsx`
nuevos.

También conviene dejar escrito que **el reporte de cierre afirmaba que el arquitecto había aprobado
`ESPEC-002`**. No lo hizo: su noveno veredicto fue `BLOQUEA` con siete condiciones. Arrancar la
Fase B sobre esa frase habría sido ejecutar una especificación sin gate.

## 5. Estado

La hoja está cerrada. Quedan **15 columnas como `Text` que deben ser `Ref`** y 43 columnas marcadas
como retiradas, ambas cosas a propósito: eso es la Fase B y una pasada posterior.

`ESPEC-002` sigue pendiente del décimo veredicto.
