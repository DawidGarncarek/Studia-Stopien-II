import numpy as np
import matplotlib.pyplot as plt
import time
from numba import njit, prange
import multiprocessing

# Parametry zbioru Mandelbrota
WIDTH = 1000
HEIGHT = 1000
MAX_ITER = 300

# Czysty Python
def mandelbrot_python(xmin, xmax, ymin, ymax, width, height, max_iter):
    image = np.zeros((height, width))
    for ix in range(width):
        for iy in range(height):
            x = xmin + ix * (xmax - xmin) / (width - 1)
            y = ymin + iy * (ymax - ymin) / (height - 1)
            c = complex(x, y)
            z = 0
            for i in range(max_iter):
                z = z*z + c
                if abs(z) > 2:
                    image[iy, ix] = i
                    break
    return image

# Wieloprocesowość
def mandelbrot_worker(args):
    xmin, xmax, ymin, ymax, width, height, max_iter, ix = args
    row = np.zeros(height)
    for iy in range(height):
        x = xmin + ix * (xmax - xmin) / (width - 1)
        y = ymin + iy * (ymax - ymin) / (height - 1)
        c = complex(x, y)
        z = 0
        for i in range(max_iter):
            z = z*z + c
            if abs(z) > 2:
                row[iy] = i
                break
    return row

def mandelbrot_multiprocessing(xmin, xmax, ymin, ymax, width, height, max_iter):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    rows = pool.map(mandelbrot_worker, [(xmin, xmax, ymin, ymax, width, height, max_iter, ix) for ix in range(width)])
    pool.close()
    pool.join()
    return np.array(rows).T

# Numba z równoległością
@njit(parallel=True)
def mandelbrot_numba_parallel(xmin, xmax, ymin, ymax, width, height, max_iter):
    image = np.zeros((height, width))
    for ix in prange(width):
        for iy in range(height):
            x = xmin + ix * (xmax - xmin) / (width - 1)
            y = ymin + iy * (ymax - ymin) / (height - 1)
            c = complex(x, y)
            z = 0
            for i in range(max_iter):
                z = z*z + c
                if abs(z) > 2:
                    image[iy, ix] = i
                    break
    return image

# Główna funkcja porównawcza
if __name__ == "__main__":
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5

    # Czysty Python
    start_time = time.time()
    image_python = mandelbrot_python(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, MAX_ITER)
    time_python = time.time() - start_time
    print(f"Czas wykonania (Python): {time_python:.4f} s")

    # Wieloprocesowość
    start_time = time.time()
    image_multiprocessing = mandelbrot_multiprocessing(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, MAX_ITER)
    time_multiprocessing = time.time() - start_time
    print(f"Czas wykonania (Multiprocessing): {time_multiprocessing:.4f} s")

    # Numba z równoległością
    start_time = time.time()
    image_numba_parallel = mandelbrot_numba_parallel(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, MAX_ITER)
    time_numba_parallel = time.time() - start_time
    print(f"Czas wykonania (Numba równoległe): {time_numba_parallel:.4f} s")

    # Wizualizacja wyników
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(image_python, cmap='hot', extent=[xmin, xmax, ymin, ymax])
    plt.title('Python')
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.imshow(image_multiprocessing, cmap='hot', extent=[xmin, xmax, ymin, ymax])
    plt.title('Multiprocessing')
    plt.colorbar()

    plt.subplot(1, 3, 3)
    plt.imshow(image_numba_parallel, cmap='hot', extent=[xmin, xmax, ymin, ymax])
    plt.title('Numba Parallel')
    plt.colorbar()

    plt.tight_layout()
    plt.show()

    # Porównanie czasów
    print(f"Czas wykonania:")
    print(f"Czysty Python: {time_python:.4f} s")
    print(f"Wieloprocesowość: {time_multiprocessing:.4f} s")
    print(f"Numba (równoległe): {time_numba_parallel:.4f} s")
