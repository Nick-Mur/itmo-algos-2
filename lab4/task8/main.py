import sys
from core.matcher import find_matches
# from core.hashing import Hasher # Не требуется напрямую в main.py

# Для возможного ускорения ввода/вывода в соревновательных задачах
# input = sys.stdin.readline
# output_write = sys.stdout.write

def solve():
    """
    Основная функция для чтения данных, вызова решателя и записи результата.
    """
    input_filename = "input.txt"
    output_filename = "output.txt"

    results_to_write = [] # Собираем результаты для одной записи в файл

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line: # Пропускаем пустые строки
                    continue

                parts = line.split()
                if len(parts) != 3:
                    # Логирование или вывод ошибки о неверном формате строки
                    print(f"Ошибка: Неверный формат строки {line_num}: '{line}'. Ожидалось 3 части.", file=sys.stderr)
                    # В зависимости от требований, можно либо пропустить строку,
                    # либо прервать выполнение. Пропустим.
                    results_to_write.append("Ошибка формата ввода") # Добавляем маркер ошибки
                    continue

                k_str, text, pattern = parts

                try:
                    k = int(k_str)
                except ValueError:
                    print(f"Ошибка: Не удалось преобразовать k='{k_str}' в целое число в строке {line_num}.", file=sys.stderr)
                    results_to_write.append("Ошибка значения k")
                    continue

                # Проверка ограничений (опционально, но полезно)
                # if not (0 <= k <= 5):
                #     print(f"Предупреждение: k={k} вне допустимого диапазона [0, 5] в строке {line_num}.", file=sys.stderr)
                # if not (1 <= len(text) <= 200000):
                #      print(f"Предупреждение: Длина текста {len(text)} вне допустимого диапазона [1, 200000] в строке {line_num}.", file=sys.stderr)
                # if not (1 <= len(pattern) <= min(len(text), 100000)):
                #      print(f"Предупреждение: Длина образца {len(pattern)} вне допустимого диапазона [1, min(|t|, 100000)] в строке {line_num}.", file=sys.stderr)
                # В соревновательных задачах обычно можно положиться на корректность входных данных в рамках ограничений.

                # Вызов основной логики
                try:
                    matches = find_matches(k, text, pattern)
                    # Форматирование результата
                    output_line = f"{len(matches)} {' '.join(map(str, matches))}"
                    results_to_write.append(output_line)
                except Exception as e:
                    # Обработка неожиданных ошибок из find_matches (например, проблемы с хешером)
                    print(f"Критическая ошибка при обработке строки {line_num}: {e}", file=sys.stderr)
                    results_to_write.append(f"Ошибка выполнения: {e}")
                    # Можно прервать выполнение, если ошибка критическая
                    # raise

    except FileNotFoundError:
        print(f"Ошибка: Входной файл '{input_filename}' не найден.", file=sys.stderr)
        return # Прерываем выполнение, если нет входного файла
    except Exception as e:
        print(f"Непредвиденная ошибка при чтении файла '{input_filename}': {e}", file=sys.stderr)
        return

    # Запись всех результатов в выходной файл
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for result_line in results_to_write:
                outfile.write(result_line + '\n')
                # Для использования sys.stdout.write:
                # output_write(result_line + '\n')
    except IOError as e:
        print(f"Ошибка записи в файл '{output_filename}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"Непредвиденная ошибка при записи файла '{output_filename}': {e}", file=sys.stderr)


if __name__ == "__main__":
    solve()