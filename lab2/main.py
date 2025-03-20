from utils import time_memory_decorator
from typing import Optional, Tuple, List


class Node:
    def __init__(self, ch: str) -> None:
        """
        Инициализирует узел rope со значением символа.

        Параметры:
          ch (str): Символ, хранящийся в узле.
        """
        self.ch: str = ch
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.parent: Optional['Node'] = None
        self.size: int = 1


def update(node: Optional[Node]) -> None:
    """
    Обновляет размер поддерева узла.

    Параметры:
      node (Optional[Node]): Узел для обновления.
    """
    if node is None:
        return
    node.size = 1
    if node.left:
        node.size += node.left.size
        node.left.parent = node
    if node.right:
        node.size += node.right.size
        node.right.parent = node


def rotate(x: Node) -> None:
    """
    Выполняет вращение узла x относительно его родителя.

    Параметры:
      x (Node): Узел, который поднимается.
    """
    p = x.parent
    if not p:
        return
    g = p.parent
    if p.left == x:
        p.left = x.right
        if x.right:
            x.right.parent = p
        x.right = p
    else:
        p.right = x.left
        if x.left:
            x.left.parent = p
        x.left = p
    p.parent = x
    x.parent = g
    if g:
        if g.left == p:
            g.left = x
        else:
            g.right = x
    update(p)
    update(x)


def splay(x: Node) -> Node:
    """
    Поднимает узел x до корня splay-дерева.

    Параметры:
      x (Node): Узел для подъёма.

    Возвращает:
      Node: Новый корень дерева.
    """
    while x.parent:
        p = x.parent
        g = p.parent
        if g:
            if (g.left == p) == (p.left == x):
                rotate(p)  # Zig-zig
            else:
                rotate(x)  # Zig-zag
        rotate(x)
    return x


def merge(left: Optional[Node], right: Optional[Node]) -> Optional[Node]:
    """
    Объединяет два splay-дерева так, что все узлы left идут перед узлами right.

    Параметры:
      left (Optional[Node]): Левое дерево.
      right (Optional[Node]): Правое дерево.

    Возвращает:
      Optional[Node]: Корень объединённого дерева.
    """
    if left is None:
        return right
    if right is None:
        return left
    cur = left
    while cur.right:
        cur = cur.right
    left = splay(cur)
    left.right = right
    right.parent = left
    update(left)
    return left


def split(root: Optional[Node], index: int) -> Tuple[Optional[Node], Optional[Node]]:
    """
    Делит дерево на две части:
      Левая часть содержит узлы с индексами [0, index-1],
      Правая часть — с индексами [index, ...].

    Параметры:
      root (Optional[Node]): Корень дерева.
      index (int): Позиция раздела (0 ≤ index ≤ size дерева).

    Возвращает:
      Tuple[Optional[Node], Optional[Node]]: (левая часть, правая часть).

    Генерирует:
      ValueError, если index вне диапазона.
    """
    if root is None:
        return None, None
    if index < 0 or index > root.size:
        raise ValueError("Invalid split index")
    if index == 0:
        return None, root
    if index == root.size:
        return root, None

    cur = root
    while True:
        left_size = cur.left.size if cur.left else 0
        if index < left_size:
            cur = cur.left
        elif index > left_size:
            index -= left_size + 1
            if cur.right is None:
                # Это может произойти, если индекс равен размеру дерева, но обработано выше.
                break
            cur = cur.right
        else:
            break
    root = splay(cur)
    left = root.left
    if left:
        left.parent = None
    root.left = None
    update(root)
    return left, root


def build_rope(s: str) -> Optional[Node]:
    """
    Строит сбалансированное splay-дерево (rope) из строки s за O(n).

    Параметры:
      s (str): Исходная строка.

    Возвращает:
      Optional[Node]: Корень дерева.
    """

    def build(left: int, right: int) -> Optional[Node]:
        if left > right:
            return None
        mid = (left + right) // 2
        node = Node(s[mid])
        node.left = build(left, mid - 1)
        if node.left:
            node.left.parent = node
        node.right = build(mid + 1, right)
        if node.right:
            node.right.parent = node
        update(node)
        return node

    return build(0, len(s) - 1)


def rope_cut_and_paste(root: Optional[Node], i: int, j: int, k: int) -> Optional[Node]:
    """
    Выполняет операцию вырезания подстроки s[i...j] из rope и вставляет её после k-го символа оставшейся строки.

    Параметры:
      root (Optional[Node]): Корень rope.
      i (int): Начальный индекс подстроки (включительно).
      j (int): Конечный индекс подстроки (включительно).
      k (int): Позиция вставки (при k=0 вставка в начало).

    Возвращает:
      Optional[Node]: Новый корень rope после операции.

    Генерирует:
      ValueError: Если i > j, или индексы невалидны.
    """
    if i < 0 or j < 0 or k < 0:
        raise ValueError("Indices must be non-negative")
    if i > j:
        raise ValueError("Invalid query: i must be <= j")

    # Разбиваем дерево на A и B: A содержит [0, i-1], B содержит [i, ...]
    A, B = split(root, i)
    if B is None or B.size < (j - i + 1):
        raise ValueError("Invalid query: j is out of range")

    # Разбиваем B на C и D: C содержит [i, j], D содержит [j+1, ...]
    C, D = split(B, j - i + 1)
    # Объединяем A и D — получаем дерево без вырезанной подстроки
    merged = merge(A, D)
    # Проверяем диапазон для k
    rem_size = merged.size if merged else 0
    if k < 0 or k > rem_size:
        raise ValueError("Invalid query: k is out of range")
    # Разбиваем merged на L и R: L содержит [0, k-1], R содержит [k, ...]
    L, R = split(merged, k)
    # Вставляем вырезанную часть между L и R
    return merge(merge(L, C), R)


def traverse(root: Optional[Node]) -> str:
    """
    Выполняет in-order обход rope и собирает итоговую строку.

    Параметры:
      root (Optional[Node]): Корень дерева.

    Возвращает:
      str: Строка, полученная из дерева.
    """
    result: List[str] = []
    stack: List[Node] = []
    cur = root
    while stack or cur:
        if cur:
            stack.append(cur)
            cur = cur.left
        else:
            cur = stack.pop()
            result.append(cur.ch)
            cur = cur.right
    return "".join(result)


@time_memory_decorator
def file_io() -> None:
    """
    Обрабатывает файлы:
      - Читает входные данные из файла txt/input.txt.
      - Выполняет операции вырезания и вставки подстроки в структуре Rope.
      - Записывает итоговую строку в файл txt/output.txt.
    """
    with open("txt/input.txt", "r") as f:
        lines = f.read().splitlines()
    s: str = lines[0].strip()
    n: int = int(lines[1].strip())
    queries: List[Tuple[int, int, int]] = [
        tuple(map(int, line.split())) for line in lines[2:2 + n]
    ]

    root = build_rope(s)
    for i, j, k in queries:
        root = rope_cut_and_paste(root, i, j, k)
    result: str = traverse(root)

    with open("txt/output.txt", "w") as f:
        f.write(result)


if __name__ == "__main__":
    file_io()
