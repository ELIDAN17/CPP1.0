#include <iostream>
#include <string>
using namespace std;
int EvaluaDigito(char c)
{
    if (c >= '0' && c <= '9')
    {
        return c - '0';
    }
    else if (c >= 'A' && c <= 'F')
    {
        return c - 'A' + 10;
    }
    return -1;
}
char RevierteDigito(int v)
{
    if (v >= 0 && v <= 9)
    {
        return v + '0';
    }
    else if (v >= 10 && v <= 15)
    {
        return v - 10 + 'A';
    }
    return -1;
}
double potencia(int base, int exp)
{
    double resul = 1.0;
    for (int i = 0; i < exp; i++)
    {
        resul *= base;
    }
    return resul;
}
string revertir(string s)
{
    string resultado = s;
    int izquierda = 0, derecha = resultado.length() - 1;
    while (izquierda < derecha)
    {
        char temp = resultado[izquierda];
        resultado[izquierda] = resultado[derecha];
        resultado[derecha] = temp;
        izquierda++;
        derecha--;
    }
    return resultado;
}
double FraccionalADecimal(const string &n, int baseDe)
{
    double valorDecimal = 0.0;
    for (int i = 0; i < n.length(); i++)
    {
        int valorDigito = EvaluaDigito(n[i]);
        if (valorDigito == -1 || valorDigito >= baseDe)
        {
            return -1.0;
        }
        valorDecimal += valorDigito / potencia(baseDe, i + 1);
    }
    return valorDecimal;
}
string DecimalAFraccional(double n, int xBase, int precision)
{
    string resultado = "";
    while (n > 0 && precision > 0)
    {
        n *= xBase;
        int digito = static_cast<int>(n);
        resultado += RevierteDigito(digito);
        n -= digito;
        precision--;
    }
    return resultado;
}
int main()
{
    int baseOrigen, baseDestino;
    string numero, parteEnteraStr, parteFraccionariaStr;
    cout << "Ingrese el numero a convertir (ej. 110.10): ";
    cin >> numero;
    size_t posPunto = string::npos;
    for (size_t i = 0; i < numero.length(); ++i)
    {
        if (numero[i] == '.')
        {
            posPunto = i;
            break;
        }
    }
    if (posPunto != string::npos)
    {
        parteEnteraStr = numero.substr(0, posPunto);
        parteFraccionariaStr = numero.substr(posPunto + 1);
    }
    else
    {
        parteEnteraStr = numero;
        parteFraccionariaStr = "";
    }
    cout << "Ingrese la base de origen (2-16): ";
    cin >> baseOrigen;
    cout << "Ingrese la base destino (2-16): ";
    cin >> baseDestino;

    if (baseOrigen < 2 || baseOrigen > 16 || baseDestino < 2 || baseDestino > 16)
    {
        cout << "Error: Ingrese una base valida entre 2 y 16." << endl;
        return 1;
    }
    long long decimalEntero = 0;
    if (!parteEnteraStr.empty())
    {
        for (int i = 0; i < parteEnteraStr.length(); ++i)
        {
            int valorDigito = EvaluaDigito(parteEnteraStr[parteEnteraStr.length() - 1 - i]);
            if (valorDigito == -1 || valorDigito >= baseOrigen)
            {
                cout << "Error: Digito de parte entera invalido." << endl;
                return 1;
            }
            decimalEntero += valorDigito * static_cast<long long>(potencia(baseOrigen, i));
        }
    }
    string resultadoEntero = "";
    if (decimalEntero == 0)
    {
        resultadoEntero = "0";
    }
    else
    {
        while (decimalEntero > 0)
        {
            int residuo = decimalEntero % baseDestino;
            resultadoEntero += RevierteDigito(residuo);
            decimalEntero /= baseDestino;
        }
        resultadoEntero = revertir(resultadoEntero);
    }
    string resultadoFraccional = "";
    if (!parteFraccionariaStr.empty())
    {
        double decimalFraccional = FraccionalADecimal(parteFraccionariaStr, baseOrigen);
        if (decimalFraccional != -1.0)
        {
            int precision = 6;
            resultadoFraccional = DecimalAFraccional(decimalFraccional, baseDestino, precision);
            if (resultadoFraccional.length() < 4)
            {
                while (resultadoFraccional.length() < 4)
                {
                    resultadoFraccional += '0';
                }
            }
            else if (resultadoFraccional.length() > 6)
            {
                resultadoFraccional = resultadoFraccional.substr(0, 6);
            }
        }
        else
        {
            cout << "Error en la conversion de la parte fraccionaria." << endl;
            return 1;
        }
    }
    cout << "El numero " << numero << " en base " << baseOrigen << " es igual a ";
    cout << resultadoEntero;
    if (!resultadoFraccional.empty())
    {
        cout << "." << resultadoFraccional;
    }
    cout << " en base " << baseDestino << endl;
    return 0;
}

/*
#include <iostream>
#include <string>
using namespace std;
int EvaluaDigito(char c) { //evalua el digito ingresado usando los valores de ASCII
    if (c >= '0' && c <= '9') { return c - '0'; }
    else if (c >= 'A' && c <= 'F') { return c - 'A' + 10; }
    return -1;
}
char RevierteDigito(int v) {//evalua el digito del resultado usando los valores de ASCII
    if (v >= 0 && v <= 9) {  return v + '0'; }
    else if (v >= 10 && v <= 15) { return v - 10 + 'A'; }
    return -1;
}
int potencia(int base, int exp) { int resul = 1;
    for (int i = 0; i < exp; i++) { resul *= base; }
    return resul;
}
int Decimal(const string& n, int baseDe) {//x base a decimal
    int evaluaDecimal = 0;
    for (int i = 0; i < n.length(); i++) {
        int valorDigito = EvaluaDigito(n[n.length() - 1 - i]);
        if (valorDigito == -1 || valorDigito >= baseDe) {
            cout << "Error: Dígito inválido o mayor que la base de origen" << endl;
            cout << "Recuerde que este programa solo funciona con numeros enteros positivos" << endl;
            return -1;
        }
        evaluaDecimal += valorDigito * potencia(baseDe, i);
    }
    return evaluaDecimal;
}
string revertir(string s) {//usando dos punteros uno inicial y otro final invierte hasta llagar al centro
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
string baseX(int evaluaDecimal, int xBase) {// base decimal a otra base
    if (evaluaDecimal == 0) { return "0"; }
    string resultado = "";
    while (evaluaDecimal > 0) {
        int residuo = evaluaDecimal % xBase;
        resultado += RevierteDigito(residuo);
        evaluaDecimal /= xBase;
    }
    return revertir(resultado);
}
int main() {
    int baseOrigen, baseDestino; string numero;
    cout << "Ingrese el número a convertir: "; cin >> numero;
    cout << "Ingrese la base de origen (2-16): "; cin >> baseOrigen;
    cout << "Ingrese la base destino (2-16): "; cin >> baseDestino;
    if (baseOrigen < 2 || baseOrigen > 16 || baseDestino < 2 || baseDestino > 16) {
        cout << "Error: Ingrese una base válida entre 2 y 16." << endl;
        return 1;//validar la base
    }
    int decimal = Decimal(numero, baseOrigen);//funcion x base a decimal
    if (decimal == -1) {
        return 1;
    }
    string resultado = baseX(decimal, baseDestino);//funcion decimal a otra base
    cout << "El número " << numero << " en base " << baseOrigen;
    cout << " es igual a " << resultado << " en base " << baseDestino << endl;
    return 0;
}
*/
