#include <stdio.h>
#include <stdlib.h>

#define PRINTLN printf("\n");

typedef struct {
    int columns;
    int rows;
    int nnz;

    int* values;
    int* column_index;
    int* row_index;
}csr_matrix;

typedef struct{
    int columns;
    int rows;
    int nnz;

    int* row_index;
    int* column_index;
    int* values;
}coo_matrix;

csr_matrix* allocate_csr_matrix(int columns, int rows, int nnz){
    csr_matrix* matrix = (csr_matrix*) malloc(sizeof(csr_matrix));
    matrix->columns = columns;
    matrix->rows = rows;
    matrix->nnz = nnz;

    matrix->values = (int*) malloc(nnz * sizeof(int));
    matrix->column_index = (int*) malloc(nnz * sizeof(int));
    matrix->row_index = (int*) malloc((rows + 1) * sizeof(int));

    return matrix;
}

coo_matrix* allocate_coo_matrix(int columns, int rows, int nnz){
    coo_matrix* matrix = (coo_matrix*) malloc(sizeof(coo_matrix));
    matrix->columns = columns;
    matrix->rows = rows;
    matrix->nnz = nnz;

    matrix->values = (int*) malloc(nnz * sizeof(int));
    matrix->column_index = (int*) malloc(nnz * sizeof(int));
    matrix->row_index = (int*) malloc(nnz * sizeof(int));

    return matrix;
}

csr_matrix* csr_from_standard(int columns, int rows, int nnz, int** input){
    csr_matrix* output = allocate_csr_matrix(columns, rows, nnz);
    int nnz_counter = 0;

    for(int i = 0; i<rows; i++){
        output->row_index[i] = nnz_counter;
        for(int j = 0; j<columns; j++){
            if(input[i][j] == 0){
                continue;
            }

            output->values[nnz_counter] = input[i][j];
            output->column_index[nnz_counter] = j;
            nnz_counter++;
        }
    }

    output->row_index[rows] = nnz;
    return output;
}

coo_matrix* coo_from_csr(csr_matrix* input){
    coo_matrix* output = allocate_coo_matrix(input->columns, input->rows, input->nnz);
    int nnz_counter = 0;
    for(int i = 0; i<input->rows; i++){
        int row_start = input->row_index[i];
        int row_end = input->row_index[i + 1];
        for(int j = row_start; j<row_end; j++){
            output->values[nnz_counter] = input->values[j];
            output->column_index[nnz_counter] = input->column_index[j];
            output->row_index[nnz_counter] = i;
            nnz_counter++;
        }
    }
    return output;
}

void deallocate_coo(coo_matrix* matrix){
    free(matrix->values);
    free(matrix->column_index);
    free(matrix->row_index);
    free(matrix);
}

void deallocate_csr(csr_matrix* matrix){
    free(matrix->values);
    free(matrix->column_index);
    free(matrix->row_index);
    free(matrix);
}

void print_csr_matrix(csr_matrix* matrix){
    printf("%d %d %d\n", matrix->columns, matrix->rows, matrix->nnz);
    for(int i = 0; i<matrix->nnz; i++){
        printf("%d ", matrix->values[i]);
    }
    printf("\n");
    for(int i = 0; i<matrix->nnz; i++){
        printf("%d ", matrix->column_index[i]);
    }
    printf("\n");
    for(int i = 0; i<matrix->rows + 1; i++){
        printf("%d ", matrix->row_index[i]);
    }
    printf("\n");
}

void print_coo_matrix(coo_matrix* matrix){
    printf("%d %d %d\n", matrix->columns, matrix->rows, matrix->nnz);
    for(int i = 0; i<matrix->nnz; i++){
        printf("%d ", matrix->values[i]);
    }
    printf("\n");
    for(int i = 0; i<matrix->nnz; i++){
        printf("%d ", matrix->column_index[i]);
    }
    printf("\n");
    for(int i = 0; i<matrix->nnz; i++){
        printf("%d ", matrix->row_index[i]);
    }
    printf("\n");
}

int** read_standard_matrix(int* rows, int* columns, int* nnz){
    scanf("%d", rows);
    scanf("%d", columns);
    *nnz = 0;

    int** standard_matrix = (int**)malloc(sizeof(int*)**rows);
    for(int i = 0; i<*rows; i++){
        standard_matrix[i] = (int*)malloc(sizeof(int)**columns);
        for(int j = 0; j<*columns; j++){
            scanf("%d", &standard_matrix[i][j]);
            if(standard_matrix[i][j] != 0){
                (*nnz)++;
            }
        }
    }
    return standard_matrix;
}

void deallocate_standard_matrix(int** matrix, int rows){
    for(int i = 0; i<rows; i++){
        free(matrix[i]);
    }
    free(matrix);
}


int main(){
    int rows;
    int columns;
    int nnz;

    int** standard_matrix = read_standard_matrix(&rows, &columns, &nnz);

    csr_matrix* csr = csr_from_standard(columns, rows, nnz, standard_matrix);
    coo_matrix* coo = coo_from_csr(csr);

    print_csr_matrix(csr);
    PRINTLN
    print_coo_matrix(coo);

    deallocate_coo(coo);
    deallocate_csr(csr);
    deallocate_standard_matrix(standard_matrix, rows);

    return 0;
}



