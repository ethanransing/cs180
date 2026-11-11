from pathlib import Path

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

from harris import get_harris_corners
from proj4 import MAX_DIM, load_rgb
from proj4b import anms, get_features, match_features

ASSETS = Path(__file__).resolve().parent / "assets"
SAVE_DIR = Path(__file__).resolve().parent / "out/b_figures"

def main():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    im1, im2 = load_pair("elaichi_1", "elaichi_2")
    corners_figure(im1)
    descriptors_figure(im1)
    matches_figure(im1, im2)

def load_pair(name1, name2):
    raw_ims = []
    for name in [name1, name2]:
        im = load_rgb(ASSETS / f"{name}.jpg")
        raw_ims.append(im)

    scale = MAX_DIM / max(raw_ims[0].shape[:2])
    ims = []
    for im in raw_ims:
        im_resized = cv.resize(im, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA)
        ims.append(np.clip(im_resized, 0, 1))
    return ims

def corners_figure(im):
    gray = rgb2gray(im)
    h, coords = get_harris_corners(gray)
    ys, xs = coords
    xy = np.stack([xs, ys], axis=1)
    corners = anms(xy, h[ys, xs])
    print(f"harris: {len(xy)} corners, anms: {len(corners)} corners")

    plot_points(im, xy, "harris.jpg")
    plot_points(im, corners, "anms.jpg")

def plot_points(im, xy, name):
    h, w = im.shape[:2]
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(im)
    ax.scatter(xy[:, 0], xy[:, 1], s=6, c="red")
    ax.axis("off")
    fig.savefig(SAVE_DIR / name)
    plt.close(fig)

def descriptors_figure(im):
    gray = rgb2gray(im)
    xy, descs = get_features(im)

    n_show = 8
    fig, axes = plt.subplots(2, n_show, figsize=(16, 4.4))
    for i in range(n_show):
        x, y = xy[i]
        window = gray[y - 20:y + 20, x - 20:x + 20]
        axes[0, i].imshow(window, cmap="gray")
        axes[0, i].set_title(f"({x}, {y})")
        axes[1, i].imshow(descs[i].reshape(8, 8), cmap="gray")
        axes[0, i].axis("off")
        axes[1, i].axis("off")
    fig.savefig(SAVE_DIR / "descriptors.jpg", dpi=100, bbox_inches="tight")
    plt.close(fig)

def matches_figure(im1, im2):
    xy1, desc1 = get_features(im1)
    xy2, desc2 = get_features(im2)
    matches = match_features(desc1, desc2)
    pts1, pts2 = xy1[matches[:, 0]], xy2[matches[:, 1]]
    plot_matches(im1, im2, pts1, pts2, "matches.jpg")

def plot_matches(im1, im2, pts1, pts2, name):
    canvas = np.hstack([im1, im2])
    w1 = im1.shape[1]
    h, w = canvas.shape[:2]

    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(canvas)
    for p1, p2 in zip(pts1, pts2):
        ax.plot([p1[0], p2[0] + w1], [p1[1], p2[1]], color="yellow", linewidth=1, marker="o", markersize=3)
    ax.axis("off")
    fig.savefig(SAVE_DIR / name)
    plt.close(fig)

if __name__ == "__main__":
    main()
