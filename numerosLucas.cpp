#include <iostream>
using namespace std;
long long lucasRecur(int n) {
    if (n == 0) {
        return 2;
    } else if (n == 1) {
        return 1;
    } else if (n < 0) {
        cout << "Error: El numero de Lucas no puede ser negativo." << endl;
        return -1;
    } else {// L(n) = L(n-1) + L(n-2)
        return lucasRecur(n - 1) + lucasRecur(n - 2);
    }
}
int main() { int n;
    cout << "Ingrese el número limite de Lucas: "; cin >> n;
    cout << "Secuencia Luca hasta " << n << ": ";
    int i = 1;
    long long resultado = lucasRecur(n);
    if ( n<0 ) cout<<"No valido, inrese un valor positivo.";
    while (i <= n) {
        cout << lucasRecur(i) << " | ";
        i++;
    }
    if (resultado != -1) {
        cout << "\nEl número de Lucas en la posicion " << n << " es: " << resultado << endl;
    }
    return 0;
}
