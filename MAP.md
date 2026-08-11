# MAP.md — Índice maestro del proyecto

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Propósito:** Mapa de navegación del repositorio. Dónde está cada cosa y qué contiene.

> **Este archivo dice dónde está cada cosa, no en qué punto va el proyecto ni qué es el sistema.**
> Para el estado, [`ESTADO.md`](ESTADO.md); para el sistema en presente,
> [`docs/SISTEMA.md`](docs/SISTEMA.md).

---

## 1. Por dónde empezar

| Si necesitas | Abre |
|---|---|
| Saber en qué punto va el proyecto y qué falta | [ESTADO.md](ESTADO.md) |
| Entender qué es el proyecto | [README.md](README.md) |
| Entender qué es el sistema hoy, sin historia ni estado | [docs/SISTEMA.md](docs/SISTEMA.md) |
| Saber qué te toca a ti, según tu rol | [docs/INDICACIONES_POR_ROL.md](docs/INDICACIONES_POR_ROL.md) |
| Entender qué hace el sistema y para quién | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) |
| Ver la arquitectura que se va a construir | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) |
| Construir o configurar la aplicación | [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) |
| Cablear la aplicación en el editor | [docs/PROMPT_CABLEADO.md](docs/PROMPT_CABLEADO.md) |
| **Saber qué hay que cerrar ANTES de que entre la primera fila** | [docs/ENCARGO_VENTANA.md](docs/ENCARGO_VENTANA.md), generado. Ocho tablas están en cero filas y eso caduca solo |
| Saber qué queda mal cableado hoy, y qué no se puede ver | [docs/CORRECCIONES_CABLEADO.md](docs/CORRECCIONES_CABLEADO.md), generado |
| Saber qué expresión va en cada sitio | [docs/sdd/RECONSTRUCCION_EXPRESIONES.md](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) |
| Probar que el despliegue funciona | [docs/sdd/PRUEBA-003-despliegue.md](docs/sdd/PRUEBA-003-despliegue.md) |
| Saber cómo se comporta AppSheet, con la cita oficial | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) |
| Consultar la estructura de datos real | [docs/bd.md](docs/bd.md), generado del `.xlsx` |
| Saber con qué supuestos se construye | [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) |
| Saber hasta dónde aguanta el sistema | `python scripts/capacidad.py` |
| Ver la aplicación y la hoja vigentes, y qué quedó superado | `python scripts/sistema.py` |
| Trabajar sobre el repositorio como agente | [CLAUDE.md](CLAUDE.md) y las skills de `.claude/skills/` |

---

## 2. Estructura de carpetas

