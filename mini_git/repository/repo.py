"""
mini_git.repository.repo
========================

[역할 및 책임]
Mini Git 저장소의 전체 상태(사용자, 브랜치 맵, 커밋 맵, 역색인)를
소유·관리하는 Repository 계층의 핵심 클래스입니다.

CLI 계층에서 파싱된 명령 인자를 받아 내부 상태를 갱신하고
결과 문자열을 반환합니다.

[관리 상태]
  - is_initialized : 저장소 초기화 여부 (bool)
  - current_user   : 현재 작성자 이름 (str | None)
  - current_branch : 현재 활성 브랜치 이름 (str | None)
  - branches       : dict[str, str | None] — 브랜치명 → HEAD 커밋 해시
  - commit_map     : dict[str, CommitNode] — 커밋 해시 → CommitNode
  - inverted_index : InvertedIndex — 검색 색인

[의존성]
  mini_git.model.commit   (CommitNode)
  mini_git.engine.index   (InvertedIndex)
  Python 표준 라이브러리: datetime, random
"""

import random
from datetime import datetime

from mini_git.model.commit import CommitNode
from mini_git.engine.index import InvertedIndex


class MiniGitRepository:
    """
    [역할 및 책임]
    저장소 상태 머신(State Machine) 역할을 수행합니다.
    INIT / BRANCH / SWITCH / COMMIT / MERGE 명령을 처리하여
    내부 상태를 전이시키고 결과 메시지를 반환합니다.

    [기능]
    - init   : 저장소 초기화, main 브랜치 생성, 사용자 등록
    - branch : 현재 HEAD 를 가리키는 새 브랜치 생성
    - switch : 활성 브랜치 전환
    - commit : 새 커밋 생성, 역색인 갱신, 브랜치 포인터 전진
    - merge  : 두 브랜치를 부모로 하는 머지 커밋 생성 (보너스)
    - commit_map property: Engine 계층에서 읽기 전용 접근용
    """

    def __init__(self):
        """
        [역할] 초기화되지 않은 상태로 저장소 객체를 생성합니다.

        [구현 사항]
        모든 상태 필드를 None 또는 빈 컨테이너로 초기화합니다.
        """
        self.is_initialized: bool = False
        self.current_user: str | None = None
        self.current_branch: str | None = None
        self.branches: dict = {}          # branch_name → commit_hash | None
        self.commit_map: dict = {}        # commit_hash → CommitNode
        self.inverted_index = InvertedIndex()

    # ------------------------------------------------------------------
    # 명령 처리 메소드
    # ------------------------------------------------------------------

    def init(self, user_name: str) -> str:
        """
        [역할] 저장소를 완전히 초기화합니다.

        [기능]
        - 기존 데이터를 모두 삭제하고 새 저장소 상태를 설정합니다.
        - 'main' 브랜치를 생성하고 HEAD 를 main 으로 설정합니다.
        - 현재 사용자를 등록합니다.

        [구현 사항]
        - is_initialized = True 로 전환합니다.
        - branches = {"main": None} 으로 초기화합니다 (커밋 없는 상태).
        - 새 InvertedIndex 인스턴스를 생성하여 이전 색인을 완전히 초기화합니다.

        Args:
            user_name: 저장소 소유자 이름

        Returns:
            str: 초기화 성공 메시지
        """
        self.is_initialized = True
        self.current_user = user_name
        self.current_branch = "main"
        self.branches = {"main": None}
        self.commit_map = {}
        self.inverted_index = InvertedIndex()
        return (
            f"Initialized repository.\n"
            f"Current branch: main\n"
            f"Current user: {user_name}"
        )

    def branch(self, branch_name: str) -> str:
        """
        [역할] 현재 HEAD 를 가리키는 새 브랜치를 생성합니다.

        [기능]
        - 이미 존재하는 브랜치명이면 'Invalid args' 를 반환합니다.
        - 성공 시 현재 브랜치의 HEAD 해시를 새 브랜치에 복사합니다.

        [구현 사항]
        branches dict 에 새 브랜치명을 키로 추가하고
        현재 브랜치 HEAD 해시(또는 None)를 값으로 설정합니다.

        Args:
            branch_name: 생성할 브랜치 이름

        Returns:
            str: 성공 메시지 또는 에러 메시지
        """
        if not self.is_initialized:
            return "Repository not initialized"
        if branch_name in self.branches:
            return "Invalid args"

        self.branches[branch_name] = self.branches.get(self.current_branch)
        return f"Created branch: {branch_name}"

    def switch(self, branch_name: str) -> str:
        """
        [역할] 활성 브랜치를 지정한 브랜치로 전환합니다.

        [기능]
        존재하지 않는 브랜치명이면 'Unknown branch: <name>' 을 반환합니다.

        [구현 사항]
        current_branch 필드를 branch_name 으로 업데이트합니다.

        Args:
            branch_name: 전환할 대상 브랜치 이름

        Returns:
            str: 성공 메시지 또는 에러 메시지
        """
        if not self.is_initialized:
            return "Repository not initialized"
        if branch_name not in self.branches:
            return f"Unknown branch: {branch_name}"

        self.current_branch = branch_name
        return f"Switched to branch: {branch_name}"

    def commit(self, message: str) -> str:
        """
        [역할] 현재 활성 브랜치에 새 커밋을 생성합니다.

        [기능]
        - 현재 HEAD 를 부모로 하는 새 CommitNode 를 생성합니다.
        - commit_map 에 등록하고 역색인(InvertedIndex)을 갱신합니다.
        - 현재 브랜치의 HEAD 포인터를 새 커밋으로 전진시킵니다.

        [구현 사항]
        - _generate_unique_hash() 로 세션 내 유일한 해시를 생성합니다.
        - datetime.now() 로 생성 시각을 기록합니다.
        - 커밋 메시지와 작성자를 InvertedIndex 에 색인합니다.

        Args:
            message: 커밋 메시지

        Returns:
            str: '[<branch> <hash>] <message>' 형식의 성공 메시지
                 또는 에러 메시지
        """
        if not self.is_initialized:
            return "Repository not initialized"
        if not self.current_user:
            return "Invalid args"

        parent_hash = self.branches[self.current_branch]
        parents = [parent_hash] if parent_hash else []

        commit_hash = self._generate_unique_hash()
        timestamp = datetime.now()

        node = CommitNode(
            commit_hash=commit_hash,
            message=message,
            author=self.current_user,
            timestamp=timestamp,
            parents=parents,
            branch=self.current_branch,
        )

        self.commit_map[commit_hash] = node
        self.inverted_index.add_commit(node)
        self.branches[self.current_branch] = commit_hash

        return f"[{self.current_branch} {commit_hash}] {message}"

    def merge(self, target_branch: str) -> str:
        """
        [역할] 대상 브랜치를 현재 브랜치에 병합하는 머지 커밋을 생성합니다.
               (보너스 기능)

        [기능]
        - 현재 브랜치 HEAD 와 대상 브랜치 HEAD 를 동시에 부모로 갖는
          CommitNode 를 생성합니다.
        - 자기 자신 병합 또는 존재하지 않는 브랜치 병합은 에러를 반환합니다.

        [구현 사항]
        - parents 리스트에 current_head 와 target_head 를 순서대로 추가합니다.
        - 머지 커밋도 commit_map 과 inverted_index 에 정상 등록합니다.

        Args:
            target_branch: 병합할 대상 브랜치 이름

        Returns:
            str: 성공 메시지 또는 에러 메시지
        """
        if not self.is_initialized:
            return "Repository not initialized"
        if target_branch not in self.branches:
            return f"Unknown branch: {target_branch}"
        if target_branch == self.current_branch:
            return "Invalid args"

        current_head = self.branches[self.current_branch]
        target_head = self.branches[target_branch]

        if not current_head and not target_head:
            return "Invalid args"

        parents = []
        if current_head:
            parents.append(current_head)
        if target_head and target_head != current_head:
            parents.append(target_head)

        commit_hash = self._generate_unique_hash()
        message = f"Merge branch '{target_branch}' into {self.current_branch}"
        node = CommitNode(
            commit_hash=commit_hash,
            message=message,
            author=self.current_user,
            timestamp=datetime.now(),
            parents=parents,
            branch=self.current_branch,
        )

        self.commit_map[commit_hash] = node
        self.inverted_index.add_commit(node)
        self.branches[self.current_branch] = commit_hash

        return (
            f"Merged branch {target_branch} into {self.current_branch}.\n"
            f"[{self.current_branch} {commit_hash}] {message}"
        )

    # ------------------------------------------------------------------
    # 내부 유틸리티
    # ------------------------------------------------------------------

    def _generate_unique_hash(self) -> str:
        """
        [역할] 세션 내에서 유일한 6자리 16진수 커밋 해시를 생성합니다.

        [구현 사항]
        random.randint(0, 0xFFFFFF) 로 해시 후보를 생성하고
        commit_map 에 없는 값이 나올 때까지 반복합니다.
        충돌 확률이 매우 낮지만 보장을 위해 while 루프를 사용합니다.

        Returns:
            str: 중복 없는 6자리 hex 문자열
        """
        while True:
            h = f"{random.randint(0, 0xFFFFFF):06x}"
            if h not in self.commit_map:
                return h
