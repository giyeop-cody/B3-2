# [종합 평가 시나리오 3] 동료 평가용 아키텍처 & 코드 리뷰 시나리오 (Peer Review - Architecture)

## 1. 동료 평가(Peer Review) 환경 안내
본 시나리오는 **동료 학습자의 코드 리뷰 관점**에서 레이어 분리, 객체 불변성, 알고리즘 구현의 정확성을 채점할 수 있도록 구성되었습니다.

* **과제 미완료자 / 초심자 평가자**: 화면 출력 비교 체크리스트를 실행하여 합격/불합격 판정.
* **과제 완료자 / 숙련자 평가자**: 클래스별 책임 분리(SRP) 및 알고리즘 소스 코드 구조 검증.

---

## 2. 초심자 평가자를 위한 쾌속 입력 & 결과 판단 가이드 (Visual Output Check)

`python main.py` 실행 후 아래 입력을 통해 기능과 출력을 대조하세요.

```bash
mini-git> init "Alice"
mini-git> commit "Initial commit"
mini-git> branch feature
mini-git> switch feature
mini-git> commit "Add login feature"
mini-git> switch main
mini-git> commit "Add payment feature"

# [핵심 검증 1] LOG 실행 시 Initial commit이 맨 상단(부모)에 출력되는가?
mini-git> log

# [핵심 검증 2] PATH 실행 시 시작 커밋 -> 목표 커밋 최단 경로가 출력되는가?
mini-git> path <initial_hash> <payment_hash>

# [핵심 검증 3] SEARCH "login" 실행 시 단일 커밋이 정확히 추출되는가?
mini-git> search "login"

# [핵심 검증 4] LOG --sort-by=date 및 author 실행 시 올바르게 정렬되는가?
mini-git> log --sort-by=date
mini-git> log --sort-by=author

# [핵심 검증 5] 보너스 MERGE 및 SORT-COMPARE 동작 확인
mini-git> merge feature
mini-git> sort-compare
mini-git> exit
```

---

## 3. 숙련자 평가자를 위한 코드 검증 & 라인바이라인 분석

### 1) Kahn's Algorithm 위상 정렬 라인바이라인 분석 (`mini_git/engine/graph.py`)
```python
def topological_sort(self) -> list:
    indegree = {h: 0 for h in self._map}  # [Line 1] 그래프 내 노드별 진입 차수 맵 생성
    children = {h: [] for h in self._map}  # [Line 2] 부모 -> 자식 인접 리스트 생성

    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                indegree[h] += 1        # [Line 3] 부모 p를 가진 자식 h의 진입 차수 1 증가
                children[p].append(h)   # [Line 4] 부모 p의 자식 목록에 h 연결

    # [Line 5] 진입 차수 0 노드(루트)를 timestamp 기준으로 병합 정렬(Merge Sort)하여 초기 큐 생성
    queue = Sorter.merge_sort(
        [h for h in self._map if indegree[h] == 0],
        key_func=lambda h: self._map[h].timestamp,
    )

    result = []
    while queue:
        curr = queue.pop(0)             # [Line 6] 큐에서 진입 차수 0인 노드를 꺼내 정렬 결과에 수집
        result.append(curr)

        for child in children[curr]:
            indegree[child] -= 1        # [Line 7] 방출된 부모 노드에 연결된 자식들의 차수 1 감수
            if indegree[child] == 0:
                queue.append(child)     # [Line 8] 차수가 0이 된 자식을 큐에 투입

        # [Line 9] 동일 차수 그룹 노드 간 정렬 순서를 timestamp 오름차순으로 유지 (Merge Sort)
        queue = Sorter.merge_sort(
            queue,
            key_func=lambda h: self._map[h].timestamp,
        )

    return result
```

---

## 4. 이론 지식 및 레포 질문지 동료 평가 답변서 (Peer Review Q&A)

### Q1. DAG(Directed Acyclic Graph)의 원리와 계통적 이력 관리의 중요성
* **답변**: 단방향 간선과 비순환성을 통해 시간 순서와 인과성을 명확히 보장합니다. 일반 커밋(부모 1개) 및 머지 커밋(부모 2개)을 단일 그래프로 표현하며, 무한 루프 없이 안전한 위상 정렬을 가능하게 합니다.

### Q2. 역색인(Inverted Index)의 자료구조적 속도 향상 원리
* **답변**: 선형 탐색은 모든 메시지를 스캔하여 $O(N \times L)$ 시간이 소요되는 반면, 역색인은 커밋 생성 시 토큰을 해시맵(`dict`)의 Key로 사전 인덱싱하여 $O(1)$ 버킷 조회를 수행합니다.

### Q3. `LOG` 연산의 계산 복잡도 및 병목 개선책
* **답변**:
  1. **Incremental Topological Caching**: 단조 증가 그래프 특성을 활용해 커밋 추가 시 캐시 배열에 $O(1)$ 덧붙임.
  2. **Paging/Lazy Iterator**: HEAD부터 역방향 탐색하여 요구 페이지 분량만 정렬하여 반환.

### Q4. 아키텍처 측면 알고리즘 트레이오프 정리

| 알고리즘 | 선정 이유 | 장점 | 트레이오프 및 판단 근거 |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | 파이썬 표준 정렬 API 사용 금지 제약 준수 | $O(N \log N)$ 최악 성능 보장 & Stable | $O(N)$ 메모리 할당 (안정성과 일관성이 더 중요) |
| **Undirected BFS** | 가중치 없는 간선 간 최단 경로 탐색 | 최단 간선 거리 및 사전순 최소 경로 선택 | 큐 메모리 사용 (분기 브랜치 간 경로 탐색 필수) |
| **LCS DP** | 외부 라이브러리 없이 줄 단위 diff 구현 | 추가/삭제/공통 정확히 추적 | $O(N \times M)$ 공간 (텍스트 파일 비교 정석) |
| **Random Hex Hash** | 메타데이터 전용 Mini Git 해시 생성 | 가독성 우수 및 collision loop 안전성 | 난수 기반 해시 (동적 매핑으로 해결) |
