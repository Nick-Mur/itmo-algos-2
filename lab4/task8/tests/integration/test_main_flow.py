import unittest
import os
import sys
import shutil
import subprocess

# Добавляем корневую директорию проекта в PYTHONPATH, чтобы найти core и main
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Импортируем функцию solve из main после добавления пути
# Если main.py не предназначен для импорта, используем subprocess
# from main import solve # Раскомментировать, если main.solve() можно вызывать

class TestMainFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Создает директорию фикстур и базовые фикстуры один раз перед всеми тестами."""
        # cls.base_dir = os.path.dirname(project_root) # Ошибка: это родительская директория
        cls.base_dir = project_root # Исправление: base_dir - это корень проекта (task8), где лежит main.py
        cls.fixtures_dir = os.path.join(project_root, 'tests', 'integration', 'fixtures')
        cls.input_path = os.path.join(cls.base_dir, "input.txt") # Путь к рабочему input.txt
        cls.output_path = os.path.join(cls.base_dir, "output.txt") # Путь к рабочему output.txt

        # Создаем директорию фикстур, если ее нет
        if not os.path.exists(cls.fixtures_dir):
            os.makedirs(cls.fixtures_dir)
            print(f"Created fixtures directory: {cls.fixtures_dir}")

        # Создаем базовые фикстуры из примера, если их нет
        cls.example_input_path = os.path.join(cls.fixtures_dir, "case_example_input.txt")
        cls.example_output_path = os.path.join(cls.fixtures_dir, "case_example_output.txt")
        cls.empty_input_path = os.path.join(cls.fixtures_dir, "case_empty_input.txt")
        cls.empty_output_path = os.path.join(cls.fixtures_dir, "case_empty_output.txt")

        if not os.path.exists(cls.example_input_path):
            with open(cls.example_input_path, 'w', encoding='utf-8') as f:
                f.write("0 ababab baaa\n")
                f.write("1 ababab baaa\n")
                f.write("1 xabcabc ccc\n")
                f.write("2 xabcabc ccc\n")
                f.write("3 aaa xxx\n")
            print(f"Created fixture: {cls.example_input_path}")

        if not os.path.exists(cls.example_output_path):
            with open(cls.example_output_path, 'w', encoding='utf-8') as f:
                f.write("0\n")
                f.write("1 1\n")
                f.write("0\n")
                f.write("4 1 2 3 4\n")
                f.write("1 0\n")
            print(f"Created fixture: {cls.example_output_path}")

        # Создаем пустые фикстуры для теста empty_input
        if not os.path.exists(cls.empty_input_path):
             with open(cls.empty_input_path, 'w', encoding='utf-8') as f:
                 pass # Просто создаем пустой файл
             print(f"Created fixture: {cls.empty_input_path}")

        if not os.path.exists(cls.empty_output_path):
             with open(cls.empty_output_path, 'w', encoding='utf-8') as f:
                 pass # Просто создаем пустой файл
             print(f"Created fixture: {cls.empty_output_path}")


    def setUp(self):
        """Настройка перед каждым интеграционным тестом."""
        # Удаляем старые рабочие файлы input/output перед каждым тестом
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists(self.input_path):
             os.remove(self.input_path)

    def tearDown(self):
        """Очистка после каждого интеграционного теста."""
        pass

    def _run_main_and_compare(self, fixture_basename: str):
        """
        Запускает main.py с фикстурным вводом и сравнивает вывод.

        Args:
            fixture_basename (str): Базовое имя файла фикстуры (без _input.txt/_output.txt).
        """
        input_fixture = os.path.join(self.fixtures_dir, f"{fixture_basename}_input.txt")
        expected_output_fixture = os.path.join(self.fixtures_dir, f"{fixture_basename}_output.txt")

        # Проверка существования фикстур (должны быть созданы в setUpClass)
        self.assertTrue(os.path.exists(input_fixture), f"Input fixture not found: {input_fixture}")
        self.assertTrue(os.path.exists(expected_output_fixture), f"Output fixture not found: {expected_output_fixture}")

        # Копируем фикстуру в input.txt
        shutil.copyfile(input_fixture, self.input_path)

        # Запускаем main.py как отдельный процесс
        main_script_path = os.path.join(self.base_dir, 'main.py') # Полный путь к main.py
        try:
            process = subprocess.run(
                [sys.executable, main_script_path], # Используем полный путь к main.py
                cwd=self.base_dir, # Устанавливаем рабочую директорию = корень проекта
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            if process.stderr:
                 print(f"Stderr from main.py:\n{process.stderr}", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            self.fail(f"main.py execution failed with code {e.returncode}:\nScript: {main_script_path}\nStdout:\n{e.stdout}\nStderr:\n{e.stderr}")
        except FileNotFoundError:
             self.fail(f"Failed to execute main.py. Is it in the correct location? ({main_script_path})")

        # Проверяем, что выходной файл создан
        self.assertTrue(os.path.exists(self.output_path), "Output file was not created.")

        # Сравниваем содержимое файлов
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f_actual, \
                 open(expected_output_fixture, 'r', encoding='utf-8') as f_expected:
                # Читаем строки, удаляем пробельные символы с концов, фильтруем пустые строки
                actual_lines = [line.strip() for line in f_actual if line.strip()]
                expected_lines = [line.strip() for line in f_expected if line.strip()]
                # Сравниваем списки строк для лучшего вывода различий
                self.assertListEqual(actual_lines, expected_lines,
                                 f"Output content mismatch for fixture '{fixture_basename}'")
        except IOError as e:
            self.fail(f"Error reading output files for fixture '{fixture_basename}': {e}")

    def test_example_cases(self):
        """Тест на основе примеров из условия задачи."""
        self._run_main_and_compare("case_example")

    def test_edge_cases(self):
        """Тест дополнительных граничных случаев."""
        # Создайте файлы case_edge_input.txt и case_edge_output.txt в fixtures
        # Пример содержимого case_edge_input.txt:
        # 0 aaaaa aaaaa
        # 1 abcdef abcdef
        # 2 abcdef xyzabc
        # 1 abc ""
        # 0 "" abc
        # 1 a b
        # 5 abcdefghijklmno pqrst
        #
        # Пример содержимого case_edge_output.txt:
        # 1 0
        # 1 0
        # 1 3
        # Ошибка формата ввода
        # Ошибка формата ввода
        # 0
        # 11 0 1 2 3 4 5 6 7 8 9 10
        #
        # Раскомментируйте строку ниже после создания файлов
        # self._run_main_and_compare("case_edge")
        pass # Заглушка, пока файлы не созданы

    def test_empty_input_file(self):
        """Тест с пустым входным файлом."""
        self._run_main_and_compare("case_empty")


if __name__ == '__main__':
    # Запуск тестов через unittest.main()
    # Создание фикстур теперь происходит в setUpClass
    unittest.main()