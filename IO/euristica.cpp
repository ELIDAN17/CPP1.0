#include <iostream>

using namespace std;

// Tamaño máximo general para las matrices
const int MAX = 20;

int main()
{
    int M, N; // M = Silos (Filas), N = Molinos (Columnas)

    int costos[MAX][MAX];
    int asignacion[MAX][MAX];
    int oferta[MAX];
    int demanda[MAX];

    // Arreglos para la lógica del VDA
    int vulnerabilidad[MAX];
    int orden_columnas[MAX];
    bool col_procesada[MAX];
    bool fila_agotada[MAX];

    // Inicializar matrices y arreglos de control
    for (int i = 0; i < MAX; i++)
    {
        fila_agotada[i] = false;
        col_procesada[i] = false;
        vulnerabilidad[i] = 0;
        orden_columnas[i] = i; // Rellenamos con índices iniciales: 0, 1, 2...
        for (int j = 0; j < MAX; j++)
        {
            asignacion[i][j] = 0;
        }
    }

    // 1. INGRESO DE DATOS POR TECLADO
    cout << "=== SIMULADOR DE TRANSPORTE: METODO VDA ===" << endl;
    cout << "Ingrese la cantidad de Silos (Filas): ";
    cin >> M;
    cout << "Ingrese la cantidad de Molinos (Columnas): ";
    cin >> N;

    cout << "\n--- MATRIZ DE COSTOS ---" << endl;
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << "Costo Silo " << i + 1 << " -> Molino " << j + 1 << ": ";
            cin >> costos[i][j];
        }
    }

    cout << "\n--- VECTOR DE OFERTAS ---" << endl;
    for (int i = 0; i < M; i++)
    {
        cout << "Oferta del Silo " << i + 1 << ": ";
        cin >> oferta[i];
    }

    cout << "\n--- VECTOR DE DEMANDAS ---" << endl;
    for (int j = 0; j < N; j++)
    {
        cout << "Demanda del Molino " << j + 1 << ": ";
        cin >> demanda[j];
    }

    // 2. PASO 1 DEL VDA: CALCULAR LA VULNERABILIDAD (Suma de columnas)
    for (int j = 0; j < N; j++)
    {
        for (int i = 0; i < M; i++)
        {
            vulnerabilidad[j] += costos[i][j];
        }
    }

    // 3. PASO 2 DEL VDA: ORDENAR COLUMNAS DE MAYOR A MENOR VULNERABILIDAD
    // Usamos un ordenamiento de burbuja (Bubble Sort)
    for (int i = 0; i < N - 1; i++)
    {
        for (int j = 0; j < N - i - 1; j++)
        {
            // Comparamos los valores de vulnerabilidad
            if (vulnerabilidad[orden_columnas[j]] < vulnerabilidad[orden_columnas[j + 1]])
            {
                // Intercambiamos los índices en nuestro arreglo de orden
                int temp = orden_columnas[j];
                orden_columnas[j] = orden_columnas[j + 1];
                orden_columnas[j + 1] = temp;
            }
        }
    }

    // 4. PASO 3 DEL VDA: BUCLE PRINCIPAL DE ASIGNACIÓN
    // Recorremos las columnas en el orden de vulnerabilidad calculado
    for (int c = 0; c < N; c++)
    {
        int j = orden_columnas[c]; // Obtenemos el índice real de la columna más vulnerable

        // Mientras esa columna todavía tenga demanda pendiente por cumplir
        while (demanda[j] > 0)
        {
            int mejor_i = -1;
            int min_costo = 999999;

            // Buscamos el costo mínimo disponible en esa columna entre los silos vivos
            for (int i = 0; i < M; i++)
            {
                if (!fila_agotada[i] && costos[i][j] < min_costo)
                {
                    min_costo = costos[i][j];
                    mejor_i = i;
                }
            }

            // Si por alguna razón de balanceo no encuentra filas vivas, rompemos
            if (mejor_i == -1)
                break;

            // Calculamos la cantidad de unidades a asignar (el menor entre oferta y demanda)
            int unidades = oferta[mejor_i];
            if (demanda[j] < unidades)
            {
                unidades = demanda[j];
            }

            // Registramos la asignación y actualizamos los saldos
            asignacion[mejor_i][j] = unidades;
            oferta[mejor_i] -= unidades;
            demanda[j] -= unidades;

            // Si el silo se quedó sin inventario, lo marcamos como agotado
            if (oferta[mejor_i] == 0)
            {
                fila_agotada[mejor_i] = true;
            }
        }
        // Al salir del while, la columna queda satisfecha
        col_procesada[j] = true;
    }

    // 5. IMPRESIÓN DE RESULTADOS
    cout << "\n=============================================" << endl;
    cout << "   MATRIZ DE ASIGNACION FINAL (SOLUCION VDA)  " << endl;
    cout << "=============================================" << endl;

    int costo_total = 0;
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << asignacion[i][j] << "\t";
            if (asignacion[i][j] > 0)
            {
                costo_total += (asignacion[i][j] * costos[i][j]);
            }
        }
        cout << endl;
    }

    cout << "\n---------------------------------------------" << endl;
    cout << "COSTO TOTAL DEL SISTEMA (Z): " << costo_total << endl;
    cout << "---------------------------------------------" << endl;

    return 0;
}