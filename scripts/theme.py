#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

NOCTALIA_COLORS = Path.home() / '.config/noctalia/colors.json'
KITTY_COLORS    = Path.home() / '.config/kitty/colors.conf'
NIRI_CONFIG     = Path.home() / '.config/niri/config.kdl'
CLOCK_SCRIPT    = Path.home() / 'Projects/datatime/main.py'

def load_colors():
    return json.loads(NOCTALIA_COLORS.read_text())

def apply_kitty(c):
    try:
        content = f"""# Auto-generated
background {c['mSurface']}
foreground {c['mOnSurface']}
selection_background {c['mPrimary']}
color4  {c['mPrimary']}
"""
        KITTY_COLORS.write_text(content)
        subprocess.run(['kitty', '@', 'set-colors', '-a', str(KITTY_COLORS)], capture_output=True)
        print('✅ kitty')
    except Exception as e:
        print(f'❌ kitty: {e}')

def apply_niri(c):
    try:
        text = NIRI_CONFIG.read_text()
        text = re.sub(r'active-color\s+"[^"]*"', f'active-color "{c["mPrimary"]}"', text)
        NIRI_CONFIG.write_text(text)
        subprocess.run(['niri', 'msg', 'action', 'reload-config'], capture_output=True)
        print('✅ niri')
    except Exception as e:
        print(f'❌ niri: {e}')

def apply_clock(c):
    try:
        if CLOCK_SCRIPT.exists():
            text = CLOCK_SCRIPT.read_text()
            text = re.sub(r'CLOCK_COLOR_HEX\s*=\s*"#[^"]*"', f'CLOCK_COLOR_HEX = "{c["mPrimary"]}"', text)
            if 'strftime' in text:
                text = re.sub(r'strftime\("%Y-%m-%d"\)', 'strftime("%a, %b %d").capitalize()', text)
            CLOCK_SCRIPT.write_text(text)
            print('✅ clock')
    except Exception as e:
        print(f'❌ clock: {e}')

def main():
    if not NOCTALIA_COLORS.exists():
        print('❌ Файл цветов Noctalia не найден')
        return
    c = load_colors()
    # Rofi теперь красится через wallust автоматически, тут не нужен
    apply_kitty(c)
    apply_niri(c)
    apply_clock(c)
    print('🎨 Тема обновлена!')

if __name__ == '__main__':
    main()
