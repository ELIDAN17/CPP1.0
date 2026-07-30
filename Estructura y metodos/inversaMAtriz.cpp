#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
const int M = 6; // Matriz A + matriz Identidad
void imprimirMatriz(double Mtx[N][M])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            cout << Mtx[i][j] << "\t";
            if (j == N - 1)
                cout << "| \t";
        }
        cout << endl;
    }
    cout << "--------------------------------------" << endl;
}
void calcularInversa()
{
    double A_Aumentada[N][M];
    cout << "Ingrese los coeficientes de la matriz A:" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "Fila " << i + 1 << ":" << endl;
        for (int j = 0; j < N; j++)
        {
            cout << "  Coeficiente x" << j + 1 << ": ";
            cin >> A_Aumentada[i][j];
        }
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = N; j < M; j++)
        {
            A_Aumentada[i][j] = (j == i + N) ? 1.0 : 0.0;
        }
    }
    cout << "\nMatriz Aumentada inicial [A | I]:" << endl;
    imprimirMatriz(A_Aumentada);
    for (int k = 0; k < N; k++)
    {
        double pivotValue = A_Aumentada[k][k];
        if (pivotValue == 0)
        {
            cout << "ERROR: El pivote es cero. La matriz no tiene inversa." << endl;
            return;
        }
        for (int j = 0; j < M; j++)
        {
            A_Aumentada[k][j] /= pivotValue;
        }
        for (int i = 0; i < N; i++)
        {
            if (i != k)
            {
                double factor = A_Aumentada[i][k];
                for (int j = 0; j < M; j++)
                {
                    A_Aumentada[i][j] -= factor * A_Aumentada[k][j];
                }
            }
        }
    }
    cout << "Matriz transformada [I | A^-1]:" << endl;
    imprimirMatriz(A_Aumentada);
    cout << "--- MATRIZ INVERSA FINAL (A^-1) ---" << endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = N; j < M; j++)
        {
            cout << A_Aumentada[i][j] << "\t";
        }
        cout << endl;
    }
}
int main()
{
    char continuar;
    do
    {
        cout << "\n=== MATRIZ INVERSA (SISTEMA 3x3) ===" << endl;
        calcularInversa();
        cout << "\n¿Deseas calcular otra inversa? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}