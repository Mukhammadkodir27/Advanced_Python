import sys

rd = sys.stdin.readline
nm = int(rd())
ht = list(map(int, rd().split()))

mx_idx = 0
sec_mx_idx = -1

for k in range(nm):
    if ht[k] > ht[mx_idx]:
        sec_mx_idx = mx_idx
        mx_idx = k
    elif sec_mx_idx == -1 or ht[k] > ht[sec_mx_idx]:
        if k != mx_idx:
            sec_mx_idx = k

print(abs(mx_idx - sec_mx_idx) + 1, " ")
