# Contexto de operación — qué dicen los documentos reales

Lo que aportan los siete documentos de `contexto/` al modelo de datos del SGMC. No es un resumen
de cada uno: es **lo que sirve** para decidir tablas, columnas y flujos, con la cita de dónde sale.

| | |
|---|---|
| Origen | `contexto/`, aportado el 2026-08-07 |
| Documentos | 7 · **todos leídos** |
| Para qué sirve | Alimentar `MODELO_EVOLUCION_FASE_2.md` con dominio verificado, no supuesto |
| Qué **no** es | Una especificación. Nada de aquí se ejecuta sin pasar por `ESPEC-00N` y su veredicto |

## Advertencia de procedencia, y es importante

**Tres de los siete documentos no son del Sisga.** Son de otros corredores y otros contratistas:

| Documento | Proyecto real | Contratista |
|---|---|---|
| `2-MANTENIMIENTO.pdf` | Neiva – Aipe – Castilla – Espinal – Girardot | ETRA · Consorcio Constructor ANG · 2017 |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` | Doble calzada, contrato 444-005-15 | INDRA Colombia · 2016 |
| `Informe … enero 2025 v1.1.docx` | Sisga | — |

Los dos primeros valen como **método a imitar**, no como obligación contractual. Cuando este
documento diga «la práctica del sector», sale de ahí. Cuando diga «el contrato», sale del plan 2026
o del cronograma supervisado por JOYCO, que sí son del Sisga.

Confundir las dos cosas sería exactamente el error que este proyecto ya cometió una vez con un
inventario ajeno.

---

## 1. El inventario de documentos

| Documento | Qué aporta que no teníamos |
|---|---|
| `Plan Maestro de Mantenimiento ITS_TI.xlsx` | 24 tipos, 355 activos, tarea, periodicidad, herramienta y **personal por tarea** |
| `PLAN_MANTENIMIENTO_SISGA_2026.docx` | El plan vigente por subsistema |
| `Plan de actividades … 2025 Componente ITS.xls` | **Cronograma contractual**, supervisado por JOYCO S.A.S. |
| `Informe … enero 2025 v1.1.docx` | La **salida** exigida: qué secciones tiene el informe mensual |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` | **La manta**: la rejilla semanal y el indicador de cumplimiento |
| `2-MANTENIMIENTO.pdf` | El **flujo de correctivo**, los SLA y la arquitectura de un GMAO real |
| `PPT 2026 Operación de Vías.xlsx` | Presupuesto de operación. Sin uso para el modelo |

---

## 2. La manta, que hasta ahora era una palabra

`PROPUESTA - PLAN MTTO DC 2016.xlsx`, hoja `SEMANA 1 AL 5 DE FEBRERO`.

```
                                 BQ   QB   BV    V
PRUEBA SEMANAL POSTES SOS         X         X    X
PRUEBA SEMANAL RADIO-COMUNICAC.   X    X    X
VERIFICACIÓN SEMANAL MÁSCARAS     X         X
MANTENIMIENTO TRIMESTRAL …             X
PRUEBA MENSUAL CON INTERVENTORÍA  X         X    X
───────────────────────────────────────────────────
TAREAS EJECUTADAS                 5   10    5    2   = 22
TAREAS NO EJECUTADAS              1    1    0    0   =  2
                                83%  91%  100% 100%
```

**Tareas en filas, sectores en columnas, y abajo planeadas contra ejecutadas.** Eso es la manta, y
ese porcentaje es el indicador que se reporta.

### Tres cosas que cambian el modelo

**Un tipo de equipo tiene varias tareas, y ahora está probado.** El poste SOS aparece con prueba
**semanal**, prueba **mensual con interventoría** y mantenimiento **trimestral**. El maestro ITS
listaba una sola tarea por tipo, y sobre esa simplificación se construyó `ACT_Activos.FrecuenciaID`.
Confirma la sección 3 de `MODELO_EVOLUCION_FASE_2.md`: la periodicidad es de la tarea, no del
activo.

**Hay tareas con la interventoría dentro.** `PRUEBA MENSUAL CON INTERVENTORÍA` no es una tarea
normal: alguien externo asiste y firma. El modelo tiene `FIR_Firmas`, pero no sabe que una tarea
pueda exigir una firma de tercero.

