#!/usr/bin/env python3
"""Build the private website: the full libretto with a player at every song.

Run from this folder:  python3 build_site.py
Writes:  site/  (index.html, audio/, fonts/, libretto.pdf) ready to upload to Cloudflare Pages.
Needs:   Python's `markdown` package and ffprobe; the PDF step also needs pandoc and XeLaTeX.
"""
import datetime
from zoneinfo import ZoneInfo
import html
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import markdown

import build_libretto as bl

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
SRC = ROOT / "site_src"
TITLE = "I Left the Lights On"
AUTHOR = "Jessica Mulein"
REPO = ""  # once the repo is public, set to "https://github.com/JessicaMulein/lights-on" to link it

CAPS_NAME = r"[A-Z][A-Z0-9.'’\-]*(?: [A-Z0-9.'’\-]+)*"
NAMES = rf"{CAPS_NAME}(?:(?:, | and | & ){CAPS_NAME})*"
STRONG_NAME = re.compile(rf"<strong>({NAMES})</strong>")
LINE_NAME = re.compile(rf"(<p>|<br />\n)({NAMES}):\s")
SD_PARA = re.compile(r"<p><em>((?:(?!</em>|</?p>).)*)</em></p>", re.S)
LEAD_APOS = re.compile(r"(^|[\s(\"“—])'(?=(?:cause|cos|til|em|round|bout|neath|tis|twas|n)\b)", re.M | re.I)
CAPS_WORD = re.compile(r"(?<![\w’'])([A-Z][A-Z’'.\-]+(?: [A-Z][A-Z’'.\-]+)*)(?![\w’'])")


def name_case(s):
    return " ".join(w if w in ("and", "&") else w.capitalize() for w in s.split(" "))


def caps_to_smallcaps(fragment):
    """ALL-CAPS names inside stage directions -> small caps, outside of tags only."""
    parts = re.split(r"(<[^>]+>)", fragment)
    for i, p in enumerate(parts):
        if p.startswith("<"):
            continue
        parts[i] = CAPS_WORD.sub(lambda m: m.group(1) if len(m.group(1)) < 2 else f'<span class="cap">{m.group(1).lower()}</span>', p)
    return "".join(parts)


def md(text, lyric=False):
    text = LEAD_APOS.sub(lambda m: m.group(1) + "’", text)
    out = markdown.markdown(text, extensions=["smarty"], output_format="html")
    out = STRONG_NAME.sub(lambda m: f'<span class="who">{name_case(m.group(1))}</span>', out)
    out = LINE_NAME.sub(lambda m: f'{m.group(1)}<span class="who">{name_case(m.group(2))}</span> ', out)
    out = out.replace('<p><span class="who">', '<p class="line"><span class="who">') if not lyric else out
    out = SD_PARA.sub(lambda m: f'<p class="sd">{caps_to_smallcaps(m.group(1))}</p>', out)
    out = re.sub(r"<em>(\(.*?\))</em>", lambda m: f"<em>{caps_to_smallcaps(m.group(1))}</em>", out)
    return out


def song_key(stem):
    n = stem.split(" - ", 1)[0]
    return "P" if n == "P" else str(int(n))


def find_mp3s():
    found = {}
    for p in (ROOT / "Songs").rglob("*.mp3"):
        m = re.match(r"(\d+) - ", p.name)
        if m and not re.search(r" \d+$", p.stem):
            n = int(m.group(1))
            found["P" if n == 0 else str(n)] = p
    return found


