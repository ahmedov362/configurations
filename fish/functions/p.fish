function p
    set projects_dir ~/Projects
    set projects (command find $projects_dir -maxdepth 1 -mindepth 1 -type d | sort)

    if test (count $projects) -eq 0
        echo "Проектов нет!"
        return 1
    end

    echo "─────────────────────────────"
    echo "  📁 Проекты"
    echo "─────────────────────────────"

    set i 1
    for proj in $projects
        set name (basename $proj)
        echo "  [$i] $name"
        set i (math $i + 1)
    end

    echo "─────────────────────────────"
    read -P "  Номер: " choice

    if test -n "$choice" -a "$choice" -ge 1 -a "$choice" -le (count $projects) 2>/dev/null
        set selected $projects[$choice]
        cd $selected
        echo "  → "(basename $selected)
    else
        echo "  Неверный номер!"
    end
end
