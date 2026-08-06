# Definición funcional y mesa de trabajo — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Dirigido a:** Líder funcional y equipo de Operaciones / ITS
**Fecha:** 6 de agosto de 2026
**Estado:** Documento de validación. No es un informe de avance: es un cuestionario estructurado.

---

## Cómo usar este documento

Este documento no pide aprobación. Pide **decisiones**.

Está organizado en tres partes:

- **Parte I y II** describen cómo entendemos hoy que debe funcionar el sistema, expresado como
  flujos de uso verificables. Léelas para confirmar o corregir.
- **Parte III** es el cuestionario. Cada punto sigue el mismo molde: *qué encontramos*, *por qué
  importa*, *qué proponemos*, *qué necesitamos que respondas*. Hay un espacio de respuesta.
- **Parte IV** muestra cómo cada respuesta se convierte en trabajo y en fecha. El roadmap no
  existe todavía porque depende de lo que respondas aquí.

Sugerencia de mesa: dos sesiones de dos horas. La primera recorre las Partes I y II y valida los
flujos. La segunda resuelve el cuestionario decisión por decisión. Lo que no se decida queda con
el supuesto por defecto que está declarado en cada punto, y ese supuesto se vuelve vinculante.

---

## Contexto: por qué volvemos a la definición

El SGMC se planteó en julio de 2026 como un producto mínimo viable de 8 días sobre Google
AppSheet, a partir de una ERS v1.0 y un formulario de levantamiento diligenciado el 25 de julio.
Se construyó, y hoy existe una aplicación publicada con un modelo de datos de 24 tablas, 34
activos catalogados y órdenes de trabajo registradas.

En el camino el alcance mutó. El modelo pasó de 17 a 24 tablas, aparecieron dos maneras distintas
de definir los formularios de inspección, y las fotografías y firmas quedaron modeladas por
duplicado. Ninguna de esas mutaciones pasó por una validación funcional.

Una auditoría del 6 de agosto de 2026 verificó ocho bloqueantes contra el archivo real. Al
revisarlos uno a uno aparece un patrón: **la mayoría no son errores de programación, son
preguntas de negocio que nadie respondió.** No se puede configurar el filtro de seguridad sin
saber si la sede de un activo es la unidad funcional o el peaje. No se puede cerrar el
requerimiento de evidencia fotográfica sin saber cuántas fotos exige realmente una inspección.

Por eso el paso siguiente no es seguir construyendo. Es definir, validar contigo, y recién
entonces ejecutar.

---

# PARTE I — Alcance funcional propuesto

## 1. Qué hace el sistema

El SGMC reemplaza el registro en papel del mantenimiento del corredor por un registro digital
con evidencia verificable de que el trabajo se hizo, dónde se hizo y en qué estado quedó el activo.

## 2. Actores

| Actor | Dónde trabaja | Responsabilidad |
|---|---|---|
| **Técnico** | Celular, con o sin señal | Ejecuta la inspección o reparación en el activo y registra la evidencia |
| **Supervisor** | Navegador | Programa y asigna el trabajo, revisa la evidencia y aprueba |
| **Administrador** | Navegador | Mantiene usuarios, catálogos, inventario de activos y formularios de inspección |
| **Consulta** | Navegador | Lee y exporta reportes, sin modificar |

Pendiente de confirmar si **Interventoría / ANI** es un actor con acceso al sistema o un
destinatario de reportes exportados. Ver decisión D-13.

## 3. Alcance propuesto para el primer sprint productivo

**Entra:** mantenimiento preventivo programado, sobre los tipos de activo que se prioricen,
ejecutado por técnico con evidencia fotográfica, firma y validación GPS, con asignación y
aprobación por parte del supervisor, y un tablero básico de cumplimiento.

**No entra por ahora, y se confirma en la mesa:** mantenimiento correctivo iniciado desde el
campo sin OT previa, generación automática de OT por frecuencia, integración con Power BI o GLPI,
gestión de repuestos e inventario, y firma de interventoría.

Este corte es una propuesta. Las decisiones D-01, D-03 y D-09 lo redefinen.

---

# PARTE II — Flujos funcionales

