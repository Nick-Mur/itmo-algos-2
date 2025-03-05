import time
import tracemalloc
import functools


def time_memory_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()  # запускаем мониторинг памяти
        start_time = time.perf_counter()  # запоминаем время старта

        result = func(*args, **kwargs)

        end_time = time.perf_counter()  # время завершения
        current, peak = tracemalloc.get_traced_memory()  # получаем текущее и пиковое использование памяти
        tracemalloc.stop()  # останавливаем мониторинг памяти

        elapsed_time = end_time - start_time
        print(f"Время выполнения функции {func.__name__}: {elapsed_time:.6f} секунд")
        print(f"Пиковое использование памяти: {peak / 1024:.2f} КБ")
        return result

    return wrapper
