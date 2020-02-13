#include<stdio.h>

#include"calculation.h"

int main()
{
    double number1 = 0.0;
    double number2 = 0.0;
    char operation = 0;
    printf("\nPlease begin calculating\n");
    scanf("%lf%c%lf", &number1, &operation, &number2);
    double result = calculate(number1, operation, number2);
    printf("\nresult:%lf", result);
}