from collections import Counter
import re

def clean_text(text):
    """
    Oczyszcza tekst z znaków specjalnych i konwertuje na małe litery.

    :param text: Wejściowy tekst do oczyszczenia.
    :return: Lista słów.
    """
    return re.findall(r'\b\w+\b', text.lower())

def count_words(titles_by_category):
    """
    Zlicza najczęściej występujące słowa w nagłówkach dla każdej kategorii.

    :param titles_by_category: Słownik kategorii z listami tytułów.
    :return: Słownik kategorii z licznikami słów.
    """
    word_counts = {}
    
    for category, titles in titles_by_category.items():
        words = []
        for title in titles:
            words.extend(clean_text(title))
        
        word_counts[category] = Counter(words)

    return word_counts
