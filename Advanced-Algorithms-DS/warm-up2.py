import sys


def find_tunnel_length(num_towers, tower_heights):
    tallest_index = 0
    for idx in range(num_towers):
        if tower_heights[idx] > tower_heights[tallest_index]:
            tallest_index = idx

    second_tallest_index = 1 if tallest_index == 0 else 0
    for idx in range(num_towers):
        if idx != tallest_index and tower_heights[idx] > tower_heights[second_tallest_index]:
            second_tallest_index = idx

    return abs(tallest_index - second_tallest_index) + 1


input_source = sys.stdin

total_towers = int(input_source.readline())
heights_list = [int(value) for value in input_source.readline().split()]

tunnel_distance = find_tunnel_length(total_towers, heights_list)
print(tunnel_distance, " ")
