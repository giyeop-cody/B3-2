"""
mini_git.engine.diff
====================

[역할 및 책임]
두 텍스트 파일을 줄 단위로 비교하여 추가/삭제/공통 줄을 식별하는
보너스 기능(Diff)을 구현합니다.

[구현 알고리즘]
LCS (Longest Common Subsequence — 최장 공통 부분 수열) DP
  - 시간 복잡도: O(N × M)  (N, M: 두 파일의 줄 수)
  - DP 테이블을 채운 뒤 역추적(backtrace)으로 diff 출력 순서를 결정합니다.

[출력 형식]
  '  <line>' : 두 파일에 공통으로 존재하는 줄
  '+ <line>' : file2 에만 추가된 줄
  '- <line>' : file1 에서만 삭제된 줄

[의존성]
  없음 (Python 표준 라이브러리 open/read 만 사용)
"""


class LcsDiff:
    """
    [역할 및 책임]
    LCS DP 알고리즘을 사용해 두 파일의 줄 단위 차이를 계산하는
    정적 메소드 컬렉션 클래스입니다.

    [기능]
    - 두 파일 경로를 입력받아 줄 단위 diff 문자열을 반환합니다.
    - 파일을 열 수 없을 경우 에러 메시지를 반환합니다.
    """

    @staticmethod
    def file_diff(path1: str, path2: str) -> str:
        """
        [역할] 두 텍스트 파일의 줄 단위 차이를 계산하여 문자열로 반환합니다.

        [기능]
        파일을 읽어 LCS DP 테이블을 생성하고, 역추적으로 각 줄의
        상태(공통/추가/삭제)를 결정합니다.

        [구현 사항]
        1. 두 파일을 UTF-8 로 읽어 줄 목록을 생성합니다.
        2. dp[i][j] = lines1[:i] 와 lines2[:j] 의 LCS 길이로 DP 테이블을 채웁니다.
        3. (N, M)에서 역추적하며 각 줄에 +/-/공백 접두어를 부여합니다.
        4. 수집된 결과를 역전(reverse)하여 올바른 순서로 반환합니다.

        Args:
            path1: 비교 기준 파일 경로 (file1)
            path2: 비교 대상 파일 경로 (file2)

        Returns:
            str: diff 출력 문자열 (줄별 +/-/공백 접두어 포함)
                 파일을 읽지 못한 경우 'Invalid args'
        """
        try:
            with open(path1, 'r', encoding='utf-8') as f:
                lines1 = [line.rstrip('\n') for line in f]
            with open(path2, 'r', encoding='utf-8') as f:
                lines2 = [line.rstrip('\n') for line in f]
        except FileNotFoundError:
            return "Invalid args"

        n, m = len(lines1), len(lines2)

        # DP 테이블 구성: dp[i][j] = LCS 길이
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if lines1[i - 1] == lines2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # 역추적으로 diff 결과 수집
        diff: list[str] = []
        i, j = n, m
        while i > 0 or j > 0:
            if i > 0 and j > 0 and lines1[i - 1] == lines2[j - 1]:
                diff.append(f"  {lines1[i - 1]}")
                i -= 1
                j -= 1
            elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
                diff.append(f"+ {lines2[j - 1]}")
                j -= 1
            else:
                diff.append(f"- {lines1[i - 1]}")
                i -= 1

        diff.reverse()
        return "\n".join(diff)
