/**
 * SGMC — Fase A del cableado de referencias.
 *
 * Aplica sobre el Google Sheets de produccion todo lo que se puede hacer sin
 * abrir el editor de AppSheet: renombrados, columnas nuevas, tablas nuevas,
 * catalogos, datos de prueba y limpieza.
 *
 * Especificacion: docs/sdd/ESPEC-001-preparacion-del-sheets.md
 * Modelo objetivo: scripts/modelo_objetivo.py  (RENOMBRADOS, RETIPADOS)
 *
 * COMO SE USA
 *   1. Con DRY_RUN = true (por defecto), ejecutar main(). NO escribe nada:
 *      solo informa que haria. Leer el registro de ejecucion.
 *   2. Si el informe cuadra, cambiar DRY_RUN a false y volver a ejecutar.
 *   3. Copiar el registro final al acta.
 *
 * ANTES DE PONER DRY_RUN EN false
 *   Debe existir el respaldo. Ya se creo el 2026-08-07:
 *   SGMC_backup_2026-08-07_antes_cableado_FaseA
 *
 * LO QUE ESTE SCRIPT NO HACE, A PROPOSITO
 *   - No borra ninguna columna. Retirar campos es de otra pasada, con datos
 *     ya migrados. Borrar es lo unico que el respaldo no vuelve gratis.
 *   - No toca ACT_Activos.Ubicacion: las coordenadas reales son D-01, trabajo
 *     de campo.
 *   - No entra al editor de AppSheet. Eso es la Fase B.
 */

// ============================================================ CONFIGURACION

/** En true no escribe nada: solo informa. Empieza SIEMPRE asi. */
var DRY_RUN = true;

/** Identificador del Sheets de produccion. Se comprueba antes de tocar nada. */
var ID_ESPERADO = '1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc';

// ================================================================ RENOMBRADOS
//
// Verificados el 2026-08-07 leyendo produccion con el conector de Drive.
// El orden dentro de OT_OrdenesTrabajo importa: 'Activo' se renombra a
// 'ActivoID' antes de que se cree la bandera 'Activo', que reutiliza el nombre.

var RENOMBRADOS = {
  'OT_OrdenesTrabajo': [
    ['Activo',            'ActivoID'],
    ['Numero_OT',         'OTID'],
    ['Tecnico',           'TecnicoID'],
    ['SupervidorID',      'SupervisorID'],
    ['Fecha Programada',  'FechaProgramada'],
    ['Estado',            'EstadoOrdenID'],
    ['Fecha_Cierre',      'FechaCierre'],
    ['Cerrada_Por',       'CerradaPor']
  ],
  'MAN_Mantenimientos': [
    ['MttoID',                  'MantenimientoID'],
    ['Tecnico_Asignado',        'TecnicoID'],
    ['Fecha_Hora_Inicio',       'FechaHoraInicio'],
    ['Fecha_Hora_Fin',          'FechaHoraFin'],
    ['Requiere_Segunda_Visita', 'RequiereSegundaVisita'],
    ['Motivo_Pendiente',        'MotivoPendienteID'],
    ['Aprobado_Supervisor',     'AprobadoSupervisor'],
    ['Usuario_Registro',        'UsuarioRegistro'],
    ['Fecha_Hora_Registro',     'FechaHoraRegistro']
  ],
  'ACT_Activos': [
    ['EstadoID', 'EstadoActivoID'],
    ['SedeID',   'UnidadFuncionalID']
  ],
  'USR_Usuarios': [
    ['usuarioID', 'UsuarioID'],
    ['Estado',    'Activo']
  ],
  'EST_Activo': [
    ['EstadoID', 'EstadoActivoID']
  ],
  'CHK_Checklists': [
    ['OTID', 'MantenimientoID']
  ],
  'CHD_ChecklistDetalle': [
    ['Observaciones', 'Observacion']
  ]
};

// ============================================================ COLUMNAS NUEVAS

var COLUMNAS_NUEVAS = {
  'OT_OrdenesTrabajo': ['OTOrigenID', 'Activo'],
  'MAN_Mantenimientos': [
    'OrigenApertura', 'UbicacionEscaneo', 'FechaHoraEscaneo', 'EstadoActivoID',
    'CierreConExcepcion', 'MotivoExcepcion', 'ModoFallaID', 'FechaAprobacion',
    'ObservacionRechazo'
  ],
  'TIP_TiposActivo': ['RadioGeofencingKm'],
  'CHK_Checklists':  ['VersionFormulario'],
  'EST_Activo':      ['GeneraAlerta', 'Activo']
};

