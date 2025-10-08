#include <iostream>
using namespace std;
long long CuadradaRepetida(int a, int n) {
    long long resultado = 1;
    long long x = a;
    while (n > 0) {
        if (n % 2 == 1) {
            resultado = resultado * x;
        }
        x = x * x; 
        n = n / 2; cout<<x<<"^"<<n<<endl;
        
    }
    return resultado;
}
int main() { int a, n;
    cout << "Ingrese la base (a): "; cin >> a;
    cout << "Ingrese el exponente (n): "; cin >> n;
    if (n < 0) {
        cout << "El exponente debe ser un entero no negativo para esta función." << endl;
        return 1;
    }
    long long resultado = CuadradaRepetida(a, n); cout<<endl;
    cout << a << "^" << n << " = " << resultado << endl;
    return 0;
}