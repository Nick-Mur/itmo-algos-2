import sys
from solver import find_longest_common_substring


def main():
    """
    Читает пары строк из input.txt, находит LCS для каждой пары
    и записывает результат в output.txt.
    """
    input_filename = "input.txt"
    output_filename = "output.txt"

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile, \
                open(output_filename, 'w', encoding='utf-8') as outfile:

            lines = infile.readlines()
            results = []

            for line in lines:
                line = line.strip()
                if not line:  # Пропустить пустые строки
                    continue

                parts = line.split()
                if len(parts) == 2:
                    s, t = parts
                    # Вызов основной функции решения
                    i, j, l = find_longest_common_substring(s, t)
                    results.append(f"{i} {j} {l}")
                elif len(parts) == 1:  # Случай, если одна из строк пустая
                    s = parts[0]
                    t = ""
                    i, j, l = find_longest_common_substring(s, t)
                    results.append(f"{i} {j} {l}")
                elif len(parts) == 0:  # Случай, если обе строки пустые (хотя split обычно не дает такого)
                    i, j, l = find_longest_common_substring("", "")
                    results.append(f"{i} {j} {l}")
                else:
                    print(f"Warning: Skipping invalid line in {input_filename}: '{line}'", file=sys.stderr)

            # Запись результатов в выходной файл
            outfile.write("\n".join(results) + "\n")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()