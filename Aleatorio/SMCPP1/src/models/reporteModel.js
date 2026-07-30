const db = require('../config/db');

const obtenerMetricasCoordinador = async (idUsuario) => {
    // Primero obtenemos el id_autoridad correspondiente a ese id_usuario
    const authQuery = 'SELECT id_autoridad FROM autoridades_academicas WHERE id_usuario = $1';
    const authRes = await db.query(authQuery, [idUsuario]);
    
    if (authRes.rows.length === 0) return { total_postulantes: 0, practicas_aceptadas: 0, solicitudes_pendientes: 0 };
    const idCoordinador = authRes.rows[0].id_autoridad;

    // Ejecutamos el conteo real sobre la tabla de prácticas
    const query = `
        SELECT 
            COUNT(*)::INT AS total_postulantes,
            COUNT(CASE WHEN estado_general = 'Finalizado' THEN 1 END)::INT AS practicas_aceptadas,
            COUNT(CASE WHEN estado_general = 'En Proceso' THEN 1 END)::INT AS solicitudes_pendientes
        FROM practicas
        WHERE id_coordinador = $1
    `;
    const resultado = await db.query(query, [idCoordinador]);
    return resultado.rows[0];
};

module.exports = { obtenerMetricasCoordinador };