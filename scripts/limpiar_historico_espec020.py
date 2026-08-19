# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_supabase import conectar

con, _ = conectar()
cur = con.cursor()
cur.execute('UPDATE public."MAN_Mantenimientos" SET "Coordenadas_Cierre_LatLong" = NULL WHERE "CierreConExcepcion" = TRUE;')
con.commit()
print("Filas de mantenimiento con excepcion saneadas a NULL:", cur.rowcount)
cur.close()
con.close()
