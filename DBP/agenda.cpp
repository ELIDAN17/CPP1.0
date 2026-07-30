#include <iostream>
#include <string>
#include <vector>
using namespace std;
/*
class agenda{
    string nombre, telefono, correo;
    public:
    //agenda(string& n, string& t, string& c): nombre(n), telefono(t), correo (c){}
    //string getNombre() { return nombre;}
    //string getTelefono() { return telefono;}
    //string getCorreo() {return correo;}
    //friend void agregarContacto(agenda& agenda);
    void mostrarContactos() {
        for(int i=0;i<11;i++){
            cout << "Nombre: "<< nombre<<endl;
            cout << "Teléfono: " << telefono<<endl;
            cout << "Correo: " << correo << endl;
        }
    }
    void agregarContacto(){
        cout<<"ingrese nombre: ";
        getline(cin,nombre);
        cout<<"ingrese el telefono: ";
        getline(cin,telefono);
        cout<<"ingrese correo: ";
        getline(cin,correo);
    }
};
int main(){
    void agregarContacto();
    void mostrarContactos();
    return 0;
}
*/

/*
class Contacto {
private:
    string nombre;
    string telefono;
    string correo;

public:
    // Constructor
    Contacto(const string& n, const string& t, const string& c)
        : nombre(n), telefono(t), correo(c) {}

    // Getter para el nombre
    string getNombre() const { return nombre; }

    // Getter para el teléfono
    string getTelefono() const { return telefono; }

    // Getter para el correo electrónico
    string getCorreo() const { return correo; }

    // Función amiga para modificar el nombre
    friend void Agenda::agregarContacto(Contacto& contacto);
};
class Agenda {
private:
    string vector<Contacto> contactos;

public:
    // Función amiga para agregar contactos
    friend void agregarContacto(Agenda& agenda, Contacto& contacto);

    // Método para mostrar todos los contactos
    void mostrarContactos() const {
        for (const auto& contacto : contactos) {
            cout << "Nombre: " << contacto.getNombre()
                      << ", Teléfono: " << contacto.getTelefono()
                      << ", Correo: " << contacto.getCorreo() << std::endl;
        }
    }
};

void agregarContacto(Agenda& agenda, Contacto& contacto) {
    agenda.contactos.push_back(contacto);
}
int main() {
    Agenda agenda;

    // Creando contactos
    Contacto contacto1("Juan Pérez", "555-1234", "juan.perez@example.com");
    Contacto contacto2("Maria García", "555-5678", "maria.garcia@example.com");

    // Agregando contactos a la agenda
    agregarContacto(agenda, contacto1);
    agregarContacto(agenda, contacto2);

    // Mostrando contactos de la agenda
    agenda.mostrarContactos();

    return 0;
}
*/

class Contacto {
private:
    string nombre;
    string telefono;
    string correo;

public:
    // Constructor
    Contacto(const string& n, const string& t, const string& c)
        : nombre(n), telefono(t), correo(c) {}

    // Función amiga para acceder a los miembros privados de Contacto
    friend class Agenda;
};
class Agenda {
private:
    struct Nodo {
        Contacto dato;
        Nodo* siguiente;

        Nodo(Contacto dato) : dato(dato), siguiente(nullptr) {}
    };

    Nodo* cabeza;

public:
    // Constructor
    Agenda() : cabeza(nullptr) {}

    // Destructor
    ~Agenda() {
        while (cabeza!= nullptr) {
            Nodo* temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }

    // Método para agregar un nuevo contacto
    void agregarContacto(const string& nombre, const string& telefono, const string& correo) {
        Nodo* nuevoNodo = new Nodo(Contacto(nombre, telefono, correo));
        nuevoNodo->siguiente = cabeza;
        cabeza = nuevoNodo;
    }

    // Método para buscar un contacto por nombre
    bool buscarContacto(const string& nombre) const {
        Nodo* actual = cabeza;
        while (actual!= nullptr) {
            if (actual->dato.nombre == nombre) {
                cout << "Contacto encontrado: " << actual->dato.nombre << std::endl;
                return true;
            }
            actual = actual->siguiente;
        }
        cout << "Contacto no encontrado." << endl;
        return false;
    }

    // Método para eliminar un contacto por nombre
    void eliminarContacto(const string& nombre) {
        Nodo* anterior = nullptr;
        Nodo* actual = cabeza;
        while (actual!= nullptr && actual->dato.nombre!= nombre) {
            anterior = actual;
            actual = actual->siguiente;
        }
        if (actual!= nullptr) {
            if (anterior == nullptr) {
                cabeza = cabeza->siguiente;
            } else {
                anterior->siguiente = actual->siguiente;
            }
            delete actual;
        } else {
            cout << "Contacto no encontrado para eliminar." << endl;
        }
    }
};
int main() {
    Agenda agenda;

    // Agregar contactos
    agenda.agregarContacto("Juan Pérez", "555-1234", "juan.perez@example.com");
    agenda.agregarContacto("Ana García", "555-5678", "ana.garcia@example.com");

    // Buscar un contacto
    agenda.buscarContacto("Juan Pérez"); // Debería encontrar y mostrar el contacto Juan Pérez

    // Eliminar un contacto
    //agenda.eliminarContacto("Ana García"); // Debería eliminar el contacto Ana García

    return 0;
}
