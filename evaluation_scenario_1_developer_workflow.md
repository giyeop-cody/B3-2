# [종합 평가 시나리오 1] 동료 평가용 실무 개발자 워크플로우 시나리오 (Peer Review - Developer Workflow)

## 1. 동료 평가(Peer Review) 환경 안내
본 시나리오는 **동등한 학습자 간 피어 리뷰(Peer Review)**를 위해 작성되었습니다.
평가자의 과제 완성 여부나 기술 이해도 수준에 상관없이 누구나 명확하게 채점할 수 있도록 구성되었습니다.

* **과제 미완료자 / 초심자 평가자**: 아래 명령어 세션을 그대로 복사-붙여넣기하여 **터미널에 출력된 문구가 동일한지** 눈으로 비교하여 채점합니다.
* **과제 완료자 / 숙련자 평가자**: 화면 출력 확인 외에 **코드 내 제약 조건 준수(내장 정렬 미사용 등)** 및 **4대 이론 질의**를 검증합니다.

---

## 2. 초심자 평가자를 위한 복사-붙여넣기 명령어 & 화면 비교 가이드 (Visual Output Check)

터미널에서 `python main.py` 실행 후 아래 명령어들을 순서대로 입력하고 출력을 대조하세요.

```bash
# ------------------------------------------------------------------
# [1] 저장소 초기화 및 첫 커밋 생성
# ------------------------------------------------------------------
mini-git> init "Alice"
# [기대 출력]
# Initialized repository.
# Current branch: main
# Current user: Alice

mini-git> commit "Initial commit"
# [기대 출력]
# [main <6자리해시>] Initial commit

# ------------------------------------------------------------------
# [2] 브랜치 생성 및 병렬 작업
# ------------------------------------------------------------------
mini-git> branch feature
# [기대 출력] Created branch: feature

mini-git> switch feature
# [기대 출력] Switched to branch: feature

mini-git> commit "Add login feature"
# [기대 출력] [feature <6자리해시>] Add login feature

mini-git> switch main
# [기대 출력] Switched to branch: main

mini-git> commit "Add payment feature"
# [기대 출력] [main <6자리해시>] Add payment feature

# ------------------------------------------------------------------
# [3] 위상 정렬 로그 및 그래프 탐색
# ------------------------------------------------------------------
mini-git> log
# [기대 출력] (부모인 Initial commit이 반드시 맨 위에 위치해야 함)
# commit <해시1> (Alice, YYYY-MM-DD HH:MM:SS) [main]
# Initial commit
# commit <해시2> (Alice, YYYY-MM-DD HH:MM:SS) [feature]
# Add login feature
# commit <해시3> (Alice, YYYY-MM-DD HH:MM:SS) [main]
# Add payment feature

mini-git> path <해시1> <해시3>
# [기대 출력] Path: <해시1> -> <해시3>

mini-git> ancestors <해시3>
# [기대 출력]
# Ancestors of <해시3>:
# - <해시1>: Initial commit

# ------------------------------------------------------------------
# [4] 역색인 검색 및 직접 구현 정렬
# ------------------------------------------------------------------
mini-git> search "login"
# [기대 출력]
# Found 1 commit:
# - <해시2>: Add login feature

mini-git> search --author="Alice"
# [기대 출력] Found 3 commits: ...

mini-git> log --sort-by=date
# [기대 출력] 날짜 오름차순 커밋 리스트 출력

mini-git> log --sort-by=author
# [기대 출력] 작성자 오름차순 커밋 리스트 출력

# ------------------------------------------------------------------
# [5] 보너스 기능 (Diff, Merge, 정렬 벤치마크)
# ------------------------------------------------------------------
mini-git> merge feature
# [기대 출력] Merged branch feature into main.

mini-git> sort-compare
# [기대 출력] Merge Sort ms 시간이 Bubble Sort ms 시간보다 훨씬 짧게 표시됨

mini-git> exit
# [기대 출력] Exiting...
```

---

## 3. 숙련자 평가자를 위한 코드 검증 & 라인바이라인 분석

### 1) 내장 정렬 API 사용 금지 제약 검증
* **검사 방법**: Terminal에서 `grep -r "sorted(" .` 및 `grep -r "\.sort(" .` 실행.
* **Pass 조건**: 파이썬 내장 `sorted()` 및 `list.sort()`가 소스 코드에 일절 없어야 함 (`mini_git/engine/sorter.py`의 `merge_sort` 직접 구현체 사용).

