#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (para un sistema 3x3)
const int N = 3; // Número de variables/ecuaciones
const int M = 4; // Columnas: 3 coeficientes + 1 constante

// Función para imprimir la matriz (opcional, para visualización)
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

// --- Método de Gauss-Jordan ---
void metodoGaussJordan()
{
    // Matriz de ejemplo (Aumentada 3x4). Puede ser leída por cin.
    double A[N][M] = {
        {2, 1, 1, 12}, // 2x + 1y + 1z = 12
        {1, 3, 2, 19}, // 1x + 3y + 2z = 19
        {3, 2, 4, 30}  // 3x + 2y + 4z = 30
    };

    // Matriz 3x4:  [a11 a12 a13 | b1]
    //              [a21 a22 a23 | b2]
    //              [a31 a32 a33 | b3]

    cout << "--- Metodo de Gauss-Jordan (Sistema 3x3) ---" << endl;
    cout << "Matriz inicial:" << endl;
    imprimirMatriz(A);

    // 1. Fase de Eliminación (Hacer la matriz Triangular Superior y luego Identidad)
    for (int k = 0; k < N; k++)
    { // k es el pivote actual (columna/fila)

        // **Normalización del Pivote**
        // Divide la fila k por el elemento A[k][k] (el pivote) para hacerlo 1
        if (A[k][k] == 0)
        {
            cout << "Error: Pivote cero. El sistema no se puede resolver con este pivote." << endl;
            return;
        }
        double pivotValue = A[k][k];
        for (int j = k; j < M; j++)
        {
            A[k][j] /= pivotValue;
        }

        // **Eliminación de Elementos** (Hacer ceros por encima y por debajo del pivote)
        for (int i = 0; i < N; i++)
        {
            if (i != k)
            { // Saltar la fila del pivote
                double factor = A[i][k];
                // Restar el factor * Fila Pivote a la Fila actual
                for (int j = k; j < M; j++)
                {
                    A[i][j] -= factor * A[k][j];
                }
            }
        }
    }

    cout << "Matriz en Forma Escalonada Reducida (Identidad):" << endl;
    imprimirMatriz(A);

    // 2. Extracción de la Solución
    cout << "--- Solucion Final ---" << endl;
    for (int i = 0; i < N; i++)
    {
        // La solución x_i se encuentra en la columna de constantes (M-1)
        cout << "x" << i + 1 << " = " << A[i][M - 1] << endl;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoGaussJordan();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}