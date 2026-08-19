export interface DatosInformeDisponibilidad {
  anio: number;
  mes: number;
  mesNombre: string;
  disponibilidadGlobal: string;
  totalActivos: number;
  totalSubsistemas: number;
  subsistemasConformes: number;
  horasProgramadasTotal: number;
  horasIndisponiblesTotal: number;
  filas: Array<{
    codigo: string;
    subsistema: string;
    uf: string;
    activos: number;
    horasProg: number;
    horasFalla: number;
    disponibilidad: number;
    cumple: boolean;
  }>;
  parteDiario: {
    otsTotal: number;
    otsCerradas: number;
    cierresExcepcion: number;
    novedades: number;
  };
}

/**
 * Genera e imprime el Informe Oficial de Disponibilidad Contractual (Di) para Interventoría / ANI
 */
export function generarInformeDisponibilidadPDF(datos: DatosInformeDisponibilidad) {
  const printWindow = window.open("", "_blank");
  if (!printWindow) {
    alert("Por favor habilite las ventanas emergentes (popups) para descargar el informe.");
    return;
  }

  const filasHtml = datos.filas.map((f) => `
    <tr>
      <td style="font-family: monospace; font-weight: bold; color: #1e293b;">${f.codigo}</td>
      <td style="font-weight: 600;">${f.subsistema}</td>
      <td style="text-align: center;">${f.uf}</td>
      <td style="text-align: center;">${f.activos}</td>
      <td style="text-align: right; font-family: monospace;">${f.horasProg.toLocaleString()}h</td>
      <td style="text-align: right; font-family: monospace; color: ${f.horasFalla > 0 ? '#b91c1c' : '#64748b'};">${f.horasFalla.toFixed(1)}h</td>
      <td style="text-align: right; font-family: monospace; font-weight: bold; color: ${f.cumple ? '#047857' : '#b91c1c'};">${f.disponibilidad.toFixed(2)}%</td>
      <td style="text-align: center;">
        <span class="badge ${f.cumple ? 'badge-ok' : 'badge-fail'}">
          ${f.cumple ? 'CONFORME' : 'NO CONFORME'}
        </span>
      </td>
    </tr>
  `).join("");

  const html = `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe de Disponibilidad Contractual Di - ${datos.mesNombre} ${datos.anio}</title>
  <style>
    @page { size: letter; margin: 12mm; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a;
      font-size: 10px;
      line-height: 1.35;
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
      border: 1px solid #94a3b8;
      padding: 6px 10px;
    }
    .logo-title {
      font-size: 13px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .subtitle {
      font-size: 9.5px;
      color: #475569;
      font-weight: 600;
    }
    .badge {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: bold;
      font-size: 8.5px;
      text-transform: uppercase;
    }
    .badge-ok {
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
    }
    .badge-fail {
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fecaca;
    }
    .section-title {
      background: #0f172a;
      color: #ffffff;
      padding: 4px 8px;
      font-size: 10.5px;
      font-weight: bold;
      margin-top: 10px;
      margin-bottom: 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .formula-box {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-left: 4px solid #047857;
      padding: 8px 12px;
      border-radius: 4px;
      margin-bottom: 10px;
      font-size: 9.5px;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-bottom: 10px;
    }
    .kpi-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 6px 8px;
      text-align: center;
    }
    .kpi-label {
      font-size: 8.5px;
      color: #64748b;
      font-weight: 600;
      text-transform: uppercase;
    }
    .kpi-val {
      font-size: 16px;
      font-weight: 800;
      color: #0f172a;
      margin-top: 2px;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 12px;
    }
    .data-table th {
      background: #1e293b;
      color: #ffffff;
      padding: 5px 6px;
      font-size: 9px;
      text-transform: uppercase;
      border: 1px solid #334155;
    }
    .data-table td {
      border: 1px solid #e2e8f0;
      padding: 4px 6px;
      font-size: 9px;
    }
    .data-table tr:nth-child(even) {
      background: #f8fafc;
    }
    .signatures-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
      page-break-inside: avoid;
    }
    .signatures-table td {
      width: 50%;
      padding: 10px 15px;
      vertical-align: top;
      border: 1px solid #cbd5e1;
    }
    .sign-line {
      border-bottom: 1px solid #0f172a;
      margin-top: 40px;
      margin-bottom: 6px;
    }
    .footer-note {
      font-size: 8px;
      color: #94a3b8;
      text-align: center;
      margin-top: 15px;
      border-top: 1px solid #e2e8f0;
      padding-top: 6px;
    }
  </style>
</head>
<body>

  <!-- Encabezado Oficial -->
  <table class="header-table">
    <tr>
      <td style="width: 25%; text-align: center; background: #f8fafc;">
        <div style="font-weight: 900; font-size: 14px; color: #047857;">SISGA</div>
        <div style="font-size: 7.5px; color: #64748b;">CONCESIÓN VIAL</div>
      </td>
      <td style="width: 50%; text-align: center;">
        <div class="logo-title">INFORME DE DISPONIBILIDAD CONTRACTUAL ($D_i$)</div>
        <div class="subtitle">CONTRATO DE CONCESIÓN BAJO ESQUEMA APP — CORREDOR VIAL DEL SISGA (137 KM)</div>
        <div style="font-size: 9px; font-weight: bold; color: #047857; margin-top: 3px;">
          PERÍODO EVALUADO: ${datos.mesNombre.toUpperCase()} ${datos.anio}
        </div>
      </td>
      <td style="width: 25%; font-size: 8.5px;">
        <div><strong>Doc:</strong> INF-DISP-${datos.anio}${String(datos.mes).padStart(2, '0')}</div>
        <div><strong>Versión:</strong> 2.0 (PostGIS)</div>
        <div><strong>Emisión:</strong> ${new Date().toLocaleDateString('es-CO')}</div>
        <div><strong>Meta ANI:</strong> $\ge 98.5\%$</div>
      </td>
    </tr>
  </table>

  <!-- Marco Teórico y Fórmula Contractual -->
  <div class="formula-box">
    <strong>Fórmula de Evaluación Contractual (Apéndice Técnico 1 - ANI):</strong><br/>
    El indicador de Disponibilidad Contractual ($D_i$) mide el porcentaje de tiempo en que la infraestructura ITS, eléctrica y de comunicaciones opera en condiciones nominales:
    <div style="text-align: center; margin: 4px 0; font-weight: bold; font-family: monospace; font-size: 11px;">
      D_i = [ 1 - ( Horas Indisponibles Totales / Horas Programadas Totales ) ] × 100%
    </div>
    Donde: <em>Horas Programadas</em> = $N \text{ activos} \times 720 \text{ h/mes}$. <em>Horas Indisponibles</em> = Tiempo acumulado de fallas no programadas registradas en el CCO.
  </div>

  <!-- Tarjetas KPI -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Disponibilidad Global</div>
      <div class="kpi-val" style="color: #047857;">${datos.disponibilidadGlobal}%</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total Activos en Censo</div>
      <div class="kpi-val">${datos.totalActivos}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Horas Indisponibles</div>
      <div class="kpi-val" style="color: ${datos.horasIndisponiblesTotal > 0 ? '#b91c1c' : '#0f172a'};">${datos.horasIndisponiblesTotal.toFixed(1)} h</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Conformidad Contractual</div>
      <div class="kpi-val" style="color: #047857; font-size: 13px;">${datos.subsistemasConformes}/${datos.totalSubsistemas} Subsistemas</div>
    </div>
  </div>

  <!-- Tabla de Detalle por Subsistema -->
  <div class="section-title">1. Matriz de Cumplimiento por Subsistema y Unidad Funcional</div>
  <table class="data-table">
    <thead>
      <tr>
        <th>Código</th>
        <th>Subsistema</th>
        <th style="text-align: center;">Zona</th>
        <th style="text-align: center;">Activos</th>
        <th style="text-align: right;">Horas Prog.</th>
        <th style="text-align: right;">Horas Falla</th>
        <th style="text-align: right;">Disponibilidad ($D_i$)</th>
        <th style="text-align: center;">Estado ANI</th>
      </tr>
    </thead>
    <tbody>
      ${filasHtml}
    </tbody>
  </table>

  <!-- Resumen Parte Diario CCO -->
  <div class="section-title">2. Resumen Operativo de Campo y Centro de Control (CCO)</div>
  <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
    <tr>
      <td style="border: 1px solid #cbd5e1; padding: 6px 10px; width: 25%; background: #f8fafc;">
        <strong>Órdenes Programadas:</strong> ${datos.parteDiario.otsTotal}
      </td>
      <td style="border: 1px solid #cbd5e1; padding: 6px 10px; width: 25%; background: #f8fafc;">
        <strong>Mantenimientos Ejecutados:</strong> ${datos.parteDiario.otsCerradas}
      </td>
      <td style="border: 1px solid #cbd5e1; padding: 6px 10px; width: 25%; background: #f8fafc;">
        <strong>Cierres con Excepción GPS:</strong> ${datos.parteDiario.cierresExcepcion} (Justificados)
      </td>
      <td style="border: 1px solid #cbd5e1; padding: 6px 10px; width: 25%; background: #f8fafc;">
        <strong>Novedades de Ruta:</strong> ${datos.parteDiario.novedades}
      </td>
    </tr>
  </table>

  <!-- Firmas de Certificación -->
  <div class="section-title">3. Certificación de Interventoría y Concesión</div>
  <table class="signatures-table">
    <tr>
      <td>
        <div style="font-weight: bold; color: #0f172a; margin-bottom: 2px;">POR LA CONCESIÓN TRANSVERSAL DEL SISGA:</div>
        <div style="font-size: 8.5px; color: #64748b;">Director Técnico / Ingeniero de Mantenimiento ITS</div>
        <div class="sign-line"></div>
        <div style="font-weight: bold;">Ing. Diego Zúñiga / Coordinador ITS</div>
        <div style="font-size: 8px; color: #64748b;">Concesión Transversal del Sisga S.A.S.</div>
      </td>
      <td>
        <div style="font-weight: bold; color: #0f172a; margin-bottom: 2px;">POR LA INTERVENTORÍA:</div>
        <div style="font-size: 8.5px; color: #64748b;">Ingeniero Especialista ITS / Auditor Contractual</div>
        <div class="sign-line"></div>
        <div style="font-weight: bold;">Ingeniero Residente de Interventoría</div>
        <div style="font-size: 8px; color: #64748b;">Consorcio Interventoría Sisga</div>
      </td>
    </tr>
  </table>

  <div class="footer-note">
    Documento emitido electrónicamente por SGMC v2 — Transversal del Sisga S.A.S. • Registro inmutable en PostgreSQL 16 / PostGIS • Válido para radicación oficial ante la Agencia Nacional de Infraestructura (ANI).
  </div>

  <script>
    window.onload = function() {
      setTimeout(function() {
        window.print();
      }, 500);
    };
  </script>
</body>
</html>
  `;

  printWindow.document.open();
  printWindow.document.write(html);
  printWindow.document.close();
}