Cada flujo se expresa con precondiciones, pasos, excepciones y criterios de aceptación
verificables, de modo que sirva a la vez como definición funcional y como base de las pruebas de
aceptación de usuario.

---

## CU-01 — El técnico ejecuta un mantenimiento preventivo en campo

**Actor:** Técnico
**Cubre:** RF-002 offline, RF-006 escaneo QR, RF-007 y RF-008 checklist dinámico, RF-010 fotos,
RF-012 geofencing, RF-013 firma
**Criticidad:** Máxima. Es el flujo que justifica el sistema.

**Precondiciones**
1. El técnico tiene la app instalada y sesión iniciada con su cuenta corporativa.
2. Sincronizó al menos una vez con señal, y su celular tiene los activos de su zona descargados.
3. Existe una orden de trabajo asignada a él, o el activo admite intervención directa (D-06).
4. El activo tiene su coordenada real registrada en el sistema.

**Flujo principal**

| # | Paso | Qué hace el sistema |
|---|---|---|
| 1 | El técnico abre la app al inicio de la jornada, con señal | Sincroniza y descarga solo los activos y OT de su zona |
| 2 | Se desplaza al activo, ya sin señal | Opera contra la caché local |
| 3 | Abre "Mis OT" y elige la orden, o escanea el código QR del equipo | Abre la ficha del activo |
| 4 | Presiona "Iniciar mantenimiento" | Registra hora de inicio y precarga técnico, activo y OT |
| 5 | El sistema abre el checklist | Selecciona el formulario que corresponde al tipo de activo |
| 6 | El técnico responde el checklist | Valida obligatorias, rangos numéricos y unidades |
| 7 | Toma las fotografías requeridas | Comprime a 600 px para no agotar los datos móviles |
| 8 | Registra el estado final del activo | Operativo, en mantenimiento o fuera de servicio |
| 9 | Firma | Captura la firma manuscrita |
| 10 | Presiona guardar | Captura posición y precisión GPS y valida la distancia al activo |
| 11 | Guardado local | Queda en cola de sincronización con indicador visible |
| 12 | Al recuperar señal | Sube en segundo plano sin intervención del técnico |

**Excepciones**

| Código | Situación | Comportamiento propuesto | Decisión |
|---|---|---|---|
| E-01 | El técnico está a más de 1 km de la coordenada del activo | Bloquea el guardado con mensaje en texto plano | D-02 |
| E-02 | El GPS no fija posición o su precisión es mala (túnel, cañón) | Pendiente de definir. Hoy bloquearía y el técnico perdería el trabajo | **D-04** |
| E-03 | La batería se agota o la app se cierra a mitad del formulario | Debe conservar el borrador local | D-05 |
| E-04 | El activo no puede intervenirse (acceso cerrado, riesgo, falta repuesto) | Se registra como pendiente con motivo y se marca segunda visita | **D-07** |
| E-05 | El técnico llega a un activo que no está en el inventario | Pendiente de definir | **D-08** |
| E-06 | Dos técnicos registran sobre la misma OT | Pendiente de definir | D-06 |

**Postcondición.** Existe un registro de mantenimiento con: fecha y horas, checklist respondido,
fotografías, firma, coordenada de cierre, precisión GPS y estado final del activo.

**Criterios de aceptación**
- CA-01.1 El registro se completa de principio a fin sin señal celular en ningún momento.
- CA-01.2 Al recuperar señal, el registro aparece en el backend sin acción del técnico.
- CA-01.3 Estando a más de 1 km del activo, el sistema impide guardar.
- CA-01.4 Estando junto al activo, el sistema permite guardar.
- CA-01.5 El checklist que abre corresponde al tipo del activo escaneado.
- CA-01.6 Las fotografías quedan asociadas al mantenimiento y comprimidas.
- CA-01.7 Un mantenimiento sin firma no puede cerrarse.

> **Advertencia sobre el estado actual.** Este flujo nunca se ha ejecutado completo. La tabla de
> mantenimientos está vacía. Las coordenadas de los 34 activos son todas iguales y apuntan a
> Bogotá, de modo que CA-01.3 y CA-01.4 hoy fallan ambos. Ver D-01.

---

## CU-02 — El supervisor programa y asigna una orden de trabajo

