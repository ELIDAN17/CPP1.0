// ARCHIVO: backend/controllers/tutorController.js
const pool = require('../config/db'); // Conexión a PostgreSQL

// 1. Obtener los estudiantes asignados al tutor logueado
const obtenerEstudiantesAsignados = async (req, res) => {
    try {
        // Obtenemos el id_usuario desde el token (verificarToken)
        const id_usuario_tutor = req.usuario.idUsuario || req.usuario.id_usuario;

        // Buscamos el id_tutor correspondiente a este usuario
        const queryTutor = `SELECT id_tutor FROM tutores_externos WHERE id_usuario = $1`;
        const resTutor = await pool.query(queryTutor, [id_usuario_tutor]);

        if (resTutor.rows.length === 0) {
            return res.status(404).json({ error: "No se encontró el registro de tutor para este usuario." });
        }

        const id_tutor = resTutor.rows[0].id_tutor;

        // Traemos las prácticas de los estudiantes asignados a este tutor
        const queryEstudiantes = `
            SELECT 
                p.id_practica,
                p.estado_general,
                p.horas_requeridas,
                p.tipo_practica,
                e.codigo_estudiante,
                (e.nombres || ' ' || e.apellidos) AS estudiante_nombre,
                -- Sumamos las horas acumuladas usando la columna real 'cantidad_horas'
                COALESCE((
                    SELECT SUM(ba.cantidad_horas) 
                    FROM bitacora_actividades ba 
                    WHERE ba.id_practica = p.id_practica 
                      AND ba.estado_validacion = 'Aprobado'
                ), 0) AS horas_acumuladas
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            WHERE p.id_tutor = $1
            ORDER BY estudiante_nombre ASC;
        `;

        const resEstudiantes = await pool.query(queryEstudiantes, [id_tutor]);
        return res.status(200).json(resEstudiantes.rows);

    } catch (error) {
        console.error("❌ Error al obtener estudiantes del tutor:", error.message);
        return res.status(500).json({ error: "Error interno del servidor." });
    }
};

// 2. Obtener la bitácora de actividades de un estudiante específico
const obtenerBitacoraEstudiante = async (req, res) => {
    try {
        const { id_practica } = req.params;

        // Mapeamos 'id_bitacora' como 'id_actividad' para mantener compatibilidad con el Frontend
        const queryBitacora = `
            SELECT 
                id_bitacora AS id_actividad, 
                id_practica,
                fecha_actividad,
                cantidad_horas,
                descripcion_actividad,
                estado_validacion,
                observaciones_tutor,
                fecha_revision
            FROM bitacora_actividades
            WHERE id_practica = $1
            ORDER BY fecha_actividad DESC;
        `;

        const resBitacora = await pool.query(queryBitacora, [id_practica]);
        return res.status(200).json(resBitacora.rows);

    } catch (error) {
        console.error("❌ Error al obtener bitácora:", error.message);
        return res.status(500).json({ error: "Error interno del servidor." });
    }
};

// 3. Validar (Aprobar u Observar) una actividad de la bitácora usando 'id_bitacora'
const validarActividadBitacora = async (req, res) => {
    try {
        const { id_actividad } = req.params; // Viene en la URL como parámetro
        const { estado_validacion, observaciones_tutor } = req.body;

        // Validamos que el estado enviado sea correcto según el dominio
        if (!['Aprobado', 'Observado', 'Pendiente'].includes(estado_validacion)) {
            return res.status(400).json({ error: "Estado de validación no permitido." });
        }

        // Actualizamos usando la columna real de la BD: id_bitacora
        const queryValidar = `
            UPDATE bitacora_actividades
            SET 
                estado_validacion = $1,
                observaciones_tutor = $2,
                fecha_revision = CURRENT_TIMESTAMP
            WHERE id_bitacora = $3
            RETURNING id_bitacora AS id_actividad, estado_validacion, observaciones_tutor;
        `;

        const resultado = await pool.query(queryValidar, [estado_validacion, observaciones_tutor || null, id_actividad]);

        if (resultado.rows.length === 0) {
            return res.status(404).json({ error: "No se encontró la actividad especificada." });
        }

        return res.status(200).json({ 
            mensaje: "Actividad evaluada con éxito.", 
            actividad: resultado.rows[0] 
        });

    } catch (error) {
        console.error("❌ Error al validar actividad:", error.message);
        return res.status(500).json({ error: "Error interno del servidor." });
    }
};

module.exports = {
    obtenerEstudiantesAsignados,
    obtenerBitacoraEstudiante,
    validarActividadBitacora
};