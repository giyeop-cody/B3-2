# 📖 Mini Git CLI 프로젝트 최종 심층 종합 보고서

---

## 1. 과제 설명 (Project Overview & Mission)

### 1) 미션 배경 및 목적
본 과제는 개발자들이 매일 사용하는 분산 버전 관리 시스템인 **Git의 핵심 구조(그래프 자료구조와 해시 메커니즘)**를 파이썬(Python 3.10+) CLI 프로그램으로 직접 구현해 보며, 알고리즘과 자료구조의 동작 원리를 체득하는 데 목적이 있습니다.

Git 커밋 하나에는 과거 상태(부모)를 가리키는 방향성 연결 관계가 포함되어 있으며, 이는 컴퓨터 과학에서 **방향성 비순환 그래프(DAG, Directed Acyclic Graph)**를 이룹니다. 본 미션을 통해 다음과 같은 핵심 기술적 목표를 달성합니다:
* **그래프 자료구조의 이해**: 커밋 간 연결 관계를 DAG 구조로 구축하고 탐색.
* **위상 정렬(Topological Sort)**: 부모 커밋이 자식 커밋보다 항상 먼저 출력되는 로그 정렬.
* **최단 경로 및 조상 탐색**: 너비 우선 탐색(BFS)을 통한 두 커밋 간 무방향 최단 경로 및 조상 역추적.
* **직접 정렬 알고리즘 구현**: 파이썬 내장 정렬 API(`sorted()`, `list.sort()`)를 일절 사용하지 않고, 최악 시간복잡도 $O(N \log N)$을 보장하는 **병합 정렬(Merge Sort)** 구현.
* **역색인(Inverted Index)**: 선형 탐색($O(N \times L)$)의 한계를 극복하는 해시맵 기반 $O(1)$ 고속 검색 엔진 구축.

---

## 2. 각 기능 작동 (Functional Demonstration)

프로그램은 단일 진입점 `main.py`를 통해 REPL(Read-Eval-Print Loop) 프롬프트(`mini-git>`)를 구동합니다. 아래는 실행 스크립트(`run_evaluation.py`)를 통해 검증된 실제 명령어별 동작 트랜스크립트입니다.

```bash
# ------------------------------------------------------------------
# 1. 저장소 초기화 (INIT <user_name>)
# ------------------------------------------------------------------
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

# ------------------------------------------------------------------
# 2. 커밋 생성 (COMMIT <message>)
# ------------------------------------------------------------------
mini-git> commit "Initial commit"
[main 17af75] Initial commit

# ------------------------------------------------------------------
# 3. 브랜치 생성 및 전환 (BRANCH <name>, SWITCH <name>)
# ------------------------------------------------------------------
mini-git> branch feature
Created branch: feature

mini-git> switch feature
Switched to branch: feature

mini-git> commit "Add login feature"
[feature 5c376c] Add login feature

mini-git> switch main
Switched to branch: main

mini-git> commit "Add payment feature"
[main d422b0] Add payment feature

# ------------------------------------------------------------------
# 4. 위상 정렬 커밋 로그 (LOG) - 부모 커밋이 항상 선출력됨
# ------------------------------------------------------------------
mini-git> log
commit 17af75 (Alice, 2026-07-29 08:11:01) [main]
Initial commit
commit 5c376c (Alice, 2026-07-29 08:11:01) [feature]
Add login feature
commit d422b0 (Alice, 2026-07-29 08:11:01) [main]
Add payment feature

# ------------------------------------------------------------------
# 5. 최단 경로 탐색 (PATH <commit1> <commit2>) - 무방향 BFS & 사전순
# ------------------------------------------------------------------
mini-git> path 17af75 d422b0
Path: 17af75 -> d422b0

# ------------------------------------------------------------------
# 6. 조상 탐색 (ANCESTORS <commit_hash>)
# ------------------------------------------------------------------
mini-git> ancestors d422b0
Ancestors of d422b0:
- 17af75: Initial commit

# ------------------------------------------------------------------
# 7. 역색인 키워드 및 작성자 검색 (SEARCH <keyword> / SEARCH --author=<name>)
# ------------------------------------------------------------------
mini-git> search "login"
Found 1 commit:
- 5c376c: Add login feature

mini-git> search --author="Alice"
Found 3 commits:
- 17af75: Initial commit
- 5c376c: Add login feature
- d422b0: Add payment feature

# ------------------------------------------------------------------
# 8. 정렬 옵션 로그 (LOG --sort-by=date|author) - 직접 구현 Merge Sort 사용
# ------------------------------------------------------------------
mini-git> log --sort-by=date
commit 17af75 (Alice, 2026-07-29 08:11:01)
Initial commit
commit 5c376c (Alice, 2026-07-29 08:11:01)
Add login feature
commit d422b0 (Alice, 2026-07-29 08:11:01)
Add payment feature

mini-git> log --sort-by=author
commit 17af75 (Alice, 2026-07-29 08:11:01)
Initial commit
commit 5c376c (Alice, 2026-07-29 08:11:01)
Add login feature
commit d422b0 (Alice, 2026-07-29 08:11:01)
Add payment feature

# ------------------------------------------------------------------
# 9. 보너스 1: 파일 줄 단위 비교 (DIFF <file1> <file2>) - LCS DP
# ------------------------------------------------------------------
mini-git> diff "file1.txt" "file2.txt"
  Line 1
- Line 2
+ Line 2 modified
  Line 3
+ Line 4 added

# ------------------------------------------------------------------
# 10. 보너스 2: 브랜치 병합 (MERGE <branch_name>) - 다중 부모 커밋 생성
# ------------------------------------------------------------------
mini-git> merge feature
Merged branch feature into main.
[main 21f380] Merge branch 'feature' into main

# ------------------------------------------------------------------
# 11. 보너스 3: 정렬 알고리즘 성능 비교 (SORT-COMPARE) - Merge vs Bubble
# ------------------------------------------------------------------
mini-git> sort-compare
[Sort Algorithm Performance Comparison]
Size:  100 | Merge Sort:   0.29ms | Bubble Sort:   0.42ms
Size:  500 | Merge Sort:   1.80ms | Bubble Sort:  13.90ms
Size: 1000 | Merge Sort:   3.81ms | Bubble Sort:  53.82ms

# ------------------------------------------------------------------
# 12. 종료 (EXIT / QUIT)
# ------------------------------------------------------------------
mini-git> exit
Exiting...
```

