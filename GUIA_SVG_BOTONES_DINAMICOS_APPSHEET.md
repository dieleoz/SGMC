# 🎨 GUÍA TÉCNICA RESCATADA: SVG DINÁMICOS, BOTONES Y TARJETAS EN APPSHEET

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma Deployed:** Google AppSheet (`SGMC-886843353`)  
**Origen:** Auditoría y Rescate del Material de Referencia de la carpeta `legacy/` (Guías Cursos Aspiazu / Lic. Miguel Aspiazu)  
**Aplicación Práctica en SGMC:** Renderizado dinámico de estados de activos (*Operativo*, *En mantenimiento*, *Fuera de servicio*), botones dinámicos y KPIs visuales.  
**Fecha:** Agosto de 2026  

---

## 📌 1. Fundamentos de SVG Dinámicos en AppSheet

En AppSheet, es posible crear **botones dinámicos, insignias de estado (badges) e indicadores gráficos personalizados** sin necesidad de alojar imágenes externas en Google Drive o la web. 

Para lograrlo, se genera el código SVG dinámicamente desde una **App Formula** en una columna de tipo `Image` o `Show`, concatenando variables del sistema y codificándolo mediante Data URI.

---

## ⚙️ 2. Patrón de Fórmula Estándar en AppSheet

La expresión universal para renderizar cualquier SVG dinámico en AppSheet es:

```excel
"data:image/svg+xml;utf8," & ENCODEURL(
  CONCATENATE(
    "<svg width='100%' viewBox='0 0 320 200' xmlns='http://www.w3.org/2000/svg'>",
    "<rect x='0' y='0' width='320' height='200' rx='10' fill='", [ColorEstado], "'/>",
    "<text x='160' y='105' font-family='Arial' font-size='20' font-weight='bold' fill='#FFFFFF' text-anchor='middle' alignment-baseline='central'>",
      [EstadoID].[Nombre],
    "</text>",
    "</svg>"
  )
)
```

### Reglas de Oro para Evitar Fallos en AppSheet:
1. **Eliminar el Prólogo XML:** NUNCA incluir `<?xml ...?>` al inicio.
2. **Reemplazo de Comillas:** Usar comillas simples (`'`) dentro del SVG para atributos de etiquetas (ej: `fill='#FFFFFF'`) para evitar escapar comillas dobles en AppSheet.
3. **Manejo de Variables:** Insertar campos de la base de datos (ej. `[EstadoID].[Nombre]`, `[MiColor]`) como argumentos separados dentro del `CONCATENATE(...)`.
4. **Sintaxis Data URI:** La cadena DEBE comenzar obligatoriamente por `"data:image/svg+xml;utf8," & ENCODEURL(...)`.

---

## 📐 3. Guía de Dimensiones y `viewBox` Recomendados

| Elemento UI en AppSheet | `viewBox` Recomendado | Configuración de Ancho | Configuración de Alto |
|---|---|---|---|
| **Tarjeta para Vista Detail** | `viewBox="0 0 320 200"` | `width="100%"` | Ajuste automático por proporción |
| **Botón Horizontal** | `viewBox="0 0 200 50"` | `width="100%"` | Centrado con `text-anchor='middle'` |
| **Tarjeta KPI Dividida (2 Cuadros)** | `viewBox="0 0 320 200"` | `width="100%"` | Cuadro Izq: `0 -> 160`, Cuadro Der: `160 -> 320` |

---

## 🛠️ 4. Aplicación Concreta en el Sistema SGMC

### 4.1 Insignia Dinámica de Estado de Activo (`ACT_Activos`)
En la vista de **Ficha de Activo** (`ACT_Activos`), se configura una Columna Virtual de tipo `Image` para renderizar el badge de estado con colores dinámicos:

* **Color Verde (Operativo):** `#28A745`
* **Color Amarillo (En mantenimiento):** `#FFC107`
* **Color Rojo (Fuera de servicio):** `#DC3545`

#### Expresión en App Formula (`ACT_Activos[BadgeEstado]`):
```excel
"data:image/svg+xml;utf8," & ENCODEURL(
  CONCATENATE(
    "<svg width='100%' viewBox='0 0 200 50' xmlns='http://www.w3.org/2000/svg'>",
    "<rect x='0' y='0' width='200' height='50' rx='8' fill='", 
      SWITCH([EstadoID],
        1, "#28A745",
        2, "#FFC107",
        3, "#DC3545",
        "#6C757D"
      ), 
    "'/>",
    "<text x='100' y='27' font-family='Arial' font-size='16' font-weight='bold' fill='#FFFFFF' text-anchor='middle' alignment-baseline='central'>",
      [EstadoID].[Nombre],
    "</text>",
    "</svg>"
  )
)
```

---

## 🖼️ 5. Embebido HTML para Tablas / Google Sheets (Data URI <img>)

Cuando se generan reportes en PDF o vistas HTML exportadas donde no se renderizan etiquetas `<svg>` directas, se utiliza el patrón HTML Data URI:

```html
<img src="data:image/svg+xml;utf8,<svg width='200' height='50' viewBox='0 0 200 50' xmlns='http://www.w3.org/2000/svg'><rect x='0' y='0' width='200' height='50' rx='6' fill='%2328A745'/><text x='100' y='28' font-family='Arial' font-size='14' fill='%23FFFFFF' text-anchor='middle'>OPERATIVO</text></svg>" style="max-width:100%;" alt="Estado Operativo"/>
```
*(Nota: En HTML directo, el símbolo `#` de los colores hex se reemplaza por `%23` para evitar que rompa el atributo `src`).*

---
*Documento rescatado de la carpeta `legacy/` e integrado al estándar técnico del SGMC.*  
*Referencias Cruzadas:* [README.md](./README.md) | [especificaciones.md](./especificaciones.md) | [especificaciones_visuales.md](./especificaciones_visuales.md) | [MAP.md](./MAP.md)
