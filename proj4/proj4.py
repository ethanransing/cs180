import time
from pathlib import Path

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import tyro

MAX_DIM = 1500
SIGMA = 10


def load_rgb(path):
    im = cv.imread(str(path))
    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    return im.astype(np.float64) / 255


def save_rgb(path, im):
    path.parent.mkdir(parents=True, exist_ok=True)
    im = np.clip(im[:, :, :3], 0, 1)
    im = (im * 255).astype(np.uint8)
    im = cv.cvtColor(im, cv.COLOR_RGB2BGR)
    cv.imwrite(str(path), im)


def pick_points(im1, im2, n):
    h1, w1 = im1.shape[:2]
    h2, w2 = im2.shape[:2]
    canvas = np.zeros((max(h1, h2), w1 + w2, 3))
    canvas[:h1, :w1] = im1
    canvas[:h2, w1:] = im2

    plt.figure(figsize=(20, 11))
    plt.imshow(canvas)
    plt.axvline(w1, color="white")
    plt.axis("off")
    plt.title("left then right")
    clicks = np.array(plt.ginput(2 * n, timeout=0))
    plt.close()

    pts1 = clicks[0::2]
    pts2 = clicks[1::2]
    pts2[:, 0] -= w1
    return pts1, pts2


def build_system(im1_pts, im2_pts):
    A = []
    b = []
    for (x, y), (xp, yp) in zip(im1_pts, im2_pts):
        A.append([x, y, 1, 0, 0, 0, -x * xp, -y * xp])
        A.append([0, 0, 0, x, y, 1, -x * yp, -y * yp])
        b.append(xp)
        b.append(yp)
    return np.array(A), np.array(b)


def computeH(im1_pts, im2_pts):
    A, b = build_system(im1_pts, im2_pts)
    h, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    h = np.append(h, 1)
    return h.reshape(3, 3)


def apply_H(H, pts):
    ones = np.ones((len(pts), 1))
    pts = np.hstack([pts, ones])
    mapped = pts @ H.T
    return mapped[:, :2] / mapped[:, 2:3]


def warp_bbox(shape, H):
    h, w = shape[:2]
    corners = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
    warped = apply_H(H, corners)
    xmin = int(np.floor(warped[:, 0].min()))
    ymin = int(np.floor(warped[:, 1].min()))
    xmax = int(np.ceil(warped[:, 0].max()))
    ymax = int(np.ceil(warped[:, 1].max()))
    return xmin, ymin, xmax, ymax


def inverse_coords(H, bbox):
    xmin, ymin, xmax, ymax = bbox
    xs, ys = np.meshgrid(np.arange(xmin, xmax + 1), np.arange(ymin, ymax + 1))
    out_pts = np.stack([xs.ravel(), ys.ravel()], axis=1)
    src_pts = apply_H(np.linalg.inv(H), out_pts)
    src_x = src_pts[:, 0].reshape(xs.shape)
    src_y = src_pts[:, 1].reshape(xs.shape)
    return src_x, src_y


def warpImageNearestNeighbor(im, H, bbox=None):
    if bbox is None:
        bbox = warp_bbox(im.shape, H)
    h, w, c = im.shape
    src_x, src_y = inverse_coords(H, bbox)

    cols = np.round(src_x).astype(int)
    rows = np.round(src_y).astype(int)
    inside = (cols >= 0) & (cols < w) & (rows >= 0) & (rows < h)

    out = np.zeros((src_x.shape[0], src_x.shape[1], c + 1))
    out[inside, :c] = im[rows[inside], cols[inside]]
    out[inside, c] = 1
    return out


def warpImageBilinear(im, H, bbox=None):
    if bbox is None:
        bbox = warp_bbox(im.shape, H)
    h, w, c = im.shape
    src_x, src_y = inverse_coords(H, bbox)

    inside = (src_x >= 0) & (src_x <= w - 1) & (src_y >= 0) & (src_y <= h - 1)
    x = src_x[inside]
    y = src_y[inside]

    x0 = np.clip(np.floor(x).astype(int), 0, w - 2)
    y0 = np.clip(np.floor(y).astype(int), 0, h - 2)
    x1 = x0 + 1
    y1 = y0 + 1
    dx = (x - x0)[:, None]
    dy = (y - y0)[:, None]

    top = im[y0, x0] * (1 - dx) + im[y0, x1] * dx
    bottom = im[y1, x0] * (1 - dx) + im[y1, x1] * dx

    out = np.zeros((src_x.shape[0], src_x.shape[1], c + 1))
    out[inside, :c] = top * (1 - dy) + bottom * dy
    out[inside, c] = 1
    return out


def center_weight(shape):
    h, w = shape[:2]
    wx = 1 - np.abs(np.linspace(-1, 1, w))
    wy = 1 - np.abs(np.linspace(-1, 1, h))
    return np.outer(wy, wx)


def chain_to_ref(pair_Hs, ref):
    Hs = []
    for i in range(len(pair_Hs) + 1):
        H = np.eye(3)
        if i < ref:
            for j in range(i, ref):
                H = pair_Hs[j] @ H
        else:
            for j in range(i, ref, -1):
                H = np.linalg.inv(pair_Hs[j - 1]) @ H
        Hs.append(H)
    return Hs


