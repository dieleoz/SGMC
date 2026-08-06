# 🗄️ ESPECIFICACIÓN TÉCNICA DE BASE DE DATOS (bd.md)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Motor de Base de Datos:** Microsoft 365 / Excel Relacional + AppSheet Data Engine  
**Archivo Físico Backend:** `Modelo_Datos_SGMC_AsBuilt.xlsx`  
**Aplicación:** [SGMC en AppSheet](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&vss=H4sIAAAAAAAAA6XOvQ7CIBQF4Hc5M0_AahyM0cWfRTpguU2ILTQF1Ibw7t6qjbM6csh37sm4Wrrtoq4vkKf8ea1phERW2I89KUiFhXdx8K2CUNjq7hUeQtKD9UGhoFRi9pECZP6Oy_-uC1hDLtrG0jB1TZI73o6_J8XBbFAEuhT1uaXnYDalcNb4OgUyR57yw4Swcst7r53ZeMOVjW4DlQcPF0XqZQEAAA==&view=Usuarios)  

---

## 1. 📌 Visión General del Modelo de Datos (17 Tablas)

El modelo de datos implementado en AppSheet se compone de **17 tablas relacionales** organizadas en tres capas de persistencia para garantizar la integridad referencial y el rendimiento en dispositivos móviles.

---

## 2. 📐 Diagrama Entidad-Relación (ER As-Built)

```
+----------------+       +----------------+       +------------------+
|   SED_Sedes    |1----* |  USR_Usuarios  | *---1 |    ROL_Roles     |
+----------------+       +----------------+       +------------------+
                                 | 1
                                 |
                                 *
                         +----------------+
                         |OT_OrdenesTrabajo|
                         +----------------+
                                 | 1
                                 |
                                 *
                         +----------------+
                         |MAN_Mantenimientos|
                         +----------------+
                          /      |       \
                         /       |        \
                        *        *         *
             +------------+ +----------+ +-----+
             |FOT_Fotografias| |FIR_Firmas| | GPS |
             +------------+ +----------+ +-----+
```

---

## 3. 📋 Diccionario de Datos Detallado (17 Tablas)

### Capa A: Soporte y Catálogos (9 Tablas)

#### 1. `USR_Usuarios` (Seguridad & RBAC)
- `usuarioID` (Numeric/Key, PK)
- `Nombres` (Text)
- `Apellidos` (Text)
- `Correo` (Email - Llave de autenticación `USEREMAIL()`)
- `Cargo` (Text)
- `Iniciales` (Text)
- `RolID` (Ref `ROL_Roles`)
- `SedeID` (Ref `SED_Sedes`)
- `Activo` (TRUE/FALSE)
- `Telefono` (Phone)
- `FechaIngreso` (Date)
- `UltimaSincronizacion` (DateTime)

#### 2. `ROL_Roles`
- `RolID` (Numeric, PK): 1=Administrador, 2=Supervisor, 3=Técnico, 4=Consulta.
- `Nombre` (Text)
- `Descripción` (LongText)
- `Activo` (TRUE/FALSE)

#### 3. `SED_Sedes` (Unidades Funcionales / Zonas)
- `SedeID` (Numeric, PK): CCO Sutatenza, Peaje Machetá, Peaje SLG, Báscula Machetá, Báscula SLG, UF1, UF2, UF3, UF4.
- `Nombre` (Text)
- `Ciudad` (Text)
- `Activo` (TRUE/FALSE)

#### 4. `TIP_TiposActivo`
- `TipoActivoID` (Numeric, PK): SOS, CCTV, PMVF, PMVM, SGM, SGE, SSA, GENERADOR, BASCULA, FO, VW, SWITCH, ROUTER, FIREWALL, UPS, SERVIDOR, NAS, SUBESTACIÓN.
- `Nombre` (Text)
- `Categoria` (Text: ITS, Eléctrico, TI, Comunicaciones)
- `Activo` (TRUE/FALSE)
- `TieneQR` (TRUE/FALSE)
- `RequiereGPS` (TRUE/FALSE)
- `FormularioID` (Ref `FRM_Formularios`)

#### 5. `FRM_Formularios`
- `FormularioID` (Text, PK): `FRM_SOS` a `FRM_SUBE` (18 plantillas dinámicas).
- `Nombre` (Text)
- `Descripción` (Text)
- `Orden` (Numeric)
- `Versión` (Numeric)
- `Activo` (TRUE/FALSE)

#### 6. `EST_Activo`
- `EstadoID` (Numeric, PK): 1=Operativo, 2=En mantenimiento, 3=Fuera de servicio, 4=Retirado.
- `Nombre` (Text)

#### 7. `FRE_Frecuencias`
- `FrecuenciaID` (Numeric, PK)
- `Nombre` (Text: Mensual, Trimestral, Semestral, Anual)
- `Dias` (Numeric)
- `Activo` (TRUE/FALSE)

#### 8. `CAL_Calzadas`
- `CalzadaID` (Numeric, PK)
- `Nombre` (Text: Calzada Principal, Calzada Secundaria)

