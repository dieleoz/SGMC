import Dexie, { Table } from 'dexie';

export interface OrdenTrabajoLocal {
  OTID: string;
  ActivoID: string;
  ActivoNombre: string;
  TipoActivoID: string;
  UnidadFuncionalID: string;
  PK: string;
  Ubicacion_LatLong: string;
  RadioGeofencingKm: number;
  EstadoOrdenID: string;
  FechaProgramada: string;
  TecnicoID: string;
}

export interface MantenimientoEnCola {
  id?: number;
  OTID: string;
  ActivoID: string;
  FechaInicio: string;
  FechaCierre: string;
  Coordenadas_Cierre_LatLong: string | null;
  PrecisionGPSMetros: number | null;
  GeofencingValido: boolean;
  DistanciaMetros: number | null;
  CierreConExcepcion?: boolean;
  MotivoExcepcion?: string | null;
  Observaciones: string;
  ChecklistRespuestas: Record<string, string | boolean | number>;
  Fotografias: Array<{ id: string; base64: string; descripcion: string; timestamp: string }>;
  FirmaBase64: string;
  Sincronizado: boolean;
  TimestampCreacion: string;
}

export interface PreguntaChecklist {
  PreguntaID: string;
  FormularioID: string;
  SeccionID: string;
  SeccionNombre?: string;
  TextoPregunta: string;
  TipoRespuestaID: string;
  TipoRespuesta?: string;
  Obligatoria?: boolean;
  Unidad?: string | null;
  ValorMinimo?: number | null;
  ValorMaximo?: number | null;
  Opciones?: string[];
  Orden: number;
}

export class SGMCLocalDatabase extends Dexie {
  ordenes!: Table<OrdenTrabajoLocal, string>;
  mantenimientosCola!: Table<MantenimientoEnCola, number>;
  preguntas!: Table<PreguntaChecklist, string>;

  constructor() {
    super('SGMC_Offline_DB');
    this.version(1).stores({
      ordenes: 'OTID, ActivoID, TipoActivoID, EstadoOrdenID, TecnicoID',
      mantenimientosCola: '++id, OTID, ActivoID, Sincronizado, TimestampCreacion',
      preguntas: 'PreguntaID, FormularioID, SeccionID',
    });
  }
}

export const dbLocal = new SGMCLocalDatabase();
