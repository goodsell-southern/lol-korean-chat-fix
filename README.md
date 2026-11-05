# LoL macOS 인게임 채팅 한글 깨짐 수정 (Karabiner-Elements)

macOS에서 리그 오브 레전드 인게임 채팅에 한글을 입력하다가 숫자나 특수기호를 누르면, 조합 중이던 글자가 지워지는 문제를 입력기 변경 없이 해결하는 Karabiner-Elements 규칙.

## 증상

- 한글 조합 중(예: `가`)에 숫자·특수기호를 입력하면 조합 중이던 글자가 사라짐.
- 스페이스, Enter, Caps Lock 한/영 전환으로 조합을 끝내면 정상.
- 롤 게임 클라이언트(`com.riotgames.LeagueofLegends.GameClient`)에서만 발생.

## 환경

| 항목 | 값 |
|---|---|
| macOS | 27.0.1 |
| 입력기 | macOS 기본 한글 2벌식 (`com.apple.inputmethod.Korean.2SetKorean`) |
| Karabiner-Elements | 16.3.0 |

## 원인

롤 게임 클라이언트는 "조합 중에 숫자·기호가 들어오는" 입력기 처리 경로를 잘못 다뤄서 조합 중인 글자를 버린다. 반면 스페이스로 조합을 확정하는 경로는 제대로 처리한다.

따라서 숫자·기호 앞에서 스페이스로 조합을 먼저 확정하면 문제를 피할 수 있다.

## 해결 방법

롤 게임 클라이언트에서 채팅창이 열려 있고 입력 소스가 한글일 때만, 숫자·기호 키를 다음 순서로 바꾼다.

```
스페이스 → 백스페이스 → 원래 키
```

1. 스페이스: 조합 중인 글자를 확정한다.
2. 백스페이스: 방금 입력된 공백을 지운다.
3. 원래 숫자·기호를 입력한다.

- 대상 키: `1`–`0`, `` ` - = [ ] \ ; ' , . / ``
- Shift 조합 기호(`! @ # ? :` 등)도 포함. Shift는 스페이스·백스페이스를 보낼 때는 떼고, 기호를 입력할 때만 다시 누른다.
- 롤 로비 클라이언트와 다른 앱에는 적용되지 않는다.

### 채팅창 상태 추적

채팅창이 닫혀 있을 때 숫자 키는 아이템 단축키다. 이때 스페이스가 함께 입력되면 롤 기본 설정의 "챔피언으로 카메라 이동"이 실행되어 화면이 튄다. 그래서 채팅창이 열려 있을 때만 규칙이 동작해야 한다.

Karabiner는 게임 화면 상태를 알 수 없으므로, 키 입력으로 채팅창 상태를 추정해 `lol_chat_open` 변수에 기록한다.

| 키 | 동작 |
|---|---|
| 인게임 Enter / Shift+Enter | 채팅창 열림 ↔ 닫힘 전환 |
| 인게임 Esc | 닫힘으로 초기화 |
| 로비 클라이언트에서 Enter | 닫힘으로 초기화 (게임이 끝난 뒤 남은 상태 정리) |

## 설치

1. 규칙 파일을 Karabiner 에셋 폴더에 복사한다.

   ```sh
   mkdir -p ~/.config/karabiner/assets/complex_modifications
   cp karabiner/lol-korean-chat.json ~/.config/karabiner/assets/complex_modifications/
   ```

2. Karabiner-Elements Settings → Complex Modifications → Add predefined rule로 이동한다.
3. `LoL in-game Hangul chat fix` 항목에서 Enable을 누른다.

## 제한 사항

채팅창 상태는 추정값이라 실제와 어긋날 수 있다. Enter·Esc 없이 채팅창이 열리거나 닫히면 어긋난다. 예: 메시지를 보내기 전에 게임이 끝난 경우.

- 어긋나서 아이템 키를 누를 때 화면이 튀면, 채팅창이 닫힌 상태에서 Esc를 두 번 누른다. 첫 번째 Esc로 상태가 초기화되고 게임 메뉴가 열리며, 두 번째 Esc로 메뉴가 닫힌다.
- 게임 중에 영문 입력으로 두면 상태와 관계없이 규칙이 동작하지 않는다.

## 시도했지만 실패한 방법

| 방법 | 결과 |
|---|---|
| `select_input_source`로 ABC 전환 → 키 → 2벌식으로 복귀 | 글자는 남지만 순서가 뒤바뀜 (`가1` → `1가`, `가!!!` → `!!!가`). Karabiner의 입력 소스 전환은 키 입력과 별개로 비동기로 처리되어, 롤에서 조합 확정이 제때 일어나지 않는다. 대기 시간을 늘려도 해결되지 않는다. |
| 오른쪽 화살표 / F18 / Caps Lock을 확정 트리거로 사용 | 스페이스+백스페이스 방식보다 결과가 나빴음 |
| 채팅창 상태와 관계없이 스페이스+백스페이스 적용 | 채팅창이 닫혀 있을 때 아이템 키를 누르면 화면이 챔피언으로 튐 |

## 규칙 수정

키 목록이나 동작을 바꾸려면 `scripts/generate.py`를 수정한 뒤 다시 생성한다.

```sh
python3 scripts/generate.py > karabiner/lol-korean-chat.json
```

## 제거

Karabiner-Elements Settings → Complex Modifications에서 해당 규칙을 Remove한다.
