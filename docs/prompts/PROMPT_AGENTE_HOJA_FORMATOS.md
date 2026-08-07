# Prompt para el agente de la hoja — normalizar formatos antes del cableado

Autocontenido. Cópialo íntegro desde la línea siguiente.

Son **dos cosas**, y las dos son de formato: no cambia ningún valor, solo cómo está guardado. Salen
de dos comprobaciones automáticas, `F-16` y `F-17` de `verificar_faseA.py`, que hoy dan **3 fallos**
y 5 avisos.

---

Vas a normalizar cómo están guardados algunos datos del Google Sheets del SGMC. **Ningún valor
cambia de significado**: un `2` sigue siendo un `2`. Lo que cambia es el formato de la celda.

## Por qué importa, en una frase

En AppSheet, una referencia entre tablas **guarda el valor de la clave de la tabla destino**. Si la
clave está guardada como número (`2`) y quien la apunta como texto (`'2'`), al convertir las
columnas a referencia AppSheet tiene que decidir cómo convertir — y de esa decisión depende que la
referencia funcione o quede rota **sin avisar**.

## Cambio 1 — Todos los identificadores como TEXTO

Estas columnas guardan identificadores. Unas están como número y otras como texto, y **tienen que
estar todas como texto**.

| Hoja | Columna | Cómo está hoy |
|---|---|---|
| `ACT_Activos` | `ActivoID` | número (`1`, `2`, … `34`) |
| `USR_Usuarios` | `UsuarioID` | número, salvo `3aa202ee` que es texto |
| `OT_OrdenesTrabajo` | `SupervisorID` | **mezclado**: unas filas número, otras texto |
| `MAN_Mantenimientos` | `TecnicoID` | número |
| `NOV_Novedades` | `UsuarioID` | número |
| `PLA_PlanMantenimiento` | `ResponsableID` | número |
| `ASG_AsignacionZona` | `UsuarioID` | número |

**Cómo hacerlo, y el orden importa:**

1. Selecciona la columna completa (sin el encabezado).
2. *Formato → Número → **Texto sin formato***.
3. **Después** vuelve a escribir los valores, o córtalos y pégalos como valores. Cambiar el formato
   de una celda que ya tiene un número **no siempre lo convierte**: Google puede seguir guardándolo
   como número por debajo.
4. La alineación a la izquierda es una pista útil, **pero no es el criterio de aceptación**. El
   criterio es que `verificar_faseA.py` deje de dar `F-16`: eso es lo único que lo comprueba de
   verdad, y lo hace sobre la descarga siguiente.

**Cuidado con dos cosas:**

- **No añadas decimales ni ceros.** El activo `2` debe quedar como `2`, no como `2.0` ni `02`.
- **`USR_Usuarios.UsuarioID` tiene un valor alfanumérico, `3aa202ee`.** Ese ya es texto y se queda
  igual. Es justamente por él por lo que toda la columna tiene que ser texto: si fuera número, esa
  fila quedaría sin clave válida.

## Cambio 2 — `TIP_TiposActivo.FormularioID` deja de ser una fórmula

Esa columna no contiene datos: contiene una fórmula en las 18 filas.

```
=CONCAT("FRM_",MID(B2,1,4))
```

Toma los cuatro primeros caracteres del nombre del tipo de activo. **Funciona hoy por casualidad del
nombrado**, y si alguien renombra un tipo, el mapeo al formulario cambia solo y en silencio — y ese
mapeo es lo que decide qué checklist abre la aplicación en campo.

**Los valores que debe conservar**, en orden: `FRM_SOS`, `FRM_CCTV`, `FRM_PMVF`, `FRM_PMVM`,
`FRM_SGM`, `FRM_SGE`, `FRM_SSA`, `FRM_GENE`, `FRM_BASC`, `FRM_FO`, `FRM_VW`, `FRM_SWIT`,
`FRM_ROUT`, `FRM_FIRE`, `FRM_UPS`, `FRM_SERV`, `FRM_NAS`, `FRM_SUBE`.

**Qué hacer:** copiar la columna `FormularioID` completa y **pegarla sobre sí misma como valores**
(*Editar → Pegado especial → Pegar solo los valores*). Los valores no cambian: siguen siendo
`FRM_SOS`, `FRM_CCTV`, `FRM_PMVF`, y así hasta `FRM_SUBE`. Lo que desaparece es la fórmula.

Después, comprueba que al hacer clic en una celda de esa columna la barra de fórmulas muestra
`FRM_SOS` y no `=CONCAT(...)`.

## Lo que NO hay que hacer

- **No cambies ningún valor.** Ni identificadores, ni nombres, ni fechas.
- **No toques `Precision_GPS` de `TEST-MTTO-002`.** Vale `45` y está bien.
- No borres filas ni columnas, ni añadas pestañas.

## Cuando termines

Descarga el libro —*Archivo → Descargar → Microsoft Excel*—, guárdalo en `BD/` y avisa con el
nombre del archivo. Se verifica con:

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir **`FASE A CERRADA`** con 0 fallos. Ahora mismo da **3 fallos** —`OT.SupervisorID`
mezclado, `ACT.ActivoID` contra las órdenes, y la fórmula de `FormularioID`— más 5 avisos que se van
solos al normalizar `USR_Usuarios.UsuarioID`.

**No lo des por cerrado tú.** En las tandas anteriores se reportó como cerrado y la verificación
encontró fallos las tres veces. Deja que lo diga el script.
