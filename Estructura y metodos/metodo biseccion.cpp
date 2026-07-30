// Juan Mamani Pari
// Metodo Biseccion
// Los epsilon son error de aproximacion (ejemplo: 0.0001)
#include <iostream>
using namespace std;
double potencia(double base, int exponente)
{
    if (exponente == 0)
        return 1.0;
    if (exponente < 0)
        return 1.0 / potencia(base, -exponente);
    if (exponente == 1)
        return base;
    if (exponente == 2)
        return base * base;
    if (exponente == 3)
        return base * base * base;
    if (exponente == 4)
        return base * base * base * base;
    double resultado = 1.0;
    for (int i = 0; i < exponente; ++i)
    {
        resultado *= base;
    }
    return resultado;
}
double valorAbsoluto(double val) // Función para el valor absoluto
{
    return (val < 0) ? -val : val;
}
// Estructura para la Función Polinómica
struct FuncionBiseccion
{
    // Coeficientes para la forma a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
    double a4, a3, a2, a1, a0;
    int grado_n;
    double calcularFx(double x) // Calcula la función F(x)
    {
        double resultado = 0.0;

        resultado += a0; // i=0
        if (grado_n >= 1)
            resultado += a1 * x; // i=1
        if (grado_n >= 2)
            resultado += a2 * potencia(x, 2); // i=2
        if (grado_n >= 3)
            resultado += a3 * potencia(x, 3); // i=3
        if (grado_n >= 4)
            resultado += a4 * potencia(x, 4); // i=4
        return resultado;
    }
};
void metodoBiseccion()
{
    double a, b, epsilon;
    double x_medio;
    FuncionBiseccion funcion = {0.0, 0.0, 0.0, 0.0, 0.0, 0};
    int k = 0;
    cout << "--- Metodo de la Biseccion (Polinomios de Grado 2, 3 o 4) ---" << endl;
    // 1. Entrada del Grado y Coeficientes
    do
    {
        cout << "Ingrese el GRADO N del polinomio (solo 2, 3 o 4): ";
        cin >> funcion.grado_n;
    } while (funcion.grado_n < 2 || funcion.grado_n > 4);
    if (funcion.grado_n == 4)
    {
        cout << "Ingrese a4 (x^4): ";
        cin >> funcion.a4;
    }
    if (funcion.grado_n >= 3)
    {
        cout << "Ingrese a3 (x^3): ";
        cin >> funcion.a3;
    }
    if (funcion.grado_n >= 2)
    {
        cout << "Ingrese a2 (x^2): ";
        cin >> funcion.a2;
    }
    cout << "Ingrese a1 (x^1): ";
    cin >> funcion.a1;
    cout << "Ingrese a0 (cte): ";
    cin >> funcion.a0;
    // Impresión de la Ecuación (para verificación)
    cout << "\nEcuacion F(x): ";
    if (funcion.a4 != 0)
        cout << funcion.a4 << "x^4 + ";
    if (funcion.a3 != 0)
        cout << funcion.a3 << "x^3 + ";
    if (funcion.a2 != 0)
        cout << funcion.a2 << "x^2 + ";
    if (funcion.a1 != 0)
        cout << funcion.a1 << "x + ";
    cout << funcion.a0 << " = 0" << endl;
    cout << "\nIngrese el limite inferior del intervalo (a): ";
    cin >> a;
    cout << "Ingrese el limite superior del intervalo (b): ";
    cin >> b;
    cout << "Ingrese la precision epsilon: ";
    cin >> epsilon;
    double fa = funcion.calcularFx(a);
    double fb = funcion.calcularFx(b);
    // Verificar condición inicial f(a)f(b) < 0
    if (fa * fb >= 0)
    {
        cout << "\n--- ERROR: La funcion debe tener signos opuestos en los limites del intervalo." << endl;
        cout << "f(a)=" << fa << ", f(b)=" << fb << ". Por favor, ingrese otro intervalo. ---" << endl;
        return;
    }
    // 3. Verificación inicial de precisión
    if ((b - a) < epsilon)
    {
        double x_aprox = (a + b) / 2.0;
        cout << "\n--- El intervalo inicial ya cumple con la precision. ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }
    k = 1;
    cout << "\nIteraciones:" << endl;
    cout << "k\t a\t\t b\t\t x_medio\t\t |b - a|" << endl;
    // Bucle de Iteraciones
    while (true)
    {

        // 4. x = (a + b) / 2
        x_medio = (a + b) / 2.0;
        double fx_medio = funcion.calcularFx(x_medio);

        // SALIDA DE LA ITERACIÓN
        cout << k << "\t " << a << "\t " << b << "\t " << x_medio << "\t " << (b - a) << endl;

        // 5. Si f(a) * f(x_medio) > 0, haga a = x_medio
        if (fa * fx_medio > 0)
        {
            a = x_medio;
            fa = fx_medio; // f(a) se actualiza
        }
        // 6. Si f(a) * f(x_medio) <= 0, haga b = x_medio
        else
        {
            b = x_medio;
        }

        // 7. Condición de Parada: |b - a| < epsilon
        if ((b - a) < epsilon)
        {
            double x_aprox = (a + b) / 2.0;
            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "El intervalo final es: [" << a << ", " << b << "]" << endl;
            cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |b - a| = " << (b - a) << " < " << epsilon << " (Epsilon)." << endl;
            break;
        }
        // 8. k = k + 1, vuelva al paso 5
        k++;
    }
}
int main()
{
    char continuar_programa;
    do
    {
        metodoBiseccion();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');
    cout << "Programa terminado." << endl;
    return 0;
}