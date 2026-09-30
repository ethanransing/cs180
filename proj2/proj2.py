import math
import time
import tyro
from pathlib import Path
from datetime import datetime

from scipy.signal import convolve2d
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import skimage.transform as sktr

def convolve_four_loops(vec1, vec2):
    vec1 = np.asarray(vec1)
    vec2 = np.atleast_2d(np.asarray(vec2))
    kh, kw = vec2.shape
    output = np.zeros((vec1.shape[0] + kh - 1, vec1.shape[1] + kw - 1))
    padded = np.pad(vec1, ((kh - 1, kh - 1), (kw - 1, kw - 1)))
    conv_kernel = np.flip(vec2)
    for i in range(len(output)):
        for j in range(len(output[0])):
            for i_kernel in range(len(conv_kernel)):
                for j_kernel in range(len(conv_kernel[0])):
                    output[i][j] += padded[i + i_kernel][j + j_kernel] * conv_kernel[i_kernel][j_kernel]
    return output

def convolve_two_loops(vec1, vec2):
    output = np.zeros(shape=np.array(vec1.shape) + np.array(vec2.shape) - 1)
    vec1 = np.pad(vec1, ((vec2.shape[0] - 1, vec2.shape[0] - 1), (vec2.shape[1] - 1, vec2.shape[1] - 1)))
    conv_kernel = np.flip(vec2)
    for i in range(len(output)):
        for j in range(len(output[0])):
            patch = vec1[i: i + conv_kernel.shape[0], j: j + conv_kernel.shape[1]]
            output[i][j] = np.sum(patch * conv_kernel)
    return output


def get_points(im1: np.ndarray, im2: np.ndarray) -> tuple:
    print('Please select 2 points in each image for alignment.')
    plt.imshow(im1)
    p1, p2 = plt.ginput(2)
    plt.close()
    plt.imshow(im2)
    p3, p4 = plt.ginput(2)
    plt.close()
    return (p1, p2, p3, p4)


def recenter(im: np.ndarray, r: float, c: float) -> np.ndarray:
    R, C = im.shape[:2]
    rpad = int(np.abs(2*r+1 - R))
    cpad = int(np.abs(2*c+1 - C))
    pad_width = [(0 if r > (R-1)/2 else rpad, 0 if r < (R-1)/2 else rpad),
                 (0 if c > (C-1)/2 else cpad, 0 if c < (C-1)/2 else cpad)]
    if im.ndim == 3:
        pad_width.append((0, 0))
    return np.pad(im, pad_width, 'constant')


def find_centers(p1: tuple, p2: tuple) -> tuple:
    cx = np.round(np.mean([p1[0], p2[0]]))
    cy = np.round(np.mean([p1[1], p2[1]]))
    return cx, cy


def align_image_centers(im1: np.ndarray, im2: np.ndarray, pts: tuple) -> tuple:
    p1, p2, p3, p4 = pts

    cx1, cy1 = find_centers(p1, p2)
    cx2, cy2 = find_centers(p3, p4)

    im1 = recenter(im1, cy1, cx1)
    im2 = recenter(im2, cy2, cx2)
    return im1, im2


def rescale_images(im1: np.ndarray, im2: np.ndarray, pts: tuple) -> tuple:
    p1, p2, p3, p4 = pts
    len1 = np.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
    len2 = np.sqrt((p4[1] - p3[1])**2 + (p4[0] - p3[0])**2)
    dscale = len2/len1
    channel_axis = -1
    if dscale < 1:
        im1 = sktr.rescale(im1, dscale, channel_axis=channel_axis)
    else:
        im2 = sktr.rescale(im2, 1./dscale, channel_axis=channel_axis)
    return im1, im2


def rotate_im1(im1: np.ndarray, pts: tuple) -> tuple:
    p1, p2, p3, p4 = pts
    theta1 = math.atan2(-(p2[1] - p1[1]), (p2[0] - p1[0]))
    theta2 = math.atan2(-(p4[1] - p3[1]), (p4[0] - p3[0]))
    dtheta = theta2 - theta1
    im1 = sktr.rotate(im1, dtheta*180/np.pi)
    return im1, dtheta


