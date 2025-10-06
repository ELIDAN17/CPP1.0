#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include <cstring>
#include <conio.h>
//#include <string.h>
//#include <time.h>
#include <fstream>
#include <vector>
//using std::stoi;
//using std::stof;
/*
class ArchivoTXT {
private:
    string nombreArchivo;
public:
    // Constructor
    ArchivoTXT(const string& nombre) : nombreArchivo(nombre) {}


    // Método para abrir el archivo
    void abrir() {
        ofstream archivo(nombreArchivo);
        if (!archivo.is_open()) {
            cout << "Error al abrir el archivo." << endl;
        }
    }

    // Método para cerrar el archivo
    void cerrar() {
        ofstream archivo(nombreArchivo, ios::app); // Usamos ios::app para agregar texto si es necesario
        if (archivo.is_open()) {
            archivo.close();
        }
    }

    // Método para escribir en el archivo
    void escribir(const string& texto) {
        ofstream archivo(nombreArchivo, ios::app); // Usamos ios::app para agregar texto sin sobrescribir
        if (archivo.is_open()) {
            archivo << texto << endl; // Agregamos un salto de línea al final
        } else {
            cout << "Error al escribir en el archivo." << endl;
        }
    }

    // Método para leer el contenido del archivo
    void leer() {
        ifstream archivo(nombreArchivo);
        string linea;
        if (archivo.is_open()) {
            while (getline(archivo, linea)) {
                cout << linea << endl;
            }
            archivo.close();
        } else {
            cout << "Error al leer el archivo." << std::endl;
        }
    }
};
int main() {
    ArchivoTXT miArchivo("Usuarios.txt");
    miArchivo.abrir();
    miArchivo.escribir("xd");
    miArchivo.leer();
    miArchivo.cerrar();
    cout << "\033[2J\033[1;1H";
    return 0;
    
}
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;
// funcion para limpiar la consola
void limpiar() { cout << "\033[2J\033[1;1H"; }
// clase de producto
class producto {
  // atributos de producto
  string nombre;
  float precio;
  int unidades;
  // metodos de producto(solo declaracion)
public:
  producto(string a, float b, int c);
  string elnombre();
  float elprecio();
  int lasunidades();
  void mostrar1();
  void mostrar2();
  void agregar_unidade(int a);
};
// metodos de producto(definicion)
void producto::agregar_unidade(int a) { unidades += a; }
void producto::mostrar1() {
  cout << nombre;
  for (int i = 0; i < 10 - nombre.size(); i++) {
    cout << ' ';
  }
  cout << unidades << endl;
}
void producto::mostrar2() {
  cout << nombre;
  for (int i = 0; i < 10 - nombre.size(); i++) {
    cout << ' ';
  }

  cout << "s/ " << precio << endl;
}
producto::producto(string a, float b, int c) {
  nombre = a;
  precio = b;
  unidades = c;
}
string producto::elnombre() { return nombre; }
float producto::elprecio() { return precio; }
int producto::lasunidades() { return unidades; }
// clase de usuario
class usuario {
  //
  string nombre;
  string contra;
  float saldo = 100;
  vector<producto> carrito;
  vector<producto> compras;

public:
  usuario();
  usuario(string a, string b);
  void mostrar();

  string elnombre();
  string lacontra();
  float elsaldo();

  void agregar_saldo(int s);
  float total_compras();
  void mostrar_compras();
  void mostrar_carrito();
  void comprar(producto r);
  void agregar_a_carrito(producto r);
  void sacar_del_carrito(int r);
  void comprar_carrito();
};
// metodos de usuario
void usuario::comprar_carrito() {
  for (producto u : carrito) {
    comprar(u);
  }
  carrito.clear();
}
void usuario::sacar_del_carrito(int r) {
  carrito.erase(carrito.begin() + r - 1);
}
void usuario::comprar(producto r) { compras.push_back(r); }
void usuario::agregar_a_carrito(producto r) { carrito.push_back(r); }
void usuario::mostrar_compras() {
  int a = 1;
  cout << "   nombre    precio" << endl;
  for (producto y : compras) {
    cout << a << ". ";
    y.mostrar2();
    a++;
  }
}
void usuario::mostrar_carrito() {
  int a = 1;
  cout << "   nombre    precio" << endl;
  for (producto y : carrito) {
    cout << a << ". ";
    y.mostrar2();
    a++;
  }
}
float usuario::total_compras() {
  int t = 0;
  if (compras.size() == 0) {
    return 0;
  } else {
    for (producto y : compras) {
      t += y.elprecio();
    }
    return t;
  }
}
void usuario::agregar_saldo(int s) { saldo += s; }
void usuario::mostrar() {
  cout << nombre;
  int espacios = 10 - nombre.size();
  for (int i = 0; i < espacios; i++) {
    cout << " ";
  }

  cout << saldo << endl;
}
usuario::usuario(string a, string b) {
  nombre = a;
  contra = b;
};
string usuario::elnombre() { return nombre; }
string usuario::lacontra() { return contra; }
// clase de menu
class menu {
  int memoria;
  vector<usuario> usuarios;
  vector<producto> almasen;

public:
  void menu_prinsipal();

  void panel_administrador();
  void panel_usuario();

  void admin_usuarios();
  void admin_almasen();

  void opcion_usuarios(int x);

  void agregar_producto();
  void eliminar_producto();
  void agregar_producto_nuevo();
  void agregar_unidades();

  void crear_cuenta();
  void iniciar_secion();
  void menu_usuario();

  void cerrar_secion();
  void ver_productos();
  void ver_carrito();
  void ver_compras();
  void menu_productos(int a);
  void eliminar_del_carrito();
  void comprar_carrito();
};
// metodos de menu
void menu::menu_prinsipal() {
  cout << "1. ADMINISTRADOR" << endl;
  cout << "2. USUARIO" << endl;
  cout << "3. SALIR" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 1:
    limpiar();
    panel_administrador();
    break;
  case 2:
    limpiar();
    panel_usuario();
    break;
  case 3:
    limpiar();
    cout << "GRACIAS POR SU VISITA" << endl;
    break;
  default:
    limpiar();
    cout << "Entrada Incorrecta\n" << endl;
    menu_prinsipal();
    break;
  }
}
//
void menu::panel_administrador() {
  cout << "0. Regresar" << endl;
  cout << "1. Administrar Usuarios" << endl;
  cout << "2. Administrar Almasen" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    menu_prinsipal();
    break;
  case 1:
    limpiar();
    admin_usuarios();
    break;
  case 2:
    limpiar();
    admin_almasen();
    break;
  default:
    limpiar();
    panel_administrador();
    cout << "entrada incorrecta\n" << endl;
    break;
  }
}

void menu::admin_usuarios() {
  switch (usuarios.size()) {
  case 0:
    limpiar();
    cout << "no hay usuarios aun\n" << endl;
    panel_administrador();
  default:
    cout << "0. Regresar" << endl;
    int a = 1;
    cout << "   nombre    saldo" << endl;
    for (usuario u : usuarios) {
      cout << a << ". ";
      a++;
      u.mostrar();
    }
    int opcion;
    cin >> opcion;
    if (opcion == 0) {
      limpiar();
      panel_administrador();
    } else {
      opcion_usuarios(opcion);
    }
  }
}
void menu::opcion_usuarios(int x) {
  limpiar();
  cout << "0. Regresar" << endl;
  cout << "1. Borrar" << endl;
  cout << "2. agregar saldo" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    admin_usuarios();
    break;
  case 1:
    limpiar();
    usuarios.erase(usuarios.begin() + x - 1);
    cout << "Usuario Borrado Exitosamente\n" << endl;
    panel_administrador();
    break;
  case 2:
    limpiar();
    int cuanto;
    cout << "cuanto: ";
    cin >> cuanto;
    usuarios[x - 1].agregar_saldo(cuanto);
    limpiar();
    cout << "saldo agregado exitosamente" << endl;
    admin_usuarios();
    break;
  default:
    limpiar();
    cout << "entrada incorrecta" << endl;
    opcion_usuarios(x);
    break;
  }
}
/*
aca enpieza almasen


*/
void menu::admin_almasen() {
  cout << "0. Regresar" << endl;
  cout << "1. Agregar Producto" << endl;
  cout << "2. Elimiar Producto" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    panel_administrador();
    break;
  case 1:
    limpiar();
    agregar_producto();
    break;
  case 2:
    limpiar();
    eliminar_producto();
    break;
  default:
    limpiar();
    cout << "entrada incorrecta\n" << endl;
    break;
  }
}
void menu::agregar_producto() {
  cout << "0. Rergresar" << endl;
  cout << "1. Producto Nuevo" << endl;
  cout << "2. Agregar Unidades" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    admin_almasen();
    break;
  case 1:
    limpiar();
    agregar_producto_nuevo();
    break;
  case 2:
    limpiar();
    agregar_unidades();
    break;
  default:
    cout << "entrada incorrecta\n" << endl;
    break;
  }
}
void menu::agregar_producto_nuevo() {
  limpiar();
  cout << "Nombre: ";
  string nom;
  float pre;
  int uni;
  cin >> nom;
  cout << "Precio: ";
  cin >> pre;
  cout << "unidades: ";
  cin >> uni;
  almasen.emplace_back(nom, pre, uni);
  limpiar();
  cout << "Producto Agregado Exitosamente\n" << endl;
  admin_almasen();
}
void menu::agregar_unidades() {
  cout << "0. regresar" << endl;
  int a = 1;
  cout << "   nombre    unidades" << endl;
  for (producto y : almasen) {
    cout << a << ". ";
    y.mostrar1();
    a -= -1;
  }
  int opcion;
  cin >> opcion;
  if (opcion == 0) {
    limpiar();
    agregar_producto();
  } else {
    limpiar();
    int b;
    cout << "cuantas unidades: ";
    cin >> b;
    almasen[opcion - 1].agregar_unidade(b);
    limpiar();
    cout << b << " unidades agregadas a " << almasen[opcion - 1].elnombre()
         << endl;
    admin_almasen();
  }
}
void menu::eliminar_producto() {
  cout << "0. regresar" << endl;
  int a = 1;
  cout << "   nombre" << endl;
  for (producto y : almasen) {
    cout << a << ". " << y.elnombre() << endl;
  }
  int opcion;
  cin >> opcion;
  if (opcion == 0) {
    limpiar();
    admin_almasen();
  } else {
    limpiar();
    almasen.erase(almasen.begin() + opcion - 1);
    cout << almasen[opcion - 1].elnombre() << " fue borrado\n" << endl;
    admin_almasen();
  }
}
/*
aca empiesa usuario



*/
void menu::panel_usuario() {
  cout << "0. Regresar" << endl;
  cout << "1. Iniciar Cesion" << endl;
  cout << "2. Crear Cuenta" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    menu_prinsipal();
    break;
  case 1:
    limpiar();
    iniciar_secion();
    break;
  case 2:
    crear_cuenta();
    break;
  default:
    limpiar();
    cout << "Entrada incorrecta" << endl;
    menu_prinsipal();
    break;
  }
}
void menu::crear_cuenta() {
  limpiar();
  string n_usuario, n_contra;
  cout << "Usuario: ";
  cin >> n_usuario;
  cout << "Contra: ";
  cin >> n_contra;
  usuarios.emplace_back(n_usuario, n_contra);
  limpiar();
  cout << "Cuenta Creada Exitosamente\n" << endl;
  menu_prinsipal();
}
void menu::iniciar_secion() {
  cout << "usuario: ";
  string us;
  bool t = false;
  cin >> us;
  for (int i = 0; i < usuarios.size(); i++) {
    if (usuarios[i].elnombre() == us) {
      t = true;
      memoria = i;
    }
  }
  if (t) {
    cout << "Contraseña: ";
    string co;
    cin >> co;
    if (usuarios[memoria].lacontra() == co) {
      limpiar();
      menu_usuario();
    } else {
      limpiar();
      memoria = -1;
      cout << "Contraseña Incorrecta\n" << endl;
      panel_usuario();
    }
  } else {
    limpiar();
    cout << "No Existe Ese Usuario\n" << endl;
    memoria = -1;
    panel_usuario();
  }
}
void menu::menu_usuario() {
  cout << "Hola " << usuarios[memoria].elnombre() << endl;
  cout << "0. Regresar" << endl;
  cout << "1. Ver Productos" << endl;
  cout << "2. ver Carrito" << endl;
  cout << "3. ver compras" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    cerrar_secion();
    break;
  case 1:
    limpiar();
    ver_productos();
    break;
  case 2:
    limpiar();
    ver_carrito();
    break;
  case 3:
    limpiar();
    ver_compras();
    break;
  default:
    cout << "entrada icorrecta\n" << endl;
    break;
  }
}
void menu::cerrar_secion() {
  cout << "cerrar secion?" << endl;
  cout << "0. NO" << endl;
  cout << "1. SI" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    menu_usuario();
    break;
  case 1:
    limpiar();
    memoria = -1;
    panel_usuario();
    break;
  default:
    limpiar();
    cout << "entrada incorrecta\n" << endl;
    cerrar_secion();
    break;
  }
}
void menu::ver_compras() {
  cout << "0. regresar" << endl;
  cout << "total gastado: " << usuarios[memoria].total_compras() << endl;
  usuarios[memoria].mostrar_compras();
  int opcion;
  cin >> opcion;
  if (opcion == 0) {
    limpiar();
    menu_usuario();
  } else {
    limpiar();
    cout << "entrada incorrecta\n" << endl;
    ver_compras();
  }
}
void menu::ver_productos() {
  cout << "0. Regresar" << endl;
  int a = 1;
  for (producto y : almasen) {
    cout << a << ". ";
    y.mostrar2();
    a++;
  }
  int opcion;
  cin >> opcion;
  if (opcion == 0) {
    limpiar();
    menu_usuario();
  } else {
    limpiar();
    menu_productos(opcion);
  }
}
void menu::menu_productos(int a) {
  cout << "0. Regresar" << endl;
  cout << "1. Comprar" << endl;
  cout << "2. agregar al carrito" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    ver_productos();
    break;
  case 1:
    limpiar();
    usuarios[memoria].comprar(almasen[a - 1]);
    cout << "compraste " << almasen[a - 1].elnombre() << endl << endl;
    ver_productos();
    break;
  case 2:
    limpiar();
    usuarios[memoria].agregar_a_carrito(almasen[a - 1]);
    cout << "agregaste " << almasen[a - 1].elnombre() << " al carrito" << endl
         << endl;
    ver_productos();
    break;
  default:
    limpiar();
    cout << "entrada incorrecta" << endl << endl;
    break;
  }
}
void menu::ver_carrito() {
  cout << "0. regresar" << endl;
  cout << "1. eliminar producto" << endl;
  cout << "2. comprar todo" << endl;
  int opcion;
  cin >> opcion;
  switch (opcion) {
  case 0:
    limpiar();
    menu_usuario();
    break;
  case 1:
    limpiar();
    eliminar_del_carrito();
    break;
  case 2:
    limpiar();
    usuarios[memoria].comprar_carrito();
    menu_usuario();
    break;
  default:
    limpiar();
    cout << "entrada incorrecta" << endl << endl;
    break;
  }
}
void menu::eliminar_del_carrito() {
  cout << "0. regresar" << endl;
  usuarios[memoria].mostrar_carrito();
  int opcion;
  cin >> opcion;
  if (opcion == 0) {
    limpiar();
    ver_carrito();
  } else {
    limpiar();
    usuarios[memoria].sacar_del_carrito(opcion);
    ver_carrito();
  }
}

