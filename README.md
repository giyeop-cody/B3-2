# Mini Git CLI 프로그램

본 프로젝트는 Git의 핵심 구조인 그래프 자료구조와 역색인, 사용자 정의 정렬 알고리즘을 직접 구현하여 완성한 CLI 기반의 **Mini Git** 프로그램입니다.

---

## 1. 실행 방법

본 프로그램은 Python 3.10 이상에서 동작합니다. 아래 명령어를 통해 REPL(Read-Eval-Print Loop) 환경을 실행할 수 있습니다.

```bash
python main.py
```

### 명령어 입력 예시
```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> commit "Initial commit"
[main e6310f] Initial commit

mini-git> branch feature
Created branch: feature

mini-git> switch feature
Switched to branch: feature

mini-git> commit "Add login feature"
[feature 1f29bb] Add login feature
```

---

## 2. 과제 목표 자가 설명 (학습 목표 답변)

### Q1. Git의 커밋 구조가 왜 DAG(방향성 비순환 그래프)인지 설명할 수 있는가?
* **답변**: Git의 커밋은 이전 상태(부모 커밋)를 가리키는 포인터를 가집니다. 일반적인 커밋은 1개의 부모를 가지며, 머지 커밋의 경우 2개 이상의 부모를 가질 수 있습니다. 커밋은 시간의 흐름에 따라 과거(부모)로만 방향성을 가지며, 미래의 커밋이 과거의 커밋의 부모가 될 수 없으므로 순환(Cycle)이 발생하지 않는 **방향성 비순환 그래프(DAG, Directed Acyclic Graph)** 구조를 이룹니다.

### Q2. “부모가 먼저 출력되는 로그”를 만들기 위해 어떤 접근이 필요한가?
* **답변**: 부모 커밋이 자식 커밋보다 항상 먼저 출력되기 위해서는 그래프의 의존 관계에 따라 노드를 정렬하는 **위상 정렬(Topological Sort)** 알고리즘이 필요합니다. 본 프로젝트에서는 각 커밋에 대해 진입 차수(Indegree, 부모의 수)를 구하고, 진입 차수가 0인 루트 커밋부터 큐에 삽입하여 자식 노드의 진입 차수를 낮추는 **Kahn's Algorithm**을 통해 부모-자식 순서가 완벽히 보장되는 로그 목록을 생성합니다.

### Q3. 두 커밋 사이의 최단 경로를 찾는 방법과 특정 커밋의 모든 조상을 탐색하는 방법은?
* **최단 경로 탐색**: 커밋 간의 간선을 방향성이 없는 무방향 간선으로 간주하여 인접 리스트를 구축합니다. 이후 **너비 우선 탐색(BFS, Breadth-First Search)**을 사용하여 탐색 거리(간선 수)가 최소인 모든 최단 경로를 구하고, 경로가 여러 개인 경우 문자열 표현(`hash1->hash2->...`) 기준으로 사전순이 가장 작은 경로를 채택합니다.
* **조상 탐색**: 특정 커밋에서 시작하여 부모 포인터(`parents`)를 역추적하는 탐색(BFS 또는 DFS)을 수행합니다. 중복 방지를 위한 방문 세트(`visited`)를 두어 모든 조상 노드를 수집한 후, 시간 오름차순으로 정렬하여 반환합니다.

### Q4. 직접 구현한 정렬 알고리즘의 시간 복잡도와 안정성(Stable Sort) 여부는?
* **답변**: 본 프로젝트는 **병합 정렬(Merge Sort)** 알고리즘을 직접 구현하였습니다.
  - **시간 복잡도**: 최선, 평균, 최악의 경우 모두 **$O(N \log N)$**의 일관된 성능을 보장합니다.
  - **안정성 (Stable Sort)**: 분할 후 병합하는 과정에서 왼쪽 하위 배열의 키와 오른쪽 하위 배열의 키가 같을 때 왼쪽 요소를 우선적으로 선택하는 조건식(`left[i] <= right[j]`)을 사용하여, 동일한 정렬 키를 가진 요소들의 원래 순서가 유지되는 **안정 정렬**을 만족하도록 설계하였습니다.

