N, M = map(int,input().split())
A = list(map(int,input().split()))
mod = 10000

dp = [[0]*(M+1) for _ in range(N+1)]
dp[0][0] = 1

for i in range(1, N+1):
    s = 0
    for j in range(M+1):
        if j <= A[i-1]:
            s += dp[i-1][j]
        else:
            s += dp[i-1][j]
            s -= dp[i-1][j-A[i-1]-1]
        s %= mod
        dp[i][j] = s

print(dp[N][M])