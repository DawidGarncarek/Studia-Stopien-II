from scraper import scrape_all_sites
from word_counter import count_words
from visualization import plot_word_frequencies

def main():
    """
    Główna funkcja uruchamiająca proces pobierania nagłówków, analizy słów i wizualizacji.
    """
    print("Pobieranie nagłówków...")
    titles_by_category = scrape_all_sites()

    print("Analiza słów...")
    word_counts = count_words(titles_by_category)

    print("Wizualizacja wyników...")
    plot_word_frequencies(word_counts)

if __name__ == "__main__":
    main()
