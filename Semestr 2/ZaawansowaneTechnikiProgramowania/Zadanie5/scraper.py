import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import time

# Lista stron podzielona na kategorie
WEBSITES = {
    "informacyjne": [
        "https://tvn24.pl/swiat",
        "https://wiadomosci.onet.pl/swiat",
        "https://www.gazetaprawna.pl/wiadomosci/swiat",
        "https://www.rp.pl/wydarzenia/swiat",
        "https://wydarzenia.interia.pl/zagranica"
    ],
    "sportowe": [
        "https://sportowefakty.wp.pl/",
        "https://sport.tvp.pl/",
        "https://przegladsportowy.onet.pl/",
        "https://www.meczyki.pl/",
        "https://www.polsatsport.pl/"
    ],
    "technologiczne": [
        "https://antyweb.pl/",
        "https://infocraft.pl/polskie-portale-technologiczne-2024/",
        "https://techsetter.pl/",
        "https://www.benchmark.pl/kategoria/ciekawostki.html",
        "https://portaltechnologiczny.pl/"
    ],
    "plotkarskie": [
        "https://www.kozaczek.pl/",
        "https://www.pomponik.pl/",
        "https://www.plotek.pl/plotek/0,0.html",
        "https://www.pudelek.pl/",
        "https://plejada.pl/"
    ]
}

def fetch_titles(url):
    """
    Pobiera tytuły/nagłówki artykułów z danej strony WWW.

    :param url: Adres URL strony internetowej.
    :return: Lista nagłówków (jeśli uda się pobrać) lub pustą listę w przypadku błędu.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Sprawdza, czy odpowiedź nie zwróciła błędu HTTP
        soup = BeautifulSoup(response.text, 'html.parser')

        # Pobieranie tytułów - różne strony mogą mieć różne znaczniki
        titles = []
        for tag in ['h1', 'h2', 'h3']:
            titles.extend([title.get_text(strip=True) for title in soup.find_all(tag)])

        return titles if titles else ["Brak nagłówków"]
    except requests.RequestException as e:
        print(f"Błąd pobierania {url}: {e}")
        return []

def scrape_all_sites():
    """
    Pobiera nagłówki artykułów z wielu stron WWW równolegle.

    :return: Słownik z kategoriami i listami tytułów.
    """
    results = {category: [] for category in WEBSITES}

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_titles, url): (category, url) for category, urls in WEBSITES.items() for url in urls}
        
        for future in futures:
            category, url = futures[future]
            results[category].extend(future.result())

    end_time = time.time()
    print(f"Pobieranie nagłówków zakończone w {end_time - start_time:.2f} s")

    return results
