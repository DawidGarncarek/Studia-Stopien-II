#include "pch.h"

extern "C" {
    __declspec(dllexport) int Dodawanie(int a, int b) {
        return a + b;
    }
    
}
