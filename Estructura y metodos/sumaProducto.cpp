#include <iostream>
#include <string>
using namespace std;
int EvaluaDigito(char c) { //usando ASCII
    if (c >= '0' && c <= '9') { return c - '0'; }
    else if (c >= 'A' && c <= 'F') { return c - 'A' + 10; }
    return -1;
}
char RevierteDigito(int v) {//usando ASCII
    if (v >= 0 && v <= 9) { return v + '0'; }
    else if (v >= 10 && v <= 15) { return v - 10 + 'A'; }
    return '\0';
}
int potencia(int base, int exp) { int res = 1;
    for (int i = 0; i < exp; i++) { res *= base; }
    return res;
}
int Decimal(const string& n, int baseDe) { int evaluaDecimal = 0;
    for (int i = 0; i < n.length(); i++) {
        int valorDigito = EvaluaDigito(n[n.length() - 1 - i]);
        if (valorDigito == -1 || valorDigito >= baseDe) {
            cout << "Error: Dígito inválido o mayor que la base de origen" << endl;
            return -1;
        }
        evaluaDecimal += valorDigito * potencia(baseDe, i);
    }
    return evaluaDecimal;
}
string revertir(string s) {
    string resultado = s;
    int izquierda = 0, derecha = resultado.length() - 1;
    while (izquierda < derecha) {
        char temp = resultado[izquierda];
        resultado[izquierda] = resultado[derecha];
        resultado[derecha] = temp;
        izquierda++;
        derecha--;
    }
    return resultado;
}
string baseX(int evaluaDecimal, int xBase) {
    if (evaluaDecimal == 0) { return "0"; }
    string resultado = "";
    while (evaluaDecimal > 0) {
        int residuo = evaluaDecimal % xBase;
        resultado += RevierteDigito(residuo);
        evaluaDecimal /= xBase;
    }
    return revertir(resultado); // Invertir el resultado antes de retornarlo
}
string sumar(string num1, int base1, string num2, int base2, int baseResultado) {
    int dec1 = Decimal(num1, base1);//convierte a decimal
    int dec2 = Decimal(num2, base2);
    if (dec1 == -1 || dec2 == -1) {
        return "Error en la conversión";
    }
    int suma = dec1 + dec2;
    return baseX(suma, baseResultado);//decimal a otra base
}
string multiplicar(string num1, int base1, string num2, int base2, int baseResultado) {
    int dec1 = Decimal(num1, base1);
    int dec2 = Decimal(num2, base2);
    if (dec1 == -1 || dec2 == -1) {
        return "Error en la conversión";
    }
    int producto = dec1 * dec2;
    return baseX(producto, baseResultado);
}
int main() {
    string num1, num2;
    int base1, base2, baseResultado;
    cout << "Ingrese el primer número: "; cin >> num1;
    cout << "Ingrese la base del primer número (2-16): "; cin >> base1;
    cout << "Ingrese el segundo número: "; cin >> num2;
    cout << "Ingrese la base del segundo número (2-16): "; cin >> base2;
    cout << "Ingrese la base para el resultado (2-16): "; cin >> baseResultado;
    if (base1 < 2 || base1 > 16 || base2 < 2 || base2 > 16 || baseResultado < 2 || baseResultado > 16) {
        cout << "Error: Las bases deben estar entre 2 y 16." << endl;
        return 1;
    }
    string suma = sumar(num1, base1, num2, base2, baseResultado);
    string producto = multiplicar(num1, base1, num2, base2, baseResultado);
    cout << "Suma: " << suma << endl;
    cout << "Producto: " << producto << endl;
    return 0;
}