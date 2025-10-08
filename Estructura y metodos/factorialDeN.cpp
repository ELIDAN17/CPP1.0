#include <iostream>
using namespace std;
long long facRecursivo(int n) {
    if (n == 0) { return 1; } //fac de 0 es 1
    else if (n < 0) {
        cout << "Error: El factorial no existe para números negativos." << endl;
        return -1;
    } else {cout<<n<<"*"; return n * facRecursivo(n - 1); }//fac(n)=n*fac(n-1)
}
int main() { int numero;
    cout << "Ingrese un número positivo: "; cin >> numero;
    long long resultado = facRecursivo(numero); cout<<endl;
    if (resultado != -1) {
        cout << "El factorial de " << numero << " es: " << resultado << endl;
    }
    return 0;
}