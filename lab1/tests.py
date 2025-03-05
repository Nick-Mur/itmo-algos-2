import unittest
from lab1.main import count_pretty_patterns


class TestCountPrettyPatterns(unittest.TestCase):
    def test_ideal(self):
        """Идеальные случаи: тестирование с известными входными данными и результатами."""
        self.assertEqual(count_pretty_patterns(2, 2), 14)
        self.assertEqual(count_pretty_patterns(3, 3), 322)

    def test_ordinary(self):
        """Обычные случаи: прямоугольники с разными сторонами и проверка симметрии."""
        self.assertEqual(count_pretty_patterns(1, 2), 4)
        self.assertEqual(count_pretty_patterns(2, 1), 4)
        # Проверяем, что результат не зависит от порядка сторон.
        self.assertEqual(count_pretty_patterns(2, 3), count_pretty_patterns(3, 2))

    def test_edge(self):
        """Краевой случай: минимальный допустимый размер 1×1."""
        self.assertEqual(count_pretty_patterns(1, 1), 2)

    def test_extreme(self):
        """Крайний допустимый случай: произведение сторон равно 30 (например, 5×6)."""
        result = count_pretty_patterns(5, 6)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_error(self):
        """Ошибочные ситуации: передача некорректных значений."""
        with self.assertRaises(ValueError):
            count_pretty_patterns(0, 5)
        with self.assertRaises(ValueError):
            count_pretty_patterns(5, 0)
        with self.assertRaises(ValueError):
            count_pretty_patterns(-1, 5)
        with self.assertRaises(ValueError):
            count_pretty_patterns(4, 8)  # 4×8 = 32, что больше допустимого значения 30
        with self.assertRaises(ValueError):
            count_pretty_patterns(2.5, 3)  # нецелое число


if __name__ == '__main__':
    unittest.main()
