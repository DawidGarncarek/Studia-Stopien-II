#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <chrono>

#ifdef _OPENMP
#include <omp.h>
#endif

#include <thread>
#include <mutex>
using namespace std;

// Struktura reprezentująca dane
struct Data {
    int value;
};

// Funkcja wczytująca dane z pliku CSV
std::vector<Data> readCSV(const std::string& filename) {
    std::vector<Data> data;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file " << filename << std::endl;
        exit(EXIT_FAILURE);
    }

    std::string line;
    while (std::getline(file, line, ';')) {
        int value = std::stoi(line);
        data.push_back({ value });
    }

    return data;
}

// Funkcja zapisująca dane do pliku CSV
void writeCSV(const std::string& filename, const std::vector<Data>& data) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file " << filename << " for writing" << std::endl;
        exit(EXIT_FAILURE);
    }

    for (const auto& d : data) {
        file << d.value << std::endl;
    }

    file.close();
}

// Funkcja sortująca bąbelkowo
void bubbleSort(std::vector<Data>& data) {
    int n = data.size();
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (data[j].value > data[j + 1].value) {
                std::swap(data[j], data[j + 1]);
            }
        }
    }
}

// Funkcja sortująca bąbelkowo OMP
void bubbleSortOMP(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    for (int i = 0; i < n - 1; ++i) {
#pragma omp parallel for shared(data) schedule(static) num_threads(num_threads)
        for (int j = 0; j < n - i - 1; ++j) {
            if (data[j].value > data[j + 1].value) {
                swap(data[j], data[j + 1]);
            }
        }
    }
}

// Funkcja sortująca bąbelkowo z użyciem wątków C++
void bubbleSortThreads(std::vector<Data>& data, int num_threads) {
    std::vector<std::thread> threads;
    const int chunk_size = data.size() / num_threads;
    std::mutex mutex;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&, i] {
            int start_index = i * chunk_size;
            int end_index = (i == num_threads - 1) ? data.size() : start_index + chunk_size;
            for (int j = start_index; j < end_index; ++j) {
                for (int k = start_index; k < end_index - 1; ++k) {
                    if (data[k].value > data[k + 1].value) {
                        std::lock_guard<std::mutex> lock(mutex);
                        std::swap(data[k], data[k + 1]);
                    }
                }
            }
            });
    }

    for (auto& t : threads) {
        t.join();
    }
}

// Implementacja algorytmu QuickSort (wersja sekwencyjna)
void quicksort(std::vector<Data>& data, int left, int right) {
    if (left >= right) return;
    int pivot = data[left + (right - left) / 2].value;
    int i = left, j = right;
    while (i <= j) {
        while (data[i].value < pivot) i++;
        while (data[j].value > pivot) j--;
        if (i <= j) {
            std::swap(data[i], data[j]);
            i++;
            j--;
        }
    }
    quicksort(data, left, j);
    quicksort(data, i, right);
}

// Implementacja algorytmu QuickSort z OpenMP
void quickSortOMP(std::vector<Data>& data, int left, int right, int depth) {
    if (left >= right) return;
    int pivot = data[left + (right - left) / 2].value;
    int i = left, j = right;
    while (i <= j) {
        while (data[i].value < pivot) i++;
        while (data[j].value > pivot) j--;
        if (i <= j) {
            std::swap(data[i], data[j]);
            i++;
            j--;
        }
    }

    if (depth > 0) {
#pragma omp parallel sections
        {
#pragma omp section
            {
                quickSortOMP(data, left, j, depth - 1);
            }
#pragma omp section
            {
                quickSortOMP(data, i, right, depth - 1);
            }
        }
    }
    else {
        quickSortOMP(data, left, j, depth);
        quickSortOMP(data, i, right, depth);
    }
}

// Function to perform QuickSort using multiple threads
void quickSortThread(std::vector<Data>& data, int left, int right, int num_threads) {
    if (left >= right) return;
    int pivot = data[left + (right - left) / 2].value;
    int i = left, j = right;
    while (i <= j) {
        while (data[i].value < pivot) i++;
        while (data[j].value > pivot) j--;
        if (i <= j) {
            std::swap(data[i], data[j]);
            i++;
            j--;
        }
    }

    if (num_threads > 1) {
        std::thread left_thread(quickSortThread, std::ref(data), left, j, num_threads / 2);
        std::thread right_thread(quickSortThread, std::ref(data), i, right, num_threads / 2);

        left_thread.join();
        right_thread.join();
    }
    else {
        quickSortThread(data, left, j, num_threads);
        quickSortThread(data, i, right, num_threads);
    }
}

