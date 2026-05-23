import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="#cccccc"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def gradient_color(index: int, total: int) -> str:
    if total <= 1:
        ratio = 1.0
    else:
        ratio = index / (total - 1)
    r = int(0x12 + (0xC8 - 0x12) * ratio)
    g = int(0x55 + (0xE0 - 0x55) * ratio)
    b = int(0xA0 + (0xFF - 0xA0) * ratio)
    return f"#{r:02X}{g:02X}{b:02X}"


def count_nodes(root: Node) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def dfs_iterative(root: Node) -> list:
    if root is None:
        return []
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def bfs_iterative(root: Node) -> list:
    if root is None:
        return []
    order = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


def color_traversal(root: Node, traversal_fn) -> None:
    order = traversal_fn(root)
    total = len(order)
    for index, node in enumerate(order):
        node.color = gradient_color(index, total)


def draw_tree(root: Node, title: str, filename: str) -> None:
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.savefig(filename)
    plt.show()


def build_sample_tree() -> Node:
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.left.right.left = Node(11)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.right = Node(7)
    return root


def reset_colors(root: Node, color: str = "#cccccc") -> None:
    if root is None:
        return
    root.color = color
    reset_colors(root.left, color)
    reset_colors(root.right, color)


if __name__ == "__main__":
    root = build_sample_tree()

    color_traversal(root, dfs_iterative)
    draw_tree(root, "Обхід у глибину (DFS, стек)", "dfs_traversal.png")

    reset_colors(root)
    color_traversal(root, bfs_iterative)
    draw_tree(root, "Обхід у ширину (BFS, черга)", "bfs_traversal.png")
