class Implementation
{
public:
    Implementation(int v) { value = v; }
    void setValue(int v) { value = v; }
    int getValue() const { return value; }

private:
    int value;
};
class Implementation; // forward class declaration
class Interface
{
public:
    Interface(int);
    void setValue(int);   // same public interface as
    int getValue() const; // class Implementation
    ~Interface();

private:
    Implementation *ptr; // requires previous
};
// #include "interface.h"
// #include "implementation.h"
Interface::Interface(int v)
    : ptr(new Implementation(v)) {}
void Interface::setValue(int v) { ptr->setValue(v); }
int Interface::getValue() const { return ptr->getValue(); }
Interface::~Interface() { delete ptr; }
#include <iostream>
using std::cout;
using std::endl;
// #include "interface.h"
int main()
{
    Interface i(5);
    cout << "Interface contains: " << i.getValue()
         << " before setValue" << endl;
    i.setValue(10);
    cout << "Interface contains: " << i.getValue() << " after setValue" << endl;
    return 0;
}