**Actor:** Supervisor | **Cubre:** RF-014

**Precondiciones.** El activo existe en el inventario y hay un técnico activo en la zona.

**Flujo principal**
1. El supervisor entra al portal web y abre Órdenes de Trabajo.
2. Crea una orden: selecciona activo, técnico responsable, fecha programada y tipo de trabajo.
3. El sistema asigna el número de orden y la deja en estado inicial.
4. Un bot envía correo al técnico con el detalle de la asignación.
5. El técnico sincroniza y la orden aparece en su celular.

**Criterios de aceptación**
- CA-02.1 El número de orden es único y se genera solo.
- CA-02.2 El técnico recibe el correo dentro de los 5 minutos siguientes.
- CA-02.3 La orden aparece en el celular del técnico asignado y no en el de otros.

**Sin resolver.** Los estados de la orden que hoy existen en los datos son Asignada, Cerrada y
Suspendida, pero no hay definición de quién puede pasar de uno a otro ni bajo qué condición. Ver
**D-06**.

---

## CU-03 — El supervisor revisa y aprueba

**Actor:** Supervisor | **Cubre:** RF-014, RF-015

1. Al sincronizar el técnico, el mantenimiento aparece en el portal.
2. El supervisor revisa checklist, fotografías, firma y coordenada de cierre.
3. Aprueba, o lo devuelve al técnico con observación.
4. Al aprobar, la orden se cierra y el indicador de cumplimiento se actualiza.

**Criterios de aceptación**
- CA-03.1 El supervisor ve la coordenada de cierre y su precisión, no solo el resultado.
- CA-03.2 Una orden no puede cerrarse sin mantenimiento aprobado.

**Sin resolver.** El modelo tiene un campo de aprobación del supervisor, pero no existe el flujo
de rechazo: qué pasa con un mantenimiento devuelto, si el técnico lo corrige sobre el mismo
registro o crea uno nuevo, y si el rechazo notifica. Ver **D-07**.

---

## CU-04 — Alerta automática por activo fuera de servicio

**Actor:** Sistema | **Cubre:** RF-016

1. El técnico cierra un mantenimiento con estado final "Fuera de servicio".
2. Al sincronizar, se dispara el bot.
3. El bot genera un informe en PDF con los datos de la falla, la ubicación y las fotografías.
4. Envía correo prioritario al CCO y al supervisor de la zona.

**Criterios de aceptación**
- CA-04.1 El correo llega dentro de los 10 minutos posteriores a la sincronización.
- CA-04.2 El PDF incluye fotografías y coordenada.
- CA-04.3 No se envían alertas por mantenimientos con estado operativo.

**Sin resolver.** A quién exactamente se notifica, si hay escalamiento cuando nadie responde, y
si un activo fuera de servicio debe generar automáticamente una orden correctiva. Ver **D-08**.

---

## CU-05 — El administrador mantiene el inventario y los formularios

**Actor:** Administrador | **Cubre:** RF-005, RF-007

1. Da de alta un activo con su código, tipo, sede, PR, calzada, sentido, coordenada real,
   frecuencia de mantenimiento y código QR.
2. Define o ajusta el formulario de inspección de un tipo de activo: secciones, preguntas, tipo
   de respuesta, obligatoriedad, rangos y si la pregunta exige fotografía.
3. Publica el cambio y los técnicos lo reciben en la siguiente sincronización.

**Criterios de aceptación**
- CA-05.1 Un activo nuevo queda disponible en el celular del técnico de su zona tras sincronizar.
- CA-05.2 Modificar una pregunta no altera las respuestas ya registradas históricamente.

**Sin resolver.** CA-05.2 hoy no se cumple: el detalle de checklist guarda el texto de la
pregunta, no su identificador, así que un cambio de redacción rompe la comparación histórica.
Ver **D-11**. Y si el administrador puede editar formularios en producción sin control de
versión. Ver **D-12**.

---

## CU-06 — Reportes y tablero

**Actor:** Supervisor, Consulta, Dirección | **Cubre:** RF-015

Este caso de uso **no está definido**. Es el vacío más grande del proyecto: el sistema captura
datos desde julio pero nadie ha especificado qué debe producir con ellos.

