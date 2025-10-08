#include <iostream>
using namespace std;
const int MAX_VERTICES = 25;
int main() {
    int vertices;
    cout << "Ingrese el número de vértices del grafo: ";
    cin >> vertices;
    if (vertices > MAX_VERTICES) {
        cout << "El grafo solo puede tener hasta 25 vértices." << endl;
        return 1;
    }
    int grafo[vertices][vertices] = {0}; // matriz adyacente
    cout << "Ingrese el número de aristas: ";
    int aris;
    cin >> aris;
    for (int i = 0; i < aris; i++) {
        int u, v;
        cout << "Arista (" << i + 1 << "): vértice inicial y final separados por espacio: ";
        cin >> u >> v;
        grafo[u][v] = grafo[v][u] = 1; // grafo es dirigido
    }
    int addVertices = 0;  // Calcular grado impar
    for (int i = 0; i < vertices; i++) {
        int degree = 0;
        for (int j = 0; j < vertices; j++) {
            degree += grafo[i][j];
        }
        if (degree & 1) addVertices++;
    }
    if (addVertices > 2) { cout << endl;
        cout << "El grafo no tiene camino o circuito euleriano." << endl;
        return 0;
    }
    bool visited[vertices] = {false};  //algoritmo de Fleury
    int actualVertice = 0;
    bool encontrado = false;
    while (true) {
        bool noVisitado = false;
        for (int i = 0; i < vertices; i++) {
            if (!visited[i]) {
                noVisitado = true;
                break;
            }
        }   
        if (!noVisitado) break;
        bool puente = false;
        int nextVertice = -1;
        for (int i = 0; i < vertices; i++) {
            if (!visited[i] && grafo[actualVertice][i] == 1) {
                visited[i] = true;
                nextVertice = i;
                int contar = 0;  //si es un puente
                for (int j = 0; j < vertices; j++) {
                    if (grafo[j][i] == 1 && !visited[j]) {
                        contar++;
                    }
                }
                grafo[actualVertice][i]--;
                grafo[i][actualVertice]--;
                bool esPuente = true; //vértices alcanzables
                for (int j = 0; j < vertices; j++) {
                    if (!visited[j] && grafo[actualVertice][j] == 1) {
                        int contarDes = 0;
                        for (int k = 0; k < vertices; k++) {
                            if (grafo[j][k] == 1 && !visited[k]) {
                                contarDes++;
                            }
                        }
                        if (contar > contarDes) {
                            esPuente = false;
                            break;
                        }
                    }
                }
                if (esPuente) {
                    puente = true;
                    break;
                }
            }
        }
        if (!puente) { cout << endl; cout << "Vertice escogido es: " << endl;
            cout << actualVertice + 1 << " ";
            visited[actualVertice] = true;
        } else { cout << endl; cout << "Vertice escogido es: " <<endl;
            cout << actualVertice + 1 << " ";
            visited[actualVertice] = true;
        }
        
        if (nextVertice != -1) {
            actualVertice = nextVertice;
        } else {
            break;
        }
    }
    cout << "\nCamino euleriano encontrado:" << endl;
    for (int i = 0; i < vertices; i++) {
        if (!visited[i]) {
            cout << (i + 1) << " ";
        }
    }
    return 0;
}
