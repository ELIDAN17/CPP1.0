#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (para un sistema 3x3)
const int N = 3; // Número de variables/ecuaciones
const int M = 4; // Columnas: 3 coeficientes + 1 constante

// Función auxiliar para imprimir la matriz
void imprimirMatriz(double A[N][M])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            cout << A[i][j] << "\t";
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
}

// --- Método de Eliminación Gaussiana ---
void metodoGauss()
{
    // Matriz de ejemplo (Aumentada 3x4).
    double A[N][M] = {
        {2, 1, 1, 12}, // 2x + 1y + 1z = 12
        {1, 3, 2, 19}, // 1x + 3y + 2z = 19
        {3, 2, 4, 30}  // 3x + 2y + 4z = 30
    };

    double soluciones[N]; // Vector para almacenar x1, x2, x3

    cout << "--- Metodo de Eliminacion Gaussiana (Sistema 3x3) ---" << endl;
    cout << "Matriz inicial:" << endl;
    imprimirMatriz(A);

    // 1. Fase de Eliminación (Hacer ceros debajo de la diagonal)
    for (int k = 0; k < N; k++)
    { // k es el pivote (fila actual)

        // Búsqueda de Pivote (Implementación simple: solo verificación)
        if (A[k][k] == 0)
        {
            cout << "Error: Pivote cero en la diagonal. Se necesita pivoteo de filas." << endl;
            return;
        }

        // Eliminación de Elementos
        for (int i = k + 1; i < N; i++)
        { // Filas debajo del pivote

            // Factor: El elemento a eliminar dividido por el pivote
            double factor = A[i][k] / A[k][k];

            // Operación: Fila[i] = Fila[i] - factor * Fila[k]
            for (int j = k; j < M; j++)
            {
                A[i][j] -= factor * A[k][j];
            }
        }
    }

    cout << "Matriz en Forma Triangular Superior:" << endl;
    imprimirMatriz(A);

    // 2. Fase de Sustitución hacia Atrás

    // Calcular la última variable (x3 o x_{N-1})
    // Ecuación: A[N-1][N-1] * x_{N-1} = A[N-1][M-1]
    soluciones[N - 1] = A[N - 1][M - 1] / A[N - 1][N - 1];

    // Calcular las variables restantes (desde x2 hasta x1)
    for (int i = N - 2; i >= 0; i--)
    {
        double suma_terminos = 0.0;

        // Sumar los términos ya conocidos (a_ij * x_j)
        for (int j = i + 1; j < N; j++)
        {
            suma_terminos += A[i][j] * soluciones[j];
        }

        // Despejar x_i: x_i = (b_i - Suma) / a_ii
        soluciones[i] = (A[i][M - 1] - suma_terminos) / A[i][i];
    }

    cout << "--- Solucion Final por Sustitucion hacia Atras ---" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "x" << i + 1 << " = " << soluciones[i] << endl;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoGauss();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}