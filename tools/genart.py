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


def generate(prompt, model="klein", ref=None, seed=None, style=None):
    tok, acct = creds()
    mid, cost = MODELS[model]
    url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{mid}"
    full = f"{prompt}. {style or STYLE}"
    if model == "schnell":
        body = {"prompt": full, "steps": 4}
        if seed is not None: body["seed"] = seed
        data, ctype = json.dumps(body).encode(), "application/json"
    else:
        fields = {"prompt": full, "width": "1024", "height": "1024"}
        if seed is not None: fields["seed"] = str(seed)
        files = {}
        if ref:
            from PIL import Image
            im = Image.open(ref).convert("RGB")
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
                sys.exit(f"Free daily limit reached (resets 7pm Central). {msg}")
            if attempt == 2: sys.exit(f"Cloudflare error {e.code}: {msg}")
            time.sleep(3)
    if not d.get("success"):
        sys.exit(f"Cloudflare error: {d.get('errors')}")
    log_usage(cost)
    return base64.b64decode(d["result"]["image"])


def log_usage(n):
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try: u = json.loads(LOG.read_text())
    except Exception: u = {}
    if u.get("day") != day: u = {"day": day, "neurons": 0, "images": 0}
    u["neurons"] += n; u["images"] += 1
    LOG.write_text(json.dumps(u))


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
    ap.add_argument("cmd", choices=["one", "batch", "poses", "sheet", "usage"])
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
    elif a.cmd == "poses":
        poses(a.args[0], a.args[1], a)
    elif a.cmd == "sheet":
        sheet(a.args[0] if a.args else "", a.out)
    elif a.cmd == "usage":
        try: u = json.loads(LOG.read_text())
        except Exception: u = {"neurons": 0, "images": 0}
        if u.get("day") != datetime.now(timezone.utc).strftime("%Y-%m-%d"): u = {"neurons": 0, "images": 0}
        left = DAILY - u["neurons"]
        print(f"today: {u['images']} images, ~{u['neurons']} neurons used, ~{left} left "
              f"(~{left//MODELS['klein'][1]} klein / ~{left//MODELS['schnell'][1]} schnell). Resets 7pm Central.")


if __name__ == "__main__":
    main()
