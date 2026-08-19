# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_supabase import conectar

con, _ = conectar()
cur = con.cursor()

cur.execute("""
SELECT f."FormularioID", f."Nombre", count(p."PreguntaID") as "TotalPreguntas"
FROM public."FRM_Formularios" f
LEFT JOIN public."FRM_Preguntas" p ON f."FormularioID" = p."FormularioID"
GROUP BY f."FormularioID", f."Nombre"
ORDER BY f."FormularioID";
""")
rows = cur.fetchall()
print("=" * 80)
print(f"{'CÓDIGO':<12} | {'NOMBRE DEL FORMULARIO':<50} | {'PREGUNTAS'}")
print("=" * 80)
for r in rows:
    print(f"{r[0]:<12} | {r[1]:<50} | {r[2]}")
print("=" * 80)

cur.close()
con.close()
