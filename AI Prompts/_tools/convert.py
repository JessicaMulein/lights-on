import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from styles import STYLES, DEMO
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/"AI Prompts"
VOICE = {
 "JENNIFER":"Female Lead","JEN":"Female Lead","YOUNG JEN":"Child Voice","TEEN JEN":"Teenage Female Voice",
 "NORA":"Second Female Voice, warm","YOUNG NORA":"Teenage Female Voice 2","LEAH":"Second Female Voice, bright",
 "LOUISE":"Older Female Voice","RUTH":"Female Minister, warm","CASEY":"Teenage Female Voice 2",
 "HAL":"Male Baritone","DR. WHITCOMB":"Male Voice, stern","MRS. WHITCOMB":"Female Voice, clipped",
 "CLAIRE":"Second Female Voice, sweet","THE ADJUSTER":"Male Voice, tired and reasonable",
 "LAWYERS":"Male Barbershop Quartet","COMPANY":"Choir","OFFICE MEN":"Male Gang Vocals",
 "THE INTERNET":"Gang Vocals","A STRANGER":"Shouted, crowd voice","ANOTHER STRANGER":"Shouted, crowd voice",
 "FRIENDS":"Group Vocals","A FRIEND":"Second Female Voice","A PHARMACIST":"Second Voice","A NEIGHBOR":"Second Female Voice",
 "THE NURSE":"Older Female Voice","NURSE":"Female Voice","THE EMT":"Female Voice, cold","A VOICE":"Corporate Voice",
 "COAT CHECK ATTENDANT":"Male Voice","TESS":"Second Female Voice","MAGGIE":"Female Voice, bright","SAM":"Male Voice, warm","HAL":"Male Baritone","OWEN":"Boy's Voice","THEO":"Small Child's Voice","DOCTOR":"Male Voice","NORA'S MOTHER":"Older Female Voice","NORA'S FAMILY":"Group Vocals","ALL":"Full Group",
}
def short(v): return v.split(",")[0]
def voice(names, qual):
    q = (qual or "").lower()
    parts = [n.strip() for n in re.split(r",| and ", names) if n.strip()]
    groups = ("COMPANY","FRIENDS","NORA'S FAMILY","ALL")
    if len(parts) == 1:
        v = VOICE.get(parts[0], "Voice")
    elif len(parts) == 2 and any(p in ("JENNIFER", "JEN") for p in parts) and any(p in groups for p in parts):
        v = "Female Lead with " + VOICE[[p for p in parts if p not in ("JENNIFER", "JEN")][0]]
    elif len(parts) > 2 or any(p in groups for p in parts):
        v = "Group Vocals"
    else:
        a, b = (short(VOICE.get(x, "Voice")) for x in parts)
        fem = lambda s: "Female" in s or s in ("Child Voice",)
        v = "Female Duet" if (a, b) in [("Female Lead", "Second Female Voice"), ("Second Female Voice", "Female Lead")] else f"Duet: {a} and {b}"
    who = " & ".join(p.title().replace("'S", "'s").replace("Emt", "EMT") for p in parts)
    spoken = "spoken" in q and "half-spoken" not in q
    tag = ("Spoken Word: " if spoken else "") + v
    extra = []
    if q.startswith("now") or "from the piano" in q: extra.append("older, reflective")
    if "half-spoken" in q: extra.append("half-spoken")
    if "overlapping" in q or "at the same time" in q: extra.append("overlapping")
    if extra: tag += ", " + ", ".join(extra)
    return f"[{tag} ({who})]", spoken
