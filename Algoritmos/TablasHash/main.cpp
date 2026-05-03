#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <chrono>
#include "logica.h" // Importamos nuestra lógica

using namespace std;

vector<string> readKeysFromCSV(string filename, int limit)
{
    vector<string> keys;
    ifstream file(filename);
    if (!file.is_open())
        return keys;

    string line;
    getline(file, line); // Saltar cabecera
    while (getline(file, line) && keys.size() < limit)
    {
        stringstream ss(line);
        string column;
        if (getline(ss, column, ','))
            keys.push_back(column);
    }
    return keys;
}

int main()
{
    // string filename = "online_retail_II.csv";
    string filename = "C:\\Users\\Kira\\Uni\\projetcs\\trabalo\\Algoritmos\\TablasHash\\online_retail_II.csv";
    int n = 5000;
    int m = 20011;

    vector<string> keys = readKeysFromCSV(filename, n);
    if (keys.empty())
    {
        cout << "Error al leer el archivo." << endl;
        return 1;
    }

    HashTableChaining hashChain(m);
    HashTableLinear hashLinear(m);
    HashTableDouble hashDouble(m);

    cout << "--- RESULTADOS EXPERIMENTALES (C++) ---" << endl;

    // Medir Encadenamiento
    auto s1 = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashChain.insert(k, k);
    auto e1 = chrono::high_resolution_clock::now();
    auto t1 = chrono::duration_cast<chrono::milliseconds>(e1 - s1);

    // Medir Lineal
    auto s2 = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashLinear.insert(k, k);
    auto e2 = chrono::high_resolution_clock::now();
    auto t2 = chrono::duration_cast<chrono::milliseconds>(e2 - s2);

    // Medir Doble
    auto s3 = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashDouble.insert(k, k);
    auto e3 = chrono::high_resolution_clock::now();
    auto t3 = chrono::duration_cast<chrono::milliseconds>(e3 - s3);

    // Salida de datos para el informe
    cout << "Metodo\t\tColisiones\tTiempo (ms)" << endl;
    cout << "Encadenamiento\t" << hashChain.getCollisions() << "\t\t" << t1.count() << endl;
    cout << "Sondeo Lineal\t" << hashLinear.getCollisions() << "\t\t" << t2.count() << endl;
    cout << "Doble Hashing\t" << hashDouble.getCollisions() << "\t\t" << t3.count() << endl;

    return 0;
}