// En tu src/controllers/bitacoraController.js
const pool = require('../config/db');

const verBitacoraEstudiante = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario; // Asegúrate de que coincida con cómo guardas el ID en tu JWT

        const resEstudiante = await pool.query(
            'SELECT id_estudiante FROM estudiantes WHERE id_usuario = $1',
            [idUsuarioUUID]
        );

        if (resEstudiante.rows.length === 0) {
            return res.status(404).json({ error: 'Perfil de estudiante no encontrado.' });
        }

        const idEstudiante = resEstudiante.rows[0].id_estudiante;

        const queryActividades = `
            SELECT b.* FROM bitacora_actividades b
            INNER JOIN practicas p ON b.id_practica = p.id_practica
            WHERE p.id_estudiante = $1
            ORDER BY b.fecha_actividad DESC
        `;
        const resBitacora = await pool.query(queryActividades, [idEstudiante]);

        // Forzamos a retornar siempre un JSON, aunque sea un array vacío []
        return res.status(200).json(resBitacora.rows);

    } catch (error) {
        return res.status(500).json({ error: 'Error interno del servidor', detalle: error.message });
    }
};

const registrarActividadDiaria = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;
        const { fecha, descripcion, horas } = req.body;

        if (!fecha || !descripcion || !horas) {
            return res.status(400).json({ error: 'Todos los campos son obligatorios.' });
        }

        // Buscar la práctica activa
        const queryPractica = `
            SELECT p.id_practica 
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            WHERE e.id_usuario = $1 AND p.estado_general = 'En Proceso'
            LIMIT 1
        `;
        const resPractica = await pool.query(queryPractica, [idUsuarioUUID]);

        if (resPractica.rows.length === 0) {
            return res.status(404).json({ error: 'No tienes ninguna práctica activa en proceso.' });
        }

        const idPractica = resPractica.rows[0].id_practica;

        // INSERT alineado exactamente a tu tabla SQL
        const queryInsertar = `
            INSERT INTO bitacora_actividades (id_practica, fecha_actividad, cantidad_horas, descripcion_actividad, estado_validacion)
            VALUES ($1, $2, $3, $4, 'Pendiente')
            RETURNING *
        `;
        const nuevaActividad = await pool.query(queryInsertar, [idPractica, fecha, horas, descripcion]);

        return res.status(201).json({
            mensaje: 'Actividad registrada con éxito.',
            actividad: nuevaActividad.rows[0]
        });

    } catch (error) {
        console.error("❌ Error al registrar actividad:", error);
        return res.status(500).json({ error: 'Error interno del servidor.' });
    }
};

module.exports = {
    verBitacoraEstudiante,
    registrarActividadDiaria
};