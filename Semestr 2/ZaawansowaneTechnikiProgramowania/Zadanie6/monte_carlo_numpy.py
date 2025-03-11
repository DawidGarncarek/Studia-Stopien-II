import numpy as np
import time

def monte_carlo_integral_numpy(a, b, num_samples):
    """
    Oblicza wartość całki funkcji kwadratowej metodą Monte Carlo z wykorzystaniem numpy.

    :param a: Początek przedziału całkowania.
    :param b: Koniec przedziału całkowania.
    :param num_samples: Liczba losowych punktów.
    :return: Przybliżona wartość całki.
    """
    def quadratic_function(x):
        return x ** 2  # Funkcja kwadratowa f(x) = x^2

    max_f = max(quadratic_function(a), quadratic_function(b))

    x_rand = np.random.uniform(a, b, num_samples)
    y_rand = np.random.uniform(0, max_f, num_samples)

    count_under_curve = np.sum(y_rand <= quadratic_function(x_rand))

    integral_value = (count_under_curve / num_samples) * ((b - a) * max_f)
    return integral_value

# Test wydajności
if __name__ == "__main__":
    a, b, num_samples = 0, 2, 10_000_000
    start_time = time.time()
    result = monte_carlo_integral_numpy(a, b, num_samples)
    end_time = time.time()
    print(f"Numpy Monte Carlo: Wynik = {result}, Czas = {end_time - start_time:.2f} s")
