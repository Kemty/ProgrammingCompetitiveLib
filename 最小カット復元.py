#ABC239-G

from collections import deque

class Dinic:

    def __init__(self, n, inf=float("inf")): # n: 頂点数, inf: minの単位元、十分大の整数にした方が速いかも
        self.V = n
        self.inf = inf
        self.G = [[] for _ in range(n)]
        self.dist = []
        self.search_from = []
        self.H = [[] for _ in range(n)] # 元グラフ(最小カット復元用)
    
    def add_edge(self, from_, to, cap): # 容量capの辺(from_, to)をグラフに追加
        self.G[from_].append([to, cap, len(self.G[to])])
        self.G[to].append([from_, 0, len(self.G[from_])-1])
        self.H[from_].append([to, cap])

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
    
    def cut_rest(self, s):
        seen = [False]*self.V
        seen[s] = True
        stack = [s]
        while stack:
            now = stack.pop()
            for next, cap, rev in self.G[now]:
                if not seen[next] and cap > 0:
                    seen[next] = True
                    stack.append(next)
        
        ret = set()
        for from_ in range(self.V):
            if seen[from_]:
                for to, cap in self.H[from_]:
                    if not seen[to]:
                        ret.add((from_, to))
        return ret

N, M = map(int,input().split())
g = Dinic(2*N-2)
for i in range(M):
    a, b = map(int,input().split())
    a, b = a-1, b-1
    if a > b:
        a, b = b, a
    if a == 0 and b == N-1:
        g.add_edge(a, 2*b-1, g.inf)
        g.add_edge(2*b-1, a, g.inf)
    elif a == 0:
        g.add_edge(a, 2*b-1, g.inf)
        g.add_edge(2*b, a, g.inf)
    elif b == N-1:
        g.add_edge(2*a, 2*b-1, g.inf)
        g.add_edge(2*b-1, 2*a-1, g.inf)
    else:
        g.add_edge(2*a, 2*b-1, g.inf)
        g.add_edge(2*b, 2*a-1, g.inf)
C = list(map(int,input().split()))
E = [0]*N
for i in range(1, N-1):
    g.add_edge(2*i-1, 2*i, C[i])

ans = g.max_flow(0, 2*N-3)
print(ans)

ans = []
E = g.cut_rest(0)
for a, b in E:
    ans.append(b//2+1)
print(len(ans))
print(*ans)