import tyro 
from datetime import datetime
from pathlib import Path
from typing import Literal
import time

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

SEARCH_WINDOW = 15
NormName = Literal["l2", "ncc"]
SAVE_DIR = Path(__file__).resolve().parent / "curated_pics_batch"

# EXAMPLE:
# uv run proj1.py --path PATH_HERE.tif --norm l2 --pyramid
# uv run proj1.py --path DIR_OF_IMAGES --norm ncc

def main(
    path: Path,
    norm: NormName = "l2",
    pyramid: bool = False,
):
    if path.is_dir():
        for img_path in path.iterdir():
            print(f"processing {img_path}")
            colorize_image(img_path, norm, pyramid)
    else:
        colorize_image(path, norm, pyramid)

def colorize_image(img_path, norm, pyramid):
    im = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    im = im.astype(np.float32) / 255.0
    height = int(np.floor(im.shape[0] / 3.0))

    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    norm_fn = NORMS[norm]
    start_time = time.perf_counter()
    if pyramid: 
        print("\nusing pyramid search")
        g_shift_rows, g_shift_cols = get_shift_with_pyramid(b, g, norm_fn)
        r_shift_rows, r_shift_cols = get_shift_with_pyramid(b, r, norm_fn)
    else:
        print("\nusing naive search")
        start_time = time.perf_counter()
        g_shift_rows, g_shift_cols = get_shift_with_exhaustive_search(b, g, norm_fn)
        r_shift_rows, r_shift_cols = get_shift_with_exhaustive_search(b, r, norm_fn)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"execution time: {execution_time} seconds")

    g_shifted = np.roll(g, (g_shift_rows, g_shift_cols), axis=(0, 1))
    r_shifted = np.roll(r, (r_shift_rows, r_shift_cols), axis=(0, 1))
    print(f"\ngreen shift: ({g_shift_rows}, {g_shift_cols})")
    print(f"red shift: ({r_shift_rows}, {r_shift_cols})")

    im_out = np.dstack([r_shifted, g_shifted, b])
    # plt.figure(figsize=(8, 8))
    # plt.imshow(im_out)
    # plt.title('Colorized')
    # plt.axis('off')
    # plt.show()

    out_uint8 = np.clip(im_out * 255.0, 0, 255).astype(np.uint8)
    out_bgr = cv.cvtColor(out_uint8, cv.COLOR_RGB2BGR)

    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if pyramid:
        fname = SAVE_DIR / f"{img_path.stem}_pyramid_{norm}_{timestamp}.jpg"
    else:
        fname = SAVE_DIR / f"{img_path.stem}_{norm}_{timestamp}.jpg"
    cv.imwrite(str(fname), out_bgr)
    print(f"\nSaved to {fname}")

    metrics_fname = fname.with_suffix(".txt")
    with open(metrics_fname, "w", encoding='utf-8') as file:
        file.write(f"img path: {fname}")
        file.write(f"\ngreen shift: ({g_shift_rows}, {g_shift_cols})")
        file.write(f"\nred shift: ({r_shift_rows}, {r_shift_cols})")
        file.write(f"\nexecution time: {execution_time}")
    print(f"Wrote metrics to {metrics_fname}")

# im1, im2 --> rows to shift im2, cols to shift im2
def get_shift_with_pyramid(im1, im2, norm, scale=16) -> tuple[int, int]:
    total_r_shift, total_c_shift = 0, 0
    im1_downscaled, im2_downscaled = im1[::scale, ::scale], im2[::scale, ::scale] # naive, aliasing

    r_shift, c_shift = get_shift_with_exhaustive_search(im1_downscaled, im2_downscaled, norm)
    total_r_shift += scale * r_shift
    total_c_shift += scale * c_shift

    # align using our best estimate so far
    im2_aligned = np.roll(im2, (total_r_shift, total_c_shift), axis=(0, 1))

    # divide scale by 2 in recursive calls
    if scale != 1:
        recursive_r_shift, recursive_c_shift = get_shift_with_pyramid(im1, im2_aligned, norm, scale // 2)
        total_r_shift += recursive_r_shift
        total_c_shift += recursive_c_shift 

    return total_r_shift, total_c_shift

# im1, im2 --> rows to shift im2, cols to shift im2
def get_shift_with_exhaustive_search(im1, im2, norm) -> tuple[int, int]:
    min_score, best_r_shift, best_c_shift = float('inf'), None, None
    for r in range(-SEARCH_WINDOW, SEARCH_WINDOW + 1, 1):
        for c in range (-SEARCH_WINDOW , SEARCH_WINDOW + 1, 1):
            im2_shifted = np.roll(im2, (r, c), axis=(0, 1))
            s = score(im1, im2_shifted, norm)
            if s < min_score:
                best_r_shift, best_c_shift = r, c
            min_score = min(min_score, s)
    
    return best_r_shift, best_c_shift

def score(im1, im2, norm, crop_percentage=0.10):
    h, w = im1.shape
    crop_h = int(h * crop_percentage)
    crop_w = int(w * crop_percentage)
    cropped_im1 = im1[crop_h:h-crop_h, crop_w:w-crop_w]
    cropped_im2 = im2[crop_h:h-crop_h, crop_w:w-crop_w]
    return norm(cropped_im1, cropped_im2)

def l2_norm(im1, im2):
    return np.sqrt(np.sum((im1 - im2) ** 2))

def ncc_norm(im1, im2):
    im1_normalized = (im1 - np.mean(im1)) / np.linalg.norm(im1 - np.mean(im1))
    im2_normalized = (im2 - np.mean(im2)) / np.linalg.norm(im2 - np.mean(im2))
    
    # return negative since we minimize in align()
    return -1 * np.dot(im1_normalized.ravel(), im2_normalized.ravel())

NORMS = {"l2": l2_norm, "ncc": ncc_norm}

if __name__ == "__main__":
    tyro.cli(main)