Lo que hoy se menciona en documentos previos, sin definición operativa:
cumplimiento de mantenimientos ejecutados contra programados, tiempo promedio de atención,
disponibilidad de activos por zona, y mapa de activos fuera de servicio.

Ninguno tiene fórmula, periodicidad, destinatario ni formato acordado. Ver **D-09 y D-10**.

---

# PARTE III — Decisiones que necesitamos

Catorce decisiones, agrupadas en cinco bloques. Cada una bloquea trabajo concreto.

---

## Bloque A — Datos maestros

### D-01. Coordenadas reales de los activos

**Qué encontramos.** Los 34 activos del inventario tienen exactamente la misma coordenada:
`4.728512, -74.114531`. Ese punto está en Bogotá, no en el corredor.

**Por qué importa.** Toda la promesa de evidencia verificable del sistema descansa en el
geofencing, y el geofencing compara la posición del técnico contra esa coordenada. Con el dato
actual, un técnico parado frente a un poste SOS en Machetá no podrá cerrar nunca su
mantenimiento, y en cambio cualquiera en ese punto de Bogotá validaría los 34 activos. La regla
está bien programada; el dato la vuelve inútil.

**Para qué sirve responder.** Es el prerrequisito absoluto de la salida a campo. Sin coordenadas
reales no hay piloto posible.

**Proponemos.** Levantar la coordenada de los 34 activos en un recorrido de corredor, capturando
con el mismo celular que usará el técnico, y cargarlas al inventario. Aprovechar el recorrido
para verificar que el código QR físico esté instalado y legible.

**Necesitamos que respondas**
- ¿Quién hace el recorrido y en qué fecha?
- ¿Existe ya un levantamiento topográfico o un inventario georreferenciado del que podamos tomar
  las coordenadas sin salir a campo?
- ¿Los 34 activos del sistema son todo el inventario, o falta cargar más?

**Respuesta:**

**Desbloquea:** el geofencing, el piloto de campo y los criterios CA-01.3 y CA-01.4.

---

### D-02. Radio de tolerancia del geofencing

**Qué encontramos.** El radio definido es 1,0 km, heredado de la ERS original.

**Por qué importa.** Un kilómetro es mucho para un poste SOS en vía abierta, donde 100 metros
bastarían para probar presencia. Y puede ser poco para un activo lineal como un tramo de fibra
óptica, donde el técnico puede intervenir legítimamente a varios kilómetros del punto registrado.
Un radio único para 18 tipos de activo muy distintos es una simplificación que conviene revisar.

**Proponemos.** Radio por tipo de activo: 200 m para activos puntuales (SOS, CCTV, PMV, básculas),
y un tratamiento distinto para fibra óptica y activos lineales.

**Necesitamos que respondas**
- ¿1 km es una exigencia contractual o de interventoría, o es un valor elegido por el equipo?
- ¿Aceptas radio diferenciado por tipo de activo?

**Respuesta:**

**Desbloquea:** la configuración definitiva de la regla de validación.

---

### D-03. Qué significa la sede de un activo

**Qué encontramos.** Los 11 usuarios están registrados en la sede 1, que es el CCO. Los 34
activos están repartidos entre las sedes 7 a 10, que son las unidades funcionales UF1 a UF4. La
intersección es vacía.

**Por qué importa.** El filtro de seguridad descarga al celular del técnico solo los activos de
su sede. Con los datos actuales, cada técnico descargaría **cero activos** y la app quedaría
vacía en sus manos el primer día de piloto. El problema de fondo es que la misma columna se está
usando con dos significados distintos: para los usuarios significa el sitio físico donde trabajan
(CCO, peaje, báscula) y para los activos significa el tramo del corredor donde están (UF1 a UF4).

**Proponemos.** Separar los dos conceptos: la unidad funcional es un atributo del activo, y la
zona de trabajo es un atributo del usuario. Un técnico puede tener asignada más de una unidad
funcional.

**Necesitamos que respondas**
- ¿Un técnico atiende una unidad funcional completa, un tramo, o todo el corredor?
- ¿Un técnico del CCO puede intervenir activos de cualquier UF?
- ¿Qué debe ver un supervisor: su zona o todo?

**Respuesta:**

