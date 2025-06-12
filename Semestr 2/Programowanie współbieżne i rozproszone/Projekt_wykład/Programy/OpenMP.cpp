
#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>
#include <chrono>
#include <omp.h>
#include <cstdlib>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
#pragma omp parallel for
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) std::swap(arr[j], arr[j + 1]);
        }
    }
}

void insertionSort(std::vector<int>& arr) {
    int n = arr.size();
#pragma omp parallel for
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void selectionSort(std::vector<int>& arr) {
    int n = arr.size();
#pragma omp parallel for
    for (int i = 0; i < n - 1; ++i) {
        int min_idx = i;
        for (int j = i + 1; j < n; ++j) {
            if (arr[j] < arr[min_idx]) min_idx = j;
        }
        std::swap(arr[i], arr[min_idx]);
    }
}

void merge(std::vector<int>& arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    std::vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(std::vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
#pragma omp parallel sections
        {
#pragma omp section
            mergeSort(arr, l, m);
#pragma omp section
            mergeSort(arr, m + 1, r);
        }
        merge(arr, l, m, r);
    }
}

int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
#pragma omp parallel sections
        {
#pragma omp section
            quickSort(arr, low, pi - 1);
#pragma omp section
            quickSort(arr, pi + 1, high);
        }
    }
}

void runAndMeasure(void (*sortFunc)(std::vector<int>&), std::vector<int> data, const std::string& name) {
    auto start = std::chrono::high_resolution_clock::now();
    sortFunc(data);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << name << ": " << duration.count() << " s\n";
}

int main() {
    int n, threads;
    std::cout << "Podaj rozmiar tablicy: ";
    std::cin >> n;
    std::cout << "Podaj liczbe watkow: ";
    std::cin >> threads;

    omp_set_num_threads(threads);

    std::vector<int> base(n);
    srand(time(0));
    for (int i = 0; i < n; i++) base[i] = rand() % 100000;

    runAndMeasure(bubbleSort, base, "Bubble Sort");
    runAndMeasure(insertionSort, base, "Insertion Sort");
    runAndMeasure(selectionSort, base, "Selection Sort");

    std::vector<int> copy = base;
    auto start = std::chrono::high_resolution_clock::now();
    mergeSort(copy, 0, n - 1);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Merge Sort: " << duration.count() << " s\n";

    copy = base;
    start = std::chrono::high_resolution_clock::now();
    quickSort(copy, 0, n - 1);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Quick Sort: " << duration.count() << " s\n";

    return 0;
}