int main() {
  menu prueva;
  prueva.menu_prinsipal();
  return 0;
}

/*
using namespace std;
class Login {
	string usuario, contrasenia;
public:
	Login() {}
	~Login() {}
	void setUsuario(string _usuario) { usuario = _usuario; }
	void setContrasenia(string _contrasenia) { contrasenia = _contrasenia; }
	string getUsuario() { return this->usuario; }
	string getContrasenia() { return this->contrasenia; }
};
class Vectorlogin {
	vector <Login> VectorLogin;
public:
	void Add(Login log) { VectorLogin.push_back(log); }
	Login Get(int pos) { return VectorLogin[pos]; }
	int rows() { return VectorLogin.size(); }
	void grabarArchivo(Login login) {
		try {
			fstream archivoLogin;
			archivoLogin.open("USUARIOS", ios::app);
			if (archivoLogin.is_open()) {
				archivoLogin << login.getUsuario() << "." << login.getContrasenia() << "." << endl;
				archivoLogin.close();
			}
		}
		catch (exception L) { cout << "ERROR DE REGISTRO" << endl; }
	}
	void guardarDatosArchivo() {
		try {
			int i;
			size_t posi;
			string linea;
			string temp[2];
			fstream archivoLogin;
			archivoLogin.open("USUARIOS", ios::in);
			if (archivoLogin.is_open()) {
				while (!archivoLogin.eof()) {
					while (getline(archivoLogin, linea)) {
						i = 0;
						while ((posi = linea.find(".")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						Login login;
						login.setUsuario(temp[1]);
						login.setContrasenia(temp[2]);
						Add(login);
					}
				}
			}
			archivoLogin.close();
		}
		catch (exception L) { cout << "ERROR EN EL ARCHIVO" << endl; }
	}
};
class Cliente1 {
	string nombre; string apellido; string dni;
	int codigo;
public:
	void setNombre(string nombre) { this->nombre = nombre; }
	void setApellido(string apellido) { this->apellido = apellido; }
	void setDni(string dni) { this->dni = dni; }
	void setCodigo(int codigo) { this->codigo = codigo; }
	string getNombre() { return nombre; }
	string getApellido() { return apellido; }
	string getDni() { return dni; }
	int getCodigo() { return codigo; }
};

class ClienteVector {
	vector<Cliente1> vectorCliente;
public:
	ClienteVector() {
		cargarDatosDelArchivoVector();
		vector<Cliente1>vectorCliente;
	}
	int getCorrelativo() {
		if (vectorCliente.size() == 0) { return 1; }
		else { return vectorCliente[vectorCliente.size() - 1].getCodigo() + 1; }
	}
	void agregar(Cliente1 objeto) {
		vectorCliente.push_back(objeto);
	}
	Cliente1 obtener(int posicion) {
		return vectorCliente[posicion];
	}
	int tamanio() {
		return vectorCliente.size();
	}
	Cliente1 buscarPorCodigo(int cod) {
		Cliente1 objError;
		objError.setNombre("ERROR");
		for (int i = 0; i < tamanio(); i++) {
			if (cod == obtener(i).getCodigo()) { return obtener(i); }
		}
		return objError;
	}
	int getPostArray(Cliente1 objeto) {
		for (int i = 0; i < tamanio(); i++) {
			if (objeto.getCodigo() == vectorCliente[i].getCodigo()) { return i; }
		}
		return -1;
	}
	void eliminar(Cliente1 objeto) {
		vectorCliente.erase(vectorCliente.begin() + getPostArray(objeto));
	}
	bool modificar(Cliente1 objeto, string name, string lastName, string DNI) {
		for (int i = 0; i < tamanio(); i++) {
			if (objeto.getCodigo() == obtener(i).getCodigo()) {
				vectorCliente[i].setNombre(name);
				vectorCliente[i].setApellido(lastName);
				vectorCliente[i].setDni(DNI); return true;
			}
		}
		return false;
	}
	void grabarEnArchivo(Cliente1 cliente) {
		try {
			fstream archivoCliente;
			archivoCliente.open("DATOS DE LOS CLIENTES.txt", ios::app);
			if (archivoCliente.is_open()) {
				archivoCliente << cliente.getCodigo() << ";" << cliente.getNombre() << ";" << cliente.getApellido() << ";" << cliente.getDni() << ";" << endl;
				archivoCliente.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRO"; }
	}
	void cargarModificado() {
		try {
			fstream archivoCliente;
			archivoCliente.open("DATOS DE LOS CLIENTES.txt", ios::out);
			if (archivoCliente.is_open()) {
				for (Cliente1 z : vectorCliente) {
					archivoCliente << z.getCodigo() << ";" << z.getNombre() << ";" << z.getApellido() << ";" << z.getDni() << ";" << endl;
				}
				archivoCliente.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRO"; }
	}
	void cargarDatosDelArchivoVector() {
		try {
			size_t posi; string linea; string temp[4];
			fstream archivoCliente;
			archivoCliente.open("DATOS DE LOS CLIENETES.txt", ios::in);
			if (archivoCliente.is_open()) {
				while (!archivoCliente.eof()) {
					while (getline(archivoCliente, linea)) {
						int i = 0;
						while ((posi = linea.find(";")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						Cliente1 cliente;
						cliente.setCodigo(std::stoi(temp[0]));
						cliente.setNombre(temp[1]);
						cliente.setApellido(temp[2]);
						cliente.setDni(temp[3]); agregar(cliente);
					}
				}
			}
			archivoCliente.close();
		}
		catch (exception e) {
			cout << "ERROR AL LEER EL ARCHIVO";
		}
	}
};
class Vendedor {
	string nombre; string apellido; string dni;
	int codigo;
public:
	void setNombre(string nombre) { this->nombre = nombre; }
	void setApellido(string apellido) { this->apellido = apellido; }
	void setDni(string dni) { this->dni = dni; }
	void setCodigo(int codigo) { this->codigo = codigo; }
	string getNombre() { return nombre; }
	string getApellido() { return apellido; }
	string getDni() { return dni; }
	int getCodigo() { return codigo; }
};
class VendedorVector {
	vector<Vendedor> vectorVendedor;
public:
	VendedorVector() {
		cargarDatosDelArchivoVector();
		vector<Vendedor>vectorVendedor;
	}
	int getCorrelativo() {
		if (vectorVendedor.size() == 0) { return 1; }
		else { return vectorVendedor[vectorVendedor.size() - 1].getCodigo() + 1; }
	}
	void agregar(Vendedor objeto) {
		vectorVendedor.push_back(objeto);
	}
	Vendedor obtener(int posicion) {
		return vectorVendedor[posicion];
	}
	int tamanio() {
		return vectorVendedor.size();
	}
	Vendedor buscarPorCodigo(int cod) {
		Vendedor objError;
		objError.setNombre("ERROR");
		for (int i = 0; i < tamanio(); i++) {
			if (cod == obtener(i).getCodigo()) { return obtener(i); }
		}
		return objError;
	}
	int getPostArray(Vendedor objeto) {
		for (int i = 0; i < tamanio(); i++) {
			if (objeto.getCodigo() == vectorVendedor[i].getCodigo()) { return i; }
		}
		return -1;
	}
	void eliminar(Vendedor objeto) {
		vectorVendedor.erase(vectorVendedor.begin() + getPostArray(objeto));
	}
	bool modificar(Vendedor objeto, string name, string lastName, string DNI) {
		for (int i = 0; i < tamanio(); i++) {
			if (objeto.getCodigo() == obtener(i).getCodigo()) {
				vectorVendedor[i].setNombre(name);
				vectorVendedor[i].setApellido(lastName);
				vectorVendedor[i].setDni(DNI); return true;
			}
		}
		return false;
	}
	void grabarEnArchivo(Vendedor vendedor) {
		try {
			fstream archivoVendedor;
			archivoVendedor.open("DATOS DE LOS VENDEDORES.txt", ios::app);
			if (archivoVendedor.is_open()) {
				archivoVendedor << vendedor.getCodigo() << ";" << vendedor.getNombre() << ";" << vendedor.getApellido() << ";" << vendedor.getDni() << ";" << endl;
				archivoVendedor.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRO"; }
	}
	void cargarModificado() {
		try {
			fstream archivoVendedor;
			archivoVendedor.open("DATOS DE LOS CLIENTES.txt", ios::out);
			if (archivoVendedor.is_open()) {
				for (Vendedor z : vectorVendedor) {
					archivoVendedor << z.getCodigo() << ";" << z.getNombre() << ";" << z.getApellido() << ";" << z.getDni() << ";" << endl;
				}
				archivoVendedor.close();
			}
		}
		catch (exception e) { cout << "EROOR AL GRABAR EL REGISTRO"; }
	}
	void cargarDatosDelArchivoVector() {
		try {
			size_t posi; string linea; string temp[4];
			fstream archivoVendedor;
			archivoVendedor.open("DATOS DE LOS CLIENETES.txt", ios::in);
			if (archivoVendedor.is_open()) {
				while (!archivoVendedor.eof()) {
					while (getline(archivoVendedor, linea)) {
						int i = 0;
						while ((posi = linea.find(";")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						Vendedor vendedor;
						vendedor.setCodigo(std::stoi(temp[0]));
						vendedor.setNombre(temp[1]);
						vendedor.setApellido(temp[2]);
						vendedor.setDni(temp[3]); agregar(vendedor);
					}
				}
			}
			archivoVendedor.close();
		}
		catch (exception e) {
			cout << "ERROR AL LEER EL ARCHIVO";
		}
	}
};
class Producto {
	int codigo;
	string descripcion;
	float precio;
	int cantidad;
public:
	Producto() {}
	~Producto() {}
	void setCantidad(int cantidad) { this->cantidad = cantidad; }
	void setCodigo(int codigo) { this->codigo = codigo; }
	void setDescripcion(string descripcion) { this->descripcion = descripcion; }
	void setPrecio(float precio) { this->precio = precio; }
	int getCodigo() { return this->codigo; }
	string getDescripcion() { return this->descripcion; }
	float getPrecio() { return this->precio; }
	int getCantidad() { return this->cantidad; }
};
class ProductoVector {
	vector<Producto>vectorProducto;
public:
	ProductoVector() { cargarDatosDelArchivoVector(); }
	void add(Producto obj) { vectorProducto.push_back(obj); }
	Producto get(int pos) { return vectorProducto[pos]; }
	int rows() { return vectorProducto.size(); }
	Producto buscarPorCodigo(int code) {
		Producto objError;
		objError.setDescripcion("ERROR");
		for (Producto x : vectorProducto) {
			if (code == x.getCodigo()) { return x; }
		} return objError;
	}
	int getPostArray(Producto obj) {
		for (int i = 0; i < rows(); i++) {
			if (obj.getCodigo() == get(i).getCodigo()) { return i; }
		} return -1;
	}
	int getCorrelativo() {
		if (vectorProducto.size() == 0) { return 1; }
		else {
			return vectorProducto[vectorProducto.size() - 1].getCodigo() + 1;
		}
	}
	void remove(Producto obj) {
		vectorProducto.erase(vectorProducto.begin() + getPostArray(obj));
	}
	bool modificar(Producto p, string descripcion, float precio) {
		for (int i = 0; i < rows(); i++) {
			if (p.getCodigo() == get(i).getCodigo()) {
				vectorProducto[i].setDescripcion(descripcion);
				vectorProducto[i].setPrecio(precio); return true;
			}
		} return false;
	}
	void grabarArchivo(Producto producto) {
		try {
			fstream archivoProducto;
			archivoProducto.open("Productos.txt", ios::app);
			if (archivoProducto.is_open()) {
				archivoProducto << producto.getCodigo() << ";" << producto.getDescripcion() << ";" << producto.getPrecio() << ";" << endl;
				archivoProducto.close();
			}
		}
		catch (exception e) {
			cout << "OCURRIO UN ERROR AL GRABAR EL REGISTRO" << endl;
		}
	}
	void cargarDatosDelArchivoVector() {
		try {
			int i;
			size_t posi;
			string linea;
			string temp[3];
			fstream archivoProducto;
			archivoProducto.open("PRODUCTOS.txt", ios::in);
			if (archivoProducto.is_open()) {
				while (!archivoProducto.eof()) {
					while (getline(archivoProducto, linea)) {
						i = 0;
						while ((posi = linea.find(";")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						Producto producto;
						producto.setCodigo(std::stoi(temp[0]));
						producto.setDescripcion(temp[1]);
						producto.setPrecio(std::stof(temp[2]));
						add(producto);
					}
				}
			} archivoProducto.close();
		}
		catch (exception e) {
			cout << "OCURRIO UN ERROR";
		}
	}
	void grabarModificarEliminarArchivo() {
		try {
			fstream archivoProducto;
			archivoProducto.open("PRODUCTOS.txt", ios::out);
			if (archivoProducto.is_open()) {
				for (Producto x : vectorProducto) {
					archivoProducto << x.getCodigo() << ";" << x.getDescripcion() << ";" << x.getPrecio() << endl;
				} archivoProducto.close();
			}
		}
		catch (exception e) {
			cout << "OCURRIO UN ERROR AL GRABAR EN EL ARCHIVO";
		}
	}
};
class Venta {
	int codVenta, codCliente, codVendedor;
	string fecha;
	float Total;
public:
	Venta() {}
	~Venta() {}
	void setcodVenta(int _codVenta) { codVenta = _codVenta; }
	void setcodCliente(int _codCliente) { codCliente = _codCliente; }
	void setcodVendedor(int _codVendedor) { codVendedor = _codVendedor; }
	void setFecha(string _Fecha) { fecha = _Fecha; }
	void setTotal(float _Total) { Total = _Total; }
	int getcodVenta() { return this->codVenta; }
	int getcodCliente() { return this->codCliente; }
	int getcodVendedor() { return this->codVendedor; }
	string getFecha() { return this->fecha; }
	float getTotal() { return this->Total; }
};
class VentaVector {
protected: vector <Venta> vectorVenta;
public: VentaVector() { }
	  int correlativo() {
		  int i = 0; try {
			  size_t posi;
			  string linea;
			  string temp[6];
			  fstream archivoVenta;
			  archivoVenta.open("Venta.txt", ios::in);
			  if (archivoVenta.is_open()) {
				  while (!archivoVenta.eof()) {
					  while (getline(archivoVenta, linea)) { i += 1; }
				  }archivoVenta.close();
			  }
		  }
		  catch (exception e) { cout << "ERROR AL ABRIR EL ARCHIVO"; } return i;
	  }
	  void agregar(Venta objeto) { vectorVenta.push_back(objeto); }
	  Venta obtener(int posicion) { return vectorVenta[posicion]; }
	  int tamanio() { return vectorVenta.size(); }
	  void grabarArchivo() {
		  try {
			  fstream archivoVenta;
			  archivoVenta.open("Venta.txt", ios::app);
			  if (archivoVenta.is_open()) {
				  for (Venta c : vectorVenta) {
					  archivoVenta << c.getcodVenta() << ";" << c.getcodCliente() << ";" << c.getcodVendedor() << ";" << c.getFecha() << ";" << c.getTotal() << endl;
				  } archivoVenta.close();
			  }
		  }
		  catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRRO!"; }
	  }
	  void cargarDatosDelArchivoVector() {
		  try {
			  int i; size_t posi;
			  string linea; string temp[6];
			  fstream archivoVenta;
			  archivoVenta.open("Venta.txt", ios::in);
			  if (archivoVenta.is_open()) {
				  while (!archivoVenta.eof()) {
					  while (getline(archivoVenta, linea)) {
						  i = 0;
						  while ((posi = linea.find(".")) != string::npos) {
							  temp[i] = linea.substr(0, posi);
							  linea.erase(0, posi + 1); i++;
						  }
						  Venta venta;
						  venta.setcodVenta(std::stoi(temp[0]));
						  venta.setcodCliente(std::stoi(temp[1]));
						  venta.setcodVendedor(std::stoi(temp[2]));
						  venta.setFecha(temp[3]);
						  venta.setTotal(std::stof(temp[4]));
						  agregar(venta);
					  }
				  }
			  } archivoVenta.close();
		  }
		  catch (exception e) { cout << "ERROR AL LEER EL ARCHIVO"; }
	  }
};
class DetalleVenta {
	int codVenta, codProducto, cantidad;
	string descripcion;
	float precioVen;
public:
	DetalleVenta() { }
	~DetalleVenta() { }
	void setcodVenta(int _codVenta) { codVenta = _codVenta; }
	void setcodProducto(int _codProducto) { codProducto = _codProducto; }
	void setCantidad(int _cantidad) { cantidad = _cantidad; }
	void setprecioVen(float _precioVen) { precioVen = _precioVen; }
	void setDescripcion(string _descripcion) { descripcion = _descripcion; }
	int getcodVenta() { return this->codVenta; }
	int getcodProducto() { return this->codProducto; }
	int getCantidad() { return this->cantidad; }
	float getprecioVen() { return this->precioVen; }
	float getSubTotal() { return getprecioVen() * getCantidad(); }
	string getDescripcion() { return this->descripcion; }
};
class DetalleVector {
	vector<DetalleVenta> detalleVector;
public:
	DetalleVector() { }
	void add(DetalleVenta obj) { detalleVector.push_back(obj); }
	DetalleVenta get(int pos) { return detalleVector[pos]; }
	int rows() { return detalleVector.size(); }
	void grabarArchivo() {
		try {
			fstream archivoDetalle;
			archivoDetalle.open("DetalleVenta.txt", ios::app);
			if (archivoDetalle.is_open()) {
				for (DetalleVenta l : detalleVector) {
					archivoDetalle << l.getcodVenta() << ";" << l.getDescripcion() << ";" << l.getCantidad() << ";" << l.getprecioVen() << endl;
				} archivoDetalle.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRO"; }
	}
	void cargarDatosDelArchivoVector() {
		try {
			int i; size_t posi;
			string linea;
			string temp[5];
			fstream archivoDetalle;
			archivoDetalle.open("DetalleVenta.txt", ios::in);
			if (archivoDetalle.is_open()) {
				while (!archivoDetalle.eof()) {
					while (getline(archivoDetalle, linea)) {
						i = 0;
						while ((posi = linea.find(";")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						DetalleVenta detalle;
						detalle.setcodVenta(std::stoi(temp[0]));
						detalle.setDescripcion(temp[1]);
						detalle.setcodProducto(std::stoi(temp[2]));
						detalle.setCantidad(std::stoi(temp[3]));
						detalle.setprecioVen(std::stof(temp[4]));
						add(detalle);
					}
				}
			} archivoDetalle.close();
		}
		catch (exception e) { cout << "ERRO AL LEER EL ARCHIVO"; }
	}
	void grabarModificarEliminarArchivo() {
		try {
			fstream archivoDetalle;
			archivoDetalle.open("DetalleVenta.txt", ios::out);
			if (archivoDetalle.is_open()) {
				for (DetalleVenta x : detalleVector) {
					archivoDetalle << x.getcodVenta() << "." << x.getcodProducto() << "." << x.getCantidad() << "." << x.getprecioVen()<<"."<< endl;
				}
				archivoDetalle.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL ARCHIVO"; }
	}
	void listarProdvector(DetalleVenta obj) {
		cout << "Codigo del producto: " << obj.getcodProducto() << endl;
		cout << "Cantidad del producto: " << obj.getCantidad() << endl;
		cout << "Subtotal: " << obj.getSubTotal() << endl;
	}
};
class Boleta {
	int codVenta, codProducto, cantidad, estado;
	string dni, nombreCli, apellidoCli, descripcion;
	string nombreVen, apellidoVen;
	float precio, subTotal, total;
public:
	void setCodVenta(int _codVenta) { codVenta = _codVenta; }
	void setEstado(int _estado) { estado = _estado; }
	void setDni(string _dni) { dni = _dni; }
	void setNombreCli(string _nombreCli) { nombreCli = _nombreCli; }
	void setApellidoCli(string _apellidoCli) { apellidoCli = _apellidoCli; }
	void setNombreVen(string _nombreVen) { nombreVen = _nombreVen; }
	void setApellidoVen(string _apellidoVen) { apellidoVen = _apellidoVen; }
	void setCodProducto(int _codProducto) { codProducto = _codProducto; }
	void setDescripcion(string _descripcion) { descripcion = _descripcion; }
	void setCantidad(int _cantidad) { cantidad = _cantidad; }
	void setPrecio(float _precio) { precio = _precio; }
	void setSubTotal(float st) { subTotal = st; }
	void setTotal(float _total) { total = _total; }
	int getCodventa() { return codVenta; }
	int getEstado() { return estado; }
	string getDni() { return dni; }
	string getNombreCli() { return nombreCli; }
	string getApellidoCli() { return apellidoCli; }
	string getNombreVen() { return nombreVen; }
	string getApellidoVen() { return apellidoVen; }
	int getCodProducto() { return codProducto; }
	string getDescripcion() { return descripcion; }
	int getCantidad() { return cantidad; }
	float getPrecio() { return precio; }
	float getSubTotal() { return subTotal; }
	float getTotal() { return total; }
};
class BoletaVector {
	vector<Boleta> boletaVector;
public:
	BoletaVector() { }
	void add(Boleta obj) { boletaVector.push_back(obj); }
	Boleta get(int pos) { return boletaVector[pos]; }
	int rows() { boletaVector.size(); }
	void grabarArchvo(Boleta boleta) {
		try {
			fstream archivoBoleta;
			archivoBoleta.open("Boleta.txt", ios::app);
			if (archivoBoleta.is_open()) {
				for (Boleta bo : boletaVector) {
					archivoBoleta << bo.getCodventa() << ";" << bo.getDni() << ";" << bo.getNombreCli() << ";" << bo.getApellidoCli() << ";" << bo.getNombreVen() << ";" << bo.getApellidoVen() << ";" << bo.getTotal() << ";" << bo.getEstado() << endl;
				}
				archivoBoleta.close();
			}
		}
		catch (exception e) { cout << "ERROR AL GRABAR EL REGISTRO"; }
	}
	void cargarDatosDelArchivoVector() {
		try {
			int i; size_t posi;
			string linea, temp[8];
			fstream archivoBoleta;
			archivoBoleta.open("Boleta.txt", ios::in);
			if (archivoBoleta.is_open()) {
				while (!archivoBoleta.eof()) {
					while (getline(archivoBoleta, linea)) {
						i = 0;
						while ((posi = linea.find(";")) != string::npos) {
							temp[i] = linea.substr(0, posi);
							linea.erase(0, posi + 1); i++;
						}
						Boleta boleta;
						boleta.setCodVenta(std::stoi(temp[0]));
						boleta.setDni(temp[1]);
						boleta.setNombreCli(temp[2]);
						boleta.setApellidoCli(temp[3]);
						boleta.setNombreVen(temp[4]);
						boleta.setApellidoVen(temp[5]);
						boleta.setTotal(std::stof(temp[6]));
						boleta.setEstado(std::stof(temp[7]));
						add(boleta);
					}
				}
			} archivoBoleta.close();
		}
		catch (exception e) { cout << "ERROR AL LEER EL ARCHIVO"; }
	}
};

VendedorVector vendedorVector;
Vectorlogin vectorlogin;
ClienteVector cliente_vector;
ProductoVector vectorProducto;
VentaVector ventaVector;
DetalleVector detalleVector;
BoletaVector boletaVector;

void menuPrincipal();
void salidaSistema();
void vistaVendedor();
void vistaCliente();
void vistaProducto();

void adicionarVendedor();
void listarVendedor();
void EliminarVendedor();
void modificarVendedor();
void buscarVendedor();

void adicionarCliente();
void modificarCliente();
void listarCliente();
void EliminarCliente();
void buscarCliente();

void adicionarProducto();
void modificarProducto();
void listarProducto();
void EliminarProducto();
void buscarProducto();

void vistaVenta();
void vistaBoleta();

void gotoxy(int x, int y) {
	HANDLE hcon = GetStdHandle(STD_OUTPUT_HANDLE);
	COORD dwPos;
	dwPos.X = x;
	dwPos.Y = y;
	SetConsoleCursorPosition(hcon, dwPos);
}
void inicioSesion() {
	vector <string> usuarios;
	vector <string> claves;

	usuarios.push_back("JUAN");
	usuarios.push_back("DANIEL");
	usuarios.push_back("SEBASTIAN");
	usuarios.push_back("fernando");
	usuarios.push_back("leon");

	claves.push_back("JUAN123");
	claves.push_back("jhonDANIEL");
	claves.push_back("pablito321");
	claves.push_back("fernando");
	claves.push_back("leonel");

	string usuario; string contrasenia;
	int intento = 0;
	bool ingreso = false;
	char caracter;
	do {
		HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
		gotoxy(4, 5); cout << "==============================";
		gotoxy(4, 6); cout << "|| ||";
		gotoxy(4, 7); cout << "|| Bienvenido ||";
		gotoxy(4, 8); cout << "|| ||";
		gotoxy(4, 9); cout << "|| Usuario: ||";
		gotoxy(4, 10); cout << "|| Contrasenia: ||";
		gotoxy(4, 11); cout << "|| ||";
		gotoxy(4, 12); cout << "==============================";
		gotoxy(22, 9); getline(cin, usuario);
		gotoxy(26, 10); caracter = _getch();
		contrasenia = "";
		while (caracter != 13) {
			if (caracter != 8) {
				contrasenia.push_back(caracter); cout << "*";
			}
			else {
				if (contrasenia.length() > 0) {
					cout << "\b \b";
					contrasenia = contrasenia.substr(0, contrasenia.length() - 1);
				}
			}
			caracter = _getch();
		}
		for (int i = 0; i < usuario.size(); i++) {
			if (usuarios[i] == usuario && claves[i] == contrasenia) {
				ingreso = true; break;
			}
		}
		if (!ingreso) {
			//HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
			gotoxy(4, 13); cout << "EL USUARIO O CONTRASENIA SON INCORRECTOS" << endl;
			gotoxy(4, 14); cout << "**INTENTOS**:" << endl;
			gotoxy(4, 15); cout << intento + 1 << "de 3 intentos" << endl;
			cin.get(); intento++;
		}
		Login login;
		login.setUsuario(usuario);
		login.setContrasenia(contrasenia);
		//VectorLogin.Add(login);
		//VectorLogin.GrabarArchivo(login);
	} while (intento < 3 && ingreso == false);
	if (ingreso == true) {
		cout << "ingreso correcto" << endl; menuPrincipal();
	}
	else { cout << "ha pasado el limite de intentos" << endl; salidaSistema(); }
}
void menuPrincipal() {
	int opcion_menu;
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	gotoxy(4, 5); cout << "===================================";
	gotoxy(4, 6); cout << "|| ||";
	gotoxy(4, 7); cout << "|| ADMINISTRADOR ||";
	gotoxy(4, 8); cout << "|| ||";
	gotoxy(4, 9); cout << "|| 1.Vendedor ||";
	gotoxy(4, 10); cout << "|| 2.Cliente ||";
	gotoxy(4, 11); cout << "|| 3.Almacen ||";
	gotoxy(4, 12); cout << "|| 4.Venta ||";
	gotoxy(4, 13); cout << "|| 5.Salida del sistema ||";
	gotoxy(4, 14); cout << "===================================";
	gotoxy(10, 18); cout << "|=====================|";
	gotoxy(10, 19); cout << "| Elija una opcion: |";
	gotoxy(10, 20); cout << "|=====================|";
	gotoxy(29, 19); cin >> opcion_menu;
	switch (opcion_menu) {
	case 1: vistaVendedor(); break;
	case 2: vistaCliente(); break;
	case 3: vistaProducto(); break;
	case 4: vistaVenta(); break;
	case 5: gotoxy(2, 24); cout << "--GRACIAS POR SU PREFERENCIA--" << endl;
		system("pause"); salidaSistema();
	default: gotoxy(10, 24); cout << "Ingrese una opcion correcta" << endl;
		system("pause"); HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); menuPrincipal();
	}
}
void vistaCliente() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	int op_menuClientes;
	gotoxy(4, 5); cout << "================================";
	gotoxy(4, 6); cout << "|| ||";
	gotoxy(4, 7); cout << "|| CLIENTES ||";
	gotoxy(4, 8); cout << "|| ||";
	gotoxy(4, 9); cout << "|| 1.Anadir cliente ||";
	gotoxy(4, 10); cout << "|| 2.Modificar cliente ||";
	gotoxy(4, 11); cout << "|| 3.Listar cliente ||";
	gotoxy(4, 12); cout << "|| 4.Eliminar cliente ||";
	gotoxy(4, 13); cout << "|| 5.buscar cliente ||";
	gotoxy(4, 14); cout << "|| 6.Regresar ||";
	gotoxy(4, 15); cout << "|| 7.Salida del sistema ||";
	gotoxy(4, 16); cout << "|| ||";
	gotoxy(4, 17); cout << "================================";
	gotoxy(10, 19); cout << "|====================|";
	gotoxy(10, 20); cout << "| Elija una opcion: |";
	gotoxy(10, 21); cout << "|====================|";
	gotoxy(29, 20); cin >> op_menuClientes;
	switch (op_menuClientes) {
	case 1: HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); adicionarCliente(); break;
	case 2: modificarCliente(); break;
	case 3: HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); listarCliente(); break;
	case 4: EliminarCliente(); break;
	case 5: buscarCliente(); break;
	case 6: menuPrincipal(); break;
	case 7: salidaSistema(); break;
	default:gotoxy(31, 20); cout << "INGRESE LA OPCION CORRECTA" << endl;
		system("pause"); HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); vistaVendedor();
	}
}
void adicionarCliente() {
	string name;
	string lastName;
	string DNI;
	int cod;
	string rpta;
	cout << "\t==ANIADIR CLIENTE==\t" << endl;
	do {
		cout << "\t";
		cod = cliente_vector.getCorrelativo();
		cout << "CODIGO: " << "[" << cod << "]" << endl;
		cin.ignore();
		cout << "Ingrese el DNI del cliente: "; getline(cin, DNI);
		cout << " " << endl;
		cout << "Ingrese el nombre del cliente: "; getline(cin, name);
		cout << " " << endl;
		cout << "ingrese el apellido del cliente: "; getline(cin, lastName);
		cout << " " << endl;
		Cliente1 cliente;
		cliente.setNombre(name);
		cliente.setApellido(lastName);
		cliente.setDni(DNI);
		cliente.setCodigo(cod);
		cliente_vector.agregar(cliente);
		cliente_vector.grabarEnArchivo(cliente);
		cout << "\t\t\tIngrese SI o NO para seguir ingresando clientes: "; cin >> rpta;
		HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	} while (rpta == "SI" || rpta == "si"); vistaCliente();
}
void modificarCliente() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	int cod;
	cout << "Ingrese el codigo a modificar: "; cin >> cod;
	Cliente1 objAModificar = cliente_vector.buscarPorCodigo(cod);
	cout << "\t==REGISTRO ENCONTRADO==\t" << endl;
	cout << "Codigo: " << objAModificar.getCodigo() << "\n";
	cout << "DNI: " << objAModificar.getDni() << "\n";
	cout << "Nombre: " << objAModificar.getNombre() << "\n";
	cout << "Apellido: " << objAModificar.getApellido() << "\n";
	cin.ignore();
	string nomModificado;
	string apeModificado;
	string dniModificado;
	cout << "\t + MODIFICAR CAMPOS + \n";
	cout << "Ingrese el DNI nuevo: "; getline(cin, dniModificado);
	cout << "Ingrese el nombre nuevo: "; getline(cin, nomModificado);
	cout << "Ingrese el apellido nuevo: "; getline(cin, apeModificado);
	bool estado = cliente_vector.modificar(objAModificar, nomModificado, apeModificado, dniModificado);
	if (estado = true) {
		cout << "Registro del cliente modificado correctamente.\n";
		cliente_vector.cargarModificado();
	}
	else { cout << "No se modifico los datos del cliente\n"; }
	system("pause"); vistaCliente();
}
void listarCliente() {
	cout << "\t+ CLIENTES REGISTRADOS +\t" << endl;
	if (cliente_vector.tamanio() == 0) {
		cout << endl; cout << "\t\t+ LIRERIA SCHOOL + " << endl;
		cout << "NO HAY REGISTRADOS POR AHORA" << endl;
		system("pause"); vistaCliente();
	}
	else {
		for (int i = 0; i < cliente_vector.tamanio(); i++) {
			cout << endl;
			cout << "Codigo: " << cliente_vector.obtener(i).getCodigo() << endl;
			cout << endl;
			cout << "\tDNI: " << cliente_vector.obtener(i).getDni() << endl;
			cout << endl;
			cout << "Nombre: " << cliente_vector.obtener(i).getNombre() << endl;
			cout << endl;
			cout << "Apellidos: " << cliente_vector.obtener(i).getApellido() << endl;
			cout << "===========================================================" << endl;
		}
		system("pause"); HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); vistaCliente();
	}
}
void EliminarCliente() {
	int cod;
	string rpt; HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	cout << "\t Ingrese codigo a eliminar: "; cin >> cod;
	Cliente1 clienteAEliminar = cliente_vector.buscarPorCodigo(cod);
	cout << endl;
	if (clienteAEliminar.getNombre() == "ERROR") {
		cout << "NO SE ENCONTRO ESE REGISTRO" << endl;
		system("pause"); vistaCliente();
	}
	else {
		cout << "\t + REGISTRO ENCONTRADO +" << endl;
		cout << "Codigo: " << clienteAEliminar.getCodigo() << endl;
		cout << "DNI: " << clienteAEliminar.getDni() << endl;
		cout << "Nombre: " << clienteAEliminar.getNombre() << endl;
		cout << "Apellidos: " << clienteAEliminar.getApellido() << endl;
		cin.ignore(); cout << "DESEA ELIMINAR EL REGISTRO(si/no): ";
		cin >> rpt;
		if (rpt == "SI" || rpt == "si") {
			cliente_vector.eliminar(clienteAEliminar);
			cout << "-REGISTRO ELIMINADO CON EXITO-" << endl;
			cliente_vector.cargarModificado();
			system("pause"); vistaCliente();
		}
		else {
			system("pause"); EliminarCliente();
		}
	}
}
void buscarCliente() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); int cod;
	cout << "\t+BUSCAR CLIENTE REGISTRADO+\t" << endl;
	cout << "Ingrese codigo de cliente a buscar: "; cin >> cod;
	Cliente1 cli = cliente_vector.buscarPorCodigo(cod);
	if (cli.getNombre() != "ERROR") {
		cout << "\t+DATOS DEL CLIENTE ENCONTRADO+\t\n";
		cout << "codigo: " << cli.getCodigo() << endl;
		cout << "Nombre: " << cli.getNombre() << endl;
		cout << "Apellidos: " << cli.getApellido() << endl;
		cout << "DNI: " << cli.getDni() << endl;
		system("pause"); vistaCliente();
	}
	else {
		cout << "NO SE ENCONTRO EL REGISTRO";
	}
	system("pause"); vistaCliente();
}
void vistaVendedor() {

}

void vistaProducto() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	int op_menuProductos;
	gotoxy(4, 5); cout << "==================================";
	gotoxy(4, 6); cout << "|| ||";
	gotoxy(4, 7); cout << "|| ALMACEN ||";
	gotoxy(4, 8); cout << "|| ||";
	gotoxy(4, 9); cout << "|| 1.Aniadir productos ||";
	gotoxy(4, 10); cout << "|| 2.Modificar productos ||";
	gotoxy(4, 11); cout << "|| 3.Listar productos ||";
	gotoxy(4, 12); cout << "|| 4.Eliminar productos ||";
	gotoxy(4, 13); cout << "|| 5.Buscar productos ||";
	gotoxy(4, 14); cout << "|| 6.Regresar ||";
	gotoxy(4, 15); cout << "|| 7.Salida del sistema ||";
	gotoxy(4, 16); cout << "|| ||";
	gotoxy(4, 17); cout << "==================================";
	gotoxy(10, 18); cout << "|====================|";
	gotoxy(10, 19); cout << "| Elija una opcion: |";
	gotoxy(10, 20); cout << "|====================|";
	gotoxy(29, 19); cin >> op_menuProductos;
	switch (op_menuProductos) {
	case 1: HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); adicionarProducto(); break;
	case 2: modificarProducto(); break;
	case 3: HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); listarProducto(); break;
	case 4: EliminarProducto(); break;
	case 5: buscarProducto(); break;
	case 6: menuPrincipal(); break;
	case 7: salidaSistema(); break;
	default: gotoxy(31, 20); cout << "INGRESE LA OPCION CORRECTA" << endl;
		system("pause"); HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); vistaProducto();
	}
}
void adicionarProducto() {
	int code;
	string descripcion;
	float precio;
	string rpta;
	do {
		cout << "\t+AGREGAR PRODUCTO A AL ALMACEN+\t";
		code = vectorProducto.getCorrelativo();
		cout << "Codigo [" << "0000" << code << "]" << endl;
		cout << "Ingresar descripcion del producto: "; cin >> descripcion;
		cout << "Ingrese precio del producto: S/. "; cin >> precio;
		Producto producto;
		producto.setCodigo(code);
		producto.setDescripcion(descripcion);
		producto.setPrecio(precio);
		vectorProducto.add(producto);
		vectorProducto.grabarArchivo(producto);
		cout << "Para continuar pulse(SI o NO): "; cin >> rpta; HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	} while (rpta == "SI" || rpta == "si");
	vistaProducto();
}
void modificarProducto() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); int cod; string rpt;
	do {
		cout << "\t+MODIFICAR DATOS DEL PRODUCTO+\t" << endl;
		cout << "Ingesar codigo a modificar: "; cin >> cod;
		Producto p = vectorProducto.buscarPorCodigo(cod);
		string desMod; float price;
		cout << "\t+REGISTRO ENCONTRADO+\t" << endl;
		cout << "Codigo: [" << "0000" << p.getCodigo() << endl;
		cout << "---------------------------------------" << endl;
		cout << "Descripcion: " << p.getDescripcion() << endl;
		cout << "----------------------------------------" << endl;
		cout << "Precio: " << "S/. " << p.getPrecio() << endl;
		cin.ignore(); cout << endl;
		cout << "\t++MODIFICAR CAMPOS++" << endl;
		cout << "descripcion modificado: "; cin >> desMod;
		cout << "Precio Modificado: "; cin >> price;
		bool estado = vectorProducto.modificar(p, desMod, price);
		if (estado = true) {
			cout << "++REGISTRO MODFICADO SATISFACTORIAMENTE++" << endl;
			vectorProducto.grabarModificarEliminarArchivo();
			cout << "Desea regresar al menu de Productos (SI o NO): "; cin >> rpt;
		}
		else { cout << "NO SE MODFICO EL REGISTRO"; }
	} while (rpt == "NO" || rpt == "no");
	system("pause"); HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); vistaProducto();
}
void listarProducto() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); if (vectorProducto.rows() == 0) {
		cout << endl;
		cout << "\t\t+LIBRERIA SCHOOL+" << endl;
		cout << "NO HAY REGISTROS POR AHORA" << endl;
		system("pause"); vistaProducto();
	}
	else {
		for (int i = 0; i < vectorProducto.rows(); i++) {
			cout << "Codigo: " << "0000" << vectorProducto.get(i).getCodigo() << endl;
			cout << "Descripcion: " << vectorProducto.get(i).getDescripcion() << endl;

		}
	}
}

void vistaVenta() {
	int codes, cantidad, estado = 0, c;
	string rpt, rpta, fecha;
	int code, codigo, cod;
	float total = 0;
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	cout << "\t++VENTA DE PRODUCTOS++\t" << endl;
	c = ventaVector.correlativo();
	fecha = "27/06/2024";
	cout << "Fecha: " << fecha << endl;
	cout << "Codigo de venta [" << "0" << c + 1 << "]" << endl;
	cout << "Ingresar codigo del cliente: "; cin >> code;
	Cliente1 cli = cliente_vector.buscarPorCodigo(code);
	cout << "Cliente: " << cli.getDni() << " " << cli.getNombre() << " " << cli.getApellido() << endl;
	cout << "===================================================" << endl;
	cout << "Ingresar codigo del vendedor: "; cin >> codigo;
	Vendedor ven = vendedorVector.buscarPorCodigo(codigo);
	cout << "Vendedor: " << ven.getNombre() << " " << ven.getApellido() << endl;
	cout << endl;
	cout << "\t++PRODUCTOS EN VENTA++\t" << endl;
	do {
		for (int i = 0; i < vectorProducto.rows(); i++) {
			cout << "Codigo: " << "000" << vectorProducto.get(i).getCodigo() << endl;
			cout << "Descripcion: " << vectorProducto.get(i).getDescripcion() << endl;
			cout << "Precio: " << vectorProducto.get(i).getPrecio() << endl;
			cout << "=====================================" << endl;
		}cout << endl;
		cout << "Ingrese el codigo del producto: "; cin >> codes; HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
		Producto p = vectorProducto.buscarPorCodigo(codes);
		if (p.getDescripcion() == "ERROR") {
			cout << "No se encontro el registro" << endl; vistaVenta();
		}
		else {
			cout << "++REGISTRO ENCONTRADO++" << endl;
			cout << "Codigo: " << "000" << p.getCodigo() << endl;
			cout << "Descripcion: " << p.getDescripcion() << endl;
			cout << "Precio: " << "S/." << p.getPrecio() << endl;
		}
		cout << "Cantidad: "; cin >> cantidad;
		cout << "Esta seguro de agregar los siguientes productos al carrito?" << endl; cin >> rpt;
		if (rpt == "SI" || rpt == "si") {
			c = ventaVector.correlativo();
			DetalleVenta detalle;
			detalle.setcodVenta(c + 1);
			detalle.setDescripcion(p.getDescripcion());
			detalle.setcodProducto(codes);
			detalle.setCantidad(cantidad);
			detalle.setprecioVen(p.getPrecio());
			detalleVector.add(detalle);
			total += detalle.getSubTotal();
			//detalleVector.listarProdVector(detalle);
		}
		else { system("pause"); vistaVenta(); }
		cout << "DESEA AGREGAR OTRO PRODUCTO A LA BOLETA?"; cin >> rpta;
	} while (rpta == "si" || rpta == "SI");
	detalleVector.grabarArchivo();
	Venta venta;
	venta.setcodVenta(c + 1);
	venta.setcodCliente(code);
	venta.setcodVendedor(codigo);
	venta.setFecha(fecha);
	venta.setTotal(total);
	ventaVector.agregar(venta);
	ventaVector.grabarArchivo();
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
	cout << "++BOLETA++" << endl;
	venta.setcodVenta(c + 1);
	cout << "Codigo de venta: F00" << c + 1 << endl;
	cout << "DNI del cliente: " << cli.getDni() << endl;
	cout << "Nombre del cliente: " << cli.getNombre() << " " << cli.getApellido() << endl;
	cout << "Nombre del vendedor: " << ven.getNombre() << " " << ven.getApellido() << endl;
	cout << "PRODUCTOS: " << endl;
	for (int i = 0; i < detalleVector.rows(); i++) {
		cout << "Codigo del Producto: " << detalleVector.get(i).getcodProducto() << endl;
		cout << "Descripcion del producto: " << detalleVector.get(i).getDescripcion() << endl;
		cout << "Cantidad del producto a llevar: " << detalleVector.get(i).getCantidad() << endl;
		cout << "Precio de venta unitario: " << detalleVector.get(i).getprecioVen() << endl;
		cout << "Subtotal: " << detalleVector.get(i).getSubTotal() << endl;
		cout << "===================================================" << endl;
	}
	cout << "Total: " << "S/. " << total << endl;
	cout << "Desea anular la boleta (0/1): "; cin >> estado;
	if (estado == 1) {
		cout << "++GRACIAS POR SU VISTA, VUELVA PRONTO!!!" << endl;
		Boleta boleta;
		boleta.setEstado(estado);
		boletaVector.add(boleta);
		//boletaVector.grabarArchivo(boleta);
		system("pause");
	}
	else {
		Boleta boleta;
		boleta.setCodVenta(c + 1);
		boleta.setDni(cli.getDni());
		boleta.setNombreCli(cli.getNombre());
		boleta.setApellidoCli(cli.getApellido());
		boleta.setNombreVen(ven.getNombre());
		boleta.setApellidoVen(ven.getApellido());
		boleta.setTotal(total);
		boleta.setEstado(estado);
		boletaVector.add(boleta);
		//boletaVector.grabarArchivo(boleta);
		cout << "++GRACIAS POR SU COMPRA, VUELVA PRONTO!!!++" << endl;
		system("pause");
	}
}
void salidaSistema() {
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); exit(0);
}
int main() {
	system("color B0");
	inicioSesion();
}
*/





