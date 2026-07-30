const db = require('../config/db');

// Insertar una nueva práctica preprofesional
const crearPractica = async (datosPractica) => {
    const {
        idEstudiante, idEmpresa, idTutor, idCoordinador,
        tipoPractica, fechaInicio, fechaFinEstimada, horasRequeridas
    } = datosPractica;

    const query = `
        INSERT INTO practicas (
            id_estudiante, id_empresa, id_tutor, id_coordinador, 
            tipo_practica, fecha_inicio, fecha_fin_estimada, horas_requeridas
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id_practica, tipo_practica, fecha_inicio, horas_requeridas, estado_general
    `;

    const valores = [
        idEstudiante, idEmpresa, idTutor, idCoordinador,
        tipoPractica, fechaInicio, fechaFinEstimada, horasRequeridas || 600
    ];

    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Obtener la práctica activa de un estudiante por su ID de perfil estudiantil
const obtenerPracticaPorEstudiante = async (idEstudiante) => {
    const query = `
        SELECT id_practica, id_empresa, tipo_practica, horas_acumuladas, horas_requeridas, estado_general 
        FROM practicas 
        WHERE id_estudiante = $1 AND estado_general = 'En Proceso'
    `;
    const resultado = await db.query(query, [idEstudiante]);
    return resultado.rows[0];
};

// Sumar horas acumuladas a una práctica específica
const acumularHoras = async (idPractica, horasASumar) => {
    const query = `
        UPDATE practicas 
        SET horas_acumuladas = horas_acumuladas + $1 
        WHERE id_practica = $2
        RETURNING id_practica, horas_acumuladas, horas_requeridas
    `;
    const resultado = await db.query(query, [horasASumar, idPractica]);
    return resultado.rows[0];
};

// Obtener el estado detallado del progreso de un estudiante para su Dashboard
const obtenerProgresoDetallado = async (idEstudiante) => {
    const query = `
        SELECT 
            p.id_practica,
            p.tipo_practica,
            p.horas_acumuladas,
            p.horas_requeridas,
            p.estado_general,
            e.nombres,
            e.apellidos,
            e.codigo_estudiante,
            em.razon_social AS empresa,
            (SELECT COUNT(*) FROM bitacora_actividades WHERE id_practica = p.id_practica) AS total_actividades,
            (SELECT COUNT(*) FROM documentos_practica WHERE id_practica = p.id_practica AND estado_aprobacion = 'Aprobado') AS documentos_aprobados
        FROM practicas p
        INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
        INNER JOIN empresas em ON p.id_empresa = em.id_empresa
        WHERE p.id_estudiante = $1 AND p.estado_general = 'En Proceso'
        LIMIT 1;
    `; 
    const resultado = await db.query(query, [idEstudiante]);
    return resultado.rows[0];
};

// Obtener panel general para el Coordinador Académico
const listarPracticasParaCoordinador = async (idCoordinador) => {
    const query = `
        SELECT 
            p.id_practica,
            est.codigo_estudiante,
            est.nombres || ' ' || est.apellidos AS estudiante,
            emp.razon_social AS empresa,
            p.tipo_practica,
            p.horas_acumuladas,
            p.estado_general
        FROM practicas p
        JOIN estudiantes est ON p.id_estudiante = est.id_estudiante
        JOIN empresas emp ON p.id_empresa = emp.id_empresa
        WHERE p.id_coordinador = $1
        ORDER BY p.fecha_inicio DESC
    `;
    const resultado = await db.query(query, [idCoordinador]);
    return resultado.rows;
};

module.exports = {
    crearPractica,
    obtenerPracticaPorEstudiante,
    acumularHoras,
    obtenerProgresoDetallado,
    listarPracticasParaCoordinador
};