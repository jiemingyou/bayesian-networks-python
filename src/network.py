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

    def not_in_list(self, list1: list, list2: list) -> bool:
        """Check if list1 is not in list2."""
        for item in list1:
            if item in list2:
                return False
        return True

    def add_node(self, node: str) -> None:
        """Add a node to the network."""
        self.nodes.add(node)

    def add_edge(self, node1: str, node2: str) -> None:
        """
        Add an directed edge to the network.
        node1 -> node2
        """
        self.edges.add((node1, node2))

    def get_parents(self, node: str) -> list:
        """Get the parents of a node."""
        parents = []
        for edge in self.edges:
            if edge[1] == node:
                parents.append(edge[0])
        return parents

    def get_children(self, node: str) -> list:
        """Get the children of a node."""
        children = []
        for edge in self.edges:
            if edge[0] == node:
                children.append(edge[1])
        return children

    def get_neighbors(self, node: str) -> list:
        """Get the neighbors of a node."""
        neighbors = []
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append(edge[1])
            elif edge[1] == node:
                neighbors.append(edge[0])
        return neighbors

    def get_paths(self, node1: str, node2: str, visited: set = None) -> list:
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

    def is_blocked(self, path: list, cond: list) -> bool:
        """Check if a path between node1 and node2 is blocked."""
        Z = set(cond)
        for w in path:
            if self.is_collider(w):
                if w not in Z and self.not_in_list(self.get_parents(w), Z):
                    return True
            else:
                if w in Z:
                    return True
        return False

    def is_d_separated(self, node1: str, node2: str, cond: list) -> bool:
        """Check if node1 and node2 are d-separated given cond."""
        for path in self.get_paths(node1, node2):
            if not self.is_blocked(path, cond):
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

    print(bn.is_d_separated("A", "B", ["C"]))
    print(bn.is_d_separated("A", "B", []))
    print(bn.is_d_separated("C", "E", ["B", "D"]))
    print(bn.is_d_separated("C", "D", ["A", "B"]))
    print(bn.is_d_separated("B", "F", ["A", "C"]))
    print(bn.is_d_separated("A", "E", ["D", "F"]))
