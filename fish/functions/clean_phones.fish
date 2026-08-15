function clean_phones
    echo "=== Проверка подключения через ADB ==="
    if not adb devices | grep -q -E "device\$"
        echo "Ошибка: Телефон не подключен или не включена отладка по USB!"
        return 1
    end

    echo "=== 1. Пакетная очистка системного кэша ==="
    adb shell pm trim-caches 40G

    echo "=== 2. Очистка тяжелого кэша приложений ==="
    adb shell "rm -rf /sdcard/Android/data/com.instagram.android/cache/*"
    adb shell pm clear-cache org.telegram.messenger
    adb shell pm clear-cache md.obsidian

    echo "=== 3. Запуск фоновой компиляции и оптимизации системы ==="
    adb shell cmd package bg-dexopt-job

    echo "=== Финал: Проверка свободного места ==="
    adb shell df -h /data
    echo "=== Очистка успешно завершена! ==="
end
