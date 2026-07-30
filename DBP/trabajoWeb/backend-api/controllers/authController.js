// backend-api/controllers/authController.js
const db = require('../config/db');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
require('dotenv').config(); // Asegúrate de cargar .env aquí también

// Función para registrar un nuevo usuario
exports.registerUser = async (req, res) => {
    const { correo, contraseña, nombre, apellido, telefono, rol } = req.body;

    if (!correo || !contraseña || !nombre || !apellido) {
        return res.status(400).json({ message: 'Todos los campos obligatorios (correo, contraseña, nombre, apellido) deben ser proporcionados.' });
    }

    try {
        const [existingUsers] = await db.execute('SELECT id_usuario FROM Usuario WHERE correo = ?', [correo]);
        if (existingUsers.length > 0) {
            return res.status(409).json({ message: 'El correo electrónico ya está registrado.' });
        }

        const hashedPassword = await bcrypt.hash(contraseña, 10); // Costo de salado 10

        const [result] = await db.execute(
            `INSERT INTO Usuario (correo, contraseña, nombre, apellido, telefono, rol, fecha_creacion)
             VALUES (?, ?, ?, ?, ?, ?, NOW())`,
            [correo, hashedPassword, nombre, apellido, telefono || null, rol || 'cliente']
        );

        const newUserId = result.insertId;

        const token = jwt.sign(
            { id_usuario: newUserId, correo: correo, rol: rol || 'cliente' },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.status(201).json({
            message: 'Usuario registrado exitosamente.',
            token: token,
            user: {
                id_usuario: newUserId,
                correo: correo,
                nombre: nombre,
                apellido: apellido,
                rol: rol || 'cliente'
            }
        });

    } catch (error) {
        console.error('Error al registrar usuario:', error);
        res.status(500).json({ message: 'Error interno del servidor al registrar usuario.' });
    }
};

// Función para iniciar sesión
exports.loginUser = async (req, res) => {
    const { correo, contraseña } = req.body;

    if (!correo || !contraseña) {
        return res.status(400).json({ message: 'Se requiere correo y contraseña.' });
    }

    try {
        const [users] = await db.execute('SELECT id_usuario, correo, contraseña, nombre, apellido, rol FROM Usuario WHERE correo = ?', [correo]);

        if (users.length === 0) {
            return res.status(401).json({ message: 'Credenciales inválidas.' });
        }

        const user = users[0];

        const isMatch = await bcrypt.compare(contraseña, user.contraseña);

        if (!isMatch) {
            return res.status(401).json({ message: 'Credenciales inválidas.' });
        }

        const token = jwt.sign(
            { id_usuario: user.id_usuario, rol: user.rol },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.status(200).json({
            message: 'Inicio de sesión exitoso.',
            token: token,
            user: {
                id_usuario: user.id_usuario,
                correo: user.correo,
                nombre: user.nombre,
                apellido: user.apellido,
                rol: user.rol
            }
        });
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
        res.status(500).json({ message: 'Error interno del servidor.' });
    }
};
