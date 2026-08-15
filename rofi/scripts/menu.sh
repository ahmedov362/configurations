#!/usr/bin/env bash
# Главное меню: калькулятор, YouTube, Google, Wikipedia

choice=$(printf "🧮 Калькулятор\n📺 YouTube\n🔍 Google\n📚 Wikipedia" | \
    rofi -dmenu -i -p "Выбери действие")

case "$choice" in
    "🧮 Калькулятор")
        python3 ~/.config/rofi/scripts/calc.py
        ;;
    "📺 YouTube")
        query=$(rofi -dmenu -p "YouTube")
        [ -z "$query" ] && exit 0
        encoded=$(echo -n "$query" | jq -sRr @uri)
        xdg-open "https://www.youtube.com/results?search_query=$encoded"
        ;;
    "🔍 Google")
        query=$(rofi -dmenu -p "Google")
        [ -z "$query" ] && exit 0
        encoded=$(echo -n "$query" | jq -sRr @uri)
        xdg-open "https://www.google.com/search?q=$encoded"
        ;;
    "📚 Wikipedia")
        python3 ~/.config/rofi/scripts/wiki.py
        ;;
esac
