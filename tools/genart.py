#!/usr/bin/env python3
"""Kapanigans art generator: Cloudflare Workers AI (free tier) -> cutout WebP in art/.

Credentials (never committed):
  ~/.config/kapanigans/cf_token, ~/.config/kapanigans/cf_account
  or env CF_TOKEN / CF_ACCOUNT

Usage:
  python3 tools/genart.py one farm/chicken "a plump red hen"
  python3 tools/genart.py batch tools/batches/farm1.json
  python3 tools/genart.py poses farm/hen "a plump red hen with a cream belly"   # stand/eat/sleep/back
  python3 tools/genart.py poses farm/carrot "a carrot plant" --crop           # sprout/growing/ripe
  python3 tools/genart.py isobatch tools/batches/farmA.json     # skips anything already made
  python3 tools/genart.py sheet farm            # contact sheet of art/farm
  python3 tools/genart.py usage                 # rough free-tier budget left today

Options: --model klein|schnell  --ref art/style/ref.webp  --keepbg  --size 512
         --firebase FAMILYCODE   (also store under families/<code>/art in the Realtime DB)
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art"
MANIFEST = ART / "manifest.json"
CFG = Path.home() / ".config" / "kapanigans"
LOG = CFG / "usage.json"
DB_URL = "https://kapanigans-default-rtdb.firebaseio.com"

# One fixed house style so every asset looks like the same game.
STYLE = ("cute chunky 3D cartoon style like a premium kids' game, soft rounded shapes, "
         "smooth clay-like materials, bright friendly saturated colors, gentle soft lighting, "
         "centered, whole subject in frame, "
         "plain solid flat light grey background, no text, no letters, no logo, no border")

# Simplified isometric sprites for things that move around the farm.
ISO = ("simple clean isometric game sprite, viewed from above at a 3/4 isometric angle, "
       "chunky simplified shapes, flat soft shading with few details, bright friendly colors, "
       "whole subject in frame, plain solid flat light grey background, no shadow, no text")
SAME = ", keep the exact same character, colors, proportions and style as the reference image"
ANIMAL_POSES = {
    "stand": "{d}, standing, body facing toward the bottom left",
    "eat":   "Edit the reference image: the animal lowers its head all the way down so its mouth touches the grass, eating, body still facing the bottom left" + SAME,
    "sleep": "Edit the reference image: the animal lies down flat on its belly on the ground with its legs folded and tucked under its body, head resting low, eyes closed, sleeping" + SAME,
    "back":  "Edit the reference image: turn the animal around 180 degrees so it faces away from the viewer toward the top right; show its rear, tail and back, the face is hidden, walking away" + SAME,
}
CROP_STAGES = {
    "ripe":    "{d}, fully grown and ripe, growing in a small mound of brown soil",
    "sprout":  "a tiny green sprout with two small leaves poking out of the same small mound of brown soil" + SAME,
    "growing": "the same plant half grown, young and green, not ripe yet, in the same small mound of brown soil" + SAME,
}

MODELS = {
    "klein":   ("@cf/black-forest-labs/flux-2-klein-4b", 105),   # neurons per 1024px image (approx)
    "schnell": ("@cf/black-forest-labs/flux-1-schnell", 58),
}
DAILY = 10000


def creds():
    tok = os.environ.get("CF_TOKEN") or (CFG / "cf_token").read_text().strip()
    acct = os.environ.get("CF_ACCOUNT") or (CFG / "cf_account").read_text().strip()
    return tok, acct


def multipart(fields, files):
    b = uuid.uuid4().hex
    out = io.BytesIO()
    for k, v in fields.items():
        out.write(f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    for k, (fn, data, ctype) in files.items():
        out.write(f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fn}\"\r\n"
                  f"Content-Type: {ctype}\r\n\r\n".encode())
        out.write(data + b"\r\n")
    out.write(f"--{b}--\r\n".encode())
    return out.getvalue(), f"multipart/form-data; boundary={b}"


def generate(prompt, model="klein", ref=None, seed=None, style=None, size=(1024, 1024)):
    tok, acct = creds()
    mid, cost = MODELS[model]
    url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{mid}"
    full = f"{prompt}. {style or STYLE}"
    if model == "schnell":
        body = {"prompt": full, "steps": 4}
        if seed is not None: body["seed"] = seed
        data, ctype = json.dumps(body).encode(), "application/json"
    else:
        fields = {"prompt": full, "width": str(size[0]), "height": str(size[1])}
        if seed is not None: fields["seed"] = str(seed)
        files = {}
        if ref:
            from PIL import Image
            src = Image.open(ref)
            if src.mode in ("RGBA", "LA", "P"):
                src = src.convert("RGBA"); bgim = Image.new("RGBA", src.size, (220, 221, 223, 255))
                bgim.alpha_composite(src); src = bgim
            im = src.convert("RGB")
            im.thumbnail((1024, 1024))
            buf = io.BytesIO(); im.save(buf, "PNG")
            files["input_image_0"] = ("ref.png", buf.getvalue(), "image/png")
            cost += 22
        data, ctype = multipart(fields, files)
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {tok}", "Content-Type": ctype})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")[:300]
            if e.code == 429 or "neurons" in msg.lower():
                sys.exit(f"Free limit reached: Cloudflare counts a rolling 24 hours (not the calendar day), so it clears about 24h after the earliest recent images. {msg}")
            if attempt == 2: sys.exit(f"Cloudflare error {e.code}: {msg}")
            time.sleep(3)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == 2: sys.exit(f"Cloudflare didn't answer after 3 tries: {e}")
            time.sleep(5)
    if not d.get("success"):
        sys.exit(f"Cloudflare error: {d.get('errors')}")
    log_usage(cost)
    return base64.b64decode(d["result"]["image"])


def log_usage(n):
    """Rolling 24-hour log (Cloudflare's cap behaves like a rolling window)."""
    now = time.time()
    try: u = json.loads(LOG.read_text())
    except Exception: u = {}
    ev = [e for e in u.get("events", []) if now - e[0] < 86400] + [[now, n]]
    LOG.write_text(json.dumps({"events": ev}))


def cutout(raw, keepbg=False, size=512):
    from PIL import Image
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    if not keepbg:
        from rembg import remove, new_session
        global _SESSION
        if "_SESSION" not in globals(): _SESSION = new_session("isnet-general-use")
        im = remove(im, session=_SESSION)
        # Background always touches the edge; refill enclosed "holes" (e.g. a light belly).
        import numpy as np
        from scipy.ndimage import binary_fill_holes
        from scipy.ndimage import label, binary_dilation
        a = np.array(im.getchannel("A"))
        rgb = np.array(Image.open(io.BytesIO(raw)).convert("RGB"))
        # The prompt asks for a flat background: anything edge-connected and close to the
        # border colour is background; everything else is solid (fixes see-through white fur).
        border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
        bgc = np.median(border, axis=0)
        near = np.abs(rgb.astype(int) - bgc).max(axis=2) < 16
        lab, _ = label(near)
        edge_ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(edge_ids))
        fg = binary_fill_holes((a > 128) | (~bg & (a > 8)))
        rim = binary_dilation(fg, iterations=2) & ~fg
        a = np.where(fg, 255, np.where(rim, a, 0)).astype("uint8")
        im = Image.fromarray(np.dstack([rgb, a]), "RGBA")
        bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bbox:
            pad = 8
            im = im.crop((max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad)))
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=82, method=6)
    return buf.getvalue(), im.size


