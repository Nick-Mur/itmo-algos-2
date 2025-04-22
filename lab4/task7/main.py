import sys
from typing import List, Tuple, Dict
from utils import time_memory_decorator
# Параметры для полиномиального хеширования.
# Используются два различных набора (основание, модуль) для снижения вероятности коллизий.
HASHING_PARAMETERS: List[Tuple[int, int]] = [
    (257, 1_000_000_007),
    (263, 1_000_000_009)
]
# Количество используемых различных хеш-функций.
NUM_HASH_FUNCTIONS = len(HASHING_PARAMETERS)

def get_substring_hash(prefix_hashes: List[int], base_powers: List[int],
                       start_index: int, length: int, modulus: int) -> int:
    """
    Вычисляет хеш подстроки text[start_index : start_index + length] за O(1).

    Использует предвычисленные префиксные хеши и степени основания.

    Args:
        prefix_hashes: Список префиксных хешей строки.
        base_powers: Список предвычисленных степеней основания по модулю.
        start_index: Начальный индекс подстроки.
        length: Длина подстроки.
        modulus: Модуль хеширования.

    Returns:
        Хеш-значение подстроки.
    """
    if length <= 0:
        return 0
    # Вычисление хеша подстроки по формуле с использованием префиксных хешей.
    hash_end = prefix_hashes[start_index + length]
    hash_start_scaled = (prefix_hashes[start_index] * base_powers[length]) % modulus
    substring_hash = (hash_end - hash_start_scaled + modulus) % modulus
    return substring_hash

def check_substring_existence(target_length: int, s_len: int, t_len: int,
                              s_prefix_hashes_all: List[List[int]],
                              t_prefix_hashes_all: List[List[int]],
                              base_powers_all: List[List[int]]) -> Tuple[bool, int, int]:
    """
    Проверяет, существует ли общая подстрока заданной длины target_length между s и t.

    Использует хеш-таблицу для O(1) проверки наличия хешей подстрок.
    Применяет множественное хеширование для надежности.

    Args:
        target_length: Проверяемая длина общей подстроки.
        s_len: Длина строки s.
        t_len: Длина строки t.
        s_prefix_hashes_all: Списки префиксных хешей для s (для каждой хеш-функции).
        t_prefix_hashes_all: Списки префиксных хешей для t (для каждой хеш-функции).
        base_powers_all: Списки предвычисленных степеней основания (для каждой хеш-функции).

    Returns:
        Кортеж (exists, index_s, index_t): флаг существования подстроки и её начальные индексы.
    """
    if target_length == 0:
        return True, 0, 0 # Подстрока нулевой длины всегда существует.
    if target_length > s_len or target_length > t_len:
         return False, 0, 0 # Подстрока не может быть длиннее строк.

    # Хеш-таблица для хранения кортежей хешей подстрок s и их начальных индексов.
    s_substring_hashes: Dict[Tuple[int, ...], int] = {}

    # Заполнение хеш-таблицы хешами подстрок строки s.
    for i in range(s_len - target_length + 1):
        current_s_hashes = []
        for func_index in range(NUM_HASH_FUNCTIONS):
            prefix_hashes = s_prefix_hashes_all[func_index]
            base_powers = base_powers_all[func_index]
            _, modulus = HASHING_PARAMETERS[func_index]
            h = get_substring_hash(prefix_hashes, base_powers, i, target_length, modulus)
            current_s_hashes.append(h)

        hash_key = tuple(current_s_hashes)
        if hash_key not in s_substring_hashes:
             s_substring_hashes[hash_key] = i # Сохраняем индекс первого вхождения.

    # Проверка хешей подстрок строки t на наличие в хеш-таблице s.
    for j in range(t_len - target_length + 1):
        current_t_hashes = []
        for func_index in range(NUM_HASH_FUNCTIONS):
            prefix_hashes = t_prefix_hashes_all[func_index]
            base_powers = base_powers_all[func_index]
            _, modulus = HASHING_PARAMETERS[func_index]
            h = get_substring_hash(prefix_hashes, base_powers, j, target_length, modulus)
            current_t_hashes.append(h)

        hash_key = tuple(current_t_hashes)
        if hash_key in s_substring_hashes:
            # Найдена общая подстрока.
            return True, s_substring_hashes[hash_key], j

    # Общая подстрока данной длины не найдена.
    return False, 0, 0

