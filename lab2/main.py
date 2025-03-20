from utils import time_memory_decorator
from typing import Optional, Tuple, List


# Класс Node представляет узел splay-дерева, который хранит один символ строки.
class Node:
    __slots__ = ['ch', 'left', 'right', 'parent', 'size']

    def __init__(self, ch: str) -> None:
        # Инициализация узла: сохраняем символ, ссылки на детей и родителя, а также размер поддерева.
        self.ch: str = ch           # Символ, который хранится в узле.
        self.left: Optional['Node'] = None   # Ссылка на левое поддерево.
        self.right: Optional['Node'] = None  # Ссылка на правое поддерево.
        self.parent: Optional['Node'] = None # Ссылка на родительский узел.
        self.size: int = 1          # Размер поддерева (начально 1, так как узел сам по себе).


# Функция update пересчитывает поле size для узла, суммируя размеры его поддеревьев.
def update(node: Optional[Node]) -> None:
    if node is None:
        return
    node.size = 1  # Начинаем с единицы для самого узла.
    if node.left:
        node.size += node.left.size  # Добавляем размер левого поддерева.
        node.left.parent = node      # Обновляем родительскую ссылку для левого ребенка.
    if node.right:
        node.size += node.right.size  # Добавляем размер правого поддерева.
        node.right.parent = node     # Обновляем родительскую ссылку для правого ребенка.


# Функция rotate выполняет поворот узла x относительно его родителя.
def rotate(x: Node) -> None:
    p = x.parent         # Узнаем родителя узла x.
    if not p:
        return           # Если родителя нет, поворот невозможен.
    g = p.parent         # Узнаем родителя родителя (необходим для переназначения связи).
    if p.left == x:
        # Если x является левым ребенком, переносим правое поддерево x на место x у p.
        p.left = x.right
        if x.right:
            x.right.parent = p
        x.right = p      # x становится родителем p.
    else:
        # Если x является правым ребенком, переносим левое поддерево x на место x у p.
        p.right = x.left
        if x.left:
            x.left.parent = p
        x.left = p       # x становится родителем p.
    p.parent = x         # p теперь является ребенком x.
    x.parent = g         # x наследует родителя от p.
    if g:
        # Если существует g, заменяем p на x в его поддереве.
        if g.left == p:
            g.left = x
        else:
            g.right = x
    update(p)            # Обновляем размер поддерева для p.
    update(x)            # Обновляем размер поддерева для x.


# Функция splay поднимает узел x до корня дерева.
def splay(x: Node) -> Node:
    while x.parent:
        p = x.parent
        g = p.parent
        if g:
            # Выбираем тип поворота: zig-zig или zig-zag.
            if (g.left == p) == (p.left == x):
                rotate(p)  # Zig-zig: сначала поворачиваем родителя.
            else:
                rotate(x)  # Zig-zag: сначала поворачиваем сам узел x.
        rotate(x)  # Выполняем поворот узла x.
    return x  # После подъема x становится корнем дерева.


# Функция merge объединяет два splay-дерева так, что все узлы из left идут до узлов из right.
def merge(left: Optional[Node], right: Optional[Node]) -> Optional[Node]:
    if left is None:
        return right
    if right is None:
        return left
    cur = left
    # Находим самый правый узел в левом дереве (последний символ).
    while cur.right:
        cur = cur.right
    left = splay(cur)    # Поднимаем этот узел к корню.
    left.right = right   # Присоединяем правое дерево как правое поддерево.
    right.parent = left  # Устанавливаем родительскую связь.
    update(left)         # Обновляем размер поддерева.
    return left


# Функция split делит дерево на две части по индексу.
# Левая часть содержит первые index элементов, правая – оставшиеся.
def split(root: Optional[Node], index: int) -> Tuple[Optional[Node], Optional[Node]]:
    if root is None:
        return None, None
    if index < 0 or index > root.size:
        raise ValueError("Invalid split index")
    if index == 0:
        return None, root
    if index == root.size:
        return root, None

    cur = root
    # Используем размер поддеревьев, чтобы спуститься к нужному узлу.
    while True:
        left_size = cur.left.size if cur.left else 0
        if index < left_size:
            cur = cur.left  # Ищем в левом поддереве.
        elif index > left_size:
            index -= left_size + 1  # Учитываем левое поддерево и текущий узел.
            if cur.right is None:
                break
            cur = cur.right  # Ищем в правом поддереве.
        else:
            break  # Нашли узел, где количество узлов в левом поддереве равно index.
    root = splay(cur)  # Поднимаем найденный узел к корню.
    left = root.left   # Левая часть – все узлы, находящиеся слева от корня.
    if left:
        left.parent = None  # Отсоединяем левую часть от корня.
    root.left = None   # Очищаем ссылку на левое поддерево у корня.
    update(root)       # Обновляем размер корня.
    return left, root


