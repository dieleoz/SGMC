# Alcance del sistema y supuestos adoptados — SGMC

**Fecha:** 6 de agosto de 2026
**Estado:** Vigente. Sustituye el enfoque de consulta previa al líder funcional.
**Regla:** todo lo que aquí se declara como supuesto es **vinculante hasta que el campo lo
desmienta**. No se espera confirmación para construir.

---

## 1. Por qué cambia el método

El enfoque anterior era preguntar al líder funcional catorce decisiones y construir con sus
respuestas. Se descartó por tres razones:

1. **El cuestionario no avanza.** Quien responde no tiene el modelo mental del sistema todavía, y
   preguntarle en abstracto produce silencio o un "de acuerdo" a todo, que es peor porque simula
   una decisión que no existe.
2. **No hay nada que mirar.** El sistema actual no permite formarse un criterio: cuatro tablas
   vacías, un formulario de dieciocho, las referencias sin cablear y ninguna transacción
   ejecutada. Pedirle a alguien que valide modos de uso sobre eso es pedirle que imagine.
3. **Una suposición escrita se corrige en una tarde. Una pregunta sin responder bloquea semanas.**

El método nuevo: **inferir, construir completo, poblar con datos de prueba, entregar con manual, y
corregir con lo que diga el campo.** El líder funcional deja de ser una compuerta previa y pasa a
ser el validador de algo que puede tocar.

---

## 2. Qué significa "sistema completo"

No es el alcance mínimo. Es el sistema que se puede usar y del que se puede opinar:

| Dimensión | Alcance |
|---|---|
| Modelo de datos | Referencias cableadas de extremo a extremo, sin tablas huérfanas ni duplicadas |
| Formularios | Los 18 tipos de activo con banco de preguntas redactado |
| Flujos | Preventivo programado, correctivo desde campo, segunda visita, devolución y aprobación |
| Evidencia | Fotografías y firma con una sola vía de captura |
| Control | Geofencing operativo con excepción supervisada |
| Reportes | Los seis reportes propuestos, construidos y con datos |
| Datos | Toda la base poblada con datos de prueba realistas |
| Documentación | Manual de uso por rol, con modos, usos y reportes explicados |

---

## 3. Los catorce supuestos adoptados

Cada uno es la opción que se marcó como propuesta en el documento de mesa de trabajo. Se adopta
como decisión de trabajo. La columna de validación dice cómo se comprobará en campo.

| # | Decisión | Supuesto adoptado | Cómo se valida | Costo si está mal |
|---|---|---|---|---|
| D-01 | Coordenadas | Se cargan coordenadas reales sobre el trazado de la vía de la Concesión; un subconjunto sirve para validar antes del levantamiento completo | El técnico cierra un mantenimiento junto al activo | Bajo. Se recargan |
| D-02 | Radio | 200 m en activos puntuales; tratamiento aparte para fibra óptica | Tasa de bloqueos indebidos en la primera semana | Bajo. Es un número |
| D-03 | Sede | La unidad funcional es atributo del activo; la zona de trabajo, del usuario. Un técnico puede tener varias | El técnico ve activos al sincronizar | Medio. Reasignación masiva |
| D-04 | GPS deficiente | Cierre con excepción: motivo escrito, fotografía, marca y aviso al supervisor. Umbral 50 m | Porcentaje de cierres con excepción | Bajo |
| D-05 | Interrupción | Borrador local; la inspección queda en curso y debe cerrarse en la jornada | Inspecciones abandonadas | Bajo |
| D-06 | Ciclo de la OT | Siete estados. El técnico llega hasta En revisión; solo el supervisor cierra o suspende. Vencida al día siguiente. Se permite ejecutar sin orden previa como novedad | Órdenes atascadas en un estado | Medio |
| D-07 | Trabajo incompleto | Cierre parcial con motivo tipificado que genera orden de seguimiento. Devolución reabre el mismo registro con traza | Frecuencia de segundas visitas | Medio |
| D-08 | Activo no inventariado | El técnico levanta novedad con foto y coordenada; el supervisor decide el alta. Fuera de servicio genera orden correctiva automática | Novedades levantadas en el piloto | Bajo |
| D-09 | Tipos priorizados | **Se construyen los 18.** Se redactan a partir de los tres existentes y de la práctica de mantenimiento; el funcional corrige sobre texto concreto | Revisión del líder técnico sobre el formulario ya cargado | Medio. Se editan preguntas |
| D-10 | Evidencia | Tablas hijas para fotografías y firmas. Mínimo 3 fotos, máximo 6, tipificadas. El supervisor aprueba en el portal, no firma en campo | El técnico completa el formulario sin fricción | Alto si se cambia después de cargar datos |
| D-11 | Trazabilidad | El detalle guarda `PreguntaID`; los formularios se versionan | Comparación histórica de un activo | Alto si se omite |
| D-12 | Reportes | Se construyen los seis propuestos. Productividad del técnico queda desactivado por defecto | Uso real en la primera quincena | Bajo |
| D-13 | Indicadores | Cumplimiento sobre órdenes cerradas en fecha. Excepción de GPS cuenta como cumplida y se reporta aparte. Disponibilidad por tiempo fuera de servicio | Contraste con el reporte manual actual | Medio. Afecta cifras a terceros |
| D-14 | Gobierno | Interventoría sin acceso, solo reportes exportados. Cambios en producción solo por el administrador con autorización escrita. Retención de evidencia 5 años | Auditoría de cambios | Bajo |

