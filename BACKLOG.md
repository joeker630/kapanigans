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

## 3. 🛠️ New game: Kapanigan Farmstand

**✅ Playable so far (v1, on this device only, nothing saved yet)**
- An isometric farm field: the hen, cow, pig and sheep wander, graze and nap on their own, with walk (waddle, front and back views), eat and sleep animations.
- Tap an animal to feed it (corn or grass); tap a sleeping animal to wake it; tap the grass to call the nearest animal over.
- Carrot and pumpkin plots grow from sprout to growing to ripe (about 36 seconds); tap a sparkly ripe crop to pick it into the basket.
- Still to build: chore puzzles by level, co-op play, saving the farm in Firebase, and the 30-minute play limit.

**🎨 Farm art still needed** (isometric sprite style, `art/iso/farm/`, made with `tools/genart.py`)

✅ Done: hen, cow, pig and sheep (stand, eat, sleep, back) · carrot and pumpkin (sprout, growing, ripe).

About **45 images** left including retries, which is roughly one day of the free allowance if nothing else is using it. Make them in this order:

*Batch A — needed for the chore puzzles (about 25)*
- [ ] Crops, growing + ripe (the carrot sprout is reused for every crop): tomato, corn, strawberry — 6
- [ ] Seed packets, one per crop (Plant puzzle: match seed to picture): carrot, tomato, corn, pumpkin, strawberry — 5
- [ ] Animal goods to collect: white egg, brown egg (sizes and colors done in code for the sorting puzzle), milk pail, ball of wool — 4
- [ ] Animal food (Feed puzzle: match the animal to its food; Big reads HAY / CORN / SLOP): hay bale, corn pile, slop bucket, chicken feed scoop — 4
- [ ] Tools: watering can in **white** so the game can tint it (Little's "tap the matching color" puzzle), empty bucket (co-op milking), harvest basket — 3
- [ ] Sheared sheep (shown after wool is collected) — 1
- [ ] Hiding spots for egg hunt: hay pile, bush — 2

*Batch B — the farm itself (about 11)*
- [ ] Buildings: red barn, chicken coop, farmhouse (door to the dressing room), farmstand stall with an awning — 4
- [ ] Fence: straight piece and corner (mirrored in code for other directions) — 2
- [ ] Nature: round tree, apple tree, flower patch, rock, small pond — 5

*Batch C — farmstand shop unlocks (about 8)*
- [ ] Decorations to buy with coins: scarecrow, windmill, flower pot, bench, mailbox, lantern — 6
- [ ] Coins for "make change" (Big): copper coin and silver coin, blank, with the value drawn on in code — 2

*Done in code (no images):* sparkles, water drops, hearts for a happy pig, sun moving across the sky, the goodnight moon and stars, chore cooldown rings.
*Covered elsewhere:* farmer avatars, costumes and following pets are in **#10**.
*Only if decided:* wilted crop stages, if crops can wilt (see decisions below) — 5 more images.

**⚠️ Art style check before #10 starts:** #10 says to use the chunky 3D hen (`art/farm/hen.webp`) as the style reference, but the farm now uses the flatter **isometric sprite** style (`art/iso/farm/`). Avatars walking on the farm should match the isometric animals, so #10 should use an isometric animal (for example `art/iso/farm/hen/stand.webp`) as its reference.

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

**🧑‍🌾 Farmer avatars (customizable)**
- Each player walks around the farm as their own **farmer avatar**, visible to everyone in the game. It replaces the plain finger marker, and each avatar's name floats above it.
- **Customize from a dressing room** before entering the farm (and anytime from the farmhouse):
  - **Little:** big picture choices for hair, skin tone, a hat (straw hat, cap, bonnet, flower crown), overalls or a dress, boots, and a color for each. Every choice is read aloud.
  - **Big:** more options for each part (hairstyles, glasses, freckles, bandanas, aprons, gloves), patterns, and color schemes.
  - **Grown-ups** get Big options.
- **Unlocks from playing:** coins from the farmstand buy extra items, such as a cowboy hat, rain boots, a pumpkin costume or a pet that follows you (a dog, cat or duckling).
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
- [ ] A shared farm view that stays in sync across devices
- [ ] At least 3 crops and 2 animals at launch
- [ ] Each player can customize a farmer avatar that everyone sees on the farm, and it's remembered across devices
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
- ~~Avatar everywhere?~~ → decided: **yes**. The custom avatar replaces the emoji avatar in the lobby, the "Who are you!? :)" screen, seat chips and all games (including as a model option in Fashion Show).
- ~~Dressing room and farm time~~ → decided: **no**. Time in the dressing room doesn't count toward the 30 minutes.
- Can a grown-up grant extra time or reset a player's cooldown (for a sick day or a road trip)?
- Should the 24 hours run from when the time ran out (as written), or should the farm reopen every morning at a set time (for example 7 AM), which is easier for little ones to understand?

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
- Should grown-ups see every inbox (a parent view), or only their own? *(For now: only their own.)*

---

## 5. 🆕 New game: Fashion Show

Kids design outfits for a "model," then watch the model walk an animated runway, take photos and call out poses.

**Designing the outfit (by level)**
- **Little (Violet):** drag and drop ready-made pieces onto the model: tops, bottoms, dresses, shoes, hats, bags and accessories (crowns, sunglasses, capes). Tap a piece to change its color from a few big color dots. Every piece and color name is read aloud.
- **Big (Quinn):** pick from more advanced templates (for example a ball gown, a superhero suit, a rock star outfit or a sports uniform) and customize each part: sleeves, length, collar and pattern (stripes, polka dots, stars, hearts). Choose from named color schemes (Ocean, Sunset, Candy, Forest, Galaxy) or pick each color separately. Can also draw a design onto the fabric with the Color Together tools.
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
- Should we do the recorded-voice option for the most common phrases now, or later?

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

## 10. 🆕 Avatar builder art (farm style)

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
- Same art kit and house style as the farm animals. The farm hen is used as the **style reference** (`--ref art/farm/hen.webp`), so the avatars look like they belong on the farm.
- Same layering approach as #9: one base body that every part fits on, parts listed in the manifest with their slot, offset and scale, and white parts tinted in the game.
- **Little-friendly:** big, simple shapes that still read clearly when small, such as on a seat chip or the lobby.
- Extra poses for the base body (walk, wave, cheer, yawn) are animated in code by moving the parts, not drawn separately.

**Shared work with #9**
- One dress-up engine, built once: slots, layering, tinting, patterns and saving each look per persona.
- Avatar parts and Fashion Show clothes can mix: a Fashion Show piece can be worn by your avatar, and your avatar can walk the runway.

**Acceptance criteria**
- [ ] Every part matches the farm animals' style side by side on a contact sheet
- [ ] At least 6 skin tones, 10 hairstyles, 6 hats and 6 outfits at launch
- [ ] Hair and clothes can be tinted to any color
- [ ] An avatar stays readable at small sizes (seat chips, lobby)
- [ ] Each person's avatar shows up the same on every device

**🔍 Decisions needed**
- ~~Body size~~ → decided: **everyone is the same size**, kids and grown-ups use the same base body.
- ~~Animal avatars~~ → decided: **humans only**. Costumes (pumpkin, chicken) are worn by the human avatar, and pets just follow along.

---

## Shared groundwork (needed by #1, #3, #4, #5 and #8)

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
