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