@time_memory_decorator
def find_longest_common_substring(s: str, t: str) -> Tuple[int, int, int]:
    """
    Находит параметры наибольшей общей подстроки между строками s и t.

    Использует бинарный поиск по длине подстроки и полиномиальное хеширование
    для эффективной проверки существования общей подстроки заданной длины.

    Args:
        s: Первая строка.
        t: Вторая строка.

    Returns:
        Кортеж (index_s, index_t, length): начальные индексы и длина наибольшей общей подстроки.
    """
    s_len = len(s)
    t_len = len(t)
    max_possible_length = min(s_len, t_len)

    # Обработка случая, когда одна из строк пустая, до вычислений
    if max_possible_length == 0:
        return 0, 0, 0

    # Предварительное вычисление хешей и степеней для обеих строк и всех хеш-функций.
    base_powers_all: List[List[int]] = []
    s_prefix_hashes_all: List[List[int]] = []
    t_prefix_hashes_all: List[List[int]] = []

    for func_index, (base, modulus) in enumerate(HASHING_PARAMETERS):
        # Вычисление степеней основания.
        powers = [1] * (max_possible_length + 1)
        for i in range(1, max_possible_length + 1):
            powers[i] = (powers[i - 1] * base) % modulus
        base_powers_all.append(powers)

        # Вычисление префиксных хешей для s.
        prefix_hashes_s = [0] * (s_len + 1)
        for i in range(s_len):
            prefix_hashes_s[i + 1] = (prefix_hashes_s[i] * base + ord(s[i])) % modulus
        s_prefix_hashes_all.append(prefix_hashes_s)

        # Вычисление префиксных хешей для t.
        prefix_hashes_t = [0] * (t_len + 1)
        for i in range(t_len):
            prefix_hashes_t[i + 1] = (prefix_hashes_t[i] * base + ord(t[i])) % modulus
        t_prefix_hashes_all.append(prefix_hashes_t)

    # Бинарный поиск по длине общей подстроки.
    low_len = 0
    high_len = max_possible_length
    best_length, best_index_s, best_index_t = 0, 0, 0 # Хранение лучшего результата.

    while low_len <= high_len:
        current_length = low_len + (high_len - low_len) // 2
        # Проверка существования общей подстроки текущей длины.
        exists, current_index_s, current_index_t = check_substring_existence(
            current_length, s_len, t_len,
            s_prefix_hashes_all, t_prefix_hashes_all, base_powers_all
        )

        if exists:
            # Если найдена, сохраняем результат и пытаемся найти подстроку большей длины.
            best_length = current_length
            best_index_s = current_index_s
            best_index_t = current_index_t
            low_len = current_length + 1
        else:
            # Если не найдена, ищем подстроку меньшей длины.
            high_len = current_length - 1

    return best_index_s, best_index_t, best_length

def process_input_file(input_filename="input.txt", output_filename="output.txt"):
    """
    Обрабатывает входной файл, содержащий пары строк, и записывает результаты
    (параметры наибольшей общей подстроки) в выходной файл.

    Args:
        input_filename: Имя входного файла.
        output_filename: Имя выходного файла.
    """
    results = [] # Список для хранения строк результата.
    try:
        # Чтение входного файла.
        with open(input_filename, 'r', encoding='utf-8') as infile:
            for line in infile:
                line = line.strip()
                if not line: continue # Пропуск пустых строк.
                try:
                    s, t = line.split()
                    # Поиск наибольшей общей подстроки.
                    index_s, index_t, length = find_longest_common_substring(s, t)
                    results.append(f"{index_s} {index_t} {length}")
                except ValueError:
                    # Обработка некорректных строк во входном файле.
                    print(f"Предупреждение: Неверный формат строки в {input_filename}: '{line}'", file=sys.stderr)

    except FileNotFoundError:
        print(f"Ошибка: Входной файл '{input_filename}' не найден.", file=sys.stderr)
        return

    try:
        # Запись результатов в выходной файл.
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for result_line in results:
                outfile.write(result_line + '\n')
    except IOError as e:
        print(f"Ошибка: Не удалось записать в выходной файл '{output_filename}'. {e}", file=sys.stderr)


def main():
    """
    Основная функция программы: запускает обработку файлов.
    """
    process_input_file() # Используются имена файлов по умолчанию "input.txt" и "output.txt".

if __name__ == "__main__":
    # Запуск основной функции при выполнении скрипта.
    main()