import ctypes
import time

# Wczytaj bibliotekę Rust
monte_carlo_rust = ctypes.CDLL("./monte_carlo_rust/target/release/monte_carlo_rust.dll")

monte_carlo_rust.monte_carlo_integral_rust.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
monte_carlo_rust.monte_carlo_integral_rust.restype = ctypes.c_double

def monte_carlo_integral_rust(a, b, num_samples):
    """
    Oblicza wartość całki funkcji kwadratowej metodą Monte Carlo przy użyciu biblioteki Rust.

    :param a: Początek przedziału całkowania.
    :param b: Koniec przedziału całkowania.
    :param num_samples: Liczba losowych punktów.
    :return: Przybliżona wartość całki.
    """
    return monte_carlo_rust.monte_carlo_integral_rust(a, b, num_samples)

# Test wydajności
if __name__ == "__main__":
    a, b, num_samples = 0, 2, 10_000_000
    start_time = time.time()
    result = monte_carlo_integral_rust(a, b, num_samples)
    end_time = time.time()
    print(f"Rust Monte Carlo: Wynik = {result}, Czas = {end_time - start_time:.2f} s")
