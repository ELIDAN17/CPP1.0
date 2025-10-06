#include <iostream>
using std::cout;
using std::endl;
class Date
{
public:
    Date(int = 1, int = 1, int = 1990); // default constructor
    void print();

private:
    int month;
    int day;
    int year;
};
Date::Date(int m, int d, int y)
{
    month = m;
    day = d;
    year = y;
}
void Date::print() { cout << month << '-' << day << '-' << year; }
int main()
{
    Date date1(7, 4, 1993), date2; // d2 defaults to 1/1/90
    cout << "date1 = ";
    date1.print();
    cout << "\ndate2 = ";
    date2.print();
    date2 = date1; // assignment by default memberwise copy
    cout << "\n\nAfter default memberwise copy, date2 = ";
    date2.print();
    cout << endl;
    return 0;
}

/*
// 7
#ifndef TIME4_H
#define TIME4_H
class Time
{
public:
    Time(int = 0, int = 0, int = 0);
    void setTime(int, int, int);
    int getHour();
    int &badSetHour(int); // DANGEROUS reference return
private:
    int hour;
    int minute;
    int second;
};
#endif

// #include "time4.h"
Time::Time(int hr, int min, int sec) { setTime(hr, min, sec); }
void Time::setTime(int h, int m, int s)
{
    hour = (h >= 0 && h < 24) ? h : 0;
    minute = (m >= 0 && m < 60) ? m : 0;
    second = (s >= 0 && s < 60) ? s : 0;
}
int Time::getHour() { return hour; }
int &Time::badSetHour(int hh)
{
    hour = (hh >= 0 && hh < 24) ? hh : 0;
    return hour; // DANGEROUS reference return
}

#include <iostream>
using std::cout;
using std::endl;
// #include "time4.h"
int main()
{
    Time t;
    int &hourRef = t.badSetHour(20);
    cout << "Hour before modification: " << hourRef;
    hourRef = 30; // modification with invalid value
    cout << "\nHour after modification: " << t.getHour();
    t.badSetHour(12) = 74;
    cout << "\n\n*********************************\n"
         << "POOR PROGRAMMING PRACTICE!!!!!!!!\n"
         << "badSetHour as an lvalue, Hour: " << t.getHour()
         << "\n*********************************" << endl;
    return 0;
}*/

/*
//6
#ifndef CREATE_H
#define CREATE_H
class CreateAndDestroy
{
public:
    CreateAndDestroy(int);
    ~CreateAndDestroy();

private:
    int data;
};
#endif

#include <iostream>
using std::cout;
using std::endl;
// #include "create.h"
CreateAndDestroy::CreateAndDestroy(int value)
{
    data = value;
    cout << "object " << data << " constructor";
}
CreateAndDestroy::~CreateAndDestroy()
{
    cout << "object " << data << " destructor" << endl;
}

void create(void);
CreateAndDestroy firts(1);
int main()
{
    cout << " (global created before main)" << endl;
    CreateAndDestroy second(2);
    cout << " (local automatic in main)" << endl;
    static CreateAndDestroy third(3);
    cout << " (local static in main)" << endl;
    create();
    CreateAndDestroy fourth(4);
    cout << " (local automatin in main)" << endl;
    return 0;
}

void create(void)
{
    CreateAndDestroy fifth(5);
    cout << "   (local automatic in create)" << endl;
    static CreateAndDestroy sixth(6);
    cout << "   (local static in create)" << endl;
    CreateAndDestroy seventh(7);
    cout << "   (local automatic in create)" << endl;
}*/

/*
//5
#ifndef CREATE_H
#define CREATE_H
class CreateAndDestroy
{
public:
    CreateAndDestroy(int);
    ~CreateAndDestroy();

private:
    int date;
};
#endif
#include <iostream>
using std::cout;
using std::endl;
CreateAndDestroy::CreateAndDestroy(int value)
{
    date = value;
    cout << "object " << date << " constructor";
}
CreateAndDestroy::~CreateAndDestroy()
{
    cout << "object " << date << " destructor" << endl;
}
void create(void);
CreateAndDestroy firts(1);
int main()
{
    cout << " (global created before main)" << endl;
    CreateAndDestroy second(2);
    cout << " (local automatic in main)" << endl;
    static CreateAndDestroy third(3);
    cout << " (local static in main)" << endl;
    create();
    CreateAndDestroy fourth(4);
    cout << " (local automatin in main)" << endl;
    return 0;
}*/

