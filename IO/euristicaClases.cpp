#include <iostream>

using namespace std;

const int MAX = 20;

// Prototipos de las funciones para mantener el código organizado
void calcularEsquinaNoroeste(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX]);
void calcularCostoMinimo(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX]);
void calcularVogel(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX]);

int main()
{
    int M, N;
    int costos[MAX][MAX];

    // Arreglos originales para lectura por teclado
    int oferta_orig[MAX];
    int demanda_orig[MAX];

    // Arreglos temporales para pasar copias a las funciones
    int oferta[MAX], demanda[MAX];

    cout << "=== SIMULADOR UNIFICADO DE METODOS CLASICOS ===" << endl;
    cout << "Ingrese la cantidad de Filas (Silos): ";
    cin >> M;
    cout << "Ingrese la cantidad de Molinos (Columnas): ";
    cin >> N;

    cout << "\n--- MATRIZ DE COSTOS ---" << endl;
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << "Costo [" << i + 1 << "][" << j + 1 << "]: ";
            cin >> costos[i][j];
        }
    }

    cout << "\n--- VECTOR DE OFERTAS ---" << endl;
    for (int i = 0; i < M; i++)
    {
        cout << "Oferta de Fila " << i + 1 << ": ";
        cin >> oferta_orig[i];
    }

    cout << "\n--- VECTOR DE DEMANDAS ---" << endl;
    for (int j = 0; j < N; j++)
    {
        cout << "Demanda de Columna " << j + 1 << ": ";
        cin >> demanda_orig[j];
    }

    // --- 1. EJECUCIÓN: ESQUINA NOROESTE ---
    for (int i = 0; i < M; i++)
        oferta[i] = oferta_orig[i];
    for (int j = 0; j < N; j++)
        demanda[j] = demanda_orig[j];
    calcularEsquinaNoroeste(M, N, costos, oferta, demanda);

    // --- 2. EJECUCIÓN: COSTO MÍNIMO ---
    for (int i = 0; i < M; i++)
        oferta[i] = oferta_orig[i];
    for (int j = 0; j < N; j++)
        demanda[j] = demanda_orig[j];
    calcularCostoMinimo(M, N, costos, oferta, demanda);

    // --- 3. EJECUCIÓN: VOGEL ---
    for (int i = 0; i < M; i++)
        oferta[i] = oferta_orig[i];
    for (int j = 0; j < N; j++)
        demanda[j] = demanda_orig[j];
    calcularVogel(M, N, costos, oferta, demanda);

    return 0;
}

// =================================================================
// 1. MÉTODO DE LA ESQUINA NOROESTE
// =================================================================
void calcularEsquinaNoroeste(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX])
{
    int asignacion[MAX][MAX] = {0};
    int i = 0, j = 0;

    while (i < M && j < N)
    {
        int unidades = (oferta[i] < demanda[j]) ? oferta[i] : demanda[j];

        asignacion[i][j] = unidades;
        oferta[i] -= unidades;
        demanda[j] -= unidades;

        if (oferta[i] == 0)
            i++;
        else
            j++;
    }

    int Z = 0;
    cout << "\n>>> MATRIZ ASIGNACION - ESQUINA NOROESTE <<<\n";
    for (int r = 0; r < M; r++)
    {
        for (int c = 0; c < N; c++)
        {
            cout << asignacion[r][c] << "\t";
            Z += asignacion[r][c] * costos[r][c];
        }
        cout << endl;
    }
    cout << "Costo Total Esquina Noroeste (Z) = " << Z << "\n-----------------------------------------\n";
}

// =================================================================
// 2. MÉTODO DEL COSTO MÍNIMO
// =================================================================
void calcularCostoMinimo(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX])
{
    int asignacion[MAX][MAX] = {0};
    bool fila_out[MAX] = {false};
    bool col_out[MAX] = {false};

    while (true)
    {
        int min_costo = 999999;
        int mejor_i = -1, mejor_j = -1;

        // Buscar la celda con el menor costo global que siga activa
        for (int i = 0; i < M; i++)
        {
            if (fila_out[i])
                continue;
            for (int j = 0; j < N; j++)
            {
                if (!col_out[j] && costos[i][j] < min_costo)
                {
                    min_costo = costos[i][j];
                    mejor_i = i;
                    mejor_j = j;
                }
            }
        }

        if (mejor_i == -1)
            break; // Ya no hay celdas disponibles

        int unidades = (oferta[mejor_i] < demanda[mejor_j]) ? oferta[mejor_i] : demanda[mejor_j];
        asignacion[mejor_i][mejor_j] = unidades;
        oferta[mejor_i] -= unidades;
        demanda[mejor_j] -= unidades;

        if (oferta[mejor_i] == 0)
            fila_out[mejor_i] = true;
        if (demanda[mejor_j] == 0)
            col_out[mejor_j] = true;
    }

    int Z = 0;
    cout << "\n>>> MATRIZ ASIGNACION - COSTO MINIMO <<<\n";
    for (int r = 0; r < M; r++)
    {
        for (int c = 0; c < N; c++)
        {
            cout << asignacion[r][c] << "\t";
            Z += asignacion[r][c] * costos[r][c];
        }
        cout << endl;
    }
    cout << "Costo Total Costo Minimo (Z) = " << Z << "\n-----------------------------------------\n";
}

