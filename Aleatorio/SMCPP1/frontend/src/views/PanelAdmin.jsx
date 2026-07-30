import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { UserPlus, Trash2, Search, Key, Shield, User, RefreshCw, X, Save } from 'lucide-react';

export default function PanelAdmin() {
    const { token, usuario } = useContext(AuthContext);

    const [usuarios, setUsuarios] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [busqueda, setBusqueda] = useState('');

    // Modal de registro
    const [mostrarModal, setMostrarModal] = useState(false);
    const [guardando, setGuardando] = useState(false);

    const [formData, setFormData] = useState({
        correo: '',
        contrasena: '',
        idRol: 3, // Estudiante por defecto
        nombres: '',
        apellidos: '',
        dni: '',
        codigoEstudiante: '',
        escuela: 'Ingeniería de Sistemas',
        cargo: '',
        celular: '',
        cargoEmpresa: '',
        nombreEmpresa: ''
    });

    const [mensaje, setMensaje] = useState({ tipo: '', texto: '' });

    // Cargar lista de usuarios
    const cargarUsuarios = async () => {
        try {
            setCargando(true);
            const res = await fetch('http://localhost:3000/api/admin/usuarios', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const datos = await res.json();
                setUsuarios(datos);
            }
        } catch (error) {
            console.error("Error al cargar usuarios:", error);
        } finally {
            setCargando(false);
        }
    };

    useEffect(() => {
        if (token) cargarUsuarios();
    }, [token]);

    // Manejar cambio en inputs
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'idRol' ? Number(value) : value
        }));
    };

    // Enviar formulario (registrar usuario)
    const handleSubmit = async (e) => {
        e.preventDefault();
        setGuardando(true);
        setMensaje({ tipo: '', texto: '' });

        try {
            const res = await fetch('http://localhost:3000/api/admin/usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });
            const datos = await res.json();

            if (!res.ok) {
                throw new Error(datos.error || "Error al registrar el usuario.");
            }

            setMensaje({ tipo: 'exito', texto: "Usuario registrado con éxito en el sistema." });
            setFormData({
                correo: '',
                contrasena: '',
                idRol: 3,
                nombres: '',
                apellidos: '',
                dni: '',
                codigoEstudiante: '',
                escuela: 'Ingeniería de Sistemas',
                cargo: '',
                celular: '',
                cargoEmpresa: '',
                nombreEmpresa: ''
            });
            setTimeout(() => {
                setMostrarModal(false);
                setMensaje({ tipo: '', texto: '' });
                cargarUsuarios();
            }, 1500);

        } catch (err) {
            setMensaje({ tipo: 'error', texto: err.message });
        } finally {
            setGuardando(false);
        }
    };

    // Eliminar usuario
    const handleEliminar = async (idUsuario) => {
        if (!window.confirm("¿Está seguro de que desea eliminar este usuario de forma permanente? Todos sus datos y perfiles y registros asociados serán borrados de la base de datos.")) {
            return;
        }

        try {
            const res = await fetch(`http://localhost:3000/api/admin/usuarios/${idUsuario}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const datos = await res.json();

            if (!res.ok) {
                alert(datos.error || "No se pudo eliminar el usuario.");
                return;
            }

            alert("Usuario eliminado correctamente.");
            cargarUsuarios();
        } catch (error) {
            console.error(error);
        }
    };

    // Filtrar
    const usuariosFiltrados = usuarios.filter(u =>
        u.nombre_completo?.toLowerCase().includes(busqueda.toLowerCase()) ||
        u.correo?.toLowerCase().includes(busqueda.toLowerCase()) ||
        u.nombre_rol?.toLowerCase().includes(busqueda.toLowerCase())
    );

    return (
        <div className="space-y-6">

            {/* HEADER DE CONTROL */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h3 className="text-lg font-bold text-white">Panel de Administración Global</h3>
                    <p className="text-xs text-slate-400">Creación, consulta y revocación de accesos de usuarios y perfiles.</p>
                </div>

                <button
                    onClick={() => setMostrarModal(true)}
                    className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs rounded-xl shadow-lg transition-all"
                >
                    <UserPlus className="w-4 h-4" /> Registrar Nuevo Usuario
                </button>
            </div>

            {/* BARRA DE BÚSQUEDA */}
            <div className="relative max-w-sm w-full">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-500">
                    <Search className="w-4 h-4" />
                </span>
                <input
                    type="text"
                    placeholder="Buscar por nombre, correo o rol..."
                    value={busqueda}
                    onChange={(e) => setBusqueda(e.target.value)}
                    className="w-full text-xs pl-9 pr-4 py-2 bg-slate-950/40 border border-slate-850 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors"
                />
            </div>

            {/* TABLA DE USUARIOS */}
            <div className="bg-slate-950/40 border border-slate-850 rounded-2xl overflow-hidden shadow-lg">
                {cargando ? (
                    <div className="flex justify-center items-center h-48 gap-2">
                        <RefreshCw className="w-5 h-5 text-cyan-400 animate-spin" />
                        <p className="text-slate-400 text-xs">Cargando base de datos...</p>
                    </div>
                ) : usuariosFiltrados.length === 0 ? (
                    <p className="text-slate-500 text-xs text-center py-12">No se encontraron usuarios coincidentes.</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-xs text-slate-350">
                            <thead>
                                <tr className="border-b border-slate-850 bg-slate-900/20 text-[10px] font-bold text-slate-400 tracking-wider uppercase">
                                    <th className="p-4">Usuario / Nombre</th>
                                    <th className="p-4">Correo</th>
                                    <th className="p-4">Identificador</th>
                                    <th className="p-4">Rol</th>
                                    <th className="p-4 text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-850/40">
                                {usuariosFiltrados.map((u) => {
                                    const esPropio = u.id_usuario === usuario?.id_usuario;
                                    return (
                                        <tr key={u.id_usuario} className="hover:bg-slate-900/10 transition-colors">
                                            <td className="p-4">
                                                <div className="font-semibold text-white">{u.nombre_completo || 'Sin Perfil Registrado'}</div>
                                                <div className="text-[10px] text-slate-500">Reg: {new Date(u.fecha_creacion).toLocaleDateString()}</div>
                                            </td>
                                            <td className="p-4 text-slate-300 font-mono">{u.correo}</td>
                                            <td className="p-4"><span className="font-mono text-cyan-400">{u.codigo || '—'}</span></td>
                                            <td className="p-4">
                                                <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase ${u.id_rol === 1 ? 'bg-rose-500/10 text-rose-450 border border-rose-500/20' :
                                                        u.id_rol === 2 ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' :
                                                            u.id_rol === 4 ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                                                                u.id_rol === 5 ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' :
                                                                    'bg-slate-800 text-slate-300 border border-slate-700'
                                                    }`}>
                                                    {u.nombre_rol}
                                                </span>
                                            </td>
                                            <td className="p-4 text-center">
                                                <button
                                                    onClick={() => handleEliminar(u.id_usuario)}
                                                    disabled={esPropio}
                                                    title={esPropio ? "No puedes eliminarte a ti mismo" : "Eliminar de base de datos"}
                                                    className={`p-1.5 rounded-lg border transition-colors ${esPropio
                                                            ? 'bg-slate-900 border-slate-850 text-slate-700 cursor-not-allowed'
                                                            : 'bg-rose-500/10 hover:bg-rose-500/20 border-rose-500/20 text-rose-400'
                                                        }`}
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* ================= MODAL DE REGISTRO DE USUARIO ================= */}
            {mostrarModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 overflow-y-auto">
                    <form onSubmit={handleSubmit} className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 space-y-4 my-8">
                        <div className="flex justify-between items-start border-b border-slate-800 pb-2">
                            <div className="flex items-center gap-2">
                                <Shield className="w-5 h-5 text-cyan-400" />
                                <div>
                                    <h4 className="text-sm font-bold text-white">Registrar Nuevo Usuario</h4>
                                    <p className="text-[11px] text-slate-400">Las validaciones de correos institucionales se aplican en el servicio.</p>
                                </div>
                            </div>
                            <button
                                type="button"
                                onClick={() => setMostrarModal(false)}
                                className="text-slate-400 hover:text-white text-xs bg-slate-800 px-2.5 py-1 rounded-lg"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        {mensaje.texto && (
                            <div className={`p-3 rounded-xl text-xs font-semibold ${mensaje.tipo === 'exito' ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400' : 'bg-rose-500/10 border border-rose-500/20 text-rose-400'
                                }`}>
                                {mensaje.texto}
                            </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">

                            {/* Rol */}
                            <div className="col-span-1 md:col-span-2">
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Seleccionar Rol de Usuario</label>
                                <select
                                    name="idRol"
                                    value={formData.idRol}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                >
                                    <option value={3}>Estudiante Preprofesional</option>
                                    <option value={2}>Coordinador Académico (EPIS)</option>
                                    <option value={4}>Tutor Externo (Empresa)</option>
                                    <option value={5}>Decano de Facultad</option>
                                    <option value={1}>Administrador General</option>
                                </select>
                            </div>

                            {/* Correo y Contraseña */}
                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Correo Electrónico</label>
                                <input
                                    type="email"
                                    name="correo"
                                    required
                                    placeholder="ejemplo@unap.edu.pe"
                                    value={formData.correo}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50 font-mono"
                                />
                            </div>

                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Contraseña</label>
                                <input
                                    type="password"
                                    name="contrasena"
                                    required
                                    placeholder="********"
                                    value={formData.contrasena}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                />
                            </div>

                            {/* Nombres y Apellidos */}
                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Nombres</label>
                                <input
                                    type="text"
                                    name="nombres"
                                    required
                                    placeholder="Nombres completos"
                                    value={formData.nombres}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                />
                            </div>

                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Apellidos</label>
                                <input
                                    type="text"
                                    name="apellidos"
                                    required
                                    placeholder="Apellidos completos"
                                    value={formData.apellidos}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                />
                            </div>

                            {/* DNI */}
                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Número de DNI</label>
                                <input
                                    type="text"
                                    name="dni"
                                    required
                                    maxLength={8}
                                    placeholder="8 dígitos"
                                    value={formData.dni}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50 font-mono"
                                />
                            </div>

                            {/* Celular */}
                            <div>
                                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Celular de Contacto</label>
                                <input
                                    type="text"
                                    name="celular"
                                    placeholder="9XXXXXXXX"
                                    value={formData.celular}
                                    onChange={handleChange}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50 font-mono"
                                />
                            </div>

                            {/* CONDICIONAL: ESTUDIANTE */}
                            {formData.idRol === 3 && (
                                <>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Código Estudiante</label>
                                        <input
                                            type="text"
                                            name="codigoEstudiante"
                                            required
                                            placeholder="6 dígitos"
                                            value={formData.codigoEstudiante}
                                            onChange={handleChange}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50 font-mono"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Escuela Profesional</label>
                                        <input
                                            type="text"
                                            name="escuela"
                                            required
                                            value={formData.escuela}
                                            onChange={handleChange}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                        />
                                    </div>
                                </>
                            )}

                            {/* CONDICIONAL: TUTOR EXTERNO */}
                            {formData.idRol === 4 && (
                                <>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Nombre de la Empresa</label>
                                        <input
                                            type="text"
                                            name="nombreEmpresa"
                                            required
                                            placeholder="Razón Social S.AC."
                                            value={formData.nombreEmpresa}
                                            onChange={handleChange}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Cargo en Empresa (Tutor)</label>
                                        <input
                                            type="text"
                                            name="cargoEmpresa"
                                            placeholder="Gerente TI, Asesor, etc."
                                            value={formData.cargoEmpresa}
                                            onChange={handleChange}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                        />
                                    </div>
                                </>
                            )}

                            {/* CONDICIONAL: COORDINADOR O DECANO */}
                            {(formData.idRol === 2 || formData.idRol === 5) && (
                                <div className="col-span-1 md:col-span-2">
                                    <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Cargo Autoridad</label>
                                    <input
                                        type="text"
                                        name="cargo"
                                        placeholder={formData.idRol === 2 ? "Coordinador de Prácticas EPIS" : "Decano de Facultad"}
                                        value={formData.cargo}
                                        onChange={handleChange}
                                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500/50"
                                    />
                                </div>
                            )}

                        </div>

                        <button
                            type="submit"
                            disabled={guardando}
                            className="w-full py-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 transition-all"
                        >
                            {guardando ? (
                                <>
                                    <RefreshCw className="w-4 h-4 animate-spin" /> Guardando...
                                </>
                            ) : (
                                <>
                                    <Save className="w-4 h-4" /> Grabar Registro de Usuario
                                </>
                            )}
                        </button>
                    </form>
                </div>
            )}

        </div>
    );
}
