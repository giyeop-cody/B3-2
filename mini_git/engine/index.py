"""
mini_git.engine.index
=====================

[역할 및 책임]
커밋 메시지 키워드 및 작성자를 사전(dict) 기반 역색인(Inverted Index)으로
관리하여 O(1) 평균 시간에 커밋 해시 목록을 조회할 수 있도록 합니다.

[구현 방식]
- 키워드 색인: 메시지를 공백 기준으로 split 후 소문자 정규화한 토큰을 키로 사용합니다.
- 작성자 색인: 작성자 이름을 소문자로 정규화하여 키로 사용합니다.
- 각 키에 대한 값은 커밋 해시의 set 으로 관리하여 중복을 자동 제거합니다.

[선형 순회 대비 이점]
- 선형 순회: O(N × L)  (N: 커밋 수, L: 평균 메시지 길이)
- 역색인 조회: O(1) 평균  (해시맵 조회)

[의존성]
  mini_git.model.commit (CommitNode)
  re (Python 표준 라이브러리)
"""

import re


class InvertedIndex:
    """
    [역할 및 책임]
    커밋 메시지 키워드와 작성자를 해시맵으로 인덱싱하여
    SEARCH 명령의 고속 검색을 지원하는 클래스입니다.

    [기능]
    - 커밋 추가 시 메시지와 작성자를 자동으로 색인에 등록합니다.
    - 키워드 또는 작성자 이름을 입력받아 해당 커밋 해시 세트를 반환합니다.

    [내부 구조]
    - keyword_index : dict[str, set[str]]  — 단어 → 커밋 해시 집합
    - author_index  : dict[str, set[str]]  — 작성자 소문자 → 커밋 해시 집합
    """

    def __init__(self):
        """
        [역할] 빈 역색인 구조를 초기화합니다.

        [구현 사항]
        keyword_index 와 author_index 를 빈 dict 로 생성합니다.
        """
        self.keyword_index: dict = {}
        self.author_index: dict = {}

    def add_commit(self, commit) -> None:
        """
        [역할] 커밋 노드를 역색인에 등록합니다.

        [기능]
        - 작성자 이름을 소문자로 정규화하여 author_index 에 추가합니다.
        - 커밋 메시지를 정규식 \\w+ 로 단어 단위로 분리하고 소문자로 정규화하여
          keyword_index 에 추가합니다.

        [구현 사항]
        - re.findall(r'\\w+', message.lower()) 로 특수문자를 제거한 단어 토큰을 추출합니다.
        - 존재하지 않는 키는 set() 으로 초기화 후 해시를 추가합니다.

        Args:
            commit: CommitNode 인스턴스
        """
        # 1. 작성자 색인
        author_key = commit.author.lower()
        self.author_index.setdefault(author_key, set()).add(commit.hash)

        # 2. 메시지 키워드 색인 (공백 분리, 소문자 정규화)
        for word in commit.message.lower().split():
            self.keyword_index.setdefault(word, set()).add(commit.hash)

    def search_by_keyword(self, keyword: str) -> set:
        """
        [역할] 키워드를 포함하는 커밋 해시 집합을 반환합니다.

        [기능]
        keyword_index 에서 소문자 정규화된 키워드로 O(1) 조회합니다.

        [구현 사항]
        키가 없으면 빈 set 을 반환합니다.

        Args:
            keyword: 검색할 단어 (대소문자 무관)

        Returns:
            set[str]: 매칭된 커밋 해시 집합
        """
        return self.keyword_index.get(keyword.lower(), set())

    def search_by_author(self, author: str) -> set:
        """
        [역할] 특정 작성자의 커밋 해시 집합을 반환합니다.

        [기능]
        author_index 에서 소문자 정규화된 작성자 이름으로 O(1) 조회합니다.

        [구현 사항]
        키가 없으면 빈 set 을 반환합니다.

        Args:
            author: 검색할 작성자 이름 (대소문자 무관)

        Returns:
            set[str]: 매칭된 커밋 해시 집합
        """
        return self.author_index.get(author.lower(), set())
