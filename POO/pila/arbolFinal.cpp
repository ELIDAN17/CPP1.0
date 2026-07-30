#include <iostream>
template <class T>
class Nodo{
    private:
        T dato;
        Nodo<T> *hijoDer;
        Nodo<T> *hijoIzq;
    public:
        Nodo(T v){
            dato = v;
            hijoDer = nullptr;
            hijoIzq = nullptr;
        }

        Nodo(){}

        Nodo<T> *retHijoDer(){
            return hijoDer;
        }
        Nodo<T> *retHijoIzq(){
            return hijoIzq;
        }
        T retDato(){
            return dato;
        }
        void unirConIzq(Nodo<T> *n){
            hijoIzq = n;
        }
        void unirConDer(Nodo<T> *n){
            hijoDer = n;
        }
};


template <class T>
class Arbol{
    private:
        Nodo<T> *raiz;
    public:
        Arbol(){
            raiz = nullptr;
        }
        void Insertar(T v){
            Nodo<T> *n = new Nodo<T>(v);
            if(raiz == nullptr)
                raiz = n;
            else
                Insertar(raiz, n, v);
        }
    protected:
        /*void Insertar(Nodo<T> *r, Nodo<T> *n, v){

            if(  comparo ){
                if(r -> izquierdo == NULL)
                    r->unirConIzq(n);
                else
                    Insertar(r->retHijoIzq(), n, v);
            }

        }*/
       bool comparar(T v1, T v2) {
        return v1 <= v2; // Asumiendo que queremos insertar en orden ascendente
    }
       void Insertar(Nodo<T>* r, Nodo<T>* n, T v) {
        if (comparar(v, r->retDato())) {
            if (r->retHijoIzq() == nullptr) {
                r->unirConIzq(n);
            } else {
                Insertar(r->retHijoIzq(), n, v);
            }
        } else {
            Insertar(r->retHijoDer(), n, v);
        }
    }


    void Imprimir() const {
    if (raiz != nullptr) {
        raiz->Imprimir();
    }
}

void Eliminar(T valor) {
    raiz = EliminarNodo(raiz, valor);
}

Nodo<T>* EliminarNodo(Nodo<T>* node, T valor) {
    if (node == nullptr) return node;

    if (valor < node->retDato()) {
        node->hijoIzquierdo = EliminarNodo(node->hijoIzquierdo, valor);
    } else if (valor > node->retDato()) {
        node->hijoDerecho = EliminarNodo(node->hijoDerecho, valor);
    } else {
        // Caso base: el nodo a eliminar es el actual
        if (node->hijoIzquierdo == nullptr && node->hijoDerecho == nullptr) {
            delete node;
            return nullptr;
        } else if (node->hijoIzquierdo == nullptr) {
            Nodo<T>* temp = node->hijoDerecho;
            delete node;
            return temp;
        } else if (node->hijoDerecho == nullptr) {
            Nodo<T>* temp = node->hijoIzquierdo;
            delete node;
            return temp;
        } else {
            // Reemplazar con el menor elemento del subárbol derecho
            Nodo<T>* temp = Minimo(node->hijoDerecho);
            node->retDato() = temp->retDato();
            node->hijoDerecho = EliminarNodo(node->hijoDerecho, temp->retDato());
        }
    }

    return node;
}

Nodo<T>* Minimo(Nodo<T>* node) {
    while (node->hijoIzquierdo != nullptr) {
        node = node->hijoIzquierdo;
    }
    return node;
}

    
    
};

int main()
{
    Arbol<int> *ar = new Arbol<int>();

    ar->Insertar(23);
    ar->Insertar(14);
    ar->Insertar(7);
    void Imprimir();

    return 0;

}