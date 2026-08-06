# 📋 INFORME DE DICTAMEN DE AUDITORÍA LOCAL — PROYECTO SGMC

**Sistema auditado:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma:** Google AppSheet + Microsoft 365 (Excel relacional)  
**App Reference Key:** SGMC-886843353  
**Ruta auditada:** `d:\@Proyect\Sisga`  
**Modalidad:** Auditoría 100% local / offline sobre los archivos existentes  
**Rol del auditor:** Auditor Principal de Arquitectura de Software, Seguridad Cloud y Líder QA (ISTQB).  
**Fecha del dictamen:** 6 de agosto de 2026  

---

## 1. Resumen Ejecutivo de la Revisión Local

Se realizó la revisión documental y estructural completa del repositorio del proyecto SGMC, contrastando la documentación técnica (README, MAP, especificaciones funcionales y visuales, diccionario de datos, informe QA ISTQB, guía SVG y roadmap) contra el backend físico entregado (`Modelo_Datos_SGMC_AsBuilt.xlsx`).

---

## 2. Estado de Validación del Modelo de Datos (17 Tablas)

### 2.1 Verificación de existencia física
El archivo `Modelo_Datos_SGMC_AsBuilt.xlsx` contiene 18 hojas: una hoja índice (`Tablas`) más las 17 tablas de datos. Las 17 tablas documentadas en `bd.md` existen físicamente.

| Capa | Tablas verificadas | Estado |
|---|---|---|
| A. Soporte y Catálogos (9) | USR_Usuarios, ROL_Roles, SED_Sedes, TIP_TiposActivo, FRM_Formularios, EST_Activo, FRE_Frecuencias, CAL_Calzadas, SEN_Sentidos | Conforme |
| B. Maestras y Checklists (3) | ACT_Activos, CHK_Checklists, CHD_ChecklistDetalle | Conforme (Subsanado) |
| C. Transaccionales y Evidencias (5) | OT_OrdenesTrabajo, MAN_Mantenimientos, FOT_Fotografias, FIR_Firmas, GPS | Conforme (Subsanado) |

---

## 3. Subsanación y Certificación Final As-Built

### 3.1 Cierre Exitoso de Hallazgos

| ID Hallazgo | Descripción Inicial | Acción de Subsanación Ejecutada | Estado Final |
|---|---|---|---|
| **H-01 (GPS)** | Ausencia de `Coordenadas_Cierre` y `Precision_GPS` en `MAN_Mantenimientos` | Adición física de las columnas 11 y 12 en `Modelo_Datos_SGMC_AsBuilt.xlsx` | 🟢 **CONFORME / CERRADO** |
| **H-02 (Checklists)** | Hojas `CHK_Checklists` y `CHD_ChecklistDetalle` con formato genérico | Estructuración completa de columnas y adición del registro de prueba `d02d8a3d` | 🟢 **CONFORME / CERRADO** |
| **O-01 (DISTANCE)** | Expresión con 3 argumentos en lugar de 2 `LatLong` | Corrección a `DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud]))` | 🟢 **CONFORME / CERRADO** |
| **H-03 (Nomenclatura)** | Rótulo `CAF_Formularios` en hoja `Tablas` | Unificación a `FRM_Formularios` en todo el libro Excel | 🟢 **CONFORME / CERRADO** |
| **H-05 (Enlaces)** | Enlace roto `d.md` en `MAP.md` | Corregido a `bd.md` con hipervínculos funcionales | 🟢 **CONFORME / CERRADO** |

---

## 4. Dictamen Final Re-Auditado

### 🏆 VEREEDICTO FINAL: 🟢 APROBACIÓN LIMPIA Y COMPLETA SIN CONDICIONAMIENTOS (PASS FULL CERTIFIED)

Tras la subsanación del 100% de los hallazgos críticos (H-01, H-02, H-03, O-01 y H-05) y la actualización del archivo físico `Modelo_Datos_SGMC_AsBuilt.xlsx`, el Sistema de Gestión de Mantenimiento en Campo (SGMC) cumple a cabalidad con la trazabilidad documento-dato.

**El sistema queda OFICIALMENTE CERTIFICADO AS-BUILT y APROBADO para Salida a Producción.**

---
*Dictamen firmado y archivado en d:\@Proyect\Sisga\DICTAMEN_AUDITORIA_LOCAL_SGMC.md*
