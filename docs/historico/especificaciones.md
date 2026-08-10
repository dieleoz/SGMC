> # Documento historico. NO SE APLICA.
>
> Especificaciones del 2026-08-06, antes de la reconstruccion. **Lo sustituye `docs/FUNCIONAL_SGMC.md`**.
>
> Se conserva por trazabilidad: explica por que se decidio lo que hay hoy.
> **El estado vigente esta en [`ESTADO.md`](../../ESTADO.md).**

# 🛠️ ESPECIFICACIONES TÉCNICAS Y REQUERIMIENTOS AS-BUILT (SGMC)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Backend en Producción (Google Sheets):** [Google Sheets Backend SGMC](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072)  
**Base de Datos Maestra (24 Hojas):** `d:\@Proyect\Sisga\BD\Modelo de Datos (2).xlsx`  
**Aplicación AppSheet:** [SGMC AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  
**Fecha:** Agosto de 2026 | **Versión:** 2.0 (Modelo de 24 Hojas)  

---

## 📌 1. Especificación de Requerimientos Funcionales (RF-001 al RF-016)

| ID Requerimiento | Nombre del Requerimiento | Descripción Técnica | Estado As-Built |
|---|---|---|---|
| **RF-001** | Autenticación Unificada M365 | Acceso mediante Single Sign-On (SSO) utilizando el correo corporativo M365 (`USEREMAIL()`). | 🟢 Conforme |
| **RF-002** | Operación 100% Offline | Almacenamiento local en caché de la app para zonas sin señal celular (túneles / montaña). | 🟢 Conforme |
| **RF-003** | Asignación de Órdenes de Trabajo | Creación y distribución de OTs por el CCO (`OT_OrdenesTrabajo`). | 🟢 Conforme |
| **RF-004** | Seguridad por Zona (RBAC) | Restricción de descarga de datos (`Security Filter`) según la `SedeID` del usuario. | 🟢 Conforme |
| **RF-005** | Ficha de Activo Completa | Despliegue de los 14 atributos de la tabla `ACT_Activos` (incluyendo `Ubicacion`). | 🟢 Conforme |
| **RF-006** | Escáner de Códigos QR | Lectura de QR mediante cámara móvil para apertura de activo. | 🟢 Conforme |
| **RF-007** | Formularios Dinámicos | Despliegue automático de checklists por tipo de activo (`FRM_SOS`, `FRM_CCTV`, etc.). | 🟢 Conforme |
| **RF-008** | Formularios de Inspección SOS | Inspección de gabinete, chasis, botón intercomunicador y panel solar. | 🟢 Conforme |
| **RF-009** | Formularios de CCTV y PMVF | Inspección de cámaras de tráfico, Domos, Paneles de Mensaje Variable. | 🟢 Conforme |
| **RF-010** | Evidencias Fotográficas | Registro de hasta 6 fotografías comprimidas a 600px en `FOT_Fotografias` (`IsPartOf`). | 🟢 Conforme |
| **RF-011** | Captura de Precisión GPS | Registro automático de `Precision_GPS` en metros mediante `USERLOCATIONACCURACY()`. | 🟢 Conforme |
| **RF-012** | Geofencing GPS de Cierre | Validación de cercanía al activo. La expresión candidata es `DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0`, pendiente de cablear las referencias. | No conforme |
| **RF-013** | Firma Manuscrita Digital | Captura táctil de firma del técnico en `FIR_Firmas` (`IsPartOf`). | 🟢 Conforme |
| **RF-014** | Portal Web para CCO | Interfaz para el CCO y supervisores en navegador web. | 🟢 Conforme |
| **RF-015** | Tablero de Indicadores KPI | Monitoreo en tiempo real de porcentaje de cumplimiento y disponibilidad. | 🟢 Conforme |
| **RF-016** | Notificación Automatizada por Email | Envió automático de correos con informe PDF cuando un activo se reporta *Fuera de servicio*. | 🟢 Conforme |

---

## ⚙️ 2. Reglas de Negocio Fórmulas Clave en AppSheet

### 2.1 Regla de Geofencing GPS (RF-012)
* **Campo Target:** `MAN_Mantenimientos[Coordenadas_Cierre]`
* **Fórmula Valid_If:**
  ```excel
  DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0
  ```
* **Texto de Error Personalizado (Invalid Text):**
  ```text
  Ubicación fuera de rango: debe estar a menos de 1.0 km del activo.
  ```

### 2.2 Security Filter por Sede (RF-004)
* **Fórmula de Seguridad:**
  ```excel
  [SedeID] = LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "SedeID")
  ```

---
*Especificaciones Técnicas SGMC | Concesión Transversal del Sisga S.A.S.*
