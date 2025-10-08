
template <class T>
class Lista{
private:
    Nodo<T> *pri;
    Nodo<T> *ult;
public:
    Lista(){
        pri = ult = NULL;
    }
    void insertInicio(T v){
        Nodo<T> *n = new Nodo<T>(v);
        if (pri == NULL)
            pri = ult = n;
        else{
           n->unirCon(pri);
           pri = n;
        }
    }
    void insertFinal(T v){
        Nodo<T> *n = new Nodo<T>(v);
        if (pri == NULL)
            pri = ult = n;
        else{
           ult->unirCon(n);
           ult = n;
        }
    }
    void eliminarPrimero(){
        if(pri != NULL){
            Nodo<T> * temp = pri;
            pri = temp->retSig();
            delete temp;
            if(pri == NULL){
                pri = ult = NULL;
            }
        }
    }

    void mostrarDatos(){
        Nodo<T> *temp = pri;
        while(temp != NULL){
            cout<<temp->retDato()<<endl;
            temp = temp->retSig();
        }
    }
};
