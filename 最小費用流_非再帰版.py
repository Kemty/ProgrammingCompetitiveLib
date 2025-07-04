# ABC004-D

from heapq import heapify, heappop, heappush

class Flow:
    def __init__(self, n, inf=float("inf")):
        self.V = n
        self.inf = inf
        self.G = [[] for _ in range(n)]
        self.H = [] #ポテンシャル
        self.pre = [] # dijkstra経路復元用
    
    def add_edge(self, from_, to, cap, cost):
        #cost(1つ目):負辺除去後コスト, cost(2つ目):元コスト
        self.G[from_].append([to, cap, len(self.G[to]), cost, cost])
        self.G[to].append([from_, 0, len(self.G[from_])-1, -cost, -cost])
    
    def dijkstra(self, s):
        self.pre = [None]*self.V
        hq = [(0, s)]
        self.H[s] = 0
        while hq:
            d, now = heappop(hq)
            if d > self.H[now]:
                continue
            for i in range(len(self.G[now])):
                next, cap, r, cost, c = self.G[now][i]
                if cap > 0 and self.H[now]+cost < self.H[next]:
                    self.H[next] = self.H[now]+cost
                    self.pre[next] = (now, i)
                    heappush(hq, (self.H[next], next))
    
    def rest(self, s, t, flow):
        now = t
        while now != s and self.pre[now] is not None:
            p, i = self.pre[now]
            flow = min(flow, self.G[p][i][1])
            now = p
        if flow == 0 or now != s:
            return 0, 0
        now = t
        ret = 0
        while now != s:
            p, i = self.pre[now]
            next, cap, rev, c, cost = self.G[p][i]
            self.G[p][i][1] -= flow
            self.G[now][rev][1] += flow
            ret += cost*flow
            now = p
        return flow, ret
    
    def minimum_cost_flow(self, s, t, F):
        flow = 0
        ans = 0
        while F-flow > 0:
            self.H = [self.inf]*self.V
            self.dijkstra(s)
            for i in range(self.V):
                for j in range(len(self.G[i])):
                    self.G[i][j][3] += self.H[i]-self.H[self.G[i][j][0]]
            f, a = self.rest(s, t, F-flow)
            if f == 0:
                return -1
            ans += a
            flow += f
        return ans

def main():
    R, G, B = map(int,input().split())
    g = Flow(1003)
    g.add_edge(1001, 400, R, 0)
    g.add_edge(1001, 500, G, 0)
    g.add_edge(1001, 600, B, 0)
    for i in range(1001):
        g.add_edge(i, 1002, 1, 0)
        if i != 1000:
            g.add_edge(i, i+1, g.inf, 1)
            g.add_edge(i+1, i, g.inf, 1)
    print(g.minimum_cost_flow(1001, 1002, R+G+B))

if __name__ == "__main__":
    main()