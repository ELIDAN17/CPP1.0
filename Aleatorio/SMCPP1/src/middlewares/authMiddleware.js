// PARTE DE TU MIDDLEWARE: src/middlewares/authMiddleware.js
const jwt = require('jsonwebtoken');

const verificarToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    
    // Si no viene el header
    if (!authHeader) {
        return res.status(401).json({ mensaje: 'Acceso denegado. Token no proporcionado.' });
    }

    // Extraer quitando el string "Bearer " de manera segura
    const token = authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : authHeader;

    if (!token) {
        return res.status(401).json({ mensaje: 'Formato de token inválido.' });
    }

    try {
        const verificado = jwt.verify(token, process.env.JWT_SECRET);
        // 🎯 OJO AQUÍ: Asegúrate de guardar todo el objeto verificado
        req.usuario = verificado; 
        next();
    } catch (error) {
        // Si el token expiró o cambió, devolvemos 403
        return res.status(403).json({ mensaje: 'Token inválido o expirado.' });
    }
};

module.exports = { verificarToken };