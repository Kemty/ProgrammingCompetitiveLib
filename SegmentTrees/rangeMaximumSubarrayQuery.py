from 藤間ゼミ.SegmentTrees.segmentTree import SegmentTree

class RangeMaximumSubarrayQuery:
    
    def __init__(self, array, add, zero, mul, one) -> None:
        """
        add: 和
        zero: 和の単位元
        mul: 積
        one: 積の単位元
        """

        class ExtendedData:
            def __init__(self, x=None) -> None:
                if x is not None:
                    self.ans = x
                    self.all_mul = x
                    self.left_acc = x
                    self.right_acc = x
                else:
                    self.ans = zero
                    self.all_mul = one
                    self.left_acc = zero
                    self.right_acc = zero
            def __repr__(self) -> str:
                return f"(ans: {self.ans}, all_mul: {self.all_mul}, left_acc: {self.left_acc}, right_acc: {self.right_acc})"
        
        self.ExtendedData = ExtendedData
        e = self.ExtendedData()

        def op(x, y):
            ret = self.ExtendedData()
            ret.ans = add(add(x.ans, y.ans), mul(x.right_acc, y.left_acc))
            ret.all_mul = mul(x.all_mul, y.all_mul)
            ret.left_acc = add(x.left_acc, mul(x.all_mul, y.left_acc))
            ret.right_acc = add(mul(x.right_acc, y.all_mul), y.right_acc)
            return ret
        
        self.st = SegmentTree([self.ExtendedData(x) for x in array], op, e)
    
    def set(self, i, x):
        assert 0 <= i < self.st.tree_length
        self.st.set(i, self.ExtendedData(x))
    
    def prod(self, l, r):
        assert 0 <= l <= r <= self.st.array_length
        return self.st.prod(l, r).ans

if __name__ == "__main__":
    rmsq = RangeMaximumSubarrayQuery([3, 1, 4, -1, -5, 9, -2], max, -float("infinity"), lambda x, y: x+y, 0)
    print(rmsq.prod(1, 6))
    rmsq.set(4, -2)
    print(rmsq.prod(1, 6))