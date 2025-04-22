import unittest
from typing import List, Tuple

# Импортируем тестируемые функции и константы из основного файла main.py
from main import (
    _get_substring_hash,
    _precompute_hashes,
    _compare_substrings,
    solve_approximate_matching,
    HASHING_PARAMETERS,
    NUM_HASH_FUNCTIONS
)

class TestApproximateMatching(unittest.TestCase):

    # Тесты для вспомогательных функций можно добавить по аналогии с предыдущей задачей,
    # если есть необходимость в их детальной проверке.
    # Здесь сосредоточимся на основной функции solve_approximate_matching.

    def test_solve_examples(self):
        """Тестирование на примерах из условия задачи."""
        self.assertEqual(solve_approximate_matching(0, "ababab", "baaa"), [])
        self.assertEqual(solve_approximate_matching(1, "ababab", "baaa"), [1])
        self.assertEqual(solve_approximate_matching(1, "xabcabc", "ccc"), [])
        self.assertEqual(solve_approximate_matching(2, "xabcabc", "ccc"), [1, 2, 3, 4])
        self.assertEqual(solve_approximate_matching(3, "aaa", "xxx"), [0])

    def test_solve_exact_match(self):
        """Тестирование с k=0 (точный поиск)."""
        self.assertEqual(solve_approximate_matching(0, "banana", "ana"), [1, 3])
        self.assertEqual(solve_approximate_matching(0, "aaaaa", "aa"), [0, 1, 2, 3])
        self.assertEqual(solve_approximate_matching(0, "abcde", "xyz"), [])
        self.assertEqual(solve_approximate_matching(0, "test", "test"), [0])

    def test_solve_no_match(self):
        """Тестирование случаев, когда совпадений нет."""
        self.assertEqual(solve_approximate_matching(1, "abcde", "xyz"), [])
        self.assertEqual(solve_approximate_matching(0, "aaaaa", "b"), [])
        # k=1, но нужно 2 несовпадения
        self.assertEqual(solve_approximate_matching(1, "abcdef", "axcdey"), [])

    def test_solve_full_match_with_k(self):
        """Тестирование случаев, когда k достаточно велико."""
        # k=1, одно несовпадение
        self.assertEqual(solve_approximate_matching(1, "banana", "banaXa"), [0])
        # k=2, два несовпадения
        self.assertEqual(solve_approximate_matching(2, "banana", "baXana"), [0])
        # k=6 (больше чем k_max=5, но для теста), вся строка может не совпадать
        self.assertEqual(solve_approximate_matching(6, "banana", "uvwxyz"), [0])
        # k=3, но строка совпадает
        self.assertEqual(solve_approximate_matching(3, "test", "test"), [0])

    def test_solve_edges(self):
        """Тестирование граничных случаев."""
        # Образец длиннее текста
        self.assertEqual(solve_approximate_matching(1, "abc", "abcd"), [])
        # Образец равен тексту
        self.assertEqual(solve_approximate_matching(0, "abc", "abc"), [0])
        self.assertEqual(solve_approximate_matching(1, "abc", "axc"), [0])
        # Образец длины 1
        self.assertEqual(solve_approximate_matching(0, "banana", "a"), [1, 3, 5])
        self.assertEqual(solve_approximate_matching(0, "banana", "b"), [0])
        self.assertEqual(solve_approximate_matching(0, "banana", "x"), [])
        # k=0, образец длины 1
        self.assertEqual(solve_approximate_matching(0, "aaaaa", "a"), [0, 1, 2, 3, 4])
        # Пустой текст (невозможен по условию, но проверим)
        self.assertEqual(solve_approximate_matching(1, "", "a"), [])
        # Пустой образец (невозможен по условию, но проверим)
        # self.assertEqual(solve_approximate_matching(1, "abc", ""), []) # Функция вернет ошибку или пустой список

    def test_solve_overlapping(self):
        """Тестирование с перекрывающимися результатами."""
        self.assertEqual(solve_approximate_matching(1, "aaaaa", "aa"), [0, 1, 2, 3])
        self.assertEqual(solve_approximate_matching(1, "ababab", "aba"), [0, 2]) # Точные совпадения
        self.assertEqual(solve_approximate_matching(1, "ababab", "aca"), [0, 2]) # k=1 на позициях 0 и 2
        self.assertEqual(solve_approximate_matching(1, "abcabcabc", "axc"), [0, 3, 6])

    def test_solve_large_k(self):
        """Тестирование с максимально допустимым k."""
        self.assertEqual(solve_approximate_matching(5, "abcdefgh", "axcyefgz"), [0])
        # Почти все позиции должны подойти, если k=5 и len(p)=6
        text = "abcdefghijklmnopqrstuvwxyz"
        pattern = "mnopqr"
        # ИСПРАВЛЕНО: Ожидаем только [12], так как только там 0 несовпадений.
        # В остальных позициях будет 6 несовпадений.
        expected = [12]
        self.assertEqual(solve_approximate_matching(5, text, pattern), expected)

    def test_binary_search_logic_edge_case(self):
        """Тест для проверки логики бинарного поиска при несовпадении с 0 индекса."""
        # Используем t="abanana", p="banana".
        # При i=0, t[0:6]="abanan" vs p="banana" -> 6 несовпадений.
        # При i=1, t[1:7]="banana" vs p="banana" -> 0 несовпадений.
        # ИСПРАВЛЕНО: Ожидаем [1], так как только i=1 подходит при k=5
        self.assertEqual(solve_approximate_matching(5, "abanana", "banana"), [1])
        # ИСПРАВЛЕНО: Ожидаем [0, 1], так как оба индекса подходят при k=6
        self.assertEqual(solve_approximate_matching(6, "abanana", "banana"), [0, 1])


if __name__ == "__main__":
    unittest.main()