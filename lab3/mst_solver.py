# -*- coding: utf-8 -*-
"""
mst_solver.py

Задача: Построение минимального остовного дерева (MST) для заданных точек на плоскости.
Алгоритм Краскала с использованием DSU.
Чтение из input.txt, запись в output.txt.
"""

import math
from typing import List, Tuple
from utils import time_memory_decorator

# Определяем тип для координат точки
Point = Tuple[int, int]
# Определяем тип для списка точек
PointList = List[Point]
# Определяем тип для ребра (вес, индекс вершины 1, индекс вершины 2)
Edge = Tuple[float, int, int]
# Определяем тип для списка ребер
EdgeList = List[Edge]


# --- Вспомогательные функции ---

def calculate_distance(point1: Point, point2: Point) -> float:
    """
    Вычисляет евклидово расстояние между двумя точками.

    Args:
        point1: Кортеж (x, y) первой точки.
        point2: Кортеж (x, y) второй точки.

    Returns:
        Расстояние между точками (float).
    """
    # Разница координат по осям
    delta_x: int = point1[0] - point2[0]
    delta_y: int = point1[1] - point2[1]
    # Формула евклидова расстояния: sqrt(dx^2 + dy^2)
    # Используем math.pow для единообразия, хотя ** 2 тоже работает
    return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


# --- Основная функция для вычисления MST ---
@time_memory_decorator
def calculate_mst_length(points_coords: PointList) -> float:
    """
    Вычисляет длину минимального остовного дерева (MST) для заданного списка точек
    с использованием алгоритма Краскала и DSU.

    Args:
        points_coords: Список кортежей с координатами точек [(x1, y1), ...].

    Returns:
        Минимальная суммарная длина ребер MST (float).
        Возвращает 0.0, если точек 0 или 1.
    """
    n_points: int = len(points_coords)
    # Если точек мало (0 или 1), то длина MST равна 0
    if n_points <= 1:
        return 0.0

    # --- Инициализация DSU (Система Непересекающихся Множеств) ---
    # parent_nodes[i] хранит родителя i-го элемента (или сам элемент, если он корень)
    parent_nodes: List[int] = list(range(n_points))
    # node_ranks[i] хранит ранг дерева с корнем i (для оптимизации объединения)
    node_ranks: List[int] = [0] * n_points

    # --- Вспомогательные функции DSU (вложенные) ---
    def find_set_representative(node_index: int) -> int:
        """Находит представителя множества для node_index (со сжатием пути)."""
        # Если узел - корень своего дерева
        if node_index == parent_nodes[node_index]:
            return node_index
        # Рекурсивно ищем корень и переподвешиваем узел сразу к корню (сжатие пути)
        parent_nodes[node_index] = find_set_representative(parent_nodes[node_index])
        return parent_nodes[node_index]

    def unite_sets(node_a_index: int, node_b_index: int) -> bool:
        """Объединяет множества узлов node_a_index и node_b_index (по рангу)."""
        # Находим корни деревьев для обоих узлов
        root_a: int = find_set_representative(node_a_index)
        root_b: int = find_set_representative(node_b_index)

        # Если корни разные, множества можно объединить
        if root_a != root_b:
            # Объединение по рангу: дерево меньшего ранга присоединяется к дереву большего ранга
            if node_ranks[root_a] < node_ranks[root_b]:
                # Меняем корни местами, чтобы root_a всегда был корнем с большим/равным рангом
                root_a, root_b = root_b, root_a
            # Присоединяем дерево B к дереву A
            parent_nodes[root_b] = root_a
            # Если ранги были одинаковы, ранг нового корня (root_a) увеличивается
            if node_ranks[root_a] == node_ranks[root_b]:
                node_ranks[root_a] += 1
            return True  # Объединение произошло
        return False  # Узлы уже были в одном множестве

    # --- Генерация всех возможных ребер ---
    all_edges: EdgeList = []
    # Перебираем все уникальные пары точек (i, j), где i < j
    for i in range(n_points):
        for j in range(i + 1, n_points):
            # Вычисляем вес ребра (расстояние)
            weight: float = calculate_distance(points_coords[i], points_coords[j])
            # Добавляем ребро в список в формате (вес, вершина1, вершина2)
            all_edges.append((weight, i, j))

    # --- Сортировка ребер по весу (по возрастанию) ---
    # Это ключевой шаг для жадного алгоритма Краскала
    all_edges.sort()

    # --- Построение MST с помощью алгоритма Краскала ---
    minimum_total_length: float = 0.0
    edges_in_mst: int = 0  # Счетчик ребер, добавленных в MST

    # Идем по ребрам от самых легких к самым тяжелым
    for edge_weight, u_node, v_node in all_edges:
        # Пытаемся объединить множества, к которым принадлежат вершины ребра
        # unite_sets вернет True, если вершины были в разных множествах (т.е. ребро не создает цикл)
        if unite_sets(u_node, v_node):
            # Добавляем вес ребра к общей длине MST
            minimum_total_length += edge_weight
            # Увеличиваем счетчик добавленных ребер
            edges_in_mst += 1
            # Оптимизация: MST для N вершин всегда содержит N-1 ребро.
            # Если мы уже добавили N-1 ребро, можно заканчивать.
            if edges_in_mst == n_points - 1:
                break

    return minimum_total_length


# --- Точка входа при запуске скрипта ---
if __name__ == "__main__":
    # Используем 'with' для автоматического и безопасного закрытия файлов
    try:
        # Чтение данных из файла input.txt
        input_filename: str = 'input.txt'
        points_input: PointList = []
        with open(input_filename, 'r', encoding='utf-8') as infile:
            # Читаем количество точек
            n_points_input: int = int(infile.readline())
            # Читаем координаты каждой точки
            for i in range(n_points_input):
                line: str = infile.readline()
                # Проверка на случай, если файл закончился раньше ожидаемого
                if not line:
                    # Генерируем ошибку, если строка пустая (неожиданный конец файла)
                    raise ValueError(f"Неожиданный конец файла при чтении точки {i+1}")
                # Разбираем строку на координаты x и y
                x_str, y_str = line.split()
                x: int = int(x_str)
                y: int = int(y_str)
                points_input.append((x, y))

        # Вычисление длины MST
        result_length: float = calculate_mst_length(points_input)

        # Запись результата в файл output.txt
        output_filename: str = 'output.txt'
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            # Форматируем вывод до 9 знаков после запятой для удовлетворения требования точности
            outfile.write(f"{result_length:.9f}")

    except FileNotFoundError:
        # Обработка случая, когда входной файл не найден
        print(f"Ошибка: Файл '{input_filename}' не найден.")
    except ValueError as ve:
        # Обработка ошибок преобразования типов (int, float) или структуры файла
        print(f"Ошибка в формате данных: {ve}")
    except Exception as e:
        # Обработка любых других непредвиденных ошибок
        # Выводим сообщение об ошибке, чтобы пользователь знал, что что-то пошло не так
        print(f"Произошла непредвиденная ошибка: {e}")
