#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (N x N)
const int N = 3;

// Función auxiliar para imprimir la matriz
void imprimirMatriz(double A[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << A[i][j] << "\t";
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
}

// ------------------------------------------------------------------
// --- 1. SUMA DE MATRICES (A + B) ---
// ------------------------------------------------------------------
void sumaMatrices()
{
    double A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    double B[N][N] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    double C[N][N]; // Matriz resultado C = A + B

    cout << "--- 1. Suma de Matrices (3x3) ---" << endl;

    // La suma solo requiere un bucle anidado doble
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            C[i][j] = A[i][j] + B[i][j];
        }
    }

    cout << "Matriz A:" << endl;
    imprimirMatriz(A);
    cout << "Matriz B:" << endl;
    imprimirMatriz(B);
    cout << "Resultado C = A + B:" << endl;
    imprimirMatriz(C);
}

// ------------------------------------------------------------------
// --- 2. TRANSUESTA DE MATRICES (A^T) ---
// ------------------------------------------------------------------
void transpuestaMatrices()
{
    double A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    double A_T[N][N]; // Matriz resultado A_T

    cout << "--- 2. Transpuesta de Matriz (3x3) ---" << endl;

    // Intercambiar filas por columnas
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            A_T[i][j] = A[j][i];
        }
    }

    cout << "Matriz A:" << endl;
    imprimirMatriz(A);
    cout << "Resultado A^T (Transpuesta):" << endl;
    imprimirMatriz(A_T);
}

// ------------------------------------------------------------------
// --- 3. MULTIPLICACIÓN DE MATRICES (A * B) ---
// ------------------------------------------------------------------
void multiplicacionMatrices()
{
    double A[N][N] = {{1, 0, 2}, {0, 3, 0}, {4, 0, 5}};
    double B[N][N] = {{1, 1, 0}, {0, 2, 1}, {1, 0, 0}};
    double C[N][N]; // Matriz resultado C = A * B

    cout << "--- 3. Multiplicacion de Matrices (3x3) ---" << endl;

    // Inicializar la matriz resultado a cero
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            C[i][j] = 0;
        }
    }

    // Triple bucle anidado: i, j, k
    for (int i = 0; i < N; i++)
    { // Filas de A
        for (int j = 0; j < N; j++)
        { // Columnas de B
            for (int k = 0; k < N; k++)
            { // Elementos de la fila/columna interna
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    cout << "Matriz A:" << endl;
    imprimirMatriz(A);
    cout << "Matriz B:" << endl;
    imprimirMatriz(B);
    cout << "Resultado C = A * B:" << endl;
    imprimirMatriz(C);
}

// ------------------------------------------------------------------
// --- FUNCION PRINCIPAL ---
// ------------------------------------------------------------------
int main()
{
    char opcion;

    do
    {
        cout << "\n--- MENU DE OPERACIONES MATRICIALES (3x3) ---" << endl;
        cout << "A. Suma de Matrices" << endl;
        cout << "B. Transpuesta de Matrices" << endl;
        cout << "C. Multiplicacion de Matrices" << endl;
        cout << "D. Metodo de Gauss-Jordan (Resuelto anteriormente)" << endl;
        cout << "X. Salir" << endl;
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        switch (opcion)
        {
        case 'A':
        case 'a':
            sumaMatrices();
            break;
        case 'B':
        case 'b':
            transpuestaMatrices();
            break;
        case 'C':
        case 'c':
            multiplicacionMatrices();
            break;
        case 'D':
        case 'd':
            // La funcion metodoGaussJordan ya está lista y funcional
            // La incluiremos aqui si el usuario la quiere ver integrada
            cout << "La funcion de Gauss-Jordan esta lista en el codigo anterior." << endl;
            break;
        case 'X':
        case 'x':
            cout << "Programa terminado." << endl;
            break;
        default:
            cout << "Opcion invalida." << endl;
        }
    } while (opcion != 'X' && opcion != 'x');

    return 0;
}