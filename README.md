# I Left the Lights On

*A musical memoir in two acts, told by Jennifer from the piano, with help from the people she's lost and the people who stayed.*

Book, lyrics and music by Jessica Mulein. 41 numbers, about three hours with an intermission.

It's a true story with the names changed. A girl hides who she is inside a borrowed coat, loses a wife, loses her sons while she's sick, comes close to dying, and is carried back by a chosen family. It is funny in the places where it hurt most, because that's how she lived it.

## Synopsis

**Act One: The Coat.** Adopted into a polished, buttoned-up family, Jennifer knows who she is at eleven and spends years hiding it inside a borrowed coat. There's an accident in high school, a party where she first hears her name said out loud, a marriage to Leah, and two boys. Then she loses her grandmother Louise, and then Leah. She finds her birth father, Hal, and a family tree full of people like her, and a photograph leads her back to Nora, the friend she pushed away years before.

**Act Two: The Empty Chairs.** Her sons are taken while she's sick. Cancer brings her to the edge of a dark river and back. An insurance man watches from the edges, and a landlord keeps score. Through all of it, Nora and a growing table of found family carry her. She learns to leave the lights on for whoever comes home.

*Content note: death of a spouse and family members, serious illness, a psychiatric hospitalization, and losing children in a custody fight.*

## Read it

- **[I Left the Lights On - Libretto.pdf](I%20Left%20the%20Lights%20On%20-%20Libretto.pdf)**: the whole show as a formatted libretto, with a list of musical numbers.
- **[I Left the Lights On - Libretto.md](I%20Left%20the%20Lights%20On%20-%20Libretto.md)**: the same text in Markdown, readable right here on GitHub.

## Hear it

