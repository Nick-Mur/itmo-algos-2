import unittest
from typing import List, Tuple
from lab2.main import apply_queries


class TestRopeOperations(unittest.TestCase):
    def test_example1(self) -> None:
        """
        Идеальный случай.
        Проверяет пример из ТЗ:
          Исходная строка: "hlelowrold"
          Запросы: (1, 1, 2) и (6, 6, 7)
          Ожидаемый результат: "helloworld"
        """
        s = "hlelowrold"
        queries: List[Tuple[int, int, int]] = [(1, 1, 2), (6, 6, 7)]
        expected = "helloworld"
        result = apply_queries(s, queries)
        self.assertEqual(result, expected)

    def test_example2(self) -> None:
        """
        Идеальный случай.
        Проверяет второй пример из ТЗ:
          Исходная строка: "abcdef"
          Запросы: (0, 1, 1) и (4, 5, 0)
          Ожидаемый результат: "efcabd"
        """
        s = "abcdef"
        queries: List[Tuple[int, int, int]] = [(0, 1, 1), (4, 5, 0)]
        expected = "efcabd"
        result = apply_queries(s, queries)
        self.assertEqual(result, expected)

    def test_no_change(self) -> None:
        """
        Обычный случай.
        Запрос не изменяет строку.
          Исходная строка: "algorithm"
          Запрос: вырезать подстроку "rith" (индексы 4-7) и вставить её сразу же обратно (k=4).
          Ожидаемый результат: "algorithm"
        """
        s = "algorithm"
        queries: List[Tuple[int, int, int]] = [(4, 7, 4)]
        expected = "algorithm"
        result = apply_queries(s, queries)
        self.assertEqual(result, expected)

    def test_single_character(self) -> None:
        """
        Крайний случай.
        Строка состоит из одного символа.
          Исходная строка: "a"
          Запрос: (0, 0, 0) — вырезание и вставка единственного символа.
          Ожидаемый результат: "a"
        """
        s = "a"
        queries: List[Tuple[int, int, int]] = [(0, 0, 0)]
        expected = "a"
        result = apply_queries(s, queries)
        self.assertEqual(result, expected)

    def test_invalid_query_i_greater_j(self) -> None:
        """
        Ошибочная ситуация.
        Передаётся запрос, где i > j, что является некорректным.
          Ожидается, что функция вызовет исключение.
        """
        s = "example"
        queries: List[Tuple[int, int, int]] = [(3, 2, 1)]
        with self.assertRaises(Exception):
            apply_queries(s, queries)

    def test_invalid_query_negative_index(self) -> None:
        """
        Ошибочная ситуация.
        Передаются отрицательные индексы.
          Ожидается, что функция вызовет исключение.
        """
        s = "test"
        queries: List[Tuple[int, int, int]] = [(-1, 2, 1)]
        with self.assertRaises(Exception):
            apply_queries(s, queries)

    def test_invalid_query_k_out_of_range(self) -> None:
        """
        Ошибочная ситуация.
        Передаётся значение k, выходящее за допустимый диапазон.
          Например, если после вырезания подстроки длина строки уменьшается,
          k должен находиться в пределах новой длины строки.
          Здесь k задано слишком большим.
          Ожидается, что функция вызовет исключение.
        """
        s = "rope"
        # Если вырезается подстрока [1,2] из "rope" (длина 4), остаётся 2 символа.
        # Допустимые значения k: 0 или 1.
        # Здесь используется k = 3.
        queries: List[Tuple[int, int, int]] = [(1, 2, 3)]
        with self.assertRaises(Exception):
            apply_queries(s, queries)


if __name__ == '__main__':
    unittest.main()
