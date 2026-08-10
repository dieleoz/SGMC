# Dónde vamos y qué falta

**Lea esto primero.** Es el mapa de todo lo demás.

Actualizado el 2026-08-09.

## Los dos enlaces

```
Aplicación   SISGA
             https://www.appsheet.com/template/appdef?appId=9e947fce-c445-4477-af20-a6c6c984bd1e

Datos        Modelo_Datos_09082026   ·   32 pestañas   ·   propiedad de la Concesión
             https://docs.google.com/spreadsheets/d/1LGabjn1iNDKiJNP7CUD4_LwCH2BGXC8oTBfXmuuAkFs
```

## En una frase

**La aplicación está reconstruida y cableada. Falta terminar cuatro ajustes, probarla, y cargar las
coordenadas reales antes de que salga a campo.**

---

## 1. Qué está hecho

| | |
|---|---|
| **La base de datos** | 28 tablas, 32 pestañas. Verificada: `FASE A CERRADA`, 59 comprobaciones |
| **La aplicación** | Reconstruida desde cero sobre esa hoja. Las 28 tablas dadas de alta |
| **Las claves** | Las 28, todas `Text`. Seis con `UNIQUEID()` para filas nuevas |
| **Las referencias** | Las 38 del modelo, con `IsPartOf` en las cuatro que lo llevan |
| **El geofencing** | Puesto, con `Editable_If = FALSE` en las cuatro columnas de captura |
| **Los filtros de seguridad** | Los dos: activos por unidad funcional, órdenes por técnico o supervisor |
| **Las marcas de tiempo** | Las cuatro, como `ChangeTimestamp` del servidor |

## 2. Qué falta para cerrar la aplicación

Está todo en [`docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`](docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md),
listo para pasar a quien esté en el editor.

| # | Qué | Por qué importa |
|---|---|---|
| 1 | **Quitar `Deletes`** en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` | **Es lo más urgente.** Con `IsPartOf` puesto, borrar un mantenimiento se lleva sus fotos, su firma y su checklist. Un clic |
| 2 | **Completar la regla del umbral de GPS** con el `OR(ISBLANK(...))` | Sin él, si alguien borra la fila del parámetro **todos los cierres salen limpios y nadie se entera** |
| 3 | **Ocultar 51 columnas retiradas** | Aparecen en el formulario del técnico. Siete de ellas AppSheet las convierte en referencia sola |
| 4 | **Las tres expresiones de prueba** | Es lo que dice si el cableado funciona de verdad |

## 3. Y una cosa que NO se arregla en el editor

**Los 34 activos comparten una sola coordenada, y está en Bogotá.**

```
4.728512, -74.114531   ← en los 34
```

Con el radio de un kilómetro, **la aplicación rechaza todo cierre hecho en el corredor**. El primer
técnico en vía no podrá cerrar ni una orden.

**No es un defecto de configuración: faltan las coordenadas reales.** Es la decisión **D-01**, y es
trabajo de campo. Hasta que se resuelva, el piloto no puede salir.

---

## 4. Qué leer, según lo que necesite

| Si necesita | Lea |
|---|---|
| **Entender qué hace el sistema** | [`docs/FUNCIONAL_SGMC.md`](docs/FUNCIONAL_SGMC.md) — para quién, cómo y para qué. Su §6 dice qué mecanismo se usa para cada cosa y cuál se descartó |
| **Construir o configurar la app** | [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md) — diez pasos, más la **ficha de las 28 tablas** columna por columna |
| **Terminar lo que falta hoy** | [`docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`](docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md) |
| **Saber qué expresión va en cada sitio** | [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) — las 20 reglas enteras, sin cortar |
| **Probar que funciona** | [`docs/sdd/PRUEBA-003-despliegue.md`](docs/sdd/PRUEBA-003-despliegue.md) |
| **Qué hay en cada tabla y columna** | [`docs/bd.md`](docs/bd.md) — generado del archivo |
| **Por qué AppSheet se comporta así** | [`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) — 12 hallazgos verificados |
| **Cómo se mantiene el corredor de verdad** | [`docs/CONTEXTO_OPERACION.md`](docs/CONTEXTO_OPERACION.md) |
| **Qué decirle al dueño de la app anterior** | [`docs/COMUNICACION_PROPIETARIO_APP.md`](docs/COMUNICACION_PROPIETARIO_APP.md) |

**El manual de usuario NO se entrega.** Describe una versión anterior y tiene nueve afirmaciones
falsas. Está marcado en su cabecera.

---

## 5. Lo que viene después, en orden

### Ahora — cerrar y probar
Los cuatro puntos del apartado 2, y correr `PRUEBA-003`. **Un día.**

### Después — dos frentes, y hay que elegir

**La interfaz.** Hoy el modelo describe **datos, no pantallas**: `modelo_objetivo.py` no tiene
vistas, ni acciones, ni slices. Por eso el manual dice «se construye sola», que es justo la clase de
instrucción que produce errores.

Hay que declarar unas veinte cosas —qué pantallas hay, de qué tipo, sobre qué tabla, qué columnas
muestran— y con eso el manual de interfaz se genera igual que el de datos. **Son decisiones de
operación, no técnicas.**

**El modelo de dominio.** `ESPEC-003` añade la capa de tareas, los doce oficios, la jerarquía de
ubicación y los tiempos del correctivo. **Está bloqueada** por el arquitecto con catorce
condiciones sin resolver, así que no es un paso disponible: es un documento por terminar.

Su pieza principal, `TAR_Tareas`, cambia cómo se generan las órdenes — **un poste SOS tiene tarea
semanal, mensual y trimestral, no una**. No se toca con el piloto a punto de arrancar.

### Y lo barato que se puede hacer ya
**Poblar `ROL_Roles` con los doce oficios** que ya están escritos en el Plan Maestro. Doce filas, en
una tabla que ya existe, sin tocar ninguna regla.

---

## 6. Lo que está bloqueado, y por quién

| Qué | Estado |
|---|---|
| `ESPEC-003` — modelo de dominio | **BLOQUEADA.** 14 condiciones del arquitecto sin resolver |
| `MANUAL_DESPLIEGUE` | Bloqueado, con 10 de 14 condiciones aplicadas. Faltan cuatro, ninguna urgente |
| Salida a campo | **Bloqueada por D-01**: las coordenadas reales |
| Generación automática de órdenes | **No cabe en el plan gratuito.** Decisión de licenciamiento |

---

## 7. Las tres cosas que costaron la semana, para no repetirlas

**AppSheet ignora las pestañas ocultas.** Ocho catálogos estaban ocultos y cargaban 24 tablas de 32,
sin un solo mensaje. Nuestra propia verificación decía `FASE A CERRADA` porque `openpyxl` sí las lee.
Cerrado con `F-18`.

**`Regenerate` fusiona, no reemplaza.** Conserva las columnas viejas a propósito. Con un esquema muy
divergente impide converger, y por eso se reconstruyó en vez de reparar.

**Una instrucción que exige criterio se ejecuta mal.** «Oculte las columnas retiradas» produjo que se
cableara una trampa como referencia y que alguien se inventara los valores de un `Enum`. Por eso
ahora los documentos llevan la lista completa, generada.

---

*Todo lo de este repositorio se genera de `scripts/modelo_objetivo.py`. Si algo no cuadra, manda el*
*modelo. Se comprueba con `validar_modelo.py`, `verificar_faseA.py` y `verificar_documentos.py`.*
