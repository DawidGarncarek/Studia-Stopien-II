// MathFunctions.cpp
#include "pch.h"

extern "C" {
    __declspec(dllexport) double MultiplyDouble(double a, double b) {
        return a * b;
    }

    __declspec(dllexport) int MultiplyInt(int a, int b) {
        return a * b;
    }

    __declspec(dllexport) int SquareInt(int n) {
        
        int result = MultiplyInt(n, n);
        
        return result;
    }

    __declspec(dllexport) int Factorial(int n) {
        if (n == 0 || n == 1)
            return 1;

        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }

        return result;
    }

    __declspec(dllexport) double Euler(int n) {

        double result = 0.0;
        for (int i = 0; i < n; i++) {
            result += 1.0/Factorial(i);
        }

        return result;
    }
}
