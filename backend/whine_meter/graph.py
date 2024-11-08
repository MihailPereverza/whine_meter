from datetime import datetime

import matplotlib.pyplot as plt
import io
import matplotlib.dates as mdates


def generate_for_dates(data: dict[datetime, float]) -> io.BytesIO:
    """
    Функция обрабатывает словарь с датами в качестве ключей и числами от 0 до 1 в качестве значений.
    И возвращает график в формате BytesIO

    Parameters:
        data (dict): Словарь, где ключи — объекты строки, а значения — числа от 0 до 1.
    """
    sorted_dates = [date for date in sorted(data)]
    sorted_values = [data[date] for date in sorted(data)]
    plt.figure(figsize=(5, 5), dpi=100)  # Итоговое изображение будет 500x500 пикселей

    # Строим линию графика
    plt.plot(sorted_dates, sorted_values, color='lightgray', linewidth=0.5, label='Уровень нытья')

    # Генерация цветов для точек в зависимости от значений
    scatter_colors = plt.cm.RdYlGn_r(sorted_values)  # Цвета для точек (обратная цветовая карта)

    # Строим точки с разными цветами
    plt.scatter(sorted_dates, sorted_values, color=scatter_colors)

    ax = plt.gca()  # Получаем текущую ось
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Автоустановка локатора для дат
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #  if len(sorted_dates) > 10 else '%d.%m'))  # Форматирование дат

    plt.ylim(0, 1.1)  # Устанавливаем пределы по оси Y
    plt.title("Как менялся уровень нытья")
    plt.xlabel("Время")
    plt.ylabel("Уровень нытья")
    plt.legend()

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Закрываем график, чтобы очистить память

    # Возвращаемся в начало буфера
    buf.seek(0)
    return buf


def generate_for_users(data: dict[str, float]) -> io.BytesIO:
    """
    Функция обрабатывает словарь с датами в качестве ключей и числами от 0 до 1 в качестве значений.
    И возвращает график в формате BytesIO

    Parameters:
        data (dict): Словарь, где ключи — объекты datetime, а значения — числа от 0 до 1.
    """
    sorted_items = sorted(data.items(), key=lambda item: item[1])
    sorted_users = [item[0] for item in sorted_items]
    sorted_values = [item[1] for item in sorted_items]

    plt.figure(figsize=(5, 5), dpi=100)  # Итоговое изображение будет 500x500 пикселей

    # Генерация цветов для точек в зависимости от значений
    scatter_colors = plt.cm.RdYlGn_r(sorted_values)  # Цвета для точек (обратная цветовая карта)

    # Строим точки с разными цветами
    plt.bar(sorted_users, sorted_values, color=scatter_colors)

    plt.ylim(0, 1)  # Устанавливаем пределы по оси Y
    plt.title("Рейтинг нытиков")
    #plt.xlabel("Имя")
    plt.ylabel("Уровень нытья")
    plt.legend()
    # Поворот подписей на оси X на 90 градусов
    plt.xticks(rotation=90)
    plt.tight_layout()
    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Закрываем график, чтобы очистить память

    # Возвращаемся в начало буфера
    buf.seek(0)
    return buf

# код для jupyter
# Генерируем изображение и отображаем его
# image_bytes = generate_for_dates(data)
# display(Image(data=image_bytes.getvalue()))

