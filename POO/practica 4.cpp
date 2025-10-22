#include <iostream>
#include <stdio.h> // para gets() y puts()
using namespace std;
#include <string.h>  // para strcpy() y strncpy()
const int MAX = 255; // #define MAX 255

// prototipos
int longcad(char *s);
int comparacad(char *s1, char *s2);
void copiacad(char *dest, char *orig);
int main()
{
    char cadena[MAX];
    cadena[0] = '\0';
    cout << "\n<1> longcad(cadena) = " << longcad(cadena) << endl;
    copiacad(cadena, "Algoritmos y Programacion");
    cout << "<2> cadena: " << cadena << endl;
    cout << "<3> longcad(cadena) = " << longcad(cadena) << endl;
    cout << "<4> comparacad(cadena, Algoritmos y Programacion) = ";
    cout << comparacad(cadena, "Algoritmos y Programacion") << endl;
    cout << "<5> comparacad(cadena, Aloritmos) = ";
    cout << comparacad(cadena, "Aloritmos") << endl;
    return 0;
}
int longcad(char *s)
{
    int i = 0;
    while (s[i] != '\0')
        ++i;
    return i;
}
int comparacad(char *s1, char *s2)
{
    int i = 0;
    for (; s1[i] != '\0' && s1[i] == s2[i]; i++)
        ;
    return (int)(s1[i] - s2[i]);
}
void copiacad(char *dest, char *orig)
{
    int i = 0;
    for (; orig[i] != '\0'; i++)
        dest[i] = orig[i];
    dest[i] = '\0';
}

/* //ejemplo 14
// prototipos
int longcad(char s[MAX]);                      // emula strlen()
int comparacad(char s1[MAX], char s2[MAX]);    // emula strcmp()
void copiacad(char dest[MAX], char orig[MAX]); // emula strcpy()
int main()
{
    char cadena[MAX];
    cadena[0] = '\0';
    cout << "\n<1> longcad(cadena) = " << longcad(cadena) << endl;
    copiacad(cadena, "Algoritmos y Programacion");
    cout << "<2> cadena: " << cadena << endl;
    cout << "<3> longcad(cadena) = " << longcad(cadena) << endl;
    cout << "<4> comparacad(cadena, Algoritmos y Programacion) = ";
    cout << comparacad(cadena, "Algoritmos y Programacion") << endl;
    cout << "<5> comparacad(cadena, Programacion) = ";
    cout << comparacad(cadena, "Programacion") << endl;
    return 0;
}
int longcad(char s[MAX])
{
    int i = 0;
    while (s[i] != '\0')
        ++i;
    return i;
}
int comparacad(char s1[MAX], char s2[MAX])
{
    int i = 0;
    for (; s1[i] != '\0' && s1[i] == s2[i]; i++)
        ;
    return (int)(s1[i] - s2[i]);
}
void copiacad(char dest[MAX], char orig[MAX])
{
    int i = 0;
    for (; orig[i] != '\0'; i++)
        dest[i] = orig[i];
    dest[i] = '\0';
}*/

/* //ejemplo 13
int main()
{
    char cade1[] = "Eres muy valiosa para mi!";
    int longitud;
    longitud = strlen(cade1);
    cout << "\nLa cadena:\n"
         << cade1 << "\n\nTiene: " << longitud << " caracteres\n";
    return 0;
}*/

/* // ejemplo 12
int main()
{
    char string[50];
    char *ptr, c = 'u';
    strcpy(string, "Esto es una cadena");
    // strchr() busca la ocurrencia de un carácter
    ptr = strchr(string, c);
    cout << "\nUso de la función strchr():\n";
    cout << "\nCadena a explorar => " << string << endl;
    if (ptr)
        cout << "\nEl carácter " << c << " está en el índice: " << (ptr - string) << endl;
    else
        cout << "\nEl carácter " << c << " no se encuentra\n";
    return 0;
}*/

/* //ejemplo 11
int main()
{
    char cade1[40], cade2[40];
    cout << "\nIngrese cadena en minúsculas: ";
    gets(cade1);
    strupr(cade1);
    cout << "\nA mayúsculas: ";
    puts(cade1);
    cout << endl;
    cout << "\nIngrese cadena en mayúsculas: ";
    gets(cade2);
    strlwr(cade2);
    cout << "\nA minúsculas: ";
    puts(cade2);
    cout << endl;
    return 0;
}*/

/* ejemplo 10
int main()
{
    char s[] = "Rosita Linda";
    cout << "Cadena impresa con espacios en blanco entre caracteres:\n\n";
    // Uso de sizeof para determinar el número de caracteres
    for (int i = 0; i < sizeof(s) / sizeof(char); i++)
        cout << s[i] << " ";
    return 0;
}*/

