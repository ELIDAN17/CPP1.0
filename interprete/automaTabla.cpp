
#include <iostream>
#include <stdio.h>
#include <string.h>   // Para strcpy
#include <ctype.h>    // Para funciones de caracteres si las usas después

//#define A 500
//#define B 501
#define FINAL 10
#define ERROR 1000
#define E 1001
#define OK 1002

// Declaración de funciones
int obtiene_token();
int analisis_lexico();     // qué palabras están presentes.
int analisis_sintactico(); // están bien ordenadas según las reglas.
int tabla[5][11]={
    {3,1,2,4,1,2,4,1,2,4,E},
    {1,2,4,1,2,4,1,2,4,1,E},
    {2,4,1,2,4,1,2,4,1,2,E},
    {E,E,E,E,E,E,E,E,E,E,OK},
    {4,1,2,4,1,2,4,1,2,4,OK}
};

// Variables globales
char cadena[20];      // Para errores
int puntcad = 0;      // Puntero para recorrer la cadena
char arch[50];        // Cadena fuente para analizar

int main(void) {
    int ok1, ok2;

    // Cadena a analizar:
    strcpy(arch, "156");//copiamos en el array arch[]

    printf("Análisis léxico:\n");

    ok1 = analisis_lexico();//confirma si los simbolos estan de nuestro alfbaeto

    if (ok1 == OK) {//si es asi =>

        printf("\nAnálisis sintáctico:\n¡Ejecutando!\n");

        ok2 = analisis_sintactico();//analiza la secuencia e indica si el orden y la combinacion es valida para la gramatica del lenguaje

        if (ok2 == OK)//si es asi =>

            printf("\nSentido Semántico:\n¡CADENA ACEPTADA!\n");
        else
            printf("\nSentido Semántico:\n¡CADENA NO ACEPTADA!\n");
    } else {
        printf("\nExisten errores en símbolos terminales\n¡CADENA NO ACEPTADA!\n");
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
            case 0:
                printf("Símbolo: 0\n");
                break;
            case 1:
                printf("Símbolo: 1\n");
                break;
            case 2:
                printf("Símbolo: 2\n");
                break;
            case 3:
                printf("Símbolo: 3\n");
                break;
            case 4:
                printf("Símbolo: 4\n");
                break;
            case 5:
                printf("Símbolo: 5\n");
                break;
            case 6:
                printf("Símbolo: 6\n");
                break;
            case 7:
                printf("Símbolo: 7\n");
                break;
            case 8:
                printf("Símbolo: 8\n");
                break;
            case 9:
                printf("Símbolo: 9\n");
                break;
            case FINAL:
                return OK;
            case ERROR:
                printf("Error en terminal: %s\n", cadena);
                return ERROR;
        }
    }
}

