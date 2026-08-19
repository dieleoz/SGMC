import { dbLocal, MantenimientoEnCola } from "./db-offline";
import { supabase } from "./supabase";
import { subirFotoEvidencia, subirFirmaDigital } from "./storage-service";

export interface SyncStatusResult {
  totalPendientes: number;
  sincronizados: number;
  fallidos: number;
  enProgreso: boolean;
}

class SyncEngine {
  private isSyncing = false;

  constructor() {
    if (typeof window !== "undefined") {
      window.addEventListener("online", () => {
        console.log("[SyncEngine] Red recuperada. Disparando sincronización automática...");
        this.sincronizarCola();
      });
    }
  }

  /**
   * Procesa la cola de mantenimientos pendientes en IndexedDB,
   * subiendo primero fotos y firmas a Supabase Storage (evidencias-sgmc)
   * y asentando atómicamente la ejecución en PostgreSQL.
   */
  async sincronizarCola(): Promise<SyncStatusResult> {
    if (this.isSyncing) {
      return { totalPendientes: 0, sincronizados: 0, fallidos: 0, enProgreso: true };
    }

    if (typeof navigator !== "undefined" && !navigator.onLine) {
      console.warn("[SyncEngine] Sin conexión a internet. Sincronización omitida.");
      return { totalPendientes: 0, sincronizados: 0, fallidos: 0, enProgreso: false };
    }

    this.isSyncing = true;
    let sincronizados = 0;
    let fallidos = 0;

    try {
      const pendientes = await dbLocal.mantenimientosCola
        .filter((m) => !m.Sincronizado)
        .toArray();

      console.log(`[SyncEngine] Procesando ${pendientes.length} mantenimientos encolados...`);

      for (const item of pendientes) {
        try {
          // 1. Subir Fotografías a Supabase Storage
          const fotosProcesadas = [];
          for (const foto of item.Fotografias || []) {
            let urlPublica = foto.base64;
            if (foto.base64 && foto.base64.startsWith("data:image/")) {
              const uploadedUrl = await subirFotoEvidencia(foto.base64, item.OTID, foto.id);
              if (uploadedUrl) {
                urlPublica = uploadedUrl;
              }
            }

            fotosProcesadas.push({
              id: foto.id,
              url: urlPublica,
              descripcion: foto.descripcion,
              timestamp: foto.timestamp,
              ubicacion: (foto as any).ubicacion || null,
            });
          }

          // 2. Subir Firma Digital a Supabase Storage
          let firmaUrl = item.FirmaBase64;
          if (item.FirmaBase64 && item.FirmaBase64.startsWith("data:image/")) {
            const uploadedFirmaUrl = await subirFirmaDigital(item.FirmaBase64, item.OTID);
            if (uploadedFirmaUrl) {
              firmaUrl = uploadedFirmaUrl;
            }
          }

          // 3. Construir Payload Atómico para Supabase RPC
          const payload = {
            OTID: item.OTID,
            ActivoID: item.ActivoID,
            FechaInicio: item.FechaInicio,
            FechaCierre: item.FechaCierre,
            Coordenadas_Cierre_LatLong: item.Coordenadas_Cierre_LatLong,
            CierreConExcepcion: item.CierreConExcepcion || false,
            MotivoExcepcion: item.MotivoExcepcion || null,
            Observaciones: item.Observaciones || "",
            ChecklistRespuestas: item.ChecklistRespuestas || {},
            Fotografias: fotosProcesadas,
            FirmaBase64: firmaUrl || null,
          };

          // 4. Invocar RPC atómica en Supabase
          const { data, error } = await supabase.rpc("sgmc_sincronizar_mantenimiento", {
            p_payload: payload,
          });

          if (error) {
            console.error(`[SyncEngine] Error RPC en OT ${item.OTID}:`, error);
            fallidos++;
            continue;
          }

          if (data && data.exito) {
            console.log(`[SyncEngine] OT ${item.OTID} sincronizada exitosamente con Storage:`, data);
            if (item.id) {
              await dbLocal.mantenimientosCola.update(item.id, { Sincronizado: true });
            }
            sincronizados++;
          } else {
            console.warn(`[SyncEngine] Respuesta de fallo en OT ${item.OTID}:`, data);
            fallidos++;
          }
        } catch (err) {
          console.error(`[SyncEngine] Excepción procesando OT ${item.OTID}:`, err);
          fallidos++;
        }
      }

      return {
        totalPendientes: pendientes.length,
        sincronizados,
        fallidos,
        enProgreso: false,
      };
    } finally {
      this.isSyncing = false;
    }
  }
}

export const syncEngine = new SyncEngine();
