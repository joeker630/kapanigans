# Kapanigans release notes

Newest first. Each release has kid-friendly notes (shown to everyone in the game's **What's new!** card) and grown-up notes (shown to grown-ups only). See backlog #20.

---

## 1.20: Color your own photo 📷
**October 31, 2026**

### For everyone
- 📷 **Your own photo:** in Color Together, tap **Your own photo**, take a picture (or pick one), and it turns into a coloring page!
- 🌈 **Light colors or black & white:** choose **Light colors** to see a pale version of the real colors underneath, so you know what color goes where, or **Black & white** for a plain coloring page.
- ✏️ **Simple, Medium or Lots of lines:** pick how many shapes there are to color. Violet starts on Simple.
- 🪣 The paint bucket fills each shape cleanly, and everyone coloring with you gets the same page.

### For grown-ups
- The photo is cropped to the page, softened, split into flat color patches (k-means), with specks merged into neighbors; a line is drawn wherever two patches meet, so every shape is closed for the fill tool. It runs on the device in about half a second.
- The page is shared through `games/<id>/photo`: the line art as a PNG (about 150–200 KB, so every device finds exactly the same shapes) and the light-color guide as a small JPEG. Like every game, it's removed after 3 days.
- The light-color guide is a separate layer under the paint: color and fill cover it, the eraser shows it again, and it's included when the finished picture is saved.
- "Take a picture" uses the device camera app; "Pick a photo" opens the photo library.

---

## 1.19: Steadier video calls 📞
**October 30, 2026**

### For everyone
- 🔊 **Voices don't cut out:** when you switch screens during a call, everyone's voice keeps playing without a hiccup.
- 📶 **Calls fix themselves:** if the Wi‑Fi blips, the call patches itself back up in a couple of seconds instead of hanging up and starting over.
- 🙂 **Voice first on bad Wi‑Fi:** if the internet gets really slow, your video takes a little break and your voice keeps going. Everyone sees your picture until the video comes back.

