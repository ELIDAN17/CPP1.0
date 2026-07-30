#include <iostream>
using namespace std;

const int MAX = 10;

void mostrarMatriz(int axb[MAX][MAX], int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cout << axb[i][j] << " ";
        }
        cout << endl;
    }
}

bool esReflexiva(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad REFLEXIVA:\n";
    cout << "Para ser reflexiva, todos los elementos de la diagonal deben ser 1.\n";
    bool reflexiva = true;

    for (int i = 0; i < n; i++)
    {
        if (axb[i][i] != 1)
        {
            cout << " - El par (" << i + 1 << "," << i + 1 << ") no está en la relación\n";
            reflexiva = false;
        }
    }

    if (reflexiva)
    {
        cout << " - Todos los elementos de la diagonal son 1\n";
        cout << "CONCLUSIÓN: La relación ES reflexiva\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES reflexiva\n";
    }

    return reflexiva;
}

bool esIrreflexiva(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad IRREFLEXIVA:\n";
    cout << "Para ser irreflexiva, todos los elementos de la diagonal deben ser 0.\n";
    bool irreflexiva = true;

    for (int i = 0; i < n; i++)
    {
        if (axb[i][i] != 0)
        {
            cout << " - El par (" << i + 1 << "," << i + 1 << ") está en la relación\n";
            irreflexiva = false;
        }
    }

    if (irreflexiva)
    {
        cout << " - Todos los elementos de la diagonal son 0\n";
        cout << "CONCLUSIÓN: La relación ES irreflexiva\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES irreflexiva\n";
    }

    return irreflexiva;
}

bool esSimetrica(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad SIMÉTRICA:\n";
    cout << "Para ser simétrica, si (a,b) está en la relación, entonces (b,a) también debe estar.\n";
    bool simetrica = true;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (axb[i][j] != axb[j][i])
            {
                cout << " - El par (" << i + 1 << "," << j + 1 << ") está en la relación pero ("
                     << j + 1 << "," << i + 1 << ") no está\n";
                simetrica = false;
            }
        }
    }

    if (simetrica)
    {
        cout << " - Todos los pares tienen su simétrico en la relación\n";
        cout << "CONCLUSIÓN: La relación ES simétrica\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES simétrica\n";
    }

    return simetrica;
}

bool esAsimetrica(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad ASIMÉTRICA:\n";
    cout << "Para ser asimétrica, si (a,b) está en la relación, entonces (b,a) NO debe estar, y la diagonal debe ser 0.\n";
    bool asimetrica = true;

    for (int i = 0; i < n; i++)
    {
        if (axb[i][i] != 0)
        {
            cout << " - El par (" << i + 1 << "," << i + 1 << ") está en la relación (diagonal no es 0)\n";
            asimetrica = false;
        }
    }

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i != j && axb[i][j] == 1 && axb[j][i] == 1)
            {
                cout << " - Ambos pares (" << i + 1 << "," << j + 1 << ") y ("
                     << j + 1 << "," << i + 1 << ") están en la relación\n";
                asimetrica = false;
            }
        }
    }

    if (asimetrica)
    {
        cout << " - La diagonal es 0 y no hay pares simétricos en la relación\n";
        cout << "CONCLUSIÓN: La relación ES asimétrica\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES asimétrica\n";
    }

    return asimetrica;
}

bool esAntisimetrica(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad ANTISIMÉTRICA:\n";
    cout << "Para ser antisimétrica, si (a,b) están en la relación, entonces (b,a) no debe estar en la relacion.\n";
    cout << "Los únicos pares simétricos permitidos son los de la diagonal (a,a).\n";
    bool antisimetrica = true;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i != j && axb[i][j] == 1 && axb[j][i] == 1)
            {
                cout << " - Ambos pares (" << i + 1 << "," << j + 1 << ") y ("
                     << j + 1 << "," << i + 1 << ") están en la relación con a != b\n";
                antisimetrica = false;
            }
        }
    }

    if (antisimetrica)
    {
        cout << " - No hay pares simétricos distintos en la relación (solo se permiten en diagonal)\n";
        cout << "CONCLUSIÓN: La relación ES antisimétrica\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES antisimétrica\n";
    }

    return antisimetrica;
}

bool esTransitiva(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando propiedad TRANSITIVA:\n";
    cout << "Para ser transitiva, si (a,b) y (b,c) están en la relación, entonces (a,c) también debe estar.\n";
    bool transitiva = true;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (axb[i][j] == 1)
            {
                for (int k = 0; k < n; k++)
                {
                    if (axb[j][k] == 1 && axb[i][k] != 1)
                    {
                        cout << " - Los pares (" << i + 1 << "," << j + 1 << ") y ("
                             << j + 1 << "," << k + 1 << ") están en la relación, pero ("
                             << i + 1 << "," << k + 1 << ") no está\n";
                        transitiva = false;
                    }
                }
            }
        }
    }

    if (transitiva)
    {
        cout << " - Se cumple la propiedad transitiva para todos los pares\n";
        cout << "CONCLUSIÓN: La relación ES transitiva\n";
    }
    else
    {
        cout << "CONCLUSIÓN: La relación NO ES transitiva\n";
    }

    return transitiva;
}

bool esEquivalencia(int axb[MAX][MAX], int n)
{
    cout << "\nAnalizando si es RELACIÓN DE EQUIVALENCIA:\n";
    cout << "Para ser de equivalencia debe ser reflexiva, simétrica y transitiva.\n";

    bool reflexiva = esReflexiva(axb, n);
    bool simetrica = esSimetrica(axb, n);
    bool transitiva = esTransitiva(axb, n);

    if (reflexiva && simetrica && transitiva)
    {
        cout << "\nCONCLUSIÓN FINAL: La relación ES de equivalencia\n";
        return true;
    }
    else
    {
        cout << "\nCONCLUSIÓN FINAL: La relación NO ES de equivalencia\n";
        return false;
    }
}

int main()
{
    int n, valor;
    int axb[MAX][MAX];

    cout << "ANÁLISIS DE PROPIEDADES DE RELACIONES\n";
    cout << "=====================================\n\n";
    do
    {
        cout << "Ingrese el tamaño de la matriz cuadrada (1-" << MAX << "): ";
        cin >> n;
    } while (n < 1 || n > MAX);

    cout << "\nIngrese los elementos de la matriz (solo 0 o 1):\n";
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            do
            {
                cout << "Elemento [" << i + 1 << "][" << j + 1 << "]: ";
                cin >> valor;

                if (valor != 0 && valor != 1)
                {
                    cout << "ERROR: Solo se permiten valores 0 o 1. Intente nuevamente.\n";
                }
            } while (valor != 0 && valor != 1);

            axb[i][j] = valor;
        }
    }

    cout << "\nMatriz de la relación:\n";
    mostrarMatriz(axb, n);
    esReflexiva(axb, n);
    esIrreflexiva(axb, n);
    esSimetrica(axb, n);
    esAsimetrica(axb, n);
    esAntisimetrica(axb, n);
    esTransitiva(axb, n);
    esEquivalencia(axb, n);

    return 0;
}
