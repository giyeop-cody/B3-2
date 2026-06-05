import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mini_git.cli.repl import CLI_REPL


def main():
    repl = CLI_REPL()

    commands = [
        ('init "Alice"', None),
        ('commit "Initial commit"', 'initial'),
        ('branch feature', None),
        ('switch feature', None),
        ('commit "Add login feature"', 'login'),
        ('switch main', None),
        ('commit "Add payment feature"', 'payment'),
        ('log', None),
        ('path', 'run_path'),
        ('ancestors', 'run_ancestors'),
        ('search "login"', None),
        ('search --author="Alice"', None),
        ('log --sort-by=date', None),
        ('log --sort-by=author', None),
        # 보너스 기능
        ('merge feature', None),
        ('sort-compare', None),
    ]

    output_lines = []
    output_lines.append("# Evaluation Scenario Execution Session\n")
    output_lines.append("본 세션 로그는 `run_evaluation.py` 실행을 통해 수집한 터미널 REPL 세션 출력입니다.\n")
    output_lines.append("```")

    h_init = None
    h_login = None
    h_payment = None

    for raw_cmd, action in commands:
        if action == 'run_path':
            cmd = f"path {h_init} {h_payment}"
        elif action == 'run_ancestors':
            cmd = f"ancestors {h_payment}"
        else:
            cmd = raw_cmd

        result = repl.execute_command(cmd)
        output_lines.append(f"mini-git> {cmd}")
        if result:
            output_lines.append(result)
        # 빈 줄 추가
        output_lines.append("")

        # 해시 동적 수집
        if action == 'initial':
            h_init = next(h for h, n in repl.repo.commit_map.items() if "Initial" in n.message)
        elif action == 'login':
            h_login = next(h for h, n in repl.repo.commit_map.items() if "login" in n.message)
        elif action == 'payment':
            h_payment = next(h for h, n in repl.repo.commit_map.items() if "payment" in n.message)

    # 마지막 빈 줄 제거하고 닫는 코드블록 추가
    if output_lines[-1] == "":
        output_lines.pop()
    output_lines.append("```")

    # 결과 저장
    evidence_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    out_path = os.path.join(evidence_dir, "evaluation_evidence.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Evaluation session log saved to {out_path}")


if __name__ == "__main__":
    main()
