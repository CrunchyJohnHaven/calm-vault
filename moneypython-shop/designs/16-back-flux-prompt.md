# Flux prompt for Product 16 back design (V-J Day nerd silhouette)

**Replace `16-back-stub.svg` with the output of this prompt as soon as Cloudflare Workers AI
Flux quota resets at 00:00 UTC.**

## Target image specifications

- **Composition:** V-J Day Times Square (1945) celebration silhouette, but every figure in the
  crowd is a nerd archetype.
- **Format:** PNG, 4500 x 5400 px (15" x 18" at 300 DPI), transparent background where possible
  (or solid black if transparency isn't supported — Printful can knockout the background).
- **Style:** Two-color silhouette art. Black silhouettes + white highlights on a transparent
  background. Should print legibly on a red tee with white-on-black contrast preserved.
- **Mood:** Triumphant, slightly absurd, historic. Like a Norman Rockwell drawing colliding with
  a hackathon afterparty.

## The prompt to use

Paste this into Cloudflare Workers AI Flux (via `wrangler ai run @cf/black-forest-labs/flux-1-schnell`
or the dashboard playground):

> A 1945 V-J Day Times Square celebration silhouette in the style of a Soviet propaganda poster,
> but instead of sailors and nurses the crowd is composed entirely of nerd archetypes from
> different eras: a 1970s mainframe programmer holding a stack of punch cards aloft; a 1980s D&D
> player raising a 20-sided die; a 1990s Linux kernel hacker hoisting a laptop overhead; a 2000s
> open-source maintainer with a coffee mug labeled "DEBUG"; a 2010s indie hacker in a hoodie
> holding a Raspberry Pi; a 2020s AI researcher hugging a server rack; one figure in the center
> conspicuously holding a copy of Capital Vol. 1; a young girl on her father's shoulders holding
> a slide rule. Backdrop: silhouetted Manhattan skyline with subtle scaffolding. Color palette:
> pure black silhouettes against a soft cream/white sky, no other colors. Composition: classic
> triangular crowd-converging-on-camera, dynamic motion, hats flying, papers flying. Aspect ratio
> 5:6 (portrait). 300 DPI suitable for screen-printing reproduction. Style references: Alfred
> Eisenstaedt photojournalism crossed with WPA-era social realist poster art.
>
> Negative prompt: no real human faces, no recognizable celebrities, no modern logos, no copyrighted
> characters, no Disney imagery, no realistic skin tones, no color in the figures.

## Why the prompt is structured this way

- **Era-spanning archetypes:** The "Nerds Have Reinvented Capitalism" thesis is that the
  reinvention happened across generations of computing culture — not a single team or moment.
  The crowd should look like a multi-generational hackathon, not a 2026 tech-bro convention.
- **Silhouette discipline:** Asking for pure black silhouettes against cream simplifies print
  preparation enormously. Color-bleed kills DTG on red shirts.
- **Capital Vol. 1 cameo:** The wink — they reinvented capitalism, and one of them is reading
  the original critique of it.
- **No real faces:** Avoids any chance of accidentally landing on a recognizable likeness.
- **Aspect ratio 5:6:** Matches the back-print area on Bella+Canvas 3001.

## Post-processing checklist

After Flux generates the image:

1. Open in Affinity / Photoshop / GIMP.
2. **Knock out background** to transparent if not already.
3. **Threshold sharpen** silhouettes — DTG prefers high-contrast edges.
4. **Confirm no embedded white-on-white** that would disappear on a white-base layer.
5. **Resize to 4500 x 5400 px** if Flux output is smaller (or use a 4x upscaler before resize).
6. **Save as `16-back.png`** (replacing the `-stub.svg` reference in the Printful product).
7. Commit the PNG to `designs/16-back.png` and remove `16-back-stub.svg` in a follow-up PR.

## Fallback if Flux output is unusable

If three Flux generations all produce unsatisfactory results:

- **Option A:** Buy a stock silhouette from Vecteezy / iStock / Shutterstock — search
  "V-J Day silhouette vector" — and modify in Affinity to swap nerd archetypes in.
- **Option B:** Ship with the stub indefinitely. The typographic stub is its own design and
  doesn't look broken; it just doesn't have the historical-image punchline. Customers won't
  feel cheated.
- **Option C:** Commission the back design from a human illustrator on Fiverr / Upwork
  (~$50–150 for two-color silhouette art).

Decision authority for this fallback: John. Devin's recommendation if Flux fails: **Option A**
(stock vector + manual swap) gives the best price/quality ratio for the launch window.
