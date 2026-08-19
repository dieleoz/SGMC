# Plan de Pruebas Periciales y Protocolo de Carga de Datos Técnicos — SGMC v2

**Sistema de Gestión de Mantenimiento en Campo**  
**Cliente:** Concesión Transversal del Sisga S.A.S. (137 km)  
**Versión:** 2.0 (PostgreSQL 16 + PostGIS + Next.js 14 PWA)  
**Documento:** PLAN-PRUEBAS-FICHAS-V2  
**Fecha:** Agosto 2026

---

## 1. Objetivo del Plan de Pruebas

Establecer el protocolo técnico y pericial para la verificación exhaustiva, validación de tolerancias instrumentales y carga controlada de datos de prueba sobre las **27 fichas de inspección técnica** asociadas a los **368 activos** de la Concesión Transversal del Sisga.

El protocolo asegura que cada formulario capture con precisión física y matemática los parámetros exigidos en el **Apéndice Técnico 1 de la ANI** (voltajes, frecuencias, potencias, atenuaciones ópticas, presiones y estados operativos).

---

## 2. Matriz de Parámetros Instrumentales por Subsistema (27 Fichas)

| Código Ficha | Subsistema / Equipo | Parámetros Clave a Medir / Validar | Rango Nominal / Tolerancia | Criterio de Aceptación Interventoría |
|:---:|---|---|:---:|---|
| **`FRM-SOS`** | **Postes SOS (Poste Auxilio)** | • Tensión batería DC<br>• Tensión panel solar circuito abierto<br>• Audio Full-Duplex CCO<br>• Hermeticidad gabinete | 12.0 V – 14.5 V DC<br>18.0 V – 22.0 V DC<br>Claridad de voz >95%<br>Grado IP66 | Conforme si batería $\ge 12.4\text{ V}$ y comunicación nítida con el CCO. |
| **`FRM-CCTV`** | **Cámaras de Circuito Cerrado** | • Tensión PoE+ (Inyector)<br>• Tasa de cuadros (FPS)<br>• Movimiento PTZ 360°<br>• Iluminador infrarrojo | 48.0 V – 54.0 V DC<br>$\ge 25\text{ FPS}$ (1080p)<br>Preset <1.5s<br>Alcance $\ge 150\text{ m}$ | Flujo de video RTSP continuo al CCO sin pérdidas de paquetes. |
| **`FRM-PMVF`** | **Panel Mensaje Variable Fijo** | • Alimentación principal AC<br>• Voltaje banco DC<br>• Conmutación píxeles LED<br>• Comunicación protocolo NTCIP | 110 V – 220 V AC<br>24.0 V / 48.0 V DC<br>100% LED activos<br>Respuesta <500 ms | Mensaje visualizable a 250 m con brillo adaptativo por fotocelda. |
| **`FRM-PMVM`** | **Panel Mensaje Variable Móvil** | • Carga remolque / batería<br>• Sistema de elevación hidráulica<br>• Enlace 4G/LTE con CCO | 12.0 V – 24.0 V DC<br>Presión normal<br>Latencia <200 ms | Elevación y orientación conforme en bermas autorizadas. |
| **`FRM-GENE`** | **Grupos Electrógenos / Plantas** | • Nivel diésel en tanque<br>• Tensión batería arranque<br>• Frecuencia de salida<br>• Tensión trifásica generada<br>• Tiempo conmutación ATS | $\ge 75\%$ capacidad<br>24.0 V – 27.5 V DC<br>60.0 Hz $\pm 0.5\text{ Hz}$<br>208 V / 220 V AC<br>$< 10\text{ segundos}$ | Transferencia automática inmediata ante corte de red eléctrica. |
| **`FRM-UPS`** | **Sistemas de Potencia Ininterrumpida** | • Tensión por celda de batería<br>• Tensión banco total<br>• Autonomía en descarga<br>• Temperatura de operación | 2.25 V – 2.30 V / celda<br>120 V / 240 V DC<br>$\ge 120\text{ minutos}$<br>20°C – 25°C | Sin caída de tensión en transición a modo inversor/batería. |
| **`FRM-SUBE`** | **Subestaciones Eléctricas** | • Nivel de aislamiento (MΩ)<br>• Puesta a tierra (Telurómetro)<br>• Nivel de aceite transformador | $\ge 1000\text{ M}\Omega$<br>$\le 5.0\ \Omega$<br>Nivel y rigidez dieléc. | Resistencia a tierra certificada y termografía sin puntos calientes. |
| **`FRM-FO`** | **Fibra Óptica (Tendido 137 km)** | • Atenuación por kilómetro<br>• Pérdida por empalme fusión<br>• Reflectancia conectores (OTDR) | $\le 0.25\text{ dB/km}$ (1550nm)<br>$\le 0.05\text{ dB}$ / fusión<br>$\le -50\text{ dB}$ | Margen óptico total conforme para anillo redundante ERPS. |
| **`FRM-SWIT`** | **Switches Industriales de Campo** | • Enlace óptico SFP (dBm)<br>• Tasa de error de tramas<br>• Temperatura chasis | $-15\text{ a }-8\text{ dBm}$<br>0 errores CRC<br>$-20\text{°C a }+70\text{°C}$ | Tiempo de convergencia de anillo ITU-T G.8032 $<50\text{ ms}$. |
| **`FRM-SWL3`** | **Switches Core Capa 3 (CCO)** | • Uso de CPU / Memoria<br>• Rutas BGP / OSPF activas<br>• Fuentes de poder redundantes | CPU $<35\%$<br>100% adyacencias<br>Dual AC activa | Cero interrupción en enrutamiento de datos del corredor. |
| **`FRM-ROUT`** | **Enrutadores de Borde / CCO** | • Túneles VPN IPsec<br>• Throughput de tráfico<br>• Firewall / Seguridad | Cifrado AES-256<br>$\ge 1\text{ Gbps}$<br>0 accesos no autorizados | Telemetría segura hacia Centro de Control Sisga y ANI. |
| **`FRM-SERV`** | **Servidores de Aplicación CCO** | • Estado arreglos RAID disco<br>• Uso de almacenamiento<br>• Servicios SGMC / Base datos | RAID 10 Conforme<br>$<70\%$ ocupación<br>Uptime $\ge 99.9\%$ | Integridad de respaldos y réplica sincrónica en PostgreSQL. |
| **`FRM-NAS`** | **Sistemas de Almacenamiento NAS** | • Días de retención de video<br>• Espacio disponible video CCTV<br>• Estado de discos SAS/SATA | $\ge 30\text{ días}$ (1080p)<br>$\ge 20\text{ TB}$ libres<br>SMART OK | Almacenamiento continuo de 30 días según pliego contractual. |
| **`FRM-VW`** | **Video Wall / Pantallas CCO** | • Calibración cromática<br>• Controladora matricial<br>• Tiempo de conmutación | Sin píxeles muertos<br>Matriz 4x2 activa<br>$<1\text{ segundo}$ | Despliegue simultáneo de cámaras, mapas y alarmas viales. |
| **`FRM-ETD`** | **Estación Toma de Datos (Tráfico)** | • Conteo volumétrico vehicular<br>• Clasificación por ejes (C1..C5)<br>• Sensor piezocable / lazo | Precisión $\ge 98\%$<br>Error $<2\%$<br>Inductancia OK | Calibración anual cotejada con aforo manual de interventoría. |
| **`FRM-BASC`** | **Básculas de Pesaje Estático** | • Error de pesaje bruto<br>• Celdas de carga (mV/V)<br>• Plataforma estructural | $\pm 0.5\%$ error máx.<br>Simetría 4 celdas<br>Sin corrosión | Certificado de calibración de pesas patrón vigente (SIC). |
| **`FRM-BASD`** | **Báscula de Pesaje Dinámico WIM** | • Sensor piezoeléctrico cuarzo<br>• Error de peso por eje (WIM)<br>• Detección sobrepeso CCO | Error $<5\%$ a 60 km/h<br>Lectura continua<br>Transmisión <1s | Alerta automática en tiempo real al peaje y patrulla vial. |
| **`FRM-OCR`** | **Cámaras OCR Reconocimiento Placas** | • Tasa de lectura correcta<br>• Iluminador infrarrojo pulso<br>• Integración RUNT / Sisga | $\ge 96\%$ placas limpias<br>Sincronía obturador<br>Respuesta <800 ms | Identificación vehicular y vinculación a registro de pesaje. |
| **`FRM-PJC`** | **Peaje: Equipos de Carril** | • Barrera electromecánica<br>• Semáforo de carril (Rojo/Verde)<br>• Sensor de altura / perfilador | Apertura $<1.2\text{ s}$<br>LEDs 100% operativos<br>Detección precisa | Cero atascamiento de carril por fallas de automatización. |
| **`FRM-PJE`** | **Peaje: Sistema Telepeaje / TAG** | • Antena RFID 915 MHz (Tag)<br>• Protocolo Colpass / ANI<br>• Tasa de lectura de Tag | Potencia nominal<br>Interoperable 100%<br>$\ge 99.5\%$ lectura | Cobro electrónico sin detención conforme a normativa nacional. |
| **`FRM-PSEG`** | **Paso Seguro Peatonal / Túnel** | • Pulsador peatonal<br>• Balizas luminosas destello<br>• Sonorizador para invidentes | Contacto seco NC/NA<br>$\ge 60\text{ destellos/min}$<br>85 dB a 1 metro | Activación inmediata de advertencia para usuarios de vía. |
| **`FRM-SGE`** | **Sistema de Gestión Energía Peaje** | • Factor de potencia (FP)<br>• Banco de condensadores<br>• Supresor de transitorios (DPS) | $\text{FP} \ge 0.95$<br>Automático por pasos<br>Varistores intactos | Cero penalización por energía reactiva ante operador de red. |
| **`FRM-SGM`** | **Sistema Gestión Medioambiental** | • Sensor de visibilidad (Niebla)<br>• Pluviómetro de precipitación<br>• Velocidad de viento | 0 – 2000 metros<br>Resolución 0.2 mm<br>0 – 150 km/h | Alertas meteorológicas tempranas en PMV ante lluvia/niebla. |
| **`FRM-SSA`** | **Sistema de Señalización Acústica** | • Sirenas de túnel / evacuación<br>• Megafonía pública (PA)<br>• Nivel de presión sonora | 110 dB a 3 metros<br>Inteligibilidad STI >0.6<br>Amplificadores Clase D | Mensajes audibles de evacuación en túneles del Sisga. |
| **`FRM-FIRE`** | **Sistema Detección y Extinción Fuego** | • Cable sensor térmico lineal<br>• Pulsadores de emergencia<br>• Gabinetes de mangueras (BIE) | Umbral $68\text{°C} / 88\text{°C}$<br>Lazo direccionable<br>Presión $\ge 6\text{ bar}$ | Prueba semestral de flujo y activación de extractor de humos. |
| **`FRM-PORT`** | **Computadores Portátiles Técnicos** | • Batería de diagnóstico<br>• Software de mantenimiento<br>• Certificados SSL / VPN | $\ge 4\text{ horas}$<br>Herramientas ITS<br>Vigentes | Terminal de configuración pericial en campo. |
| **`FRM-IMPR`** | **Impresoras Térmicas de Peaje** | • Cabezal térmico de corte<br>• Velocidad de impresión<br>• Sensor fin de papel | Corte limpio $<0.5\text{ s}$<br>$\ge 200\text{ mm/s}$<br>Aviso preventivo | Emisión de tiquetes de peaje sin demoras en cabina. |

