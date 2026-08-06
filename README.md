# 🚀 Sistema de Gestión de Mantenimiento en Campo (SGMC) — As-Built & Documentación Técnica

**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma de Despliegue:** Google AppSheet  
**App Reference Key:** SGMC-886843353  
**Estado:** 🟢 As-Built & Auditado para Salida a Producción (Agosto 2026)  
**URL de la Aplicación en Vivo:** [SGMC en AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  

---

## 📌 Visión General del Proyecto

El **SGMC** es la solución tecnológica diseñada para digitalizar la operación, inspección y mantenimiento preventivo/correctivo de la infraestructura vial de la Concesión Transversal del Sisga S.A.S. (Postes SOS, CCTV, PMVF, PMVM, Sensores Ambientales, Básculas, Peajes, Generadores, Fibra Óptica y equipos de TI).

La plataforma permite la operación **100% Offline** en corredor vial mediante dispositivos móviles (Android/iOS) con sincronización automática a una base de datos relacional de **17 tablas** alojada en Microsoft 365.

---

## 🗺️ Mapa de Navegación y Documentación Cruzada

Toda la documentación técnica y manuales de usuario están hipervinculados en el índice maestro:

| Documento | Descripción | Enlace |
|---|---|---|
| 🗺️ **MAP.md** | Mapa completo de archivos, rutas y referencias cruzadas | [MAP.md](./MAP.md) |
| 📖 **MANUAL_DE_USUARIO.md** | Manual de usuario y guía operativa (Técnicos, Supervisores, Admin) | [MANUAL_DE_USUARIO.md](./Manuales/MANUAL_DE_USUARIO.md) |
| 📱 **MANUAL_DE_USUARIO_ILUSTRADO.md** | Manual de usuario ilustrado con diagramas y maquetas visuales | [MANUAL_DE_USUARIO_ILUSTRADO.md](./Manuales/MANUAL_DE_USUARIO_ILUSTRADO.md) |
| 🛠️ **especificaciones.md** | Levantamiento técnico completo de lo construido (Funcional, UI, Reglas y Bots) | [especificaciones.md](./especificaciones.md) |
| 🗄️ **bd.md** | Diccionario de datos de 17 tablas, Diagrama ER, Tipos y Relaciones | [bd.md](./bd.md) |
| 📅 **plan_de_trabajo.md** | Plan de trabajo operativo para despliegue y piloto | [plan_de_trabajo.md](./plan_de_trabajo.md) |
| 📋 **DICTAMEN_AUDITORIA_LOCAL_SGMC.md** | Dictamen oficial de auditoría local 100% Conforme | [DICTAMEN_AUDITORIA_LOCAL_SGMC.md](./DICTAMEN_AUDITORIA_LOCAL_SGMC.md) |
| 🗺️ **ROADMAP.md** | Hoja de ruta de avance, estado actual (Fase 1 As-Built) y evolución a Fase 2 | [ROADMAP.md](./ROADMAP.md) |

---

## 🏗️ Arquitectura de la Solución (3 Capas)

`mermaid
graph TD
    UserMobile[Técnico Móvil - AppSheet App] -->|Operación Offline / Sync| AppEngine[Motor AppSheet Cloud]
    UserWeb[Supervisor / Interventor - Web] -->|Consulta & KPIs| AppEngine
    
    AppEngine -->|Security Filter por SedeID| Auth[SSO Google / Microsoft 365]
    AppEngine -->|Data Provider / REST| Backend[Microsoft 365 / Excel 17 Tablas]
    
    subgraph Capa_Datos [Capa de Datos - 17 Tablas Relacionales]
        Backend --> Lookups[Soporte & Catálogos - 9 Tablas]
        Backend --> Masters[Maestras & Checklists - 3 Tablas]
        Backend --> Trans[Transaccionales & Evidencias - 5 Tablas]
    end
    
    subgraph Automatizaciones [Motor de Automatización]
        AppEngine --> Bot[Automation Bot - Notificaciones PDF/Email]
    end
`

---
*SGMC - Concesión Transversal del Sisga S.A.S. | Agosto 2026*
