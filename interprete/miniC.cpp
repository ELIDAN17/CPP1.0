#include <iostream>
#include <string.h>
#include <list>
#include <queue>
#include <stack>
#include <sstream>

#define ALLAVE 0
#define CLLAVE 1
#define IGUAL 2
#define MAS 3
#define MENOS 4
#define POR 5
#define PCOMA 6
#define CIN 7
#define COUT 8
#define VAR 9
#define NUM 10
#define ENTRE 11
#define COMA 12

#define FIN 666
#define ERROR 999

#define null "6c3e226b4d4795d518ab341b0824ec29"
#define vacio "-"
#define asignado "asignado"

using namespace std;

class PostFija
{
private:
    string infija[100];
    int n;
    queue<string> posfija;
    stack<string> signos;
    stack<string> result;

public:
    PostFija()
    {
        n = 0; // 2+1*2*3*4*5-7
    }
    void SetExpresion(string exp[100], int _n)
    {
        n = _n;
        for (int i = 0; i < n; i++)
        {
            infija[i] = exp[i];
        }
    }
    int EsOperador(string op)
    {
        if (op == "+" || op == "-" || op == "*" || op == "/")
        {
            return true;
        }
        return false;
    }
    int GetPrioridad(string op)
    {
        if (op == "+" || op == "-")
        {
            return 1;
        }
        else if (op == "*" || op == "/")
        {
            return 2;
        }
    }
    void GetPosFija()
    {
        string token;
        int cont = 0;
        while (cont < n)
        {
            token = infija[cont++];
            // cout<<token<<endl;
            if (EsOperador(token))
            {
                while (!signos.empty() && GetPrioridad(signos.top()) >= GetPrioridad(token))
                {
                    posfija.push(signos.top());
                    signos.pop();
                }
                signos.push(token);
            }
            else
            {
                posfija.push(token);
            }
        }
        while (!signos.empty())
        {
            posfija.push(signos.top());
            signos.pop();
        }
    }
    string Evaluar()
    {
        queue<string> tmp;
        tmp = posfija;
        string token;
        while (!posfija.empty())
        {
            token = posfija.front();
            posfija.pop();
            if (EsOperador(token))
            {
                string a = result.top();
                result.pop();
                string b = result.top();
                result.pop();
                // cout<<b<<token<<a<<endl;
                float r;
                if (token == "+")
                {
                    r = atof(b.c_str()) + atof(a.c_str());
                }
                if (token == "-")
                {
                    r = atof(b.c_str()) - atof(a.c_str());
                }
                if (token == "*")
                {
                    r = atof(b.c_str()) * atof(a.c_str());
                }
                if (token == "/")
                {
                    r = atof(b.c_str()) / atof(a.c_str());
                }
                stringstream ss(stringstream::in | stringstream::out);
                ss << r;
                result.push(ss.str());
            }
            else
            {
                result.push(token);
            }
        }
        return result.top();
    }

    void Ver()
    {
        while (!posfija.empty())
        {
            cout << posfija.front() << " ";
            posfija.pop();
        }
    }
};

class Atributos
{
public:
    string lexema;
    int token;
    string tipo;
    string valor;
    string estado;
    Atributos()
    {
        lexema = "";
        token = -999;
        tipo = "";
        valor = null;
        estado = "";
    }
    Atributos(string lex, int tok, string tip, string val, string est)
    {
        lexema = lex;
        token = tok;
        tipo = tip;
        valor = val;
        estado = est;
    }
    void Mostrar()
    {
        cout << "Tipo(" << tipo << ") \t";
        cout << "Lexema(" << lexema << ") \t";
        cout << "Token(" << token << ") \t";
        cout << "Valor(" << valor << ") \t";
        cout << "Estado(" << estado << ")" << endl;
    }
};