**El cumplimiento es una resta, no un dato.** Planeadas menos ejecutadas. Con
`PLA_PlanMantenimiento` y `OT_OrdenesTrabajo` esa cifra **sale sola**, sin que nadie la teclee — y
hoy se teclea. Es el argumento de venta más fuerte que tiene este sistema y no estaba escrito en
ninguna parte.

---

## 3. El flujo de correctivo, que el modelo no tiene

`2-MANTENIMIENTO.pdf` §6. Es la parte más útil de los siete documentos, porque el correctivo es
justo donde nuestro modelo está en blanco.

### La cadena completa

```
Aviso            teléfono · web · correo · alarma del SCADA
   ↓
Ticket           número que se entrega a quien reporta, y le sirve para consultar estado
   ↓
Tipología        Incidencia · Consulta · Petición
Criticidad       Total/Crítica · Parcial grave · Parcial leve
   ↓
Nivel            N1 técnico en campo · N2 especialista · N3 taller o fabricante
   ↓
Reparación       cambiar el elemento, nunca repararlo en sitio
   ↓
Parte de trabajo elemento reparado · hora de puesta en marcha · observaciones
```

### La criticidad se define por porcentaje de servicio, no por opinión

| Nivel | Definición | Respuesta | Resolución |
|---|---|---|---|
| Total / Crítica | 75–100 % de la instalación en avería | **2 h** | **4 h** |
| Parcial grave | 25–75 % | **4 h** | **12 h** |
| Parcial leve | 25 % o menos | **12 h** | **48 h** |

Y las dos definiciones que hacen medible el SLA:

- **Tiempo de respuesta:** desde que se notifica hasta que **empiezan a trabajar** en la resolución.
- **Tiempo de resolución:** desde que se informa hasta que está resuelta **y el cliente informado**.
- **Reloj parado:** el tiempo bloqueado por terceros o fuerza mayor no cuenta.

Esa última es la que nadie modela y siempre hace falta. Sin ella, cualquier SLA se incumple por
esperar un repuesto.

### Qué le falta al modelo para esto

`OT_OrdenesTrabajo` no tiene criticidad, ni hora de aviso, ni hora de inicio de trabajos, ni reloj
parado. Tiene `FechaCreacion` y `FechaCierre`, que dan una duración total — y la duración total no
es ninguno de los dos tiempos que se miden.

**Y encaja con lo que usted describió**: el operador del centro de control recibe la llamada
—«no funciona el poste 3»— valida contra el SCADA y lanza la correctiva. Eso es exactamente §6.1.1,
con el matiz de que **solo operadores autorizados** pueden dar el aviso, «para evitar notificar
incidencias a través de terceras personas».

---

## 4. GIMAN: el sistema que estamos replicando

`2-MANTENIMIENTO.pdf` §11. ETRA describe su herramienta **GIMAN**, un GMAO con interfaz **web y
Android**. Conviene mirarlo de frente: **el SGMC es un GIMAN pobre montado sobre AppSheet.**

Eso no es malo. Es útil, porque da un mapa de qué falta y en qué orden.

| Módulo GIMAN | En el SGMC |
|---|---|
| Mapa con código de colores por estado | Parcial. AppSheet lo da |
| Gestión de inventario | **Sí** — `ACT_Activos`, `TIP_TiposActivo` |
| Gestión de recursos | Parcial — `USR_Usuarios`, `ASG_AsignacionZona` |
| Mantenimiento preventivo | Parcial — falta la capa de tareas |
| Mantenimiento correctivo | **No** — sin criticidad, sin niveles, sin SLA |
| Almacén y existencias | **No** |
| SAT | **No** |
| Gestión documental | Parcial — `FOT_Fotografias` |
| Flotas de vehículos | No, y es opcional también en GIMAN |

### Lo que GIMAN hace y confirma decisiones nuestras

**Atributos por tipo de elemento.** GIMAN deja definir atributos adicionales por tipo —código,
dimensiones, color— sin tocar el esquema. Es el patrón que resuelve el problema de que un poste SOS
y un servidor no comparten propiedades. **En AppSheet sobre Sheets no se puede hacer**: no hay
esquema dinámico. Se paga con columnas vacías o con tablas por familia. Merece estar escrito como
limitación, no descubrirse en producción.

**Generación programada de tareas.** Se configura fecha de inicio y periodicidad, el sistema genera
las tareas solas, **y hay que activarlas antes de que sean ejecutables**. Ese paso intermedio es
inteligente: separa lo generado de lo comprometido, y deja reprogramar sin borrar.

