#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>
using namespace std;
using namespace chrono;

// ------------------------- BUBBLE SORT -------------------------
void bubbleSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// ------------------------- INSERTION SORT -------------------------
void insertionSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 1; i < n; i++)
    {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// ------------------------- MERGE SORT -------------------------
void merge(vector<int> &arr, int left, int mid, int right)
{
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }

    while (i < n1)
        arr[k++] = L[i++];
    while (j < n2)
        arr[k++] = R[j++];
}

void mergeSort(vector<int> &arr, int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

// ------------------------- QUICK SORT -------------------------
int partition(vector<int> &arr, int low, int high)
{
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int> &arr, int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// ------------------------- FUNCIÓN PARA MEDIR TIEMPO -------------------------
double medirTiempo(void (*func)(vector<int> &), vector<int> arr, string nombre)
{
    auto inicio = high_resolution_clock::now();
    func(arr);
    auto fin = high_resolution_clock::now();
    duration<double, milli> elapsed = fin - inicio;
    return elapsed.count();
}

double medirTiempoMerge(vector<int> &arr, string nombre)
{
    auto inicio = high_resolution_clock::now();
    mergeSort(arr, 0, arr.size() - 1);
    auto fin = high_resolution_clock::now();
    duration<double, milli> elapsed = fin - inicio;
    return elapsed.count();
}

double medirTiempoQuick(vector<int> &arr, string nombre)
{
    auto inicio = high_resolution_clock::now();
    quickSort(arr, 0, arr.size() - 1);
    auto fin = high_resolution_clock::now();
    duration<double, milli> elapsed = fin - inicio;
    return elapsed.count();
}

// ------------------------- GENERAR DATOS DE PRUEBA -------------------------
vector<int> generarAleatorio(int n)
{
    vector<int> arr(n);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(1, 10000);
    for (int i = 0; i < n; i++)
        arr[i] = dis(gen);
    return arr;
}

vector<int> generarOrdenado(int n)
{
    vector<int> arr(n);
    for (int i = 0; i < n; i++)
        arr[i] = i + 1;
    return arr;
}

vector<int> generarInverso(int n)
{
    vector<int> arr(n);
    for (int i = 0; i < n; i++)
        arr[i] = n - i;
    return arr;
}

// ------------------------- MENÚ PRINCIPAL -------------------------
int main()
{
    cout << "\n===============================================\n";
    cout << "   ANÁLISIS DE ALGORITMOS DE ORDENAMIENTO\n";
    cout << "===============================================\n";

    vector<int> tamanos = {1000, 5000, 10000};
    vector<string> tipos = {"Aleatoria", "Ordenada", "Inversa"};

    cout << "\n📊 RESULTADOS (tiempos en milisegundos):\n\n";

    for (int n : tamanos)
    {
        cout << "\n🔹 TAMAÑO: " << n << " elementos\n";
        cout << "------------------------------------------------\n";

        // Aleatoria
        vector<int> aleatorio = generarAleatorio(n);
        vector<int> ordenado = generarOrdenado(n);
        vector<int> inverso = generarInverso(n);

        // Bubble Sort (solo para 1000, porque es muy lento)
        if (n == 1000)
        {
            cout << "Bubble Sort:\n";
            cout << "  Aleatoria: " << medirTiempo(bubbleSort, aleatorio, "Bubble") << " ms\n";
            cout << "  Ordenada: " << medirTiempo(bubbleSort, ordenado, "Bubble") << " ms\n";
            cout << "  Inversa: " << medirTiempo(bubbleSort, inverso, "Bubble") << " ms\n";
        }
        else
        {
            cout << "Bubble Sort: [DEMASIADO LENTO para n=" << n << ", no se ejecutó]\n";
        }

        // Insertion Sort
        cout << "Insertion Sort:\n";
        cout << "  Aleatoria: " << medirTiempo(insertionSort, aleatorio, "Insertion") << " ms\n";
        cout << "  Ordenada: " << medirTiempo(insertionSort, ordenado, "Insertion") << " ms\n";
        cout << "  Inversa: " << medirTiempo(insertionSort, inverso, "Insertion") << " ms\n";

        // Merge Sort
        cout << "Merge Sort:\n";
        vector<int> arrMerge = aleatorio;
        cout << "  Aleatoria: " << medirTiempoMerge(arrMerge, "Merge") << " ms\n";
        arrMerge = ordenado;
        cout << "  Ordenada: " << medirTiempoMerge(arrMerge, "Merge") << " ms\n";
        arrMerge = inverso;
        cout << "  Inversa: " << medirTiempoMerge(arrMerge, "Merge") << " ms\n";

        // Quick Sort
        cout << "Quick Sort:\n";
        vector<int> arrQuick = aleatorio;
        cout << "  Aleatoria: " << medirTiempoQuick(arrQuick, "Quick") << " ms\n";
        arrQuick = ordenado;
        cout << "  Ordenada: " << medirTiempoQuick(arrQuick, "Quick") << " ms\n";
        arrQuick = inverso;
        cout << "  Inversa: " << medirTiempoQuick(arrQuick, "Quick") << " ms\n";
    }

    cout << "\n===============================================\n";
    cout << "   FIN DEL ANÁLISIS\n";
    cout << "===============================================\n";

    return 0;
}