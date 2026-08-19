"use client";

import { useState, useEffect } from "react";
import { 
  AlertTriangle, 
  MapPin, 
  Plus, 
  Camera, 
  CheckCircle2, 
  Clock, 
  Search, 
  Filter,
  Layers,
  ArrowRight,
  RefreshCw,
  X
} from "lucide-react";
import { supabase } from "@/lib/supabase";
import CameraCapture, { FotoEvidencia } from "@/components/CameraCapture";
import { subirFotoEvidencia } from "@/lib/storage-service";

interface NovedadRuta {
  NovedadID: string;
  UsuarioID: string;
  Tipo: string;
  Descripcion: string;
  Ubicacion_LatLong: string | null;
  Fotografia: string | null;
  ActivoID: string | null;
  Estado: string;
  FechaHora: string;
  ACT_Activos?: {
    Nombre: string;
    PK: string;
    UnidadFuncionalID: string;
  };
}

interface ActivoSimple {
  ActivoID: string;
  Nombre: string;
  PK: string;
  UnidadFuncionalID: string;
  Ubicacion_LatLong: string;
}

export default function NovedadesPage() {
  const [novedades, setNovedades] = useState<NovedadRuta[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  
  // Activos para autocompletado
  const [activos, setActivos] = useState<ActivoSimple[]>([]);
  const [filtroTexto, setFiltroTexto] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("TODOS");

  // Formulario nueva novedad
  const [nuevoActivoId, setNuevoActivoId] = useState("");
  const [nuevoTipo, setNuevoTipo] = useState("Falla detectada");
  const [nuevaDescripcion, setNuevaDescripcion] = useState("");
  const [generaOT, setGeneraOT] = useState(true);
  const [fotos, setFotos] = useState<FotoEvidencia[]>([]);
  const [gpsCoords, setGpsCoords] = useState<{ lat: number; lng: number; accuracy: number } | null>(null);
  const [guardando, setGuardando] = useState(false);
  const [mensajeExito, setMensajeExito] = useState<string | null>(null);

  // Cargar novedades de la base de datos
  const cargarNovedades = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from("NOV_Novedades")
        .select(`
          NovedadID,
          UsuarioID,
          Tipo,
          Descripcion,
          Ubicacion_LatLong,
          Fotografia,
          ActivoID,
          Estado,
          FechaHora,
          ACT_Activos (
            Nombre,
            PK,
            UnidadFuncionalID
          )
        `)
        .order("FechaHora", { ascending: false });

      if (!error && data) {
        setNovedades(data as any);
      }
    } catch (e) {
      console.warn("Error cargando novedades:", e);
    } finally {
      setLoading(false);
    }
  };

  // Cargar catálogo de activos
  useEffect(() => {
    cargarNovedades();

    const fetchActivos = async () => {
      const { data } = await supabase
        .from("ACT_Activos")
        .select("ActivoID, Nombre, PK, UnidadFuncionalID, Ubicacion_LatLong")
        .order("PK", { ascending: true });
      if (data) setActivos(data);
    };
    fetchActivos();
  }, []);

  // Capturar GPS
  const handleGetLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setGpsCoords({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
          });
        },
        (err) => console.warn("Error GPS:", err),
        { enableHighAccuracy: true }
      );
    }
  };

  // Guardar novedad llamando a RPC
  const handleSubmitNovedad = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nuevaDescripcion.trim()) {
      alert("Por favor ingrese la descripción del hallazgo.");
      return;
    }

    setGuardando(true);
    try {
      let fotoUrl = "https://placeholder.sgmc.co/novedad.webp";
      if (fotos.length > 0 && fotos[0].base64) {
        const upUrl = await subirFotoEvidencia(fotos[0].base64, "NOV-DIRECT", fotos[0].id);
        if (upUrl) fotoUrl = upUrl;
      }

      const payload = {
        UsuarioID: "USR-004", // Técnico / Patrullero
        Tipo: nuevoTipo,
        Descripcion: nuevaDescripcion,
        Ubicacion_LatLong: gpsCoords ? `${gpsCoords.lat.toFixed(6)}, ${gpsCoords.lng.toFixed(6)}` : null,
        Fotografia: fotoUrl,
        ActivoID: nuevoActivoId || null,
        GeneraOT: generaOT,
      };

      const { data, error } = await supabase.rpc("sgmc_reportar_novedad", {
        p_payload: payload,
      });

      if (error || !data?.exito) {
        alert(`Error al registrar novedad: ${error?.message || data?.error}`);
      } else {
        setMensajeExito(`Novedad ${data.novedad_id} registrada con éxito. ${data.ot_id ? `OT Correctiva creada: ${data.ot_id}` : ""}`);
        setModalOpen(false);
        setNuevaDescripcion("");
        setNuevoActivoId("");
        setFotos([]);
        cargarNovedades();
        setTimeout(() => setMensajeExito(null), 5000);
      }
    } catch (err) {
      console.error("Excepción en registro de novedad:", err);
      alert("Error inesperado al guardar la novedad");
    } finally {
      setGuardando(false);
    }
  };

  const novedadesFiltradas = novedades.filter((n) => {
    const matchEstado = filtroEstado === "TODOS" || n.Estado === filtroEstado;
    const matchTexto = 
      n.NovedadID.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      n.Descripcion.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      (n.ACT_Activos?.Nombre || "").toLowerCase().includes(filtroTexto.toLowerCase()) ||
      (n.ACT_Activos?.PK || "").toLowerCase().includes(filtroTexto.toLowerCase());
    return matchEstado && matchTexto;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Cabecera Principal */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold border border-amber-500/20 mb-2">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Gestión de Incidentes y Novedades de Ruta (ESPEC-016)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Novedades de Campo</h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Registro y atención ágil de hallazgos imprevistos sobre los 137 km del corredor vial.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={cargarNovedades}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
            title="Refrescar"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <button
            onClick={() => {
              setModalOpen(true);
              handleGetLocation();
            }}
            className="px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs sm:text-sm shadow-lg shadow-amber-950 flex items-center gap-2 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Reportar Novedad</span>
          </button>
        </div>
      </div>

      {mensajeExito && (
        <div className="p-4 rounded-2xl bg-emerald-950/80 border border-emerald-500 text-emerald-200 text-xs flex items-center gap-3 animate-in fade-in">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <span>{mensajeExito}</span>
        </div>
      )}

      {/* Filtros de Búsqueda */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-900/60 p-3 rounded-2xl border border-slate-800">
        <div className="relative sm:col-span-2">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Buscar por ID, activo, PK o descripción..."
            value={filtroTexto}
            onChange={(e) => setFiltroTexto(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-500"
          />
        </div>

        <select
          value={filtroEstado}
          onChange={(e) => setFiltroEstado(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
        >
          <option value="TODOS">Todos los Estados</option>
          <option value="Reportada">Reportada</option>
          <option value="Aceptada">Aceptada / Con OT</option>
          <option value="Descartada">Descartada</option>
        </select>
      </div>

      {/* Listado de Novedades */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800 animate-pulse">
          Cargando novedades de ruta...
        </div>
      ) : novedadesFiltradas.length === 0 ? (
        <div className="p-12 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800 space-y-2">
          <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
          <p className="font-semibold text-slate-300">No hay novedades registradas con estos filtros</p>
          <p className="text-[11px] text-slate-500">Haz clic en "Reportar Novedad" para asentar un hallazgo en ruta.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {novedadesFiltradas.map((nov) => (
            <div
              key={nov.NovedadID}
              className="bg-slate-900 p-5 rounded-2xl border border-slate-800 hover:border-amber-500/40 transition-all space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  {nov.NovedadID}
                </span>
                <span className="text-xs text-slate-500 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" />
                  {nov.FechaHora ? new Date(nov.FechaHora).toLocaleString("es-CO", { dateStyle: "short", timeStyle: "short" }) : "Hoy"}
                </span>
              </div>

              <div>
                <h3 className="font-bold text-sm text-white">
                  {nov.ACT_Activos?.Nombre || nov.ActivoID || "Activo No Inventariado"}
                </h3>
                <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" />
                  {nov.ACT_Activos?.PK ? `PK ${nov.ACT_Activos.PK}` : "Vía Principal"} • {nov.ACT_Activos?.UnidadFuncionalID || "Corredor Sisga"}
                </p>
              </div>

              <p className="text-xs text-slate-300 bg-slate-950 p-2.5 rounded-xl border border-slate-800/80 leading-relaxed">
                {nov.Descripcion}
              </p>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                <span className="text-slate-400 font-medium">Tipo: {nov.Tipo}</span>
                <span className={`px-2 py-0.5 rounded-md font-bold text-[10px] ${
                  nov.Estado === "Reportada" 
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                    : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                }`}>
                  {nov.Estado}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal: Registrar Novedad de Ruta */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-slate-900 border border-slate-800 w-full max-w-lg rounded-2xl shadow-2xl p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                Reportar Novedad de Ruta
              </h2>
              <button onClick={() => setModalOpen(false)} className="p-1 hover:bg-slate-800 rounded-lg text-slate-400">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitNovedad} className="space-y-4 text-xs">
              {/* Tipo de Novedad */}
              <div>
                <label className="block text-slate-400 font-medium mb-1">Tipo de Hallazgo:</label>
                <select
                  value={nuevoTipo}
                  onChange={(e) => setNuevoTipo(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white font-medium focus:outline-none focus:border-amber-500"
                >
                  <option value="Falla detectada">Falla detectada en equipo existente</option>
                  <option value="Activo no inventariado">Activo no inventariado en vía</option>
                </select>
              </div>

              {/* Activo Asociado */}
              <div>
                <label className="block text-slate-400 font-medium mb-1">Activo Afectado (Opcional):</label>
                <select
                  value={nuevoActivoId}
                  onChange={(e) => setNuevoActivoId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white font-medium focus:outline-none focus:border-amber-500"
                >
                  <option value="">-- Sin activo específico / En corredor --</option>
                  {activos.map((a) => (
                    <option key={a.ActivoID} value={a.ActivoID}>
                      {a.ActivoID} - {a.Nombre} (PK {a.PK} / {a.UnidadFuncionalID})
                    </option>
                  ))}
                </select>
              </div>

              {/* Descripción */}
              <div>
                <label className="block text-slate-400 font-medium mb-1">Descripción del Hallazgo / Daño:</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Describa el componente afectado, señales de vandalismo, choque vehicular o falla observada..."
                  value={nuevaDescripcion}
                  onChange={(e) => setNuevaDescripcion(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-amber-500"
                />
              </div>

              {/* Check Generar OT Correctiva */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between">
                <label className="flex items-center gap-2 text-slate-300 font-medium cursor-pointer">
                  <input
                    type="checkbox"
                    checked={generaOT}
                    onChange={(e) => setGeneraOT(e.target.checked)}
                    className="rounded bg-slate-900 border-slate-700 text-amber-500 focus:ring-amber-500 w-4 h-4"
                  />
                  <span>Generar automáticamente Orden de Trabajo Correctiva</span>
                </label>
              </div>

              {/* Cámara y Fotos */}
              <CameraCapture
                fotos={fotos}
                onAddFoto={(f) => setFotos([...fotos, f])}
                onRemoveFoto={(id) => setFotos(fotos.filter((f) => f.id !== id))}
                gpsCoords={gpsCoords}
              />

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-300 hover:text-white bg-slate-800 font-medium"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={guardando}
                  className="px-5 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold shadow-lg shadow-amber-950 disabled:opacity-50"
                >
                  {guardando ? "Guardando..." : "Registrar Novedad"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
