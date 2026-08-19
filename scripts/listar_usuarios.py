# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_supabase import conectar

con, _ = conectar()
cur = con.cursor()
cur.execute('SELECT "RolID", "Nombre", "Descripcion" FROM public."ROL_Roles";')
print(cur.fetchall())
cur.close()
con.close()
