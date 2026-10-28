from pathlib import Path

import numpy as np
from proj4 import computeH, warpImageNearestNeighbor, warpImageBilinear, save_rgb

N = 400
square = np.zeros((N, N))
square[100:300, 100:300] = 1
card = np.array([[0, 0], [N - 1, 0], [N - 1, N - 1], [0, N - 1]])

scenes = {
    "floor": [[250, 300], [550, 300], [700, 550], [100, 550]],
    "wall": [[150, 80], [600, 180], [600, 470], [150, 560]],
    "tilted": [[300, 60], [680, 200], [520, 560], [90, 380]],
}

out = Path("out/a3/test")
for name, corners in scenes.items():
    corners = np.array(corners, float)
    photo = warpImageBilinear(square[..., None], computeH(card, corners), (0, 0, 799, 599))[..., 0]
    save_rgb(out / f"{name}_input.png", np.dstack([photo] * 3))
    for label, warp in (("nn", warpImageNearestNeighbor), ("bilinear", warpImageBilinear)):
        rect = warp(photo[..., None], computeH(corners, card), (0, 0, N - 1, N - 1))[..., 0]
        save_rgb(out / f"{name}_rectified_{label}.png", np.dstack([rect] * 3))
        print(f"{name} {label}: mean |error| {np.abs(rect - square).mean():.4f}, "
              f"pixels off by > 0.5: {(np.abs(rect - square) > 0.5).mean():.2%}")
