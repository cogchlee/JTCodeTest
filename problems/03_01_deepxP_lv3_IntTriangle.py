import time
import random
import sys

# 재귀 제한 해제 (solution2의 Top-Down DFS를 위함)
sys.setrecursionlimit(20000)

def solution1(triangle):
    """
    [최적화 방식 - Bottom-Up DP]
    삼각형의 맨 아래층부터 시작해서 바로 위층으로 올라가며, 
    자신의 양쪽 자식 중 더 큰 값을 현재 위치에 더하는 방식입니다.
    불필요한 함수 호출 없이 단순 반복문으로 O(N^2) 시간에 가장 효율적으로 정답을 도출합니다.
    """
    # 원본 훼손 방지를 위한 깊은 복사 (리스트 컴프리헨션)
    dp = [row[:] for row in triangle]
    
    # 밑에서 두 번째 줄부터 꼭대기(0)까지 거꾸로 올라감
    for i in range(len(dp) - 2, -1, -1):
        for j in range(len(dp[i])):
            # 내 바로 아래(j)와 우측 아래(j+1) 중 큰 값을 내 위치에 누적
            dp[i][j] += max(dp[i+1][j], dp[i+1][j+1])
            
    return dp[0][0]

def solution2(triangle):
    """
    [덜 최적화된 방식 - Top-Down 재귀 + 메모이제이션]
    꼭대기부터 시작하여 바닥까지 재귀적으로 탐색하되, 
    한 번 계산된 위치의 최댓값을 memo 딕셔너리에 저장하여 중복 연산을 방지합니다.
    시간 복잡도는 O(N^2)으로 동일하여 프로그래머스 테스트는 통과하지만, 
    파이썬의 깊은 재귀 호출 오버헤드와 딕셔너리 접근 때문에 Bottom-Up보다 느립니다.
    """
    memo = {}
    n = len(triangle)
    
    def solve(r, c):
        # 바닥에 도달하면 그 위치의 값을 반환
        if r == n - 1:
            return triangle[r][c]
            
        # 이미 계산된 결과가 있다면 재사용
        if (r, c) in memo:
            return memo[(r, c)]
            
        # 왼쪽 아래와 오른쪽 아래 경로 중 더 큰 값을 선택하여 내 값과 더함
        res = triangle[r][c] + max(solve(r + 1, c), solve(r + 1, c + 1))
        memo[(r, c)] = res
        return res
        
    return solve(0, 0)

def main():
    # 기본 테스트 케이스
    triangle_test = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
    expected = 30

    print("\n[ 정수 삼각형 실행 모드 선택 ]")
    print("1. solution1 (최적화 - Bottom-Up DP 반복문) 실행")
    print("2. solution2 (덜 최적화 - Top-Down 재귀+메모이제이션) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(triangle_test)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(triangle_test)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (높이 500의 거대한 무작위 정수 삼각형 생성) ===")
        # 최대 제약 조건인 높이 500의 삼각형 생성
        BIG_N = 500
        big_triangle = []
        for i in range(1, BIG_N + 1):
            big_triangle.append([random.randint(0, 9999) for _ in range(i)])

        start1 = time.perf_counter()
        solution1(big_triangle)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(big_triangle)
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
