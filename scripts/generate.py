#!/usr/bin/env python3
"""Generate the Karabiner-Elements complex modification for LoL in-game Hangul chat.

Usage: python3 scripts/generate.py > karabiner/lol-korean-chat.json
"""
import json

GAME_CLIENT = "^com\\.riotgames\\.LeagueofLegends\\.GameClient$"

# Digits and symbol keys that break Hangul composition in the LoL game client.
KEYS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "grave_accent_and_tilde", "hyphen", "equal_sign", "open_bracket", "close_bracket", "backslash",
    "semicolon", "quote", "comma", "period", "slash",
]

CONDITIONS = [
    {"type": "frontmost_application_if", "bundle_identifiers": [GAME_CLIENT]},
    {"type": "input_source_if", "input_sources": [{"language": "^ko$"}]},
]

# Space commits the composing syllable correctly in LoL; backspace removes the space.
COMMIT = [{"key_code": "spacebar"}, {"key_code": "delete_or_backspace"}]


def manipulators():
    for key in KEYS:
        # Shift is mandatory here so it is released while space/backspace are sent,
        # then re-applied only to the symbol key.
        yield {
            "type": "basic",
            "conditions": CONDITIONS,
            "from": {"key_code": key, "modifiers": {"mandatory": ["shift"], "optional": ["caps_lock"]}},
            "to": COMMIT + [{"key_code": key, "modifiers": ["left_shift"]}],
        }
        yield {
            "type": "basic",
            "conditions": CONDITIONS,
            "from": {"key_code": key, "modifiers": {"optional": ["caps_lock"]}},
            "to": COMMIT + [{"key_code": key}],
        }


def main():
    print(json.dumps({
        "title": "LoL in-game Hangul chat fix",
        "rules": [{
            "description": "LoL in-game chat: commit Hangul composition before digits/symbols (space, backspace, key)",
            "manipulators": list(manipulators()),
        }],
    }, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