def mosaic_bbox(ims, Hs):
    boxes = np.array([warp_bbox(im.shape, H) for im, H in zip(ims, Hs)])
    xmin = boxes[:, 0].min()
    ymin = boxes[:, 1].min()
    xmax = boxes[:, 2].max()
    ymax = boxes[:, 3].max()
    return xmin, ymin, xmax, ymax


def build_mosaic(ims, Hs):
    bbox = mosaic_bbox(ims, Hs)

    images = []
    lows = []
    highs = []
    alphas = []
    weights = []
    for im, H in zip(ims, Hs):
        low = cv.GaussianBlur(im, (0, 0), SIGMA)
        high = im - low
        weight = center_weight(im.shape)

        stack = np.dstack([im, low, high, weight])
        warped = warpImageBilinear(stack, H, bbox)

        images.append(warped[:, :, 0:3])
        lows.append(warped[:, :, 3:6])
        highs.append(warped[:, :, 6:9])
        alphas.append(warped[:, :, 10])
        weights.append(warped[:, :, 9] * warped[:, :, 10])
    weights = np.array(weights)

    noblend = np.zeros_like(images[0])
    for im, alpha in zip(images, alphas):
        noblend[alpha > 0] = im[alpha > 0]

    total = weights.sum(axis=0)
    safe_total = np.maximum(total, 1e-8)[:, :, None]
    feather = np.zeros_like(noblend)
    low = np.zeros_like(noblend)
    for i in range(len(ims)):
        w = weights[i][:, :, None]
        feather += w * images[i]
        low += w * lows[i]
    feather /= safe_total
    low /= safe_total

    best = weights.argmax(axis=0)
    high = np.zeros_like(noblend)
    for i in range(len(ims)):
        high[best == i] = highs[i][best == i]
    blend = low + high
    blend[total == 0] = 0

    return noblend, feather, blend


def mosaic(imgs: list[Path], points: list[Path], name: str, ref: int):
    ims = [load_rgb(path) for path in imgs]
    scale = MAX_DIM / max(ims[0].shape[:2])
    ims = [cv.resize(im, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA) for im in ims]

    pair_Hs = []
    for path in points:
        pts1, pts2 = np.load(path)
        pts1 = (pts1 + 0.5) * scale - 0.5
        pts2 = (pts2 + 0.5) * scale - 0.5
        pair_Hs.append(computeH(pts1, pts2))
    Hs = chain_to_ref(pair_Hs, ref)

    noblend, feather, blend = build_mosaic(ims, Hs)

    out_dir = Path("out/a4")
    save_rgb(out_dir / f"{name}_noblend.jpg", noblend)
    save_rgb(out_dir / f"{name}_feather.jpg", feather)
    save_rgb(out_dir / f"{name}_blend.jpg", blend)

    padded = [np.pad(im, ((0, 0), (10, 10), (0, 0)), constant_values=1) for im in ims]
    save_rgb(out_dir / f"{name}_sources.jpg", np.hstack(padded))


def pick(img1: Path, img2: Path, points: Path, n: int):
    pts1, pts2 = pick_points(load_rgb(img1), load_rgb(img2), n)
    np.save(points, np.stack([pts1, pts2]))


def a2(img1: Path, img2: Path, points: Path):
    out_dir = Path("out/a2")
    out_dir.mkdir(parents=True, exist_ok=True)
    pts1, pts2 = np.load(points)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    axes[0].imshow(load_rgb(img1))
    axes[0].scatter(pts1[:, 0], pts1[:, 1], c="red")
    axes[0].axis("off")
    axes[1].imshow(load_rgb(img2))
    axes[1].scatter(pts2[:, 0], pts2[:, 1], c="red")
    axes[1].axis("off")
    fig.tight_layout()
    fig.savefig(out_dir / f"{points.stem}_correspondences.jpg", dpi=150)
    plt.close(fig)

    A, b = build_system(pts1, pts2)
    H = computeH(pts1, pts2)
    np.set_printoptions(precision=4, suppress=True, linewidth=150)
    text = f"A:\n{A}\n\nb:\n{b}\n\nH:\n{H}\n"
    (out_dir / f"{points.stem}.txt").write_text(text)
    print(text)


def rectify(img: Path, width: int, height: int):
    im = load_rgb(img)
    plt.imshow(im)
    corners = np.array(plt.ginput(4, timeout=0))
    plt.close()

    out_dir = Path("out/a3")
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / f"{img.stem}_corners.npy", corners)
    rectify_with(im, corners, width, height, img.stem)


def rectify_with(im, corners, width, height, name):
    target = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    H = computeH(corners, target)
    bbox = (-width // 2, -height // 2, width * 3 // 2, height * 3 // 2)

    out_dir = Path("out/a3")
    for label, warp in [("nn", warpImageNearestNeighbor), ("bilinear", warpImageBilinear)]:
        start = time.perf_counter()
        out = warp(im, H, bbox)
        print(f"{name} {label}: {time.perf_counter() - start:.2f}s")
        save_rgb(out_dir / f"{name}_rectified_{label}.png", out)


if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict({"pick": pick, "a2": a2, "rectify": rectify, "mosaic": mosaic})
