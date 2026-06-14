# Sublime Text Plugins

Custom plugins for [Sublime Text](https://www.sublimetext.com/).

## AutoFile

Automatically gives new (untitled) buffers a real filename and saves them to a
configurable working folder. Sublime already keeps unsaved buffers in its session
cache, but those tabs still have no real file on disk — so saving one prompts you
for a name and location. AutoFile removes that friction: every new tab immediately
becomes a real, named file in your working folder, so you can just keep typing and
hit save (or rely on auto-save) without ever being prompted for a filename.

### Features
- Auto-names and saves every new tab (Ctrl+N) into a working folder
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
Copy the `AutoFile/` files into your Sublime Text **User** package folder:

- Standard install: `%APPDATA%\Sublime Text\Packages\User`
- Portable install: `<Sublime Text>\Data\Packages\User`

Files:
- `AutoFile.py`
- `AutoFile.sublime-settings`
- `AutoFile.sublime-commands`

### Settings
Command Palette (`Ctrl+Shift+P`) → **AutoFile: Open Settings**

```json
{
    "auto_create_on_new": true,
    "working_folder": "D:\\Work\\Scratch",
    "pattern": "note-%Y-%m-%d-###",
    "extension": ".txt"
}
```
Leave `working_folder` empty to use `<home>\AutoFile`.

### Commands (Command Palette)
- **AutoFile: New Auto-Named File**
- **AutoFile: Toggle Auto-Create on New File**
- **AutoFile: Open Settings**