**Desbloquea:** el filtro de seguridad, y con él la descarga de datos al celular. Sin esto el
piloto no arranca.

---

## Bloque B — Operación en campo

### D-04. Qué hacer cuando el GPS falla

**Qué encontramos.** El sistema captura la precisión del GPS pero no define qué hacer cuando es
mala. El plan original ya señalaba el riesgo de falsos negativos y proponía un mecanismo de
excepción supervisada, que nunca se especificó.

**Por qué importa.** En túnel, en cañón o bajo copa densa, el celular puede reportar una posición
con error de cientos de metros o no fijar nada. Si el sistema bloquea sin salida, el técnico
pierde el trabajo de una hora y el sistema pierde su confianza el primer día. Si el sistema deja
pasar todo, el geofencing no sirve para nada. Este es el punto donde el control se gana o se
pierde.

**Proponemos.** Permitir el cierre con excepción cuando la precisión reportada sea peor que un
umbral, exigiendo al técnico un motivo escrito y una fotografía del activo, marcando el registro
como cerrado con excepción y notificando al supervisor para revisión. La excepción no se oculta:
queda visible en el reporte.

**Necesitamos que respondas**
- ¿Aceptas el cierre con excepción, o prefieres bloqueo estricto y que el técnico regrese?
- Si lo aceptas, ¿quién autoriza: se marca solo y el supervisor revisa después, o requiere
  autorización previa por llamada al CCO?
- ¿Qué porcentaje de excepciones sería aceptable antes de que se considere un problema?

**Respuesta:**

**Desbloquea:** la excepción E-02 de CU-01 y buena parte de la aceptación del sistema por los
técnicos.

---

### D-05. Interrupción a mitad de formulario

**Qué encontramos.** No hay definición de qué ocurre si el técnico cierra la app, se le agota la
batería o lo interrumpen a mitad del checklist.

**Por qué importa.** Una inspección de poste SOS son 15 preguntas más fotografías. Perder eso por
una llamada entrante es la clase de fricción que hace que un técnico vuelva al papel.

**Proponemos.** Guardado del borrador local, con la inspección visible como "en curso" hasta que
se cierre formalmente.

**Necesitamos que respondas**
- ¿Un mantenimiento puede quedar abierto de un día para otro, o debe cerrarse en la jornada?
- ¿Un mantenimiento iniciado y no cerrado cuenta como incumplimiento?

**Respuesta:**

**Desbloquea:** la excepción E-03 y la definición del indicador de cumplimiento.

---

### D-06. Ciclo de vida de la orden de trabajo

**Qué encontramos.** Las órdenes registradas tienen estados Asignada, Cerrada y Suspendida, pero
no hay regla que diga quién cambia cada estado ni bajo qué condición. Además, el único checklist
existente apunta a una orden que no existe, señal de que hoy se puede registrar trabajo sin
orden válida.

**Por qué importa.** Sin ciclo de vida definido no hay indicador de cumplimiento confiable: no se
puede medir "ejecutado contra programado" si no está claro cuándo una orden cuenta como vencida,
quién la suspende y si un trabajo puede existir sin orden.

**Proponemos.** Estados: Programada, Asignada, En ejecución, En revisión, Cerrada, Suspendida y
Vencida. El técnico mueve hasta En revisión; solo el supervisor cierra o suspende; el sistema
marca Vencida por fecha.

**Necesitamos que respondas**
- ¿Un técnico puede ejecutar un mantenimiento sin orden previa? Es el caso típico del correctivo
  detectado en ruta.
- ¿Cuándo una orden se considera vencida: al día siguiente de la fecha programada, al cierre de
  semana, al cierre de mes?
- ¿Quién puede suspender una orden y qué motivos son válidos?
- ¿Se permite reasignar una orden a otro técnico y queda traza?

**Respuesta:**

**Desbloquea:** el indicador de cumplimiento, el flujo CU-02 y la excepción E-06.

---

### D-07. Trabajo incompleto, segunda visita y devoluciones

**Qué encontramos.** El modelo prevé marcar que se requiere una segunda visita con su motivo, y
la aprobación del supervisor, pero ninguno de los dos flujos está definido.

