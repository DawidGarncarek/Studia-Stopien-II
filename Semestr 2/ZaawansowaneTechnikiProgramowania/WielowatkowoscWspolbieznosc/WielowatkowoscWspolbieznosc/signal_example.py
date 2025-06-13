
import signal
import time

def obsluga_sygnalu(signum, frame):
    print(f"Otrzymano sygnał: {signum}")

# Rejestrowanie funkcji obsługi sygnału SIGINT (Ctrl+C) - nie da się teraz przerwać programu CTRL+C
signal.signal(signal.SIGINT, obsluga_sygnalu)

print("Oczekuję na sygnał (Ctrl+C)...")
while True:
    time.sleep(1)
