from 藤間ゼミ.SegmentTrees.segmentTree import SegmentTree

class PersistentSegmentTree(SegmentTree):
    
    def __init__(self, array, op, e, v):

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
        self.versions = {v: self.Node(0, self.tree_length)}
        super()._dfs_for_build(self.versions[v], array)
    
    def get(self, v, i):
        assert v in self.versions and 0 <= i < self.array_length
        return super()._dfs_for_get(self.versions[v], i)
    
    def set(self, u, v, i, x):
        assert u in self.versions and v not in self.versions
        assert 0 <= i < self.array_length
        self.versions[v] = self.Node(0, self.tree_length)
        self._dfs_for_set(self.versions[u], self.versions[v], i, x)
    
    def _dfs_for_set(self, u_node, v_node, i, x):
        if u_node.R-u_node.L == 1:
            v_node.data = x
            return x
        mid = (u_node.L+u_node.R) >> 1
        if i < mid:
            v_node.left_son = self.Node(v_node.L, mid)
            v_node.right_son = u_node.right_son
            v_node.data = self.op(self._dfs_for_set(u_node.left_son, v_node.left_son, i, x),
                                  v_node.right_son.data)
        else:
            v_node.left_son = u_node.left_son
            v_node.right_son = self.Node(mid, v_node.R)
            v_node.data = self.op(v_node.left_son.data,
                                  self._dfs_for_set(u_node.right_son, v_node.right_son, i, x))
        return v_node.data
    
    def prod(self, v, l, r):
        assert v in self.versions and 0 <= l <= r <= self.array_length
        if l == r: return self.e
        rednodes = []
        super()._search_rednodes(self.versions[v], l, r, rednodes)
        return super()._solve_prod(rednodes)
    
    def all_prod(self, v):
        assert v in self.versions
        return self.versions[v].data
    
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
    
    def copy(self, u, v): # 更新なしでバージョンだけ新しく作る
        assert u in self.versions and v not in self.versions
        self.versions[v] = self.versions[u]
    
    def __repr__(self) -> str:
        ret = {}
        for v, root in self.versions.items():
            leaves = []
            super()._dfs_for_repr(root, leaves)
            ret[v] = leaves
        return ret.__repr__()

if __name__ == "__main__":

    # モノイドの演算
    def op(x, y):
        return x+y
    
    # 単位元
    e = 0

    array = [3, 1, 4, 1, 5, 9, 2]
    pst = PersistentSegmentTree(array, op, e, 0)
    print(pst)
    print(pst.prod(0, 2, 7))
    pst.set(0, 1, 5, 3)
    print(pst)
    print(pst.prod(1, 2, 7))
    print(pst.prod(0, 2, 7))