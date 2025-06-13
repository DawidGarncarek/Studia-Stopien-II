import asyncio
import aiohttp

async def fetch_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Błąd HTTP: {response.status}")
                return await response.text()
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None

async def main():
    url1 = 'https://jsonplaceholder.typicode.com/posts/1'
    url2 = 'https://jsonplaceholder.typicode.com/invalid-url'
    
    task1 = asyncio.create_task(fetch_data(url1))
    task2 = asyncio.create_task(fetch_data(url2))
    
    data = await asyncio.gather(task1, task2, return_exceptions=True)
    print("Dane:", data)

# Uruchomienie pętli zdarzeń
if __name__ == "__main__":
    asyncio.run(main())
