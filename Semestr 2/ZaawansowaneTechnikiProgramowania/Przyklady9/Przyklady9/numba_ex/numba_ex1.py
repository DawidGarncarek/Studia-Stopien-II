
# Przykłady użycia Numba

from numba import jit
import numpy as np


# Przyspieszenie operacji na tablicach NumPy
@jit
def multiply_arrays(a, b):
    result = np.zeros_like(a)
    for i in range(len(a)):
        result[i] = a[i] * b[i]
    return result

# Dane
a = np.random.rand(10**6)
b = np.random.rand(10**6)

# Przyspieszone mnożenie
result = multiply_arrays(a, b)
print("First 5 results from array multiplication:", result[:5])

