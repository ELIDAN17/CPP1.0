const { Pool } = require('pg');
require('dotenv').config(); // Carga las variables del archivo .env

// Configuración del Pool de conexiones usando las variables secretas
const pool = new Pool({
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_DATABASE,
});

// Verificación inicial de la conexión
pool.query('SELECT NOW()', (err, res) => {
    if (err) {
        console.error('❌ Error crítico al conectar con PostgreSQL:', err.stack);
    } else {
        console.log('---');
        console.log('🚀 ¡Conexión exitosa a PostgreSQL establecida correctamente!');
        console.log(`📅 Hora del servidor BD: ${res.rows[0].now}`);
        console.log('---');
    }
});

// Exportamos el pool para usarlo de forma segura en los modelos
module.exports = {
    query: (text, params) => pool.query(text, params),
};