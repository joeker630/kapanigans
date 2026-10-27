# Kapanigans Backlog

Status key: 🆕 new · 🔍 needs decisions · 🛠️ in progress · ✅ done

Levels used below: **Little** = Violet level (age 3), **Big** = Quinn level (age 6).

---

## 1. ✅ New game: Write a Bedtime Story

A fill-in-the-blanks (mad-libs style) bedtime story that one child makes as a **gift** for another child, with simple characters they draw that get gentle animations.

**How it plays**
1. The author picks who the story is for (any other player).
2. The author picks a story template (for example "The Sleepy Dragon", "The Moon Picnic" or "The Lost Teddy").
3. The author fills in the blanks:
   - **Little:** picks from big picture buttons (an animal, a color, a food, a place), with no reading needed. Each choice reads aloud.
   - **Big:** picks from word lists or types a word, with blanks labeled by type (a silly word, an animal, a place).
4. The author draws 1–3 characters on a small canvas, using the same tools as Color Together for their level.
5. The app adds a basic animation to each character, such as bob, hop, wiggle, float, slow spin, or "sleepy" (gently shrinks with zzz).
6. The author taps **Send gift**. The other child gets a wrapped-present notification and opens a page-by-page story, with the characters animating and each page read aloud.

**Story player**
- One page per scene, with big next/back arrows and an auto-play option.
- Read aloud with the device's built-in voice (works offline on iPad and iPhone). Words highlight as they're read for Big readers.
- Calm bedtime look: a dark blue night palette, stars and a dimmed screen.
- "Thank you" reactions go back to the author (❤️, 😴, 🤗).

**Acceptance criteria**
- [x] At least 3 story templates, each with 5–8 blanks and 4–6 pages (The Sleepy Dragon, The Moon Picnic, The Lost Teddy)
- [x] Little authors can finish a story without reading anything (picture choices, everything read aloud)
- [x] Drawn characters appear on the story pages with at least 4 animation types (bob, hop, wiggle, float, spin, sleepy)
- [x] The gift arrives on the recipient's device even if they weren't online when it was sent (saved in Firebase, delivered to their Inbox)
- [x] "My stories" shelf to rewatch received stories, the same on every device
- [x] Thank-you reactions (❤️ 😴 🤗) go back to the author, even if they're offline

**🔍 Decisions needed**
- ~~Where gifts are stored~~ → decided: Firebase (see Shared groundwork). Gifts land in the recipient's **Inbox** (#4).
- ~~Can grown-ups send stories too?~~ → yes, already works: every persona can make and send stories.
- ~~Record your own voice?~~ → ✅ built: after picking moves, choose "I'll read it!" and record each page (up to 30 s). Pages you skip use the reading voice. The reader shows "🎤 read by …".

---

## 2. ✅ New persona: Grown Ups

Add grown-up players to the **Who's playing?** screen.

**Names:** Joe, Layla, Lisa, Parker, Apple G, Uncle Jeff, Gramma Mia, Grandpa George

**Details**
- All grown-ups get **Big (Quinn level)** tools for now.
- They count as a player seat (still 4 players max per game) and show up in the lobby, seat chips and zone labels like the kids do.
- Each grown-up gets their own emoji avatar and color.
- Layout: the kids stay big at the top, with a smaller **Grown ups** row underneath so kids don't tap the wrong one.
- Video chat rule stays the same: it turns on when exactly 2 players are in a game, including a grown-up and a kid. This lets Gramma Mia color with Violet over video.

**Acceptance criteria**
- [x] All 8 grown-ups are selectable and remembered per device, like the kids
- [x] Grown-ups get Quinn-level tools in Color Together
- [x] Bear friend and Fox friend stay available

