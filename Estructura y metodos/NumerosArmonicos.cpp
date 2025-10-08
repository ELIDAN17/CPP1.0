#include <iostream>
using namespace std;
double numArmRecur(int n) {
    if (n == 0) { return 0.0; } 
    else if (n < 0) {
        cout << "Error: El número armónico no existe para números negativos." << endl;
        return -1.0;
    } else { return 1.0 / n + numArmRecur(n - 1); }
}
int main() { int n;
    cout << "Ingrese el número limite de Armonico: "; cin >> n;
    cout << "Secuencia Armonica hasta " << n << ": ";
    int i = 1;
    double resultado = numArmRecur(n);
    if ( n<0 ) cout<<"No valido, inrese un valor positivo.";
    while (i <= n) {
        cout << numArmRecur(i) << " | ";
        i++;
    }
    cout << endl; cout << "El numero armonico en la posicion "<<n<<" es: "<<resultado<<endl;
    return 0;
}