# 🖥️ CLI 패키지 기술 문서 (`mini_git/cli/`)

## 1. 개요 및 역할
`cli` 패키지는 사용자의 입력 명령을 처리하고 출력을 전담하는 **표현 계층(Presentation Layer)**입니다.

---

## 2. 모듈 구성
1. **`readline.py` (`MiniGitReadline`)**: 쉘 스타일 토큰화 및 따옴표/옵션 파싱 유틸리티.
2. **`repl.py` (`CLI_REPL`)**: 명령어 디스패처 및 REPL 입력 루프 제어.

---

## 3. 핵심 파싱 메커니즘 및 설계 특성

### 1) `MiniGitReadline` 파싱 정규식
```python
_TOKEN_PATTERN = re.compile(r'\S+?=(?:"[^"]*"|\'[^\']*\'|\S+)|"[^"]*"|\'[^\']*\'|\S+')
```
* **동작 원리**: 
  * 큰따옴표/작은따옴표로 감싸진 공백 포함 인자(`COMMIT "Add login feature"`)를 단일 토큰으로 추출.
  * `--key=value` 및 `--key="value with spaces"` 형태의 옵션을 정상 분리.
  * 추출된 토큰의 외곽 따옴표 자동 제거.

### 2) `CLI_REPL` 대소문자 정규화 및 명령 라우팅
* 명령어 키워드(예: `init`, `INIT`, `Commit`)를 대문자로 정규화하여 핸들러 딕셔너리 매핑.
* `exit` / `quit` / `Ctrl+D` 입력 시 REPL 환경의 안전한 종료 처리.
