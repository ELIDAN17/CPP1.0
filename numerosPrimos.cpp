#include <iostream>
using namespace std;
bool esPrimo(int n, int d) {
    if (n <= 1) { cout<<"Error: Ingrese un numero valido."<<endl;
        return false; }
    if (d * d > n) { 
        return true; }
    if (n % d == 0) {
        return false; }
    return esPrimo(n, d + 1);
}
void mostrarPrimos(int limite, int numActual) {
    if (numActual > limite) {
        return; }
    if (esPrimo(numActual, 2)) {
        cout << numActual << (numActual < limite); }
    mostrarPrimos(limite, numActual + 1);
}

int main() {
    int n; cout<< "Ingrese un numero para comprobar si es primo: "; cin>>n; 
    if (esPrimo(n,2)){ cout<<"El numero "<<n<<" es primo."<<endl;}
    else{cout<<"El numero "<<n<<" no es primo"<<endl;}
    cout << "Los primeros " << n << " números primos son: ";
    int numActual = 2, count = 0;
    while (count < n) {
        if (esPrimo(numActual, 2)) {
            cout << numActual << ", ";
            count++;
        }
        numActual++;
    } cout << endl;
    return 0;
}