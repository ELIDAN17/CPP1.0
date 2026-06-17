#include <iostream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

// Se agregó MULT y DIV para los nuevos componentes léxicos
enum TokenType
{
    ID,
    NUMBER,
    PLUS,
    MINUS,
    MULT,
    DIV,
    END,
    ERROR
};

struct Token
{
    TokenType type;
    string lexeme;
};

class Lexer
{
private:
    string source;
    size_t cursor;

public:
    Lexer(string src) : source(src), cursor(0) {}

    Token nextToken()
    {
        // Salta espacios en blanco y tabulaciones
        while (cursor < source.length() && isspace(source[cursor]))
        {
            cursor++;
        }

        if (cursor >= source.length())
            return {END, ""};

        char current = source[cursor];

        // Reconocimiento de Números: [0-9]+
        if (isdigit(current))
        {
            string value;
            while (cursor < source.length() && isdigit(source[cursor]))
            {
                value += source[cursor++];
            }
            return {NUMBER, value};
        }

        // Reconocimiento de Identificadores: [a-zA-Z][a-zA-Z0-9]*
        if (isalpha(current))
        {
            string id;
            while (cursor < source.length() && isalnum(source[cursor]))
            {
                id += source[cursor++];
            }
            return {ID, id};
        }

        // Reconocimiento de Operadores
        if (current == '+')
        {
            cursor++;
            return {PLUS, "+"};
        }
        if (current == '-')
        {
            cursor++;
            return {MINUS, "-"};
        }

        // NUEVO COMPONENTE: Multiplicación
        if (current == '*')
        {
            cursor++;
            return {MULT, "*"};
        }
        // NUEVO COMPONENTE: División
        if (current == '/')
        {
            cursor++;
            return {DIV, "/"};
        }

        // Manejo de errores para caracteres no definidos
        cursor++;
        return {ERROR, string(1, current)};
    }
};

int main()
{
    // Se cambió la combinación de lexemas para probar el nuevo operador
    // string input = "resultado + 42 - total";
    string input = "area = base * 10 - ajuste";
    // string input = "x = (base * altura) / 2 + offset - 5";
    // string input = "total=cuenta*1.15/impuesto+10";
    // string input = "precio_final @ 100 / $descuento";
    Lexer lexer(input);
    Token t;

    cout << "Analizando: " << input << endl;
    cout << "---------------------------" << endl;

    do
    {
        t = lexer.nextToken();
        string typeName;

        switch (t.type)
        {
        case ID:
            typeName = "IDENTIFICADOR";
            break;
        case NUMBER:
            typeName = "NUMERO";
            break;
        case PLUS:
            typeName = "OPERADOR SUMA";
            break;
        case MINUS:
            typeName = "OPERADOR RESTA";
            break;
        case MULT:
            typeName = "OPERADOR MULT";
            break; // Nuevo caso
        case DIV:
            typeName = "OPERADOR DIV";
            break; // Nuevo caso
        case ERROR:
            typeName = "ERROR";
            break;
        case END:
            typeName = "FIN";
            break;
        }

        if (t.type != END)
        {
            cout << "Token: " << typeName << " | Valor: '" << t.lexeme << "'" << endl;
        }
    } while (t.type != END);

    return 0;
}