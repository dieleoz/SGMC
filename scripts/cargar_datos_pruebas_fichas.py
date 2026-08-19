# -*- coding: utf-8 -*-
"""
Carga masiva de datos de prueba periciales para las 27 Fichas Técnicas del SGMC v2.
Inserta mantenimientos cerrados con mediciones exactas (voltajes, frecuencias, potencias,
respuestas de checklist dinámico, fotos WebP y firmas) en PostgreSQL / Supabase.
"""

import os
import sys
import json
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_supabase import conectar

VALORES_PRUEBA_POR_FICHA = {
    "FRM_SOS": {
        "1. Tensión de batería DC": "12.8",
        "2. Tensión panel solar circuito abierto": "19.5",
        "3. Prueba de audio Full-Duplex CCO": "Conforme",
        "4. Hermeticidad de gabinete IP66": "Conforme",
        "5. Fijación y anclaje mecánico": "Conforme"
    },
    "FRM_CCTV": {
        "1. Tensión PoE+ (Inyector)": "52.0",
        "2. Flujo RTSP 1080p hacia CCO": "Conforme",
        "3. Movimiento PTZ 360 y presets": "Conforme",
        "4. Iluminador Infrarrojo": "Conforme",
        "5. Limpieza de domo y óptica": "Conforme"
    },
    "FRM_PMVF": {
        "1. Tensión de alimentación AC": "218.0",
        "2. Tensión banco DC": "24.2",
        "3. Conmutación de píxeles LED": "Conforme",
        "4. Enlace protocolo NTCIP": "Conforme",
        "5. Sensor de brillo / fotocelda": "Conforme"
    },
    "FRM_GENE": {
        "1. Nivel diésel en tanque (%)": "88.0",
        "2. Tensión batería de arranque DC": "26.4",
        "3. Frecuencia de salida generada": "60.1",
        "4. Tensión trifásica generada": "219.0",
        "5. Prueba de conmutación ATS": "Conforme"
    },
    "FRM_UPS": {
        "1. Tensión total banco DC": "242.0",
        "2. Tensión media por celda": "2.27",
        "3. Autonomía estimada descarga": "145.0",
        "4. Temperatura gabinete UPS": "22.5",
        "5. Estado general de baterías": "Conforme"
    },
    "FRM_SUBE": {
        "1. Resistencia puesta a tierra (Ohm)": "2.1",
        "2. Nivel de aislamiento general": "1450.0",
        "3. Inspección termográfica bornes": "Conforme",
        "4. Nivel aceite transformador": "Conforme"
    },
    "FRM_FO": {
        "1. Atenuación media 1550nm (dB/km)": "0.21",
        "2. Pérdida por empalme (dB)": "0.03",
        "3. Continuidad de hilos de fibra": "Conforme",
        "4. Limpieza de conectores ópticos": "Conforme"
    },
    "FRM_PEAJE": {
        "1. Tiempo apertura barrera (segundos)": "0.95",
        "2. Lectura antena Telepeaje TAG RFID": "Conforme",
        "3. Semáforo de carril Rojo/Verde": "Conforme",
        "4. Sensores de lazo inductivo": "Conforme"
    }
}

