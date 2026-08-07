---
name: revisar-arquitectura
description: Revisa el diseño del SGMC desde seis ángulos — usuario, operador, gerente, interventoría, capacidad y evolución — antes de construir o de aprobar un cambio grande. Úsala cuando cambie el modelo objetivo, cuando se vaya a desplegar, o cuando alguien proponga una funcionalidad nueva.
---

# Revisar la arquitectura del SGMC desde varias aristas

Un diseño puede validar contra sí mismo y aun así ser inviable. `validar_modelo.py` comprueba
coherencia interna: que las referencias resuelvan y que nada quede huérfano. **No comprueba si el
sistema se puede pagar, operar, ni si aguanta el crecimiento.** Esta skill cubre eso.

## Antes de opinar, dos precisiones sobre la plataforma

No propongas patrones que AppSheet no puede implementar. Aquí no hay microservicios, ni CQRS, ni
event sourcing, ni elección entre monolito y servicios: es una plataforma no-code sobre hojas de
cálculo. Las decisiones de arquitectura que sí existen son de **modelo de datos, límites de
plataforma, propiedad de los activos digitales y costo por usuario**.

Y verifica los límites antes de razonar sobre ellos. Los vigentes, comprobados el 2026-08-06:

| Límite | Valor | Dónde muerde |
|---|---|---|
| Celdas por hoja de cálculo | 10.000.000 | Rara vez. Se degrada antes la sincronización |
| Filas por tabla antes de degradar el sync | ~50.000 | `CHD_ChecklistDetalle`, que multiplica por 15 cada mantenimiento |
| Almacenamiento de imágenes | Carpeta contigua a la hoja, en el Drive del **propietario** | Cuenta contra su cuota, no la de quien sube la foto |
| Cuenta personal de Gmail | 15 GB compartidos con Gmail y Fotos | Es el caso actual del backend del SGMC |
| API REST de AppSheet | Requiere plan Core o superior | Decisión de costo |

Las cifras de crecimiento se calculan con `python scripts/capacidad.py`, no a ojo.

---

## Los seis ángulos

Recórrelos en orden. Cada uno tiene preguntas que los demás no hacen.

### 1. Usuario — el técnico en la vía

Quien usa el sistema con guantes, bajo el sol y sin señal.

- ¿Cuántos toques cuesta cerrar un mantenimiento? Cada campo obligatorio de más es fricción real.
- ¿Qué pasa si se agota la batería a mitad del formulario? ¿Y si entra una llamada?
- ¿El mensaje de error dice **qué hacer**, o solo que algo falló?
- ¿Cuántos megas consume una jornada? El técnico paga su plan de datos.
- ¿Puede ver lo que ya hizo, o el sistema solo le pide y nunca le devuelve?
- ¿La app le sirve para algo a él, o solo sirve para vigilarlo? Un sistema que solo controla se
  sabotea solo.

### 2. Operador — quien mantiene el sistema vivo

El administrador, seis meses después de la entrega.

- ¿Puede dar de alta un usuario o un activo sin tocar el modelo?
- ¿Puede corregir un formulario sin romper el histórico ya respondido?
- ¿Cómo se entera de que una sincronización falló, o de que un bot no envió el correo?
- ¿Cómo reprocesa una alerta que no salió?
- ¿Qué hace cuando alguien borra una fila por error?
- ¿Existe procedimiento de cambio con respaldo previo, o cada cambio es una apuesta?

### 3. Gerente — quien paga y responde

- ¿Cuánto cuesta al mes hoy, y cuánto con el doble de técnicos? El cobro es por usuario activo.
- ¿Qué pasa si mañana no se paga la licencia? ¿Se pierden los datos o solo el acceso?
- ¿De quién son los activos digitales: la aplicación, el backend, las fotografías?
- ¿Qué decisión permite tomar el sistema que hoy no se puede tomar? Si no hay respuesta, el
  sistema es un costo, no una inversión.
- ¿Cuánto tarda alguien nuevo en ser productivo con él?

### 4. Interventoría y contrato — quien audita

- ¿Qué informe se entrega, con qué periodicidad y en qué formato?
- ¿La cifra que reporta el sistema **coincide con la definición contractual**? Disponibilidad
  medida por tiempo, por cantidad o ponderada por criticidad da tres números distintos ante la
  misma realidad.
- ¿La evidencia es defendible? Fotografía, coordenada, precisión del GPS y firma, todo trazable
  a una persona y una hora.
- ¿Se puede reconstruir cómo era un formulario en una fecha pasada?
- ¿Cuánto tiempo se conserva la evidencia y dónde queda respaldada?

### 5. Capacidad — hasta dónde aguanta

Corre `python scripts/capacidad.py` y lee tres cosas:

- Qué tabla llega antes al umbral de sincronización, y en qué escenario.
- En cuántos años se agota la cuota de almacenamiento del propietario.
- Si ese plazo es **menor que la retención exigida**, hay un defecto de diseño, no un problema
  futuro.

Pregunta siempre: ¿qué se archiva, cada cuánto, y quién lo hace?

### 6. Evolución — qué pasa cuando cambie

- ¿Qué se rompe si se duplican los activos? ¿Y si se añade un tipo nuevo?
- ¿Qué cambio obligaría a migrar datos ya cargados? Esos son los que hay que decidir **antes**
  de poblar, no después.
- ¿Qué está deliberadamente fuera de alcance, y qué costaría meterlo luego?

---

## Cómo entregar la revisión

Una tabla por ángulo, con tres columnas: **hallazgo**, **impacto** y **qué hacer**. Sin adjetivos.

Marca cada hallazgo como:

- **Bloqueante** — impide desplegar.
- **Antes de poblar** — se puede desplegar, pero corregirlo después obliga a migrar datos.
- **Vigilar** — no urge, pero necesita un umbral y un responsable.

La categoría del medio es la que más se olvida y la más cara.

## Regla final

Si un ángulo no produce ningún hallazgo, probablemente no se recorrió de verdad. Vuelve a
hacerlo con una pregunta concreta y un número, no con una impresión.