def match_img_size(im1: np.ndarray, im2: np.ndarray) -> tuple:
    h1, w1 = im1.shape[:2]
    h2, w2 = im2.shape[:2]
    if h1 < h2:
        im2 = im2[int(np.floor((h2-h1)/2.)) : -int(np.ceil((h2-h1)/2.)), :]
    elif h1 > h2:
        im1 = im1[int(np.floor((h1-h2)/2.)) : -int(np.ceil((h1-h2)/2.)), :]
    if w1 < w2:
        im2 = im2[:, int(np.floor((w2-w1)/2.)) : -int(np.ceil((w2-w1)/2.))]
    elif w1 > w2:
        im1 = im1[:, int(np.floor((w1-w2)/2.)) : -int(np.ceil((w1-w2)/2.))]
    assert im1.shape == im2.shape
    return im1, im2


def align_images(im1: np.ndarray, im2: np.ndarray) -> tuple:
    pts = get_points(im1, im2)
    im1, im2 = align_image_centers(im1, im2, pts)
    im1, im2 = rescale_images(im1, im2, pts)
    im1, angle = rotate_im1(im1, pts)
    im1, im2 = match_img_size(im1, im2)
    return im1, im2

def main(
    img_path: Path,
    img_path2: Path | None = None,
    alpha: float = 1.0,
    sigma: float = 0,
    sigma_low: float = 6.0,
    sigma_high: float = 3.0,
    align: bool = False,
    points: tuple[float, ...] | None = None,
    crop: tuple[int, int, int, int] | None = None,
    levels: int = 5,
    sigma_stack: float = 2.0,
    mask: str = "vertical",
):
    # part1_1(img_path)
    # part1_2(img_path)
    # part1_3(img_path)
    # part2_1(img_path, alpha, sigma)
    part2_2(img_path, img_path2, sigma_low, sigma_high, align, points, crop)
    # part2_3(img_path, img_path2, levels, sigma_stack)
    # part2_4(img_path, img_path2, mask, levels, sigma_stack)

FINITE_DIFF_X = np.array([[1, 0, -1]])
FINITE_DIFF_Y = FINITE_DIFF_X.T

def load_gray(img_path: Path):
    return cv.imread(img_path, cv.IMREAD_GRAYSCALE).astype(np.float64) / 255

def conv_same(im, kernel):
    return convolve2d(im, kernel, mode="same", boundary="symm")

def save_outputs(save_dir: Path, stem: str, timestamp: str, outputs: dict):
    for name, img in outputs.items():
        fname = save_dir / f"{stem}_{name}_{timestamp}.jpg"
        cv.imwrite(str(fname), img)
        print(f"\nSaved {name} to {fname}")

def save_threshold_sweep(grad_magnitude, thresholds, fname):
    fig, axes = plt.subplots(1, len(thresholds), figsize=(4 * len(thresholds), 4.3))
    for ax, t in zip(axes, thresholds):
        ax.imshow(grad_magnitude > t, cmap="gray")
        ax.set_title(f"threshold {t}")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved threshold sweep to {fname}")

def gradients(im):
    partial_x = conv_same(im, FINITE_DIFF_X)
    partial_y = conv_same(im, FINITE_DIFF_Y)
    return partial_x, partial_y, np.sqrt(partial_x ** 2 + partial_y ** 2)

def part1_2(img_path: Path, threshold: float = 0.25):
    im = load_gray(img_path)
    partial_x, partial_y, grad_magnitude = gradients(im)
    edges = (grad_magnitude > threshold).astype(np.uint8) * 255

    SAVE_DIR = Path(__file__).resolve().parent / "part1.2"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_outputs(SAVE_DIR, img_path.stem, timestamp, {
        "partial_x": to_uint8_signed(partial_x),
        "partial_y": to_uint8_signed(partial_y),
        "grad_magnitude": to_uint8(grad_magnitude / grad_magnitude.max()),
        f"edges_t{threshold}": edges,
    })
    save_threshold_sweep(grad_magnitude, [0.1, 0.15, 0.25, 0.35],
                         SAVE_DIR / f"{img_path.stem}_threshold_sweep_{timestamp}.jpg")

def gaussian_2d(ksize: int = 9, sigma: float = 0):
    g = cv.getGaussianKernel(ksize=ksize, sigma=sigma)
    return g @ g.T

def dog_filters(ksize: int = 9, sigma: float = 0):
    g = gaussian_2d(ksize, sigma)
    return convolve2d(g, FINITE_DIFF_X), convolve2d(g, FINITE_DIFF_Y)

