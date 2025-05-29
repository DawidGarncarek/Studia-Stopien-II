#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <omp.h>
#include <cstring>

const int WIDTH = 8000;
const int HEIGHT = 8000;

struct Point {
    int x1, y1, x2, y2;
};

std::vector<Point> load_segments(const std::string& filename) {
    std::vector<Point> segments;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Nie można otworzyć pliku: " << filename << std::endl;
        return segments;
    }

    int x1, y1, x2, y2;
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        ss >> x1 >> y1 >> x2 >> y2;
        if (ss) {
            segments.push_back({ x1, y1, x2, y2 });
        }
    }

    return segments;
}

// Prosty rasteryzator (DDA)
void rasterize_line(unsigned char* image, int width, int height, Point p) {
    int dx = p.x2 - p.x1;
    int dy = p.y2 - p.y1;
    int steps = std::max(abs(dx), abs(dy));
    float x_inc = dx / (float)steps;
    float y_inc = dy / (float)steps;
    float x = p.x1;
    float y = p.y1;

    for (int i = 0; i <= steps; i++) {
        int xi = std::round(x);
        int yi = std::round(y);
        if (xi >= 0 && xi < width && yi >= 0 && yi < height) {
            int index = (yi * width + xi) * 3;
            image[index] = 255;  // R
            image[index + 1] = 255;  // G
            image[index + 2] = 255;  // B
        }
        x += x_inc;
        y += y_inc;
    }
}


void save_bmp(const std::string& filename, unsigned char* data, int width, int height) {
    FILE* f;
    int filesize = 54 + 3 * width * height;
    unsigned char bmpfileheader[14] = {
        'B','M', 0,0,0,0, 0,0, 0,0, 54,0,0,0
    };
    unsigned char bmpinfoheader[40] = {
        40,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,24,0
    };

    bmpfileheader[2] = (unsigned char)(filesize);
    bmpfileheader[3] = (unsigned char)(filesize >> 8);
    bmpfileheader[4] = (unsigned char)(filesize >> 16);
    bmpfileheader[5] = (unsigned char)(filesize >> 24);

    bmpinfoheader[4] = (unsigned char)(width);
    bmpinfoheader[5] = (unsigned char)(width >> 8);
    bmpinfoheader[6] = (unsigned char)(width >> 16);
    bmpinfoheader[7] = (unsigned char)(width >> 24);
    bmpinfoheader[8] = (unsigned char)(height);
    bmpinfoheader[9] = (unsigned char)(height >> 8);
    bmpinfoheader[10] = (unsigned char)(height >> 16);
    bmpinfoheader[11] = (unsigned char)(height >> 24);

    f = fopen(filename.c_str(), "wb");
    fwrite(bmpfileheader, 1, 14, f);
    fwrite(bmpinfoheader, 1, 40, f);

    for (int y = height - 1; y >= 0; y--)
        fwrite(data + y * width * 3, 3, width, f);

    fclose(f);
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cout << "Uzycie: " << argv[0] << " input.txt output.bmp P\n";
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];
    int threads = atoi(argv[3]);

    if (threads <= 0) {
        std::cout << "Blad: liczba watkow musi być dodatnia!\n";
        return 1;
    }

    omp_set_num_threads(threads);

    printf("Wczytywanie pliku: %s\n", input_file.c_str());

    auto segments = load_segments(input_file);

    printf("Liczba odcinkow: %zu\n", segments.size());

    printf("Rozpoczynam rasteryzacje na %d watkach...\n", threads);

    unsigned char* image = new unsigned char[WIDTH * HEIGHT * 3];
    std::memset(image, 0, WIDTH * HEIGHT * 3);  

    double t_start = omp_get_wtime();

#pragma omp parallel for
    for (int i = 0; i < segments.size(); i++) {
        rasterize_line(image, WIDTH, HEIGHT, segments[i]);
    }

    double t_end = omp_get_wtime();

    printf("Czas rasteryzacji (%d watkow): %.6f s\n", threads, t_end - t_start);

    save_bmp(output_file, image, WIDTH, HEIGHT);
    printf("Zapisano plik: %s\n", output_file.c_str());

    delete[] image;
    return 0;
}

