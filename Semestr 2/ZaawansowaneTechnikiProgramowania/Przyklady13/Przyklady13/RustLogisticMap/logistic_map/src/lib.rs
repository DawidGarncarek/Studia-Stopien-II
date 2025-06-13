#[no_mangle]
pub extern "C" fn logistic_map_bifurcation(
    r_start: f64,
    r_end: f64,
    r_steps: usize,
    x0: f64,
    iterations: usize,
    last_points: usize,
    output: *mut f64,
) {
    let step = (r_end - r_start) / (r_steps as f64);
    let mut index = 0;

    for i in 0..r_steps {
        let r = r_start + step * (i as f64);
        let mut x = x0;

        // Pomijanie początkowych iteracji
        for _ in 0..iterations {
            x = r * x * (1.0 - x);
        }

        // Zapis ostatnich punktów
        for _ in 0..last_points {
            x = r * x * (1.0 - x);
            unsafe {
                *output.add(index) = r;
                *output.add(index + 1) = x;
            }
            index += 2;
        }
    }
}


//#[no_mangle]: Zapobiega modyfikacji nazwy funkcji przez kompilator.
//extern "C": Umożliwia zgodność z językiem C.