#include <mpi.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <random>

using namespace std;
using Grid = vector<vector<float>>;

Grid load_matrix(const string& filename) {
    ifstream file(filename);
    Grid matrix;
    string line;
    while (getline(file, line)) {
        vector<float> row;
        stringstream ss(line);
        string cell;
        while (getline(ss, cell, ';')) {
            row.push_back(stof(cell));
        }
        matrix.push_back(row);
    }
    return matrix;
}

Grid create_random_matrix(int rows, int cols, float min_val, float max_val) {
    mt19937 rng(random_device{}());
    uniform_real_distribution<float> dist(min_val, max_val);
    Grid matrix(rows, vector<float>(cols));
    for (auto& row : matrix)
        for (auto& val : row)
            val = dist(rng);
    return matrix;
}

void save_matrix(const string& filename, const Grid& matrix) {
    ofstream file(filename);
    for (const auto& row : matrix) {
        for (size_t j = 0; j < row.size(); ++j) {
            file << row[j];
            if (j + 1 < row.size()) file << ";";
        }
        file << '\n';
    }
}

vector<float> flatten(const Grid& matrix) {
    vector<float> flat;
    for (const auto& row : matrix)
        flat.insert(flat.end(), row.begin(), row.end());
    return flat;
}

Grid unflatten(const vector<float>& data, int rows, int cols) {
    Grid matrix(rows, vector<float>(cols));
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            matrix[i][j] = data[i * cols + j];
    return matrix;
}

vector<float> merge_vectors(const vector<float>& a, const vector<float>& b) {
    vector<float> merged;
    merged.reserve(a.size() + b.size());
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        merged.push_back((a[i] <= b[j]) ? a[i++] : b[j++]);
    }
    while (i < a.size()) merged.push_back(a[i++]);
    while (j < b.size()) merged.push_back(b[j++]);
    return merged;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, num_procs;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    int total = 0, rows = 0, cols = 0;
    vector<float> flat_data;
    string output;
    double timer_start;

    if (rank == 0) {
        timer_start = MPI_Wtime();

        if (argc < 3) {
            cerr << "Uzycie: <exe> m n min max out.csv | <exe> in.csv out.csv" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        if (isdigit(argv[1][0])) {
            rows = stoi(argv[1]);
            cols = stoi(argv[2]);
            float min_v = stof(argv[3]);
            float max_v = stof(argv[4]);
            output = argv[5];
            flat_data = flatten(create_random_matrix(rows, cols, min_v, max_v));
        }
        else {
            Grid mat = load_matrix(argv[1]);
            output = argv[2];
            rows = mat.size();
            cols = mat[0].size();
            flat_data = flatten(mat);
        }

        total = rows * cols;
    }

    MPI_Bcast(&rows, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&cols, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&total, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int local_size = total / num_procs;
    vector<float> local_data(local_size);

    MPI_Scatter(flat_data.data(), local_size, MPI_FLOAT, local_data.data(), local_size, MPI_FLOAT, 0, MPI_COMM_WORLD);

    sort(local_data.begin(), local_data.end());

    int stride = 1;
    while (stride < num_procs) {
        if (rank % (2 * stride) == 0) {
            if (rank + stride < num_procs) {
                int recv_count;
                MPI_Recv(&recv_count, 1, MPI_INT, rank + stride, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                vector<float> recv_buf(recv_count);
                MPI_Recv(recv_buf.data(), recv_count, MPI_FLOAT, rank + stride, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                local_data = merge_vectors(local_data, recv_buf);
            }
        }
        else {
            int target = rank - stride;
            int send_count = local_data.size();
            MPI_Send(&send_count, 1, MPI_INT, target, 0, MPI_COMM_WORLD);
            MPI_Send(local_data.data(), send_count, MPI_FLOAT, target, 1, MPI_COMM_WORLD);
            break;
        }
        stride *= 2;
    }

    if (rank == 0) {
        double timer_end = MPI_Wtime();
        Grid final_result = unflatten(local_data, rows, cols);
        save_matrix(output, final_result);
        cout << "Czas sortowania (MPI) z drzewem scalania: " << (timer_end - timer_start) << " s" << endl;
    }

    MPI_Finalize();
    return 0;
}
