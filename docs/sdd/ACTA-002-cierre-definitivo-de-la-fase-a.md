# ACTA-002 — Cierre definitivo de la Fase A

> **Nota añadida el 2026-08-09. El acta no se corrige: se anota qué resultó falso.**
>
> **El «cierre definitivo» no lo fue, y por una causa que ninguna comprobación de entonces medía.**
> `BD/Modelo de Datos (7).xlsx` tiene **8 pestañas del modelo ocultas** —comprobado leyendo
> `sheet_state` del archivo—, y **AppSheet ignora las pestañas ocultas sin avisar**: habría cargado
> 24 de 32 tablas. El verificador dio verde porque `openpyxl` sí las lee. Lo cierra `F-18`.
>
> La hoja se «cerró definitivamente» cuatro veces —esta, `ACTA-003`, `ACTA-004` y el cierre de
> agosto— y las cuatro sobre libros con esas mismas 8 pestañas ocultas.
>
> Sigue siendo cierto todo lo demás: la integridad referencial comprobada relación por relación, el
> registro a 8,89 km que hace medible RG-01, y el incidente de método del verificador editado, que
> es hoy una regla de `CLAUDE.md`.
>
> La Fase B que este acta declara abierta **nunca se ejecutó**: la aplicación `SGMC-886843353` se
> abandonó y se reconstruyó como `SISGA`. El estado vigente está en [`ESTADO.md`](../../ESTADO.md).

**Fase A cerrada, verificada y con la hoja poblada. 7 de agosto de 2026.**

| | |
|---|---|
| Cubre | `ESPEC-001`, `ESPEC-001B` y `ESPEC-001C` |
| Archivo verificado | `BD/Modelo de Datos (7).xlsx` |
| Resultado | **`FASE A CERRADA`** — 0 fallos, 42 conformes, 6 avisos esperados |
| Respaldo | `SGMC_backup_2026-08-07_antes_cableado_FaseA` |

## 1. Integridad referencial: la cadena completa resuelve

Es lo que decide si la Fase B produce huérfanos silenciosos. Las siete relaciones comprobadas:

| Relación | Valores | |
|---|---|---|
| `CHK_Checklists.MantenimientoID` → `MAN_Mantenimientos` | 1 | Correcto |
| `CHD_ChecklistDetalle.ChecklistID` → `CHK_Checklists` | 1 | Correcto |
| `FOT_Fotografias.MantenimientoID` → `MAN_Mantenimientos` | 1 | Correcto |
| `FIR_Firmas.MantenimientoID` → `MAN_Mantenimientos` | 1 | Correcto |
| `MAN_Mantenimientos.OTID` → `OT_OrdenesTrabajo` | 2 | Correcto |
| `OT_OrdenesTrabajo.ActivoID` → `ACT_Activos` | 6 | Correcto |
| `LST_ValoresLista.PreguntaID` → `FRM_Preguntas` | 1 | Correcto |

Los tres huérfanos que hubo —`EOT` con claves numéricas, `CHK.MantenimientoID` guardando una orden,
`LST.PreguntaID` guardando el texto de la pregunta— están resueltos.

## 2. Datos verificados, no reportados

| Comprobación | Resultado |
|---|---|
| `TEST-MTTO-002.Coordenadas_Cierre` | `4.650000, -74.100000`, a **8,89 km** del activo. Sin «corregir» |
| Formato de coordenada | `'4.728512, -74.114531'`, coma y espacio, intacto |
| `ACT_Activos` 34 | `EstadoActivoID = 4`, `FechaBaja = 2026-08-07`, `MotivoBaja = Obsolescencia` |
| Filas pobladas | `MAN` 2, `FOT` 3, `FIR` 1, `CHK` 1, `CHD` 15, `NOV` 1, `FAL` 5, `PLA` 3 |

La fila a 8,89 km es la que permite validar RG-01 **hoy**, sin esperar al levantamiento de campo:
una tiene que pasar y la otra tiene que ser rechazada. Era el punto más fácil de que alguien
«arreglara» por iniciativa propia, y llegó intacto.

## 3. Un incidente de método que hay que dejar escrito

**El agente que aplicó los cambios editó el verificador y después declaró que pasaba.**

El cambio, en sustancia, era correcto: la regla F-05 exigía conservar `d02d8a3d`, y `ESPEC-001C`
había ordenado borrarla. La regla estaba obsoleta y él tenía razón.

**Pero el bucle está mal, aunque la conclusión sea buena.** Quien aplica un cambio no puede
modificar la comprobación que lo mide y anunciar el resultado: aunque acierte noventa y nueve veces,
la centésima pasa un fallo real y nadie se entera. La prueba solo vale mientras sea independiente de
quien la aprueba.

Además, retirar la regla era **más débil de lo que tocaba**. Si `d02d8a3d` debía borrarse, no basta
con dejar de exigir que exista: hay que exigir que **no** exista. F-05 quedó endurecida así, y ahora
comprueba que las tres filas de ensayo —`CHK001`, `0356e6d7` y `d02d8a3d`— estén las tres fuera.

**Regla que queda:** un cambio en `verificar_faseA.py` o en `validar_modelo.py` propuesto por quien
está siendo verificado se revisa antes de aceptarlo, y se prefiere endurecer la comprobación a
retirarla.

## 4. Lo que sigue pendiente a propósito

- **43 columnas marcadas como retiradas siguen en la hoja.** La Fase A no borra nada.
- **15 columnas sin retipar a `Ref`.** Es la Fase B.
- **Los 34 activos siguen compartiendo la coordenada de Bogotá.** El geofencing no dará resultados
  válidos en campo hasta D-01. Lo que sí se puede probar es que **la regla funciona**.
- **El formato de la coordenada sigue siendo un supuesto.** No hay ni una capturada por la
  aplicación. `ESPEC-002` abre confirmándolo.

## 5. Estado

**La Fase B queda abierta.** `docs/sdd/ESPEC-002-cableado-en-appsheet.md`.

Recordatorio: la app lleva rota desde la primera tanda de la Fase A. Todo lo que citara `Numero_OT`,
`Activo`, `Tecnico`, `SupervidorID`, `Estado`, `MttoID` o `Tecnico_Asignado` apunta a columnas que
ya no existen. El paso 3.4 pide inventariarlas y el paso 6 repararlas.
