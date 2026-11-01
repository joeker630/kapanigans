"""Fairy Garden Batch B/D: standalone painted objects placed on fixed canvases (see fairygardenartspec.md)."""
import sys, io, json
sys.path.insert(0, "tools"); import genart
import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_dilation

R = genart.CFG / "raw" / "fairy"; R.mkdir(parents=True, exist_ok=True)
G = "isolated single object, centered, plain solid flat medium grey background, no shadow, no ground"
WH = "pure white and very pale cream petals with soft grey watercolor shading and fine sepia outlines"


def keycut(raw, warm_halo=False):
    E = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(int)
    bgc = np.median(np.concatenate([E[0], E[-1], E[:, 0], E[:, -1]]), axis=0)
    d = np.abs(E - bgc).max(axis=2); a = np.clip((d - 12) / 22, 0, 1)
    lab, k = label(a > .5)
    if k:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        a = a * binary_dilation((sz > max(sz.max() * .01, 40))[lab], iterations=3)
    if warm_halo:
        h = (a < .85) & (a > 0); E[h] = (E[h] * .3 + np.array([255, 236, 170]) * .7).astype(int); a = np.where(h, a * .7, a)
    im = Image.fromarray(np.dstack([E, a * 255]).astype("uint8"), "RGBA")
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())


