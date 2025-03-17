#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int num_blocks;
    std::cin >> num_blocks;

    std::vector<int> block_heights(num_blocks);
    for (int k = 0; k < num_blocks; ++k) {
        std::cin >> block_heights[k];
    }

    int highest_block_idx = 0;
    int second_highest_block_idx = -1;

    for (int k = 0; k < num_blocks; ++k) {
        if (block_heights[k] > block_heights[highest_block_idx]) {
            second_highest_block_idx = highest_block_idx;
            highest_block_idx = k;
        } else if (second_highest_block_idx == -1 || block_heights[k] > block_heights[second_highest_block_idx]) {
            if (k != highest_block_idx) {
                second_highest_block_idx = k;
            }
        }
    }

    std::cout << std::abs(highest_block_idx - second_highest_block_idx) + 1 << " " << std::endl;

    return 0;
}