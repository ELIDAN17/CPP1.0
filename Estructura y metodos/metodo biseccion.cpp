#include <iostream>

using namespace std;

// Función para elevar un número a una potencia entera
double potencia(double base, int exponente)
{
    if (exponente == 0)
        return 1.0;
    if (exponente < 0)
        return 1.0 / potencia(base, -exponente);
    double resultado = 1.0;
    for (int i = 0; i < exponente; ++i)
    {
        resultado *= base;
    }
    return resultado;
}

// Función para el valor absoluto
double valorAbsoluto(double val)
{
    if (val < 0)
    {
        return -val;
    }
    return val;
}

// --- Estructura para la Función Polinómica ---
struct FuncionGeneral
{
    double a, b, c;
    int n;

    // Calcula la función f(x) = a*x^n + b*x + c
    double calcularFx(double x)
    {
        return a * potencia(x, n) + b * x + c;
    }
};

// --- Implementación del Método de la Bisección ---
void metodoBiseccion()
{
    double a, b, epsilon;
    double x_medio;
    FuncionGeneral funcion;
    int k = 0;

    cout << "--- Metodo de la Biseccion (para f(x) = a*x^n + b*x + c) ---" << endl;

    // 1. Entrada de la función polinómica
    cout << "Ingrese el exponente n (ej: 3 para cubica): ";
    cin >> funcion.n;
    cout << "Ingrese el coeficiente a: ";
    cin >> funcion.a;
    cout << "Ingrese el coeficiente b: ";
    cin >> funcion.b;
    cout << "Ingrese el coeficiente c: ";
    cin >> funcion.c;
    cout << "Ecuacion: " << funcion.a << "x^" << funcion.n << " + " << funcion.b << "x + " << funcion.c << " = 0" << endl;

    // 1. Entrada del intervalo inicial y precisión
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
        cout << "f(a) * f(b) >= 0. Por favor, ingrese otro intervalo. ---" << endl;
        return;
    }

    // 2. Si (b - a) < epsilon, haga x_bar cualquier x en [a,b] Fin. (Verificación inicial)
    if ((b - a) < epsilon)
    {
        double x_aprox = (a + b) / 2.0;
        cout << "\n--- El intervalo inicial ya cumple con la precision. ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }

    // 3. k = 1
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t a\t\t b\t\t x_medio\t |b - a|" << endl;

    // Bucle de Iteraciones (Paso 9: Vuelva al paso 5)
    while (true)
    {

        // 4. M = f(a) (Guardamos f(a) en una variable auxiliar para el paso 6)
        // Ya tenemos fa, no necesitamos una variable 'M' separada.

        // 5. x = (a + b) / 2
        x_medio = (a + b) / 2.0;
        double fx_medio = funcion.calcularFx(x_medio);

        // SALIDA DE LA ITERACIÓN
        cout << k << "\t " << a << "\t " << b << "\t " << x_medio << "\t " << (b - a) << endl;
        // -----------------------------

        // 6. Si M * f(x) > 0, haga a = x vaya al paso 8. (Donde M es f(a) de la iteración anterior)
        if (fa * fx_medio > 0)
        {
            a = x_medio;
            fa = fx_medio; // f(a) se actualiza
        }
        // 7. b = x (Si M * f(x) <= 0)
        else
        {
            b = x_medio;
            // No necesitamos actualizar fb, ya que f(b) no se usa en la verificación M*f(x)>0
        }

        // 8. Si (b - a) < epsilon, haga x_bar cualquier x en [a, b] Fin.
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

        // 9. k = k + 1, vuelva al paso 5
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