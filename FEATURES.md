# Mini Git - 기능 명세 (Features)

## 필수 명령어

### 저장소 및 브랜치 관리

| 명령어 | 설명 | 비고 |
|--------|------|------|
| `INIT <user_name>` | 저장소 초기화 + main 브랜치 생성 + HEAD 설정 + 사용자 설정 | 최초 실행 필수 |
| `BRANCH <branch_name>` | 현재 HEAD를 가리키는 새 브랜치 생성 | - |
| `SWITCH <branch_name>` | HEAD를 지정된 브랜치로 이동 | 존재하지 않는 브랜치 에러 |
| `COMMIT <message>` | 새 커밋 생성 (현재 HEAD를 부모로) + 역색인 갱신 | - |

### 커밋 로그 및 탐색

| 명령어 | 설명 | 출력 조건 |
|--------|------|----------|
| `LOG` | 부모가 자식보다 먼저 출력되는 로그 (위상 정렬 성격) | hash, author, timestamp, message 식별 가능 |
| `LOG --sort-by=date` | timestamp 기준 정렬 | 동률 규칙 자유 |
| `LOG --sort-by=author` | 작성자 기준 정렬 | 동률 규칙 자유 |
| `PATH <commit1> <commit2>` | 두 커밋 사이 최단 경로 (무방향 간선 기준) | 없으면 `No path`, 여러 개면 사전순 최소 경로 |
| `ANCESTORS <commit_hash>` | 해당 커밋에서 도달 가능한 모든 조상 출력 | - |

### 검색

| 명령어 | 설명 | 기반 |
|--------|------|------|
| `SEARCH <keyword>` | 키워드가 포함된 메시지의 커밋 검색 | 역색인 |
| `SEARCH --author=<name>` | 특정 작성자의 커밋 검색 | 역색인 |

## REPL 인터페이스

- 프롬프트: `mini-git>`
- `exit` 또는 `quit` 입력 시 종료
- 명령어 파싱 → 실행 → 결과 출력 반복

## 에러 처리 기준 (표준 에러 메시지)

잘못된 입력 및 유효하지 않은 요청에 대해 아래의 에러 메시지를 표준화하여 출력해야 합니다.
- **인자 오류 (개수/형식 등)**: `Invalid args`
- **존재하지 않는 브랜치 대상**: `Unknown branch: <name>`
- **존재하지 않는 커밋 대상**: `Unknown commit: <hash>`

## 보너스 기능 (선택)

1. **Diff**
   - `diff <file1> <file2>`
   - 줄 단위 비교 (추가/삭제/공통 구분)

2. **Merge**
   - `merge <branch_name>`
   - 2개의 부모를 가진 merge commit 생성

3. **정렬 알고리즘 성능 비교**
   - 2개 이상의 정렬 알고리즘 구현
   - 입력 크기별 실행 시간 비교

---

**참고**: 위 내용은 `B3-2.md` Section 4.1, 4.5 및 Section 5를 기반으로 정리.