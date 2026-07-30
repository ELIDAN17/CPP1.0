// ==========================================
// RUTA DE TU ARCHIVO: src/views/Login.jsx
// ==========================================
import { useState, useContext } from 'react';
import { Shield, Mail, Lock, ArrowRight, AlertTriangle, Eye, EyeOff } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

export default function Login() {
  const { iniciarSesion } = useContext(AuthContext);

  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [mostrarPassword, setMostrarPassword] = useState(false);
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setCargando(true);

    try {
      const respuesta = await fetch('http://localhost:3000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, contrasena: password }),
      });

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(datos.error || 'Credenciales inválidas');
      }

      // <-- 3. CORRECCIÓN: Pasamos el token Y los datos del usuario al AuthContext
      // Asegúrate de que tu backend devuelva el objeto con el perfil (ej: datos.usuario)
      iniciarSesion(datos.token, datos.usuario);

    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#070a13] relative overflow-hidden px-4">
      {/* Efectos de luces de fondo (Glow effects) */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-600/10 rounded-full blur-[120px]"></div>
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-cyan-500/10 rounded-full blur-[120px]"></div>

      <div className="w-full max-w-md bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-2xl relative z-10">
        
        {/* Encabezado animado */}
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-cyan-500/10 rounded-2xl border border-cyan-500/20 mb-4 shadow-[0_0_20px_rgba(6,182,212,0.15)]">
            <Shield className="w-8 h-8 text-cyan-400" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white">SMCPP - UNA PUNO</h2>
          <p className="text-slate-400 text-sm mt-1">Control de Prácticas Preprofesionales</p>
        </div>

        {/* Alerta de Error Dinámica */}
        {error && (
          <div className="mb-5 flex items-center gap-3 bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-xl text-sm animate-shake">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Correo Institucional</label>
            <div className="relative">
              <Mail className="absolute left-4 top-3.5 w-5 h-5 text-slate-500" />
              <input 
                type="email"
                required
                placeholder="usuario@unap.edu.pe"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                className="w-full bg-slate-950/50 border border-slate-800 rounded-xl py-3 pl-12 pr-4 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all text-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Contraseña</label>
            <div className="relative">
              <Lock className="absolute left-4 top-3.5 w-5 h-5 text-slate-500" />
              <input 
                type={mostrarPassword ? "text" : "password"}
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-950/50 border border-slate-800 rounded-xl py-3 pl-12 pr-4 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all text-sm"
              />
              <button
                type="button"
                onClick={() => setMostrarPassword(!mostrarPassword)}
                className="absolute right-4 top-3.5 text-slate-500 hover:text-slate-300 focus:outline-none"
              >
                {mostrarPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={cargando}
            className="w-full group relative flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-semibold py-3 px-4 rounded-xl shadow-[0_4px_20px_rgba(6,182,212,0.25)] transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm mt-2 overflow-hidden"
          >
            <span>{cargando ? 'Verificando huella digital...' : 'Ingresar al Portal'}</span>
            {!cargando && <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />}
          </button>
        </form>

      </div>
    </div>
  );
}