#### 9. `SEN_Sentidos`
- `SentidoID` (Numeric, PK)
- `Nombre` (Text: Bogotá - Sutatenza, Sutatenza - Bogotá)

---

### Capa B: Maestras y Checklists (3 Tablas)

#### 10. `ACT_Activos` (Inventario Maestro - RF-005)
- `ActivoID` (Numeric, PK)
- `CodigoActivo` (Text)
- `Nombre` (Text)
- `TipoActivoID` (Ref `TIP_TiposActivo`)
- `SedeID` (Ref `SED_Sedes`)
- `PR` (Text - Punto de Referencia)
- `CalzadaID` (Ref `CAL_Calzadas`)
- `Latitud` (Decimal / LatLong)
- `Longitud` (Decimal / LatLong)
- `EstadoID` (Ref `EST_Activo`)
- `CodigoQR` (Text - Searchable & Scan)
- `Sentido` (Ref `SEN_Sentidos`)
- `Activo` (TRUE/FALSE)
- `FrecuenciaID` (Ref `FRE_Frecuencias`)
- `Observaciones` (LongText)

#### 11. `CHK_Checklists` & 12. `CHD_ChecklistDetalle`
- Modelo Padre-Hijo (`IsPartOf = True`) que almacena las secciones e ítems de inspección dinámicos por tipo de activo.

---

### Capa C: Transaccionales y Evidencias (5 Tablas)

#### 13. `OT_OrdenesTrabajo` (Nivel 1 Padre)
- `OTID` (Numeric, PK)
- `Número OT` (Text)
- `Activo` (Ref `ACT_Activos`)
- `Técnico` (Ref `USR_Usuarios`)
- `Fecha Programada` (Date)
- `Estado` (Enum: Pendiente, En Proceso, Cerrada, Vencida)

#### 14. `MAN_Mantenimientos` (Nivel 2 Hijo)
- `MantenimientoID` (Numeric, PK)
- `OTID` (Ref `OT_OrdenesTrabajo`)
- `ActivoID` (Ref `ACT_Activos`)
- `TécnicoID` (Ref `USR_Usuarios`)
- `Fecha` (Date)
- `Hora Inicio` (Time)
- `Hora Fin` (Time)
- `Tipo` (Enum: Preventivo, Correctivo)
- `Estado Final` (Enum: Operativo, Fuera de servicio)
- `Coordenadas_Cierre` (LatLong - Expresión `HERE()`)
- `Precision_GPS` (Decimal - Expresión `USERLOCATIONACCURACY()`)
- `Observaciones` (LongText)

#### 15. `FOT_Fotografias` (Nivel 3 Nieto)
- `FotoID` (Numeric, PK)
- `MantenimientoID` (Ref `MAN_Mantenimientos` - `IsPartOf = True`)
- `Archivo` (Image - Compresión Low 600px)
- `Fecha` (DateTime)
- `Usuario` (Ref `USR_Usuarios`)

#### 16. `FIR_Firmas` (Nivel 3 Nieto)
- `FirmaID` (Numeric, PK)
- `MantenimientoID` (Ref `MAN_Mantenimientos` - `IsPartOf = True`)
- `TipoFirma` (Enum: Técnico, Supervisor, Interventor)
- `Imagen` (Signature)

#### 17. `GPS` (Nivel 3 Nieto - Auditoría)
- `GPSID` (Numeric, PK)
- `MantenimientoID` (Ref `MAN_Mantenimientos`)
- `Latitud` (Decimal)
- `Longitud` (Decimal)
- `Precisión` (Decimal)
- `Altitud` (Decimal)
- `Proveedor` (Text)
- `FechaHora` (DateTime)

---

## 4. 🔗 Relaciones e Integridad Referencial (Foreign Keys)

| Tabla Origen | Columna FK | Tabla Destino | Regla AppSheet | Comportamiento en AppSheet |
|---|---|---|---|---|
| `USR_Usuarios` | `RolID` | `ROL_Roles` | `Ref` | Menú desplegable Enum |
| `USR_Usuarios` | `SedeID` | `SED_Sedes` | `Ref` | Menú desplegable Enum / Security Filter |
| `ACT_Activos` | `TipoActivoID` | `TIP_TiposActivo` | `Ref` | Dispara el checklist dinámico |
| `ACT_Activos` | `SedeID` | `SED_Sedes` | `Ref` | Aplica Security Filter por zona |
| `MAN_Mantenimientos` | `OTID` | `OT_OrdenesTrabajo` | `Ref` | Relación Padre-Hijo Nivel 1 a Nivel 2 |
| `FOT_Fotografias` | `MantenimientoID` | `MAN_Mantenimientos` | `Ref (IsPartOf = True)` | Múltiples fotos embebidas en formulario |
| `FIR_Firmas` | `MantenimientoID` | `MAN_Mantenimientos` | `Ref (IsPartOf = True)` | Firmas digitales manuscritas embebidas |

---
*Referencias Cruzadas:* [README.md](./README.md) | [especificaciones.md](./especificaciones.md) | [ROADMAP.md](./ROADMAP.md) | [MAP.md](./MAP.md)
