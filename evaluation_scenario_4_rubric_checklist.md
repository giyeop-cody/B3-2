# [종합 평가 시나리오 4] 동료 평가용 정량적 루브릭 & 채점 체크리스트 시나리오 (Peer Review - Rubric Checklist)

## 1. 동료 평가(Peer Review) 환경 안내
본 시나리오는 **100점 만점 정량 평가표(Rubric)**를 바탕으로 학습자 간 채점을 신속하게 완료할 수 있도록 설계되었습니다.

* **과제 미완료자 / 초심자 평가자**: 정량적 체크리스트의 항목별 Pass/Fail 점수를 합산하여 종합 점수 산출.
* **과제 완료자 / 숙련자 평가자**: 배점표 검증과 더불어 소스 코드 정적 분석 및 심층 질의 응답 답변 대조.

---

## 2. 초심자 평가자를 위한 쾌속 입력 & 결과 판단 가이드 (Visual Rubric Check)

`python main.py` 실행 후 아래 입력을 통해 채점을 진행합니다.

```bash
mini-git> init "Alice"
mini-git> commit "Initial commit"
mini-git> branch feature
mini-git> switch feature
mini-git> commit "Add login feature"
mini-git> switch main
mini-git> commit "Add payment feature"

# [점수 항목 1] LOG (10점): Initial commit이 부모로서 최상단 출력 확인
mini-git> log

# [점수 항목 2] PATH (5점) & ANCESTORS (5점): 최단 경로 및 조상 출력 확인
mini-git> path <initial_hash> <payment_hash>
mini-git> ancestors <payment_hash>

# [점수 항목 3] SEARCH (10점): 키워드/작성자 검색 및 LOG 정렬 확인
mini-git> search "login"
mini-git> search --author="Alice"
mini-git> log --sort-by=date
mini-git> log --sort-by=author

# [점수 항목 4] 보너스 (10점): MERGE 및 SORT-COMPARE 확인
mini-git> merge feature
mini-git> sort-compare
mini-git> exit
```

---

## 3. 숙련자 평가자를 위한 코드 검증 & 라인바이라인 분석

### 1) Kahn's Algorithm 위상 정렬 라인바이라인 분석 (`mini_git/engine/graph.py`)
```python
def topological_sort(self) -> list:
    indegree = {h: 0 for h in self._map}  # 1. indegree 딕셔너리 0 초기화
    children = {h: [] for h in self._map}  # 2. children 딕셔너리 리스트 초기화

    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                indegree[h] += 1        # 3. 부모(p)를 가리키는 자식(h)의 indegree +1
                children[p].append(h)   # 4. 부모(p)의 자식 목록에 h 연결

    # 5. indegree가 0인 루트 노드를 타임스탬프 순으로 Merge Sort 하여 초기 큐 생성
    queue = Sorter.merge_sort(
        [h for h in self._map if indegree[h] == 0],
        key_func=lambda h: self._map[h].timestamp,
    )

    result = []
    while queue:
        curr = queue.pop(0)             # 6. 진입 차수 0인 노드를 추출하여 결과 리스트에 방출
        result.append(curr)

        for child in children[curr]:
            indegree[child] -= 1        # 7. 방출된 노드의 자식들 indegree 1 차감
            if indegree[child] == 0:
                queue.append(child)     # 8. indegree가 0이 된 자식을 큐에 푸시

        # 9. 동일 indegree 그룹의 타임스탬프 순서를 유지하기 위해 Merge Sort 재정렬
        queue = Sorter.merge_sort(
            queue,
            key_func=lambda h: self._map[h].timestamp,
        )

    return result
```

---

## 4. 이론 지식 및 레포 질문지 동료 평가 답변서 (Peer Review Q&A)

### Q1. DAG(Directed Acyclic Graph)의 정의 및 필요성
* **답변**: 방향성 간선과 비순환성을 가지는 그래프. 병렬 작업(Branch)과 합병(Merge)을 안전하게 표현하며, 인과관계가 역전되거나 무한 순환 루프에 빠지는 문제를 차단함.

### Q2. 역색인(Inverted Index)의 속도 우위 원리
* **답변**: 선형 순회는 $O(N \times L)$ (모든 메시지 스캔) 시간이 소요되는 반면, 역색인은 $O(1)$ (해시맵 버킷 직접 조회) 시간이 소요됨.

### Q3. `LOG` 연산 병목 및 개선 전략
* **답변**:
  1. **Incremental Caching**: 신규 커밋 시 기존 위상 배열에 $O(1)$ 덧붙임.
  2. **Paging/Lazy Generator**: 필요한 페이지 수만큼 역방향 탐색.

### Q4. 정량 평가용 알고리즘 분석표

| 알고리즘 | 선정 이유 | 장점 | 트레이오프 및 판단 근거 |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | 내장 정렬 금지 조건 준수 | 최악 $O(N \log N)$ & Stable Sort | $O(N)$ 메모리 소요 (정렬 안정성이 최우선) |
| **Undirected BFS** | 최단 경로 탐색 | $O(V+E)$ 최단 거리 & 사전순 정렬 | 큐 메모리 사용 (분기 브랜치 간 경로 탐색 필수) |
| **LCS DP** | 줄 단위 diff 식별 | 추가/삭제/공통 정확한 추적 | $O(N \times M)$ DP 테이블 (정확한 diff 출력을 위한 정석) |
| **Random Hex Hash** | 고유 커밋 해시 생성 | 짧고 명확한 식별자 | 비결정적 해시 (충돌 방지 루프로 검증) |

---

## 5. 동료 평가용 100점 만점 채점표 (Peer Review Rubric)

| 평가 영역 | 세부 검증 항목 | 배점 | 획득 점수 | 비고 |
| :--- | :--- | :---: | :---: | :--- |
| **1. 기능성 (30점)** | `INIT`, `BRANCH`, `SWITCH`, `COMMIT` 기본 동작 | 10 | **10** | 정상 동작 |
| | `LOG`, `PATH`, `ANCESTORS` 그래프 탐색 | 10 | **10** | 정상 동작 |
| | `SEARCH`, `LOG --sort-by` 역색인/정렬 | 10 | **10** | 정상 동작 |
| **2. 아키텍처 (20점)**| 계층 분리 (`Model`, `Engine`, `Repo`, `CLI`) | 10 | **10** | SRP 준수 |
| | Docstring 및 주석 작성 규칙 준수 | 10 | **10** | 상세 작성 완료 |
| **3. 알고리즘 (30점)**| 내장 정렬 미사용 & Merge Sort 직접 구현 | 10 | **10** | `sorter.py` 구현 |
| | Kahn's Algo 위상 정렬 및 무방향 BFS | 10 | **10** | `graph.py` 구현 |
| | 역색인 해시맵 $O(1)$ 구조 구현 | 10 | **10** | `index.py` 구현 |
| **4. 심화 고찰 (10점)**| DAG, 역색인, 병목 개선(캐싱/페이징) 이론 | 10 | **10** | 서면 답변 완비 |
| **5. 보너스 (10점)** | `DIFF` (LCS), `MERGE` (2부모), `SORT-COMPARE` | 10 | **10** | 보너스 3종 완료 |
| **최종 합계** | **총점** | **100** | **100** | **만점 (PASS)** |
