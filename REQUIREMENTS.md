# Mini Git - 요구사항 (Requirements)

## 1. CLI 공통 규칙 (문법 표준)

- 명령어는 **대소문자를 구분하지 않음** (`INIT` = `init`)
- 문자열 인자는 공백 포함 시 **따옴표**로 감싸야 함
  - 예: `COMMIT "Add login feature"`
- 옵션 형식 통일
  - `SEARCH --author=<name>`
  - `LOG --sort-by=date|author`
- 에러 메시지 표준화
  - `Invalid args`
  - `Unknown branch: <name>`
  - `Unknown commit: <hash>`

## 2. 커밋 그래프 (핵심 자료구조)

- 커밋 노드 필수 필드:
  - `hash`, `message`, `author`, `timestamp`, `parents`
- 부모는 0개 이상 가능
- **DAG(방향성 비순환 그래프)** 구조 유지
- 커밋은 hash로 O(1) 조회 가능해야 함 (dict 사용 권장)
- hash는 세션 내 **유일**해야 함 (중복 금지)

## 3. 역색인 (Inverted Index)

- 모든 커밋을 순회하지 않고 검색 가능해야 함
- 키워드 추출 규칙:
  - 메시지를 공백으로 split
  - 소문자(lower)로 정규화
- 최소 2종 인덱스 지원
  - `keyword → commit_hash 목록`
  - `author → commit_hash 목록`

## 4. 정렬 알고리즘

- **Python 표준 정렬 API 사용 금지**
  - `sorted()`, `list.sort()` 금지
- 비교 기준 변경 가능해야 함 (date, author)

## 5. 과제 목표 (학습 목표)

- 커밋 그래프가 왜 DAG(방향성 비순환 그래프) 구조를 가지는지 말로 설명할 수 있음
- "부모가 먼저 출력되는 로그" 출력을 위해 필요한 알고리즘적 접근(예: 위상 정렬 성격의 출력)을 설명할 수 있음
- 두 커밋 간 최단 경로 검색 및 특정 커밋의 모든 조상 탐색 방법을 설명할 수 있음
- 직접 구현한 정렬 알고리즘의 시간복잡도(평균/최악) 및 안정 정렬(Stable Sort) 여부를 설명할 수 있음
- 역색인(Inverted Index)의 동작 원리와 선형 순회 검색보다 빠른 이유를 시간복잡도 관점에서 설명할 수 있음

---

**참고**: 위 요구사항은 `B3-2.md` Section 3 및 Section 4를 기반으로 정리하였음.