# -*- coding: utf-8 -*-
"""Calcula la capacidad y el crecimiento del SGMC sobre AppSheet + Google Sheets.

Existe para que las cifras de CAPACIDAD_Y_OPERACION_SGMC.md sean reproducibles y
no una estimacion de sobremesa. Ajusta los supuestos de arriba y vuelve a correr.

Limites de plataforma (verificados 2026-08-06):
  - Google Sheets: 10.000.000 de celdas por documento.
  - AppSheet guarda las imagenes en una carpeta contigua a la hoja, en el Drive
    del PROPIETARIO. Cuenta contra su cuota, no contra la de quien las sube.
  - Cuenta personal de Gmail: 15 GB compartidos con Gmail y Fotos.
"""

# ------------------------------------------------------------------ supuestos
ESCENARIOS = {
    "Hoy": dict(activos=34, mantenimientos_activo_anio=12),
    "Inventario real estimado": dict(activos=150, mantenimientos_activo_anio=12),
    "Corredor completo": dict(activos=500, mantenimientos_activo_anio=12),
}

FOTOS_POR_MANTENIMIENTO = 4          # supuesto D-10: minimo 3, maximo 6
KB_POR_FOTO = 120                    # JPEG de 600 px, calidad baja de AppSheet
KB_POR_FIRMA = 20
KB_POR_PDF = 250                     # informe adjunto del bot de alerta
PCT_CORRECTIVO = 0.20                # ordenes correctivas sobre las preventivas
PREGUNTAS_POR_CHECKLIST = 15
RETENCION_ANIOS = 5                  # supuesto D-14

LIMITE_CELDAS = 10_000_000
CUOTA_GB_PERSONAL = 15
UMBRAL_FILAS_SYNC = 50_000           # a partir de aqui la sincronizacion se degrada

# Columnas por tabla que crecen con la operacion
COLUMNAS = {
    "OT_OrdenesTrabajo": 12,
    "MAN_Mantenimientos": 21,
    "CHK_Checklists": 7,
    "CHD_ChecklistDetalle": 9,
    "FOT_Fotografias": 6,
    "FIR_Firmas": 5,
}


def calcular(activos, mantenimientos_activo_anio):
    mtto = int(activos * mantenimientos_activo_anio * (1 + PCT_CORRECTIVO))
    filas = {
        "OT_OrdenesTrabajo": mtto,
        "MAN_Mantenimientos": mtto,
        "CHK_Checklists": mtto,
        "CHD_ChecklistDetalle": mtto * PREGUNTAS_POR_CHECKLIST,
        "FOT_Fotografias": mtto * FOTOS_POR_MANTENIMIENTO,
        "FIR_Firmas": mtto,
    }
    celdas = sum(filas[t] * COLUMNAS[t] for t in filas)
    kb = mtto * (FOTOS_POR_MANTENIMIENTO * KB_POR_FOTO + KB_POR_FIRMA + KB_POR_PDF * 0.15)
    return mtto, filas, celdas, kb / (1024 * 1024)   # GB


print("=" * 92)
print("CAPACIDAD Y CRECIMIENTO — SGMC sobre AppSheet + Google Sheets")
print("=" * 92)
print(f"Supuestos: {FOTOS_POR_MANTENIMIENTO} fotos de {KB_POR_FOTO} KB por mantenimiento, "
      f"{PREGUNTAS_POR_CHECKLIST} preguntas por checklist,")
print(f"           {int(PCT_CORRECTIVO*100)}% de correctivos, retencion de {RETENCION_ANIOS} anios.")
print()

for nombre, e in ESCENARIOS.items():
    mtto, filas, celdas, gb = calcular(**e)
    print("-" * 92)
    print(f"{nombre}: {e['activos']} activos  ->  {mtto:,} mantenimientos al anio")
    print()
    print(f"  {'Tabla':<24} {'filas/anio':>12} {'filas a 5 anios':>18} {'celdas a 5 anios':>18}")
    for t, f in sorted(filas.items(), key=lambda x: -x[1]):
        f5 = f * RETENCION_ANIOS
        alerta = "  <-- degrada sync" if f5 > UMBRAL_FILAS_SYNC else ""
        print(f"  {t:<24} {f:>12,} {f5:>18,} {f5*COLUMNAS[t]:>18,}{alerta}")
    c5 = celdas * RETENCION_ANIOS
    print()
    print(f"  Celdas a {RETENCION_ANIOS} anios : {c5:>14,}  ({c5/LIMITE_CELDAS:.1%} del limite de 10M)")
    print(f"  Almacenamiento    : {gb:>14.2f} GB/anio   -> {gb*RETENCION_ANIOS:.2f} GB a {RETENCION_ANIOS} anios")
    print(f"  Cuota personal    : {gb*RETENCION_ANIOS/CUOTA_GB_PERSONAL:>13.0%} de los 15 GB de una cuenta Gmail")
    anios_hasta_cuota = CUOTA_GB_PERSONAL / gb if gb else 999
    print(f"  Se agota la cuota en {anios_hasta_cuota:.1f} anios "
          f"{'*** ANTES DE LA RETENCION EXIGIDA ***' if anios_hasta_cuota < RETENCION_ANIOS else ''}")
    print()

print("=" * 92)
print("CONCLUSIONES")
print("=" * 92)
print("1. El limite de 10 millones de celdas NO es la restriccion. Se agota antes la")
print("   sincronizacion: AppSheet se degrada por encima de ~50.000 filas por tabla, y la")
print("   tabla critica es CHD_ChecklistDetalle, que multiplica por 15 cada mantenimiento.")
print("2. La restriccion real es el ALMACENAMIENTO, y no por el volumen sino por DONDE vive:")
print("   las fotografias cuentan contra la cuota del propietario del documento, que hoy es")
print("   una cuenta personal de Gmail con 15 GB compartidos con su correo y sus fotos.")
print("3. Mitigaciones, en orden de urgencia:")
print("   a. Trasladar la propiedad a una cuenta corporativa. Resuelve el problema de raiz.")
print("   b. Archivar por anio: mover los mantenimientos cerrados a una hoja historica.")
print("   c. Bajar a 3 fotografias obligatorias reduce el almacenamiento un 25%.")
