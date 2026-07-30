# 🏛️ Repository 패키지 기술 문서 (`mini_git/repository/`)

## 1. 개요 및 역할
`repository` 패키지는 Mini Git의 상태 관리 및 데이터베이스를 담당하는 **비즈니스 로직 계층(Repository Layer)**입니다.

---

## 2. 모듈 구성
* **`repo.py` (`MiniGitRepository`)**: 브랜치 포인터, 커밋 맵, 현재 유저 및 초기화 상태 제어.

---

## 3. 핵심 상태 필드 및 자료구조
* `is_initialized`: 저장소 초기화 플래그 (`bool`).
* `current_user`: 현재 활성 유저 이름 (`str | None`).
* `current_branch`: 현재 HEAD가 위치한 브랜치 이름 (`str | None`).
* `branches`: 브랜치 포인터 맵 (`dict[str, str | None]`, 브랜치명 $\rightarrow$ 커밋 해시).
* `commit_map`: 커밋 데이터베이스 (`dict[str, CommitNode]`, 커밋 해시 $\rightarrow$ CommitNode).
* `inverted_index`: 역색인 인스턴스 (`InvertedIndex`).

---

## 4. 핵심 메커니즘 및 트레이드오프 분석

### 1) 6자리 16진수 해시 생성 및 중복 차단 루프
```python
def _generate_unique_hash(self) -> str:
    while True:
        h = f"{random.randint(0, 0xFFFFFF):06x}"
        if h not in self.commit_map:
            return h
```
* **동작 원리**: $16^6 = 16,777,216$ 크기의 난수 해시 공간에서 생성하되, `commit_map`에 이미 존재하는 해시가 나올 경우 존재하지 않을 때까지 `while` 루프로 검증합니다.
* **트레이오프**: SHA-1 파일 트리 직렬화 없이 메타데이터 전용 Mini Git 구조에서 구현 복잡도를 대폭 단순화하면서 세션 내 100% 해시 유일성을 보장.

### 2) 브랜치 포인터 갱신 및 머지 커밋 생성
* `branch(name)`: 현재 브랜치의 HEAD 해시 포인터를 복사하여 새 키 추가.
* `commit(msg)`: 새 `CommitNode` 생성 후 현재 브랜치 포인터를 전진시킴.
* `merge(target)`: 현재 브랜치 HEAD와 대상 브랜치 HEAD 2개를 `parents` 리스트로 갖는 머지 노드 생성.
