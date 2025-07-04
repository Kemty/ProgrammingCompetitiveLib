from 藤間ゼミ.SegmentTrees.lazySegmentTree import LazySegmentTree

class PersistentLazySegmentTree(LazySegmentTree):

    def __init__(self, array, op, e, mp, cp, idmp, v):

        class Node:
            def __init__(self, L, R, data=e, lazy=idmp):
                self.L = L
                self.R = R
                self.data = data
                self.lazy = lazy
                self.left_son = None
                self.right_son = None

        self.Node = Node
        self.op = op
        self.e = e
        self.mp = mp
        self.cp = cp
        self.idmp = idmp
        self.array_length = len(array)
        self.tree_length = 1 << (self.array_length-1).bit_length()
        self.versions = {v: self.Node(0, self.tree_length)}
        super()._dfs_for_build(self.versions[v], array)
    
    def _push(self, node):
        if node.lazy == self.idmp:
            return node.data
        if node.R-node.L > 1:
            mid = (node.L+node.R) >> 1
            lls = node.left_son.left_son
            lrs = node.left_son.right_son
            rls = node.right_son.left_son
            rrs = node.left_son.right_son
            node.left_son = self.Node(node.L, mid, data=node.left_son.data, lazy=self.cp(node.lazy, node.left_son.lazy))
            node.left_son.left_son = lls
            node.left_son.right_son = lrs
            node.right_son = self.Node(mid, node.R, data=node.right_son.data, lazy=self.cp(node.lazy, node.right_son.lazy))
            node.right_son.left_son = rls
            node.right_son.right_son = rrs
        node.data = self.mp(node.lazy, node.data)
        node.lazy = self.idmp
        return node.data

    def get(self, v, i):
        assert v in self.versions and 0 <= i < self.array_length
        return self._dfs_for_get(self.versions[v], i)
    
    def _dfs_for_get(self, node, i):
        while node.R-node.L > 1:
            self._push(node)
            mid = (node.L+node.R) >> 1
            if i < mid:
                node = node.left_son
            else:
                node = node.right_son
        self._push(node)
        return node.data
        
    def set(self, u, v, i, x):
        assert u in self.versions and v not in self.versions
        assert 0 <= i < self.array_length
        self.versions[v] = self.Node(0, self.tree_length)
        self._dfs_for_set(self.versions[u], self.versions[v], i, x)
    
    def _dfs_for_set(self, u_node, v_node, i, x):
        self._push(u_node)
        if u_node.R-u_node.L == 1:
            v_node.data = x
            return v_node.data
        mid = (u_node.L+u_node.R) >> 1
        if i < mid:
            v_node.left_son = self.Node(v_node.L, mid)
            v_node.right_son = u_node.right_son
            v_node.data = self.op(self._dfs_for_set(v_node.left_son, i, x),
                                self._push(v_node.right_son))
        else:
            v_node.left_son = u_node.left_son
            v_node.right_son = self.Node(mid, v_node.R)
            v_node.data = self.op(self._push(v_node.left_son),
                                self._dfs_for_set(v_node.right_son, i, x))
        return v_node.data
    
    def prod(self, v, l, r):
        assert v in self.versions and 0 <= l <= r <= self.array_length
        if l == r: return self.e
        rednodes = []
        super()._search_rednodes(self.versions[v], l, r, rednodes)
        return super()._solve_prod(rednodes)

    def all_prod(self, v):
        assert v in self.versions
        self._push(self.versions[v])
        return self.versions[v].data

    def apply(self, u, v, l, r, f):
        assert u in self.versions and v not in self.versions
        assert 0 <= l < r <= self.array_length
        u_node = self.versions[u]
        v_node = self.Node(0, self.tree_length)
        self.versions[v] = v_node
        self._search_rednodes_for_apply(u_node, v_node, l, r, f)
    
    def _search_rednodes_for_apply(self, u_node, v_node, l, r, f):
        self._push(u_node)
        v_node.data = u_node.data
        if l == u_node.L and r == u_node.R:
            if v_node.R-v_node.L > 1:
                v_node.left_son = u_node.left_son
                v_node.right_son = u_node.right_son
            v_node.lazy = f
            self._push(v_node)
            return v_node.data
        mid = (u_node.L+u_node.R) >> 1
        if r <= mid:
            v_node.left_son = self.Node(v_node.L, mid)
            v_node.right_son = u_node.right_son
            v_node.data = self.op(self._search_rednodes_for_apply(u_node.left_son, v_node.left_son, l, r, f),
                                  self._push(v_node.right_son))
        elif mid <= l:
            v_node.left_son = u_node.left_son
            v_node.right_son = self.Node(mid, v_node.R)
            v_node.data = self.op(self._push(v_node.left_son),
                                  self._search_rednodes_for_apply(u_node.right_son, v_node.right_son, l, r, f))
        else:
            v_node.left_son = self.Node(v_node.L, mid)
            v_node.right_son = self.Node(mid, v_node.R)
            v_node.data = self.op(self._search_rednodes_for_apply(u_node.left_son, v_node.left_son, l, mid, f),
                                  self._search_rednodes_for_apply(u_node.right_son, v_node.right_son, mid, r, f))
        return v_node.data
    
    def all_apply(self, u, v, f):
        assert u in self.versions and v not in self.versions
        u_node = self.versions[u]
        v_node = self.Node(0, self.tree_length, data=u_node.data, lazy=self.cp(f, u_node.lazy))
        v_node.left_son = u_node.left_son
        v_node.right_son = u_node.right_son
        self.versions[v] = v_node
    
    def max_right(self, v, l, p):
        assert v in self.versions and 0 <= l < self.array_length
        rednodes = []
        super()._search_rednodes(self.versions[v], l, self.array_length, rednodes)
        return super()._solve_max_right(p, rednodes)
    
    def min_left(self, v, r, p):
        assert v in self.versions and 0 < r <= self.array_length
        rednodes = []
        super()._search_rednodes(self.versions[v], 0, r, rednodes)
        return super()._solve_min_left(p, rednodes)
    
    def __repr__(self) -> str:
        ret = {}
        for v, root in self.versions.items():
            leaves = []
            super()._dfs_for_repr(root, leaves)
            ret[v] = leaves
        return ret.__repr__()

if __name__ == "__main__":

    # https://atcoder.jp/contests/typical90/tasks/typical90_ac

    def mp(f, x):
        if f is None:
            return x
        return f
    
    def cp(f, g):
        if f is None:
            return g
        return f

    W, N = map(int, input().split())
    plst = PersistentLazySegmentTree([0]*W, max, -float("inf"), mp, cp, None, 0)
    for i in range(N):
        l, r = map(int, input().split())
        l -= 1
        h = plst.prod(i, l, r)
        print(h+1)
        plst.apply(i, i+1, l, r, h+1)
        print(plst)