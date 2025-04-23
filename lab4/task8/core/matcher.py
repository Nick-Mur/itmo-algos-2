from typing import List
from lab4.task8.core.hashing import Hasher

def find_matches(k: int, text: str, pattern: str) -> List[int]:
    """
    Находит все начальные индексы в тексте 'text', с которых начинается
    подстрока, отличающаяся от образца 'pattern' не более чем на 'k' символов.

    Использует полиномиальное хеширование и бинарный поиск для
    эффективного нахождения несовпадений.

    Args:
        k (int): Максимально допустимое количество несовпадений.
        text (str): Строка текста для поиска.
        pattern (str): Строка-образец.

    Returns:
        List[int]: Отсортированный список начальных индексов (0-based)
                   вхождений образца с не более чем k несовпадениями.
                   Возвращает пустой список, если вхождений нет или
                   длина образца больше длины текста.
    """
    text_len = len(text)
    pattern_len = len(pattern)
    result_indices: List[int] = []

    if pattern_len == 0 or pattern_len > text_len or k < 0:
        return []

    try:
        text_hasher = Hasher(text)
        pattern_hasher = Hasher(pattern)
    except Exception as e:
        # В реальном приложении здесь было бы логирование
        # print(f"Ошибка инициализации Hasher: {e}", file=sys.stderr)
        return []

    for i in range(text_len - pattern_len + 1):
        mismatches = 0
        current_pos_in_pattern = 0

        while current_pos_in_pattern < pattern_len:
            # --- Бинарный поиск для Longest Common Prefix (LCP) ---
            low = 0
            high = pattern_len - current_pos_in_pattern
            lcp_len = 0

            while low <= high:
                mid = (low + high) // 2
                if mid == 0:
                    low = mid + 1
                    continue

                try:
                    pattern_sub_hash = pattern_hasher.get_hash(current_pos_in_pattern, mid)
                    text_sub_hash = text_hasher.get_hash(i + current_pos_in_pattern, mid)
                except IndexError:
                    # Теоретически не должно происходить при правильных границах high
                    high = mid - 1
                    continue

                if pattern_sub_hash == text_sub_hash:
                    lcp_len = mid
                    low = mid + 1
                else:
                    high = mid - 1
            # --- Конец бинарного поиска ---

            current_pos_in_pattern += lcp_len

            if current_pos_in_pattern < pattern_len:
                mismatches += 1
                if mismatches > k:
                    # Превысили лимит, дальше для этого i проверять бессмысленно
                    break
                current_pos_in_pattern += 1 # Пропускаем символ несовпадения

        # Если цикл завершился (проверили весь паттерн) и не превысили k
        if mismatches <= k:
            result_indices.append(i)

    return result_indices