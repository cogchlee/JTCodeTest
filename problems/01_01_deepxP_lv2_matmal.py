import time
import random

def solution1(arr1, arr2):
    """
    최적화된 방식 (List Comprehension + zip)
    """
    arr2_t = list(zip(*arr2))
    return [[sum(a * b for a, b in zip(row, col)) for col in arr2_t] for row in arr1]

def solution2(arr1, arr2):
    """
    직관적이지만 덜 최적화된 방식 (3중 for문)
    """
    answer = []
    for i in range(len(arr1)):
        row_result = []
        for j in range(len(arr2[0])):
            cell_sum = 0
            for k in range(len(arr1[0])):
                cell_sum += arr1[i][k] * arr2[k][j]
            row_result.append(cell_sum)
        answer.append(row_result)
    return answer

def main():
    arr1_test = [[2, 3, 2], [4, 2, 4], [3, 1, 4]]
    arr2_test = [[5, 4, 3], [2, 4, 1], [3, 1, 1]]
    expected = [[22, 22, 11], [36, 28, 18], [29, 20, 14]]
    
    print("\n[ 행렬의 곱셈 실행 모드 선택 ]")
    print("1. solution1 (최적화 방식) 실행")
    print("2. solution2 (3중 for문) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(arr1_test, arr2_test)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(arr1_test, arr2_test)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (100x100 행렬 임의 생성) ===")
        SIZE = 100
        big_arr1 = [[random.randint(-10, 20) for _ in range(SIZE)] for _ in range(SIZE)]
        big_arr2 = [[random.randint(-10, 20) for _ in range(SIZE)] for _ in range(SIZE)]

        start1 = time.perf_counter()
        solution1(big_arr1, big_arr2)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(big_arr1, big_arr2)
        time2 = time.perf_counter() - start2

        print(f"solution1 (최적화): {time1:.5f}초")
        print(f"solution2 (3중 for문): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
