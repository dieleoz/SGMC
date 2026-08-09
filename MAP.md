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
| Ver la arquitectura correcta que se va a construir | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) |
| Saber cómo se comporta AppSheet, con la cita oficial | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) |
| Cablear una referencia, o entender por qué el geofencing no funciona | [docs/sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) |
| Saber qué necesita la operación y qué de eso no cabe hoy en AppSheet | [docs/sdd/ESPEC-003-modelo-de-dominio.md](docs/sdd/ESPEC-003-modelo-de-dominio.md) |
| Construir cualquier cambio, y saber qué se aprueba antes de tocar producción | [docs/SDD_PIPELINE_SGMC.md](docs/SDD_PIPELINE_SGMC.md) |
| Saber hasta dónde aguanta el sistema | `python scripts/capacidad.py` |
| Saber con qué supuestos se construye | [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) |
| Ejecutar la construcción | [docs/prompts/PROMPT_CONSTRUCCION_SGMC.md](docs/prompts/PROMPT_CONSTRUCCION_SGMC.md) |
| Saber el estado real y qué está bloqueado | [docs/AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) |
| Enviar la definición funcional al cliente | [entregables/CORREO_ENVIO_MESA_DE_TRABAJO.md](entregables/CORREO_ENVIO_MESA_DE_TRABAJO.md) y el .docx adjunto |
| Trabajar sobre el repositorio como agente | [CLAUDE.md](CLAUDE.md) y las skills de `.claude/skills/` |
| Consultar la estructura de datos real | [docs/bd.md](docs/bd.md), generado desde `BD/Modelo de Datos (9).xlsx` |

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
│   ├── historico/                 Documentos retirados. No usar como fuente
│   ├── BASE_CONOCIMIENTO_APPSHEET.md   Comportamiento verificado contra Google
│   ├── ARQUITECTURA_OBJETIVO_SGMC.md
│   ├── SDD_PIPELINE_SGMC.md
│   ├── ALCANCE_Y_SUPUESTOS_SGMC.md
│   ├── DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md
│   ├── AUDITORIA_PLAN_Y_ROADMAP.md
│   ├── bd.md
│   ├── especificaciones.md
│   ├── especificaciones_visuales.md
│   ├── plan_de_trabajo.md
│   ├── ROADMAP.md
│   ├── GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md
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
│   ├── Propuesta_Arquitectura_SGMC.docx
│   ├── Definicion_Funcional_SGMC_Mesa_de_Trabajo.docx
│   ├── CORREO_ENVIO_MESA_DE_TRABAJO.md
│   ├── Especificaciones_Tecnicas_SGMC_AsBuilt.docx
│   └── Modelo_Datos_SGMC_AsBuilt.xlsx
│
├── .claude/skills/               Skills del proyecto
│   ├── auditar-modelo/           Verificar producción vs Excel antes de afirmar nada
│   ├── revisar-arquitectura/     Validar el diseño desde 6 ángulos antes de construir
│   └── generar-entregables/      Regenerar figuras y documentos Word
│
├── scripts/                      Generadores
│   ├── _helpers_docx.py
│   ├── generate_figuras.py
│   ├── capacidad.py
│   ├── generar_doc_arquitectura.py
│   ├── generate_especificaciones_docx.py
│   ├── generate_propuesta_docx.py
│   ├── modelo_objetivo.py
│   ├── validar_modelo.py
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
| [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | Modelo objetivo: 27 tablas, 192 columnas, 38 referencias, 13 reglas. Generado y validado | **Vigente. Es el frente activo** |
| [docs/historico/](docs/historico/) | **Documentos retirados el 2026-08-07.** Describen estados superados y por eso salieron de `docs/`: seguirlos induce a deshacer trabajo correcto | Histórico. No usar como fuente |
| [docs/SDD_PIPELINE_SGMC.md](docs/SDD_PIPELINE_SGMC.md) | Método de construcción: cinco agentes, dos fases, el gate antes del paso caro y la decisión de descartar el QR | **Vigente. Es el método** |
| [docs/sdd/ESPEC-001-preparacion-del-sheets.md](docs/sdd/ESPEC-001-preparacion-del-sheets.md) | Fase A del cableado: todo lo que se hace sobre la hoja sin abrir AppSheet. Verificada contra producción | **Vigente** |
| [scripts/faseA_sheets.gs](scripts/faseA_sheets.gs) | La Fase A como Apps Script. Google bloqueó su ejecución en esta cuenta | Histórico |
| [docs/sdd/ESPEC-001B-cierre-de-la-fase-a.md](docs/sdd/ESPEC-001B-cierre-de-la-fase-a.md) | Los 23 fallos que faltaban para cerrar la Fase A | Aplicado |
| [docs/sdd/ACTA-001-cierre-de-la-fase-a.md](docs/sdd/ACTA-001-cierre-de-la-fase-a.md) | Acta de cierre de la Fase A: qué se aplicó, qué se verificó y qué sigue pendiente a propósito | Vigente |
| [docs/sdd/ESPEC-001C-baja-de-activos-y-datos-de-prueba.md](docs/sdd/ESPEC-001C-baja-de-activos-y-datos-de-prueba.md) | Baja de activos, doctrina de reportes históricos y poblado de prueba | Aplicado |
| [docs/sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md](docs/sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md) | Cierre de la Fase A y el incidente de método del verificador editado | Vigente |
| [docs/sdd/ACTA-003-cierre-de-la-hoja.md](docs/sdd/ACTA-003-cierre-de-la-hoja.md) | Cierre definitivo de la hoja, y las dos alucinaciones que paró el verificador | Vigente |
| [docs/prompts/PROMPT_AGENTE_HOJA_ESPEC_001C.md](docs/prompts/PROMPT_AGENTE_HOJA_ESPEC_001C.md) | Prompt autocontenido para el agente que trabaja sobre la hoja | Aplicado |
| [docs/prompts/PROMPT_AGENTE_HOJA_CIERRE_FASE_A.md](docs/prompts/PROMPT_AGENTE_HOJA_CIERRE_FASE_A.md) | Las cuatro ediciones de contenido de la hoja | Aplicado |
| [docs/prompts/PROMPT_AGENTE_HOJA_FORMATOS.md](docs/prompts/PROMPT_AGENTE_HOJA_FORMATOS.md) | Normalizar formatos: identificadores como texto y quitar las fórmulas | Aplicado |
| [docs/sdd/ACTA-004-cierre-de-formatos.md](docs/sdd/ACTA-004-cierre-de-formatos.md) | Cierre de formatos, y el defecto sistémico de leer fórmulas en vez de valores | Vigente |
| [docs/sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) | Fase B: cableado en AppSheet, con orden obligatorio, verificación y reversión | **Vigente. Es el frente activo** |
| [docs/sdd/ESPEC-003-modelo-de-dominio.md](docs/sdd/ESPEC-003-modelo-de-dominio.md) | El modelo de dominio en dos planos: qué quiere la operación y qué cabe hoy en AppSheet. Capa de tareas, jerarquía de ubicación, roles, correctivo y recepción del trabajo. Incluye la tabla de lo NO REALIZABLE HOY | Propuesta. **No se aplica hasta cerrar la Fase B**: declarar sus tablas antes bloquea `ESPEC-002` |
| [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) | Alcance del sistema completo y los 14 supuestos adoptados | Vigente |
| [docs/prompts/PROMPT_CONSTRUCCION_SGMC.md](docs/prompts/PROMPT_CONSTRUCCION_SGMC.md) | Directiva de construcción en 7 pasos con criterios de aceptación | Vigente |
| [docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) | 6 casos de uso estilo ISTQB y 14 decisiones | Enviado. Sus propuestas son ahora los supuestos adoptados |
| [docs/AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) | Dictamen del 6 de agosto: 8 bloqueantes con evidencia y Fase 0 corregida | Vigente |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Fases con criterio de cierre verificable | Vigente |
| [docs/plan_de_trabajo.md](docs/plan_de_trabajo.md) | Plan operativo Audit-First | Supeditado a la mesa de trabajo |

### Especificación técnica

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/bd.md](docs/bd.md) | **Diccionario As-Built, generado.** Las 32 hojas reales, con el estado de cada columna | Vigente. Se regenera, no se edita |
| [docs/especificaciones.md](docs/especificaciones.md) | Requerimientos RF-001 a RF-016 | Vigente |
| [docs/especificaciones_visuales.md](docs/especificaciones_visuales.md) | Pantallas, vistas y elementos de interfaz | Vigente |
| [docs/GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md](docs/GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md) | Fórmulas SVG, botones y colores dinámicos | Vigente |

