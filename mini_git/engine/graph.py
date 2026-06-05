"""
mini_git.engine.graph
=====================

[역할 및 책임]
커밋 DAG(방향성 비순환 그래프)에 대한 탐색 알고리즘을 전담합니다.
저장소 상태(commit_map)를 주입받아 동작하며, 상태를 직접 변경하지 않습니다.

[구현 알고리즘]
1. topological_sort  : Kahn's Algorithm 기반 위상 정렬
2. find_shortest_path: 무방향 BFS + 사전순 타이 브레이킹
3. get_ancestors     : BFS 기반 조상 전체 탐색

[의존성]
  mini_git.model.commit (CommitNode)
  mini_git.engine.sorter (Sorter)
"""

from mini_git.engine.sorter import Sorter


class CommitGraph:
    """
    [역할 및 책임]
    커밋 해시 맵(dict[str, CommitNode])을 기반으로 그래프 탐색 알고리즘을
    실행하는 서비스 클래스입니다.
    외부에서 commit_map 을 주입받아 사용하며, 내부 상태를 가지지 않습니다.

    [기능]
    - 위상 정렬: LOG 명령에서 부모가 자식보다 먼저 출력되도록 순서 결정
    - 최단 경로: PATH 명령에서 두 커밋 사이 최소 간선 경로 탐색
    - 조상 탐색: ANCESTORS 명령에서 특정 커밋의 모든 조상 수집
    """

    def __init__(self, commit_map: dict):
        """
        [역할] 그래프 알고리즘 실행을 위한 커밋 맵 참조를 저장합니다.

        [구현 사항]
        commit_map 은 외부(Repository)에서 관리되며 이 클래스는
        읽기 전용으로만 사용합니다.

        Args:
            commit_map: dict[str, CommitNode] — 해시 → 커밋 노드 매핑
        """
        self._map = commit_map

    # ------------------------------------------------------------------
    # 1. 위상 정렬 (Topological Sort)
    # ------------------------------------------------------------------

    def topological_sort(self) -> list:
        """
        [역할] 전체 커밋을 '부모가 자식보다 먼저 나오는' 순서로 정렬합니다.

        [기능]
        Kahn's Algorithm을 사용해 진입 차수(indegree) 기준으로 정렬합니다.
        동일 진입 차수의 커밋은 timestamp 오름차순으로 처리하여 출력 일관성을 보장합니다.

        [구현 사항]
        1. 각 커밋의 indegree(부모 수)와 children(자식 목록)을 계산합니다.
        2. indegree == 0 인 루트 커밋을 timestamp 순으로 큐에 삽입합니다.
        3. 큐에서 커밋을 꺼내 결과에 추가하고, 자식의 indegree를 감소시킵니다.
        4. indegree가 0이 된 자식을 큐에 추가하고 큐를 재정렬합니다.

        Returns:
            list[str]: 위상 정렬된 커밋 해시 목록
        """
        indegree = {h: 0 for h in self._map}
        children = {h: [] for h in self._map}

        # 진입 차수(indegree) 및 자식 관계 계산
        for h, node in self._map.items():
            for p in node.parents:
                if p in self._map:
                    indegree[h] += 1
                    children[p].append(h)

        # 루트 커밋(indegree == 0)을 timestamp 오름차순으로 초기 큐 구성
        queue = Sorter.merge_sort(
            [h for h in self._map if indegree[h] == 0],
            key_func=lambda h: self._map[h].timestamp,
        )

        result = []
        while queue:
            curr = queue.pop(0)
            result.append(curr)

            for child in children[curr]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

            # 큐를 timestamp 순으로 재정렬하여 일관성 유지
            queue = Sorter.merge_sort(
                queue,
                key_func=lambda h: self._map[h].timestamp,
            )

        return result

    # ------------------------------------------------------------------
    # 2. 최단 경로 탐색 (Shortest Path — 무방향 BFS)
    # ------------------------------------------------------------------

    def find_shortest_path(self, start: str, end: str) -> list:
        """
        [역할] 두 커밋 사이의 무방향 최단 경로를 탐색합니다.

        [기능]
        - 커밋 간 간선을 무방향으로 취급하여 BFS로 최단 경로를 찾습니다.
        - 최단 경로가 여럿이면 'h1->h2->...' 문자열이 사전순으로 가장 작은
          경로를 반환합니다.
        - 경로가 없으면 빈 리스트를 반환합니다.

        [구현 사항]
        1. 부모-자식 간선을 양방향으로 인접 리스트를 구성합니다.
        2. BFS로 레벨 단위 탐색을 수행하며 최단 거리(target_depth)를 확정합니다.
        3. target_depth를 초과하는 경로는 탐색을 중단합니다.
        4. 수집된 최단 경로 중 문자열 표현이 사전순 최소인 경로를 선택합니다.

        Args:
            start: 시작 커밋 해시
            end  : 목표 커밋 해시

        Returns:
            list[str]: 경로 상의 커밋 해시 목록 (없으면 [])
        """
        if start not in self._map or end not in self._map:
            return []

        if start == end:
            return [start]

        # 무방향 인접 리스트 구성
        adj: dict[str, set] = {h: set() for h in self._map}
        for h, node in self._map.items():
            for p in node.parents:
                if p in self._map:
                    adj[h].add(p)
                    adj[p].add(h)

        # BFS: 경로 전체를 큐에 저장하며 탐색
        queue = [[start]]
        visited: dict[str, int] = {start: 0}   # hash → 방문 깊이
        shortest: list[list] = []
        target_depth = None

        while queue:
            path = queue.pop(0)
            depth = len(path) - 1
            node = path[-1]

            if target_depth is not None and depth > target_depth:
                break

            if node == end:
                target_depth = depth
                shortest.append(path)
                continue

            for nb in adj.get(node, []):
                if nb not in visited or visited[nb] == depth + 1:
                    visited[nb] = depth + 1
                    queue.append(path + [nb])

        if not shortest:
            return []

        # 사전순 최소 경로 선택 (직접 비교, sorted() 미사용)
        best = None
        best_str = None
        for p in shortest:
            s = "->".join(p)
            if best_str is None or s < best_str:
                best_str = s
                best = p

        return best

    # ------------------------------------------------------------------
    # 3. 조상 탐색 (Ancestors — BFS)
    # ------------------------------------------------------------------

    def get_ancestors(self, commit_hash: str) -> list:
        """
        [역할] 지정 커밋에서 도달 가능한 모든 조상 커밋을 수집합니다.

        [기능]
        부모 포인터를 따라 BFS로 탐색하여 직접·간접 조상을 모두 반환합니다.
        지정 커밋 자신은 결과에 포함하지 않습니다.

        [구현 사항]
        - visited set 으로 중복 방문을 방지합니다.
        - 결과를 timestamp 오름차순(Merge Sort)으로 정렬해 반환합니다.

        Args:
            commit_hash: 조상을 탐색할 대상 커밋 해시

        Returns:
            list[str]: timestamp 오름차순으로 정렬된 조상 커밋 해시 목록
        """
        if commit_hash not in self._map:
            return []

        ancestors: set = set()
        queue = list(self._map[commit_hash].parents)

        while queue:
            curr = queue.pop(0)
            if curr in self._map and curr not in ancestors:
                ancestors.add(curr)
                queue.extend(self._map[curr].parents)

        return Sorter.merge_sort(
            list(ancestors),
            key_func=lambda h: self._map[h].timestamp,
        )
