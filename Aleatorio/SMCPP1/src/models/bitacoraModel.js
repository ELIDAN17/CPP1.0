const db = require('../config/db');

// Insertar una nueva actividad diaria en la bitácora
const insertarActividad = async (idPractica, fechaActividad, cantidadHoras, descripcionActividad) => {
    const query = `
        INSERT INTO bitacora_actividades (id_practica, fecha_actividad, cantidad_horas, descripcion_actividad)
        VALUES ($1, $2, $3, $4)
        RETURNING id_bitacora, fecha_actividad, cantidad_horas, estado_validacion
    `;
    const valores = [idPractica, fechaActividad, cantidadHoras, descripcionActividad];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Obtener todas las actividades registradas de una práctica específica
const obtenerActividadesPorPractica = async (idPractica) => {
    const query = `
        SELECT id_bitacora, fecha_actividad, cantidad_horas, descripcion_actividad, estado_validacion
        FROM bitacora_actividades
        WHERE id_practica = $1
        ORDER BY fecha_actividad DESC
    `;
    const resultado = await db.query(query, [idPractica]);
    return resultado.rows[0];
};

// Actualizar el estado de validación de una actividad (Tutor)
const revisarActividad = async (idBitacora, estado, observaciones) => {
    const query = `
        UPDATE bitacora_actividades
        SET estado_validacion = $1,
            observaciones_tutor = $2,
            fecha_revision = CURRENT_TIMESTAMP
        WHERE id_bitacora = $3
        RETURNING id_bitacora, id_practica, cantidad_horas, estado_validacion
    `;
    const resultado = await db.query(query, [estado, observaciones || null, idBitacora]);
    return resultado.rows[0];
};

module.exports = {
    insertarActividad,
    obtenerActividadesPorPractica,
    revisarActividad
};