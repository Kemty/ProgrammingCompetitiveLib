N,K = map(int,input().split())
S = input()

#c[i][j]=i文字目以降の文字jについて、最左のもののインデックス(なければINF)
c = [[float("INF")]*26 for i in range(N)]
for i in range(N-1,-1,-1):
    for j in range(26):
        if j == ord(S[i])-ord('a'):
            c[i][j] = i
        elif i != N-1:
            c[i][j] = c[i+1][j]
            
ans = ""
now = -1 #最後に取った文字のインデックス
for k in range(K,0,-1):
    for i in range(26):
        if c[now+1][i] <= N-k:
            ans += chr(i+ord('a'))
            now = c[now+1][i]
            break
print(ans)
