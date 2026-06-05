"""
mini_git.engine.sorter
======================

[역할 및 책임]
Python 내장 정렬 API(sorted, list.sort)를 사용하지 않고
직접 구현한 정렬 알고리즘을 제공합니다.

[구현 알고리즘]
병합 정렬 (Merge Sort)
  - 시간 복잡도: 최선·평균·최악 O(N log N)
  - 공간 복잡도: O(N) (임시 병합 배열)
  - 안정 정렬(Stable Sort) 보장:
      병합 시 두 원소의 키가 같을 때 왼쪽 원소를 우선 선택(<=)하여
      입력 순서를 유지합니다.

[의존성]
  없음 (순수 Python)
"""


class Sorter:
    """
    [역할 및 책임]
    키 함수(key_func) 기반의 범용 병합 정렬(Merge Sort)을 제공하는
    정적 메소드 컬렉션 클래스입니다.

    [기능]
    - 임의 타입의 리스트를 key_func 반환값 기준으로 오름차순 정렬
    - 안정 정렬 보장
    - sorted() / list.sort() 미사용
    """

    @staticmethod
    def merge_sort(arr: list, key_func) -> list:
        """
        [역할] 병합 정렬의 분할(Divide) 단계를 담당합니다.

        [기능]
        리스트를 절반씩 재귀적으로 분할한 뒤, 정렬된 두 부분을
        _merge 를 통해 합칩니다.

        [구현 사항]
        - 길이 0 또는 1인 리스트는 이미 정렬된 상태이므로 즉시 반환합니다.
        - 원본 리스트를 변경하지 않고 새 리스트를 반환합니다.

        Args:
            arr      : 정렬 대상 리스트
            key_func : 비교 기준을 반환하는 단항 함수

        Returns:
            list: key_func 기준 오름차순으로 정렬된 새 리스트
        """
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = Sorter.merge_sort(arr[:mid], key_func)
        right = Sorter.merge_sort(arr[mid:], key_func)
        return Sorter._merge(left, right, key_func)

    @staticmethod
    def _merge(left: list, right: list, key_func) -> list:
        """
        [역할] 정렬된 두 부분 리스트를 합치는 병합(Merge) 단계입니다.

        [기능]
        두 리스트의 원소를 key_func 반환값 순서로 비교하며 하나의
        정렬된 리스트로 결합합니다.

        [구현 사항]
        - left[i] 의 키 <= right[j] 의 키일 때 left 원소를 먼저 선택합니다.
          동일 키에서 left 를 우선하므로 입력 순서가 보존되어 안정 정렬이 됩니다.
        - 두 포인터(i, j) 방식으로 O(N) 시간에 병합합니다.

        Args:
            left     : 정렬된 왼쪽 부분 리스트
            right    : 정렬된 오른쪽 부분 리스트
            key_func : 비교 기준 함수

        Returns:
            list: 두 리스트를 합친 정렬된 새 리스트
        """
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            # <= 비교: 동일 키일 때 left(앞쪽 입력)를 먼저 삽입 → Stable Sort
            if key_func(left[i]) <= key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # 남은 원소 추가
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
