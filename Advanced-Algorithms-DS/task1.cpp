#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

class SegmentTree {
private:
    vector<int> tree;
    int size;

    void build(const vector<int>& data, int node, int start, int end) {
        if (start == end) {
            tree[node] = data[start];
        } else {
            int mid = (start + end) / 2;
            build(data, 2 * node + 1, start, mid);
            build(data, 2 * node + 2, mid + 1, end);
            tree[node] = max(tree[2 * node + 1], tree[2 * node + 2]);
        }
    }

    int query(int node, int start, int end, int l, int r, int value) {
        if (start > r || end < l || tree[node] < value) {
            return INT_MAX;
        }
        if (start == end) {
            return start;
        }
        int mid = (start + end) / 2;
        int left_result = query(2 * node + 1, start, mid, l, r, value);
        if (left_result != INT_MAX) {
            return left_result;
        }
        return query(2 * node + 2, mid + 1, end, l, r, value);
    }

public:
    SegmentTree(const vector<int>& data) {
        size = data.size();
        tree.resize(4 * size);
        build(data, 0, 0, size - 1);
    }

    int findFirstGE(int l, int r, int value) {
        return query(0, 0, size - 1, l, r, value);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Input reading
    int n, k;
    long long s;
    cin >> n >> k >> s;

    vector<int> timeline(n);
    for (int i = 0; i < n; ++i) {
        cin >> timeline[i];
    }

    vector<int> costs(k);
    for (int i = 0; i < k; ++i) {
        cin >> costs[i];
    }

    // Initial coins after buying the sword
    long long remaining_coins = s - timeline[0];

    // Build segment tree for timeline
    SegmentTree segTree(timeline);

    // Process each epic item cost
    vector<int> result(k);
    for (int i = 0; i < k; ++i) {
        if (costs[i] <= remaining_coins) {
            result[i] = 0;
        } else {
            long long required = costs[i] - remaining_coins;
            int idx = segTree.findFirstGE(1, n - 1, required); // Search from minute 1 onward
            result[i] = (idx == INT_MAX ? n : idx);
        }
    }

    // Output results
    for (int res : result) {
        cout << res << "\n";
    }

    return 0;
}
