import sys


class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.data = data
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.max_tree = [-float('inf')] * (2 * self.size)
        for i in range(self.n):
            self.max_tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.max_tree[i] = max(self.max_tree[2 * i],
                                   self.max_tree[2 * i + 1])

    def find_first_ge(self, x):
        if self.max_tree[1] < x:
            return self.n
        return self._find_first_ge(1, 0, self.size - 1, x)

    def _find_first_ge(self, node, l, r, x):
        if l == r:
            return l if self.max_tree[node] >= x else self.n
        mid = (l + r) // 2
        left_node = 2 * node
        if self.max_tree[left_node] >= x:
            left_result = self._find_first_ge(left_node, l, mid, x)
            if left_result != self.n:
                return left_result
        right_node = 2 * node + 1
        return self._find_first_ge(right_node, mid + 1, r, x)


def main():
    data = list(map(int, sys.stdin.read().split()))
    ptr = 0
    n = data[ptr]
    ptr += 1
    k = data[ptr]
    ptr += 1
    s = data[ptr]
    ptr += 1
    timeline = data[ptr:ptr + n]
    ptr += n
    costs = data[ptr:ptr + k]
    ptr += k

    remaining_s = s - timeline[0]
    st = SegmentTree(timeline)

    output = []
    for cost in costs:
        if cost <= remaining_s:
            output.append(0)
        else:
            required = cost - remaining_s
            idx = st.find_first_ge(required)
            output.append(idx if idx != st.n else n)

    for num in output:
        print(num)


if __name__ == '__main__':
    main()
