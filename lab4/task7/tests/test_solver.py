import unittest
import sys
import os
from lab4.task7.solver import find_longest_common_substring


class TestLongestCommonSubstring(unittest.TestCase):

    def assertLCSEquals(self, s, t, expected_l, expected_i=None, expected_j=None):
        """
        Вспомогательный метод для проверки результата.
        Проверяет длину LCS и, если возможно, сами подстроки по индексам.
        """
        i, j, l = find_longest_common_substring(s, t)

        # 1. Проверяем длину
        self.assertEqual(l, expected_l,
                         f"Failed for s='{s}', t='{t}'. Expected length {expected_l}, got {l}.")

        # 2. Если ожидаемая длина > 0, проверяем, что найденная подстрока действительно общая
        if expected_l > 0:
            substring_s = s[i: i + l]
            substring_t = t[j: j + l]
            self.assertEqual(substring_s, substring_t,
                             f"Failed for s='{s}', t='{t}'. Substrings s[{i}:{i + l}]='{substring_s}' and t[{j}:{j + l}]='{substring_t}' do not match for length {l}.")

            # Дополнительная проверка: убедимся, что найденная подстрока есть в обеих исходных строках
            self.assertIn(substring_s, s, f"Substring '{substring_s}' not found in s='{s}'")
            self.assertIn(substring_t, t, f"Substring '{substring_t}' not found in t='{t}'")

        # 3. Если заданы ожидаемые индексы, проверяем их (не всегда возможно из-за множественности ответов)
        # Эту проверку можно ослабить или убрать, если точные индексы не важны, а важна только длина
        # В данной задаче требуется вывести *любую* тройку, поэтому проверка индексов может быть излишней,
        # если мы доверяем проверке длины и совпадению подстрок.
        # Оставим для примера, но с оговоркой.
        if expected_i is not None and expected_j is not None:
            # Проверяем, что найденная пара (i, j) дает подстроку нужной длины
            # Это косвенно проверяется в п.2, но можно явно
            self.assertEqual(s[i:i + l], t[j:j + l])
            # Можно было бы проверить s[expected_i:expected_i+l] == t[expected_j:expected_j+l]
            # но наша функция может вернуть другую валидную пару индексов.

    def test_example_cases(self):
        """Тестирование примеров из условия задачи."""
        # Пример 1: cool toolbox -> ool (длина 3, индексы 1, 1)
        self.assertLCSEquals("cool", "toolbox", 3, 1, 1)

        # Пример 2: aaa bb -> "" (длина 0)
        self.assertLCSEquals("aaa", "bb", 0)

        # Пример 3: aabaa babbaab -> aab (длина 3, индексы 0, 4 или 2, 3)
        # Наша функция может вернуть любую из валидных троек. Проверяем только длину и совпадение подстрок.
        self.assertLCSEquals("aabaa", "babbaab", 3)

    def test_edge_cases(self):
        """Тестирование граничных случаев."""
        # Пустые строки
        self.assertLCSEquals("", "", 0)
        self.assertLCSEquals("abc", "", 0)
        self.assertLCSEquals("", "abc", 0)

        # Идентичные строки
        self.assertLCSEquals("abcde", "abcde", 5, 0, 0)
        self.assertLCSEquals("aaaaa", "aaaaa", 5, 0, 0)

        # Одна строка является подстрокой другой
        self.assertLCSEquals("apple", "pineapple", 5)  # apple в pineapple
        self.assertLCSEquals("test", "thisisatestcase", 4)  # test в thisisatestcase
        self.assertLCSEquals("sub", "substring", 3)  # sub в substring

        # Нет общих подстрок (кроме пустой)
        self.assertLCSEquals("abcdef", "ghijkl", 0)
        self.assertLCSEquals("xyz", "abc", 0)

    def test_multiple_matches(self):
        """Тестирование случаев с несколькими LCS одинаковой максимальной длины."""
        # "banana", "atana" -> "ana" (длина 3)
        # Возможные варианты: (1, 1, 3) или (3, 1, 3)
        self.assertLCSEquals("banana", "atana", 3)

        # "abcabc", "xyzabc" -> "abc" (длина 3)
        # Возможные варианты: (0, 3, 3) или (3, 3, 3)
        self.assertLCSEquals("abcabc", "xyzabc", 3)

    def test_long_strings(self):
        """Тестирование на относительно длинных строках."""
        s = "a" * 500 + "b" * 500
        t = "c" * 500 + "a" * 500
        # LCS: "a" * 500
        self.assertLCSEquals(s, t, 500)

        s = "x" * 1000
        t = "y" * 500 + "x" * 500
        # LCS: "x" * 500
        self.assertLCSEquals(s, t, 500)


if __name__ == '__main__':
    unittest.main()
