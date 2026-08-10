> # Documento historico. NO SE APLICA.
>
> Construccion inicial. **La aplicacion se reconstruyo desde cero** el 2026-08-09 por otro camino.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# Prompt de construcción del SGMC

Directiva de ejecución para el agente que va a reparar y completar el sistema. Sustituye a
`PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md`, cuyo Paso 2 ordenaba configurar sobre decisiones que
no estaban tomadas y sobre un modelo que no está cableado.

---

## Contexto que debes asumir como cierto

Lee primero `CLAUDE.md`, `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` y la sección 10 de
`docs/AUDITORIA_PLAN_Y_ROADMAP.md`. Lo esencial:

- El backend que corre la aplicación es el Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.
  El Excel local es un registro paralelo que diverge. **Ante discrepancia manda producción.**
- **Las referencias del modelo no existen en la aplicación.** `MAN_Mantenimientos.OTID` es de tipo
  `Text`, y esa tabla no tiene ninguna columna hacia el activo. La cadena Activo → Orden →
  Mantenimiento está en el papel y no en la app. Este es el defecto raíz: explica las cuatro
  tablas vacías y que el flujo nunca se haya ejecutado.
- No preguntes al líder funcional. Los catorce supuestos están adoptados en
  `docs/ALCANCE_Y_SUPUESTOS_SGMC.md` y son vinculantes hasta que el campo los desmienta.

---

## Objetivo

Entregar un sistema **completo y usable**, poblado con datos de prueba realistas y documentado,
para que el líder funcional pueda operarlo, opinar sobre modos y usos, y corregir sobre algo
concreto en lugar de imaginar.

El criterio de éxito no es "configurado". Es: **un técnico ejecuta un mantenimiento de extremo a
extremo, sin señal, y el registro aparece en el backend con su evidencia.**

---

## Orden de ejecución

Es una cadena. Cada paso depende del anterior y saltárselo produce trabajo que hay que rehacer.

### Paso 1. Cablear las referencias

Sin esto no funciona nada de lo demás.

- `MAN_Mantenimientos.OTID` → tipo `Ref`, tabla referenciada `OT_OrdenesTrabajo`.
- `OT_OrdenesTrabajo.Activo` → confirmar o convertir a `Ref` hacia `ACT_Activos`. Verifica primero
  si ya lo es; el nombre de la columna es engañoso.
- `CHK_Checklists.OTID` → `Ref` a `OT_OrdenesTrabajo`. `CHD_ChecklistDetalle.ChecklistID` → `Ref` a
  `CHK_Checklists`, con `IsPartOf`.
- `FOT_Fotografias.MantenimientoID` y `FIR_Firmas.MantenimientoID` → `Ref` a `MAN_Mantenimientos`,
  con `IsPartOf`.
- Revisa el resto de columnas terminadas en `ID`: la nomenclatura sugiere referencia, pero varias
  están como texto.

**Verificación:** abre el Asistente de Expresiones y comprueba que
`DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0` deja de dar error. Si el
Asistente acepta la expresión, la cadena está cableada.

### Paso 2. Datos maestros

- Cargar coordenadas sobre el trazado real de la vía de la Concesión. Hoy los 34 activos comparten
  un punto en Bogotá. Basta con distribuirlas de forma realista a lo largo del corredor; el
  levantamiento topográfico definitivo vendrá después.
- Realinear `SedeID` según D-03: unidad funcional en el activo, zona de trabajo en el usuario.
- Limpiar los datos de prueba corruptos de `CHK_Checklists`: el registro `CHK001` trae el nombre
  del técnico donde va un identificador y `NOW()` como texto literal.

### Paso 3. Formularios, los 18

Redactar el banco de preguntas de los 15 tipos que no lo tienen, en `FRM_Preguntas`, siguiendo el
patrón de `FRM_SOS`: sección, orden, tipo de respuesta, obligatoriedad, rangos, unidad y ayuda.

Usa como base las tres hojas planas existentes (`FRM_SOS`, `FRM_CCTV`, `FRM_PMVF`) y la práctica
estándar de mantenimiento del tipo de activo. Estructura recurrente: estado encontrado, limpieza,
inspección física, pruebas funcionales, sistema eléctrico, comunicaciones, novedades y evidencia.

Mapear `TIP_TiposActivo.FormularioID` en los 18 tipos.

Retirar las hojas planas una vez migradas: son una arquitectura paralela y mantener las dos
garantiza que se desincronicen.

### Paso 4. Reglas y automatizaciones