// ============================================================== TABLAS NUEVAS
//
// Las claves de UNF_UnidadesFuncionales son 7 a 10 A PROPOSITO: es lo que hoy
// guarda ACT_Activos.SedeID, que pasa a llamarse UnidadFuncionalID. Reutilizar
// esos identificadores hace que las 34 filas de activos sigan resolviendo sin
// tocar ni una. Cambiarlos obligaria a reescribir las 34.
//
// Lo mismo con EOT_EstadosOrden: la clave es el propio nombre del estado,
// porque OT_OrdenesTrabajo.Estado ya guarda 'Asignada', 'Cerrada' y
// 'Suspendida'. Asi las 6 ordenes existentes resuelven sin migracion.

var TABLAS_NUEVAS = {
  'UNF_UnidadesFuncionales': {
    encabezados: ['UnidadFuncionalID', 'Nombre', 'PRInicial', 'PRFinal', 'Activo'],
    filas: [
      [7,  'UF1', '', '', true],
      [8,  'UF2', '', '', true],
      [9,  'UF3', '', '', true],
      [10, 'UF4', '', '', true]
    ]
  },
  'EOT_EstadosOrden': {
    encabezados: ['EstadoOrdenID', 'Nombre', 'Orden', 'QuienCambia', 'EsFinal', 'Activo'],
    filas: [
      ['Programada',   'Programada',   1, 'Sistema',    false, true],
      ['Asignada',     'Asignada',     2, 'Supervisor', false, true],
      ['En ejecucion', 'En ejecucion', 3, 'Tecnico',    false, true],
      ['En revision',  'En revision',  4, 'Tecnico',    false, true],
      ['Cerrada',      'Cerrada',      5, 'Supervisor', true,  true],
      ['Suspendida',   'Suspendida',   6, 'Supervisor', false, true],
      ['Vencida',      'Vencida',      7, 'Sistema',    false, true]
    ]
  },
  'MOT_MotivosPendiente': {
    encabezados: ['MotivoPendienteID', 'Nombre', 'GeneraSeguimiento', 'Activo'],
    filas: [
      ['MOT-01', 'Falta de repuesto',     true, true],
      ['MOT-02', 'Clima',                 true, true],
      ['MOT-03', 'Acceso restringido',    true, true],
      ['MOT-04', 'Riesgo para el tecnico', true, true],
      ['MOT-05', 'Requiere especialista', true, true]
    ]
  },
  'ASG_AsignacionZona': {
    encabezados: ['AsignacionID', 'UsuarioID', 'UnidadFuncionalID', 'Activo'],
    // Tecnicos reales (RolID 4) contra las cuatro unidades funcionales.
    // Sin estas filas el Security Filter de la Fase B deja a todos en cero.
    filas: [
      ['ASG-01', 3, 7,  true],
      ['ASG-02', 4, 8,  true],
      ['ASG-03', 5, 9,  true],
      ['ASG-04', 6, 10, true]
    ]
  },
  'FAL_ModosFalla': {
    encabezados: ['ModoFallaID', 'TipoActivoID', 'Nombre', 'Componente', 'Criticidad', 'Activo'],
    filas: []   // Requiere criterio de mantenimiento. Se puebla en otro frente.
  },
  'NOV_Novedades': {
    encabezados: ['NovedadID', 'UsuarioID', 'Tipo', 'Descripcion', 'Ubicacion',
                  'Fotografia', 'ActivoID', 'Estado', 'FechaHora'],
    filas: []
  },
  'PLA_PlanMantenimiento': {
    encabezados: ['PlanID', 'ActivoID', 'FrecuenciaID', 'UltimaEjecucion',
                  'ProximaFecha', 'ResponsableID', 'Activo'],
    filas: []
  }
};

// ============================================================ DATOS DE PRUEBA
//
// Prefijo TEST- obligatorio, y el borrado esta en este mismo archivo:
// ejecutar borrarDatosDePrueba() cuando ya no hagan falta.
//
// OTID vale 'OT-0001' y no '1'. Escribirlas con la forma final es lo que
// impide que la conversion a Ref de la Fase B las deje huerfanas.

