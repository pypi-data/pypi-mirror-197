from docstruct.text_block import Paragraph


class Node:
    def __init__(self, data: object):
        self.data: object = data
        self.neighbors: list[Node] = []

    def add_neighbor(self, neighbor: "Node"):
        self.neighbors.append(neighbor)

    def __str__(self):
        return f"{self.__class__.__name__}(data = {self.data})"

    def __repr__(self):
        return str(self)


class Graph:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def get_connected_components(
        self, nodes_order: list[Node] = None
    ) -> list[list[Node]]:
        if nodes_order is None:
            nodes_order = self.nodes
        visited = set()
        connected_components: list[list[Node]] = []
        for node in nodes_order:
            if node not in visited:
                connected_component = self.get_connected_component(node, visited)
                connected_components.append(connected_component)
        return connected_components

    def get_connected_component(self, node: Node, visited: set[Node]) -> list[Node]:
        stack = [node]
        connected_component = []
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                connected_component.append(current)
                for neighbor in current.neighbors:
                    stack.append(neighbor)
        return connected_component

    @staticmethod
    def is_symmetric(graph: "Graph"):
        for node in graph.nodes:
            for neighbor in node.neighbors:
                if node not in neighbor.neighbors:
                    return False
        return True

    def get_nodes_with_bounded_degree(
        self, min_degree: int = 0, max_degree: int = -1
    ) -> list[Node]:
        if max_degree == -1:
            max_degree = len(self.nodes)
        nodes = []
        for node in self.nodes:
            if min_degree <= len(node.neighbors) <= max_degree:
                nodes.append(node)
        return nodes

    def remove_node(self, node: Node):
        """
        Remove a given node from the graph.
        For undirected graphs only!
        """

        for neighbor in node.neighbors:
            neighbor.neighbors.remove(node)
        node.neighbors = []
        self.nodes.remove(node)

    def topological_sort(self) -> list[Node]:
        num_nodes = len(self.nodes)
        in_degree = [0 for _ in range(num_nodes)]
        for node in range(num_nodes):
            for neighbor in self.nodes[node].neighbors:
                in_degree[neighbor.data] += 1
        queue = []
        for node in range(num_nodes):
            if in_degree[node] == 0:
                queue.append(self.nodes[node])

        sorted_nodes = []

        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for neighbor in self.nodes[node.data].neighbors:
                in_degree[neighbor.data] -= 1
                if in_degree[neighbor.data] == 0:
                    queue.append(self.nodes[neighbor.data])
        if len(sorted_nodes) < num_nodes:
            raise Exception("Graph is not a DAG")
        return [node.data for node in sorted_nodes]


class BipartiteGraph(Graph):
    def __init__(self, left_nodes: list[Node], right_nodes: list[Node]):
        super().__init__(left_nodes + right_nodes)
        self.left_nodes = left_nodes
        self.right_nodes = right_nodes

    def remove_node(self, node: Node):
        super().remove_node(node)
        if node in self.left_nodes:
            self.left_nodes.remove(node)
        else:
            self.right_nodes.remove(node)


class ParaGraph(Graph):
    def __init__(self, nodes, paragraphs: list[Paragraph], height_offset: int):
        super(ParaGraph, self).__init__(nodes)
        self.paragraphs = paragraphs
        self.height_offset = height_offset
        self.pre_sort = self.top_left_traversal_sort()

    def paragraph_sort(self) -> list[Node]:
        num_nodes = len(self.nodes)
        in_degree = [0 for _ in range(num_nodes)]
        for node in range(num_nodes):
            for neighbor in self.nodes[node].neighbors:
                in_degree[neighbor.data] += 1
        queue = []
        for node in range(num_nodes):
            if in_degree[node] == 0:
                queue.append(self.nodes[node])
        if len(queue) == 0:
            queue.append(self.nodes[self.pre_sort[0].data])

        sorted_nodes = []

        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for neighbor in self.nodes[node.data].neighbors:
                if neighbor not in sorted_nodes:
                    in_degree[neighbor.data] -= 1
                    if in_degree[neighbor.data] == 0:
                        queue.append(self.nodes[neighbor.data])

            if len(queue) == 0 and len(sorted_nodes) < num_nodes:
                for node in self.pre_sort:
                    if node not in sorted_nodes:
                        queue.append(self.nodes[node.data])
                        break
        return [node.data for node in sorted_nodes]

    def top_left_traversal_sort(self):
        if len(self.nodes) <= 1:
            return self.nodes
        sorted_nodes_by_height = sorted(
            self.nodes,
            key=lambda node: self.paragraphs[node.data]
            .get_bounding_box()
            .get_center()
            .y,
            reverse=True,
        )

        same_line = [sorted_nodes_by_height[0]]
        ordered_list = []
        for i in range(len(sorted_nodes_by_height[:-1])):
            if (
                abs(
                    self.paragraphs[sorted_nodes_by_height[i].data]
                    .get_bounding_box()
                    .get_center()
                    .y
                    - self.paragraphs[sorted_nodes_by_height[i + 1].data]
                    .get_bounding_box()
                    .get_center()
                    .y
                )
                < self.height_offset / 2
            ):
                same_line.append(sorted_nodes_by_height[i + 1])
            else:
                ordered_same_line = sorted(
                    same_line,
                    key=lambda node: self.paragraphs[node.data]
                    .get_bounding_box()
                    .get_left(),
                )
                ordered_list += ordered_same_line
                same_line = [sorted_nodes_by_height[i + 1]]

        return ordered_list
