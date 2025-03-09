#include <stdio.h>
#include <omp.h>
#include <iostream>

int main()
{
    double start = omp_get_wtime();

    const int N = 1000;
#pragma omp parallel
    {
        #pragma omp for
        for (int i = 0; i < N; i++)
            obliczenia();
    }

    double stop = omp_get_wtime();
    printf("Czas realizacji zadania: %f", stop-start)
}

void obliczenia()
{

}

