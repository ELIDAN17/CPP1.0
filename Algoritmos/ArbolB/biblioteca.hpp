// biblioteca.hpp
#pragma once

#include <vector>
#include <memory>
#include <string>
#include <algorithm>
#include <iostream>

struct Libro
{
    std::string codigoTopo;
    std::string titulo;
    std::string autor;
    bool disponible = true;
};

struct NodoB
{
    std::vector<std::string> claves;
    std::vector<Libro> libros;
    std::vector<std::unique_ptr<NodoB>> hijos;
    bool esHoja = true;
};

class ArbolBBiblioteca
{
private:
    int t;
    std::unique_ptr<NodoB> raiz;

    // ==================== BÚSQUEDA ====================

    std::pair<NodoB *, int> buscar(NodoB *nodo, const std::string &codigo)
    {
        int i = 0;
        while (i < (int)nodo->claves.size() && codigo > nodo->claves[i])
        {
            i++;
        }

        if (i < (int)nodo->claves.size() && codigo == nodo->claves[i])
        {
            return {nodo, i};
        }

        if (nodo->esHoja)
        {
            return {nullptr, -1};
        }

        return buscar(nodo->hijos[i].get(), codigo);
    }

    // ==================== SPLIT ====================

    void split(NodoB *padre, int i, NodoB *y)
    {
        auto z = std::make_unique<NodoB>();
        z->esHoja = y->esHoja;

        // Mover mitad superior a z
        z->claves.assign(y->claves.begin() + t, y->claves.end());
        z->libros.assign(y->libros.begin() + t, y->libros.end());

        if (!y->esHoja)
        {
            for (size_t k = t; k < y->hijos.size(); k++)
            {
                z->hijos.push_back(std::move(y->hijos[k]));
            }
        }

        // Guardar clave media
        std::string claveMedia = y->claves[t - 1];
        Libro libroMedio = y->libros[t - 1];

        // Reducir y
        y->claves.resize(t - 1);
        y->libros.resize(t - 1);
        if (!y->esHoja)
        {
            y->hijos.resize(t);
        }

        // Insertar z en padre
        padre->hijos.insert(padre->hijos.begin() + i + 1, std::move(z));
        padre->claves.insert(padre->claves.begin() + i, claveMedia);
        padre->libros.insert(padre->libros.begin() + i, libroMedio);
    }

    // ==================== INSERCIÓN ====================

    void insertarNoLleno(NodoB *nodo, const std::string &codigo, Libro libro)
    {
        int i = (int)nodo->claves.size() - 1;

        if (nodo->esHoja)
        {
            nodo->claves.push_back("");
            nodo->libros.push_back(Libro{});

            while (i >= 0 && codigo < nodo->claves[i])
            {
                nodo->claves[i + 1] = nodo->claves[i];
                nodo->libros[i + 1] = nodo->libros[i];
                i--;
            }

            nodo->claves[i + 1] = codigo;
            nodo->libros[i + 1] = std::move(libro);
        }
        else
        {
            while (i >= 0 && codigo < nodo->claves[i])
            {
                i--;
            }
            i++;

            if ((int)nodo->hijos[i]->claves.size() == 2 * t - 1)
            {
                split(nodo, i, nodo->hijos[i].get());
                if (codigo > nodo->claves[i])
                {
                    i++;
                }
            }

            insertarNoLleno(nodo->hijos[i].get(), codigo, std::move(libro));
        }
    }

public:
    ArbolBBiblioteca(int orden = 50) : t(orden)
    {
        raiz = std::make_unique<NodoB>();
        raiz->esHoja = true;
    }

    // ==================== BÚSQUEDA PÚBLICA ====================

    bool buscar(const std::string &codigo)
    {
        auto [nodo, idx] = buscar(raiz.get(), codigo);
        return nodo != nullptr;
    }

    // ==================== INSERCIÓN PÚBLICA ====================

    void insertar(const std::string &codigo, Libro libro)
    {
        if ((int)raiz->claves.size() == 2 * t - 1)
        {
            auto nuevaRaiz = std::make_unique<NodoB>();
            nuevaRaiz->esHoja = false;
            nuevaRaiz->hijos.push_back(std::move(raiz));
            split(nuevaRaiz.get(), 0, nuevaRaiz->hijos[0].get());
            raiz = std::move(nuevaRaiz);
        }

        insertarNoLleno(raiz.get(), codigo, std::move(libro));
    }

    // ==================== ALTURA ====================

    int altura()
    {
        return alturaRec(raiz.get());
    }

    int alturaRec(NodoB *nodo)
    {
        if (nodo->esHoja)
            return 1;
        return 1 + alturaRec(nodo->hijos[0].get());
    }

    // ==================== RECORRIDO IN-ORDER ====================

    void inorder()
    {
        inorderRec(raiz.get());
        std::cout << "\n";
    }

    void inorderRec(NodoB *nodo)
    {
        if (nodo->esHoja)
        {
            for (const auto &clave : nodo->claves)
            {
                std::cout << clave << " ";
            }
        }
        else
        {
            for (size_t i = 0; i < nodo->claves.size(); i++)
            {
                inorderRec(nodo->hijos[i].get());
                std::cout << nodo->claves[i] << " ";
            }
            inorderRec(nodo->hijos.back().get());
        }
    }
};