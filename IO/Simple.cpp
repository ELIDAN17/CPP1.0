#include <iostream>

using namespace std;

const int MAX_F = 10;
const int MAX_C = 20;

void imprimirTabla(double tabla[MAX_F][MAX_C], int filas, int cols, int iter)
{
    cout << "\nTABLA " << iter << ":" << endl;
    for (int i = 0; i < filas; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            if (tabla[i][j] > -0.0001 && tabla[i][j] < 0.0001)
                cout << "0\t";
            else
                cout << tabla[i][j] << "\t";
        }
        cout << endl;
    }
}

int main()
{
    int v, r, opcion;
    double tabla[MAX_F][MAX_C] = {0};

    cout << "--- MOTOR SIMPLEX ---" << endl;
    cout << "1. Maximizar\n2. Minimizar\nSeleccione: ";
    cin >> opcion;

    cout << "Variables: ";
    cin >> v;
    cout << "Restricciones (<=): ";
    cin >> r;

    cout << "\n--- COEFICIENTES DE Z ---" << endl;
    for (int j = 0; j < v; j++)
    {
        cout << "Coef x" << j + 1 << ": ";
        double c;
        cin >> c;
        // Si minimizamos, Maximizar(-Z)
        if (opcion == 1)
            tabla[0][j] = -c;
        else
            tabla[0][j] = c;
    }

    for (int i = 1; i <= r; i++)
    {
        cout << "\n--- RESTRICCION " << i << " ---" << endl;
        for (int j = 0; j < v; j++)
        {
            cout << "x" << j + 1 << ": ";
            cin >> tabla[i][j];
        }
        cout << "b (Lado derecho): ";
        cin >> tabla[i][v + r];
        tabla[i][v + i - 1] = 1; // Holgura s
    }

    int iter = 0;
    int cols = v + r + 1;
    int filas = r + 1;

    while (true)
    {
        imprimirTabla(tabla, filas, cols, iter);

        // 1. Columna pivote (el más negativo)
        int colP = -1;
        double minZ = -0.0001;
        for (int j = 0; j < cols - 1; j++)
        {
            if (tabla[0][j] < minZ)
            {
                minZ = tabla[0][j];
                colP = j;
            }
        }

        if (colP == -1)
            break;

        // 2. Fila pivote (cociente mínimo)
        int filaP = -1;
        double minC = 1e15;
        for (int i = 1; i <= r; i++)
        {
            if (tabla[i][colP] > 0)
            {
                double c = tabla[i][cols - 1] / tabla[i][colP];
                if (c < minC)
                {
                    minC = c;
                    filaP = i;
                }
            }
        }

        if (filaP == -1)
        {
            cout << "\nNo acotado";
            return 0;
        }

        // 3. Gauss-Jordan
        double pv = tabla[filaP][colP];
        for (int j = 0; j < cols; j++)
            tabla[filaP][j] /= pv;
        for (int i = 0; i <= r; i++)
        {
            if (i != filaP)
            {
                double f = tabla[i][colP];
                for (int j = 0; j < cols; j++)
                    tabla[i][j] -= f * tabla[filaP][j];
            }
        }
        iter++;
    }

    // Ajuste final del valor de Z si era minimización
    double resultadoZ = (opcion == 2) ? -tabla[0][cols - 1] : tabla[0][cols - 1];

    cout << "\n=================================" << endl;
    cout << "RESULTADOS FINALES:" << endl;
    cout << "Z = " << resultadoZ << endl;

    // Mostrar valores de x
    for (int j = 0; j < v; j++)
    {
        double valX = 0;
        for (int i = 1; i <= r; i++)
        {
            if (tabla[i][j] == 1)
                valX = tabla[i][cols - 1];
        }
        cout << "x" << j + 1 << " = " << valX << endl;
    }
    cout << "=================================" << endl;

    return 0;
}