### Auditorías anteriores

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/historico/DICTAMEN_AUDITORIA_LOCAL_SGMC.md](docs/historico/DICTAMEN_AUDITORIA_LOCAL_SGMC.md) | Dictamen "100% conforme" | **Retirado el 2026-08-07.** Certifica un modelo anterior con tablas vacías |
| [docs/historico/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md](docs/historico/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md) | Informe QA y simulación de flujo | **Retirado el 2026-08-07.** Describe una ejecución sin respaldo en los datos |

### Manuales

| Documento | Contenido |
|---|---|
| [Manuales/MANUAL_DE_USUARIO.md](Manuales/MANUAL_DE_USUARIO.md) | Guías por rol: técnico, supervisor, administrador |
| [Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md](Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md) | Versión con maquetas de pantalla |
| [Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx](Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx) | Word. No es entregable ahora: aplica cuando la app esté lista para usarse |

### Prompts de auditoría

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/prompts/PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md](docs/prompts/PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md) | Directiva Audit-First | **Superado** por PROMPT_CONSTRUCCION_SGMC.md |
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
| Cableado de referencias | [docs/sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) | `python scripts/validar_modelo.py`, reglas V-14 a V-17 |
| Comportamiento de la plataforma | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | Cita textual y URL oficial por cada afirmación |
| Estado real de una columna | [docs/bd.md](docs/bd.md) | `python scripts/generar_diccionario_bd.py` |
| Pantallas y vistas | [docs/especificaciones_visuales.md](docs/especificaciones_visuales.md) | Aplicación AppSheet |
| Deriva documental conocida | [CLAUDE.md](CLAUDE.md) sección 8 | — |

