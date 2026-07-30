const bcrypt = require('bcryptjs');
const saltRounds = 10; // Debe ser el mismo que usas en tu authController.js

async function generateHashes() {
    const clientPass = 'cliente123'; // Contraseña para el cliente
    const vendorPass1 = 'vendedor123'; // Contraseña para el Vendedor Uno
    const vendorPass2 = 'vendedor456'; // Contraseña para el Vendedor Dos

    const hashedClientPass = await bcrypt.hash(clientPass, saltRounds);
    const hashedVendorPass1 = await bcrypt.hash(vendorPass1, saltRounds);
    const hashedVendorPass2 = await bcrypt.hash(vendorPass2, saltRounds);

    console.log('--- Hashes Generados ---');
    console.log('Cliente (cliente@example.com) - Contraseña:', clientPass, 'Hash:', hashedClientPass);
    console.log('Vendedor Uno (vendedor1@example.com) - Contraseña:', vendorPass1, 'Hash:', hashedVendorPass1);
    console.log('Vendedor Dos (vendedor2@example.com) - Contraseña:', vendorPass2, 'Hash:', hashedVendorPass2);
    console.log('------------------------');
}
generateHashes();