**Por qué importa.** El caso real más común no es el mantenimiento perfecto: es el técnico que
llega y no puede terminar por falta de repuesto, por lluvia o por acceso cerrado. Si el sistema
no modela ese caso, el técnico va a forzar un cierre falso o no va a registrar nada.

**Proponemos.** Cierre parcial con motivo tipificado, que genera automáticamente una orden de
seguimiento asociada a la original. Y devolución del supervisor con observación, que reabre el
mantenimiento al mismo técnico conservando la traza del rechazo.

**Necesitamos que respondas**
- ¿Qué motivos de trabajo incompleto son válidos? Necesitamos la lista para el desplegable.
- ¿La segunda visita es una orden nueva o la misma orden reabierta?
- Cuando el supervisor devuelve, ¿el técnico corrige el registro original o crea uno nuevo?
- ¿El rechazo debe notificar por correo?

**Respuesta:**

**Desbloquea:** las excepciones E-04, el flujo CU-03 y el cálculo real de cumplimiento.

---

### D-08. Activos no inventariados y correctivo desde campo

**Qué encontramos.** No hay ruta para un activo que el técnico encuentra en vía y que no está en
el sistema, ni para una falla detectada fuera de programación.

**Proponemos.** Permitir al técnico levantar un reporte de novedad con foto, coordenada y
descripción, que llega al supervisor como solicitud de alta de activo o de orden correctiva, sin
que el técnico pueda crear activos directamente.

**Necesitamos que respondas**
- ¿Los técnicos deben poder reportar novedades de activos no inventariados?
- Un activo que queda fuera de servicio, ¿debe generar automáticamente una orden correctiva o el
  correctivo se gestiona por fuera del sistema?

**Respuesta:**

**Desbloquea:** la excepción E-05 y el alcance de CU-04.

---

## Bloque C — Alcance de los formularios

### D-09. Cuántos tipos de activo entran al primer sprint

**Qué encontramos.** Hay 18 tipos de activo y 18 formularios declarados, pero solo el de postes
SOS tiene sus preguntas construidas: 15 preguntas. Los otros 17 están vacíos. Además la columna
que conecta cada tipo de activo con su formulario está vacía en los 18 tipos, de modo que hoy la
app no sabría qué checklist abrir ni siquiera para el SOS.

**Por qué importa.** Construir los 17 bancos restantes son del orden de 250 preguntas que alguien
con criterio técnico debe redactar, con sus rangos, unidades y obligatoriedad. Es la tarea más
grande que queda y es trabajo tuyo y de tu equipo técnico, no de configuración. Intentar
construir los 18 a la vez es lo que hará que el proyecto se estanque otro mes.

**Proponemos.** Arrancar con tres tipos que cubran la mayor cantidad de activos y de casuística
— postes SOS, CCTV y paneles de mensaje variable — validar el ciclo completo en campo con ellos,
y luego incorporar el resto en tandas quincenales según criticidad.

**Necesitamos que respondas**
- ¿Cuáles tres tipos priorizamos? ¿Coincides con SOS, CCTV y PMV?
- ¿Quién redacta y valida técnicamente las preguntas de cada tipo, y con qué disponibilidad?
- ¿Existen formatos de inspección en papel vigentes que podamos transcribir en lugar de redactar
  desde cero? Sería la vía más rápida y la que mejor refleja la práctica real.
- ¿Hay un requisito contractual o de interventoría sobre qué debe contener una inspección?

**Respuesta:**

**Desbloquea:** el alcance real del primer sprint y su fecha. Es la decisión que más mueve el
cronograma.

---

### D-10. Evidencia fotográfica y firmas

**Qué encontramos.** El requerimiento habla de hasta 6 fotografías. El modelo de datos las
soporta de dos maneras a la vez, incompatibles entre sí: dos campos fijos dentro del registro de
mantenimiento (imagen de inicio e imagen final) y una tabla separada sin límite. Lo mismo ocurre
con las firmas. Las tablas separadas están vacías.

**Por qué importa.** Si no se decide, el técnico terminará firmando dos veces y adjuntando fotos
en dos lugares distintos, o peor, la evidencia quedará repartida y los reportes no la
encontrarán completa.

