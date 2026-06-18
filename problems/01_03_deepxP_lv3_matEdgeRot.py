import time
import random
from collections import deque

def solution1(rows, columns, queries):
    """
    [최적화 방식]
    In-place(제자리) 원소 이동 방식을 사용하여 메모리 할당을 최소화하고 
    단 한 번의 순회로 회전과 최솟값 탐색을 동시에 수행합니다.
    """
    board = [[(r * columns + c + 1) for c in range(columns)] for r in range(rows)]
    answer = []
    
    for r1, c1, r2, c2 in queries:
        # 문제의 인덱스는 1부터 시작하므로 0부터 시작하도록 보정
        r1, c1, r2, c2 = r1 - 1, c1 - 1, r2 - 1, c2 - 1
        
        temp = board[r1][c1]
        min_val = temp
        
        # 1. 왼쪽 세로선 (위로 당기기)
        for i in range(r1, r2):
            board[i][c1] = board[i + 1][c1]
            if board[i][c1] < min_val: min_val = board[i][c1]
            
        # 2. 아래쪽 가로선 (왼쪽으로 당기기)
        for i in range(c1, c2):
            board[r2][i] = board[r2][i + 1]
            if board[r2][i] < min_val: min_val = board[r2][i]
            
        # 3. 오른쪽 세로선 (아래로 당기기)
        for i in range(r2, r1, -1):
            board[i][c2] = board[i - 1][c2]
            if board[i][c2] < min_val: min_val = board[i][c2]
            
        # 4. 위쪽 가로선 (오른쪽으로 당기기)
        for i in range(c2, c1, -1):
            board[r1][i] = board[r1][i - 1]
            if board[r1][i] < min_val: min_val = board[r1][i]
            
        # 임시 보관한 값을 빈자리에 삽입
        board[r1][c1 + 1] = temp
        
        answer.append(min_val)
        
    return answer

def solution2(rows, columns, queries):
    """
    [덜 최적화된 방식]
    테두리의 모든 원소를 deque에 빼내어 담고, rotate 연산을 수행한 뒤
    최솟값을 찾고 다시 배열에 덮어쓰는 직관적이지만 오버헤드가 큰 방식입니다.
    """
    board = [[(r * columns + c + 1) for c in range(columns)] for r in range(rows)]
    answer = []
    
    for r1, c1, r2, c2 in queries:
        r1, c1, r2, c2 = r1 - 1, c1 - 1, r2 - 1, c2 - 1
        
        border_elements = deque()
        
        # 테두리 요소 순서대로 수집 (상 -> 우 -> 하 -> 좌)
        for i in range(c1, c2): border_elements.append(board[r1][i])
        for i in range(r1, r2): border_elements.append(board[i][c2])
        for i in range(c2, c1, -1): border_elements.append(board[r2][i])
        for i in range(r2, r1, -1): border_elements.append(board[i][c1])
        
        # 최솟값 기록
        answer.append(min(border_elements))
        
        # 시계 방향으로 1칸 회전
        border_elements.rotate(1)
        
        # 회전된 값들을 다시 보드에 덮어쓰기
        for i in range(c1, c2): board[r1][i] = border_elements.popleft()
        for i in range(r1, r2): board[i][c2] = border_elements.popleft()
        for i in range(c2, c1, -1): board[r2][i] = border_elements.popleft()
        for i in range(r2, r1, -1): board[i][c1] = border_elements.popleft()
        
    return answer

def main():
    # 기본 테스트 케이스
    rows = 6
    columns = 6
    queries = [[2, 2, 5, 4], [3, 3, 6, 6], [5, 1, 6, 3]]
    expected = [8, 10, 25]

    print("\n[ 행렬 테두리 회전하기 실행 모드 선택 ]")
    print("1. solution1 (최적화 - In-place 교환) 실행")
    print("2. solution2 (덜 최적화 - Deque 추출/삽입) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(rows, columns, queries)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(rows, columns, queries)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (100x100 행렬, 랜덤 쿼리 10,000번) ===")
        BIG_ROWS, BIG_COLS = 100, 100
        # 10,000번의 임의의 사각형 영역 쿼리 생성
        big_queries = []
        for _ in range(10000):
            r1 = random.randint(1, BIG_ROWS - 1)
            c1 = random.randint(1, BIG_COLS - 1)
            r2 = random.randint(r1 + 1, BIG_ROWS)
            c2 = random.randint(c1 + 1, BIG_COLS)
            big_queries.append([r1, c1, r2, c2])

        start1 = time.perf_counter()
        solution1(BIG_ROWS, BIG_COLS, big_queries)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(BIG_ROWS, BIG_COLS, big_queries)
        time2 = time.perf_counter() - start2

        print(f"solution1 (최적화): {time1:.5f}초")
        print(f"solution2 (덜 최적화 - Deque): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
