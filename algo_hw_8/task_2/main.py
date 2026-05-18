class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def get_height(node):
    return node.height if node else 0


def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def left_rotate(z):
    y = z.right
    t2 = y.left
    y.left = z
    z.right = t2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y):
    x = y.left
    t3 = x.right
    x.right = y
    y.left = t3
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def insert(root, key):
    if not root:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and key < root.left.key:
        return right_rotate(root)
    if balance < -1 and key > root.right.key:
        return left_rotate(root)
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root


def tree_sum(root):
    if root is None:
        return 0
    return root.key + tree_sum(root.left) + tree_sum(root.right)


if __name__ == "__main__":
    root = None
    values = [25, 10, 40, 5, 18, 30, 50, 1, 7]
    for value in values:
        root = insert(root, value)

    print(f"Значення у дереві: {values}")
    print(f"Сума всіх значень: {tree_sum(root)}")
