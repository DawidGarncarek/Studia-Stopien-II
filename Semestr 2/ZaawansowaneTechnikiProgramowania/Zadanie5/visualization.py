import matplotlib.pyplot as plt

def plot_word_frequencies(word_counts, top_n=10):
    """
    Tworzy wykresy najczęściej występujących słów w nagłówkach.

    :param word_counts: Słownik kategorii z licznikami słów.
    :param top_n: Liczba najczęściej występujących słów do pokazania.
    """
    for category, counter in word_counts.items():
        most_common = counter.most_common(top_n)
        words, counts = zip(*most_common) if most_common else ([], [])

        plt.figure(figsize=(10, 5))
        plt.bar(words, counts, color='skyblue')
        plt.xlabel("Słowa")
        plt.ylabel("Liczba wystąpień")
        plt.title(f"Najczęściej występujące słowa w kategorii: {category}")
        plt.xticks(rotation=45)
        plt.show()
