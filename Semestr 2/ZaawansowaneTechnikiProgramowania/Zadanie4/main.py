from sequential import run_sequential
from parallel_threads import run_parallel_threads
from parallel_processes import run_parallel_processes

if __name__ == "__main__":
    print("Uruchamianie obliczeń sekwencyjnych...")
    run_sequential()

    print("Uruchamianie obliczeń wielowątkowych...")
    run_parallel_threads()

    print("Uruchamianie obliczeń wieloprocesowych...")
    run_parallel_processes()
