# Dónde vamos y qué falta

**Lea esto primero.** Es el mapa de todo lo demás.

Actualizado el 2026-08-09.

## Los dos enlaces

```
Aplicación   SISGA
             https://www.appsheet.com   ->   entrar por el listado de aplicaciones

Datos        Modelo_Datos_09082026   ·   32 pestañas   ·   0 ocultas
             https://docs.google.com/spreadsheets/d/1LGabjn1iNDKiJNP7CUD4_LwCH2BGXC8oTBfXmuuAkFs
```

> **El enlace directo a la aplicación que había aquí daba 404**, y también `/Home/MyApps`. El
> `appId=9e947fce-...` no resuelve. `SISGA` sí existe y aparece en el listado de
> `https://www.appsheet.com`, junto a `SGMC2` y al `SGMC` de la cuenta anterior, los dos con aviso
> de error. **Hasta tener el identificador bueno, se entra por el listado**, no por enlace directo.

## En una frase

**La aplicación está reconstruida y cableada. Falta terminar cuatro ajustes, probarla, y cargar las
coordenadas reales antes de que salga a campo.**

---

## 1. Qué está hecho

| | |
|---|---|
| **La base de datos** | 28 tablas, 32 pestañas. Verificada: `FASE A CERRADA`, 61 comprobaciones |
| **La aplicación** | Reconstruida desde cero sobre esa hoja. Las 28 tablas dadas de alta |
| **Las claves** | Las 28, todas `Text`. Seis con `UNIQUEID()` para filas nuevas |
| **Las referencias** | Las 38 del modelo, con `IsPartOf` en las cuatro que lo llevan |
| **El geofencing** | Puesto, con `Editable_If = FALSE` en las cuatro columnas de captura |
| **Los filtros de seguridad** | Los dos: activos por unidad funcional, órdenes por técnico o supervisor |
| **Las marcas de tiempo** | Las cuatro, como `ChangeTimestamp` del servidor |

## 2. Qué falta para cerrar la aplicación

El agente del editor avanzó bastante antes de que se parara. **Esto es lo que quedó hecho:**

```
✓  Las 38 referencias, con IsPartOf en las cuatro
✓  Las 3 columnas trampa en Text y ocultas
✓  MAN.Diagnostico revertida (tenía una App formula que escribía en la hoja)
✓  Los 4 ChangeTimestamp
✓  Geofencing, Editable_If y los dos filtros de seguridad
✓  Deletes desmarcado en OT_OrdenesTrabajo y MAN_Mantenimientos
```

**Y esto es lo que falta:**

| # | Qué | Por qué importa |
|---|---|---|
| 1 | **La regla del umbral de GPS con el `OR(ISBLANK(...))`** | Sin él, si alguien borra la fila del parámetro **todos los cierres salen limpios y nadie se entera** |
| 2 | ~~Las columnas retiradas, a medias~~ | **Ya no aplica.** Ver la decisión de abajo |
| 3 | **Las tres expresiones de prueba** | Es lo que dice si el cableado funciona de verdad |

La 1 y la 3 siguen pendientes, en
[`docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`](docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md).

> ## La decisión, tomada el 2026-08-09: la hoja limpia
>
> **El funcional parte del Excel que le entreguemos y a partir de ahí sigue las guías.** Por eso lo
> que se le entrega tiene que salir limpio del repositorio, no ser una hoja heredada con 47 columnas
> escondidas encima.
>
> **Eso cancela el punto 2.** Las 47 columnas desaparecen del archivo en vez de esconderse en la
> aplicación, y con ellas las tres trampas. Ocultarlas ahora sería trabajo que se tira.
>
> El coste de la migración está medido en
> [`docs/MIGRACION_HOJA_LIMPIA.md`](docs/MIGRACION_HOJA_LIMPIA.md): 8 tablas de 28 y 14 reglas a
> reponer.

## 3. La plantilla de datos

**`BD/Modelo_Datos_PLANTILLA.xlsx`** — generada del modelo. **Es el entregable de datos.**

```
28 pestañas · 202 columnas · ninguna de sobra
ACT_Activos: 34 activos reales (ID 1-34) + 355 sintéticos (ID 1001-1355)
0 referencias rotas de las 38 · FASE A CERRADA
```

**Los 34 reales se conservan intactos** y las seis órdenes existentes siguen apuntando a su equipo:
`FO-001` la fibra, `CCTV-002` la cámara, `VW-001` el videowall.

**Los 355 sintéticos** llevan los códigos del Plan Maestro —`SOS_1` a `SOS_54`, `SWIT_1` a
`SWIT_142`— repartidos por los 137 km del corredor. **Cada fila dice en `Observaciones`:
`ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL`.**

Sirven para ejercitar el filtro por zona, la navegación y el volumen de sincronización.

