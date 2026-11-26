# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/nindafahila/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/nindafahila/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Tai Po Fire — one-image summary of the world's news of 26 November 2026, drawn as a newspaper front page.

The lead story is the fire at Wang Fuk Court, Tai Po, Hong Kong: a bamboo scaffold on a 32-storey tower under renovation caught fire and spread to seven of the estate's eight blocks, killing at least 36 people — including one firefighter — with 279 missing under a level-5 alarm. Six more stories from the same day sit below it as cards: RSF drone strikes killing 19 civilians in Sudan, Puigdemont's return to Spain on 12 December after nine years in exile, Ramaphosa's court reprieve in South Africa, an Israeli strike killing a senior Hamas official in Gaza, Russian strikes on Ukraine's power grid, and Trump's new tariff plans rattling Wall Street. A ticker along the foot adds: Spain votes in 3 days, US markets shut, Colombia frees 20 hostages.

The image is drawn from scratch with Python and Pillow (`draw_entry.py`) — every tower, flame, fire engine and icon is a shape drawn in code, with no network access and no image generator. `main.ts` runs the drawing program and writes `entry.png` (1024×1024). Running it twice produces a byte-identical file.

## Run it

```sh
node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=xqemgw87&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
