#include <iostream>  
#include <string>  
using namespace std;

// x (x|y)* xz
#define X 500
#define Y 501
#define Z 502
#define FINAL '\0'
#define ERROR 10
#define OK 11

// Declaración de funciones
int obtiene_token();
int analisis_lexico();
int analisis_sintactico();

// Variables globales
char cadena[20];      // Para errores
int puntcad = 0;      // variable que recorre las cadenas
string palabra;        // Cadena fuente para analizar

int main(void) {
    int ok1, ok2;//ok1 lexico, ok2 sintactico

        // Cadena a analizar
        cout<<"introduzca su cadena: ";
        getline(cin, palabra);
    
        cout<<"Análisis léxico:\n";
        ok1 = analisis_lexico();
        if (ok1 == OK) {
            cout<<"\nAnálisis sintáctico:\n¡Ejecutando!\n";
            
            ok2 = analisis_sintactico();
            
            if (ok2 == OK)
                cout<<"\nSentido Semántico:\n¡CADENA ACEPTADA!\n";
            else
                cout<<"\nSentido Semántico:\n¡CADENA NO ACEPTADA!\n";
        } else {
            cout<<"\nExisten errores en símbolos terminales\n¡CADENA NO ACEPTADA!\n";
        }

    return 0;
}

// Analizador léxico
int analisis_lexico() {
    puntcad = 0;
    int token;
    while (1) {
        token = obtiene_token();
        switch (token) {
            case X:
                cout<<"Símbolo: x\n";
                break;
            case Y:
                cout<<"Símbolo: y\n";
                break;
            case Z:
                cout<<"Símbolo: z\n";
                break;
            case FINAL:
                return OK;
            case ERROR:
                cout<<"Error en terminal: %s\n" << cadena;
                return ERROR;
        }
    }
}

// Devuelve el siguiente token
int obtiene_token() {
    char t;//(x|y)*
    while (1) {
        t = palabra[puntcad++];
        switch (t) {
            case 'x': return X;
            case 'y': return Y;
            case 'z': return Z;
            case ' ':  break;         // Ignora espacios
            case '\0': return FINAL;
            default:
                cadena[0] = t;
                cadena[1] = '\0';
                return ERROR;
        }
    }
}

// Analizador sintáctico por autómata de estados
int analisis_sintactico() {
    int estado = 0;
    puntcad = 0;

    while (1) {
        int token = obtiene_token();
        printf("Estado de Análisis: %d\n", estado);
        switch (estado) {
            case 0:
                if (token == FINAL) return ERROR;//estado de terminacion (pregunta al nodo si es final o no)
                if (token == X) { estado = 1; break; }
                return ERROR;

            case 1:
                if (token == FINAL) return ERROR;//estado de terminacion
                if (token == X) { estado = 2; break; }
                if (token == Y) { estado = 1; break; }
                return ERROR;

            case 2:
                if (token == FINAL) return ERROR;//estado de terminacion
                if (token == Y) { estado = 1; break; }
                if (token == X) { estado = 2; break; }
                if (token == Z) { estado = 3; break; }
                return ERROR;

            case 3:
                if (token == FINAL) return OK;  // Aceptación
                return ERROR;
        }
    }
}