---

## 3. Protocolo de Ejecución de Pruebas de Campo

### 3.1. Fase 1: Calibración Instrumental Previa
* **Multímetro Digital:** Calibrado con certificado vigente (medición de VDC, VAC, frecuencia y resistencia).
* **Telurómetro:** Calibrado para medición de puesta a tierra con picas a 5m y 10m ($\le 5\ \Omega$).
* **OTDR y Medidor de Potencia Óptica:** Limpieza de conectores FC/APC con casete de alcohol isopropílico.
* **Cámara Termográfica:** Rango -20°C a +350°C para detección de sobrecalentamiento en bornes y breakers.

### 3.2. Fase 2: Ejecución Offline y Georreferenciada en PWA
1. El técnico arriba al punto kilométrico del activo en su vehículo de cuadrilla.
2. Abre la PWA [`sisga-2.vercel.app/tecnico`](https://sisga-2.vercel.app/tecnico).
3. Captura el GPS satelital. El sistema calcula la distancia euclidiana en PostGIS contra el PK oficial.
4. Diligencia las mediciones numéricas exactas en el checklist (ej. *Tensión batería SOS: 12.8V*, *Puesta a tierra: 2.3 Ohm*).
5. Toma 2 fotos WebP georreferenciadas (*Gabinete cerrado con estampa GPS*, *Medición en multímetro*).
6. Firma digitalmente en el canvas táctil y presiona **"Guardar y Cerrar Mantenimiento"**.

### 3.3. Fase 3: Auditoría y Certificación Pericial
1. El supervisor ingresa a [`sisga-2.vercel.app/supervisor`](https://sisga-2.vercel.app/supervisor).
2. Valida que el geofencing esté en verde (distancia dentro de tolerancia) y que las mediciones se encuentren dentro del rango técnico nominal.
3. Aprueba la orden de trabajo.
4. Descarga la **Ficha Técnica Pericial en PDF** para el expediente de interventoría.

---

## 4. Procedimiento de Carga Masiva de Datos de Prueba

Para poblar y auditar en lote las 27 fichas de prueba con mediciones periciales exactas y evidencia fotográfica, se ejecuta el script automatizado:

```cmd
python scripts/cargar_datos_pruebas_fichas.py
```

### Resultados de la Carga de Prueba:
* **27 Mantenimientos Ejecutados:** Uno por cada tipo de activo y ficha técnica.
* **Checklists Detallados:** 333 respuestas numéricas y cualitativas asentadas en `CHD_ChecklistDetalle`.
* **Fotografías y Firmas:** 54 fotos WebP con georreferenciación y 27 firmas digitales registradas en `FOT_Fotografias` y `FIR_Firmas`.
* **Disponibilidad Contractual:** Actualización automática del indicador $D_i$ en `/reportes`.

---

## 5. Criterios de Aceptación y Certificación Final

| Criterio | Descripción | Umbral Requerido | Resultado Obtenido |
|---|---|:---:|:---:|
| **Completitud de Fichas** | Cobertura de los 27 tipos de equipos del corredor. | 27 de 27 Fichas | 🟢 **100% CUBIERTO** |
| **Integridad de Preguntas** | Registro de 333 ítems técnicos con unidades y rangos. | 333 Preguntas | 🟢 **100% CONFORME** |
| **Aislamiento de Coordenadas** | Cero coordenadas inventadas en cierres con excepción. | 0 Falsos GPS | 🟢 **FAIL-CLOSED ACTIVO** |
| **Disponibilidad Contractual** | Cálculo mensual de $D_i$ contra meta ANI. | $\ge 98.5\%$ | 🟢 **100.00% CONFORME** |

---

## 6. Bloque de Firmas y Homologación

```text
POR LA CONCESIÓN TRANSVERSAL DEL SISGA S.A.S.:


_________________________________________________________
Ing. Diego Zúñiga
Coordinador ITS / Director Técnico SGMC
Concesión Transversal del Sisga S.A.S.


POR EL CONSORCIO DE INTERVENTORÍA:


_________________________________________________________
Ingeniero Especialista ITS / Auditor Contractual
Consorcio Interventoría Sisga
Agencia Nacional de Infraestructura (ANI)
```
