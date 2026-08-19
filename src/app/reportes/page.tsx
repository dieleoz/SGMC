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
  FileSpreadsheet
} from "lucide-react";
import { supabase } from "@/lib/supabase";

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
  
  // Resumen Parte Diario CCO
  const [parteDiario, setParteDiario] = useState({
    otsTotal: 0,
    otsCerradas: 0,
    cierresConExcepcion: 0,
    tecnicosActivos: 5,
    novedadesReportadas: 0,
  });

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

  // Promedio General de Disponibilidad
  const promedioGeneral = disponibilidad.length > 0
    ? (disponibilidad.reduce((acc, curr) => acc + curr.DisponibilidadPorcentaje, 0) / disponibilidad.length).toFixed(2)
    : "100.00";

  const totalCumplen = disponibilidad.filter((d) => d.CumpleMeta).length;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Cabecera Principal */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20 mb-2">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Indicadores Contractuales & Auditoría ANI (ESPEC-021)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Disponibilidad & Reportes</h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Cálculo de Disponibilidad Contractual ($D_i \ge 98.5\%$) y Parte Diario de Operaciones del CCO.
          </p>
        </div>

        <div className="flex items-center gap-2">
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
            onClick={() => window.print()}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-slate-700 flex items-center gap-1.5 transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Exportar Informe</span>
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
            De {parteDiario.otsTotal} órdenes programadas
          </p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Cierres con Excepción GPS</span>
          <div className="text-3xl font-extrabold text-amber-400">{parteDiario.cierresConExcepcion}</div>
          <p className="text-[11px] text-slate-500">
            Túneles o zonas sin cobertura satelital
          </p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Novedades de Ruta</span>
          <div className="text-3xl font-extrabold text-blue-400">{parteDiario.novedadesReportadas}</div>
          <p className="text-[11px] text-slate-500">
            Imprevistos atendidos con OT Correctiva
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
                  <th className="p-3">Zona (UF)</th>
                  <th className="p-3 text-center">Activos</th>
                  <th className="p-3 text-right">Horas Prog.</th>
                  <th className="p-3 text-right">Horas Falla</th>
                  <th className="p-3 text-right">Disponibilidad</th>
                  <th className="p-3 text-center">Estado ANI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {disponibilidad.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-850/50 transition-colors">
                    <td className="p-3 font-mono font-bold text-blue-400">{row.TipoActivoID}</td>
                    <td className="p-3 font-bold text-white">{row.TipoActivoNombre}</td>
                    <td className="p-3">{row.UnidadFuncionalID}</td>
                    <td className="p-3 text-center">{row.TotalActivos}</td>
                    <td className="p-3 text-right font-mono">{row.HorasProgramadas.toFixed(0)}h</td>
                    <td className="p-3 text-right font-mono">{row.HorasIndisponibles.toFixed(1)}h</td>
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
