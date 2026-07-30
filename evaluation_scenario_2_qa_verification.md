# [종합 평가 시나리오 2] 동료 평가용 QA & 품질 검증 시나리오 (Peer Review - QA & Verification)

## 1. 동료 평가(Peer Review) 환경 안내
본 시나리오는 **학습자 간 피어 리뷰(Peer Review)** 시, 예외 케이스 처리, 에러 메시지 표준화, 정렬 제약 조건 준수 등 품질 검증 관점에서 채점할 수 있도록 구성되었습니다.

* **과제 미완료자 / 초심자 평가자**: 아래 테스트 스크립트 실행 후 **화면 출력 결과**만 대조하여 판정.
* **과제 완료자 / 숙련자 평가자**: 코드 내 제약 조건 준수 여부 정적 분석 및 심층 질의 응답 검증.

---

## 2. 초심자 평가자를 위한 쾌속 입력 & 결과 판단 가이드 (QA Visual Diff)

`python main.py` 실행 후 아래 입력을 통해 기능과 예외 처리를 검증합니다.

```bash
# ------------------------------------------------------------------
# [1] 파싱 및 예외 처리 검증 (공백 포함 따옴표, 대소문자 미구분)
# ------------------------------------------------------------------
mini-git> init "Alice Bob"
# [판정] Initialized repository. 출력 확인 (공백 포함 이름 지원)

mini-git> COMMIT "Initial setup"
# [판정] 대문자 COMMIT 도 정상 인식되는지 확인

mini-git> switch unknown_branch
# [판정] Unknown branch: unknown_branch 에러 메시지 표준화 확인

# ------------------------------------------------------------------
# [2] 브랜치 및 커밋 트레이싱
# ------------------------------------------------------------------
mini-git> branch feature
mini-git> switch feature
mini-git> commit "Add login feature"
mini-git> switch main
mini-git> commit "Add payment feature"

# ------------------------------------------------------------------
# [3] 위상 정렬 및 최단 경로 검증
# ------------------------------------------------------------------
mini-git> log
# [판정] Initial setup이 부모 커밋으로서 맨 위에 위치해야 합격 (Kahn's Algorithm)

mini-git> path invalid_hash1 invalid_hash2
# [판정] Unknown commit: invalid_hash1 에러 출력 확인

# ------------------------------------------------------------------
# [4] 역색인 및 정렬 검증
# ------------------------------------------------------------------
mini-git> search "login"
# [판정] Found 1 commit: - <hash>: Add login feature

mini-git> log --sort-by=date
# [판정] 날짜 오름차순 출력

mini-git> log --sort-by=author
# [판정] 작성자 오름차순 출력

# ------------------------------------------------------------------
# [5] 보너스 기능 검증
# ------------------------------------------------------------------
mini-git> merge feature
# [판정] Merged branch feature into main. 출력 확인

mini-git> sort-compare
# [판정] Merge Sort ms < Bubble Sort ms 수치 차이 확인

mini-git> quit
```

---

## 3. 숙련자 평가자를 위한 코드 검증 & 라인바이라인 분석

### 1) Kahn's Algorithm 위상 정렬 라인바이라인 분석 (`mini_git/engine/graph.py`)
```python
def topological_sort(self) -> list:
    indegree = {h: 0 for h in self._map}  # [Line 1] 진입 차수(indegree) 테이블 0으로 초기화
    children = {h: [] for h in self._map}  # [Line 2] 자식 간선 인접 리스트 테이블 초기화

    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                indegree[h] += 1        # [Line 3] 부모(p)가 있는 자식(h)의 indegree 증가
                children[p].append(h)   # [Line 4] 부모(p)의 자식 목록에 h 연결

    # [Line 5] indegree == 0 (부모가 없는 루트 노드) 커밋을 타임스탬프 순으로 정렬하여 큐 구성
    queue = Sorter.merge_sort(
        [h for h in self._map if indegree[h] == 0],
        key_func=lambda h: self._map[h].timestamp,
    )

    result = []
    while queue:
        curr = queue.pop(0)             # [Line 6] indegree=0 노드를 큐에서 추출 (결과에 수집)
        result.append(curr)

        for child in children[curr]:
            indegree[child] -= 1        # [Line 7] 자식 노드의 indegree 1 차감 (부모 방문 완료)
            if indegree[child] == 0:
                queue.append(child)     # [Line 8] 차수가 0이 된 자식을 큐에 넣어 정렬 대기

        # [Line 9] 동일 indegree 그룹 내 출력 일관성을 보장하기 위해 큐 재정렬 (Merge Sort)
        queue = Sorter.merge_sort(
            queue,
            key_func=lambda h: self._map[h].timestamp,
        )

    return result
```

---

## 4. 이론 지식 및 레포 질문지 동료 평가 답변서 (Peer Review Q&A)

### Q1. DAG(Directed Acyclic Graph)의 구조와 사이클 발생 시 영향
* **답변**: 자식 커밋에서 부모 커밋으로만 연결되는 단방향 간선과 비순환성을 가집니다. 사이클이 발생하면 위상 정렬에서 진입 차수가 0이 되지 않아 출력이 불가능해지고, BFS 탐색에서 무한 루프가 발생합니다.

### Q2. 역색인(Inverted Index) 대 선형 순회 비교
* **답변**: 선형 순회는 모든 커밋을 순회하며 $O(N \times L)$ 시간이 걸리지만, 역색인은 커밋 생성 시 생성된 해시맵을 버킷 검색하므로 평균 **$O(1)$** 시간이 걸립니다.

### Q3. `LOG` 성능 병목 및 개선 전략
* **답변**:
  1. **Incremental Caching**: 커밋 추가 시 기존 위상 목록에 $O(1)$로 덧붙여 캐싱.
  2. **Paging**: HEAD부터 역방향 탐색 제너레이터를 통해 필요 수량만 반환.

### Q4. 알고리즘 트레이오프 및 평가 요약

| 알고리즘 | 선정 이유 | 장점 | 트레이오프 및 판단 근거 |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | 내장 정렬 금지 조건 준수 | $O(N \log N)$ 최악 성능 보장 & Stable | $O(N)$ 메모리 소요 (정렬 안정성 우대) |
| **Undirected BFS** | 가중치 1 최단 경로 탐색 | $O(V+E)$ 최단 거리 & 사전순 정렬 | 큐 메모리 사용 (분기 브랜치 간 경로 탐색 필수) |
| **LCS DP** | 줄 단위 Diff 추적 | 정확한 삭제/추가/공통 분리 | $O(N \times M)$ DP 테이블 (정확한 diff 식별) |
| **Random Hex Hash** | 6자리 hex 유일 해시 생성 | 가독성 우수 및 충돌 루프 검증 | 비결정적 해시 (동적 매핑으로 해결) |
