#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

double* read_matrix_csv(const char* filename, int* rows, int* cols) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Blad otwarcia pliku: %s\n", filename);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    fscanf(file, "%d", rows);
    fscanf(file, "%d", cols);

    double* data = (double*)malloc((*rows) * (*cols) * sizeof(double));
    for (int i = 0; i < (*rows); i++) {
        for (int j = 0; j < (*cols); j++) {
            if (fscanf(file, "%lf;", &data[i * (*cols) + j]) != 1) {
                printf("Blad odczytu danych w (%d,%d)\n", i, j);
                MPI_Abort(MPI_COMM_WORLD, 1);
            }
        }
    }
    fclose(file);
    return data;
}

void save_matrix_csv(const char* filename, double* C, int m, int p, double T1, double Tp) {
    char outname[128];
    sprintf(outname, "%s_%.4lf_%.4lf.csv", filename, T1, Tp);
    FILE* file = fopen(outname, "w");
    if (!file) {
        printf("Nie mozna zapisac pliku wynikowego\n");
        return;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            fprintf(file, "%.4lf", C[i * p + j]);
            if (j < p - 1) fprintf(file, ";");
        }
        fprintf(file, "\n");
    }
    fclose(file);
}

// Prosta funkcja do mno¿enia macierzy sekwencyjnie, jeden proces (tylko dla rank 0)
void multiply_sequential(double* A, double* B, double* C, int m, int n, int p) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            for (int k = 0; k < n; k++) {
                C[i * p + j] += A[i * n + k] * B[k * p + j];
            }
        }
    }
}

int main(int argc, char** argv) {
    int rank, size;
    int m, n, p; // rozmiary: A[m][n], B[n][p], C[m][p]
    double* A = NULL, * B = NULL, * C = NULL;
    double* local_A, * local_C;
    double T1 = 0, Tp = 0;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        A = read_matrix_csv("A.csv", &m, &n);
        B = read_matrix_csv("B.csv", &n, &p);

        double* C_seq = (double*)calloc(m * p, sizeof(double));
        double start_seq = MPI_Wtime();
        multiply_sequential(A, B, C_seq, m, n, p);
        double end_seq = MPI_Wtime();
        T1 = end_seq - start_seq;
        free(C_seq);

        C = (double*)calloc(m * p, sizeof(double));
    }

    MPI_Bcast(&m, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&p, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (m % size != 0) {
        if (rank == 0) printf("Liczba wierszy A (%d) musi byæ podzielna przez liczbê procesów (%d)\n", m, size);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int local_rows = m / size;
    local_A = (double*)malloc(local_rows * n * sizeof(double));
    local_C = (double*)calloc(local_rows * p, sizeof(double));

    if (rank != 0) B = (double*)malloc(n * p * sizeof(double));

    MPI_Scatter(A, local_rows * n, MPI_DOUBLE, local_A, local_rows * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B, n * p, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    double start = MPI_Wtime();

    for (int i = 0; i < local_rows; i++) {
        for (int j = 0; j < p; j++) {
            for (int k = 0; k < n; k++) {
                local_C[i * p + j] += local_A[i * n + k] * B[k * p + j];
            }
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double end = MPI_Wtime();
    if (rank == 0) Tp = end - start;

    MPI_Gather(local_C, local_rows * p, MPI_DOUBLE, C, local_rows * p, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        save_matrix_csv("C", C, m, p, T1, Tp);
        printf("Wynik zapisany do pliku C_T1_Tp.csv\n");
        printf("Czas wykonania sekwencyjnie (jeden proces T1): %.6lf s\n", T1);
        printf("Czas wykonania rownolegle (Tp):   %.6lf s\n", Tp);
        printf("Przyspieszenie T1/Tp: %.2lf\n", T1 / Tp);
        free(A); free(B); free(C);
    }
    else {
        free(B);
    }
    free(local_A); free(local_C);

    MPI_Finalize();
    return 0;
}
