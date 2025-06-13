import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    """Pobieranie zawartości strony.
    Funkcja pobiera zawartość HTML z danego URL za pomocą aiohttp.
    Dzięki await funkcja nie blokuje pętli zdarzeń i pozwala na równoczesne wykonywanie innych zadań."""
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Nie udało się pobrać {url}: {response.status}")
            return None

async def parse_page(html, url):
    """Analizowanie strony przy pomocy BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "Brak tytułu"
    print(f"Tytuł strony {url}: {title}")

async def scrape_urls(urls):
    """Główna funkcja do scrapingu listy URL."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(scrape_single_url(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def scrape_single_url(session, url):
    """Scrapowanie pojedynczej strony."""
    html = await fetch_page(session, url)
    if html:
        await parse_page(html, url)

if __name__ == "__main__":
    urls_to_scrape = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    asyncio.run(scrape_urls(urls_to_scrape))
