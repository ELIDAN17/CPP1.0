#include <iostream>
using namespace std;
long long numTrianRecur(int n) {
    if (n == 0) { return 0;} 
    else if (n < 0) {
        cout << "Error: El numero debe ser positivo." << endl;
        return -1;
    } else { cout<<n<<"+";
        return n + numTrianRecur(n - 1);
    }
}
int main() { int numero;
    cout << "Ingrese un número entero positivo: "; cin >> numero;
    int resultado = numTrianRecur(numero); cout<<endl;
    if (resultado != -1) {
        cout << "El número triangular de " << numero << " es: " << resultado << endl;
    } cout<<endl;
    cout<<"** Ahora por la formula n(n+1)/2 **"<<endl;
    int total = 0;
    for (int i = 1; i <= numero; i++) {cout << i <<"+";}
    total=(numero*(numero+1))/2;
    cout << "\nResultado final: " << total << endl;
    return 0;
}