import numpy as np
from scipy.integrate import solve_ivp

def spring_mass_system(t, state, m, c, k, A, f):
    """
    Definiuje równania różniczkowe dla układu masa na sprężynie.

    :param t: Czas
    :param state: Wektor stanu [x, v] (przemieszczenie, prędkość)
    :param m: Masa
    :param c: Współczynnik tłumienia
    :param k: Współczynnik sztywności sprężyny
    :param A: Amplituda siły wymuszającej
    :param f: Częstotliwość siły wymuszającej
    :return: Lista pochodnych [dx/dt, dv/dt]
    """
    x, v = state
    force = A * np.sin(2 * np.pi * f * t)  # Siła wymuszająca
    dxdt = v
    dvdt = (force - c * v - k * x) / m
    return [dxdt, dvdt]

def simulate(m, f, t_max=10, dt=0.01, c=0.001, k=1000, A=1):
    """
    Przeprowadza symulację układu masa-sprężyna dla danej wartości m i f.

    :param m: Masa
    :param f: Częstotliwość siły wymuszającej
    :param t_max: Czas symulacji (s)
    :param dt: Krok czasowy
    :param c: Współczynnik tłumienia
    :param k: Współczynnik sprężystości
    :param A: Amplituda siły wymuszającej
    :return: Maksymalne przemieszczenie w symulacji
    """
    t_eval = np.arange(0, t_max, dt)
    initial_state = [0, 0]  # x=0, v=0
    sol = solve_ivp(spring_mass_system, [0, t_max], initial_state, t_eval=t_eval, args=(m, c, k, A, f))
    
    return np.max(np.abs(sol.y[0]))  # Maksymalne przemieszczenie