def part1_3(img_path: Path, threshold: float = 0.08, fd_threshold: float = 0.25):
    im = load_gray(img_path)
    g = gaussian_2d()
    dog_x, dog_y = dog_filters()

    blurred = conv_same(im, g)
    blur_x, blur_y, blur_magnitude = gradients(blurred)
    dog_px = conv_same(im, dog_x)
    dog_py = conv_same(im, dog_y)
    dog_magnitude = np.sqrt(dog_px ** 2 + dog_py ** 2)
    interior = (slice(10, -10), slice(10, -10))
    diff = max(np.abs(blur_x - dog_px)[interior].max(), np.abs(blur_y - dog_py)[interior].max())

    edges = (dog_magnitude > threshold).astype(np.uint8) * 255
    blur_edges = (blur_magnitude > threshold).astype(np.uint8) * 255

    SAVE_DIR = Path(__file__).resolve().parent / "part1.3"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = img_path.stem
    save_outputs(SAVE_DIR, stem, timestamp, {
        "gaussblur": to_uint8(blurred),
        "blur_then_partial_x": to_uint8_signed(blur_x),
        "blur_then_partial_y": to_uint8_signed(blur_y),
        "blur_then_grad_magnitude": to_uint8(blur_magnitude / blur_magnitude.max()),
        f"blur_then_edges_t{threshold}": blur_edges,
        "dog_partial_x": to_uint8_signed(dog_px),
        "dog_partial_y": to_uint8_signed(dog_py),
        "dog_grad_magnitude": to_uint8(dog_magnitude / dog_magnitude.max()),
        f"dog_edges_t{threshold}": edges,
    })
    save_threshold_sweep(dog_magnitude, [0.04, 0.06, 0.08, 0.12],
                         SAVE_DIR / f"{stem}_threshold_sweep_{timestamp}.jpg")

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
    for ax, (title, k) in zip(axes, [("Gaussian 9x9", g), ("DoG x", dog_x), ("DoG y", dog_y)]):
        m = np.abs(k).max()
        ax.imshow(k, cmap="gray", vmin=-m if k.min() < 0 else 0, vmax=m, interpolation="nearest")
        ax.set_title(title)
        ax.axis("off")
    fname = SAVE_DIR / f"filters_{timestamp}.jpg"
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved filters to {fname}")

    _, _, fd_magnitude = gradients(im)
    fig, axes = plt.subplots(2, 2, figsize=(8, 8.4))
    panels = [
        ("finite diff magnitude", fd_magnitude / fd_magnitude.max()),
        ("DoG magnitude", dog_magnitude / dog_magnitude.max()),
        (f"finite diff edges (t={fd_threshold})", fd_magnitude > fd_threshold),
        (f"DoG edges (t={threshold})", dog_magnitude > threshold),
    ]
    for ax, (title, img) in zip(axes.flat, panels):
        ax.imshow(img, cmap="gray")
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    fname = SAVE_DIR / f"{stem}_fd_vs_dog_{timestamp}.jpg"
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved comparison to {fname}")

def to_uint8(img):
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)

def to_uint8_signed(img):
    m = np.abs(img).max()
    return ((img / (2 * m) + 0.5) * 255).astype(np.uint8)

def convolve_color(im, kernel):
    if im.ndim == 2:
        return convolve2d(im, kernel, mode="same", boundary="symm")
    return np.dstack([
        convolve2d(im[:, :, c], kernel, mode="same", boundary="symm")
        for c in range(im.shape[2])
    ])

