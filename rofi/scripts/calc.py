#!/usr/bin/env python3
"""Супер-калькулятор через rofi"""
import subprocess
import random
import math
import sys

def rofi(prompt, options=None):
    """Показать rofi-диалог. Если options — меню, иначе — ввод"""
    if options:
        input_data = "\n".join(options)
        result = subprocess.run(
            ["rofi", "-dmenu", "-i", "-p", prompt],
            input=input_data, capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            ["rofi", "-dmenu", "-p", prompt],
            input="", capture_output=True, text=True
        )
    return result.stdout.strip()

def notify(title, message):
    subprocess.run(["notify-send", title, message])
    subprocess.run(["wl-copy"], input=str(message), text=True)

def to_float(s):
    try:
        return float(s)
    except ValueError:
        return None

def to_int(s):
    try:
        return int(float(s))
    except ValueError:
        return None

# --- Арифметика ---
def arithmetic():
    a = to_float(rofi("Первое число"))
    if a is None: return
    op = rofi("Операция", ["+", "-", "*", "/", "**"])
    if not op: return
    b = to_float(rofi("Второе число"))
    if b is None: return
    
    try:
        if op == "+": r = a + b
        elif op == "-": r = a - b
        elif op == "*": r = a * b
        elif op == "/": r = a / b if b != 0 else "деление на ноль"
        elif op == "**": r = a ** b
        notify(f"{a} {op} {b}", f"= {r}")
    except Exception as e:
        notify("Ошибка", str(e))

# --- Проверка чётности ---
def parity():
    n = to_int(rofi("Число"))
    if n is None: return
    notify(f"{n}", "чётное" if n % 2 == 0 else "нечётное")

# --- Случайное число ---
def random_num():
    a = to_int(rofi("От"))
    if a is None: return
    b = to_int(rofi("До"))
    if b is None: return
    r = random.randint(a, b)
    notify(f"Случайное {a}..{b}", f"= {r}")

# --- Геометрия ---
def geometry():
    kind = rofi("Тип", ["📐 Площадь", "📦 Объём"])
    if not kind: return
    
    if "Площадь" in kind:
        fig = rofi("Фигура", ["Прямоугольник", "Квадрат", "Круг"])
        if fig == "Прямоугольник":
            l = to_float(rofi("Длина"))
            w = to_float(rofi("Ширина"))
            if l and w: notify("Площадь прямоугольника", f"= {l * w}")
        elif fig == "Квадрат":
            s = to_float(rofi("Сторона"))
            if s: notify("Площадь квадрата", f"= {s ** 2}")
        elif fig == "Круг":
            r = to_float(rofi("Радиус"))
            if r: notify("Площадь круга", f"= {round(math.pi * r ** 2, 2)}")
    else:
        fig = rofi("Фигура", ["Куб", "Параллелепипед", "Цилиндр"])
        if fig == "Куб":
            a = to_float(rofi("Сторона"))
            if a: notify("Объём куба", f"= {a ** 3}")
        elif fig == "Параллелепипед":
            a = to_float(rofi("Длина"))
            b = to_float(rofi("Ширина"))
            c = to_float(rofi("Высота"))
            if a and b and c: notify("Объём", f"= {a * b * c}")
        elif fig == "Цилиндр":
            r = to_float(rofi("Радиус"))
            h = to_float(rofi("Высота"))
            if r and h: notify("Объём цилиндра", f"= {round(math.pi * r ** 2 * h, 2)}")

# --- Время ---
def time_conv():
    kind = rofi("Что конвертировать", ["📅 Дни → годы/месяцы", "⏱ Секунды → дни/часы/мин"])
    if not kind: return
    
    if "Дни" in kind:
        d = to_int(rofi("Сколько дней"))
        if d is None: return
        y = d // 365
        m = (d % 365) // 30
        rem = (d % 365) % 30
        notify(f"{d} дней", f"{y} лет, {m} мес, {rem} дн")
    else:
        s = to_int(rofi("Сколько секунд"))
        if s is None: return
        d = s // 86400
        rem = s % 86400
        h = rem // 3600
        mi = (rem % 3600) // 60
        se = rem % 60
        notify(f"{s} сек", f"{d}д {h}ч {mi}м {se}с")

# --- Скидки ---
def discount():
    price = to_float(rofi("Старая цена"))
    if price is None: return
    perc = to_float(rofi("Скидка %"))
    if perc is None: return
    save = price * (perc / 100)
    notify(f"Скидка {perc}% от {price}", f"Экономия: {save} | Итог: {price - save}")

# --- Быстрое выражение ---
def quick_expr():
    """Ввести выражение как есть, посчитать через eval"""
    expr = rofi("Выражение (2+2*3, math.sqrt(16))")
    if not expr: return
    try:
        # Безопасный eval с math
        allowed = {"math": math, "abs": abs, "round": round, "min": min, "max": max, "pow": pow}
        r = eval(expr, {"__builtins__": {}}, allowed)
        notify(f"{expr}", f"= {r}")
    except Exception as e:
        notify("Ошибка", str(e))

# --- Главное меню ---
def main():
    choice = rofi("Калькулятор", [
        "⚡ Быстрое выражение",
        "➕ Арифметика",
        "📐 Геометрия",
        "⏱ Время",
        "🎲 Случайное число",
        "💰 Скидки",
        "🔢 Чётность",
    ])
    
    if "Быстрое" in choice: quick_expr()
    elif "Арифметика" in choice: arithmetic()
    elif "Геометрия" in choice: geometry()
    elif "Время" in choice: time_conv()
    elif "Случайное" in choice: random_num()
    elif "Скидки" in choice: discount()
    elif "Чётность" in choice: parity()

if __name__ == "__main__":
    main()