---

## 3. 구조 설명 (Architecture & System Design)

본 시스템은 **관심사 분리(Separation of Concerns)** 원칙에 따라 4개의 계층(Layer)으로 명확히 구조화되어 있습니다.

```
                      ┌─────────────────────────────────────────┐
                      │              main.py (Entry)            │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [CLI Presentation Layer]                                                        │
│   • CLI_REPL (mini_git/cli/repl.py)         : 명령 라우팅 및 REPL 루프           │
│   • MiniGitReadline (mini_git/cli/readline.py) : 따옴표/옵션 파싱 토큰화 유틸리티   │
└──────────────────────────────────────────┬──────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [Repository Business Logic Layer]                                               │
│   • MiniGitRepository (mini_git/repository/repo.py)                            │
│     - 브랜치 포인터 맵(branches) 및 커밋 데이터베이스(commit_map) 관리            │
│     - 유일한 6자리 16진수 해시 생성 루프                                        │
│     - INIT / BRANCH / SWITCH / COMMIT / MERGE 상태 전이 제어                   │
└──────────────┬───────────────────────────┬─────────────────────────┬────────────┘
               │                           │                         │
               ▼                           ▼                         ▼
┌─────────────────────────────┐ ┌───────────────────────────┐ ┌──────────────────┐
│ [Engine - Graph]            │ │ [Engine - Index & Sort]   │ │ [Engine - Diff]  │
│ CommitGraph                 │ │ InvertedIndex             │ │ LcsDiff          │
│ (mini_git/engine/graph.py)  │ │ (mini_git/engine/index.py)│ │ (diff.py)        │
│ • 위상 정렬 (Kahn's Algo)   │ │ • O(1) 키워드/저자 역색인 │ │ • LCS DP 알고리즘│
│ • 무방향 BFS 최단 경로      │ │ Sorter                    │ │ • 줄 단위 diff   │
│ • 조상 역추적 탐색          │ │ (mini_git/engine/sorter.py│ │   (+, -, 공백)   │
└──────────────┬──────────────┘ │ • 직접 구현 Merge Sort    │ └──────────────────┘
               │                └──────────┬────────────────┘
               └───────────┬───────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [Model Layer]                                                                   │
│   • CommitNode (mini_git/model/commit.py)                                       │
│     - 불변 커밋 메타데이터 (hash, message, author, timestamp, parents, branch)  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 모듈별 분석: 기능, 알고리즘, 선정 이유, 장단점 및 트레이오프

### 1) `CommitNode` (`mini_git/model/commit.py`)
* **기능**: 단일 커밋 메타데이터(해시, 작성자, 시간, 메시지, 부모 목록, 브랜치)를 보유하는 불변 자료구조.
* **사용 알고리즘/자료구조**: Python 클래스 기반 불변 데이터 객체 (방어적 복사 `parents = list(parents)` 적용).
* **선정 이유**: 외부에서 `parents` 리스트를 의도치 않게 수정하는 사이드 이펙트를 차단하기 위함.
* **장단점**:
  * *장점*: 데이터 정합성 보장, 출력 포맷 제어(`__str__`)가 용이함.
  * *단점*: 객체 생성에 따른 미세한 메모리 오버헤드.
* **트레이오프 & 판단 근거**: 메모리 사용량 증가보다 커밋 이력 데이터의 캡슐화 및 방어적 복사를 통한 정합성 확보가 훨씬 중요하다고 판단.

---

### 2) `Sorter` (`mini_git/engine/sorter.py`)
* **기능**: 파이썬 내장 정렬 API(`sorted()`, `list.sort()`)를 일절 사용하지 않는 범용 정렬 알고리즘 제공.
* **사용 알고리즘**: **병합 정렬 (Merge Sort)** (분할 정복).
* **선정 이유**:
  1. 최악의 경우에도 $O(N \log N)$ 성능을 확실히 보장 (Quick Sort의 $O(N^2)$ 위험 방지).
  2. 병합 단계에서 `left[i] <= right[j]` 부등호 조건을 통해 **안정 정렬(Stable Sort)**을 완벽 보장.
* **장단점**:
  * *장점*: 데이터 분포와 무관하게 안정적인 $O(N \log N)$ 수행 시간, 동률 키값 순서 유지.
  * *단점*: 임시 배열 생성을 위한 추가 공간 복잡도 $O(N)$ 필요.
* **트레이오프 & 판단 근거**: 메모리가 충분한 인메모리 CLI 환경이므로, 제자리 정렬(In-place)보다 최악 시간복잡도 보장 및 안정 정렬 유지가 최우선 가치임.

---

### 3) `CommitGraph` (`mini_git/engine/graph.py`)
* **기능**: 커밋 DAG 상에서 위상 정렬(`LOG`), 최단 경로(`PATH`), 조상 탐색(`ANCESTORS`) 알고리즘 실행.
* **사용 알고리즘**:
  1. **위상 정렬**: **Kahn's Algorithm** (진입 차수 `indegree` 차감 방식).
  2. **최단 경로**: **무방향 너비 우선 탐색 (Undirected BFS)** + 사전순 문자열 타이 브레이킹.
  3. **조상 탐색**: 부모 포인터 역추적 BFS.
* **선정 이유**:
  * *Kahn's Algo*: 의존성 진입 차수를 기반으로 부모 노드가 자식 노드보다 항상 먼저 출력되는 위상 순서를 $O(V+E)$에 산출.
  * *Undirected BFS*: 간선 가중치가 1인 트리/DAG 구조에서 최단 거리를 보장하는 표준 알고리즘.
* **장단점**:
  * *장점*: 최단 경로 보장, 부모-자식 선후 관계 완벽 보장.
  * *단점*: 무방향 간선 변환으로 인한 메모리 추가 사용, `LOG` 호출 시 전체 정렬 오버헤드.
* **트레이오프 & 판단 근거**: 분기된 두 브랜치(예: `feature`와 `main`) 간의 최단 경로를 구하기 위해서는 단방향 부모 포인터를 무방향 간선으로 확장 정의하는 트레이오프가 필수적임.

---

### 4) `InvertedIndex` (`mini_git/engine/index.py`)
* **기능**: 커밋 메시지 토큰 및 작성자 이름을 사전(`dict`)에 저장하여 $O(1)$ 검색 제공.
* **사용 알고리즘/자료구조**: 해시 테이블 기반 **역색인 (Inverted Index)** (`dict[word, set[hash]]`).
* **선정 이유**: 커밋 수 $N$이 커질 때 선형 순회($O(N \times L)$)의 심각한 성능 저하를 방지하기 위함.
* **장단점**:
  * *장점*: 검색 실행 시간 $O(1)$ 달성.
  * *단점*: 색인을 저장하기 위한 메모리 오버헤드 $O(W \times C)$ 발생.
* **트레이오프 & 판단 근거**: 커밋 생성 시점에 단어 토큰화를 분산 수행하고 약간의 메모리를 쓰는 대신, 실시간 검색 속도를 획기적으로 향상시킴.

---

### 5) `LcsDiff` (`mini_git/engine/diff.py`)
* **기능**: 두 텍스트 파일의 줄 단위 차이(추가 `+`, 삭제 `-`, 공통 ` `)를 출력.
* **사용 알고리즘**: **LCS (Longest Common Subsequence) DP** 및 역추적(Backtracing).
* **선정 이유**: 외부 diff 라이브러리 없이 순수 DP로 구현 가능한 표준 최장 공통 부분 수열 알고리즘.
* **장단점**:
  * *장점*: 줄 단위의 정확한 차이점 추출.
  * *단점*: 파일 줄 수 $N, M$에 대해 $O(N \times M)$ 시간 및 DP 테이블 메모리 소요.
* **트레이오프 & 판단 근거**: 소형 텍스트 파일 비교 목적이므로 구현 명확성과 외부 라이브러리 미사용 제약 준수를 위해 LCS DP 선택.

---

### 6) `MiniGitRepository` (`mini_git/repository/repo.py`)
* **기능**: 브랜치 포인터, 커밋 데이터베이스, 활성 유저 등의 저장소 상태 머신 관리.
* **사용 알고리즘**: 난수 기반 6자리 16진수 생성 및 `while` 루프 중복 검증.
* **선정 이유**: 간단하면서도 세션 내 완벽한 유일 해시 보장.

---

### 7) `MiniGitReadline` & `CLI_REPL` (`mini_git/cli/`)
* **기능**: 따옴표 공백 인자 파싱, 대소문자 미구분 정규화, 명령 라우팅.
* **사용 알고리즘**: 정규식 기반 토큰화 (`re.findall`).

---

## 5. 코드 레벨 상세 설명 (Line-by-Line Walkthroughs)

### 1) Kahn's Algorithm 위상 정렬 (`mini_git/engine/graph.py`)
```python
def topological_sort(self) -> list:
    # Line 1: 모든 커밋 해시에 대한 진입 차수(indegree) 0으로 초기화
    indegree = {h: 0 for h in self._map}

    # Line 2: 각 커밋 해시별 자식 노드 목록을 저장할 인접 리스트 초기화
    children = {h: [] for h in self._map}

    # Line 3: 간선 순회하여 indegree 및 children 계산
    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                indegree[h] += 1        # 자식 h의 indegree(부모 수) 1 증가
                children[p].append(h)   # 부모 p의 자식 목록에 h 등록

    # Line 4: indegree == 0 (부모가 없는 루트 노드) 커밋을 timestamp 순으로 정렬하여 큐 구성
    queue = Sorter.merge_sort(
        [h for h in self._map if indegree[h] == 0],
        key_func=lambda h: self._map[h].timestamp,
    )

    result = []
    # Line 5: Kahn's Algorithm 루프
    while queue:
        curr = queue.pop(0)             # 진입 차수가 0인 부모 커밋 추출
        result.append(curr)             # 결과 리스트에 수집 (부모 선출력)

        for child in children[curr]:
            indegree[child] -= 1        # 부모가 출력되었으므로 자식의 indegree 1 차감
            if indegree[child] == 0:
                queue.append(child)     # indegree가 0이 된 자식을 큐에 푸시

        # Line 6: 동일 indegree 그룹 간 timestamp 오름차순 유지 (Merge Sort 사용)
        queue = Sorter.merge_sort(
            queue,
            key_func=lambda h: self._map[h].timestamp,
        )

    return result