**Proponemos.** Si se mantienen las 6 fotografías, la única vía viable es la tabla separada, y
hay que retirar los campos fijos del registro de mantenimiento. Firma del técnico siempre;
firma del supervisor solo si efectivamente firma en campo.

**Necesitamos que respondas**
- ¿Cuántas fotografías exige realmente una inspección: un mínimo obligatorio y un máximo?
- ¿Deben ser fotografías tipificadas, es decir "antes", "después", "novedad", o libres?
- ¿El supervisor firma en campo junto al técnico, o su validación es la aprobación en el portal?
- ¿La firma tiene valor contractual frente a interventoría o es control interno?

**Respuesta:**

**Desbloquea:** el diseño definitivo del formulario y el cumplimiento verificable de RF-010 y
RF-013.

---

### D-11. Trazabilidad histórica de las respuestas

**Qué encontramos.** El detalle de las inspecciones guarda el texto de la pregunta, no su
identificador. Si alguien reformula una pregunta, los registros anteriores dejan de ser
comparables con los nuevos.

**Por qué importa.** Si el sistema debe mostrar la evolución de un activo en el tiempo, o
demostrar ante interventoría que se aplicó el mismo criterio durante un periodo, esta trazabilidad
es indispensable. Si el sistema solo debe dejar constancia de cada visita por separado, no lo es.

**Proponemos.** Guardar el identificador de la pregunta junto al texto, y versionar el formulario
cuando cambie.

**Necesitamos que respondas**
- ¿Necesitas comparar la misma pregunta a lo largo del tiempo para un activo?
- ¿El sistema debe poder reconstruir cómo era un formulario en una fecha pasada?

**Respuesta:**

**Desbloquea:** el criterio CA-05.2 y los reportes históricos.

---

## Bloque D — Reportes

### D-12. Qué debe entregar el sistema

**Qué encontramos.** Ningún reporte está definido. Se mencionan indicadores en documentos previos
pero ninguno tiene fórmula, periodicidad ni destinatario.

**Por qué importa.** Este es el vacío más costoso del proyecto. Todo lo que el técnico captura en
campo existe para producir algo, y ese algo nunca se especificó. Definir el reporte al final
obliga casi siempre a volver atrás y capturar datos que no se pidieron. Definirlo ahora es lo que
garantiza que el formulario pida lo correcto.

**Necesitamos que respondas**, para cada reporte que necesites:
- ¿Qué debe mostrar y para tomar qué decisión?
- ¿Quién lo recibe y con qué periodicidad: diario, semanal, mensual?
- ¿En qué formato: pantalla, PDF por correo, Excel exportable?
- ¿Alguno se entrega a un tercero, interventoría o ANI, con formato obligatorio?

Reportes candidatos que proponemos, para que confirmes, descartes o completes:

| Reporte | Propósito | Destinatario | Periodicidad |
|---|---|---|---|
| Cumplimiento del plan de mantenimiento | Ejecutado contra programado por zona y por técnico | Supervisor, Dirección | Mensual |
| Activos fuera de servicio | Qué está caído, desde cuándo y quién lo atiende | CCO | Diario |
| Hoja de vida del activo | Historial completo de intervenciones de un equipo | Supervisor, Interventoría | A demanda |
| Certificado de mantenimiento | Constancia de una intervención con evidencia y firma | Interventoría | Por intervención |
| Productividad del técnico | Mantenimientos ejecutados y tiempo promedio | Supervisor | Semanal |
| Excepciones de geofencing | Cierres con GPS fuera de rango o de baja precisión | Supervisor | Semanal |

**Respuesta:**

**Desbloquea:** CU-06 completo y, hacia atrás, la validación de que los formularios capturan lo
necesario.

---

### D-13. Definición de los indicadores

**Qué encontramos.** Se habla de cumplimiento, disponibilidad y tiempo de atención sin fórmula.

**Por qué importa.** "Disponibilidad de activos" puede significar tres cosas distintas según se
mida por tiempo, por cantidad o ponderado por criticidad, y cada una da un número diferente ante
la misma realidad. Si ese número va a un informe de interventoría, la definición debe estar
acordada antes y no después.

