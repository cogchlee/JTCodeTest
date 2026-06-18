import time
import random
import sys

# 재귀 깊이 제한 해제 (덜 최적화된 방식이 깊은 재귀를 할 수 있으므로)
sys.setrecursionlimit(10000)

def solution1(matrix_sizes):
    """
    [최적화 방식 - Bottom-Up DP]
    동적 계획법(Dynamic Programming)을 사용하여 중복 연산을 제거합니다.
    작은 부분 문제부터 구하여 배열(dp)에 저장해 두고 재사용하므로 O(N^3)에 해결 가능합니다.
    """
    n = len(matrix_sizes)
    dp = [[0] * n for _ in range(n)]
    
    # 구간의 길이 (1부터 n-1까지)
    for length in range(1, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = float('inf')
            
            # i부터 j까지 행렬을 자를 수 있는 모든 분할점 k에 대해 탐색
            for k in range(i, j):
                # 비용 = 왼쪽 그룹 비용 + 오른쪽 그룹 비용 + 두 그룹을 곱하는 비용
                cost = (dp[i][k] + dp[k+1][j] + 
                        matrix_sizes[i][0] * matrix_sizes[k][1] * matrix_sizes[j][1])
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    return dp[0][n-1]

def solution2(matrix_sizes):
    """
    [덜 최적화된 방식 - Top-Down 재귀 + 메모이제이션]
    재귀 호출을 사용하되, 중복 계산을 막기 위해 memo 배열에 결과를 캐싱(저장)합니다.
    시간 복잡도는 O(N^3)으로 프로그래머스 테스트를 모두 통과하지만,
    파이썬의 함수 재귀 호출 오버헤드 때문에 Bottom-Up(solution1) 방식보다는 상대적으로 느립니다.
    """
    n = len(matrix_sizes)
    memo = [[-1] * n for _ in range(n)]
    
    def solve(i, j):
        # 행렬이 1개만 남으면 곱셈 연산이 필요 없음
        if i == j:
            return 0
            
        # 이미 계산된 결과가 있다면 재사용 (메모이제이션)
        if memo[i][j] != -1:
            return memo[i][j]
            
        min_cost = float('inf')
        for k in range(i, j):
            cost = (solve(i, k) + solve(k+1, j) + 
                    matrix_sizes[i][0] * matrix_sizes[k][1] * matrix_sizes[j][1])
            if cost < min_cost:
                min_cost = cost
                
        memo[i][j] = min_cost
        return min_cost
        
    return solve(0, n - 1)

def main():
    # 기본 테스트 케이스
    matrix_sizes = [[5, 3], [3, 2], [2, 6]]
    expected = 90

    print("\n[ 최적의 행렬 곱셈 실행 모드 선택 ]")
    print("1. solution1 (최적화 - DP) 실행")
    print("2. solution2 (덜 최적화 - 순수 재귀) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(matrix_sizes)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(matrix_sizes)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (행렬 N=80개 임의 생성) ===")
        # 두 방식 모두 통과하는 수준(O(N^3))이므로 N=80 정도로 측정하여 재귀 오버헤드 차이를 봅니다.
        N = 80
        # 행렬 곱셈 조건(앞 행렬의 열 = 뒤 행렬의 행)을 만족하도록 차원 배열 생성
        dims = [random.randint(10, 50) for _ in range(N + 1)]
        big_matrices = [[dims[i], dims[i+1]] for i in range(N)]

        start1 = time.perf_counter()
        solution1(big_matrices)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(big_matrices)
        time2 = time.perf_counter() - start2

        print(f"solution1 (최적화 - DP): {time1:.5f}초")
        print(f"solution2 (비최적화 - 재귀): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
