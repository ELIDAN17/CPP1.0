#include <iostream>
using namespace std;

<node.h>  
template < class morph > 
class ttnode{ 
    private: 
        morph r_val; 
        ttnode <morph> *r_next; 
    public: 
        ttnode(){ 
            r_next = NULL; 
        }//bb 
        ttnode ( morph e_val ){ 
            r_next = NULL; 
            r_val = e_val; 
        }//bb 
        void f_joincon ( ttnode <morph> *e_ttnode ){ 
            r_next = e_ttnode; 
        }//mth 
        ttnode <morph> *f_getnext(){ 
            return ( r_next ); 
        } 
        morph f_getval(){ 
            return ( r_val ); 
        }//mth; 
        void f_plotval(){ 
            cout << r_val << endl; 
        }//mth 
};//clss 
 
 
 
<pile.h> 
template < class morph > //ccpile 
class superpile{ 
    private: 
        ttnode <morph> *r_head; 
    public: 
        superpile(){ 
            r_head = NULL; 
        };//bb 
        void f_push ( morph e_val, char e_position = 'b' ){ 
            ttnode <morph> *element = new ttnode <morph> ( e_val ); 
            if ( r_head == NULL ){ 
                element->f_joincon ( r_head ); 
                r_head = element; 
            }//cd  
            else{ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                if ( e_position == 'f' || e_position == 'F' ){ 
                    while ( aux->f_getnext() != NULL ){ 
                        aux = aux->f_getnext(); 
                    }//wh 
                    aux->f_joincon ( element ); 
                    element->f_joincon ( NULL ); 
                }//cd 
                else if ( e_position == 'b' || e_position == 'B' ){ 
                    element->f_joincon ( r_head ); 
                    r_head = element; 
                }//cd 
                aux = NULL; 
                delete ( aux ); 
            }//cd 
        }//mth 
        void f_plotdoublepile(){ 
            if ( r_head != NULL ){ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                while ( aux->f_getnext() != NULL ){ 
                    aux->f_plotval(); 
                    aux = aux->f_getnext(); 
                } 
                aux->f_plotval(); 
                aux = NULL; 
                delete ( aux ); 
            } 
        }//mth 
        void f_pop ( char e_position = 'b' ){ 
            if ( r_head != NULL ){ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                if ( e_position == 'f' || e_position == 'F' ){ 
                    ttnode <morph> *zaux = new ttnode <morph>; 
                    if ( aux->f_getnext() != NULL ){ 
                        while ( aux->f_getnext() != NULL ){ 
                            zaux = aux; 
                            aux = aux->f_getnext(); 
                        }//wh 
                        zaux->f_joincon( NULL ); 
                    }//cd 
                    else{ 
                        delete ( r_head ); 
                        r_head = NULL; 
                        aux = NULL; 
                    }//cd 
                    zaux = NULL; 
                    delete ( zaux ); 
                    delete ( aux ); 
                }//cd 
                else if ( e_position == 'b' || e_position == 'B' ){ 
                    aux = aux->f_getnext(); 
                    delete ( r_head ); 
                    r_head = aux; 
                    aux = NULL; 
                    delete ( aux ); 
                }//cd 
            }//cd 
        }//mth 
        int f_size(){ 
            if ( r_head == NULL ){ 
                return ( 0 ); 
            }//cd 
            else if ( r_head->f_getnext() == NULL ){ 
                return ( 1 ); 
            }//cd 
            else{ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                int val = 0; 
                while ( aux->f_getnext() != NULL ){ 
                    val++; 
                    aux = aux->f_getnext(); 
                }//wh 
                val++; 
                return ( val ); 
            }//cd 
        }//mth 
        int f_getindex ( int e_val ){ 
            if ( r_head != NULL ){ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                int x = 0; 
                while ( aux->f_getnext() != NULL && aux->f_getval() != e_val ){ 
                    x++; 
                    aux = aux->f_getnext(); 
                }//wh 
                if ( e_val != aux->f_getval() ){ 
                    return ( -1 ); 
                }//cd 
                else{ 
                    return ( x ); 
                }//cd 
            }//cd 
            else{ 
                return ( -1 ); 
            }//cd 
        }//mth 
        morph f_getvalbyindex ( int e_index ){ 
            if ( r_head == NULL ){ 
                return ( -1 ); 
            }//cd 
            else{ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_head; 
                int pos = 0; 
                while ( pos < e_index && aux->f_getnext() != NULL ){ 
                    aux = aux->f_getnext(); 
                    pos++; 
                }//wh 
                if ( e_index == pos ){ 
                    return ( aux->f_getval() ); 
                }//cd 
                else{ 
                    return ( -1 ); 
                }//cd 
            }//cd 
        }//mth 
        morph f_getval (){ 
            if ( r_head != NULL ){ 
                return ( r_head->f_getval() ); 
            }//mth 
        }//mth 
};//css 
 
 
<ccpile.h> 
template < class morph > 
class ttccpile{ 
    private: 
        ttnode <morph> *r_spv; 
        ttnode <morph> *r_pck; 
    public: 
        ttlist(){ 
            r_spv = NULL; 
            r_pck = NULL; 
        }//bb 
        void f_pop (){ 
            if ( r_spv == NULL ){ 
                cout << "Empty" << endl; 
            }//cd 
            else if( r_spv != NULL && r_spv != r_spv->f_getnext() ){ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_spv; 
                while ( aux->f_getnext() != r_spv ){ 
                    aux = aux->f_getnext(); 
                }//wh 
                aux->f_joincon( r_spv->f_getnext() ); 
                delete ( r_spv ); 
                r_spv = aux; 
            }//cd 
            else if ( r_spv == r_spv->f_getnext() ){ 
                delete ( r_spv ); 
                r_spv = NULL; 
                r_pck = NULL; 
            }//cd 
        }//mth 
        void f_push ( morph e_val ){ 
            ttnode <morph> *member = new ttnode <morph> ( e_val ); 
            if ( r_spv == NULL ){ 
                member->f_joincon ( member ); 
                r_spv = member; 
                r_pck = member; 
            }//cd 
            member->f_joincon ( r_spv->f_getnext() ); 
            r_spv->f_joincon ( member ); 
            r_spv = member; 
        }//mth 
        void f_plotpile(){ 
            if ( r_spv != NULL ){ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_spv; 
                aux = aux->f_getnext(); 
                while ( aux != r_spv ){ 
                    aux->f_plotval(); 
                    aux = aux->f_getnext(); 
                }//wh 
                aux->f_plotval(); 
                aux = NULL; 
                delete ( aux ); 
            }//cd 
        }//mth 
        void f_plotval(){ 
            if ( r_pck != NULL ){ 
                r_pck->f_plotval(); 
            }//cd 
        }//mth 
        void f_roamer( int e_distance = 1 ){ 
            if ( r_spv != NULL ){ 
                for ( int n = 0; n < e_distance; n++ ){ 
                    r_pck = r_pck->f_getnext(); 
                }//fr 
            }//cd 
            else{ 
                cout << "Empty" << endl; 
            }//cd 
        }//mth 
        void f_popval(){ 
            if ( r_pck == NULL ){ 
                if ( r_pck == r_pck->f_getnext() ){ 
                    delete ( r_pck ); 
                    r_pck = NULL; 
                    r_spv = NULL; 
                }//cd 
                else{ 
                    ttnode <morph> *aux = new ttnode <morph>; 
                    aux = r_spv; 
                    while ( aux->f_getnext() != r_pck ){ 
                        aux = aux->f_getnext(); 
                    }//wh 
                    aux->f_joincon ( r_pck->f_getnext() ); 
                    delete ( r_pck ); 
                    if ( r_spv == r_pck ){ 
                        r_spv = aux; 
                    } 
                    r_pck = aux->f_getnext(); 
                    aux = NULL; 
                    delete ( aux ); 
                }//cd 
            }//cd 
        }//mth 
        void f_restart(){ 
            r_pck = r_spv->f_getnext(); 
        }//mth 
        morph f_getval (){ 
            if ( r_spv != NULL ){ 
                return ( r_spv->f_getval() ); 
            }//cd 
        }//mth 
        int f_size(){ 
            if ( r_spv == NULL ){ 
                return ( 0 ); 
            }//cd 
            else if ( r_spv == r_spv->f_getnext() ){ 
                return ( 1 ); 
            } 
            else{ 
                ttnode <morph> *aux = new ttnode <morph>; 
                aux = r_spv; 
                int n = 0; 
                while ( aux->f_getnext() != r_spv ){ 
                    n++; 
                    aux = aux->f_getnext(); 
                }//wh 
                return ( n + 1 ); 
            }//cd 
        }//cd 
};//css 
 
