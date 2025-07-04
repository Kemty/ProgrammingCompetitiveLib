from collections import defaultdict, deque, Counter
from itertools import combinations, permutations, product, accumulate
from heapq import heapify, heappop, heappush
import math
import bisect
import sys
# sys.setrecursionlimit(700000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353
def seil_div(x, y): return -(-x//y)

#################################################

# ABC291-Ex

N = int(input())
adj = [[] for _ in range(N)]
for _ in range(N-1):
    a, b = map(int, input().split())
    a -= 1; b -= 1
    adj[a].append(b)
    adj[b].append(a)

size = [None]*N
next_node = [(-inf, -inf)]*N
is_bloked = [False]*N
ans = [-2]*N

def find_centroid(p, s):
    ss = subtree_size(p, s)
    if ss == 1:
        return s
    t = s
    while next_node[t][0]*2 > ss:
        t = next_node[t][1]
    is_bloked[t] = True
    for u in adj[t]:
        if is_bloked[u]: continue
        ans[find_centroid(t, u)] = t
    return t

def subtree_size(p, s):
    tps = []
    stack = [(p, s)]
    while stack:
        p, u = stack.pop()
        tps.append((p, u))
        for v in adj[u]:
            if v == p or is_bloked[v]: continue
            stack.append((u, v))
    for p, u in reversed(tps):
        size[u] = 1
        next_node[u] = (-inf, -inf)
        for v in adj[u]:
            if v == p or is_bloked[v]: continue
            size[u] += size[v]
            next_node[u] = max(next_node[u], (size[v], v))
    return size[s]

find_centroid(None, 0)
ans = list(map(lambda x: x+1, ans))
print(*ans)