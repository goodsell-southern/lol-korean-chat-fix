#!/usr/bin/env python3
"""Generate the Karabiner-Elements complex modification for LoL in-game Hangul chat.

Usage: python3 scripts/generate.py > karabiner/lol-korean-chat.json
"""
import json

GAME_CLIENT = "^com\\.riotgames\\.LeagueofLegends\\.GameClient$"
LOBBY_CLIENT = "^com\\.riotgames\\.LeagueofLegends\\.LeagueClient(Ux)?$"

# Tracks whether the in-game chat box is open. Karabiner cannot see LoL's UI state,
# so it is toggled by Enter (open/send) and cleared by Escape (cancel).
CHAT_VAR = "lol_chat_open"

# Digits and symbol keys that break Hangul composition in the LoL game client.
KEYS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "grave_accent_and_tilde", "hyphen", "equal_sign", "open_bracket", "close_bracket", "backslash",
    "semicolon", "quote", "comma", "period", "slash",
]

ENTER_KEYS = ["return_or_enter", "keypad_enter"]

IN_GAME = {"type": "frontmost_application_if", "bundle_identifiers": [GAME_CLIENT]}
IN_LOBBY = {"type": "frontmost_application_if", "bundle_identifiers": [LOBBY_CLIENT]}
CHAT_OPEN = {"type": "variable_if", "name": CHAT_VAR, "value": 1}

# Only while chatting: outside chat, digits are item hotkeys and space would snap the camera.
CONDITIONS = [
    IN_GAME,
    CHAT_OPEN,
    {"type": "input_source_if", "input_sources": [{"language": "^ko$"}]},
]

# Space commits the composing syllable correctly in LoL; backspace removes the space.
COMMIT = [{"key_code": "spacebar"}, {"key_code": "delete_or_backspace"}]


def set_chat(value):
    return {"set_variable": {"name": CHAT_VAR, "value": value}}


def chat_state_manipulators():
    for key in ENTER_KEYS:
        # Shift+Enter opens all chat, so shift stays optional and is passed through.
        frm = {"key_code": key, "modifiers": {"optional": ["shift", "caps_lock"]}}
        # Enter while open sends (or closes an empty) message.
        yield {"type": "basic", "conditions": [IN_GAME, CHAT_OPEN], "from": frm,
               "to": [set_chat(0), {"key_code": key}]}
        yield {"type": "basic", "conditions": [IN_GAME], "from": frm,
               "to": [set_chat(1), {"key_code": key}]}
        # Back in the lobby means the game ended; clear state left from an unsent message.
        yield {"type": "basic", "conditions": [IN_LOBBY], "from": frm,
               "to": [set_chat(0), {"key_code": key}]}
    yield {
        "type": "basic",
        "conditions": [IN_GAME],
        "from": {"key_code": "escape", "modifiers": {"optional": ["any"]}},
        "to": [set_chat(0), {"key_code": "escape"}],
    }


def commit_manipulators():
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
            "description": "LoL in-game chat: commit Hangul composition before digits/symbols (space, backspace, key) while chat is open",
            "manipulators": list(chat_state_manipulators()) + list(commit_manipulators()),
        }],
    }, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
