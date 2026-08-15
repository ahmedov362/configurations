function synccolors --description "Синк цветов с текущими обоями Noctalia"
    # Пробуем разные возможные пути в settings.json
    set wallpaper (jq -r ".wallpaper.currentWallpapers // .wallpaper.currentWallpaper // .currentWallpaper // empty | if type == \"object\" then to_entries[0].value else . end" ~/.config/noctalia/settings.json 2>/dev/null)
    
    if test -z "$wallpaper"
        echo "❌ Не нашёл текущие обои. Проверь структуру:"
        jq "." ~/.config/noctalia/settings.json | grep -i wallpaper | head -5
        return 1
    end
    
    if not test -f "$wallpaper"
        echo "❌ Файл обоев не существует: $wallpaper"
        return 1
    end
    
    wallust run "$wallpaper"
    echo "🎨 Синхронизировано с: $wallpaper"
end
