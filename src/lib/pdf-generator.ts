export interface DatosFichaMantenimiento {
  otid: string;
  activo: string;
  tipo: string;
  uf: string;
  pk: string;
  tecnico: string;
  supervisor: string;
  fecha: string;
  estado: string;
  coordenadasActivo: string;
  coordenadasCierre: string;
  distanciaMetros: number;
  geofenceValido: boolean;
  observaciones: string;
  checklist: Record<string, string>;
  fotos: Array<{ id: string; url: string; descripcion: string; timestamp: string }>;
  firmaTecnicoUrl?: string;
}

/**
 * Genera e imprime la Ficha Técnica Pericial de Mantenimiento en formato PDF
 */
export function generarFichaPDF(datos: DatosFichaMantenimiento) {
  const printWindow = window.open("", "_blank");
  if (!printWindow) {
    alert("Por favor habilite las ventanas emergentes (popups) para descargar la Ficha PDF.");
    return;
  }

  const html = `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Ficha Técnica Pericial - ${datos.otid}</title>
  <style>
    @page { size: letter; margin: 15mm; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      font-size: 11px;
      line-height: 1.4;
      margin: 0;
      padding: 0;
    }
    .header-table {
      width: 100%;
      border-collapse: collapse;
      border: 2px solid #0f172a;
      margin-bottom: 12px;
    }
    .header-table td {
      border: 1px solid #cbd5e1;
      padding: 6px 10px;
    }
    .logo-title {
      font-size: 14px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .subtitle {
      font-size: 10px;
      color: #64748b;
      font-weight: 600;
    }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: bold;
      font-size: 10px;
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
    }
    .section-title {
      background: #0f172a;
      color: #ffffff;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: bold;
      margin-top: 10px;
      margin-bottom: 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .info-grid {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
    }
    .info-grid td {
      border: 1px solid #e2e8f0;
      padding: 5px 8px;
      font-size: 10.5px;
    }
    .info-label {
      background: #f8fafc;
      font-weight: bold;
      color: #475569;
      width: 25%;
    }
    .checklist-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
    }
    .checklist-table th, .checklist-table td {
      border: 1px solid #cbd5e1;
      padding: 4px 8px;
      font-size: 10px;
    }
    .checklist-table th {
      background: #f1f5f9;
      text-align: left;
      color: #334155;
    }
    .photos-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-bottom: 10px;
    }
    .photo-card {
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 4px;
      text-align: center;
      background: #f8fafc;
    }
    .photo-card img {
      width: 100%;
      height: 140px;
      object-fit: cover;
      border-radius: 2px;
    }
    .photo-meta {
      font-size: 9px;
      color: #64748b;
      margin-top: 3px;
    }
    .signatures-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    .signatures-table td {
      width: 50%;
      border: 1px solid #cbd5e1;
      padding: 10px;
      text-align: center;
      vertical-align: bottom;
    }
    .signature-img {
      max-height: 50px;
      margin-bottom: 5px;
    }
    .signature-line {
      border-top: 1px solid #0f172a;
      margin: 5px auto 3px auto;
      width: 80%;
    }
    .signature-name {
      font-weight: bold;
      font-size: 10px;
    }
    .signature-role {
      font-size: 9px;
      color: #64748b;
    }
    .footer {
      margin-top: 15px;
      text-align: center;
      font-size: 9px;
      color: #94a3b8;
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
    }
  </style>
</head>
<body>
  <!-- Encabezado Membretado Oficial -->
  <table class="header-table">
    <tr>
      <td style="width: 20%; text-align: center;">
        <span style="font-size: 18px; font-weight: 900; color: #047857;">SISGA</span>
      </td>
      <td style="width: 55%; text-align: center;">
        <div class="logo-title">Concesión Transversal del Sisga S.A.S.</div>
        <div class="subtitle">Sistema de Gestión de Mantenimiento en Campo (SGMC v2)</div>
        <div style="font-size: 10px; font-weight: bold; margin-top: 2px; color: #0f172a;">
          FICHA TÉCNICA DE MANTENIMIENTO Y CERTIFICACIÓN PERICIAL
        </div>
      </td>
      <td style="width: 25%; text-align: right;">
        <div style="font-weight: bold; font-size: 11px;">OT: ${datos.otid}</div>
        <div style="margin-top: 3px;"><span class="badge">ESTADO: ${datos.estado.toUpperCase()}</span></div>
        <div style="font-size: 9px; color: #64748b; margin-top: 3px;">Fecha: ${datos.fecha}</div>
      </td>
    </tr>
  </table>

  <!-- 1. Datos del Activo y Ubicación -->
  <div class="section-title">1. Identificación del Activo e Infraestructura</div>
  <table class="info-grid">
    <tr>
      <td class="info-label">Nombre del Activo:</td>
      <td><strong>${datos.activo}</strong></td>
      <td class="info-label">Tipo de Activo:</td>
      <td>${datos.tipo}</td>
    </tr>
    <tr>
      <td class="info-label">Unidad Funcional:</td>
      <td><strong>${datos.uf}</strong></td>
      <td class="info-label">Progresiva (PK):</td>
      <td>PK ${datos.pk}</td>
    </tr>
  </table>

  <!-- 2. Validación Satelital de Presencia -->
  <div class="section-title">2. Validación Espacial Satelital (PostGIS Geofencing)</div>
  <table class="info-grid">
    <tr>
      <td class="info-label">Coordenadas Objetivo (Censo):</td>
      <td>${datos.coordenadasActivo || "Sin registrar en censo"}</td>
      <td class="info-label">Coordenadas Cierre en Sitio:</td>
      <td>${datos.coordenadasCierre || "No disponible (Cierre con Excepción)"}</td>
    </tr>
    <tr>
      <td class="info-label">Distancia Medida:</td>
      <td><strong>${datos.distanciaMetros} metros</strong></td>
      <td class="info-label">Resultado Certificación GPS:</td>
      <td>
        <span style="color: ${datos.geofenceValido ? '#047857' : '#b91c1c'}; font-weight: bold;">
          ${datos.geofenceValido ? "✓ CONFORME (Dentro del radio permitido)" : "⚠️ CIERRE CON EXCEPCIÓN JUSTIFICADA"}
        </span>
      </td>
    </tr>
  </table>

  <!-- 3. Checklist de Inspección -->
  <div class="section-title">3. Resultados del Checklist de Inspección</div>
  <table class="checklist-table">
    <thead>
      <tr>
        <th style="width: 75%;">Ítem de Inspección Técnica</th>
        <th style="width: 25%; text-align: center;">Resultado</th>
      </tr>
    </thead>
    <tbody>
      ${
        Object.entries(datos.checklist).length > 0
          ? Object.entries(datos.checklist)
              .map(
                ([k, v]) => `
          <tr>
            <td>${k}</td>
            <td style="text-align: center; font-weight: bold; color: #047857;">${v}</td>
          </tr>`
              )
              .join("")
          : `<tr><td colspan="2" style="text-align: center; color: #94a3b8;">Sin preguntas de checklist asociadas</td></tr>`
      }
    </tbody>
  </table>

  <!-- 4. Registro Fotográfico de Evidencias -->
  <div class="section-title">4. Evidencias Fotográficas Digitales (Storage S3)</div>
  <div class="photos-grid">
    ${
      datos.fotos.length > 0
        ? datos.fotos
            .map(
              (f) => `
        <div class="photo-card">
          <img src="${f.url}" alt="${f.descripcion}" />
          <div class="photo-meta">
            <strong>${f.descripcion}</strong><br/>
            <span>Estampa: ${f.timestamp}</span>
          </div>
        </div>`
            )
            .join("")
        : `<div style="grid-column: span 2; text-align: center; padding: 15px; color: #94a3b8;">No se registraron evidencias fotográficas</div>`
    }
  </div>

  <!-- 5. Observaciones Técnicas -->
  <div class="section-title">5. Observaciones Técnicas y Trabajo Ejecutado</div>
  <div style="border: 1px solid #cbd5e1; padding: 8px; font-size: 10.5px; background: #f8fafc; border-radius: 4px; margin-bottom: 10px;">
    ${datos.observaciones || "Sin observaciones adicionales registradas."}
  </div>

  <!-- 6. Firmas y Certificación Pericial -->
  <table class="signatures-table">
    <tr>
      <td>
        ${
          datos.firmaTecnicoUrl
            ? `<img src="${datos.firmaTecnicoUrl}" class="signature-img" alt="Firma Técnico" />`
            : `<div style="height: 40px;"></div>`
        }
        <div class="signature-line"></div>
        <div class="signature-name">${datos.tecnico}</div>
        <div class="signature-role">Técnico de Mantenimiento en Campo</div>
      </td>
      <td>
        <div style="height: 25px; font-weight: bold; color: #047857; font-size: 11px;">
          ✓ APROBADO & CERTIFICADO
        </div>
        <div class="signature-line"></div>
        <div class="signature-name">${datos.supervisor}</div>
        <div class="signature-role">Supervisor de Infraestructura & ITS (Sisga)</div>
      </td>
    </tr>
  </table>

  <div class="footer">
    Documento emitido electrónicamente por el SGMC v2 • Concesión Transversal del Sisga S.A.S. • Código de Verificación SHA-256
  </div>

  <script>
    window.onload = function() {
      window.print();
    };
  </script>
</body>
</html>
  `;

  printWindow.document.open();
  printWindow.document.write(html);
  printWindow.document.close();
}