//EJERCICIOS 
//EJERCICIO 01 
 
#include “node.h” 
#include “pile.h” 
 
string f_invert ( string entry ){ 
    string rtrn; 
    for ( int n = entry.size() - 1; n > - 1; n-- ){ 
        rtrn += entry[n]; 
    }//fr 
    return ( rtrn ); 
}//fc 
int main(){ 
    superpile <char> *ops; 
    ops = new superpile <char>(); 
    string operations = "(1*(2-3))+(4+5)"; 
    string result; 
    int parenthesis = 0; 
    operations = f_invert ( operations ); 
    for ( char part: operations ){ 
        if ( part != '+' && part != '-' && part != '*' && part != '/' && part 
            != '(' && part != ')' ){ 
            result += part; 
        }//cd 
        else{ 
            if ( part == '+' || part == '-' || part == '*' || part == '/' ){ 
                ops->f_push ( part ); 
            } 
            else if ( part == ')' ){ 
                ops->f_push ( part ); 
                parenthesis++; 
            }//cd 
            else if ( part == '(' && parenthesis != 0 ){ 
                while ( ops->f_getval() != ')' ){ 
                    result += ops->f_getval(); 
                    ops->f_pop(); 
                }//wh 
                parenthesis--; 
                ops->f_pop(); 
            }//cd 
        }//cd 
    }//fr 
    if ( ops->f_size() != 0 ){ 
        for ( int n = ops->f_size(); n > 0; n-- ){ 
            result += ops->f_getval(); 
            ops->f_pop(); 
        }//fr 
    }//cd 
    result = f_invert ( result ); 
    cout << result; 
    return (0); 
} 
 
 
//EJERCICIO 03 
 
