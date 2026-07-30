// backend-api/config/db.js
const mysql = require('mysql2/promise'); // Usamos la versión de promesas
require('dotenv').config(); // Carga las variables de entorno

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root', // Asegúrate de que este sea tu usuario de DB por defecto si no se carga del .env
    password: process.env.DB_PASSWORD || '', // Asegúrate de que esta sea tu contraseña de DB por defecto si no se carga del .env
    database: process.env.DB_NAME || 'MinimarketShop',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Función para probar la conexión a la base de datos
async function testDbConnection() {
    try {
        const connection = await pool.getConnection();
        console.log('Conexión a la base de datos MySQL exitosa!');
        connection.release(); // Liberar la conexión
    } catch (error) {
        console.error('Error al conectar a la base de datos MySQL:', error);
        process.exit(1); // Salir de la aplicación si no se puede conectar a la DB
    }
}

testDbConnection(); // Ejecutar la prueba de conexión al iniciar

module.exports = pool; // Exporta el pool de conexiones
