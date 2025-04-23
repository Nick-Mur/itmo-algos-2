import unittest
from lab4.task8.core.matcher import find_matches

class TestMatcher(unittest.TestCase):

    def test_no_match_k0(self):
        """Тест: Нет совпадений при k=0."""
        self.assertEqual(find_matches(k=0, text="abcde", pattern="xyz"), [])

    def test_exact_match_k0(self):
        """Тест: Точные совпадения при k=0."""
        self.assertEqual(find_matches(k=0, text="abcabcabc", pattern="abc"), [0, 3, 6])
        self.assertEqual(find_matches(k=0, text="aaaaa", pattern="a"), [0, 1, 2, 3, 4])
        self.assertEqual(find_matches(k=0, text="abc", pattern="abc"), [0])

    def test_one_mismatch_found_k1(self):
        """Тест: Одно несовпадение найдено при k=1."""
        self.assertEqual(find_matches(k=1, text="axcde", pattern="abc"), [0]) # aXc vs abc
        self.assertEqual(find_matches(k=1, text="abxde", pattern="abc"), [0]) # abX vs abc
        self.assertEqual(find_matches(k=1, text="abcde", pattern="axc"), [0]) # abc vs aXc
        self.assertEqual(find_matches(k=1, text="abcde", pattern="abx"), [0]) # abc vs abX

    def test_multiple_mismatches_found_k2(self):
        """Тест: Несколько несовпадений найдено при k=2."""
        self.assertEqual(find_matches(k=2, text="axcye", pattern="abcde"), [0]) # aXcYe vs abcde (2 mism)
        # Проверка случая, где было 3 несовпадения (должен вернуть [])
        self.assertEqual(find_matches(k=2, text="abcde", pattern="axyze"), []) # abcde vs aXYZe (3 mism)

    def test_no_match_with_k(self):
        """Тест: Нет совпадений, даже с учетом k."""
        self.assertEqual(find_matches(k=1, text="abcde", pattern="xyz"), [])
        self.assertEqual(find_matches(k=1, text="aaaaa", pattern="bbb"), [])

    def test_exact_match_found_k_large(self):
        """Тест: Точное совпадение найдено при большом k."""
        # При k >= длины паттерна, любая подстрока текста подходит
        self.assertEqual(find_matches(k=5, text="abcabc", pattern="abc"), [0, 1, 2, 3])

    def test_mismatches_at_ends(self):
        """Тест: Несовпадения на краях образца."""
        # i=0: xbc vs abc (1 mism); i=3: abc vs abc (0 mism)
        self.assertEqual(find_matches(k=1, text="xbcabc", pattern="abc"), [0, 3])
        # i=0: abc vs abc (0 mism); i=3: abx vs abc (1 mism)
        self.assertEqual(find_matches(k=1, text="abcabx", pattern="abc"), [0, 3])
        # i=0: xbc vs abc (1 mism); i=3: abx vs abc (1 mism)
        self.assertEqual(find_matches(k=2, text="xbcabx", pattern="abc"), [0, 3])

    def test_k_equals_pattern_length(self):
        """Тест: k равно длине образца (любая подстрока подходит)."""
        text = "abcdefgh"
        pattern = "xyz"
        k = 3
        expected = list(range(len(text) - len(pattern) + 1)) # 0, 1, 2, 3, 4, 5
        self.assertEqual(find_matches(k, text, pattern), expected)

    def test_overlapping_matches(self):
        """Тест: Перекрывающиеся совпадения."""
        # aaaaa vs aba, k=1
        # i=0: aaa vs aba (1 mismatch) -> [0]
        # i=1: aaa vs aba (1 mismatch) -> [0, 1]
        # i=2: aaa vs aba (1 mismatch) -> [0, 1, 2]
        self.assertEqual(find_matches(k=1, text="aaaaa", pattern="aba"), [0, 1, 2])
        # babab vs bab, k=0
        # i=0: bab vs bab (0 mism) -> [0]
        # i=1: aba vs bab (3 mism) -> skip
        # i=2: bab vs bab (0 mism) -> [0, 2]
        self.assertEqual(find_matches(k=0, text="babab", pattern="bab"), [0, 2])
        # babab vs bab, k=1
        # i=0: bab vs bab (0 mism) -> [0]
        # i=1: aba vs bab (3 mism) -> skip
        # i=2: bab vs bab (0 mism) -> [0, 2]
        self.assertEqual(find_matches(k=1, text="babab", pattern="bab"), [0, 2]) # i=1: aba -> bab (3 mism > k=1)

    def test_pattern_longer_than_text(self):
        """Тест: Образец длиннее текста."""
        self.assertEqual(find_matches(k=1, text="abc", pattern="abcde"), [])

    def test_empty_pattern(self):
        """Тест: Пустой образец (по условиям задачи не должно быть, но проверим)."""
        self.assertEqual(find_matches(k=0, text="abcde", pattern=""), [])

    def test_k_negative(self):
        """Тест: Отрицательное k."""
        self.assertEqual(find_matches(k=-1, text="abcde", pattern="abc"), [])

    # --- Тесты из описания задачи ---
    def test_example_1(self):
        # 0 ababab baaa -> 0
        self.assertEqual(find_matches(k=0, text="ababab", pattern="baaa"), [])

    def test_example_2(self):
        # 1 ababab baaa -> 1 1
        # i=0: abab vs baaa (2 mism)
        # i=1: baba vs baaa (1 mism at index 2) -> [1]
        # i=2: abab vs baaa (2 mism)
        self.assertEqual(find_matches(k=1, text="ababab", pattern="baaa"), [1])

    def test_example_3(self):
        # 1 xabcabc ccc -> 0
        self.assertEqual(find_matches(k=1, text="xabcabc", pattern="ccc"), [])

    def test_example_4(self):
        # 2 xabcabc ccc -> 4 1 2 3 4
        # i=0: xab vs ccc (3 mism)
        # i=1: abc vs ccc (2 mism) -> [1]
        # i=2: bca vs ccc (2 mism) -> [1, 2]
        # i=3: cab vs ccc (2 mism) -> [1, 2, 3]
        # i=4: abc vs ccc (2 mism) -> [1, 2, 3, 4]
        self.assertEqual(find_matches(k=2, text="xabcabc", pattern="ccc"), [1, 2, 3, 4])

    def test_example_5(self):
        # 3 aaa xxx -> 1 0
        # i=0: aaa vs xxx (3 mism) -> [0]
        self.assertEqual(find_matches(k=3, text="aaa", pattern="xxx"), [0])

    def test_long_strings_performance(self):
        """Тест: Проверка на относительно длинных строках (не нагрузочный)."""
        text = "a" * 5000 + "b" + "a" * 5000
        pattern = "a" * 100 + "c" + "a" * 100
        text_len = len(text)
        pattern_len = len(pattern)
        k = 1
        # Ожидаем совпадения везде, где несовпадений <= 1
        results = find_matches(k, text, pattern)
        # Индекс, где 'c' наложится на 'b', должен присутствовать, т.к. k=1
        mismatch_center_index = 5000 - 100 # Индекс в text, где 'c' наложится на 'b'
        self.assertIn(mismatch_center_index, results)
        # Позиции i, где 'c' (p[100]) и 'b' (t[5000]) вызывают несовпадения:
        # 'c' вызывает несовпадение для t[i+100] != 'c' (всегда)
        # 'b' вызывает несовпадение для p[5000-i] != 'b' (всегда), если 0 <= 5000-i < pattern_len
        # Два несовпадения происходят, когда i != 4900 и 4800 <= i <= 5000.
        # Таких позиций 200.
        # Общее число позиций: text_len - pattern_len + 1 = 10001 - 201 + 1 = 9801
        # Ожидаемое число совпадений = Общее число позиций - Число позиций с > k несовпадениями
        # Ожидаемое число совпадений = 9801 - 200 = 9601
        expected_matches_count = 9601
        self.assertEqual(len(results), expected_matches_count)


if __name__ == '__main__':
    unittest.main()