import requests
from bs4 import BeautifulSoup

# Pobranie strony
url = "https://example.com"
response = requests.get(url)

# Parsowanie HTML
soup = BeautifulSoup(response.text, "html.parser")

# Wyszukiwanie tytułu strony
title = soup.find("title").get_text()
print("Title:", title)

# Wyszukiwanie wszystkich linków na stronie
links = soup.find_all("a")
for link in links:
    print("Link:", link.get("href"))
