# 📅 PLAN DE TRABAJO Y HOJA DE RUTA OPERATIVA (SGMC)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma:** Google AppSheet (`SGMC-886843353`) + Microsoft 365  
**URL de la Aplicación:** [SGMC en AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  
**Estado de la Solución:** Re-auditado | **Fase Inicial Obligatoria:** Fase 0 Bloqueante  
**Fecha:** Agosto de 2026 | **Versión:** 2.0 (Con Fase 0 de Subsanación Estructural)  

---

## 🛑 1. Principio de Arranque: Fase 0 Bloqueante Primero

> **[!CRITICAL] REGLA DE ARRANQUE INMOCIONABLE PARA EL AGENTE:**  
> El agente **NO DEBE iniciar** por la Fase A (Piloto). Debe iniciar **OBLIGATORIAMENTE** por la **Fase 0 — Subsanación Estructural Bloqueante (Tareas T-00.1 a T-00.5)**.  
> Si se arranca el piloto sin verificar las columnas físicas de GPS y Checklists en Excel, las tareas T-03 (Geofencing) y Q-05 (Checklist y firmas) fallarán en campo por falta de almacenamiento de destino.

---

## 🗓️ 2. Cronograma de Trabajo Integrado (Gantt Mermaid)

```mermaid
gantt
    title Plan de Trabajo SGMC: Subsanación Bloqueante, Piloto y Producción
    dateFormat  YYYY-MM-DD
    section FASE 0: Subsanación Estructural (Bloqueante)
    T-00.1: Columnas GPS (Coordenadas_Cierre / Precision_GPS) :crit, active, f0_1, 2026-08-07, 2026-08-08
    T-00.2: Estructurar CHK_Checklists y CHD_ChecklistDetalle :crit, f0_2, 2026-08-08, 2026-08-09
    T-00.3: Nomenclatura FRM_Formularios en Hoja Tablas    :f0_3, 2026-08-09, 2026-08-09
    T-00.4: Aplicar DEF-FUNC-01 y DEF-FUNC-02 (Mensaje GPS)  :f0_4, 2026-08-09, 2026-08-10
    T-00.5: Ajuste Enlaces MAP.md y Catálogo Estados OT   :f0_5, 2026-08-10, 2026-08-10
    section FASE A: Preparación & Despliegue Móvil
    Instalación AppSheet App en Dispositivos               :a1, 2026-08-11, 2026-08-12
    Asignación de Roles & Sedes M365 (Security Filter)     :a2, 2026-08-12, 2026-08-13
    section FASE B: Piloto de Campo (Corredor Vial)
    Prueba de Carga Inicial Offline en Vía (Túneles)      :b1, 2026-08-14, 2026-08-16
    Ejecución Mantenimientos SOS, CCTV & Básculas         :b2, 2026-08-16, 2026-08-19
    Validación de Alertas Email Automation (PDF)           :b3, 2026-08-18, 2026-08-20
    section FASE C: Estabilización & Salida a Producción
    Ajustes de Caché & Calibración GPS Final              :c1, 2026-08-21, 2026-08-22
    Salida a Producción 100% Concesión Transversal Sisga  :c2, 2026-08-23, 2026-08-28
```

---

## 🛠️ 3. Matriz Detallada de Tareas por Agente y Fase

### 🛑 FASE 0 — SUBSANACIÓN ESTRUCTURAL BLOQUEANTE (INICIO OBLIGATORIO)
- [ ] **Tarea T-00.1 [BLOQUEANTE CRÍTICO]:** Verificar en `Modelo_Datos_SGMC_AsBuilt.xlsx` que la hoja `MAN_Mantenimientos` posea físicamente las columnas 11 y 12: `Coordenadas_Cierre` (`LatLong`, captura `HERE()`) y `Precision_GPS` (`Decimal`, `USERLOCATIONACCURACY()`).
- [ ] **Tarea T-00.2 [BLOQUEANTE CRÍTICO]:** Verificar en `Modelo_Datos_SGMC_AsBuilt.xlsx` que las hojas `CHK_Checklists` (9 columnas) y `CHD_ChecklistDetalle` (6 columnas) tengan sus esquemas de datos completos y el registro de prueba `d02d8a3d`.
- [ ] **Tarea T-00.3 [BLOQUEANTE]:** Confirmar que la hoja índice `Tablas` rotule `FRM_Formularios` en reemplazo de `CAF_Formularios`.
- [ ] **Tarea T-00.4 [BLOQUEANTE]:** Configurar en AppSheet las reglas `DEF-FUNC-01` (`Valid_If: ISNOTBLANK([Coordenadas_Cierre])`) y `DEF-FUNC-02` (Mensaje de error GPS personalizado: *"Debe activar el GPS de su celular y ubicarse a menos de 1.0 km del activo"*).
- [ ] **Tarea T-00.5 [BLOQUEANTE]:** Verificar hipervínculos en `MAP.md` y unificar el catálogo de estados de OT (`Programada`, `En Proceso`, `Finalizada`, `Cancelada`).

---

### 🛠️ FASE A — PREPARACIÓN Y CONFIGURACIÓN DE ENTORNO
- [ ] **Tarea T-01:** Conectar el Excel `Modelo_Datos_SGMC_AsBuilt.xlsx` verificado a AppSheet como Data Source principal.
- [ ] **Tarea T-02:** Marcar `SedeID` como `Required` en la tabla `USR_Usuarios` para garantizar el filtrado por sede (`Security Filter`).
- [ ] **Tarea T-03:** Validar la regla de Geofencing en AppSheet:
  `DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])) <= 1.0`
- [ ] **Tarea T-04:** Configurar compresión de imágenes en calidad `Low` (600px) en `FOT_Fotografias`.
- [ ] **Tarea T-05:** Configurar el Bot de Automatización de alertas por correo con informe PDF adjunto ante activos *Fuera de servicio*.

---

### 📱 FASE B — PILOTO DE CAMPO Y PRUEBAS QA
- [ ] **Tarea Q-01:** Instalar AppSheet en los 10 móviles del grupo piloto.
- [ ] **Tarea Q-02:** Autenticación M365 (`USEREMAIL()`) y prueba de descarga por zona.
- [ ] **Tarea Q-03:** Prueba de escáner QR sobre 5 activos en vía.
- [ ] **Tarea Q-04:** Prueba de bloqueo por rango GPS (> 1.0 km).
- [ ] **Tarea Q-05:** Prueba Offline en Modo Avión (checklist + 3 fotos + firma + Sync al recuperar red).

---

### 👤 FASE C — SUPERVISIÓN CCO Y PRODUCCIÓN 100%
- [ ] **Tarea S-01:** Asignación de OTs desde la interfaz Web ([#view=Usuarios](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)).
- [ ] **Tarea S-02:** Monitoreo del Tablero KPI de indicadores.
- [ ] **Tarea S-03:** Cierre de Acta de Aceptación Final por la Concesión Transversal del Sisga S.A.S.

---

## 🎯 4. Hitos de Entrega y Criterios de Aceptación

| Hito | Descripción | Criterio de Aceptación | Estado |
|---|---|---|---|
| **HITO-00** | Subsanación Estructural Verificada | Hojas `MAN_Mantenimientos`, `CHK_Checklists` y `CHD_ChecklistDetalle` con columnas físicas comprobadas en Excel | 🔲 **BLOQUEANTE (Paso 1)** |
| **HITO-01** | Despliegue Móvil | 100% de técnicos autenticados con SSO M365 y filtro por sede | 🔲 Pendiente |
| **HITO-02** | Registro Offline Exitoso | Checklist guardado sin señal celular y sincronizado a Excel | 🔲 Pendiente |
| **HITO-03** | Calibración GPS Validada | Geofencing (1.0 km) y Bypass en túneles operativos en vía | 🔲 Pendiente |
| **HITO-04** | Alerta CCO Operativa | Email con informe PDF recibido en el CCO tras falla en activo | 🔲 Pendiente |

---
*Plan de trabajo actualizado con Fase 0 Bloqueante.*  
*Referencias Cruzadas:* [README.md](./README.md) | [MAP.md](./MAP.md) | [especificaciones.md](./especificaciones.md) | [DICTAMEN_AUDITORIA_LOCAL_SGMC.md](./DICTAMEN_AUDITORIA_LOCAL_SGMC.md) | [Manuales/MANUAL_DE_USUARIO.md](./Manuales/MANUAL_DE_USUARIO.md)