/*
// 4
#ifndef TIME1_H
#define TIME1_H

class Time
{
public:
    Time();
    void setTime(int, int, int);
    void printMilitary();
    void printStandard();
    int getMinute() const; // Getter for minute

private:
    int hour;
    int minute;
    int second;
};
#endif

#include <iostream>
using std::cout;
// #include "time1.h"
Time::Time() { hour = minute = second = 0; }
void Time::setTime(int h, int m, int s)
{
    hour = (h >= 0 && h < 24) ? h : 0;
    minute = (m >= 0 && m < 60) ? m : 0;
    second = (s >= 0 && s < 60) ? s : 0;
}
void Time::printMilitary()
{
    cout << (hour < 10 ? "0" : "") << hour << ":"
         << (minute < 10 ? "0" : "") << minute;
}

void Time::printStandard()
{
    cout << ((hour == 0 || hour == 12) ? 12 : hour % 12)
         << ":" << (minute < 10 ? "0" : "") << minute
         << ":" << (second < 10 ? "0" : "") << second
         << (hour < 12 ? " AM" : " PM");
}

int Time::getMinute() const
{
    return minute;
}
int main()
{
    Time t;
    t.setTime(13, 27, 6);
    cout << "Military time: ";
    t.printMilitary();
    cout << "\nStandard time: ";
    t.printStandard();
    cout << "\nminute = " << t.getMinute();
    return 0;
}*/
/*
// 3
#include <iostream>
using std::cout;
using std::endl;
class Count
{
public:
    int x;
    void print() { cout << x << endl; }
};
int main()
{
    Count counter, *counterPtr = &counter,
                   &counterRef = counter;
    cout << "Assign 7 to x and print using the object name:";
    counter.x = 7;
    counter.print();
    cout << "Assign 8 to x and print using the reference:";
    counterRef.x = 8;
    counterRef.print();
    cout << "Assign 9 to x and print using the pointer:";
    counterPtr->x = 10;
    counterPtr->print();
    return 0;
}*/
/*
// 2
#include <iostream>
using std::cout;
using std::endl;
class Time
{
public:
    Time();
    void setTime(int, int, int);
    void printMilitary() const;
    void printStandard() const;

private:
    int hour;
    int minute;
    int second;
};
Time::Time() { hour = minute = second = 0; }
void Time::setTime(int h, int m, int s)
{
    hour = (h >= 0 && h < 24) ? h : 0;
    minute = (m >= 0 && m < 60) ? m : 0;
    second = (s >= 0 && s < 60) ? s : 0;
}
void Time::printMilitary() const
{
    cout << (hour < 10 ? "0" : "") << hour << ":"
         << (minute < 10 ? "0" : "") << minute;
}
void Time::printStandard() const
{
    cout << ((hour == 0 || hour == 12) ? 12 : hour % 12)
         << ":" << (minute < 10 ? "0" : "") << minute
         << ":" << (second < 10 ? "0" : "") << second
         << (hour < 12 ? " AM" : " PM");
}
int main()
{
    Time t;
    cout << "The initial military time is ";
    t.printMilitary();
    cout << "\nThe initial standard time is ";
    t.printStandard();

    t.setTime(13, 27, 6);
    cout << "\n\nMilitary time after setTime is ";
    t.printMilitary();
    cout << "\nStandard time after setTime is ";
    t.printStandard();

    t.setTime(99, 99, 99);
    cout << "\n\nAfter attempting invalid settings:"
         << "\nMilitary time: ";
    t.printMilitary();
    cout << "\nStandard time: ";
    t.printStandard();
    return 0;
}*/

/*
// 1
#include <iostream>
using std::cout;
using std::endl;
struct Time
{
    int hour, minute, second;
};
void printMilitary(const Time &);
void printStandard(const Time &);
int main()
{
    Time dinnerTime;
    dinnerTime.hour = 18;
    dinnerTime.minute = 30;
    dinnerTime.second = 0;
    cout << "Dinner will be held at";
    printMilitary(dinnerTime);
    cout << " military time,\nwhich is ";
    printStandard(dinnerTime);
    cout << "standard time.\n";
    dinnerTime.hour = 29;
    dinnerTime.minute = 73;
    cout << "\nTime with invalid values: ";
    printMilitary(dinnerTime);
    cout << endl;
    return 0;
}
void printMilitary(const Time &t)
{
    cout << (t.hour < 10 ? "0" : "") << t.hour << ":"
         << (t.minute < 10 ? "0" : "") << t.minute;
}
void printStandard(const Time &t)
{
    cout << ((t.hour == 0 || t.hour == 12) ? 12 : t.hour % 12)
         << ":" << (t.minute < 10 ? "0" : "") << t.minute
         << ":" << (t.second < 10 ? "0" : "") << t.second
         << (t.hour < 12 ? " AM" : " PM");
}*/