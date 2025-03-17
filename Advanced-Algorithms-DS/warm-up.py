import sys


def secret_tunnel_length(n, heights):
    # Find the index of the highest tower.
    highest_index = 0
    for i in range(n):
        if heights[i] > heights[highest_index]:
            highest_index = i

    # Initialize second highest tower's index.
    # Ensure we pick a different index than the highest.
    if highest_index == 0:
        second_highest_index = 1
    else:
        second_highest_index = 0

    # Find the index of the second highest tower.
    for i in range(n):
        if i == highest_index:
            continue
        if heights[i] > heights[second_highest_index]:
            second_highest_index = i

    # Compute the secret tunnel length.
    # The distance is given by |index1 - index2| + 1.
    return abs(highest_index - second_highest_index) + 1


# The below part handles the input/output.
# Set SUBMIT_TO_SZKOPUL=True when submitting to the Szkopuł webserver.
SUBMIT_TO_SZKOPUL = True

if SUBMIT_TO_SZKOPUL:
    reader = sys.stdin
else:
    reader = open("input.txt", "r")

# Reads the input: first line gives n, second line gives n heights.
astr = reader.readline()
n = int(astr)
heights = [int(val) for val in reader.readline().split()]

if not SUBMIT_TO_SZKOPUL:
    reader.close()

# Compute the secret tunnel length.
output = secret_tunnel_length(n, heights)

# Write the result to standard output.
print(output, " ")