**[The demo site](https://lights-on-musical.pages.dev/)** has the whole show on one page: the synopsis, then the libretto from the prologue to the finale, with a player at every song and a download of the PDF. At the top is a house with a window for every number (Act One upstairs, Act Two downstairs, and the front door lit at the end). A song's window lights up once you've played it, and "Turn all the lights off" starts you over.

Every number has a rough demo recording, made with AI music tools (Mozart AI and Suno) from the prompts in `AI Prompts/`. They're sketches to show the shape of each song, not finished recordings, and not the sound the show is meant to have. The audio isn't stored in this repository; it lives on the demo site.

## Stage it

You're welcome to. The license (below) lets readings, schools, community theaters and nonprofit theaters put it up, trim it, cut it, reorder it and restage it. Before you do, read **About this story** at the end of [LICENSE.md](LICENSE.md): six things to keep, so that what happened still reads as what happened.

Some practical notes:

- **Names.** Every name is a stage name. JENNIFER is the narrator (YOUNG JEN and TEEN JEN are her younger selves; between 2001 and 2016 she's JEN, the in-between name she goes by in public). NORA is her wife, LEAH her late wife, OWEN and THEO her sons.
- **Doubling.** The ensemble is built to double. The Lawyers' actors also play the CREDITORS, three silent dark-coated figures who never speak. The ADJUSTER and the LANDLORD (with a real ledger) watch from the edges of Act Two.
- **Timing.** The show runs long as drafted. These rules take time out without cutting a word of story: intros of four bars at most; no fade-outs (every number ends on a button or segues into the next scene); instrumental breaks of eight bars at most, except the dance in *The Crossing*; and cut music before lyrics, since almost every repeated chorus changes words or carries the story.
- **Style.** Sing it in the moment. Only Jennifer, in the present, gets to look back. The lyrics are written for human range, with places to breathe, and for an audience that hears each line once.
- **Nothing is borrowed.** No lines from other people's songs appear in the show.

## What's here

- **`Script/Act One.md`, `Script/Act Two.md`**: the book: scenes, dialogue and stage directions. A line like `{{song: 01 - Trainwreck}}` marks where a number goes.
- **`Songs/Act One/`, `Songs/Act Two/`**: one file per number, named by its place in the show. Each has a header (who sings it, status, the plan), the stage lyric between `<!-- lyrics -->` and `<!-- /lyrics -->`, and notes for the composer.
- **`AI Prompts/`**: a tagged lyric and a style prompt for each number, ready to paste into Suno or Mozart AI (see its own README).
- **`build_libretto.py`**: stitches the script and the stage lyrics into the libretto Markdown file. Don't edit the libretto directly; it's overwritten on every build.
- **`build_pdf.py`**: the same libretto as a PDF, with a title page, a list of numbers with page numbers, and each act starting on a new page. Needs [pandoc](https://pandoc.org) and XeLaTeX (on a Mac: `brew install pandoc` plus BasicTeX or MacTeX).
- **`build_site.py`**, **`site_src/`**: build a single-page demo website (the libretto with a player at every song, and a house of 41 windows that light up as you listen). It expects the demo audio next to the songs, which isn't included here. Needs the `markdown` package (`pip3 install markdown`).
- **`deploy_site.sh`**: builds the site and uploads it to Cloudflare Pages in one step (`./deploy_site.sh`). You'll need your own Cloudflare account and project name; edit the script to match.
- **`Synopsis.md`**: the synopsis shown at the top of the site.

To rebuild after editing: `python3 build_libretto.py`, then `python3 build_pdf.py`.

## Song registrations

Every number is registered with ASCAP (Mulein Studios). The same table is printed at the back of the libretto, for theaters that need work IDs for performance reports and cue sheets.

| # | Song | ASCAP work ID |
|:--|:-----|:--------------|
| P | I Left the Lights On (Prologue) | 940070363 |
| 1 | Trainwreck | 940102965 |
| 2 | The Mirror | 940103031 |
| 3 | Louise | 940103063 |
| 4 | Thirteen | 940103074 |
| 5 | Keep Clear | 940103097 |
| 6 | The Notebook | 940103124 |
| 7 | Road Less Traveled | 940103146 |
| 8 | June Snow | 940103167 |
| 9 | The Party | 940103192 |
| 10 | Giving Up | 940103211 |
| 11 | Leah and the Boys | 940103239 |
| 12 | Another Night | 940103260 |
| 13 | Fluorescent Moon | 940103280 |
| 14 | Ghost in the Machine | 940103304 |
| 15 | The Winter Coat | 940103309 |
| 16 | Ruth's Blessing | 940103313 |
| 17 | Sport Coat at the Door | 940103336 |
| 18 | Turns Out It's Genetic | 940103363 |
| 19 | The Photograph | 940103388 |
| 20 | Small Euphorias | 940103414 |
| 21 | Curtains Up, World | 940103436 |
| 22 | Open Source | 940103475 |
| 23 | Silver Tongues | 940103502 |
| 24 | Frozen in the Light | 940103525 |
| 25 | Good Grief | 940103561 |
| 26 | Spy in the Boys Club | 940103998 |
| 27 | Javert in a Cubicle | 940104029 |
| 28 | Alive in the Breeze | 940104048 |
| 29 | The Crossing | 940104072 |
| 30 | Six Month Bites | 940104101 |
| 31 | Fine, How Are You? | 940104116 |
| 32 | Lawyer Up, Hit the Gym | 940104131 |
| 33 | We Take Turns | 940104144 |
| 34 | Hope | 940104166 |
| 35 | Before I Broke | 940104180 |
| 36 | Break Me | 940104201 |
| 37 | Highly Capable | 940104215 |
| 38 | Unspoken Cost | 940104226 |
| 39 | Carry Me | 940104269 |
| 40 | I Left the Lights On (Finale) | 940104317 |

## License

Book, lyrics and music © 2026 Jessica Mulein, under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), plus extra permissions to trim, cut, reorder and restage, and to charge admission for readings, schools, and community and nonprofit theater. Professional or commercial productions need permission. The details, and what I ask you to keep, are in [LICENSE.md](LICENSE.md).

The demo recordings were made with AI music tools, and their use may also be governed by those tools' terms.

## Contact

Jessica Mulein: jessica@mulein.com

*The world is responsible for keeping my light on.*
