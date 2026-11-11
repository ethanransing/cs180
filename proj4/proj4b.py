import tyro
from pathlib import Path

import numpy as np
import cv2 as cv
from skimage.color import rgb2gray

from harris import get_harris_corners, dist2
from proj4 import MAX_DIM, build_mosaic, chain_to_ref, computeH, apply_H, load_rgb, save_rgb

SAVE_DIR = Path(__file__).resolve().parent / "out/b4"

def main(imgs: list[Path], name: str, ref: int):
    raw_ims = []
    for path in imgs:
        im = load_rgb(path)
        raw_ims.append(im)

    scale = MAX_DIM / max(raw_ims[0].shape[:2])
    ims = []
    for im in raw_ims:
        im_resized = cv.resize(im, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA)
        ims.append(im_resized)

    features = []
    for im in ims:
        im_features = get_features(im)
        features.append(im_features)

    pair_Hs = []
    for (corners1, descriptors1), (corners2, descriptors2) in zip(features, features[1:]):
        matches = match_features(descriptors1, descriptors2)
        matched_pts1 = corners1[matches[:, 0]]
        matched_pts2 = corners2[matches[:, 1]]
        H, _ = ransac_homography(matched_pts1, matched_pts2)
        pair_Hs.append(H)

    blend = build_mosaic(ims, chain_to_ref(pair_Hs, ref))[2]
    save_path = SAVE_DIR / f"{name}_blend.jpg"
    print(f'saved at {save_path}')
    save_rgb(save_path, blend)

def get_features(im):
    gray = rgb2gray(im)
    harris_strengths, coords = get_harris_corners(gray)
    ys, xs = coords
    corner_xy = np.stack([xs, ys], axis=1)
    corners = anms(corner_xy, harris_strengths[ys, xs])
    descriptors = extract_descriptors(gray, corners)
    return corners, descriptors

MAX_HARRIS_CORNERS = 8000
def anms(corner_xy, strengths, n_keep=1000):
    strongest_idxs = np.argsort(-strengths)[:MAX_HARRIS_CORNERS]
    corner_xy = corner_xy[strongest_idxs]
    strengths = strengths[strongest_idxs]
    sq_dists = dist2(corner_xy, corner_xy)

    strength_i = strengths[:, None]
    strength_j = strengths[None, :]
    j_is_stronger = strength_i < 0.9 * strength_j
    not_stronger = ~j_is_stronger

    sq_dists[not_stronger] = np.inf
    radii = sq_dists.min(axis=1)
    largest_radii_idxs = np.argsort(-radii)[:n_keep]
    return corner_xy[largest_radii_idxs]

def extract_descriptors(gray, corners):
    blurred = cv.GaussianBlur(gray, (0, 0), 2)

    descriptors = []
    for x, y in corners:
        patch = blurred[y - 20:y + 20:5, x - 20:x + 20:5]
        normalized_patch = (patch - patch.mean()) / patch.std()
        descriptors.append(normalized_patch.ravel())
    return np.array(descriptors)

def match_features(descriptors1, descriptors2, ratio=0.8):
    dists = np.sqrt(dist2(descriptors1, descriptors2))

    matches = []
    for i in range(len(descriptors1)):
        sorted_idxs = np.argsort(dists[i])
        closest_dist = dists[i, sorted_idxs[0]]
        second_closest_dist = dists[i, sorted_idxs[1]]
        if closest_dist / second_closest_dist < ratio:
            matches.append([i, sorted_idxs[0]])
    return np.array(matches)

def ransac_homography(pts1, pts2, n_iters=2000, inlier_threshold=2.0):
    rng = np.random.default_rng(0)

    max_inliers, best_inliers = 0, None
    for _ in range(n_iters):
        sample_idxs = rng.choice(len(pts1), 4, replace=False)
        H = computeH(pts1[sample_idxs], pts2[sample_idxs])
        projected_pts1 = apply_H(H, pts1)
        errors = np.linalg.norm(projected_pts1 - pts2, axis=1)
        inliers = errors < inlier_threshold
        num_inliers = inliers.sum()
        if num_inliers > max_inliers:
            max_inliers = num_inliers
            best_inliers = inliers

    best_H = computeH(pts1[best_inliers], pts2[best_inliers])
    return best_H, best_inliers

if __name__ == "__main__":
    tyro.cli(main)