### For grown-ups
- Remote voices now play from hidden audio players that never move; the videos are always muted. Moving a video between the home cards and the bubble could pause it in Safari, which cut out the voice.
- A dropped or failed connection is repaired with an ICE restart on the same call (the side that placed the call restarts it, up to 3 tries, then calls fresh). Also retried when the device comes back online.
- New fourth quality step: video sending is paused (voice only) when packet loss or jitter persists at the lowest video level. Others see your face picture via presence (`vp`), and video resumes after the network has been clean for a while.
- A stalled incoming video (muted track) shows the face picture instead of a frozen frame.
- Video and voice bitrates are unchanged (larger tiles than Thirtyone, so its lower 160×120 setting wasn't brought over).

---

## 1.18: Spider repellent 🧴
**October 29, 2026**

### For everyone
- 🧴 **Spider repellent in Snake Race:** grab the green 🧴 box and for 12 seconds the spider can't snip your tail. He just bounces off you like a wall! The spider can't pick up repellent either. He bounces right off the box.

---

## 1.17: Short voice messages work every time 🎤
**October 29, 2026**

### For everyone
- 🎤 **Short voice messages:** in the Inbox, voice messages of any length from 1 to 30 seconds now record and send, including quick 10-second hellos. While you record, a counter shows how many seconds so far.

### For grown-ups
- Safari sometimes hands over a recording a moment after it stops. Short messages were missing it and showing "That was too short." The game now waits for the recording before checking it.
- Recording during a video call uses a copy of your microphone. Recording no longer turns your call mic back on if you'd muted it.
- Voice messages and family voice clips record at slightly higher quality (48 kbps).

---

## 1.16: Watch out for the spider! 🕷️
**October 29, 2026**

### For everyone
- 🕷️ **Joe is a spider in Snake Race:** a glowing white spider with scissors and no tail. He gets bigger as he eats. If he runs into your snake's tail, ✂️ snip, it's cut off and spills out as snacks. He can't knock you out, so bumping into him is safe. Keep your tail away from the spider!
- 🧩 **One puzzle after a crash:** everyone solves just one puzzle to get back into Snake Race.

### For grown-ups
- 🐍 Grown-ups go back into Snake Race after one respawn puzzle, win or lose. Joe's snips count as bumps on the podium; head-to-head with the spider just bounces.

---

## 1.15: Bigger picture on phones 📱
**October 29, 2026**

### For everyone
- 🎨 **Bigger coloring:** with a phone or iPad sideways, the coloring picture now fills the full height. The spare width goes to the tools instead of empty blue space, so the tools are bigger too.
- 🏠 **Less wasted space:** the home button now shares a line with the players or the reactions.
- 📹 **Videos fit on short screens:** the video column starts at the top and shrinks the videos as needed, so the buttons are never cut off at the bottom.

### For grown-ups
- 📲 **Full screen, no Safari bars:** a web page can't hide Safari's address bar and tabs. Add Kapanigans to the Home Screen instead: in Safari, tap Share › **Add to Home Screen**, and turn on **Open as Web App** if you see it. Opening it from that icon runs it full screen. Grown-ups see a one-time tip about this on iPhone and iPad.
- Added a web app manifest and a see-through status bar, so the home-screen version uses the whole screen.

---

## 1.14: Neater video buttons and coloring tools ✨
**October 29, 2026**

### For everyone
- 📹 **Neater video buttons:** the video controls are now one slim bar of simple icons under the videos: microphone, camera, shrink, and turn off (red). A red button means it's off. To flip the camera, tap the little 🔄 in the corner of your own picture.
- 🎨 **Coloring tools fixed:** on iPads and phones the tools, stickers and colors no longer squeeze together or overlap. Everything shrinks together to fit the left column neatly, with nothing cut off.

### For grown-ups
- The tools used CSS zoom to shrink, which Safari doesn't apply to everything inside. Every tool, sticker and color now sizes from one scale that the game lowers until it all fits. Checked from big iPads down to phones held sideways.

---

## 1.13: Clearer voices on calls 🎤
**October 29, 2026**

### For everyone
- 🎤 **Clearer voices:** voices on family calls cut out less and sound fuller, even on busy Wi-Fi.

### For grown-ups
- Each voice packet now also carries a spare copy of the one before it (RED). If one goes missing on the Wi-Fi, the next one fills the gap instead of a crackle.
- Silence suppression is off. It was clipping the first sound of a word after a pause.
- Voices get more room: 48 kbps (was 32) plus error correction, with a little more buffer (0.15 seconds) to smooth out bumpy Wi-Fi.
- Voices come first: if others start losing your voice or hearing it in bumps, your video automatically steps down to make room.
- The microphone asks for a single channel at 48 kHz, the best fit for voice calls.

---

## 1.12: Smoother video, tidy coloring tools 🎨
**October 29, 2026**

### For everyone
- 📹 **Smoother video calls:** family videos move more smoothly (24 frames a second, up from 15) and look a little sharper.
- 🎨 **Coloring tools always fit:** on the coloring page, every tool and color fits in the left column with no scrolling, even with four people coloring. Players' names sit side by side to save room.

### For grown-ups
- Calls now ask for H.264 video, which iPads and iPhones encode in hardware, so the tablet works less and video stays smooth while games run.
- When the Wi-Fi or the tablet struggles, the video first gets a smaller picture but keeps moving smoothly. It only lowers the frame rate as a last step, and it waits until the connection has been clean for about 15 seconds before stepping back up, so quality doesn't bounce up and down.
- Video has a slightly bigger buffer (0.2 seconds) to smooth out bumpy Wi-Fi.

---

## 1.11: Family videos on every page 📹
**October 29, 2026**

### For everyone
- 📹 **Videos everywhere:** the family video column now has its own space on every page: Capture the Flag, reading a story, and the drawing pad in My own story, as well as coloring, the farm, Snake Race, dress up, the Inbox and Grown-ups. Nothing gets covered.

### For grown-ups
- Capture the Flag's map now shrinks to make room for the videos, and the "Draw your character" pad no longer hides them.
- Fixed a rare farm hiccup the first time a family opens the farm (the farm and its first orders were saving at the same moment).
- The home screen still shows everyone's video on their person cards, so the column only appears once you're inside a game.

---

## 1.10: A quieter reading voice 🔉
**October 29, 2026**

### For everyone
- 🔉 **Quieter reading voice:** tap the 🔊 button at the top to make the voice softer. Each tap goes Loud › Medium › Quiet › Off, then back to Loud.
- 📹 **Slimmer video column:** the video buttons now sit in a neat 2 by 2 square, so the family videos take up less room on the right.
- 🎨 **Videos while coloring:** the family videos now have their own column on the right of the coloring page, so the picture isn't covered and doesn't squeeze under the tools.

### For grown-ups
- Grown-ups › 🔊 Voice has a volume slider for you and, for grown-ups, for Violet and Quinn. It's saved for the family, so Violet's setting follows her to every device. Violet starts at 50%.
- The setting also softens recorded voice clips and Inbox voice messages.
- On iPad and iPhone, Safari doesn't always lower the built-in voice. If it stays loud, turn the device volume down too.

---

## 1.9: Write it, and the pictures appear ✨
**October 28, 2026**

### For everyone
- ✨ **Write my story:** in Bedtime Story › Make a story, pick **✨ Write my story**, choose a theme (Bedtime, Space adventure, Under the sea, Fairy tale castle, Forest friends and more), then type or 🎙️ tell your story. Tap **Make my pictures** and Kapanigans turns it into pages with places, characters, moves and feelings that match your words.
- 🧔 **Family in the pictures:** write a family name (tap it under "Who's in it?") and their cartoon shows up in a pose that fits, like Joe running, waving or reading a story.
- 🔄 **Try another:** on the "Here's your story!" screen, tap a picture to see it move, 🔄 for a different place, 🎲 for new moves, or ✏️ to change anything on that page.
- 🧩 **Build it page by page** is still there for making every page yourself.

### For grown-ups
- The story engine runs on the device with no internet: blank lines (📄 New page) start a new page, otherwise one or two sentences make a page (12 at most). It matches about 200 words to pictures, places, moves and feelings, and keeps the same friends on the next page when nobody new is named.
- Changing the words or theme and tapping Make my pictures again redraws the pages (hand edits on those pages are replaced). Drafts remember the words and theme.

---

## 1.8: Family cartoons in stories 🧔
**October 28, 2026**

### For everyone
- 🧔 **Star in your story:** in ✨ My own story, tap ➕ Add › 👨‍👩‍👧 Family, pick a person, then a pose (running, waving, reading a story, pillow fight and lots more). New cartoons show up as soon as they're made.
- 🔄 **Change pose:** tap a family cartoon on the page and pick a different pose or outfit. It stays in the same spot with the same moves.

### For grown-ups
- Cartoons load from the family's private space only when the Family tab is open, one picture at a time as it scrolls into view. The list of names is re-checked at most once a minute, so new uploads appear without reloading the game.

---

## 1.7: Storybook magic 📖
**October 28, 2026**

### For everyone
- 📖 **A real storybook:** stories now sit in a golden picture-book frame with a cozy reading font, and pages **turn like a book** when you go forward or back. Fireflies drift over the Sleepy Dragon, Moon Picnic and Lost Teddy pages too.
- ✨ **Drawings glow:** characters you draw get a soft glowing outline and a little shadow on the ground, so they look great on every scene.
- 〰️ **Smooth lines:** wobbly lines come out neat. Violet's crayon is always smooth; Quinn and grown-ups can turn **Smooth** on or off on the drawing pad.
- 🔔 **Story sounds:** a page-turn swish, a whoosh when someone flies or runs, a pop, a twinkle when you tap to wake a character, an owl hoot in the forest, and a music-box lullaby at "The End." Tap 🔔 in the story to turn sounds off.
- 🔤 **Spelling helper:** when Quinn or a grown-up types a page, tricky words get a wavy red line with ideas to tap ("elefant" → elephant). 🔊 hears the word, 👍 **Keep it** for made-up and silly words.
- 🎨 **Draw your own cover:** on the last step of ✨ My own story, tap **Draw a cover**. It shows on the story shelf and in drafts.

### For grown-ups
- 🧩 Sounds are all made in code (no downloads) and remember their on/off setting on each device.
- 📚 The spelling helper uses a list of about 39,000 common words (kid-safe filtered), loaded only when someone types a story page, plus family names and the story builder's characters.
- 🎨 A drawn cover is a small picture saved with the story. Older copies of Kapanigans still show the cover emoji.

---

## 1.6: The family dashboard 📈
**October 28, 2026**

### For grown-ups
- 📈 **Family dashboard (Joe):** in 🔒 Grown-ups › Reports, **📈 Family dashboard** puts everyone on one page for the last 7 days, 30 days or all time:
  - headline numbers (family play time, active profiles, sessions, average session, puzzles and first-try %, busiest time), each compared with the period before
  - each person's **share of family play time**, kids vs grown-ups, and time by game
  - **everyone at a glance**: time, % of family, change, sessions, days active, top game, puzzles and first-try %, last played (tap a row for the full report)
  - **right on the first try** for each person, and **skills side by side** (kids and grown-ups) with ▲ ▼ = changes from the week before
  - **week by week** first-try % for the last 6 weeks, when the family plays (day × hour), and the play timers (breaks and extra time)
- Grown-up puzzles are now recorded by name (sudoku, word guess, blackjack, minesweeper, traffic jam) so they show up as skills.

---

## 1.5: Everyone's usage for Joe 📊
**October 28, 2026**

### For grown-ups
- 📊 **Joe sees everyone:** in 🔒 Grown-ups › Reports, Joe now has an **Everyone** view (each person's time played in the last 7 days, times played, days, most-played game and when they last played) plus a full report for each grown-up as well as the kids. Other grown-ups still see the kids' reports.
- ⏱️ Reports now also count time in Capture the Flag, the dressing room and the Grown-ups area.

---

## 1.4: Ask for help on the farm ❗
**October 27, 2026**: night update.

### For everyone
- ❗ **Asking for help:** when you start a team chore, you glow yellow with a big ❗ over your head on everyone's farm. Tap the ❗ (or the person) to walk over and help.
- 🤝 **Team chores are for 2:** one person asks, one person helps, and then it's full.

---

## 1.3: Jeppson comes to the farm 🐶
**October 27, 2026**: night update.

### For everyone
- 🐶 **Jeppson on the farm:** Jeppson the corgi trots around the farm, sniffs, wiggles, sits and naps. Tap him for a woof and a happy wiggle!
- 💩 **Poop patrol:** every so often Jeppson leaves a poop (with buzzing flies). Tap it and solve a quick puzzle to scoop it up for 2 Moolah. Nothing bad happens if you leave it.
- 🤝 **More team chores:** stack the hay, fix the fence, fill the water trough, pick apples, sweep the barn, carry the giant pumpkin, herd the sheep, and give Jeppson a bath, together. Everyone taps the big button 10 times to finish, for 2 Moolah each.

### For grown-ups
- 🧪 The new team chores are simple placeholders (tap a button) until the real activities are built. Jeppson is drawn in code until his art is approved.

---

## 1.2: Quinn's play timer ⏰
**October 27, 2026**: late evening update.

### For everyone
- ⏰ **Quinn's play timer:** Quinn now gets a countdown and a break screen too, just like Violet.

### For grown-ups
- ⏰ **Timers in Grown-ups:** a new **⏰ Timers** tab shows each kid's time left or break, with play time, break length and extra time settings. **Only Lisa and Parker can change Quinn's timer.** Any grown-up can still hold the 🔒 on the break screen, or tap **Give more minutes** or **Fresh start** in the tab, and it reaches the kid's iPad right away.

---

## 1.1: Play time and a quieter inbox ⏰
**October 27, 2026**: evening update.

### For everyone
- ⏰ **Violet's play timer:** Violet plays for 30 minutes at a time, with a countdown at the top of the screen. When it's time for a break, a sleepy moon says "Great playing, Violet!" and the games rest for 30 minutes. Her video chat stays on.
- 💌 **Simpler sending:** the Inbox now offers Sticker, Drawing, Type it and Voice (the "Say something" choice is gone).

### For grown-ups
- ⏰ **Grown-up override:** on Violet's break screen, hold the 🔒 for 3 seconds to give her 15 more minutes. Her time follows her to any device, and a 30-minute break away from the game also starts a fresh 30 minutes.
- 🔇 **Quiet inbox for grown-ups:** messages no longer read themselves aloud or auto-play for grown-ups; tap 🔊 or ▶️ when you want to hear one. The kids still hear theirs.

---

## 1.0: Welcome to Kapanigans! 🎉
**October 27, 2026**: everything built so far, made in one day.

### For everyone
- 🖍️ **Color Together:** color a picture together with up to 4 people. Everyone gets their own part, or you can share the whole page. There are 3 pictures plus a **blank page**, undo, and saving your finished picture. Others can tap 👀 **Watch** to see a game live and send cheers.
- 🦄 **Violet's crayons:** big, easy tools, with white, black and grey crayons, an eraser and a **sparkly Unicorn brush**.
- 🌙 **Bedtime Stories:** make a story as a **gift** for someone. Pick a story and fill in the blanks, draw characters that hop, wiggle and float, then send it. Read it aloud with the reading voice or **your own voice**, and get ❤️ 😴 🤗 thank-yous back.
- 📖 **My own story:** build a whole story page by page, with 13 scenes, characters, your avatar, drawings, 22 moves, paths to follow, feelings, 9 magic effects, and typed, spoken or recorded words. Drafts are saved, and stories wait for ▶️ Play.
- 🚜 **Kapanigan Farmstand:** a family farm everyone shares. Plant, water and harvest crops, and feed animals and collect eggs, milk and wool. **Every chore is a learning puzzle.** Sell at the farmstand for **Moolah**, shop the Farm Store (seeds, buildings, decorations, a bigger field), fill **family orders** on the corkboard, and share goods in the **Family Basket** and **Family Bank**. Press and hold to move things around.
- 🧩 **Puzzles for every level:** counting, colors, matching, patterns, letters and word tracing (CAT, HAT, ICE…), memory, jigsaws (Violet's are now 9 pieces), building shapes, making change, shadow match, big-bigger-biggest, and tap the numbers in order. Grown-ups get real games they can lose: mini sudoku, word guess, blackjack, minesweeper and traffic jam.
- 🧑‍🌾 **Your own avatar:** dress up in the dressing room with skin tones, faces, hair, hats, clothes, glasses and more. Your avatar shows up everywhere, and walks around the farm to do your chores.
- 💌 **Inbox:** send stickers, quick phrases, notes, drawings, voice messages, colored pictures and story gifts to anyone, even if they're not playing right now.
- 📹 **Family video:** see and hear each other while you play. Flip between the front and back camera (🔄 and **Show it!**), minimize the bubble without muting anyone, or turn video off for your device. Calls are smoother with 3 or more people.
- 🚩 **Capture the Flag (Beta):** grab the other team's flag on a big oval field, with power-ups and **Jeppson** leaving poops that slow you down. **Play together:** invite family and pick teams before you start, or join a game that's already going. Computer players fill any empty spots. Get tagged? Solve a quick puzzle to get back in!
- 🐍 **Snake Race (Beta):** steer your snake anywhere on a big dark field full of glowing candy and fruit, and grow the longest snake before time runs out. Hold your finger where you want to go, hold ⚡ to boost, and grab glowing boxes for 🧲 magnet, ⚡ speed, ✖️3 snacks and ⭐ go-through-snakes. Bump into another snake and half of you spills out; solve a quick puzzle to get back in! Computer snakes fill in when there aren't 4 players.
- 👋 **Who are you!? :)** Pick yourself when you open Kapanigans. Each person plays on one device at a time, and the **Who's on** cards show where everyone is with a one-tap Join.
- 👨‍👩‍👧 **The whole family's here:** Violet, Quinn, Bear friend, Fox friend, and grown-ups Joe, Layla, Lisa, Parker, Apple G, Uncle Jeff, Gramma Mia, Grandpa George, Oma, Aunt Mimi, Uncle Hammy and Aunt Sara.
- 🔊 **A friendlier reading voice:** slower and warmer, and it reads to Violet so she doesn't need to read.

### For grown-ups
- 🔒 **Grown-ups corner** (hold the lock for 3 seconds): voice settings, clear any inbox, a parent inbox view, and "show the help tips again."
- 📊 **Progress reports:** play time per game and day, and every puzzle's skill, speed, wrong tries and hints, with a skills view and struggle spots for each kid. A **weekly summary** arrives in every grown-up's Inbox. Records are kept 90 days, then rolled up weekly, and you can export or clear them.
- 🔑 **4-character family codes:** easy to type on every device.
- 💡 **Help tips:** a how-to card on each screen, shown once to grown-ups and never to kids.
- 📰 **What's new:** after each update, everyone sees what changed (the kids get a picture version read aloud). Tap 📰 on the home screen, or the version number, to see all updates. An iPad left open gets a "Tap to update" button when a new version is ready.
- 📱 **iPad and iPhone fixes:** no accidental page zoom or sideways scrolling, screens that fit without scrolling, a steadier farm, and quick recovery after dropped connections, with a connection light for each player.
- 🎨 **Art kit:** free AI-generated farm, avatar and family art (Cloudflare Workers AI), with family cartoons kept private under the family code.
- 🐍 Snake Race respawn puzzles: kids get the quick puzzle types; grown-ups get blackjack or minesweeper, and go back in after one puzzle, win or lose. Reports now count snake races, snacks, crashes and longest snake.

### ⏱️ How long it took (grown-ups only)
Approximate time Joe spent prompting, from the send times of his messages in each chat. Back-and-forth gaps of up to 15 minutes count as active time; a longer gap counts as a 5-minute wrap-up and then a break. Claude's build time between messages isn't counted on its own.

| Chat | What it built | Messages | Prompt time |
|---|---|---|---|
| Primary Build | Color Together, video, Firebase, Inbox, Bedtime Stories, grown-ups, reports, avatars, iPad fixes | 59 | ~5 h 35 m |
| Farmstand game design | The farm, Moolah, store, orders, basket and bank | 25 | ~2 h 10 m |
| Image Generation | Art kit, farm and avatar art, family cartoons | 20 | ~1 h 35 m |
| Backlog | Planning, backlog items #5–#20, decisions | 32 | ~1 h 35 m |
| Age-appropriate tasks | Kid and grown-up puzzles | 13 | ~1 h 15 m |
| Snake Race | Snake Race | 5 | ~35 m |
| Capture the Flag | Capture the Flag Beta | 4 | ~20 m |
| **Total** | | **158** | **~13 h 10 m** |

Several chats ran at the same time, so the actual time on the clock was about **9 h 15 m**, between 8:28 AM and 9:06 PM.

### Coming soon
Fashion Show, Jeppson the corgi on the farm, storybook film art, and online multiplayer for Capture the Flag.
