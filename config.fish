if status is-interactive
    # Отключаем приветствие Fish
    set fish_greeting

    # Скрываем вывод ошибок батареи (для Starship/Waybar)
    set -g theme_display_battery no

end
function set_wall
    awww img $argv
    wallust run $argv
end

function wt
    python ~/Projects/weather/weather.py
end
function clock
    python ~/Projects/datatime/main.py
end
# Твои алиасы (из скринов)
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gpl='git pull'
alias lg='lazygit'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias install='sudo pacman -S'
alias myip='curl ifconfig.me'
alias pinggoogle='ping -c 5 8.8.8.8'
alias fetch='fastfetch'
alias py='python3'
alias pyversion='python3 --version'
alias cls='clear'
alias usage='du -sh * | sort -h'
alias space='df -h'
alias cava='cava'
alias ef='nvim ~/.config/fish/config.fish'
alias sf='source ~/.config/fish/config.fish'
alias projects='cd ~/Projects/'
alias lessons='cd ~/Projects/lessons'
alias aliases='fish ~/Projects/lessons/main.fish '
alias sfish='source ~/.config/fish/config.fish'
alias clr=clear
alias ls=lsd
alias lsend="/home/akmedovshamil/Downloads/LocalSend-*.AppImage --enable-features=UseOzonePlatform --ozone-platform=wayland"
function fastfetch_smart
    if test $COLUMNS -lt 110
        # Если окно узкое — подгружаем конфиг с маленьким логотипом
        fastfetch -c ~/.config/fastfetch/small.jsonc
    else
        # Если окно широкое — подгружаем конфиг с большим логотипом
        fastfetch -c ~/.config/fastfetch/big.jsonc
    end
end

# Создаем быстрый алиас, чтобы при вводе команды "fastfetch" работал наш умный скрипт
alias ff=fastfetch_smart
fastfetch_smart

