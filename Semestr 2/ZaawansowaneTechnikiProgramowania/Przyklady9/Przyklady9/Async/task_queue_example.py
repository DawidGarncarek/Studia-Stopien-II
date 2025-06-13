import asyncio
import random

async def background_task(task_number):
    print(f"Zadanie {task_number} rozpoczęte")
    await asyncio.sleep(random.randint(1, 3))  # Symulacja długiego zadania
    print(f"Zadanie {task_number} zakończone")

async def main():
    tasks = []
    for i in range(5):  # Tworzymy pięć zadań do przetwarzania w tle
        tasks.append(asyncio.create_task(background_task(i)))
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
