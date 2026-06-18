import time
import random
from collections import deque, defaultdict

def solution1(n, results):
    """
    [최적화 방식 - BFS (너비 우선 탐색)]
    각 노드에서 정방향(이기는 방향)과 역방향(지는 방향)으로 각각 BFS를 수행하여
    자신과 승패가 확실히 결정된 선수들의 수를 셉니다.
    시간 복잡도: O(V * (V + E)) 로 플로이드-워셜(O(V^3))보다 훨씬 빠릅니다.
    """
    wins = defaultdict(list)
    loses = defaultdict(list)
    
    for a, b in results:
        wins[a].append(b)
        loses[b].append(a)
        
    def bfs(start, graph):
        visited = {start}
        q = deque([start])
        count = 0
        while q:
            node = q.popleft()
            for nxt in graph[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
                    count += 1
        return count

    answer = 0
    for i in range(1, n + 1):
        # 내가 확실히 이기는 사람 수 + 내가 확실히 지는 사람 수 == 전체 인원 - 1 이면 순위 결정
        if bfs(i, wins) + bfs(i, loses) == n - 1:
            answer += 1
            
    return answer

def solution2(n, results):
    """
    [덜 최적화된 방식 - 플로이드-워셜 (Floyd-Warshall)]
    모든 노드 쌍에 대해 A가 B를 이기고 B가 C를 이기면 A가 C를 이긴다는
    논리를 3중 for문으로 모든 노드에 대해 적용합니다.
    시간 복잡도는 O(V^3)이지만, n이 최대 100이므로 100만 번 연산으로 테스트는 모두 통과합니다.
    """
    # 0: 승패 모름, 1: 이김, -1: 짐
    graph = [[0] * (n + 1) for _ in range(n + 1)]
    for a, b in results:
        graph[a][b] = 1
        graph[b][a] = -1
        
    # k: 거쳐가는 노드, i: 출발 노드, j: 도착 노드
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if graph[i][j] == 0:
                    if graph[i][k] == 1 and graph[k][j] == 1:
                        graph[i][j] = 1
                    elif graph[i][k] == -1 and graph[k][j] == -1:
                        graph[i][j] = -1
                        
    answer = 0
    for i in range(1, n + 1):
        # 자기 자신을 제외하고 모든 사람과의 승패(1 또는 -1)가 결정되었는지 확인
        count = sum(1 for j in range(1, n + 1) if graph[i][j] != 0)
        if count == n - 1:
            answer += 1
            
    return answer

def main():
    # 기본 테스트 케이스
    n = 5
    results = [[4, 3], [4, 2], [3, 2], [1, 2], [2, 5]]
    expected = 2

    print("\n[ 순위 실행 모드 선택 ]")
    print("1. solution1 (최적화 - BFS) 실행")
    print("2. solution2 (덜 최적화 - 플로이드-워셜) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(n, results)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(n, results)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (선수 N=100명, 무작위 승패 데이터) ===")
        # N=100 명에 대해 임의의 승패 결과 2000개를 생성 (사이클이 없도록 방향 설정)
        BIG_N = 100
        big_results = []
        # 사이클 방지를 위해 항상 앞 번호가 뒷 번호를 이기는 방향의 무작위 데이터 생성
        for _ in range(2000):
            a = random.randint(1, BIG_N - 1)
            b = random.randint(a + 1, BIG_N)
            big_results.append([a, b])

        start1 = time.perf_counter()
        solution1(BIG_N, big_results)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(BIG_N, big_results)
        time2 = time.perf_counter() - start2

        print(f"solution1 (BFS): {time1:.5f}초")
        print(f"solution2 (플로이드-워셜): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
