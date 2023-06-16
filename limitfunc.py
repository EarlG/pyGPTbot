import time

def limit_function_calls(func, n_max=10, t_period=3600):
    count = 0
    last_call_time = 0

    def wrapper(*args, **kwargs):
        nonlocal count, last_call_time

        current_time = time.time()
        elapsed_time = current_time - last_call_time

        if count >= n_max and elapsed_time < t_period:
            print("Превышен лимит вызовов функции.")
        else:
            func(*args, **kwargs)
            count += 1
            last_call_time = current_time

    return wrapper

# Пример функции func1, которую мы хотим ограничить
def func1():
    print("Функция func1 была вызвана.")

# Применение декоратора к функции func1
func1 = limit_function_calls(func1, n_max=5, t_period=1800)

# Пример вызова функции
func1()  # Вызывается успешно
func1()  # Вызывается успешно
# ...
func1()  # Вызывается успешно
func1()  # Вызывается успешно
func1()  # Вызывается успешно
func1()  # Вызывается успешно
# Вызов функции func1 превышает лимит 5 раз в течение 30 минут
func1()  # Выводит сообщение "Превышен лимит вызовов функции."