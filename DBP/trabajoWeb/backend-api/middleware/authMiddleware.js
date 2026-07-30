// backend-api/middleware/authMiddleware.js
const jwt = require('jsonwebtoken');
require('dotenv').config(); // Asegúrate de cargar .env aquí también

const jwtSecret = process.env.JWT_SECRET; // Obtener el secreto de las variables de entorno

const authMiddleware = (req, res, next) => {
    if (!jwtSecret) {
        console.error('ERROR CRÍTICO: JWT_SECRET no está configurado en las variables de entorno.');
        return res.status(500).json({ message: 'Error de configuración del servidor: JWT_SECRET no definido.' });
    }

    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ message: 'Acceso denegado. No se proporcionó token de autenticación.' });
    }

    jwt.verify(token, jwtSecret, (err, user) => {
        if (err) {
            console.error('Error al verificar token JWT:', err.message);
            return res.status(403).json({ message: 'Token de autenticación inválido o expirado.' });
        }
        req.user = user; // Adjunta el payload del token (ej. { id_usuario: 1, rol: 'cliente' })
        next();
    });
};

// Función para autorizar roles
const authorizeRoles = (...roles) => {
    return (req, res, next) => {
        // Si no hay información de usuario en la solicitud (authMiddleware no se ejecutó o falló)
        // o si el rol del usuario no está incluido en los roles permitidos
        if (!req.user || !roles.includes(req.user.rol)) {
            return res.status(403).json({ message: 'Acceso denegado: No tienes permiso para realizar esta acción.' });
        }
        next(); // Si tiene el rol permitido, pasa al siguiente middleware/controlador
    };
};

// CORRECCIÓN CLAVE: Exportar AMBAS funciones como propiedades de un objeto
module.exports = { authMiddleware, authorizeRoles };
