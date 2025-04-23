import sys
from typing import Tuple, List

# Для ускорения ввода/вывода в соревновательных задачах
# input = sys.stdin.readline
# print = sys.stdout.write


class Hasher:
    """
    Класс для вычисления полиномиальных хешей строк и их подстрок.

    Использует двойное хеширование для уменьшения вероятности коллизий.
    Позволяет получать хеш любой подстроки за O(1) после O(N)
    предварительной обработки, где N - длина исходной строки.
    """
    _DEFAULT_BASE1 = 31
    _DEFAULT_MOD1 = 10**9 + 7
    _DEFAULT_BASE2 = 37
    _DEFAULT_MOD2 = 10**9 + 9

    def __init__(self, text: str,
                 base1: int = _DEFAULT_BASE1, mod1: int = _DEFAULT_MOD1,
                 base2: int = _DEFAULT_BASE2, mod2: int = _DEFAULT_MOD2):
        """
        Инициализирует хешер для заданной строки.

        Args:
            text (str): Входная строка.
            base1 (int): Основание для первого хеша.
            mod1 (int): Модуль для первого хеша.
            base2 (int): Основание для второго хеша.
            mod2 (int): Модуль для второго хеша.
        """
        self.text = text
        self.n = len(text)
        self.base1 = base1
        self.mod1 = mod1
        self.base2 = base2
        self.mod2 = mod2

        # Предвычисление степеней оснований
        self.powers1 = self._precompute_powers(self.base1, self.mod1, self.n)
        self.powers2 = self._precompute_powers(self.base2, self.mod2, self.n)

        # Предвычисление префиксных хешей
        self.prefix_hashes1 = self._compute_prefix_hashes(self.base1, self.mod1)
        self.prefix_hashes2 = self._compute_prefix_hashes(self.base2, self.mod2)

    def _precompute_powers(self, base: int, mod: int, length: int) -> List[int]:
        """Вычисляет степени основания base по модулю mod до length."""
        powers = [1] * (length + 1)
        for i in range(1, length + 1):
            powers[i] = (powers[i - 1] * base) % mod
        return powers

    def _compute_prefix_hashes(self, base: int, mod: int) -> List[int]:
        """Вычисляет префиксные хеши для строки."""
        prefix_hashes = [0] * (self.n + 1)
        for i in range(self.n):
            # Используем ord(c) - ord('a') + 1 для отображения 'a'->1, 'b'->2, ...
            # Это предотвращает проблемы с нулевым хешем для строк вида "aaaa"
            char_code = ord(self.text[i]) - ord('a') + 1
            prefix_hashes[i + 1] = (prefix_hashes[i] * base + char_code) % mod
        return prefix_hashes

    def get_hash(self, start: int, length: int) -> Tuple[int, int]:
        """
        Возвращает двойной хеш подстроки text[start:start+length].

        Индексация 0-based. Длина подстроки - length.
        Подстрока включает символы с индексами от start до start + length - 1.

        Args:
            start (int): Начальный индекс подстроки (включительно).
            length (int): Длина подстроки.

        Returns:
            Tuple[int, int]: Кортеж из двух хешей подстроки.

        Raises:
            IndexError: Если start или start + length выходят за границы строки.
        """
        if not (0 <= start <= start + length <= self.n):
             raise IndexError(f"Substring indices [{start}:{start+length}] are out of bounds for string of length {self.n}")
        if length == 0:
            return (0, 0)

        end_index = start + length

        # Вычисление первого хеша
        hash1 = (self.prefix_hashes1[end_index] -
                 (self.prefix_hashes1[start] * self.powers1[length]) % self.mod1 +
                 self.mod1) % self.mod1

        # Вычисление второго хеша
        hash2 = (self.prefix_hashes2[end_index] -
                 (self.prefix_hashes2[start] * self.powers2[length]) % self.mod2 +
                 self.mod2) % self.mod2

        return (hash1, hash2)

    def compare_substrings(self, start1: int, start2: int, length: int) -> bool:
        """
        Сравнивает две подстроки одинаковой длины с использованием хешей.

        Args:
            start1 (int): Начальный индекс первой подстроки.
            start2 (int): Начальный индекс второй подстроки.
            length (int): Длина сравниваемых подстрок.

        Returns:
            bool: True, если хеши подстрок совпадают, иначе False.
                  (С высокой вероятностью означает равенство подстрок).
        """
        # Эта функция полезна, если обе подстроки находятся в ОДНОЙ строке text
        # Для сравнения подстрок из РАЗНЫХ строк (t и p) нужно использовать
        # get_hash() для каждой строки отдельно.
        if length == 0:
            return True
        hash1_sub1, hash2_sub1 = self.get_hash(start1, length)
        hash1_sub2, hash2_sub2 = self.get_hash(start2, length)
        return hash1_sub1 == hash1_sub2 and hash2_sub1 == hash2_sub2