```
D:\@Proyect\Sisga\
├── ESTADO.md                     Dónde vamos y qué falta. Se lee primero
├── README.md                     Entrada del proyecto: qué es y cómo funciona
├── CLAUDE.md                     Reglas de trabajo para agentes
├── MAP.md                        Este archivo
│
├── BD/                           Hojas de datos
│   └── Modelo_Datos_PLANTILLA.xlsx   El entregable de datos, generado del modelo.
│                                      Es el mismo archivo publicado como Modelo_Datos_10082026
│
├── docs/                         Documentación técnica y funcional
│   ├── CORRECCIONES_CABLEADO.md   Lo que falta cablear en el editor. GENERADO por
│   │                               auditar_cableado.py contra la aplicación en vivo
│   ├── ENCARGO_VENTANA.md         Lo único que hay que cerrar mientras las ocho tablas
│   │                               de movimiento sigan en cero filas. GENERADO por
│   │                               generar_encargo_ventana.py. Caduca solo: el primer
│   │                               registro cierra la ventana para siempre
│   ├── images/                    fig_01 a fig_07, figuras de los documentos
│   └── sdd/                       Artefactos vigentes del pipeline: ESPEC-003 (bloqueada),
│                                   PRUEBA-003, RECONSTRUCCION_EXPRESIONES, ESPEC-004
│                                   (tercera version, reescrita 2026-08-11 bajo la vara de
│                                   CLAUDE.md §7.18 tras la segunda pasada de 15 hallazgos;
│                                   ESPEC-005 ya no es supuesto, esta aplicada), ESPEC-005
│                                   (APLICADA al modelo; le falta la mitad
│                                   que vive en el editor, que es el ENCARGO_VENTANA) y
│                                   ESPEC-006 (CERRADA con 4 riesgos aceptados; no ejecutada)
│
├── Manuales/                     Manual de usuario
│   └── MANUAL_DE_USUARIO.md
│
├── scripts/                      Fuente del modelo, validadores y generadores
│   ├── modelo_objetivo.py         FUENTE ÚNICA. De aquí sale todo lo demás
│   ├── sistema.py                 La aplicación y la hoja vigentes, y las superadas con su motivo
│   ├── catalogo_tipos.py          Los 27 tipos de activo y las 18 familias del Plan Maestro
│   │
│   │                              Los SEIS verificadores (CLAUDE.md §7.4). Leen ARCHIVOS,
│   │                              son el gate, ninguno sustituye a otro y los seis se
│   │                              corren antes de cerrar nada
│   ├── validar_modelo.py          El modelo consigo mismo. Gate objetivo del pipeline
│   ├── verificar_faseA.py         El modelo contra la hoja descargada: estructura y tipos
│   ├── verificar_datos.py         Los DATOS de esa hoja: obligatorias vacías, huérfanas, tipos
│   │                               mezclados, tablas vacías (G-04) y **reglas que leen una
│   │                               columna vacía y por tanto no hacen nada** (G-05)
│   ├── verificar_documentos.py    La prosa contra el modelo
│   ├── verificar_enlaces.py       Que todo enlace relativo entre documentos resuelve
│   ├── verificar_reproducible.py  Que generar la plantilla dos veces dé lo mismo
│   │
│   │                              Los TRES que miran la aplicación EN VIVO. No son
│   │                              verificadores y no bloquean: informan. Comparten un
│   │                              límite —lo que la API no devuelve, no se puede ver—
│   ├── auditar_cableado.py        El cableado REAL contra el declarado. Emite
│   │                               docs/CORRECCIONES_CABLEADO.md. Método en
│   │                               BASE_CONOCIMIENTO_APPSHEET §16, con sus tres límites
│   ├── verificar_app.py           Recuento de filas por la API. Se llama como los seis
│   │                               y NO es uno de ellos; lo dice su propio docstring
│   ├── instantanea.py             Fotografía los datos vivos y compara dos fotos celda a
│   │                               celda. La red de las reglas que ESCRIBEN
│   ├── probar_auditor.py          Prueba negativa de auditar_cableado.py: le mete
│   │                               defectos y comprueba que los caza. Sin red
│   │
│   │                              Módulos que responden una sola pregunta, y los consumen
│   │                              los generadores para que el saber no se quede en prosa
│   ├── inferencia.py              Quién consigue el tipo de cada columna: a mano, el
│   │                               nombre o el contenido. El reparto lo imprime el propio script
│   ├── alcance_reglas.py          Qué columnas toca de verdad cada regla, con su tabla.
│   │                               Atribuir por nombre suelto infla la cifra al doble
│   ├── lectura_de_vuelta.py       Quién comprueba cada clase de cambio. Tres tienen
│   │                               comando; **cuatro no tiene nadie**
│   ├── navegacion_editor.py       Dónde está cada control en pantalla. El nombre de la
│   │                               regla NO es el del control: Required_If es Require?
│   ├── generar_encargo_ventana.py Emite docs/ENCARGO_VENTANA.md desde el modelo: las 2
│   │                               columnas virtuales Etiqueta y los 54 tipos a cotejar
│   │                               en las 8 tablas vacías, más lo que deja fuera y por qué
│   └── generar_*.py               El resto de generadores de la plantilla y los documentos
│
├── contexto/                     Material de contexto operativo, no versionado. No es la vara.
│   └── SISGA Contrato/            Cinco PDF del contrato de ESTA Concesión. Sin catalogar,
│                                   y no son «ejemplo de otro corredor»: véase CLAUDE.md §7.6
└── archivo/                      Material de origen, no versionado
```

> **No hay carpeta `entregables/`.** Se deja dicho porque un mapa que nombra una carpeta inexistente
> manda a buscarla; lo que contenía lo guarda `git`.

---

## 3. Índice de documentos

