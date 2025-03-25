def waiting_times(n, k, s, timeline, costs):
    output = [n] * k  # Default waiting time is `n` if no solution is found

    for j in range(k):  # Loop through each cost
        # Start with initial coins after buying sword
        remaining_coins = s - timeline[0]
        for i in range(n):  # Loop through timeline
            total_coins = remaining_coins + timeline[i]  # Add timeline value
            if total_coins >= costs[j]:  # If we can afford it
                output[j] = i
                break  # Stop looking for this cost once found

    return output


# Read input from input.txt
with open("input.txt", "r") as f:
    lines = f.readlines()

n, k, s = map(int, lines[0].split())
timeline = list(map(int, lines[1].split()))
costs = list(map(int, lines[2].split()))

# Validate input length
assert len(timeline) == n, "Error: timeline length mismatch"
assert len(costs) == k, "Error: costs length mismatch"

# Get the expected output from waiting_times function
output = waiting_times(n, k, s, timeline, costs)

# Write output to output.txt
with open("output.txt", "w") as f:
    for value in output:
        f.write(str(value) + "\n")

print("output.txt has been generated successfully.")
