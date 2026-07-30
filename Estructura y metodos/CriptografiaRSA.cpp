#include <iostream>
using namespace std;
long long MCD(long long a, long long b) {
    while (b) {
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
long long modInverso(long long a, long long m) {
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
long long exponente(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp /= 2;
    }
    return res;
}
bool esPrimo(long long n) {
    if (n <= 1) return false;
    for (long long i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}
long long generarPrimo(long long min, long long max) {
    long long num = min;
    while (true) {
        if (esPrimo(num)) return num;
        num++;
        if (num > max) return -1;
    }
}
int main() {
    long long p = 23;//generarPrimo(100, 200);
    long long q = 31;//generarPrimo(201, 300);
    if (p == -1 || q == -1) {
        cout << "Error al generar numeros primos." << endl;
        return 1;
    }
    cout << "Primos elegidos: p = " << p << ", q = " << q << endl;
    long long n = p * q;//n = p*q.
    cout << "n = p * q = " << n << endl;    
    long long phi_n = (p - 1) * (q - 1);//φ(n) = (p-1)(q-1)
    cout << "phi(n) = (p-1)(q-1) = " << phi_n << endl;
    long long e = 29;//65537;
    while (MCD(e, phi_n) != 1) {
        e++;
        if (e >= phi_n) {
            cout << "Error finding a suitable e." << endl;
            return 1;
        }
    }
    cout << "Exponente público (e): " << e << endl;
    long long d = modInverso(e, phi_n);//invers0 e modulo φ(n).
    cout << "Exponente privado (d): " << d << endl;
    cout << "\nClave Pública (n, e): (" << n << ", " << e << ")" << endl;
    cout << "Clave Privada (n, d): (" << n << ", " << d << ")" << endl;
    long long mensaje;//encriptado
    cout << "\nIngrese el mensaje numérico a encriptar: ";
    cin >> mensaje;
    if (mensaje >= n) {
        cout << "Error: Mensaje debe ser menor que n (" << n << ")." << endl;
        return 1;
    }
    long long ciphertext = exponente(mensaje, e, n);
    cout << "Mensaje encriptado (c): " << ciphertext << endl;
    long long decrypted_message = exponente(ciphertext, d, n);//m = c^d mod n
    cout << "Mensaje descifrado (m): " << decrypted_message << endl;
    cout << "\nVerificación: Mensaje original = " << mensaje << ", Mensaje descifrado = " << decrypted_message << endl;
    return 0;
} 