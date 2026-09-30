#!/bin/bash
# UX thingy

m=$(uname -m)
case "$m" in
    *arm*|*aarch64*) is_arm=1 ;;
    *)               is_arm=0 ;;
esac

d=$(pwd)
f="$d/vcs"
b="/data/data/com.termux/files/usr/bin/vcs"
bx="/usr/local/bin/vcs"

if [ "$1" = "-r" ]; then
    if [ $is_arm -eq 1 ]; then
        rm -f "$b"
    else
        rm -f "$b" "$bx"
        sudo rm -f "$bx" 2>/dev/null
    fi
    echo "removed device=$is_arm"
    exit 0
fi

git_root=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -n "$git_root" ]; then
    for rel_file in $(git -C "$git_root" ls-files 2>/dev/null); do
        abs_file="$git_root/$rel_file"
        if [ ! -f "$abs_file" ]; then
            echo -e "\033[1m$rel_file\033[0m missing"
            echo -e "\033[1mrestoring $rel_file\033[0m using git."
            git -C "$git_root" checkout HEAD -- "$rel_file" >/dev/null 2>&1 && echo "$rel_file restored" || { echo "$rel_file missing"; exit 1; }
        fi
    done
fi

[ ! -f "$f" ] && { echo "there's no file named vcs here"; exit 1; }
chmod +x "$f"

if [ $is_arm -eq 1 ]; then
    [ ! -d "/data/data/com.termux/files/usr/bin" ] && { echo "not termux eh?"; exit 1; }
    rm -f "$b"
    ln -s "$f" "$b"
else
    rm -f "$b" "$bx"
    if [ -d "/data/data/com.termux/files/usr/bin" ]; then
        ln -s "$f" "$b"
    else
        ln -s "$f" "$bx" 2>/dev/null || sudo ln -s "$f" "$bx"
    fi
fi

echo -e "\033[1minstalled\033[0m arch=$m arm=$is_arm"