### Q5. 역색인(Inverted Index)의 동작 원리와 선형 순회보다 빠른 이유는?
* **답변**: 
  - **동작 원리**: 커밋이 생성될 때 메시지를 형태소/단어 단위로 토큰화하여 소문자로 정규화한 후, 각 키워드와 작성자를 Key로 하고 해당 키워드가 포함된 커밋 해시 세트(Set)를 Value로 하는 해시맵을 구축합니다.
  - **선형 순회와의 속도 비교**: 모든 커밋의 메시지를 처음부터 끝까지 문자열 검색하는 선형 순회 방식은 $O(N \times L)$(N: 커밋 수, L: 메시지 길이)의 시간이 걸립니다. 반면, 역색인은 해시맵 조회 속도가 평균적으로 **$O(1)$**이므로 커밋 수가 대량으로 늘어나도 실시간에 준하는 빠른 검색 속도를 보여줍니다.

---

## 3. 구현된 핵심 클래스 및 구조

프로그램은 관심사 분리와 계층형 아키텍처 설계 원칙(Model → Engine → Repository → CLI)에 따라 독립된 모듈로 구조화되었습니다.

*   **[main.py](main.py)**: 프로그램의 단일 진입점(Entry Point). `CLI_REPL`을 임포트하여 REPL 루프를 시작합니다.
*   **[mini_git/](mini_git/)**: 프로그램의 핵심 패키지
    *   **[model/](mini_git/model/) (데이터 계층)**
        *   [commit.py](mini_git/model/commit.py) (`CommitNode`): 커밋 객체 데이터 모델 (해시, 저자, 타임스탬프, 메시지, 부모 목록 등)
    *   **[engine/](mini_git/engine/) (알고리즘 및 핵심 엔진 계층)**
        *   [sorter.py](mini_git/engine/sorter.py) (`Sorter`): 직접 구현한 안정 정렬 알고리즘 (Merge Sort)
        *   [graph.py](mini_git/engine/graph.py) (`CommitGraph`): Kahn's Algorithm 위상 정렬, BFS 기반 무방향 최단 경로 탐색, 조상 역추적 탐색
        *   [index.py](mini_git/engine/index.py) (`InvertedIndex`): 키워드 및 작성자 역색인 기반 O(1) 검색 엔진
        *   [diff.py](mini_git/engine/diff.py) (`LcsDiff`): LCS DP 알고리즘 기반 줄 단위 파일 비교 (보너스)
    *   **[repository/](mini_git/repository/) (저장소 비즈니스 로직 계층)**
        *   [repo.py](mini_git/repository/repo.py) (`MiniGitRepository`): 저장소 초기화, 브랜치 맵 관리, 브랜치 전환 및 커밋 생성(Merge 포함) 등의 상태 관리
    *   **[cli/](mini_git/cli/) (표현 계층)**
        *   [readline.py](mini_git/cli/readline.py) (`MiniGitReadline`): 쉘 스타일 토큰화(따옴표 및 옵션 지원) 및 옵션 파싱 유틸리티
        *   [repl.py](mini_git/cli/repl.py) (`CLI_REPL`): 명령어 디스패처 및 REPL 입력 처리 제어 루프

---

## 4. 제약 사항 준수 여부

1. **그래프 전용 라이브러리 사용 금지**: 기본 dict와 set을 활용하여 그래프 구조를 직접 코드로 다루었습니다.
2. **표준 정렬 API 금지**: `sorted()` 및 `list.sort()`를 소스코드 전체에서 일절 사용하지 않고, 직접 작성한 `Sorter.merge_sort` 메소드를 통해서만 정렬을 수행하였습니다.
3. **독립된 클래스/함수 분리**: 정렬, 역색인, 그래프, 저장소, REPL 로직이 명확한 단일 책임 원칙에 맞추어 클래스로 구현되었습니다.
4. **상세 주석 작성**: 각 파일, 클래스, 메소드마다 역할, 책임, 기능, 구현 사항을 한국어로 작성한 상세 Docstring이 명시되어 있습니다.

