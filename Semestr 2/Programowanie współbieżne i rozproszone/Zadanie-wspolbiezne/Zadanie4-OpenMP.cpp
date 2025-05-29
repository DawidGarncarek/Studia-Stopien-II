#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <time.h>

void sort_row(int* row, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (row[j] > row[j + 1]) {
                int temp = row[j];
                row[j] = row[j + 1];
                row[j + 1] = temp;
            }
        }
    }
}

void write_matrix_csv(const char* filename, int** matrix, int m, int n) {
    FILE* fp = fopen(filename, "w");
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            fprintf(fp, "%d", matrix[i][j]);
            if (j != n - 1) fprintf(fp, ",");
        }
        fprintf(fp, "\n");
    }
    fclose(fp);
}

int** allocate_matrix(int m, int n) {
    int** matrix = (int**)malloc(m * sizeof(int*));
    for (int i = 0; i < m; i++)
        matrix[i] = (int*)malloc(n * sizeof(int));
    return matrix;
}

void free_matrix(int** matrix, int m) {
    for (int i = 0; i < m; i++)
        free(matrix[i]);
    free(matrix);
}

void generate_matrix(int** matrix, int m, int n, int min, int max) {
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            matrix[i][j] = rand() % (max - min + 1) + min;
}

void read_matrix_csv(const char* filename, int*** matrix_out, int* m_out, int* n_out) {
    FILE* fp = fopen(filename, "r");
    char line[4096];
    int m = 0, n = 0;

    while (fgets(line, sizeof(line), fp)) {
        if (m == 0) {
            char* tok = strtok(line, ",");
            while (tok) {
                n++;
                tok = strtok(NULL, ",");
            }
        }
        m++;
    }

    rewind(fp);
    int** matrix = allocate_matrix(m, n);
    for (int i = 0; i < m; i++) {
        fgets(line, sizeof(line), fp);
        char* tok = strtok(line, ",");
        for (int j = 0; j < n; j++) {
            matrix[i][j] = atoi(tok);
            tok = strtok(NULL, ",");
        }
    }

    fclose(fp);
    *matrix_out = matrix;
    *m_out = m;
    *n_out = n;
}

int main(int argc, char* argv[]) {
    int m, n, min, max, P;

    if (argc == 7) {
        // Tryb A: generowanie macierzy
        m = atoi(argv[1]);
        n = atoi(argv[2]);
        min = atoi(argv[3]);
        max = atoi(argv[4]);
        const char* output_file = argv[5];
        P = atoi(argv[6]);

        srand(time(NULL));

        int** matrix = allocate_matrix(m, n);
        generate_matrix(matrix, m, n, min, max);

        int** matrix_copy = allocate_matrix(m, n);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                matrix_copy[i][j] = matrix[i][j];

        // Sekwencyjnie (T_S)
        omp_set_num_threads(1);
        double start_seq = omp_get_wtime();
        for (int i = 0; i < m; i++) {
            sort_row(matrix[i], n);
        }
        double end_seq = omp_get_wtime();
        printf("Czas sekwencyjny: %.6f s\n", end_seq - start_seq);

        // Równolegle (T_P)
        omp_set_num_threads(P);
        double start_par = omp_get_wtime();
#pragma omp parallel for
        for (int i = 0; i < m; i++) {
            sort_row(matrix_copy[i], n);
        }
        double end_par = omp_get_wtime();
        printf("Czas równoległy (%d wątków): %.6f s\n", P, end_par - start_par);

        write_matrix_csv(output_file, matrix_copy, m, n);
        free_matrix(matrix, m);
        free_matrix(matrix_copy, m);
    }

    else if (argc == 4) {
        // Tryb B: wczytanie z pliku CSV
        const char* input_file = argv[1];
        const char* output_file = argv[2];
        P = atoi(argv[3]);

        int** matrix;
        read_matrix_csv(input_file, &matrix, &m, &n);

        // Kopia macierzy
        int** matrix_copy = allocate_matrix(m, n);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                matrix_copy[i][j] = matrix[i][j];

        // Sekwencyjnie
        omp_set_num_threads(1);
        double start_seq = omp_get_wtime();
        for (int i = 0; i < m; i++) {
            sort_row(matrix[i], n);
        }
        double end_seq = omp_get_wtime();
        printf("Czas sekwencyjny: %.6f s\n", end_seq - start_seq);

        // Równolegle
        omp_set_num_threads(P);
        double start_par = omp_get_wtime();
#pragma omp parallel for
        for (int i = 0; i < m; i++) {
            sort_row(matrix_copy[i], n);
        }
        double end_par = omp_get_wtime();
        printf("Czas rownolegly (%d watkow): %.6f s\n", P, end_par - start_par);

        write_matrix_csv(output_file, matrix_copy, m, n);
        free_matrix(matrix, m);
        free_matrix(matrix_copy, m);
    }

    else {
        printf("Uzycie:\n");
        printf("  A: %s m n min max output_file P\n", argv[0]);
        printf("  B: %s input_file output_file P\n", argv[0]);
        return 1;
    }

    return 0;
}

