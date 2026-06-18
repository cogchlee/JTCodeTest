import time
import random

def solution1(arrows):
    """
    [최적화 방식 - 사이클 감지 (On-the-fly)]
    대각선 교차 시 새로운 방이 생성되지만 정점(노드)으로 인식되지 않는 문제를 해결하기 위해,
    모든 이동을 2배(스케일업)로 늘려 정중앙 교차점도 정수 좌표가 되게 만듭니다.
    이동하면서 '이미 방문한 노드를 재방문' 하되 '처음 지나가는 간선'일 경우 방이 생성된 것으로 즉시 카운트합니다.
    """
    dx = [0, 1, 1, 1, 0, -1, -1, -1]
    dy = [1, 1, 0, -1, -1, -1, 0, 1]
    
    pos = (0, 0)
    visited_nodes = {pos}
    visited_edges = set()
    rooms = 0
    
    for arrow in arrows:
        # 스케일업(2칸씩 이동)하여 대각선 교차점을 정점으로 처리
        for _ in range(2):
            nxt = (pos[0] + dx[arrow], pos[1] + dy[arrow])
            
            # 이미 방문한 노드인데 통과한 적 없는 간선이라면 사이클(방) 완성
            if nxt in visited_nodes and (pos, nxt) not in visited_edges:
                rooms += 1
                
            visited_nodes.add(nxt)
            # 무방향 그래프이므로 양방향 간선 모두 저장
            visited_edges.add((pos, nxt))
            visited_edges.add((nxt, pos))
            
            pos = nxt
            
    return rooms

def solution2(arrows):
    """
    [덜 최적화된 방식 - 오일러 다면체 정리 (Euler's Formula)]
    수학적인 기하학/위상수학 공식을 활용합니다.
    연결된 평면 그래프에서 (꼭짓점 수 - 간선 수 + 면의 수 = 2)가 성립합니다.
    외부의 무한한 면 1개를 제외하면, 실제 만들어진 방의 개수는 (E - V + 1)이 됩니다.
    모든 이동의 고유 정점(V)과 간선(E)을 구한 뒤 마지막에 수학 공식으로 일괄 계산합니다.
    """
    dx = [0, 1, 1, 1, 0, -1, -1, -1]
    dy = [1, 1, 0, -1, -1, -1, 0, 1]
    
    pos = (0, 0)
    visited_nodes = {pos}
    visited_edges = set()
    
    for arrow in arrows:
        for _ in range(2):
            nxt = (pos[0] + dx[arrow], pos[1] + dy[arrow])
            visited_nodes.add(nxt)
            
            # 간선 중복 방지를 위해 좌표를 정렬하여 하나의 튜플로 저장
            edge = tuple(sorted([pos, nxt]))
            visited_edges.add(edge)
            
            pos = nxt
            
    # 방의 개수(면의 수) = 간선(E) - 정점(V) + 1
    return len(visited_edges) - len(visited_nodes) + 1

def main():
    # 기본 테스트 케이스
    arrows_test = [6, 6, 6, 4, 4, 4, 2, 2, 2, 0, 0, 0, 1, 6, 5, 5, 3, 6, 0]
    expected = 3

    print("\n[ 방의 개수 실행 모드 선택 ]")
    print("1. solution1 (최적화 - On-the-fly 사이클 감지) 실행")
    print("2. solution2 (수학적 - 오일러 다면체 정리) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(arrows_test)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(arrows_test)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (화살표 100,000개 임의 생성) ===")
        # 최대 제약 조건인 100,000개의 무작위 방향 생성
        BIG_N = 100000
        big_arrows = [random.randint(0, 7) for _ in range(BIG_N)]

        start1 = time.perf_counter()
        solution1(big_arrows)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(big_arrows)
        time2 = time.perf_counter() - start2

        print(f"solution1 (사이클 감지): {time1:.5f}초")
        print(f"solution2 (오일러 정리): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
