from monte_carlo_pure import monte_carlo_integral_pure
from monte_carlo_numpy import monte_carlo_integral_numpy
from monte_carlo_rust import monte_carlo_integral_rust
import time

a, b, num_samples = 0, 2, 10_000_000

for method, func in [
    ("Python", monte_carlo_integral_pure),
    ("Numpy", monte_carlo_integral_numpy),
    ("Rust", monte_carlo_integral_rust)
]:
    start_time = time.time()
    result = func(a, b, num_samples)
    end_time = time.time()
    print(f"{method} Monte Carlo: Wynik = {result}, Czas = {end_time - start_time:.2f} s")