def part2_1(img_path: Path, alpha: float = 1.0, sigma: float = 0):
    im = cv.imread(img_path, cv.IMREAD_COLOR).astype(np.float64) / 255
    ksize = 9 if sigma == 0 else int(6 * sigma) | 1
    gaussian_1d = cv.getGaussianKernel(ksize=ksize, sigma=sigma)
    gaussian_kernel = gaussian_1d @ gaussian_1d.T

    impulse = np.zeros_like(gaussian_kernel)
    impulse[gaussian_kernel.shape[0] // 2, gaussian_kernel.shape[1] // 2] = 1
    unsharp_kernel = (1 + alpha) * impulse - alpha * gaussian_kernel

    blurred = convolve_color(im, gaussian_kernel)
    high_freq = im - blurred
    sharpened = convolve_color(im, unsharp_kernel)

    SAVE_DIR = Path(__file__).resolve().parent / "part2.1"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputs = {
        "blurred": to_uint8(blurred),
        "high_freq": to_uint8_signed(high_freq),
        f"sharpened_alpha{alpha}": to_uint8(sharpened),
    }
    stem = img_path.stem if sigma == 0 else f"{img_path.stem}_sigma{sigma}"
    for name, img in outputs.items():
        fname = SAVE_DIR / f"{stem}_{name}_{timestamp}.jpg"
        cv.imwrite(str(fname), img)
        print(f"\nSaved {name} to {fname}")

    alphas = [0, 0.5, 1, 2, 5]
    fig, axes = plt.subplots(1, len(alphas), figsize=(4 * len(alphas), 4.3))
    for ax, a in zip(axes, alphas):
        ax.imshow(to_rgb(np.clip(im + a * high_freq, 0, 1)))
        ax.set_title("original" if a == 0 else f"alpha = {a}")
        ax.axis("off")
    fig.tight_layout()
    fname = SAVE_DIR / f"{stem}_alpha_sweep_{timestamp}.jpg"
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved alpha sweep to {fname}")

    resharpened = convolve_color(blurred, unsharp_kernel)
    blur_err = np.abs(blurred - im).mean()
    resharpen_err = np.abs(resharpened - im).mean()
    print(f"\nmean = {blur_err:.4f}, mean = {resharpen_err:.4f}")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.3))
    panels = [("original", im), ("blurred", blurred), (f"blurred, then sharpened (alpha = {alpha})", resharpened)]
    for ax, (title, img) in zip(axes, panels):
        ax.imshow(to_rgb(np.clip(img, 0, 1)))
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    fname = SAVE_DIR / f"{stem}_resharpen_test_{timestamp}.jpg"
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved resharpen test to {fname}")

def gaussian_blur(im, sigma):
    ksize = int(6 * sigma)
    g = cv.getGaussianKernel(ksize, sigma)
    return convolve_color(convolve_color(im, g), g.T)

def to_gray(im):
    if im.ndim == 2:
        return im
    return im @ np.array([0.114, 0.587, 0.299]) 

def log_fft(im):
    return np.log(np.abs(np.fft.fftshift(np.fft.fft2(to_gray(im)))) + 1e-8)

def valid_crop(mask):
    top, bottom, left, right = 0, mask.shape[0], 0, mask.shape[1]
    while not mask[top:bottom, left:right].all():
        box = mask[top:bottom, left:right]
        bad = [(~box[0]).mean(), (~box[-1]).mean(), (~box[:, 0]).mean(), (~box[:, -1]).mean()]
        side = int(np.argmax(bad))
        if side == 0: top += 1
        elif side == 1: bottom -= 1
        elif side == 2: left += 1
        else: right -= 1
    return top, bottom, left, right

def fit_similarity(src, dst):
    src, dst = np.asarray(src, float), np.asarray(dst, float)
    A = np.zeros((2 * len(src), 4))
    A[0::2] = np.column_stack([src[:, 0], -src[:, 1], np.ones(len(src)), np.zeros(len(src))])
    A[1::2] = np.column_stack([src[:, 1], src[:, 0], np.zeros(len(src)), np.ones(len(src))])
    a, b, tx, ty = np.linalg.lstsq(A, dst.reshape(-1), rcond=None)[0]
    return np.array([[a, -b, tx], [b, a, ty]])

