import os
import importlib.util
import sys

PROBLEMS_DIR = "problems"

def run_problem_file(file_path):
    """
    주어진 파일 경로의 파이썬 스크립트를 동적으로 로드하고 실행합니다.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"\n{'='*50}")
    print(f"▶ 실행 중: {module_name}")
    print(f"{'='*50}")
    
    try:
        # 모듈 동적 로드
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        # 파일 내용 실행 (스크립트 레벨 코드 실행)
        spec.loader.exec_module(module)
        
        # main() 또는 solve() 함수가 있다면 추가로 실행
        if hasattr(module, 'main'):
            print("\n--- main() 함수 실행 ---")
            module.main()
        elif hasattr(module, 'solve'):
            print("\n--- solve() 함수 실행 ---")
            module.solve()
            
    except Exception as e:
        print(f"\n실행 중 오류 발생 ({module_name}): {e}")
    print(f"{'='*50}\n")

def setup_environment():
    """
    코딩 테스트 문제를 저장할 디렉토리와 샘플 파일을 생성합니다.
    """
    if not os.path.exists(PROBLEMS_DIR):
        os.makedirs(PROBLEMS_DIR)
        print(f"'{PROBLEMS_DIR}' 디렉토리를 생성했습니다.")
        
        # 샘플 파일 생성
        sample_path = os.path.join(PROBLEMS_DIR, "sample_problem.py")
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write("# 프로그래머스 샘플 문제\n")
            f.write("def solution(n):\n")
            f.write("    return n * 2\n\n")
            f.write("def main():\n")
            f.write("    # 테스트 케이스 1\n")
            f.write("    result1 = solution(10)\n")
            f.write("    print(f'입력: 10 -> 출력: {result1}')\n\n")
            f.write("    # 테스트 케이스 2\n")
            f.write("    result2 = solution(5)\n")
            f.write("    print(f'입력: 5 -> 출력: {result2}')\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    main()\n")
        print(f"샘플 파일 '{sample_path}'이 생성되었습니다.")

def main():
    setup_environment()
            
    # problems 폴더 내의 파이썬 파일 목록 가져오기
    problem_files = [f for f in os.listdir(PROBLEMS_DIR) if f.endswith('.py') and not f.startswith('__')]
    
    if not problem_files:
        print(f"\n'{PROBLEMS_DIR}' 폴더에 실행할 문제 파일이 없습니다.")
        return

    while True:
        print("\n[ 코딩 테스트 문제 목록 ]")
        for idx, f in enumerate(problem_files, 1):
            print(f"{idx}. {f}")
            
        print("\n실행할 문제 번호를 입력하세요 (전체 실행: 'all', 종료: 'q'):")
        choice = input(">> ").strip().lower()
        
        if choice == 'q':
            print("종료합니다.")
            break
        elif choice == 'all':
            for f in problem_files:
                run_problem_file(os.path.join(PROBLEMS_DIR, f))
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(problem_files):
                    run_problem_file(os.path.join(PROBLEMS_DIR, problem_files[idx]))
                else:
                    print("유효하지 않은 번호입니다. 다시 입력해주세요.")
            except ValueError:
                print("잘못된 입력입니다. 번호, 'all', 또는 'q'를 입력해주세요.")

if __name__ == "__main__":
    main()