// MergeSort sekwencyjny
void merge(std::vector<Data>& data, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    std::vector<Data> left_half(n1), right_half(n2);

    for (int i = 0; i < n1; ++i)
        left_half[i] = data[left + i];
    for (int j = 0; j < n2; ++j)
        right_half[j] = data[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (left_half[i].value <= right_half[j].value) {
            data[k] = left_half[i];
            ++i;
        }
        else {
            data[k] = right_half[j];
            ++j;
        }
        ++k;
    }

    while (i < n1) {
        data[k] = left_half[i];
        ++i;
        ++k;
    }

    while (j < n2) {
        data[k] = right_half[j];
        ++j;
        ++k;
    }
}

void mergeSort(std::vector<Data>& data, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(data, left, mid);
        mergeSort(data, mid + 1, right);
        merge(data, left, mid, right);
    }
}

// MergeSort z OpenMP
void mergeSortOMP(std::vector<Data>& data, int left, int right, int num_threads) {
    if (left < right) {
        int mid = left + (right - left) / 2;
#pragma omp parallel sections
        {
#pragma omp section
            mergeSortOMP(data, left, mid, num_threads);
#pragma omp section
            mergeSortOMP(data, mid + 1, right, num_threads);
        }
        merge(data, left, mid, right);
    }
}

// MergeSort z użyciem wątków C++
void mergeSortThreads(std::vector<Data>& data, int left, int right, int num_threads) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        if (num_threads > 1) {
            std::thread left_thread(mergeSortThreads, std::ref(data), left, mid, num_threads / 2);
            std::thread right_thread(mergeSortThreads, std::ref(data), mid + 1, right, num_threads - num_threads / 2);
            left_thread.join();
            right_thread.join();
        }
        else {
            mergeSortThreads(data, left, mid, num_threads);
            mergeSortThreads(data, mid + 1, right, num_threads);
        }
        merge(data, left, mid, right);
    }
}

// InsertionSort sekwencyjny
void insertionSort(std::vector<Data>& data) {
    int n = data.size();
    for (int i = 1; i < n; ++i) {
        Data key = data[i];
        int j = i - 1;
        while (j >= 0 && data[j].value > key.value) {
            data[j + 1] = data[j];
            --j;
        }
        data[j + 1] = key;
    }
}

// InsertionSort z OpenMP
void insertionSortOMP(std::vector<Data>& data, int num_threads) {
    int n = data.size();
#pragma omp parallel for shared(data) schedule(static) num_threads(num_threads)
    for (int i = 1; i < n; ++i) {
        Data key = data[i];
        int j = i - 1;
        while (j >= 0 && data[j].value > key.value) {
            data[j + 1] = data[j];
            --j;
        }
        data[j + 1] = key;
    }
}

// InsertionSort z użyciem wątków C++
void insertionSortThreads(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    std::vector<std::thread> threads;
    const int chunk_size = n / num_threads;
    std::mutex mutex;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&, i] {
            int start_index = i * chunk_size;
            int end_index = (i == num_threads - 1) ? n : start_index + chunk_size;
            for (int j = start_index + 1; j < end_index; ++j) {
                Data key = data[j];
                int k = j - 1;
                while (k >= start_index && data[k].value > key.value) {
                    std::lock_guard<std::mutex> lock(mutex);
                    data[k + 1] = data[k];
                    --k;
                }
                data[k + 1] = key;
            }
            });
    }

    for (auto& t : threads) {
        t.join();
    }
}

// SelectionSort sekwencyjny
void selectionSort(std::vector<Data>& data) {
    int n = data.size();
    for (int i = 0; i < n - 1; ++i) {
        int min_index = i;
        for (int j = i + 1; j < n; ++j) {
            if (data[j].value < data[min_index].value) {
                min_index = j;
            }
        }
        if (min_index != i) {
            std::swap(data[i], data[min_index]);
        }
    }
}

// SelectionSort z OpenMP
void selectionSortOMP(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    for (int i = 0; i < n - 1; ++i) {
        int min_index = i;
#pragma omp parallel for shared(data, min_index) num_threads(num_threads)
        for (int j = i + 1; j < n; ++j) {
            if (data[j].value < data[min_index].value) {
#pragma omp critical
                {
                    if (data[j].value < data[min_index].value) {
                        min_index = j;
                    }
                }
            }
        }
        if (min_index != i) {
            std::swap(data[i], data[min_index]);
        }
    }
}

