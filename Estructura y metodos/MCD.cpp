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
int Euclidean(int x, int y, int &s, int &t) {
    if (y == 0) {
        s = 1;
        t = 0;
        return x;
    } else {
        int s1, t1;
        int gcd = Euclidean(y, x % y, s1, t1);
        s = t1;
        t = s1 - (x / y) * t1;
        return gcd;
    }
}
int main() {
    int num1, num2,s,t;
    cout << "Ingrese el primer número (x): "; cin >> num1;
    cout << "Ingrese el segundo número (y): "; cin >> num2;
    if (num1 < 0 || num2 < 0) {
        cout << "Error: Los números deben ser positivos." << endl;
        return 1;
    }
    int mcd = MCD(num1, num2);
    cout << "El Máximo Común Divisor (MCD) de " << num1 << " y " << num2 << " es: " << mcd << endl;
    int gcd = Euclidean(num1, num2, s, t);
    cout << "Los valores Euclideanos son: s="<<s<<" y t="<<t<<endl;
    return 0;
}