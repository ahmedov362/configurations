#!/bin/sh
TEXT=$(wl-paste --primary)
if [ ! -z "$TEXT" ]; then
    TRANSLATED=$(curl -s "https://googleapis.com(echo "$TEXT" | jq -sRr @uri)" | jq -r ".[0][0][0]")
    if [ "$TRANSLATED" != "null" ] && [ ! -z "$TRANSLATED" ]; then
        wl-copy --primary "$TRANSLATED"
        wl-copy "$TRANSLATED"
        wtype -M ctrl v
    fi
fi