---

## 5. Enlaces externos

- Aplicación AppSheet: [SGMC-886843353](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&view=Usuarios)
- Backend Google Sheets: [abrir](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
*SGMC | Concesión Transversal del Sisga S.A.S.*

## Frente de reconstruccion (2026-08-09)

| Documento | Que es |
|---|---|
| [`docs/prompts/PROMPT_AGENTE_APPSHEET_FASE_B.md`](docs/prompts/PROMPT_AGENTE_APPSHEET_FASE_B.md) | **El instructivo vigente.** Las 38 referencias, los tipos, las reglas y las trampas |
| [`docs/COMUNICACION_PROPIETARIO_APP.md`](docs/COMUNICACION_PROPIETARIO_APP.md) | Que comunicarle al propietario de la app original, con borrador del mensaje |
| [`docs/FUNCIONAL_SGMC.md`](docs/FUNCIONAL_SGMC.md) | Que hace el sistema. Su §6 es el registro de una sola forma por proposito |
| [`docs/sdd/RECONSTRUCCION_EXPRESIONES.md`](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) | Los 27 nombres renombrados y las 20 reglas a reponer |
| [`docs/BASE_CONOCIMIENTO_APPSHEET.md`](docs/BASE_CONOCIMIENTO_APPSHEET.md) | 12 comportamientos verificados. §11 y §12 son los que cambiaron el plan |
| [`docs/CONTEXTO_OPERACION.md`](docs/CONTEXTO_OPERACION.md) | Como se mantiene el corredor de verdad |

**Obsoleto:** `docs/ENTREGA_TECNICA_SGMC.md` describe reparar la app vieja tabla por tabla. Se
abandono ese camino.
