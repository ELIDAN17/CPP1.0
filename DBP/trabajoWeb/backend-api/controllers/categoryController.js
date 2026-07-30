// backend-api/controllers/categoryController.js
const connection = require('../config/db'); // Asegúrate que la ruta a tu archivo 'db.js' sea correcta

// Función para obtener todas las categorías
exports.getAllCategories = async (req, res) => {
    try {
        // La consulta SQL selecciona todas las columnas de tu tabla Categoria
        // CORREGIDO: Ahora selecciona 'nombre' directamente, sin alias, para que coincida con el frontend
        const [rows] = await connection.execute('SELECT id_categoria, nombre FROM Categoria');
        
        // Si todo va bien, envía las categorías como respuesta JSON
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener categorías:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener categorías.' });
    }
};

// Puedes añadir otras funciones de categorías aquí (ej. getCategoryById, addCategory, etc.)
