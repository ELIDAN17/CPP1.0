#include <iostream>

using namespace std;

// --- Funciones Matemáticas Auxiliares (sin librerías) ---

// Método de Herón para la raíz cuadrada
double raizCuadrada(double n)
{
    if (n < 0)
        return 1.0 / 0.0; // Devolver infinito si es raíz de negativo (divergencia)
    if (n == 0)
        return 0.0;
    double x = n;
    double y = 1.0;
    double epsilon_local = 0.00000001;
    while (x - y > epsilon_local)
    {
        x = (x + y) / 2;
        y = n / x;
    }
    return x;
}

// Función potencia
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

// Función raíz n-ésima (basada en Newton-Raphson)
double raizN(double n, int indice)
{
    if (n < 0 && indice % 2 == 0)
        return 1.0 / 0.0;
    if (n == 0)
        return 0.0;
    double x = n;
    double epsilon_local = 0.00000001;
    for (int i = 0; i < 100; ++i)
    {
        double x_anterior = x;
        x = (1.0 / indice) * ((indice - 1) * x + n / potencia(x, indice - 1));
        if (valorAbsoluto(x - x_anterior) < epsilon_local)
            break;
    }
    return x;
}

// --- Functor para representar la función de iteración (Despeje) ---
struct FuncionPhi
{
    double a, b, c;
    int n, opcion_phi;

    double operator()(double x)
    {
        // Si el usuario eligió una opción de la lista específica (1-4)
        if (opcion_phi >= 1 && opcion_phi <= 4)
        {
            switch (opcion_phi)
            {
            case 1: // phi1(x) = 6 - x^2
                return 6.0 - x * x;
            case 2: // phi2(x) = sqrt(6 - x) (Solo se usa la raíz positiva para este ejemplo)
                return raizCuadrada(6.0 - x);
            case 3: // phi3(x) = 6/x - 1
                if (x == 0)
                    return 1.0 / 0.0;
                return 6.0 / x - 1.0;
            case 4: // phi4(x) = 6 / (x + 1)
                if (x + 1.0 == 0)
                    return 1.0 / 0.0;
                return 6.0 / (x + 1.0);
            }
        }
        // Si el usuario eligió una opción genérica (Opción 5, 6, 7 en el nuevo menú)
        else
        {
            switch (opcion_phi)
            {
                // Se dejan los despejes genéricos por si se usan para otro polinomio
            case 5: // Corresponde al Despeje Genérico 1: x = (-a*x^n - c) / b
                if (b == 0)
                    return 1.0 / 0.0;
                return (-a * potencia(x, n) - c) / b;
            case 6: // Corresponde al Despeje Genérico 2: x = Raiz n-ésima [(-b*x - c) / a]
                if (a == 0)
                    return 1.0 / 0.0;
                return raizN((-b * x - c) / a, n);
            case 7: // Corresponde al Despeje Genérico 3: x = -c / (a*x^(n-1) + b)
                if ((a * potencia(x, n - 1) + b) == 0)
                    return 1.0 / 0.0;
                return -c / (a * potencia(x, n - 1) + b);
            default:
                return 1.0 / 0.0;
            }
        }
        return 1.0 / 0.0;
    }

    // Función original f(x) para la verificación de error |f(x_k)|
    double calcularFx(double x)
    {
        return a * potencia(x, n) + b * x + c;
    }
};

// --- Verificación de Raíces Cuadráticas Exactas (Se mantiene) ---
// NOTA: Esta función se mantiene, pero ahora se llama al final de metodoPuntoFijo
// Usamos los coeficientes a, b, c de la estructura FuncionPhi para asegurar la coherencia
void verificarRaicesCuadraticas(double a, double b, double c, double x_aprox)
{
    cout << "\n=============================================" << endl;
    cout << "VERIFICACION DE RAICES EXACTAS (SOLO PARA N=2)" << endl;

    double discriminante = b * b - 4 * a * c;

    if (discriminante >= 0)
    {
        double raiz_d = raizCuadrada(discriminante);
        // Manejar el caso donde la raizCuadrada devuelve infinito (discriminante negativo)
        if (raiz_d == 1.0 / 0.0)
        {
            cout << "La ecuacion tiene raices complejas. No se realiza verificacion simple." << endl;
            return;
        }

        double x1_exacta = (-b + raiz_d) / (2 * a);
        double x2_exacta = (-b - raiz_d) / (2 * a);

        cout << "La ecuacion cuadratica tiene las siguientes raices exactas:" << endl;
        cout << "Raiz 1 (x1) = " << x1_exacta << endl;
        cout << "Raiz 2 (x2) = " << x2_exacta << endl;

        double error1 = valorAbsoluto(x_aprox - x1_exacta);
        double error2 = valorAbsoluto(x_aprox - x2_exacta);

        cout << "\nComparacion con el resultado del Punto Fijo (" << x_aprox << "):" << endl;

        if (error1 < error2)
        {
            cout << "El valor aproximado se acerca a la Raiz 1 (Error: " << error1 << ")" << endl;
        }
        else
        {
            cout << "El valor aproximado se acerca a la Raiz 2 (Error: " << error2 << ")" << endl;
        }
    }
    else
    {
        cout << "La ecuacion tiene raices complejas. No se realiza verificacion simple." << endl;
    }
    cout << "=============================================" << endl;
}

