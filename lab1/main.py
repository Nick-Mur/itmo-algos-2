from utils import time_memory_decorator
from typing import Dict, List


def is_valid_transition(mask1: int, mask2: int, cols: int) -> bool:
    """
    Проверяет, допускается ли переход от раскраски mask1 к раскраске mask2,
    чтобы не образовался квадрат 2×2, заполненный плитками одного цвета.

    Параметры:
      mask1 (int): Битовая маска первой строки.
      mask2 (int): Битовая маска второй строки.
      cols (int): Число столбцов (длина строки).

    Возвращает:
      bool: True, если переход допустим, иначе False.
    """
    for i in range(cols - 1):
        a = (mask1 >> i) & 1
        b = (mask1 >> (i + 1)) & 1
        c = (mask2 >> i) & 1
        d = (mask2 >> (i + 1)) & 1
        if a == b == c == d:
            return False
    return True


def count_pretty_patterns(M: int, N: int) -> int:
    """
    Вычисляет количество симпатичных узоров для двора размера M×N.
    Узор считается симпатичным, если нигде не встречается квадрат 2×2,
    полностью заполненный плитками одного цвета.

    Параметры:
      M (int): Число, представляющее одну сторону двора (должно быть положительным).
      N (int): Число, представляющее другую сторону двора (должно быть положительным).
              Допускается условие 1 ≤ M*N ≤ 30.

    Возвращает:
      int: Количество различных симпатичных узоров.

    Генерирует:
      ValueError: Если M или N не являются положительными целыми числами,
                  либо если произведение M*N превышает 30.
    """
    # Проверка корректности входных данных
    if not (isinstance(M, int) and isinstance(N, int)):
        raise ValueError("M and N must be integers")
    if M < 1 or N < 1:
        raise ValueError("M and N must be positive integers")
    if M * N > 30:
        raise ValueError("Product of M and N must not exceed 30")

    # Определяем число строк и столбцов:
    # больший размер будем считать числом строк, меньший – числом столбцов.
    rows: int = max(M, N)
    cols: int = min(M, N)

    total_masks: int = 2 ** cols  # общее число состояний строки
    if rows == 1:
        return total_masks

    # Генерируем список всех состояний строки.
    states: List[int] = list(range(total_masks))

    # Предварительно вычисляем допустимые переходы между двумя соседними строками.
    valid_transitions: Dict[int, List[int]] = {
        mask: [mask2 for mask2 in states if is_valid_transition(mask, mask2, cols)]
        for mask in states
    }

    # Инициализируем динамическое программирование:
    # dp_prev[mask] хранит количество способов получить раскраску mask для предыдущей строки.
    dp_prev: List[int] = [1] * total_masks

    # Итеративно обрабатываем каждую последующую строку.
    for _ in range(1, rows):
        dp_curr: List[int] = [0] * total_masks
        for mask1 in states:
            ways = dp_prev[mask1]
            if ways:
                for mask2 in valid_transitions[mask1]:
                    dp_curr[mask2] += ways
        dp_prev = dp_curr

    return sum(dp_prev)


@time_memory_decorator
def file_io() -> None:
    """
    Обрабатывает файлы:
      - Читает входные данные из файла txt/input.txt.
      - Вызывает функцию count_pretty_patterns для вычисления результата.
      - Записывает результат в файл txt/output.txt.
    """
    with open("txt/input.txt", "r") as f:
        parts = f.read().strip().split()
        M, N = int(parts[0]), int(parts[1])

    result: int = count_pretty_patterns(M, N)

    with open("txt/output.txt", "w") as f:
        f.write(str(result))


if __name__ == "__main__":
    file_io()
