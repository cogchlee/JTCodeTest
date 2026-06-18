import time
import random

def solution1(elements):
    """
    [최적화 방식 - 누적합 (Accumulation)]
    원형 수열 처리를 위해 배열을 2배로 늘린 뒤, 
    각 시작점(start)에서 출발하여 길이를 1씩 늘려가며(length)
    이전 합에 현재 숫자 하나만 더해나가는 방식입니다.
    매번 전체를 다시 더할 필요가 없으므로 O(N^2)의 시간 복잡도로 가장 빠르게 동작합니다.
    """
    n = len(elements)
    extended = elements * 2
    unique_sums = set()
    
    # 각 시작점에서 1부터 n까지의 길이를 늘려가며 더함
    for start in range(n):
        current_sum = 0
        # start부터 n개의 원소를 차례대로 누적
        for i in range(start, start + n):
            current_sum += extended[i]
            unique_sums.add(current_sum)
            
    return len(unique_sums)

def solution2(elements):
    """
    [덜 최적화된 방식 - 매번 슬라이싱과 sum() 호출]
    마찬가지로 원형 수열 처리를 위해 배열을 2배로 늘립니다.
    이후 원하는 길이(length)만큼 매번 파이썬 리스트를 슬라이싱([start:start+length])하고
    내장 함수 sum()을 통해 합을 구하는 직관적인 방식입니다.
    이 방식은 O(N^3)의 시간 복잡도를 가져 비효율적이지만, 
    문제의 제약 조건인 N=1000 수준에서는 파이썬 C엔진의 빠른 sum() 덕분에 테스트를 간신히 통과합니다.
    """
    n = len(elements)
    extended = elements * 2
    unique_sums = set()
    
    for length in range(1, n + 1):
        for start in range(n):
            # 매번 부분 배열을 복사(슬라이싱)하고 0부터 다시 합계를 구함
            part_sum = sum(extended[start:start+length])
            unique_sums.add(part_sum)
            
    return len(unique_sums)

def main():
    # 기본 테스트 케이스
    elements_test = [7, 9, 1, 1, 4]
    expected = 18

    print("\n[ 연속 부분 수열 합의 개수 실행 모드 선택 ]")
    print("1. solution1 (최적화 - On-the-fly 누적합 O(N^2)) 실행")
    print("2. solution2 (덜 최적화 - 매번 슬라이싱 O(N^3)) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(elements_test)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(elements_test)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (배열 길이 N=1000 무작위 생성) ===")
        # 최대 제약 조건인 N=1000 크기의 배열 생성
        BIG_N = 1000
        big_elements = [random.randint(1, 1000) for _ in range(BIG_N)]

        start1 = time.perf_counter()
        solution1(big_elements)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(big_elements)
        time2 = time.perf_counter() - start2

        print(f"solution1 (단일 누적합 O(N^2)): {time1:.5f}초")
        print(f"solution2 (슬라이싱 합 O(N^3)): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
