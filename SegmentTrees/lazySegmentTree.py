from 藤間ゼミ.SegmentTrees.segmentTree import SegmentTree

class LazySegmentTree(SegmentTree):

    def __init__(self, array, op, e, mp, cp, idmp):

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
        self.root = self.Node(0, self.tree_length)
        super()._dfs_for_build(self.root, array)
    
    def _push(self, node):
        if node.R-node.L > 1:
            node.left_son.lazy = self.cp(node.lazy, node.left_son.lazy)
            node.right_son.lazy = self.cp(node.lazy, node.right_son.lazy)
        node.data = self.mp(node.lazy, node.data)
        node.lazy = self.idmp
        return node.data
    
    def get(self, i):
        assert 0 <= i < self.array_length
        return self._dfs_for_get(self.root, i)
    
    def _dfs_for_get(self, node, i):
        self._push(node)
        return self._dfs_for_get(node, i)
        
    def set(self, i, x):
        assert 0 <= i < self.array_length
        self._dfs_for_set(self.root, i, x)
    
    def _dfs_for_set(self, node, i, x):
        self._push(node)
        if node.R-node.L == 1:
            node.data = x
            return node.data
        mid = (node.L+node.R) >> 1
        if i < mid:
            node.data = self.op(self._dfs_for_set(node.left_son, i, x),
                                self._push(node.right_son))
        else:
            node.data = self.op(self._push(node.left_son),
                                self._dfs_for_set(node.right_son, i, x))
        return node.data
    
    def prod(self, l, r):
        assert 0 <= l <= r <= self.array_length
        if l == r: return self.e
        rednodes = []
        self._search_rednodes(self.root, l, r, rednodes)
        return super()._solve_prod(rednodes)
    
    def _search_rednodes(self, node, l, r, rednodes):
        self._push(node)
        if node.L == l and node.R == r:
            rednodes.append(node)
            return
        mid = (node.L+node.R) >> 1
        if r <= mid:
            self._search_rednodes(node.left_son, l, r, rednodes)
        elif mid <= l:
            self._search_rednodes(node.right_son, l, r, rednodes)
        else:
            self._search_rednodes(node.left_son, l, mid, rednodes)
            self._search_rednodes(node.right_son, mid, r, rednodes)

    def all_prod(self):
        self._push(self.root)
        return self.root.data

    def apply(self, l, r, f):
        assert 0 <= l < r <= self.array_length
        self._search_rednodes_for_apply(self.root, l, r, f)
    
    def _search_rednodes_for_apply(self, node, l, r, f):
        self._push(node)
        if node.L == l and node.R == r:
            node.lazy = f
            self._push(node)
            return node.data
        mid = (node.L+node.R) >> 1
        if r <= mid:
            node.data = self.op(self._search_rednodes_for_apply(node.left_son, l, r, f),
                                self._push(node.right_son))
        elif mid <= l:
            node.data = self.op(self._push(node.left_son),
                                self._search_rednodes_for_apply(node.right_son, l, r, f))
        else:
            node.data = self.op(self._search_rednodes_for_apply(node.left_son, l, mid, f),
                                self._search_rednodes_for_apply(node.right_son, mid, r, f))
        return node.data
    
    def all_apply(self, f):
        self.root.lazy = self.cp(f, self.root.lazy)
    
    def max_right(self, l, p):
        assert 0 <= l < self.array_length
        rednodes = []
        self._search_rednodes(self.root, l, self.array_length, rednodes)
        return self._solve_max_right(p, rednodes)
    
    def _solve_max_right(self, p, rednodes):
        acc = self.e
        for node in rednodes:
            if not p(self.op(acc, node.data)):
                while node.R-node.L > 1:
                    self._push(node.left_son)
                    if p(self.op(acc, node.left_son.data)):
                        acc = self.op(acc, node.left_son.data)
                        node = node.right_son
                        self._push(node)
                    else:
                        node = node.left_son
                return node.L
            acc = self.op(acc, node.data)
        return self.array_length
    
    def min_left(self, r, p):
        assert 0 < r <= self.array_length
        rednodes = []
        self._search_rednodes(self.root, 0, r, rednodes)
        return self._solve_min_left(p, rednodes)
    
    def _solve_min_left(self, p, rednodes):
        acc = self.e
        for node in reversed(rednodes):
            if not p(self.op(node.data, acc)):
                while node.R-node.L > 1:
                    self._push(node.right_son)
                    if p(self.op(node.right.data, acc)):
                        acc = self.op(node.right_son.data, acc)
                        node = node.left_son
                        self._push(node)
                    else:
                        node = node.right_son
                return node.R
            acc = self.op(node.data, acc)
        return 0
    
    def __repr__(self) -> str:
        leaves = []
        self._dfs_for_repr(self.root, leaves)
        return leaves.__repr__()
    
    def _dfs_for_repr(self, node, leaves):
        self._push(node)
        if node.R-node.L == 1:
            leaves.append(node.data)
            return
        self._dfs_for_repr(node.left_son, leaves)
        if node.right_son.L < self.array_length:
            self._dfs_for_repr(node.right_son, leaves)

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
    lst = LazySegmentTree([0]*W, max, -float("inf"), mp, cp, None)
    for _ in range(N):
        l, r = map(int, input().split())
        l -= 1
        h = lst.prod(l, r)
        print(h+1)
        lst.apply(l, r, h+1)
        print(lst)