#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
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
void transpuestaMatrices()
{
    double A[N][N];
    double A_T[N][N];
    cout << "Ingrese los elementos de la matriz A (3x3):" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "Fila " << i + 1 << ":" << endl;
        for (int j = 0; j < N; j++)
        {
            cout << "  Elemento x" << j + 1 << ": ";
            cin >> A[i][j];
        }
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            A_T[i][j] = A[j][i];
        }
    }
    cout << "\nMatriz A original:" << endl;
    imprimirMatriz(A);
    cout << "Resultado A^T (Transpuesta):" << endl;
    imprimirMatriz(A_T);
}
int main()
{
    char continuar;
    do
    {
        cout << "\n=== MATRIZ TRANSPUESTA (SISTEMA 3x3) ===" << endl;
        transpuestaMatrices();
        cout << "\n¿Deseas transponer otra matriz? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}