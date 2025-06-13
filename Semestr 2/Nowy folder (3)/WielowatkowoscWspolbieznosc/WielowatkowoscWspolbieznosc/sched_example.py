
import sched
import time

def zadanie(nazwa):
    print(f"Zadanie {nazwa} zostało wykonane w czasie: {time.time()}")

# Tworzenie planera
planer = sched.scheduler(time.time, time.sleep)

# Planowanie zadań
planer.enter(2, 1, zadanie, argument=('A',))
planer.enter(8, 1, zadanie, argument=('B',))

print("Zadania zostały zaplanowane")
planer.run()
print("Wszystkie zadania zostały wykonane")