### 2) Kahn's Algorithm 위상 정렬 라인바이라인 분석 (`mini_git/engine/graph.py`)
```python
def topological_sort(self) -> list:
    indegree = {h: 0 for h in self._map}  # 1. 모든 커밋의 진입 차수(부모 수) 0 초기화
    children = {h: [] for h in self._map}  # 2. 부모 -> 자식 인접 리스트 초기화

    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                indegree[h] += 1        # 3. 부모(p)가 있는 자식(h)의 indegree 1 증가
                children[p].append(h)   # 4. 부모(p)의 자식 목록에 h 등록

    # 5. indegree == 0 (부모가 없는 루트 노드) 커밋을 타임스탬프 순으로 Merge Sort 정렬
    queue = Sorter.merge_sort(
        [h for h in self._map if indegree[h] == 0],
        key_func=lambda h: self._map[h].timestamp,
    )

    result = []
    while queue:
        curr = queue.pop(0)             # 6. 진입 차수 0인 부모 커밋을 방출하여 결과 수집
        result.append(curr)

        for child in children[curr]:
            indegree[child] -= 1        # 7. 방출된 부모 노드에 연결된 자식들의 차수 1 감소
            if indegree[child] == 0:
                queue.append(child)     # 8. 차수가 0이 된 자식을 큐에 푸시

        # 9. 동일 차수 그룹 노드 간 정렬 순서를 timestamp 오름차순으로 유지 (Merge Sort)
        queue = Sorter.merge_sort(
            queue,
            key_func=lambda h: self._map[h].timestamp,
        )

    return result
```

---

## 4. 이론 지식 및 레포 질문지 동료 평가 답변서 (Peer Review Q&A)

### Q1. DAG(Directed Acyclic Graph)의 원리와 Git 커밋 그래프가 DAG여야 하는 이유
* **답변**: 커밋은 과거의 부모 커밋만 가리키므로 방향성(Directed)을 가지며, 미래 커밋이 과거 커밋의 부모가 될 수 없어 순환(Cycle)이 발생하지 않습니다(Acyclic). 브랜치 분기 및 다중 부모 머지 커밋을 자유롭게 표현하면서 무한 루프를 방지하기 위해 필수적입니다.

### Q2. 역색인(Inverted Index)의 속도가 선형 순회보다 빠른 이유 (시간복잡도)
* **답변**: 선형 순회는 모든 커밋 메시지를 스캔하여 $O(N \times L)$ 시간이 걸리는 반면, 역색인은 커밋 생성 시 단어를 해시맵(`dict`)의 키로 미리 인덱싱하므로 검색 시 평균 **$O(1)$** 만에 결과를 수집합니다.

### Q3. `LOG` 연산 병목 원인 및 아키텍처 개선책 (Incremental Caching / Paging)
* **답변**: 
  * **병목 원인**: `LOG` 실행마다 전체 노드 $V$개에 대해 Kahn's Algorithm($O(V \log V + E)$) 전체 정렬을 재실행함.
  * **개선책 1 (Incremental Caching)**: 커밋 추가 시 기존 위상 리스트 뒤에 $O(1)$로 덧붙여 캐싱.
  * **개선책 2 (Paging)**: HEAD에서 부모 포인터를 역추적하는 Lazy Generator로 필요한 분량만 정렬.

### Q4. 알고리즘 트레이오프 및 평가 요약

| 알고리즘 | 선정 이유 | 장점 | 트레이오프 (단점 및 감내 이유) |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | 파이썬 표준 정렬 API 금지 제약 준수 | $O(N \log N)$ 최악 성능 보장 & Stable | $O(N)$ 메모리 할당 (정렬 안정성 확보) |
| **Undirected BFS** | 미가중치 최단 경로 탐색 | $O(V+E)$ 최단 거리 & 사전순 선택 | 큐 메모리 사용 (분기 브랜치 간 경로 탐색 필수) |
| **LCS DP Diff** | 줄 단위 diff 정확 식별 | 추가/삭제/공통 정확히 추적 | $O(N \times M)$ 공간 (파일 비교 정석 알고리즘) |
| **Random Hex Hash** | 고유 커밋 해시 생성 | 짧고 명확한 식별자 | 비결정적 해시 (충돌 루프 검증으로 해결) |