MUSIC = re.compile(r"piano(?! bench)|strings\b|string quartet|cello|violin|fiddle|guitar|steel|slide (?:guitar|resonator)|lone slide|resonator|banjo|bass\b|drum|snare|toms|timpani|harp|harmonica|organ|hums?\b|humming|vocalise|\bband\b|orchestra|melody|tune|lullaby|music|celesta|trumpet|horn|concertina|whistle|bell|tempo|key change|a cappella|instrumental|solo|beat\b|shuffle|\bswing\b|stomp|clap|finger snap|rubato|swell|builds?\b|building|slows?|quiet|softer|silence|(?:music|band|everything|piano|stomp) stops|stops short|\bcut\b|fades? out|music fades|falls away|drops? (?:to|out)|stripped|felt piano|pulse|alarm|flatline|tone\b|gavel|hammer|chord|harmony|hymn|choir|dance|waves|chime|beep|gasp|bluesy|cabaret|blowout|\blick\b|gaudy|game show|full band|voice and|(?:piano|cello|voice|harp|guitar|harmonica|strings) (?:alone|only)|unaccompanied|twang|accordion|wordless|impact|train-beat", re.I)
STAGING = re.compile(r"at the piano|from the piano|to the mirror|the party (?:freezes|moves)|lightbox|lights? snap|house lights|windows|leaves the piano|crosses to|cake|tray table|everyone knows|\bsing to\b|\bsings to\b|\bclaps\b", re.I)
DROP = re.compile(r"french horns|swelling strings|full strings|strings return|strings out|drops? to|stripped|voice and (?:piano|harmonica|steel|pedal steel|concertina|a lone)|piano and voice|(?:piano|cello) alone|slows|quiet\b|bridge|full band|full strings|key change|instrumental|operatic piano|snare roll|music thins|instruments fall away|the music (?:stops|swells|falls)|stop-time|the stomp stops|fantasy pops|sincere", re.I)
NAMES = re.compile(r"\b(?:THE |A |ANOTHER )?[A-Z][A-Z.'’]+(?: [A-Z][A-Z.'’]+)*\b")
def clean_dir(text):
    text = re.sub(r"\(#\d+\)|,? ?from #\d+|#\d+", "", text)
    sents = [s.strip() for s in re.split(r"(?<=[.;!?])\s+", text) if s.strip()]
    keep = [s for s in sents if MUSIC.search(s) and not STAGING.search(s)]
    out = []
    for s in keep:
        s = NAMES.sub(lambda m: short(VOICE[m.group(0).replace("’","'")]).lower() if m.group(0).replace("’","'") in VOICE else m.group(0).lower(), s)
        out.append(s.rstrip(".").strip())
    return re.sub(r";\s*;", ";", "; ".join(o for o in out if o))
def convert(stem, lyr):
    items = []
    for raw in lyr.splitlines():
        s = raw.strip()
        if not s: items.append(("blank",)); continue
        m = re.match(r"^\*\*([^*]+)\*\*\s*(?:\*\(([^)]*)\)\*)?\s*(.*)$", s)
        if m and not s.startswith("**END"):
            tag, sp = voice(m.group(1), m.group(2)); items.append(("sing", tag, sp, m.group(2) or ""))
            if m.group(3): items.append(("line", m.group(3)))
            continue
        m = re.match(r"^\*\((.*)\)\*$", s)
        if m:
            d = m.group(1); dl = d.lower()
            if items and items[-1][0] == "sing" and len(d) < 40 and (d.endswith("!") or d.endswith("?") or not MUSIC.search(d)):
                items.append(("line", f"({d})")); continue
            if dl.startswith("spoken") or dl.startswith("sung"):
                items.append(("mode", dl.startswith("spoken")))
                rest = re.sub(r"^(spoken|sung)[,;]?\s*", "", d, flags=re.I)
                if rest and MUSIC.search(rest): items.append(("dir", clean_dir(rest), rest))
                continue
            c = clean_dir(d)
            items.append(("dir", c, d))
            continue
        s = re.sub(r"\s*\*\([^)]*\)\*\s*", " … ", s).strip()
        items.append(("line", re.sub(r"\*([^*]+)\*", r"\1", s)))
    stanzas = []; cur = None; pre = []; spoken = False; singer = None
    for it in items:
        if it[0] == "line":
            if cur is None: cur = {"pre": pre, "lines": [], "spoken": spoken, "singer": singer}; pre = []
            cur["lines"].append(it[1])
        else:
            if cur is not None: stanzas.append(cur); cur = None
            if it[0] == "sing": spoken = it[2]; singer = it[1]
            elif it[0] == "mode":
                spoken = it[1]
                if singer: singer = re.sub(r"^\[(Spoken Word: )?", "[Spoken Word: " if spoken else "[", singer)
            if it[0] in ("sing", "dir"): pre.append(it)
    if cur: stanzas.append(cur)
    trailing = [p for p in pre if p[0] == "dir" and p[1]]
    def key(st):
        k = re.sub(r"[^a-z ]", "", st["lines"][0].lower()).strip()
        k = re.sub(r"^(?:and|so|but|well|oh|cause|now|then)\s+", "", k)
        return k[:40]
    counts = {}
    for st in stanzas: counts[key(st)] = counts.get(key(st), 0) + 1
    def ends(line, _st=None):
        return bool(re.search(r"[.!?…\"”)]$|—$", line.rstrip()))
    def last_line(st):
        ls = [l for l in st["lines"] if not l.startswith("(")]
        return ls[-1] if ls else st["lines"][-1]
    long_keys = {}
    for st in stanzas:
        if len(st["lines"]) >= 3: long_keys[key(st)] = long_keys.get(key(st), 0) + 1
    def is_ch(st):
        n = len(st["lines"]); k = key(st)
        if n >= 3: return counts[k] >= 2 and long_keys.get(k, 0) >= 1 and (long_keys.get(k, 0) >= 2 or counts[k] >= 2)
        return k in long_keys and long_keys[k] >= 1 and counts[k] >= 2 and len(k) >= 12
    N = len(stanzas)
    labels = [None]*N; seen_ch = False; vn = 0; cur_lab = None
    for i, st in enumerate(stanzas):
        n = len(st["lines"]); prev = stanzas[i-1] if i else None
        drop = any(p[0] == "dir" and DROP.search(p[2]) for p in st["pre"])
        cont = prev is not None and not ends(last_line(prev))
        ch = is_ch(st)
        later_ch = any(is_ch(s) for s in stanzas[i+1:])
        if i == 0: new = True
        elif cont and not drop: new = False
        elif cur_lab == "[Chorus]" and not ch and len(prev["lines"]) >= 4: new = True
        elif ch and cur_lab == "[Chorus]" and n < 3: new = False
        elif drop or ch: new = True
        elif n >= 4: new = True
        elif i == N-1 and st["spoken"]: new = True
        else:
            j = i + 1
            while j < N and not ends(last_line(stanzas[j-1])): j += 1
            new = (j < N and is_ch(stanzas[j]) and sum(len(s["lines"]) for s in stanzas[i:j]) <= 4 and cur_lab != "[Pre-Chorus]" and not st["spoken"])
        if not new: continue
        j = i + 1
        while j < N and not ends(last_line(stanzas[j-1])): j += 1
        run = sum(len(s["lines"]) for s in stanzas[i:j])
        if st["spoken"] and i != N-1: lab = "[Spoken Word]"
        elif ch and n < 3 and i + 1 < N and is_ch(stanzas[i+1]) and len(stanzas[i+1]["lines"]) >= 3: lab = "[Pre-Chorus]"
        elif ch: lab = "[Chorus]"; seen_ch = True
        elif i == N-1 and (st["spoken"] or (seen_ch and n <= 6)): lab = "[Outro]"
        elif drop and seen_ch and later_ch: lab = "[Bridge]"
        elif i > 0 and run <= 4 and j < N and is_ch(stanzas[j]): lab = "[Pre-Chorus]"
        else: vn += 1; lab = f"[Verse {vn}]"
        if lab == cur_lab and lab in ("[Outro]", "[Chorus]", "[Pre-Chorus]", "[Spoken Word]"): continue
        labels[i] = lab; cur_lab = lab
    out = ["[Intro]"]; last_voice = None
    first_dirs = [f"[{p[1]}]" for p in (stanzas[0]["pre"] if stanzas else []) if p[0] == "dir" and p[1]]
    out += first_dirs
    for i, st in enumerate(stanzas):
        block = []
        if i > 0:
            block += [f"[{p[1]}]" for p in st["pre"] if p[0] == "dir" and p[1]]
        if labels[i]: block = [""] + block + [labels[i]]
        v = st["singer"]
        if v and (v != last_voice or labels[i]):
            if v != last_voice: block.append(v)
            last_voice = v
        out += block + st["lines"]
    for p in trailing: out += ["", f"[{p[1]}]"]
    out += ["", "[End]"]
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip() + "\n"