def place(name, prompt, canvas, box, anchor, seed=41, halo=False, size=(1024, 1024)):
    """box = (max_w, max_h); anchor = ("center"|"bottom", x, y)."""
    if (genart.ART / f"fairy/{name}.webp").exists(): return
    rp = R / f"{name}.jpg"
    if not rp.exists(): rp.write_bytes(genart.generate(prompt + ", " + G, "klein", None, seed, genart.FAIRY_STYLE, size))
    im = keycut(rp.read_bytes(), halo)
    s = min(box[0] / im.width, box[1] / im.height); im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    mode, x, y = anchor
    pos = (x - im.width // 2, y - im.height // 2) if mode == "center" else (x - im.width // 2, y - im.height)
    out.alpha_composite(im, pos)
    buf = io.BytesIO(); out.save(buf, "WEBP", quality=85, method=6)
    genart.save(f"fairy/{name}", prompt, "klein", buf.getvalue(), canvas, False)
    print("✓", name)


def batch_b():
    C = (640, 1024)   # release 2: bigger canvas; stem base (320, 1024), head centre (320, 360)
    place("flower_stem", "one thin gently curving green flower stem growing straight up with two small veined green leaves near the bottom, no flower, no bud, botanical painting",
          C, (250, 675), ("bottom", 320, 1024), size=(768, 1280))
    kinds = {"rose": "a wild rose", "bell": "a bindweed trumpet flower", "carnation": "a frilly carnation",
             "daisy": "a daisy", "poppy": "a poppy"}
    buds = {"rose": "a closed wild rose bud with green sepals", "bell": "a closed twisted bindweed bud with green sepals",
            "carnation": "a closed carnation bud with frilly petal tips peeking out of a green calyx",
            "daisy": "a closed daisy bud with green sepals", "poppy": "a closed nodding poppy bud with hairy green sepals"}
    blooms = {"rose": "a fully open wild rose with five rounded petals and golden stamens, seen from the front",
              "bell": "an open bindweed trumpet flower seen from the front, a wide funnel with soft pleats",
              "carnation": "a fully open frilly carnation with ruffled serrated petals, seen from the front",
              "daisy": "a fully open daisy with many slim petals and a golden yellow center, seen from the front",
              "poppy": "a fully open poppy with four crinkled petals and a dark center, seen from the front"}
    for k in kinds:
        place(f"bud_{k}", f"{buds[k]}, {WH.replace('petals', 'petal tips')}, no stem", C, (138, 188), ("center", 320, 360))
        place(f"bloom_{k}", f"{blooms[k]}, {WH}, no stem, no leaves", C, (288, 288), ("center", 320, 360))
    place("rainbow_bud", f"one large plump closed magical flower bud with green sepals, petals {WH}, glowing softly, no stem",
          (512, 512), (300, 400), ("center", 256, 256))
    place("rainbow_petal", f"one single large rounded flower petal pointing straight up, {WH}, fine veins, no stem",
          (256, 256), (150, 240), ("bottom", 128, 256))
    place("rainbow_center", "a round golden glowing flower center with soft stamens and a warm golden glow, seen from the front",
          (256, 256), (200, 200), ("center", 128, 128), halo=True)


def batch_d():
    for i, p in enumerate(["a single small four-point golden star glint with soft glow", "a tiny round soft white and golden sparkle of light",
                           "a small six-point white starburst glint", "a cluster of three tiny golden sparkles"], 1):
        place(f"fx_sparkle{i}", p, (64, 64), (60, 60), ("center", 32, 32), seed=40 + i, halo=True)
    for c, col in (("", "pale lilac and cream"), ("2", "pale buttercup yellow and peach")):
        place(f"fx_butterfly_open{c}", f"a small delicate {col} butterfly with wings spread wide open, seen from above", (128, 128), (120, 120), ("center", 64, 64), seed=51)
        place(f"fx_butterfly_closed{c}", f"a small delicate {col} butterfly with wings folded up together, seen from the side", (128, 128), (120, 120), ("center", 64, 64), seed=51)
    place("fx_heart", "a small soft painted golden heart with a gentle glow", (128, 128), (110, 110), ("center", 64, 64), halo=True)
    for i in (1, 2, 3):
        place(f"fx_cloud{i}", "a soft fluffy white and pale pink watercolor cloud", (512, 256), (500, 240), ("center", 256, 128), seed=60 + i, size=(1024, 512))


def background(name, prompt, gen, out, seed=70):
    """Full painted background, no cutout."""
    if (genart.ART / f"fairy/{name}.webp").exists(): return
    rp = R / f"{name}.jpg"
    if not rp.exists(): rp.write_bytes(genart.generate(prompt, "klein", None, seed, genart.FAIRY_STYLE, gen))
    im = Image.open(io.BytesIO(rp.read_bytes())).convert("RGB").resize(out, Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=80, method=6)
    genart.save(f"fairy/{name}", prompt, "klein", buf.getvalue(), out, True)
    print("✓", name)


SCENE = ("a dreamy fairy meadow garden scene, warm golden-pink sky glowing from the upper right, misty soft meadow, faint lilac and foxglove "
         "silhouettes in the distance, faded pressed-leaf shapes in the corners, soft green grass with tiny wildflowers, paper grain, "
         "no people, no fairies, no animals, no big flowers in the middle, no text")


def batch_c():
    background("garden_wide", SCENE + ", wide landscape view, horizon at a little above the middle, the middle of the lower half is open empty grass, "
               "any bushes or details only near the far left and right edges", (1536, 864), (2048, 1152))
    background("garden_tall", SCENE + ", tall portrait view, horizon at about 40 percent from the top, the whole middle and lower area is open empty grass, "
               "any bushes or details only near the left and right edges", (864, 1536), (1152, 2048))
    place("prop_stump", "an old mossy tree stump with a tiny arched round-topped wooden fairy door with a little brass knob and a small glowing lantern hanging beside it, original design",
          (512, 512), (480, 480), ("bottom", 256, 500), seed=71)
    place("prop_toadstool", "one speckled brown-capped toadstool mushroom with a cream stem", (256, 256), (230, 240), ("bottom", 128, 252), seed=72)
    place("prop_toadstool2", "two small speckled tan and russet toadstool mushrooms growing together, one taller", (256, 256), (230, 240), ("bottom", 128, 252), seed=73)
    place("prop_pond", "a small shallow oval pond seen from a low angle, still blue-green water with soft reflections, one round lily pad with a tiny pink water lily, a few reeds at one end",
          (512, 200), (500, 196), ("center", 256, 100), seed=74, size=(1024, 512))


def batch_r2():
    """Release 2 (game 1.24): Rainbow Flower in 4 stages on one shared stem, finale arc, redos, optional UI bits."""
    C = (768, 1200)
    stem_p = "one tall strong gently curving green flower stem growing straight up with three long veined green leaves along it, no flower, no bud, botanical painting"
    rp = R / "rainbow_stem.jpg"
    if not rp.exists(): rp.write_bytes(genart.generate(stem_p + ", " + G, "klein", None, 80, genart.FAIRY_STYLE, (768, 1280)))
    heads = {
        0: ("one tall plump closed flower bud wrapped in green sepals, petals barely showing soft pastel rainbow tints at the tip, a soft golden glow around it, lovely and magical, no stem", None),
        1: ("the same bud just beginning to open: two soft pastel petals (rose pink and apricot) unfurling at the front, the rest still closed, soft golden glow, no stem", 0),
        2: ("the same flower half open: four soft pastel petals (rose, apricot, buttercup yellow, sage green) opened, two still closed, a golden center peeking out, soft golden glow, no stem", 0),
        3: ("a fully open magical flower seen from the front with six large rounded pastel rainbow petals in order rose pink, apricot, buttercup yellow, sage green, sky blue, lavender around a glowing golden center, no stem", None),
    }
    for i, (p, ref) in heads.items():
        hp = R / f"rainbow_head{i}.jpg"
        if not hp.exists():
            if ref is None: hp.write_bytes(genart.generate(p + ", " + G, "klein", None, 81, genart.FAIRY_STYLE))
            else: hp.write_bytes(genart.generate("Edit the reference image: " + p + ", keep the same plain flat grey background" + genart.SAME, "klein", str(R / f"rainbow_head{ref}.jpg"), 81, genart.FAIRY_STYLE))
    for i in range(4):
        name = f"rainbow_stage{i}"
        if (genart.ART / f"fairy/{name}.webp").exists(): continue
        stem = keycut(rp.read_bytes()); s = min(330 / stem.width, 820 / stem.height)
        stem = stem.resize((round(stem.width * s), round(stem.height * s)), Image.LANCZOS)
        head = keycut((R / f"rainbow_head{i}.jpg").read_bytes(), warm_halo=True); s = min(400 / head.width, 440 / head.height)
        head = head.resize((round(head.width * s), round(head.height * s)), Image.LANCZOS)
        out = Image.new("RGBA", C, (0, 0, 0, 0))
        out.alpha_composite(stem, (384 - stem.width // 2, 1200 - stem.height))
        out.alpha_composite(head, (384 - head.width // 2, 400 - head.height // 2))
        buf = io.BytesIO(); out.save(buf, "WEBP", quality=85, method=6)
        genart.save(f"fairy/{name}", heads[i][0], "klein", buf.getvalue(), C, False); print("✓", name)
    place("rainbow_arc", "one huge soft watercolor rainbow arc, a wide gentle half circle with soft pastel bands, misty white cloud puffs at both feet of the rainbow",
          (2048, 1024), (2040, 1020), ("bottom", 1024, 1024), seed=82, size=(1536, 768))
    place("fx_sparkle4", "a tiny soft golden sparkle star of light, no flower", (64, 64), (60, 60), ("center", 32, 32), seed=90, halo=True)
    place("fx_cloud3", "a soft fluffy white and pale pink watercolor cloud, nothing else", (512, 256), (500, 240), ("center", 256, 128), seed=91, size=(1024, 512))
    place("fx_heart", "a simple soft painted golden heart with a gentle glow, nothing else, no petals", (128, 128), (110, 110), ("center", 64, 64), seed=92, halo=True)
    place("fx_petalglow", "a soft round golden burst of warm glowing light with gentle rays and tiny sparkles", (256, 256), (250, 250), ("center", 128, 128), seed=93, halo=True)
    place("ui_goal", "a long horizontal parchment ribbon banner with a thin gold edge and gently folded ends, plain empty middle, no text",
          (512, 128), (508, 124), ("center", 256, 64), seed=94, size=(1024, 256))


def batch_e():
    place("icon_game", "a little fairy girl with gauzy wings flying over a pink wildflower, round storybook vignette", (256, 256), (250, 250), ("center", 128, 128), seed=100)
    tabs = {"wings": "a pair of gauzy fairy wings", "hair": "a soft curl of hair tied with a little ribbon", "eyes": "a gentle painted eye with long lashes",
            "skin": "a small round watercolor paint palette with skin-tone paints", "top": "a little petal dress on a hanger", "bottom": "a small flared petal skirt",
            "shoes": "a pair of tiny ballet slippers", "extra": "a golden fairy wand with a star", "name": "a small blank parchment name tag on a ribbon"}
    for k, p in tabs.items():
        place(f"tab_{k}", p + ", simple icon", (128, 128), (120, 120), ("center", 64, 64), seed=101)
    background("paper", "plain warm cream watercolor paper texture, subtle even grain, seamless tileable pattern, nothing drawn on it", (1024, 1024), (1024, 1024), seed=110)


if __name__ == "__main__":
    {"b": batch_b, "c": batch_c, "d": batch_d, "r2": batch_r2, "e": batch_e}[sys.argv[1]]()