def save(name, prompt, model, webp, dims, keepbg):
    path = ART / f"{name}.webp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(webp)
    try: m = json.loads(MANIFEST.read_text())
    except Exception: m = {}
    m[name] = {"file": f"art/{name}.webp", "w": dims[0], "h": dims[1], "prompt": prompt,
               "model": model, "cutout": not keepbg, "made": datetime.now().strftime("%Y-%m-%d")}
    MANIFEST.write_text(json.dumps(dict(sorted(m.items())), indent=1))
    return path


def to_firebase(code, name, webp):
    key = name.replace("/", "_")
    body = json.dumps({"img": "data:image/webp;base64," + base64.b64encode(webp).decode(), "t": int(time.time()*1000)}).encode()
    req = urllib.request.Request(f"{DB_URL}/families/{code}/art/{key}.json", data=body, method="PUT",
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30).read()


def make_one(name, prompt, a):
    t = time.time()
    raw = generate(prompt, a.model, a.ref, a.seed)
    webp, dims = cutout(raw, a.keepbg, a.size)
    p = save(name, prompt, a.model, webp, dims, a.keepbg)
    if a.firebase: to_firebase(a.firebase, name, webp)
    print(f"✓ {p.relative_to(ROOT)}  {dims[0]}x{dims[1]}  {len(webp)//1024}KB  {time.time()-t:.0f}s")


