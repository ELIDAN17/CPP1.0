#include <iostream>
using namespace std;
int MCD(int x, int y) {
    if (x < y) {
        int temp = x;
        x = y;
        y = temp;
    }
    while (y != 0) {
        int temp = y;
        y = x % y;
        x = temp;
    }
    return x;  
}
int MCM(int x, int y,int r){
    r=(x*y)/MCD(x,y);
    return r;
}
int main() {
    int num1, num2,s;
    cout << "Ingrese el primer número (x): "; cin >> num1;
    cout << "Ingrese el segundo número (y): "; cin >> num2;
    if (num1 < 0 || num2 < 0) {
        cout << "Error: Los números deben ser positivos." << endl;
        return 1;
    }
    int mcm = MCM(num1, num2,s);
    cout << "El Minimo Común Multiplo (MCM) de " << num1 << " y " << num2 << " es: " << mcm << endl;
    return 0;
}