#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define big_int long long int
#define MAX_NUM 5000

big_int dot_product(big_int* vec1, big_int* vec2, int length){
    big_int result = 0;
    for(int i = 0; i<length; i++){
        result += vec1[i] * vec2[i];
    }
    return result;
}


// we assume that A is rowwise, and B is column wise
void m_multiply(big_int** A, big_int** B, big_int** C, int m, int k, int n){
    for(int i = 0; i<m; i++){
        for(int j = 0; j<n; j++){
            C[i][j] += dot_product(A[i], B[j], k);
        }
    }
}

int main(){
    int m = 1500;
    int k = 1000;
    int n = 1500;

    big_int** A = (big_int**)malloc(sizeof(big_int*) * m);
    big_int** B = (big_int**)malloc(sizeof(big_int*) * n);
    big_int** C = (big_int**)malloc(sizeof(big_int*) * m);

    for(int i = 0; i<m; i++){
        A[i] = (big_int*) malloc(sizeof(big_int) * k);
        for(int j = 0; j <k; j++){
            A[i][j] = rand() % MAX_NUM;
        }
    }

    for(int i = 0; i<n; i++){
        B[i] = (big_int*) malloc(sizeof(big_int) * k);
        for(int j = 0; j <k; j++){
            B[i][j] = rand() % MAX_NUM;
        }
    }

    for(int i = 0; i<m; i++){
        C[i] = (big_int*)malloc(sizeof(big_int)*n);
    }

    clock_t start = clock();
    m_multiply(A, B, C, m, k, n);
    clock_t end = clock();

    for(int i = 0; i<m;i++){
        free(A[i]);
        free(C[i]);
    }

    for(int i = 0; i<n;i++){
        free(B[i]);
    }

    printf("Execution time: %ld\n", (end - start)/CLOCKS_PER_SEC);
    return 0;
}
