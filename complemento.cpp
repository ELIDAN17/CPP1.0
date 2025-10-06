#include <iostream>
#include <string>
using namespace std;
string invertirCadena(string s) {
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
string decimalABinario(int n, int nBits) {
    if (n == 0) return string(nBits, '0');
    string binarioInvertido = "";
    int valorAbsoluto = (n < 0) ? -n : n;
    while (valorAbsoluto > 0) {
        binarioInvertido += (valorAbsoluto % 2 == 0 ? '0' : '1');
        valorAbsoluto /= 2;
    }
    string binario = invertirCadena(binarioInvertido);
    while (binario.length() < nBits) {//aumenta 0 a los bits faltantes
        binario = "0" + binario;
    }
    if (n < 0) {
        string complementoUno = "";
        for (char bit : binario) { complementoUno += (bit == '0' ? '1' : '0'); }
        string complementoDos = complementoUno;
        int acarreo = 1;
        for (int i = complementoDos.length() - 1; i >= 0; --i) {
            if (complementoDos[i] == '0' && acarreo == 1) {
                complementoDos[i] = '1';
                acarreo = 0; break;
            } else if (complementoDos[i] == '1' && acarreo == 1) {
                complementoDos[i] = '0';
            }
        }
        binario = complementoDos;
    }
    return binario;
}
string sumarBinario(string bin1, string bin2) {
    int nBits = bin1.length();
    if (nBits != bin2.length()) { return "Error: Las longitudes binarias deben ser iguales."; }
    string resultadoInvertido = ""; int acarreo = 0;
    for (int i = nBits - 1; i >= 0; --i) {
        int bit1 = bin1[i] - '0';
        int bit2 = bin2[i] - '0';
        int suma = bit1 + bit2 + acarreo;
        resultadoInvertido += (suma % 2 == 0 ? "0" : "1");
        acarreo = suma / 2;
    }
    string resultado = invertirCadena(resultadoInvertido);
    return resultado;
}
int binarioADecimalConSigno(string binario, int nBitsAsumidos) {
    int longitudBinario = binario.length();
    if (longitudBinario == 0) return 0;
    string subBinario = binario.substr(max(0, longitudBinario - nBitsAsumidos));//bits insignificativos
    int nBitsEfectivos = subBinario.length();
    int decimal = 0;
    if (subBinario[0] == '1') {// Negativo (complemento a dos)
        string complementoUno = "";
        for (int i = 0; i < nBitsEfectivos; ++i) {
            complementoUno += (subBinario[i] == '0' ? '1' : '0');
        }
        string complementoDos = complementoUno;
        int acarreo = 1;
        for (int i = nBitsEfectivos - 1; i >= 0; --i) {
            if (complementoDos[i] == '0' && acarreo == 1) {
                complementoDos[i] = '1';
                acarreo = 0; break;
            } else if (complementoDos[i] == '1' && acarreo == 1) {
                complementoDos[i] = '0';
            }
        }
        cout<<"Suma binaria Final C2: "<<complementoDos<<endl;
        int valor = 0, potencia = 1;
        for (int i = nBitsEfectivos - 1; i > 0; --i) {
            if (complementoDos[i] == '1') { valor += potencia; }
            potencia *= 2;
        }
        decimal = -(valor + 1);
    } else {
        int potencia = 1;//positivo
        for (int i = nBitsEfectivos - 1; i >= 0; --i) {
            if (subBinario[i] == '1') { decimal += potencia; }
            potencia *= 2;
        }
    }
    return decimal;
}
int main() {
    int num1, num2, nBitsAsignados;
    cout << "Ingrese el número de bits que desee (n): "; cin >> nBitsAsignados;
    cout << "Ingrese el primer número: "; cin >> num1;
    cout << "Ingrese el segundo número: "; cin >> num2;
    string bin1 = decimalABinario(num1, nBitsAsignados);
    string bin2 = decimalABinario(num2, nBitsAsignados);
    cout << "Binario (" << nBitsAsignados << " bits, " << num1 << "): " << bin1 << endl;
    cout << "Binario (" << nBitsAsignados << " bits, " << num2 << "): " << bin2 << endl;
    string suma = sumarBinario(bin1, bin2);
    cout << "Suma binaria (" << suma.length() << " bits): " << suma << endl;
    int sumaB = binarioADecimalConSigno(suma, nBitsAsignados);
    int sumaD = (int)num1 + num2;
    cout << "Suma decimal: " << sumaD << endl;
    if (suma.length() > nBitsAsignados) {
        cout << "**Desvordamiento**" << endl;
    }
    return 0;
}