---

## 5. 필수 증거 (Mandatory Evidence)

프로그램이 모든 제약 조건 및 요구사항에 맞추어 정상 동작함을 증명하기 위한 터미널 세션 로그 자료입니다.
- **[동작 검증 증거 자료 (Markdown)](./evidence/evidence.md)**: 요구사항에 부합하는 명령어 실행 로그를 수집하여 마크다운 문서로 기록하였습니다.

---

## 6. 평가 문항 답변 및 실제 동작 검증

본 섹션은 `evaluation_question.md`에 기재된 평가 질문들에 대해, 실제 코드의 구현 및 동작 검증을 기준으로 작성한 답변서 및 실행 결과입니다.

### 항목 1: 기능 구현 검증 (실제 동작 기반)

*   **Q1. `INIT <user_name>` 실행 후 main 브랜치/HEAD/현재 사용자 설정이 정상적으로 초기화되어 있는가?**
    *   **답변**: 예, 정상 초기화됩니다. `init` 명령은 저장소 상태를 리셋하여 `branches` 맵에 `main: None`을 설정하고 활성 브랜치를 `main`으로 이동시키며 `current_user`를 입력받은 사용자명으로 설정합니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        ```
        mini-git> init "Alice"
        Initialized repository.
        Current branch: main
        Current user: Alice
        ```
*   **Q2. `BRANCH <name>` 생성 후 `SWITCH <name>` 로 전환되며, 이후 `COMMIT` 이 해당 브랜치에 반영되는가?**
    *   **답변**: 예. `branch feature` 명령을 통해 현재 HEAD 커밋을 가리키는 `feature` 브랜치를 생성하고, `switch feature`로 활성 브랜치(`current_branch`)를 이동시킨 뒤 `commit` 실행 시 해당 브랜치의 HEAD 포인터만 신규 커밋으로 갱신해 나갑니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        ```
        mini-git> branch feature
        Created branch: feature

        mini-git> switch feature
        Switched to branch: feature

        mini-git> commit "Add login feature"
        [feature f826d4] Add login feature
        ```
