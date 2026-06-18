import time
import random
import heapq
import copy

def solution1(A, B):
    """
    [최적화 방식 - 정렬 및 투 포인터 (Greedy)]
    A와 B를 내림차순(또는 오름차순)으로 정렬한 뒤, 두 배열의 인덱스를 관리하는 투 포인터를 사용합니다.
    가장 큰 숫자부터 비교하면서 B가 A를 이길 수 있다면 둘 다 포인터를 이동시키고 승점을 추가합니다.
    이길 수 없다면 B의 가장 큰 카드는 보존한 채 A의 포인터만 다음으로 이동시킵니다.
    정렬 O(N log N) 이후 순회에 O(N)만 소요되므로 가장 빠르고 가벼운 최적화 방식입니다.
    """
    # 내림차순 정렬
    A.sort(reverse=True)
    B.sort(reverse=True)
    
    i = 0  # A의 포인터
    j = 0  # B의 포인터
    score = 0
    
    while i < len(A) and j < len(B):
        if B[j] > A[i]:
            score += 1
            i += 1
            j += 1
        else:
            # B의 현재 카드가 A의 현재 카드를 이기지 못하면, 
            # A의 카드는 포기하고 다음으로 넘어감 (B의 강력한 카드는 아껴둠)
            i += 1
            
    return score

def solution2(A, B):
    """
    [덜 최적화된 방식 - 우선순위 큐 (Min-Heap)]
    B를 최소 힙(Min-Heap)으로 변환하고, A를 오름차순으로 정렬합니다.
    A의 가장 작은 숫자부터 순회하며 B 힙에서 가장 작은 숫자를 하나씩 꺼내어 비교합니다.
    B가 A를 이길 때까지 계속 꺼내 버리는 탐욕법(Greedy) 방식입니다.
    시간 복잡도는 정렬과 힙 연산으로 O(N log N)이 보장되어 테스트는 무난하게 통과하지만, 
    매번 heappop()을 수행하는 트리 균형화 오버헤드 때문에 단순 배열 투 포인터보다는 느립니다.
    """
    A.sort()
    heapq.heapify(B)
    
    score = 0
    for a in A:
        # B에서 A를 이길 수 있는 가장 작은 숫자를 찾을 때까지 뽑음
        while B:
            b = heapq.heappop(B)
            if b > a:
                score += 1
                break
                
    return score

def main():
    # 기본 테스트 케이스
    A_test = [5, 1, 3, 7]
    B_test = [2, 2, 6, 8]
    expected = 3

    print("\n[ 숫자 게임 실행 모드 선택 ]")
    print("1. solution1 (최적화 - 투 포인터) 실행")
    print("2. solution2 (덜 최적화 - 우선순위 큐/Heap) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(copy.deepcopy(A_test), copy.deepcopy(B_test))
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(copy.deepcopy(A_test), copy.deepcopy(B_test))
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (배열 길이 N=100,000 무작위 생성) ===")
        # 최대 제약 조건인 원소 100,000개(값 최대 10억) 배열 생성
        BIG_N = 100000
        big_A = [random.randint(1, 1000000000) for _ in range(BIG_N)]
        big_B = [random.randint(1, 1000000000) for _ in range(BIG_N)]

        # 원본 데이터 보호
        A_copy1, B_copy1 = copy.deepcopy(big_A), copy.deepcopy(big_B)
        A_copy2, B_copy2 = copy.deepcopy(big_A), copy.deepcopy(big_B)

        start1 = time.perf_counter()
        solution1(A_copy1, B_copy1)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(A_copy2, B_copy2)
        time2 = time.perf_counter() - start2

        print(f"solution1 (투 포인터 O(N log N)): {time1:.5f}초")
        print(f"solution2 (우선순위 큐 O(N log N)): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
