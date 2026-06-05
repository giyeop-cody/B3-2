"""
main.py — Mini Git CLI 진입점
==============================

[역할 및 책임]
프로그램의 단일 진입점입니다.
mini_git 패키지를 초기화하고 CLI_REPL 루프를 구동합니다.

[실행 방법]
    python main.py

[아키텍처 개요]
    main.py
      └── mini_git.cli.repl    (CLI_REPL)
            ├── mini_git.cli.readline    (MiniGitReadline — 입력 파싱 유틸리티)
            ├── mini_git.repository.repo (MiniGitRepository — 저장소 상태 관리)
            ├── mini_git.engine.graph    (CommitGraph — 위상정렬/BFS/조상탐색)
            ├── mini_git.engine.sorter   (Sorter — Merge Sort 직접 구현)
            └── mini_git.engine.diff     (LcsDiff — LCS 파일 비교)
"""

from mini_git.cli.repl import CLI_REPL


if __name__ == "__main__":
    CLI_REPL().run_repl()
