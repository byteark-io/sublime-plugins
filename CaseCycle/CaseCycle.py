"""
CaseCycle plugin for Sublime Text

Press the hotkey repeatedly to cycle the selected text through:
    UPPERCASE -> lowercase -> lowerCamelCase -> UpperCamelCase -> original

The original text is remembered, so camelCase conversions are not lossy across
the cycle. If you change the selection, the cycle restarts from that text.

Default hotkey: Ctrl+Shift+M  (see Default (Windows).sublime-keymap)
Command: cycle_case
"""

import sublime
import sublime_plugin
import re

CYCLE = ["upper", "lower", "lower_camel", "upper_camel", "original"]

# Per-view state: { view_id: {"regions": [(a,b),...], "originals": [...], "index": n} }
_state = {}


def split_words(s):
    """Split a string into words across spaces, _ , - and camelCase boundaries."""
    s2 = re.sub(r"[_\-\s]+", " ", s)
    # boundary: lower/digit followed by Upper  (helloWorld -> hello World)
    s2 = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", s2)
    # boundary: Upper run followed by Upper+lower (HTMLParser -> HTML Parser)
    s2 = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", s2)
    return [w for w in s2.split() if w]


def _cap(word):
    return word[:1].upper() + word[1:].lower() if word else word


def _camel_line(line, lower_first):
    words = split_words(line)
    if not words:
        return line
    if lower_first:
        return words[0].lower() + "".join(_cap(w) for w in words[1:])
    return "".join(_cap(w) for w in words)


def _apply_per_line(text, fn):
    """Apply fn to each line's content while keeping the original line breaks."""
    parts = re.split(r"(\r\n|\r|\n)", text)
    out = []
    for i, p in enumerate(parts):
        out.append(p if (i % 2) else fn(p))
    return "".join(out)


def transform(text, style):
    if style == "original":
        return text
    if style == "upper":
        return text.upper()
    if style == "lower":
        return text.lower()
    if style == "lower_camel":
        return _apply_per_line(text, lambda ln: _camel_line(ln, True))
    if style == "upper_camel":
        return _apply_per_line(text, lambda ln: _camel_line(ln, False))
    return text


class CycleCaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        vid = view.id()

        # Build working regions (expand empty selections to the word under caret)
        regions = []
        for r in view.sel():
            if r.empty():
                regions.append(view.word(r))
            else:
                regions.append(sublime.Region(r.begin(), r.end()))
        if not regions:
            return

        # Sort by position for stable multi-selection handling
        regions.sort(key=lambda r: r.begin())
        cur = [(r.begin(), r.end()) for r in regions]

        st = _state.get(vid)
        if st and st["regions"] == cur:
            originals = st["originals"]
            index = st["index"]
        else:
            originals = [view.substr(sublime.Region(a, b)) for (a, b) in cur]
            index = 0

        style = CYCLE[index % len(CYCLE)]
        new_texts = [transform(originals[i], style) for i in range(len(cur))]

        # Replace from last region to first so earlier offsets stay valid
        for i in range(len(cur) - 1, -1, -1):
            a, b = cur[i]
            view.replace(edit, sublime.Region(a, b), new_texts[i])

        # Recompute resulting regions left-to-right with a cumulative delta
        new_regions = []
        delta = 0
        for i in range(len(cur)):
            a, b = cur[i]
            na = a + delta
            nb = na + len(new_texts[i])
            new_regions.append((na, nb))
            delta += len(new_texts[i]) - (b - a)

        # Update the selection to cover the transformed text
        view.sel().clear()
        for (na, nb) in new_regions:
            view.sel().add(sublime.Region(na, nb))

        _state[vid] = {"regions": new_regions, "originals": originals, "index": index + 1}
        sublime.status_message("Case: " + style)
