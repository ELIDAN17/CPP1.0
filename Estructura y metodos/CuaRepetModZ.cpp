#include <iostream>
using namespace std;
int cuadradoRepetMod(int a, int n, int z) {
    int resultado = 1;
    int x = a % z;
    while(n > 0) {
        if(n % 2 == 1) {
            resultado = (resultado*x) % z;
        }
        x = (x * x) % z;
        n = n / 2; cout<<x<<"^"<<n<<endl;
    }
    return resultado;
}
int main() { int a, n, z;
    cout << "Ingrese la base (a): "; cin >> a;
    cout << "Ingrese el exponente (n): "; cin >> n;
    cout << "Ingrese el Residuo (z): "; cin >> z;
    if(n < 0) {
        cout << "Los numeros ingresados deben ser positivos." << endl;
        return 1;
    }
    int resultado = cuadradoRepetMod(a, n, z);
    cout << resultado << endl;
    return 0;
}