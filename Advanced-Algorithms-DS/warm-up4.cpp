#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;

    std::vector<int> heights(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> heights[i];
    }

    int tallest_idx = 0;
    int second_tallest_idx = -1;

    for (int i = 0; i < n; ++i) {
        if (heights[i] > heights[tallest_idx]) {
            second_tallest_idx = tallest_idx;
            tallest_idx = i;
        } else if (second_tallest_idx == -1 || heights[i] > heights[second_tallest_idx]) {
            if (i != tallest_idx) {
                second_tallest_idx = i;
            }
        }
    }

    std::cout << std::abs(tallest_idx - second_tallest_idx) + 1 << " " << std::endl;

    return 0;
}
