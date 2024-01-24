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
        pass
