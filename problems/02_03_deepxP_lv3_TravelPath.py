import time
import random
import copy
from collections import defaultdict

def solution1(tickets):
    """
    [최적화 방식 - 오일러 경로 (Hierholzer's Algorithm) + Stack]
    도착지를 역순으로 정렬한 뒤 스택과 DFS를 이용하여 
    막다른 길에 도달할 때마다 경로에 추가하는 방식입니다.
    O(E log E)의 정렬 시간 외에는 간선을 한 번씩만 방문하므로 백트래킹 없이 매우 빠릅니다.
    """
    graph = defaultdict(list)
    # 도착지 기준 역순 정렬 (pop() 시 알파벳 순서가 가장 빠른 것이 나오도록)
    for start, end in sorted(tickets, reverse=True):
        graph[start].append(end)
        
    stack = ["ICN"]
    path = []
    
    while stack:
        top = stack[-1]
        # 갈 수 있는 곳이 없으면 스택에서 꺼내어 경로에 추가 (역순으로 쌓임)
        if not graph[top]:
            path.append(stack.pop())
        else:
            # 갈 수 있는 곳이 있다면 거기로 이동하고 간선 삭제
            stack.append(graph[top].pop())
            
    # 완성된 경로를 뒤집어서 반환
    return path[::-1]

def solution2(tickets):
    """
    [덜 최적화된 방식 - 완전 탐색 (백트래킹 DFS)]
    티켓을 알파벳 순으로 미리 정렬한 뒤, 사용 여부를 체크하며 모든 경로를 탐색합니다.
    모든 티켓을 사용한 첫 번째 경로가 알파벳 순으로 가장 빠른 경로이므로 즉시 반환합니다.
    잘못된 길로 들어섰을 경우 다시 돌아와야(백트래킹) 하므로 최악의 경우 O(V^E) 수준으로 매우 느려집니다.
    """
    # 원본 티켓 배열이 변경되지 않도록 복사 후 정렬
    tcks = sorted(tickets, key=lambda x: (x[0], x[1]))
    used = [False] * len(tcks)
    answer = []
    
    def dfs(airport, path):
        # 모든 티켓을 사용했으면 결과 저장 후 종료
        if len(path) == len(tcks) + 1:
            answer.append(path)
            return True
            
        for i, ticket in enumerate(tcks):
            if not used[i] and ticket[0] == airport:
                used[i] = True
                if dfs(ticket[1], path + [ticket[1]]):
                    return True
                used[i] = False
                
        return False
        
    dfs("ICN", ["ICN"])
    return answer[0]

def main():
    # 기본 테스트 케이스
    tickets_test = [["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL","SFO"]]
    expected = ["ICN", "ATL", "ICN", "SFO", "ATL", "SFO"]

    print("\n[ 여행경로 실행 모드 선택 ]")
    print("1. solution1 (최적화 - 오일러 경로 스택) 실행")
    print("2. solution2 (덜 최적화 - 완전 탐색 백트래킹) 실행")
    print("3. 성능 비교 테스트")
    choice = input(">> ").strip()

    if choice == '1':
        res = solution1(copy.deepcopy(tickets_test))
        print(f"\n[solution1 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '2':
        res = solution2(copy.deepcopy(tickets_test))
        print(f"\n[solution2 실행 결과]")
        print(f"기대값: {expected}")
        print(f"실제값: {res}")
        print(f"-> {'Pass' if res == expected else 'Fail'}")
    elif choice == '3':
        print("\n=== 성능 비교 테스트 (막다른 길이 많은 비행 경로 임의 생성) ===")
        # 백트래킹 오버헤드를 발생시키기 위해, 알파벳이 더 빠른 막다른 길을 다수 포함하는 데이터 생성
        big_tickets = []
        current = "ICN"
        
        # 정답 경로가 되는 긴 체인 생성 (Z로 시작해서 알파벳이 늦게 탐색되도록 유도)
        for i in range(1, 400):
            nxt = f"Z{i:03d}"
            big_tickets.append([current, nxt])
            current = nxt
            
        # ICN에서 출발하는 수많은 막다른 길 추가 (A로 시작해서 먼저 탐색되게 유도)
        for i in range(1, 400):
            dead_end = f"A{i:03d}"
            big_tickets.append(["ICN", dead_end])
            big_tickets.append([dead_end, "ICN"]) # 다시 돌아오게 함 (사이클)
            
        # 순서 무작위로 섞기
        random.shuffle(big_tickets)

        start1 = time.perf_counter()
        solution1(copy.deepcopy(big_tickets))
        time1 = time.perf_counter() - start1

        start2 = time.perf_counter()
        solution2(copy.deepcopy(big_tickets))
        time2 = time.perf_counter() - start2

        print(f"solution1 (오일러 경로 - Stack): {time1:.5f}초")
        print(f"solution2 (완전탐색 - Backtracking): {time2:.5f}초")
        if time1 < time2:
            print(f"-> solution1이 약 {time2/time1:.1f}배 빠릅니다.")
        else:
            print(f"-> solution2가 약 {time1/time2:.1f}배 빠릅니다.")
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
