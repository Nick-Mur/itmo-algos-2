from utils import time_memory_decorator


@time_memory_decorator
def count_pretty_patterns(M, N):
    """
    Вычисляет количество симпатичных узоров для двора размера M×N.
    Узоры симпатичные, если нигде не встречается квадрат 2×2, полностью заполненный плитками одного цвета.

    Параметры:
      M, N - целые положительные числа, такие что 1 ≤ M*N ≤ 30.

    Возвращает:
      Количество симпатичных узоров.

    Генерирует:
      ValueError, если M или N не являются положительными целыми числами,
      либо если произведение M*N превышает 30.
    """
    # Проверка корректности входных данных
    if not (isinstance(M, int) and isinstance(N, int)):
        raise ValueError("M and N must be integers")
    if M < 1 or N < 1:
        raise ValueError("M and N must be positive integers")
    if M * N > 30:
        raise ValueError("Product of M and N must not exceed 30")

    # Для оптимизации считаем большую сторону за число строк, меньшую – за число столбцов
    rows = max(M, N)
    cols = min(M, N)

    total_masks = 2 ** cols  # все возможные состояния строки

    # Если двор состоит из одной строки, количество узоров равно количеству масок
    if rows == 1:
        return total_masks

    states = list(range(total_masks))

    # Вычисляем допустимые переходы между двумя соседними строками
    valid_transitions = {mask: [] for mask in states}
    for mask1 in states:
        for mask2 in states:
            for i in range(cols - 1):
                a = (mask1 >> i) & 1
                b = (mask1 >> (i + 1)) & 1
                c = (mask2 >> i) & 1
                d = (mask2 >> (i + 1)) & 1
                # Если в квадрате 2×2 все плитки одного цвета – переход недопустим
                if a == b == c == d:
                    break
            else:
                valid_transitions[mask1].append(mask2)

    # Динамическое программирование по строкам
    dp_prev = [1] * total_masks  # для первой строки любая маска допустима
    for _ in range(1, rows):
        dp_curr = [0] * total_masks
        for mask1 in states:
            if dp_prev[mask1]:
                for mask2 in valid_transitions[mask1]:
                    dp_curr[mask2] += dp_prev[mask1]
        dp_prev = dp_curr

    return sum(dp_prev)


def file_io():
    """
    Обрабатывает файлы:
      - Читает входные данные из файла input.txt.
      - Вызывает основной алгоритм.
      - Записывает результат в файл output.txt.
    """
    with open("txt/input.txt", "r") as f:
        parts = f.read().strip().split()
        M, N = int(parts[0]), int(parts[1])

    result = count_pretty_patterns(M, N)

    with open("txt/output.txt", "w") as f:
        f.write(str(result))


if __name__ == "__main__":
    file_io()
