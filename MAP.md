# 🗺️ MAPA DEL PROYECTO Y MATRIZ DE REFERENCIAS CRUZADAS (MAP.md)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Aplicación en Vivo:** [SGMC en AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  
**Propósito:** Índice maestro de archivos, especificaciones visuales, guías técnicas, dictámenes de auditoría, manuales ilustrados en /Manuales y prompt de validación para auditorías externas.

---

## 📂 Estructura Limpia de Archivos (d:\@Proyect\Sisga)

`
d:\@Proyect\Sisga\
├── README.md                                  <- Visión general, arquitectura de 3 capas y enlace a AppSheet
├── MAP.md                                     <- Mapa de navegación e índice de referencias cruzadas (ESTE ARCHIVO)
├── ROADMAP.md                                 <- Hoja de ruta de implementación As-Built y evolución
├── plan_de_trabajo.md                         <- Plan de trabajo operativo para el agente / equipo de despliegue
├── especificaciones.md                        <- Especificaciones técnicas funcionales (RF-001 al RF-016)
├── especificaciones_visuales.md               <- Levantamiento de pantallas visuales y elementos DOM de la app
├── bd.md                                      <- Especificación técnica de Base de Datos (17 tablas, ER)
├── GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md    <- Guía rescatada de legacy: SVG dinámicos, botones y colores
├── INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md <- Informe ISTQB, simulación de flujo, guardado y hallazgos
├── DICTAMEN_AUDITORIA_LOCAL_SGMC.md           <- Dictamen oficial de auditoría local 100% Conforme
├── PROMPT_VALIDACION_IA_EXTERNA.md            <- Prompt maestro listo para enviar a otra IA para auditar
├── PROMPT_PARA_AGENTE_AUDITOR_Y_SUBSANADOR.md <- Directiva Audit-First para que el agente audite primero y subsane después            <- Prompt maestro listo para enviar a otra IA para auditar
├── Modelo_Datos_SGMC_AsBuilt.xlsx             <- Base de datos Excel construida y subsanada (17 Hojas)
├── Especificaciones_Tecnicas_SGMC_AsBuilt.docx <- Documento formal en Word
├── 📁 Manuales/                               <- Carpeta oficial de manuales de usuario y operación
│   ├── MANUAL_DE_USUARIO.md                   <- Manual de usuario completo (Técnicos, Supervisores, Admin)
│   ├── MANUAL_DE_USUARIO_ILUSTRADO.md         <- Manual con diagramas y maquetas visuales de pantallas
│   ├── Manual_de_Usuario_SGMC_Con_Diagramas.docx <- Documento ejecutable Word listo para enviar al líder funcional
│   └── generate_user_manual_docx.py           <- Script Python generador del manual Word
└── 📁 legacy/                                 <- Insumos originales, PDFs, videos y borradores
`

---

## 🔗 Matriz de Referencias Cruzadas (Cross-Reference Matrix)

| Concepto / Componente | Archivo Documentado | Sección Específica | Enlace Directo |
|---|---|---|---|
| **Arquitectura de Software** | README.md | Sección 3: Arquitectura | [README.md](./README.md) |
| **Manual de Usuario Ilustrado (Word para Entrega)** | Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx | Documento Word | [Manual Word](./Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx) |
| **Manual de Usuario Ilustrado en Línea** | Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md | Sección 2 y 3: Pantallas | [MANUAL_DE_USUARIO_ILUSTRADO.md](./Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md) |
| **Manual de Usuario Operativo** | Manuales/MANUAL_DE_USUARIO.md | Sección 2 a 4: Guías por Rol | [MANUAL_DE_USUARIO.md](./Manuales/MANUAL_DE_USUARIO.md) |
| **Script Generador del Manual Word** | Manuales/generate_user_manual_docx.py | Script Python | [generate_user_manual_docx.py](./Manuales/generate_user_manual_docx.py) |
| **Plan de Trabajo y Despliegue** | plan_de_trabajo.md | Sección 2 y 3: Cronograma y Tareas | [plan_de_trabajo.md](./plan_de_trabajo.md) |
| **Especificación de Requerimientos (RF-001 a RF-016)** | especificaciones.md | Sección 2: Matriz RF | [especificaciones.md](./especificaciones.md) |
| **Navegación Visual y Pantallas Capturadas** | especificaciones_visuales.md | Sección 2: Vistas Capturadas | [especificaciones_visuales.md](./especificaciones_visuales.md) |
| **Modelo ER (24 Tablas)** | bd.md | Sección 2: Diagrama ER | [bd.md](./bd.md) |
| **Definición Funcional y Mesa de Trabajo (Validación con el Funcional)** | DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md | Parte II: Flujos y Parte III: 14 Decisiones | [DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](./DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) |
| **Instrucciones para Agentes (Fuente de Verdad y Convenciones)** | CLAUDE.md | Secciones 2, 3 y 7 | [CLAUDE.md](./CLAUDE.md) |
| **Dictamen de Auditoría Vigente (Plan y Roadmap)** | AUDITORIA_PLAN_Y_ROADMAP.md | Sección 3 y 6 | [AUDITORIA_PLAN_Y_ROADMAP.md](./AUDITORIA_PLAN_Y_ROADMAP.md) |
| **Diseño SVG y Botones Dinámicos** | GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md | Sección 2 y 4: Fórmulas SVG | [GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md](./GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md) |
| **Informe QA (ISTQB) y Evaluación de Flujo** | INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md | Sección 2 a 4: Flujo y Hallazgos | [INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md](./INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md) |
| **Dictamen Oficial de Auditoría Local** | DICTAMEN_AUDITORIA_LOCAL_SGMC.md | Sección 3 y 4: Cierre de Hallazgos | [DICTAMEN_AUDITORIA_LOCAL_SGMC.md](./DICTAMEN_AUDITORIA_LOCAL_SGMC.md) |
| **Prompt para Auditoría por IA Externa** | PROMPT_VALIDACION_IA_EXTERNA.md | Prompt Maestro | [PROMPT_VALIDACION_IA_EXTERNA.md](./PROMPT_VALIDACION_IA_EXTERNA.md) |
| **Roadmap y Fases** | ROADMAP.md | Sección 2: Detalle Fases | [ROADMAP.md](./ROADMAP.md) |

---
*SGMC Document Map | Concesión Transversal del Sisga S.A.S.*
