"""
mini_git.cli.repl
=================

[역할 및 책임]
사용자 명령을 수신·디스패치하고 REPL 루프를 구동하는 CLI 계층의 핵심 클래스입니다.
MiniGitReadline 으로 입력을 파싱하고, MiniGitRepository 와 Engine 을 호출하여
결과를 출력합니다.

[계층 위치]
  CLI_REPL (최상위 진입점 역할)
    ├── MiniGitReadline   : 입력 파싱
    ├── MiniGitRepository : 저장소 상태 변경 (init/branch/switch/commit/merge)
    ├── CommitGraph       : 그래프 탐색 (log/path/ancestors)
    ├── Sorter            : 정렬 (log --sort-by=)
    └── LcsDiff           : 파일 비교 (diff)

[의존성]
  mini_git.cli.readline    (MiniGitReadline)
  mini_git.repository.repo (MiniGitRepository)
  mini_git.engine.graph    (CommitGraph)
  mini_git.engine.sorter   (Sorter)
  mini_git.engine.diff     (LcsDiff)
  Python 표준 라이브러리: sys, random, time
"""

import sys
import random
import time

from mini_git.cli.readline import MiniGitReadline
from mini_git.repository.repo import MiniGitRepository
from mini_git.engine.graph import CommitGraph
from mini_git.engine.sorter import Sorter
from mini_git.engine.diff import LcsDiff


