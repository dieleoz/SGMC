# Comunicación al Propietario de la Aplicación

> **Documento por rol, no por persona.** El **Propietario de la Aplicación** es quien figura como
> *owner* de la app en AppSheet y del documento de Google Sheets que le sirve de backend. En este
> proyecto es un tercero, con una entrega planificada a la Concesión. El documento está escrito así
> para poder replicarlo en otro contrato sin reescribirlo.

**Ya no estamos bloqueados.** Este documento decía que hacía falta un permiso suyo para continuar.
Se resolvió por otro camino, y ahora lo que queda es **avisar y cerrar un punto**.

| | |
|---|---|
| Actualizado | 2026-08-09 |
| Aplicación original | `SGMC-886843353`, de `[correo del Propietario]` |
| Aplicación nueva | `SISGA`, propiedad de `[correo de la Concesión]` |
| Hoja de producción | La que declara `scripts/sistema.py`, generada del modelo |

> **Y aquí hay un punto que no se puede cerrar desde el repositorio.** `ESTADO.md` y `CLAUDE.md` §2
> dan esa hoja como **propiedad de la Concesión**; este documento la daba como del Propietario,
> compartida con nosotros. **Las dos no pueden ser ciertas, y ninguna se verifica leyendo un archivo
> del repositorio**: hay que abrir el documento en Drive y mirar el propietario. Si ya es de la
> Concesión, el apartado 3 está resuelto y lo único que queda de este documento es el apartado 4.

## 1. Qué pasó

El modelo de datos se corrigió **en la hoja**: 27 columnas renombradas, 8 tablas nuevas, 43 campos
retirados. La aplicación conservaba el esquema anterior y no había forma de que lo recogiera.

**Y no era falta de maña. Son dos límites de AppSheet, los dos verificados:**

**`Regenerate` fusiona, no reemplaza.** Su documentación oficial dice que combina la información
nueva con la existente e intenta mantener las columnas que ya están. Sirve para añadir una columna;
no para un esquema que divergió tanto. La tabla de órdenes sobrevivió a varios *Regenerate*
conservando `Numero_OT`, `Tecnico` y `Estado`.

**Y las columnas reales no se pueden borrar una a una.** El propio AppSheet indica la salida:
*«Delete and re-add the table to create the column structure»*.

**Por eso se reconstruyó.** Se creó una aplicación nueva sobre la misma estructura de datos y
funcionó a la primera. Lo que llevaba dos días atascado se resolvió en una tarde.

## 2. Un hallazgo que conviene que conozca

**Ocho pestañas de la hoja estaban marcadas como ocultas**, y son el núcleo del modelo:

```
ACT_Activos · USR_Usuarios · TIP_TiposActivo · ROL_Roles
SED_Sedes · CAL_Calzadas · SEN_Sentidos · FRE_Frecuencias
```

**AppSheet ignora las pestañas ocultas y no avisa.** Simplemente no aparecen al dar de alta tablas.
Por eso cargaban 24 de 32 y `ROL_Roles` no salía en ningún desplegable.

Es probablemente la causa de buena parte de lo que se venía atascando, y no era evidente desde
ninguna parte.

## 3. Lo único que se le pide

**Confirmar sobre qué hoja opera la aplicación en producción.** Hay dos opciones y las dos
funcionan:

**Que la aplicación nueva apunte a su hoja** —`Modelo de Datos`—. Tenemos permiso de edición sobre
ella, así que técnicamente no hace falta nada más. Solo saber que está de acuerdo.

**O que pase a ser nuestra**, y su hoja queda como respaldo. Más limpio de cara a la entrega que ya
estaba prevista, porque las fotografías del sistema consumen cuota de Drive del propietario del
documento, y eso hoy es su cuenta.

**No corre prisa, pero tampoco sobra tanto como parecía.** Con los 355 activos del Plan Maestro esa
cuota da para **5,7 años**, frente a los 5 de retención de evidencia que exige el proyecto; si el
parque crece a 500, se agota en 4,1 y ya no llega. Sale de `python scripts/capacidad.py`. Es el tipo
de cosa que conviene decidir antes de que haya técnicos en campo, no después: mover un backend con
evidencia dentro cuesta mucho más.

## 4. Y una cosa que le debemos

**La aplicación original quedó en la versión 1.000245, sin poder ejecutarse.**

Ya no cargaba antes —ese era el problema que fuimos a diagnosticar—, pero **dos de sus errores los
introdujimos nosotros** al renombrar una tabla durante el diagnóstico.

> **No sirve rodar atrás a una versión anterior.** La pestaña `SEC_Secciones` ya no existe en la
> hoja —la Fase A la renombró a `FRM_Secciones`—, así que cualquier versión antigua apunta a una
> pestaña que no está. Habría que reconstruirla igual.

Como la aplicación nueva la sustituye, **lo razonable es despublicarla** en vez de repararla. Y hay
una razón técnica para hacerlo pronto: si las dos aplicaciones apuntan a la misma hoja, la vieja
sigue pudiendo escribir con permisos que el modelo nuevo ya no concede.

## 5. Borrador del mensaje

> Hola,
>
> Te cuento dónde estamos con el SGMC.
>
> El modelo de datos de la hoja se corrigió bastante —27 columnas renombradas, ocho tablas nuevas,
> campos retirados— y la aplicación no había forma de que lo recogiera. No era cosa de insistir: el
> *Regenerate* de AppSheet conserva las columnas viejas en vez de sustituirlas, y las columnas
> reales no se pueden borrar una a una. Lo dice el propio AppSheet cuando te atascas.
>
> Así que levantamos una aplicación nueva sobre la misma estructura y funcionó a la primera.
>
> De paso encontramos algo que te va a interesar: **ocho pestañas de la hoja estaban ocultas**, y
> son las principales — activos, usuarios, tipos, roles, sedes. AppSheet ignora las pestañas ocultas
> sin avisar, así que solo veía 24 de 32. Ahí estaba buena parte del misterio.
>
> Lo único que necesitamos de ti es confirmar sobre qué hoja opera la aplicación de producción: si
> seguimos con la tuya —tenemos permiso de edición— o si pasa a la cuenta de la Concesión. Lo
> segundo es más limpio porque las fotografías consumen cuota de Drive del propietario, y con el
> inventario completo esos 15 GB dan justo para los cinco o seis años que hay que guardar.
>
> Y algo que te debemos: la aplicación original quedó en un estado que no arranca. Ya venía
> fallando, pero dos de esos errores los provocamos nosotros diagnosticando, y no se arreglan
> volviendo atrás porque una pestaña cambió de nombre. Como la nueva la sustituye, nuestra
> recomendación es despublicarla.
>
> Cuando quieras te enseñamos la nueva.

---

*Estado del proyecto en `ESTADO.md`. Qué hace el sistema, en `docs/FUNCIONAL_SGMC.md`. Los dos*
*límites de AppSheet que explican la reconstrucción, con su cita oficial, en*
*`docs/BASE_CONOCIMIENTO_APPSHEET.md` §11 y §12.*
