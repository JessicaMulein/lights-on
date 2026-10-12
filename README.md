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

Every number has a rough demo recording, made with AI music tools (Mozart AI and Suno) from the prompts in `AI Prompts/`. They're sketches to show the shape of each song, not finished recordings, and not the sound the show is meant to have. The audio isn't stored in this repository; it's hosted separately.

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
- **`build_site.py`**, **`site_src/`**: build a single-page demo website (the libretto with a player at every song, and a house of 41 windows that light up as you listen). It expects the demo audio next to the songs, which isn't included here.
- **`Synopsis.md`**: the synopsis shown at the top of the site.

To rebuild after editing: `python3 build_libretto.py`, then `python3 build_pdf.py`.

## License

Book, lyrics and music © 2026 Jessica Mulein, under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), plus extra permissions to trim, cut, reorder and restage, and to charge admission for readings, schools, and community and nonprofit theater. Professional or commercial productions need permission. The details, and what I ask you to keep, are in [LICENSE.md](LICENSE.md).

The demo recordings were made with AI music tools, and their use may also be governed by those tools' terms.

## Contact

Jessica Mulein: jessica@mulein.com

*The world is responsible for keeping my light on.*
