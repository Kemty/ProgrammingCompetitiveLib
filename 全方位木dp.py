from collections import defaultdict, deque, Counter
from itertools import permutations, product
from heapq import heapify, heappop, heappush
import math
import bisect
import sys
sys.setrecursionlimit(700000)
input = lambda: sys.stdin.readline().rstrip('\n')
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353

#################################################

# EDPC-V

class TreeDP_all:

    def __init__(self, adj, root, merge, e, modify_bu, modify_td, modify_fin) -> None:
        """
        adj: 隣接リスト
        root: 根
        merge(x, y): 2つの部分木情報x, y(調整済み)をマージする関数
        e: mergeの単位元
        modify_bu(x, i): ボトムアップ中、部分木情報x (根はi)の情報を配る用に調整する関数
        modify_td(x, i, p): トップダウン中、部分木情報x (根はpで、頂点iと反対側の部分木)の情報を頂点i に配る用に調整する関数
        modify_fin(x, i): 最後に、頂点i のもつ情報x を真に求めったかった値に調整する関数(dp遷移には影響しない)
        """
        self.N = len(adj)
        self.adj = adj
        self.root = root
        self.merge = merge
        self.e = e
        self.modify_bu = modify_bu
        self.modify_td = modify_td
        self.modify_fin = modify_fin
        self.parent, self.son, self.tps = self.setup()
        self.res = self.run()
    
    def setup(self):
        parent = [None]*self.N
        son = [[] for _ in range(self.N)]
        tps = []
        dq = deque([self.root])
        while dq:
            now = dq.pop()
            tps.append(now)
            for next in self.adj[now]:
                if next == parent[now]: continue
                son[now].append(next)
                parent[next] = now
                dq.appendleft(next)
        return parent, son, tps
    
    def run(self):
        acc = [self.e]*self.N
        res = [None]*self.N
        for i in reversed(self.tps[1:]):
            res[i] = self.modify_bu(acc[i], i)
            acc[self.parent[i]] = self.merge(acc[self.parent[i]], res[i])
        res[self.tps[0]] = self.modify_fin(acc[self.tps[0]], self.tps[0])
        res_td = [self.e]*self.N
        for i in self.tps:
            ac = res_td[i]
            for j in self.son[i]:
                res_td[j] = ac
                ac = self.merge(ac, res[j])
            ac = self.e
            for j in reversed(self.son[i]):
                res_td[j] = self.modify_td(self.merge(res_td[j], ac), j, i)
                ac = self.merge(ac, res[j])
                res[j] = self.modify_fin(self.merge(acc[j], res_td[j]), j)
        return res

N, M = map(int, input().split())
adj = [[] for _ in range(N)]
for _ in range(N-1):
    x, y = map(int, input().split())
    x -= 1; y -= 1
    adj[x].append(y)
    adj[y].append(x)

dp = TreeDP_all(adj, 0, lambda x, y: x*y%M, 1, lambda x, i: (x+1)%M, lambda x, i, p: (x+1)%M, lambda x, i: x)
print(*dp.res, sep="\n")