# MAP.md — Índice maestro del proyecto

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 6 de agosto de 2026
**Propósito:** Mapa de navegación del repositorio. Dónde está cada cosa y qué contiene.

---

## 1. Por dónde empezar

| Si necesitas | Abre |
|---|---|
| Entender qué es el proyecto | [README.md](README.md) |
| Saber el estado real y qué está bloqueado | [docs/AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) |
| Enviar la definición funcional al cliente | [entregables/CORREO_ENVIO_MESA_DE_TRABAJO.md](entregables/CORREO_ENVIO_MESA_DE_TRABAJO.md) y el .docx adjunto |
| Trabajar sobre el repositorio como agente | [CLAUDE.md](CLAUDE.md) y las skills de `.claude/skills/` |
| Consultar la estructura de datos | [docs/bd.md](docs/bd.md) y `BD/Modelo de Datos (2).xlsx` |

---

## 2. Estructura de carpetas

```
D:\@Proyect\Sisga\
├── README.md                     Entrada del proyecto: qué es, cómo funciona, estado real
├── CLAUDE.md                     Reglas de trabajo para agentes
├── MAP.md                        Este archivo
│
├── BD/                           FUENTE DE VERDAD
│   └── Modelo de Datos (2).xlsx  24 hojas. Único archivo que se edita
│
├── docs/                         Documentación técnica y funcional
│   ├── DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md
│   ├── AUDITORIA_PLAN_Y_ROADMAP.md
│   ├── bd.md
│   ├── especificaciones.md
│   ├── especificaciones_visuales.md
│   ├── plan_de_trabajo.md
│   ├── ROADMAP.md
│   ├── GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md
│   ├── INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md
│   ├── DICTAMEN_AUDITORIA_LOCAL_SGMC.md
│   ├── images/                   fig_01 a fig_07, figuras de los documentos
│   └── prompts/                  Directivas para agentes de auditoría
│
├── Manuales/                     Manuales de usuario
│   ├── MANUAL_DE_USUARIO.md
│   ├── MANUAL_DE_USUARIO_ILUSTRADO.md
│   ├── Manual_de_Usuario_SGMC_Con_Diagramas.docx
│   └── images/                   img_01 a img_06, maquetas del manual
│
├── entregables/                  Listos para enviar al cliente
│   ├── Definicion_Funcional_SGMC_Mesa_de_Trabajo.docx
│   ├── CORREO_ENVIO_MESA_DE_TRABAJO.md
│   ├── Especificaciones_Tecnicas_SGMC_AsBuilt.docx
│   └── Modelo_Datos_SGMC_AsBuilt.xlsx
│
├── .claude/skills/               Skills del proyecto
│   ├── auditar-modelo/           Verificar producción vs Excel antes de afirmar nada
│   └── generar-entregables/      Regenerar figuras y documentos Word
│
├── scripts/                      Generadores
│   ├── _helpers_docx.py
│   ├── generate_figuras.py
│   ├── generate_especificaciones_docx.py
│   ├── generate_mesa_trabajo_docx.py
│   └── generate_user_manual_docx.py
│
└── archivo/                      Material de origen. No versionado
    └── legacy/                   ERS, plan original, levantamiento de UI, PDFs, video
```

---

## 3. Índice de documentos

### Definición y estado

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) | 6 casos de uso estilo ISTQB y 14 decisiones para el líder funcional | Vigente. Es el frente activo |
| [docs/AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) | Dictamen del 6 de agosto: 8 bloqueantes con evidencia y Fase 0 corregida | Vigente |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Fases con criterio de cierre verificable | Vigente |
| [docs/plan_de_trabajo.md](docs/plan_de_trabajo.md) | Plan operativo Audit-First | Supeditado a la mesa de trabajo |

### Especificación técnica

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/bd.md](docs/bd.md) | Diccionario de datos de las 24 tablas | Sección 3.1 desactualizada, ver CLAUDE.md |
| [docs/especificaciones.md](docs/especificaciones.md) | Requerimientos RF-001 a RF-016 | Vigente |
| [docs/especificaciones_visuales.md](docs/especificaciones_visuales.md) | Pantallas, vistas y elementos de interfaz | Vigente |
| [docs/GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md](docs/GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md) | Fórmulas SVG, botones y colores dinámicos | Vigente |

### Auditorías anteriores

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md](docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md) | Dictamen "100% conforme" | **Superado.** Certifica un modelo anterior con tablas vacías |
| [docs/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md](docs/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md) | Informe QA y simulación de flujo | **Superado.** Describe una ejecución sin respaldo en los datos |

### Manuales

| Documento | Contenido |
|---|---|
| [Manuales/MANUAL_DE_USUARIO.md](Manuales/MANUAL_DE_USUARIO.md) | Guías por rol: técnico, supervisor, administrador |
| [Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md](Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md) | Versión con maquetas de pantalla |
| [Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx](Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx) | Word. No es entregable ahora: aplica cuando la app esté lista para usarse |

### Prompts de auditoría

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/prompts/PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md](docs/prompts/PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md) | Directiva Audit-First | Por reescribir contra la Fase 0 corregida |
| [docs/prompts/PROMPT_VALIDACION_IA_EXTERNA.md](docs/prompts/PROMPT_VALIDACION_IA_EXTERNA.md) | Prompt para auditoría por IA externa | Vigente |

---

## 4. Matriz de referencias cruzadas

| Concepto | Dónde está documentado | Dónde está el dato real |
|---|---|---|
| Arquitectura de 3 capas | [README.md](README.md) sección 4 | Aplicación AppSheet `SGMC-886843353` |
| Modelo relacional de 24 tablas | [docs/bd.md](docs/bd.md) y [README.md](README.md) sección 5 | `BD/Modelo de Datos (2).xlsx` |
| Regla de geofencing | [CLAUDE.md](CLAUDE.md) sección 6 | `MAN_Mantenimientos[Coordenadas_Cierre]` en AppSheet |
| Requerimientos funcionales | [docs/especificaciones.md](docs/especificaciones.md) | — |
| Flujos por actor y casos de uso | [docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) parte II | — |
| Decisiones pendientes del funcional | [docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) parte III | — |
| Bloqueantes verificados | [docs/AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) sección 3 | Verificable con `openpyxl` sobre `BD/` |
| Fases y criterios de cierre | [docs/ROADMAP.md](docs/ROADMAP.md) | — |
| Pantallas y vistas | [docs/especificaciones_visuales.md](docs/especificaciones_visuales.md) | Aplicación AppSheet |
| Deriva documental conocida | [CLAUDE.md](CLAUDE.md) sección 8 | — |

---

## 5. Enlaces externos

- Aplicación AppSheet: [SGMC-886843353](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&view=Usuarios)
- Backend Google Sheets: [abrir](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
*SGMC | Concesión Transversal del Sisga S.A.S.*
