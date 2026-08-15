#!/usr/bin/env python3
"""Поиск по Wikipedia через MediaWiki API + rofi UI"""
import subprocess
import sys
import re
import urllib.parse

try:
    import requests
except ImportError:
    subprocess.run(["notify-send", "Wiki", "pip install requests"])
    sys.exit(1)


def rofi(prompt, options=None, lines=10):
    args = ["rofi", "-dmenu", "-i", "-p", prompt, "-lines", str(lines)]
    input_data = "\n".join(options) if options else ""
    result = subprocess.run(args, input=input_data, capture_output=True, text=True)
    return result.stdout.strip()


def notify(title, message):
    subprocess.run(["notify-send", title, message[:300]])


def clean_text(text):
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\([^)]*МФА[^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" .", ".")
    return text.strip()


def detect_lang(text):
    if any("а" <= c.lower() <= "я" or c == "ё" for c in text):
        return "ru"
    return "en"


def wiki_search(query, lang="ru", limit=8):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    }
    r = requests.get(url, params=params, timeout=10,
                     headers={"User-Agent": "SynByte-Rofi-Wiki/1.0"})
    r.raise_for_status()
    data = r.json()
    return [item["title"] for item in data.get("query", {}).get("search", [])]


def wiki_summary(title, lang="ru", sentences=5):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": title,
        "format": "json",
    }
    r = requests.get(url, params=params, timeout=10,
                     headers={"User-Agent": "SynByte-Rofi-Wiki/1.0"})
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            return None
        extract = page.get("extract", "")
        parts = re.split(r"(?<=[.!?])\s+", extract)
        return clean_text(" ".join(parts[:sentences]))
    return None


def wiki_url(title, lang="ru"):
    encoded = urllib.parse.quote(title.replace(" ", "_"))
    return f"https://{lang}.wikipedia.org/wiki/{encoded}"


def show_long_text(text, title):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > 70:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", title, "-lines", "15", "-width", "70"],
        input="\n".join(lines), text=True
    )


def main():
    query = rofi("Wikipedia")
    if not query:
        return
    lang = "ru"
    try:
        results = wiki_search(query, lang=lang)
    except requests.RequestException as e:
        notify("Wiki: нет сети", str(e))
        return
    if not results:
        notify("Wiki", f"Ничего не найдено: {query}")
        return
    if len(results) > 1:
        title = rofi("Выбери статью", results, lines=len(results))
    else:
        title = results[0]
    if not title:
        return
    try:
        summary = wiki_summary(title, lang=lang)
    except requests.RequestException as e:
        notify("Wiki: ошибка", str(e))
        return
    if not summary:
        notify("Wiki", f"Пустая статья: {title}")
        return
    url = wiki_url(title, lang=lang)
    action = rofi(title, [
        "📖 Показать текст",
        "🌐 Открыть в браузере",
        "📋 Скопировать текст",
        "🔗 Скопировать ссылку",
    ], lines=4)
    if "Показать" in action:
        show_long_text(summary, title)
    elif "браузере" in action:
        subprocess.run(["xdg-open", url])
    elif "текст" in action:
        subprocess.run(["wl-copy"], input=summary, text=True)
        notify("Wiki ✅", "Текст скопирован")
    elif "ссылку" in action:
        subprocess.run(["wl-copy"], input=url, text=True)
        notify("Wiki ✅", f"Ссылка: {url}")


if __name__ == "__main__":
    main()
