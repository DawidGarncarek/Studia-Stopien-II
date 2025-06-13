
# Przykłady użycia Numba

from numba import njit, prange


# Obliczenia równoległe na CPU
@njit(parallel=True)
def parallel_sum(n):
    total = 0
    for i in prange(n):
        total += i ** 2
    return total

print("Parallel sum of squares:", parallel_sum(10**6))