- Geofencing con el radio de D-02 y su mensaje de error en texto plano.
- Excepción por precisión GPS insuficiente según D-04.
- Security Filter por zona, verificado con una cuenta real de técnico.
- Estados de la orden según D-06, con las transiciones y quién las ejecuta.
- Bots de notificación de asignación y de alerta por activo fuera de servicio.

### Paso 5. Poblar con datos de prueba

**Este paso es método, no relleno.** Al ejercitar la aplicación con datos se descubre lo que
ninguna lectura del modelo revela: qué tablas reciben escrituras de verdad, cuáles quedaron
huérfanas o son legacy y se pueden eliminar, y dónde escriben realmente los disparadores.

- Volumen sugerido: 30 a 40 órdenes en distintos estados, repartidas entre técnicos y unidades
  funcionales, cubriendo los tipos de activo priorizados.
- Al menos 10 mantenimientos ejecutados con checklist respondido, fotografías, firma y coordenada
  de cierre.
- Casos de borde deliberados: un cierre con excepción de GPS, una segunda visita, una devolución
  del supervisor, un activo fuera de servicio que dispare la alerta.
- Los datos deben ser **verosímiles**: nombres de técnicos reales del catálogo, PR coherentes con
  el corredor, voltajes dentro de rango.

**Al terminar, documenta qué tablas quedaron sin recibir un solo registro.** Esas son las
candidatas a eliminar o a recablear, y ese inventario es uno de los entregables.

### Paso 6. Reportes

Construir los seis reportes de D-12, con los indicadores definidos en D-13. Con datos cargados se
ven de inmediato los que no cuadran.

### Paso 7. Documentación de entrega

- **Manual de uso por rol**, con los modos de operación, no solo la secuencia de clics: qué hace un
  técnico en un día normal, qué hace cuando algo se sale de lo normal, qué mira un supervisor y
  para decidir qué.
- Explicación de cada reporte: qué muestra, para qué decisión sirve, quién lo recibe.
- Inventario de tablas activas contra tablas sin uso, con recomendación.
- Registro de supuestos aplicados y de cómo corregir cada uno.

---

## Reglas de trabajo

**Verificación.** No declares nada conforme por reporte. Verifícalo contra el archivo y di contra
cuál de las dos fuentes. Distingue estructura de población: que exista la columna no significa que
tenga datos.

**Una relación solo existe si la columna es de tipo `Ref`.** Que dos tablas compartan un nombre de
columna no las relaciona. Compruébalo en el editor antes de escribir cualquier expresión que
desreferencie.

**Economía de interfaz.** Manejar el editor clic a clic es caro y frágil. Reglas:
- Los datos se cargan por lote sobre el Sheets, nunca celda por celda.
- La configuración de AppSheet no tiene API, así que va por navegador, pero **agrupa las acciones**
  y verifica al final del bloque, no después de cada clic.
- Para comprobar una expresión, el Asistente de Expresiones es más rápido y seguro que probar en
  la aplicación.
- Antes de tocar el editor, confirma que hay copia de respaldo de la aplicación: *Regenerate
  Structure* advierte que no se puede deshacer.
- URL del editor: `https://www.appsheet.com/Template/AppDef?appName=SGMC-886843353`. La variante
  con `appId` devuelve 404.

**Entregables sin iconos.** Español con tildes correctas, sin emojis en documentos, mensajes de
error ni textos de interfaz.

**Los `.md` en `docs/`, los `.py` en `scripts/`, los entregables en `entregables/`.** Todo
documento nuevo se enlaza en `MAP.md` y en `README.md`.

---

## Criterios de aceptación

El trabajo está terminado cuando **todos** se cumplen y cada uno es verificable por un tercero:

1. El Asistente de Expresiones acepta `DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0`.
2. Las 34 coordenadas de `ACT_Activos` son distintas y están sobre el corredor.
3. Los 18 tipos de activo resuelven su formulario y los 18 formularios tienen preguntas.
4. Un usuario de prueba con rol técnico ve activos al aplicar el Security Filter.
5. `MAN_Mantenimientos`, `FOT_Fotografias` y `FIR_Firmas` tienen registros reales, escritos desde
   la aplicación.
6. Un mantenimiento se completa en modo avión y sincroniza al recuperar señal.
7. Los seis reportes devuelven cifras coherentes con los datos cargados.
8. Existe el manual de uso por rol y el inventario de tablas sin uso.

Mientras el punto 5 no se cumpla, el sistema no está probado: está configurado, que no es lo mismo.
