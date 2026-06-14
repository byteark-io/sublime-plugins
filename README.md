# Sublime Text Plugins

Custom plugins for [Sublime Text](https://www.sublimetext.com/).  
Cross-platform: works on Windows, macOS, and Linux.

## AutoFile

Automatically gives new (untitled) buffers a real filename and saves them to a
configurable working folder. Every new tab immediately becomes a real, named file
in your working folder, so you can just keep typing and hit save without ever
being prompted for a filename.

### Features
- Auto-names and saves every new tab into a working folder
- Configurable naming pattern, folder, and extension
- Manual command + toggle via the Command Palette

### Naming pattern tokens
| Token | Meaning            | Example |
|-------|--------------------|---------|
| `%Y`  | Year (4-digit)     | 2026    |
| `%y`  | Year (2-digit)     | 26      |
| `%m`  | Month              | 06      |
| `%d`  | Day                | 14      |
| `%H`  | Hour (24h)         | 08      |
| `%M`  | Minute             | 15      |
| `%S`  | Second             | 30      |
| `#`   | Sequence counter   | `###` → 001 |

Default pattern: `note-%Y-%m-%d-###` → `note-2026-06-14-001.txt`

### Installation

Copy the `AutoFile/` folder into your Sublime Text **Packages** directory:

| Platform | Path |
|----------|------|
| macOS    | `~/Library/Application Support/Sublime Text/Packages/AutoFile/` |
| Windows  | `%APPDATA%\Sublime Text\Packages\AutoFile\` |
| Linux    | `~/.config/sublime-text/Packages/AutoFile/` |

**macOS (terminal):**
```bash
cp -R AutoFile/ ~/Library/Application\ Support/Sublime\ Text/Packages/AutoFile/
```

**Windows (cmd):**
```cmd
xcopy /E /I AutoFile "%APPDATA%\Sublime Text\Packages\AutoFile"
```

Files installed:
- `AutoFile.py`
- `AutoFile.sublime-settings`
- `AutoFile.sublime-commands`

### Settings
Command Palette → **AutoFile: Open Settings**

```json
{
    "auto_create_on_new": true,
    "working_folder": "",
    "pattern": "note-%Y-%m-%d-###",
    "extension": ".txt"
}
```
Leave `working_folder` empty to use `~/AutoFile` (macOS/Linux) or `%USERPROFILE%\AutoFile` (Windows).

### Commands (Command Palette)
- **AutoFile: New Auto-Named File**
- **AutoFile: Toggle Auto-Create on New File**
- **AutoFile: Open Settings**

## CaseCycle

Cycle the selected text through case styles with a single hotkey:

`UPPERCASE` → `lowercase` → `Title Case` → `Sentence case` → `lowerCamelCase` → `UpperCamelCase` → `original`

The original text is remembered, so repeated presses always return to the exact
original. Works with multiple selections. With an empty selection it uses the word
under the caret.

### Hotkey

| Platform | Key |
|----------|-----|
| macOS    | `⌘+Shift+M` |
| Windows  | `Ctrl+Shift+M` |

### Installation

Copy the `CaseCycle/` folder into your Sublime Text **Packages** directory:

| Platform | Path |
|----------|------|
| macOS    | `~/Library/Application Support/Sublime Text/Packages/CaseCycle/` |
| Windows  | `%APPDATA%\Sublime Text\Packages\CaseCycle\` |
| Linux    | `~/.config/sublime-text/Packages/CaseCycle/` |

**macOS (terminal):**
```bash
cp -R CaseCycle/ ~/Library/Application\ Support/Sublime\ Text/Packages/CaseCycle/
```

**Windows (cmd):**
```cmd
xcopy /E /I CaseCycle "%APPDATA%\Sublime Text\Packages\CaseCycle"
```

### Command Palette
- **Case: Cycle (UPPER / lower / Title / Sentence / camelCase / PascalCase / original)**