// Devuelve el siguiente token/simbolos que estan en la cadena
int obtiene_token() {
    char t;
    while (1) {
        t = arch[puntcad++];
        switch (t) {
            case '0': return 0;
            case '1': return 1;
            case '2': return 2;
            case '3': return 3;
            case '4': return 4;
            case '5': return 5;
            case '6': return 6;
            case '7': return 7;
            case '8': return 8;
            case '9': return 9;
            case ' ':  break;         // Ignora espacios
            case '\0': return FINAL;//cuando encontremos el marcador
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
        if(tabla[estado][token]==E) return ERROR;
        if(tabla[estado][token]==OK) return OK;
        
        estado = tabla[estado][token];
    }
}
/*
#include <iostream>
#include <stdio.h>
#include <string.h>   // Para strcpy
#include <ctype.h>    // Para funciones de caracteres si las usas después

#define A 0
#define B 1
#define FINAL 2
#define X 1000
#define Y 1001
#define ERROR 1004
#define E 1002
#define OK 1003

// Declaración de funciones
int obtiene_token();
int analisis_lexico();     // qué palabras están presentes.
int analisis_sintactico(); // están bien ordenadas según las reglas.
int tabla[5][3]={
    {E,1,E},
    {2,E,E},
    {2,3,E},
    {2,3,OK}
};

// Variables globales
char cadena[20];      // Para errores
int puntcad = 0;      // Puntero para recorrer la cadena
char arch[50];        // Cadena fuente para analizar

int main(void) {
    int ok1, ok2;

    // Cadena a analizar:
    strcpy(arch, "baabb");//copiamos en el array arch[]

    printf("Análisis léxico:\n");

    ok1 = analisis_lexico();//confirma si los simbolos estan de nuestro alfbaeto

    if (ok1 == OK) {//si es asi =>

        printf("\nAnálisis sintáctico:\n¡Ejecutando!\n");

        ok2 = analisis_sintactico();//analiza la secuencia e indica si el orden y la combinacion es valida para la gramatica del lenguaje

        if (ok2 == OK)//si es asi =>

            printf("\nSentido Semántico:\n¡CADENA ACEPTADA!\n");
        else
            printf("\nSentido Semántico:\n¡CADENA NO ACEPTADA!\n");
    } else {
        printf("\nExisten errores en símbolos terminales\n¡CADENA NO ACEPTADA!\n");
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
            case 0:
                printf("Símbolo: A\n");
                break;
            case 1:
                printf("Símbolo: B\n");
                break;
            case FINAL:
                return OK;
            case ERROR:
                printf("Error en terminal: %s\n", cadena);
                return ERROR;
        }
    }
}

// Devuelve el siguiente token/simbolos que estan en la cadena
int obtiene_token() {
    char t;
    while (1) {
        t = arch[puntcad++];
        switch (t) {
            case 'a': return A;
            case 'b': return B;
            case ' ':  break;         // Ignora espacios
            case '\0': return FINAL;//cuando encontremos el marcador
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
        if(tabla[estado][token]==E) return ERROR;
        if(tabla[estado][token]==OK) return OK;
        
        estado = tabla[estado][token];
    }
}*/

/*
#include <iostream>
#include <stdio.h>
#include <string.h>  
#include <ctype.h>    

#define FINAL 10
#define ERROR 1000
#define E 1001
#define OK 1002

// Declaración de funciones
int obtiene_token();
int analisis_lexico();     // qué palabras están presentes.
int analisis_sintactico(); // están bien ordenadas según las reglas.
int tabla[5][11]={
    {E,1,2,1,2,1,2,1,2,1,E},
    {2,1,2,1,2,1,2,1,2,1,E},
    {2,1,2,1,2,1,2,1,2,1,OK}
};

// Variables globales
char cadena[20];      // Para errores
int puntcad = 0;      // Puntero para recorrer la cadena
char arch[50];        // Cadena fuente para analizar

int main(void) {
    int ok1, ok2;

    // Cadena a analizar:
    strcpy(arch, "22222");//copiamos en el array arch[]

    printf("Análisis léxico:\n");

    ok1 = analisis_lexico();//confirma si los simbolos estan de nuestro alfbaeto

    if (ok1 == OK) {//si es asi =>

        printf("\nAnálisis sintáctico:\n¡Ejecutando!\n");

        ok2 = analisis_sintactico();//analiza la secuencia e indica si el orden y la combinacion es valida para la gramatica del lenguaje

        if (ok2 == OK)//si es asi =>

            printf("\nSentido Semántico:\n¡CADENA ACEPTADA!\n");
        else
            printf("\nSentido Semántico:\n¡CADENA NO ACEPTADA!\n");
    } else {
        printf("\nExisten errores en símbolos terminales\n¡CADENA NO ACEPTADA!\n");
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
            case 0:
                printf("Símbolo: 0\n");
                break;
            case 1:
                printf("Símbolo: 1\n");
                break;
            case 2:
                printf("Símbolo: 2\n");
                break;
            case 3:
                printf("Símbolo: 3\n");
                break;
            case 4:
                printf("Símbolo: 4\n");
                break;
            case 5:
                printf("Símbolo: 5\n");
                break;
            case 6:
                printf("Símbolo: 6\n");
                break;
            case 7:
                printf("Símbolo: 7\n");
                break;
            case 8:
                printf("Símbolo: 8\n");
                break;
            case 9:
                printf("Símbolo: 9\n");
                break;
            case FINAL:
                return OK;
            case ERROR:
                printf("Error en terminal: %s\n", cadena);
                return ERROR;
        }
    }
}

// Devuelve el siguiente token/simbolos que estan en la cadena
int obtiene_token() {
    char t;
    while (1) {
        t = arch[puntcad++];
        switch (t) {
            case '0': return 0;
            case '1': return 1;
            case '2': return 2;
            case '3': return 3;
            case '4': return 4;
            case '5': return 5;
            case '6': return 6;
            case '7': return 7;
            case '8': return 8;
            case '9': return 9;
            case ' ':  break;         // Ignora espacios
            case '\0': return FINAL;//cuando encontremos el marcador
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
        if(tabla[estado][token]==E) return ERROR;
        if(tabla[estado][token]==OK) return OK;
        
        estado = tabla[estado][token];
    }
}
*/
