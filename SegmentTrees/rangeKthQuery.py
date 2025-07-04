from 藤間ゼミ.SegmentTrees.persistentSegmentTree import PersistentSegmentTree

class RangeKthQuery:
    
    def __init__(self, array) -> None:
        self.length = len(array)
        self.decomp = sorted(set(array))
        self.comp = {a: i for i, a in enumerate(self.decomp)}
        self.st = PersistentSegmentTree([0]*len(self.comp), lambda x, y: x+y, 0, 0)
        cnt = [0]*len(self.comp)
        for r, a in enumerate(array):
            a = self.comp[a]
            cnt[a] += 1
            self.st.set(r, r+1, a, cnt[a])
    
    def prod(self, l, r, k):
        assert 0 <= l < r <= self.length and 0 <= k < r-l
        l_node, r_node = self.st.versions[l], self.st.versions[r]
        l_acc, r_acc = 0, 0
        while l_node.R-l_node.L > 1:
            if (r_acc+r_node.left_son.data)-(l_acc+l_node.left_son.data) <= k:
                l_acc += l_node.left_son.data
                l_node = l_node.right_son
                r_acc += r_node.left_son.data
                r_node = r_node.right_son
            else:
                l_node = l_node.left_son
                r_node = r_node.left_son
        return self.decomp[l_node.L]

if __name__ == "__main__":
    array = [3, 1, 4, 1, 5, 9, 2]
    rkq = RangeKthQuery(array)
    print(rkq.prod(1, 6, 2))