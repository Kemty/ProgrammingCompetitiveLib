from collections import defaultdict, deque, Counter
from itertools import permutations, product
from heapq import heapify, heappop, heappush
import itertools
import math
import bisect
from pprint import pprint
import sys
sys.setrecursionlimit(700000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353

#################################################

# ABC242-G

N = int(input())
A = list(map(int, input().split()))
querys = [defaultdict(list) for _ in range(1<<10)]
Q = int(input())
for i in range(Q):
    l, r = map(int, input().split())
    l -= 1
    querys[l>>8][r].append((l, i))

def add(idx):
    global a
    a += cnt[A[idx]]
    cnt[A[idx]] ^= 1

def pop(idx):
    global a
    cnt[A[idx]] ^= 1
    a -= cnt[A[idx]]

ans = [None]*Q
a = 0
cnt = [0]*(N+1)
nl, nr = 0, 0
rev = 1
for qs in querys:
    if not qs: continue
    rev ^= 1
    for r in sorted(qs.keys(), reverse=rev):
        for l, i in qs[r]:
            while nl < l: pop(nl); nl += 1
            while nl > l: nl -= 1; add(nl)
            while nr < r: add(nr); nr += 1
            while nr > r: nr -= 1; pop(nr)
            ans[i] = a
print(*ans, sep="\n")