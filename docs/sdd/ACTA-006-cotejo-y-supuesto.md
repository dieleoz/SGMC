# ACTA-006 — El cotejo de `OT_OrdenesTrabajo` y la medición del supuesto

Dos hechos del mundo, medidos en el editor y por API. No son documento: son lo que hay.

Se levantó porque el arquitecto bloqueó `ESPEC-006` señalando que su precondición se apoyaba en un
instrumento incapaz de observarla, y que un supuesto que sostenía cuatro pruebas se podía **medir en
cinco minutos** en vez de declararse.

---

## 1. Las nueve columnas de `OT_OrdenesTrabajo`

**Cotejo a ojo, con `Ctrl+Shift+R` previo.** La recarga en duro no es ceremonia: una sesión anterior
vio estas mismas nueve columnas **como `Text`** cuando ya estaban puestas, y era caché. Ese cotejo
anterior quedó en duda y por eso se rehízo.

El aviso «A newer version of the app exists» **no apareció** en ningún momento.

| Columna | `TYPE` literal | Detalle |
|---|---|---|
| `Activo` | **`Yes/No`** | |
| `ActivoID` | **`Ref`** | `Source table: ACT_Activos` |
| `CerradaPor` | **`Ref`** | `Source table: USR_Usuarios` |
| `EstadoOrdenID` | **`Ref`** | `Source table: EOT_EstadosOrden` |
| `OTOrigenID` | **`Ref`** | `Source table: OT_OrdenesTrabajo` — auto-referencia |
| `Observaciones` | **`LongText`** | |
| `SupervisorID` | **`Ref`** | `Source table: USR_Usuarios` |
| `TecnicoID` | **`Ref`** | `Source table: USR_Usuarios` |
| `Tipo` | **`Enum`** | valores: `Preventivo`, `Correctivo` |

**Las nueve coinciden**, incluida `EstadoOrdenID`, que es de la que depende la desreferencia de
`RG-37`.

Se transcribieron aunque coincidieran. No hay comando que las recupere —la API devuelve filas, no
esquema— y el cotejo anterior se reportó sin registro: esa fue exactamente la razón del bloqueo.

---

## 2. Una columna virtual **sí** se lee por la API

Era el supuesto 7 de `ESPEC-006`, y sostenía cuatro pruebas y el gasto irreversible de la ventana.
`docs/BASE_CONOCIMIENTO_APPSHEET.md` §16 solo documentaba que viajan las **virtuales inversas de
`Ref`**; de una virtual calculada con `App formula` no había ni cita ni observación.

**Se midió en vez de debatirse.** Sobre `PAR_Parametros`, que tiene 3 filas y **no** es una de las
ocho tablas de movimiento, así que la prueba no cierra ninguna ventana y la columna es reversible:

```
1  Add virtual column  ->  PruebaVirtual, App formula CONCATENATE("x-", [Valor]), Show? activo
2  python scripts/instantanea.py guardar prueba-virtual
3  leer las columnas que devuelve PAR_Parametros
4  borrarla
```

Lo que devolvió la API:

```
['Activo', 'Descripcion', 'Nombre', 'ParametroID', 'PruebaVirtual', 'Unidad', 'Valor', '_RowNumber']
```

**`PruebaVirtual` aparece.** El supuesto pasa de apuesta a hecho medido, y las cuatro pruebas que
dependían de él son ejecutables.

Borrada después: `PAR_Parametros` volvió a sus siete columnas exactas. Las columnas virtuales sí
tienen papelera, a diferencia de las reales — que es lo que hacía esta prueba barata.

---

## 3. Lectura de vuelta

```
python scripts/instantanea.py comparar antes-de-la-ventana tras-cotejo
-> NINGUNA CELDA CAMBIO
```

Las ocho tablas de movimiento siguen en cero. **La ventana barata sigue abierta.**

---

## 4. Qué desbloquea

| Condición del dictamen | Estado |
|---|---|
| 1 · el cotejo, ni pendiente ni hecho | **resuelta**: hecho, con recarga y transcrito |
| 2 · retirar `clasificar()` como evidencia de estado | **resuelta**: la evidencia es esta acta |
| 3 · dueño y momento de la precondición | **resuelta**: cerrada aquí |
| 6 · el supuesto 7, medido antes de gastar | **resuelta**: se lee por API |
| 8 · el criterio de cierre de `P-60` | deja de depender de pruebas bloqueadas |

Lo que queda de ese dictamen son **notas**, no bloqueantes: prosa desincronizada y alcance. Por la
vara de `CLAUDE.md` §7.18, ninguna nombra qué se rompe en producción.
