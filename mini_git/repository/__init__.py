"""
mini_git.repository 패키지

[역할]
Mini Git 저장소의 상태를 관리하는 계층입니다.
Engine 계층의 알고리즘 클래스들을 조합하여 사용자 명령을 처리하고
저장소 상태(브랜치, HEAD, 커밋 맵)를 유지합니다.

[의존성]
  mini_git.model  (CommitNode)
  mini_git.engine (InvertedIndex, Sorter)
"""
from mini_git.repository.repo import MiniGitRepository

__all__ = ["MiniGitRepository"]
