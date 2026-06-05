# Mini Git CLI - 필수 증거 (Mandatory Evidence)

본 문서는 `collect_evidence.py` 실행을 통해 자동 수집된 Mini Git CLI 프로그램의 동작 검증 트랜스크립트입니다.
[DELIVERABLES.md](../DELIVERABLES.md)의 필수 증거 항목(1~6) 기준에 맞추어 각 항목별로 출력 결과를 기록합니다.

---

### 1. 저장소 초기화 및 브랜치 관리

`INIT`, `BRANCH`, `SWITCH`, `COMMIT` 명령 정상 동작 및 커밋 생성 시 hash 출력을 확인합니다.

```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> branch feature
Created branch: feature

mini-git> switch feature
Switched to branch: feature

mini-git> commit "Add login feature"
[feature 0e5207] Add login feature

mini-git> switch main
Switched to branch: main

mini-git> commit "Add payment feature"
[main b343f1] Add payment feature
```

---

### 2. 커밋 그래프 동작

DAG 구조를 바탕으로 `LOG` 위상 정렬, `PATH` 최단 경로, `ANCESTORS` 조상 탐색 동작을 확인합니다.

```
mini-git> log
commit 34f589 (Alice, 2026-06-04 08:22:53) [main]
Initial commit
commit 46b83b (Alice, 2026-06-04 08:22:53) [feature]
Add login feature
commit cbeacd (Alice, 2026-06-04 08:22:53) [main]
Add payment feature

mini-git> path 34f589 cbeacd
Path: 34f589 -> cbeacd

mini-git> ancestors 46b83b
Ancestors of 46b83b:
- 34f589: Initial commit
```

---

### 3. 검색 및 정렬

`SEARCH` 역색인 기반 키워드/작성자 검색 및 `LOG --sort-by=` 직접 구현 정렬(Merge Sort) 동작을 확인합니다.

```
mini-git> search "login"
Found 1 commit:
- d882b3: Add login feature

mini-git> search --author="Alice"
Found 3 commits:
- 3f4676: Initial commit
- d882b3: Add login feature
- 42f332: Add payment feature

mini-git> log --sort-by=date
commit 3f4676 (Alice, 2026-06-04 08:22:53)
Initial commit
commit d882b3 (Alice, 2026-06-04 08:22:53)
Add login feature
commit 42f332 (Alice, 2026-06-04 08:22:53)
Add payment feature

mini-git> log --sort-by=author
commit 3f4676 (Alice, 2026-06-04 08:22:53)
Initial commit
commit d882b3 (Alice, 2026-06-04 08:22:53)
Add login feature
commit 42f332 (Alice, 2026-06-04 08:22:53)
Add payment feature
```

---

### 4. CLI REPL

`mini-git>` 프롬프트에서 명령을 반복 입력하고, `exit`/`quit`으로 정상 종료되는 흐름을 확인합니다.

```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> commit "First commit"
[main 98b650] First commit

mini-git> commit "Second commit"
[main 594667] Second commit

mini-git> log
commit 98b650 (Alice, 2026-06-04 08:22:53) [main]
First commit
commit 594667 (Alice, 2026-06-04 08:22:53) [main]
Second commit

mini-git> exit
Exiting...
```

---

### 5. 코드 품질

알고리즘 로직(탐색/정렬/인덱싱)이 독립된 클래스로 분리되어 있으며, 모든 주요 함수에 역할·책임·기능·구현 사항 Docstring이 작성된 것을 확인합니다.

```
# main.py 내 독립 구현 클래스 목록
#
# 1. CommitNode         - 커밋 메타데이터 자료구조 (hash, message, author, timestamp, parents)
# 2. InvertedIndex      - 키워드/작성자 역색인 검색 엔진 (O(1) 조회)
# 3. Sorter             - 병합 정렬(Merge Sort) 직접 구현 (sorted/list.sort 미사용)
# 4. CommitGraph        - 위상 정렬 / BFS 최단 경로 / 조상 탐색 알고리즘
# 5. MiniGitRepository  - 저장소 상태 머신 (브랜치, HEAD, 커밋 맵 관리)
# 6. BonusFeatures      - LCS Diff / Merge commit 생성 (보너스)
# 7. CLI_REPL           - 따옴표 파싱 지원 명령어 파서 및 REPL 제어 루프
#
# 각 클래스·메소드에 [역할] [기능] [구현 사항] 형식의 Docstring 작성 완료
```

---

### 6. 보너스 (선택)

`DIFF` 줄 단위 파일 비교(LCS), `MERGE` 다중 부모 커밋 생성, 정렬 알고리즘 성능 비교(Merge Sort vs Bubble Sort) 동작을 확인합니다.

```
mini-git> diff "evidence\_diff_a.txt" "evidence\_diff_b.txt"
  Line 1
- Line 2
+ Line 2 modified
  Line 3
+ Line 4 added

mini-git> merge feature
Merged branch feature into main.
[main f3bbad] Merge branch 'feature' into main

mini-git> sort-compare
[Sort Algorithm Performance Comparison]
Size:  100 | Merge Sort:   0.17ms | Bubble Sort:   0.52ms
Size:  500 | Merge Sort:   1.13ms | Bubble Sort:   8.51ms
Size: 1000 | Merge Sort:   2.40ms | Bubble Sort:  42.10ms
```

---

*본 문서는 `python collect_evidence.py` 실행 시 자동으로 재생성됩니다.*