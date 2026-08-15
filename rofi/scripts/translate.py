#!/usr/bin/env python3
"""Перевод выделенного текста через deep-translator с fallback"""
import subprocess
import sys
import time

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except ImportError:
    subprocess.run(["notify-send", "Translate", "pip install deep-translator"])
    sys.exit(1)

def get_selection():
    try:
        result = subprocess.run(["wl-paste", "--primary"], capture_output=True, text=True, timeout=2)
        return result.stdout.rstrip('\n\r').strip()
    except Exception:
        return ""

def notify(title, message):
    subprocess.run(["notify-send", title, message])

def detect_lang(text):
    for c in text:
        if 'а' <= c.lower() <= 'я' or c.lower() == 'ё':
            return "ru"
    return "en"

def try_translate(text, source, target):
    errors = []
    translators = [
        ("Google", lambda: GoogleTranslator(source=source, target=target).translate(text)),
        ("MyMemory", lambda: MyMemoryTranslator(source=source, target=target).translate(text)),
    ]
    for name, fn in translators:
        try:
            result = fn()
            if result and result.strip():
                return result, name, None
        except Exception as e:
            errors.append(f"{name}: {str(e)[:60]}")
            continue
    return None, None, " | ".join(errors)

def replace_selection(new_text):
    subprocess.run(["wl-copy"], input=new_text, text=True)
    time.sleep(0.05)
    subprocess.run(["wtype", "-M", "ctrl", "v", "-m", "ctrl"])

def main():
    text = get_selection()
    if not text:
        notify("Translate", "Ничего не выделено")
        sys.exit(1)

    source = detect_lang(text)
    target = "en" if source == "ru" else "ru"

    start = time.time()
    translated, provider, errors = try_translate(text, source, target)
    elapsed = time.time() - start

    if not translated:
        notify("Translate ошибка", errors or "Все переводчики недоступны")
        sys.exit(1)

    replace_selection(translated)
    preview = translated[:100] + ("..." if len(translated) > 100 else "")
    notify(f"Перевод {source.upper()}→{target.upper()} · {provider} ({elapsed:.2f}с)", preview)

if __name__ == "__main__":
    main()