def ejecutar_carga():
    con, _ = conectar()
    con.set_session(autocommit=True)
    cur = con.cursor()

    print("=" * 80)
    print("CARGA DE DATOS DE PRUEBA PERICIALES PARA LAS 27 FICHAS TÉCNICAS")
    print("=" * 80)

    cur.execute('SELECT "FormularioID", "Nombre" FROM public."FRM_Formularios" ORDER BY "FormularioID";')
    formularios = cur.fetchall()

    total_cargados = 0

    for form_id, form_nombre in formularios:
        cur.execute('''
            SELECT a."ActivoID", a."Nombre", a."UnidadFuncionalID", a."Ubicacion_LatLong", a."PK"
            FROM public."ACT_Activos" a
            JOIN public."TIP_TiposActivo" t ON a."TipoActivoID" = t."TipoActivoID"
            WHERE t."FormularioID" = %s
            LIMIT 1;
        ''', (form_id,))
        activo_row = cur.fetchone()

        if not activo_row:
            cur.execute('SELECT "ActivoID", "Nombre", "UnidadFuncionalID", "Ubicacion_LatLong", "PK" FROM public."ACT_Activos" LIMIT 1;')
            activo_row = cur.fetchone()

        activo_id, activo_nombre, uf_id, coords, pk = activo_row

        cur.execute('''
            SELECT "PreguntaID", "Pregunta", "TipoRespuestaID", "Unidad"
            FROM public."FRM_Preguntas"
            WHERE "FormularioID" = %s
            ORDER BY "Orden";
        ''', (form_id,))
        preguntas = cur.fetchall()

        clean_form_id = form_id.replace('FRM_', '')
        ot_id = f"OT-PRUEBA-FICHA-{clean_form_id}"
        man_id = f"MAN-PRUEBA-FICHA-{clean_form_id}"
        chk_id = f"CHK-PRUEBA-FICHA-{clean_form_id}"
        now_iso = datetime.now(timezone.utc).isoformat()
        cierre_coords = coords if coords else "4.851230, -73.521100"

        # 1. Crear / Actualizar OT
        cur.execute('''
            INSERT INTO public."OT_OrdenesTrabajo" 
            ("OTID", "ActivoID", "Tipo", "EstadoOrdenID", "FechaProgramada", "SupervisorID", "TecnicoID")
            VALUES (%s, %s, 'Preventivo', 'Cerrada', %s, 'USR-006', 'USR-002')
            ON CONFLICT ("OTID") DO UPDATE 
            SET "EstadoOrdenID" = 'Cerrada';
        ''', (ot_id, activo_id, now_iso[:10]))

        # 2. Crear Mantenimiento
        cur.execute('''
            INSERT INTO public."MAN_Mantenimientos"
            ("MantenimientoID", "OTID", "TecnicoID", "EstadoActivoID", "FechaHoraInicio", "FechaHoraFin", "Coordenadas_Cierre_LatLong", "CierreConExcepcion", "Observaciones", "AprobadoSupervisor", "FechaAprobacion")
            VALUES (%s, %s, 'USR-002', 'EST-01', %s, %s, %s, FALSE, %s, TRUE, %s)
            ON CONFLICT ("MantenimientoID") DO UPDATE
            SET "FechaHoraFin" = %s, "Coordenadas_Cierre_LatLong" = %s, "AprobadoSupervisor" = TRUE;
        ''', (man_id, ot_id, now_iso, now_iso, cierre_coords, f"Inspección pericial conforme según ficha {form_id} ({form_nombre}) sobre {activo_nombre}.", now_iso, now_iso, cierre_coords))

        # 3. Crear Checklist en CHK_Checklists
        cur.execute('''
            INSERT INTO public."CHK_Checklists" 
            ("ChecklistID", "MantenimientoID", "FormularioID", "VersionFormulario", "Finalizado")
            VALUES (%s, %s, %s, 1, TRUE)
            ON CONFLICT ("ChecklistID") DO NOTHING;
        ''', (chk_id, man_id, form_id))

        # 4. Poblar respuestas tipadas en CHD_ChecklistDetalle
        respuestas_custom = VALORES_PRUEBA_POR_FICHA.get(form_id, {})
        
        for preg_id, texto_preg, tipo_resp, unidad in preguntas:
            val_texto = "Conforme"
            val_num = None
            val_bool = True

            for k, v in respuestas_custom.items():
                if any(word in texto_preg.lower() for word in k.lower().split()[:2]):
                    val_texto = v
                    try:
                        val_num = float(v)
                    except ValueError:
                        pass
                    break

            if tipo_resp == "TPR-03" and val_num is None:
                val_num = 12.5
                val_texto = "12.5"

            detalle_id = f"CHD-PRF-{clean_form_id}-{preg_id.replace('PRG-', '')}"

            cur.execute('''
                INSERT INTO public."CHD_ChecklistDetalle"
                ("DetalleID", "ChecklistID", "PreguntaID", "RespuestaTexto", "RespuestaNumero", "RespuestaBoolean", "Contestada")
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                ON CONFLICT ("DetalleID") DO NOTHING;
            ''', (detalle_id, chk_id, preg_id, val_texto, val_num, val_bool))

        # 5. Insertar 2 Fotos Periciales en FOT_Fotografias
        cur.execute('''
            INSERT INTO public."FOT_Fotografias"
            ("FotoID", "MantenimientoID", "Tipo", "Archivo", "Ubicacion_LatLong", "FechaHora", "Usuario")
            VALUES 
            (%s, %s, 'Antes', %s, %s, %s, 'USR-002'),
            (%s, %s, 'Despues', %s, %s, %s, 'USR-002')
            ON CONFLICT ("FotoID") DO NOTHING;
        ''', (
            f"FOT-PRF-{clean_form_id}-1", man_id, f"https://evidencias.sgmc.co/{form_id}_antes.webp", cierre_coords, now_iso,
            f"FOT-PRF-{clean_form_id}-2", man_id, f"https://evidencias.sgmc.co/{form_id}_despues.webp", cierre_coords, now_iso
        ))

        # 6. Insertar Firma Digital en FIR_Firmas
        cur.execute('''
            INSERT INTO public."FIR_Firmas"
            ("FirmaID", "MantenimientoID", "TipoFirma", "Imagen", "FechaHora")
            VALUES (%s, %s, 'Tecnico', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK8AAAA8CAYAAAC0z...', %s)
            ON CONFLICT ("FirmaID") DO NOTHING;
        ''', (f"FIR-PRF-{clean_form_id}", man_id, now_iso))

        total_cargados += 1
        print(f"[{total_cargados:02d}/27] [OK] Ficha {form_id:<10} -> {activo_nombre} (PK {pk} - {uf_id}) poblada con mediciones periciales.")

    print("=" * 80)
    print(f"CARGA FINALIZADA CON ÉXITO: {total_cargados} de 27 FICHAS TÉCNICAS POBLADAS.")
    print("=" * 80)

    cur.close()
    con.close()

if __name__ == "__main__":
    ejecutar_carga()
