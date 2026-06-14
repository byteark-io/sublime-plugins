"""
AutoFile plugin for Sublime Text

Automatically assigns a filename to new (untitled) buffers and saves them to a
configurable working folder, so unsaved tabs are never lost.

Naming pattern tokens:
    %Y %y %m %d %H %M %S   (date/time, like strftime)
    #                       (sequence counter; ### = 001, #### = 0001)

Commands (Command Palette):
    AutoFile: New Auto-Named File
    AutoFile: Toggle Auto-Create on New File
    AutoFile: Open Settings

Settings file: AutoFile.sublime-settings
"""

import sublime
import sublime_plugin
import os
import re
import datetime

SETTINGS_FILE = "AutoFile.sublime-settings"


def _settings():
    return sublime.load_settings(SETTINGS_FILE)


def _next_sequence(folder, prefix, suffix, digits):
    """Find the next available counter value for files matching prefix*suffix."""
    mx = 0
    try:
        for fname in os.listdir(folder):
            if fname.startswith(prefix) and fname.endswith(suffix):
                mid = fname[len(prefix):len(fname) - len(suffix)] if suffix else fname[len(prefix):]
                # strip leading digits
                m = re.match(r"(\d+)", mid)
                if m:
                    mx = max(mx, int(m.group(1)))
    except (FileNotFoundError, OSError):
        pass
    return mx + 1


def expand_pattern(pattern, ext, folder):
    """Expand a naming pattern into a full filename (without folder)."""
    now = datetime.datetime.now()
    repl = {
        "%Y": now.strftime("%Y"),
        "%y": now.strftime("%y"),
        "%m": now.strftime("%m"),
        "%d": now.strftime("%d"),
        "%H": now.strftime("%H"),
        "%M": now.strftime("%M"),
        "%S": now.strftime("%S"),
    }
    name = pattern
    for k, v in repl.items():
        name = name.replace(k, v)

    m = re.search(r"#+", name)
    if m:
        digits = len(m.group(0))
        prefix = name[:m.start()]
        suffix = name[m.end():]
        seq = _next_sequence(folder, prefix, suffix + ext, digits)
        name = prefix + str(seq).zfill(digits) + suffix

    return name + ext


def _make_path():
    s = _settings()
    folder = s.get("working_folder", "")
    if not folder:
        # default: <home>/AutoFile
        folder = os.path.join(os.path.expanduser("~"), "AutoFile")
    pattern = s.get("pattern", "note-%Y-%m-%d-###")
    ext = s.get("extension", ".txt")
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        return None
    return os.path.join(folder, expand_pattern(pattern, ext, folder))


def _auto_name_view(view):
    """Assign a generated file path to an unsaved view and save it."""
    if view is None:
        return
    if view.file_name():
        return  # already has a real file
    if view.settings().get("autofile_assigned"):
        return  # avoid recursion
    path = _make_path()
    if not path:
        return
    try:
        # create the file on disk (empty) so the name is reserved
        if not os.path.exists(path):
            open(path, "a", encoding="utf-8").close()
    except OSError as e:
        sublime.status_message("AutoFile: cannot create file: %s" % e)
        return
    view.settings().set("autofile_assigned", True)
    view.retarget(path)
    view.run_command("save")
    sublime.status_message("AutoFile: %s" % path)


class AutoFileListener(sublime_plugin.EventListener):
    def on_new_async(self, view):
        s = _settings()
        if not s.get("auto_create_on_new", True):
            return
        # slight delay to let the view settle
        sublime.set_timeout(lambda: _auto_name_view(view), 50)


class AutofileNewCommand(sublime_plugin.WindowCommand):
    """Manually create a new auto-named file."""
    def run(self):
        view = self.window.new_file()
        sublime.set_timeout(lambda: _auto_name_view(view), 50)


class AutofileToggleCommand(sublime_plugin.WindowCommand):
    """Toggle auto-create-on-new behaviour."""
    def run(self):
        s = _settings()
        cur = s.get("auto_create_on_new", True)
        s.set("auto_create_on_new", not cur)
        sublime.save_settings(SETTINGS_FILE)
        sublime.status_message("AutoFile auto-create: %s" % ("ON" if not cur else "OFF"))


class AutofileOpenSettingsCommand(sublime_plugin.WindowCommand):
    """Open the AutoFile settings file."""
    def run(self):
        self.window.run_command("open_file", {
            "file": "${packages}/User/" + SETTINGS_FILE
        })
