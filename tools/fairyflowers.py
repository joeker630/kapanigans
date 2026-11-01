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
    C = (512, 800)
    place("flower_stem", "one thin gently curving green flower stem growing straight up with two small veined green leaves near the bottom, no flower, no bud, botanical painting",
          C, (200, 540), ("bottom", 256, 800), size=(768, 1280))
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
        place(f"bud_{k}", f"{buds[k]}, {WH.replace('petals', 'petal tips')}, no stem", C, (110, 150), ("center", 256, 280))
        place(f"bloom_{k}", f"{blooms[k]}, {WH}, no stem, no leaves", C, (230, 230), ("center", 256, 280))
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


if __name__ == "__main__":
    {"b": batch_b, "d": batch_d}[sys.argv[1]]()
