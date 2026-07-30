/*#include <iostream>
using namespace std;

// Función para encontrar el máximo común divisor (gcd)
long long gcd(long long a, long long b) {
    while (b) {
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Función para calcular el inverso modular
long long modInverse(long long a, long long m) {
    long long m0 = m, y = 0, x = 1;
    if (m == 1) return 0;

    while (a > 1) {
        long long q = a / m;
        long long t = m;
        m = a % m, a = t;
        t = y;
        y = x - q * y;
        x = t;
    }

    if (x < 0) x += m0;
    return x;
}

// Función para calcular (base^exp) % mod de manera eficiente
long long power(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp /= 2;
    }
    return res;
}

// Función para factorizar n (solo funciona eficientemente para números pequeños)
bool factorize(long long n, long long& p, long long& q) {
    // Busca factores primos comenzando desde 2
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            p = i;
            q = n / i;
            return true;
        }
    }
    return false; // No se encontraron factores (posiblemente n es primo)
}

int main() {
    // Entrada: clave pública (n, e) y el mensaje cifrado c
    long long n, e, cifrado;
    
    cout << "Ingrese el valor de n (producto de dos primos): ";
    cin >> n;
    
    cout << "Ingrese el exponente público (e): ";
    cin >> e;
    
    cout << "Ingrese el mensaje cifrado: ";
    cin >> cifrado;
    
    // Paso 1: Factorizar n para obtener p y q
    long long p, q;
    if (!factorize(n, p, q)) {
        cout << "No se pudo factorizar n. Este algoritmo solo funciona para valores pequeños." << endl;
        return 1;
    }
    
    // Paso 2: Calcular φ(n) = (p-1)(q-1)
    long long phi_n = (p - 1) * (q - 1);
    
    // Paso 3: Calcular la clave privada d como el inverso modular de e mod φ(n)
    long long d = modInverse(e, phi_n);
    
    // Paso 4: Descifrar el mensaje usando m = c^d mod n
    long long mensaje_original = power(cifrado, d, n);
    
    // Mostrar resultados
    cout << "\nResultados del ataque:" << endl;
    cout << "Factorización de n = " << n << ":" << endl;
    cout << "p = " << p << ", q = " << q << endl;
    cout << "φ(n) = " << phi_n << endl;
    cout << "Clave privada calculada (d): " << d << endl;
    cout << "Mensaje original descifrado: " << mensaje_original << endl;
    
    return 0;
}*/


#include <iostream>
using namespace std;

// Función para calcular el máximo común divisor (GCD)
long long gcd(long long a, long long b) {
    while (b) {
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Función para obtener valor absoluto
long long abs_val(long long x) {
    return x < 0 ? -x : x;
}

// Función de iteración para Pollard Rho f(x) = (x^2 + c) % n
long long f(long long x, long long c, long long n) {
    return (((x * x) % n) + c) % n;
}

// Algoritmo de Pollard Rho para factorización
long long pollardRho(long long n) {
    // Si n es par, retornar 2 como factor
    if (n % 2 == 0)
        return 2;
    
    // Valores iniciales sin aleatoriedad
    long long x = 2;  // Valor inicial para x
    long long y = 2;  // Valor inicial para y
    long long c = 1;  // Constante para la función f(x)
    long long d = 1;
    
    // Bucle principal de Pollard Rho
    while (d == 1) {
        // Tortoise move (paso simple)
        x = f(x, c, n);
        
        // Hare move (paso doble)
        y = f(f(y, c, n), c, n);
        
        // Calcular GCD de |x-y| y n
        d = gcd(abs_val(x - y), n);
        
        // Si encontramos un factor no trivial
        if (d != 1 && d != n)
            return d;
        
        // Si caemos en un ciclo sin encontrar factor, reiniciar con nuevos valores
        if (d == n) {
            x = x + 1;  // Incrementar x para intentar con otro valor
            y = x;
            c = c + 1;  // Cambiar la constante
            d = 1;
        }
    }
    
    return d;
}

// Función para calcular el inverso modular (para la clave privada)
long long modInverse(long long a, long long m) {
    long long m0 = m, y = 0, x = 1;
    if (m == 1) return 0;
    
    while (a > 1) {
        long long q = a / m;
        long long t = m;
        m = a % m, a = t;
        t = y;
        y = x - q * y;
        x = t;
    }
    
    if (x < 0) x += m0;
    return x;
}

// Exponenciación modular rápida
long long power(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp /= 2;
    }
    return res;
}

int main() {
    // Entrada: clave pública (n, e) y el mensaje cifrado
    long long n, e, cifrado;
    
    cout << "Ingrese el valor de n (producto de dos primos): ";
    cin >> n;
    
    cout << "Ingrese el exponente público (e): ";
    cin >> e;
    
    cout << "Ingrese el mensaje cifrado: ";
    cin >> cifrado;
    
    // Paso 1: Factorizar n usando Pollard Rho para encontrar p
    cout << "\nFactorizando n usando Pollard Rho..." << endl;
    long long p = pollardRho(n);
    
    if (p == n) {
        cout << "No se pudo factorizar n. Intente de nuevo." << endl;
        return 1;
    }
    
    // Calcular q = n/p
    long long q = n / p;
    
    cout << "Factorización exitosa!" << endl;
    cout << "p = " << p << ", q = " << q << endl;
    
    // Paso 2: Calcular φ(n) = (p-1)(q-1)
    long long phi_n = (p - 1) * (q - 1);
    cout << "φ(n) = (p-1)(q-1) = " << phi_n << endl;
    
    // Paso 3: Calcular la clave privada d como el inverso modular de e mod φ(n)
    long long d = modInverse(e, phi_n);
    cout << "Clave privada calculada (d): " << d << endl;
    
    // Paso 4: Descifrar el mensaje usando m = c^d mod n
    long long mensaje_original = power(cifrado, d, n);
    
    cout << "\nMensaje original descifrado: " << mensaje_original << endl;
    
    return 0;
}