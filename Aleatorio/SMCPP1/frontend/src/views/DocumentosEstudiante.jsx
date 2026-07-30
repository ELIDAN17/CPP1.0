// ==========================================
// RUTA DE TU ARCHIVO: src/views/DocumentosEstudiante.jsx
// ==========================================
import { useState, useEffect, useContext, useRef } from 'react';
import { AuthContext } from '../context/AuthContext';
import { FileText, FileCheck, TriangleAlert, RefreshCw, UploadCloud, CheckCircle, X, Send } from 'lucide-react';

export default function DocumentosEstudiante() {
  // Extraemos el token y cerrarSesion del AuthContext maestro
  const { token, cerrarSesion } = useContext(AuthContext);
  const [documentos, setDocumentos] = useState([]);
  const [cargando, setCargando] = useState(true);

  const [colaDeSubida, setColaDeSubida] = useState({});
  const [subiendoId, setSubiendoId] = useState(null);

  const fileInputRefs = useRef({});

  // ESCUCHADOR DE RED: Si vuelve el internet o se cae mientras revisa sus entregables
  useEffect(() => {
    const manejarRegresoRed = () => {
      console.log("Internet restablecido. Refrescando expediente digital...");
      setCargando(true); // Dispara la recarga limpia del useEffect de abajo
    };

    window.addEventListener('online', manejarRegresoRed);

    return () => {
      window.removeEventListener('online', manejarRegresoRed);
    };
  }, []);

  useEffect(() => {
    if (!token) return;
    let activo = true;

    const obtenerDocumentos = async () => {
      try {
        // SEGURIDAD BLINDADA: El backend extrae el estudiante a través del Token.
        const respuesta = await fetch(`http://localhost:3000/api/documentos/estudiante`, {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${token}` }
        });

        // CONTROL DE EXPIRACIÓN: Si el token caducó
        if (respuesta.status === 401 || respuesta.status === 403) {
          alert("Tu sesión ha caducado por seguridad. Por favor, vuelve a ingresar.");
          cerrarSesion();
          return;
        }

        const datos = await respuesta.json();

        if (activo && respuesta.ok) {
          setDocumentos(Array.isArray(datos) ? datos : []);
          setCargando(false);
        }
      } catch (err) {
        console.error("Error al traer documentos:", err);
        if (activo) setCargando(false);
      }
    };

    if (cargando) {
      obtenerDocumentos();
    }

    return () => {
      activo = false;
    };
  }, [token, cargando, cerrarSesion]);

  const recargarDocumentosSilenciosamente = async () => {
    try {
      const respuesta = await fetch(`http://localhost:3000/api/documentos/estudiante`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (respuesta.status === 401 || respuesta.status === 403) {
        cerrarSesion();
        return;
      }

      const datos = await respuesta.json();
      if (respuesta.ok) setDocumentos(Array.isArray(datos) ? datos : []);
    } catch (err) {
      console.error("Error al refrescar documentos:", err);
    }
  };

  const handleFileSelect = (e, reqId) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const todosSonPdf = files.every(file => file.type === 'application/pdf');
    if (!todosSonPdf) {
      alert('Por favor, selecciona únicamente archivos en formato PDF.');
      return;
    }

    setColaDeSubida(prev => {
      const archivosExistentes = prev[reqId] || [];
      return {
        ...prev,
        [reqId]: [...archivosExistentes, ...files]
      };
    });

    if (fileInputRefs.current[reqId]) fileInputRefs.current[reqId].value = '';
  };

  const handleRemoveFromCola = (reqId, indexAliminar) => {
    setColaDeSubida(prev => {
      const archivosExistentes = prev[reqId] || [];
      const nuevaLista = archivosExistentes.filter((_, idx) => idx !== indexAliminar);

      const nuevaCola = { ...prev };
      if (nuevaLista.length === 0) {
        delete nuevaCola[reqId];
      } else {
        nuevaCola[reqId] = nuevaLista;
      }
      return nuevaCola;
    });
  };

  const handleSubirDocumentoIndividual = async (reqId) => {
    const archivos = colaDeSubida[reqId];
    if (!archivos || archivos.length === 0) return;

    if (!navigator.onLine) {
      alert("No tienes conexión a internet en este momento. Restablece tu red para enviar los archivos.");
      return;
    }

    setSubiendoId(reqId);

    try {
      for (const archivo of archivos) {
        const formData = new FormData();
        // 🔄 SINCRONIZADO AL 100% CON TU BACKEND POSTGRES Y MULTER:
        formData.append('id_tipo_doc', reqId);     // Coincide con req.body.id_tipo_doc
        formData.append('documento', archivo);     // Coincide con upload.single('documento')

        const respuesta = await fetch('http://localhost:3000/api/documentos/subir', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        });

        if (respuesta.status === 401 || respuesta.status === 403) {
          alert("Tu sesión expiró. El archivo actual y los siguientes no pudieron procesarse.");
          cerrarSesion();
          return;
        }

        if (!respuesta.ok) {
          const resError = await respuesta.json();
          throw new Error(resError.error || `Error al guardar el archivo "${archivo.name}"`);
        }
      }

      setColaDeSubida(prev => {
        const nuevaCola = { ...prev };
        delete nuevaCola[reqId];
        return nuevaCola;
      });

      // Refrescamos la lista local con los datos actualizados de la base de datos
      await recargarDocumentosSilenciosamente();
      alert("¡Todos los archivos se enviaron y registraron con éxito!");
    } catch (err) {
      alert(err.message);
    } fileInputRefs.current = {};
    setSubiendoId(null);
  };

  if (cargando) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[300px] gap-3">
        <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin" />
        <p className="text-slate-400 text-sm animate-pulse">Abriendo repositorio de entregables...</p>
      </div>
    );
  }

  // Sincronizado con los IDS correlativos de tu tabla 'tipos_documento'
  const requisitos = [
    { id: 1, nombre: 'Convenio de Prácticas Preprofesionales', desc: 'Esquema detallado firmado por la empresa y el asesor.' },
    { id: 2, nombre: 'Plan de Trabajo Inicial', desc: 'Reporte del primer avance y metas del proceso.' },
    { id: 3, nombre: 'Informe Inicial de Prácticas', desc: 'Memoria descriptiva inicial de la práctica.' },
    { id: 4, nombre: 'Informe Final de Prácticas', desc: 'Memoria descriptiva final junto a la constancia de término.' }
  ];

  return (
    <div className="space-y-6 max-w-4xl">

      <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl backdrop-blur-md">
        <h3 className="text-base font-bold text-white tracking-wide">Expediente Digital de Prácticas</h3>
        <p className="text-xs text-slate-400 mt-1">Carga tus entregables en formato <span className="text-cyan-400 font-semibold">PDF</span>. Puedes seleccionar múltiples archivos si lo necesitas.</p>
      </div>

      <div className="space-y-4">
        {requisitos.map((req) => {
          // Buscamos usando el campo exacto de tu tabla: id_tipo_doc
          const docEnBD = documentos.find(d => parseInt(d.id_tipo_doc) === req.id);
          const yaEstaEnBD = !!docEnBD;
          const listaArchivosTemporales = colaDeSubida[req.id] || [];
          const tieneArchivosEnCola = listaArchivosTemporales.length > 0;
          const estaSubiendo = subiendoId === req.id;
          const estadoTexto = yaEstaEnBD ? docEnBD.estado_aprobacion : 'No Entregado';

          return (
            <div
              key={req.id}
              className="bg-slate-900/20 border border-slate-850 p-5 rounded-2xl flex flex-col md:flex-row md:items-start justify-between gap-4 transition-all hover:border-slate-800"
            >
              <input
                type="file"
                accept=".pdf"
                multiple
                className="hidden"
                ref={el => fileInputRefs.current[req.id] = el}
                onChange={(e) => handleFileSelect(e, req.id)}
              />

              {/* LADO IZQUIERDO: Info del entregable */}
              <div className="flex items-start gap-4 flex-1">
                <div className={`p-3 rounded-xl border shrink-0 ${yaEstaEnBD && docEnBD.estado_aprobacion === 'Aprobado' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                  tieneArchivosEnCola ? 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400' :
                    yaEstaEnBD ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                      'bg-slate-800/40 border-slate-750 text-slate-400'
                  }`}>
                  {yaEstaEnBD && docEnBD.estado_aprobacion === 'Aprobado' ? <FileCheck className="w-6 h-6" /> : <FileText className="w-6 h-6" />}
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">{req.nombre}</h4>
                  <p className="text-xs text-slate-400 mt-0.5">{req.desc}</p>

                  <span className={`inline-flex items-center gap-1 mt-2.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${yaEstaEnBD && docEnBD.estado_aprobacion === 'Aprobado' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                      yaEstaEnBD ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                        'bg-rose-500/10 border-rose-500/20 text-rose-400'
                    }`}>
                    {yaEstaEnBD && docEnBD.estado_aprobacion === 'Aprobado' && <CheckCircle className="w-3 h-3" />}
                    {yaEstaEnBD && docEnBD.estado_aprobacion !== 'Aprobado' && <RefreshCw className="w-3 h-3 animate-spin text-amber-400" />}
                    {!yaEstaEnBD && <TriangleAlert className="w-3 h-3" />}
                    {estadoTexto}
                  </span>

                  {yaEstaEnBD && docEnBD.comentarios_revision && (
                    <div className="mt-3 p-2.5 bg-rose-500/5 border border-rose-500/10 rounded-xl text-[11px] text-rose-400 leading-relaxed max-w-md">
                      <strong>Observaciones del Coordinador:</strong> {docEnBD.comentarios_revision}
                    </div>
                  )}
                </div>
              </div>

              {/* LADO DERECHO: Acciones */}
              <div className="shrink-0 flex items-center justify-end w-full md:w-auto pt-1">
                {estaSubiendo ? (
                  <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800 w-full md:w-52 justify-center">
                    <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin" />
                    <span>Enviando ({listaArchivosTemporales.length}) archivos...</span>
                  </div>
                ) : yaEstaEnBD && docEnBD.estado_aprobacion === 'Aprobado' ? (
                  <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/5 px-4 py-2 rounded-xl border border-emerald-500/10 block w-full text-center md:w-52">
                    Validado en Sistema
                  </span>
                ) : (
                  <div className="flex flex-col gap-2 w-full md:w-52">

                    {tieneArchivosEnCola && (
                      <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1 custom-scrollbar">
                        {listaArchivosTemporales.map((archivo, index) => (
                          <div
                            key={index}
                            className="bg-slate-950/60 border border-cyan-500/20 rounded-xl p-2 flex items-center justify-between gap-2 shadow-inner"
                          >
                            <div className="flex items-center gap-1.5 min-w-0 flex-1">
                              <CheckCircle className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                              <span className="text-xs text-slate-200 truncate font-semibold" title={archivo.name}>
                                {archivo.name}
                              </span>
                            </div>
                            <button
                              type="button"
                              onClick={() => handleRemoveFromCola(req.id, index)}
                              className="text-slate-500 hover:text-rose-400 p-0.5 rounded transition-colors shrink-0"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))}
                      </div>
                    )}

                    <button
                      type="button"
                      onClick={() => fileInputRefs.current[req.id].click()}
                      className="w-full flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-750 text-white font-semibold py-2 px-4 rounded-xl text-xs transition-all border border-slate-700"
                    >
                      <UploadCloud className="w-3.5 h-3.5 text-slate-400" />
                      <span>{tieneArchivosEnCola ? 'Añadir más PDFs' : yaEstaEnBD ? 'Reenviar Corrección' : 'Seleccionar PDFs'}</span>
                    </button>

                    {tieneArchivosEnCola && (
                      <button
                        type="button"
                        onClick={() => handleSubirDocumentoIndividual(req.id)}
                        className="flex items-center justify-center gap-1.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold py-1.5 px-3 rounded-xl text-xs transition-all shadow-[0_0_15px_rgba(6,182,212,0.15)] w-full"
                      >
                        <Send className="w-3 h-3" />
                        <span>Confirmar Envío ({listaArchivosTemporales.length})</span>
                      </button>
                    )}

                  </div>
                )}
              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
}