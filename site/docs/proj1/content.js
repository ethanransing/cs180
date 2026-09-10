// Hand-written per-section descriptions for this project page. Edit the
// strings below — script.js drops each one into its matching
// <p class="section-desc" data-key="...">.
window.PROJECT_CONTENT = {
  overview: "[Placeholder: intro to the Prokudin-Gorskii glass-plate collection and the goal of automatically colorizing the digitized negatives by separating and stacking the B/G/R channels.]",
  "naive-stacking": "[Placeholder: explain why simply stacking the three channels without alignment fails — the plates were photographed at slightly different times/positions, so each channel is offset from the others.]",
  "single-scale": "[Placeholder: describe the exhaustive single-scale search — for every candidate (row, col) shift in a fixed window, score the alignment with a similarity metric (L2 / NCC) and keep the best-scoring shift. Note that this only works when the true displacement is smaller than the search window, which is fine for the small .jpg examples.]",
  pyramid: "[Placeholder: describe the image pyramid speedup — recursively downscale both channels, run the same exhaustive search at the coarsest level to get a rough shift, upscale and refine at each finer level. This lets the search window stay small while still finding large displacements, which is necessary for the full-resolution .tif images.]",
  results: "[Placeholder: overall discussion of results across the full image set — how well alignment worked, which images were hardest, and any qualitative observations about the NCC vs. L2 metrics.]",
  problems: "[Placeholder: problems encountered — e.g. border artifacts from the roll-based shift wrapping around the edges, and any images that were especially slow or difficult to align.]"
};