// --- Implementación del Método de Punto Fijo (ARREGLADA) ---

void metodoPuntoFijo()
{
    double x0, x1; // Usamos x0 y x1 según el algoritmo
    double epsilon1, epsilon2;
    FuncionPhi phi;
    int k = 0; // k comienza en 0

    cout << "--- Metodo del Punto Fijo Generalizado (a*x^n + b*x + c = 0) ---" << endl;

    // 1. Entrada de la función polinómica
    cout << "Ingrese el exponente n (ej: 2 para cuadratica): ";
    cin >> phi.n;
    cout << "Ingrese el coeficiente a: ";
    cin >> phi.a;
    cout << "Ingrese el coeficiente b: ";
    cin >> phi.b;
    cout << "Ingrese el coeficiente c: ";
    cin >> phi.c;
    cout << "Ecuacion: " << phi.a << "x^" << phi.n << " + " << phi.b << "x + " << phi.c << " = 0" << endl;

    // 2. Seleccion de la función de iteración (Incluye los 4 despejes específicos)
    cout << "\nSeleccione el despeje phi(x) a usar:" << endl;
    cout << "Despejes ESPECIFICOS (para la ecuacion x^2 + x - 6 = 0):" << endl;
    cout << "1. phi1(x) = 6 - x^2" << endl;
    cout << "2. phi2(x) = sqrt(6 - x)" << endl;
    cout << "3. phi3(x) = 6/x - 1" << endl;
    cout << "4. phi4(x) = 6/(x + 1)" << endl;
    cout << "---------------------------------------------------------" << endl;
    cout << "Despejes GENERICOS (solo si su ecuacion coincide):" << endl;
    cout << "5. (-a*x^n - c) / b" << endl;
    cout << "6. Raiz n-esima [(-b*x - c) / a]" << endl;
    cout << "7. -c / (a*x^(n-1) + b)" << endl;
    cout << "Opcion: ";
    cin >> phi.opcion_phi;

    // 1. Entrada de la aproximacion inicial y error
    cout << "\nIngrese la aproximacion inicial (x0): ";
    cin >> x0;
    cout << "Ingrese la precision epsilon1 (|f(x)|): ";
    cin >> epsilon1;
    cout << "Ingrese la precision epsilon2 (|x_k - x_{k-1}|): ";
    cin >> epsilon2;

    // 2. Si |f(x0)| < epsilon1, haga x_bar = x0 Fin.
    if (valorAbsoluto(phi.calcularFx(x0)) < epsilon1)
    {
        cout << "\n--- Convergencia inmediata en x0. Raiz aproximada (x_bar): " << x0 << " ---" << endl;
        if (phi.n == 2)
            verificarRaicesCuadraticas(phi.a, phi.b, phi.c, x0);
        return;
    }

    // 3. k = 1
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t x_k\t\t |f(x_k)|\t |x_k - x_{k-1}|" << endl;

    // --- Bucle de Iteraciones ---
    while (true)
    {

        // 4. x1 = phi(x0)
        x1 = phi(x0);
        double fx1 = phi.calcularFx(x1);
        double error_aproximacion = valorAbsoluto(x1 - x0);

        // Manejo de divergencias...
        if (x1 == 1.0 / 0.0 || x1 == -1.0 / 0.0)
        {
            cout << "\n--- ERROR: El metodo diverge (division por cero, raiz negativa, o el despeje no converge) ---" << endl;
            return;
        }

        // SALIDA DE LAS ITERACIONES (Tabla)
        cout << k << "\t " << x1 << "\t " << valorAbsoluto(fx1) << "\t " << error_aproximacion << endl;
        // -----------------------------

        // 5. Si |f(x1)| < epsilon1 o si |x1 - x0| < epsilon2 entonces haga x_bar = x1 Fin.
        if (valorAbsoluto(fx1) < epsilon1 || error_aproximacion < epsilon2)
        {
            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x1 << endl;
            cout << "Numero de iteraciones: " << k << endl;

            // Verificación explícita de la condición de parada
            if (valorAbsoluto(fx1) < epsilon1)
            {
                cout << "Condicion cumplida: |f(x1)| = " << valorAbsoluto(fx1) << " < " << epsilon1 << " (Epsilon1)." << endl;
            }
            if (error_aproximacion < epsilon2)
            {
                cout << "Condicion cumplida: |x1 - x0| = " << error_aproximacion << " < " << epsilon2 << " (Epsilon2)." << endl;
            }
            break;
        }

        // 6. x0 = x1
        x0 = x1;

        // 7. k = k + 1, vuelva al paso 4
        k++;
    }

    // Llama a la función de verificación de raíces exactas (al final, fuera del bucle)
    if (phi.n == 2)
    {
        verificarRaicesCuadraticas(phi.a, phi.b, phi.c, x1);
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoPuntoFijo();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}