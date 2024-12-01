#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>
#include <random>
#include <ctime>
#include <utility>

using std::cout;
using std::vector;
using std::unique_ptr;
using std::make_unique;
using std::mt19937;
using std::uniform_int_distribution;
using std::endl;
using std::sort;
using std::pair;

class ArrayBase {
protected:
    int dimensions;
    vector<int> sizes;
    unique_ptr<int[]> data;

public:
    ArrayBase(int dim, const vector<int>& sz)
        : dimensions(dim), sizes(sz) {
        int totalSize = 1;
        for (int s : sizes) {
            totalSize *= s;
        }
        data = make_unique<int[]>(totalSize);
    }

    virtual int& at(const vector<int>& indices) {
        int index = 0;
        int stride = 1;
        for (int i = dimensions - 1; i >= 0; i--) {
            index += indices[i] * stride;
            stride *= sizes[i];
        }
        return data[index];
    }

    virtual void fillArray() = 0;
    virtual void printArray() const = 0;
    virtual void sortRowsBySum() = 0;
    virtual ~ArrayBase() {}
};

class Array2D : public ArrayBase {
private:
    mt19937 mt;

public:
    Array2D(int rows, int cols)
        : ArrayBase(2, {rows, cols}), mt(static_cast<unsigned>(time(0))) {}

    void fillArray() override {
        uniform_int_distribution<int> dist(0, 10);
        for (int i = 0; i < sizes[0]; i++) {
            for (int j = 0; j < sizes[1]; j++) {
                at({i, j}) = dist(mt);
            }
        }
    }

    void printArray() const override {
        for (int i = 0; i < sizes[0]; i++) {
            for (int j = 0; j < sizes[1]; j++) {
                cout << data[i * sizes[1] + j] << " ";
            }
            cout << endl;
        }
    }

    void sortRowsBySum() override {
        vector<pair<int, vector<int>>> rowSums;
        for (int i = 0; i < sizes[0]; i++) {
            int sum = 0;
            vector<int> row(sizes[1]);
            for (int j = 0; j < sizes[1]; j++) {
                int value = at({i, j});
                sum += value;
                row[j] = value;
            }
            rowSums.push_back({sum, row});
        }

        sort(rowSums.begin(), rowSums.end(), 
             [](const auto& a, const auto& b) { return a.first > b.first; });

        for (int i = 0; i < sizes[0]; i++) {
            for (int j = 0; j < sizes[1]; j++) {
                at({i, j}) = rowSums[i].second[j];
            }
        }
    }
};

int main() {
    Array2D array(10, 10);
    array.fillArray();
    cout << "Початковий масив:\n";
    array.printArray();
    array.sortRowsBySum();
    cout << "\nВідсортований масив:\n";
    array.printArray();
    return 0;
}
