from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import openpyxl

# Inicjalizacja przeglądarki (np. Chrome)
driver = webdriver.Chrome()

# Otwieranie strony
driver.get("https://sowa.bg.po.edu.pl/")

time.sleep(5)
search=driver.find_element(By.XPATH,'//*[@id="simple-search-phrase"]')
search.send_keys('Python')
search.send_keys(Keys.RETURN)

time.sleep(10)

results = driver.find_element(By.CLASS_NAME,'found-records')
books = results.find_elements(By.CLASS_NAME,'desc-o-mb-title')
authors = results.find_elements(By.CLASS_NAME,'desc-o-b-rest')
print(books)
titles=[]
rest=[]
for i in range(len(books)):
    titles.append(books[i].text)
    rest.append(authors[i].text[2:-1]) #usunięcie / na początku
    
name_dict = {
            'Title': titles,
            'Author': rest
          }

df = pd.DataFrame(name_dict)
df.to_excel('books.xlsx',index=False)
print(df)

driver.quit()