def duration(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def fmt(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def place(src, dst):
    """Link (or copy) a file into the site, skipping it if it's already current."""
    if dst.exists():
        if os.path.samefile(src, dst):
            return
        if dst.stat().st_size == src.stat().st_size and dst.stat().st_mtime >= src.stat().st_mtime:
            return
        shutil.copyfile(src, dst)      # overwrite in place (deleting files isn't always allowed here)
        shutil.copystat(src, dst)
        return
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def build_body(mp3s):
    songs = bl.song_files()
    out, buf, windows = [], [], {"Act One": [], "Act Two": []}

    def flush():
        if buf:
            out.append(md("\n".join(buf)))
            buf.clear()

    for act in ("Act One", "Act Two"):
        text = (ROOT / "Script" / f"{act}.md").read_text(encoding="utf-8").replace(" ", " ")
        for line in text.splitlines():
            if line.startswith("# ") or line.startswith("*Book, draft") or line.strip() == "---":
                continue
            m = re.match(r"^## (Act \w+): (.+)$", line)
            if m:
                flush()
                if out:
                    out.append("</div></section>")
                aid = m.group(1).lower().replace(" ", "-")
                out.append(f'<section class="act" id="{aid}" aria-labelledby="{aid}-h">'
                           f'<div class="act-band"><h2 id="{aid}-h">{m.group(1)}<span>{html.escape(m.group(2))}</span></h2></div>'
                           f'<div class="script">')
                continue
            m = re.match(r"^### (.+)$", line)
            if m:
                flush()
                out.append(f'<h3 class="scene">{html.escape(m.group(1))}</h3>')
                continue
            if re.fullmatch(r"\*\*END OF (ACT ONE|PLAY)\*\*\s*", line):
                flush()
                words = line.strip("* \n").capitalize().replace("act one", "Act One")
                out.append(f'<p class="end">{words}</p>')
                continue
            cue = bl.CUE.match(line)
            if not cue:
                buf.append(line)
                continue
            flush()
            stem = cue.group(1)
            path = songs.get(stem)
            if path is None:
                continue
            title, status, lyric = bl.song_block(path)
            key = song_key(stem)
            label = "Prologue" if key == "P" else key
            windows[act].append((key, title))
            mp3 = mp3s.get(key)
            t = html.escape(title)
            head = (f'<section class="song" id="song-{key}" data-song="{key}" data-title="{t}"'
                    + (f' data-src="audio/{"00" if key == "P" else key.zfill(2)}.mp3"' if mp3 else "") + ">")
            out.append(head)
            out.append('<div class="song-head">')
            if mp3:
                d = duration(mp3)
                out.append(f'<button class="play" type="button" aria-label="Play {t}"></button>')
                out.append(f'<h4 class="song-title"><span class="n">{label}</span> {t}</h4>')
                out.append(f'<span class="time"><span class="cur">0:00</span> / {fmt(d)}</span></div>')
                out.append(f'<input class="seek" type="range" min="0" max="{int(d)}" step="1" value="0" aria-label="Position in {t}">')
            else:
                out.append(f'<h4 class="song-title"><span class="n">{label}</span> {t}</h4></div>')
            lyr = bl.hard_breaks(lyric) if status.lower().startswith("stage draft") else f"*[{status}]*"
            out.append(f'<div class="lyrics">{md(lyr, lyric=True)}</div></section>')
    flush()
    out.append("</div></section>")
    return "\n".join(out), windows


def house(windows):
    def floor(items, act, door=False):
        lis = []
        for i, (key, title) in enumerate(items):
            name = f"Prologue: {title}" if key == "P" else f"{key}. {title}"
            if door and i == len(items) // 2:
                lis.append('<li class="door" aria-hidden="true"></li>')
            lis.append(f'<li><a class="win" href="#song-{key}" data-song="{key}" data-label="{html.escape(name)}" '
                       f'aria-label="{html.escape(name)}"></a></li>')
        return f'<ol class="floor" aria-label="{act}">' + "".join(lis) + "</ol>"
    return ('<div class="house"><div class="roof" aria-hidden="true"></div>'
            + floor(windows["Act One"], "Act One") + floor(windows["Act Two"], "Act Two", door=True) + "</div>")


CSS = r"""
@font-face{font-family:"Spectral";font-weight:300;font-style:normal;font-display:swap;src:url(fonts/spectral-latin-300-normal.woff2) format("woff2")}
@font-face{font-family:"Spectral";font-weight:400;font-style:normal;font-display:swap;src:url(fonts/spectral-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Spectral";font-weight:400;font-style:italic;font-display:swap;src:url(fonts/spectral-latin-400-italic.woff2) format("woff2")}
@font-face{font-family:"Spectral";font-weight:600;font-style:normal;font-display:swap;src:url(fonts/spectral-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Spectral SC";font-weight:500;font-style:normal;font-display:swap;src:url(fonts/spectral-sc-latin-500-normal.woff2) format("woff2")}
:root{--night:#1A2238;--wall:#222B45;--frame:#3A4466;--glass:#2B3454;--lamp:#F3B94D;--moon:#E9ECF4;--dim:#AEB6CC;
--paper:#F5F6F8;--ink:#1D2233;--muted:#5B6276;--panel:#E8ECF3}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.125rem/1.65 "Spectral",Georgia,serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-underline-offset:.18em}
:focus-visible{outline:3px solid var(--lamp);outline-offset:3px}
.hero{background:var(--night);color:var(--moon);text-align:center;padding:4.5rem 1rem 3rem}
.hero h1{font-weight:300;font-size:clamp(2.5rem,7.5vw,4.6rem);line-height:1.05;margin:0;letter-spacing:.005em}
.hero .sub{font-style:italic;color:var(--dim);margin:.8rem 0 0}
.house{position:relative;display:inline-block;margin:4.2rem auto 0;padding:1.6rem 1.8rem 0;background:var(--wall);max-width:100%}
.roof{position:absolute;left:-1.2rem;right:-1.2rem;bottom:100%;height:4.2rem;background:var(--wall);clip-path:polygon(50% 0,100% 100%,0 100%)}
.floor{list-style:none;margin:0;padding:0 0 1.4rem;display:flex;flex-wrap:wrap;justify-content:center;align-items:flex-end;gap:10px}
.floor+.floor{padding-bottom:0}
.win{display:block;width:26px;height:36px;background:var(--glass) linear-gradient(var(--frame),var(--frame)) center/2px 100% no-repeat;
border:2px solid var(--frame);position:relative;transition:background-color .9s,box-shadow .9s}
.win::after{content:"";position:absolute;left:0;right:0;top:50%;height:2px;margin-top:-1px;background:var(--frame)}
.win:hover{background-color:#3A4570}
.win.lit{background-color:var(--lamp);box-shadow:0 0 16px 2px rgba(243,185,77,.5)}
.win.playing{box-shadow:0 0 26px 6px rgba(243,185,77,.75)}
.door{display:flex;justify-content:center}
.door::before{content:"";width:36px;height:58px;background:var(--lamp);border:2px solid var(--frame);border-bottom:none;box-shadow:0 0 22px 3px rgba(243,185,77,.35)}
.caption{min-height:1.65em;color:var(--dim);margin:1.1rem 0 0;font-style:italic}
.how{margin:1.6rem auto 0;max-width:36rem;text-wrap:balance}
.links{margin:1rem 0 0}
.links a{color:var(--moon)}
.note{color:var(--dim);font-size:.95rem;max-width:34rem;margin:1.6rem auto 0;text-wrap:balance}
.synopsis{padding:3.2rem 0 1.4rem}
.synopsis .script{padding-bottom:0}
.synopsis p:first-child{font-size:1.2rem}
.synopsis strong{font:500 1em "Spectral SC",Georgia,serif;letter-spacing:.02em}
.synopsis p:last-child em{color:var(--muted);font-size:.95rem}
.act-band{background:var(--night);color:var(--moon);text-align:center;padding:3.6rem 1rem;margin:0 0 1rem}
.act-band h2{font-weight:300;font-size:clamp(2rem,5.5vw,3rem);line-height:1.1;margin:0}
.act-band h2 span{display:block;font-style:italic;font-size:.55em;color:var(--dim);margin-top:.35rem}
.script{max-width:40rem;margin:0 auto;padding:0 1.25rem 3rem}
.scene{font:500 1.2rem/1.3 "Spectral SC",Georgia,serif;letter-spacing:.03em;margin:3.2rem 0 1rem}
p{margin:0 0 1rem}
.sd{font-style:italic;color:var(--muted)}
.cap{font-family:"Spectral SC",Georgia,serif;font-style:normal;font-weight:500;letter-spacing:.02em}
.who{font-family:"Spectral SC",Georgia,serif;font-weight:500;letter-spacing:.03em}
.line .who{margin-right:.35em}
.song{background:var(--panel);border-radius:6px;padding:1.25rem 1.5rem 1.1rem;margin:2.2rem -1.5rem}
.song-head{display:flex;align-items:center;gap:.9rem}
.song-title{margin:0;font-size:1.3rem;font-weight:600;line-height:1.25}
.song-title .n{font:500 1rem "Spectral SC",Georgia,serif;color:var(--muted);margin-right:.45em}
.play{flex:none;width:46px;height:46px;border-radius:50%;border:0;background:var(--night);color:var(--moon);cursor:pointer;
display:grid;place-items:center;transition:background-color .3s,color .3s}
.play::before{content:"";width:0;height:0;border-left:14px solid currentColor;border-top:9px solid transparent;border-bottom:9px solid transparent;margin-left:4px}
.song.playing .play{background:var(--lamp);color:var(--night)}
.song.playing .play::before{width:14px;height:16px;border:0;margin:0;background:linear-gradient(90deg,currentColor 0 5px,transparent 5px 9px,currentColor 9px)}
.time{margin-left:auto;color:var(--muted);font-size:.92rem;white-space:nowrap;font-variant-numeric:tabular-nums}
.seek{display:block;width:100%;margin:.9rem 0 1.1rem;accent-color:var(--night)}
.song.playing .seek{accent-color:#B9821A}
.lyrics p:last-child{margin-bottom:.2rem}
.end{text-align:center;font:500 1.15rem "Spectral SC",Georgia,serif;letter-spacing:.06em;margin:3.5rem 0 1rem}
footer{background:var(--night);color:var(--dim);text-align:center;padding:3rem 1rem;font-size:.95rem}
footer button{font:inherit;color:var(--moon);background:none;border:0;text-decoration:underline;text-underline-offset:.18em;cursor:pointer;padding:0}
@media (max-width:700px){
  body{font-size:1.06rem}
  .house{padding:1.2rem .9rem 0}
  .floor{gap:7px}
  .win{width:20px;height:28px}
  .door{order:99;flex:0 0 100%;margin-top:4px}
  .door::before{width:28px;height:44px}
  .song{margin:2rem -.5rem;padding:1.1rem 1rem 1rem}
  .time{display:none}
}
"""

JS = r"""
(function(){
  var audio = new Audio(); audio.preload = "none";
  var current = null, KEY = "ilto-lit", lit = [];
  try { lit = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { lit = []; }
  function win(id){ return document.querySelector('.win[data-song="' + id + '"]'); }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(lit)); } catch (e) {} }
  lit.forEach(function(id){ var w = win(id); if (w) w.classList.add("lit"); });
  function light(id){ if (lit.indexOf(id) < 0) { lit.push(id); save(); } var w = win(id); if (w) w.classList.add("lit"); }
  function fmt(s){ s = Math.floor(s || 0); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function setState(sec, on){
    if (!sec) return;
    sec.classList.toggle("playing", on);
    sec.querySelector(".play").setAttribute("aria-label", (on ? "Pause " : "Play ") + sec.dataset.title);
    var w = win(sec.dataset.song); if (w) w.classList.toggle("playing", on);
  }
  function start(sec, at){
    if (current && current !== sec) { audio.pause(); setState(current, false); current.querySelector(".seek").value = 0; current.querySelector(".cur").textContent = "0:00"; }
    current = sec; audio.src = sec.dataset.src;
    if (at) audio.addEventListener("loadedmetadata", function(){ audio.currentTime = at; }, { once: true });
    audio.play();
  }
  document.querySelectorAll(".song[data-src]").forEach(function(sec){
    sec.querySelector(".play").addEventListener("click", function(){
      if (current === sec) { audio.paused ? audio.play() : audio.pause(); } else { start(sec, 0); }
    });
    sec.querySelector(".seek").addEventListener("input", function(e){
      var v = +e.target.value;
      if (current === sec) { audio.currentTime = v; } else { start(sec, v); }
    });
  });
  audio.addEventListener("play", function(){ setState(current, true); light(current.dataset.song); });
  audio.addEventListener("pause", function(){ setState(current, false); });
  audio.addEventListener("ended", function(){ setState(current, false); });
  audio.addEventListener("timeupdate", function(){
    if (!current) return;
    current.querySelector(".seek").value = audio.currentTime;
    current.querySelector(".cur").textContent = fmt(audio.currentTime);
  });
  var cap = document.querySelector(".caption"), idle = cap.textContent;
  document.querySelectorAll(".win").forEach(function(w){
    function show(){ cap.textContent = w.dataset.label; }
    function hide(){ cap.textContent = idle; }
    w.addEventListener("mouseenter", show); w.addEventListener("focus", show);
    w.addEventListener("mouseleave", hide); w.addEventListener("blur", hide);
  });
  var off = document.querySelector(".lights-off");
  if (off) off.addEventListener("click", function(){
    lit = []; save();
    document.querySelectorAll(".win.lit").forEach(function(w){ w.classList.remove("lit"); });
  });
})();
"""


def main():
    try:
        import build_pdf
        build_pdf.main()
    except (Exception, SystemExit) as e:
        bl.main()
        print(f"PDF not rebuilt ({e}); using the existing one if there is one.")
    mp3s = find_mp3s()
    body, windows = build_body(mp3s)
    syn = ROOT / "Synopsis.md"
    synopsis = ('<section class="synopsis" aria-label="Synopsis"><div class="script">'
                + markdown.markdown(syn.read_text(encoding="utf-8"), extensions=["smarty"]) + "</div></section>\n") if syn.exists() else ""
    date = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%B %-d, %Y")
    repo_link = f' · <a href="{REPO}">The script and songs on GitHub</a>' if REPO else ""
    license_where = f', <a href="{REPO}/blob/main/LICENSE.md">in full here</a>' if REPO else ", printed at the front of the PDF"
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{TITLE}, a musical in two acts by {AUTHOR}: the whole libretto, with a demo of every song.">
<meta name="referrer" content="no-referrer">
<title>{TITLE}</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
<h1>{TITLE}</h1>
<p class="sub">A musical in two acts by {AUTHOR}. Draft of {date}.</p>
{house(windows)}
<p class="caption" aria-live="polite">Every window is a song.</p>
<p class="how">Choose a window to jump to its song. Play a song and its light stays on.</p>
<p class="links"><a href="libretto.pdf" download="{TITLE} - Libretto.pdf">Download the libretto as a PDF</a>{repo_link}</p>
<p class="note">The recordings are rough demos, made with AI. You're welcome to share all of it: anyone may read, share and perform the show for non-commercial purposes. The license and “About this story” are at the front of the PDF.</p>
</header>
{synopsis}<main>
{body}
</main>
<footer>
<p>{TITLE}. Book, lyrics and music by {AUTHOR}. Draft of {date}.</p>
<p>Free to read, share and perform for non-commercial purposes under its license (<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>){license_where}.</p>
<p><button class="lights-off" type="button">Turn all the lights off</button></p>
</footer>
<script>{JS}</script>
</body>
</html>
"""
    (SITE / "audio").mkdir(parents=True, exist_ok=True)
    (SITE / "fonts").mkdir(exist_ok=True)
    (SITE / "index.html").write_text(page, encoding="utf-8")
    for key, p in mp3s.items():
        place(p, SITE / "audio" / f"{'00' if key == 'P' else key.zfill(2)}.mp3")
    for f in (SRC / "fonts").iterdir():
        place(f, SITE / "fonts" / f.name)
    pdf = ROOT / "I Left the Lights On - Libretto.pdf"
    if pdf.exists():
        place(pdf, SITE / "libretto.pdf")
    (SITE / "robots.txt").write_text("User-agent: *\nDisallow:\n")
    (SITE / "_headers").write_text("/*\n  Referrer-Policy: no-referrer\n"
                                   "/audio/*\n  Cache-Control: public, max-age=86400\n")
    n = sum(1 for _ in (SITE / "audio").glob("*.mp3"))
    print(f"Wrote site/ : index.html, {n} songs, PDF {'included' if pdf.exists() else 'missing'}.")


if __name__ == "__main__":
    main()
