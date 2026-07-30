// src/controllers/notificacionController.js
const pool = require('../config/db');

// Obtener todas las notificaciones del usuario (priorizando las no leídas)
const obtenerNotificaciones = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;

        const query = `
            SELECT id_notificacion, titulo, mensaje, tipo, leido, fecha_creacion
            FROM notificaciones
            WHERE id_usuario = $1
            ORDER BY leido ASC, fecha_creacion DESC
            LIMIT 20
        `;
        const resultado = await pool.query(query, [idUsuarioUUID]);

        return res.status(200).json(resultado.rows);
    } catch (error) {
        console.error("❌ Error al obtener notificaciones:", error);
        return res.status(500).json({ error: 'Error interno al cargar las alertas.' });
    }
};

// Marcar una notificación específica como leída
const marcarComoLeida = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;
        const { id } = req.params;

        const query = `
            UPDATE notificaciones
            SET leido = true
            WHERE id_notificacion = $1 AND id_usuario = $2
            RETURNING id_notificacion
        `;
        const resultado = await pool.query(query, [id, idUsuarioUUID]);

        if (resultado.rows.length === 0) {
            return res.status(404).json({ error: 'Notificación no encontrada o no autorizada.' });
        }

        return res.status(200).json({ mensaje: 'Notificación actualizada con éxito.' });
    } catch (error) {
        console.error("❌ Error al actualizar notificación:", error);
        return res.status(500).json({ error: 'Error interno al procesar la operación.' });
    }
};

module.exports = {
    obtenerNotificaciones,
    marcarComoLeida
};