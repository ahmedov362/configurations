#!/usr/bin/env python3
"""Смена раскладки выделенного текста ru↔en + замена выделения"""
import subprocess
import sys
import time

EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~"
RU = "йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"

EN_TO_RU = str.maketrans(EN, RU)
RU_TO_EN = str.maketrans(RU, EN)

def get_selection():
    try:
        result = subprocess.run(["wl-paste", "--primary"], capture_output=True, text=True, timeout=2)
        return result.stdout
    except Exception:
        return ""

def detect_lang(text):
    ru_count = sum(1 for c in text if c in RU)
    en_count = sum(1 for c in text if c in EN)
    return "ru" if ru_count > en_count else "en"

def notify(title, message):
    subprocess.run(["notify-send", title, message])

def replace_selection(new_text):
    subprocess.run(["wl-copy"], input=new_text, text=True)
    time.sleep(0.05)
    subprocess.run(["wtype", "-M", "ctrl", "v", "-m", "ctrl"])

def main():
    text = get_selection()
    if not text.strip():
        notify("Switch", "Ничего не выделено")
        sys.exit(1)

    lang = detect_lang(text)
    if lang == "ru":
        converted = text.translate(RU_TO_EN)
        direction = "RU → EN"
    else:
        converted = text.translate(EN_TO_RU)
        direction = "EN → RU"

    replace_selection(converted)
    preview = converted[:50] + ("..." if len(converted) > 50 else "")
    notify(f"Смена раскладки ({direction})", preview)

if __name__ == "__main__":
    main()