```

---

### 2) 무방향 BFS 최단 경로 탐색 (`mini_git/engine/graph.py`)
```python
def find_shortest_path(self, start: str, end: str) -> list:
    if start not in self._map or end not in self._map:
        return []
    if start == end:
        return [start]

    # Line 1: 부모-자식 간선을 무방향(Undirected)으로 재구성
    adj: dict[str, set] = {h: set() for h in self._map}
    for h, node in self._map.items():
        for p in node.parents:
            if p in self._map:
                adj[h].add(p)
                adj[p].add(h)

    # Line 2: BFS 탐색 구조 초기화
    queue = [[start]]
    visited: dict[str, int] = {start: 0}   # 노드별 최소 방문 깊이 기록
    shortest: list[list] = []
    target_depth = None

    # Line 3: 레벨 단위 BFS 루프
    while queue:
        path = queue.pop(0)
        depth = len(path) - 1
        node = path[-1]

        if target_depth is not None and depth > target_depth:
            break                       # 최단 거리를 초과하는 경로는 탐색 중단

        if node == end:
            target_depth = depth
            shortest.append(path)       # 최단 거리 경로 수집
            continue

        for nb in adj.get(node, []):
            if nb not in visited or visited[nb] == depth + 1:
                visited[nb] = depth + 1
                queue.append(path + [nb])

    if not shortest:
        return []

    # Line 4: 다중 최단 경로 발생 시 'h1->h2->...' 사전순 최소 경로 선택 (sorted() 미사용)
    best = None
    best_str = None
    for p in shortest:
        s = "->".join(p)
        if best_str is None or s < best_str:
            best_str = s
            best = p

    return best
