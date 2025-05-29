#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

double f(double x, double A, double B, double C, double D) {
    return A * x * x * x + B * x * x + C * x + D;
}

double integrate_sequential(double x1, double x2, int n, int method, double A, double B, double C, double D) {
    double h = (x2 - x1) / n;
    double sum = 0.0;
    int i;

    switch (method) {
    case 1: // Prostokąty 
        for (i = 0; i < n; i++) {
            sum += f(x1 + i * h, A, B, C, D);
        }
        return sum * h;

    case 2: // Trapezy
        sum += (f(x1, A, B, C, D) + f(x2, A, B, C, D)) / 2.0;
        for (i = 1; i < n; i++) {
            sum += f(x1 + i * h, A, B, C, D);
        }
        return sum * h;

    case 3: // Simpsona
        if (n % 2 != 0) n++; 
        sum = f(x1, A, B, C, D) + f(x2, A, B, C, D);
        for (i = 1; i < n; i++) {
            double x = x1 + i * h;
            sum += f(x, A, B, C, D) * (i % 2 == 0 ? 2 : 4);
        }
        return sum * h / 3.0;

    default:
        printf("Nieznana metoda.\n");
        return 0.0;
    }
}

double integrate_parallel(double x1, double x2, int n, int method, double A, double B, double C, double D, int threads) {
    double h = (x2 - x1) / n;
    double sum = 0.0;
    int i;

    omp_set_num_threads(threads);

    switch (method) {
    case 1: // Prostokąty
#pragma omp parallel for reduction(+:sum)
        for (i = 0; i < n; i++) {
            sum += f(x1 + i * h, A, B, C, D);
        }
        return sum * h;

    case 2: // Trapezy
        sum = (f(x1, A, B, C, D) + f(x2, A, B, C, D)) / 2.0;
#pragma omp parallel for reduction(+:sum)
        for (i = 1; i < n; i++) {
            sum += f(x1 + i * h, A, B, C, D);
        }
        return sum * h;

    case 3: // Simpsona
        if (n % 2 != 0) n++;
        sum = f(x1, A, B, C, D) + f(x2, A, B, C, D);
#pragma omp parallel for reduction(+:sum)
        for (i = 1; i < n; i++) {
            double x = x1 + i * h;
            sum += f(x, A, B, C, D) * (i % 2 == 0 ? 2 : 4);
        }
        return sum * h / 3.0;

    default:
        printf("Nieznana metoda.\n");
        return 0.0;
    }
}

int main() {
    double A, B, C, D, x1, x2;
    int n, method, threads;

    printf("Podaj wspolczynniki A, B, C, D: ");
    if (scanf("%lf %lf %lf %lf", &A, &B, &C, &D) != 4) {
        fprintf(stderr, "Blad: Nieprawidlowe dane dla A, B, C, D.\n");
        return 1;
    }

    printf("Podaj granice calkowania x1 i x2: ");
    if (scanf("%lf %lf", &x1, &x2) != 2) {
        fprintf(stderr, "Blad: Nieprawidlowe granice calkowania.\n");
        return 1;
    }

    printf("Podaj liczbe przedzialow n: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        fprintf(stderr, "Blad: Liczba przedzialow musi byc dodatnia.\n");
        return 1;
    }

    printf("Podaj liczbe watkow p: ");
    if (scanf("%d", &threads) != 1 || threads <= 0) {
        fprintf(stderr, "Blad: Liczba wat0kow musi byc dodatnia.\n");
        return 1;
    }

    printf("Wybierz metode calkowania (1 - prostokaty, 2 - trapezy, 3 - Simpsona): ");
    if (scanf("%d", &method) != 1 || method < 1 || method > 3) {
        fprintf(stderr, "Blad: Nieprawidlowa metoda (1-3).\n");
        return 1;
    }

    // Sekwencyjne
    double start = omp_get_wtime();
    double result_seq = integrate_sequential(x1, x2, n, method, A, B, C, D);
    double end = omp_get_wtime();
    double Ts = end - start;

    // Równoległe
    start = omp_get_wtime();
    double result_par = integrate_parallel(x1, x2, n, method, A, B, C, D, threads);
    end = omp_get_wtime();
    double Tp = end - start;

    printf("\nWynik calkowania (sekwencyjnie): %.10lf\n", result_seq);
    printf("Wynik calkowania (rownolegle):   %.10lf\n", result_par);
    printf("Czas Ts (sekwencyjnie): %.6lf s\n", Ts);
    printf("Czas Tp (rownolegle):   %.6lf s\n", Tp);
    printf("Przyspieszenie (Ts/Tp): %.2lf\n", Ts / Tp);

    return 0;
}
