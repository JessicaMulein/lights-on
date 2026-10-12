import re
from pathlib import Path
OUT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"^\[(Intro|Verse \d+|Chorus|Pre-Chorus|Bridge|Outro|Spoken Word|End)\]$")
S = lambda s: [x.strip() for x in s.split(",")]
P = {
"P - I Left the Lights On": dict(text=[("[A music box plays four bars and stops; female lead finds the same notes on the piano, slower]", "[A music box plays four bars and stops; the same notes on piano, slower]")]),
"02 - The Mirror": dict(text=[("[Intro]\n\n[Verse 1]", "[Intro]\n[Stiff, polite string-quartet minuet]\n\n[Verse 1]"), ("[Verse 2]\nThere's a boy", "[Melts into a 6/8 lullaby: felt piano, music box]\n[Verse 2]\nThere's a boy")]),
"03 - Louise": dict(labels=S("Intro, Verse 1, Verse 2, Chorus, Verse 3, End")),
"05 - Keep Clear": dict(labels=S("Intro, Verse 1, Pre-Chorus, Chorus, Verse 2, Chorus, Bridge, Chorus, Outro, End"), text=[("[Impact: light and sound]", "[Impact: the music stops dead]")]),
"07 - Road Less Traveled": dict(labels=S("Intro, Spoken Word, Chorus, Verse 1, Verse 2, Chorus, Bridge, Outro, End"), text=[("[The first verse is spoken over a few piano chords; the music gathers under her until she's singing]", "[Spoken word over a few piano chords; the music gathers underneath]"), ("[The music falls away; Spoken, quietly]", "[The music falls away; spoken, quietly]")]),
"10 - Giving Up": dict(labels=S("Intro, Spoken Word, Verse 1, Chorus, Spoken Word, Verse 2, Chorus, Bridge, Outro, End")),
"11 - Leah and the Boys": dict(labels=S("Intro, Verse 1, Verse 2, Chorus, Bridge, Chorus, Outro, End"), text=[("[The music box tune from the Prologue, very softly]", "[A music-box lullaby, very softly]")]),
"13 - Fluorescent Moon": dict(text=[("[Then, very quietly, to no one:]", "[Very quietly, spoken]")]),
"12 - Another Night": dict(text=[("[Older Female Voice (Louise)]\nI don't think", "[Spoken Word: Older Female Voice (Louise)]\nI don't think"), ("[Older Female Voice (Louise)]\nWalt's waiting.", "[Spoken Word, barely: Older Female Voice (Louise)]\nWalt's waiting.")]),
"15 - The Winter Coat": dict(labels=S("Intro, Verse 1, Chorus, -, Verse 2, Verse 3, Chorus, Outro, End"), text=[("[Female Lead, older, reflective (Jennifer)]\nThen one night", "\n[Music drops out into a 6/8 lullaby: felt piano, music box]\n[Bridge]\n[Female Lead, older, reflective (Jennifer)]\nThen one night")]),
"17 - Sport Coat at the Door": dict(labels=S("Intro, Verse 1, -, Chorus, Verse 2, Chorus, Bridge, Outro, End"), text=[("[Intro]\n\n[Verse 1]", "[Intro]\n[Stiff, polite string-quartet minuet]\n\n[Verse 1]"), ("[Verse 2]\nTown and Country", "[Softer, warmer strings]\n[Verse 2]\nTown and Country")]),
"18 - Turns Out It's Genetic": dict(text=[(re.compile(r"grin\.\n+(\[Female Lead \(Jennifer\)\]\n)?I'd been looking"), r"grin.\n\n[Pre-Chorus]\n\1I'd been looking")]),
"21 - Curtains Up, World": dict(text=[("[Operatic piano break; The choir in choir harmony]", "[Operatic piano break; choir harmonies]")]),
"23 - Silver Tongues": dict(labels=S("Intro, Interlude, Verse 1, Interlude, Chorus, Verse 2, Verse 3, Verse 4, Interlude, Chorus, Interlude, Outro, End"),
   text=[(re.compile(r"\[Behind the whitcombs[^\]]*\]"), "[Raw, slow solo piano]"),
         ("[Verse 2]\nThey didn't go together", "[The music blurs, like fog]\n[Verse 2]\n[Female Lead (Jennifer)]\nThey didn't go together"),
         ("[Verse 3]\nThen Owen", "[Verse 3]\n[Female Lead (Jennifer)]\nThen Owen"),
         ("[Verse 4]\nYou painted", "[Verse 4]\n[Female Lead (Jennifer)]\nYou painted"),
         ("\nI own the mistakes I made", "\n\n[Pre-Chorus]\n[Female Lead (Jennifer)]\nI own the mistakes I made"),
         ("[Male Barbershop Quartet (Lawyers)]\nSo ordered.", "[Male Lawyer, slow and final (Lawyer)]\nSo ordered."),
         (re.compile(r"\[Male Barbershop Quartet(, overlapping)? \(Lawyers\)\]"), r"[Male Lawyer\1 (Lawyer)]")]),
"24 - Frozen in the Light": dict(labels=S("Intro, Verse 1, Chorus, Verse 2, Chorus, Verse 3, Bridge, Chorus, Outro, End")),
"26 - Spy in the Boys Club": dict(labels=S("Intro, Verse 1, Pre-Chorus, Chorus, Verse 2, Pre-Chorus, Chorus, Bridge, Chorus, Outro, -, End")),
"29 - The Crossing": dict(labels=S("Intro, Verse 1, Verse 2, Chorus, Bridge, Verse 3, Outro, End"),
   text=[('[Dance: "The Dark Oars" from Journeying the Styx]', "\n[Instrumental Break: dark rowing dance; harp, timpani, wordless choir]\n\n[Spoken Word]")]),
"31 - Fine, How Are You": dict(labels=S("Intro, Verse 1, Pre-Chorus, Chorus, Verse 3, Bridge, Chorus, Spoken Word, Outro, End"),
   text=[(re.compile(r"(I told her true:\n)\n?(I'm fine! How are you\?)"), r"\1\n[Chorus]\n\2"), (re.compile(r"\n+(Then the pharmacist was counting)"), r"\n\n[Verse 2]\n\1")]),
"32 - Lawyer Up, Hit the Gym": dict(labels=S("Intro, Spoken Word, -, Chorus, Verse 3, -, Bridge, Chorus, Outro, End"),
   text=[("[Boots stomp in]\nThrowaway account", "\n[Boots stomp in]\n[Verse 1]\n[Female Lead (Jennifer)]\nThrowaway account"),
         ("here's what they said:\n[Gang Vocals (The Internet)]", "here's what they said:\n\n[Chorus]\n[Gang Vocals (The Internet)]"),
         ("say kiss her goodbye!\n[Female Lead (Jennifer)]\nThen the replies", "say kiss her goodbye!\n\n[Verse 2]\n[Female Lead (Jennifer)]\nThen the replies")]),
"33 - We Take Turns": dict(labels=S("Intro, Verse 1, Chorus, Verse 2, Verse 3, Verse 4, Chorus, Bridge, -, Chorus, Outro, -, -, End")),
"34 - Hope": dict(labels=S("Intro, Verse 1, Chorus, Verse 2, Chorus, Bridge, Chorus, -, End"), text=[("[Bridge]\nIt wasn't a choice", "[Bridge]\n[Second Female Voice, warm (Nora)]\nIt wasn't a choice")]),
"35 - Before I Broke": dict(labels=S("Intro, Spoken Word, Verse 1, -, Pre-Chorus, Verse 2, Pre-Chorus, Bridge, Outro, End"),
   text=[("\n'Cause before I broke, I would have believed", "\n\n[Chorus]\n'Cause before I broke, I would have believed")]),
"36 - Break Me": dict(labels=S("Intro, Verse 1, Chorus, Verse 2, Chorus, Bridge, Chorus, Spoken Word, Coda, End"),
   text=[("[The Good Grief melody, on piano alone]", "[Key change; soft solo piano, a tender new melody]")]),
"37 - Highly Capable": dict(labels=S("Intro, Verse 1, -, Pre-Chorus, -, Chorus, Verse 2, Pre-Chorus, -, Chorus, Verse 3, Bridge, Chorus, Outro, End"),
   text=[("\nWell, I wore it to the door.", "\n[Stop-time]\nWell, I wore it to the door."), ("\nand I took a nap that day.", "\n[Stop-time]\nand I took a nap that day."),
         ("[A chicken-pickin' Telecaster lick; The lights go gaudy, like a game show]", "[A chicken-pickin' Telecaster lick; game-show swagger]")]),
"38 - Unspoken Cost": dict(labels=S("Intro, Verse 1, Verse 2, -, -, Chorus, Verse 3, Verse 4, Bridge, -, -, Final Chorus, -, Outro, End")),
"39 - Carry Me": dict(labels=S("Intro, Verse 1, Pre-Chorus, Chorus, Verse 2, Pre-Chorus, Chorus, Bridge, -, Chorus, -, Outro, End"),
   text=[("\nwho stayed, and called it love.", "\n[Female Lead (Jennifer)]\nwho stayed, and called it love.")]),
"40 - I Left the Lights On (Finale)": dict(labels=S("Intro, Verse 1, Chorus, Verse 2, Bridge, Chorus, Verse 3, -, Outro, End"),
   text=[("[Louise's melody; second female voice hums it under her]", "[A hymn-like folk melody; second female voice hums under her]")]),
}
NOTES = {
"09 - The Party": "Two women trade lines fast here. If the model blurs the voices, generate Leah's lines as a separate take.",
"23 - Silver Tongues": "Mozart can't do a barbershop quartet and blurs the voices, so this demo uses one male lawyer. Every section of hers names her voice, so Mozart doesn't hand part of a verse to him. If it still does, generate her part alone (leave out the lawyer's lines) and record his lines as a separate take to cut in. The stage version keeps the quartet.",
"29 - The Crossing": "This runs long (about 7 to 8 minutes on stage). If the model cuts it short, generate it in two parts: through the rowing chorus, then from the far shore to the end.",
"38 - Unspoken Cost": "On stage the final chorus is two melodies at once. The model will sing Teen Jen's lines after Jennifer's rather than over them, so generate them as a separate take if you want the real counterpoint.",
"18 - Turns Out It's Genetic": "Solo demo. When the style asked for a duet with a male baritone, Mozart brought in a man's voice on its own, partway through the first verse. So the demo style no longer mentions a man, and the character tags are gone: one singer sings everything, Hal's lines and the phone calls included, the way a writer's demo often has one person cover every part. Who sings what is in the stage version in Songs. Use the demo style, not the full production style, which still describes the duet.",
"39 - Carry Me": "Voices should enter one at a time. If the model jumps straight to a full choir, start with only the first verse and chorus and extend from there.",
}
def fix(lyr, spec):
    lines = lyr.split("\n")
    if "labels" in spec:
        idx = [i for i, l in enumerate(lines) if LABEL.match(l)]
        assert len(idx) == len(spec["labels"]), (len(idx), len(spec["labels"]), [lines[i] for i in idx])
        for i, s in zip(idx, spec["labels"]): lines[i] = None if s == "-" else f"[{s}]"
        out = []
        for l in lines:
            if l is None:
                if out and out[-1] == "": out.pop()
                continue
            out.append(l)
        lyr = "\n".join(out)
    for o, n in spec.get("text", []):
        if isinstance(o, re.Pattern):
            lyr, k = o.subn(n, lyr)
        else:
            k = lyr.count(o); lyr = lyr.replace(o, n)
        assert k >= 1, (o if isinstance(o, str) else o.pattern)[:60]
    return re.sub(r"\n{3,}", "\n\n", lyr).strip("\n")