// SelectionSort z użyciem wątków C++
void selectionSortThreads(std::vector<Data>& data, int num_threads) {
    int n = data.size();
    const int chunk_size = n / num_threads;
    std::vector<std::thread> threads;
    std::mutex mutex;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&, i] {
            int start_index = i * chunk_size;
            int end_index = (i == num_threads - 1) ? n : start_index + chunk_size;
            for (int j = start_index; j < end_index - 1; ++j) {
                int min_index = j;
                for (int k = j + 1; k < n; ++k) {
                    if (data[k].value < data[min_index].value) {
                        min_index = k;
                    }
                }
                if (min_index != j) {
                    std::lock_guard<std::mutex> lock(mutex);
                    std::swap(data[j], data[min_index]);
                }
            }
            });
    }

    for (auto& t : threads) {
        t.join();
    }
}


int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " input_filename.csv output_filename.csv num_threads" << std::endl;
        return EXIT_FAILURE;
    }

    std::string input_filename = argv[1];
    std::string output_filename = argv[2];
    int num_threads = std::stoi(argv[3]);
    std::vector<Data> data = readCSV(input_filename);

    //// Pomiary czasu dla wariantu sekwencyjnego
    //auto start_sequential = std::chrono::steady_clock::now();
    //bubbleSort(data);
    //auto end_sequential = std::chrono::steady_clock::now();
    //std::chrono::duration<double> sequential_duration = end_sequential - start_sequential;
    //std::cout << "Sequential Bubble Sort Time: " << sequential_duration.count() << " seconds" << std::endl;

#ifdef _OPENMP
    // Pomiary czasu dla wariantu z OpenMP
    auto start_openmp = std::chrono::steady_clock::now();
    bubbleSortOMP(data, num_threads);
    auto end_openmp = std::chrono::steady_clock::now();
    std::chrono::duration<double> openmp_duration = end_openmp - start_openmp;
    std::cout << "OpenMP Bubble Sort Time: " << openmp_duration.count() << " seconds" << std::endl;
#endif

    // Pomiary czasu dla wariantu z wątkami C++
    auto start_threads = std::chrono::steady_clock::now();
    bubbleSortThreads(data, num_threads);
    auto end_threads = std::chrono::steady_clock::now();
    std::chrono::duration<double> threads_duration = end_threads - start_threads;
    std::cout << "Threads Bubble Sort Time: " << threads_duration.count() << " seconds" << std::endl;

    //// Pomiary czasu dla QuickSort
    //auto start_quick_sequential = std::chrono::steady_clock::now();
    //quicksort(data, 0, data.size() - 1);
    //auto end_quick_sequential = std::chrono::steady_clock::now();
    //std::chrono::duration<double> quick_sequential_duration = end_quick_sequential - start_quick_sequential;
    //std::cout << "Sequential QuickSort Time: " << quick_sequential_duration.count() << " seconds" << std::endl;

#ifdef _OPENMP
    // Pomiary czasu dla QuickSort z OpenMP
    omp_set_num_threads(num_threads);
    auto start_quick_openmp = std::chrono::steady_clock::now();
#pragma omp parallel
    {
#pragma omp single nowait
        {
            quickSortOMP(data, 0, data.size() - 1, num_threads);
        }
    }
    auto end_quick_openmp = std::chrono::steady_clock::now();
    std::chrono::duration<double> quick_openmp_duration = end_quick_openmp - start_quick_openmp;
    std::cout << "OpenMP QuickSort Time: " << quick_openmp_duration.count() << " seconds" << std::endl;
#endif

    // Pomiary czasu dla QuickSort z wątkami C++
    auto start_quick_threads = std::chrono::steady_clock::now();
    quickSortThread(data, 0, data.size() - 1, num_threads);
    auto end_quick_threads = std::chrono::steady_clock::now();
    std::chrono::duration<double> quick_threads_duration = end_quick_threads - start_quick_threads;
    std::cout << "Threads QuickSort Time: " << quick_threads_duration.count() << " seconds" << std::endl;

    //// Pomiary czasu dla MergeSort
    //auto start_merge_sequential = std::chrono::steady_clock::now();
    //mergeSort(data, 0, data.size() - 1);
    //auto end_merge_sequential = std::chrono::steady_clock::now();
    //std::chrono::duration<double> merge_sequential_duration = end_merge_sequential - start_merge_sequential;
    //std::cout << "Sequential MergeSort Time: " << merge_sequential_duration.count() << " seconds" << std::endl;

