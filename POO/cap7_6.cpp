#include <iostream>
using std::cout;
using std::endl;
class Test
{
public:
    Test(int = 0); // default constructor
    void print() const;

private:
    int x;
};
Test::Test(int a) { x = a; } // constructor
void Test::print() const     // ( ) around *this required
{
    cout << "        x = " << x << "\n  this->x = " << this->x
         << "\n(*this).x = " << (*this).x << endl;
}
int main()
{
    Test testObject(12);
    testObject.print();
    return 0;
}
