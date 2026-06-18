import time
import random
import heapq
from collections import deque

def solution1(n, edge):
    """
    [최적화 방식 - BFS (너비 우선 탐색)]
    모든 간선의 가중치가 1로 동일한 그래프의 최단 거리는 단순 BFS가 가장 빠릅니다.
    큐(Deque)를 이용하여 O(V + E)의 시간 복잡도로 빠르게 탐색합니다.
    """
    graph = [[] for _ in range(n + 1)]
    for u, v in edge:
        graph[u].append(v)
        graph[v].append(u)
        
    distances = [-1] * (n + 1)
    distances[1] = 0
    q = deque([1])
    
    max_dist = 0
    count = 0
    
    while q:
        node = q.popleft()
        
        for nxt in graph[node]:
            # 아직 방문하지 않은 노드라면
            if distances[nxt] == -1:
                distances[nxt] = distances[node] + 1
                q.append(nxt)
                
                # 최댓값 갱신 및 카운트
                if distances[nxt] > max_dist:
                    max_dist = distances[nxt]
                    count = 1
                elif distances[nxt] == max_dist:
                    count += 1
                    
    return count

def solution2(n, edge):
    """
    [덜 최적화된 방식 - 다익스트라 (Dijkstra)]
    최단 경로를 찾는 범용적인 알고리즘인 다익스트라와 우선순위 큐(heapq)를 사용합니다.
    간선 가중치가 모두 1인 문제에서는 굳이 힙(Heap) 정렬을 유지할 필요가 없으므로
    O((V + E) log V)의 오버헤드가 발생하여 단순 BFS보다 속도가 느립니다.
    (하지만 n=20000이라도 파이썬에서 충분히 테스트를 통과하는 수준입니다)
    """
    graph = [[] for _ in range(n + 1)]
    for u, v in edge:
        graph[u].append(v)
        graph[v].append(u)
        
    distances = [float('inf')] * (n + 1)
    distances[1] = 0
    
    pq = [(0, 1)] # (누적 거리, 노드 번호)
    
    while pq:
        dist, node = heapq.heappop(pq)
        
        # 이미 처리된 적이 있는 노드면 무시
        if dist > distances[node]:
            continue
            
        for nxt in graph[node]:
            cost = dist + 1
            if cost < distances[nxt]:
                distances[nxt] = cost
                heapq.heappush(pq, (cost, nxt))
                
    max_dist = 0
    count = 0
    for i in range(1, n + 1):
        if distances[i] != float('inf'):
            if distances[i] > max_dist:
                max_dist = distances[i]
                count = 1
            elif distances[i] == max_dist:
                count += 1
                
    return count

def main():
    # 기본 테스트 케이스
    n = 6
    edge = [[3, 6], [4, 3], [3, 2], [1, 3], [1, 2], [2, 4], [5, 2]]
    expected = 3

    print("\n[ 가장 먼 노드 실행 모드 선택 ]")
    print("1. solution1 (최적화 - BFS) 실행")
    print("2. solution2 (덜 최적화 - 다익스트라) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(n, edge)
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(n, edge)
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (노드 N=20,000, 간선 E=50,000 임의 생성) ===")
        BIG_N = 20000
        BIG_E = 50000
        edges_set = set()
        
        # 최소한 그래프가 연결되어 있도록 1번 노드부터 선형으로 연결
        for i in range(1, BIG_N):
            edges_set.add((i, i + 1))
            
        # 남은 간선을 무작위로 추가
        while len(edges_set) < BIG_E:
            u = random.randint(1, BIG_N)
            v = random.randint(1, BIG_N)
            if u != v:
                edges_set.add((min(u, v), max(u, v)))
                
        big_edge = list(edges_set)

        start1 = time.perf_counter()
        solution1(BIG_N, big_edge)
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(BIG_N, big_edge)
        time2 = time.perf_counter() - start2

        print(f"solution1 (단순 BFS): {time1:.5f}초")
        print(f"solution2 (다익스트라): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