**Dos supuestos que el campo puede tumbar y conviene vigilar:** D-10, porque cambiar el modelo de
evidencia después de cargar datos obliga a migrar; y D-13, porque si las cifras van a interventoría
la definición debe estar acordada antes de emitir el primer informe.

### 3.1 D-09 diverge de lo que se envió al funcional

El documento que ya salió proponía **arrancar con tres tipos** y advertía, con estas palabras, que
*intentar construir los 18 a la vez es lo que hará que el proyecto se estanque otro mes*.

Aquí se adopta lo contrario: **se construyen los 18**. La divergencia es deliberada y el motivo es
que cambió la premisa. Aquella advertencia suponía que los bancos los redactaba el equipo de la
Concesión, y en ese escenario era cierta. Con el método nuevo los redacta el agente a partir del
patrón existente, y el líder técnico corrige sobre texto concreto. Redactar es lo caro; corregir
es barato.

El riesgo que permanece es distinto y hay que nombrarlo: **250 preguntas escritas por quien no
hace el mantenimiento**. Saldrán razonables por venir del patrón de los tres existentes, pero no
son la práctica real del equipo. Deben presentarse como borrador técnico, nunca como definitivas,
y la revisión del líder técnico es obligatoria antes del piloto.

Si al revisar aparece que la mayoría no sirve, se vuelve a la propuesta original de tres tipos.

---

## 4. Fuera de alcance

- Integración con Power BI o mesas de ayuda.
- Gestión de repuestos, inventario de almacén y costos.
- Firma con valor probatorio frente a terceros.
- Generación automática de órdenes por frecuencia. Se deja el catálogo listo pero sin el
  disparador, hasta ver el comportamiento del preventivo manual.

---

## 5. Cómo se corrige un supuesto

1. El campo o el líder funcional detecta que un supuesto no sirve.
2. Se registra en este documento con fecha y motivo.
3. Se evalúa el costo de cambio según la columna correspondiente.
4. Si implica migrar datos, se decide antes de seguir cargando.

Un supuesto corregido no es un error del método: es el método funcionando.

---

## 6. Relación con los documentos existentes

- El documento de mesa de trabajo y su correo **ya se enviaron**. No se remiten de nuevo. Lo que
  responda el líder funcional se contrasta contra estos supuestos y se integra.
- `docs/ROADMAP.md` recoge la secuencia de construcción.
- `docs/prompts/PROMPT_CONSTRUCCION_SGMC.md` es la directiva de ejecución.
