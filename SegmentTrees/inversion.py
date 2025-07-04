from 藤間ゼミ.SegmentTrees.segmentTree import SegmentTree

class Inversion:
    
    def solve(pmt_array):
        st = SegmentTree([0]*len(pmt_array), lambda x, y: x+y, 0)
        ret = 0
        for p in pmt_array:
            ret += st.prod(p+1, st.array_length)
            st.set(p, 1)
        return ret

if __name__ == "__main__":
    pmt_array = [2, 1, 4, 5, 3, 0]
    print(Inversion.solve(pmt_array))