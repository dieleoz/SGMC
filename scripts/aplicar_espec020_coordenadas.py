# -*- coding: utf-8 -*-
"""Aplica ESPEC-020: Corrección atómica de Coordenadas de Cierre e Idempotencia.

1. Relaja el NOT NULL en MAN_Mantenimientos.Coordenadas_Cierre_LatLong y FOT_Fotografias.Ubicacion_LatLong.
2. Instala la función fn_actualizar_geom_man() y su trigger.
3. Actualiza public.sgmc_sincronizar_mantenimiento(JSONB) sin coordenadas falsas fabricadas.
4. Prueba la inserción con CierreConExcepcion=True y Coordenadas=NULL (fail-closed y transparente).
5. Prueba idempotencia ante reintentos.
"""

import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    print("=" * 78)
    print("APLICANDO ESPEC-020: CORRECCIÓN ATÓMICA DE COORDENADAS E IDEMPOTENCIA")
    print("=" * 78)

    con, origen = conectar()
    print(f"Conectado a Supabase por: {origen}")
    con.set_session(autocommit=True)
    cur = con.cursor()

    # 1. Relajar NOT NULL
    print("1. Relajando restricciones NOT NULL en MAN_Mantenimientos y FOT_Fotografias...")
    cur.execute('ALTER TABLE public."MAN_Mantenimientos" ALTER COLUMN "Coordenadas_Cierre_LatLong" DROP NOT NULL;')
    cur.execute('ALTER TABLE public."FOT_Fotografias" ALTER COLUMN "Ubicacion_LatLong" DROP NOT NULL;')
    print("   -> OK: Columnas ahora admiten NULL.")

    # 2. Leer y aplicar BD/supabase_sync_rpc.sql
    ruta_rpc = os.path.join(RAIZ, "BD", "supabase_sync_rpc.sql")
    with open(ruta_rpc, "r", encoding="utf-8") as f:
        sql_rpc = f.read()

    print("2. Aplicando nueva RPC sgmc_sincronizar_mantenimiento y triggers geométricos...")
    cur.execute(sql_rpc)
    print("   -> OK: RPC y triggers instalados correctamente.")

    # 3. Probar sincronización con CierreConExcepcion y Coordenadas Nulas
    test_otid = "OT-TEST-ESPEC020"
    print(f"3. Probando sincronización para {test_otid} con Coordenadas_Cierre_LatLong=NULL y CierreConExcepcion=True...")
    
    # Limpiar prueba anterior si existía
    cur.execute('DELETE FROM public."CHD_ChecklistDetalle" WHERE "ChecklistID" IN (SELECT "ChecklistID" FROM public."CHK_Checklists" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s));', (test_otid,))
    cur.execute('DELETE FROM public."CHK_Checklists" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."FOT_Fotografias" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."FIR_Firmas" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."MAN_Mantenimientos" WHERE "OTID" = %s;', (test_otid,))
    cur.execute('DELETE FROM public."OT_OrdenesTrabajo" WHERE "OTID" = %s;', (test_otid,))

    payload = {
        "OTID": test_otid,
        "ActivoID": "ACT-0001",
        "FechaInicio": "2026-08-19T10:00:00Z",
        "FechaCierre": "2026-08-19T10:30:00Z",
        "Coordenadas_Cierre_LatLong": None,
        "CierreConExcepcion": True,
        "MotivoExcepcion": "Túnel sin cobertura GPS. Prueba técnica ESPEC-020.",
        "Observaciones": "Cierre con excepción verificado",
        "ChecklistRespuestas": {},
        "Fotografias": [
            {
                "id": "FOT-TEST-001",
                "tipo": "Despues",
                "base64": "data:image/webp;base64,UklGRg...",
                "ubicacion": None,
                "timestamp": "2026-08-19T10:25:00Z"
            }
        ],
        "FirmaBase64": "data:image/png;base64,iVBORw0KGgo..."
    }

    cur.execute("SELECT public.sgmc_sincronizar_mantenimiento(%s::jsonb);", (json.dumps(payload),))
    res1 = cur.fetchone()[0]
    print("   -> Resultado Inserción 1:", json.dumps(res1, indent=2))
    assert res1.get("exito") is True, f"Fallo la sincronización con coordenadas nulas: {res1}"

    # Verificar que el mantenimiento fue insertado con Coordenadas_Cierre_LatLong = NULL
    cur.execute('SELECT "MantenimientoID", "Coordenadas_Cierre_LatLong", "CierreConExcepcion", "MotivoExcepcion", "geom" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s;', (test_otid,))
    fila = cur.fetchone()
    print("   -> Fila en MAN_Mantenimientos:", fila)
    assert fila[1] is None, "ERROR: Coordenadas_Cierre_LatLong debió ser NULL, pero tiene valor fabricado!"
    assert fila[2] is True, "ERROR: CierreConExcepcion debió ser True"
    assert fila[4] is None, "ERROR: geom debió ser NULL cuando no hay coordenadas"

    # 4. Probar Idempotencia (segundo envío con el mismo OTID)
    print("4. Probando Idempotencia (reintento del mismo payload)...")
    cur.execute("SELECT public.sgmc_sincronizar_mantenimiento(%s::jsonb);", (json.dumps(payload),))
    res2 = cur.fetchone()[0]
    print("   -> Resultado Inserción 2:", json.dumps(res2, indent=2))
    assert res2.get("exito") is True, f"Fallo la prueba de idempotencia: {res2}"
    assert res2.get("mantenimiento_id") == res1.get("mantenimiento_id"), "ERROR: Devolvió un MantenimientoID distinto!"

    # Contar filas en MAN_Mantenimientos para esta OT (debe ser exactamente 1)
    cur.execute('SELECT count(*) FROM public."MAN_Mantenimientos" WHERE "OTID" = %s;', (test_otid,))
    count = cur.fetchone()[0]
    print(f"   -> Filas en MAN_Mantenimientos para {test_otid}: {count}")
    assert count == 1, f"ERROR: Se crearon {count} filas en lugar de 1 sola!"

    # Limpiar registro de prueba
    cur.execute('DELETE FROM public."CHD_ChecklistDetalle" WHERE "ChecklistID" IN (SELECT "ChecklistID" FROM public."CHK_Checklists" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s));', (test_otid,))
    cur.execute('DELETE FROM public."CHK_Checklists" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."FOT_Fotografias" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."FIR_Firmas" WHERE "MantenimientoID" IN (SELECT "MantenimientoID" FROM public."MAN_Mantenimientos" WHERE "OTID" = %s);', (test_otid,))
    cur.execute('DELETE FROM public."MAN_Mantenimientos" WHERE "OTID" = %s;', (test_otid,))
    cur.execute('DELETE FROM public."OT_OrdenesTrabajo" WHERE "OTID" = %s;', (test_otid,))

    cur.close()
    con.close()

    print("\n" + "=" * 78)
    print("ESPEC-020 APLICADA Y VALIDADA CON ÉXITO: 0 FALLOS")
    print("=" * 78)

if __name__ == "__main__":
    main()