def isobatch(path, a):
    """Batch of isometric sprites. Items: {"crop": "desc"} -> ripe + growing stages;
    {"prompt": "...", "ref": "art/iso/...webp"} -> one sprite. Skips files that already exist."""
    spec = json.loads(Path(path).read_text())
    done = fails = 0
    for name, it in spec["items"].items():
        if it.get("crop"):
            if all((ART / f"iso/{name}/{st}.webp").exists() for st in ("ripe", "growing")): continue
            a.crop, a.only = True, "ripe,growing"
            poses(name, it["crop"], a); done += 2; continue
        if (ART / f"iso/{name}.webp").exists(): continue
        t = time.time()
        ref = str(ROOT / it["ref"]) if it.get("ref") else None
        prompt = it["prompt"] + (SAME if ref else "")
        raw = generate(prompt, "klein", ref, it.get("seed", a.seed), ISO)
        rd = CFG / "raw" / Path(name).parent; rd.mkdir(parents=True, exist_ok=True)
        (CFG / "raw" / f"{name}.jpg").write_bytes(raw)
        webp, dims = cutout(raw, False, 256)
        save(f"iso/{name}", prompt, "klein", webp, dims, False); done += 1
        print(f"✓ art/iso/{name}.webp  {dims[0]}x{dims[1]}  {len(webp)//1024}KB  {time.time()-t:.0f}s")
    print(f"batch done: {done} made")


AV_STYLE = ISO.replace("plain solid flat light grey background", "plain solid flat medium grey background")
AV_ZONES = {"wings": (-.35, 1.1), "hairtop": (-.3, .8), "crown": (-.3, .32), "dress": (.16, 1.0), "wand": (.15, .9),
            "hair": (0, .74), "head": (0, .56), "torso": (.45, .88), "feet": (.80, 1.0), "face": (.15, .56), "all": (0, 1)}
AV_FRAME = 320


