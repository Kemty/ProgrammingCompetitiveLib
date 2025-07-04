from 藤間ゼミ.SegmentTrees.persistentSegmentTree import PersistentSegmentTree

class OnLine_RangeMexQuery:
    
    def __init__(self, array) -> None:
        self.array = array
        self.pst = PersistentSegmentTree([-float("inf")]*len(array), min, float("inf"), 0)
        self._build()

    def _build(self):
        for r, a in enumerate(self.array):
            if a < len(self.array):
                self.pst.set(r, r+1, a, r)
            else:
                self.pst.copy(r, r+1)
    
    def prod(self, l, r):
        return self.pst.max_right(r, 0, lambda x: x >= l)

if __name__ == "__main__":
    array = [3, 1, 0, 2, 5, 3, 1]
    querys = [(3, 7), (0, 4), (2, 5), (1, 3)]
    on_rmq = OnLine_RangeMexQuery(array)
    for l, r in querys:
        print(on_rmq.prod(l, r))