LIMIT = 3000
VTAG = re.compile(r"^\[(Spoken Word[^:]*: )?([^\]]*?) \(([^)]*)\)\]$")
def compact(lyr):
    """Shorten voice tags (no lyric words change) for songs over Mozart's 3,000-character box."""
    L = lyr.split("\n")
    L = [l for i, l in enumerate(L) if not (l == "[Spoken Word]" and i + 1 < len(L) and L[i + 1].startswith("[Spoken Word"))]
    tok = []
    for l in L:
        m = VTAG.match(l)
        if not m: tok.append(("line", l)); continue
        spoken, desc, names = m.groups()
        if "&" in names: name = "All" if names.count("&") > 1 else "Duet"
        else: name = names + (", baritone" if "Baritone" in desc and not spoken else "")
        tok.append(("spoken" if spoken else "sung", name))
    out, cur, i = [], None, 0
    while i < len(tok):
        kind, v = tok[i]
        if kind == "spoken":
            j, n = i, 0
            while j < len(tok):
                k2, v2 = tok[j]
                if k2 == "spoken": n += 1
                elif k2 == "sung" or v2.startswith("["): break
                j += 1
            if n > 1: out.append("[Spoken]")
            for k2, v2 in tok[i:j]:
                out.append((f"[{v2}]" if n > 1 else f"[{v2}, spoken]") if k2 == "spoken" else v2)
            cur, i = None, j; continue
        if kind == "sung":
            if v != cur: out.append(f"[{v}]"); cur = v
        else: out.append(v)
        i += 1
    return "\n".join(out)

