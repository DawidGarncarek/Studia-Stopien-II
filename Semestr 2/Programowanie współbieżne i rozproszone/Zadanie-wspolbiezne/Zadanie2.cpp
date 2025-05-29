#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <time.h>
#include <math.h>

#define MAX_FILENAME 256

// Wczytuje macierz rozszerzona z pliku CSV
double** read_matrix_from_csv(const char* filename, int* n) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Blad otwarcia pliku");
        exit(EXIT_FAILURE);
    }

    fscanf(file, "%d", n);
    double** C = (double**)malloc(*n * sizeof(double*));
    for (int i = 0; i < *n; i++) {
        C[i] = (double*)malloc((*n + 1) * sizeof(double));
        for (int j = 0; j < *n + 1; j++) {
            if (j == *n)
                fscanf(file, "%lf", &C[i][j]);
            else
                fscanf(file, "%lf;", &C[i][j]);
        }
    }
    fclose(file);
    return C;
}

// Zapisuje wynikowy wektor X do pliku
void write_result_to_csv(const char* base_filename, double* X, int n, double Ts, double Tp) {
    char filename[MAX_FILENAME];
    sprintf(filename, "X_%.4lf_%.4lf.csv", Ts, Tp);
    FILE* file = fopen(filename, "w");
    if (!file) {
        perror("Blad zapisu pliku");
        exit(EXIT_FAILURE);
    }
    fprintf(file, "%d\n", n);
    for (int i = 0; i < n; i++) {
        fprintf(file, "%.4lf", X[i]);
        if (i < n - 1) fprintf(file, ";");
    }
    fprintf(file, "\n");
    fclose(file);
}

void log_results(int n, int threads, double Ts, double Tp) {
    FILE* file = fopen("datalogger.txt", "a");
    if (!file) {
        perror("Nie moge zapisac logu");
        return;
    }
    fprintf(file, "N=%d, Threads=%d, Ts=%.6lf, Tp=%.6lf\n", n, threads, Ts, Tp);
    fclose(file);
}

// Kopiuje macierz
double** clone_matrix(double** src, int n) {
    double** dst = (double**)malloc(n * sizeof(double*));
    for (int i = 0; i < n; i++) {
        dst[i] = (double*)malloc((n + 1) * sizeof(double));
        for (int j = 0; j <= n; j++) {
            dst[i][j] = src[i][j];
        }
    }
    return dst;
}

void free_matrix(double** matrix, int n) {
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

void swap_rows(double** matrix, int row1, int row2, int cols) {
    for (int j = 0; j < cols; j++) {
        double temp = matrix[row1][j];
        matrix[row1][j] = matrix[row2][j];
        matrix[row2][j] = temp;
    }
}

// Etap I - Eliminacja Gaussa z pivotingiem (sekwencyjnie)
void gauss_sequential(double** C, double* X, int n) {
    for (int r = 0; r < n - 1; r++) {
        int max_row = r;
        for (int i = r + 1; i < n; i++) {
            if (fabs(C[i][r]) > fabs(C[max_row][r])) {
                max_row = i;
            }
        }
        if (max_row != r) swap_rows(C, r, max_row, n + 1);

        for (int i = r + 1; i < n; i++) {
            double factor = C[i][r] / C[r][r];
            for (int j = r; j <= n; j++) {
                C[i][j] -= factor * C[r][j];
            }
        }
    }

    for (int i = n - 1; i >= 0; i--) {
        double sum = C[i][n];
        for (int j = i + 1; j < n; j++) {
            sum -= C[i][j] * X[j];
        }
        X[i] = sum / C[i][i];
    }
}

// Etap I - Eliminacja Gaussa z pivotingiem (równolegle z OpenMP)
void gauss_parallel(double** C, double* X, int n, int threads) {
    omp_set_num_threads(threads);
    for (int r = 0; r < n - 1; r++) {
        int max_row = r;
        for (int i = r + 1; i < n; i++) {
            if (fabs(C[i][r]) > fabs(C[max_row][r])) {
                max_row = i;
            }
        }
        if (max_row != r) swap_rows(C, r, max_row, n + 1);

#pragma omp parallel for
        for (int i = r + 1; i < n; i++) {
            double factor = C[i][r] / C[r][r];
            for (int j = r; j <= n; j++) {
                C[i][j] -= factor * C[r][j];
            }
        }
    }

    for (int i = n - 1; i >= 0; i--) {
        double sum = C[i][n];
        for (int j = i + 1; j < n; j++) {
            sum -= C[i][j] * X[j];
        }
        X[i] = sum / C[i][i];
    }
}

int main() {
    while (1) {
        int n, threads;
        printf("Podaj liczbe watkow: ");
        scanf("%d", &threads);

        double** C_seq = read_matrix_from_csv("C.csv", &n);
        double** C_par = clone_matrix(C_seq, n);

        double* X_seq = (double*)malloc(n * sizeof(double));
        double* X_par = (double*)malloc(n * sizeof(double));

        double start = omp_get_wtime();
        gauss_sequential(C_seq, X_seq, n);
        double Ts = omp_get_wtime() - start;

        start = omp_get_wtime();
        gauss_parallel(C_par, X_par, n, threads);
        double Tp = omp_get_wtime() - start;

        write_result_to_csv("X", X_par, n, Ts, Tp);

        printf("Zapisuje do logu...\n");
        log_results(n, threads, Ts, Tp);
        printf("Zapis zakonczony.\n");

        printf("Sekwencyjnie: %.6lf s\n", Ts);
        printf("Rownolegle:   %.6lf s\n", Tp);
        printf("Przyspieszenie: %.2lf\n", Ts / Tp);

        free_matrix(C_seq, n);
        free_matrix(C_par, n);
        free(X_seq);
        free(X_par);

        char choice;
        printf("Czy chcesz wykonac ponownie? (t/n): ");
        scanf(" %c", &choice);
        if (choice != 't' && choice != 'T') break;
    }

    return 0;
}
