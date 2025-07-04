from collections import defaultdict, deque, Counter
from itertools import permutations, product
from heapq import heapify, heappop, heappush
import math
import bisect
import sys
sys.setrecursionlimit(700000)
input = sys.stdin.readline
inf = float('inf')
mod1 = 10**9+7
mod2 = 998244353

#################################################

# ABC194-E

class SegTree():

    def __init__(self, L, op, e): #コンストラクタ
        self.ope = op
        self.e = e
        self.seg_tree = self.make_tree(L)
        return  

    def make_tree(self, L): #配列Lをセグ木に変換
        l = len(L)

        # 完全二分木にするため配列seg_treeの長さを調整
        # 1_indexedで扱う
        self.tree_l_half = 1<<(l-1).bit_length()
        seg_tree = [self.e]*self.tree_l_half*2

        # 配列Lの要素をseg_treeの子の方に左詰めで入れる
        for i in range(l):
            seg_tree[i+self.tree_l_half] = L[i]
        
        # seg_treeを根まで埋める
        for i in range(len(seg_tree)-1, 2, -2):
            seg_tree[i//2] = self.ope(seg_tree[i-1], seg_tree[i])

        return seg_tree
    
    def seg_ope(self, l, r): # L[l:r](半開区間)での演算結果
        l += self.tree_l_half
        r += self.tree_l_half

        L = self.e
        R = self.e
        while l < r:
            if l&1 == 1: # 右の子ならメモして伯父に
                L = self.ope(L, self.seg_tree[l])
                l += 1
            l >>= 1
            if r&1 == 1: # 右の子なら弟をメモして親に
                r -= 1
                R = self.ope(self.seg_tree[r], R)
            r >>= 1

        return self.ope(L, R)

    def update(self, i, data): # データの更新
        i += self.tree_l_half
        self.seg_tree[i] = data
        while i > 1:
            if i&1 == 0:
                self.seg_tree[i>>1] = self.ope(self.seg_tree[i], self.seg_tree[i+1])
            else:
                self.seg_tree[i>>1] = self.ope(self.seg_tree[i-1], self.seg_tree[i])
            i >>= 1
    
    def get(self, i): #L[i]を取得
        return self.seg_tree[i+self.tree_l_half]
    
    def lower_bound(self, x):
        i = 1
        r = self.tree_l_half
        length = self.tree_l_half>>1
        L = self.e
        while i < self.tree_l_half:
            if self.ope(L, self.seg_tree[i<<1]) < x:
                i = (i<<1)
                r -= length
            else:
                L = self.seg_ope(L, self.seg_tree[i<<1])
                i = (i<<1)+1
            length >>= 1
        return r-1
    
    def __repr__(self):
        return "{}".format(self.seg_tree[self.tree_l_half:])

N, M = map(int, input().rstrip('\n').split())
A = list(map(int, input().rstrip('\n').split()))

querys = [(i, i+M) for i in range(N-M+1)]
Q = len(querys)
idx = sorted(list(range(Q)), key=lambda i: querys[i][1])

ans = inf
st = SegTree([-1]*(1<<(N).bit_length()), min, inf)
# st[i]:=A[:r]でiの最大index
# N以上の数が存在する場合必ず一つは数字が飛ばされる
# → N以上はmexに影響しない

R = 0
for i in idx:
    l, r = querys[i]
    while R < r:
        if A[R] < N:
            st.update(A[R], R)
        R += 1
    ans = min(ans, st.lower_bound(l))
print(ans)