import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import Login from '../views/Login';

export default function RutaProtegida({ children }) {
  const { usuario } = useContext(AuthContext);

  // Si el usuario no está autenticado, renderizamos el Login de inmediato
  if (!usuario || !usuario.logueado) {
    return <Login />;
  }

  // Si está autenticado, le permitimos ver la pantalla solicitada
  return children;
}