def main():
    for act in ("Act One","Act Two"):
        (OUT/act).mkdir(parents=True, exist_ok=True)
        for f in sorted((ROOT/"Songs"/act).glob("*.md")):
            if re.search(r" \d+$", f.stem):
                print(f"skipping duplicate copy: {f.name}"); continue   # iCloud/Finder "name 2.md" copies
            try:
                t = f.read_text()
            except OSError as e:
                print(f"skipping unreadable file: {f.name} ({e})"); continue
            title = t.splitlines()[0].lstrip("# ").strip()
            num = re.search(r"\*\*(Act \w+ · #?\w+)\*\*", t).group(1)
            lyr = re.search(r"<!-- lyrics -->(.*?)<!-- /lyrics -->", t, re.S).group(1)
            lyrics = convert(f.stem, lyr)
            style, excl = STYLES[f.stem]
            md = [f"# {title}", "", f"**{num}** · Suno / Mozart AI version of `Songs/{act}/{f.name}`", "",
                  "## Demo style (Broadway pit)", "", "```", DEMO[f.stem], "```", "",
                  "## Full production style", "", "```", style, "```", ""]
            if excl: md += [f"**Exclude styles (Suno only; Mozart has no exclude box):** {excl}", ""]
            md += ["## Lyrics", "", "```", lyrics.rstrip(), "```", "",
                   "## Notes", "", f"- Lyrics: {len(lyrics):,} characters (the lyrics box holds 5,000). Style: {len(style)} characters (the style box holds 1,000).", ""]
            (OUT/act/f.name).write_text("\n".join(md))
            print(f"{f.stem:38} {len(lyrics):5}")
main()
