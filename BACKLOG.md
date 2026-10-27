# Kapanigans Backlog

Status key: 🆕 new · 🔍 needs decisions · 🛠️ in progress · ✅ done

Levels used below: **Little** = Violet level (age 3), **Big** = Quinn level (age 6).

---

## 1. 🛠️ New game: Write a Bedtime Story (playable; waiting on Firebase for reliable delivery)

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
- [~] The gift arrives on the recipient's device even if they weren't online when it was sent: works today through retained messages on the relay, which the relay may drop. Moves to Firebase for a guarantee.
- [~] "My stories" shelf to rewatch received stories: works, but each device keeps its own copy. Firebase will sync it across devices.
- [x] Thank-you reactions (❤️ 😴 🤗) go back to the author, even if they're offline

**🔍 Decisions needed**
- ~~Where gifts are stored~~ → decided: Firebase (see Shared groundwork). Gifts land in the recipient's **Inbox** (#4).
- Can grown-ups send stories too, for example Gramma Mia sending one to Violet?
- Should the author be able to record their own voice instead of the built-in reader?

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
- Avatars: shipped with emoji (🧔 Joe, 👩 Layla, 👩‍🦰 Lisa, 🧑 Parker, 🍎 Apple G, 🧢 Uncle Jeff, 👵 Gramma Mia, 👴 Grandpa George). Swap any of them for a photo or drawing later?
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
- [ ] A shared farm view that stays in sync across devices
- [ ] At least 3 crops and 2 animals at launch
- [ ] Every chore has a Little and a Big puzzle version
- [ ] Farm progress is saved and still there the next day
- [ ] Gentle failure only: wrong answers get a "try again" with a hint, never a penalty or a dead plant
- [ ] Each player's farm time stops at 30 minutes and reopens 24 hours later, on any device
- [ ] Puzzle cooldowns are tuned so finishing all available chores takes about 30 minutes
- [ ] A 5-minute "sleepy animals" warning and a goodnight screen with a countdown

**🔍 Decisions needed**
- ~~Saving the farm~~ → decided: Firebase (see Shared groundwork).
- Should crops be able to wilt if nobody visits, or stay safe forever (kinder for little ones)?
- ~~Daily play limit~~ → decided: 30 minutes per player, then a 24-hour rest (see above).
- Do grown-ups follow the same 30-minute limit, or are they exempt?
- Can a grown-up grant extra time or reset a player's cooldown (for a sick day or a road trip)?
- Should the 24 hours run from when the time ran out (as written), or should the farm reopen every morning at a set time (for example 7 AM), which is easier for little ones to understand?

---

## 4. 🆕 Inbox for every persona

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
- Messages stay until you delete them; grown-ups can clear any inbox

**Acceptance criteria**
- [ ] A message sent to a device that's asleep or closed is waiting in the inbox when it's next opened
- [ ] Unread badge on the lobby mailbox and on each person in the "Who are you?" screen
- [ ] Violet can send and open messages without reading anything
- [ ] Voice messages up to 30 seconds

**🔍 Decisions needed**
- Should kids be able to message only family personas, or Bear friend and Fox friend too?
- Should grown-ups see every inbox (a parent view), or only their own?

---

## Shared groundwork (needed by #1, #3 and #4)

- ✅ **Saved data: decided on Firebase Realtime Database (free Spark plan).** No credit card, live updates to every device, works from GitHub Pages. Everything lives under `families/<family code>/`, so the family code is the key (no passwords).
  - Why not the others: Supabase's free plan pauses projects after a week without use, and Firebase *Storage* (for files) now needs a paid plan, so voice clips and drawings are saved as small compressed data inside the database instead.
  - 🛠️ Waiting on Joe: create the Firebase project and send over its web config.
  - Later: consider moving live game sync from the HiveMQ relay to Firebase too, so everything uses one service.
- ✅ **Read-aloud helper:** `say()` / `sayLittle()` use the device's built-in voice. Little players already hear their tool, color, picture and reaction names; there's a 🔊 on/off button in the lobby. Ready for stories, chore instructions and inbox messages.
- ✅ **Game menu:** the placeholder cards are replaced with Bedtime Story, Kapanigan Farmstand and Inbox (marked Soon; tapping one says "Coming soon!").

## Done

- ✅ Color Together: co-op coloring for 1–4 players with Little and Big tools, 3 pictures, undo, and saving the finished picture
- ✅ Family code sync over the relay service (same one as the 31 game)
- ✅ Video chat bubble when exactly 2 players are in a game
- ✅ Home-screen icon
- ✅ Grown-up personas (#2) and the "Who are you!? :)" welcome
- ✅ Read-aloud helper and new game menu
- ✅ Bedtime Story: make, send, unwrap, read aloud with word highlighting, thank-yous
