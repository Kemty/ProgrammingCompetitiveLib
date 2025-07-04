# ABC186-E

from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
import math
import bisect
import sys
sys.setrecursionlimit(10**9)
input = sys.stdin.readline
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353

#################################################

xy = [None, None]
def extend_gcd(a, b, r=0):
    if b == 0:
        xy[r] = 1
        xy[r^1] = 0
        return a
    d = extend_gcd(b, a%b, r^1)
    xy[r^1] -= a//b*xy[r]
    return d

T = int(input())
ans = []
for _ in range(T):
    N, S, K = map(int, input().rstrip('\n').split())
    d = extend_gcd(K, -N)
    if (-S)%d != 0:
        ans.append(-1)
    else:
        xy[0] *= (-S)//d
        t = (-N)//d
        s = -(xy[0]//t)
        ans.append(xy[0]+s*t)
print(*ans, sep="\n")