# Kapanigans Backlog

Status key: 🆕 new · 🔍 needs decisions · 🛠️ in progress · ✅ done

Levels used below: **Little** = Violet level (age 3), **Big** = Quinn level (age 6).

---

## 1. 🆕 New game: Write a Bedtime Story

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
- [ ] At least 3 story templates, each with 5–8 blanks and 4–6 pages
- [ ] Little authors can finish a story without reading anything
- [ ] Drawn characters appear on the story pages with at least 4 animation types
- [ ] The gift arrives on the recipient's device even if they weren't online when it was sent
- [ ] A "Gift shelf" where each child can rewatch stories they've received

**🔍 Decisions needed**
- **Where gifts are stored:** the relay service only passes messages along; it doesn't reliably keep them. To deliver a gift to a sleeping iPad we need storage, such as a free Firebase or Supabase project, or keeping gifts on the relay as retained messages (simple, but not guaranteed to last).
- Can grown-ups send stories too, for example Gramma Mia sending one to Violet?
- Should the author be able to record their own voice instead of the built-in reader?

---

## 2. 🆕 New persona: Grown Ups

Add grown-up players to the **Who's playing?** screen.

**Names:** Joe, Layla, Lisa, Parker, Apple G, Uncle Jeff, Gramma Mia, Grandpa George

**Details**
- All grown-ups get **Big (Quinn level)** tools for now.
- They count as a player seat (still 4 players max per game) and show up in the lobby, seat chips and zone labels like the kids do.
- Each grown-up gets their own emoji avatar and color.
- Layout: the kids stay big at the top, with a smaller **Grown ups** row underneath so kids don't tap the wrong one.
- Video chat rule stays the same: it turns on when exactly 2 players are in a game, including a grown-up and a kid. This lets Gramma Mia color with Violet over video.

**Acceptance criteria**
- [ ] All 8 grown-ups are selectable and remembered per device, like the kids
- [ ] Grown-ups get Quinn-level tools in Color Together
- [ ] Bear friend and Fox friend stay available

**🔍 Decisions needed**
- Avatars: emoji (for example 🧔 Joe, 👵 Gramma Mia, 🍎 Apple G), or a photo or drawing for each person?
- Should grown-ups get a separate "grown-up level" later, such as with hints turned off or as a game host?

---

## 3. 🆕 New game: Kapanigan Farmstand

A **live co-op farm** that the kids share. They grow crops and raise animals together, and each chore is a short, age-appropriate learning puzzle.

**The farm**
- One shared farm per family code. Everyone sees the same farm live, with each player's finger marker, like Color Together.
- **Crops:** carrots, tomatoes, corn, pumpkins and strawberries. Plant → water → grow → harvest.
- **Animals:** chickens (eggs), a cow (milk), a sheep (wool) and a pig (happiness). Feed → care → collect.
- Things grow over real time (minutes to hours), so the kids come back later to check on the farm.
- A **farmstand** where harvested goods get "sold" for coins to buy new seeds, animals and decorations.

**Chore puzzles by level**

| Chore | Little (age 3) | Big (age 6) |
|---|---|---|
| Water | Tap the matching color watering can | Count the drops: "This plant needs 7" |
| Plant | Drag the seed to the matching picture | Plant in a pattern (ABAB rows) |
| Harvest | Count up to 5 carrots with taps | Simple adding: "3 carrots + 2 carrots" |
| Feed animals | Match the animal to its food | Read the word: "HAY", "CORN" or "SLOP" |
| Collect eggs | Find the hidden eggs (tap) | Sort eggs by size or color |
| Sell at farmstand | Tap the coin to pay | Make change with coins up to 20¢ |

**Co-op moments**
- Some jobs need two players at once. For example, one holds the bucket while the other milks, or one plants while the other waters.
- A shared goal board, such as "Fill the farmstand with 10 pumpkins by Saturday," with a celebration when it's done.

**Acceptance criteria**
- [ ] A shared farm view that stays in sync across devices
- [ ] At least 3 crops and 2 animals at launch
- [ ] Every chore has a Little and a Big puzzle version
- [ ] Farm progress is saved and still there the next day
- [ ] Gentle failure only: wrong answers get a "try again" with a hint, never a penalty or a dead plant

**🔍 Decisions needed**
- **Saving the farm:** same storage question as the bedtime stories. A living farm has to be stored somewhere besides the devices.
- Should crops be able to wilt if nobody visits, or stay safe forever (kinder for little ones)?
- Is there a daily play limit or bedtime cutoff for the farm?

---

## Shared groundwork (needed by #1 and #3)

- 🔍 **Saved data:** choose a storage service for gifts and farm progress. The relay service only passes messages along, so it can't store them.
- 🆕 **Read-aloud helper:** one shared text-to-speech function for stories, chore instructions and Little-level labels.
- 🆕 **Game menu:** move the "Soon" placeholder cards (Puzzle Pals, Animal Sounds, Shape Hunt) behind the new games, or replace them.

## Done

- ✅ Color Together: co-op coloring for 1–4 players with Little and Big tools, 3 pictures, undo, and saving the finished picture
- ✅ Family code sync over the relay service (same one as the 31 game)
- ✅ Video chat bubble when exactly 2 players are in a game
- ✅ Home-screen icon
