// https://dev.to/nokha_debbarma/implement-kruskal-s-algorithm-in-c-29cn

#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
class Arista
{
public:
    int vo, vd, p;
    Arista(int vo, int vd, int p)
    {
        this->vo = vo;
        this->vd = vd;
        this->p = p;
    }
};

class Graph
{
public:
    vector<Arista> Contenedor;
    void addArista(int o, int d, int p)
    {
        Arista obj(o, d, p);
        Contenedor.push_back(obj);
    }
};
void mostrarMST(const vector<Arista> &);

class Kruskal
{
public:
    int totalVertices;
    vector<pair<int, int>> almacen; // [padre-rango] compress
    vector<Arista> mst;             // contenedor MST
    Kruskal(int totalVertices)
    {
        this->totalVertices = totalVertices;
        almacen.resize(totalVertices); // ajuste
        for (int i = 0; i < totalVertices; ++i)
        {
            almacen[i].first = i;  // padre
            almacen[i].second = 0; // rank
        }
    }

    static bool comparador(Arista &a, Arista &b)
    {
        return a.p < b.p;
    }

    void crearMST(Graph &graph)
    {
        sort(graph.Contenedor.begin(), graph.Contenedor.end(), comparador); // orden
        int i = 0, e = 0;                                                   // i=full a y e=mst a (n-1)
        while (e < (totalVertices - 1) && i < graph.Contenedor.size())
        { // tamaño
            Arista actualArista = graph.Contenedor[i++];
            // ciclo mst
            int x = encontrar(actualArista.vo);
            int y = encontrar(actualArista.vd);
            if (x != y)
            {
                mst.push_back(actualArista);
                makeUnion(x, y);
                e++;
            }
        }
        mostrarMST(mst);
    }

    int encontrar(int i)
    {
        if (almacen[i].first != i)
        {
            almacen[i].first = encontrar(almacen[i].first);
        }
        return almacen[i].first;
    }

    void makeUnion(int x, int y)
    { // union-find
        int xraiz = encontrar(x);
        int yraiz = encontrar(y);
        if (almacen[xraiz].second < almacen[yraiz].second)
        { // decision padre
            almacen[xraiz].first = yraiz;
        }
        else if (almacen[xraiz].second > almacen[yraiz].second)
        {
            almacen[yraiz].first = xraiz;
        }
        else
        {
            almacen[xraiz].first = yraiz;
            almacen[yraiz].second++;
        }
    }
};

void mostrarMST(const vector<Arista> &Aristas)
{
    int totalMinimoCosto = 0;
    cout << "Todas las aristas del MST:\n[origen - destino = peso]\n";
    for (auto Arista : Aristas)
    {
        cout << "   " << Arista.vo << "    -    " << Arista.vd << "    =  " << Arista.p << '\n';
        totalMinimoCosto += Arista.p;
    }
    cout << "Costo minimo total = " << totalMinimoCosto << endl;
}

int main()
{
    Graph g;
    /*g.addArista(0, 1, 50);
    g.addArista(0, 2, 10);
    g.addArista(0, 3, 50);
    g.addArista(1, 4, 30);
    g.addArista(3, 4, 100);
    g.addArista(2, 4, 100);
    Kruskal graph(5);*/
    // A=0 ; B=1 ; C=2 ; D=3 ; E=4 ; F=5 ; G=6
    g.addArista(0, 1, 7);
    g.addArista(0, 3, 5);
    g.addArista(1, 3, 9);
    g.addArista(1, 2, 8);
    g.addArista(1, 4, 7);
    g.addArista(2, 4, 5);
    g.addArista(3, 4, 15);
    g.addArista(3, 5, 6);
    g.addArista(4, 5, 8);
    g.addArista(4, 6, 9);
    g.addArista(5, 6, 11);
    Kruskal graph(7);

    graph.crearMST(g);
    return 0;
}

/**********************************************
 ***Algoritmo: Minimum Spanning Tree - Kruskal
 ***Tipo: Teoria de Grafos
 ***Autor: Jhosimar George Arias Figueroa
 *********************************************/
