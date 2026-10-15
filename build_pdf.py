#!/usr/bin/env python3
"""Render the libretto as a PDF, laid out like a published script.

Run from this folder:  python3 build_pdf.py
Writes:  I Left the Lights On - Libretto.pdf   (and refreshes the .md libretto)
         LICENSE.md, if present, goes on the page after the title page.
Needs:   pandoc and XeLaTeX (on a Mac: `brew install pandoc` and BasicTeX or MacTeX).
"""
import datetime
from zoneinfo import ZoneInfo
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import build_libretto as bl

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "I Left the Lights On - Libretto.pdf"
TITLE = "I Left the Lights On"
SUBTITLE = "A musical in two acts"
AUTHOR = "Book, lyrics and music by Jessica Mulein"

SPEAKER = re.compile(r"^([A-Z][A-Z0-9'’.\-]*(?: [A-Z0-9'’.\-]+)*(?: and [A-Z][A-Z0-9'’.\-]*(?: [A-Z0-9'’.\-]+)*)*):\s")

PREAMBLE = r"""
\usepackage{newunicodechar}
\IfFontExistsTF{DejaVu Sans}{\newfontfamily\symbolfont{DejaVu Sans}}{%
  \IfFontExistsTF{Apple Symbols}{\newfontfamily\symbolfont{Apple Symbols}}{%
    \IfFontExistsTF{Arial Unicode MS}{\newfontfamily\symbolfont{Arial Unicode MS}}{\newcommand{\symbolfont}{}}}}
\newunicodechar{♪}{{\symbolfont ♪}}
\usepackage{titlesec}
\titleformat{\section}[display]{\centering\normalfont}{}{0pt}{\Huge\scshape}
\titlespacing*{\section}{0pt}{1.6in}{0.5in}
\newcommand{\sectionbreak}{\clearpage\thispagestyle{plain}}
\titleformat{\subsection}{\normalfont\large\scshape}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{2.4em}{0.6em}
\titleformat{\subsubsection}{\centering\normalfont\large\itshape}{}{0pt}{}
\titlespacing*{\subsubsection}{0pt}{1.8em}{1.1em}
\usepackage{changepage}
\newenvironment{song}{\begin{adjustwidth}{2.5em}{1.5em}}{\end{adjustwidth}\medskip}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\scshape I Left the Lights On}
\fancyhead[R]{\footnotesize\scshape\leftmark}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\sectionmark}[1]{\markboth{#1}{}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0pt}}
\widowpenalty=10000
\clubpenalty=10000
"""


def latex(s):
    return f"\n```{{=latex}}\n{s}\n```\n"


def tex_escape(s):
    return re.sub(r"([&%$#_{}])", r"\\\1", s)


def clean(line):
    line = line.replace(" ", " ")
    m = SPEAKER.match(line)
    if m:
        line = f"**{m.group(1)}:** " + line[m.end():]
    return line


def song_number(stem):
    n = stem.split(" - ", 1)[0]
    return "P" if n == "P" else str(int(n))


def assemble():
    songs = bl.song_files()
    body, numbers = [], []          # numbers: (act, number, title, label)
    for act in ("Act One", "Act Two"):
        script = ROOT / "Script" / f"{act}.md"
        for line in script.read_text(encoding="utf-8").splitlines():
            if line.startswith("# ") or line.startswith("*Book, draft") or line.strip() == "---":
                continue
            if re.fullmatch(r"\*\*END OF (ACT ONE|PLAY)\*\*\s*", line):
                words = line.strip("* \n").title().replace(" Of ", " of ")
                body.append(latex(r"\begin{center}\vspace{2em}\textsc{" + words + r"}\end{center}"))
                continue
            m = bl.CUE.match(line)
            if not m:
                body.append(clean(line))
                continue
            stem = m.group(1)
            path = songs.get(stem)
            if path is None:
                body.append(f"> **[Missing song: {stem}]**")
                continue
            title, status, lyric = bl.song_block(path)
            num = song_number(stem)
            label = f"song-{num}"
            numbers.append((act, num, title, label))
            body.append(f"\n#### ♪ {title}\n")
            body.append(latex(r"\label{" + label + "}"))
            if status.lower().startswith("stage draft"):
                body.append(latex(r"\begin{song}"))
                body.append(bl.hard_breaks("\n".join(clean(l) for l in lyric.splitlines())))
                body.append(latex(r"\end{song}"))
            else:
                body.append(f"> *[{status}]*")
    return body, numbers


