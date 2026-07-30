#include <iostream>
using namespace std;
/*
template <class T>
class Nodo{
    private: T info; NodoArbol<T> *HijoIzquierdo; NodoArbol<T> *HijoDerecho;
    public: NodoArbol(); T regresaInfo();
};
template<class T>
class Arbol{
    private: Nodo<T> *raiz;
    public:Arbol(){raiz=nullptr;}
    void insertar(T v){
        Nodo<T> *n=new Nodo<T>(v);
        if(raiz==nullptr)
    }
};
template <class T>
NodoArbol<T>::NodoArbol(){HijoIzquierdo=NULL; HijoDerecho=NULL;}
template <class T>
T NodoArbol<T>::regresaInfo(){return info;}
*/

//template <class T>
//ArbolBinario<T>::ArbolBinario(){raiz=NULL;}
/*
template <class T>
void ArbolBin<T>::CrearArbol(NodoArbol<T> *Apunta){
    char respuesta;
    Apunta= new NodoArbol<T>;
    cout<<"ingrese info: "; cin>>Apunta->info;
    cout<<Apunta->info<<"tiene hijo izquierdo (S/N)?"; cin>>respuesta;
    if(Respuesta == ´S´){
        CrearArbol(Apunta->HijoIzquierdo);
        Apunta->HijoIzquierdo=raiz;
    }
    cout<<Apunta->info<<"tiene hijo Derecho (S/N)?"; cin>>respuesta;
    if(Respuesta == ´S´){
        CrearArbol(Apunta->HijoDerecho);
        Apunta->HijoDerecho=raiz;
    }
    raiz=Apunta;
}*/
/*
int main(){
    Arbol<string> *ar = new Arbol<string>();
    ar->insertar("maria");
    ar->insertar("JUana");
    return 0;
}*/



/*
class Nodo {
public:
    int valor;
    Nodo* izquierdo;
    Nodo* derecho;
    
    Nodo(int val) : valor(val), izquierdo(nullptr), derecho(nullptr) {}
};

class ArbolBinario {
private:
    Nodo* raiz;
    
public:
    ArbolBinario() : raiz(nullptr) {}
    
    ~ArbolBinario() {
        borrar(raiz);
    }
    
    void insertar(int valor) {
        raiz = insertar(valor, raiz);
    }
    
    void imprimirPreorden() {
        imprimirPreorden(raiz);
        cout << endl;
    }
    
    void imprimirEntreorden() {
        imprimirEntreorden(raiz);
        cout << endl;
    }
    
    void imprimirPosorden() {
        imprimirPosorden(raiz);
        cout << endl;
    }
    
private:
    Nodo* insertar(int valor, Nodo* nodo) {
        if (nodo == nullptr) {
            return new Nodo(valor);
        }
        
        if (valor < nodo->valor) {
            nodo->izquierdo = insertar(valor, nodo->izquierdo);
        } else {
            nodo->derecho = insertar(valor, nodo->derecho);
        }
        
        return nodo;
    }
    
    void imprimirPreorden(Nodo* nodo) { //raiz izquierda derecha
        if (nodo != nullptr) {
            cout << nodo->valor << " ";
            imprimirPreorden(nodo->izquierdo);
            imprimirPreorden(nodo->derecho);
        }
    }
    
    void imprimirEntreorden(Nodo* nodo) { //izquierdo raiz derecho
        if (nodo != nullptr) {
            imprimirEntreorden(nodo->izquierdo);
            cout << nodo->valor << " ";
            imprimirEntreorden(nodo->derecho);
        }
    }
    
    void imprimirPosorden(Nodo* nodo) { //izquierdo derecho raiz
        if (nodo != nullptr) {
            imprimirPosorden(nodo->izquierdo);
            imprimirPosorden(nodo->derecho);
            cout << nodo->valor << " ";
        }
    }
    
    void borrar(Nodo* nodo) {
        if (nodo == nullptr) return;
        
        borrar(nodo->izquierdo);
        borrar(nodo->derecho);
        delete nodo;
    }
};

int main() {
    ArbolBinario arbol;
    
    arbol.insertar(50);
    arbol.insertar(30);
    arbol.insertar(70);
    arbol.insertar(20);
    arbol.insertar(40);
    arbol.insertar(60);
    arbol.insertar(80);
    
    cout << "Imprimir preorden: ";
    arbol.imprimirPreorden();
    
    cout << "Imprimir entreorden: ";
    arbol.imprimirEntreorden();
    
    cout << "Imprimir posorden: ";
    arbol.imprimirPosorden();
    
    return 0;
}
*/

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
        void Imprimir() const {
        std::cout << dato << " ";
        if (hijoIzq != NULL) hijoIzq->Imprimir();
        if (hijoDer != NULL) hijoDer->Imprimir();
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
        void PreOrden() const {
        if (raiz != nullptr) {
            raiz->Imprimir();
            PreOrden(raiz->retHijoIzq());
            PreOrden(raiz->retHijoDer());
        }
    }

    void PostOrden() const {
        if (raiz != nullptr) {
            PostOrden(raiz->retHijoIzq());
            PostOrden(raiz->retHijoDer());
            raiz->Imprimir();
        }
    }

    void EnProfundidad() const {
        if (raiz != nullptr) {
            EnProfundidad(raiz);
        }
    }

    void BuscarBinaria(T valor) const {
        Nodo<T> *actual = raiz;
        while (actual != nullptr) {
            if (valor == actual->retDato()) {
                cout << "Elemento encontrado: " << valor << endl;
                return;
            } else if (valor < actual->retDato()) {
                actual = actual->retHijoIzq();
            } else {
                actual = actual->retHijoDer();
            }
        }
        cout << "Elemento no encontrado." << endl;
    }
    void Imprimir() const {
        if (raiz != nullptr) {
            raiz->Imprimir();
        }   
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
private:
    void PreOrden(Nodo<T>* nodo) const {
        if (nodo != nullptr) {
            nodo->Imprimir();
            PreOrden(nodo->retHijoIzq());
            PreOrden(nodo->retHijoDer());
        }
    }

    void PostOrden(Nodo<T>* nodo) const {
        if (nodo != nullptr) {
            PostOrden(nodo->retHijoIzq());
            PostOrden(nodo->retHijoDer());
            nodo->Imprimir();
        }
    }

    void EnProfundidad(Nodo<T>* nodo) const {
        if (nodo != nullptr) {
            EnProfundidad(nodo->retHijoIzq());
            cout << nodo->retDato() << " ";
            EnProfundidad(nodo->retHijoDer());
        }
    }
    
    
};

int main() {
    Arbol<int> *ar = new Arbol<int>();

    ar->Insertar(23);
    ar->Insertar(14);
    ar->Insertar(7);
    ar->Insertar(5);
    ar->Insertar(8);
    ar->Insertar(12);
    ar->Insertar(18);
    ar->Insertar(25);

    cout << "Preorden: ";
    ar->PreOrden();
    cout << "\nPostorden: ";
    ar->PostOrden();
    cout << "\nEnprofundidad: ";
    ar->EnProfundidad();

    int valorABuscar = 14;
    cout << "\nBusqueda binaria de " << valorABuscar << ": ";
    ar->BuscarBinaria(valorABuscar);

    return 0;
}

