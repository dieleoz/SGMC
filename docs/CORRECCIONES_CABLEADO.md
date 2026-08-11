# Correcciones de cableado

**Generado** por `scripts/auditar_cableado.py` contra la aplicacion en vivo. No editar a
mano: vuelve a correr el script y se rehace con lo que quede pendiente.

---

En la aplicacion **`_SISGA_-323965761`**, 0 columnas de `ACT_Activos` estan mal. El resto del
cableado no contradice al modelo, pero conviene leer la cifra con cuidado: de las 39
referencias, **4 estan verificadas** —la aplicacion nombra la columna— y **26 solo son
compatibles**: la aplicacion nombra la tabla destino, y que la referencia este en la columna que
el modelo declara **lo dice el modelo, no la aplicacion**. Sumarlas es la cifra inflada que ya
costo cara una vez.

## Antes de tocar nada, por que importa

`ACT_Activos.TipoActivoID` apunta hoy a `SED_Sedes`. Con eso, **cada activo lee el checklist
de una sede**, y la regla del geofencing falla con un mensaje que despista:

```
Can't find column "RadioGeofencingKm" in table "SED_Sedes"
```

**La expresion esta bien escrita. No la cambies.** El error dice la verdad: navega a
`SED_Sedes` porque la referencia esta mal puesta, y ahi ese radio no existe. Reescribir la
expresion para acomodarla seria romper una regla correcta para tapar un cableado roto.

Ninguna regla se cablea hasta que estas 0 esten hechas.

## Como se llego a esto

Al cablear `ACT_Activos` salio un aviso rojo. Se corrigieron dos columnas a mano y se guardo.
Pero al guardar quedaron **tres columnas de texto convertidas en `Ref`** y **dos referencias
apuntando a `SED_Sedes`**, que era la tabla que estaba seleccionada. Nada lo detecto: la API
respondio 28/28, `validar_modelo.py` dio APTO y las 368 filas seguian ahi.

Es la regla **R-04**: *una referencia que resuelve puede apuntar a lo que no es.* Preguntar
«apunta a algo» nunca contesta «apunta a lo correcto».

## No hay nada que corregir

El cableado que **se puede medir** coincide con el modelo. Eso no es lo mismo que estar
terminado: mira más abajo lo que este método no alcanza a ver.



## Como saber que quedo

El boton `SAVE` pasa de gris a azul al recoger el cambio, y vuelve a gris al guardar. Ese
ciclo es la senal; si sigue gris, el editor no recogio nada y se pierde al recargar.

Despues, desde el repositorio:

```bash
python scripts/auditar_cableado.py
```

Sale con **0 correcciones** cuando esta bien. No te fies del recuento de tablas de la API:
dio 28/28 con estas 0 rotas.

## Lo que este script NO puede ver

9 referencias no son observables por este medio, porque su tabla destino esta **vacia** y
la columna virtual inversa vive en el destino. **No estan bien ni mal: no se sabe.**

| Referencia | Destino | Mirada en el editor |
|---|---|---|
| `CHD_ChecklistDetalle.ChecklistID` | `CHK_Checklists` | el 2026-08-10 por Diego, en el editor |
| `CHK_Checklists.MantenimientoID` | `MAN_Mantenimientos` | el 2026-08-10 por Diego, en el editor |
| `FIR_Firmas.MantenimientoID` | `MAN_Mantenimientos` | el 2026-08-10 por Diego, en el editor |
| `FOT_Fotografias.MantenimientoID` | `MAN_Mantenimientos` | el 2026-08-10 por Diego, en el editor |
| `MAN_Mantenimientos.OTID` | `OT_OrdenesTrabajo` | el 2026-08-10 por Diego, en el editor |
| `NOV_Novedades.ActivoID` | `ACT_Activos` | **nadie la ha mirado** |
| `OT_OrdenesTrabajo.ActivoID` | `ACT_Activos` | **nadie la ha mirado** |
| `OT_OrdenesTrabajo.OTOrigenID` | `OT_OrdenesTrabajo` | el 2026-08-10 por Diego, en el editor |
| `PLA_PlanMantenimiento.ActivoID` | `ACT_Activos` | **nadie la ha mirado** |

**3 sin mirar.** Abrelas en el editor una por una y confirma su `Source table`.
Dar por buena una referencia que nadie ha mirado es como se llego a un informe de
«39/39 asignadas» con cinco columnas rotas.

Para **medirlas**, sembrar una fila en `MAN_Mantenimientos`, `CHK_Checklists` y
`OT_OrdenesTrabajo` y volver a correr el auditor. De paso deja de haber tablas cuya clave
AppSheet tipo a ciegas por llegar vacias.
