"""
mini_git.engine 패키지

[역할]
Mini Git의 핵심 알고리즘 구현체를 제공합니다.

[포함 모듈]
  sorter  : 병합 정렬 (Merge Sort) 직접 구현
  graph   : 위상 정렬 / BFS 최단 경로 / 조상 탐색
  index   : 역색인 (Inverted Index) 검색 엔진
  diff    : LCS 기반 줄 단위 파일 비교

[의존성]
  mini_git.model 에만 의존합니다.
  Python 표준 라이브러리 이외의 외부 라이브러리를 사용하지 않습니다.
"""
from mini_git.engine.sorter import Sorter
from mini_git.engine.graph import CommitGraph
from mini_git.engine.index import InvertedIndex
from mini_git.engine.diff import LcsDiff

__all__ = ["Sorter", "CommitGraph", "InvertedIndex", "LcsDiff"]
