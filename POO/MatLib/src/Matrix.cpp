#ifndef MATRIX_H
#define MATRIX_H
#include <vector>
#include <stdexcept>
class Matrix
{
private:
    std::vector<std::vector<double>> data;
    int rows, cols;

public:
    Matrix(int r, int c);
    double get(int r, int c) const;
    void set(int r, int c, double value);
    Matrix add(const Matrix &other) const;
    Matrix multiply(const Matrix &other) const;
    void print() const;
};
#endif
#include <iostream>
Matrix::Matrix(int r, int c) : rows(r), cols(c)
{
    data.resize(rows, std::vector<double>(cols, 0.0));
}
double Matrix::get(int r, int c) const
{
    if (r >= rows || c >= cols)
        throw std::out_of_range("Índice fuera de rango");
    return data[r][c];
}
void Matrix::set(int r, int c, double value)
{
    if (r >= rows || c >= cols)
        throw std::out_of_range("Índice fuera de rango");
    data[r][c] = value;
}
Matrix Matrix::add(const Matrix &other) const
{
    if (rows != other.rows || cols != other.cols)
        throw std::invalid_argument("Las matrices deben tener el mismo tamaño");
    Matrix result(rows, cols);
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            result.set(i, j, get(i, j) + other.get(i, j));
    return result;
}
Matrix Matrix::multiply(const Matrix &other) const
{
    if (cols != other.rows)
        throw std::invalid_argument("Dimensiones incompatibles para multiplicación");
    Matrix result(rows, other.cols);
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < other.cols; ++j)
            for (int k = 0; k < cols; ++k)
                result.set(i, j, result.get(i, j) + get(i, k) * other.get(k, j));
    return result;
}
void Matrix::print() const
{
    for (const auto &row : data)
    {
        for (double val : row)
            std::cout << val << " ";
        std::cout << "\n";
    }
}
int main()
{
    Matrix A(2, 2), B(2, 2);
    A.set(0, 0, 1);
    A.set(0, 1, 2);
    A.set(1, 0, 3);
    A.set(1, 1, 4);
    B.set(0, 0, 5);
    B.set(0, 1, 6);
    B.set(1, 0, 7);
    B.set(1, 1, 8);
    Matrix C = A.add(B);
    Matrix D = A.multiply(B);
    std::cout << "Suma:\n";
    C.print();
    std::cout << "Multiplicación:\n";
    D.print();
    return 0;
}