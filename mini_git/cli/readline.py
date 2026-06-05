"""
mini_git.cli.readline
=====================

[역할 및 책임]
CLI 입력 파싱에 특화된 유틸리티 클래스입니다.
쉘 규칙(따옴표로 묶인 공백 포함 인자, --key=value 옵션)을 지원하여
REPL 계층이 파싱 세부사항을 알 필요 없도록 캡슐화합니다.

[설계 의도]
- REPL(repl.py)은 파싱 결과(토큰 목록, 옵션 값)만 받아 명령 로직에 집중합니다.
- readline.py는 파싱 규칙 변경이 필요할 때 이 파일만 수정하면 됩니다.

[지원 문법]
  - 공백으로 구분된 일반 토큰: INIT Alice
  - 큰따옴표로 묶인 공백 포함 인자: COMMIT "Add login feature"
  - 작은따옴표로 묶인 인자: COMMIT 'fix bug'
  - --key=value 형식의 옵션: LOG --sort-by=date
  - --key="value with spaces" 형식의 옵션 (따옴표 포함 옵션 값 지원)

[의존성]
  re (Python 표준 라이브러리)
"""

import re


class MiniGitReadline:
    """
    [역할 및 책임]
    Mini Git CLI 전용 입력 파싱 유틸리티 클래스입니다.
    모든 메소드는 상태 없이 동작하므로 정적(static) 메소드로 제공됩니다.

    [기능]
    - tokenize      : 입력 줄을 따옴표 규칙을 적용하여 토큰 목록으로 분리
    - parse_option  : '--key=value' 형식의 옵션 토큰에서 값(value)을 추출
    - normalize_cmd : 명령어 토큰을 대문자로 정규화 (대소문자 무관 처리)
    """

    # 따옴표 포함 토큰을 추출하는 정규식 패턴
    # --key="value" | --key='value' | --key=value | "..." | '...' | 공백 없는 문자열 순으로 매칭
    _TOKEN_PATTERN = re.compile(r'\S+?=(?:"[^"]*"|\'[^\']*\'|\S+)|"[^"]*"|\'[^\']*\'|\S+')

    @staticmethod
    def tokenize(line: str) -> list:
        """
        [역할] 입력 줄을 따옴표 규칙을 적용하여 토큰 목록으로 분리합니다.

        [기능]
        - 큰따옴표/작은따옴표로 묶인 문자열은 공백을 포함하더라도 하나의 토큰으로 처리합니다.
        - 따옴표 자체(외곽 따옴표)는 제거하여 순수 값만 반환합니다.
        - 빈 줄이나 공백만 있는 줄은 빈 리스트를 반환합니다.

        [구현 사항]
        정규식 _TOKEN_PATTERN 으로 토큰 후보를 추출한 뒤,
        각 토큰의 시작과 끝이 동일한 따옴표 문자로 감싸여 있으면
        해당 따옴표를 제거합니다.

        예시:
          tokenize('init "Alice Bob"')   → ['init', 'Alice Bob']
          tokenize("commit 'fix bug'")   → ['commit', 'fix bug']
          tokenize('log --sort-by=date') → ['log', '--sort-by=date']

        Args:
            line: REPL 에서 입력된 원시 줄 문자열

        Returns:
            list[str]: 파싱된 토큰 목록 (따옴표 제거 완료)
        """
        raw_tokens = MiniGitReadline._TOKEN_PATTERN.findall(line)
        result = []
        for token in raw_tokens:
            if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
                # 외곽 따옴표 제거
                result.append(token[1:-1])
            else:
                result.append(token)
        return result

    @staticmethod
    def parse_option(token: str, prefix: str) -> str | None:
        """
        [역할] '--key=value' 형식의 옵션 토큰에서 value 를 추출합니다.

        [기능]
        token 이 prefix 로 시작하면 '=' 이후의 값을 반환합니다.
        prefix 로 시작하지 않으면 None 을 반환합니다.
        값에 남아있는 외곽 따옴표도 제거합니다.

        [구현 사항]
        str.startswith 로 prefix 를 확인하고
        prefix 길이 이후의 문자열에서 외곽 따옴표를 제거합니다.

        예시:
          parse_option('--sort-by=date',   '--sort-by=') → 'date'
          parse_option('--author="Alice"', '--author=')  → 'Alice'
          parse_option('log',              '--sort-by=') → None

        Args:
            token  : 파싱할 옵션 토큰 문자열
            prefix : '--key=' 형식의 접두어 (등호 포함)

        Returns:
            str  : 접두어 제거 후의 값 (따옴표 제거 포함)
            None : 토큰이 prefix 로 시작하지 않는 경우
        """
        if not token.startswith(prefix):
            return None

        value = token[len(prefix):]
        # 외곽 따옴표 제거
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        return value

    @staticmethod
    def normalize_cmd(token: str) -> str:
        """
        [역할] 명령어 토큰을 대문자로 정규화합니다.

        [기능]
        사용자가 소문자로 입력한 명령어(예: 'init', 'log')를
        내부 비교용 대문자('INIT', 'LOG')로 변환합니다.

        [구현 사항]
        str.upper() 를 사용합니다.
        이 메소드는 명령어 토큰(tokens[0])에만 적용합니다.

        Args:
            token: 입력된 명령어 토큰

        Returns:
            str: 대문자로 변환된 명령어
        """
        return token.upper()
