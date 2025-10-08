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
    double a_coef, b_coef, c_coef; // Renombradas para evitar conflicto con los límites del intervalo [a, b]
    int n;

    // Calcula la función f(x) = a*x^n + b*x + c
    double calcularFx(double x)
    {
        return a_coef * potencia(x, n) + b_coef * x + c_coef;
    }
};

// --- Implementación del Método de la Posición Falsa ---
void metodoPosicionFalsa()
{
    double a, b, epsilon1, epsilon2;
    double x_actual;
    FuncionGeneral funcion;
    int k = 0;
    double fa, fb;
    double fx_actual;

    cout << "--- Metodo de la Posicion Falsa (para f(x) = a*x^n + b*x + c) ---" << endl;

    // 1. Entrada de la función polinómica
    cout << "Ingrese el exponente n (ej: 3 para cubica): ";
    cin >> funcion.n;
    cout << "Ingrese el coeficiente a: ";
    cin >> funcion.a_coef;
    cout << "Ingrese el coeficiente b: ";
    cin >> funcion.b_coef;
    cout << "Ingrese el coeficiente c: ";
    cin >> funcion.c_coef;
    cout << "Ecuacion: " << funcion.a_coef << "x^" << funcion.n << " + " << funcion.b_coef << "x + " << funcion.c_coef << " = 0" << endl;

    // 1. Entrada del intervalo inicial y precisiones
    cout << "\nIngrese el limite inferior del intervalo (a): ";
    cin >> a;
    cout << "Ingrese el limite superior del intervalo (b): ";
    cin >> b;
    cout << "Ingrese la precision epsilon1 (|b - a|): ";
    cin >> epsilon1;
    cout << "Ingrese la precision epsilon2 (|f(x)|): ";
    cin >> epsilon2;

    fa = funcion.calcularFx(a);
    fb = funcion.calcularFx(b);

    // Verificar condición inicial f(a)f(b) < 0
    if (fa * fb >= 0)
    {
        cout << "\n--- ERROR: La funcion debe tener signos opuestos en los limites del intervalo." << endl;
        cout << "f(a) * f(b) >= 0. Por favor, ingrese otro intervalo. ---" << endl;
        return;
    }

    // 2. Verificaciones iniciales
    if ((b - a) < epsilon1)
    { // 2. Si (b - a) < epsilon1
        double x_aprox = (a + b) / 2.0;
        cout << "\n--- El intervalo inicial ya cumple con la precision epsilon1. ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }
    if (valorAbsoluto(fa) < epsilon2 || valorAbsoluto(fb) < epsilon2)
    { // 2. Si |f(a)| < epsilon2 o si |f(b)| < epsilon2
        double x_aprox = (valorAbsoluto(fa) < epsilon2) ? a : b;
        cout << "\n--- Uno de los limites iniciales ya cumple con la precision epsilon2. ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }

    // 3. k = 1
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t a\t\t b\t\t x_nuevo\t f(x_nuevo)\t |b - a|" << endl;

    // Bucle de Iteraciones (Paso 10: Vuelva al paso 5)
    while (true)
    {

        // 4. M = f(a) (Lo usamos directamente como fa)

        // Denominador para la fórmula
        double denominador = fb - fa;

        // Si el denominador es cero, el método falla
        if (denominador == 0)
        {
            cout << "\n--- ERROR: El denominador f(b) - f(a) es cero. El metodo fallara. ---" << endl;
            return;
        }

        // 5. Formula de la Posición Falsa: x = (a*f(b) - b*f(a)) / (f(b) - f(a))
        x_actual = (a * fb - b * fa) / denominador;
        fx_actual = funcion.calcularFx(x_actual);

        // 6. Si |f(x)| < epsilon2 seleccione x_bar = x. Fin.
        if (valorAbsoluto(fx_actual) < epsilon2)
        {

            // SALIDA DE LA ÚLTIMA ITERACIÓN
            cout << k << "\t " << a << "\t " << b << "\t " << x_actual << "\t " << fx_actual << "\t " << (b - a) << endl;

            cout << "\n--- Convergencia por |f(x)| alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x_actual << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |f(x)| = " << valorAbsoluto(fx_actual) << " < " << epsilon2 << " (Epsilon2)." << endl;
            break;
        }

        // 7. Si M * f(x) > 0, haga a = x. Vaya al paso 9.
        if (fa * fx_actual > 0)
        {
            a = x_actual;
            fa = fx_actual; // f(a) se actualiza
        }
        // 8. b = x
        else
        {
            b = x_actual;
            fb = fx_actual; // f(b) se actualiza
        }

        // SALIDA DE LA ITERACIÓN ANTES DE LA VERIFICACIÓN FINAL
        cout << k << "\t " << a << "\t " << b << "\t " << x_actual << "\t " << fx_actual << "\t " << (b - a) << endl;

        // 9. Si b - a < epsilon1, seleccione x_bar cualquiera en [a, b]. Fin.
        if ((b - a) < epsilon1)
        {
            double x_aprox = (a + b) / 2.0;
            cout << "\n--- Convergencia por intervalo |b - a| alcanzada y verificada ---" << endl;
            cout << "El intervalo final es: [" << a << ", " << b << "]" << endl;
            cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |b - a| = " << (b - a) << " < " << epsilon1 << " (Epsilon1)." << endl;
            break;
        }

        // 10. k = k + 1, vuelva al paso 5
        k++;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoPosicionFalsa();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}