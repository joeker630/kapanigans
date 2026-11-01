# Kapanigans art inventory

Every finished image, where it lives and whether the game uses it yet. Updated Nov 1, 2026.

- **In game** = `index.html` already loads it.
- **Ready, not wired** = the file exists; the game doesn't use it yet. This is the main build's to-do list.
- All repo art is transparent WebP, listed with prompts and sizes in `art/manifest.json`.
- Isometric sprites face the bottom left. Mirror them for the other direction.

## 1. Farm sprites: `art/iso/farm/` (isometric style)

### Animals: 4 poses each (stand, eat, sleep, back)
| Files | Status |
|---|---|
| `hen/`, `cow/`, `pig/`, `sheep/` × `stand` `eat` `sleep` `back` | In game |
| `sheep/sheared` (after wool is collected) | In game |

### Crops
| Files | Status |
|---|---|
| `carrot/` and `pumpkin/` × `sprout` `growing` `ripe` | In game |
| `tomato/`, `corn/`, `strawberry/` × `growing` `ripe` (sprout: reuse `carrot/sprout`) | In game |
| `seeds/` × `carrot` `tomato` `corn` `pumpkin` `strawberry` (seed packets) | In game |

### Goods, food, tools
| Files | Status |
|---|---|
| `goods/egg_white`, `goods/milk`, `goods/wool` | In game |
| `goods/egg_brown` (for the Big "sort eggs by color" puzzle; sizes in code) | **Ready, not wired** |
| `food/hay`, `food/slop`, `food/feed` | In game |
| `food/corn` (corn pile, the Feed puzzle's CORN choice) | **Ready, not wired** |
| `tools/wateringcan` (white, tint in code) | In game |
| `tools/bucket` (empty bucket, co-op milking) | **Ready, not wired** |
| `tools/basket` (harvest basket) | **Ready, not wired** |
| `hide/haypile`, `hide/bush` (egg-hunt hiding spots) | **Ready, not wired** |

### Buildings: `bld/` (named after `STRUCT` keys; `barn` uses `store`)
| Files | Status |
|---|---|
| `stand` `board` `fbasket` `bank` `store` `coop` `pen` `shed` `stable` | In game |
| `fence` (straight piece), `fencecorner` (L corner); mirror for other directions | **Ready, not wired** (the pasture fence is still drawn in code) |

### Decorations: `decor/` (named after `DECOR` keys)
| Files | Status |
|---|---|
| `flowers` `sunflower` `lantern` `bench` `mailbox` `tree` `beehive` `pond` | In game |

### Older chunky 3D set: `art/farm/`
`hen` `cow` `pig` `sheep` `carrot` `pumpkin`: the first test batch. Superseded by `art/iso/farm/`, so it's safe to ignore.

## 2. Avatar parts: `art/avatar/` (isometric style)

Every file is a 320×320 full-frame layer at the same position. Stack them in this order: `base` → outfit → feet → face hair → hair → glasses → hat → bow. Parts marked white in `tools/batches/avatar1.json` are tinted in code.

| Group | Files | Status |
|---|---|---|
| Body | `base` (skin recolored in code) | In game |
| Hair (10) | `hair/` pigtails short curly ponytail bun braids long spiky bob buzz | In game |
| Hats (7) | `hat/` straw cap bonnet flowercrown beanie cowboy crown | In game |
| Outfits (6) | `outfit/` overalls dress shirt apron bandana raincoat | In game |
| Feet | `feet/rainboots` | In game |
| Face hair (4) | `facehair/` mustache beard goatee stubble | In game |
| Glasses (3) | `extra/` glasses squareglasses sunglasses | In game |
| Bow | `extra/bow` | In game |

## 3. Bedtime Story test art: `art/story/test/` (storybook film style)

**Waiting on Joe's picks.** Each subject has 2 versions (`_v1` = A, `_v2` = B). Don't wire these in until Joe chooses; the picks then become the style reference for the full library (backlog #14).

| Subject | Kind |
|---|---|
| `bg_forest`, `bg_bedroom` | 1536×1024 backgrounds, for the `forest` and `bedroom` scene slots (`art/story/bg/<id>.webp`) |
| `puppy` `owl` `dragon` `unicorn` `firefighter` `police` `rocket` `chest` | 768px character and prop cutouts |
| `page_owl`, `page_dragon` | 1536×1024 full illustrated pages |

## 4. Family likeness art: private, NOT in the repo

Stored only in the family's Firebase space: `families/<code>/art/family/<person>/<name>`
= `{img: "data:image/webp;base64,…", w, h, kind, key, style: "storybook", t}`, about 35 KB each, 768px, transparent cutouts.

| Person | Files (41 each) | Status |
|---|---|---|
| `joe` | `master`, `pose_<key>` × 30, `outfit_<key>` × 10 | Ready; the story builder already reads this path |
| `violet` | same 41 names | Ready |

- **Pose keys:** front threequarter side back wave run jump sleep yawn story laugh think surprised point thumbsup hero karate pillowfight sit cheer sneak dance hug gift cook highfive sad peek plant fly
- **Outfit keys:** farmer pajamas astronaut firefighter chef pirate wizard superhero winter beach
- `story` (armchair and lamp) and `plant` (grass patch) include a small prop.
- Most are full body; a few outfits are head and shoulders: Joe's astronaut and superhero, Violet's astronaut, firefighter and winter.
- Read one person's folder only when it's needed, never the whole `art` tree.

## Not made yet

- **Farm Batch C (11):** shop extras: scarecrow, windmill, flower pot, plus copper, silver and Moolah coins and a fertilizer bag (backlog #3).
- **Jeppson the corgi (#17):** waiting on his photo.
- **Avatar extras:** hoodie, pumpkin and chicken costumes, pets, back views (#10).
- **Fairy Garden art:** see the project's `fairygardenartspec.md`.
