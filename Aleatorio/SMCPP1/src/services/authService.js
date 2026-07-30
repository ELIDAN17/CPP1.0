const usuarioModel = require('../models/usuarioModel');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const crearCuenta = async (datosUsuario) => {
    const { correo, contrasena, idRol, codigoEstudiante, dni, nombres, apellidos, escuela, cargo, celular, cargoEmpresa, nombreEmpresa } = datosUsuario;

    // 1. VALIDACIÓN DE REGLA DE NEGOCIO: Formato de correo según el Rol
    if (idRol === 3) {
        const regexEstudiante = /^\d{8}@est\.unap\.edu\.pe$/;
        if (!regexEstudiante.test(correo)) {
            throw new Error('Para el rol de Estudiante, debes usar el correo institucional obligatorio de la UNA Puno (ejemplo: DNI@est.unap.edu.pe).');
        }
        // Validación extra: El DNI del correo debería coincidir con el DNI del campo de texto
        const dniCorreo = correo.split('@')[0];
        if (dniCorreo !== dni) {
            throw new Error('El DNI ingresado no coincide con el número de DNI de tu correo institucional.');
        }
    } else if (idRol === 2 || idRol === 5) {
        if (!correo.endsWith('@unap.edu.pe') || correo.includes('@est.')) {
            throw new Error('Para los roles de Coordinador o Decano, debes usar el correo institucional de docente (@unap.edu.pe).');
        }
    } else if (idRol === 1) {
        if (!correo.endsWith('@unap.edu.pe') && !correo.endsWith('@gmail.com')) {
            throw new Error('Para el rol de Administrador, utiliza un correo @unap.edu.pe o @gmail.com válido.');
        }
    }

    // 2. Validar si el correo ya existe
    const usuarioExistente = await usuarioModel.obtenerPorCorreo(correo);
    if (usuarioExistente) {
        throw new Error('Este correo electrónico ya se encuentra registrado en el sistema.');
    }

    // 3. Encriptar la contraseña
    const salt = await bcrypt.genSalt(10);
    const contrasenaHash = await bcrypt.hash(contrasena, salt);

    // 4. Guardar primero las credenciales en la tabla 'usuarios'
    const nuevoUsuario = await usuarioModel.insertarUsuario(correo, contrasenaHash, idRol);

    // 5. Si el usuario es un Estudiante, registramos de inmediato su perfil académico asociado
    if (idRol === 3) {
        const perfilEstudiante = await usuarioModel.insertarPerfilEstudiante(
            nuevoUsuario.id_usuario,
            codigoEstudiante,
            dni,
            nombres,
            apellidos,
            escuela || 'Ingeniería de Sistemas' // Valor por defecto para la EPIS
        );
        // Retornamos el objeto completo combinado
        return { ...nuevoUsuario, perfil: perfilEstudiante };

    } else if (idRol === 2 || idRol === 5) {
        // Autoridad: Coordinador (2) o Decano (5)
        // Definimos el cargo automáticamente si no lo envían
        const cargoDefinido = cargo || (idRol === 2 ? 'Coordinador EPIS' : 'Decano');
        const perfilAutoridad = await usuarioModel.insertarPerfilAutoridad(
            nuevoUsuario.id_usuario, dni, nombres, apellidos, cargoDefinido, celular || null
        );
        return { ...nuevoUsuario, perfil: perfilAutoridad };
        
    } else if (idRol === 4) {
        // Tutor Externo de Empresa
        const perfilTutor = await usuarioModel.insertarPerfilTutor(
            nuevoUsuario.id_usuario, dni, nombres, apellidos, cargoEmpresa || null, nombreEmpresa, celular || null
        );
        return { ...nuevoUsuario, perfil: perfilTutor };
    }

    return nuevoUsuario;
};  

const autenticar = async (correo, contrasena) => {
    // 1. Buscar el usuario por correo en la base de datos (Usa la query corregida con COALESCE)
    const usuarioBD = await usuarioModel.obtenerPorCorreo(correo);
    if (!usuarioBD) {
        throw new Error('El correo electrónico o la contraseña son incorrectos.');
    }

    // 2. Comparar la contraseña proporcionada con el hash almacenado
    const coinciden = await bcrypt.compare(contrasena, usuarioBD.contrasena_hash);
    if (!coinciden) {
        throw new Error('El correo electrónico o la contraseña son incorrectos.');
    }

    // 3. 🎯 PAYLOAD ROBUSTO PARA EL JWT: Insertamos los datos reales unificados de la BD
    const payload = { 
        id_usuario: usuarioBD.id_usuario, 
        id_rol: usuarioBD.id_rol,
        nombre_completo: usuarioBD.nombre_completo || 'Usuario del Sistema',
        codigo: usuarioBD.codigo || null
    };

    // Generar el token firmado
    const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '2h' });

    // 4. 🎯 RETORNO COMPATIBLE CON EL FRONTEND: Entregamos el objeto idéntico
    return { 
        mensaje: 'Inicio de sesión exitoso', 
        token, 
        usuario: { 
            id_usuario: usuarioBD.id_usuario, 
            correo: usuarioBD.correo, // Mapeado desde 'correo_institucional' en tu query
            id_rol: usuarioBD.id_rol, 
            nombre_completo: usuarioBD.nombre_completo || 'Usuario del Sistema', 
            codigo: usuarioBD.codigo || null
        } 
    };
};

module.exports = {
    crearCuenta,
    autenticar
};