# Функция build_rope строит сбалансированное splay-дерево (rope) из заданной строки.
def build_rope(s: str) -> Optional[Node]:
    def build(left: int, right: int) -> Optional[Node]:
        if left > right:
            return None  # Если диапазон пуст, возвращаем None.
        mid = (left + right) // 2  # Находим средний индекс для балансировки.
        node = Node(s[mid])        # Создаем узел для символа из середины.
        node.left = build(left, mid - 1)   # Рекурсивно строим левое поддерево.
        if node.left:
            node.left.parent = node
        node.right = build(mid + 1, right)  # Рекурсивно строим правое поддерево.
        if node.right:
            node.right.parent = node
        update(node)  # Обновляем размер узла с учетом его поддеревьев.
        return node
    return build(0, len(s) - 1)


# Функция rope_cut_and_paste реализует основную операцию: вырезание подстроки S[i...j] и вставка её
# после k-го символа оставшейся строки.
def rope_cut_and_paste(root: Optional[Node], i: int, j: int, k: int) -> Optional[Node]:
    # Проверяем, что индексы неотрицательны и что i не больше j.
    if i < 0 or j < 0 or k < 0:
        raise ValueError("Indices must be non-negative")
    if i > j:
        raise ValueError("Invalid query: i must be <= j")

    # Разбиваем дерево на две части: A содержит символы [0, i-1], а B содержит символы [i, конец].
    A, B = split(root, i)
    if B is None or B.size < (j - i + 1):
        raise ValueError("Invalid query: j is out of range")

    # Из дерева B вырезаем поддерево C (подстрока S[i...j]) и получаем D, которое содержит оставшиеся символы.
    C, D = split(B, j - i + 1)
    # Объединяем A и D, чтобы получить дерево без вырезанной подстроки.
    merged = merge(A, D)
    # Проверяем, что позиция вставки k не превышает размер обновленного дерева.
    rem_size = merged.size if merged else 0
    if k < 0 or k > rem_size:
        raise ValueError("Invalid query: k is out of range")
    # Разбиваем дерево merged на L (первые k символов) и R (оставшиеся символы).
    L, R = split(merged, k)
    # Вставляем вырезанную подстроку C между L и R и возвращаем итоговое дерево.
    return merge(merge(L, C), R)


# Функция traverse выполняет in-order обход дерева и собирает символы в итоговую строку.
def traverse(root: Optional[Node]) -> str:
    result: List[str] = []
    stack: List[Node] = []
    cur = root
    # Обход дерева с использованием стека: идем влево, затем обрабатываем узлы, потом идем вправо.
    while stack or cur:
        if cur:
            stack.append(cur)
            cur = cur.left  # Переход к левому поддереву.
        else:
            cur = stack.pop()
            result.append(cur.ch)  # Добавляем символ текущего узла.
            cur = cur.right  # Переход к правому поддереву.
    return "".join(result)


# Функция file_io осуществляет ввод исходных данных, выполнение операций над деревом и вывод результата в файл.
@time_memory_decorator
def file_io() -> None:
    with open("txt/input.txt", "r") as f:
        lines = f.read().splitlines()
    s: str = lines[0].strip()  # Первая строка – исходная строка S.
    n: int = int(lines[1].strip())  # Вторая строка – количество запросов.
    queries: List[Tuple[int, int, int]] = [
        tuple(map(int, line.split())) for line in lines[2:2 + n]
    ]

    result = apply_queries(s=s, queries=queries)

    with open("txt/output.txt", "w") as f:
        f.write(result)


def apply_queries(s: str, queries: List[Tuple[int, int, int]]) -> str:
    """
    Применяет последовательность запросов к строке, используя структуру Rope.

    Параметры:
      s (str): Исходная строка.
      queries (List[Tuple[int, int, int]]): Список запросов, где каждый запрос задаётся тройкой (i, j, k):
            - i (int): Начальный индекс подстроки (включительно).
            - j (int): Конечный индекс подстроки (включительно).
            - k (int): Позиция вставки (при k = 0 вставка в начало).

    Возвращает:
      str: Итоговая строка после применения всех запросов.
    """
    root = build_rope(s)
    for i, j, k in queries:
        root = rope_cut_and_paste(root, i, j, k)
    return traverse(root)


# Точка входа в программу: запускаем file_io, если скрипт запущен напрямую.
if __name__ == "__main__":
    file_io()
