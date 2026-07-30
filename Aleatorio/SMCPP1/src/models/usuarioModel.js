const db = require('../config/db');

const obtenerPorCorreo = async (correo) => {
    const query = `
        SELECT 
            u.id_usuario, 
            u.correo_institucional AS correo, 
            u.contrasena_hash, 
            u.id_rol,
            -- 🎯 Juntamos nombres y apellidos reales buscando en cascada en las 3 tablas
            COALESCE(
                e.nombres || ' ' || e.apellidos, 
                a.nombres || ' ' || a.apellidos, 
                t.nombres || ' ' || t.apellidos
            ) AS nombre_completo,
            -- 🎯 Juntamos el identificador o código disponible (Código o DNI)
            COALESCE(e.codigo_estudiante, a.dni, t.dni) AS codigo
        FROM usuarios u
        LEFT JOIN estudiantes e ON u.id_usuario = e.id_usuario
        LEFT JOIN autoridades_academicas a ON u.id_usuario = a.id_usuario
        LEFT JOIN tutores_externos t ON u.id_usuario = t.id_usuario
        WHERE u.correo_institucional = $1
    `;
    const resultado = await db.query(query, [correo]);
    return resultado.rows[0];
};

// Retorna el UUID generado de forma nativa por PostgreSQL al insertar un nuevo usuario
const insertarUsuario = async (correo, contrasena_hash, idRol) => {
    const query = 'INSERT INTO usuarios (correo_institucional, contrasena_hash, id_rol) VALUES ($1, $2, $3) RETURNING id_usuario, correo_institucional, id_rol, fecha_creacion';
    const valores = [correo, contrasena_hash, idRol];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Insertar el perfil detallado del estudiante vinculado a su id_usuario
const insertarPerfilEstudiante = async (idUsuario, codigoEstudiante, dni, nombres, apellidos, escuela) => {
    const query = `
        INSERT INTO estudiantes (id_usuario, codigo_estudiante, dni, nombres, apellidos, escuela_profesional)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id_estudiante, codigo_estudiante, nombres, apellidos
    `;
    const valores = [idUsuario, codigoEstudiante, dni, nombres, apellidos, escuela];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Insertar perfil de Autoridad Académica (Coordinador / Decano)
const insertarPerfilAutoridad = async (idUsuario, dni, nombres, apellidos, cargo, celular) => {
    const query = `
        INSERT INTO autoridades_academicas (id_usuario, dni, nombres, apellidos, cargo, celular)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id_autoridad, cargo, nombres, apellidos
    `;
    const valores = [idUsuario, dni, nombres, apellidos, cargo, celular];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Insertar perfil de Tutor Externo (Empresa)
const insertarPerfilTutor = async (idUsuario, dni, nombres, apellidos, cargoEmpresa, nombreEmpresa, celular) => {
    const query = `
        INSERT INTO tutores_externos (id_usuario, dni, nombres, apellidos, cargo_empresa, nombre_empresa, celular)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id_tutor, nombre_empresa, nombres, apellidos
    `;
    const valores = [idUsuario, dni, nombres, apellidos, cargoEmpresa, nombreEmpresa, celular];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

module.exports = {
    obtenerPorCorreo,
    insertarUsuario,
    insertarPerfilEstudiante,
    insertarPerfilAutoridad,
    insertarPerfilTutor 
};
