import unittest
from lab4.task8.core.hashing import Hasher

# Используем стандартные параметры для тестов
BASE1 = 31
MOD1 = 10**9 + 7
BASE2 = 37
MOD2 = 10**9 + 9

class TestHasher(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.sample_text = "ababababa"
        self.hasher_instance = Hasher(self.sample_text, BASE1, MOD1, BASE2, MOD2)
        self.n = len(self.sample_text)

    def test_init(self):
        """Тест инициализации Hasher."""
        self.assertEqual(self.hasher_instance.n, self.n)
        self.assertEqual(len(self.hasher_instance.powers1), self.n + 1)
        self.assertEqual(len(self.hasher_instance.powers2), self.n + 1)
        self.assertEqual(len(self.hasher_instance.prefix_hashes1), self.n + 1)
        self.assertEqual(len(self.hasher_instance.prefix_hashes2), self.n + 1)
        self.assertEqual(self.hasher_instance.powers1[0], 1)
        self.assertEqual(self.hasher_instance.powers2[0], 1)
        self.assertEqual(self.hasher_instance.prefix_hashes1[0], 0)
        self.assertEqual(self.hasher_instance.prefix_hashes2[0], 0)

    def test_get_hash_entire_string(self):
        """Тест получения хеша всей строки."""
        full_hash = self.hasher_instance.get_hash(0, self.n)
        # Хеш всей строки должен совпадать с последним префиксным хешем
        self.assertEqual(full_hash, (self.hasher_instance.prefix_hashes1[self.n], self.hasher_instance.prefix_hashes2[self.n]))
        self.assertIsInstance(full_hash, tuple)
        self.assertEqual(len(full_hash), 2)
        self.assertIsInstance(full_hash[0], int)
        self.assertIsInstance(full_hash[1], int)

    def test_get_hash_substrings(self):
        """Тест получения хешей различных подстрок."""
        # "ab" в начале
        hash_ab1 = self.hasher_instance.get_hash(0, 2)
        # "ab" в середине
        hash_ab2 = self.hasher_instance.get_hash(2, 2)
        # "ab" в конце
        hash_ab3 = self.hasher_instance.get_hash(6, 2)

        # "ba" в начале
        hash_ba1 = self.hasher_instance.get_hash(1, 2)
        # "ba" в середине
        hash_ba2 = self.hasher_instance.get_hash(3, 2)
        # "ba" в конце
        hash_ba3 = self.hasher_instance.get_hash(7, 2)

        # Одинаковые подстроки должны иметь одинаковые хеши
        self.assertEqual(hash_ab1, hash_ab2)
        self.assertEqual(hash_ab2, hash_ab3)
        self.assertEqual(hash_ba1, hash_ba2)
        self.assertEqual(hash_ba2, hash_ba3)

        # Разные подстроки должны иметь разные хеши (с высокой вероятностью)
        self.assertNotEqual(hash_ab1, hash_ba1)

        # Тест подстроки из одного символа
        hash_a = self.hasher_instance.get_hash(0, 1)
        hash_b = self.hasher_instance.get_hash(1, 1)
        self.assertNotEqual(hash_a, hash_b)

        # Тест подстроки "bab"
        hash_bab = self.hasher_instance.get_hash(1, 3)
        self.assertIsInstance(hash_bab, tuple)

    def test_get_hash_empty_substring(self):
        """Тест получения хеша пустой подстроки."""
        self.assertEqual(self.hasher_instance.get_hash(0, 0), (0, 0))
        self.assertEqual(self.hasher_instance.get_hash(5, 0), (0, 0))

    def test_compare_substrings_internal(self):
        """Тест сравнения подстрок внутри одной строки."""
        # Сравнение одинаковых подстрок "aba"
        self.assertTrue(self.hasher_instance.compare_substrings(0, 2, 3))
        self.assertTrue(self.hasher_instance.compare_substrings(2, 4, 3))

        # Сравнение разных подстрок "aba" и "bab"
        self.assertFalse(self.hasher_instance.compare_substrings(0, 1, 3))

        # Сравнение подстрок разной длины не предусмотрено, но проверим длину 1
        self.assertTrue(self.hasher_instance.compare_substrings(0, 2, 1)) # 'a' == 'a'
        self.assertFalse(self.hasher_instance.compare_substrings(0, 1, 1)) # 'a' != 'b'

        # Сравнение с нулевой длиной
        self.assertTrue(self.hasher_instance.compare_substrings(0, 5, 0))

    def test_get_hash_out_of_bounds(self):
        """Тест выхода за границы при запросе хеша."""
        with self.assertRaises(IndexError):
            self.hasher_instance.get_hash(-1, 2) # Отрицательный старт
        with self.assertRaises(IndexError):
            self.hasher_instance.get_hash(0, self.n + 1) # Длина больше строки
        with self.assertRaises(IndexError):
            self.hasher_instance.get_hash(self.n, 1) # Старт на последнем символе, длина 1 (выход за границу)
        with self.assertRaises(IndexError):
            self.hasher_instance.get_hash(self.n - 1, 2) # Старт на предпоследнем, длина 2 (выход за границу)

        # Корректный случай на границе
        self.assertIsNotNone(self.hasher_instance.get_hash(self.n - 1, 1)) # Последний символ
        self.assertIsNotNone(self.hasher_instance.get_hash(0, self.n)) # Вся строка

    def test_different_bases_mods(self):
        """Тест работы с другими основаниями и модулями."""
        text = "abcabc"
        base1, mod1 = 257, 10**9 + 7  # Простое основание > 256
        base2, mod2 = 263, 10**9 + 9  # Другое простое основание
        hasher = Hasher(text, base1, mod1, base2, mod2)

        hash_abc1 = hasher.get_hash(0, 3)
        hash_abc2 = hasher.get_hash(3, 3)
        hash_bca = hasher.get_hash(1, 3)

        self.assertEqual(hash_abc1, hash_abc2)
        self.assertNotEqual(hash_abc1, hash_bca)

    def test_long_string(self):
        """Тест на длинной строке для проверки производительности и отсутствия переполнений."""
        text = "a" * 10000 + "b" * 10000
        hasher = Hasher(text, BASE1, MOD1, BASE2, MOD2)

        hash_a_block = hasher.get_hash(0, 10000)
        hash_b_block = hasher.get_hash(10000, 10000)
        hash_mixed = hasher.get_hash(9995, 10) # 5 'a' и 5 'b'

        self.assertIsInstance(hash_a_block, tuple)
        self.assertIsInstance(hash_b_block, tuple)
        self.assertIsInstance(hash_mixed, tuple)
        self.assertNotEqual(hash_a_block, hash_b_block)
        self.assertNotEqual(hash_a_block, hash_mixed)
        self.assertNotEqual(hash_b_block, hash_mixed)

        # Проверка равенства одинаковых подстрок на длинной строке
        hash_a_part1 = hasher.get_hash(100, 50)
        hash_a_part2 = hasher.get_hash(5000, 50)
        self.assertEqual(hash_a_part1, hash_a_part2)

        hash_b_part1 = hasher.get_hash(10100, 50)
        hash_b_part2 = hasher.get_hash(15000, 50)
        self.assertEqual(hash_b_part1, hash_b_part2)

if __name__ == '__main__':
    unittest.main()