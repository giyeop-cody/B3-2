"""
mini_git.cli 패키지

[역할]
사용자와의 인터페이스를 담당하는 CLI 계층입니다.

[포함 모듈]
  readline : 입력 파싱 유틸리티 (MiniGitReadline)
  repl     : 명령 디스패처 및 REPL 루프 (CLI_REPL)

[의존성]
  mini_git.repository (MiniGitRepository)
  mini_git.engine     (CommitGraph, Sorter, LcsDiff)
  mini_git.cli.readline
"""
from mini_git.cli.readline import MiniGitReadline
from mini_git.cli.repl import CLI_REPL

__all__ = ["MiniGitReadline", "CLI_REPL"]
