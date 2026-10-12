# AI prompts for Suno and Mozart AI

One file per number, mirroring the `Songs` folder. Each file has four parts:

1. **Demo style**: use this one for the musical's demo. Every one starts with "Broadway cast recording," and names only the instruments a real Broadway pit would use for that number: a band of about eight for most songs, piano and a string or two for the intimate ones, and a fuller pit with strings and brass for the big moments (Curtains Up, World, Alive in the Breeze, Break Me, the finale).
2. **Full production style**: the big, record-style version, for when you want the song as a single.
3. **Lyrics**: paste into the Lyrics box. The stage lyric, with the stage directions turned into tags the model can use.
4. **Notes**: character counts, which tag stands for which character, and tips for the hard ones.

**Jennifer's voice:** every demo style opens with the same line, "Theatrical female Broadway lead smooth alto vocal with clear, standard American diction." Keeping it first and identical is what keeps her sounding like one woman across the demo. The styles also describe each sound by its instruments rather than by genre names like "outlaw country," because the genre names pull in a twang.

**If a demo still comes out orchestral:** some lyric tags name big instruments, like `[French horns, swelling strings]` in Alive in the Breeze or the timpani and choir in The Crossing. Delete those tags for the demo; the model takes them as instructions. It also helps to describe only the instruments you want, since Mozart has no exclude box.

## How the lyrics are marked up

- **Section tags** like `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Interlude]`, `[Spoken Word]`, `[Outro]` and `[End]` give the model the song's shape.
- **Voice tags** like `[Female Lead (Jennifer)]` or `[Male Baritone (Hal)]` sit above whoever sings next. The words outside the parentheses are for the model; the character name inside is for you.
- **Spoken lines** are tagged `[Spoken Word: ...]`.
- **Production cues** in brackets, like `[Strings out; voice and piano]` or `[A gavel]`, come from the stage directions. Staging that a model can't hear (who crosses where, the lightbox, the chairs) has been left out.
- **Parentheses inside a lyric**, like `(Slow down!)` in Trainwreck, are backing vocals. That's how Suno reads them, so stage directions never use parentheses here.

## Limits

Mozart AI's lyrics box holds 3,000 characters, and the bracketed tags count toward it. Suno's current models allow 1,000 characters of style and, by most reports, 5,000 of lyrics. Every lyric here fits in one Mozart box (the longest is about 2,930 characters), and the longest style is about 400. Turns Out It's Genetic only fits because its bracketed tags are shortened; its Notes explain the short tags. ([Suno character limits](https://hookgenius.app/learn/suno-character-limits/))

## What the models won't do well

These are musical-theater songs, so several of them ask a lot of one AI generation:

- **Two women singing to each other** (The Party, We Take Turns, Hope, the finale). The model may blur the two voices. If so, generate the second voice as its own take.
- **A sudden change of style mid-song** (Silver Tongues' barbershop lawyers, The Mirror's minuet turning into a lullaby, Break Me's piano coda). Generate the odd section separately if the model refuses to switch.
- **Two melodies at once** (the end of Unspoken Cost). A model sings them one after the other.
- **Very long numbers** (The Crossing). Generate it in two parts.

## Keeping these in step with the show

These are copies made from the stage lyrics in `Songs/`. If you change a stage lyric, change it here too, or ask me to rebuild the folder. The scripts that made it are in `_tools`.
