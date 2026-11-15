import numpy as np
from PIL import Image
import os, sys
OUT = '../../assets'
def load(n): return np.asarray(Image.open(f'raw/{n:02d}.png').convert('RGB')).astype(np.float32)

def unmul_white(a):
    dark = 1 - a.min(axis=2) / 255.0
    al = np.clip((dark - 0.05) / 0.45, 0, 1) ** 0.8
    c = np.minimum(a, 70) * 0.9
    return np.dstack([c, al * 255])

def unmul_black(a):
    al = a.max(axis=2) / 255.0
    al = np.clip((al - 0.05) / 0.95, 0, 1)
    safe = np.maximum(al, 1e-3)[..., None]
    c = np.clip(a / safe, 0, 255)
    return np.dstack([c, al * 255])

def key_magenta(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = np.minimum(R, B) - G
    corner = np.concatenate([m[:20, :20].ravel(), m[-20:, -20:].ravel()])
    mbg = np.median(corner)
    lo, hi = 45.0, mbg - 35
    al = np.clip((hi - m) / (hi - lo), 0, 1)
    c = a.copy()
    edge = al < 0.999
    # despill: pull red/blue down toward green on edge pixels
    lim = G + 45
    c[..., 0] = np.where(edge, np.minimum(R, np.maximum(lim, G + (R - G) * al)), R)
    c[..., 2] = np.where(edge, np.minimum(B, lim), B)
    return np.dstack([c, al * 255])

def trim(rgba, pad=8):
    al = rgba[..., 3] > 8
    ys, xs = np.where(al)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, rgba.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]

def spans(profile, min_gap=20):
    on = profile > 0
    out, start, gap = [], None, 0
    for i, v in enumerate(on):
        if v:
            if start is None: start = i
            gap = 0; end = i
        elif start is not None:
            gap += 1
            if gap >= min_gap: out.append((start, end + 1)); start = None
    if start is not None: out.append((start, end + 1))
    return out

def split(rgba, axis):
    al = (rgba[..., 3] > 20).astype(np.int32)
    prof = al.sum(axis=0 if axis == 'x' else 1)
    prof = np.where(prof > 3, prof, 0)
    parts = []
    for s, e in spans(prof, 25):
        if e - s < 30: continue
        parts.append(rgba[:, s:e] if axis == 'x' else rgba[s:e, :])
    return parts

def save(rgba, name, maxside):
    rgba = trim(rgba)
    im = Image.fromarray(rgba.astype(np.uint8), 'RGBA')
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(f'{OUT}/{name}.webp', quality=92, method=6)
    im.save(f'{OUT}/{name}.png', optimize=True)
    print(name, im.size)

save(unmul_white(load(1)), 'ink-disc', 1280)
save(unmul_black(load(2)), 'brush-ring', 1280)
save(key_magenta(load(3)), 'seal-knob', 256)
for p, n in zip(split(key_magenta(load(4)), 'x'), ['slot-normal', 'slot-hover', 'slot-selected']): save(p, n, 256)
for p, n in zip(split(key_magenta(load(5)), 'x'), ['hub-ink', 'hub-paper']): save(p, n, 640)
save(key_magenta(load(6)), 'card-front', 900)
save(key_magenta(load(7)), 'card-back', 900)
for p, n in zip(split(key_magenta(load(8)), 'x'), ['stamp-seen', 'stamp-playing']): save(p, n, 360)
save(unmul_white(load(9)), 'ink-pool', 1600)
for p, n in zip(split(key_magenta(load(10)), 'y'), ['pill-paper', 'pill-ink']): save(p, n, 1200)
dec = unmul_white(load(11))
rows = split(dec, 'y')
names = [['decal-crack', 'decal-flick'], ['decal-spatter', 'decal-blot']]
for r, row in enumerate(rows[:2]):
    for c, p in enumerate(split(row, 'x')[:2]): save(p, names[r][c], 400)
