use rand::Rng;
use std::ffi::c_double;

#[no_mangle]
pub extern "C" fn monte_carlo_integral_rust(a: c_double, b: c_double, num_samples: i32) -> c_double {
    let mut rng = rand::thread_rng();
    let mut count_under_curve = 0;
    let max_f = b * b; // Maksymalna wartość funkcji f(x) = x^2

    for _ in 0..num_samples {
        let x_rand: f64 = rng.gen_range(a..b);
        let y_rand: f64 = rng.gen_range(0.0..max_f);

        if y_rand <= x_rand * x_rand {
            count_under_curve += 1;
        }
    }

    (count_under_curve as f64 / num_samples as f64) * ((b - a) * max_f)
}