var PREFIJO_PRUEBA = 'TEST-';

var DATOS_PRUEBA = {
  'MAN_Mantenimientos': [
    { MantenimientoID: 'TEST-MTTO-001', OTID: 'OT-0001', TecnicoID: 4,
      OrigenApertura: 'Lista', EstadoActivoID: 1, Activo: true,
      Observaciones: 'Fila de prueba de la Fase A. Borrar con borrarDatosDePrueba().' },
    { MantenimientoID: 'TEST-MTTO-002', OTID: 'OT-0003', TecnicoID: 5,
      OrigenApertura: 'Lista', EstadoActivoID: 1, Activo: true,
      Observaciones: 'Fila de prueba de la Fase A. Borrar con borrarDatosDePrueba().' }
  ]
};

// ================================================================== LIMPIEZA

/** Filas basura verificadas en produccion el 2026-08-07. d02d8a3d SI se conserva. */
var LIMPIEZA_CHK = ['CHK001', '0356e6d7'];

/** FRM_CCTV y FRM_PMVF escriben FALSO en vez de FALSE. AppSheet no lo resuelve. */
var HOJAS_FALSO = ['FRM_CCTV', 'FRM_PMVF'];

// =================================================================== MOTOR

var _log = [];

function reg(nivel, msg) {
  var linea = nivel + '  ' + msg;
  _log.push(linea);
  Logger.log(linea);
}

function encabezados(hoja) {
  var n = hoja.getLastColumn();
  if (n === 0) return [];
  return hoja.getRange(1, 1, 1, n).getValues()[0];
}

function indiceDe(hoja, nombre) {
  var h = encabezados(hoja);
  for (var i = 0; i < h.length; i++) {
    if (String(h[i]).trim() === nombre) return i + 1;
  }
  return -1;
}

// ------------------------------------------------------------------ pasos

function paso1_renombrar(ss) {
  reg('==', 'PASO 1 — Renombrados');
  Object.keys(RENOMBRADOS).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) { reg('XX', nombreHoja + ' no existe. Se omite la tabla entera.'); return; }

    RENOMBRADOS[nombreHoja].forEach(function (par) {
      var viejo = par[0], nuevo = par[1];
      var iViejo = indiceDe(hoja, viejo);
      var iNuevo = indiceDe(hoja, nuevo);

      if (iViejo === -1 && iNuevo !== -1) {
        reg('==', nombreHoja + '.' + nuevo + ' ya estaba renombrada. Sin cambios.');
        return;
      }
      if (iViejo === -1) {
        reg('XX', nombreHoja + ': no encuentro la columna "' + viejo + '". ' +
                  'Produccion no coincide con la especificacion. REVISAR.');
        return;
      }
      if (iNuevo !== -1 && iNuevo !== iViejo) {
        reg('XX', nombreHoja + ': "' + nuevo + '" YA EXISTE en la columna ' + iNuevo +
                  ' y "' + viejo + '" en la ' + iViejo + '. Renombrar dejaria dos ' +
                  'columnas iguales. NO SE TOCA.');
        return;
      }
      if (!DRY_RUN) hoja.getRange(1, iViejo).setValue(nuevo);
      reg('->', nombreHoja + ': columna ' + iViejo + '  "' + viejo + '"  ->  "' + nuevo + '"');
    });
  });
}

function paso2_columnasNuevas(ss) {
  reg('==', 'PASO 2 — Columnas nuevas');
  Object.keys(COLUMNAS_NUEVAS).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) { reg('XX', nombreHoja + ' no existe.'); return; }

    COLUMNAS_NUEVAS[nombreHoja].forEach(function (col) {
      if (indiceDe(hoja, col) !== -1) {
        reg('==', nombreHoja + '.' + col + ' ya existe. Sin cambios.');
        return;
      }
      var destino = hoja.getLastColumn() + 1;
      if (!DRY_RUN) {
        if (destino > hoja.getMaxColumns()) hoja.insertColumnsAfter(hoja.getMaxColumns(), 1);
        hoja.getRange(1, destino).setValue(col);
      }
      reg('->', nombreHoja + ': columna nueva ' + destino + '  "' + col + '"');
    });
  });
}