/* ejemplo 9
int main()
{
    char cade1[] = "lenguaje C++";
    char cade2[] = "LENGUAJE C++";
    char cade3[] = "lenguaje C++";
    char cade4[] = "LENGuaje c++";
    int result;
    cout << "\nFunción strcmp():\n\n";
    cout << "Cadena 1: " << cade1 << endl;
    cout << "Cadena 2: " << cade2 << endl;
    cout << "Cadena 3: " << cade3 << endl;
    cout << "Cadena 4: " << cade4 << endl
         << endl;
    result = strcmp(cade1, cade2);
    if (result < 0)
        cout << cade1 << " es menor que: " << cade2 << " => resultado = ";
    if (result == 0)
        cout << cade1 << " es igual que: " << cade2 << " => resultado = ";
    if (result > 0)
        cout << cade1 << " es mayor que: " << cade2 << " => resultado = ";
    cout << result << endl
         << endl;
    result = strcmp(cade1, cade3);
    if (result < 0)
        cout << cade1 << " es menor que: " << cade3 << " => resultado = ";
    if (result == 0)
        cout << cade1 << " es igual que: " << cade3 << " => resultado = ";
    if (result > 0)
        cout << cade1 << " es mayor que: " << cade3 << " => resultado = ";
    cout << result << endl
         << endl;
    result = strcmp(cade4, cade1);
    if (result < 0)
        cout << cade4 << " es menor que: " << cade1 << " => resultado = ";
    if (result == 0)
        cout << cade4 << " es igual que: " << cade1 << " => resultado = ";
    if (result > 0)
        cout << cade4 << " es mayor que: " << cade1 << " => resultado = ";
    cout << result << endl
         << endl;
    return 0;
}*/

/* // ejemplo 8
int main()
{
    char linea[MAX], c, sig, blanco;
    int i = 0, numpal;
    cout << "\nIngrese línea de texto> ";
    while ((c = cin.get()) != '\n')
    {
        linea[i++] = c;
    }
    linea[i++] = '\0'; // marca de fin de cadena
    numpal = 0;
    blanco = ' ';
    i = 0;
    c = linea[i];
    while (c)
    {
        if (c != blanco)
        {
            sig = linea[i + 1];
            if (sig == blanco || sig == '\0')
                ++numpal;
        }
        c = linea[++i];
    }
    cout << "\nTexto -> " << linea << "\nLa línea de texto tiene ";
    cout << numpal << " palabras" << endl;
    return 0;
}*/

/* // ejemplo 7
int main()
{
    char s1[100] = "Con todo lo bueno que";
    char s2[] = " significa heredar una biblioteca, ";
    char s3[] = " mejor aun es reunirla - Agustine Birrel";
    cout << "\nFunciones strcat() y strncat():\n";
    // strcat() concatena una cadena a otra
    strcat(s1, s2);
    cout << "\nConcatenar s2 en s1:\n"
         << s1 << endl;
    strcat(s1, s3);
    cout << "\nConcatenar s3 en s1:\n"
         << s1 << endl;
    // strncat() concatena los primeros n caracteres de una cadena a otra
    cout << "\nParte de s3 concatenada en s2:\n";
    strncat(s2, s3, 10);
    cout << s2 << endl;
    return 0;
}*/

/* // ejemplo 6
int main()
{
    char x[] = "Universidad Nacional Mayor de San Marcos";
    char y[40], z[40];
    cout << "\nFunciones strcpy() y strncpy():\n";
    cout << "\nEl string en el array x es -> " << x << endl;
    // strcpy() copia una cadena a otra
    cout << "\nEl string en el array x copiado al array y es ->\n";
    cout << strcpy(y, x) << endl;
    // strncpy() copia los n primeros caracteres de una cadena a otra
    strncpy(z, x, 15);
    z[15] = '\0'; // marca de fin de cadena
    cout << "\nParte del string en el array x copiado al array z es ->\n";
    cout << z << endl;
    return 0;
}*/

/* // Ejemplo  5
int main()
{
    char cadena[] = "ALGORITMOS";
    cout << "\nCadena inicial: " << cadena << endl;
    cout << "\nCadena con un espacio entre caracteres: ";
    for (int i = 0; cadena[i] != '\0'; i++)
        cout << cadena[i] << ' ';
    cout << endl;
    return 0;
}*/

/* // Ejemplo 4
int main()
{
    char cad[40];
    cout << "\nIngrese sus nombres y apellidos: ";
    gets(cad); // Lee la cadena
    cout << "\nHola, ";
    puts(cad); // Imprime la cadena
    cout << endl;
    return 0;
}*/

/* // ejemplo 3
int main()
{
    char c;
    cout << "\nIngrese un carácter: ";
    cin.get(c); // Lee un carácter
    cout << "\nEl carácter leído es: " << c << endl;
    return 0;
}*/

/* // Ejemplo 2
int main()
{
    char cadena[80];
    cout << "\nIngrese una cadena:\n";
    cin.getline(cadena, 80); // Lee hasta 80 caracteres
    cout << "\nLa cadena leída es:\n"
         << cadena << endl;
    return 0;
}*/

/* // Ejemplo 1
int main()
{
    char nombre[40];
    cout << "Ingrese su nombre completo: ";
    cin >> nombre; // Lee hasta el primer espacio en blanco
    cout << "Hola, " << nombre << endl;
    return 0;
}*/
