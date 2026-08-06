# 🛠️ ESPECIFICACIONES TÉCNICAS Y LEVANTAMIENTO AS-BUILT (especificaciones.md)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma Deployed:** Google AppSheet  
**App ID Key:** `SGMC-886843353`  
**URL de la Aplicación:** [SGMC en AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  
**Fecha:** Agosto de 2026 | **Versión:** 1.0 As-Built  

---

## 1. 📌 Resumen Ejecutivo

El presente documento especifica formalmente lo **construido e implementado (As-Built)** en la plataforma Google AppSheet para la Concesión Transversal del Sisga S.A.S. La solución digitaliza la operación de mantenimiento de activos viales (Postes SOS, CCTV, PMVF, PMVM, Sensores Ambientales, Básculas, Peajes, Generadores, Fibra Óptica y TI).

---

## 2. 📋 Matriz de Cumplimiento de Requerimientos (ERS v1.0)

| ID Requerimiento | Requerimiento Funcional ERS | Componente / Regla Construida en AppSheet | Estado As-Built |
|---|---|---|---|
| **RF-001** | Inicio de sesión corporativo | SSO Google / Microsoft 365 + Tabla `USR_Usuarios` | 🟢 Implementado |
| **RF-002** | Operación Offline obligatoria | Caché nativo de AppSheet mobile | 🟢 Implementado |
| **RF-003** | Sincronización automática al detectar red | Background Sync + Botón de resincronización | 🟢 Implementado |
| **RF-004** | Descarga acotada por zona/sede | `Security Filter:` `[SedeID] = LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "SedeID")` | 🟢 Implementado |
| **RF-005** | Ficha de activo (15 atributos) | Tabla `ACT_Activos` (PR, Calzada, Sentido, Lat/Lng, Estado, Foto) | 🟢 Implementado |
| **RF-006** | Apertura de activo por Código QR | Columna `CodigoQR` (`Searchable & Scan`) | 🟢 Implementado |
| **RF-007** | Formulario dinámico mantenimiento | Relación `TIP_TiposActivo` -> `FRM_Formularios` (18 plantillas) | 🟢 Implementado |
| **RF-008** | Checklists de inspección dinámicos | Modelo Padre-Hijo `CHK_Checklists` / `CHD_ChecklistDetalle` | 🟢 Implementado |
| **RF-009** | Captura de fotos (máx 6) | Tabla `FOT_Fotografias` (Compresión Low 600px) | 🟢 Implementado |
| **RF-010** | Firmas digitales manuscritas | Tabla `FIR_Firmas` (Campos tipo `Signature`) | 🟢 Implementado |
| **RF-011** | Captura automática de GPS | Expresiones `HERE()` e `Initial Value` `USERLOCATIONACCURACY()` | 🟢 Implementado |
| **RF-012** | Validaciones GPS (Geofencing 1 km) | `Valid_If:` `DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])) <= 1.0` | 🟢 Implementado |
| **RF-013** | Historial por activo | Inline View `MAN_Mantenimientos` en Ficha de Activo | 🟢 Implementado |
| **RF-014** | Reportes filtrables exportables | Vistas de consulta Web con exportación PDF/Excel | 🟢 Implementado |
| **RF-015** | Tablero de indicadores KPI | Vista Dashboard Web (Disponibilidad, Cumplimiento, Tiempos) | 🟢 Implementado |
| **RF-016** | Notificaciones por correo | AppSheet Automation Bot en evento `Adds and Updates` | 🟢 Implementado |

---

## 3. 📱 Diseño de Interfaz (UX), Menús y Vistas Construidas

### 3.1 Estructura de Menús
* **Navegación Móvil (Primary Views):**
  1. `Mis OT` (Tabla: `OT_OrdenesTrabajo` — agrupada por `[Periodo]` Año-Mes).
  2. `Activos` (Tabla: `ACT_Activos` — Dual View: Mapa + Tarjeta + Escáner QR).
  3. `Mantenimientos` (Tabla: `MAN_Mantenimientos` — lista de intervenciones).
  4. `Sincronización` (Estado de la cola offline).
* **Menú Lateral Hamburguesa (Menu Views):**
  * `Usuarios` (`#view=Usuarios` / Tabla: `USR_Usuarios` — perfiles, roles y sedes).
  * `Tipos de Activo` (Taxonomía ITS, Eléctrico y TI).
* **Portal Web de Administración:**
  * `Tablero KPI` (Dashboard multidimensional).
  * `Órdenes de Trabajo` (Programación y asignación).
  * `Reportes` (Generador de PDF/Excel).

---

## 4. ⚙️ Catálogo de Expresiones y Reglas de Negocio

### 4.1 Geofencing GPS (RF-012)
* **Columna:** `MAN_Mantenimientos[Coordenadas_Cierre]`
* **Expresión `Valid_If`:**
  ```excel
  DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])) <= 1.0
  ```

### 4.2 Precisión Satelital (Auditoría / Bypass)
* **Columna:** `MAN_Mantenimientos[Precision_GPS]`
* **Expresión `Initial Value`:**
  ```excel
  USERLOCATIONACCURACY()
  ```

### 4.3 Security Filter por Sede (RF-004)
* **Tablas Target:** `ACT_Activos` y `OT_OrdenesTrabajo`
* **Security Filter:**
  ```excel
  [SedeID] = LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "SedeID")
  ```

---

## 5. 🤖 Motor de Automatización (Automation Bots)

* **Bot:** `Notificación de Asignación y Alerta de Servicio`
* **Evento:** Data Change (`Adds and Updates`) sobre `MAN_Mantenimientos` u `OT_OrdenesTrabajo`.
* **Condición:** `OR([Estado] = "Pendiente", [Estado] = "Fuera de servicio")`
* **Acción:** Envía un correo electrónico estructurado con informe PDF adjunto al Supervisor y CCO.

---

## 6. 🧪 Protocolo de Pruebas de QA y Verificación

| ID Caso | Módulo | Prueba | Resultado Esperado | Criterio de Aceptación |
|---|---|---|---|---|
| **TC-SEC-01** | `USR_Usuarios` | Autenticación M365/Google | Carga perfil, rol y sede | `USEREMAIL()` resuelve en `USR_Usuarios` |
| **TC-SEC-02** | Security Filters | Login como Técnico Sede A | Solo descarga activos de Sede A | Descarga limitada en servidor |
| **TC-ACT-01** | Activos | Escaneo de Código QR | Abre ficha del activo | Muestra 15 atributos e historial |
| **TC-GPS-01** | Geofencing | Intento de cierre a > 1.0 km | Bloquea guardado | Mensaje de error por distancia |
| **TC-GPS-02** | Geofencing | Cierre a < 1.0 km | Guardado exitoso con GPS | Registra coordenadas y precisión |
| **TC-OFF-01** | Modo Offline | Registro sin señal móvil | Guarda en cola local | Sin errores de interfaz |
| **TC-OFF-02** | Sincronización | Reconectar red y Sync | Envía registros a OneDrive | Reflejado en Excel |

---
*Referencias Cruzadas:* [README.md](./README.md) | [bd.md](./bd.md) | [ROADMAP.md](./ROADMAP.md) | [MAP.md](./MAP.md)
