import random
import time

def monte_carlo_integral_pure(a, b, num_samples):
    """
    Oblicza wartość całki funkcji kwadratowej metodą Monte Carlo w czystym Pythonie.

    :param a: Początek przedziału całkowania.
    :param b: Koniec przedziału całkowania.
    :param num_samples: Liczba losowych punktów.
    :return: Przybliżona wartość całki.
    """
    def quadratic_function(x):
        return x ** 2  # Funkcja kwadratowa f(x) = x^2

    max_f = max(quadratic_function(a), quadratic_function(b))  # Maksymalna wartość funkcji
    count_under_curve = 0

    for _ in range(num_samples):
        x_rand = random.uniform(a, b)
        y_rand = random.uniform(0, max_f)

        if y_rand <= quadratic_function(x_rand):
            count_under_curve += 1

    integral_value = (count_under_curve / num_samples) * ((b - a) * max_f)
    return integral_value

# Test wydajności
if __name__ == "__main__":
    a, b, num_samples = 0, 2, 10_000_000
    start_time = time.time()
    result = monte_carlo_integral_pure(a, b, num_samples)
    end_time = time.time()
    print(f"Python Monte Carlo: Wynik = {result}, Czas = {end_time - start_time:.2f} s")
