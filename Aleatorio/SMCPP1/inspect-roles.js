const pool = require('./src/config/db');

async function inspect() {
    try {
        console.log("=== ROLES IN DATABASE ===");
        const resRoles = await pool.query("SELECT * FROM roles");
        console.log(resRoles.rows);

        console.log("\n=== COLUMNS IN bitacora_actividades ===");
        const resBitacoraCols = await pool.query(`
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'bitacora_actividades'
        `);
        console.log(resBitacoraCols.rows);

        console.log("\n=== EMPRESAS IN DATABASE ===");
        const resEmpresas = await pool.query("SELECT * FROM empresas");
        console.log(resEmpresas.rows);

    } catch (e) {
        console.error(e);
    }
}

inspect();
