#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <chrono>
#include <cstdlib>

struct Data {
    int value;
};

void merge(std::vector<Data>& data, int left, int mid, int right) {
    std::vector<Data> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    while (i <= mid && j <= right)
        temp[k++] = (data[i].value <= data[j].value) ? data[i++] : data[j++];
    while (i <= mid) temp[k++] = data[i++];
    while (j <= right) temp[k++] = data[j++];
    for (int l = 0; l < temp.size(); ++l)
        data[left + l] = temp[l];
}

void bubbleSortThreads(std::vector<Data>& data, int num_threads) {
    std::vector<std::thread> threads;
    std::mutex mutex;
    int chunk = data.size() / num_threads;
    for (int t = 0; t < num_threads; ++t) {
        threads.emplace_back([&, t]() {
            int start = t * chunk;
            int end = (t == num_threads - 1) ? data.size() : start + chunk;
            for (int i = start; i < end; ++i) {
                for (int j = start; j < end - 1; ++j) {
                    if (data[j].value > data[j + 1].value) {
                        std::lock_guard<std::mutex> lock(mutex);
                        std::swap(data[j], data[j + 1]);
                    }
                }
            }
        });
    }
    for (auto& t : threads) t.join();
}

void insertionSortThreads(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    int chunk = n / num_threads;
    std::vector<std::thread> threads;
    std::mutex mutex;
    for (int t = 0; t < num_threads; ++t) {
        threads.emplace_back([&, t]() {
            int start = t * chunk;
            int end = (t == num_threads - 1) ? n : start + chunk;
            for (int i = start + 1; i < end; ++i) {
                Data key = data[i];
                int j = i - 1;
                while (j >= start && data[j].value > key.value) {
                    std::lock_guard<std::mutex> lock(mutex);
                    data[j + 1] = data[j];
                    --j;
                }
                data[j + 1] = key;
            }
        });
    }
    for (auto& t : threads) t.join();
}

void selectionSortThreads(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    int chunk = n / num_threads;
    std::vector<std::thread> threads;
    std::mutex mutex;
    for (int t = 0; t < num_threads; ++t) {
        threads.emplace_back([&, t]() {
            int start = t * chunk;
            int end = (t == num_threads - 1) ? n : start + chunk;
            for (int i = start; i < end - 1; ++i) {
                int min_idx = i;
                for (int j = i + 1; j < n; ++j) {
                    if (data[j].value < data[min_idx].value) {
                        min_idx = j;
                    }
                }
                std::lock_guard<std::mutex> lock(mutex);
                std::swap(data[i], data[min_idx]);
            }
        });
    }
    for (auto& t : threads) t.join();
}

void mergeSortThreads(std::vector<Data>& data, int left, int right, int num_threads) {
    if (left < right) {
        int mid = (left + right) / 2;
        if (num_threads > 1) {
            std::thread t1(mergeSortThreads, std::ref(data), left, mid, num_threads / 2);
            std::thread t2(mergeSortThreads, std::ref(data), mid + 1, right, num_threads - num_threads / 2);
            t1.join();
            t2.join();
        } else {
            mergeSortThreads(data, left, mid, 1);
            mergeSortThreads(data, mid + 1, right, 1);
        }
        merge(data, left, mid, right);
    }
}

void quickSortThreads(std::vector<Data>& data, int left, int right, int num_threads) {
    if (left >= right) return;
    int pivot = data[(left + right) / 2].value;
    int i = left, j = right;
    while (i <= j) {
        while (data[i].value < pivot) ++i;
        while (data[j].value > pivot) --j;
        if (i <= j) std::swap(data[i++], data[j--]);
    }
    if (num_threads > 1) {
        std::thread t1(quickSortThreads, std::ref(data), left, j, num_threads / 2);
        std::thread t2(quickSortThreads, std::ref(data), i, right, num_threads - num_threads / 2);
        t1.join(); t2.join();
    } else {
        quickSortThreads(data, left, j, 1);
        quickSortThreads(data, i, right, 1);
    }
}

void runSort(const std::string& name, void (*func)(std::vector<Data>&, int), std::vector<Data> base, int threads) {
    auto start = std::chrono::high_resolution_clock::now();
    func(base, threads);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> time = end - start;
    std::cout << name << ": " << time.count() << " s\n";
}

int main() {
    int n, threads;
    std::cout << "Podaj rozmiar tablicy: ";
    std::cin >> n;
    std::cout << "Podaj liczbę wątków: ";
    std::cin >> threads;

    std::vector<Data> data(n);
    for (int i = 0; i < n; ++i) data[i].value = rand() % 100000;

    runSort("Bubble Sort", bubbleSortThreads, data, threads);
    runSort("Insertion Sort", insertionSortThreads, data, threads);
    runSort("Selection Sort", selectionSortThreads, data, threads);

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<Data> data_merge = data;
    mergeSortThreads(data_merge, 0, n - 1, threads);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Merge Sort: " << std::chrono::duration<double>(end - start).count() << " s\n";

    start = std::chrono::high_resolution_clock::now();
    std::vector<Data> data_quick = data;
    quickSortThreads(data_quick, 0, n - 1, threads);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Quick Sort: " << std::chrono::duration<double>(end - start).count() << " s\n";

    return 0;
}