class TablaSimbolos
{
private:
    list<Atributos> tabla;

public:
    void Insertar(string lex, int tok, string tip, string val, string est)
    {
        Atributos attr(lex, tok, tip, val, est);
        tabla.push_back(attr);
    }
    bool ActualizarValor(string lex, string val)
    {
        for (auto &item : tabla)
        {
            if (item.lexema == lex)
            {
                item.valor = val;
                return true;
            }
        }
        return false;
    }
    bool ActualizarEstado(string lex, string est)
    {
        for (auto &item : tabla)
        {
            if (item.lexema == lex)
            {
                item.estado = est;
                return true;
            }
        }
        return false;
    }
    void Mostrar()
    {
        for (auto item : tabla)
        {
            item.Mostrar();
        }
    }
    bool Buscar(string lex, Atributos &attr)
    {
        for (auto item : tabla)
        {
            if (item.lexema == lex)
            {
                attr = item;
                return true;
            }
        }
        return false;
    }
    bool BuscarPClave(string lex, Atributos &attr)
    {
        for (auto item : tabla)
        {
            if (item.lexema == lex && item.tipo == "pclave")
            {
                attr = item;
                return true;
            }
        }
        return false;
    }
    list<Atributos> getTabla()
    {
        return tabla;
    }
};

class Analisis
{
private:
    int i;
    char cad[100];
    string numero;
    string variable;
    int tTransicion[8][12];
    TablaSimbolos ts;

    int estado;
    int estado_ant;

public:
    Analisis(char input[100])
    {
        // Aqu� hacer la apertura de archivo de texto plano
        strcpy(cad, input);
        i = 0;

        ts.Insertar("{", ALLAVE, "pclave", vacio, vacio);
        ts.Insertar("}", CLLAVE, "pclave", vacio, vacio);
        ts.Insertar("=", IGUAL, "pclave", vacio, vacio);
        ts.Insertar("+", MAS, "pclave", vacio, vacio);
        ts.Insertar("-", MENOS, "pclave", vacio, vacio);
        ts.Insertar("*", POR, "pclave", vacio, vacio);
        ts.Insertar("/", ENTRE, "pclave", vacio, vacio);
        ts.Insertar(";", PCOMA, "pclave", vacio, vacio);
        ts.Insertar(">", CIN, "pclave", vacio, vacio);
        ts.Insertar("<", COUT, "pclave", vacio, vacio);
        ts.Insertar(",", COMA, "pclave", vacio, vacio);

        for (int ii = 0; ii < 8; ii++)
        {
            for (int jj = 0; jj < 11; jj++)
            {
                tTransicion[ii][jj] = ERROR;
            }
        }
        tTransicion[0][ALLAVE] = 1;
        tTransicion[1][VAR] = 2;
        tTransicion[1][COUT] = 5;
        tTransicion[1][CIN] = 5;
        tTransicion[1][CLLAVE] = 7;
        tTransicion[2][IGUAL] = 3;
        tTransicion[3][VAR] = 4;
        tTransicion[3][NUM] = 4;
        tTransicion[4][MAS] = 3;
        tTransicion[4][MENOS] = 3;
        tTransicion[4][POR] = 3;
        tTransicion[4][ENTRE] = 3;
        tTransicion[4][PCOMA] = 1;
        tTransicion[4][CLLAVE] = 7;
        tTransicion[5][VAR] = 6;
        tTransicion[6][PCOMA] = 1;
        tTransicion[6][COMA] = 5;
    }

