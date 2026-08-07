# ACTA-001 — Cierre de la Fase A

**Fase A cerrada y verificada el 7 de agosto de 2026.**

| | |
|---|---|
| Cubre | `ESPEC-001` y `ESPEC-001B` |
| Aplicado por | Asistente en la hoja, a mano, sobre el Sheets de producción |
| Verificado por | `python scripts/verificar_faseA.py "BD/Modelo de Datos (6).xlsx"` |
| Resultado | **`FASE A CERRADA`** — 0 fallos, 6 avisos esperados |
| Respaldo | `SGMC_backup_2026-08-07_antes_cableado_FaseA` (`1CwLyJFn…OvF_8`) |

## 1. Qué quedó aplicado

- **23 renombrados** en 8 tablas. `Numero_OT` es ahora `OTID`, `MttoID` es `MantenimientoID`,
  `Tecnico_Asignado` es `TecnicoID`, y las tildes de `Descripción` y `Versión` desaparecieron.
- **13 columnas nuevas**, entre ellas las nueve de `MAN_Mantenimientos` que sostienen la cadena de
  evidencia, y `RadioGeofencingKm` en `TIP_TiposActivo`.
- **7 tablas nuevas**, cuatro de ellas pobladas: `UNF_UnidadesFuncionales` (4),
  `EOT_EstadosOrden` (7), `MOT_MotivosPendiente` (5) y `ASG_AsignacionZona` (4).
- **Limpieza de `CHK_Checklists`:** borradas `CHK001` —la del `TecnicoID = "Santiago Moreno"` y el
  `NOW()` literal— y `0356e6d7`. Conservada `d02d8a3d`.

## 2. Integridad referencial comprobada

Es lo que decide si la Fase B funciona o produce huérfanos en silencio:

| Comprobación | Resultado |
|---|---|
| Las 4 unidades funcionales usadas por `ACT_Activos` resuelven contra `UNF` | Correcto |
| Los 3 estados usados por las órdenes resuelven contra `EOT_EstadosOrden` | Correcto |
| `ASG_AsignacionZona.UsuarioID` resuelve contra `USR_Usuarios` | Correcto |
| `ASG_AsignacionZona.UnidadFuncionalID` resuelve contra `UNF` | Correcto |
| Las 6 órdenes siguen intactas, con sus claves `OT-0001` a `OT-0006` | Correcto |

## 3. El fallo que se corrigió, y por qué importa

`EOT_EstadosOrden` se creó con claves numéricas `1..7` mientras `OT_OrdenesTrabajo.EstadoOrdenID`
guardaba `Asignada`, `Cerrada` y `Suspendida`. Convertir a `Ref` con eso habría dejado las **6
órdenes huérfanas y sin aviso**: el mismo defecto que `OTID` lleva meses causando, reproducido en
una tabla creada el día anterior.

Se corrigió el catálogo, no las órdenes: `EOT` no tenía dependientes y la transaccional sí tiene
historia. **Ante la duda, se mueve lo que no tiene historia.**

De aquí sale la regla **R-8** de `CLAUDE.md`: un catálogo nuevo se diseña mirando los datos que va a
tener que resolver, y su clave es el valor que esos datos ya guardan.

## 4. Lo que sigue pendiente, y es correcto que lo esté

- **43 columnas marcadas como retiradas siguen en la hoja** — 13 en `MAN`, 15 en `CHK`, 12 en `CHD`,
  3 en `OT`. La Fase A no borra nada, deliberadamente: borrar es lo único que el respaldo no vuelve
  gratis.
- **15 columnas siguen sin retipar a `Ref`.** Es la Fase B, en el editor de AppSheet.
- **`MAN_Mantenimientos` sigue con 0 filas.** Los datos de prueba nunca se escribieron, y conviene:
  mantiene la propiedad de que convertir `OTID` a `Ref` no arrastra nada.

## 5. Lecciones de método

**Tres reportes de cierre consecutivos no resistieron la comprobación contra el archivo.** El
primero declaró la Fase A «100% cerrada y validada» con 19 fallos abiertos; el segundo dejó 23. Solo
el tercero cerró de verdad. No es descuido de nadie en particular: es que **el trabajo manual sobre
una hoja de 31 pestañas no se puede autoverificar de memoria.**

Lo que funcionó fue tener un verificador que compara contra `modelo_objetivo.py` y no contra lo que
alguien recuerda haber hecho. Ese script es ahora parte del repositorio.

**Dos defectos fueron míos y quedan anotados:**

1. La función `verificar()` del Apps Script marcaba como error las dos columnas `Activo` de
   `OT_OrdenesTrabajo`, que están bien. No distinguía una reutilización legítima del nombre.
2. `verificar_faseA.py` informaba «los estados de las 3 órdenes resuelven» cuando contaba **valores
   distintos**, no órdenes. Con 6 órdenes en la tabla, el mensaje inducía a error.

Ambos corregidos. El segundo importa especialmente: un verificador que informa mal es peor que no
tenerlo, porque se le cree.

## 6. Estado del gate

**La Fase B queda desbloqueada.** `docs/sdd/ESPEC-002-cableado-en-appsheet.md` puede ejecutarse.

Recordatorio antes de empezar: guardar versión de la aplicación en *Manage → Versions*, y buscar en
el editor cada vista o fórmula que cite `Numero_OT`, `Activo`, `Tecnico`, `SupervidorID`, `Estado`,
`MttoID` o `Tecnico_Asignado`. **Esas columnas ya no existen, y todo lo que las citaba lleva roto
desde que se aplicó la Fase A.**
