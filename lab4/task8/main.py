import sys
from typing import List, Tuple, Dict

# Параметры для полиномиального хеширования.
HASHING_PARAMETERS: List[Tuple[int, int]] = [
    (257, 1_000_000_007),
    (353, 1_000_000_009) # Используем другие простые числа
]
NUM_HASH_FUNCTIONS = len(HASHING_PARAMETERS)

def _get_substring_hash(prefix_hashes: List[int], base_powers: List[int],
                       start_index: int, length: int, modulus: int) -> int:
    """Вычисляет хеш подстроки text[start_index : start_index + length] за O(1)."""
    if length <= 0:
        return 0
    hash_end = prefix_hashes[start_index + length]
    hash_start_scaled = (prefix_hashes[start_index] * base_powers[length]) % modulus
    substring_hash = (hash_end - hash_start_scaled + modulus) % modulus
    return substring_hash

def _precompute_hashes(text: str, max_len: int) -> Tuple[List[List[int]], List[List[int]]]:
    """Предвычисляет префиксные хеши и степени оснований."""
    text_len = len(text)
    all_prefix_hashes: List[List[int]] = []
    all_base_powers: List[List[int]] = []

    # Обработка случая, когда max_len=0 (например, пустой образец)
    safe_max_len = max(max_len, 0)

    for base, modulus in HASHING_PARAMETERS:
        # Степени основания
        powers = [1] * (safe_max_len + 1)
        for i in range(1, safe_max_len + 1):
            powers[i] = (powers[i - 1] * base) % modulus
        all_base_powers.append(powers)

        # Префиксные хеши
        prefix_hashes = [0] * (text_len + 1)
        for i in range(text_len):
            prefix_hashes[i + 1] = (prefix_hashes[i] * base + ord(text[i])) % modulus
        all_prefix_hashes.append(prefix_hashes)

    return all_prefix_hashes, all_base_powers

def _compare_substrings(
    p_hashes_all: List[List[int]],
    t_hashes_all: List[List[int]],
    powers_all: List[List[int]],
    p_start: int,
    t_start: int,
    length: int
) -> bool:
    """Сравнивает подстроки p и t длины length, используя все хеш-функции."""
    if length == 0:
        return True # Пустые подстроки равны

    for i in range(NUM_HASH_FUNCTIONS):
        modulus = HASHING_PARAMETERS[i][1]
        # Проверка наличия данных (на случай пустых строк)
        if not p_hashes_all[i] or not t_hashes_all[i] or not powers_all[i]:
             return False # Невозможно сравнить, если хеши не вычислены
        p_hash = _get_substring_hash(p_hashes_all[i], powers_all[i], p_start, length, modulus)
        t_hash = _get_substring_hash(t_hashes_all[i], powers_all[i], t_start, length, modulus)
        if p_hash != t_hash:
            return False # Несовпадение хотя бы по одному хешу -> строки не равны
    return True # Хеши совпали для всех функций

def solve_approximate_matching(k: int, t: str, p: str) -> List[int]:
    """
    Находит все вхождения образца p в текст t с не более чем k несовпадениями.

    Args:
        k: Максимальное допустимое количество несовпадений.
        t: Текст.
        p: Образец.

    Returns:
        Список начальных индексов вхождений в t.
    """
    len_t = len(t)
    len_p = len(p)
    result_indices = []

    if len_p == 0: # Образец не может быть пустым по условию, но добавим проверку
        return []
    if len_p > len_t:
        return [] # Образец длиннее текста

    # Предвычисление хешей и степеней
    p_hashes_all, p_powers_all = _precompute_hashes(p, len_p)
    t_hashes_all, t_powers_all = _precompute_hashes(t, len_p) # Степени нужны только до len_p

    # Используем общие степени (они зависят только от длины, не от текста)
    powers_all = p_powers_all

    # Итерация по возможным начальным позициям в тексте
    for i in range(len_t - len_p + 1):
        mismatches = 0
        current_pos = 0 # Текущая позиция сравнения внутри p и t[i:...]

        while current_pos < len_p:
            # Бинарный поиск длины следующего совпадающего участка
            low = 0
            high = len_p - current_pos # Макс. возможная длина совпадения
            match_len = 0

            while low <= high:
                mid = low + (high - low) // 2
                if mid == 0: # Пустой участок всегда совпадает
                    # Не обновляем match_len здесь, чтобы правильно обработать случай
                    # когда сразу идет несовпадение (match_len останется 0)
                    low = mid + 1
                    continue

                # Проверяем, совпадает ли участок длины mid
                if _compare_substrings(
                    p_hashes_all, t_hashes_all, powers_all,
                    current_pos, i + current_pos, mid
                ):
                    # Участок совпал, запоминаем длину и пытаемся найти длиннее
                    match_len = mid # Обновляем на действительную длину совпадения
                    low = mid + 1
                else:
                    # Участок не совпал, ищем короче
                    high = mid - 1

            # Перемещаем текущую позицию на длину совпавшего участка
            current_pos += match_len

            # Если мы не дошли до конца образца, значит, следующий символ - несовпадение
            if current_pos < len_p:
                mismatches += 1
                if mismatches > k:
                    break # Превысили лимит несовпадений для этой позиции i
                current_pos += 1 # Пропускаем символ несовпадения

        # Если цикл завершился без break, значит несовпадений <= k
        if mismatches <= k:
            result_indices.append(i)

    return result_indices

def process_files(input_filename="input.txt", output_filename="output.txt"):
    """
    Читает входные данные из файла, обрабатывает каждую строку и
    записывает результат в выходной файл.
    """
    results_to_write = []
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            for line in infile:
                line = line.strip()
                if not line: continue # Пропуск пустых строк

                parts = line.split()
                if len(parts) != 3:
                    print(f"Предупреждение: Неверный формат строки в {input_filename}: '{line}'", file=sys.stderr)
                    continue # Пропуск некорректных строк

                try:
                    k = int(parts[0])
                    t = parts[1]
                    p = parts[2]
                    # Проверка ограничений (опционально, но полезно)
                    if not (1 <= len(t) <= 200000 and 1 <= len(p) <= min(len(t), 100000) and 0 <= k <= 5):
                         print(f"Предупреждение: Нарушены ограничения для строки: '{line}'", file=sys.stderr)
                         continue

                except ValueError:
                    print(f"Предупреждение: Неверный формат числа k в строке: '{line}'", file=sys.stderr)
                    continue

                # Решение задачи для текущей тройки
                indices = solve_approximate_matching(k, t, p)
                # Формирование строки для вывода
                output_line = f"{len(indices)} {' '.join(map(str, indices))}"
                results_to_write.append(output_line)

    except FileNotFoundError:
        print(f"Ошибка: Входной файл '{input_filename}' не найден.", file=sys.stderr)
        return # Прерываем выполнение, если файл не найден
    except Exception as e:
        print(f"Ошибка при чтении входного файла '{input_filename}': {e}", file=sys.stderr)
        return

    try:
        # Запись всех собранных результатов в выходной файл
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for result_line in results_to_write:
                outfile.write(result_line + '\n')
    except IOError as e:
        print(f"Ошибка: Не удалось записать в выходной файл '{output_filename}'. {e}", file=sys.stderr)


def main():
    """
    Основная функция программы: запускает обработку файлов.
    """
    process_files() # Используются имена файлов по умолчанию "input.txt" и "output.txt".

if __name__ == "__main__":
    # Запуск основной функции при выполнении скрипта.
    main()