import unittest

# Импортируем тестируемые функции и константы из основного файла
from lab4.task7.main import (
    get_substring_hash,
    check_substring_existence,
    find_longest_common_substring,
    HASHING_PARAMETERS
)

class TestLongestCommonSubstring(unittest.TestCase):

    def setUp(self):
        """Вспомогательная функция для предвычисления хешей и степеней для get_substring_hash."""
        self.test_string = "banana"
        self.s_len = len(self.test_string)
        self.base_powers_all = []
        self.prefix_hashes_all = []

        for base, modulus in HASHING_PARAMETERS:
            powers = [1] * (self.s_len + 1)
            for i in range(1, self.s_len + 1):
                powers[i] = (powers[i - 1] * base) % modulus
            self.base_powers_all.append(powers)

            prefix_hashes = [0] * (self.s_len + 1)
            for i in range(self.s_len):
                prefix_hashes[i + 1] = (prefix_hashes[i] * base + ord(self.test_string[i])) % modulus
            self.prefix_hashes_all.append(prefix_hashes)

    def test_get_substring_hash(self):
        """Тестирование вычисления хеша подстроки."""
        # Используем только первый набор параметров для простоты проверки
        prefix_hashes = self.prefix_hashes_all[0]
        base_powers = self.base_powers_all[0]
        base, modulus = HASHING_PARAMETERS[0]

        # Классический случай: "ana" с индекса 1
        expected_hash_ana = (ord('a') * base**2 + ord('n') * base**1 + ord('a') * base**0) % modulus
        self.assertEqual(get_substring_hash(prefix_hashes, base_powers, 1, 3, modulus), expected_hash_ana)

        # Крайний случай: длина 0
        self.assertEqual(get_substring_hash(prefix_hashes, base_powers, 2, 0, modulus), 0)

        # Крайний случай: длина 1 ("n" с индекса 2)
        expected_hash_n = ord('n') % modulus
        self.assertEqual(get_substring_hash(prefix_hashes, base_powers, 2, 1, modulus), expected_hash_n)

        # Крайний случай: вся строка "banana"
        expected_hash_banana = prefix_hashes[6] # h[6] - h[0]*p[6] = h[6]
        self.assertEqual(get_substring_hash(prefix_hashes, base_powers, 0, 6, modulus), expected_hash_banana)

        # Крайний случай: последний символ "a"
        expected_hash_last_a = ord('a') % modulus
        self.assertEqual(get_substring_hash(prefix_hashes, base_powers, 5, 1, modulus), expected_hash_last_a)

    def test_check_substring_existence(self):
        """Тестирование функции проверки существования общей подстроки."""
        s = "banana"
        t = "atana"
        s_len = len(s)
        t_len = len(t)
        max_len = min(s_len, t_len)

        # Предвычисление для s и t
        base_powers_all = []
        s_prefix_hashes_all = []
        t_prefix_hashes_all = []
        for base, modulus in HASHING_PARAMETERS:
            powers = [1] * (max_len + 1)
            for i in range(1, max_len + 1): powers[i] = (powers[i - 1] * base) % modulus
            base_powers_all.append(powers)

            prefix_hashes_s = [0] * (s_len + 1)
            for i in range(s_len): prefix_hashes_s[i + 1] = (prefix_hashes_s[i] * base + ord(s[i])) % modulus
            s_prefix_hashes_all.append(prefix_hashes_s)

            prefix_hashes_t = [0] * (t_len + 1)
            for i in range(t_len): prefix_hashes_t[i + 1] = (prefix_hashes_t[i] * base + ord(t[i])) % modulus
            t_prefix_hashes_all.append(prefix_hashes_t)

        # Классический случай: k=3 ("ana")
        exists, i, j = check_substring_existence(3, s_len, t_len, s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all)
        self.assertTrue(exists)
        self.assertEqual(s[i:i+3], "ana") # Проверяем, что найденная подстрока действительно "ana"
        self.assertEqual(t[j:j+3], "ana")
        # Возможные i,j: (1,2) или (3,2) - код вернет (1,2) т.к. i=1 первый в s
        self.assertEqual(i, 1)
        # ИСПРАВЛЕНО: Ожидаем j=2, так как "ana" в "atana" начинается с индекса 2
        self.assertEqual(j, 2)


        # Классический случай: k=1 ("a")
        exists, i, j = check_substring_existence(1, s_len, t_len, s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all)
        self.assertTrue(exists)
        self.assertEqual(s[i:i+1], "a")
        self.assertEqual(t[j:j+1], "a")
        # Возможные i,j: (1,0), (3,2), (5,4) - код вернет (1,0)
        self.assertEqual(i, 1)
        self.assertEqual(j, 0)

        # Случай, когда подстроки нет: k=4 ("nana" vs "tana")
        exists, _, _ = check_substring_existence(4, s_len, t_len, s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all)
        self.assertFalse(exists)

        # Крайний случай: k=0
        exists, i, j = check_substring_existence(0, s_len, t_len, s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all)
        self.assertTrue(exists)
        self.assertEqual(i, 0)
        self.assertEqual(j, 0)

        # Крайний случай: k > min(s_len, t_len)
        exists, _, _ = check_substring_existence(6, s_len, t_len, s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all)
        self.assertFalse(exists)

        # Крайний случай: пустая строка t
        exists, _, _ = check_substring_existence(1, s_len, 0, s_prefix_hashes_all, [[] for _ in HASHING_PARAMETERS], base_powers_all)
        self.assertFalse(exists)

        # Крайний случай: пустая строка s
        exists, _, _ = check_substring_existence(1, 0, t_len, [[] for _ in HASHING_PARAMETERS], t_prefix_hashes_all, base_powers_all)
        self.assertFalse(exists)


    def test_find_longest_common_substring(self):
        """Тестирование основной функции поиска."""

        # Примеры из условия
        self.assertEqual(find_longest_common_substring("cool", "toolbox"), (1, 1, 3)) # "ool"
        self.assertEqual(find_longest_common_substring("aaa", "bb"), (0, 0, 0)) # или (0,1,0) - проверяем только длину 0
        # Для aabaa babbaab допустимы (0, 4, 3) ["aab"] и (2, 3, 3) ["baa"]
        # Проверяем, что результат один из допустимых
        result_aab = find_longest_common_substring("aabaa", "babbaab")
        self.assertIn(result_aab, [(0, 4, 3), (2, 3, 3)])

        # Крайние случаи: пустые строки
        self.assertEqual(find_longest_common_substring("", "abc"), (0, 0, 0))
        self.assertEqual(find_longest_common_substring("abc", ""), (0, 0, 0))
        self.assertEqual(find_longest_common_substring("", ""), (0, 0, 0))

        # Крайний случай: идентичные строки
        self.assertEqual(find_longest_common_substring("banana", "banana"), (0, 0, 6))

        # Крайний случай: одна строка - подстрока другой
        # Проверяем только длину и соответствие подстрок, т.к. индексы могут варьироваться
        i_ana, j_ana, l_ana = find_longest_common_substring("ana", "banana")
        self.assertEqual(l_ana, 3)
        self.assertEqual("ana"[i_ana:i_ana+l_ana], "banana"[j_ana:j_ana+l_ana])

        i_bana, j_bana, l_bana = find_longest_common_substring("banana", "ana")
        self.assertEqual(l_bana, 3)
        self.assertEqual("banana"[i_bana:i_bana+l_bana], "ana"[j_bana:j_bana+l_bana])


        # Случай: нет общих символов
        self.assertEqual(find_longest_common_substring("abc", "def"), (0, 0, 0))

        # Случай: общая подстрока длины 1
        # Проверяем только длину и соответствие символов
        i_ap, j_ap, l_ap = find_longest_common_substring("apple", "orange")
        self.assertEqual(l_ap, 1)
        self.assertEqual("apple"[i_ap], "orange"[j_ap]) # Должны совпадать ('a' или 'e')


        # Более длинный пример
        # ИСПРАВЛЕНО: Ожидаем один из возможных результатов для длины 1, например (2, 1, 1) для 'o'
        # Можно также проверить только длину:
        # _, _, l_prog = find_longest_common_substring("programming", "competition")
        # self.assertEqual(l_prog, 1)
        # Или проверить принадлежность к множеству допустимых первых символов:
        i_prog, j_prog, l_prog = find_longest_common_substring("programming", "competition")
        self.assertEqual(l_prog, 1)
        self.assertEqual("programming"[i_prog], "competition"[j_prog])


        # Пример с повторениями
        # Проверяем только длину и соответствие подстрок
        i_ab, j_ab, l_ab = find_longest_common_substring("abababab", "babababa")
        self.assertEqual(l_ab, 7)
        self.assertEqual("abababab"[i_ab:i_ab+l_ab], "babababa"[j_ab:j_ab+l_ab])


if __name__ == "__main__":
    # Запуск тестов при выполнении этого файла
    unittest.main()