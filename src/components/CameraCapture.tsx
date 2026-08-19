"use client";

import React, { useRef, useState } from "react";
import { Camera, Trash2, Image as ImageIcon, Plus } from "lucide-react";

export interface FotoEvidencia {
  id: string;
  base64: string;
  descripcion: string;
  timestamp: string;
  sizeKb: number;
  ubicacion?: string | null;
}

interface CameraCaptureProps {
  fotos: FotoEvidencia[];
  onAddFoto: (foto: FotoEvidencia) => void;
  onRemoveFoto: (id: string) => void;
  gpsCoords?: { lat: number; lng: number } | null;
}

export default function CameraCapture({ fotos, onAddFoto, onRemoveFoto, gpsCoords }: CameraCaptureProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsProcessing(true);

    try {
      // 1. Leer imagen
      const img = new Image();
      const reader = new FileReader();

      reader.onload = (event) => {
        img.src = event.target?.result as string;
        img.onload = () => {
          // 2. Redimensionar en Canvas (máx 1200px de ancho/alto)
          const canvas = document.createElement("canvas");
          const MAX_WIDTH = 1200;
          const MAX_HEIGHT = 1200;
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width;
              width = MAX_WIDTH;
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height;
              height = MAX_HEIGHT;
            }
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          if (!ctx) return;

          // Dibujar imagen
          ctx.drawImage(img, 0, 0, width, height);

          // 3. Estampa pericial con GPS real y timestamp sobre la foto
          const timeStr = new Date().toLocaleString("es-CO");
          const gpsText = gpsCoords 
            ? `${gpsCoords.lat.toFixed(5)}, ${gpsCoords.lng.toFixed(5)}`
            : "Sin señal GPS";
          const watermarkText = `SGMC SISGA • ${gpsText} • ${timeStr}`;

          ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
          ctx.fillRect(10, height - 38, Math.min(width - 20, 480), 28);
          ctx.font = "bold 12px monospace, sans-serif";
          ctx.fillStyle = "#22c55e";
          ctx.fillText(watermarkText, 18, height - 20);

          // 4. Exportar a WebP con calidad 0.82
          const webpData = canvas.toDataURL("image/webp", 0.82);
          const sizeKb = Math.round((webpData.length * (3 / 4)) / 1024);

          const nuevaFoto: FotoEvidencia = {
            id: `FOT-${Date.now()}`,
            base64: webpData,
            descripcion: `Evidencia fotográfica ${fotos.length + 1}`,
            timestamp: new Date().toISOString(),
            sizeKb,
            ubicacion: gpsCoords ? `${gpsCoords.lat.toFixed(6)}, ${gpsCoords.lng.toFixed(6)}` : null
          };

          onAddFoto(nuevaFoto);
          setIsProcessing(false);
          if (fileInputRef.current) fileInputRef.current.value = "";
        };
      };

      reader.readAsDataURL(file);
    } catch (err) {
      console.error("Error al procesar fotografía:", err);
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-3">
      {/* Input de Cámara Nativo Oculto */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileChange}
        className="hidden"
      />

      <div className="flex items-center justify-between">
        <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
          <Camera className="w-4 h-4 text-emerald-400" />
          Evidencias Fotográficas Reales ({fotos.length})
        </label>
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={isProcessing}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-950 transition-all hover:scale-105 disabled:opacity-50"
        >
          {isProcessing ? (
            <span className="animate-spin text-xs">⏳</span>
          ) : (
            <Plus className="w-3.5 h-3.5" />
          )}
          <span>{isProcessing ? "Comprimiendo WebP..." : "Abrir Cámara"}</span>
        </button>
      </div>

      {/* Grid de Fotos Capturadas */}
      {fotos.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {fotos.map((foto, index) => (
            <div
              key={foto.id}
              className="relative group rounded-xl overflow-hidden border border-slate-800 bg-slate-950 aspect-video flex flex-col justify-end"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={foto.base64}
                alt={foto.descripcion}
                className="absolute inset-0 w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-transparent to-transparent pointer-events-none" />
              
              <div className="relative p-2 flex items-center justify-between text-[10px] text-slate-300">
                <span className="truncate max-w-[100px] font-mono text-emerald-400">
                  {foto.sizeKb} KB
                </span>
                <button
                  type="button"
                  onClick={() => onRemoveFoto(foto.id)}
                  className="p-1 rounded-lg bg-rose-600/80 hover:bg-rose-600 text-white transition-colors"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-slate-800 hover:border-emerald-500/50 rounded-2xl p-6 text-center cursor-pointer transition-colors space-y-2 bg-slate-950/40"
        >
          <div className="w-10 h-10 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
            <ImageIcon className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-300">No hay fotografías capturadas</p>
            <p className="text-[11px] text-slate-500">Toca para abrir la cámara nativa del dispositivo</p>
          </div>
        </div>
      )}
    </div>
  );
}
