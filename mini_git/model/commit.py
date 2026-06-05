"""
mini_git.model.commit
=====================

[역할 및 책임]
Git의 개별 커밋 데이터를 표현하는 불변 데이터 모델입니다.
커밋의 고유 해시, 메시지, 저자, 생성 시간, 부모 커밋 목록을 저장합니다.

[의존성]
  Python 표준 라이브러리 datetime 만 사용합니다.
  다른 mini_git 하위 패키지에 의존하지 않습니다.
"""

from datetime import datetime


class CommitNode:
    """
    [역할 및 책임]
    단일 커밋의 메타데이터를 보관하는 데이터 클래스입니다.
    커밋 그래프의 노드 역할을 하며, parents 필드를 통해 DAG 구조를 형성합니다.

    [기능]
    - 커밋 객체 생성 및 필드 제공
    - 타임스탬프 포맷팅 출력
    - 로그용 문자열 표현 제공

    [필드]
    - hash      : 세션 내 유일한 6자리 16진수 커밋 식별자
    - message   : 커밋 메시지 문자열
    - author    : 작성자 이름
    - timestamp : 커밋 생성 시각 (datetime 객체)
    - parents   : 부모 커밋 해시 목록 (0개 이상; 머지 커밋은 2개)
    - branch    : 커밋이 작성된 브랜치 이름
    """

    def __init__(
        self,
        commit_hash: str,
        message: str,
        author: str,
        timestamp: datetime,
        parents: list,
        branch: str,
    ):
        """
        [역할] CommitNode 인스턴스를 초기화합니다.

        [구현 사항]
        - 모든 인자를 동일 이름의 인스턴스 속성에 저장합니다.
        - parents 는 외부 리스트를 그대로 참조하지 않고 복사본을 저장해
          우발적인 변이를 방지합니다.

        Args:
            commit_hash : 고유 커밋 해시 (str, 6자리 hex)
            message     : 커밋 메시지
            author      : 작성자 이름
            timestamp   : 생성 시각 (datetime)
            parents     : 부모 해시 목록 (list[str])
            branch      : 작성 브랜치 이름
        """
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = list(parents)   # 방어적 복사
        self.branch = branch

    # ------------------------------------------------------------------
    # 출력 유틸리티
    # ------------------------------------------------------------------

    def get_formatted_timestamp(self) -> str:
        """
        [역할] timestamp 를 사람이 읽기 쉬운 문자열로 변환합니다.

        [구현 사항]
        datetime.strftime 을 사용하여 'YYYY-MM-DD HH:MM:SS' 포맷을 반환합니다.

        Returns:
            str: 'YYYY-MM-DD HH:MM:SS' 형식의 타임스탬프 문자열
        """
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        """
        [역할] LOG 명령 출력에 사용되는 커밋 요약 문자열을 반환합니다.

        [구현 사항]
        'commit <hash> (<author>, <timestamp>) [<branch>]' 헤더와
        메시지 본문으로 구성된 2줄 문자열을 생성합니다.
        """
        header = (
            f"commit {self.hash} "
            f"({self.author}, {self.get_formatted_timestamp()}) "
            f"[{self.branch}]"
        )
        return f"{header}\n{self.message}"

    def __repr__(self) -> str:
        return f"CommitNode(hash={self.hash!r}, message={self.message!r})"
