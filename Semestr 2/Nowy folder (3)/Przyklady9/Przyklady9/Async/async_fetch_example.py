import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    url1 = 'https://jsonplaceholder.typicode.com/posts/1'
    url2 = 'https://jsonplaceholder.typicode.com/posts/2'
    
    # tworzenie zadan
    task1 = asyncio.create_task(fetch_data(url1))
    task2 = asyncio.create_task(fetch_data(url2))
    
    # grupowanie zadań i oczekiwanie na wynik
    data1, data2 = await asyncio.gather(task1, task2)
    
    print("Dane z URL 1:", data1[:100])  # Drukowanie pierwszych 100 znaków
    print("Dane z URL 2:", data2[:100])

# Uruchomienie pętli zdarzeń
if __name__ == "__main__":
    asyncio.run(main())
