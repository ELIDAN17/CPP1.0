#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (N x N)
const int N = 3;

// Función auxiliar para imprimir la matriz
void imprimirMatriz(double M[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << M[i][j] << "\t";
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
}

// --- Método de la Transpuesta (A^T) ---
void transpuestaMatrices()
{
    // Matriz de ejemplo A (3x3).
    double A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    double A_T[N][N]; // Matriz resultado A_T

    cout << "--- Metodo de la Transpuesta de Matriz (3x3) ---" << endl;

    // El núcleo de la Transpuesta: A_T[i][j] = A[j][i]
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            A_T[i][j] = A[j][i];
        }
    }

    cout << "Matriz A original:" << endl;
    imprimirMatriz(A);
    cout << "Resultado A^T (Transpuesta):" << endl;
    imprimirMatriz(A_T);
}

int main()
{
    char continuar_programa;
    do
    {
        transpuestaMatrices();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}