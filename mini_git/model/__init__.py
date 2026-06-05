"""
mini_git.model 패키지

[역할]
Mini Git의 순수 데이터 모델(도메인 객체)을 정의합니다.
어떤 다른 패키지에도 의존하지 않습니다.
"""
from mini_git.model.commit import CommitNode

__all__ = ["CommitNode"]
