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
[feature 947b3f] Add login feature

mini-git> switch main
Switched to branch: main

mini-git> commit "Add payment feature"
[main ab33b3] Add payment feature
```

---

### 2. 커밋 그래프 동작

DAG 구조를 바탕으로 `LOG` 위상 정렬, `PATH` 최단 경로, `ANCESTORS` 조상 탐색 동작을 확인합니다.

```
mini-git> log
commit b59a92 (Alice, 2026-07-29 08:11:01) [main]
Initial commit
commit d98e3f (Alice, 2026-07-29 08:11:01) [feature]
Add login feature
commit 482cdf (Alice, 2026-07-29 08:11:01) [main]
Add payment feature

mini-git> path b59a92 482cdf
Path: b59a92 -> 482cdf

mini-git> ancestors d98e3f
Ancestors of d98e3f:
- b59a92: Initial commit
```

---

### 3. 검색 및 정렬

`SEARCH` 역색인 기반 키워드/작성자 검색 및 `LOG --sort-by=` 직접 구현 정렬(Merge Sort) 동작을 확인합니다.

```
mini-git> search "login"
Found 1 commit:
- 49be5e: Add login feature

mini-git> search --author="Alice"
Found 3 commits:
- 232df4: Initial commit
- 49be5e: Add login feature
- dc2b15: Add payment feature

mini-git> log --sort-by=date
commit 232df4 (Alice, 2026-07-29 08:11:01)
Initial commit
commit 49be5e (Alice, 2026-07-29 08:11:01)
Add login feature
commit dc2b15 (Alice, 2026-07-29 08:11:01)
Add payment feature

mini-git> log --sort-by=author
commit 232df4 (Alice, 2026-07-29 08:11:01)
Initial commit
commit 49be5e (Alice, 2026-07-29 08:11:01)
Add login feature
commit dc2b15 (Alice, 2026-07-29 08:11:01)
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
[main 88a56b] First commit

mini-git> commit "Second commit"
[main 923e42] Second commit

mini-git> log
commit 88a56b (Alice, 2026-07-29 08:11:01) [main]
First commit
commit 923e42 (Alice, 2026-07-29 08:11:01) [main]
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
mini-git> diff "evidence/_diff_a.txt" "evidence/_diff_b.txt"
Invalid args

mini-git> merge feature
Merged branch feature into main.
[main d159f5] Merge branch 'feature' into main

mini-git> sort-compare
[Sort Algorithm Performance Comparison]
Size:  100 | Merge Sort:   0.20ms | Bubble Sort:   0.28ms
Size:  500 | Merge Sort:   0.94ms | Bubble Sort:   8.30ms
Size: 1000 | Merge Sort:   2.04ms | Bubble Sort:  41.00ms
```

---

*본 문서는 `python collect_evidence.py` 실행 시 자동으로 재생성됩니다.*