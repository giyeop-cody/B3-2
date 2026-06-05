# Evaluation Scenario Execution Session

본 세션 로그는 `run_evaluation.py` 실행을 통해 수집한 터미널 REPL 세션 출력입니다.

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