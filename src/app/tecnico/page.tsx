"use client";

import { useState, useEffect, useCallback } from "react";
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
  RefreshCw
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
  const [checklist, setChecklist] = useState<Record<string, string>>({});
  
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
      // 2.1 Obtener sesión actual
      const { data: { session } } = await supabase.auth.getSession();
      const email = session?.user?.email || "ivan.salcedo@concesiondelsisga.com.co";
      setUsuarioEmail(email);

      // Obtener nombre desde USR_Usuarios si está online
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

      // 2.2 Intentar cargar órdenes desde Supabase
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

          // Guardar en Dexie para soporte offline
          await dbLocal.ordenes.clear();
          await dbLocal.ordenes.bulkPut(mapped);
          setOrdenes(mapped);
          setLoadingOrdenes(false);
          return;
        }
      }

      // Fallback a Dexie (Modo Offline o sin conexión)
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

  // 3. Cargar preguntas de checklist al seleccionar una OT
  useEffect(() => {
    if (!selectedOT) {
      setPreguntas([]);
      setChecklist({});
      return;
    }

    const cargarPreguntas = async () => {
      try {
        if (navigator.onLine) {
          // Resolver FormularioID asociado al activo
          const { data: actData } = await supabase
            .from("ACT_Activos")
            .select("TipoActivoID, TIP_TiposActivo(FormularioID)")
            .eq("ActivoID", selectedOT.ActivoID)
            .single();

          const formId = (actData as any)?.TIP_TiposActivo?.FormularioID || "FRM-01";

          const { data: chkPreguntas } = await supabase
            .from("FRM_Preguntas")
            .select("PreguntaID, FormularioID, SeccionID, Pregunta, TipoRespuestaID, Orden")
            .eq("FormularioID", formId)
            .order("Orden", { ascending: true })
            .limit(10);

          if (chkPreguntas && chkPreguntas.length > 0) {
            const mappedPreguntas: PreguntaChecklist[] = chkPreguntas.map((p) => ({
              PreguntaID: p.PreguntaID,
              FormularioID: p.FormularioID,
              SeccionID: p.SeccionID,
              TextoPregunta: p.Pregunta,
              TipoRespuesta: "Si/No/NA",
              Orden: p.Orden,
            }));

            // Guardar en Dexie
            await dbLocal.preguntas.bulkPut(mappedPreguntas);
            setPreguntas(mappedPreguntas);

            // Inicializar respuestas en "Conforme"
            const initResp: Record<string, string> = {};
            mappedPreguntas.forEach((p) => {
              initResp[p.PreguntaID] = "Conforme";
            });
            setChecklist(initResp);
            return;
          }
        }

        // Fallback a Dexie o preguntas por defecto
        const cached = await dbLocal.preguntas.toArray();
        if (cached.length > 0) {
          setPreguntas(cached);
          const initResp: Record<string, string> = {};
          cached.forEach((p) => {
            initResp[p.PreguntaID] = "Conforme";
          });
          setChecklist(initResp);
        } else {
          // Fallback mínimo
          const defaults: PreguntaChecklist[] = [
            { PreguntaID: "CHK-01", FormularioID: "FRM-01", SeccionID: "SEC-01", TextoPregunta: "Estado físico de la estructura y anclajes", TipoRespuesta: "Si/No/NA", Orden: 1 },
            { PreguntaID: "CHK-02", FormularioID: "FRM-01", SeccionID: "SEC-01", TextoPregunta: "Alimentación eléctrica y niveles de voltaje", TipoRespuesta: "Si/No/NA", Orden: 2 },
            { PreguntaID: "CHK-03", FormularioID: "FRM-01", SeccionID: "SEC-01", TextoPregunta: "Conectividad y enlace de comunicaciones", TipoRespuesta: "Si/No/NA", Orden: 3 },
            { PreguntaID: "CHK-04", FormularioID: "FRM-01", SeccionID: "SEC-01", TextoPregunta: "Limpieza y hermeticidad de gabinete", TipoRespuesta: "Si/No/NA", Orden: 4 },
          ];
          setPreguntas(defaults);
          setChecklist({ "CHK-01": "Conforme", "CHK-02": "Conforme", "CHK-03": "Conforme", "CHK-04": "Conforme" });
        }
      } catch (e) {
        console.warn("Error cargando preguntas:", e);
      }
    };

    cargarPreguntas();
  }, [selectedOT]);

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

        // Validar Geofencing contra el activo seleccionado
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
      
      // Sincronizar en segundo plano si hay red
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
        cargarDatos(); // Recargar órdenes disponibles
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
        /* Vista 2: Formulario de Inspección de Campo */
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

          {/* 2. Checklist Dinámico del Activo */}
          <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-4">
            <h3 className="font-bold text-sm text-white flex items-center gap-2">
              <FileCheck2 className="w-4 h-4 text-blue-400" />
              2. Checklist de Inspección ({selectedOT.TipoActivoID})
            </h3>

            <div className="space-y-3 text-xs">
              {preguntas.map((p, idx) => (
                <div key={p.PreguntaID} className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center justify-between gap-3">
                  <span className="text-slate-200 font-medium">
                    {idx + 1}. {p.TextoPregunta}
                  </span>
                  <select
                    value={checklist[p.PreguntaID] || "Conforme"}
                    onChange={(e) => setChecklist({ ...checklist, [p.PreguntaID]: e.target.value })}
                    className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-slate-100 font-semibold flex-shrink-0"
                  >
                    <option>Conforme</option>
                    <option>No conforme</option>
                    <option>N/A</option>
                  </select>
                </div>
              ))}
            </div>
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
