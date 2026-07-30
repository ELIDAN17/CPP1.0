#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
void imprimirMatriz(double M[N][N], const char *nombre)
{
    cout << "Matriz " << nombre << ":" << endl;
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
void operacionesMatriciales()
{
    double A[N][N], B[N][N], S[N][N], R[N][N], M[N][N];
    cout << "--- INGRESO DE MATRIZ A ---" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "Fila " << i + 1 << ":" << endl;
        for (int j = 0; j < N; j++)
        {
            cout << "  Elemento A" << j + 1 << ": ";
            cin >> A[i][j];
        }
    }
    cout << "\n--- INGRESO DE MATRIZ B ---" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "Fila " << i + 1 << ":" << endl;
        for (int j = 0; j < N; j++)
        {
            cout << "  Elemento B" << j + 1 << ": ";
            cin >> B[i][j];
        }
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            // Suma y Resta
            S[i][j] = A[i][j] + B[i][j];
            R[i][j] = A[i][j] - B[i][j];
            M[i][j] = 0;
        }
    }
    // Multiplicación (Fila x Columna)
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            for (int k = 0; k < N; k++)
            {
                M[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    cout << "\n======= RESULTADOS DE LAS OPERACIONES =======" << endl;
    imprimirMatriz(S, "SUMA (A + B)");
    imprimirMatriz(R, "RESTA (A - B)");
    imprimirMatriz(M, "MULTIPLICACION (A * B)");
}
int main()
{
    char continuar;
    do
    {
        cout << "\n=== OPERACIONES MATRICIALES (SISTEMA 3x3) ===" << endl;
        operacionesMatriciales();
        cout << "\n¿Deseas ingresar otras matrices? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    cout << "Programa terminado." << endl;
    return 0;
}