def solid_cut(raw):
    """Full-frame cutout with no see-through patches: background = edge-connected pixels
    close to the flat background colour; everything enclosed is solid."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import label, binary_fill_holes, binary_opening, gaussian_filter
    rgb = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(int)
    bgc = np.median(np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]), axis=0)
    near = np.abs(rgb - bgc).max(axis=2) < 14
    lab, _ = label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = binary_fill_holes(~np.isin(lab, list(edge)))
    # drop the soft ground shadow: neutral grey, darker than the background, in the bottom fifth
    ys = np.where(fg.any(axis=1))[0]
    if len(ys):
        low = np.zeros_like(fg); low[int(ys.max() - (ys.max() - ys.min()) * .35):] = True
        mx, mn = rgb.max(axis=2), rgb.min(axis=2)
        shadow = low & (mx - mn < 20) & (mx < bgc.max() - 3) & (mx > 90)
        fg = binary_fill_holes(fg & ~shadow)   # enclosed grey (fur shading) comes back; open shadow stays gone
    fg = binary_opening(fg, iterations=2)
    lab2, k = label(fg)
    if k:
        sz = np.bincount(lab2.ravel()); sz[0] = 0; fg = (sz > sz.max() * .05)[lab2]
    a = np.clip(gaussian_filter(fg.astype(float), .8) * 255, 0, 255)
    a = np.where(fg, 255, a).astype("uint8")
    return Image.fromarray(np.dstack([rgb, a]).astype("uint8"), "RGBA")


def _fgmask(raw):
    """Figure mask from rembg (ignores painterly background blotches)."""
    import numpy as np
    from PIL import Image
    from rembg import remove, new_session
    global _SESSION
    if "_SESSION" not in globals(): _SESSION = new_session("isnet-general-use")
    return np.array(remove(Image.open(io.BytesIO(raw)).convert("RGB"), session=_SESSION).getchannel("A")) > 100


def _layer(raw, base_raw, zone, white, fgonly=False):
    """Pull one dress-up part out of an edit of the base body by diffing, kept full-frame so layers stack."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import binary_opening, binary_closing, binary_fill_holes, binary_dilation, label, gaussian_filter
    E = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(int)
    B = np.array(Image.open(io.BytesIO(base_raw)).convert("RGB")).astype(int)
    bgc = np.median(np.concatenate([E[0], E[-1], E[:, 0], E[:, -1]]), axis=0)
    notbg = np.abs(E - bgc).max(axis=2) > 16
    dd = np.abs(E - B).sum(axis=2) if fgonly else np.abs(E - B).max(axis=2)
    m = (gaussian_filter(dd.astype(float), 2) > (22 if fgonly else 25)) & notbg
    if fgonly: m &= binary_dilation(_fgmask(raw), iterations=2)
    bnb = np.abs(B - bgc).max(axis=2) > 16
    ys = np.where(bnb.any(axis=1))[0]; top, bot = ys.min(), ys.max(); z0, z1 = AV_ZONES[zone]
    zm = np.zeros_like(m); zm[max(0, int(top + (bot - top) * z0)):max(0, int(top + (bot - top) * z1) + 1)] = True; m &= zm
    if white:  # tintable parts: only near-white pixels (+ their outline), never skin or shirt
        mx, mn = E.max(axis=2), E.min(axis=2)
        wh = ((mn > 110) & (mx - mn < 26)) if fgonly else ((mn > 165) & (mx - mn < 40))
        m &= binary_dilation(wh & m, iterations=3)
    m = binary_opening(m, iterations=3 if fgonly else 5); m = binary_closing(m, iterations=8 if fgonly else 3); m = binary_fill_holes(m)
    if fgonly: m &= binary_dilation(_fgmask(raw), iterations=1)
    if fgonly and zone == "hairtop":  # inside the face only keep strong changes (bangs), never the eyes or mouth
        from scipy.ndimage import binary_erosion
        skin = (B[..., 0] - B[..., 2] > 15) & bnb
        hz = np.zeros_like(skin); hz[top:int(top + (bot - top) * .26)] = True
        face = binary_erosion(binary_fill_holes(skin & hz), iterations=6)
        above = np.zeros_like(m); above[:int(top + (bot - top) * .095)] = True
        bangs = wh & (B[..., 0] - B[..., 2] > 15) & above & (dd > 30)
        m &= ~face | binary_closing(binary_opening(bangs, iterations=2), iterations=3)
        R = binary_fill_holes(bnb); R[:int(top + (bot - top) * .21)] = False   # over the body below the chin
        m = (m & ~R) | binary_opening(m & R, iterations=6)
    lab, k = label(m)
    if k:
        sz = np.bincount(lab.ravel()); sz[0] = 0; m = (sz > sz.max() * .08)[lab]
    im = Image.fromarray(np.dstack([E, m * 255]).astype("uint8"), "RGBA")
    return im


KEY_COLOR = "solid bright vivid turquoise blue"


