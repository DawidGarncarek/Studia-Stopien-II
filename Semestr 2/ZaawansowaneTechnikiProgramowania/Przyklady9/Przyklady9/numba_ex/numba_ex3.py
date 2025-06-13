
# Przykłady użycia Numba

from numba import cuda
import numpy as np


# Obliczenia na GPU
@cuda.jit
def multiply_arrays_gpu(a, b, result):
    idx = cuda.grid(1)
    if idx < a.size:
        result[idx] = a[idx] * b[idx]

# Dane
a = np.random.rand(10**6)
b = np.random.rand(10**6)
result_gpu = np.zeros_like(a)

# Przenoszenie danych na GPU i uruchamianie obliczeń
threads_per_block = 256
blocks_per_grid = (a.size + threads_per_block - 1) // threads_per_block
multiply_arrays_gpu[blocks_per_grid, threads_per_block](a, b, result_gpu)
print("First 5 results from GPU array multiplication:", result_gpu[:5])
