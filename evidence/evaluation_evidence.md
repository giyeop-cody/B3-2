# Evaluation Scenario Execution Session

본 세션 로그는 `run_evaluation.py` 실행을 통해 수집한 터미널 REPL 세션 출력입니다.

```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> commit "Initial commit"
[main 17af75] Initial commit

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

mini-git> log
commit 17af75 (Alice, 2026-07-29 08:11:01) [main]
Initial commit
commit 5c376c (Alice, 2026-07-29 08:11:01) [feature]
Add login feature
commit d422b0 (Alice, 2026-07-29 08:11:01) [main]
Add payment feature

mini-git> path 17af75 d422b0
Path: 17af75 -> d422b0

mini-git> ancestors d422b0
Ancestors of d422b0:
- 17af75: Initial commit

mini-git> search "login"
Found 1 commit:
- 5c376c: Add login feature

mini-git> search --author="Alice"
Found 3 commits:
- 17af75: Initial commit
- 5c376c: Add login feature
- d422b0: Add payment feature

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

mini-git> merge feature
Merged branch feature into main.
[main 21f380] Merge branch 'feature' into main

mini-git> sort-compare
[Sort Algorithm Performance Comparison]
Size:  100 | Merge Sort:   0.29ms | Bubble Sort:   0.42ms
Size:  500 | Merge Sort:   1.80ms | Bubble Sort:  13.90ms
Size: 1000 | Merge Sort:   3.81ms | Bubble Sort:  53.82ms
```