def part2_2(img_path: Path, img_path2: Path, sigma_low: float = 6.0, sigma_high: float = 3.0, align: bool = False,
            points: tuple[float, ...] | None = None, crop: tuple[int, int, int, int] | None = None):
    im1 = cv.imread(img_path, cv.IMREAD_COLOR).astype(np.float64) / 255
    im2 = cv.imread(img_path2, cv.IMREAD_COLOR).astype(np.float64) / 255
    if align or points is not None:
        if points is None:
            dst_pts, src_pts = np.reshape(get_points(im1[:, :, ::-1], im2[:, :, ::-1]), (2, 2, 2))
        else:
            dst_pts, src_pts = np.reshape(points, (2, -1, 2))
        M = fit_similarity(src_pts, dst_pts)
        size = (im1.shape[1], im1.shape[0])
        valid = cv.warpAffine(np.ones(im2.shape[:2]), M, size, flags=cv.INTER_LINEAR) > 0.999
        im2 = cv.warpAffine(im2, M, size, flags=cv.INTER_LINEAR)
        top, bottom, left, right = valid_crop(valid)
        if crop is not None:
            x0, y0, x1, y1 = crop
            top, bottom, left, right = max(top, y0), min(bottom, y1), max(left, x0), min(right, x1)
        im1, im2 = im1[top:bottom, left:right], im2[top:bottom, left:right]
    else:
        im2 = cv.resize(im2, (im1.shape[1], im1.shape[0]))

    low = gaussian_blur(im1, sigma_low)
    high = im2 - gaussian_blur(im2, sigma_high)
    hybrid = low + high

    SAVE_DIR = Path(__file__).resolve().parent / "part2.2"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{img_path.stem}_{img_path2.stem}"
    outputs = {
        "aligned1": to_uint8(im1),
        "aligned2": to_uint8(im2),
        "low": to_uint8(low),
        "high": to_uint8_signed(high),
        f"hybrid_low{sigma_low}_high{sigma_high}": to_uint8(hybrid),
    }
    for name, img in outputs.items():
        fname = SAVE_DIR / f"{stem}_{name}_{timestamp}.jpg"
        cv.imwrite(str(fname), img)
        print(f"\nSaved {name} to {fname}")

    panels = {
        img_path.stem: im1,
        img_path2.stem: im2,
        f"low-pass (σ={sigma_low})": low,
        f"high-pass (σ={sigma_high})": high,
        "hybrid": hybrid,
    }
    fig, axes = plt.subplots(1, len(panels), figsize=(4 * len(panels), 4))
    for ax, (title, img) in zip(axes, panels.items()):
        ax.imshow(log_fft(img), cmap="gray")
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    fname = SAVE_DIR / f"{stem}_fft_{timestamp}.jpg"
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)
    print(f"\nSaved fft to {fname}")

def gaussian_stack(im, levels, sigma):
    stack = [im]
    for i in range(1, levels):
        stack.append(gaussian_blur(stack[-1], sigma * 2 ** (i - 1)))
    return stack

def laplacian_stack(im, levels, sigma):
    g = gaussian_stack(im, levels, sigma)
    return [g[i] - g[i + 1] for i in range(levels - 1)] + [g[-1]]

def stretch(img):
    return (img - img.min()) / (img.max() - img.min())

def to_rgb(img):
    return img[:, :, ::-1]

def save_stacks_figure(im, levels, sigma, fname):
    g = gaussian_stack(im, levels, sigma)
    lap = laplacian_stack(im, levels, sigma)
    fig, axes = plt.subplots(2, levels, figsize=(3 * levels, 6.5))
    for i in range(levels):
        axes[0, i].imshow(to_rgb(np.clip(g[i], 0, 1)), cmap="gray")
        axes[0, i].set_title(f"Gaussian {i}")
        axes[1, i].imshow(to_rgb(stretch(lap[i])), cmap="gray")
        axes[1, i].set_title(f"Laplacian {i}")
    for ax in axes.flat:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)

def load_pair(img_path: Path, img_path2: Path):
    im1 = cv.imread(img_path, cv.IMREAD_COLOR).astype(np.float64) / 255
    im2 = cv.imread(img_path2, cv.IMREAD_COLOR).astype(np.float64) / 255
    im2 = cv.resize(im2, (im1.shape[1], im1.shape[0]))
    return im1, im2