def _keyed(raw, base_raw, zone):
    """Tint layer by colour key: the part was painted turquoise, so pick it out by hue (nothing else in
    the picture is turquoise), then turn it into white with the same watercolour shading."""
    import numpy as np, colorsys
    from PIL import Image
    from scipy.ndimage import binary_opening, binary_closing, binary_fill_holes, binary_dilation, label
    E = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(float) / 255
    B = np.array(Image.open(io.BytesIO(base_raw)).convert("RGB")).astype(int)
    mx, mn = E.max(axis=2), E.min(axis=2); sat = (mx - mn) / np.maximum(mx, 1e-3)
    r, g, b = E[..., 0], E[..., 1], E[..., 2]
    blue = (b >= r + .04) & (g >= r) & (sat > .12) & (mx > .2)
    bgc = np.median(np.concatenate([B[0], B[-1], B[:, 0], B[:, -1]]), axis=0)
    bnb = np.abs(B - bgc).max(axis=2) > 16
    ys = np.where(bnb.any(axis=1))[0]; top, bot = ys.min(), ys.max(); z0, z1 = AV_ZONES[zone]
    zm = np.zeros_like(blue); zm[max(0, int(top + (bot - top) * z0)):max(0, int(top + (bot - top) * z1) + 1)] = True
    if zone == "hairtop":  # never the face below the bangs (pale grey-blue eyes would pass the key)
        from scipy.ndimage import binary_erosion
        skin = (B[..., 0] - B[..., 2] > 15) & bnb
        hz = np.zeros_like(skin); hz[top:int(top + (bot - top) * .26)] = True
        face = binary_erosion(binary_fill_holes(skin & hz), iterations=4)
        face[:int(top + (bot - top) * .105)] = False
        blue &= ~face
    m = binary_opening(blue & zm, iterations=2)
    lab, k = label(m)
    if k: sz = np.bincount(lab.ravel()); sz[0] = 0; m = (sz > sz.max() * .03)[lab]
    m = binary_fill_holes(binary_closing(m, iterations=3))
    ring = binary_dilation(m, iterations=3) & ~m & (mx < .5)          # dark pencil outline around the part
    m = m | ring
    v = mx / max(np.percentile(mx[m], 97), 1e-3) if m.any() else mx
    grey = (np.clip(v, 0, 1) * 255).astype("uint8")
    return Image.fromarray(np.dstack([grey, grey, grey, (m * 255).astype("uint8")]), "RGBA")


