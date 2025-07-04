from collections import defaultdict, deque, Counter
from functools import cache
# import copy
from itertools import combinations, permutations, product, accumulate, groupby, chain
from more_itertools import distinct_permutations
from heapq import heapify, heappop, heappush, heappushpop
import math
import bisect
from pprint import pprint
from random import randint, shuffle, randrange
from sortedcontainers import SortedSet, SortedList, SortedDict
import sys
sys.setrecursionlimit(2000000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353
def ceil_div(x, y): return -(-x//y)

#################################################   

class ZeroOne_on_Tree:

    class V(object):
        def __init__(self, zero, one, idx):
            self.zero = zero
            self.one = one
            self.idx = idx
        def __eq__(self, other):
            return self.one * other.zero == self.zero * other.one
        def __lt__(self, other):
            return self.one * other.zero < self.zero * other.one
        def __ne__(self, other):
            return not self.__eq__(other)
        def __le__(self, other):
            return self.__lt__(other) or self.__eq__(other)
        def __gt__(self, other):
            return not self.__le__(other)
        def __ge__(self, other):
            return not self.__lt__(other)
        def __iter__(self):
            yield self.zero
            yield self.one
            yield self.idx
        def merge(self, other):
            new_zero = self.zero + other.zero
            new_one = self.one + other.one
            inv = self.one * other.zero
            return ZeroOne_on_Tree.V(new_zero, new_one, self.idx), inv

    class UnionFind:
        def __init__(self, AA):
            self.n = len(AA)
            self.parents = [-1]*self.n
            self.V = [ZeroOne_on_Tree.V(a, 1, i) for i, a in enumerate(AA)]
            self.inv = 0
        def find(self, x):
            if self.parents[x] < 0:
                return x
            else:
                self.parents[x] = self.find(self.parents[x])
                return self.parents[x]
        def union(self, x, y):
            x = self.find(x)
            y = self.find(y)
            assert x != y
            self.parents[x] += self.parents[y]
            self.parents[y] = x
            v = self.V[x]
            nv, inv = self.V[x].merge(self.V[y])
            self.V[x] = nv
            self.inv += inv
            return v, nv
    
    def solve(P, A): # P は 1-indexed で与える！！
        PP = [0]+P
        AA = [0]+A
        uf = ZeroOne_on_Tree.UnionFind(AA)
        hq = uf.V[1:]
        heapify(hq)
        erased = set()
        for _ in range(len(A)):
            while tuple(hq[0]) in erased:
                erased.discard(tuple(heappop(hq)))
            x = heappop(hq).idx
            v, nv = uf.union(PP[x], x)
            if nv.idx != 0:
                heappush(hq, nv)
                erased.add(tuple(v))
        return uf.inv

# ABC376-G
T = int(input())
for _ in range(T):
    N = int(input())
    P = list(map(int, input().split()))
    A = list(map(int, input().split()))
    inv = ZeroOne_on_Tree.solve(P, A)
    print(inv % mod2 * pow(sum(A), -1, mod2) % mod2)