from collections import defaultdict, deque, Counter
from functools import cache
# import copy
from itertools import combinations, permutations, product, accumulate, groupby, chain
from more_itertools import distinct_permutations
from heapq import heapify, heappop, heappush, heappushpop
import math
import bisect
# from pprint import pprint
from random import randint, shuffle, randrange
from sortedcontainers import SortedSet, SortedList, SortedDict
import sys
# sys.setrecursionlimit(2000000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353
def ceil_div(x, y): return -(-x//y)

#################################################   

class UnionFind:
    #コンストラクタ
    def __init__(self, n):
        self.n = n
        self.parents = [-1]*n

    #点xの根を調べる+親が根になるよう移動
    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    #点x,yの属する集合同士を連結(要素数が少ない方を多い方に連結)
    #辺を追加したらTrue, しなければFalseを返す
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x
        return True

    #点xが属する集合の要素数を取得
    def size(self, x):
        return -self.parents[self.find(x)]

    #点x,yが同じ集合に属しているか判定
    def same(self, x, y):
        return self.find(x) == self.find(y)

    #点xの属する集合の全要素を取得
    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    #根になっている全要素を取得
    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    #集合の数を取得
    def group_count(self):
        return len(self.roots())

    #全集合の「根と全要素」を取得
    def get_groups(self):
        groups = defaultdict(list)
        for x in range(self.n):
            groups[self.find(x)].append(x)
        return groups

    #print(インスタンス)で、全集合の「根と全要素」を出力
    def __str__(self):
        return '\n'.join('{}:{}'.format(r, self.menbers(r)) for r in self.roots())

def parallel_binary_search():
    oks, ngs = [M+1]*Q, [-1]*Q
    while True:
        exit_flag = True
        mids = [[] for _ in range(M+1)]
        for q in range(Q):
            if abs(oks[q]-ngs[q]) > 1:
                exit_flag = False
                mid = (oks[q]+ngs[q])>>1
                mids[mid].append(q)
        if exit_flag:
            return oks
        
        uf = UnionFind(N)
        for mid in range(M):
            for q in mids[mid]:
                x, y = querys[q]
                if uf.same(x, y):
                    oks[q] = mid
                else:
                    ngs[q] = mid
            a, b = E[mid]
            uf.union(a, b)
        for q in mids[M]:
            x, y = querys[q]
            if uf.same(x, y):
                oks[q] = M
            else:
                ngs[q] = M

N, M = map(int, input().split())
E = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(M)]

Q = int(input())
querys = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(Q)]
ans = parallel_binary_search()
for a in ans:
    if a == M+1:
        print(-1)
    else:
        print(a)
