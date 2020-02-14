import sys

if __name__ == '__main__':
    lines = int(sys.stdin.readline())
    for i in range(int(sys.stdin.readline())):
        l, a, b = map(int, sys.stdin.readline().split())
        s = sys.stdin.readline()
        i = 1
        cost = [float('inf')] * (l + 1)
        cost[0] = 0
        k = 0
        while i <= l: 
            j = max(i, k)
            while j<=l and (s[i-1:j] in s[:i-1]):
                j += 1
                 
            if j-1 != i:
                cost[j-1] = min(cost[i-1] + b, cost[j-1])
                k = j
            cost[i] = min(cost[i-1] + a, cost[i])
            i += 1               
                
        print("\n", cost[-1])
