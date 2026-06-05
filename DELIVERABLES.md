# Mini Git - 결과물 및 필수 증거 (Deliverables & Evidence)

## 필수 제출물

| 항목 | 설명 | 필수 여부 |
|------|------|----------|
| `main.py` (또는 동등한 엔트리 포인트) | 프로그램 실행 파일 | 필수 |
| `README.md` | 프로젝트 설명서 | 필수 |

## 실행 방법

```bash
python main.py
```

## 필수 증거 (Mandatory Evidence)

프로그램이 정상 동작함을 증명하기 위해 아래 항목이 충족되어야 함:

1. **저장소 초기화 및 브랜치 관리**
   - `INIT`, `BRANCH`, `SWITCH`, `COMMIT` 명령 정상 동작
   - 커밋 생성 시 커밋 hash 출력 (저장소 초기화 및 브랜치 생성/전환 시 결과 메시지 출력)

2. **커밋 그래프 동작**
   - DAG 구조 유지
   - `LOG`에서 부모가 자식보다 먼저 출력
   - `PATH`, `ANCESTORS` 명령 정상 동작

3. **검색 및 정렬**
   - `SEARCH` 및 `SEARCH --author=` 역색인 기반으로 동작
   - `LOG --sort-by=` 명령에서 **직접 구현한 정렬** 사용

4. **CLI REPL**
   - `mini-git>` 프롬프트에서 반복 입력 가능
   - `exit`/`quit`로 정상 종료

5. **코드 품질**
   - 알고리즘 로직(탐색/정렬/인덱싱)이 **독립된 함수/클래스**로 분리
   - 주요 함수에 docstring 또는 주석 작성

6. **보너스 (선택)**
   - Diff, Merge, 정렬 성능 비교 중 하나 이상 구현 시 가산점

## 결과물 예시 구조

```
mini-git/
├── main.py (필수 제출)
└── README.md (필수 제출)
```
*(참고: REQUIREMENTS.md, FEATURES.md, DELIVERABLES.md, CONSTRAINTS.md 등의 명세 관련 Markdown 파일은 제출하지 않아도 무방합니다.)*

---

**참고**: `B3-2.md` Section 2 및 Section 3을 기반으로 정리.