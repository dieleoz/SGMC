# -*- coding: utf-8 -*-
"""Aplica y prueba los procedimientos de base de datos de la Fase 5:
1. sgmc_reportar_novedad (ESPEC-016)
2. sgmc_generar_plan_mensual (ESPEC-017)
3. sgmc_calcular_disponibilidad (ESPEC-021)
"""

import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    print("=" * 78)
    print("APLICANDO Y VERIFICANDO RPCS DE FASE 5 (NOVEDADES, PLANES, DISPONIBILIDAD)")
    print("=" * 78)

    con, origen = conectar()
    print(f"Conectado a Supabase por: {origen}\n")
    con.set_session(autocommit=True)
    cur = con.cursor()

    # 1. Aplicar SQL
    sql_path = os.path.join(RAIZ, "BD", "supabase_fase5_rpc.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    
    print("1. Ejecutando BD/supabase_fase5_rpc.sql...")
    cur.execute(sql)
    print("   -> OK: Procedimientos creados en Supabase.")

    # 2. Probar sgmc_reportar_novedad con un ActivoID real
    print("\n2. Probando reporte de novedad y generación automática de OT correctiva...")
    cur.execute('SELECT "ActivoID", "Nombre" FROM public."ACT_Activos" WHERE "UnidadFuncionalID" = \'UNF-01\' LIMIT 1;')
    activo_real, activo_nombre = cur.fetchone()
    print(f"   • Usando activo real de prueba: {activo_real} ({activo_nombre})")

    payload_novedad = json.dumps({
        "NovedadID": "NOV-TEST-001",
        "UsuarioID": "USR-004",
        "Tipo": "Falla detectada",
        "Descripcion": f"Falla detectada en prueba pericial para {activo_nombre}",
        "Ubicacion_LatLong": "4.851230, -73.521100",
        "Fotografia": "https://placeholder.sgmc.co/sos-test.webp",
        "ActivoID": activo_real,
        "GeneraOT": True
    })
    cur.execute("SELECT public.sgmc_reportar_novedad(%s::jsonb);", (payload_novedad,))
    res_nov = cur.fetchone()[0]
    print(f"   • Resultado Novedad: {res_nov}")
    assert res_nov.get("exito") is True, f"Fallo al reportar novedad: {res_nov}"

    # 3. Probar sgmc_generar_plan_mensual para Septiembre 2026 en UF1
    print("\n3. Probando generación de Plan Preventivo Mensual (PLA) para UF1...")
    cur.execute("SELECT public.sgmc_generar_plan_mensual(2026, 9, 'UNF-01');")
    res_plan = cur.fetchone()[0]
    print(f"   • Resultado Plan: {res_plan}")
    assert res_plan.get("exito") is True, f"Fallo al generar plan: {res_plan}"

    # 4. Probar sgmc_calcular_disponibilidad
    print("\n4. Probando cálculo de Disponibilidad Contractual ($D_i$)...")
    cur.execute("SELECT * FROM public.sgmc_calcular_disponibilidad(2026, 8) LIMIT 5;")
    rows_disp = cur.fetchall()
    print("   • Primeros 5 subsistemas analizados:")
    for r in rows_disp:
        print(f"     - {r[0]} ({r[1]} - {r[2]}): {r[3]} activos | Disp: {r[6]}% | Meta: {'CUMPLE' if r[7] else 'NO CUMPLE'}")

    cur.close()
    con.close()

    print("\n" + "=" * 78)
    print("TODAS LAS PRUEBAS DE PROCEDIMIENTOS DE FASE 5 PASARON EXITOSAMENTE (0 FALLOS)")
    print("=" * 78)

if __name__ == "__main__":
    main()