// =================================================================
// 3. MÉTODO DE APROXIMACIÓN DE VOGEL (VAM)
// =================================================================
void calcularVogel(int M, int N, int costos[MAX][MAX], int oferta[MAX], int demanda[MAX])
{
    int asignacion[MAX][MAX] = {0};
    bool fila_out[MAX] = {false};
    bool col_out[MAX] = {false};

    while (true)
    {
        // Verificar si quedan al menos celdas vivas
        int filas_vivas = 0, cols_vivas = 0;
        int ultima_fila = -1, ultima_col = -1;
        for (int i = 0; i < M; i++)
            if (!fila_out[i])
            {
                filas_vivas++;
                ultima_fila = i;
            }
        for (int j = 0; j < N; j++)
            if (!col_out[j])
            {
                cols_vivas++;
                ultima_col = j;
            }

        if (filas_vivas == 0 || cols_vivas == 0)
            break;

        // Caso especial de arrastre: Si solo queda una fila viva, vaciar todo el inventario
        if (filas_vivas == 1)
        {
            for (int j = 0; j < N; j++)
            {
                if (!col_out[j])
                {
                    int unidades = (oferta[ultima_fila] < demanda[j]) ? oferta[ultima_fila] : demanda[j];
                    asignacion[ultima_fila][j] = unidades;
                    oferta[ultima_fila] -= unidades;
                    demanda[j] -= unidades;
                    if (demanda[j] == 0)
                        col_out[j] = true;
                }
            }
            fila_out[ultima_fila] = true;
            continue;
        }
        // Si solo queda una columna viva, vaciar en ella
        if (cols_vivas == 1)
        {
            for (int i = 0; i < M; i++)
            {
                if (!fila_out[i])
                {
                    int unidades = (oferta[i] < demanda[ultima_col]) ? oferta[i] : demanda[ultima_col];
                    asignacion[i][ultima_col] = unidades;
                    oferta[i] -= unidades;
                    demanda[ultima_col] -= unidades;
                    if (oferta[i] == 0)
                        fila_out[i] = true;
                }
            }
            col_out[ultima_col] = true;
            continue;
        }

        // CALCULO DE PENALIZACIONES
        int p_fila[MAX] = {0};
        int p_col[MAX] = {0};

        // Penalización de Filas
        for (int i = 0; i < M; i++)
        {
            if (fila_out[i])
                continue;
            int m1 = 999999, m2 = 999999;
            for (int j = 0; j < N; j++)
            {
                if (col_out[j])
                    continue;
                if (costos[i][j] < m1)
                {
                    m2 = m1;
                    m1 = costos[i][j];
                }
                else if (costos[i][j] < m2)
                {
                    m2 = costos[i][j];
                }
            }
            p_fila[i] = (m2 == 999999) ? 0 : (m2 - m1);
        }

        // Penalización de Columnas
        for (int j = 0; j < N; j++)
        {
            if (col_out[j])
                continue;
            int m1 = 999999, m2 = 999999;
            for (int i = 0; i < M; i++)
            {
                if (fila_out[i])
                    continue;
                if (costos[i][j] < m1)
                {
                    m2 = m1;
                    m1 = costos[i][j];
                }
                else if (costos[i][j] < m2)
                {
                    m2 = costos[i][j];
                }
            }
            p_col[j] = (m2 == 999999) ? 0 : (m2 - m1);
        }

        // ENCONTRAR LA MÁXIMA PENALIZACIÓN
        int max_p = -1;
        bool es_fila = true;
        int linea_elegida = -1;

        for (int i = 0; i < M; i++)
        {
            if (!fila_out[i] && p_fila[i] > max_p)
            {
                max_p = p_fila[i];
                es_fila = true;
                linea_elegida = i;
            }
        }
        for (int j = 0; j < N; j++)
        {
            if (!col_out[j] && p_col[j] > max_p)
            {
                max_p = p_col[j];
                es_fila = false;
                linea_elegida = j;
            }
        }

        // ENCONTRAR EL MENOR COSTO EN LA LÍNEA SELECCIONADA Y ASIGNAR
        int mejor_i = -1, mejor_j = -1;
        int min_val = 999999;

        if (es_fila)
        {
            mejor_i = linea_elegida;
            for (int j = 0; j < N; j++)
            {
                if (!col_out[j] && costos[mejor_i][j] < min_val)
                {
                    min_val = costos[mejor_i][j];
                    mejor_j = j;
                }
            }
        }
        else
        {
            mejor_j = linea_elegida;
            for (int i = 0; i < M; i++)
            {
                if (!fila_out[i] && costos[i][mejor_j] < min_val)
                {
                    min_val = costos[i][mejor_j];
                    mejor_i = i;
                }
            }
        }

        int unidades = (oferta[mejor_i] < demanda[mejor_j]) ? oferta[mejor_i] : demanda[mejor_j];
        asignacion[mejor_i][mejor_j] = unidades;
        oferta[mejor_i] -= unidades;
        demanda[mejor_j] -= unidades;

        if (oferta[mejor_i] == 0)
            fila_out[mejor_i] = true;
        if (demanda[mejor_j] == 0)
            col_out[mejor_j] = true;
    }

    int Z = 0;
    cout << "\n>>> MATRIZ ASIGNACION - VOGEL <<<\n";
    for (int r = 0; r < M; r++)
    {
        for (int c = 0; c < N; c++)
        {
            cout << asignacion[r][c] << "\t";
            Z += asignacion[r][c] * costos[r][c];
        }
        cout << endl;
    }
    cout << "Costo Total Vogel (Z) = " << Z << "\n-----------------------------------------\n";
}