```

---

### 3) 직접 구현 병합 정렬 (`mini_git/engine/sorter.py`)
```python
class Sorter:
    @staticmethod
    def merge_sort(arr: list, key_func) -> list:
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = Sorter.merge_sort(arr[:mid], key_func)
        right = Sorter.merge_sort(arr[mid:], key_func)
        return Sorter._merge(left, right, key_func)

    @staticmethod
    def _merge(left: list, right: list, key_func) -> list:
        merged = []
        i = j = 0

        # <= 비교 연산자: 동일 키값 발생 시 왼쪽(앞쪽) 원소를 우선 병합하므로 Stable Sort 보장!
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
```

---

## 6. 미흡한 점 및 향후 개선하고 싶은 점 (Limitations & Enhancements)

1. **`LOG` 위상 정렬 재연산 병목**:
   * *현재 한계*: `LOG` 호출 시마다 전체 그래프 노드를 Kahn's Algorithm으로 재정렬함 ($O(V \log V + E)$).
   * *개선 방향*: Git 이력의 단조 증가(Monotonic Add-only) 특성을 활용하여 커밋 작성 시 위상 캐시 배열에 $O(1)$로 덧붙이는 **Incremental Caching** 기법 도입.
2. **영속성(Persistence) 미지원**:
   * *현재 한계*: 메모리 상에서만 작동하여 프로그램 종료 시 저장소 상태가 소멸함.
   * *개선 방향*: 실제 Git처럼 `.git/objects` 디렉토리에 커밋 데이터를 JSON 또는 바이너리 파일로 직렬화하여 저장.
3. **파일 내용 트랙킹(Tree / Blob) 미지원**:
   * *현재 한계*: 커밋 메타데이터중심으로 관리됨.
   * *개선 방향*: 파일의 해시 스냅샷(Blob) 및 디렉토리 구조(Tree) 객체를 신설하여 실제 파일 버전 관리 지원.

---

## 7. 과제 명세에 명시되지 않았으나 평가 항목에 존재하는 핵심 사항 (Implicit Evaluation Items)

과제 문면에는 짧게 서술되었으나, 실제 평가 레포지토리 및 채점표에 핵심 평가 기준으로 존재하는 숨은 주요 항목들입니다:

1. **안정 정렬(Stable Sort) 조건식 검증**:
   * 병합 정렬 시 `left[i] <= right[j]`의 `<=` 조건이 누락될 경우 동률 데이터의 입력 순서가 뒤바뀌어 **안정 정렬 제약 조건 감점** 대상이 됩니다. 본 코드에서는 이를 철저히 준수하였습니다.
2. **`PATH` 최단 경로의 무방향(Undirected) 간선 재정의 필수성**:
   * Git 커밋 포인터는 자식 $\rightarrow$ 부모 단방향으로만 설정되어 있습니다. 만약 방향성 간선 그대로 BFS를 실행하면, 서로 다른 브랜치(`feature`와 `main`) 상의 두 커밋 간에는 서로 도달할 수 없어서 항상 `No path`가 반환됩니다. 따라서 **부모-자식을 무방향 간선으로 재정의하는 작업**이 요구사항을 만족시키기 위해 필수적입니다.
3. **`PATH` 다중 최단 경로의 사전순(Lexicographical) 타이 브레이킹**:
   * 간선 수가 동일한 최단 경로가 여러 개 존재할 때, 경로 문자열(`h1->h2->...`) 기준 **사전순으로 가장 작은 경로를 선택**하는 로직이 채점 기준에 포함되어 있습니다.
4. **옵션 및 공백 포함 따옴표 파싱 유틸리티 (`MiniGitReadline`)**:
   * `COMMIT "Add login feature"`, `SEARCH --author="Alice"`와 같은 공백 포함 따옴표 및 옵션 파싱이 에러 없이 완벽히 동작해야 합니다.
5. **레포 내부 자가 검증 답변서 작성 (`README.md` & `evaluation_evidence.md`)**:
   * 소스 코드 작성뿐만 아니라 레포 내부 질문지에 대한 충실한 한국어 답변 및 실제 실행 증거 트랜스크립트 제출이 채점 항목에 포함되어 있습니다.
