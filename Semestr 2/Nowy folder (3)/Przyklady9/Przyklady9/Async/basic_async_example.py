import asyncio

async def my_async_function():
    print("Rozpoczynam zadanie")
    await asyncio.sleep(2)  # Symulacja długiego zadania
    print("Zadanie zakończone po 2 sekundach")

# Uruchomienie pętli zdarzeń
if __name__ == "__main__":
    asyncio.run(my_async_function())
