"use client";

import { useState, useEffect } from "react";
import { 
  Calendar, 
  Layers, 
  Sparkles, 
  CheckCircle2, 
  Clock, 
  Search, 
  RefreshCw, 
  HardHat, 
  MapPin, 
  Play, 
  ChevronRight,
  ShieldCheck
} from "lucide-react";
import { supabase } from "@/lib/supabase";

interface PlanPreventivo {
  PlanID: string;
  ActivoID: string;
  FrecuenciaID: string;
  UltimaEjecucion: string | null;
  ProximaFecha: string;
  ResponsableID: string | null;
  Activo: boolean;
  ACT_Activos?: {
    Nombre: string;
    PK: string;
    UnidadFuncionalID: string;
    TIP_TiposActivo?: {
      Nombre: string;
    };
  };
  USR_Usuarios?: {
    Nombres: string;
    Apellidos: string;
  };
}

export default function PlanesPage() {
  const [planes, setPlanes] = useState<PlanPreventivo[]>([]);
  const [loading, setLoading] = useState(true);
  const [generando, setGenerando] = useState(false);
  const [mensajeExito, setMensajeExito] = useState<string | null>(null);

  // Parámetros de Generación
  const [mesGenerar, setMesGenerar] = useState(9); // Septiembre por defecto
  const [anioGenerar, setAnioGenerar] = useState(2026);
  const [ufGenerar, setUfGenerar] = useState("TODAS");

  // Filtros de visualización
  const [filtroUF, setFiltroUF] = useState("TODAS");
  const [filtroTexto, setFiltroTexto] = useState("");

  const cargarPlanes = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from("PLA_PlanMantenimiento")
        .select(`
          PlanID,
          ActivoID,
          FrecuenciaID,
          UltimaEjecucion,
          ProximaFecha,
          ResponsableID,
          Activo,
          ACT_Activos (
            Nombre,
            PK,
            UnidadFuncionalID,
            TIP_TiposActivo (
              Nombre
            )
          ),
          USR_Usuarios (
            Nombres,
            Apellidos
          )
        `)
        .order("ProximaFecha", { ascending: true });

      if (!error && data) {
        setPlanes(data as any);
      }
    } catch (e) {
      console.warn("Error cargando planes:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarPlanes();
  }, []);

  const handleDispararGeneracion = async () => {
    const ufParam = ufGenerar === "TODAS" ? null : ufGenerar;
    const confirmMsg = `¿Desea generar automáticamente el plan preventivo y las Órdenes de Trabajo para el ciclo ${anioGenerar}-${String(mesGenerar).padStart(2, "0")} (${ufGenerar})?`;
    if (!confirm(confirmMsg)) return;

    setGenerando(true);
    try {
      const { data, error } = await supabase.rpc("sgmc_generar_plan_mensual", {
        p_anio: anioGenerar,
        p_mes: mesGenerar,
        p_uf_id: ufParam,
      });

      if (error || !data?.exito) {
        alert(`Error al generar plan: ${error?.message || data?.error}`);
      } else {
        setMensajeExito(`¡Plan Preventivo Generado con Éxito! Procesados: ${data.planes_procesados} planes | Creadas: ${data.ots_generadas} órdenes de trabajo.`);
        cargarPlanes();
        setTimeout(() => setMensajeExito(null), 6000);
      }
    } catch (err) {
      console.error("Excepción generando plan:", err);
      alert("Error al ejecutar generador de planes preventivos");
    } finally {
      setGenerando(false);
    }
  };

  const planesFiltrados = planes.filter((p) => {
    const matchUF = filtroUF === "TODAS" || p.ACT_Activos?.UnidadFuncionalID === filtroUF;
    const matchTexto = 
      p.PlanID.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      (p.ACT_Activos?.Nombre || "").toLowerCase().includes(filtroTexto.toLowerCase()) ||
      (p.ACT_Activos?.PK || "").toLowerCase().includes(filtroTexto.toLowerCase()) ||
      (p.ACT_Activos?.TIP_TiposActivo?.Nombre || "").toLowerCase().includes(filtroTexto.toLowerCase());
    return matchUF && matchTexto;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Cabecera Principal */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold border border-blue-500/20 mb-2">
            <Calendar className="w-3.5 h-3.5" />
            <span>Generador de Planes Preventivos Mensuales (ESPEC-017)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Planes de Mantenimiento</h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Programación y asignación masiva de tareas preventivas por Unidad Funcional sobre los 368 activos.
          </p>
        </div>

        <button
          onClick={cargarPlanes}
          className="self-start sm:self-auto p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
          title="Refrescar"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Banner de Ejecución del Generador */}
      <div className="bg-gradient-to-r from-blue-950/80 via-slate-900 to-slate-900 p-5 rounded-2xl border border-blue-500/30 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-400" />
              Generador Automático de Ciclo Preventivo
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Crea registros en <code className="text-blue-300 font-mono">PLA_PlanMantenimiento</code> y emite las OTs programadas para los técnicos de zona.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={mesGenerar}
              onChange={(e) => setMesGenerar(parseInt(e.target.value))}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white font-semibold focus:outline-none focus:border-blue-500"
            >
              <option value={8}>Agosto 2026</option>
              <option value={9}>Septiembre 2026</option>
              <option value={10}>Octubre 2026</option>
              <option value={11}>Noviembre 2026</option>
              <option value={12}>Diciembre 2026</option>
            </select>

            <select
              value={ufGenerar}
              onChange={(e) => setUfGenerar(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white font-semibold focus:outline-none focus:border-blue-500"
            >
              <option value="TODAS">Todas las UFs (368 Activos)</option>
              <option value="UNF-01">UF1 (146 Activos)</option>
              <option value="UNF-02">UF2 (53 Activos)</option>
              <option value="UNF-03">UF3 (45 Activos)</option>
              <option value="UNF-04">UF4 (124 Activos)</option>
            </select>

            <button
              onClick={handleDispararGeneracion}
              disabled={generando}
              className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-lg shadow-blue-950 flex items-center gap-1.5 transition-all disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{generando ? "Generando Lote..." : "Generar OTs del Mes"}</span>
            </button>
          </div>
        </div>
      </div>

      {mensajeExito && (
        <div className="p-4 rounded-2xl bg-emerald-950/80 border border-emerald-500 text-emerald-200 text-xs flex items-center gap-3 animate-in fade-in">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <span>{mensajeExito}</span>
        </div>
      )}

      {/* Barra de Filtros */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-900/60 p-3 rounded-2xl border border-slate-800">
        <div className="relative sm:col-span-2">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Buscar por código de plan, activo, tipo o PK..."
            value={filtroTexto}
            onChange={(e) => setFiltroTexto(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <select
          value={filtroUF}
          onChange={(e) => setFiltroUF(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
        >
          <option value="TODOS">Todas las Unidades Funcionales</option>
          <option value="UNF-01">UF1 — Sisga / Guateque</option>
          <option value="UNF-02">UF2 — Guateque / Macanal</option>
          <option value="UNF-03">UF3 — Macanal / Santa María</option>
          <option value="UNF-04">UF4 — Santa María / Aguaclara</option>
        </select>
      </div>

      {/* Listado de Planes de Mantenimiento */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800 animate-pulse">
          Cargando planes preventivos...
        </div>
      ) : planesFiltrados.length === 0 ? (
        <div className="p-12 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800 space-y-2">
          <Calendar className="w-8 h-8 text-blue-400 mx-auto" />
          <p className="font-semibold text-slate-300">No hay planes registrados para este criterio</p>
          <p className="text-[11px] text-slate-500">Utiliza el botón "Generar OTs del Mes" para programar el próximo ciclo preventivo.</p>
        </div>
      ) : (
        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span className="font-bold text-slate-200">Total Planes Registrados: {planesFiltrados.length}</span>
            <span>Frecuencia Mensual (FRE-04)</span>
          </div>

          <div className="divide-y divide-slate-800/80">
            {planesFiltrados.map((p) => (
              <div key={p.PlanID} className="p-4 hover:bg-slate-850/60 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                      {p.PlanID}
                    </span>
                    <span className="font-bold text-white text-sm">
                      {p.ACT_Activos?.Nombre || p.ActivoID}
                    </span>
                  </div>
                  <p className="text-slate-400 flex items-center gap-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-500" />
                    <span>PK {p.ACT_Activos?.PK || "00+000"}</span>
                    <span>•</span>
                    <span className="text-slate-300 font-medium">{p.ACT_Activos?.UnidadFuncionalID}</span>
                    <span>•</span>
                    <span>{p.ACT_Activos?.TIP_TiposActivo?.Nombre || "Activo"}</span>
                  </p>
                </div>

                <div className="flex items-center gap-4 text-right">
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase tracking-wider">Próxima Fecha</span>
                    <span className="font-mono font-bold text-emerald-400 text-xs">
                      {p.ProximaFecha ? p.ProximaFecha.substring(0, 10) : "2026-09-05"}
                    </span>
                  </div>

                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase tracking-wider">Responsable</span>
                    <span className="text-slate-300 font-medium">
                      {p.USR_Usuarios ? `${p.USR_Usuarios.Nombres} ${p.USR_Usuarios.Apellidos || ""}` : "Técnico de Zona"}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
