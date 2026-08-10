# MAP.md — Índice maestro del proyecto

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 10 de agosto de 2026
**Propósito:** Mapa de navegación del repositorio. Dónde está cada cosa y qué contiene.

> **Este archivo dice dónde está cada cosa, no en qué punto va el proyecto.**
> Para el estado, [`ESTADO.md`](ESTADO.md).

---

## 1. Por dónde empezar

| Si necesitas | Abre |
|---|---|
| Saber en qué punto va el proyecto y qué falta | [ESTADO.md](ESTADO.md) |
| Entender qué es el proyecto | [README.md](README.md) |
| Saber qué te toca a ti, según tu rol | [docs/INDICACIONES_POR_ROL.md](docs/INDICACIONES_POR_ROL.md) |
| Entender qué hace el sistema y para quién | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) |
| Ver la arquitectura que se va a construir | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) |
| Construir o configurar la aplicación | [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) |
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
│   ├── images/                    fig_01 a fig_07, figuras de los documentos
│   └── sdd/                       Artefactos vigentes del pipeline: ESPEC-003 (bloqueada),
│                                   PRUEBA-003 y RECONSTRUCCION_EXPRESIONES
│
├── Manuales/                     Manual de usuario
│   └── MANUAL_DE_USUARIO.md
│
├── entregables/                  Word y Excel enviados o publicados antes de la reconstrucción
│
├── scripts/                      Fuente del modelo, validadores y generadores
│   ├── modelo_objetivo.py         FUENTE ÚNICA. De aquí sale todo lo demás
│   ├── sistema.py                 La aplicación y la hoja vigentes, y las superadas con su motivo
│   ├── catalogo_tipos.py          Los 27 tipos de activo y las 18 familias del Plan Maestro
│   ├── validar_modelo.py          Gate objetivo del pipeline
│   ├── verificar_faseA.py         El modelo contra la hoja descargada
│   ├── verificar_documentos.py    La prosa contra el modelo
│   ├── verificar_enlaces.py       Que todo enlace relativo entre documentos resuelve
│   └── generar_*.py               Generadores de la plantilla y de los documentos
│
├── contexto/                     Material de contexto operativo, no versionado. No es la vara
└── archivo/                      Material de origen, no versionado
```

---

## 3. Índice de documentos

### Estado y método

| Documento | Contenido | Vigencia |
|---|---|---|
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
| [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | Modelo objetivo: 28 tablas, 202 columnas, 38 referencias, 20 reglas | Vigente. **Se regenera, no se edita** |
| [docs/bd.md](docs/bd.md) | Diccionario As-Built: lo que la hoja tiene hoy, columna a columna | Vigente. **Se regenera, no se edita** |
| [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) | De cero a app desplegada, con la ficha de las 28 tablas columna por columna | Vigente. Generado |
| [docs/sdd/RECONSTRUCCION_EXPRESIONES.md](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) | Los nombres renombrados y las 20 reglas a reponer, sin cortar | Vigente |
| [docs/sdd/PRUEBA-003-despliegue.md](docs/sdd/PRUEBA-003-despliegue.md) | Las pruebas de aceptación del despliegue reconstruido | Vigente |

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
| Capacidad y crecimiento | — | `python scripts/capacidad.py` |

---

## 5. Enlaces externos

- Aplicación AppSheet vigente: [abrir](https://www.appsheet.com/template/appdef?appId=d180a1b5-19ca-448e-a44c-f985396dce12) — confirme el identificador contra `python scripts/sistema.py` antes de fiarse de un enlace guardado
- Backend Google Sheets vigente: [abrir](https://docs.google.com/spreadsheets/d/1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
*SGMC | Concesión Transversal del Sisga S.A.S.*