class CLI_REPL:
    """
    [역할 및 책임]
    Mini Git CLI 의 명령 디스패처이자 REPL 루프 컨트롤러입니다.

    [기능]
    - execute_command : 단일 입력 줄을 파싱하여 적절한 핸들러로 분기하고 결과 반환
    - run_repl        : 'mini-git> ' 프롬프트를 표시하며 입력을 반복 수신하는 루프
    - _sort_compare   : 보너스 — Merge Sort 와 Bubble Sort 성능 비교 출력

    [파싱 위임]
    명령어 파싱은 모두 MiniGitReadline 에 위임합니다.
    이 클래스는 파싱 결과(토큰 목록)만 받아 비즈니스 로직을 수행합니다.
    """

    PROMPT = "mini-git> "

    def __init__(self):
        """
        [역할] REPL 구동에 필요한 컴포넌트를 생성하고 주입합니다.

        [구현 사항]
        - MiniGitRepository : 저장소 상태 관리
        - MiniGitReadline   : 입력 파싱 (인스턴스 불필요, 정적 메소드 사용)
        """
        self.repo = MiniGitRepository()

    # ------------------------------------------------------------------
    # 공개 인터페이스
    # ------------------------------------------------------------------

    def execute_command(self, line: str) -> str:
        """
        [역할] 입력 줄 하나를 파싱하고 해당 명령 핸들러를 실행합니다.

        [기능]
        MiniGitReadline.tokenize 로 토큰을 분리하고
        명령어를 대문자로 정규화한 뒤 명령별 핸들러를 호출합니다.

        [구현 사항]
        - 빈 입력은 빈 문자열을 반환합니다.
        - 알 수 없는 명령어는 'Invalid args' 를 반환합니다.
        - 각 명령의 인자 개수 검증은 핸들러 내부에서 수행합니다.

        [지원 명령어]
          INIT, BRANCH, SWITCH, COMMIT, LOG, PATH, ANCESTORS,
          SEARCH, DIFF, MERGE, SORT-COMPARE, EXIT, QUIT

        Args:
            line: REPL 에서 입력된 원시 줄 문자열

        Returns:
            str: 명령 실행 결과 문자열
        """
        tokens = MiniGitReadline.tokenize(line)
        if not tokens:
            return ""

        cmd = MiniGitReadline.normalize_cmd(tokens[0])

        # 명령 라우팅 테이블
        handlers = {
            "INIT":         self._handle_init,
            "BRANCH":       self._handle_branch,
            "SWITCH":       self._handle_switch,
            "COMMIT":       self._handle_commit,
            "LOG":          self._handle_log,
            "PATH":         self._handle_path,
            "ANCESTORS":    self._handle_ancestors,
            "SEARCH":       self._handle_search,
            "DIFF":         self._handle_diff,
            "MERGE":        self._handle_merge,
            "SORT-COMPARE": self._sort_compare,
            "EXIT":         lambda t: "Exiting...",
            "QUIT":         lambda t: "Exiting...",
        }

        handler = handlers.get(cmd)
        if handler is None:
            return "Invalid args"
        return handler(tokens)

    def run_repl(self):
        """
        [역할] Mini Git REPL 루프를 구동합니다.

        [기능]
        - 'mini-git> ' 프롬프트를 출력하고 사용자 입력을 대기합니다.
        - 입력된 명령을 execute_command 로 처리하고 결과를 출력합니다.
        - 'exit' 또는 'quit' 입력 시 루프를 종료합니다.
        - EOF(Ctrl+D) 또는 KeyboardInterrupt(Ctrl+C) 시 정상 종료합니다.

        [구현 사항]
        sys.stdout.write 로 프롬프트를 버퍼 플러시와 함께 출력합니다.
        readline 처리는 MiniGitReadline 에 위임합니다.
        """
        print("Mini Git CLI Client. Type 'exit' or 'quit' to close.")
        while True:
            try:
                sys.stdout.write(self.PROMPT)
                sys.stdout.flush()

                line = sys.stdin.readline()
                if not line:                    # EOF
                    break

                line = line.strip()
                if not line:
                    continue

                if line.lower() in ("exit", "quit"):
                    break

                result = self.execute_command(line)
                if result:
                    print(result)

            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                break
            except Exception as exc:            # 예상치 못한 예외는 최소 복구
                print(f"Error: {exc}")

    # ------------------------------------------------------------------
    # 명령 핸들러 (private)
    # ------------------------------------------------------------------

    def _handle_init(self, tokens: list) -> str:
        """
        [역할] INIT <user_name> 명령을 처리합니다.

        [구현 사항]
        인자가 없으면 'Invalid args' 를 반환합니다.
        사용자 이름은 따옴표 제거 후 공백을 포함할 수 있습니다.
        """
        if len(tokens) < 2:
            return "Invalid args"
        user_name = " ".join(tokens[1:])
        return self.repo.init(user_name)

    def _handle_branch(self, tokens: list) -> str:
        """
        [역할] BRANCH <branch_name> 명령을 처리합니다.

        [구현 사항]
        정확히 2개 토큰(명령 + 브랜치명)이 있어야 합니다.
        """
        if len(tokens) != 2:
            return "Invalid args"
        return self.repo.branch(tokens[1])

    def _handle_switch(self, tokens: list) -> str:
        """
        [역할] SWITCH <branch_name> 명령을 처리합니다.

        [구현 사항]
        정확히 2개 토큰(명령 + 브랜치명)이 있어야 합니다.
        """
        if len(tokens) != 2:
            return "Invalid args"
        return self.repo.switch(tokens[1])

    def _handle_commit(self, tokens: list) -> str:
        """
        [역할] COMMIT <message> 명령을 처리합니다.

        [구현 사항]
        메시지는 따옴표 제거 후 공백을 포함할 수 있습니다.
        인자가 없으면 'Invalid args' 를 반환합니다.
        """
        if len(tokens) < 2:
            return "Invalid args"
        message = " ".join(tokens[1:])
        return self.repo.commit(message)

    def _handle_log(self, tokens: list) -> str:
        """
        [역할] LOG [--sort-by=date|author] 명령을 처리합니다.

        [기능]
        - 옵션 없음 : 위상 정렬 순서로 출력 (부모 → 자식)
        - --sort-by=date   : timestamp 기준 오름차순 정렬 후 출력
        - --sort-by=author : 작성자명 기준 오름차순 정렬 후 출력

        [구현 사항]
        CommitGraph.topological_sort 또는 Sorter.merge_sort 를 사용합니다.
        정렬 시 Python 내장 sorted/list.sort 를 사용하지 않습니다.
        """
        if not self.repo.is_initialized:
            return "Repository not initialized"
        if not self.repo.commit_map:
            return "No commits found."

        # --sort-by= 옵션 파싱 (MiniGitReadline 위임)
        sort_by = None
        if len(tokens) == 2:
            sort_by = MiniGitReadline.parse_option(tokens[1], "--sort-by=")
            if sort_by is None:
                return "Invalid args"

        if sort_by is None:
            # 위상 정렬
            graph = CommitGraph(self.repo.commit_map)
            ordered = [self.repo.commit_map[h] for h in graph.topological_sort()]
        elif sort_by == "date":
            commits = list(self.repo.commit_map.values())
            ordered = Sorter.merge_sort(commits, key_func=lambda c: c.timestamp)
        elif sort_by == "author":
            commits = list(self.repo.commit_map.values())
            ordered = Sorter.merge_sort(commits, key_func=lambda c: c.author.lower())
        else:
            return "Invalid args"

        if sort_by is None:
            # 위상 정렬 로그: 브랜치 정보 포함
            lines = [str(c) for c in ordered]
        else:
            # 정렬 로그: 브랜치 정보 제외 (B3-2.md Section 8 예시 참조)
            lines = [
                f"commit {c.hash} ({c.author}, {c.get_formatted_timestamp()})\n{c.message}"
                for c in ordered
            ]

        return "\n".join(lines) if lines else "No commits found."

    def _handle_path(self, tokens: list) -> str:
        """
        [역할] PATH <commit1> <commit2> 명령을 처리합니다.

        [기능]
        두 커밋 사이 무방향 최단 경로를 탐색하고 출력합니다.
        경로가 없으면 'No path' 를 반환합니다.
        두 커밋 중 하나라도 존재하지 않으면 표준 에러 메시지를 반환합니다.

        [구현 사항]
        CommitGraph.find_shortest_path 에 탐색을 위임합니다.
        """
        if not self.repo.is_initialized:
            return "Repository not initialized"
        if len(tokens) != 3:
            return "Invalid args"

        c1, c2 = tokens[1], tokens[2]
        if c1 not in self.repo.commit_map:
            return f"Unknown commit: {c1}"
        if c2 not in self.repo.commit_map:
            return f"Unknown commit: {c2}"

        graph = CommitGraph(self.repo.commit_map)
        path = graph.find_shortest_path(c1, c2)
        return f"Path: {' -> '.join(path)}" if path else "No path"

    def _handle_ancestors(self, tokens: list) -> str:
        """
        [역할] ANCESTORS <commit_hash> 명령을 처리합니다.

        [기능]
        지정 커밋의 모든 조상을 timestamp 오름차순으로 나열합니다.
        조상이 없으면 'No ancestors' 를 반환합니다.

        [구현 사항]
        CommitGraph.get_ancestors 에 탐색을 위임합니다.
        """
        if not self.repo.is_initialized:
            return "Repository not initialized"
        if len(tokens) != 2:
            return "Invalid args"

        h = tokens[1]
        if h not in self.repo.commit_map:
            return f"Unknown commit: {h}"

        graph = CommitGraph(self.repo.commit_map)
        ancestors = graph.get_ancestors(h)
        if not ancestors:
            return "No ancestors"

        lines = [f"Ancestors of {h}:"]
        for anc in ancestors:
            node = self.repo.commit_map[anc]
            lines.append(f"- {node.hash}: {node.message}")
        return "\n".join(lines)

    def _handle_search(self, tokens: list) -> str:
        """
        [역할] SEARCH <keyword> 또는 SEARCH --author=<name> 명령을 처리합니다.

        [기능]
        역색인(InvertedIndex)을 통해 O(1) 평균 시간에 커밋을 검색합니다.
        결과는 timestamp 오름차순(Merge Sort)으로 정렬하여 반환합니다.

        [구현 사항]
        --author= 접두어 유무를 MiniGitReadline.parse_option 으로 판별합니다.
        """
        if not self.repo.is_initialized:
            return "Repository not initialized"
        if len(tokens) != 2:
            return "Invalid args"

        arg = tokens[1]
        author_val = MiniGitReadline.parse_option(arg, "--author=")

        if author_val is not None:
            matched = self.repo.inverted_index.search_by_author(author_val)
        else:
            matched = self.repo.inverted_index.search_by_keyword(arg)

        if not matched:
            return "Found 0 commits"

        sorted_hashes = Sorter.merge_sort(
            list(matched),
            key_func=lambda h: self.repo.commit_map[h].timestamp,
        )
        count = len(sorted_hashes)
        header = f"Found {count} commit{'s' if count > 1 else ''}:"
        lines = [header] + [
            f"- {h}: {self.repo.commit_map[h].message}"
            for h in sorted_hashes
        ]
        return "\n".join(lines)

    def _handle_diff(self, tokens: list) -> str:
        """
        [역할] DIFF <file1> <file2> 명령을 처리합니다. (보너스)

        [기능]
        두 텍스트 파일을 줄 단위로 비교하여 +/-/공백 접두어로 결과를 출력합니다.

        [구현 사항]
        LcsDiff.file_diff 에 비교를 위임합니다.
        """
        if len(tokens) != 3:
            return "Invalid args"
        return LcsDiff.file_diff(tokens[1], tokens[2])

    def _handle_merge(self, tokens: list) -> str:
        """
        [역할] MERGE <branch_name> 명령을 처리합니다. (보너스)

        [기능]
        대상 브랜치를 현재 브랜치에 병합하는 머지 커밋을 생성합니다.

        [구현 사항]
        MiniGitRepository.merge 에 처리를 위임합니다.
        """
        if len(tokens) != 2:
            return "Invalid args"
        return self.repo.merge(tokens[1])

    def _sort_compare(self, tokens: list) -> str:
        """
        [역할] SORT-COMPARE 명령을 처리합니다. (보너스)

        [기능]
        직접 구현한 Merge Sort 와 Bubble Sort 의 성능을 비교하여 출력합니다.
        N = 100 / 500 / 1000 크기의 무작위 데이터를 사용합니다.

        [구현 사항]
        time.perf_counter 로 경과 시간(ms)을 측정합니다.
        Bubble Sort 는 이 메소드 내에서만 사용하는 로컬 함수로 정의합니다.
        """
        def bubble_sort(arr: list) -> list:
            """
            [역할] 비교 대상 알고리즘인 버블 정렬을 구현합니다.
            [구현 사항] 인접 원소를 비교하며 O(N²) 시간에 정렬합니다.
            """
            data = list(arr)
            n = len(data)
            for i in range(n):
                for j in range(n - i - 1):
                    if data[j] > data[j + 1]:
                        data[j], data[j + 1] = data[j + 1], data[j]
            return data

        sizes = [100, 500, 1000]
        report = ["[Sort Algorithm Performance Comparison]"]

        for size in sizes:
            data = [random.random() for _ in range(size)]

            t0 = time.perf_counter()
            Sorter.merge_sort(data, key_func=lambda x: x)
            t_merge = (time.perf_counter() - t0) * 1000

            t0 = time.perf_counter()
            bubble_sort(data)
            t_bubble = (time.perf_counter() - t0) * 1000

            report.append(
                f"Size: {size:4d} | Merge Sort: {t_merge:6.2f}ms | Bubble Sort: {t_bubble:6.2f}ms"
            )

        return "\n".join(report)