> **Lo que NO desbloquean: la prueba del geofencing.** Los registros de prueba tienen su coordenada
> en Bogotá y el activo sintético más cercano queda a 60 km. Así que **`P-08` —el cierre legítimo que
> debe aceptarse— pasa a ser imposible sin desplazarse**, y `P-09` se vuelve trivial. El par deja de
> discriminar. Antes era al revés.

> **Y un hallazgo del arquitecto que cambia una decisión:** con 355 activos, el radio de 1 km mete
> **8 activos de media dentro de cada geofence**, con un máximo de 13. Ninguno de los 355 queda
> identificado de forma única. **El radio por tipo deja de ser opcional** — con 1,0 km el sistema
> prueba «estás en el corredor», no «estás frente al equipo», que es su propósito.

**El principio, que es de operación:** entregamos la estructura; el dato real lo pone quien lo
conoce. Los bloqueantes se resuelven descargando el Excel y completándolo.

Se regenera entera con **un comando**, desde el 2026-08-10:

```bash
python scripts/generar_plantilla.py
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"   # FASE A CERRADA, 61 conformes
```

**Y se reproduce:** dos ejecuciones seguidas dan las 29 pestañas idénticas, celda por celda. Antes
hacían falta dos scripts y varios pasos a mano —unir, añadir `_LEEME`, poblar el radio— que no
estaban escritos en ninguna parte, así que la plantilla era un artefacto que se conservaba en vez de
generarse. Es justo lo que este proyecto decidió no volver a tener.

### El catálogo de tipos, corregido el 2026-08-09

**Había dos taxonomías y nadie lo había escrito.** `TIP_TiposActivo` tenía 18 tipos, que es lo que
decide **qué checklist ve el técnico**; el Plan Maestro tiene 18 familias, que es como operación
cuenta los equipos. **No son la misma lista.** Nueve familias no tenían tipo propio y se colgaban
del tipo de otra cosa:

```
la impresora heredaba el checklist del NAS
el portátil, el del servidor
el carril de peaje, el de la báscula
```

**Eran 78 activos de 355 —el 22%— con el checklist equivocado.** Y como `TipoActivoID` resolvía
contra una fila que existe, **ningún verificador lo veía**: es el mismo patrón que el inventario que
pisó los 34 reales.

**`scripts/catalogo_tipos.py` lo cierra** como fuente única de los dos generadores: 27 tipos —los 18
de siempre más los 9 que faltaban—, cada familia con tipo, checklist y radio propios. Trae
`comprobar()`, que falla si dos familias comparten tipo o si un tipo se queda sin radio.

**Llevado al archivo el 2026-08-10.** La plantilla trae los **27 tipos**, los 27 formularios —nueve
nuevos, uno por tipo, porque un tipo sin formulario deja la referencia rota— y **cero activos con el
tipo equivocado**, comprobado sobre el archivo generado y no sobre el informe del script.

De paso desaparecieron dos cosas que venían de la hoja heredada: el nombre de la subestación con la
tilde rota, y la mezcla de tipos en las claves —el fixture guardaba `'1'` como texto y los generados
salían como número—. **Las claves y las 38 referencias viajan todas como texto**, que es como el
modelo las declara. Son 2.424 celdas, y la regla se deriva del modelo, no se decide archivo a
archivo.

## 4. Qué leer, según lo que necesite

| Si necesita | Lea |
|---|---|
| **Saber qué le toca a usted** | [`docs/INDICACIONES_POR_ROL.md`](docs/INDICACIONES_POR_ROL.md) — el reparto por rol: qué hacer, qué decidir, qué leer y cuánto cuesta |
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

> **Comprobado en Drive el 2026-08-09: en la hoja publicada no hay ninguna oculta.** Las 32 pestañas
> están visibles, y las 28 del modelo entre ellas. Lo que estaba mal era **el volcado del
> repositorio**, que se descargó antes de que se mostraran y arrastraba las ocho.
>
> El volcado ya refleja el estado real y `verificar_faseA.py` sin argumentos apunta a él. Antes
> apuntaba a `Modelo de Datos (4).xlsx`, retirado hacía días: correrlo sin argumento **daba un
> veredicto sobre un archivo muerto**.
>
> **La regla se queda igual de todos modos.** El día que alguien oculte una pestaña para trabajar
> más cómodo, AppSheet cargará 24 de 32 sin decir nada. `F-18` es lo único que lo ve, y por eso
> se corre cada vez que se toque la hoja con datos.

**`Regenerate` fusiona, no reemplaza.** Conserva las columnas viejas a propósito. Con un esquema muy
divergente impide converger, y por eso se reconstruyó en vez de reparar.

**Una instrucción que exige criterio se ejecuta mal.** «Oculte las columnas retiradas» produjo que se
cableara una trampa como referencia y que alguien se inventara los valores de un `Enum`. Por eso
ahora los documentos llevan la lista completa, generada.

---

*Todo lo de este repositorio se genera de `scripts/modelo_objetivo.py`. Si algo no cuadra, manda el*
*modelo. Se comprueba con `validar_modelo.py`, `verificar_faseA.py` y `verificar_documentos.py`.*