function paso3_tablasNuevas(ss) {
  reg('==', 'PASO 3 — Tablas nuevas');
  Object.keys(TABLAS_NUEVAS).forEach(function (nombreHoja) {
    var def = TABLAS_NUEVAS[nombreHoja];
    var hoja = ss.getSheetByName(nombreHoja);

    if (hoja) {
      reg('==', nombreHoja + ' ya existe. No se recrea ni se repuebla.');
      return;
    }
    reg('->', nombreHoja + ': crear con ' + def.encabezados.length + ' columnas y ' +
              def.filas.length + ' filas');
    if (DRY_RUN) return;

    hoja = ss.insertSheet(nombreHoja);
    hoja.getRange(1, 1, 1, def.encabezados.length).setValues([def.encabezados]);
    hoja.getRange(1, 1, 1, def.encabezados.length).setFontWeight('bold');
    if (def.filas.length) {
      hoja.getRange(2, 1, def.filas.length, def.encabezados.length).setValues(def.filas);
    }
    hoja.setFrozenRows(1);
  });
}

function paso4_datosDePrueba(ss) {
  reg('==', 'PASO 4 — Datos de prueba (prefijo ' + PREFIJO_PRUEBA + ')');
  Object.keys(DATOS_PRUEBA).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) { reg('XX', nombreHoja + ' no existe.'); return; }

    var h = encabezados(hoja).map(function (x) { return String(x).trim(); });

    DATOS_PRUEBA[nombreHoja].forEach(function (obj) {
      var clave = obj[h[0]];
      if (String(clave).indexOf(PREFIJO_PRUEBA) !== 0) {
        reg('XX', nombreHoja + ': la fila "' + clave + '" no lleva el prefijo ' +
                  PREFIJO_PRUEBA + '. NO SE ESCRIBE.');
        return;
      }
      var faltan = Object.keys(obj).filter(function (k) { return h.indexOf(k) === -1; });
      if (faltan.length) {
        reg('XX', nombreHoja + ': la fila "' + clave + '" usa columnas que no existen: ' +
                  faltan.join(', ') + '. Ejecuta antes los pasos 1 y 2.');
        return;
      }
      var fila = h.map(function (col) { return obj.hasOwnProperty(col) ? obj[col] : ''; });
      if (!DRY_RUN) hoja.appendRow(fila);
      reg('->', nombreHoja + ': fila de prueba "' + clave + '" con OTID=' + obj.OTID);
    });
  });
}

function paso5_limpieza(ss) {
  reg('==', 'PASO 5 — Limpieza');

  var chk = ss.getSheetByName('CHK_Checklists');
  if (chk) {
    var datos = chk.getDataRange().getValues();
    for (var f = datos.length - 1; f >= 1; f--) {
      if (LIMPIEZA_CHK.indexOf(String(datos[f][0]).trim()) !== -1) {
        if (!DRY_RUN) chk.deleteRow(f + 1);
        reg('->', 'CHK_Checklists: borrar fila ' + (f + 1) + '  "' + datos[f][0] + '"');
      }
    }
  }

  HOJAS_FALSO.forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) { reg('XX', nombreHoja + ' no existe.'); return; }
    var rango = hoja.getDataRange();
    var v = rango.getValues();
    var n = 0;
    for (var i = 1; i < v.length; i++) {
      for (var j = 0; j < v[i].length; j++) {
        if (String(v[i][j]).trim().toUpperCase() === 'FALSO') { v[i][j] = false; n++; }
      }
    }
    if (n && !DRY_RUN) rango.setValues(v);
    reg(n ? '->' : '==', nombreHoja + ': ' + n + ' celdas FALSO -> FALSE');
  });
}

// ==================================================================== MAIN

