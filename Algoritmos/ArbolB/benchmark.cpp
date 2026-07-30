// benchmark.cpp
#include <iostream>
#include <chrono>
#include <random>
#include <set>
#include "biblioteca.hpp"

using namespace std;

vector<string> generarCodigos(int n)
{
    set<string> codigos;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distClase(0, 999);
    uniform_int_distribution<> distSubclase(0, 999);
    uniform_int_distribution<> distLetra(0, 25);
    uniform_int_distribution<> distNum(1, 99);

    while ((int)codigos.size() < n)
    {
        string clase = to_string(distClase(gen));
        clase = string(3 - clase.length(), '0') + clase;

        string subclase = to_string(distSubclase(gen));
        subclase = string(3 - subclase.length(), '0') + subclase;

        char letra = 'A' + distLetra(gen);
        int num = distNum(gen);

        string codigo = clase + "." + subclase + " " + letra + to_string(num);
        codigos.insert(codigo);
    }

    return vector<string>(codigos.begin(), codigos.end());
}

void benchmarkOrden(int t, int n)
{
    cout << "\n🔬 t = " << t << " | n = " << n << " registros" << endl;

    ArbolBBiblioteca arbol(t);
    vector<string> codigos = generarCodigos(n);

    auto inicio = chrono::high_resolution_clock::now();

    for (const auto &cod : codigos)
    {
        Libro libro{cod, "Titulo", "Autor", true};
        arbol.insertar(cod, libro);
    }

    auto fin = chrono::high_resolution_clock::now();
    auto duracion = chrono::duration_cast<chrono::milliseconds>(fin - inicio);

    int altura = arbol.altura();
    int maxClavesPorNodo = 2 * t - 1;

    cout << "  ⏱️ Inserción: " << duracion.count() << " ms" << endl;
    cout << "  📐 Altura: " << altura << endl;
    cout << "  📊 Claves/nodo (máx): " << maxClavesPorNodo << endl;
}

int main()
{
    int n = 1000000;
    cout << "=" << 60 << endl;
    cout << "📊 BENCHMARK - ÁRBOL B" << endl;
    cout << "=" << 60 << endl;
    cout << "Comparando diferentes órdenes t para n=" << n << " registros\n"
         << endl;

    for (int t : {2, 10, 50, 100, 500})
    {
        benchmarkOrden(t, n);
    }

    cout << "\n✅ Benchmark completado" << endl;
    return 0;
}