import math
import timeit
import matplotlib.pyplot as plt


"""
Время вычислений (Baseline)  = 229.25 секунд
Шаг 1. Оставив представленный ниже код, переписать функции для нахождения чисел с помощью Cython, 
запустить timeit с аналогичными параметрами и сравнить два варианта, построить график.
С помощью annotate=True сгенерируйте html (где визуализировано взаимодействие с Python-интерпретатором) и приложите его к отчету. 
"""


def is_perfect_square(n):
    """Проверяет, является ли число полным квадратом."""
    if n < 0:
        return False
    root = int(math.isqrt(n))
    return root * root == n


def fermat_factorization(N, max_iter=10**7):
    """Разложение числа N на множители методом Ферма."""
    if N % 2 == 0:
        return 2, N // 2  # Если N четное, делим на 2

    x = math.isqrt(N) + 1  # Начинаем с ближайшего целого числа к √N
    count = 0
    while count < max_iter:
        y_squared = x * x - N
        if is_perfect_square(y_squared):
            y = int(math.isqrt(y_squared))
            return (x - y, x + y)  # Возвращаем найденные множители
        x += 1  # Увеличиваем x
        count += 1
    return None  # Не удалось найти разложение за max_iter шагов


# Пример использования
if __name__ == '__main__':
    TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009, 700000133,
                61335395416403926747]

    # Python version timing
    py_time = timeit.repeat(
        "res = [fermat_factorization(i) for i in TEST_LST]",
        number=10, repeat=1, globals=globals()
    )
    print("Python time:", py_time)

    # Cython version timing
    cy_time = None
    try:
        from fermat_cy import fermat_factorization_cy
        
        _MAX_ITER_VALUE = 10**7  # Define the max_iter value to be passed

        stmt_for_cython = "res = [fermat_factorization_cy(i, _MAX_ITER_VALUE) for i in TEST_LST]"
        
        cy_globals = {
            'fermat_factorization_cy': fermat_factorization_cy,
            'TEST_LST': TEST_LST,
            '_MAX_ITER_VALUE': _MAX_ITER_VALUE
        }

        cy_time = timeit.repeat(
            stmt_for_cython,
            number=10, 
            repeat=1, 
            globals=cy_globals
        )
        print("Cython time:", cy_time)
    except ImportError:
        print("Cython module not compiled. Please run: python setup.py build_ext --inplace")

    # Plotting
    try:
        if cy_time is not None:
            plt.bar(['Python', 'Cython'], [py_time[0], cy_time[0]])
            plt.ylabel('Time (s)')
            plt.title('Fermat Factorization: Python vs Cython')
            plt.show()
        else:
            print("Skipping plot: Cython results not available.")
    except Exception as e:
        print("Plotting failed:", e)