### Estado y método

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/SISTEMA.md](docs/SISTEMA.md) | El sistema tal como es hoy, en presente: qué resuelve, de qué se compone, el modelo, las decisiones de diseño, qué se puede comprobar y los límites vigentes | **Vigente. Es la línea de partida contra la que se leen las demás especificaciones** |
| [ESTADO.md](ESTADO.md) | Qué está hecho, qué falta y qué está bloqueado | **Vigente. Es la verdad del estado** |
| [docs/SDD_PIPELINE_SGMC.md](docs/SDD_PIPELINE_SGMC.md) | Método de construcción: cinco agentes y el gate antes del paso caro | Vigente en sus agentes; sus referencias a fases anteriores a la reconstrucción están superadas |
| [docs/INDICACIONES_POR_ROL.md](docs/INDICACIONES_POR_ROL.md) | El reparto por rol: qué hacer, qué decidir, qué leer | Vigente |
| [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) | Alcance del sistema y los supuestos adoptados, vinculantes hasta que el campo los desmienta | Vigente |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Fases con criterio de cierre verificable | Vigente |

### Definición funcional y de dominio

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) | Qué hace el sistema, para quién, cómo y para qué. Su §6 es el registro de una sola forma por propósito | **Vigente. Es la fuente funcional** |
| [docs/CONTEXTO_OPERACION.md](docs/CONTEXTO_OPERACION.md) | Cómo se mantiene el corredor de verdad, y la procedencia de cada documento de contexto | Vigente |
| [docs/GUIA_IMPLEMENTACION_FUNCIONAL.md](docs/GUIA_IMPLEMENTACION_FUNCIONAL.md) | La implementación vista desde la operación, paso a paso. Generada | Vigente en el método; verifique cada identificador contra `scripts/sistema.py` |
| [docs/MODELO_EVOLUCION_FASE_2.md](docs/MODELO_EVOLUCION_FASE_2.md) | Lo que el modelo actual no representa, para después del piloto | Propuesta |
| [docs/sdd/ESPEC-003-modelo-de-dominio.md](docs/sdd/ESPEC-003-modelo-de-dominio.md) | Capa de tareas, jerarquía de ubicación, oficios y correctivo | **Bloqueada.** 14 condiciones del arquitecto sin resolver; nada de ella está en `scripts/modelo_objetivo.py` |