/*
EJEMPLO DE INPUT
9 14
1 2 4
1 8 9
2 3 9
2 8 11
3 4 7
3 9 2
3 6 4
4 5 10
4 6 15
5 6 11
6 7 2
7 8 1
7 9 6
8 9 7
*/
/*
EJEMPLO VERIFICACION DE MST
9 11
1 2 4
1 8 9
2 3 9
2 8 11
3 9 2
7 8 1
7 9 6
8 9 7
4 5 10
4 6 15
5 6 11
*/
/*
#include <stdio.h>
#include <algorithm>
#include <cstring>

#define MAX 1005 // maximo numero de vértices

/// UNION-FIND
int padre[MAX]; // Este arreglo contiene el padre del i-esimo nodo

// Método de inicialización
void MakeSet(int n)
{
    for (int i = 1; i <= n; ++i)
        padre[i] = i;
}

// Método para encontrar la raiz del vértice actual X
int Find(int x)
{
    return (x == padre[x]) ? x : padre[x] = Find(padre[x]);
}

// Método para unir 2 componentes conexas
void Union(int x, int y)
{
    padre[Find(x)] = Find(y);
}

// Método que me determina si 2 vértices estan o no en la misma componente conexa
bool sameComponent(int x, int y)
{
    if (Find(x) == Find(y))
        return true;
    return false;
}
/// FIN UNION-FIND

int V, E; // numero de vertices y aristas
// Estructura arista( edge )
struct Edge
{
    int origen;  // Vértice origen
    int destino; // Vértice destino
    int peso;    // Peso entre el vértice origen y destino
    Edge() {}
    // Comparador por peso, me servira al momento de ordenar lo realizara en orden ascendente
    // Cambiar signo a > para obtener el arbol de expansion maxima
    bool operator<(const Edge &e) const
    {
        return peso < e.peso;
    }
} arista[MAX]; // Arreglo de aristas para el uso en kruskal
Edge MST[MAX]; // Arreglo de aristas del MST encontrado

void Kruskal()
{
    int origen, destino, peso;
    int total = 0;      // Peso total del MST
    int numAristas = 0; // Numero de Aristas del MST

    MakeSet(V);                    // Inicializamos cada componente
    std::sort(arista, arista + E); // Ordenamos las aristas por su comparador

    for (int i = 0; i < E; ++i)
    {                                // Recorremos las aristas ya ordenadas por peso
        origen = arista[i].origen;   // Vértice origen de la arista actual
        destino = arista[i].destino; // Vértice destino de la arista actual
        peso = arista[i].peso;       // Peso de la arista actual

        // Verificamos si estan o no en la misma componente conexa
        if (!sameComponent(origen, destino))
        {                                  // Evito ciclos
            total += peso;                 // Incremento el peso total del MST
            MST[numAristas++] = arista[i]; // Agrego al MST la arista actual
            Union(origen, destino);        // Union de ambas componentes en una sola
        }
    }

    // Si el MST encontrado no posee todos los vértices mostramos mensaje de error
    // Para saber si contiene o no todos los vértices basta con que el numero
    // de aristas sea igual al numero de vertices - 1
    if (V - 1 != numAristas)
    {
        puts("No existe MST valido para el grafo ingresado, el grafo debe ser conexo.");
        return;
    }
    puts("-----El MST encontrado contiene las siguientes aristas-----");
    for (int i = 0; i < numAristas; ++i)
        printf("( %d , %d ) : %d\n", MST[i].origen, MST[i].destino, MST[i].peso); //( vertice u , vertice v ) : peso

    printf("El costo minimo de todas las aristas del MST es : %d\n", total);
}

int main()
{
    int mst;

    scanf("%d %d", &V, &E);

    // Realizamos el ingreso del grafo, almacenando las aristas en un arreglo con los datos respectivos
    for (int i = 0; i < E; ++i)
        scanf("%d %d %d", &arista[i].origen, &arista[i].destino, &arista[i].peso);

    Kruskal();

    return 0;
}*/
