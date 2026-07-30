#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
double calcularDeterminante(double M[N][N])
{
    double det_a11 = M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]);
    double det_a12 = M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]);
    double det_a13 = M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]);
    return det_a11 - det_a12 + det_a13;
}
void metodoCramer()
{
    double A_Aumentada[N][N + 1];
    double A_Coeff[N][N];
    double b[N];
    double soluciones[N];
    cout << "Ingrese los coeficientes del sistema:" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "Fila " << i + 1 << ":" << endl;
        for (int j = 0; j < N; j++)
        {
            cout << "  Coeficiente x" << j + 1 << ": ";
            cin >> A_Aumentada[i][j];
            A_Coeff[i][j] = A_Aumentada[i][j];
        }
        cout << "  Termino independiente (b): ";
        cin >> A_Aumentada[i][N];
        b[i] = A_Aumentada[i][N];
    }
    double det_principal = calcularDeterminante(A_Coeff);
    cout << "\nDeterminante principal (Det A): " << det_principal << endl;
    if (det_principal == 0)
    {
        cout << "ERROR: El determinante es cero. El sistema no tiene solucion unica." << endl;
        return;
    }
    for (int i = 0; i < N; i++)
    {
        double matrizTemporal[N][N];
        for (int r = 0; r < N; r++)
        {
            for (int c = 0; c < N; c++)
            {
                matrizTemporal[r][c] = A_Coeff[r][c];
            }
        }
        for (int r = 0; r < N; r++)
        {
            matrizTemporal[r][i] = b[r];
        }
        double det_auxiliar = calcularDeterminante(matrizTemporal);
        soluciones[i] = det_auxiliar / det_principal;

        cout << "Det A" << i + 1 << " = " << det_auxiliar << endl;
    }
    cout << "\n--- SOLUCION FINAL POR CRAMER ---" << endl;
    cout << "x1 = " << soluciones[0] << endl;
    cout << "x2 = " << soluciones[1] << endl;
    cout << "x3 = " << soluciones[2] << endl;
}

int main()
{
    char continuar;
    do
    {
        cout << "\n=== METODO DE CRAMER (SISTEMA 3x3) ===" << endl;
        metodoCramer();
        cout << "\n¿Deseas resolver otro sistema? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}