//#include “node.h” 
//#include “pile.h” 
 
int main(){ 
    superpile <int> *ress; 
    superpile <int> *ops; 
    ops = new superpile <int>(); 
    ress = new superpile <int>(); 
    ress->f_push ( 450 ); 
    ress->f_push ( 450 ); 
    ress->f_push ( 1500 ); 
    ress->f_push ( 1285 ); 
    ress->f_push ( 1285 ); 
    ress->f_push ( 1285 ); 
    ress->f_push ( 879 ); 
    for ( int n = ress->f_size(); n > 0; n-- ){ 
        ops->f_push ( ress->f_getval() ); 
        ress->f_pop(); 
    }//fr 
    int last; 
    int ssz = ops->f_size(); 
    for ( int n = ops->f_size(); n > 0; n-- ){ 
        if ( n == ssz ){ 
            ress->f_push ( ops->f_getval() ); 
            last = ops->f_getval(); 
        }//cd 
        else{ 
            if ( ops->f_getval() != last ){ 
                ress->f_push ( ops->f_getval() ); 
                last = ops->f_getval(); 
            }//cd 
        }//cd 
        ops->f_pop(); 
    }//fr 
    ress->f_plotdoublepile(); 
    return 0; 
}//main

//EJERCICIO 04 
#include <iostream> 
//#include “node.h” 
//#include “pile.h” 
using namespace std; 
int main(){ 
    superpile <int> *ress; 
    superpile <int> *ops; 
    ops = new superpile <int>(); 
    ress = new superpile <int>(); 
    ress->f_push ( 928 ); 
    ress->f_push ( 3209 ); 
    ress->f_push ( 1024 ); 
    ress->f_push ( 623 ); 
    for ( int n = ress->f_size(); n > 0; n-- ){ 
        ops->f_push ( ress->f_getval() ); 
        ress->f_pop(); 
    }//fr 
    ops->f_plotdoublepile(); 
    return 0; 
}//main

//EJERCICIO 06 
#include <iostream> 
//#include “node.h” 
//#include “pile.h” 
using namespace std; 
int main(){ 
    superpile <int> *ress; 
    superpile <int> *ops; 
    ops = new superpile <int>(); 
    ress = new superpile <int>(); 
    ress->f_push ( 928 ); 
    ress->f_push ( 3209 ); 
    ress->f_push ( 1024 ); 
    ress->f_push ( 623 ); 
    for ( int n = ress->f_size(); n > 0; n-- ){ 
        ops->f_push ( ress->f_getval() ); 
        ress->f_pop(); 
    }//fr 
    ops->f_plotdoublepile(); 
    return 0; 
}//main

//EJERCICIO 07 
#include <iostream> 
//#include “node.h” 
//#include “pile.h” 
using namespace std; 
template < class morph > 
void *f_invertpile ( superpile <morph> *e_pile, superpile <morph> *r_pile = NULL ){ 
    if ( r_pile == NULL ){ 
        r_pile = new superpile <morph>(); 
    }//cd 
    r_pile->f_push ( e_pile->f_getval() ); 
    e_pile->f_pop(); 
    if ( e_pile->f_size() - 1 > 0 ){ 
        f_invertpile ( e_pile, r_pile ); 
    }//cd 
    else{ 
        e_pile = r_pile; 
    }//cd 
}//cd 
int main(){ 
    superpile <int> *ress; 
    ress = new superpile <int> (); 
    ress->f_push ( 1 ); 
    ress->f_push ( 2 ); 
    ress->f_push ( 3 ); 
    ress->f_push ( 4 ); 
    ress->f_plotdoublepile(); 
    f_invertpile ( ress ); 
    ress->f_plotdoublepile(); 
    return 0; 
}//main 

