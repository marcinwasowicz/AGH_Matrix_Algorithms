#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define MAX_NUM 2.0
#define EPSILON 1e-15
#define MATRIX_SIZE 100
#define DO_PIVOTING 1

double abs_float(double f){
    if(f >= -EPSILON){
        return f;
    }
    return -1.0 * f;
}

int get_pivot_idx(double* column, int start, int n){

    int result = start;
    double curr_max = abs_float(column[start]);
    for(int i = start; i<n; i++){
        if(abs_float(column[i]) > curr_max){
            result = i;
            curr_max = abs_float(column[i]);
        }
    }
    return result;
}

void pivoting(double** matrix, int n){
    for(int k = 0; k<n; k++){
        int pivot_idx = get_pivot_idx(matrix[k], k, n);
        if(abs_float(matrix[k][pivot_idx]) <= EPSILON){
            printf("singular matrix\n");
            exit(-1);
        }
        if(pivot_idx != k){
            for(int i = k; i<n; i++){
                double temp = matrix[i][k];
                matrix[i][k] = matrix[i][pivot_idx];
                matrix[i][pivot_idx] = temp;
            }
        }
    }
}

void divide_column(double* column, int start, int n, double divisor){
    for(int i = start; i<n; i++){
        column[i] /= divisor;
    }
}

void subtract_columns(double * col1, double* col2, int start, int n, double factor){
    for(int i = start; i<n; i++){
        col1[i] -= col2[i] * factor;
    }
}

void column_wise_gauss_elimination(double** matrix, int n){
    for(int k = 0; k < n - 1; k++){
        divide_column(matrix[k], k + 1, n, matrix[k][k]);
        for(int j = k + 1; j<n; j++){
            subtract_columns(matrix[j], matrix[k], k + 1, n, matrix[j][k]);
        }
    }
}

void print_matrix(double** matrix, int n){
    for(int i = 0; i<n ; i++){
        for(int j = 0; j<n; j++){
            printf("%lf ", matrix[j][i]);
        }
        printf("\n");
    }
}

int main() {
    int n = MATRIX_SIZE;

    double **matrix = (double **) malloc(n * sizeof(double *));

    for (int i = 0; i < n; i++) {
        matrix[i] = (double *) malloc(n * sizeof(double));
        for (int j = 0; j < n; j++) {
            matrix[i][j] = (double) rand() * MAX_NUM / (double) RAND_MAX;
        }
    }

    print_matrix(matrix, n);

    if (DO_PIVOTING) {
        clock_t pivoting_start = clock();
        pivoting(matrix, n);
        clock_t pivoting_end = clock();
        printf("Pivoting took %ld milliseconds\n", (pivoting_end - pivoting_start) * 1000 / CLOCKS_PER_SEC);
    }

    clock_t gauss_start = clock();
    column_wise_gauss_elimination(matrix, n);
    clock_t  gauss_end = clock();

    printf("Column wise gauss elimination took %ld milliseconds\n", (gauss_end - gauss_start)*1000/CLOCKS_PER_SEC);

    print_matrix(matrix, n);

    return 0;
}

