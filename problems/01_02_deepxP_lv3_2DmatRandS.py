import time
import random

def rotate90(key):
    """2차원 배열을 90도 시계방향으로 회전시키는 함수"""
    return [list(row) for row in zip(*key[::-1])]

def solution1(key, lock):
    """
    [최적화 방식]
    새로운 보드(2차원 배열)를 생성하지 않고, 자물쇠의 홈 갯수만 미리 센 뒤
    상대 좌표(dx, dy)를 이용해 겹치는 영역만 계산합니다. 공간/시간 최적화.
    """
    M = len(key)
    N = len(lock)
    
    lock_holes = 0
    for i in range(N):
        for j in range(N):
            if lock[i][j] == 0:
                lock_holes += 1
                
    if lock_holes == 0:
        return True
        
    for _ in range(4):
        for dx in range(1 - M, N):
            for dy in range(1 - M, N):
                matched = 0
                collision = False
                for i in range(M):
                    for j in range(M):
                        if key[i][j] == 1:
                            lock_i, lock_j = i + dx, j + dy
                            if 0 <= lock_i < N and 0 <= lock_j < N:
                                if lock[lock_i][lock_j] == 1:
                                    collision = True
                                    break
                                else:
                                    matched += 1
                    if collision: break
                
                if not collision and matched == lock_holes:
                    return True
        key = rotate90(key)
        
    return False

def check_lock(new_lock, offset, n):
    for i in range(n):
        for j in range(n):
            if new_lock[offset + i][offset + j] != 1:
                return False
    return True

def solution2(key, lock):
    """
    [덜 최적화된 방식]
    자물쇠 주변에 패딩을 붙인 아주 큰 2차원 보드(새 배열)를 매번 생성하고
    열쇠를 더해본 뒤 가운데 자물쇠 영역이 모두 1이 되었는지 확인하는 전형적이지만 느린 방식.
    """
    M = len(key)
    N = len(lock)
    
    offset = M - 1
    board_size = N + 2 * offset
    
    for _ in range(4):
        for x in range(board_size - M + 1):
            for y in range(board_size - M + 1):
                # 매번 새로운 보드 생성 및 초기화
                new_lock = [[0] * board_size for _ in range(board_size)]
                for i in range(N):
                    for j in range(N):
                        new_lock[offset + i][offset + j] = lock[i][j]
                
                # 열쇠 돌기 더하기
                for i in range(M):
                    for j in range(M):
                        new_lock[x + i][y + j] += key[i][j]
                        
                # 자물쇠 영역 확인
                if check_lock(new_lock, offset, N):
                    return True
        key = rotate90(key)
        
    return False

def main():
    key_test = [[0, 0, 0], [1, 0, 0], [0, 1, 1]]
    lock_test = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    expected = True

    print("\n[ 자물쇠와 열쇠 실행 모드 선택 ]")
    print("1. solution1 (최적화 방식) 실행")
    print("2. solution2 (배열 확장 방식) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        print(f"\n[solution1 실행 결과] : {solution1(key_test, lock_test)} (기대값: {expected})")
    elif choice == '2':
        print(f"\n[solution2 실행 결과] : {solution2(key_test, lock_test)} (기대값: {expected})")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (큰 배열 임의 생성) ===")
        # 크기를 조금 키워서 속도 체감이 가능하도록 구성 (N=30, M=15)
        N, M = 30, 15
        big_lock = [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]
        big_key = [[random.choice([0, 1]) for _ in range(M)] for _ in range(M)]
        
        start = time.perf_counter()
        solution1(big_key, big_lock)
        time1 = time.perf_counter() - start
        
        start = time.perf_counter()
        solution2(big_key, big_lock)
        time2 = time.perf_counter() - start
        
        print(f"solution1 (최적화): {time1:.5f}초")
        print(f"solution2 (비최적화): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