def make_mask(spec: str, shape):
    h, w = shape[:2]
    mask = np.zeros((h, w))
    if spec == "vertical":
        mask[:, : w // 2] = 1
    elif spec == "horizontal":
        mask[: h // 2, :] = 1
    else:
        m = cv.imread(spec, cv.IMREAD_GRAYSCALE)
        mask = cv.resize(m, (w, h)).astype(np.float64) / 255
    return mask

def blend_stacks(im1, im2, mask, levels, sigma):
    lap1 = laplacian_stack(im1, levels, sigma)
    lap2 = laplacian_stack(im2, levels, sigma)
    mask_stack = [m[:, :, None] for m in gaussian_stack(mask, levels, sigma)]
    left = [m * l for m, l in zip(mask_stack, lap1)]
    right = [(1 - m) * l for m, l in zip(mask_stack, lap2)]
    combined = [a + b for a, b in zip(left, right)]
    return left, right, combined

def save_blend_figure(left, right, combined, rows, fname):
    levels = len(combined)
    fig, axes = plt.subplots(len(rows) + 1, 3, figsize=(9, 3 * (len(rows) + 1)))
    for r, i in enumerate(rows):
        row = [left[i], right[i], combined[i]]
        scale = max(np.abs(img).max() for img in row) + 1e-12
        for c, img in enumerate(row):
            shown = np.clip(img, 0, 1) if i == levels - 1 else img / (2 * scale) + 0.5
            axes[r, c].imshow(to_rgb(shown))
        axes[r, 0].set_ylabel(f"level {i}")
    for c, stack in enumerate([left, right, combined]):
        axes[-1, c].imshow(to_rgb(np.clip(sum(stack), 0, 1)))
    axes[-1, 0].set_ylabel("collapsed")
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(fname, dpi=150, pil_kwargs={"quality": 90})
    plt.close(fig)

def part2_3(img_path: Path, img_path2: Path, levels: int = 5, sigma: float = 2.0):
    im1, im2 = load_pair(img_path, img_path2)
    left, right, combined = blend_stacks(im1, im2, make_mask("vertical", im1.shape), levels, sigma)

    SAVE_DIR = Path(__file__).resolve().parent / "part2.3"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{img_path.stem}_{img_path2.stem}"
    for path, im in [(img_path, im1), (img_path2, im2)]:
        fname = SAVE_DIR / f"{path.stem}_stacks_L{levels}_s{sigma}_{timestamp}.jpg"
        save_stacks_figure(im, levels, sigma, fname)
        print(f"\nSaved stacks to {fname}")
    fname = SAVE_DIR / f"{stem}_fig3.42_L{levels}_s{sigma}_{timestamp}.jpg"
    save_blend_figure(left, right, combined, sorted({0, levels // 2, levels - 1}), fname)
    print(f"\nSaved figure to {fname}")
    fname = SAVE_DIR / f"{stem}_blended_L{levels}_s{sigma}_{timestamp}.jpg"
    cv.imwrite(str(fname), to_uint8(sum(combined)))
    print(f"\nSaved blend to {fname}")

def part2_4(img_path: Path, img_path2: Path, mask: str = "vertical", levels: int = 5, sigma: float = 2.0):
    im1, im2 = load_pair(img_path, img_path2)
    mask = make_mask(mask, im1.shape)
    left, right, combined = blend_stacks(im1, im2, mask, levels, sigma)
    SAVE_DIR = Path(__file__).resolve().parent / "part2.4"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_name = mask 
    stem = f"{img_path.stem}_{img_path2.stem}_{mask_name}_L{levels}_s{sigma}"
    fname = SAVE_DIR / f"{stem}_blended_{timestamp}.jpg"
    cv.imwrite(str(fname), to_uint8(sum(combined)))
    print(f"\nSaved blend to {fname}")
    fname = SAVE_DIR / f"{stem}_levels_{timestamp}.jpg"
    save_blend_figure(left, right, combined, list(range(levels)), fname)
    print(f"\nSaved figure to {fname}")

def part1_1(img_path: Path, timing_size: int = 256):
    im = load_gray(img_path)
    box_filter = np.ones(shape=(9, 9)) / 81

    SAVE_DIR = Path(__file__).resolve().parent / "part1.1"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = []

    rng = np.random.default_rng(0)
    a, k = rng.random((30, 40)), rng.random((5, 4))
    ref = convolve2d(a, k)

    scale = timing_size / max(im.shape)
    small = cv.resize(im, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA)
    report.append(f"\nruntime, {small.shape[1]}x{small.shape[0]} image, 9x9 box filter:")
    for name, fn in [("four loops", convolve_four_loops), ("two loops", convolve_two_loops),
                     ("scipy convolve2d", convolve2d)]:
        start = time.perf_counter()
        fn(small, box_filter)
        report.append(f"  {name:<17} {time.perf_counter() - start:8.4f} s")

    text = "\n".join(report)
    print(text)
    (SAVE_DIR / f"{img_path.stem}_report_{timestamp}.txt").write_text(text + "\n")

    kernel_map = {
        "box": (box_filter, to_uint8),
        "finite_diff_x": (FINITE_DIFF_X, to_uint8_signed),
        "finite_diff_y": (FINITE_DIFF_Y, to_uint8_signed),
    }
    save_outputs(SAVE_DIR, img_path.stem, timestamp, {
        name: show(convolve_two_loops(im, kernel)) for name, (kernel, show) in kernel_map.items()
    })

if __name__ == "__main__":
    tyro.cli(main)