#include "grafo_puno.hpp"
#include <queue>
#include <unordered_set>
#include <chrono>

std::vector<std::vector<int>> componentesConexas(
    const GrafoPuno &g, const std::unordered_set<int> &excluidos = {})
{
    std::vector<std::vector<int>> componentes;
    std::unordered_set<int> visitados = excluidos;
    for (int inicio = 0; inicio < g.numVertices(); inicio++)
    {
        if (visitados.count(inicio))
            continue;
        std::vector<int> comp;
        std::queue<int> cola;
        cola.push(inicio);
        visitados.insert(inicio);
        while (!cola.empty())
        {
            int u = cola.front();
            cola.pop();
            comp.push_back(u);
            for (auto &[v, _] : g.vecinos(u))
                if (!visitados.count(v) && !excluidos.count(v))
                {
                    visitados.insert(v);
                    cola.push(v);
                }
        }
        componentes.push_back(comp);
    }
    return componentes;
}

int main()
{
    auto t0 = std::chrono::high_resolution_clock::now();

    GrafoPuno g(14);
    std::vector<std::tuple<int, int, int>> rutas = {
        {0, 1, 44}, {0, 2, 55}, {0, 5, 80}, {1, 6, 37}, {1, 7, 70}, {1, 11, 90}, {2, 3, 50}, {2, 4, 45}, {3, 4, 25}, {5, 4, 60}, {7, 8, 95}, {7, 10, 110}, {7, 11, 75}, {8, 9, 40}, {11, 12, 140}, {11, 13, 180}};
    for (auto &[u, v, p] : rutas)
        g.agregarArista(u, v, p);

    auto t1 = std::chrono::high_resolution_clock::now();

    std::cout << "V=" << g.numVertices() << " E=" << g.numAristas()
              << " densidad=" << g.densidad() << '\n';

    std::cout << "\nGrado de cada ciudad:\n";
    for (int i = 0; i < g.numVertices(); i++)
        std::cout << "  " << g.nombreCiudad(i) << ": " << g.grado(i) << '\n';

    auto comp = componentesConexas(g);
    auto t2 = std::chrono::high_resolution_clock::now();

    std::cout << "\nComponentes (sin bloqueos): " << comp.size() << '\n';
    for (auto &c : comp)
    {
        std::cout << "  [";
        for (size_t i = 0; i < c.size(); i++)
        {
            std::cout << g.nombreCiudad(c[i]);
            if (i + 1 < c.size())
                std::cout << ", ";
        }
        std::cout << "]\n";
    }

    auto compLluvia = componentesConexas(g, {12, 13});
    std::cout << "\nComponentes (Macusani/Sandia bloqueadas): "
              << compLluvia.size() << '\n';
    for (auto &c : compLluvia)
    {
        std::cout << "  [";
        for (size_t i = 0; i < c.size(); i++)
        {
            std::cout << g.nombreCiudad(c[i]);
            if (i + 1 < c.size())
                std::cout << ", ";
        }
        std::cout << "]\n";
    }

    auto t3 = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::micro> tConstruccion = t1 - t0;
    std::chrono::duration<double, std::micro> tComponentes = t2 - t1;
    std::chrono::duration<double, std::micro> tTotal = t3 - t0;

    std::cout << "\n--- Tiempos de ejecucion (C++17, -O2) ---\n";
    std::cout << "Construccion del grafo: " << tConstruccion.count() << " us\n";
    std::cout << "Calculo de componentes: " << tComponentes.count() << " us\n";
    std::cout << "Total: " << tTotal.count() << " us\n";

    return 0;
}