**Necesitamos que respondas**
- Cumplimiento: ¿se calcula sobre órdenes cerradas en fecha, o basta con que se hayan ejecutado?
  ¿Una orden cerrada con excepción de GPS cuenta como cumplida?
- Disponibilidad: ¿por tiempo fuera de servicio, por cantidad de activos, ponderada por
  criticidad?
- ¿Existe una meta contractual de disponibilidad o de tiempo de atención frente a la ANI, que el
  sistema deba reportar?

**Respuesta:**

**Desbloquea:** el tablero y cualquier reporte a terceros.

---

## Bloque E — Gobierno

### D-14. Usuarios, licenciamiento y gobierno del cambio

**Qué encontramos.** Hay 11 usuarios registrados, dos de ellos inactivos. El presupuesto
declarado en el plan original fue de 100 USD mensuales, y AppSheet se cobra por usuario activo.
No hay definición de quién puede modificar la aplicación en producción.

**Necesitamos que respondas**
- ¿Cuántos técnicos usarán el sistema en régimen, más allá de los 10 del piloto?
- ¿El personal de interventoría o de la ANI tendrá acceso, aunque sea de consulta?
- ¿Quién es el responsable funcional que autoriza cambios en producción?
- ¿Cuánto tiempo debe conservarse la evidencia fotográfica y dónde se respalda?

**Respuesta:**

**Desbloquea:** el dimensionamiento de licencias y el procedimiento de cambios.

---

# PARTE IV — De las respuestas al roadmap

El roadmap no está escrito porque depende de esta mesa. Este es el mapa de dependencias: qué
habilita cada decisión.

| Decisión | Trabajo que habilita | Quién ejecuta | Bloquea |
|---|---|---|---|
| D-01 | Levantamiento y carga de coordenadas reales | Operaciones, recorrido de corredor | Todo el campo |
| D-03 | Realineación de sedes y configuración del filtro | Configuración | Descarga de datos al celular |
| D-09 | Construcción de los bancos de preguntas | Líder técnico y equipo ITS | Alcance del sprint |
| D-10 | Rediseño del formulario y limpieza de evidencia duplicada | Configuración | Diseño del formulario |
| D-12, D-13 | Construcción de reportes y tablero | Configuración | Entregables a Dirección e Interventoría |
| D-02, D-04, D-05 | Reglas de validación y excepción | Configuración | Aceptación en campo |
| D-06, D-07, D-08 | Estados, notificaciones y flujos de excepción | Configuración | Indicador de cumplimiento |
| D-11 | Versionado de formularios | Configuración | Reportes históricos |
| D-14 | Licencias y procedimiento de cambios | Dirección | Salida a producción |

**La ruta crítica son D-01 y D-09.** Ambas son trabajo de tu equipo, no de configuración, y ambas
se miden en semanas, no en días. El cronograma del proyecto lo fijan esas dos y no las demás.

Una vez cerrada la mesa, el orden de ejecución es:

1. **Definición** — esta mesa y sus respuestas.
2. **Datos** — coordenadas reales, mapeo de formularios por tipo, realineación de sedes,
   construcción de los bancos de preguntas priorizados.
3. **Configuración** — reglas de validación, filtro de seguridad, formularios, bots y reportes.
4. **Prueba controlada** — un mantenimiento completo de extremo a extremo ejecutado por una
   persona, primero con señal y luego en modo avión. El criterio de cierre es que existan
   registros reales en la base, verificados leyendo el archivo.
5. **Piloto** — los 10 celulares, solo después de que el paso 4 haya funcionado.
6. **Producción y evolución** — resto de tipos de activo, integraciones y respaldo automático.

---

# PARTE V — Acta de la mesa

| Campo | |
|---|---|
| Fecha de la sesión | |
| Participantes | |
| Decisiones cerradas | |
| Decisiones aplazadas y hasta cuándo | |
| Supuestos que quedan vinculantes | |
| Responsable de D-01 (coordenadas) y fecha comprometida | |
| Responsable de D-09 (preguntas) y fecha comprometida | |
| Próxima sesión | |

Firma del líder funcional: ______________________  Fecha: ____________

---
*Documento de validación funcional. Las decisiones aquí registradas son la base del roadmap de
implementación y del alcance contractual del sprint.*