function main() {
  _log = [];
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  reg('==', '================================================================');
  reg('==', 'SGMC — FASE A  ' + (DRY_RUN ? '[SIMULACION, no escribe]' : '[ESCRITURA REAL]'));
  reg('==', 'Documento: ' + ss.getName() + '  (' + ss.getId() + ')');
  reg('==', '================================================================');

  if (ss.getId() !== ID_ESPERADO) {
    reg('XX', 'ESTE NO ES EL DOCUMENTO ESPERADO. Se aborta sin tocar nada.');
    reg('XX', 'Esperado: ' + ID_ESPERADO);
    return _log.join('\n');
  }

  paso1_renombrar(ss);
  paso2_columnasNuevas(ss);
  paso3_tablasNuevas(ss);
  paso4_datosDePrueba(ss);
  paso5_limpieza(ss);

  var errores = _log.filter(function (l) { return l.indexOf('XX') === 0; });
  reg('==', '================================================================');
  reg('==', 'Acciones: ' + _log.filter(function (l) { return l.indexOf('->') === 0; }).length +
            '   |   Avisos y errores: ' + errores.length);
  if (errores.length) {
    reg('==', 'HAY PUNTOS MARCADOS XX. Leelos antes de poner DRY_RUN en false.');
  } else if (DRY_RUN) {
    reg('==', 'Simulacion limpia. Para aplicar: DRY_RUN = false y volver a ejecutar.');
  } else {
    reg('==', 'Aplicado. Copia este registro al acta y pasa a verificar.');
  }
  reg('==', '================================================================');

  return _log.join('\n');
}

// ============================================================ VERIFICACION

/**
 * Comprueba que los encabezados quedaron como dice la especificacion.
 * Se ejecuta DESPUES de main() con DRY_RUN = false.
 */
function verificar() {
  _log = [];
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  reg('==', 'VERIFICACION DE LA FASE A');

  var fallos = 0;

  Object.keys(RENOMBRADOS).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) { reg('XX', nombreHoja + ' no existe.'); fallos++; return; }
    RENOMBRADOS[nombreHoja].forEach(function (par) {
      if (indiceDe(hoja, par[1]) === -1) {
        reg('XX', nombreHoja + '.' + par[1] + ' NO existe.'); fallos++;
      } else if (indiceDe(hoja, par[0]) !== -1) {
        reg('XX', nombreHoja + '.' + par[0] + ' sigue existiendo con el nombre viejo.'); fallos++;
      }
    });
  });

  Object.keys(COLUMNAS_NUEVAS).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) return;
    COLUMNAS_NUEVAS[nombreHoja].forEach(function (col) {
      if (indiceDe(hoja, col) === -1) { reg('XX', nombreHoja + '.' + col + ' NO existe.'); fallos++; }
    });
  });

  Object.keys(TABLAS_NUEVAS).forEach(function (nombreHoja) {
    if (!ss.getSheetByName(nombreHoja)) { reg('XX', nombreHoja + ' NO existe.'); fallos++; }
  });

  var chk = ss.getSheetByName('CHK_Checklists');
  if (chk) {
    var ids = chk.getDataRange().getValues().map(function (f) { return String(f[0]).trim(); });
    LIMPIEZA_CHK.forEach(function (id) {
      if (ids.indexOf(id) !== -1) { reg('XX', 'CHK_Checklists: "' + id + '" sigue ahi.'); fallos++; }
    });
    if (ids.indexOf('d02d8a3d') === -1) {
      reg('XX', 'CHK_Checklists: se borro d02d8a3d, que debia CONSERVARSE.'); fallos++;
    }
  }

  reg('==', fallos === 0 ? 'VERIFICACION LIMPIA. Fase A cerrada.'
                         : 'VERIFICACION CON ' + fallos + ' FALLOS.');
  return _log.join('\n');
}

// ======================================================= BORRADO DE PRUEBAS

/**
 * Borra las filas de prueba. Vive en el mismo archivo que las crea, a
 * proposito: el proyecto ya arrastra basura de prueba en produccion que entro
 * sin marca y sin fecha de caducidad.
 */
function borrarDatosDePrueba() {
  _log = [];
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  reg('==', 'BORRADO DE DATOS DE PRUEBA  ' + (DRY_RUN ? '[SIMULACION]' : '[REAL]'));

  Object.keys(DATOS_PRUEBA).forEach(function (nombreHoja) {
    var hoja = ss.getSheetByName(nombreHoja);
    if (!hoja) return;
    var datos = hoja.getDataRange().getValues();
    for (var f = datos.length - 1; f >= 1; f--) {
      if (String(datos[f][0]).indexOf(PREFIJO_PRUEBA) === 0) {
        if (!DRY_RUN) hoja.deleteRow(f + 1);
        reg('->', nombreHoja + ': borrar fila ' + (f + 1) + '  "' + datos[f][0] + '"');
      }
    }
  });
  return _log.join('\n');
}