*   **Q3. LOG 가 “부모 커밋이 자식 커밋보다 먼저” 출력되도록 동작하는가?**
    *   **답변**: 예. `log` 명령어 실행 시 그래프의 상속 및 의존 관계인 진입 차수(Indegree)에 따라 정렬하는 위상 정렬(Kahn's Algorithm)이 적용되어 부모 커밋이 자식 커밋보다 반드시 먼저 출력됩니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        ```
        mini-git> log
        commit ad48cc (Alice, 2026-06-04 09:10:11) [main]
        Initial commit
        commit f826d4 (Alice, 2026-06-04 09:10:11) [feature]
        Add login feature
        commit 6b666f (Alice, 2026-06-04 09:10:11) [main]
        Add payment feature
        ```
*   **Q4. `PATH <a> <b>` 가 경로가 있으면 최단 경로를, 없으면 `No path` 를 출력하는가?**
    *   **답변**: 예. 무방향 BFS 탐색 알고리즘을 사용해 최단 경로를 탐색하며, 경로가 존재하면 `Path: a -> ... -> b` 형태로 출력하고 없는 경우 `No path`를 반환합니다. 다중 최단 경로 시 사전순 최소 경로를 선택합니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        ```
        mini-git> path ad48cc 6b666f
        Path: ad48cc -> 6b666f
        ```
*   **Q5. `ANCESTORS <hash>` 가 모든 조상을 빠짐없이 출력하는가?**
    *   **답변**: 예. 지정 커밋의 부모들을 추적해나가는 BFS 탐색을 통해 직접/간접 조상을 누락 없이 수집하고, 타임스탬프 기준으로 정렬하여 반환합니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        ```
        mini-git> ancestors 6b666f
        Ancestors of 6b666f:
        - ad48cc: Initial commit
        ```
*   **Q6. `SEARCH <keyword> / SEARCH --author=<name> / LOG --sort-by=date|author` 가 요구사항대로 동작하는가?**
    *   **답변**: 예. 메시지 역색인 및 옵션 파싱(공백포함 따옴표), 직접 구현한 Sorter(Merge Sort)를 통한 안정 정렬이 요구사항대로 동작합니다.
    *   **실제 실행 증거 (명령어 및 터미널 결과)**:
        *   **메시지 키워드 검색 (`SEARCH <keyword>`)**:
            ```
            mini-git> search "login"
            Found 1 commit:
            - f826d4: Add login feature
            ```
        *   **작성자 검색 (`SEARCH --author=<name>`)**:
            ```
            mini-git> search --author="Alice"
            Found 3 commits:
            - f826d4: Add login feature
            - 6b666f: Add payment feature
            - ad48cc: Initial commit
            ```
        *   **날짜순 정렬 로그 (`LOG --sort-by=date`)**:
            ```
            mini-git> log --sort-by=date
            commit ad48cc (Alice, 2026-06-04 09:10:11)
            Initial commit
            commit f826d4 (Alice, 2026-06-04 09:10:11)
            Add login feature
            commit 6b666f (Alice, 2026-06-04 09:10:11)
            Add payment feature
            ```
        *   **작성자순 정렬 로그 (`LOG --sort-by=author`)**:
            ```
            mini-git> log --sort-by=author
            commit ad48cc (Alice, 2026-06-04 09:10:11)
            Initial commit
            commit f826d4 (Alice, 2026-06-04 09:10:11)
            Add login feature
            commit 6b666f (Alice, 2026-06-04 09:10:11)
            Add payment feature
            ```

### 항목 2: 설계 및 책임 분리

*   **Q1. 커밋 저장소/브랜치/HEAD/사용자 정보를 어떤 구조로 분리했고, 각 책임을 설명할 수 있는가?**
    *   **답변**: 계층 아키텍처 원칙에 따라 분리하여 관심사 및 결합도를 낮췄습니다.
        *   `CommitNode` (Model 계층): 해시, 작성자, 시간, 메시지, 부모 목록 필드를 보유한 불변 데이터 개체입니다.
        *   `MiniGitRepository` (Repository 계층): `branches` 포인터 맵, `commit_map` 데이터베이스 및 `InvertedIndex` 인스턴스를 보관하며 상태 전이를 제어합니다.
        *   `CLI_REPL` & `MiniGitReadline` (CLI 표현 계층): 입출력 인터페이스 구동, 명령어 토큰화 및 따옴표 옵션 파싱 등의 유틸리티 책임을 갖습니다.
*   **Q2. 커밋 hash로 빠르게 조회하기 위해 어떤 키-값 구조를 사용했고, 중복/충돌을 어떻게 방지했는지 설명할 수 있는가?**
    *   **답변**: 커밋 해시를 Key로 하고 `CommitNode` 인스턴스를 Value로 매핑하는 파이썬 해시맵 딕셔너리(`dict`)를 사용해 평균 O(1) 조회 성능을 냅니다. 해시 생성 시 무작위 6자리 16진수를 생성한 후 `commit_map`에 존재하지 않을 때까지 `while` 루프로 검증 및 재추출하여 중복을 원천 차단합니다.
*   **Q3. 커밋이 추가될 때 역색인(author/keyword)을 어떤 시점에, 어떤 방식으로 갱신하도록 설계했는지 설명할 수 있는가?**
    *   **답변**: `MiniGitRepository.commit` 시점에 신규 `CommitNode`를 성공적으로 데이터베이스에 삽입한 즉시, `self.inverted_index.add_commit(node)`을 동기 호출합니다. 작성자명을 소문자화해 맵에 삽입하고, 메시지를 공백 기준 `split()` 및 소문자화하여 단어별 Key에 해시 Set을 구성하는 형태로 점진적 갱신합니다.
*   **Q4. LOG , PATH , ANCESTORS 에서 사용하는 그래프 탐색 로직을 어떻게 재사용 가능하게 구성했는지 설명할 수 있는가?**
    *   **답변**: 상태 비소유 엔진인 `CommitGraph` 서비스 클래스로 탐색 로직을 완전 분리하였습니다. 생성자로 `commit_map`만을 주입받아 읽기 전용으로 알고리즘만 처리함으로써 여러 계층이나 다른 연산(LOG, PATH, ANCESTORS)에서 중복 로직 없이 순수 알고리즘 메소드를 호출해 재사용할 수 있습니다.
*   **Q5. 주요 함수/클래스에 docstring/주석을 어떤 기준으로 작성했는지 설명할 수 있는가?**
    *   **답변**: 클래스와 함수 단위별로 `[역할 및 책임]`, `[기능]`, `[구현 사항 / 설계 의도]` 세 섹션을 두어, 설계 목적과 시간복잡도 제약 준수 방안(예: Merge Sort 안정 정렬 조건 등)을 한국어로 투명하고 일관성 있게 기술하였습니다.

### 항목 3: 알고리즘 및 복잡도 분석

*   **Q1. 커밋 그래프가 왜 DAG여야 하는지, 사이클이 생기면 어떤 문제가 발생하는지 설명할 수 있는가?**
    *   **답변**: 커밋 이력은 미래의 커밋이 과거 커밋의 부모가 될 수 없는 일방적인 시간 흐름성(인과성)을 가집니다. 따라서 방향성 비순환 그래프(DAG) 구조여야 합니다. 사이클이 존재하면 위상 정렬이 불가능(진입 차수가 0으로 내려가지 않음)해져 로그 출력이 안 되며, 최단 경로 및 조상 탐색 시 무한 루프나 Stack Overflow에 빠지게 됩니다.
*   **Q2. LOG 에서 “부모가 먼저” 조건을 만족시키기 위해 어떤 접근(예: 위상정렬 성격의 출력)을 적용했는지 설명할 수 있는가?**
    *   **답변**: **Kahn's Algorithm 위상 정렬**을 도입하여 해결하였습니다. 각 커밋의 진입 차수(Indegree, 즉 자식 관점의 부모 수)를 구하고, 진입 차수가 0인 루트들을 큐에 넣은 후 순차적으로 꺼내면서 연결된 자식들의 차수를 낮춰 다시 큐에 넣는 위상 차수 차감 루프를 적용했습니다.
*   **Q3. PATH 에서 최단 경로를 찾기 위해 어떤 알고리즘(예: BFS)을 선택했고, 간선을 무방향으로 정의한 이유를 설명할 수 있는가?**
    *   **답변**: 모든 간선 가중치가 1인 트리 형태에서 최단 거리를 무조건 보장하는 **BFS(너비 우선 탐색)**를 선택했습니다. 무방향 간선으로 취급한 이유는, Git 구조상 간선이 역방향(자식 $\rightarrow$ 부모)으로만 설정되어 있어 방향성 간선으로 조회 시 분기된 타 브랜치의 두 커밋(예: `feature`와 `main`) 간에는 서로 도달할 수 없어 경로 조회가 불가능해지기 때문입니다.
*   **Q4. 정렬 알고리즘의 평균/최악 시간복잡도와 안정 정렬 여부를 설명할 수 있는가?**
    *   **답변**: 직접 구현한 **병합 정렬(Merge Sort)**은 최선, 평균, 최악 모두 **O(N log N)**의 시간복잡도를 가지며, 나뉜 배열을 병합할 때 동률 데이터에 대해 앞쪽에 있던 요소를 선점하도록 부등호(`left[i] <= right[j]`) 조건을 주어 **안정 정렬(Stable Sort)**을 완전하게 보장합니다.
*   **Q5. 역색인이 순회 검색보다 빠른 이유를, 자료구조/시간복잡도 관점에서 설명할 수 있는가?**
    *   **답변**: 리스트 순회 검색은 $N$개 커밋의 메시지 길이 $L$을 다 훑으므로 **O(N * L)**의 시간이 소요되는 반면, 역색인은 해시 테이블 기반의 딕셔너리(`dict`)에서 사전에 색인된 단어(Key)로 즉시 탐색하여 평균 **O(1)** 시간에 일련의 커밋 해시 셋을 획득하므로 압도적으로 빠릅니다.

### 항목 4: 심화 고찰 및 확장 전략

*   **Q1. 커밋 수가 10배 늘어났을 때 병목이 될 지점을 예측하고, 개선 방향(자료구조/알고리즘)을 설명할 수 있는가?**
    *   **답변**: `LOG` 명령 호출 시마다 그래프의 전체 노드들을 위상 정렬하는 Kahn's Algorithm 연산이 병목 지점이 될 것입니다.
        *   *개선 방향*: 매번 처음부터 정렬하지 않고, 커밋 생성 시점마다 이전 정렬 결과 뒤에 추가되는 방식으로 정렬을 점진적(Incremental) 갱신 및 캐싱하도록 만들거나, 한 번에 전체를 출력하지 않고 현재 HEAD에서 역추적하여 일부 개수만 반환하는 Paging 기법을 도입하여 처리해야 합니다.
*   **Q2. PATH 의 간선 정의를 “부모 방향만 허용”으로 바꾸면 결과가 어떻게 달라지고, 구현은 무엇을 바꿔야 하는지 설명할 수 있는가?**
    *   **답변**:
        *   *결과*: 서로 다른 브랜치(공통 조상에서 분기된 다른 노선) 사이의 경로는 무조건 `No path`가 나오며, 오직 자손 커밋에서 조상 커밋으로 이동하는 수직적 시간 역선 상에서만 경로가 발견될 것입니다.
        *   *구현 변경*: `CommitGraph.find_shortest_path`에서 인접 리스트(`adj`)를 구성할 때 자식과 부모를 양방향으로 묶어주던 관계를 생략하고, 오직 `adj[h].add(p)`와 같이 자식(`h`) 노드에서 부모(`p`) 노드로만 향하는 단방향 간선만 등록해야 합니다.
*   **Q3. `LOG --sort-by=author` 요구사항이 “부모-자식 선후도 유지”로 강화된다면, 어떤 전략으로 해결할지 설명할 수 있는가?**
    *   **답변**: 위상적 순서는 보장하면서, 부모-자식 관계가 없어 선후 관계가 무관한 병렬 커밋들(예: 서로 다른 브랜치의 개별 작업들) 사이에서만 작성자 순서로 정렬이 이루어져야 합니다.
        *   *해결 전략*: Kahn's Algorithm 기반 위상 정렬 수행 시 진입 차수가 0이 되어 큐에 들어가는 후보군들을 작성자 소문자 오름차순 우선순위를 가진 **우선순위 큐(Priority Queue)**로 정렬 보존하여 하나씩 추출(Pop)해 내는 전략을 적용하면, 계통적 제약을 침범하지 않는 선에서 작성자순을 유지하도록 정렬할 수 있습니다.
*   **Q4. 해시 생성 방식을 카운터 기반 ↔ 난수 기반으로 바꿀 때 테스트/재현성/디버깅에 미치는 영향을 설명할 수 있는가?**
    *   **답변**:
        *   *난수 기반 (현재 방식)*: 매 실행 시마다 해시가 달라지므로 충돌 가능성이 낮으나, 테스트 검증 코드에서 예측 결과값 해시를 하드코딩할 수 없어 정규식 캡처나 동적 맵핑 Assert가 강제되므로 디버깅 및 재현성이 복잡해집니다.
        *   *카운터 기반 (또는 고정 해시함수)*: 실행 제어 흐름과 그래프 구조가 같다면 매번 동일한 고정 해시값(예: `000001`, `000002` 등)이 도출되므로 테스트 코드 작성이 단순해지고 재현이 극도로 용이해져 디버깅 편의성이 향상됩니다.

---

### 실제 동작 검증 세션 로그

아래는 `run_evaluation.py` 스크립트를 빌드하여, REPL 환경에서 모든 명령어(INIT, BRANCH, SWITCH, COMMIT, LOG, PATH, ANCESTORS, SEARCH, LOG --sort-by, MERGE, SORT-COMPARE)를 실행한 실제 결과를 리다이렉션하여 출력한 터미널 트랜스크립트입니다.

```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> commit "Initial commit"
[main ad48cc] Initial commit

mini-git> branch feature
Created branch: feature

mini-git> switch feature
Switched to branch: feature

mini-git> commit "Add login feature"
[feature f826d4] Add login feature

mini-git> switch main
Switched to branch: main

mini-git> commit "Add payment feature"
[main 6b666f] Add payment feature

mini-git> log
commit ad48cc (Alice, 2026-06-04 09:10:11) [main]
Initial commit
commit f826d4 (Alice, 2026-06-04 09:10:11) [feature]
Add login feature
commit 6b666f (Alice, 2026-06-04 09:10:11) [main]
Add payment feature

mini-git> path ad48cc 6b666f
Path: ad48cc -> 6b666f

mini-git> ancestors 6b666f
Ancestors of 6b666f:
- ad48cc: Initial commit

mini-git> search "login"
Found 1 commit:
- f826d4: Add login feature

mini-git> search --author="Alice"
Found 3 commits:
- f826d4: Add login feature
- 6b666f: Add payment feature
- ad48cc: Initial commit

mini-git> log --sort-by=date
commit ad48cc (Alice, 2026-06-04 09:10:11)
Initial commit
commit f826d4 (Alice, 2026-06-04 09:10:11)
Add login feature
commit 6b666f (Alice, 2026-06-04 09:10:11)
Add payment feature

mini-git> log --sort-by=author
commit ad48cc (Alice, 2026-06-04 09:10:11)
Initial commit
commit f826d4 (Alice, 2026-06-04 09:10:11)
Add login feature
commit 6b666f (Alice, 2026-06-04 09:10:11)
Add payment feature

mini-git> merge feature
Merged branch feature into main.
[main 5d3881] Merge branch 'feature' into main

mini-git> sort-compare
[Sort Algorithm Performance Comparison]
Size:  100 | Merge Sort:   0.17ms | Bubble Sort:   0.28ms
Size:  500 | Merge Sort:   1.05ms | Bubble Sort:   8.70ms
Size: 1000 | Merge Sort:   2.24ms | Bubble Sort:  44.87ms
```

---

## 7. 추가 참고 가이드 및 하위 기술 문서 안내

본 프로젝트의 심층 이해와 동료 평가(Peer Review)를 원활히 진행할 수 있도록 아래 추가 기술 문서들을 제공합니다.

*   **[동료 평가(Peer Review) 종합 가이드](./PEER_EVALUATION_GUIDE.md)**: 평가자 이해도 수준별(초심자/숙련자) 채점 안내서.
*   **[대화형 HTML 시각화 가이드](./dag_visualizer.html)**: DAG, Kahn's Algo, BFS, 역색인 동적 애니메이션 시뮬레이터.
*   **[패키지별 기술 문서]**:
    *   [mini_git/model/README.md](./mini_git/model/README.md): `CommitNode` 데이터 모델 기술 문서.
    *   [mini_git/engine/README.md](./mini_git/engine/README.md): 정렬/그래프/역색인/Diff 핵심 알고리즘 기술 문서.
    *   [mini_git/repository/README.md](./mini_git/repository/README.md): 저장소 상태 관리 기술 문서.
    *   [mini_git/cli/README.md](./mini_git/cli/README.md): CLI 정규식 토큰화 및 REPL 기술 문서.
