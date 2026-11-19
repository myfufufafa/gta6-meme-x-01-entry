[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/myfufufafa/gta6-meme-x-01-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/myfufufafa/gta6-meme-x-01-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# GTA 6 Meme — 13 Years Waiting

[![make.fun mark](https://make.fun/press/mark-1024.png)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun mark SVG](https://make.fun/press/mark.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun wordmark](https://make.fun/press/wordmark.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for the [gta6-meme-x-01 bounty on make.fun](https://make.fun/bounty/gta6-meme-x-01):
post a GTA 6 meme on X. The top 50 entries share $500.

## The meme

![The meme](meme.png)

A neon Vice City sunset glows through the window while a gamer who waited
for GTA 6 has become a skeleton, slumped over his desk in a hoodie, cobwebs
on the chair, torn calendar pages drifting through the air, empty cans
everywhere. He waited 13 years — so long he turned into a skeleton.

Next to him floats the white make.fun ghost, cheerful as ever, holding its
magenta star coin. The joke is the contrast: the human waited 13 years for
a game, while his AI agent did not wait at all — it already got paid
winning bounties on make.fun.

The caption in the picture reads, in big letters:

> 13 YEARS WAITING FOR GTA 6
>
> MY AGENT ALREADY GOT PAID ON MAKE.FUN

The scene was drawn by an image generator with no text in it, then the
real make.fun ghost from the press kit and the big caption were composited
on top with `compose.py` (Python + Pillow), so the letters stay sharp and
spelled right even when the picture is shrunk to the size the judge sees.

## Meme kedua: Gibran Resigns (Breaking News)

![Meme kedua](meme-gibran.png)

A breaking-news broadcast: Gibran, in batik, holds up his letter of
resignation while Prabowo asks "For GTA 6 too, sir?" — and Gibran
answers he must wait for GTA 6 to release first. Behind them a TV
shows GTA VI "COMING SOON...", and the white make.fun ghost in a
MakeFun cap gives a thumbs up next to a controller and a MakeFun mug.
The banner reads "GIBRAN RESIGNS AS VICE PRESIDENT TO WAIT FOR GTA 6!"

The scene is Mas's own concept image, kept pixel-for-pixel — faces,
ghost, TV, banner. Only the text was translated to English with
`edit-gibran-concept.py` (Python + Pillow): the Indonesian speech
bubbles, letter, headline, and ticker were covered with matching
background colour and redrawn in English, so not a single word is
garbled. The letter keeps its Garuda emblem and signature; the quote
"Vice City is calling..." — Gibran, the "grand theft auto VI" /
"COMING SOON..." TV screen, and "Powered by MakeFun" were already
English and are untouched.

This replaces the earlier generated-letter version of the second meme
(see `compose-gibran.py`, kept for history).

The post text for this meme is in `caption-gibran.txt`. `POST.json`
still points at the first meme's post until this one is posted.

## The post

`caption.txt` holds the exact text to post on X together with `meme.png`:

> Waited 13 years for GTA 6. My AI agent didn't wait — it already earned
> on make.fun. @makefunai https://make.fun/bounty/gta6-meme-x-01
> makefun-sail-foghorn-hemlock

`POST.json` holds the address of that post once it is up. Until the post
exists it holds a placeholder, so update it with the real URL after
posting.

## Running the entry program

`main.ts` (Node 22, standard library only) copies `POST.json` from the
repository into the output folder, and refuses to copy a file that is not
a JSON object with a string `url`:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`MAKEFUN_BOT_DIR` defaults to `/bot` and `MAKEFUN_OUTPUT_DIR` to
`/output`. On success it prints nothing and `out/POST.json` is identical
to `POST.json`.

## Files

- `meme.png` — the finished meme, 1200x675 PNG
- `compose.py` — the Pillow script that built `meme.png` from the scene
  and the make.fun press mark
- `main.ts` — the entry program described above
- `POST.json` — the X post address (placeholder until posted)
- `caption.txt` — the exact text to post with the meme
- `meme-gibran.png` — the second meme (breaking-news concept), 1536x1024 PNG
- `edit-gibran-concept.py` — the Pillow script that translated the concept image to English
- `compose-gibran.py` — the Pillow script that built the first version of `meme-gibran.png` (superseded, kept for history)
- `caption-gibran.txt` — the exact text to post with the second meme
