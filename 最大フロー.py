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

# ABC010-D

from collections import deque

class Dinic:

    def __init__(self, n, inf=float("inf")): # n: 頂点数, inf: minの単位元、十分大の整数にした方が速いかも
        self.V = n
        self.inf = inf
        self.G = [[] for _ in range(n)]
        self.dist = []
        self.search_from = []
    
    def add_edge(self, from_, to, cap): # 容量capの辺(from_, to)をグラフに追加
        self.G[from_].append([to, cap, len(self.G[to])])
        self.G[to].append([from_, 0, len(self.G[from_])-1])

    def _bfs(self, s, t):
        self.dist = [-1]*self.V
        self.dist[s] = 0
        dq = deque([s])
        while dq:
            now = dq.pop()
            for edge in self.G[now]:
                next, cap, _ = edge
                if cap > 0 and self.dist[next] < 0:
                    self.dist[next] = self.dist[now]+1
                    if next == t: return True
                    dq.appendleft(next)
        return False

    def _dfs(self, s, t):
        stack = [t]
        goal = False
        flow = self.inf
        while stack:
            now = stack.pop()
            if now >= 0:
                if now == s:
                    goal = True
                    continue
                i = self.search_from[now]
                while i < len(self.G[now]):
                    self.search_from[now] = i
                    pre, _, rev = self.G[now][i]
                    _, cap, _ = self.G[pre][rev]
                    if cap > 0 and self.dist[now] > self.dist[pre] >= 0:
                        stack.append(~now)
                        stack.append(pre)
                        break
                    i += 1
            else:
                now = ~now
                if goal:
                    i = self.search_from[now]
                    pre, _, rev = self.G[now][i]
                    flow = min(flow, self.G[pre][rev][1])
                    continue
                else:
                    i = self.search_from[now]+1
                    while i < len(self.G[now]):
                        self.search_from[now] = i
                        pre, _, rev = self.G[now][i]
                        _, cap, _ = self.G[pre][rev]
                        if cap > 0 and self.dist[now] > self.dist[pre] >= 0:
                            stack.append(~now)
                            stack.append(pre)
                            break
                        i += 1
        if not goal: return 0
        now = t
        while now != s:
            i = self.search_from[now]
            pre, _, rev = self.G[now][i]
            self.G[now][i][1] += flow
            self.G[pre][rev][1] -= flow
            now = pre
        return flow

    def max_flow(self, s, t): # sからtへの最大流を求める
        flow = 0
        while True:
            if not self._bfs(s, t): return flow
            self.search_from = [0]*self.V
            f = self._dfs(s, t)
            while f > 0:
                flow += f
                f = self._dfs(s, t)

class Ford_fulkerson:
    def __init__(self, n, inf=float("inf")):
        self.V = n
        self.inf = inf
        self.G = [[] for _ in range(n)]
        self.used = []
    
    def add_edge(self, from_, to, cap):
        self.G[from_].append([to, cap, len(self.G[to])])
        self.G[to].append([from_, 0, len(self.G[from_])-1])
    
    def _dfs(self, now, t, flow):
        if now == t:
            return flow
        for i in range(len(self.G[now])):
            next, cap, rev = self.G[now][i]
            if not self.used[next] and cap > 0:
                self.used[next] = True
                d = self._dfs(next, t, min(flow, cap))
                if d > 0:
                    self.G[now][i][1] -= d
                    self.G[next][rev][1] += d
                    return d
        return 0
    
    def max_flow(self, s, t):
        flow = 0
        while True:
            self.used = [False]*self.V
            f = self._dfs(s, t, self.inf)
            if f > 0:
                flow += f
                continue
            return flow

if __name__ == "__main__":
    N, G, E = map(int,input().split())
    P = list(map(int,input().split()))
    g = Dinic(N+1)
    for p in P:
        g.add_edge(p, N, 1)
    for _ in range(E):
        a, b = map(int,input().split())
        g.add_edge(a, b, 1)
        g.add_edge(b, a, 1)
    print(g.max_flow(0, N))