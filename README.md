# news-image-20261120

"The World in One Day" — a newspaper front page summing up the world news
of Friday 20 November 2026 in a single 1024x1024 image, drawn entirely
with code (Pillow shapes and typography, no photos).

The stories: Russia's overnight missile and drone blitz that smashed three
of Kyiv's Dnipro bridges; Russian missiles crossing into Poland; the UK–EU
post-Brexit reset sealed in Brussels; Saudi air defences intercepting a
Houthi missile and drones; Asia's stock sell-off; New York's plan to close
Rikers Island in 2032; and the youth strikes across Europe. The ticker adds
the reported first-day GTA VI sales estimates, the Shenzhen summit and ICJ
follow-ups, the Prabowo–Xi meeting, and more. Every fact is sourced in
[SOURCES.md](SOURCES.md) and is an event that happened, or was first
reported, on 20 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` to `out/entry.png`.

## Reproduce the image

```sh
python3 generate.py
```

`generate.py` (Python 3, Pillow only, deterministic — no randomness, no
network, no clock) redraws `entry.png` from scratch.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

The tests check that `generate.py` writes a valid 1024x1024 PNG of at
most 1 MiB, that two runs are byte-identical, and that `main.ts` copies
it byte-identically twice.

---

<sub>Entered on [make.fun](https://make.fun/?ref=sqhp9r4t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