def license_page():
    """LICENSE.md on its own page, small type, like the rights page of a published script."""
    text = bl.license_text()
    if not text:
        return ""
    text = re.sub(r"^## (.+?)\s*$", lambda m: latex(r"\medskip{\centering\scshape " + tex_escape(m.group(1)) + r"\par}"),
                  text, flags=re.M)
    return (latex(r"\thispagestyle{empty}\begingroup\small\setlength{\parskip}{0.55em}\setlength{\parindent}{0pt}")
            + "\n" + text + "\n" + latex(r"\endgroup\clearpage"))


def front_matter(numbers):
    date = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%B %-d, %Y")
    out = [r"\begin{titlepage}\centering",
           r"\vspace*{2.4in}",
           r"{\Huge\scshape " + tex_escape(TITLE) + r"\par}",
           r"\vspace{1.2em}",
           r"{\large\itshape " + tex_escape(SUBTITLE) + r"\par}"]
    if AUTHOR:
        out += [r"\vspace{2.5em}", r"{\large " + tex_escape(AUTHOR) + r"\par}"]
    out += [r"\vfill", r"{\small Draft \textperiodcentered\ " + date + r"\par}", r"\end{titlepage}"]
    title_page, out = out, [r"\thispagestyle{empty}",
            r"{\centering\Large\scshape Musical Numbers\par}\vspace{1em}",
            r"\begingroup\small\setlength{\parskip}{1.5pt}"]
    current = None
    for act, num, title, label in numbers:
        if act != current:
            current = act
            out.append(r"\par\medskip{\centering\scshape " + act + r"\par}\smallskip")
        n = "" if num == "P" else num + "."
        out.append(r"\noindent\makebox[2.2em][r]{" + n + r"}\hspace{0.8em}" + tex_escape(title)
                   + r"\dotfill\pageref{" + label + r"}\par")
    out.append(r"\endgroup\clearpage\pagenumbering{arabic}")
    return latex("\n".join(title_page)) + license_page() + latex("\n".join(out))


def main():
    bl.main()                                   # keep the .md libretto in step
    body, numbers = assemble()
    md = front_matter(numbers) + "\n".join(body) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "libretto.md").write_text(md, encoding="utf-8")
        (tmp / "preamble.tex").write_text(PREAMBLE, encoding="utf-8")
        cmd = ["pandoc", str(tmp / "libretto.md"), "-f", "markdown+raw_attribute", "-o", str(tmp / "out.pdf"),
               "--pdf-engine=xelatex", "--shift-heading-level-by=-1", "-H", str(tmp / "preamble.tex"),
               "-V", "papersize=letter", "-V", "geometry:margin=1in", "-V", "fontsize=11pt",
               "-V", "mainfont=texgyrepagella-regular.otf",
               "-V", "mainfontoptions=BoldFont=texgyrepagella-bold.otf, ItalicFont=texgyrepagella-italic.otf, BoldItalicFont=texgyrepagella-bolditalic.otf",
               "-V", "linkcolor=black", "-M", f"title={TITLE}", "-V", "title=", "-M", "pagetitle=" + TITLE]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("pandoc failed:\n" + r.stderr[-3000:])
        PDF.write_bytes((tmp / "out.pdf").read_bytes())
    print(f"Wrote {PDF.name}")


if __name__ == "__main__":
    main()
