# Dónde vamos y qué falta

**Lea esto primero.** Es el mapa de todo lo demás.

Actualizado el 2026-08-10.

## Los dos enlaces

```
Aplicación   SISGA_-323965761-26-08-10     appId d180a1b5-19ca-448e-a44c-f985396dce12
             https://www.appsheet.com/template/appdef?appId=d180a1b5-19ca-448e-a44c-f985396dce12

Datos        Modelo_Datos_10082026        Hoja de cálculo de Google, generada del modelo
             https://docs.google.com/spreadsheets/d/1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0
```

> **Se reconstruyó sobre hoja limpia el 2026-08-10**, con las 28 tablas dadas de alta sobre
> `Modelo_Datos_10082026`.
>
> **En la cuenta hay cinco aplicaciones y solo una es el sistema.** Las otras cuatro no se borran
> —son la traza de cómo se llegó hasta aquí— pero **ninguna es el SGMC**:
>
> | Aplicación | Qué es |
> |---|---|
> | **`SISGA_-323965761-26-08-10`** (`d180a1b5…`) | **EL SISTEMA.** 28 tablas sobre la hoja limpia |
> | `SISGA_-323965761` (`7cc0b0eb…`) | Intento previo del mismo día. La de arriba es su copia |
> | `SISGA` | Leía `Modelo_Datos_09082026`. Respaldo del estado anterior a la hoja limpia |
> | `SGMC2` | Con aviso de error. Abandonada |
> | `SGMC-886843353` | De la cuenta del Propietario anterior. Abandonada el 2026-08-09 |
>
> **Si alguien le pasa un enlace que no sea el `d180a1b5…`, no es este sistema.**
>
> **Por qué hay dos y no una migración en sitio.** Lo barato habría sido reemplazar el contenido de
> la hoja de producción conservando su identificador —*Archivo → Importar → Reemplazar hoja de
> cálculo*—, y entonces solo cambiaban 8 tablas de 28. Al crear archivo nuevo, la aplicación no
> puede seguirlo: **hay que dar de alta las 28 y reponer las 38 referencias y las 20 reglas**. El
> procedimiento entero está en [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md), que es
> exactamente eso, de cero a aplicación desplegada.
>
> **El `appId=9e947fce-...` que estuvo aquí no resolvía**, daba 404. Este sí.

## En una frase

**La aplicación está reconstruida y cableada. Faltan dos ajustes en el editor, probarla, y cargar
las coordenadas reales antes de que salga a campo.**

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
28 pestañas de datos más _LEEME · 202 columnas · ninguna de sobra
ACT_Activos:      368 activos, un solo inventario, codigos SOS-001 / SWIT-001
TIP_TiposActivo:   27 tipos, con RadioGeofencingKm poblado en los 27
FRM_Formularios:   27 filas, uno por tipo
FRM_Preguntas:    333 preguntas, los 27 formularios con checklist
Sin registros de prueba · 0 referencias rotas · FASE A CERRADA, 61 conformes
```

**Un solo inventario, con el código de operación.** Cada familia suma exactamente lo que dice el
Plan Maestro —54 postes SOS, 142 switches, 26 cámaras— completando lo que ya había en la hoja. Los
**13 equipos que el Plan Maestro no cuenta por unidades** se conservan: la fibra, el generador, el
video wall, el router, el firewall, la UPS, el NAS, la subestación y la báscula estática. Sin ellos,
nueve de los 27 tipos se quedarían sin un solo activo con el que probar su checklist.

**Cada fila dice en `Observaciones`: `ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL`.**

**Los 27 checklists tienen preguntas.** 45 estaban acordadas —SOS, CCTV y PMVF—, y dos de ellas se
recuperaron de pestañas retiradas donde se estaban perdiendo. Las otras 288 son borrador y lo dicen
de sí mismas: llevan `[BORRADOR: validar con operacion]` en su ayuda. **Buscar esa marca en la hoja
dice exactamente qué queda por revisar**, y el día que no aparezca ninguna, el banco está cerrado.

**Sin registros de prueba.** Se retiraron las órdenes, mantenimientos, checklists, fotografías y
firmas de ensayo: no son dato del funcional, son ruido que tendría que distinguir y borrar.

> **Lo que se llevó por delante retirar los registros de prueba: los fixtures de `P-08` y `P-09`.**
> No es pérdida. Una fila de mantenimiento escrita a mano en la hoja no prueba que la aplicación
> sepa crearla; hay que rehacerlos **desde la aplicación**, que es lo que esa prueba mide en
> realidad.

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
modelo las declara. Son 2.929 celdas, y la regla se deriva del modelo, no se decide archivo a
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

**El manual de usuario todavía no se entrega, pero no porque esté equivocado.** Eso decía aquí y era
falso: se reescribió el 2026-08-07 contra `FUNCIONAL_SGMC.md` y su cabecera lleva el cuadro de qué
está montado y qué no. **La versión que describía un sistema inexistente es la anterior**, y está en
`docs/historico/`. Se entrega el día que dejen de existir los recuadros de «Estado:» de su interior.

---

## 5. Lo que viene después, en orden

### Ahora — cerrar y probar
Los dos puntos vivos del apartado 2 —la regla del umbral y las tres expresiones—, y correr
`PRUEBA-003`. **Un día.**

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
| `MANUAL_DESPLIEGUE` | Vigente y generado. Se rehace con `python scripts/generar_manual_despliegue.py` |
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
*modelo. Se comprueba con `validar_modelo.py`, `verificar_faseA.py`, `verificar_documentos.py` y*
*`verificar_enlaces.py`.*
