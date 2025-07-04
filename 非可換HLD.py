class HLD:

    # https://github.com/shakayami/ACL-for-python/blob/master/segtree.py
    class segtree():
        n=1
        size=1
        log=2
        d=[0]
        op=None
        e=10**15
        def __init__(self,V,OP,E):
            self.n=len(V)
            self.op=OP
            self.e=E
            self.log=(self.n-1).bit_length()
            self.size=1<<self.log
            self.d=[E for i in range(2*self.size)]
            for i in range(self.n):
                self.d[self.size+i]=V[i]
            for i in range(self.size-1,0,-1):
                self.update(i)
        def set(self,p,x):
            assert 0<=p and p<self.n
            p+=self.size
            self.d[p]=x
            for i in range(1,self.log+1):
                self.update(p>>i)
        def get(self,p):
            assert 0<=p and p<self.n
            return self.d[p+self.size]
        def prod(self,l,r):
            assert 0<=l and l<=r and r<=self.n
            sml=self.e
            smr=self.e
            l+=self.size
            r+=self.size
            while(l<r):
                if (l&1):
                    sml=self.op(sml,self.d[l])
                    l+=1
                if (r&1):
                    smr=self.op(self.d[r-1],smr)
                    r-=1
                l>>=1
                r>>=1
            return self.op(sml,smr)
        def all_prod(self):
            return self.d[1]
        def max_right(self,l,f):
            assert 0<=l and l<=self.n
            assert f(self.e)
            if l==self.n:
                return self.n
            l+=self.size
            sm=self.e
            while(1):
                while(l%2==0):
                    l>>=1
                if not(f(self.op(sm,self.d[l]))):
                    while(l<self.size):
                        l=2*l
                        if f(self.op(sm,self.d[l])):
                            sm=self.op(sm,self.d[l])
                            l+=1
                    return l-self.size
                sm=self.op(sm,self.d[l])
                l+=1
                if (l&-l)==l:
                    break
            return self.n
        def min_left(self,r,f):
            assert 0<=r and r<=self.n
            assert f(self.e)
            if r==0:
                return 0
            r+=self.size
            sm=self.e
            while(1):
                r-=1
                while(r>1 and (r%2)):
                    r>>=1
                if not(f(self.op(self.d[r],sm))):
                    while(r<self.size):
                        r=(2*r+1)
                        if f(self.op(self.d[r],sm)):
                            sm=self.op(self.d[r],sm)
                            r-=1
                    return r+1-self.size
                sm=self.op(self.d[r],sm)
                if (r& -r)==r:
                    break
            return 0
        def update(self,k):
            self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
        def __str__(self):
            return str([self.get(i) for i in range(self.n)])

    def __init__(self, adj, op, e, root=0) -> None:
        self.n = len(adj)
        self.root = root
        self.parent = [None]*self.n
        stack = [root]
        tps = []
        while stack:
            u = stack.pop()
            tps.append(u)
            for v in adj[u]:
                adj[v].remove(u)
                self.parent[v] = u
                stack.append(v)
        size = [1]*self.n
        heavy = [None]*self.n
        for u in reversed(tps):
            ms = -inf
            for v in adj[u]:
                if size[v] > ms:
                    heavy[u] = v
                    ms = size[v]
                size[u] += size[v]
        del tps, size
        self.idx = [None]*self.n
        self.heavy_root = [None]*self.n
        stack = [(None, root)]
        i = 0
        while stack:
            p, u = stack.pop()
            self.idx[u] = i
            if p is not None:
                self.parent[i] = self.idx[p]
            if self.heavy_root[i] is None:
                self.heavy_root[i] = i
            for v in adj[u]:
                if v == heavy[u]: continue
                stack.append((u, v))
            if heavy[u] is not None:
                self.heavy_root[i+1] = self.heavy_root[i]
                stack.append((u, heavy[u]))
            i += 1
        self.vertex = [None]*self.n
        for u in range(self.n):
            self.vertex[self.idx[u]] = u
        array_td = [0]*self.n
        array_bu = [0]*self.n
        for u in range(N, N+N-1):
            array_td[self.idx[u]] = 1
            array_bu[self.n-1-self.idx[u]] = 1
        self.paths_td = self.segtree(array_td, op, e)
        self.paths_bu = self.segtree(array_bu, op, e)

    def prod(self, u, v):
        u, v = self.idx[u], self.idx[v]
        ret_u = self.paths_bu.e
        ret_v = self.paths_td.e
        while self.heavy_root[u] != self.heavy_root[v]:
            if u > v:
                ret_u = self.paths_bu.op(ret_u, self.paths_bu.prod(self.n-1-u, self.n-self.heavy_root[u]))
                u = self.parent[self.heavy_root[u]]
            else:
                ret_v = self.paths_td.op(self.paths_td.prod(self.heavy_root[v], v+1), ret_v)
                v = self.parent[self.heavy_root[v]]
        if u < v:
            return self.paths_td.op(ret_u, self.paths_td.op(self.paths_td.prod(u, v+1), ret_v))
        else:
            return self.paths_bu.op(ret_u, self.paths_bu.op(self.paths_bu.prod(self.n-1-u, self.n-v), ret_v))

    def set_td(self, u, w):
        self.paths_td.set(self.idx[u], w)
    
    def set_bu(self, u, w):
        self.paths_bu.set(self.n-1-self.idx[u], w)

    def lca(self, u, v):
        u, v = self.idx[u], self.idx[v]
        while self.heavy_root[u] != self.heavy_root[v]:
            if u > v:
                u = self.parent[self.heavy_root[u]]
            else:
                v = self.parent[self.heavy_root[v]]
        return self.vertex[min(u, v)]

    def through(self, u, v, x):
        u, v, x = self.idx[u], self.idx[v], self.idx[x]
        while self.heavy_root[u] != self.heavy_root[v]:
            if u > v:
                if self.heavy_root[u] <= x <= u: return True
                u = self.parent[self.heavy_root[u]]
            else:
                if self.heavy_root[v] <= x <= v: return True
                v = self.parent[self.heavy_root[v]]
        if u > v: u, v = v, u
        return u <= x <= v

N, M = map(int, input().split())
adj = [[] for _ in range(N+N-1)]
for i in range(N, N+N-1):
    p, q = map(int, input().split())
    p -= 1; q -= 1
    adj[p].append(i)
    adj[i].append(p)
    adj[q].append(i)
    adj[i].append(q)

hld = HLD(copy.deepcopy(adj), lambda x, y: x+y, 0)
for _ in range(M):
    query = tuple(input().split())
    if query[0] == "I":
        r, s, t = int(query[1])+N-1, int(query[2]), int(query[3])
        u, v = adj[r]
        if u > v: u, v = v, u
        if hld.idx[u] < hld.idx[v]:
            hld.set_td(r, s)
            hld.set_bu(r, t)
        else:
            hld.set_td(r, t)
            hld.set_bu(r, s)
    else:
        x, y = int(query[1])-1, int(query[2])-1
        print(hld.prod(x, y))