SOLO = {"18 - Turns Out It's Genetic": [("[Intro]\n[A long, awkward silence]", "[Intro]"), ("[slows down, half-spoken]", "[Slower, half-spoken]")]}
def solo(lyr):
    """One singer for everything: drop character tags, keep section labels, mark spoken runs."""
    out, spoken = [], False
    for l in lyr.split("\n"):
        m = VTAG.match(l)
        if l == "[Spoken Word]" or (m and m.group(1)):
            if not spoken: out.append("[Spoken]"); spoken = True
            continue
        if m:
            if spoken: out.append("[Sung]"); spoken = False
            continue
        if l.startswith("["): spoken = False
        out.append(l)
    return "\n".join(out)

COMPACT = {
"18 - Turns Out It's Genetic": [("[Intro]\n[A long, awkward silence]", "[Intro]"), ("[The music softens]\n[Spoken]", "[Softer, spoken]"), ("[slows down, half-spoken]", "[Slower, half-spoken]")],
}

for f in sorted(OUT.rglob("*.md")):
    if f.name == "README.md": continue
    t = f.read_text(); stem = f.stem
    m = re.search(r"## Lyrics\n\n```\n(.*?)\n```\n", t, re.S)
    lyr = m.group(1)
    if stem in P: lyr = fix(lyr, P[stem])
    voices = []
    for v in re.findall(r"^\[(?:Spoken Word(?:, barely)?: )?([^\]]*?) \(([^)]*)\)\]$", lyr, re.M):
        name = v[1]
        if name not in [x[0] for x in voices]: voices.append((name, v[0].split(", older")[0]))
    if stem in SOLO:
        lyr = solo(lyr)
        for o, n in SOLO[stem]:
            assert o in lyr, o; lyr = lyr.replace(o, n)
        voices = []
    full = len(lyr)
    if full > LIMIT:
        lyr = compact(lyr)
        for o, n in COMPACT.get(stem, []):
            assert o in lyr, o; lyr = lyr.replace(o, n)
        assert len(lyr) <= LIMIT, (stem, len(lyr))
        voices = [v for v in voices if "&" not in v[0]]
    t = t[:m.start(1)] + lyr + t[m.end(1):]
    demo_len = len(re.search(r"## Demo style[^\n]*\n\n```\n(.*?)\n```", t, re.S).group(1))
    style_len = len(re.search(r"## Full production style\n\n```\n(.*?)\n```", t, re.S).group(1))
    notes = [f"- Lyrics: {len(lyr):,} characters (Mozart's lyrics box holds 3,000, counting the bracketed tags; Suno's holds 5,000). Styles: {demo_len} and {style_len} characters (Suno's style box holds 1,000)."]
    if full > LIMIT:
        notes.append(f"- Shortened to fit: with the usual tags this song ran {full:,} characters, so the bracketed tags are trimmed and every lyric word is still here. [Spoken] starts a run of spoken lines, and each name after it says who's talking. [Duet] is Jennifer and Hal together; [All] is everyone.")
    if voices: notes.append("- Voices: " + "; ".join(f"{n} = {d}" for n, d in voices) + ".")
    if stem in NOTES: notes.append("- " + NOTES[stem])
    t = re.sub(r"## Notes\n\n.*\Z", "## Notes\n\n" + "\n".join(notes) + "\n", t, flags=re.S)
    f.write_text(t)
print("patched", len(P))
