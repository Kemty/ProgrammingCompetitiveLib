class SegmentTree:
    
    def __init__(self, array, op, e):

        class Node:
            def __init__(self, L, R, data=e):
                self.L = L
                self.R = R
                self.data = data
                self.left_son = None
                self.right_son = None

        self.Node = Node
        self.op = op
        self.e = e
        self.array_length = len(array)
        self.tree_length = 1 << (self.array_length-1).bit_length()
        self.root = self.Node(0, self.tree_length, e)
        self._dfs_for_build(self.root, array)
    
    def _dfs_for_build(self, node, array):
        if node.R-node.L == 1:
            if node.L < self.array_length:
                node.data = array[node.L]
        else:
            mid = (node.L+node.R) >> 1
            node.left_son = self.Node(node.L, mid)
            node.right_son = self.Node(mid, node.R)
            node.data = self.op(self._dfs_for_build(node.left_son, array),
                                self._dfs_for_build(node.right_son, array))
        return node.data

    def get(self, i):
        assert 0 <= i < self.array_length
        return self._dfs_for_get(self.root, i)

    def _dfs_for_get(self, node, i):
        while node.R-node.L > 1:
            mid = (node.L+node.R) >> 1
            if i < mid:
                node = node.left_son
            else:
                node = node.right_son
        return node.data
    
    def set(self, i, x):
        assert 0 <= i < self.array_length
        self._dfs_for_set(self.root, i, x)
    
    def _dfs_for_set(self, node, i, x):
        if node.R-node.L == 1:
            node.data = x
            return x
        mid = (node.L+node.R) >> 1
        if i < mid:
            node.data = self.op(self._dfs_for_set(node.left_son, i, x),
                                node.right_son.data)
        else:
            node.data = self.op(node.left_son.data,
                                self._dfs_for_set(node.right_son, i, x))
        return node.data
    
    def prod(self, l, r):
        assert 0 <= l <= r <= self.array_length
        if l == r: return self.e
        rednodes = []
        self._search_rednodes(self.root, l, r, rednodes)
        return self._solve_prod(rednodes)
    
    def _search_rednodes(self, node, l, r, rednodes):
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
    
    def _solve_prod(self, rednodes):
        ret = self.e
        for node in rednodes:
            ret = self.op(ret, node.data)
        return ret
    
    def all_prod(self):
        return self.root.data
    
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
                    if p(self.op(acc, node.left_son.data)):
                        acc = self.op(acc, node.left_son.data)
                        node = node.right_son
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
                    if p(self.op(node.right_son.data, acc)):
                        acc = self.op(node.right_son.data, acc)
                        node = node.left_son
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
        if node.R-node.L == 1:
            leaves.append(node.data)
            return
        self._dfs_for_repr(node.left_son, leaves)
        if node.right_son.L < self.array_length:
            self._dfs_for_repr(node.right_son, leaves)

if __name__ == "__main__":

    # モノイドの演算
    def op(x, y):
        return x+y
    
    # 単位元
    e = 0

    array = [3, 1, 4, 1, 5, 9, 2]
    st = SegmentTree(array, op, e)
    print(st)
    print(st.prod(2, 7))
    st.set(5, 3)
    print(st)
    print(st.prod(2, 7))

    def p(x):
        return x <= 5

    print(st.max_right(2, p))
    print(st.min_left(4, p))