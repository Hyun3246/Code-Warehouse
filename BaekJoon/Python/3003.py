import sys

K, Q, R, B, N, P = map(int, sys.stdin.readline().split())

print(1-K, 1-Q, 2-R, 2-B, 2-N, 8-P)
