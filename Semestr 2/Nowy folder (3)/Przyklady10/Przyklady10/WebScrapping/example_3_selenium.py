from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Inicjalizacja przeglądarki (np. Chrome)
driver = webdriver.Chrome()

# Otwieranie strony
driver.get("https://example.com")

# Pobieranie tytułu strony
title = driver.title
print("Title:", title)

# Wyszukiwanie elementów załadowanych dynamicznie
element = driver.find_element(By.ID, "dynamic-content")
print("Dynamic Content:", element.text)

# Zamknięcie przeglądarki
driver.quit()
