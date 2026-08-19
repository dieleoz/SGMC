"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import { 
  HardHat, 
  MapPin, 
  FileCheck2, 
  Wifi, 
  WifiOff, 
  CheckCircle2, 
  AlertCircle, 
  Navigation,
  Save,
  RotateCcw,
  Sparkles,
  AlertTriangle,
  Upload,
  RefreshCw,
  Layers,
  ChevronDown,
  ChevronRight
} from "lucide-react";
import { dbLocal, OrdenTrabajoLocal, MantenimientoEnCola, PreguntaChecklist } from "@/lib/db-offline";
import { syncEngine } from "@/lib/sync-engine";
import { supabase } from "@/lib/supabase";
import CameraCapture, { FotoEvidencia } from "@/components/CameraCapture";
import SignaturePad from "@/components/SignaturePad";

export default function TecnicoPage() {
  const [isOnline, setIsOnline] = useState(true);
  const [usuarioEmail, setUsuarioEmail] = useState<string>("ivan.salcedo@concesiondelsisga.com.co");
  const [usuarioNombre, setUsuarioNombre] = useState<string>("Iván Salcedo");
  
  const [ordenes, setOrdenes] = useState<OrdenTrabajoLocal[]>([]);
  const [loadingOrdenes, setLoadingOrdenes] = useState(true);
  const [selectedOT, setSelectedOT] = useState<OrdenTrabajoLocal | null>(null);
  
  // Preguntas dinámicas para la OT seleccionada
  const [preguntas, setPreguntas] = useState<PreguntaChecklist[]>([]);
  const [loadingPreguntas, setLoadingPreguntas] = useState(false);
  const [checklist, setChecklist] = useState<Record<string, string>>({});
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({});
  
  // GPS & Geofencing
  const [currentCoords, setCurrentCoords] = useState<{ lat: number; lng: number; accuracy: number } | null>(null);
  const [isLocating, setIsLocating] = useState(false);
  const [gpsError, setGpsError] = useState<string | null>(null);
  const [geofencingResult, setGeofencingResult] = useState<{ valido: boolean; distanciaMetros: number } | null>(null);
  
  // Cierre con Excepción (ESPEC-004 / ESPEC-020)
  const [cierreConExcepcion, setCierreConExcepcion] = useState(false);
  const [motivoExcepcion, setMotivoExcepcion] = useState("Túnel o zona sin cobertura satelital GPS");
  
  // Evidencias y firma
  const [observaciones, setObservaciones] = useState("");
  const [fotos, setFotos] = useState<FotoEvidencia[]>([]);
  const [firmaBase64, setFirmaBase64] = useState<string | null>(null);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [syncStatus, setSyncStatus] = useState<string | null>(null);

  // 1. Monitoreo de conectividad
  useEffect(() => {
    setIsOnline(navigator.onLine);
    const handleOnline = () => {
      setIsOnline(true);
      syncEngine.sincronizarCola().then((res) => {
        if (res.sincronizados > 0) {
          setSyncStatus(`${res.sincronizados} mantenimiento(s) sincronizado(s) automáticamente.`);
          setTimeout(() => setSyncStatus(null), 4000);
        }
      });
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  // 2. Cargar usuario autenticado y órdenes
  const cargarDatos = useCallback(async () => {
    setLoadingOrdenes(true);
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const email = session?.user?.email || "ivan.salcedo@concesiondelsisga.com.co";
      setUsuarioEmail(email);

      if (navigator.onLine) {
        const { data: usrData } = await supabase
          .from("USR_Usuarios")
          .select("Nombres, Apellidos")
          .ilike("Correo", email)
          .single();
        if (usrData) {
          setUsuarioNombre(`${usrData.Nombres} ${usrData.Apellidos || ""}`.trim());
        }
      }

      if (navigator.onLine) {
        const { data: otsDb, error: otErr } = await supabase
          .from("OT_OrdenesTrabajo")
          .select(`
            OTID,
            ActivoID,
            Tipo,
            FechaProgramada,
            EstadoOrdenID,
            TecnicoID,
            ACT_Activos (
              Nombre,
              PK,
              UnidadFuncionalID,
              Ubicacion_LatLong,
              TipoActivoID,
              TIP_TiposActivo (
                Nombre,
                FormularioID,
                RadioGeofencingKm
              )
            )
          `)
          .in("EstadoOrdenID", ["Asignada", "Programada", "En ejecucion"]);

        if (!otErr && otsDb && otsDb.length > 0) {
          const mapped: OrdenTrabajoLocal[] = otsDb.map((item: any) => {
            const activo = item.ACT_Activos;
            const tipoActivo = activo?.TIP_TiposActivo;
            return {
              OTID: item.OTID,
              ActivoID: item.ActivoID,
              ActivoNombre: activo?.Nombre || item.ActivoID,
              TipoActivoID: tipoActivo?.Nombre || activo?.TipoActivoID || "Equipo",
              UnidadFuncionalID: activo?.UnidadFuncionalID || "UF1",
              PK: activo?.PK || "00+000",
              Ubicacion_LatLong: activo?.Ubicacion_LatLong || "",
              RadioGeofencingKm: tipoActivo?.RadioGeofencingKm || 0.05,
              EstadoOrdenID: item.EstadoOrdenID,
              FechaProgramada: item.FechaProgramada ? item.FechaProgramada.substring(0, 10) : "2026-08-19",
              TecnicoID: item.TecnicoID || "USR-004",
            };
          });

          await dbLocal.ordenes.clear();
          await dbLocal.ordenes.bulkPut(mapped);
          setOrdenes(mapped);
          setLoadingOrdenes(false);
          return;
        }
      }

      const offlineOTs = await dbLocal.ordenes.toArray();
      setOrdenes(offlineOTs);
    } catch (err) {
      console.warn("[TecnicoPage] Error cargando órdenes desde Supabase, usando Dexie:", err);
      const offlineOTs = await dbLocal.ordenes.toArray();
      setOrdenes(offlineOTs);
    } finally {
      setLoadingOrdenes(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  // 3. Cargar preguntas dinámicas de checklist con Secciones y Valores de Lista
  useEffect(() => {
    if (!selectedOT) {
      setPreguntas([]);
      setChecklist({});
      return;
    }

    const cargarFormularioDinamico = async () => {
      setLoadingPreguntas(true);
      try {
        if (navigator.onLine) {
          // 3.1 Resolver FormularioID asociado al Tipo de Activo
          const { data: actData } = await supabase
            .from("ACT_Activos")
            .select("TipoActivoID, TIP_TiposActivo(FormularioID)")
            .eq("ActivoID", selectedOT.ActivoID)
            .single();

          const formId = (actData as any)?.TIP_TiposActivo?.FormularioID || "FRM_SOS";

          // 3.2 Traer preguntas con su sección
          const { data: chkPreguntas, error: pregErr } = await supabase
            .from("FRM_Preguntas")
            .select(`
              PreguntaID,
              FormularioID,
              SeccionID,
              Orden,
              Pregunta,
              TipoRespuestaID,
              Obligatoria,
              Unidad,
              ValorMinimo,
              ValorMaximo,
              FRM_Secciones (
                Nombre
              )
            `)
            .eq("FormularioID", formId)
            .order("Orden", { ascending: true });

          if (!pregErr && chkPreguntas && chkPreguntas.length > 0) {
            // 3.3 Traer opciones de lista asociadas (LST_ValoresLista)
            const preguntaIds = chkPreguntas.map((p) => p.PreguntaID);
            const { data: listData } = await supabase
              .from("LST_ValoresLista")
              .select("PreguntaID, Valor, Orden")
              .in("PreguntaID", preguntaIds)
              .order("Orden", { ascending: true });

            const opcionesMap: Record<string, string[]> = {};
            if (listData) {
              listData.forEach((item) => {
                if (!opcionesMap[item.PreguntaID]) opcionesMap[item.PreguntaID] = [];
                opcionesMap[item.PreguntaID].push(item.Valor);
              });
            }

            const mappedPreguntas: PreguntaChecklist[] = chkPreguntas.map((p: any) => ({
              PreguntaID: p.PreguntaID,
              FormularioID: p.FormularioID,
              SeccionID: p.SeccionID,
              SeccionNombre: p.FRM_Secciones?.Nombre || "Inspección General",
              TextoPregunta: p.Pregunta,
              TipoRespuestaID: p.TipoRespuestaID,
              Obligatoria: p.Obligatoria,
              Unidad: p.Unidad,
              ValorMinimo: p.ValorMinimo,
              ValorMaximo: p.ValorMaximo,
              Opciones: opcionesMap[p.PreguntaID] || ["Operativo", "Operativo con observaciones", "Fuera de servicio", "No aplica"],
              Orden: p.Orden,
            }));

            // Cachear en Dexie
            await dbLocal.preguntas.bulkPut(mappedPreguntas);
            setPreguntas(mappedPreguntas);

            // Inicializar respuestas por defecto
            const initResp: Record<string, string> = {};
            const initialSections: Record<string, boolean> = {};
            mappedPreguntas.forEach((p) => {
              if (p.TipoRespuestaID === "TPR-01") initResp[p.PreguntaID] = "Conforme";
              else if (p.TipoRespuestaID === "TPR-02") initResp[p.PreguntaID] = p.Opciones?.[0] || "Operativo";
              else if (p.TipoRespuestaID === "TPR-03") initResp[p.PreguntaID] = "";
              else initResp[p.PreguntaID] = "";

              if (p.SeccionNombre) initialSections[p.SeccionNombre] = true;
            });

            setChecklist(initResp);
            setOpenSections(initialSections);
            setLoadingPreguntas(false);
            return;
          }
        }

        // Fallback a Dexie si estamos offline
        const cached = await dbLocal.preguntas.toArray();
        if (cached.length > 0) {
          setPreguntas(cached);
          const initResp: Record<string, string> = {};
          const initialSections: Record<string, boolean> = {};
          cached.forEach((p) => {
            initResp[p.PreguntaID] = p.TipoRespuestaID === "TPR-01" ? "Conforme" : (p.Opciones?.[0] || "Operativo");
            if (p.SeccionNombre) initialSections[p.SeccionNombre] = true;
          });
          setChecklist(initResp);
          setOpenSections(initialSections);
        }
      } catch (e) {
        console.warn("Error cargando formulario dinámico:", e);
      } finally {
        setLoadingPreguntas(false);
      }
    };

    cargarFormularioDinamico();
  }, [selectedOT]);

  // Agrupar preguntas por Sección
  const preguntasPorSeccion = useMemo(() => {
    const grupos: Record<string, PreguntaChecklist[]> = {};
    preguntas.forEach((p) => {
      const sec = p.SeccionNombre || "Inspección General";
      if (!grupos[sec]) grupos[sec] = [];
      grupos[sec].push(p);
    });
    return grupos;
  }, [preguntas]);

  // 4. Captura de GPS Real
  const handleCaptureGPS = () => {
    setIsLocating(true);
    setGpsError(null);

    if (!navigator.geolocation) {
      setGpsError("Geolocalización no soportada en este navegador.");
      setIsLocating(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        const acc = pos.coords.accuracy;
        setCurrentCoords({ lat, lng, accuracy: acc });
        setIsLocating(false);

        if (selectedOT && selectedOT.Ubicacion_LatLong) {
          const [actLat, actLng] = selectedOT.Ubicacion_LatLong.split(",").map((s) => parseFloat(s.trim()));
          if (!isNaN(actLat) && !isNaN(actLng)) {
            const distMetros = calcularDistanciaMetros(lat, lng, actLat, actLng);
            const radioMaxMetros = (selectedOT.RadioGeofencingKm || 0.05) * 1000;
            setGeofencingResult({
              valido: distMetros <= radioMaxMetros,
              distanciaMetros: Math.round(distMetros)
            });
          }
        }
      },
      (err) => {
        console.warn("GPS error:", err);
        setCurrentCoords(null);
        setGeofencingResult({ valido: false, distanciaMetros: -1 });
        setGpsError(`GPS sin señal (${err.message}). Si estás en un túnel o sin cobertura, activa 'Cierre con Excepción'.`);
        setIsLocating(false);
      },
      { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
    );
  };

  const calcularDistanciaMetros = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371e3;
    const φ1 = (lat1 * Math.PI) / 180;
    const φ2 = (lat2 * Math.PI) / 180;
    const Δφ = ((lat2 - lat1) * Math.PI) / 180;
    const Δλ = ((lon2 - lon1) * Math.PI) / 180;
    const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  // 5. Guardar en cola local Offline y Sincronizar
  const handleGuardarCierre = async () => {
    if (!selectedOT) return;

    if (!geofencingResult?.valido && !cierreConExcepcion) {
      alert("Error: Validación GPS obligatoria. Debe estar dentro del radio del activo o justificar un 'Cierre con Excepción'.");
      return;
    }

    if (!firmaBase64) {
      alert("Error: La firma táctil del técnico es obligatoria.");
      return;
    }

    const nuevoMantenimiento: MantenimientoEnCola = {
      OTID: selectedOT.OTID,
      ActivoID: selectedOT.ActivoID,
      FechaInicio: new Date().toISOString(),
      FechaCierre: new Date().toISOString(),
      Coordenadas_Cierre_LatLong: currentCoords ? `${currentCoords.lat.toFixed(6)}, ${currentCoords.lng.toFixed(6)}` : null,
      PrecisionGPSMetros: currentCoords?.accuracy || null,
      GeofencingValido: geofencingResult?.valido ?? false,
      DistanciaMetros: geofencingResult?.distanciaMetros ?? null,
      CierreConExcepcion: cierreConExcepcion,
      MotivoExcepcion: cierreConExcepcion ? motivoExcepcion : null,
      Observaciones: observaciones,
      ChecklistRespuestas: checklist,
      Fotografias: fotos.map((f) => ({
        id: f.id,
        base64: f.base64,
        descripcion: f.descripcion,
        timestamp: f.timestamp,
        ubicacion: f.ubicacion || null,
      })),
      FirmaBase64: firmaBase64,
      Sincronizado: false,
      TimestampCreacion: new Date().toISOString()
    };

    try {
      await dbLocal.mantenimientosCola.add(nuevoMantenimiento);
      setSavedSuccess(true);
      
      if (typeof navigator !== "undefined" && navigator.onLine) {
        syncEngine.sincronizarCola().then((res) => {
          console.log("[TecnicoPage] Auto-sync resultado:", res);
        });
      }

      setTimeout(() => {
        setSavedSuccess(false);
        setSelectedOT(null);
        setCurrentCoords(null);
        setGeofencingResult(null);
        setCierreConExcepcion(false);
        setFotos([]);
        setFirmaBase64(null);
        setObservaciones("");
        cargarDatos();
      }, 2000);
    } catch (err) {
      console.error("Error guardando en cola offline:", err);
      alert("Error al guardar mantenimiento en almacenamiento local");
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Barra de Estado de Conectividad e Identidad */}
      <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900 border border-slate-800 text-xs shadow-sm">
        <div className="flex items-center gap-2">
          <div className={`w-2.5 h-2.5 rounded-full ${isOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"}`} />
          <span className="font-semibold text-slate-300">
            {isOnline ? "Modo En Línea (Supabase Sync)" : "Modo Offline Activo (Túneles/Vía)"}
          </span>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          {isOnline ? <Wifi className="w-4 h-4 text-emerald-400" /> : <WifiOff className="w-4 h-4 text-amber-400" />}
          <span className="font-medium text-slate-300 truncate max-w-[220px]">
            {usuarioNombre} ({usuarioEmail})
          </span>
          <button
            onClick={cargarDatos}
            title="Refrescar órdenes"
            className="p-1 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loadingOrdenes ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {syncStatus && (
        <div className="p-3 rounded-xl bg-blue-950/60 border border-blue-800 text-blue-300 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-blue-400" />
          <span>{syncStatus}</span>
        </div>
      )}

      {savedSuccess && (
        <div className="p-4 rounded-2xl bg-emerald-900/50 border border-emerald-500 text-emerald-200 flex items-center gap-3 animate-bounce">
          <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
          <div>
            <p className="font-bold text-sm">¡Mantenimiento Guardado Exitosamente!</p>
            <p className="text-xs text-emerald-300">Asentado en cola local y sincronizado hacia Supabase sin inventar coordenadas.</p>
          </div>
        </div>
      )}

      {/* Vista 1: Selector de Órdenes Asignadas */}
      {!selectedOT ? (
        <div className="space-y-4">
          {/* Banner de Instalación Rápida */}
          <div className="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 border border-emerald-500/30 p-4 rounded-2xl flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 flex-shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-white">¿Trabajando en el corredor vial?</h3>
                <p className="text-[11px] text-slate-400">Instala esta app en tu pantalla de inicio para ejecutar inspecciones sin cobertura.</p>
              </div>
            </div>
            <button
              onClick={() => {
                if ((window as any).__pwaPrompt) {
                  (window as any).__pwaPrompt.prompt();
                } else {
                  alert("Para instalar:\n• En Android: Menú (3 puntos) > 'Instalar aplicación'.\n• En iPhone: 'Compartir' > 'Agregar a pantalla de inicio'.");
                }
              }}
              className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold whitespace-nowrap shadow-lg shadow-emerald-950 flex-shrink-0 flex items-center gap-1.5"
            >
              <Upload className="w-3.5 h-3.5 rotate-180" />
              <span>Instalar App</span>
            </button>
          </div>

          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <HardHat className="w-5 h-5 text-emerald-400" />
              Órdenes de Trabajo Ejecutables ({ordenes.length})
            </h2>
            <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
              Estado: Asignada
            </span>
          </div>

          {loadingOrdenes ? (
            <div className="p-8 text-center text-slate-400 text-xs bg-slate-900/50 rounded-2xl border border-slate-800 animate-pulse">
              Cargando órdenes de trabajo asignadas desde Supabase / Dexie...
            </div>
          ) : ordenes.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-xs bg-slate-900/50 rounded-2xl border border-slate-800 space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
              <p className="font-semibold text-slate-300">No tienes órdenes de trabajo pendientes de ejecución</p>
              <p className="text-[11px] text-slate-500">Todas las órdenes asignadas a tu usuario se encuentran cerradas o en revisión.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {ordenes.map((ot) => (
                <div
                  key={ot.OTID}
                  onClick={() => setSelectedOT(ot)}
                  className="bg-slate-900 p-5 rounded-2xl border border-slate-800 hover:border-emerald-500/50 cursor-pointer transition-all hover:bg-slate-850 space-y-3 group"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {ot.OTID}
                    </span>
                    <span className="text-xs text-slate-400">Prog: {ot.FechaProgramada}</span>
                  </div>

                  <div>
                    <h3 className="font-bold text-base text-white group-hover:text-emerald-400 transition-colors">
                      {ot.ActivoNombre}
                    </h3>
                    <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-1">
                      <MapPin className="w-3.5 h-3.5 text-slate-500" />
                      PK {ot.PK} • {ot.UnidadFuncionalID} • {ot.TipoActivoID}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
                    <span className="text-slate-500 font-mono">
                      Tolerancia: {(ot.RadioGeofencingKm || 0.05) * 1000}m
                    </span>
                    <span className="text-emerald-400 font-semibold flex items-center gap-1">
                      Iniciar Inspección &rarr;
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        /* Vista 2: Formulario de Inspección de Campo Dinámico */
        <div className="space-y-6 animate-in fade-in duration-300">
          <div className="flex items-center justify-between bg-slate-900 p-4 rounded-2xl border border-slate-800">
            <div>
              <span className="text-xs font-bold text-emerald-400">{selectedOT.OTID}</span>
              <h2 className="text-lg font-bold text-white">{selectedOT.ActivoNombre}</h2>
              <p className="text-xs text-slate-400">PK {selectedOT.PK} • Radio permitido: {(selectedOT.RadioGeofencingKm || 0.05) * 1000}m</p>
            </div>
            <button
              onClick={() => setSelectedOT(null)}
              className="px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 flex items-center gap-1 border border-slate-700"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Volver</span>
            </button>
          </div>

          {/* 1. Validación Satelital de Geofencing */}
          <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-white flex items-center gap-2">
                <Navigation className="w-4 h-4 text-emerald-400" />
                1. Validación de Presencia Satelital (Geofencing Fail-Closed)
              </h3>
              <button
                onClick={handleCaptureGPS}
                disabled={isLocating}
                className="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-md shadow-emerald-950 transition-all disabled:opacity-50"
              >
                <MapPin className="w-3.5 h-3.5" />
                <span>{isLocating ? "Obteniendo GPS..." : "Capturar Coordenadas GPS"}</span>
              </button>
            </div>

            {gpsError && (
              <div className="p-3 rounded-xl bg-rose-950/50 border border-rose-800 text-rose-300 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
                <span>{gpsError}</span>
              </div>
            )}

            {currentCoords && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-500 block">Latitud GPS</span>
                  <span className="font-mono text-slate-200 font-semibold">{currentCoords.lat.toFixed(6)}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-500 block">Longitud GPS</span>
                  <span className="font-mono text-slate-200 font-semibold">{currentCoords.lng.toFixed(6)}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 col-span-2 sm:col-span-1">
                  <span className="text-slate-500 block">Precisión Satelital</span>
                  <span className="font-mono text-emerald-400 font-semibold">±{Math.round(currentCoords.accuracy)} metros</span>
                </div>
              </div>
            )}

            {geofencingResult && geofencingResult.distanciaMetros >= 0 && (
              <div className={`p-3 rounded-xl text-xs flex items-center gap-2 ${geofencingResult.valido ? "bg-emerald-950/60 text-emerald-300 border border-emerald-700/50" : "bg-rose-950/60 text-rose-300 border border-rose-700/50"}`}>
                {geofencingResult.valido ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <AlertCircle className="w-4 h-4 text-rose-400" />}
                <span>
                  {geofencingResult.valido 
                    ? `¡Validación Conforme! A ${geofencingResult.distanciaMetros}m del activo (Dentro del radio de ${(selectedOT.RadioGeofencingKm || 0.05) * 1000}m).`
                    : `Fuera de radio: Distancia calculada ${geofencingResult.distanciaMetros}m (Máximo permitido: ${(selectedOT.RadioGeofencingKm || 0.05) * 1000}m).`}
                </span>
              </div>
            )}

            {/* Panel de Cierre con Excepción (ESPEC-004 / ESPEC-020) */}
            {(!geofencingResult?.valido || gpsError) && (
              <div className="p-3.5 rounded-xl bg-slate-950 border border-amber-500/40 space-y-2.5 text-xs">
                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer text-amber-300 font-bold">
                    <input
                      type="checkbox"
                      checked={cierreConExcepcion}
                      onChange={(e) => setCierreConExcepcion(e.target.checked)}
                      className="rounded bg-slate-900 border-slate-700 text-amber-500 focus:ring-amber-500 w-4 h-4"
                    />
                    <AlertTriangle className="w-4 h-4 text-amber-400" />
                    <span>Activar Cierre con Excepción Manual (ESPEC-004)</span>
                  </label>
                </div>

                {cierreConExcepcion && (
                  <div className="space-y-1.5 pt-1">
                    <label className="text-[11px] text-slate-400">Motivo de Excepción (Auditable por Interventoría):</label>
                    <select
                      value={motivoExcepcion}
                      onChange={(e) => setMotivoExcepcion(e.target.value)}
                      className="w-full bg-slate-900 border border-amber-500/50 rounded-xl p-2 text-xs text-white font-medium focus:outline-none"
                    >
                      <option>Túnel o zona sin cobertura satelital GPS</option>
                      <option>Equipo en altura o recinto cerrado bajo techo</option>
                      <option>Falla de hardware / sensor GPS del dispositivo</option>
                      <option>Operación de emergencia vial autorizada por CCO</option>
                    </select>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 2. Checklist Dinámico por Subsistema */}
          <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-5">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-white flex items-center gap-2">
                <FileCheck2 className="w-4 h-4 text-blue-400" />
                2. Checklist Dinámico de Inspección ({selectedOT.TipoActivoID})
              </h3>
              <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded-lg">
                {preguntas.length} Ítems
              </span>
            </div>

            {loadingPreguntas ? (
              <div className="p-6 text-center text-xs text-slate-400 animate-pulse bg-slate-950 rounded-xl border border-slate-800">
                Cargando formulario y preguntas por subsistema...
              </div>
            ) : Object.keys(preguntasPorSeccion).length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-400 bg-slate-950 rounded-xl border border-slate-800">
                No hay preguntas configuradas para este tipo de activo.
              </div>
            ) : (
              <div className="space-y-4">
                {Object.entries(preguntasPorSeccion).map(([seccionNombre, items]) => {
                  const isOpen = openSections[seccionNombre] ?? true;
                  return (
                    <div key={seccionNombre} className="rounded-xl border border-slate-800 bg-slate-950/60 overflow-hidden">
                      {/* Cabecera de Sección */}
                      <button
                        type="button"
                        onClick={() => setOpenSections((prev) => ({ ...prev, [seccionNombre]: !isOpen }))}
                        className="w-full p-3 bg-slate-850/80 hover:bg-slate-800/80 flex items-center justify-between text-left transition-colors border-b border-slate-800/60"
                      >
                        <span className="text-xs font-bold text-slate-200 flex items-center gap-2">
                          <Layers className="w-3.5 h-3.5 text-emerald-400" />
                          {seccionNombre} ({items.length})
                        </span>
                        {isOpen ? (
                          <ChevronDown className="w-4 h-4 text-slate-400" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-slate-400" />
                        )}
                      </button>

                      {/* Preguntas de la Sección */}
                      {isOpen && (
                        <div className="p-3.5 space-y-3">
                          {items.map((p, idx) => (
                            <div
                              key={p.PreguntaID}
                              className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs"
                            >
                              <div className="flex items-start justify-between gap-2">
                                <span className="text-slate-200 font-medium leading-tight">
                                  {idx + 1}. {p.TextoPregunta}
                                  {p.Obligatoria && <span className="text-rose-400 ml-1 font-bold">*</span>}
                                </span>
                                {p.Unidad && (
                                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-emerald-400 border border-slate-700 flex-shrink-0">
                                    {p.Unidad}
                                  </span>
                                )}
                              </div>

                              {/* Renderizador de Control según TipoRespuestaID */}
                              {p.TipoRespuestaID === "TPR-01" ? (
                                /* Sí / No / NA */
                                <div className="flex items-center gap-2 pt-1">
                                  {["Conforme", "No conforme", "N/A"].map((opt) => {
                                    const isSelected = (checklist[p.PreguntaID] || "Conforme") === opt;
                                    let activeClass = "bg-emerald-600 text-white font-bold border-emerald-500";
                                    if (opt === "No conforme") activeClass = "bg-rose-600 text-white font-bold border-rose-500";
                                    if (opt === "N/A") activeClass = "bg-slate-700 text-white font-bold border-slate-600";

                                    return (
                                      <button
                                        key={opt}
                                        type="button"
                                        onClick={() => setChecklist({ ...checklist, [p.PreguntaID]: opt })}
                                        className={`px-3 py-1 rounded-lg text-xs font-semibold border transition-all ${
                                          isSelected
                                            ? activeClass
                                            : "bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700"
                                        }`}
                                      >
                                        {opt}
                                      </button>
                                    );
                                  })}
                                </div>
                              ) : p.TipoRespuestaID === "TPR-02" ? (
                                /* Lista Desplegable (LST_ValoresLista) */
                                <select
                                  value={checklist[p.PreguntaID] || p.Opciones?.[0] || ""}
                                  onChange={(e) => setChecklist({ ...checklist, [p.PreguntaID]: e.target.value })}
                                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white font-medium focus:outline-none focus:border-emerald-500"
                                >
                                  {(p.Opciones || ["Operativo", "Operativo con observaciones", "Fuera de servicio", "No aplica"]).map((opc) => (
                                    <option key={opc} value={opc}>
                                      {opc}
                                    </option>
                                  ))}
                                </select>
                              ) : p.TipoRespuestaID === "TPR-03" ? (
                                /* Número con Unidad */
                                <div className="flex items-center gap-2">
                                  <input
                                    type="number"
                                    step="any"
                                    min={p.ValorMinimo ?? undefined}
                                    max={p.ValorMaximo ?? undefined}
                                    placeholder={p.Unidad ? `Valor en ${p.Unidad}` : "Ingrese valor numérico..."}
                                    value={checklist[p.PreguntaID] || ""}
                                    onChange={(e) => setChecklist({ ...checklist, [p.PreguntaID]: e.target.value })}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                                  />
                                  {p.Unidad && <span className="text-xs text-slate-400 font-mono">{p.Unidad}</span>}
                                </div>
                              ) : p.TipoRespuestaID === "TPR-05" ? (
                                /* Texto Largo / Observación */
                                <textarea
                                  rows={2}
                                  placeholder="Escriba detalle u observación..."
                                  value={checklist[p.PreguntaID] || ""}
                                  onChange={(e) => setChecklist({ ...checklist, [p.PreguntaID]: e.target.value })}
                                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                                />
                              ) : (
                                /* Texto Corto / Fallback */
                                <input
                                  type="text"
                                  placeholder="Escriba respuesta..."
                                  value={checklist[p.PreguntaID] || ""}
                                  onChange={(e) => setChecklist({ ...checklist, [p.PreguntaID]: e.target.value })}
                                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                                />
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* 3. Captura Real de Fotografías WebP con Georreferenciación */}
          <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-4">
            <CameraCapture
              fotos={fotos}
              onAddFoto={(nuevaFoto) => setFotos([...fotos, nuevaFoto])}
              onRemoveFoto={(id) => setFotos(fotos.filter((f) => f.id !== id))}
              gpsCoords={currentCoords}
            />
          </div>

          {/* 4. Observaciones y Firma Táctil Real */}
          <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1 font-medium">Observaciones del Técnico:</label>
              <textarea
                value={observaciones}
                onChange={(e) => setObservaciones(e.target.value)}
                placeholder="Indique el trabajo realizado o novedades encontradas en campo..."
                rows={2}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <SignaturePad
              onSave={(b64) => setFirmaBase64(b64)}
              onClear={() => setFirmaBase64(null)}
            />
          </div>

          {/* Botón de Cierre de Mantenimiento */}
          <button
            onClick={handleGuardarCierre}
            disabled={(!geofencingResult?.valido && !cierreConExcepcion) || !firmaBase64}
            className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white font-bold text-sm shadow-xl shadow-emerald-950 flex items-center justify-center gap-2 transition-all hover:scale-[1.01] disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            <span>Guardar y Cerrar Mantenimiento (En Revisión)</span>
          </button>
        </div>
      )}
    </div>
  );
}
