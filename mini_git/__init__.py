"""
mini_git 패키지

[역할]
Mini Git CLI 프로그램의 루트 패키지입니다.
model / engine / repository / cli 4개의 하위 계층으로 구성됩니다.

[계층 구조]
  model      : 순수 데이터 모델 (의존성 없음)
  engine     : 알고리즘 구현체 (model에만 의존)
  repository : 저장소 상태 관리 (model + engine에 의존)
  cli        : 사용자 인터페이스 (모든 하위 계층에 의존 가능)
"""
