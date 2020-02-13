#include"calculation.h"

double calculate(double n1, char op, double n2)
{
    switch (op)
    {
    case '+':
        return n1+n2;
        break;
    case '-':
        return n1-n2;
        break;
    case '*':
        return n1*n2;
        break;
    case '/':
        return n1/n2;
        break;
    default:
        return 0;
        break;
    }
}