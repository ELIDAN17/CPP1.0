const authService = require('../services/authService');

const registrarUsuario = async (req, res) => {
    try {
        const data = req.body;
        const nuevoUsuario = await authService.crearCuenta(data);
        res.status(201).json({ personalizado: "Éxito", usuario: nuevoUsuario });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};

const loginUsuario = async (req, res) => {
    try {
        const { correo, contrasena } = req.body;
        const sesion = await authService.autenticar(correo, contrasena);
        res.status(200).json(sesion);
    } catch (error) {
        res.status(401).json({ error: error.message });
    }
};

module.exports = {
    registrarUsuario,
    loginUsuario
};