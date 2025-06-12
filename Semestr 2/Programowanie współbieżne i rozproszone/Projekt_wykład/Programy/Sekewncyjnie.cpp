#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>

// --- Algorytmy sortowania ---
void bubbleSort(std::vector<int>& arr) {
    size_t n = arr.size();
    for (size_t i = 0; i < n; ++i)
        for (size_t j = 0; j < n - i - 1; ++j)
            if (arr[j] > arr[j + 1])
                std::swap(arr[j], arr[j + 1]);
}

void insertionSort(std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key)
            arr[j + 1] = arr[j--];
        arr[j + 1] = key;
    }
}

void selectionSort(std::vector<int>& arr) {
    for (size_t i = 0; i < arr.size(); ++i) {
        size_t minIdx = i;
        for (size_t j = i + 1; j < arr.size(); ++j)
            if (arr[j] < arr[minIdx])
                minIdx = j;
        std::swap(arr[i], arr[minIdx]);
    }
}

void merge(std::vector<int>& arr, int l, int m, int r) {
    std::vector<int> left(arr.begin() + l, arr.begin() + m + 1);
    std::vector<int> right(arr.begin() + m + 1, arr.begin() + r + 1);

    size_t i = 0, j = 0, k = l;
    while (i < left.size() && j < right.size())
        arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
    while (i < left.size()) arr[k++] = left[i++];
    while (j < right.size()) arr[k++] = right[j++];
}

void mergeSort(std::vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high], i = low - 1;
    for (int j = low; j < high; ++j)
        if (arr[j] < pivot)
            std::swap(arr[++i], arr[j]);
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// --- Pomiar czasu ---
void measureAndPrint(const std::string& name, void(*sortFunc)(std::vector<int>&), const std::vector<int>& base) {
    std::vector<int> data = base;
    auto start = std::chrono::high_resolution_clock::now();
    sortFunc(data);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << name << ":\t" << duration.count() << " s\n";
}

int main() {
    int N;
    std::cout << "Podaj rozmiar tablicy do posortowania: ";
    std::cin >> N;

    if (N <= 0) {
        std::cerr << "Nieprawidłowy rozmiar.\n";
        return 1;
    }

    std::vector<int> original(N);
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(0, 999999999);
    for (auto& x : original) x = dist(rng);

    std::cout << "\nSekwencyjne sortowanie (" << N << " elementów):\n";

    measureAndPrint("Bubble Sort", bubbleSort, original);
    measureAndPrint("Insertion Sort", insertionSort, original);
    measureAndPrint("Selection Sort", selectionSort, original);

    std::vector<int> mergeData = original;
    auto t1 = std::chrono::high_resolution_clock::now();
    mergeSort(mergeData, 0, mergeData.size() - 1);
    auto t2 = std::chrono::high_resolution_clock::now();
    std::cout << "Merge Sort:\t" << std::chrono::duration<double>(t2 - t1).count() << " s\n";

    std::vector<int> quickData = original;
    auto t3 = std::chrono::high_resolution_clock::now();
    quickSort(quickData, 0, quickData.size() - 1);
    auto t4 = std::chrono::high_resolution_clock::now();
    std::cout << "Quick Sort:\t" << std::chrono::duration<double>(t4 - t3).count() << " s\n";

    return 0;
}