class productos{
    public:
    long long codigo;
    string nombre;
    double precio;
    void mostrar();
    // Constructor
    Producto(string n, double p) : nombre(n), precio(p) {}

    
    
};
// Método para mostrar detalles del producto
void productos::mostrar(){
        cout << "Nombre: " << nombre << ", Precio: $" << precio << endl;
}
// Clase Tienda
class Tienda {
private:
    vector<Producto*> productos;

public:
    void agregarProducto();
    void mostrarProductos();
    void venderProducto();
    void ticketProducto();
};
// Método para agregar un nuevo producto a la tienda
void Tienda::agregarProducto(int i;int cant){
    cout<<"Producto: "<<i<<" ("<<cant+1<<")."<<endl;
    cout<<"ingrese el nombre del producto: ";
    cin>>nombre;
    cout<<"Ingrese el precio del producto: ";
    cin>>precio;
    cout<<"ingrese el codigo del producto: ";
    cin>>codigo;
}

// Método para mostrar todos los productos disponibles
void Tienda::mostrarProductos(){
    for (int i=0;i<=cant;i++) {
        cout<<"Codigo:\tProducto:\tPrecio: "<<endl;
        cout<<codigo<<"\t"<<nombre<<"\t\t$"<<precio<<endl;
    }
}

// Método para realizar una venta (simplemente muestra el detalle del producto)
void Tienda::venderProducto(Tienda obj[],int cant){
    int tick[30],i=0,j=0,aux=1,aux2,cont=0;
    while(aux!=0){
        cout<<"Ingrese el codigo del producto (Presione 0 para finalizar la compra)"<<endl;
        cin<<aux;
        if(aux==0){
            break;
        }
        while(i<cant){
            if(obj[i].codigo==aux){
                aux2=i;
            } i++;
        }
        obj[aux2].mostrarProducto();
        if(aux!=0){
            tick[j]=aux;
            i++;
        }else{cout<<"Producto agotado."<<endl; system("PAUSE");}
        cont=cont++;
    }
    ticketProducto(tick.cont.obj.cant);
    cout<<endl;
}
void Tienda::ticketProducto(int tick[],int cant,Tienda obj[],int cont){
	int i=0,j=0,b=0,a=0,folio,aux=0;
	float total=0,ptos=0,pago=0,cambio=0;
	for(a=0;a<cant;a++){
		for(b=0;b<cont;b++){
		if(tick[a]==obj[b].codigo){
		total=total+obj[b].precio;	
		}
		}
	}
    cout<<endl<<endl<<endl<<endl;
    if(total<500){
        ptos=0;
    }
    if(total>=500 && total<1000){
			ptos=total*-0.01;
		}
	if(total>=1000 && total <50000){
			ptos=total*-0.02;
		}
	if(total>=50000 && total <250000){
			ptos=total*-0.03;
		}
	if(total>=250000){
			ptos=total*-0.05;
		}
	total=total+ptos;
	cout<<"TOTAL:\t"<<total<<endl;;
	while(aux==0){
	cout<<"Importe\n$";
	cin>>pago;
    if(pago<total){
        cout<<"EL PAGO NO PUEDE SER MENOR."<<endl;
        system("PAUSE");
    }else{aux=1;}
    }
    string nombreArchivo = "ticket.txt";
    ofstream archivo;
    archivo.open(nombreArchivo.c_str(), fstream::out);
	cout<<"\n\n\n\t\t\t***TICKET TIENDA***\n";
	archivo<<"\n\n\n\t\t\t***TICKET TIENDA***\n";
	cout<<"\tProducto:\t\t\t\tPrecio:\n";	
	archivo<<"\tProducto:\t\t\t\tPrecio:\n";	
	srand(time(NULL));		  
	folio=10000000 + rand() % 99999999;	
	for(i=0;i<cant;i++){
		for(j=0;j<cont;j++){
		if(tick[i]==obj[j].codigo){
		cout<<"\t"<<obj[j].nombre<<"\t\t\t\t\t$"<<obj[j].precio<<"\n";
		archivo<<"\t"<<obj[j].nombre<<"\t\t\t\t\t$"<<obj[j].precio<<"\n";
		}
		}
	}
    cambio=total-pago;
	if(ptos!=0){
		ptos=ptos*-1;
	}
	cout<<"\tCompra:\t\t\t\t\t$"<<total+ptos<<"\n";	
	archivo<<"\tCompra:\t\t\t\t\t$"<<total+ptos<<"\n";	
	cout<<"\tDescuento:\t\t\t\t-$"<<ptos<<"\n";	
	archivo<<"\tDescuento:\t\t\t\t-$"<<ptos<<"\n";	
	cout<<"\tTotal:\t\t\t\t\t$"<<total<<"\n";
	archivo<<"\tTotal:\t\t\t\t\t$"<<total<<"\n";
	cout<<"\tImporte:\t\t\t\t$"<<pago<<"\n";	
	archivo<<"\tImporte:\t\t\t\t$"<<pago<<"\n";	
	cout<<"\tCambio:\t\t\t\t\t$"<<cambio*-1<<"\n";	
	archivo<<"\tCambio:\t\t\t\t\t$"<<cambio*-1<<"\n";	
	cout<<"\tFolio:\t\t\t\t\t"<<folio<<"\n";
	archivo<<"\tFolio:\t\t\t\t\t"<<folio<<"\n";
	archivo.close();
	cout<<"\nTicket guardado correctamente!\n";
}
int main() {
    // Creando objetos de Producto
    Producto lapicero("Lapicero", 5.00);
    Producto cuaderno("Cuaderno", 10.00);
    Producto mochila("Mochila", 20.00);

    // Creando objeto de Tienda
    Tienda tienda;

    // Agregando productos a la tienda
    tienda.agregarProducto(&lapicero);
    tienda.agregarProducto(&cuaderno);
    tienda.agregarProducto(&mochila);

    // Mostrando productos disponibles
    cout << "Productos disponibles:" << endl;
    tienda.mostrarProductos();

    // Realizando una venta (por ejemplo, vendiendo el primer producto)
    tienda.venderProducto(0); // Esto imprimirá los detalles del Lapicero

    return 0;
}