    int getToken()
    {
        // Eliminar los espacion en blanco
        while (cad[i] == ' ')
        {
            i++;
        }
        if (cad[i] == '\0')
        {
            return FIN;
        }
        // buscando en la tabla de simbolos
        for (auto item : ts.getTabla())
        {
            Atributos attr;
            string lex(1, cad[i]);
            if (ts.BuscarPClave(lex, attr))
            {
                i++;
                return attr.token;
            }
        }

        if (isdigit(cad[i]))
        {
            numero = cad[i];
            i++;
            return NUM;
        }
        else if (isalpha(cad[i]))
        {
            variable = cad[i];
            i++;
            return VAR;
        }
        else
        {
            i++;
            return ERROR;
        }
    }
    bool Lexico()
    {
        i = 0;
        int token = 0;
        while (true)
        {
            token = getToken();
            // cout<<"Lexico: "<<token<<endl;
            if (token == FIN)
            {
                // ts.Mostrar();
                return true;
            }
            else if (token == VAR)
            {
                Atributos attr;
                if (!ts.Buscar(variable, attr))
                {
                    ts.Insertar(variable, VAR, "var", null, null);
                }
            }
            else if (token == ERROR)
            {
                // Aqui deben de mostrar el error lo m�s especifico posible
                Error(100);
                return false;
            }
        }
    }
    bool Sintactico()
    {
        i = 0;
        int token = 0;
        estado = 0;
        while (true)
        {
            token = getToken();
            if (token == FIN)
            {
                if (estado == 7)
                    return true;
                Error(2000);
                return false;
            }
            // cout<<"(e"<<estado<<",t"<<token<<")"<<endl;
            estado_ant = estado;
            estado = tTransicion[estado][token];
            if (estado == ERROR)
            {
                Error(400);
                return false;
            }
        }
        return false;
    }
    //      { g=7; h=g; x=g+2; y=h+x; <g,h,x; >r,b,a; g=r+g+a; <g; }
    bool Semantico()
    {
        i = 0;
        int token = 0;
        while (true)
        {
            token = getToken();
            if (token == FIN)
            {
                return true;
            }
            if (token == COUT)
            {
                // cout<<"COUT"<<endl;
                while (token != PCOMA)
                {
                    token = getToken(); //;
                    if (token == VAR)
                    {
                        Atributos attr;
                        ts.Buscar(variable, attr);
                        if (attr.estado == null)
                        {
                            Error(1000);
                            return false;
                        }
                    }
                }
                token = getToken(); //;
            }
            else if (token == CIN)
            {
                // cout<<"CIN"<<endl;
                while (token != PCOMA)
                {
                    token = getToken(); // a
                    if (token == VAR)
                    {
                        ts.ActualizarEstado(variable, asignado);
                    }
                }
                token = getToken(); //;
                token = getToken();
                ts.ActualizarEstado(variable, asignado);
                getToken();
            }
            else if (token == VAR)
            {
                // cout<<"ASIGNACION"<<endl;
                string var_actual = variable; // h
                token = getToken();           //=
                Atributos attr;
                while (token != PCOMA)
                {
                    token = getToken(); //;
                    if (token == VAR)
                    {
                        // cout<<"=>"<<variable<<" ";
                        ts.Buscar(variable, attr);
                        // attr.Mostrar();
                        // cout<<"["<<attr.estado<<"]"<<endl;
                        if (attr.estado == null)
                        {
                            // cout<<cad[i];
                            Error(30001);
                            return false;
                        }
                    }
                }
                ts.ActualizarEstado(var_actual, asignado);
            }
            // ts.Mostrar();
            // cout<<endl;
        }
    }
    bool Ejecucion()
    {
        i = 0;
        int token = 0;
        while (true)
        {
            token = getToken();
            if (token == FIN)
            {
                return true;
            }
            if (token == COUT)
            {
                token = getToken();
                Atributos attr;
                ts.Buscar(variable, attr);
                cout << attr.valor << endl;
            }
            else if (token == CIN)
            {
                token = getToken();
                string input;
                cin >> input;
                ts.ActualizarValor(variable, input);
                token = getToken();
            }
            else if (token == VAR)
            {
                string var_actual = variable;
                string infija[100];
                int cont_infija = 0;
                while (token != PCOMA)
                {
                    token = getToken();
                    if (token == MAS)
                        infija[cont_infija++] = "+";
                    else if (token == MENOS)
                        infija[cont_infija++] = "-";
                    else if (token == POR)
                        infija[cont_infija++] = "*";
                    else if (token == ENTRE)
                        infija[cont_infija++] = "/";
                    else if (token == VAR)
                    {
                        Atributos attr;
                        ts.Buscar(variable, attr);
                        infija[cont_infija++] = attr.valor;
                    }
                    else if (token == NUM)
                    {
                        infija[cont_infija++] = numero;
                    }
                }
                /*for(int ii=0;ii<cont_infija;ii++){
                    if(infija[ii]==null){
                        Error(20001);
                        return false;
                    }
                }*/
                PostFija p;
                p.SetExpresion(infija, cont_infija);
                p.GetPosFija();
                ts.ActualizarValor(var_actual, p.Evaluar());
                // ts.Mostrar();
            }
        }
    }
    void Analizar()
    {
        ts.Mostrar();
        cout << endl;
        cout << endl;
        if (Lexico())
        {
            ts.Mostrar();
            cout << endl;
            cout << endl;
            if (Sintactico())
            {
                ts.Mostrar();
                cout << endl;
                cout << endl;
                if (Semantico())
                {
                    ts.Mostrar();
                    // cout<<endl;
                    // cout<<endl;
                    Ejecucion();
                    ts.Mostrar();
                    cout << endl;
                    cout << endl;
                }
            }
        }
    }
    void Error(int nroError)
    {
        cout << "Error " << nroError << ": ";
        if (nroError == 100)
        {
            cout << "No se reconoce el caracter " << cad[i - 1] << " [linea 1, columna " << i << "]";
            // cout<<"Detallar el error 300";
        }
        else if (nroError == 2000)
        {
            cout << "Se espera terminar el programa con } [linea 1, columna " << i << "]";
            // cout<<"Detallar el error 300";
        }
        else if (nroError == 400)
        {
            cout << "->" << estado_ant << "<-" << endl;
            if (estado_ant == 3)
            {
                cout << "Se espera escribir una variable o numero" << " [linea 1, columna " << i << "]";
            }
            if (estado_ant == 5)
            {
                cout << "Se esperaba una variable [linea 1, columna" << i << "]";
                // cout<<"Se esta intentando ingresar o mostrar el valor a una variable";
            }
            if (estado_ant == 2)
            {
                cout << "Se esta intentando asignar un valor a una variable, se espera el signo = " << " [linea 1, columna " << i << "]";
            }
            if (estado_ant == 6 || estado_ant == 4)
            {
                cout << "Se espera ; " << " [linea 1, columna " << i << "]";
            }
            // cout<<estado_ant;
            // cout<<"Detallar el error 300";
        }
        else if (nroError == 300)
        {
            // cout<<"Detallar el error 300";
            cout << "Detallar el error 300";
        }
        else if (nroError == 30001)
        {
            // cout<<"La variable "<<cad[i-1]<<" no tiene un valor inicial [linea 1, columna "<<i<<"] ";
            cout << "la variable " << cad[i - 1] << " no tiene un valor asignado [linea 1, columna " << i << "]";
        }
    }
};

int main()
{
    // Analisis*obj=new Analisis("{ x=7 y=2; >z; x=x+y; z=z-9; y=x*z; <x; <y; <z; }");
    // Analisis*obj=new Analisis("{ >a; >b; >c; s=a+b+c+1; <s; }");
    // Analisis*obj=new Analisis("{ a=7; b=2; c=a+b; <c; }");
    // Analisis*obj=new Analisis("{ >k; >z; >e; k=k*k+z*z+e; <k; }");
    // Analisis*obj=new Analisis("{ g=7; h=g; x=g+2; y=h+x; <g,h,x; >r; g=r+g; <g; }");
    Analisis *obj = new Analisis("{ n=5; >n; s=n*n+n; s=s/2; <s; }");
    // Analisis*obj=new Analisis("{ n=5; >n; s=(n*n+n)/2; s=s/2; <s; }");
    obj->Analizar();
    system("pause");
    return true;
}