**🔍 Decisions needed**
- ~~Photos instead of emoji~~ → ✅ built: Grown-ups › Photos lets you choose a photo or snap one from the live camera for each person; it replaces their emoji everywhere until custom avatars (#10) arrive.
- Should grown-ups get a separate "grown-up level" later, such as with hints turned off or as a game host?

---

## 3. 🛠️ New game: Kapanigan Farmstand

A **live co-op farm** the kids share. Every farm action is done by solving a short, age-appropriate puzzle. Goods are sold at the farmstand for **Moolah**, which buys farm upgrades and new clothes for Fashion Show (#5). Family members place **orders** sized to each kid's age.

**The loop:** puzzle → farm action → goods → sell or fill an order → Moolah → build the farm or buy clothes → bigger farm, more chores.

### ✅ Built so far
- **v1 field:** an isometric farm where the hen, cow, pig and sheep wander, graze and nap, with walk (front and back), eat and sleep animations. Tapping an animal feeds it, tapping a sleeping one wakes it, and tapping the grass calls the nearest animal over. Carrot and pumpkin plots grow from sprout to ripe in about 36 seconds, and a ripe one can be tapped into the basket. Runs on this device only; nothing is saved yet.
- **v1.1 (Oct 27):**
  - The map is **16 × 16 tiles** (was 8 × 8). About 9 tiles fit across an iPad, and the farm fills the height of an upright phone. Drag to look around.
  - Animals stay inside a fenced **pasture** (a dashed line until fence art exists). Crops are in their own **field**.
  - Animals walk at about a third of the old speed, take short strolls, and spend most of their time grazing (6–10 s) and napping (12–20 s).
- **Puzzle engine (Oct 27):** all 8 puzzle types below are built, each with a Little and a Big version. Feeding an animal and picking a ripe crop now open a puzzle; the action happens when it's solved. See **✅ Puzzle engine** below.
- **v2: one family farm (Oct 27):**
  - **Saved in Firebase** at `families/<code>/farm` and the same on every device. Plots, animals, buildings and decorations are shared; Moolah, goods and orders are per person.
  - **Every action is a puzzle** through `farmDo()`, which wraps the engine's `farmPuzzle()`:
    - plant, water and harvest crops
    - feed animals, then collect eggs, milk the cow and shear the sheep
    - sell at the farmstand, build at the Farm Store, and pack an order
    - backing out of a puzzle changes nothing; seeds, animals, fertilizer and decorations are plain purchases with no puzzle
  - **Crops:** plant (pick a seed, optionally with fertilizer) → water → sprout → growing → ripe → pick.
    - Grow times: carrot 2 min, tomato and strawberry 3, corn 4, pumpkin 6. Fertilizer halves the time and gives 2.
  - **Animals:** feed, then the hen lays an egg (1 min), the cow makes milk (2 min) or the sheep's wool grows (3 min); tap to collect.
    - The sheep shows sheared until its wool grows back. Feeding the pig gives hearts and a 1 Moolah tip.
  - **Gentle droop, never loss:**
    - A crop not watered within 2 minutes droops, and a ripe crop left 30+ minutes droops a little.
    - An animal not fed for 20 minutes gets hungry, looks faded and walks slowly.
    - Nothing dies and nothing is lost. Bubbles show what's needed (💧, the animal's food, a ready 🥚 🥛 🧶, 🌱 on empty plots).
  - **Farmstand** (counter by the path): tap a good to sell one; Big also gets "Sell everything".
    - Prices: carrot and egg 1; tomato, strawberry and corn 2; milk and wool 3; pumpkin 5.
  - **Moolah jar per person** (🪙 button). **Gift** 1, 5, 10 or 25 Moolah to anyone in the family; they get a 🪙 note in their Inbox.
  - **Farm Store** (red barn):
    - seeds for tomatoes 10, corn 15 and strawberries 20
    - a bigger field (+3 plots, up to 18): 15, 25, 40 and 60
    - a wooden fence and bigger pasture 20, and fertilizer 3
    - chicken coop 15 (+3 hens), pig pen 20, sheep shed 30 and stable 40 (+2 each)
    - new animals: hen 5, pig 12, sheep 15, cow 25, only if there's room
    - 8 decorations, 3–20
  - **Order board** (📋): each person always has up to 3 orders from family members. A new one comes 4 minutes after one is delivered.
    - Little: 1 kind of good, 1–3 of it, pictures only, read aloud.
    - Big: 2–3 kinds, up to 6 each, written out with how many you have. Some have a "+3 by <time>" bonus.
    - Orders pay about 1.5× the farmstand price, and the family member sends a 💛 thank-you to the Inbox.
    - Grown-ups can **write an order** for Violet or Quinn.
  - Buildings, the farmstand, the board and decorations are drawn in code (boxes and emoji) until the Batch B art exists. Crops without art yet (tomato, corn, strawberry) show their emoji.
  - Testing: `?farmlocal` runs the farm in memory, without Firebase.
- **v2.1 (Oct 27):**
  - **Farmer avatars:** everyone on the farm walks around as their own farmer, and everyone sees everyone live with name tags.
    - The placeholder sprite is drawn in code: straw hat, overalls in the person's color, and their photo or emoji as the head. It has front and back views and walk and idle animation.
    - Tapping a crop, animal, building or decoration walks your farmer there first, and the puzzle starts when they arrive. An animal waits while you walk to it, and tapping grass just walks there.
    - A 🧩 bubble shows over anyone doing a puzzle, and the camera follows your farmer.
    - Synced at `families/<code>/farmwalk/<who>`, one record per walk (from, to, start time, speed), removed when the device drops.
    - Real isometric avatar art is part of #10, which is waiting on the art credentials.
  - **Zoom:** pinch, mouse wheel, or the ➕ ➖ buttons, zooming around the finger. It goes from the whole farm on screen to 2.5×.
  - **Camera and mic on the farm:** the family video bubble now shows on the Farmstand too. Farm sheets sit above it; puzzles cover it.
  - **Farm Family Bank (🏦 building, also from the 🪙 jar):** anyone can put Moolah in from their jar.
    - The Farm Store has a **Pay with: 🫙 My jar / 🏦 Family Bank** switch.
    - Every deposit and every bank purchase goes in the **ledger** (who, what, how much, when), with totals put in and spent per person.
    - Data: `farm/bank` is the balance; `farm/ledger/<id>` = `{at, who, kind: in|out, amt, what}`.
  - Fixed: the farm's ⬅️ and 🏠 buttons had stopped working (lost in the v2 merge).
- **One problem per puzzle (Oct 27):** every puzzle is a single round now (`roundsFor()` returns 1). That covers counting, letters, colors and patterns (were 2–3 rounds) and Big tracing (was 2). Big's money puzzle takes turns between adding up and making change.
  - **Longer puzzles pay more:** a Moolah bonus on top of the chore's reward, shown on the 🎉 screen ("Big puzzle bonus +2 🪙"). See `PUZZLE_SIZE`:
    - Big: memory +1, tracing +1, jigsaw +2, building shapes +2.
    - Little: memory, tracing, jigsaw and building shapes +1 each.
    - Quick ones (counting, letters, colors, patterns, money) +0.
- **Clearer tapping (Oct 27):**
  - Bubbles (💧 🌱 🥚 🥛 🧶 and the food an animal wants) are their own tap targets and always win.
  - Touching shows a glowing ring and a name tag with its state ("🐔 Hen · 🥚 ready"). Lifting does it, and dragging cancels.
  - If two or more things are under the finger, a **"Which one?"** picker shows big buttons with each one's state, read aloud.
  - Animal tap areas hug the body.
  - Animals gently keep about a tile apart, so they stack up less.
- **Ready to use:** `farmPuzzle()` to put a puzzle in front of any farm action, `logAttempt()` for the grown-up dashboard (#8), `say()` / `sayLittle()` read-aloud, Firebase under `families/<code>/`, and `tools/genart.py` for isometric art.

### 🧩 Every action is a puzzle
Puzzle types come from the **Age-appropriate tasks** chat. That chat is building them into the Farmstand as a reusable puzzle engine. **Its output defines the final puzzle behind each action.** The table below is the starting mapping, and any puzzle type can be swapped in. Each action has a **main puzzle** and draws from the others now and then so it doesn't get stale.

| Farm action | Main puzzle type | Little (Violet, 3–4) | Big (Quinn, 5–7) |
|---|---|---|---|
| 🌱 Plant crops | Patterns | Red-blue-red-blue… which seed comes next? | ABC / AABB rows, growing patterns |
| 💧 Water crops | Colors & shapes | Tap the watering can that matches the color dot | Sort by two attributes ("big blue cans"), or count the drops: "this plant needs 7" |
| 🧺 Harvest crops | Counting | Tap all 5 carrots; each tap counts out loud | Count 10–20, or add and take away ("3 carrots + 2 carrots") |
| 🌽 Feed animals | Letters & words | Find the letter on the food sack (C for corn) | Read the word (HAY, CORN, SLOP) or spell it with letter tiles |
| 🥚 Collect eggs | Memory match | 6 cards (3 pairs), with a face-up preview | 12–16 cards, no preview |
| 🥛 Milk the cow | Jigsaw | 4–6 big pieces with a faint outline | 12–20 pieces, no outline, some rotated |
| 🧶 Shear the sheep | Tracing | Trace a thick dotted letter from her name, following the star | Thin path with stroke-order arrows, lowercase and 0–20, then without dots |
| 🔨 Build (fence, stable) | Building shapes | Drag 2–3 pieces into a silhouette | Tangram, 4–7 pieces, rotation allowed |
| 💰 Sell at the farmstand | Counting money | Tap one coin per item ("3 carrots, tap 3 coins") | Add up prices, then make change up to 20 |

### ✅ Puzzle engine (built Oct 27)
- **Hook up an action:** `farmPuzzle("milk", {title:"🥛 Milk the cow", item:{em:"🥛",one:"pail",many:"pails"}, pic:"cow/stand", reward:"+1 🥛"}, () => { /* do the action */ })`. `item` is what counting puzzles count; `pic` is the isometric sprite the jigsaw uses.
- **Which puzzle:** `FARM_ACTIONS` holds each action's main type from the table above. With `FARM_MIX` = 0.6 the action borrows a different type 60% of the time, picking the one that player did least recently, so all 8 come around while only feed and harvest exist. Lower it as more actions are built.
- **What's in each type:**

| Type | Little (Violet, 3–4) | Big (Quinn, 5–7) |
|---|---|---|
| Counting | Tap each one to count 2–5 (counts out loud); put 1–5 in the basket | How many? (6–20, tap to mark); add or take away within 10 with pictures; which side has more? |
| Letters & words | Find the letter (mostly V-I-O-L-E-T); find the same letter | Big letter to small letter (with b/d/p/q tricks); what letter does 🐮 start with?; spell a 3-letter word with tiles |
| Colors & shapes | Tap the red balloon; find the circle; drag balloons into the same color basket | Tap the small blue triangle (two clues); find the hexagon, octagon, trapezoid…; how many sides? |
| Jigsaw | 4 big pieces over a faint picture | 12 pieces, no picture, pieces start turned (tap to turn) |
| Building shapes | 2–3 shapes into dotted outlines (house, ice cream, snowman, sailboat, tree, square from two triangles) | 5 shapes into a solid silhouette (rocket, house, tree, sailboat, cat, fish), shapes start turned |
| Tracing | Thick letter path, follow the star ⭐ | Lowercase letters and numbers 0–20 with numbered start dots and arrows, then again with a faint line |
| Patterns | AB: 🍎🍌🍎🍌🍎 ? | ABC, AABB, ABB, AAB; growing (1, 2, 3 → 4); counting by 2s, 5s and 10s |
| Memory match | 3 pairs, face-up preview | 6 pairs, no preview |

- Counting, letters, colors and patterns are 2 quick rounds for Little and 3 for Big. Every prompt is spoken, with a 🔊 button to repeat it. After two wrong tries the right answer glows (Little and Big).
- ✅ **Counting money (Sell), Oct 27:** a 9th puzzle type, `money`, set as the main puzzle for Sell (`FARM_ACTIONS.sell="money"`). It uses the real sale and the Moolah prices.
  - **Little:** "🥚 × 3: tap 3 coins". Each tapped coin flies into the jar and lights up one item.
  - **Big:** round 1 adds up the sale (for example "3 carrots × 1 each and 1 pumpkin × 5 each"). Round 2 makes change from 10 or 20 by tapping 1, 5 and 10 coins. Too much starts the tray over gently, there's a "Take one back" button, and the hint says what to count up to.
  - Coins are drawn in code: gold 1, silver 5, copper 10. They switch to `art/iso/farm/coins/moolah.webp` automatically once that art exists.
- ✅ **Stars and streak for Big, Oct 27:** each finished puzzle shows 1–3 ⭐ (3 with no wrong tries, 2 with up to 2, otherwise 1) and a 🔥 meter of 5.
  - The meter only goes up; wrong tries and backing out never take anything away.
  - At 5 in a row: "Five in a row! Super farmer!", +2 Moolah on the farm, and the meter starts over. It's kept per person on each device.
  - Little is unchanged.
- ✅ **Co-op chores, Oct 27 (jigsaw first):** the 🤝 button on the farm starts a team chore. Today that's **🥛 Milk the cow together**, which needs a cow with milk ready.
  - Everyone else on the farm gets an invite banner (read aloud) with a Join button. The chore starts as soon as a second player joins.
  - **Shared jigsaw:** one picture, split into blocks in join order. Each Little gets a 4×4 block of 4 big pieces (with a faint guide picture), and each Big a 3×4 block of 12 small pieces that can be turned. Name tags show whose part is whose, and the others' pieces land live.
  - When the last piece goes in, everyone celebrates, each player gets 1 🥛, and the cow's milk is used. If someone backs out, everyone sees "had to go, try again later" and nothing is lost.
  - **Session (generic):** `families/<code>/coop/<id>` = `{chore, type, title, pic, target, host, at, status: open|playing|done|off, members, order, lv, prog:{who:{piece:true}}}`. A new team chore is an entry in `COOP_CHORES` (puzzle type, picture, what it needs, what it gives). A new puzzle type joins by building its shared version when `api.ctx.coop` is set, like `buildCoopJigsaw`. Sessions older than an hour are cleaned up.
  - Next: more team chores (shear together, a team harvest) and co-op versions of other puzzle types.

- **Grown-up puzzles (Oct 27):** grown-ups get real games on their chores, and they **can lose**. Losing ends the chore (it doesn't happen) and that chore **rests for 3 minutes** before it can be tried again; walking away mid-game counts as a loss. Tapping a resting chore shows a countdown ring. The farm can read `farmCooldown(action, o)` to draw that ring on the map, and can pass `o.key` to farmPuzzle so the cooldown applies to one specific animal or plot (otherwise it's per chore title). Each chore picks the game that grown-up played least recently: **Mini sudoku** (6×6 with 1–6, 18 blanks, 3 wrong numbers and you lose), **Word guess** (5 letters, 6 tries; guess list in `words/guesses.txt`), **Blackjack** (first to win 2 hands; dealer stands on 17; double down counts twice), **Minesweeper** (6×6, 5 mines, first tap is always safe, long-press or flag mode to flag) and **Traffic jam** (slide cars and trucks on a 6×6 lot so the red car can drive out; 60-second timer; every puzzle is checked solvable in 5–11 moves). Wins pay a Moolah bonus (Sudoku +2, the rest +1). Losses are logged as unfinished attempts.

**Rules for every puzzle** (from the Age-appropriate tasks chat):
- **Little:** no fail state. A wrong tap wiggles and stays put. Every prompt is spoken, and a puzzle is done in under a minute.
- **Big:** shows a star rating and a streak of up to 5 (built), and never punishes a wrong answer.
- Every attempt calls `logAttempt({puzzle, skill, ms, wrong, hint, done})`.
- **Co-op:** each kid solves their own tier of the same chore. For example, Violet places 4 big jigsaw pieces and Quinn places 12 small ones to finish one milk pail.

### 🥕 Goods
| Source | Good | Notes |
|---|---|---|
| Hen | 🥚 eggs | white or brown (Quinn sorts them) |
| Cow | 🥛 milk, sold by the gallon | |
| Sheep | 🧶 wool | sheep shows as sheared until it regrows |
| Pig | ❤️ happiness | no goods; a happy pig gives a small Moolah tip at the stand |
| Crops | 🥕 carrots, 🍅 tomatoes, 🌽 corn, 🎃 pumpkins, 🍓 strawberries | |

### 💰 Moolah
- Earned by **selling goods at the farmstand** (the "Sell" puzzle) and by **filling family orders** (pays more, plus a bonus).
- Prices are whole numbers small enough for Quinn's change-making. For example, a carrot is 1, an egg 1, a tomato 2, wool 3, milk 3 per gallon, and a pumpkin 5.
- Spent in two stores:
  - **🏗️ Farm Store** (in the barn): build and upgrade the farm.
  - **👗 Closet Store** (in the farmhouse): new clothes for **Fashion Show (#5)** and the farmer avatar (#10).
- Little sees Moolah as a jar of coins, with no numbers needed. Big sees the number.

### 🏗️ Build the farm (Farm Store)
Building happens on empty **build lots** around the map. Paying starts a **Build puzzle** (tangram).

| Item | What it does |
|---|---|
| 🪵 Fences | Must enclose a pen before a new animal can move in. Placed piece by piece on the grid. |
| 🐄 Stable / 🐔 coop / 🐑 sheep shed | Each holds more animals of that kind, so goods are collected faster |
| 🐣 New animals | More hens, a second cow, and so on. Needs room in a pen and a building. |
| 🌱 New field plots and seeds | More plots; tomato, corn and strawberry seeds unlock here |
| 💩 Fertilizer | Use on a plot to make the next crop grow faster or give double |
| 💧 Water trough / well | Watering puzzles give extra water |
| 🌻 Decorations | Scarecrow, windmill, flower pots, bench, mailbox, lantern |

- Each build makes the farm visibly bigger. The map can grow past 16 × 16 later.
- Builds are **shared**: everyone's Moolah can go toward one build together (see decisions).

### 👗 Closet Store → Fashion Show
- Sells pieces from the white clothing library (#9) and avatar extras (#10): hats, boots, dresses, capes and costumes.
- What's bought shows up in the Fashion Show dressing screen and the farmer dressing room. Items not bought yet show with a 🔒 and their price.
- Depends on the shared dress-up engine (#9 and #10). Until then the store can sell from a small starter set.

### 📋 Family orders (challenges)
- An **order board** at the farmstand shows requests from family members, each with their avatar. For example: "Gramma Mia wants 1 gallon of milk and 2 carrots."
- Filling an order: gather the goods (by doing chores), then tap **Deliver**. Pays more Moolah than selling, and sends a **thank-you to the kid's Inbox (#4)** from that family member.
- **Scaled to the player's age:**

| | Little (Violet) | Big (Quinn) |
|---|---|---|
| Kinds of goods | 1 | 2–4 |
| How many of each | 1–3 | up to 10 (later "half a dozen eggs") |
| How it's shown | pictures only, read aloud | written words and numbers |
| Extra | none | some orders have a "by dinner" goal for bonus Moolah; missing it never fails the order |
| Example | "Grandpa wants 🥕🥕" | "Apple G wants 2 gallons of milk, 6 eggs and 3 pumpkins" |

- Each kid gets their own orders. **Co-op orders** need both kids' goods, such as Violet's eggs plus Quinn's milk.
- New orders appear each visit (about 3 per kid), so the board is fresh but finishable within the 30 minutes.
- Grown-ups can **write a custom order** from the grown-ups corner, for example "Daddy wants 1 pumpkin for Halloween."

**🎨 Farm art still needed** (isometric sprite style, `art/iso/farm/`, made with `tools/genart.py`)

✅ Done: hen, cow, pig and sheep (stand, eat, sleep, back) · carrot and pumpkin (sprout, growing, ripe).

About **48 images** left including retries, which is roughly one day of the free allowance if nothing else is using it. Make them in this order:

*Batch A — needed for the chore puzzles (about 25)*
- Ready to run: `python3 tools/genart.py isobatch tools/batches/farmA.json` (skips anything already made). Scheduled to run automatically at 7:05 PM Central on Oct 27.
- [ ] Crops, growing + ripe (the carrot sprout is reused for every crop): tomato, corn, strawberry — 6
- [ ] Seed packets, one per crop (Plant puzzle: match seed to picture): carrot, tomato, corn, pumpkin, strawberry — 5
- [ ] Animal goods to collect: white egg, brown egg (sizes and colors done in code for the sorting puzzle), milk pail, ball of wool — 4
- [ ] Animal food (Feed puzzle: match the animal to its food; Big reads HAY / CORN / SLOP): hay bale, corn pile, slop bucket, chicken feed scoop — 4
- [ ] Tools: watering can in **white** so the game can tint it (Little's "tap the matching color" puzzle), empty bucket (co-op milking), harvest basket — 3
- [x] Sheared sheep (shown after wool is collected) — 1
- [ ] Hiding spots for egg hunt: hay pile, bush — 2

*Batch B — the farm itself (about 12)*
- [ ] Buildings: red barn, chicken coop, farmhouse (door to the dressing room), farmstand stall with an awning, stable (buildable with Moolah) — 5
- [ ] Fence: straight piece and corner (mirrored in code for other directions) — 2
- [ ] Nature: round tree, apple tree, flower patch, rock, small pond — 5

*Batch B2 — new for building and orders (about 9)*
- [ ] Stable, sheep shed, water trough or well — 3
- [ ] Fence gate, fertilizer bag, milk jug (gallon) — 3
- [ ] Order board, Moolah jar, Moolah coin (replaces the copper and silver coins in Batch C) — 3

*Batch C — farmstand shop unlocks (about 11)*
- [ ] Decorations to buy with coins: scarecrow, windmill, flower pot, bench, mailbox, lantern — 6
- [ ] Coins for "make change" (Big): copper coin and silver coin, blank, with the value drawn on in code — 2
- [ ] Moolah: a gold Moolah coin and a small coin pile (the farm money for building and Fashion Show clothes) — 2
- [ ] Fertilizer bag (buildable/buyable) — 1

*Done in code (no images):* sparkles, water drops, hearts for a happy pig, sun moving across the sky, the goodnight moon and stars, chore cooldown rings.
*Covered elsewhere:* farmer avatars, costumes and following pets are in **#10**.
*Only if decided:* wilted crop stages, if crops can wilt (see decisions below) — 5 more images.

**⚠️ Art style check before #10 starts:** #10 says to use the chunky 3D hen (`art/farm/hen.webp`) as the style reference, but the farm now uses the flatter **isometric sprite** style (`art/iso/farm/`). Avatars walking on the farm should match the isometric animals, so #10 should use an isometric animal (for example `art/iso/farm/hen/stand.webp`) as its reference.

**🧑‍🌾 Farmer avatars (customizable)**
- Each player walks around the farm as their own **farmer avatar**, visible to everyone in the game. It replaces the plain finger marker, and each avatar's name floats above it.
- **Customize from a dressing room** before entering the farm (and anytime from the farmhouse):
  - **Little:** big picture choices for hair, skin tone, a hat (straw hat, cap, bonnet, flower crown), overalls or a dress, boots, and a color for each. Every choice is read aloud.
  - **Big:** more options for each part (hairstyles, glasses, freckles, bandanas, aprons, gloves), patterns, and color schemes.
  - **Grown-ups** get Big options.
- **Unlocks from playing:** Moolah from the farmstand buys extra items in the Closet Store, such as a cowboy hat, rain boots, a pumpkin costume or a pet that follows you (a dog, cat or duckling).
- Avatars do small animations: walk, wave, cheer when a chore puzzle is solved, and yawn as the 30 minutes wind down.
- The look is saved per persona (in Firebase), so it's the same on every device.
- **Shares a dress-up system with Fashion Show (#5).** Body parts, clothing layers and recoloring are built once and used by both games, and as each player's avatar everywhere in Kapanigans.

**⏱️ 30-minute play limit (per player)**
- The farm is designed so a full visit takes **no more than 30 minutes**. Each player gets **30 minutes of farm time**; once it's used, the farm is closed to that player for **24 hours** from that moment.
- Time is tracked per persona (Violet, Quinn, Joe…), not per device, and saved in Firebase. Switching iPads doesn't reset it.
- Only active farm time counts: the clock pauses when the app is closed, the iPad sleeps, or the player leaves the farm for the lobby or another game.
- **Cooldown timers on the puzzles set the pace.** After a chore puzzle is solved, that spot rests (for example, a watered plant "drinks" for 3 minutes and a fed chicken naps for 5). The cooldowns are tuned so that doing every available chore fills about 30 minutes, which makes the limit feel like a natural end to the visit rather than a sudden cutoff.
- **Winding down, not a hard stop:**
  - The sun moves across the farm sky as the player's time is used; sunset means time's nearly up.
  - At 5 minutes left: "The animals are getting sleepy!" No new chores start, but the current puzzle can be finished.
  - At 0: a goodnight scene ("See you tomorrow!") with a countdown to when the farm opens again, shown as a picture for Little players (the moon going around).
- The rest of Kapanigans (Color Together, Bedtime Stories, Inbox) stays available while the farm is resting.
- In co-op chores, each player's own clock runs separately. If one player runs out mid-game, the other can keep going.
- Grown-ups can see everyone's remaining farm time. Whether grown-ups can grant extra time is still an open question below.

**Acceptance criteria**
- [x] A bigger farm (16 × 16) to explore by dragging, with calmer, slower animals
- [x] Every farm action (plant, water, harvest, feed, collect eggs, milk, shear, build, sell) opens a puzzle, with a Little and a Big version
- [ ] Puzzle types and rules match the Age-appropriate tasks puzzle engine
- [x] Gentle failure only: wrong answers get a "try again" with a hint, never a penalty or a dead plant
- [x] Goods can be sold at the farmstand for Moolah
- [x] Moolah buys fences, buildings, animals, plots, seeds, fertilizer and decorations, and each shows up on the farm
- [ ] Moolah buys clothes in the Closet Store, and they appear in Fashion Show and the farmer dressing room
- [x] An order board with family-member orders sized for Little and Big, paying Moolah and sending a thank-you to the Inbox
- [x] Grown-ups can write a custom order
- [ ] A shared farm view that stays in sync across devices
- [x] Farm, Moolah, goods and orders are saved in Firebase and still there the next day
- [ ] Each player can customize a farmer avatar that everyone sees on the farm, and it's remembered across devices
- [ ] Each player's farm time stops at 30 minutes and reopens 24 hours later, on any device
- [ ] Puzzle cooldowns are tuned so finishing all available chores takes about 30 minutes
- [ ] A 5-minute "sleepy animals" warning and a goodnight screen with a countdown

**🔍 Decisions needed**
- ~~Saving the farm~~ → decided: Firebase (see Shared groundwork).
- ~~Wilting~~ → decided: **gentle droop, no loss**. Thirsty plants and hungry animals droop until someone helps; nothing dies.
- ~~Daily play limit~~ → decided: 30 minutes per player, then a 24-hour rest (see above).
- Do grown-ups follow the same 30-minute limit, or are they exempt?
- ~~Avatar everywhere?~~ → decided: **yes**. The custom avatar replaces the emoji avatar in the lobby, the "Who are you!? :)" screen, seat chips and all games (including as a model option in Fashion Show).
- ~~Dressing room and farm time~~ → decided: **no**. Time in the dressing room doesn't count toward the 30 minutes.
- Can a grown-up grant extra time or reset a player's cooldown (for a sick day or a road trip)?
- Should the 24 hours run from when the time ran out (as written), or should the farm reopen every morning at a set time (for example 7 AM), which is easier for little ones to understand?
- ~~Moolah wallet~~ → decided: **one jar per person**, anyone can **gift** Moolah to anyone, plus a shared **Farm Family Bank** with a ledger.
- ~~Family Bank spending~~ → decided: **anyone can spend, no limit**; the ledger shows who spent what.
- Should Little players spend Moolah on their own, or does a grown-up approve big purchases?
- Can grown-ups give Moolah as a reward (for example from the grown-ups corner)?
- Can family members other than the 8 grown-ups place orders (Bear friend, Fox friend)?
- Should an unfinished order stay on the board until it's done, or be replaced after a few days?


### 🗺️ Build order
1. ✅ **v1.1:** bigger map, panning, slower animals, pasture and field.
2. **Puzzle engine wired to actions:** the Age-appropriate tasks chat's work. Tapping a crop or animal opens its puzzle; solving it does the action.
3. **Goods and the farmstand:** collect all goods, the Sell puzzle, Moolah.
4. **Farm Store and building:** build lots, fences, stables and coops, new animals, fertilizer and seeds. Needs Batch B and B2 art.
5. **Family orders:** the order board, sizing by age, Inbox thank-yous, custom orders from grown-ups.
6. **Save and share:** Firebase farm state, live co-op on one farm, the 30-minute limit with cooldowns.
7. **Closet Store:** after the dress-up engine and clothing art (#9, #10).

---

## 4. ✅ Inbox for every persona

Every person (kids, friends and grown-ups) gets an **Inbox** for messages the family sends each other. No passwords: it's all family, and the family code is the only key.

**Welcome**
- ✅ First open asks **"Who are you!? :)"** and remembers the answer on that device. Tap your name chip in the lobby to switch.

**Sending**
- Tap **Send a message**, then pick who it's for (one person or "Everyone").
- What you can send, by level:
  - **Little:** a sticker or emoji, a quick drawing, or a short voice message (hold the big mic button)
  - **Big and grown-ups:** all of the above, plus typed text and quick phrases ("Good night!", "I love you", "Come play!")
- Bedtime Story gifts (#1) and finished Color Together pictures can be sent to an inbox too.

**Receiving**
- A mailbox on the lobby screen with a badge count of unread messages
- A happy chime and a bouncing envelope when something new arrives while the app is open
- Opening a message reads it aloud for Little readers
- Reply with one tap (heart, hug, or "send one back")
- Messages stay until you delete them; grown-ups can clear any inbox (Grown-ups › Inboxes) ✅

**Acceptance criteria**
- [x] A message sent to a device that's asleep or closed is waiting in the inbox when it's next opened
- [x] Unread badge on the lobby mailbox and on each person in the "Who are you?" screen
- [x] Violet can send and open messages without reading anything
- [x] Voice messages up to 30 seconds
- [x] Send a finished Color Together picture to someone's inbox ("Send it 💌" on the celebration screen)

**🔍 Decisions needed**
- Should kids be able to message only family personas, or Bear friend and Fox friend too? *(For now: anyone can message anyone; "Everyone" goes to family only, not Bear or Fox friend.)*
- ~~Parent view~~ → ✅ built: Grown-ups › Inboxes › 👀 Open shows any person's messages without marking them read.

---

## 5. 🆕 New game: Fashion Show

Kids design outfits for a "model," then watch the model walk an animated runway, take photos and call out poses.

**Designing the outfit (by level)**
- **Little (Violet):** drag and drop ready-made pieces onto the model: tops, bottoms, dresses, shoes, hats, bags and accessories (crowns, sunglasses, capes). Tap a piece to change its color from a few big color dots. Every piece and color name is read aloud.
- **Big (Quinn):** pick from more advanced templates (for example a ball gown, a superhero suit, a rock star outfit or a sports uniform) and customize each part: sleeves, length, collar and pattern (stripes, polka dots, stars, hearts). Choose from named color schemes (Ocean, Sunset, Candy, Forest, Galaxy) or pick each color separately. Can also draw a design onto the fabric with the Color Together tools.
- **Clothes come from the Farmstand:** a starter wardrobe is free; more pieces are bought with Moolah in the Farmstand's Closet Store (#3). Pieces not owned yet show with a 🔒 and their price.
- **Models:** a handful of friendly characters to dress (kid, animal and robot models), plus each player's own persona avatar.

**The runway**
- The model walks down an animated runway with lights, music and a cheering crowd, then stops at the end and holds a pose before walking back.
- Walk styles to choose: strut, twirl, skip, hop and silly walk.
- Each player's model gets a turn, with their name announced ("Here comes Quinn's Galaxy Rock Star!").

**Interactive: photos and poses**
- A **camera button** takes a photo with a flash and shutter sound. Photos go into a **Lookbook** and can be sent to someone's Inbox (#4).
- **Pose buttons** make the model strike a pose: hands on hips, wave, peace sign, twirl, superhero, and blow a kiss. Little players get big picture buttons; Big players can chain poses into a short routine.
- The crowd reacts with applause, hearts and confetti, and other players can tap reactions live.

**Co-op**
- Up to 4 players, each dressing their own model, then a shared show where everyone's models walk in turn.
- Optional "design together": two players dress the same model, one picks the top while the other picks the bottom.

**Acceptance criteria**
- [ ] Little players can dress a model and change colors without reading anything
- [ ] Big players get at least 4 templates, piece customization, patterns and at least 5 color schemes
- [ ] An animated runway walk with at least 3 walk styles and a pose at the end
- [ ] At least 5 poses triggered by buttons during the show
- [ ] Photos can be taken during the show and saved to a Lookbook
- [ ] Shows sync live for everyone in the game, like Color Together

**🔍 Decisions needed**
- Models: generic characters only, each player's own avatar, or both?
- Should Lookbook photos save to the iPad's Photos app, or stay inside Kapanigans (and the Inbox)?
- Should there be any judging or scoring, or keep it all cheering with no winners (kinder for little ones)?

---

## 6. ✅ Shorter family code: 4 random letters and numbers

Today the family code is a word plus 4 digits (for example `CABBAGE4821`), at least 6 characters. Make it **4 random letters and numbers** instead (for example `K7QM`), so it's quick to type on every iPad.

**Details**
- **Generate it:** a grown-up taps **New code** and gets 4 random characters from a secure random source.
- **Easy to read:** leave out look-alike characters (0/O, 1/I/L, 5/S, 2/Z), so kids and grandparents can copy it correctly. That leaves about 28 characters, or roughly 600,000 possible codes.
- **Big display:** show the code in big type with each character in its own box, and use 4 boxes on the entry screen too, with auto-advance to the next box.
- **Existing devices:** a device already using a long code keeps working until a grown-up switches it. Long codes are still accepted if typed.
- **Firebase rules:** the planned rule `$code.length >= 6` changes to allow 4-character codes.

**Acceptance criteria**
- [x] New codes are exactly 4 characters, random, uppercase, with no look-alike characters
- [x] Typing is not case-sensitive; any lowercase letters typed are treated as uppercase
- [x] Devices with the same 4-character code find each other in the lobby
- [x] The Inbox and saved data (Firebase) work with 4-character codes

**🔍 Decisions needed**
- ~~Privacy trade-off~~ → decided: **accept it**. The 4-character code is the only key; change it anytime from Grown-ups › Family code.
- (Original note) **Privacy trade-off:** the family code is the only key to your games, the video chat and (later) the Inbox. A 4-character code is much easier for a stranger to guess than the current one. Options:
  - Accept it: the risk is low for a family app, and the code can be changed anytime.
  - Add a lock so only devices a grown-up approves can join, or ask a grown-up to approve the first time a new device joins.
  - Keep video chat and the Inbox behind a separate, longer grown-up code.

---

## 7. ✅ Friendlier, slower read-aloud voice

The read-aloud voice talks too fast and sounds a bit robotic. Make it slower and warmer, better suited to young kids.

**Today:** `say()` uses the device's built-in voice, picking the first one found from Samantha, Ava, Allison, Karen and others. Speed is 0.85 for Little and 0.95 for Big, with pitch at 1.1. On iPad the basic "compact" voices are the robotic-sounding ones.

**Changes**
- **Slow it down:** about 0.7 for Little and 0.8 for Big, with a slightly higher pitch (about 1.15) for a warmer sound.
- **Natural pauses:** read one sentence at a time, with a short pause between sentences (longer between story pages), instead of one long run.
- **Better voices first:** prefer the iPad's higher-quality **Enhanced** and **Premium** voices when they're installed (for example Ava, Zoe or Samantha), and skip the novelty and robotic voices.
- **Grown-up voice settings:** a small settings panel to pick the voice, choose a speed (Slow, Normal or Faster) and tap **Test** to hear "Hi Violet! Let's play!" Saved per device.
- **Setup tip in the app:** if only basic voices are found, show grown-ups how to download a better one on the iPad: **Settings → Accessibility → Spoken Content → Voices → English**, then download an Enhanced or Premium voice. It's free and works offline.

**Later option: recorded voices**
- For fixed phrases (button names, chore instructions, "Great job!"), use recorded audio clips instead of the built-in voice. These could even be family recordings, such as Gramma Mia reading the bedtime stories. Fill-in words in stories would still use the built-in voice.

**Acceptance criteria**
- [x] Little-level speech is noticeably slower, with pauses between sentences
- [x] A higher-quality voice is chosen automatically when the iPad has one installed
- [x] Grown-ups can change the voice and speed and hear a test line (Grown-ups › Voice)
- [x] Story read-aloud word highlighting still lines up with the slower speech

**🔍 Decisions needed**
- ~~Preferred voice style~~ → decided: **female voice** by default (Ava, Zoe, Samantha, Allison). Male voices are left out of the automatic pick; grown-ups can still choose another voice in settings.
- ~~Recorded voices for common phrases~~ → ✅ built: Grown-ups › Voice › Family voice clips. Record "Hi Violet!", "Let's color!", "Color on your part!", "You did it together!" and more; the game plays them instead of the reading voice.

---

## 8. 🛠️ Grown-up progress and usage dashboard (built; puzzle skills fill in when the Farmstand ships)

Track how much each player uses Kapanigans and how they're doing on puzzles and tasks, so grown-ups can see where each kid is thriving or stuck.

**What gets tracked (per persona)**
- **Usage:** sessions, time played per day and week, time in each game, time of day, and which device.
- **Farm time:** minutes used of the daily 30, and when the farm reopens.
- **Puzzles and tasks** (Farmstand chores, Bedtime Story steps, and future puzzles), one record per attempt:
  - Which puzzle and level (Little or Big) and the skill it practices (colors, matching, counting, adding, patterns, reading words, sorting, making change)
  - How long it took, from showing the puzzle to solving it
  - Wrong tries before the right answer, and whether a hint was used
  - Finished or left unfinished
- **Creative play:** stories made and sent, pictures colored, Fashion Show outfits and photos, and Inbox messages sent (counts only, not content).

**Grown-up dashboard**
- A **Grown-ups** button in the lobby, behind a simple grown-up check (for example "hold for 3 seconds" or a quick multiplication question), so kids don't wander in.
- **Per kid:** a weekly summary card, such as "Quinn played 2h 10m this week, solved 46 puzzles, 89% right on first try."
- **Skills view:** each skill shows accuracy, average solve time and its trend over time, marked as Got it ✅, Getting there 🟡 or Needs practice 🔴.
- **Struggle spots:** puzzles with many wrong tries or slow solves, such as "Violet takes 3+ tries on counting past 4."
- **Usage view:** a daily time chart for each game, and the times of day they usually play.
- **Compare over time,** not between kids: each child is shown against their own past, never ranked against siblings.

**Kid-facing rules**
- Kids never see scores, accuracy or timers from this data. Their side stays all cheering and gentle hints.
- Optional later: use the data to adjust difficulty automatically, such as easier counting when Violet is struggling, or moving Quinn to harder adding when she's acing it.

**Privacy**
- All data stays in the family's own Firebase under `families/<family code>/stats/`. No third-party analytics or trackers.
- Grown-ups can export (CSV) or clear any kid's data.
- Store small summary records, not recordings or drawings.

**Acceptance criteria**
- [~] Every puzzle attempt records the skill, level, solve time, wrong tries and hint use: `logAttempt()` is ready; the Farmstand will call it
- [x] Play time is recorded per persona, per game and per day, and syncs across devices
- [x] A dashboard behind a grown-up check (hold the 🔒 for 3 seconds), with a weekly summary, usage chart, time of day, skills view and struggle spots per kid
- [x] Every grown-up persona can see every kid's dashboard
- [x] A weekly summary arrives in each grown-up's Inbox (sent once per week, for the week before)
- [x] Detailed records older than 90 days roll up into weekly summaries
- [x] Kids see no scores or stats anywhere
- [x] Grown-ups can clear a kid's data, and export it as CSV

**🔍 Decisions needed**
- ~~Record retention~~ → decided: keep detailed records for **90 days**, then roll them up into **weekly summaries**.
- ~~Weekly report delivery~~ → decided: a weekly summary goes to each grown-up's **in-game Inbox** (#4).
- ~~Automatic difficulty~~ → decided: **look at the data first**; no automatic adjustment for now.
- ~~Who can see reports~~ → decided: **every grown-up** (all 8) can see both kids' reports.

---

## 9. 🆕 Fashion Show art: blank (white) clothing library

Build a library of **white, colorable clothing pieces** for Fashion Show (#5), so Violet and Quinn add all the color themselves.

**The pieces (first set: about 40)**
| Group | Pieces |
|---|---|
| Tops | T-shirt, long-sleeve shirt, tank top, blouse with puffy sleeves, hoodie, sweater, jacket, vest |
| Bottoms | Jeans, leggings, shorts, skirt, tutu, overalls, sweatpants |
| Dresses | Party dress, ball gown, sundress, princess dress, nightgown |
| Outerwear and costumes | Raincoat, cape, superhero suit, lab coat, rock star jacket |
| Shoes | Sneakers, boots, sandals, ballet slippers, rain boots, high-tops |
| Hats and accessories | Crown, sun hat, beanie, baseball cap, bow, sunglasses, scarf, handbag, necklace |

**How they're made**
- Generated with the art kit (`tools/genart.py`, FLUX.2 klein) in the same house style as the farm animals, but **pure white with soft grey shading**, so a color tint looks natural with the folds and shadows kept.
- Every piece is drawn **front-facing, flat, on its own**, at the same scale, matching one standard model body (a "mannequin" template made first), so pieces line up on any model.
- Each piece in `art/manifest.json` gets fit info: which body slot it goes on (top, bottom, dress, shoes, head, neck, hand), plus an offset and scale so it snaps on correctly.
- **Coloring:** the game tints the white piece to any color. For Quinn, patterns (stripes, dots, stars, hearts) and color schemes are drawn on top and clipped to the piece's outline, and she can draw on it directly.
- A separate small detail layer (buttons, zippers, laces) stays uncolored where it looks better that way.

**Plan**
1. Make the mannequin template (front view, arms slightly out) and confirm it looks right on the runway.
2. Generate the first set over about 2 days within the free daily allowance (about 85 images a day), including retries for pieces that don't come out clean.
3. A contact sheet (`genart.py sheet fashion`) for Joe to approve, then wire the pieces into the dressing screen.

**Acceptance criteria**
- [ ] At least 6 pieces in each group, all white with shading, as clean cutouts
- [ ] Every piece lines up on the mannequin without manual fixing in the game
- [ ] Any piece can be tinted to any color and still looks shaded, not flat
- [ ] Patterns stay inside the piece's outline
- [ ] Each piece is a small WebP (under about 40 KB)

**🔍 Decisions needed**
- ~~First set contents~~ → decided: go with the set above; nothing to add for now.

---

## 10. 🛠️ Avatar builder (engine and dressing room built with code-drawn parts; generated art still to come)

Build the **simple parts for the avatar builder** (#3 farmer avatars, used as every player's avatar across Kapanigans) in the **same chunky 3D style as the farm animals** (`art/farm/`).

**The parts (first set)**
| Group | Parts |
|---|---|
| Body and face | A round, friendly base body in 6 skin tones; 6 face expressions (happy, big smile, surprised, sleepy, silly, wink) |
| Hair | About 10 styles (short, curly, pigtails, ponytail, bun, braids, long, spiky, bob, buzz), made **white** so any hair color can be applied |
| Hats | Straw hat, ball cap, bonnet, flower crown, beanie, cowboy hat, crown |
| Farm clothes | Overalls, farm dress, plaid shirt, apron, bandana, gloves, boots, rain boots (white for coloring, like #9) |
| Extras | Glasses, freckles, rosy cheeks, bow |
| Unlockables | Pumpkin costume, chicken costume, a pet dog, cat and duckling that follow you |

**How they're made**
- ~~Same chunky 3D style, hen as reference~~ → changed: isometric sprite style (see the generated art section below).
- Same layering approach as #9: one base body that every part fits on, parts listed in the manifest with their slot, offset and scale, and white parts tinted in the game.
- **Little-friendly:** big, simple shapes that still read clearly when small, such as on a seat chip or the lobby.
- Extra poses for the base body (walk, wave, cheer, yawn) are animated in code by moving the parts, not drawn separately.

**Shared work with #9**
- One dress-up engine, built once: slots, layering, tinting, patterns and saving each look per persona.
- Avatar parts and Fashion Show clothes can mix: a Fashion Show piece can be worn by your avatar, and your avatar can walk the runway.

**✅ Built so far (code-drawn parts, no image credits used)**
- **Dressing room** (👗 Dress up on your home-screen card): Skin (6), Face (6: happy, big smile, surprised, sleepy, silly, wink), Hair (10 styles + 10 colors), Hat (7 + none, any color), Clothes (overalls, farm dress, plaid shirt, apron, T-shirt, hoodie, any of 12 colors), Extras for Big/grown-ups (glasses, freckles, rosy cheeks, bow), 🎲 surprise me. Violet's level gets bigger tiles and no Extras tab.
- Saved per person in Firebase (`families/<code>/looks/<person>`), the same on every device.
- The avatar replaces the emoji (and photo) on the home screen, "Who are you?", seat chips, zone labels, inbox and the video tile when the camera is off; the farm farmer wears the avatar's face and hair under the straw hat.
- **Swapping in art later:** each part is one slot in `avatarSVG()` (skin, face, hair back/front, hat, outfit, extras). Generated cutouts can replace a slot's drawing one at a time without changing the dressing room or saved looks.
- Still to do: unlockables (pumpkin and chicken costumes, pets) once Farmstand coins can buy them; generated art per the table above.

**🎨 Generated art ready to swap in (Oct 27) — `art/avatar/`, from `tools/batches/avatar1.json`**
- **Style:** the flat **isometric sprite** style of the farm animals (`art/iso/farm/`), not the chunky 3D `art/farm/` style named above, so farmers match the animals they walk among. Facing the bottom left like the animals; mirror for the other side.
- **How to stack:** every file is a **320×320 full-frame layer at the same position**. Draw `base.webp`, then outfit → feet → hair → hat → extras on top at the same x, y and size. No offsets needed.
- **Tinting:** files marked `"white": true` in the batch file are white; tint them in the game (multiply by the chosen color). Straw hat, cowboy hat, crown, flower crown and glasses keep their own colors.
- **Files → dressing-room slots:**
  - Hair (10, matches the 10 styles): `hair/` pigtails, short, curly, ponytail, bun, braids, long, spiky, bob, buzz.
  - Hat (7, matches): `hat/` straw, cap, bonnet, flowercrown, beanie, cowboy, crown.
  - Clothes: `outfit/` overalls, dress (farm dress), shirt (use for plaid shirt; the plaid can be drawn over it), apron. The dressing room's T-shirt is the base body's own shirt, tinted. **No art yet for hoodie**; there's art for **bandana** and **raincoat**, which aren't in the dressing room yet.
  - Feet: `feet/rainboots` (no slot yet). Extras: `extra/glasses`, `extra/bow`.
- **Done in code, not images:**
  - **Skin:** recolor the peach pixels of `base.webp` (red > green + 15 and green > blue). Leave the boots out (bottom 15% of the figure), or they get recolored too.
  - **Face:** the base face is plain dot eyes and a smile; keep drawing the 6 expressions on top. This also keeps the eyes visible on the darkest skin tones.
  - Freckles and rosy cheeks.
- **Still to make:**
  - A hoodie.
  - Pumpkin and chicken costumes.
  - Pet dog, cat and duckling, as isometric pose sets like the farm animals (via `genart.py poses`).
  - Back views, if the farmer should show its back when walking away (about 27 images).
  - Do these on a later day: the 7 PM art budget tonight goes to farm Batch A.
- **New parts:** add to `tools/batches/avatar1.json` and run `python3 tools/genart.py avatar tools/batches/avatar1.json` (skips what's made). Each part is generated as an edit of the base, then cut out by comparing it to the base, which is why every layer lines up.

**Acceptance criteria**
- [x] Every part matches the farm animals' style side by side on a contact sheet (generated set, `art/avatar/`)
- [x] At least 6 skin tones, 10 hairstyles, 6 hats and 6 outfits at launch
- [x] Hair and clothes can be tinted to any color
- [x] An avatar stays readable at small sizes (seat chips, lobby)
- [x] Each person's avatar shows up the same on every device

**🔍 Decisions needed**
- ~~Body size~~ → decided: **everyone is the same size**, kids and grown-ups use the same base body.
- ~~Animal avatars~~ → decided: **humans only**. Costumes (pumpkin, chicken) are worn by the human avatar, and pets just follow along.

---

## 11. ✅ One device per person (no double logins)

Make sure the same person (for example Quinn) can't be signed in on two devices at the same time.

**Why it matters**
- Two "Quinns" in a game take two seats and confuse the lobby, seat chips and video.
- Farm time (#3) and progress stats (#8) are tracked per person, so two devices playing as the same person would double-count or get around the 30-minute limit.
- Inbox (#4) "unread" and reply state should belong to one active device.

**How it works**
- When a device picks a person, it **claims** that person in Firebase (`families/<code>/claims/<persona>`), with the device ID and time. The claim uses the same presence system the lobby already uses, and is released automatically (`onDisconnect`) when the app closes, the iPad sleeps or the connection drops.
- On the **"Who are you!? :)"** screen, people already playing on another device are shown greyed out with a small "playing on another iPad" label, read aloud for Little players.
- Tapping a taken person asks: **"Quinn is playing on another iPad. Play here instead?"**
  - **Yes:** this device takes over. The other device goes back to the "Who are you!? :)" screen with a friendly message ("Quinn moved to another iPad"), and any game it was in saves first.
  - **No:** pick someone else.
- A heartbeat every 30 seconds clears claims left behind by a device that crashed or lost Wi-Fi, so nobody stays stuck as "taken."
- A device that wakes from sleep re-checks its claim; if someone else has taken over, it goes back to the "Who are you!? :)" screen.

**Acceptance criteria**
- [x] A person can be active on only one device at a time
- [x] Taken people are clearly marked on the "Who are you!? :)" screen
- [x] "Play here instead" moves the person cleanly, and the other device returns to the picker without losing game progress
- [x] A claim from a closed or crashed device clears within about a minute
- [x] Farm time and stats can't be doubled by playing as the same person on two devices

**🔍 Decisions needed**
- ~~Guests on several devices?~~ → built as **yes**: Bear friend and Fox friend can be used on several devices at once. Easy to change.
- Should a kid be able to take over their own name from another device, or only a grown-up? *(Built: anyone can, after a "Play here instead?" confirm. It could go behind the grown-up hold if siblings bump each other.)*

---

## 12. 🛠️ Switch camera: front or back (built; needs a test on the real Fire tablet)

Add a button to the video chat bubble to **flip between the iPad's front and back cameras**, so a kid can show the other person something (a drawing on paper, a toy, the dog) and then flip back to their face.

**Today:** the video always uses the front camera (`facingMode: "user"`).

**How it works**
- A **flip camera button** (🔄) in the video bubble, next to mute and camera-off. It's big enough for Violet, and reads "Flip camera" aloud for Little players.
- Tapping it switches cameras **without dropping the call**: the new camera's video is swapped into the live connection (`replaceTrack`), so the other person just sees the picture change.
- The iPad can only use one camera at a time, so the old camera is turned off first, then the new one starts. There's a brief fade during the swap.
- **Your own small preview** is mirrored for the front camera (like a mirror) and not mirrored for the back camera, so text and drawings read the right way.
- The choice resets to the front camera at the start of each new call.
- On a device with only one camera, the button is hidden.

**📱 Amazon Fire tablet (a must)**
- The Fire tablet runs the game in Amazon's **Silk** browser (or Chrome, if installed), which handles the camera differently from Safari on iPad.
- Don't rely only on asking for "front" or "back": some Android and Fire browsers ignore that. Fallback: list the cameras the tablet reports (`enumerateDevices`), pick the front and back ones by their labels ("front", "back", "facing"), and switch by camera ID. If labels aren't available, cycle through every camera the tablet has.
- Ask for a modest video size (for example 640×480) so the Fire's smaller cameras and slower processor keep up, and so the switch is quick.
- Handle the camera permission prompt in Silk, and show a clear grown-up tip if the camera is blocked (Settings → Apps → Silk Browser → Permissions → Camera).
- Test on the family's actual Fire tablet model, both cameras, in both portrait and landscape, during a call with an iPad.

**Acceptance criteria**
- [~] The flip button switches between front and back cameras on iPad, iPhone **and the Fire tablet (Silk browser)**: built with facing-mode, camera-label and cycle fallbacks; not yet tried on real devices
- [x] The call stays connected and the other person sees the new view within about a second
- [x] Mute and camera-off still work after flipping
- [x] The self-view is mirrored only for the front camera
- [x] The button is hidden on devices with one camera
- [ ] A call between a Fire tablet and an iPad works both ways, before and after flipping on either side

**🔍 Decisions needed**
- Which Fire tablet model is it (for example Fire HD 8 or Fire HD 10)? Is it running Silk, or is Chrome installed?
- ~~"Show it!" for Little players~~ → ✅ built: big 👀 Show it! button (Violet level, devices with two cameras) flips to the back camera and back after 20 seconds.

---

## Shared groundwork (needed by #1, #3, #4, #5 and #8)

- ⚠️ **One shared script:** Farmstand and the rest of the game live in the same `<script>`, so two `function` declarations with the same name silently replace each other (this broke story and inbox sending once: `sendGift`, `deliver`). Use unique names; a quick check is to list duplicate `function` names before pushing.

- ✅ **Art kit: decided on Cloudflare Workers AI (free) + `tools/genart.py`.** Claude generates art on request and pushes it to `art/` in this repo (served by GitHub Pages).
  - Model: FLUX.2 klein 4B (polished 3D look, about 85 images a day free); FLUX.1 schnell for quick drafts (about 150 a day). Free allowance resets at 7 PM Central.
  - One fixed house style is baked into every prompt; backgrounds are removed automatically and images saved as small WebP cutouts (about 25 KB), listed in `art/manifest.json`.
  - Why not the others: the Gemini/Nano Banana API has no free image tier; Pollinations and Hugging Face give only small one-time or tiny balances; ChatGPT has no free API.
  - Why not Firebase Storage: it needs the paid Blaze plan. Game art lives in the repo; only images made *during play* (e.g. story pictures) go in the Realtime Database under the family's code (`--firebase CODE`).
  - ✅ First batch: farm animals and crops (hen, cow, pig, sheep, pumpkin, carrot).
  - ✅ Isometric animation sprites (`art/iso/farm/`): stand, eat, sleep and back views for each animal, and sprout/growing/ripe for each crop. Made with `genart.py poses`: the first pose is generated, the rest are edits of it so the animal stays the same. Motion (waddle, peck, breathing, Z's) is done in code.
  - ⚠️ **The free allowance (about 85 images a day) is shared by every chat using the Cloudflare token**, but `genart.py usage` only counts images made in that chat's own workspace, so it can overstate what's left. When the allowance runs out the script stops with "Free daily limit reached (resets 7pm Central)" and nothing is lost. To avoid two chats competing, let one chat do art at a time, and do big batches right after 7 PM Central.
  - Later: a small Cloudflare Worker so the game itself can generate pictures, with a kid-safe prompt wrapper.

- ✅ **Saved data: decided on Firebase Realtime Database (free Spark plan).** No credit card, live updates to every device, works from GitHub Pages. Everything lives under `families/<family code>/`, so the family code is the key (no passwords).
  - Why not the others: Supabase's free plan pauses projects after a week without use, and Firebase *Storage* (for files) now needs a paid plan, so voice clips and drawings are saved as small compressed data inside the database instead.
  - ✅ Firebase project `kapanigans` is connected. Rules only allow reading and writing under `families/<code>` (codes of 4+ characters); everything else is denied.
  - ✅ Live game sync moved from the public HiveMQ relay to Firebase, so everything uses one service.
- ✅ **Read-aloud helper:** `say()` / `sayLittle()` use the device's built-in voice. Little players already hear their tool, color, picture and reaction names; there's a 🔊 on/off button in the lobby. Ready for stories, chore instructions and inbox messages.
- ✅ **Game menu:** the placeholder cards are replaced with Bedtime Story, Kapanigan Farmstand and Inbox (marked Soon; tapping one says "Coming soon!").

## Done

- ✅ Own-voice stories (#1), family voice clips (#7), Show it! (#12), parent inbox view (#4), photo avatars (#2)
- ✅ One device per person (#11) and front/back camera flip (#12)
- ✅ Release 1 (Grown-ups corner): hold-to-open grown-ups area, voice settings (#7), 4-character family codes (#6), clear any inbox
- ✅ Release 2: usage tracking, grown-up reports dashboard and weekly Inbox report (#8)
- ✅ Watch mode: anyone not in a game can tap 👀 Watch on an in-progress game to see it live (view only, can send cheers; doesn't join the video call)
- ✅ Connection reliability: live play on Firebase (no public relay), every stroke saved so dropped or reloaded devices catch up, quick recovery when an iPhone comes back to the app, 60-second "reconnecting…" grace period, lighter traffic (fewer finger updates, smaller video), and a connection light for each player

- ✅ Color Together: co-op coloring for 1–4 players with Little and Big tools, 3 pictures, undo, and saving the finished picture
- ✅ Family code sync over the relay service (same one as the 31 game)
- ✅ Video chat bubble when exactly 2 players are in a game
- ✅ Home-screen icon
- ✅ Grown-up personas (#2) and the "Who are you!? :)" welcome
- ✅ Read-aloud helper and new game menu
- ✅ Bedtime Story: make, send, unwrap, read aloud with word highlighting, thank-yous
- ✅ Firebase storage and the Inbox (#4): stickers, phrases, typed notes, drawings, voice messages, colored pictures, story gifts and thank-yous