Y aquí está la limitación de fondo, que ya conocíamos y ahora tiene consecuencia: **AppSheet gratuito
no ejecuta bots programados**. La generación automática que GIMAN da por sentada, nosotros no la
tenemos. Por eso las órdenes se crean a mano o por carga, y por eso la creación masiva es el
problema de usabilidad que usted señaló.

**Jerarquía de recursos.** Técnico → Supervisor/Capataz → Cuadrilla. Nuestro `ASG_AsignacionZona`
asigna técnico a zona, sin brigada intermedia.

### Y una cosa que GIMAN **no** tiene

El técnico en GIMAN se registra con **nombre, identificador y empresa**. Nada más. **No hay
certificaciones, ni especialidades, ni vigencias.**

Es un dato en contra de la propuesta de perfiles —electricista, alturas, electrónico, ayudante,
SISO— que usted planteó. No la invalida: un GMAO genérico de 2017 no es la vara. Pero conviene
saber que la herramienta de referencia resolvió la asignación **por zona y por brigada**, no por
certificación, y aun así funcionó.

Refuerza dejarlo en Fase 2.

---

## 5. Qué confirma y qué contradice nuestro modelo

### Confirma

| Decisión nuestra | Qué la respalda |
|---|---|
| Capa `TAR_Tareas` entre tipo y trabajo | GIMAN §11.1.5.1: el tipo de tarea se define **sobre el tipo de elemento** |
| Retirar `ACT_Activos.FrecuenciaID` | La manta: el SOS tiene tarea semanal, mensual y trimestral |
| Estado de alta/baja en el activo | GIMAN §11.1.3.1 lo lleva como campo del elemento |
| Fotografías con coordenada como evidencia | Cliente Android de GIMAN, para «introducir información en tiempo real» |
| Histórico que no se borra | «Seguimiento y tratamiento estadístico de averías» |

### Contradice o deja corto

| Hueco | Dónde duele |
|---|---|
| Sin criticidad ni SLA en la orden | Es lo que mide la interventoría por disponibilidad |
| Sin niveles N1/N2/N3 ni escalado | Una orden que el técnico no resuelve no tiene a dónde ir |
| Sin reloj parado | Cualquier espera de repuesto cuenta como incumplimiento |
| Sin almacén ni repuestos | El informe mensual pide «Repuestos y Herramientas» |
| Sin firma de tercero en la tarea | `PRUEBA MENSUAL CON INTERVENTORÍA` la exige |
| Sin brigada entre técnico y zona | GIMAN §11.1.4.3 |

**Ninguno de los seis bloquea la Fase B.** Todos son de correctivo o de recurso, y la Fase B es
cableado de referencias sobre el preventivo. Pero los seis son columnas, y **añadir columnas después
de producción es el problema que usted pidió evitar**.

---

## 6. Lo que sigue faltando, y no está en ningún documento

Estas no salen de leer más. Salen de preguntar en operación:

1. **¿El Sisga tiene SLA contractuales propios?** Los de ETRA son de otro corredor. Si el Sisga
   tiene los suyos, son otros números; si no tiene, hay que decidir si el sistema los mide igual.
2. **¿Quién puede dar el aviso de una correctiva?** ETRA restringe a operadores autorizados. En el
   Sisga, ¿el operador de turno, el supervisor, cualquiera con la app?
3. **¿Existe almacén de repuestos gestionado**, o los repuestos se anotan en texto libre?
4. **Las 600 cajas de fibra**: ¿hay inventario o hay que levantarlo?
5. **¿Cuántas estructuras** —puentes, viaductos— tienen paso de fibra?
6. **El inventario real del Sisga.** Trabajamos con 355 activos de un maestro que usted describió
   como «muy similar» al del Sisga, no el del Sisga. **Es el vacío más grande que queda.**

La 6 es la que más pesa: todo el dimensionamiento —1.916 órdenes al año, la cuota de 15 GB que se
agota en 4,1 años— está calculado sobre un inventario que no es el de este corredor.

---

*Alimenta `MODELO_EVOLUCION_FASE_2.md`. Ninguna pieza de aquí es ejecutable hasta que tenga su*
*`ESPEC`, su `PRUEBA` y el veredicto del arquitecto.*
