> # Documento historico. NO SE APLICA.
>
> Validacion externa del 2026-08-06. El proyecto tiene ahora sus propios verificadores y agentes.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# 🤖 PROMPT MAESTRO PARA AUDITORÍA Y VALIDACIÓN POR IA EXTERNA

**Instrucción:** Copia y pega el siguiente prompt completo en cualquier agente de IA o modelo de lenguaje (ChatGPT, Claude, Gemini, Copilot, DeepSeek) para solicitar una auditoría técnica externa e imparcial del proyecto SGMC.

---

```markdown
PROMPT DE AUDITORÍA TÉCNICA EXTERNA PARA SISTEMA SGMC (APPSHEET)

Actúa como un Auditor Principal de Arquitectura de Software y Seguridad Cloud. Tu objetivo es auditar y validar el repositorio del proyecto "Sistema de Gestión de Mantenimiento en Campo (SGMC)" desarrollado para la Concesión Transversal del Sisga S.A.S. sobre Google AppSheet y Microsoft 365.

URL del Sistema Auditado:
https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios

Instrucciones de Auditoría:

1. Revisa los siguientes archivos del repositorio:
   - README.md (Arquitectura general de 3 capas)
   - MAP.md (Mapa de navegación e índice de referencias cruzadas)
   - especificaciones.md (Requerimientos funcionales RF-001 al RF-016 y reglas de negocio)
   - bd.md (Modelo relacional de 17 tablas y diagrama ER)
   - ROADMAP.md (Estado de la Fase 1 As-Built)
   - Modelo_Datos_SGMC_AsBuilt.xlsx (Base de datos relacional en Excel con 17 hojas)
   - Especificaciones_Tecnicas_SGMC_AsBuilt.docx (Documentación formal en Word)

2. Evalúa los siguientes puntos críticos de auditoría:
   A. Integridad del Modelo de Datos (17 Tablas): Verifica si la estructura relacional cumple con la jerarquía de 4 niveles (OT -> Mantenimientos -> Fotografías/Firmas/GPS).
   B. Seguridad y Particionamiento (RF-004): Evalúa la regla de Security Filter:
      [SedeID] = LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "SedeID")
   C. Regla Geofencing GPS (RF-012): Valida la fórmula de restricción de distancia de 1.0 km:
      DISTANCE([Coordenadas_Cierre], [ActivoID].[Latitud], [ActivoID].[Longitud]) <= 1.0
   D. Operación Offline (RF-002/RF-003): Revisa si la estrategia de caché local y sincronización en segundo plano cumple las restricciones viales.

3. Emite un Informe de Auditoría con la siguiente estructura:
   - Resumen Ejecutivo de Evaluación.
   - Tabla de Verificación de Requerimientos (RF-001 a RF-016) con estado (Aprobado / Rechazado / Con Observaciones).
   - Análisis de Riesgos Técnicos (Latencia, Caché móvil, Cobertura GPS).
   - Dictamen Final de Auditoría (Favorable / Desfavorable) para salida a Producción.
```

---
*Referencias Cruzadas:* [README.md](../../README.md) | [especificaciones.md](../../docs/especificaciones.md) | [especificaciones_visuales.md](../../docs/especificaciones_visuales.md) | [MAP.md](../../MAP.md)
