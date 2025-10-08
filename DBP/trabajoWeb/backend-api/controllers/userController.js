// backend-api/controllers/userController.js
const db = require('../config/db'); // Asumimos que es un pool de mysql2/promise
const bcrypt = require('bcryptjs');

// Obtener todos los usuarios (solo para administradores)
// Renombrado de getProfile a getAllUsers si esta ruta es para todos los usuarios
exports.getAllUsers = async (req, res) => {
    try {
        const [rows] = await db.execute('SELECT id_usuario, correo, nombre, apellido, telefono, rol, fecha_creacion, fecha_actualizacion FROM Usuario');
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener todos los usuarios:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener usuarios.' });
    }
};

// Obtener un usuario por ID
// Renombrado de getProfile a getUserById para mayor claridad
exports.getUserById = async (req, res) => {
    const { id } = req.params; // Usamos ':id' en la ruta, así que aquí es 'id'
    const authenticatedUserId = req.user?.id_usuario;
    const authenticatedUserRole = req.user?.rol;

    try {
        const [rows] = await db.execute('SELECT id_usuario, correo, nombre, apellido, telefono, rol, fecha_creacion, fecha_actualizacion FROM Usuario WHERE id_usuario = ?', [id]);

        if (rows.length === 0) {
            return res.status(404).json({ message: 'Usuario no encontrado.' });
        }

        const userFound = rows[0];

        // Autorización: un usuario solo puede ver su propio perfil, a menos que sea admin
        if (authenticatedUserRole !== 'administrador' && String(userFound.id_usuario) !== String(authenticatedUserId)) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver este perfil.' });
        }

        res.status(200).json(userFound);
    } catch (error) {
        console.error('Error al obtener perfil de usuario:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener perfil.' });
    }
};

// Actualizar perfil de usuario
// Renombrado de updateProfile a updateUser
exports.updateUser = async (req, res) => {
    const { id } = req.params; // ID del usuario a actualizar (usamos ':id' en la ruta)
    const { nombre, apellido, telefono, correo, contraseña } = req.body;
    const authenticatedUserId = req.user?.id_usuario;
    const authenticatedUserRole = req.user?.rol;

    // Validación básica de entrada
    if (!nombre || !apellido || !correo) {
        return res.status(400).json({ message: 'Nombre, apellido y correo son campos obligatorios.' });
    }

    try {
        // Primero, verifica si el usuario existe y si el usuario autenticado tiene permiso
        const [userRows] = await db.execute('SELECT id_usuario, rol FROM Usuario WHERE id_usuario = ?', [id]);
        if (userRows.length === 0) {
            return res.status(404).json({ message: 'Usuario no encontrado.' });
        }

        // Autorización: un usuario solo puede actualizar su propio perfil, a menos que sea admin
        if (authenticatedUserRole !== 'administrador' && String(userRows[0].id_usuario) !== String(authenticatedUserId)) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para actualizar este perfil.' });
        }

        let query = 'UPDATE Usuario SET nombre = ?, apellido = ?, telefono = ?, correo = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id_usuario = ?';
        let queryParams = [nombre, apellido, telefono, correo, id];

        if (contraseña) {
            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(contraseña, salt);
            // Asegúrate de que tu columna de contraseña en la DB sea 'contraseña_hash' si es así
            query = 'UPDATE Usuario SET nombre = ?, apellido = ?, telefono = ?, correo = ?, contraseña_hash = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id_usuario = ?';
            queryParams = [nombre, apellido, telefono, correo, hashedPassword, id];
        }

        const [result] = await db.execute(query, queryParams);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Usuario no encontrado o no se realizaron cambios.' });
        }

        res.status(200).json({ message: 'Perfil de usuario actualizado con éxito.' });
    } catch (error) {
        console.error('Error al actualizar perfil de usuario:', error);
        if (error.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ message: 'El correo electrónico ya está registrado.' });
        }
        res.status(500).json({ message: 'Error interno del servidor al actualizar perfil.' });
    }
};

// Eliminar un usuario (solo para administradores)
exports.deleteUser = async (req, res) => {
    const { id } = req.params;
    const authenticatedUserRole = req.user?.rol;

    if (authenticatedUserRole !== 'administrador') {
        return res.status(403).json({ message: 'Acceso denegado. Solo los administradores pueden eliminar usuarios.' });
    }

    try {
        const [result] = await db.execute('DELETE FROM Usuario WHERE id_usuario = ?', [id]);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Usuario no encontrado para eliminar.' });
        }
        res.status(200).json({ message: 'Usuario eliminado con éxito.' });
    } catch (error) {
        console.error('Error al eliminar usuario:', error);
        res.status(500).json({ message: 'Error interno del servidor al eliminar usuario.' });
    }
};
