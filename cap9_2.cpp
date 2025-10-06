#include <iostream>
#include <iomanip>
#include <cstring>
#include <cassert>

using namespace std;

class Employee
{
public:
    Employee(const char *, const char *);
    void print() const;
    ~Employee();

private:
    char *firstName;
    char *lastName;
};

Employee::Employee(const char *first, const char *last)
{
    firstName = new char[strlen(first) + 1];
    assert(firstName != 0);
    strcpy(firstName, first);

    lastName = new char[strlen(last) + 1];
    assert(lastName != 0);
    strcpy(lastName, last);
}

void Employee::print() const
{
    cout << firstName << ' ' << lastName;
}

Employee::~Employee()
{
    delete[] firstName;
    delete[] lastName;
}

class HourlyWorker : public Employee
{
public:
    HourlyWorker(const char *, const char *, double, double);
    double getPay() const;
    void print() const;

private:
    double wage;
    double hours;
};

HourlyWorker::HourlyWorker(const char *first,
                           const char *last,
                           double initHours, double initWage)
    : Employee(first, last)
{
    hours = initHours;
    wage = initWage;
}

double HourlyWorker::getPay() const
{
    return wage * hours;
}

void HourlyWorker::print() const
{
    cout << "HourlyWorker::print() is executing\n\n";
    Employee::print();

    cout << " is an hourly worker with pay of $"
         << setiosflags(ios::fixed | ios::showpoint)
         << setprecision(2) << getPay() << endl;
}

int main()
{
    HourlyWorker h("Bob", "Smith", 40.0, 10.00);
    h.print();
    return 0;
}
