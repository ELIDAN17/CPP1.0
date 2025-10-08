#include <iostream>
using std::cout;
using std::endl;
class Count
{
    friend void setX(Count &, int); // friend declaration
public:
    Count() { x = 0; }                        // constructor
    void print() const { cout << x << endl; } // output
private:
    int x; // data member
};
void setX(Count &c, int val)
{
    c.x = val; // legal: setX is a friend of Count
}
int main()
{
    Count counter; // create Count object
    cout << "counter.x after instantiation: ";
    counter.print();
    cout << "counter.x after call to setX friend function: ";
    setX(counter, 8); // set x with a friend
    counter.print();
    return 0;
}
