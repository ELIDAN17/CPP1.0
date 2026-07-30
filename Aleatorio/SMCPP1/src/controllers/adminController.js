const pool = require('../config/db');
const authService = require('../services/authService');

// 1. Listar todos los usuarios con sus roles y nombres completos
const listarUsuarios = async (req, res) => {
    try {
        const query = `
            SELECT 
                u.id_usuario, 
                u.correo_institucional AS correo, 
                u.id_rol,
                r.nombre_rol,
                u.fecha_creacion,
                COALESCE(
                    e.nombres || ' ' || e.apellidos, 
                    a.nombres || ' ' || a.apellidos, 
                    t.nombres || ' ' || t.apellidos
                ) AS nombre_completo,
                COALESCE(e.codigo_estudiante, a.dni, t.dni) AS codigo
            FROM usuarios u
            LEFT JOIN roles r ON u.id_rol = r.id_rol
            LEFT JOIN estudiantes e ON u.id_usuario = e.id_usuario
            LEFT JOIN autoridades_academicas a ON u.id_usuario = a.id_usuario
            LEFT JOIN tutores_externos t ON u.id_usuario = t.id_usuario
            ORDER BY u.fecha_creacion DESC
        `;
        const resultado = await pool.query(query);
        return res.status(200).json(resultado.rows);
    } catch (error) {
        console.error("❌ Error al listar usuarios:", error.message);
        return res.status(500).json({ error: "Error interno del servidor al obtener la lista de usuarios." });
    }
};

// 2. Registrar un nuevo usuario (cualquier rol) desde el panel de administración
const crearUsuario = async (req, res) => {
    try {
        const nuevoUsuario = await authService.crearCuenta(req.body);
        return res.status(201).json({
            mensaje: "Usuario y perfil creados con éxito.",
            usuario: nuevoUsuario
        });
    } catch (error) {
        console.error("❌ Error al crear usuario desde Admin:", error.message);
        return res.status(400).json({ error: error.message });
    }
};

// 3. Eliminar un usuario de forma segura con transacciones
const eliminarUsuario = async (req, res) => {
    const { id_usuario } = req.params;

    // Evitar eliminarse a uno mismo
    if (id_usuario === req.usuario.id_usuario || id_usuario === req.usuario.idUsuario) {
        return res.status(400).json({ error: "No puedes eliminar tu propio usuario activo." });
    }

    const client = await pool.connect();
    try {
        await client.query('BEGIN');

        // Eliminar cascada manual en perfiles
        await client.query('DELETE FROM estudiantes WHERE id_usuario = $1', [id_usuario]);
        await client.query('DELETE FROM autoridades_academicas WHERE id_usuario = $1', [id_usuario]);
        await client.query('DELETE FROM tutores_externos WHERE id_usuario = $1', [id_usuario]);

        // Finalmente eliminar el usuario principal
        const resDelete = await client.query('DELETE FROM usuarios WHERE id_usuario = $1 RETURNING id_usuario', [id_usuario]);

        if (resDelete.rowCount === 0) {
            await client.query('ROLLBACK');
            return res.status(404).json({ error: "El usuario no existe o ya fue eliminado." });
        }

        await client.query('COMMIT');
        return res.status(200).json({ mensaje: "Usuario y sus datos asociados eliminados correctamente." });
    } catch (error) {
        await client.query('ROLLBACK');
        console.error("❌ Error al eliminar usuario:", error.message);
        return res.status(500).json({ error: "Error interno de base de datos al eliminar el usuario." });
    } finally {
        client.release();
    }
};

module.exports = {
    listarUsuarios,
    crearUsuario,
    eliminarUsuario
};