//EJERCICIO 08 
#include <iostream> 
//#include “node.h” 
//#include “ccpile.h” 
using namespace std; 
int main(){ 
    ttccpile <int> *cirpilefinal = new ttccpile <int> (); 
    ttccpile <int> *cirpileops = new ttccpile <int> (); 
    cirpilefinal->f_push ( 87 ); 
    cirpilefinal->f_push ( 54 ); 
    cirpilefinal->f_push ( 54 ); 
    cirpilefinal->f_push ( 54 ); 
    cirpilefinal->f_push ( 91 ); 
    cirpilefinal->f_push ( 91 ); 
    cirpilefinal->f_push ( 69 ); 
    cirpilefinal->f_push ( 69 ); 
    cirpilefinal->f_push ( 69 ); 
    cirpilefinal->f_push ( 1 ); 
    for ( int n = cirpilefinal->f_size(); n > 0; n-- ){ 
        cirpileops->f_push ( cirpilefinal->f_getval() ); 
        cirpilefinal->f_pop(); 
    }//fr 
    int last; 
    int ssz = cirpileops->f_size(); 
    for ( int n = cirpileops->f_size(); n > 0; n-- ){ 
        if ( n == ssz ){ 
            cirpilefinal->f_push ( cirpileops->f_getval() ); 
            last = cirpileops->f_getval(); 
        }//cd 
        else{ 
            if ( cirpileops->f_getval() != last ){ 
                cirpilefinal->f_push ( cirpileops->f_getval() ); 
                last = cirpileops->f_getval(); 
            }//cd 
        }//cd 
        cirpileops->f_pop(); 
    }//fr 
    cirpilefinal->f_plotpile(); 
    return ( 0 ); 
}//main 

//EJERCICIO 11 
 
//#include “node.h” 
//#include “ccpile.h” 
 
int main(){ cout<<"EJERCICIO 11"<<endl; 
    ttccpile <int> *bank_user_entry = new ttccpile <int> (); 
    ttccpile <int> *bank_user_number = new ttccpile <int> (); 
    char choose; 
    int number; 
    int customers = 0; 
    while ( choose != 'x' && choose != 'X' ){ 
        cout << "Option: "; 
        cin >> choose; 
        if ( choose == 'a' ){ 
            cout << "DNI: "; 
            cin >> number; 
            bank_user_entry->f_push ( number ); 
            bank_user_number->f_push ( number ); 
        }//cd 
        else if ( choose == 'b' ){ 
            cout << "DNI de cliente: "; 
            cin >> number; 
            for ( int n = 0; n < bank_user_entry->f_size() + 1; n++ ){ 
                if ( bank_user_entry->f_getval() != number ){ 
                    bank_user_entry->f_roamer(); 
                    bank_user_number->f_roamer(); 
                    choose = 'f'; 
                }//cd 
                else{ 
                    choose = 't'; 
                } 
            }//fr 
            if ( choose == 't' ){ 
                cout << "Usuario Detectado - " << number << endl; 
                cout << "N° de Ventanilla: "; 
                cin >> number; 
                bank_user_number->f_rplc ( number ); 
            }//cd 
        }//cd 
        bank_user_entry->f_restart(); 
        bank_user_number->f_restart(); 
    }//wh 
    for ( int n = bank_user_entry->f_size(); n > 0; n-- ){ 
        if ( bank_user_entry->f_getval() == bank_user_number->f_getval() ){ 
            customers++; 
        }//cd 
        bank_user_entry->f_roamer(); 
        bank_user_number->f_roamer(); 
    }//fr 
    cout << "Clientes atendidos: " << customers; 
    return 0;
}//main


/*
class Pila{
    Nodo* cima;
    public: Pila(){cima=NULL;}
    void Push(int v){
        Nodo *n = new Nodo(v);
        if(cima==NULL){cima=n;}
        else{n->unirCon(cima); cima=n;}
        n->unirCon(cima); cima=n;
    }
    void Pop(){
        if(cima !=NULL){
            Nodo *temp = cima;
            cima=temp->retSig();
            delete temp;
        }
    }
    void mostrarDatos(){
        Nodo *temp =cima;
        while (temp !=NULL){
            cout<<temp->retDato()<<endl; 
            temp =temp->retSig();
        }
    }
    int Size(){
        Nodo *temp = cima; int i=0;
        while(temp !=NULL){
            i++; temp = temp ->retSig();
        }
        return i;
    }
};
*/