#!/usr/bin/env python3
import subprocess
import time
import sys

def get_current_lang():
    try:
        res = subprocess.run(["niri", "msg", "keyboard-layouts"], capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if '*' in line:
                line_lower = line.lower()
                if "russian" in line_lower:
                    return "RU"
                elif "english" in line_lower or "us" in line_lower:
                    return "EN"
    except:
        pass
    return "EN"

last_lang = ""

while True:
    current_lang = get_current_lang()
    if current_lang != last_lang:
        print(current_lang, flush=True)
        last_lang = current_lang
    # Увеличили паузу до 0.25 сек, чтобы процессор полностью отдыхал
    time.sleep(0.25)