def _keep(raw, base_raw, zone):
    """Coloured accessory (tiara, flowers, wand): new, saturated or strongly changed pixels only, so a
    slightly re-shaded face or body never comes along."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import binary_opening, binary_closing, binary_fill_holes, binary_dilation, label, gaussian_filter
    E = np.array(Image.open(io.BytesIO(raw)).convert("RGB")).astype(int)
    B = np.array(Image.open(io.BytesIO(base_raw)).convert("RGB")).astype(int)
    dd = gaussian_filter(np.abs(E - B).sum(axis=2).astype(float), 1.5)
    mx, mn = E.max(axis=2), E.min(axis=2); sat = (mx - mn) / np.maximum(mx, 1)
    skinlike = (E[..., 0] >= E[..., 1]) & (E[..., 1] >= E[..., 2] - 5) & (sat < .42)
    bgc = np.median(np.concatenate([B[0], B[-1], B[:, 0], B[:, -1]]), axis=0)
    bnb = np.abs(B - bgc).max(axis=2) > 16
    ys = np.where(bnb.any(axis=1))[0]; top, bot = ys.min(), ys.max(); z0, z1 = AV_ZONES[zone]
    zm = np.zeros_like(bnb); zm[max(0, int(top + (bot - top) * z0)):max(0, int(top + (bot - top) * z1) + 1)] = True
    m = (dd > 90) & zm & ~skinlike & binary_dilation(_fgmask(raw), iterations=2)
    m = binary_opening(m, iterations=2)
    lab, k = label(m)
    if k: sz = np.bincount(lab.ravel()); sz[0] = 0; m = (sz > max(sz.max() * .04, 60))[lab]
    m = binary_fill_holes(binary_closing(m, iterations=3))
    m = m | (binary_dilation(m, iterations=2) & (mx < 120))
    return Image.fromarray(np.dstack([E, m * 255]).astype("uint8"), "RGBA")


def _frame(im, size=None, fit=None):
    from PIL import Image
    if fit:  # fit = (scale, dx, dy): same affine for every layer so they stay aligned
        s, dx, dy = fit
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sm = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        out.paste(sm, (round(dx), round(dy)), sm)
        im = out
    else:
        im = im.resize((size or AV_FRAME, size or AV_FRAME), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=85, method=6); return buf.getvalue()


def avatar(path, a):
    """Avatar parts batch. {"base": prompt, "items": {"hair/pigtails": {"prompt":..., "zone":"head", "white":true}}}
    Every layer is saved full-frame (same size, same position) in art/avatar/ so the game just stacks them."""
    from PIL import Image
    import numpy as np
    spec = json.loads(Path(path).read_text())
    D = spec.get("dir", "avatar"); style = {"fairy": FAIRY_STYLE}.get(spec.get("style"), AV_STYLE)
    F = spec.get("frame", AV_FRAME); only = set(a.only.split(",")) if getattr(a, "only", None) else None
    rd = CFG / "raw" / D; rd.mkdir(parents=True, exist_ok=True)
    bp = rd / "base.jpg"
    if not bp.exists():
        ref = str(ROOT / spec["base_ref"]) if spec.get("base_ref") else None
        bp.write_bytes(generate(spec["base"], "klein", ref, spec.get("seed", 31), style))
    base_raw = bp.read_bytes()
    cut = solid_cut(base_raw)
    fit = None
    if spec.get("anchor"):  # place the body so head top / feet / centre land on the game's anchor points
        an = spec["anchor"]; al = np.array(cut.getchannel("A")) > 128
        ys = np.where(al.any(axis=1))[0]; top, bot = ys.min(), ys.max()
        xs = np.where(al[int(top + (bot - top) * .3):int(top + (bot - top) * .6)].any(axis=0))[0]
        s_ = (an["bottom"] - an["top"]) / (bot - top); cx = (xs.min() + xs.max()) / 2
        fit = (s_, an["cx"] - cx * s_, an["top"] - top * s_)
    if not (ART / f"{D}/base.webp").exists():
        save(f"{D}/base", spec["base"], "klein", _frame(cut, F, fit), (F, F), False)
        print(f"✓ art/{D}/base.webp")
    made = 0
    for name, it in spec["items"].items():
        if only and name not in only: continue
        outs = [name] + ([it["back"]] if it.get("back") else [])
        if all((ART / f"{D}/{o}.webp").exists() for o in outs): continue
        t = time.time()
        rp = (rd / name.replace("/", "_")).with_suffix(".jpg")
        if rp.exists(): raw = rp.read_bytes()
        else:
            pr = it["prompt"]
            if it.get("white") and spec.get("key"):
                pr = pr.replace("pure white and very pale silver", KEY_COLOR).replace("soft grey", "darker blue")
            raw = generate("Edit the reference image: " + pr + ". Change nothing else" + spec.get("keep", "") + SAME,
                           "klein", str(bp), it.get("seed", spec.get("seed", 31)), style)
            rp.write_bytes(raw)
        if it.get("white") and spec.get("key"): lay = _keyed(raw, base_raw, it.get("zone", "head"))
        elif spec.get("key"): lay = _keep(raw, base_raw, it.get("zone", "head"))
        else: lay = _layer(raw, base_raw, it.get("zone", "head"), it.get("white", False), spec.get("fgonly", False))
        if it.get("back"):  # split hair: hanging part outside the body below the chin goes to the back layer
            al = np.array(lay.getchannel("A")); body = np.array(cut.getchannel("A")) > 128
            ys = np.where(body.any(axis=1))[0]; chin = int(ys.min() + (ys.max() - ys.min()) * .2)
            back = (~body) & (al > 0); back[:chin] = False
            front = al.copy(); front[back] = 0
            back[chin - 10:chin] = ((~body) & (al > 0))[chin - 10:chin]   # small overlap so no seam shows at the chin line
            bk = np.where(back, al, 0).astype("uint8")
            rgb = np.array(lay)[..., :3]
            save(f"{D}/{it['back']}", it["prompt"], "klein",
                 _frame(Image.fromarray(np.dstack([rgb, bk]), "RGBA"), F, fit), (F, F), False)
            lay = Image.fromarray(np.dstack([rgb, front]), "RGBA")
        save(f"{D}/{name}", it["prompt"], "klein", _frame(lay, F, fit), (F, F), False)
        made += 1
        print(f"✓ art/{D}/{name}.webp  {time.time()-t:.0f}s")
    print(f"{D} batch done: {made} made")


STORY_STYLE = ("feature-film quality 3D animated movie look, rich cinematic soft warm lighting, subtle rim light, gentle atmosphere, "
               "detailed fur, fabric and textures, expressive appealing faces with big warm eyes, gentle stylized proportions, "
               "cozy bedtime storybook warmth, friendly and never scary, original design, no text, no logo")


FAIRY_STYLE = ("vintage botanical watercolor storybook illustration, soft transparent watercolor washes, fine thin sepia pencil outlines, "
               "delicate realistic children's-book painting, warm golden soft light, muted petal colors (dusty rose, lavender, sage green, "
               "buttercup yellow, cream), gentle and sweet, original character design, no text, no letters, no logo")


def storybatch(path, a):
    """Storybook art (#14). Items: {"prompt", "kind": "bg"|"char"|"page", "versions": n}.
    bg/page: 1536x1024 full scenes; char: 1024 cutouts on a plain background. Saved to art/story/<dir>/<name>_v<n>.webp."""
    spec = json.loads(Path(path).read_text()); out = spec.get("dir", "test"); made = 0
    for name, it in spec["items"].items():
        kind = it.get("kind", "char")
        for v in range(1, it.get("versions", 2) + 1):
            dest = f"story/{out}/{name}_v{v}"
            if (ART / f"{dest}.webp").exists(): continue
            t = time.time()
            if kind == "char":
                prompt = it["prompt"] + ", full body, centered, whole character in frame, plain soft warm cream studio background"
                raw = generate(prompt, "klein", None, 100 + v * 7, STORY_STYLE)
                webp, dims = cutout(raw, False, 768)
            else:
                prompt = it["prompt"] + (", wide storybook background scene with open space in the lower middle for characters to stand" if kind == "bg" else ", wide storybook page")
                raw = generate(prompt, "klein", None, 100 + v * 7, STORY_STYLE, (1536, 1024))
                from PIL import Image
                im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((1536, 1024))
                buf = io.BytesIO(); im.save(buf, "WEBP", quality=80, method=6); webp, dims = buf.getvalue(), im.size
            rd = CFG / "raw" / "story" / out; rd.mkdir(parents=True, exist_ok=True); (rd / f"{name}_v{v}.jpg").write_bytes(raw)
            save(dest, prompt, "klein", webp, dims, kind != "char"); made += 1
            print(f"✓ art/{dest}.webp  {dims[0]}x{dims[1]}  {len(webp)//1024}KB  {time.time()-t:.0f}s", flush=True)
    print(f"story batch done: {made} made")


def poses(name, desc, a):
    """art/iso/<name>/<pose>.webp: base pose first, the rest drawn from it as a reference."""
    kind = "crop" if a.crop else "animal"
    table = CROP_STAGES if a.crop else ANIMAL_POSES
    rawdir = CFG / "raw" / name; rawdir.mkdir(parents=True, exist_ok=True)
    base = next(iter(table))
    only = set(a.only.split(",")) if a.only else set(table)
    for pose, tmpl in table.items():
        if pose not in only: continue
        t = time.time()
        prompt = tmpl.format(d=desc)
        ref = None if pose == base else str(rawdir / f"{base}.jpg")
        if ref and not Path(ref).exists(): sys.exit(f"make the {base} pose first")
        raw = generate(prompt, "klein", ref, a.seed, ISO)
        (rawdir / f"{pose}.jpg").write_bytes(raw)
        webp, dims = cutout(raw, False, 256)
        save(f"iso/{name}/{pose}", prompt, "klein", webp, dims, False)
        print(f"✓ art/iso/{name}/{pose}.webp  {dims[0]}x{dims[1]}  {len(webp)//1024}KB  {time.time()-t:.0f}s")


def sheet(folder, out=None):
    from PIL import Image, ImageDraw
    files = sorted((ART / folder).rglob("*.webp")) if folder else sorted(ART.rglob("*.webp"))
    if not files: sys.exit("no images")
    cell, cols = 220, 5
    rows = (len(files) + cols - 1) // cols
    sh = Image.new("RGB", (cols*cell, rows*(cell+24)), (238, 242, 247))
    d = ImageDraw.Draw(sh)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGBA"); im.thumbnail((cell-16, cell-16))
        x, y = (i % cols)*cell, (i // cols)*(cell+24)
        sh.paste(im, (x+(cell-im.width)//2, y+(cell-im.height)//2), im)
        d.text((x+6, y+cell+4), f.stem[:30], fill=(40, 40, 40))
    out = out or str(CFG / f"sheet_{(folder or 'all').replace('/', '_')}.png")
    sh.save(out); print(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["one", "batch", "isobatch", "avatar", "storybatch", "poses", "sheet", "usage"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--model", default="klein", choices=MODELS)
    ap.add_argument("--ref"); ap.add_argument("--seed", type=int)
    ap.add_argument("--keepbg", action="store_true"); ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--firebase", metavar="FAMILYCODE")
    ap.add_argument("--out")
    ap.add_argument("--crop", action="store_true", help="poses: growth stages instead of animal poses")
    ap.add_argument("--only", help="poses: comma list, e.g. back,sleep")
    a = ap.parse_args()
    if a.cmd == "one":
        make_one(a.args[0], a.args[1], a)
    elif a.cmd == "batch":
        spec = json.loads(Path(a.args[0]).read_text())
        for k in ("model", "ref", "size"):
            if k in spec.get("options", {}): setattr(a, k, spec["options"][k])
        a.keepbg = a.keepbg or spec.get("options", {}).get("keepbg", False)
        for name, prompt in spec["items"].items():
            make_one(name, prompt, a)
    elif a.cmd == "storybatch":
        storybatch(a.args[0], a)
    elif a.cmd == "avatar":
        avatar(a.args[0], a)
    elif a.cmd == "isobatch":
        isobatch(a.args[0], a)
    elif a.cmd == "poses":
        poses(a.args[0], a.args[1], a)
    elif a.cmd == "sheet":
        sheet(a.args[0] if a.args else "", a.out)
    elif a.cmd == "usage":
        try: ev = json.loads(LOG.read_text()).get("events", [])
        except Exception: ev = []
        now = time.time(); ev = [e for e in ev if now - e[0] < 86400]
        used = sum(e[1] for e in ev); left = DAILY - used
        msg = f"last 24h: {len(ev)} images, ~{int(used)} neurons, ~{int(left)} left (~{max(0,int(left))//MODELS['klein'][1]} klein)."
        if ev and left < 1000:
            free_at = datetime.fromtimestamp(min(e[0] for e in ev) + 86400).strftime("%a %H:%M")
            msg += f" Oldest image rolls off {free_at} (this machine's clock)."
        print(msg + " Only counts this workspace; the Cloudflare dashboard is the real number.")


if __name__ == "__main__":
    main()
