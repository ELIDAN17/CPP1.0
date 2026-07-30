#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>
#include <numeric>
#include <iomanip>
#include <string>
using namespace std;
int busquedaLineal(const vector<int> &a, int x)
{
    for (size_t i = 0; i < a.size(); ++i)
    {
        if (a[i] == x)
            return (int)i;
    }
    return -1;
}
int busquedaBinaria(const vector<int> &a, int x)
{
    int l = 0, r = (int)a.size() - 1;
    while (l <= r)
    {
        int m = l + (r - l) / 2;
        if (a[m] == x)
            return m;
        if (a[m] < x)
            l = m + 1;
        else
            r = m - 1;
    }
    return -1;
}
int busquedaExponencial(const vector<int> &a, int x)
{
    if (a.empty())
        return -1;
    if (a[0] == x)
        return 0;
    int i = 1;
    int n = (int)a.size();
    while (i < n && a[i] < x)
        i <<= 1;
    int l = i / 2, r = min(i, n - 1);
    while (l <= r)
    {
        int m = l + (r - l) / 2;
        if (a[m] == x)
            return m;
        if (a[m] < x)
            l = m + 1;
        else
            r = m - 1;
    }
    return -1;
}
int busquedaInterpolacion(const vector<int> &a, int x)
{
    int low = 0, high = (int)a.size() - 1;
    while (low <= high && x >= a[low] && x <= a[high])
    {
        if (low == high)
            return (a[low] == x ? low : -1);
        long long pos = low + (long long)((double)(high - low) * (x - a[low]) / (a[high] - a[low]));
        if (pos < low || pos > high)
            break;
        if (a[pos] == x)
            return (int)pos;
        if (a[pos] < x)
            low = (int)pos + 1;
        else
            high = (int)pos - 1;
    }
    return -1;
}
template <class F> // Utilidades de medicion
double medir(const vector<int> &a, const vector<int> &queries, F buscador)
{
    auto t0 = chrono::high_resolution_clock::now();
    volatile long long checksum = 0;
    for (int x : queries)
    {
        checksum += buscador(a, x);
    }
    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double, milli> ms = t1 - t0;
    return ms.count() / (double)queries.size();
}
int main()
{
    ios::sync_with_stdio(false); // Optimización de E/S
    cin.tie(nullptr);
    // Tamaños solicitados: 10^4, 10^5, 5*10^5
    vector<int> ns = {10000, 100000, 500000};
    mt19937 rng(123);
    cout << fixed << setprecision(6);
    cout << "Algoritmos de Busqueda\n";
    cout << "==========================================================\n";
    for (int n : ns)
    {
        vector<int> uni(n); // Uniforme ordenado
        iota(uni.begin(), uni.end(), 0);
        vector<int> ses(n); // Sesgado ordenado (80% en 10% del rango)
        for (int i = 0; i < n; i++)
        {
            double u = uniform_real_distribution<double>(0, 1)(rng);
            if (u < 0.8)
                ses[i] = uniform_int_distribution<int>(0, (int)(0.1 * n))(rng);
            else
                ses[i] = uniform_int_distribution<int>((int)(0.1 * n), 5 * n)(rng);
        }
        sort(ses.begin(), ses.end());
        vector<int> des = uni; // Desordenado
        shuffle(des.begin(), des.end(), rng);
        // Generación (70% Hits, 30% Misses)
        auto mkqueries = [&](const vector<int> &base)
        {
            vector<int> q;
            q.reserve(1000);
            uniform_int_distribution<int> idx(0, (int)base.size() - 1);
            for (int i = 0; i < 700; i++)
                q.push_back(base[idx(rng)]); // Hits
            for (int i = 0; i < 300; i++)
                q.push_back((int)(base.size() * 10 + i)); // Misses
            shuffle(q.begin(), q.end(), rng);
            return q;
        };
        auto q_uni = mkqueries(uni);
        auto q_ses = mkqueries(ses);
        auto q_des = mkqueries(des);
        auto report = [&](const string &nombre, const vector<int> &arr, const vector<int> &q, bool ordenado)
        {
            cout << "\n[RESULTADOS] n = " << n << " | Dataset: " << nombre << "\n";
            cout << "  - Lineal:        " << medir(arr, q, busquedaLineal) << " ms/busq\n";
            if (ordenado)
            {
                cout << "  - Binaria:       " << medir(arr, q, busquedaBinaria) << " ms/busq\n";
                cout << "  - Exponencial:   " << medir(arr, q, busquedaExponencial) << " ms/busq\n";
                cout << "  - Interpolacion: " << medir(arr, q, busquedaInterpolacion) << " ms/busq\n";
            }
            else
            {
                cout << "  - (Algoritmos ordenados omitidos para este dataset)\n";
            }
        };
        report("Uniforme Ordenado", uni, q_uni, true);
        report("Sesgado Ordenado", ses, q_ses, true);
        report("Desordenado", des, q_des, false);
        cout << "----------------------------------------------------------\n";
    }
    return 0;
}