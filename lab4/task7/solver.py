# Рекомендуется использовать большие простые числа для модулей и баз
# Можно выбрать другие, но эти достаточно распространены
MOD1 = 10 ** 9 + 7
MOD2 = 10 ** 9 + 9
BASE1 = 31  # Простое число больше размера алфавита (26)
BASE2 = 53  # Другое простое число


class Hasher:
    """
    Класс для вычисления полиномиальных хешей строки с использованием
    заданных базы (p) и модуля (m).
    Позволяет быстро вычислять хеш любой подстроки.
    """

    def __init__(self, text, base, mod):
        """
        Инициализирует хешер и предварительно вычисляет необходимые значения.
        :param text: Входная строка.
        :param base: База для полиномиального хеша.
        :param mod: Модуль для хеша.
        """
        self.text = text
        self.base = base
        self.mod = mod
        self.n = len(text)

        # Предварительное вычисление степеней базы по модулю
        self.powers = [1] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.powers[i] = (self.powers[i - 1] * self.base) % self.mod

        # Предварительное вычисление префиксных хешей
        # h[i] хранит хеш префикса text[0...i-1]
        self.prefix_hashes = [0] * (self.n + 1)
        for i in range(self.n):
            # Используем ord(c) - ord('a') + 1, чтобы 'a' соответствовало 1
            char_code = ord(self.text[i]) - ord('a') + 1
            self.prefix_hashes[i + 1] = (self.prefix_hashes[i] * self.base + char_code) % self.mod

    def get_hash(self, start, length):
        """
        Вычисляет хеш подстроки text[start...start+length-1].
        Использует предварительно вычисленные значения для O(1) времени.
        :param start: Начальный индекс подстроки (включительно).
        :param length: Длина подстроки.
        :return: Хеш подстроки.
        """
        if length == 0:
            return 0
        if start + length > self.n:
            raise IndexError("Substring index out of range")

        # Формула: hash(s[i..j]) = (h[j+1] - h[i] * p^(j-i+1)) % m
        # В наших обозначениях: j = start + length - 1, i = start
        # j - i + 1 = length
        # h[j+1] -> self.prefix_hashes[start + length]
        # h[i] -> self.prefix_hashes[start]
        # p^(j-i+1) -> self.powers[length]

        hash_end = self.prefix_hashes[start + length]
        hash_start = (self.prefix_hashes[start] * self.powers[length]) % self.mod

        # Вычисляем (hash_end - hash_start) % mod, учитывая возможное отрицательное значение
        substring_hash = (hash_end - hash_start + self.mod) % self.mod
        return substring_hash


def find_longest_common_substring(s, t):
    """
    Находит наибольшую общую подстроку (LCS) строк s и t с использованием
    бинарного поиска по длине и двойного полиномиального хеширования.

    :param s: Первая строка.
    :param t: Вторая строка.
    :return: Кортеж (i, j, l), где i - начальный индекс LCS в s,
             j - начальный индекс LCS в t, l - длина LCS.
             Если общих подстрок нет, возвращает (0, 0, 0).
    """
    len_s = len(s)
    len_t = len(t)

    # Инициализация хешеров для обеих строк с двумя разными парами (база, модуль)
    hasher_s1 = Hasher(s, BASE1, MOD1)
    hasher_s2 = Hasher(s, BASE2, MOD2)
    hasher_t1 = Hasher(t, BASE1, MOD1)
    hasher_t2 = Hasher(t, BASE2, MOD2)

    # --- Вспомогательная функция для проверки ---
    def check(k):
        """
        Проверяет, существует ли общая подстрока длины k между s и t.
        Использует двойное хеширование для уменьшения коллизий.
        Возвращает (found, index_s, index_t)
        """
        if k == 0:
            return True, 0, 0
        if k > min(len_s, len_t):
            return False, -1, -1

        # Сохраняем хеши подстрок длины k из строки s
        # Ключ - кортеж из двух хешей, значение - начальный индекс i
        hashes_s = {}
        for i in range(len_s - k + 1):
            h1 = hasher_s1.get_hash(i, k)
            h2 = hasher_s2.get_hash(i, k)
            # Если хеш уже есть, сохраняем первый встреченный индекс (не принципиально)
            if (h1, h2) not in hashes_s:
                hashes_s[(h1, h2)] = i

        # Проверяем хеши подстрок длины k из строки t
        for j in range(len_t - k + 1):
            h1 = hasher_t1.get_hash(j, k)
            h2 = hasher_t2.get_hash(j, k)
            if (h1, h2) in hashes_s:
                # Найдена общая подстрока
                return True, hashes_s[(h1, h2)], j  # Возвращаем индексы i и j

        # Общая подстрока длины k не найдена
        return False, -1, -1

    # --- Конец вспомогательной функции ---

    # Бинарный поиск по длине k
    best_l = 0
    best_i = 0
    best_j = 0

    low = 0
    high = min(len_s, len_t)

    while low <= high:
        mid = low + (high - low) // 2
        found, i, j = check(mid)

        if found:
            # Нашли общую подстроку длины mid, возможно есть длиннее
            # Сохраняем текущий лучший результат
            best_l = mid
            best_i = i
            best_j = j
            # Пытаемся найти подстроку большей длины
            low = mid + 1
        else:
            # Подстрока длины mid не найдена, нужно искать короче
            high = mid - 1

    return best_i, best_j, best_l