#ifdef _OPENMP
    // Pomiary czasu dla MergeSort z OpenMP
    auto start_merge_openmp = std::chrono::steady_clock::now();
    mergeSortOMP(data, 0, data.size() - 1, num_threads);
    auto end_merge_openmp = std::chrono::steady_clock::now();
    std::chrono::duration<double> merge_openmp_duration = end_merge_openmp - start_merge_openmp;
    std::cout << "OpenMP MergeSort Time: " << merge_openmp_duration.count() << " seconds" << std::endl;
#endif

    // Pomiary czasu dla MergeSort z wątkami C++
    auto start_merge_threads = std::chrono::steady_clock::now();
    mergeSortThreads(data, 0, data.size() - 1, num_threads);
    auto end_merge_threads = std::chrono::steady_clock::now();
    std::chrono::duration<double> merge_threads_duration = end_merge_threads - start_merge_threads;
    std::cout << "Threads MergeSort Time: " << merge_threads_duration.count() << " seconds" << std::endl;

    //// Pomiary czasu dla InsertionSort
    //auto start_insertion_sequential = std::chrono::steady_clock::now();
    //insertionSort(data);
    //auto end_insertion_sequential = std::chrono::steady_clock::now();
    //std::chrono::duration<double> insertion_sequential_duration = end_insertion_sequential - start_insertion_sequential;
    //std::cout << "Sequential InsertionSort Time: " << insertion_sequential_duration.count() << " seconds" << std::endl;

#ifdef _OPENMP
    // Pomiary czasu dla InsertionSort z OpenMP
    auto start_insertion_openmp = std::chrono::steady_clock::now();
    insertionSortOMP(data, num_threads);
    auto end_insertion_openmp = std::chrono::steady_clock::now();
    std::chrono::duration<double> insertion_openmp_duration = end_insertion_openmp - start_insertion_openmp;
    std::cout << "OpenMP InsertionSort Time: " << insertion_openmp_duration.count() << " seconds" << std::endl;
#endif

    // Pomiary czasu dla InsertionSort z wątkami C++
    auto start_insertion_threads = std::chrono::steady_clock::now();
    insertionSortThreads(data, num_threads);
    auto end_insertion_threads = std::chrono::steady_clock::now();
    std::chrono::duration<double> insertion_threads_duration = end_insertion_threads - start_insertion_threads;
    std::cout << "Threads InsertionSort Time: " << insertion_threads_duration.count() << " seconds" << std::endl;

    //// Pomiary czasu dla SelectionSort
    //auto start_selection_sequential = std::chrono::steady_clock::now();
    //selectionSort(data);
    //auto end_selection_sequential = std::chrono::steady_clock::now();
    //std::chrono::duration<double> selection_sequential_duration = end_selection_sequential - start_selection_sequential;
    //std::cout << "Sequential SelectionSort Time: " << selection_sequential_duration.count() << " seconds" << std::endl;

#ifdef _OPENMP
    // Pomiary czasu dla SelectionSort z OpenMP
    auto start_selection_openmp = std::chrono::steady_clock::now();
    selectionSortOMP(data, num_threads);
    auto end_selection_openmp = std::chrono::steady_clock::now();
    std::chrono::duration<double> selection_openmp_duration = end_selection_openmp - start_selection_openmp;
    std::cout << "OpenMP SelectionSort Time: " << selection_openmp_duration.count() << " seconds" << std::endl;
#endif

    // Pomiary czasu dla SelectionSort z wątkami C++
    auto start_selection_threads = std::chrono::steady_clock::now();
    selectionSortThreads(data, num_threads);
    auto end_selection_threads = std::chrono::steady_clock::now();
    std::chrono::duration<double> selection_threads_duration = end_selection_threads - start_selection_threads;
    std::cout << "Threads SelectionSort Time: " << selection_threads_duration.count() << " seconds" << std::endl;

    // Zapisanie posortowanych danych do pliku CSV
    //writeCSV(output_filename, data);
    //std::cout << "Sorted data saved to " << output_filename << std::endl;

    return EXIT_SUCCESS;
}
