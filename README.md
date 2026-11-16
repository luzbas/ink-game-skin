# Ink Wheel

A Video.js v10 skin (React, CSS) whose controls live on a painted sumi-ink wheel, like a game's radial menu.
Black ink, warm paper (#EDE8DF) and one vermillion accent (#D9472B), set in IM Fell English SC and Inter.

## How it works

- **Wheel.** Nine slots around an ink disc: Play/Pause, Rewind 10, Skip 10, Volume, Captions, Chapters, Speed,
  Mini player and Fullscreen. Clicking a slot acts at once and moves the highlight; the slots never rotate. The hub
  says what the highlighted slot does.
- **Timeline ring.** The outer ring is the timeline, split by chapter gaps, with a seal knob at the playhead. Grab it
  anywhere and turn: it scrubs from the current time, one full turn is the whole video, and it turns smoothly from chapter
  to chapter (crossing a boundary clicks, and buzzes on phones that can). Scrolling over the wheel does not turn it.
- **Volume dial.** With Volume highlighted, the ring becomes a 300° dial (0–100). Click Volume again to mute; any
  other slot or Esc brings the timeline back.
- **Chapter cards.** Chapters open as paper cards on a 3D carousel over an ink pool, with a frame from each chapter
  (from the storyboard track, when there is one). Swipe, use the arrows or the arrow keys; the front card plays.
- **Ink effects.** Animated sprite strips for play, pause, seeking, slot presses, scrubbing, volume, mute, the wheel
  opening and a card dissolving. Turned off for `prefers-reduced-motion`.

## Layouts

The skin reads the video's shape from its metadata (`data-orientation` on the stage) and the room it has:

| Video | Wide player (≥ 640 px, or a landscape screen in fullscreen) | Narrow player |
| --- | --- | --- |
| Wide (16:9) | `overlay`: medium wheel bottom-right while playing; full wheel in the middle on pause | `stack`: video, a title strip, then the full wheel |
| Tall (9:16) | `side`: video in the middle over a blurred copy of itself, info left, wheel right | `tall`: video fills the player, wheel as in `overlay` |

Pass `orientation="portrait" | "landscape"` to `VideoSkin` to skip the detection.

## Keys

The usual Video.js hotkeys (Space/K, J/L, arrows, M, C, F, I, 0–9, < >), plus `[` and `]` for chapters and Esc to step
back out. On the wheel the arrow keys move between slots (one tab stop) and turn the focused ring (Page Up/Down jump a
chapter).

## Art

`src/assets` holds the painted pieces and `src/assets/fx` the effect strips, all made with Melius (GPT Image 2.6
Sunburst and its GIF model) from one approved style sheet and keyed to transparent WebP. `assets/` keeps the keyed
masters (PNG and WebP) and the effect sprite sheets. `design/melius` has the style sheet, contact sheets of the
generations, the effect GIFs and the keying scripts (`cutout.py`, `fxkey.py`); the full-size raw generations stay in
the Melius project.

## The demo

`app/App.tsx` plays the skin full-window over the reveal trailer of *Nine Strokes*, a concept game made for this skin:
15 seconds, five chapters, English captions, streamed from Mux (HLS) with a Mux storyboard for the chapter-card frames.
The chapters and captions tracks are in `public/nine-strokes/`; the trailer's keyframes and timing notes are in
`design/nine-strokes/`.

To use the skin with your own video, put a `VideoSkin` inside a `VideoPlayer` around any Video.js media element and
give it a chapters track (and, for the card frames, a thumbnails track such as a Mux storyboard).

## Working on it

```sh
npm install
npm run dev       # http://localhost:5173 — add ?shape=tall to preview the tall layouts
npm run build     # type-checks, then builds the demo page into dist/
npm run lint
```

- `src/` is the skin itself (it imports its own modules with the `@/` alias, set in `vite.config.ts`). The entry is
  `src/video/skin.tsx`, which exports `VideoSkin`.
- `app/` is the demo page.
- `design/` is the art sources and the trailer notes; it is not part of the build.

## Deploying to Vercel

Import the repository in Vercel; `vercel.json` sets everything (Vite, `npm run build`, output in `dist/`, every path
served by `index.html`). No environment variables are needed.

## License

Apache License 2.0 — see `LICENSE`.
