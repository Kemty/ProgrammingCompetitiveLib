from 藤間ゼミ.SegmentTrees.segmentTree import SegmentTree

class OffLine_RangeMexQuery:
    
    def solve(array, querys) -> list:
        st = SegmentTree([-float("infinity")]*len(array), min, float("infinity"))
        ret = [0]*len(querys)
        qidx = list(range(len(querys)))
        qidx.sort(key=lambda i: querys[i][1]) # クエリをrの昇順にソート
        q = 0
        for r, a in enumerate(array):
            while q < len(qidx) and querys[qidx[q]][1] == r:
                l = querys[qidx[q]][0]
                ret[qidx[q]] = st.max_right(0, lambda x: x >= l)
                q += 1
            if a < len(array):
                st.set(a, r)
        return ret

if __name__ == "__main__":
    array = [3, 1, 0, 2, 5, 3, 1]
    querys = [(3, 7), (0, 4), (2, 5), (1, 3)]
    off_rmq = OffLine_RangeMexQuery.solve(array, querys)
    print(off_rmq)