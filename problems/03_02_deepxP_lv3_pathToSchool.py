import time
import random
import sys

# 파이썬 재귀 호출 제한 해제 (solution2 Top-Down 방식을 위함)
sys.setrecursionlimit(20000)

def solution1(m, n, puddles):
    """
    [최적화 방식 - Bottom-Up DP (반복문)]
    집(1,1)에서부터 학교(m,n)까지 격자판을 순회하며, 
    자신의 위쪽 칸과 왼쪽 칸의 경우의 수를 더해나가는 동적 계획법입니다.
    이중 반복문으로 구현되어 함수 호출 오버헤드가 없으므로 가장 빠릅니다.
    """
    # 웅덩이 좌표를 O(1)에 찾기 위해 Set으로 변환
    puddles_set = {(p[0], p[1]) for p in puddles}
    
    # 1-based index를 위해 (n+1) x (m+1) 크기 배열 생성
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[1][1] = 1 # 시작점
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if i == 1 and j == 1:
                continue
                
            # 웅덩이인 경우 경로가 0개
            if (j, i) in puddles_set:
                dp[i][j] = 0
            else:
                # 위쪽에서 오는 경우 + 왼쪽에서 오는 경우
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % 1000000007
                
    return dp[n][m]

def solution2(m, n, puddles):
    """
    [덜 최적화된 방식 - Top-Down DFS (재귀 + 메모이제이션)]
    학교(m,n)에서부터 거꾸로 집(1,1)을 찾아 들어가는 재귀 탐색 방식입니다.
    동일한 좌표를 여러 번 계산하지 않기 위해 memo 딕셔너리에 결과를 저장(캐싱)합니다.
    시간 복잡도는 O(m*n)으로 테스트는 모두 통과하지만, 
    수만 번의 재귀 함수 호출과 해시맵 접근 비용 때문에 Bottom-Up 방식보다 상대적으로 느립니다.
    """
    puddles_set = {(p[0], p[1]) for p in puddles}
    memo = {}
    
    def dfs(x, y):
        # 격자 밖을 벗어나거나 웅덩이인 경우 경로 없음
        if x < 1 or y < 1 or (x, y) in puddles_set:
            return 0
        # 집에 도착한 경우 1가지 경로 반환
        if x == 1 and y == 1:
            return 1
            
        # 이미 계산된 결과가 있으면 재사용
        if (x, y) in memo:
            return memo[(x, y)]
            
        # 왼쪽 칸에서 오는 경우 + 위쪽 칸에서 오는 경우
        ways = (dfs(x - 1, y) + dfs(x, y - 1)) % 1000000007
        memo[(x, y)] = ways
        return ways
        
    return dfs(m, n)

def main():
    # 기본 테스트 케이스
    m = 4
    n = 3
    puddles = [[2, 2]]
    expected = 4

    print("\n[ 등굣길 실행 모드 선택 ]")
    print("1. solution1 (최적화 - Bottom-Up DP 반복문) 실행")
    print("2. solution2 (덜 최적화 - Top-Down 재귀+메모이제이션) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(m, n, puddles)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(m, n, puddles)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (m=100, n=100, 랜덤 웅덩이 100개) ===")
        # 최대 제약 조건인 100x100 맵 생성
        BIG_M = 100
        BIG_N = 100
        big_puddles = []
        
        # 임의의 웅덩이 100개 배치 (시작점, 도착점 제외)
        while len(big_puddles) < 100:
            x = random.randint(1, BIG_M)
            y = random.randint(1, BIG_N)
            if (x, y) != (1, 1) and (x, y) != (BIG_M, BIG_N):
                if [x, y] not in big_puddles:
                    big_puddles.append([x, y])

        start1 = time.perf_counter()
        solution1(BIG_M, BIG_N, big_puddles)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(BIG_M, BIG_N, big_puddles)
        time2 = time.perf_counter() - start2

        print(f"solution1 (Bottom-Up 반복문): {time1:.5f}초")
        print(f"solution2 (Top-Down 재귀): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
