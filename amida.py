from collections import defaultdict, deque, Counter
from functools import cache
# import copy
from itertools import combinations, permutations, product, accumulate, groupby, chain
# from more_itertools import distinct_permutations
from heapq import heapify, heappop, heappush, heappushpop
import math
import bisect
# from pprint import pprint
from random import randint, shuffle, randrange
# from sortedcontainers import SortedSet, SortedList, SortedDict
import sys
# sys.setrecursionlimit(2000000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353
def ceil_div(x, y): return -(-x//y)

#################################################   

class Amida:

    BUCKET_SIZE = 100
    
    def __init__(self):
        self._kuji = dict()
        self.lines = [None]*Amida.BUCKET_SIZE
    
    def add(self, idx, x):
        lu, ru = self._up(idx, x)
        ld, rd = self._down(idx, x)
        self._kuji[lu] = rd
        self._kuji[ru] = ld
        self.lines[idx] = x
    
    def discard(self, idx, x):
        self.lines[idx] = None
        lu, ru = self._up(idx, x)
        ld, rd = self._down(idx, x)
        self._kuji[lu] = ld
        self._kuji[ru] = rd

    def kuji(self, x):
        if x not in self._kuji:
            return x
        return self._kuji[x]
    
    def _up(self, idx, x):
        lx = x
        rx = x+1
        for i in range(idx-1, -1, -1):
            if self.lines[i] is None: continue
            xx = self.lines[i]
            if xx == lx:
                lx += 1
            elif xx+1 == lx:
                lx -= 1
            if xx == rx:
                rx += 1
            elif xx+1 == rx:
                rx -= 1
        return lx, rx
    
    def _down(self, idx, x):
        lx = x
        rx = x+1
        for i in range(idx+1, Amida.BUCKET_SIZE):
            if self.lines[i] is None: continue
            xx = self.lines[i]
            if xx == lx:
                lx += 1
            elif xx+1 == lx:
                lx -= 1
            if xx == rx:
                rx += 1
            elif xx+1 == rx:
                rx -= 1
        return lx, rx

N, M = map(int, input().split())
Q = int(input())

E = []
xy = {}
querys = []
for i in range(Q):
    q = tuple(map(int, input().split()))
    querys.append(q)
    if q[0] == 1:
        _, x, y = q
        if (x, y) not in xy:
            E.append((y, i))
            xy[(x, y)] = i
E.sort()
bucket_idx = [None]*Q
c = 0
for _, i in E:
    bucket_idx[i] = divmod(c, Amida.BUCKET_SIZE)
    c += 1
Amidas = [Amida() for _ in range(ceil_div(c, Amida.BUCKET_SIZE))]

for i, query in enumerate(querys):
    if query[0] == 1:
        _, x, y = query
        j, k = bucket_idx[xy[(x, y)]]
        Amidas[j].add(k, x)
    elif query[0] == 2:
        _, x, y = query
        j, k = bucket_idx[xy[(x, y)]]
        Amidas[j].discard(k, x)
    else:
        _, x = query
        for amida in Amidas:
            x = amida.kuji(x)
        print(x)