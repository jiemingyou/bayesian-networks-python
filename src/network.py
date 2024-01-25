from typing import Set, List


class BayesianNetwork:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"

    def __repr__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"

    def add_node(self, node: str) -> None:
        """Add a node to the network."""
        self.nodes.add(node)

    def add_edge(self, node1: str, node2: str) -> None:
        """
        Add an directed edge to the network.
        node1 -> node2
        """
        self.edges.add((node1, node2))

    def get_parents(self, node: str) -> Set[str]:
        """Get the parents of a node."""
        parents = set()
        for edge in self.edges:
            if edge[1] == node:
                parents.add(edge[0])
        return parents

    def get_descendants(self, node: str) -> Set[str]:
        """Get the descendants of a node."""
        descendants = set()
        for edge in self.edges:
            if edge[0] == node:
                descendants.add(edge[1])
                descendants.update(self.get_descendants(edge[1]))
        return descendants

    def get_neighbors(self, node: str) -> Set[str]:
        """Get the neighbors of a node."""
        neighbors = set()
        for edge in self.edges:
            if edge[0] == node:
                neighbors.add(edge[1])
            elif edge[1] == node:
                neighbors.add(edge[0])
        return neighbors

    def get_paths(
        self,
        node1: str,
        node2: str,
        visited: Set[str] = None,
    ) -> List[List[str]]:
        """
        Get all paths from node1 to node2.
        Treat the network as an undirected graph.
        """
        if visited is None:
            visited = set()
        visited.add(node1)

        paths = []
        if node1 == node2:
            return [[node1]]

        for node in self.get_neighbors(node1):
            if node not in visited:
                for path in self.get_paths(node, node2, visited.copy()):
                    paths.append([node1] + path)

        return paths

    def is_collider(self, node1: str) -> bool:
        """Check if a node is a collider."""
        return len(self.get_parents(node1)) >= 2

    def is_collider_in_path(self, node, path: list) -> bool:
        """Check if a node is a collider in a path."""
        if len(path) < 3:
            return False
        shared_nodes = set(path).intersection(self.get_parents(node))
        return len(shared_nodes) >= 2

    def no_common_nodes(self, set1: Set[str], set2: Set[str]) -> bool:
        """Check if two sets have any common nodes."""
        return len(set1.intersection(set2)) == 0

    def is_blocked(self, path: list, C: Set[str]) -> bool:
        """Check if a path between node1 and node2 is blocked."""

        for w in path:
            if self.is_collider_in_path(w, path):
                descendants = self.get_descendants(w)
                # Neither the collider nor any of its descendants are in the conditioning set
                if (w not in C) and (self.no_common_nodes(descendants, C)):
                    return True
            elif w in C:
                # The non-collider is in the conditioning set
                return True

        return False

    def is_d_separated(
        self,
        node1: str,
        node2: str,
        C: Set[str],
    ):
        """Check if node1 and node2 are d-separated given cond."""
        for path in self.get_paths(node1, node2):
            if not self.is_blocked(path, C):
                return False, path

        return True


if __name__ == "__main__":
    bn = BayesianNetwork()
    bn.add_node("A")
    bn.add_node("B")
    bn.add_node("C")
    bn.add_node("D")
    bn.add_node("E")
    bn.add_node("F")

    bn.add_edge("A", "C")
    bn.add_edge("A", "D")
    bn.add_edge("A", "F")
    bn.add_edge("B", "C")
    bn.add_edge("B", "E")
    bn.add_edge("C", "D")
    bn.add_edge("D", "E")
    bn.add_edge("F", "E")

    print("a)", bn.is_d_separated("A", "B", {"C"}))
    print("b)", bn.is_d_separated("A", "B", {}))
    print("c)", bn.is_d_separated("C", "E", {"B", "D"}))
    print("d)", bn.is_d_separated("C", "D", {"A", "B"}))
    print("e)", bn.is_d_separated("B", "F", {"A", "C"}))
    print("f)", bn.is_d_separated("A", "E", {"D", "F"}))