### Modelo de datos y despliegue

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | Modelo objetivo: 28 tablas, 211 columnas, 39 referencias, 23 reglas | Vigente. **Se regenera, no se edita** |
| [docs/PROMPT_CABLEADO.md](docs/PROMPT_CABLEADO.md) | El encargo de cableado, autocontenido: las 39 referencias, los tipos y el orden | Vigente. **Se regenera, no se edita** |
| [docs/ENCARGO_VENTANA.md](docs/ENCARGO_VENTANA.md) | El encargo de la **ventana barata**, autocontenido: las 2 columnas virtuales `Etiqueta` y el cotejo de 54 tipos en las 8 tablas que siguen en cero filas. Y **lo que deja fuera, con su motivo** | Vigente. **Se regenera, no se edita.** Vale mientras las ocho sigan vacías: el primer registro lo caduca entero |
| [docs/REGLAS_DEL_MODELO_DE_DATOS.md](docs/REGLAS_DEL_MODELO_DE_DATOS.md) | Las diez reglas que manda el motor de datos, con el fallo del que salió cada una | Vigente. **Se regenera, no se edita** |
| [docs/bd.md](docs/bd.md) | Diccionario As-Built: lo que la hoja tiene hoy, columna a columna | Vigente. **Se regenera, no se edita** |
| [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) | De cero a app desplegada, con la ficha de las 28 tablas columna por columna | Vigente. Generado |
| [docs/CORRECCIONES_CABLEADO.md](docs/CORRECCIONES_CABLEADO.md) | Qué referencias quedan mal en el editor y en qué orden se arreglan, más **las que el método no puede ver** | Vigente. **Se regenera, no se edita.** Vale para la lectura con que se generó, no para siempre |
| [docs/sdd/RECONSTRUCCION_EXPRESIONES.md](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) | Los nombres renombrados y las 23 reglas a reponer, sin cortar | Vigente |
| [docs/sdd/PRUEBA-003-despliegue.md](docs/sdd/PRUEBA-003-despliegue.md) | Las pruebas de aceptación del despliegue reconstruido | Vigente |
| [docs/sdd/ESPEC-004-cierre-excepcion-manual.md](docs/sdd/ESPEC-004-cierre-excepcion-manual.md) | `RG-02`/`RG-19` dependen de `USERLOCATIONACCURACY()`, que no existe en AppSheet: `CierreConExcepcion` nunca se dispara. Corrige a que el técnico la marque | **APROBADA CON RIESGOS ACEPTADOS** el 2026-08-11, tercera versión, bajo la vara de `CLAUDE.md` §7.18. Las cuatro condiciones del arquitecto ya están aplicadas (commit `e8befce`), y su único bloqueante se cerró **midiéndolo**: `CierreConExcepcion` ya era `Yes/No` ([ACTA-004](docs/sdd/ACTA-004-lecturas-editor.md)). El defecto sigue vivo entero —`RG-19` está puesta como `App formula`—. Especificada y validada, **no ejecutada**: lo siguiente es una `ORDEN-004` |
| [docs/sdd/ACTA-004-lecturas-editor.md](docs/sdd/ACTA-004-lecturas-editor.md) | Lo que el editor tenía **de verdad** en `MAN_Mantenimientos`: los tipos, las expresiones, el `App formula` de `RG-19` y el censo de bots | Vigente. **Es evidencia, no documento**: la API devuelve filas y no esquema, así que esta transcripción es lo único que existe. Cierra el bloqueante de `ESPEC-004`, confirma la Rama A, y registra que **no hay ningún bot creado en la app** |
| [docs/sdd/ACTA-006-cotejo-y-supuesto.md](docs/sdd/ACTA-006-cotejo-y-supuesto.md) | Las 9 columnas de `OT_OrdenesTrabajo` cotejadas con recarga en duro, y la medición de que una columna virtual `App formula` **sí** se lee por la API | Vigente. Desbloqueó nueve pruebas de `PRUEBA-006`: pasaron de *bloqueadas* a *ejecutables a la espera de gastar la ventana* |
| [docs/sdd/ACTA-005-clave-otid-planid.md](docs/sdd/ACTA-005-clave-otid-planid.md) y [ACTA-005-pruebas.md](docs/sdd/ACTA-005-pruebas.md) | La aplicación de `ESPEC-005` al modelo, y sus pruebas —incluida `P-09`, el cotejo a ojo de `OTID`/`PlanID` en el editor | Vigentes |
| [docs/sdd/ESPEC-005-clave-otid-planid.md](docs/sdd/ESPEC-005-clave-otid-planid.md) | `OTID` y `PlanID` son claves legibles sin generador declarado; `RG-10` y `RG-12` crean filas en `OT_OrdenesTrabajo` sin asignarlo. Propone `UNIQUEID()` para ambas y una columna `Etiqueta` **virtual** (`RG-35`/`RG-36`, no `App formula` sobre columna real) para que la orden se identifique ante el técnico | **APLICADA AL MODELO**, tras pasar el gate del arquitecto en segunda pasada. `CLAVE_LEGIBLE` bajó de 22 a 20 tablas y `CLAVE_GENERADA` subió de 6 a 8; se comprueba volcando las dos listas de `scripts/modelo_objetivo.py`. **Falta la mitad que vive en el editor** —las dos virtuales, con `Show?` y `Label`—, que es el paso 1 de [ENCARGO_VENTANA.md](docs/ENCARGO_VENTANA.md) |
| [docs/sdd/ESPEC-006-reemplazo-bots-programados.md](docs/sdd/ESPEC-006-reemplazo-bots-programados.md) | `RG-08` y `RG-12` son bots programados y no corren en la cuenta gratuita; además `RG-08` movería la orden al estado `Vencida`, que es final, e impediría al técnico tardío cerrarla. Propone `RG-37`, columna virtual `EstaVencida` sobre `OT_OrdenesTrabajo`, y `RG-38`, una vista más una acción (`Data: add a new row...`) sobre `PLA_PlanMantenimiento` que el supervisor pulsa | **CERRADA el 2026-08-11**, en su tercera pasada de arquitecto, con **cuatro riesgos aceptados** con nombre y fecha (§8). Especificada y validada, **no ejecutada**: nada aplicado aún en `scripts/modelo_objetivo.py` ni en el editor. Lo siguiente que le pase será una `ORDEN-006` |

