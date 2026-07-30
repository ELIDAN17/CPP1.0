#ifndef HASH_LOGIC_H
#define HASH_LOGIC_H

#include <iostream>
#include <vector>
#include <list>
#include <string>

using namespace std;

struct Record
{
    string key;
    string value;
};

// --- ENCADENAMIENTO SEPARADO ---
class HashTableChaining
{
private:
    int size;
    vector<list<Record>> table;
    int collisions;

public:
    HashTableChaining(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
    }
    int hashFunction(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }
    void insert(string key, string value)
    {
        int index = hashFunction(key);
        if (!table[index].empty())
            collisions++;
        table[index].push_back({key, value});
    }
    int getCollisions() { return collisions; }
    double loadFactor(int n) { return (double)n / size; }
};

// --- SONDEO LINEAL ---
class HashTableLinear
{
private:
    int size;
    vector<Record> table;
    vector<bool> occupied;
    int collisions;

public:
    HashTableLinear(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
        occupied.resize(size, false);
    }
    int hashFunction(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }
    void insert(string key, string value)
    {
        int index = hashFunction(key);
        while (occupied[index])
        {
            collisions++;
            index = (index + 1) % size;
        }
        table[index] = {key, value};
        occupied[index] = true;
    }
    int getCollisions() { return collisions; }
};

// --- DOBLE HASHING ---
class HashTableDouble
{
private:
    int size;
    vector<Record> table;
    vector<bool> occupied;
    int collisions;
    int prime;

public:
    HashTableDouble(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
        occupied.resize(size, false);
        prime = 10007;
    }
    int hash1(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }
    int hash2(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 17 + c;
        return prime - (hash % prime);
    }
    void insert(string key, string value)
    {
        int index = hash1(key);
        int step = hash2(key);
        while (occupied[index])
        {
            collisions++;
            index = (index + step) % size;
        }
        table[index] = {key, value};
        occupied[index] = true;
    }
    int getCollisions() { return collisions; }
};

#endif

/*
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <chrono>
#include <string>

using namespace std;

// Estructura para almacenar los datos
struct Record
{
    string key;
    string value;
};

// --- 1. ENCADENAMIENTO SEPARADO ---
class HashTableChaining
{
private:
    int size;
    vector<list<Record>> table;
    int collisions;

public:
    HashTableChaining(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
    }

    int hashFunction(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }

    void insert(string key, string value)
    {
        int index = hashFunction(key);
        if (!table[index].empty())
            collisions++;
        table[index].push_back({key, value});
    }

    string search(string key)
    {
        int index = hashFunction(key);
        for (const auto &r : table[index])
        {
            if (r.key == key)
                return r.value;
        }
        return "No encontrado";
    }

    int getCollisions() { return collisions; }
    double loadFactor(int totalElements) { return (double)totalElements / size; }
};

// --- 2. SONDEO LINEAL ---
class HashTableLinear
{
private:
    int size;
    vector<Record> table;
    vector<bool> occupied;
    int collisions;

public:
    HashTableLinear(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
        occupied.resize(size, false);
    }

    int hashFunction(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }

    void insert(string key, string value)
    {
        int index = hashFunction(key);
        while (occupied[index])
        {
            collisions++;
            index = (index + 1) % size;
        }
        table[index] = {key, value};
        occupied[index] = true;
    }

    string search(string key)
    {
        int index = hashFunction(key);
        int start = index;
        while (occupied[index])
        {
            if (table[index].key == key)
                return table[index].value;
            index = (index + 1) % size;
            if (index == start)
                break;
        }
        return "No encontrado";
    }

    int getCollisions() { return collisions; }
};

// --- 3. DOBLE HASHING (ESTO FALTABA EN EL PDF) ---
class HashTableDouble
{
private:
    int size;
    vector<Record> table;
    vector<bool> occupied;
    int collisions;
    int prime; // Primo menor que el tamaño de la tabla

public:
    HashTableDouble(int tableSize) : size(tableSize), collisions(0)
    {
        table.resize(size);
        occupied.resize(size, false);
        prime = 10007; // Debe ser menor a tableSize
    }

    int hash1(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 31 + c;
        return hash % size;
    }

    int hash2(string key)
    {
        unsigned long hash = 0;
        for (char c : key)
            hash = hash * 17 + c;
        return prime - (hash % prime);
    }

    void insert(string key, string value)
    {
        int index = hash1(key);
        if (occupied[index])
        {
            int step = hash2(key);
            while (occupied[index])
            {
                collisions++;
                index = (index + step) % size;
            }
        }
        table[index] = {key, value};
        occupied[index] = true;
    }

    string search(string key)
    {
        int index = hash1(key);
        int step = hash2(key);
        int start = index;
        while (occupied[index])
        {
            if (table[index].key == key)
                return table[index].value;
            index = (index + step) % size;
            if (index == start)
                break;
        }
        return "No encontrado";
    }

    int getCollisions() { return collisions; }
};

// --- LECTURA DE CSV MEJORADA ---
vector<string> readKeysFromCSV(string filename, int limit)
{
    vector<string> keys;
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "Error: No se pudo abrir " << filename << endl;
        return keys;
    }
    string line;
    getline(file, line); // Saltar cabecera
    while (getline(file, line) && keys.size() < limit)
    {
        stringstream ss(line);
        string column;
        if (getline(ss, column, ','))
        { // Lee la primera columna (StockCode / UserID)
            keys.push_back(column);
        }
    }
    return keys;
}

int main()
{
    string filename = "online_retail_II.csv"; // Asegúrate de que el nombre sea correcto
    int limit = 5000;
    int tableSize = 20011;

    vector<string> keys = readKeysFromCSV(filename, limit);
    if (keys.empty())
        return 1;

    HashTableChaining hashChain(tableSize);
    HashTableLinear hashLinear(tableSize);
    HashTableDouble hashDouble(tableSize);

    // --- Ejecución y Medición ---
    cout << "EJECUTANDO EXPERIMENTO CON N=" << keys.size() << "..." << endl
         << endl;

    // Medir Encadenamiento
    auto start = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashChain.insert(k, k);
    auto end = chrono::high_resolution_clock::now();
    // Corrección: Usar milliseconds (plural) y cast explícito
    auto t_ins_chain = chrono::duration_cast<chrono::milliseconds>(end - start);

    // Medir Lineal
    start = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashLinear.insert(k, k);
    end = chrono::high_resolution_clock::now();
    auto t_ins_linear = chrono::duration_cast<chrono::milliseconds>(end - start);

    // Medir Doble
    start = chrono::high_resolution_clock::now();
    for (string k : keys)
        hashDouble.insert(k, k);
    end = chrono::high_resolution_clock::now();
    auto t_ins_double = chrono::duration_cast<chrono::milliseconds>(end - start);

    // --- MOSTRAR RESULTADOS ---
    // Usamos .count() para imprimir el valor numérico
    cout << "Metodo\t\tColisiones\tTiempo Ins. (ms)" << endl;
    cout << "------------------------------------------------" << endl;
    cout << "Encadenamiento\t" << hashChain.getCollisions() << "\t\t" << t_ins_chain.count() << endl;
    cout << "Sondeo Lineal\t" << hashLinear.getCollisions() << "\t\t" << t_ins_linear.count() << endl;
    cout << "Doble Hashing\t" << hashDouble.getCollisions() << "\t\t" << t_ins_double.count() << endl;

    return 0;
}*/