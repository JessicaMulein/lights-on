#!/usr/bin/env python3
"""Build one readable libretto from Script/ and Songs/.

Run from this folder:  python3 build_libretto.py
Writes:  I Left the Lights On - Libretto.md
Includes LICENSE.md, if present: a pointer at the top and the full text at the end.
Also ends with a Song registrations table from ASCAP-WORKS.md, if present.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "I Left the Lights On - Libretto.md"
LICENSE = ROOT / "LICENSE.md"
WORKS = ROOT / "ASCAP-WORKS.md"
CUE = re.compile(r"^\{\{song:\s*(.+?)\s*\}\}\s*$")
LYRICS = re.compile(r"<!-- lyrics -->(.*?)<!-- /lyrics -->", re.S)
STATUS = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.M)


def license_text():
    """LICENSE.md without its title line, with line breaks kept and the URL linked. Empty if there's no license."""
    if not LICENSE.exists():
        return ""
    lines = LICENSE.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = re.sub(r"(https?://\S+)", r"<\1>", "\n".join(lines).strip())
    return hard_breaks(text)


def registry_rows():
    """(number, title, ASCAP work ID) from ASCAP-WORKS.md. Empty if the file is missing."""
    if not WORKS.exists():
        return []
    rows = []
    for line in WORKS.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 3 and re.fullmatch(r"\d\d", c[0]) and re.fullmatch(r"\d{9}", c[2]):
            rows.append(("P" if c[0] == "00" else str(int(c[0])), c[1], c[2]))
    return rows


def registry_block():
    """Markdown for the Song registrations section, or empty if there is nothing to list."""
    rows = registry_rows()
    if not rows:
        return ""
    out = ["## Song registrations", "",
           "Every number is registered with ASCAP (Mulein Studios). Theaters can use these work IDs for performance reports and cue sheets.",
           "", "| # | Song | ASCAP work ID |", "|:--|:-----|:--------------|"]
    out += [f"| {n} | {t} | {i} |" for n, t, i in rows]
    return "\n".join(out)


def song_files():
    # Skips iCloud/Finder duplicate copies such as "11 - Leah and the Boys 2.md".
    return {p.stem: p for p in sorted((ROOT / "Songs").rglob("*.md")) if not re.search(r" \d+$", p.stem)}


def hard_breaks(block):
    """Markdown joins single lines; add two trailing spaces so lyric lines stay separate."""
    out = []
    for line in block.splitlines():
        s = line.rstrip()
        out.append(s + "  " if s else "")
    return "\n".join(out)


def song_block(path):
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("#").strip()
    status = STATUS.search(text)
    status = status.group(1) if status else "unknown"
    m = LYRICS.search(text)
    body = m.group(1).strip() if m else ""
    return title, status, body


def main():
    songs = song_files()
    parts = [
        "# I Left the Lights On",
        "",
        "*Assembled libretto. Don't edit this file: edit Script/ and Songs/, then run build_libretto.py.*",
        "",
    ]
    license = license_text()
    if license:
        parts += ["*License and “About this story”: see the end of this file.*", ""]
    missing, written, pending = [], 0, 0
    for act in ("Act One", "Act Two"):
        script = ROOT / "Script" / f"{act}.md"
        if not script.exists():
            continue
        if act != "Act One":
            parts += ["", "---", ""]
        for line in script.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                continue
            m = CUE.match(line)
            if not m:
                parts.append(line)
                continue
            stem = m.group(1)
            path = songs.get(stem)
            if path is None:
                missing.append(stem)
                parts.append(f"> **[No song file named \"{stem}\"]**")
                continue
            title, status, body = song_block(path)
            parts += [f"#### ♪ {title}", ""]
            if status.lower().startswith("stage draft"):
                written += 1
                parts += [hard_breaks(body), ""]
            else:
                pending += 1
                parts += [f"> *[{status}]*", ""]
    if license:
        parts += ["", "---", "", "## License", "", re.sub(r"^## ", "### ", license, flags=re.M)]
    reg = registry_block()
    if reg:
        parts += ["", "---", "", reg]
    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}: {written} songs drafted, {pending} still to write.")
    if missing:
        print("Cues with no song file:", ", ".join(missing))


if __name__ == "__main__":
    main()