### Plataforma

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | Cómo se comporta AppSheet, con cita textual y URL oficial. §11 y §12 explican por qué se reconstruyó la aplicación | Vigente |
| [docs/COMUNICACION_PROPIETARIO_APP.md](docs/COMUNICACION_PROPIETARIO_APP.md) | Qué decirle al dueño de la aplicación anterior | Vigente en el punto pendiente; sus identificadores de aplicación y hoja están superados — véase `scripts/sistema.py` |

### Manuales

| Documento | Contenido |
|---|---|
| [Manuales/MANUAL_DE_USUARIO.md](Manuales/MANUAL_DE_USUARIO.md) | Guía de operación por rol: técnico, supervisor, administrador. **No se entrega todavía**, y su cabecera dice por qué |

---

## 4. Matriz de referencias cruzadas

| Concepto | Dónde está documentado | Dónde está el dato real |
|---|---|---|
| Estado del proyecto | [ESTADO.md](ESTADO.md) | — |
| Aplicación y hoja vigentes, y las superadas | [ESTADO.md](ESTADO.md) | `python scripts/sistema.py` |
| Arquitectura de 3 capas | [README.md](README.md) sección 4 | Aplicación AppSheet vigente, ver `scripts/sistema.py` |
| El modelo de 28 tablas | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | `scripts/modelo_objetivo.py` |
| Lo que la hoja tiene hoy | [docs/bd.md](docs/bd.md) | `python scripts/generar_diccionario_bd.py` |
| Regla de geofencing, sin cablear todavía | [README.md](README.md) sección 5, [CLAUDE.md](CLAUDE.md) sección 6 | Expresión completa en `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` |
| Radio por tipo de activo | [README.md](README.md) sección 5 | `TIP_TiposActivo.RadioGeofencingKm` en `BD/Modelo_Datos_PLANTILLA.xlsx` |
| Los 27 tipos y las 18 familias del Plan Maestro | [README.md](README.md) sección 2 | `scripts/catalogo_tipos.py` |
| Flujos por actor | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) | — |
| Una sola forma por propósito | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) §6 | `DECISIONES` en `scripts/modelo_objetivo.py` |
| Reglas de cableado de referencias | [CLAUDE.md](CLAUDE.md) sección 6 | `python scripts/validar_modelo.py`, reglas V-14 a V-17 |
| Comportamiento de la plataforma | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | Cita textual y URL oficial por cada afirmación |
| Deriva documental | [CLAUDE.md](CLAUDE.md) sección 8 | `python scripts/verificar_documentos.py` |
| Enlaces rotos entre documentos | — | `python scripts/verificar_enlaces.py` |
| Columnas obligatorias vacías y referencias huérfanas en los datos | [CLAUDE.md](CLAUDE.md) sección 7.4 | `python scripts/verificar_datos.py` |
| Cableado real de la aplicación contra el declarado | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) §16 | `python scripts/auditar_cableado.py`, que emite [docs/CORRECCIONES_CABLEADO.md](docs/CORRECCIONES_CABLEADO.md) |
| Lo que solo es barato mientras las ocho tablas sigan vacías | [CLAUDE.md](CLAUDE.md) sección 7.17 | `python scripts/generar_encargo_ventana.py`, que emite [docs/ENCARGO_VENTANA.md](docs/ENCARGO_VENTANA.md); las filas vivas, con `python scripts/instantanea.py` |
| Dónde está cada control del editor en pantalla | [docs/ENCARGO_VENTANA.md](docs/ENCARGO_VENTANA.md) | `python scripts/navegacion_editor.py` |
| Capacidad y crecimiento | — | `python scripts/capacidad.py` |

---

## 5. Enlaces externos

- Aplicación AppSheet vigente: [abrir](https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e) — confirme el identificador contra `python scripts/sistema.py` antes de fiarse de un enlace guardado
- Backend Google Sheets vigente: [abrir](https://docs.google.com/spreadsheets/d/1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
*SGMC | Concesión Transversal del Sisga S.A.S.*
