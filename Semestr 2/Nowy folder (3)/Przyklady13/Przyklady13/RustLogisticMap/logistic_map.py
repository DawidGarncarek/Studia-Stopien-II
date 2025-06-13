import ctypes
import numpy as np
import matplotlib.pyplot as plt

# Załaduj bibliotekę DLL
lib = ctypes.CDLL('./target/release/logistic_map.dll')  # Zmień na .so/.dylib na Linux/macOS

# Zdefiniuj funkcję z biblioteki
lib.logistic_map_bifurcation.argtypes = [
    ctypes.c_double, ctypes.c_double, ctypes.c_size_t,  # r_start, r_end, r_steps
    ctypes.c_double, ctypes.c_size_t, ctypes.c_size_t,  # x0, iterations, last_points
    ctypes.POINTER(ctypes.c_double),                   # output
]
lib.logistic_map_bifurcation.restype = None

def calculate_bifurcation(r_start, r_end, r_steps, x0, iterations, last_points):
    total_points = r_steps * last_points
    results = (ctypes.c_double * (total_points * 2))()  # Alokacja pamięci na r i x
    lib.logistic_map_bifurcation(r_start, r_end, r_steps, x0, iterations, last_points, results)
    return np.array(results).reshape(-1, 2)

# Parametry bifurkacji
r_start = 2.5
r_end = 4.0
r_steps = 100000
x0 = 0.5
iterations = 1000
last_points = 100

# Oblicz bifurkacje
data = calculate_bifurcation(r_start, r_end, r_steps, x0, iterations, last_points)

# Wizualizacja
plt.figure(figsize=(10, 6))
plt.plot(data[:, 0], data[:, 1], ',k', alpha=0.25, markersize=0.5)
plt.title('Wykres bifurkacji mapy logistycznej')
plt.xlabel('r')
plt.ylabel('x')
plt.show()
print(np.shape(data))