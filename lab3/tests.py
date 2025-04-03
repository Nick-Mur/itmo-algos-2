# -*- coding: utf-8 -*-
"""
tests.py

Модульные тесты для mst_solver.py.
Тестируем функцию calculate_distance и основную логику calculate_mst_length.
"""

import unittest
import math
# Импортируем функции из нашего основного файла
from mst_solver import calculate_distance, calculate_mst_length


class TestMSTCalculation(unittest.TestCase):
    """Набор тестов для вычисления MST."""

    # --- Тесты для вспомогательной функции calculate_distance ---

    def test_distance_simple(self):
        """Тест: Простое расстояние (Пифагорова тройка)."""
        p1 = (0, 0)
        p2 = (3, 4)
        # Ожидаемое расстояние = sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5.0
        self.assertAlmostEqual(calculate_distance(p1, p2), 5.0, places=9)

    def test_distance_same_point(self):
        """Тест: Расстояние до той же точки."""
        p1 = (10, -5)
        p2 = (10, -5)
        # Ожидаемое расстояние = 0.0
        self.assertAlmostEqual(calculate_distance(p1, p2), 0.0, places=9)

    def test_distance_horizontal(self):
        """Тест: Расстояние по горизонтали."""
        p1 = (2, 5)
        p2 = (7, 5)
        # Ожидаемое расстояние = |7 - 2| = 5.0
        self.assertAlmostEqual(calculate_distance(p1, p2), 5.0, places=9)

    def test_distance_vertical(self):
        """Тест: Расстояние по вертикали."""
        p1 = (3, 1)
        p2 = (3, -4)
        # Ожидаемое расстояние = |1 - (-4)| = 5.0
        self.assertAlmostEqual(calculate_distance(p1, p2), 5.0, places=9)

    def test_distance_negative_coords(self):
        """Тест: Расстояние с отрицательными координатами."""
        p1 = (-1, -2)
        p2 = (-4, -6)
        # Ожидаемое расстояние = sqrt((-1 - (-4))^2 + (-2 - (-6))^2)
        # = sqrt(3^2 + 4^2) = sqrt(9 + 16) = 5.0
        self.assertAlmostEqual(calculate_distance(p1, p2), 5.0, places=9)

    # --- Тесты для основной функции calculate_mst_length ---

    def test_mst_example1(self):
        """Тест: Пример 1 из условия (квадрат)."""
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
        # Ожидаемая длина = 1.0 + 1.0 + 1.0 = 3.0
        expected_length = 3.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=7)

    def test_mst_example2(self):
        """Тест: Пример 2 из условия."""
        points = [(0, 0), (0, 2), (1, 1), (3, 0), (3, 2)]
        # Ожидаемая длина = 2 * sqrt(2) + sqrt(5) + 2
        expected_length = 2 * math.sqrt(2) + math.sqrt(5) + 2.0
        # Примерное значение: 2 * 1.41421356 + 2.23606798 + 2 = 2.82842712 + 2.23606798 + 2 = 7.06449510
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=7)  # Проверяем с точностью 7 знаков

    def test_mst_single_point(self):
        """Тест: Критический случай - одна точка."""
        points = [(10, 20)]
        # Ожидаемая длина = 0.0
        expected_length = 0.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=9)

    def test_mst_two_points(self):
        """Тест: Критический случай - две точки."""
        points = [(0, 0), (5, 12)]
        # Ожидаемая длина = sqrt(5^2 + 12^2) = sqrt(25 + 144) = sqrt(169) = 13.0
        expected_length = 13.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=9)

    def test_mst_collinear_points(self):
        """Тест: Три точки на одной линии."""
        points = [(0, 0), (2, 0), (5, 0)]
        # Ожидаемая длина = расстояние(0,0 до 2,0) + расстояние(2,0 до 5,0) = 2.0 + 3.0 = 5.0
        expected_length = 5.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=9)

    def test_mst_collinear_diagonal(self):
        """Тест: Три точки на диагонали."""
        points = [(0, 0), (1, 1), (3, 3)]
        # Ожидаемая длина = расстояние(0,0 до 1,1) + расстояние(1,1 до 3,3)
        # = sqrt(1^2+1^2) + sqrt(2^2+2^2) = sqrt(2) + sqrt(8) = sqrt(2) + 2*sqrt(2) = 3*sqrt(2)
        expected_length = 3 * math.sqrt(2)
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=7)

    def test_mst_empty_input(self):
        """Тест: Критический случай - пустой список точек."""
        points = []
        # Ожидаемая длина = 0.0
        expected_length = 0.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=9)

    def test_mst_triangle(self):
        """Тест: Простой треугольник."""
        points = [(0, 0), (3, 0), (0, 4)]
        # Стороны: 3, 4, 5. MST будет из ребер 3 и 4.
        # Ожидаемая длина = 3.0 + 4.0 = 7.0
        expected_length = 7.0
        self.assertAlmostEqual(calculate_mst_length(points), expected_length, places=9)


# --- Запуск тестов ---
if __name__ == '__main__':
    # Запускаем все тесты в этом модуле
    unittest.main()
