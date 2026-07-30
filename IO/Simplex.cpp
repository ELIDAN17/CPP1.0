#include <iostream>
using namespace std;
void mostrarTabla(double **tabla, int *variablesEnBase, int filas, int columnas, int itera, int filPivote, int colPivote, int variables, int restricciones)
{
    cout << "\n========================================================================" << endl;
    cout << "                TABLA " << itera << endl;
    cout << "========================================================================" << endl;
    cout << "Base\tZ\t";
    for (int j = 0; j < variables; j++)
        cout << "x" << j + 1 << "\t";
    for (int j = 0; j < restricciones; j++)
        cout << "y" << j + 1 << "\t";
    cout << "b\tRazon" << endl;
    cout << "------------------------------------------------------------------------" << endl;
    for (int i = 0; i < filas; i++)
    {
        if (i == 0)
            cout << "Z\t";
        else
        {
            int varIdx = variablesEnBase[i];
            if (varIdx <= variables)
                cout << "x" << varIdx << "\t";
            else
                cout << "y" << (varIdx - variables) << "\t";
        }
        for (int j = 0; j < columnas; j++)
        {
            if (i == filPivote && j == colPivote && filPivote != -1)
            {
                cout << "[" << tabla[i][j] << "]\t";
            }
            else
            {
                if (tabla[i][j] > -0.0001 && tabla[i][j] < 0.0001)
                {
                    cout << "0\t";
                }
                else
                {
                    cout << tabla[i][j] << "\t";
                }
            }
        }
        cout << endl;
    }
    cout << "------------------------------------------------------------------------" << endl;
}
int main()
{
    int variables = 0;
    int restricciones = 0;
    cout << "--- SIMULADOR SIMPLEX Juan ---" << endl;
    cout << "Ingrese la cantidad de variables de decision (X): ";
    cin >> variables;
    cout << "Ingrese la cantidad de restricciones (Y): ";
    cin >> restricciones;
    int filas = restricciones + 1;
    // Columnas: Z, X, holguras Y, b, Razón
    int columnas = 1 + variables + restricciones + 2;
    double **tabla = new double *[filas];
    for (int i = 0; i < filas; i++)
    {
        tabla[i] = new double[columnas];
        for (int j = 0; j < columnas; j++)
            tabla[i][j] = 0.0;
    }
    int *variablesEnBase = new int[filas];
    variablesEnBase[0] = 0;
    for (int i = 1; i <= restricciones; i++)
    {
        variablesEnBase[i] = variables + i;
    }
    cout << "\n========================================================================" << endl;
    cout << "             GUIA DE LLENADO DE LA MATRIZ SIMPLEX" << endl;
    cout << "========================================================================" << endl;
    cout << "Debe ingresar los valores de cada fila separados por espacios." << endl;
    cout << "El orden exacto de las columnas que el programa espera es:" << endl;
    cout << "\nZ\t";
    for (int j = 0; j < variables; j++)
        cout << "x" << j + 1 << "\t";
    for (int j = 0; j < restricciones; j++)
        cout << "y" << j + 1 << "\t";
    cout << "b" << endl;
    cout << "------------------------------------------------------------------------" << endl;
    // Captura de datos
    for (int i = 0; i < filas; i++)
    {
        if (i == 0)
            cout << "\n-> Ingrese la FILA 0/Z (" << columnas - 1 << " valores): " << endl;
        else
            cout << "-> Ingrese la FILA de la restriccion y" << i << " (" << columnas - 1 << " valores): " << endl;
        for (int j = 0; j < columnas - 1; j++)
        {
            cin >> tabla[i][j];
        }
    }
    int iteracion = 0;
    while (true)
    {
        // Identificar la columna pivote (X1 en la columna 1)
        int colPivote = 1;
        double menorZ = tabla[0][1];
        // Recorremos todas las columnas
        for (int j = 1; j <= variables + restricciones; j++)
        {
            if (tabla[0][j] < menorZ)
            {
                menorZ = tabla[0][j];
                colPivote = j;
            }
        }
        // Condición de parada
        if (menorZ >= -0.00001)
        {
            mostrarTabla(tabla, variablesEnBase, filas, columnas, iteracion, -1, -1, variables, restricciones);
            cout << "\n>>> ¡SOLUCION OPTIMA ENCONTRADA CON EXITO! <<<" << endl;
            break;
        }

        // Determinar la fila pivote
        int filPivote = -1;
        double menorRazon = 99999.0;
        int colSolucion = variables + restricciones + 1;
        for (int i = 1; i < filas; i++)
        {
            if (tabla[i][colPivote] > 0.00001)
            {
                tabla[i][columnas - 1] = tabla[i][colSolucion] / tabla[i][colPivote];
                if (tabla[i][columnas - 1] < menorRazon)
                {
                    menorRazon = tabla[i][columnas - 1];
                    filPivote = i;
                }
            }
            else
            {
                tabla[i][columnas - 1] = -1; // Razón no válida
            }
        }
        if (filPivote == -1)
        {
            cout << "\nError: El problema tiene una solucion no acotada." << endl;
            break;
        }
        mostrarTabla(tabla, variablesEnBase, filas, columnas, iteracion, filPivote, colPivote, variables, restricciones);
        cout << "-> ANALISIS DE LA ITERACION:" << endl;
        if (colPivote <= variables)
        {
            cout << "   * Variable ENTRANTE: x" << colPivote << " (Columna " << colPivote << ")" << endl;
        }
        else
        {
            cout << "   * Variable ENTRANTE: y" << (colPivote - variables) << " (Columna " << colPivote << ")" << endl;
        }

        int varSalienteIdx = variablesEnBase[filPivote];
        if (varSalienteIdx <= variables)
        {
            cout << "   * Variable SALIENTE de la base: x" << varSalienteIdx << " (Fila " << filPivote << ")" << endl;
        }
        else
        {
            cout << "   * Variable SALIENTE de la base: y" << (varSalienteIdx - variables) << " (Fila " << filPivote << ")" << endl;
        }

        cout << "   * Elemento PIVOTE seleccionado: [" << tabla[filPivote][colPivote] << "]" << endl;
        cout << "========================================================================" << endl;

        // Actualizar el índice de la base
        variablesEnBase[filPivote] = colPivote;

        // Normalizar la fila pivote
        double valorPivote = tabla[filPivote][colPivote];
        for (int j = 1; j < columnas - 1; j++)
        {
            tabla[filPivote][j] /= valorPivote;
        }

        // Operación de Gauss-Jordan
        for (int i = 0; i < filas; i++)
        {
            if (i != filPivote)
            {
                double factor = tabla[i][colPivote];
                for (int j = 1; j < columnas - 1; j++)
                {
                    tabla[i][j] = tabla[i][j] - (factor * tabla[filPivote][j]);
                }
            }
        }

        iteracion++;
    }

    // Lectura dinámica de los resultados
    int colSolucion = variables + restricciones + 1;
    double z = tabla[0][colSolucion];
    double *resultadosX = new double[variables + 1];
    for (int j = 1; j <= variables; j++)
        resultadosX[j] = 0.0;

    for (int i = 1; i < filas; i++)
    {
        int varIdx = variablesEnBase[i];
        if (varIdx <= variables)
        {
            resultadosX[varIdx] = tabla[i][colSolucion];
        }
    }

    cout << "\n=======================================================" << endl;
    cout << "                 VALORES ENCONTRADOS" << endl;
    cout << "=======================================================" << endl;
    cout << "Valor final de Z  = " << z << endl;
    for (int j = 1; j <= variables; j++)
    {
        cout << "Valor final de X" << j << " = " << resultadosX[j] << endl;
    }
    cout << "=======================================================" << endl;

    delete[] resultadosX;
    delete[] variablesEnBase;
    for (int i = 0; i < filas; i++)
        delete[] tabla[i];
    delete[] tabla;

    return 0;
}