"use client";

import { useState, useEffect } from "react";
import { 
  BarChart3, 
  ShieldCheck, 
  Calendar, 
  CheckCircle2, 
  AlertTriangle, 
  Download, 
  RefreshCw, 
  Activity, 
  Clock, 
  TrendingUp, 
  HardHat, 
  Layers,
  FileText,
  HelpCircle
} from "lucide-react";
import { supabase } from "@/lib/supabase";
import { generarInformeDisponibilidadPDF } from "@/lib/pdf-reporte-disponibilidad";

interface DisponibilidadRow {
  TipoActivoID: string;
  TipoActivoNombre: string;
  UnidadFuncionalID: string;
  TotalActivos: number;
  HorasProgramadas: number;
  HorasIndisponibles: number;
  DisponibilidadPorcentaje: number;
  CumpleMeta: boolean;
}

export default function ReportesPage() {
  const [loading, setLoading] = useState(true);
  const [anio, setAnio] = useState(2026);
  const [mes, setMes] = useState(8); // Agosto
  const [disponibilidad, setDisponibilidad] = useState<DisponibilidadRow[]>([]);
  const [mostrarFormula, setMostrarFormula] = useState(true);
  
  // Resumen Parte Diario CCO
  const [parteDiario, setParteDiario] = useState({
    otsTotal: 0,
    otsCerradas: 0,
    cierresConExcepcion: 0,
    tecnicosActivos: 5,
    novedadesReportadas: 0,
  });

  const mesesNombres = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];

  const cargarDatosReporte = async () => {
    setLoading(true);
    try {
      // 1. Cargar Disponibilidad Contractual desde RPC
      const { data: dispData, error: dispErr } = await supabase.rpc("sgmc_calcular_disponibilidad", {
        p_anio: anio,
        p_mes: mes,
      });

      if (!dispErr && dispData) {
        setDisponibilidad(dispData);
      }

      // 2. Cargar Métricas de Parte Diario
      const { count: countOTs } = await supabase.from("OT_OrdenesTrabajo").select("*", { count: "exact", head: true });
      const { count: countCerradas } = await supabase.from("MAN_Mantenimientos").select("*", { count: "exact", head: true });
      const { count: countExcepciones } = await supabase.from("MAN_Mantenimientos").select("*", { count: "exact", head: true }).eq("CierreConExcepcion", true);
      const { count: countNov } = await supabase.from("NOV_Novedades").select("*", { count: "exact", head: true });

      setParteDiario({
        otsTotal: countOTs || 0,
        otsCerradas: countCerradas || 0,
        cierresConExcepcion: countExcepciones || 0,
        tecnicosActivos: 5,
        novedadesReportadas: countNov || 0,
      });
    } catch (e) {
      console.warn("Error cargando reporte:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarDatosReporte();
  }, [anio, mes]);

  // Cálculos consolidados
  const promedioGeneral = disponibilidad.length > 0
    ? (disponibilidad.reduce((acc, curr) => acc + curr.DisponibilidadPorcentaje, 0) / disponibilidad.length).toFixed(2)
    : "100.00";

  const totalCumplen = disponibilidad.filter((d) => d.CumpleMeta).length;
  const horasProgTotal = disponibilidad.reduce((acc, curr) => acc + curr.HorasProgramadas, 0);
  const horasFallaTotal = disponibilidad.reduce((acc, curr) => acc + curr.HorasIndisponibles, 0);

  const handleDescargarPDF = () => {
    generarInformeDisponibilidadPDF({
      anio,
      mes,
      mesNombre: mesesNombres[mes] || "Agosto",
      disponibilidadGlobal: promedioGeneral,
      totalActivos: 368,
      totalSubsistemas: disponibilidad.length,
      subsistemasConformes: totalCumplen,
      horasProgramadasTotal: horasProgTotal,
      horasIndisponiblesTotal: horasFallaTotal,
      filas: disponibilidad.map((d) => ({
        codigo: d.TipoActivoID,
        subsistema: d.TipoActivoNombre,
        uf: d.UnidadFuncionalID,
        activos: d.TotalActivos,
        horasProg: d.HorasProgramadas,
        horasFalla: d.HorasIndisponibles,
        disponibilidad: d.DisponibilidadPorcentaje,
        cumple: d.CumpleMeta,
      })),
      parteDiario: {
        otsTotal: parteDiario.otsTotal,
        otsCerradas: parteDiario.otsCerradas,
        cierresExcepcion: parteDiario.cierresConExcepcion,
        novedades: parteDiario.novedadesReportadas,
      },
    });
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Cabecera Principal */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20 mb-2">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Indicadores Contractuales & Auditoría ANI (ESPEC-021)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Disponibilidad Contractual ($D_i$)</h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Tablero oficial de cumplimiento para la Concesión Transversal del Sisga e Interventoría.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select
            value={mes}
            onChange={(e) => setMes(parseInt(e.target.value))}
            className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white font-semibold focus:outline-none focus:border-emerald-500"
          >
            <option value={8}>Agosto 2026</option>
            <option value={9}>Septiembre 2026</option>
            <option value={10}>Octubre 2026</option>
          </select>

          <button
            onClick={handleDescargarPDF}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-950 flex items-center gap-1.5 transition-all"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Descargar Informe PDF (ANI)</span>
          </button>

          <button
            onClick={cargarDatosReporte}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
            title="Refrescar"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* Cuadro Explicativo: Cómo se calcula Di */}
      <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-200 flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-blue-400" />
            ¿Cómo se calcula la Disponibilidad Contractual ($D_i$)?
          </h3>
          <button
            onClick={() => setMostrarFormula(!mostrarFormula)}
            className="text-[11px] text-blue-400 hover:underline"
          >
            {mostrarFormula ? "Ocultar detalles" : "Ver fórmula y parámetros"}
          </button>
        </div>

        {mostrarFormula && (
          <div className="text-xs text-slate-400 space-y-2 pt-1 border-t border-slate-800/60 animate-in fade-in">
            <p className="leading-relaxed">
              De acuerdo con el <strong>Apéndice Técnico 1 de la ANI</strong>, la Disponibilidad Contractual ($D_i$) evalúa el tiempo efectivo que cada subsistema permanece operativo frente a las horas totales de servicio programadas en el mes:
            </p>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-center text-xs text-emerald-400 font-semibold">
              D_i = [ 1 - ( Σ Horas Indisponibles por Falla / ( N° Activos × 720 h ) ) ] × 100%
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px] pt-1">
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <strong className="text-slate-300 block">Horas Programadas:</strong>
                <span>720 horas/mes (30 días × 24h) multiplicadas por el número de activos del subsistema.</span>
              </div>
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <strong className="text-slate-300 block">Horas Indisponibles:</strong>
                <span>Tiempo acumulado de fallas no programadas registradas en <code className="text-amber-400">NOV_Novedades</code>.</span>
              </div>
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                <strong className="text-slate-300 block">Umbral Contractual ANI:</strong>
                <span>Meta mínima de cumplimiento: <strong className="text-emerald-400">≥ 98.5%</strong>. Menor a 98.5% genera no conformidad.</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tarjetas de Indicadores Clave */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Disponibilidad Promedio</span>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-emerald-400">{promedioGeneral}%</span>
            <span className="text-xs text-slate-500">Meta $\ge 98.5\%$</span>
          </div>
          <p className="text-[11px] text-emerald-400/90 font-medium flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            {totalCumplen} de {disponibilidad.length} subsistemas conformes
          </p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Mantenimientos Ejecutados</span>
          <div className="text-3xl font-extrabold text-white">{parteDiario.otsCerradas}</div>
          <p className="text-[11px] text-slate-400 font-medium">
            De {parteDiario.otsTotal} órdenes en base de datos
          </p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Cierres con Excepción GPS</span>
          <div className="text-3xl font-extrabold text-amber-400">{parteDiario.cierresConExcepcion}</div>
          <p className="text-[11px] text-slate-500">
            Túneles o zonas sin señal justificados
          </p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Novedades de Ruta</span>
          <div className="text-3xl font-extrabold text-blue-400">{parteDiario.novedadesReportadas}</div>
          <p className="text-[11px] text-slate-500">
            Imprevistos con OT Correctiva
          </p>
        </div>
      </div>

      {/* Tabla Detallada de Disponibilidad por Subsistema */}
      <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-sm text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            Matriz de Disponibilidad Contractual por Subsistema ($D_i$)
          </h3>
          <span className="text-xs font-mono text-slate-400">Ciclo: {anio}-{String(mes).padStart(2, "0")}</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs animate-pulse">
            Calculando métricas contractuales de los 368 activos...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Código</th>
                  <th className="p-3">Subsistema</th>
                  <th className="p-3 text-center">Zona (UF)</th>
                  <th className="p-3 text-center">Activos</th>
                  <th className="p-3 text-right">Horas Prog.</th>
                  <th className="p-3 text-right">Horas Falla</th>
                  <th className="p-3 text-right">Disponibilidad ($D_i$)</th>
                  <th className="p-3 text-center">Estado ANI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {disponibilidad.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-850/50 transition-colors">
                    <td className="p-3 font-mono font-bold text-blue-400">{row.TipoActivoID}</td>
                    <td className="p-3 font-bold text-white">{row.TipoActivoNombre}</td>
                    <td className="p-3 text-center">{row.UnidadFuncionalID}</td>
                    <td className="p-3 text-center">{row.TotalActivos}</td>
                    <td className="p-3 text-right font-mono">{row.HorasProgramadas.toFixed(0)}h</td>
                    <td className="p-3 text-right font-mono" style={{ color: row.HorasIndisponibles > 0 ? "#f87171" : "#94a3b8" }}>
                      {row.HorasIndisponibles.toFixed(1)}h
                    </td>
                    <td className="p-3 text-right font-mono font-bold text-emerald-400">
                      {row.DisponibilidadPorcentaje.toFixed(2)}%
                    </td>
                    <td className="p-3 text-center">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                        row.CumpleMeta 
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40" 
                          : "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                      }`}>
                        {row.CumpleMeta ? "CONFORME" : "NO CONFORME"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
