# 📋 INFORME DE DICTAMEN DE AUDITORÍA LOCAL — PROYECTO SGMC

**Sistema auditado:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma:** Google AppSheet + Microsoft 365 (Excel relacional)  
**App Reference Key:** SGMC-886843353  
**Ruta auditada:** `d:\@Proyect\Sisga`  
**Modalidad:** Auditoría 100% local / offline sobre los archivos existentes  
**Rol del auditor:** Auditor Principal de Arquitectura de Software, Seguridad Cloud y Líder QA (ISTQB)  
**Fecha del dictamen:** 6 de agosto de 2026  

---

## 1. Resumen Ejecutivo de la Revisión Local

Se realizó la revisión estructural del repositorio del proyecto SGMC, contrastando la documentación técnica contra el backend físico (`Modelo_Datos_SGMC_AsBuilt.xlsx`).

* **Dictamen Inicial:** Aprobación Condicionada (debido a hallazgos H-01 en GPS y H-02 en Checklists).
* **Fase Exigida:** **Fase 0 — Subsanación Estructural Bloqueante (T-00.1 a T-00.5)** como requisito previo inmocionable antes del despliegue del Grupo Piloto.

---

## 2. Estado de Validación del Modelo de Datos (17 Tablas)

| Capa | Tablas verificadas | Estado |
|---|---|---|
| A. Soporte y Catálogos (9) | USR_Usuarios, ROL_Roles, SED_Sedes, TIP_TiposActivo, FRM_Formularios, EST_Activo, FRE_Frecuencias, CAL_Calzadas, SEN_Sentidos | Conforme |
| B. Maestras y Checklists (3) | ACT_Activos, CHK_Checklists, CHD_ChecklistDetalle | Conforme (Fase 0 Verificada) |
| C. Transaccionales y Evidencias (5) | OT_OrdenesTrabajo, MAN_Mantenimientos, FOT_Fotografias, FIR_Firmas, GPS | Conforme (Fase 0 Verificada) |

---

## 3. Matriz de Subsanaciones de la Fase 0 Bloqueante

| Tarea Fase 0 | ID Hallazgo | Descripción | Acción de Subsanación Ejecutada | Estado |
|---|---|---|---|---|
| **T-00.1** | **H-01 (GPS)** | Ausencia de columnas GPS en `MAN_Mantenimientos` | Adición física de las columnas 11 y 12 (`Coordenadas_Cierre` y `Precision_GPS`) en Excel | 🟢 **VERIFICADO PASS** |
| **T-00.2** | **H-02 (Checklists)** | Hojas `CHK_Checklists` y `CHD_ChecklistDetalle` con formato genérico | Estructuración completa de 9 cols en CHK y 6 cols en CHD con registro de prueba `d02d8a3d` | 🟢 **VERIFICADO PASS** |
| **T-00.3** | **H-03 (Nomenclatura)** | Rótulo `CAF_Formularios` en hoja `Tablas` | Unificación a `FRM_Formularios` en la hoja índice | 🟢 **VERIFICADO PASS** |
| **T-00.4** | **DEF-FUNC-01/02** | Expresión de Geofencing y Mensaje de error | Aplicación de `Valid_If: ISNOTBLANK([Coordenadas_Cierre])` y mensaje de error GPS personalizado | 🟢 **VERIFICADO PASS** |
| **T-00.5** | **H-05 (Enlaces)** | Enlace roto `d.md` en `MAP.md` y catálogo OT | Corregido a `bd.md` y unificado catálogo de estados de OT (`Programada`, `En Proceso`, `Finalizada`) | 🟢 **VERIFICADO PASS** |

---

## 4. Dictamen Final de Auditoría

### 🏆 VEREDICTO FINAL TRAS FASE 0: 🟢 APROBACIÓN LIMPIA Y COMPLETA (PASS CERTIFIED)

Tras la verificación e inspección física del 100% de las tareas de la **Fase 0 Bloqueante (T-00.1 a T-00.5)** en el backend `Modelo_Datos_SGMC_AsBuilt.xlsx`, el sistema SGMC queda habilitado para iniciar las Tareas T-01/T-02 de la Fase A y el despliegue del Grupo Piloto.

---
*Dictamen firmado y archivado en d:\@Proyect\Sisga\DICTAMEN_AUDITORIA_LOCAL_SGMC.md*
