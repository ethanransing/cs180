// Hand-written per-section descriptions for this project page. Edit the
// strings below — script.js drops each one (as HTML) into its matching
// .section-desc[data-key] element. Multi-paragraph entries should use a
// <div class="section-desc"> in index.html and wrap each paragraph in <p>.
// Empty strings are hidden on the page, so unwritten sections don't show.
//
// The comment above each key says what the project spec asks that section to
// cover, and which figures it sits under.
window.PROJECT_CONTENT = {
  // Short intro to the project as a whole.
  overview: "In this project, we stitch multiple photos into a single panorama. In Part A, we hand-pick point correspondences between overlapping photos, solve for the homography that relates them, warp the images with our own inverse warping code, and blend them into a mosaic.",

  // ===== A.1 Shoot the Pictures =====
  // Above the source images: how the photos were taken (fixed center of
  // projection, rotating the camera, ~40–70% overlap).
  "shoot-intro": "I took three sets of photos with a (mostly) still camera and rotated about the lens -- outside Elaichi, inside of it, and my roommate's bedroom wall.",
  // Under the three sets: anything notable about the scenes.
  "shoot-notes": "The building and the bedroom wall are mostly flat surfaces far from the camera, which is the ideal case for a homography. The café is a harder scene for our rectangular mapping because the room has a lot of depth and people moved between the two shots.",

  // ===== A.2 Recover Homographies =====
  // Above the equations: H has 8 unknowns (H[2,2] = 1), each correspondence
  // gives two linear equations, solved with least squares for n > 4.
  "homography-intro": "A homography \\(H\\) maps a point \\((x, y)\\) in one image to \\((x', y')\\) in the other, up to a scale factor. There are 8 unknowns, which means 4 points in (x, y) space provide enough values to solve for each unknown, but using least-squares with more points gives us a more reliable estimate of our \\(A\\mathbf{h} = \\mathbf{b}\\) system.",
  // How the correspondences were picked (side-by-side ginput tool).
  "correspondence-tool": "Spreading the points across the whole overlap turned out to matter a lot: my first attempt put every point on one pillar, and that homography was off by over 60 pixels everywhere else in the image.",
  // Under the correspondences and recovered matrices.
  "homography-results": "Each \\(H\\) maps the first image's pixel coordinates into the second's. The big translation terms come from panning the camera between shots, and the tiny bottom-row values are what make it a projective transform (rather than just an affine one). Once the points were spread out, the Elaichi and bedroom homographies line up the overlapping images to within a few pixels.",

  // ===== A.3 Warp the Images =====
  // Above the code: inverse warping, bounding box from the four corners,
  // alpha mask, and the two interpolation methods (written from scratch).
  "warp-intro": "Both warps use inverse warping. We push the four corners of the input through \\(H\\) to get the output's bounding box, then send every output pixel back through \\(H^{-1}\\) to see where it came from in the source image. Nearest neighbor just rounds to the closest pixel, and bilinear takes a weighted average of the four pixels around it. Both also return an alpha channel that's 0 wherever there's no source pixel.",
  // Above the synthetic figure: how the test images were made.
  "rectify-synthetic": "Before trying real photos, I tested on a hardcoded \\(400 \\times 400\\) matrix of 0s with a \\(200 \\times 200\\) square of 1s in the middle. I warped it into three perspective views, rectified each one back with its four corners, and compared against the original matrix. Both methods get the square back almost perfectly -- the only wrong pixels are a handful along the edges.",
  // Under the real rectifications: what rectification shows and why it works.
  "rectify-results": "For rectification, we mark the four corners of something we know is a rectangle, solve for the \\(H\\) that sends them to an upright rectangle, and warp the whole image. The Elaichi window was shot from the sidewalk looking up, and after rectifying it the window grid is square and the siding is horizontal (like we're standing right in front of the wall). Anything that's not on the wall, like the tree branches, gets stretched since a homography only works for one plane.",
  // Under the zoom and timing table: speed vs. quality tradeoff.
  "interp-comparison": "<p>Nearest neighbor is about 2x faster since it only reads one pixel per output pixel instead of four. But zoomed in, its edges are jagged and stair-stepped, while bilinear is smooth (if slightly softer).</p><p>The jaggies are basically aliasing. Nearest neighbor takes a single sample of the source for each output pixel with no smoothing, so sharp edges and fine repeating detail (like the siding stripes) get chopped into blocky steps. Bilinear averages its four neighbors, which acts like a tiny low-pass filter before sampling and smooths most of that out. It's not a full fix though -- if we shrank an image a lot, both would still alias without blurring first. Since the quality difference is worth the extra time, I used bilinear for all the mosaics.</p>",

  // ===== A.4 Blend the Images into a Mosaic =====
  // Above the code: one-shot procedure (warp everything into the reference
  // frame on a shared canvas), alpha falloff, feathering, 2-level pyramid.
  "mosaic-intro": "<p>We keep the middle image fixed and warp the others into its frame, chaining homographies through neighboring pairs (for Elaichi, left &rarr; middle &larr; right). We first push every image's corners through its homography to get the size of the whole mosaic, then warp everything onto that one canvas. To keep things fast, the images are downscaled to 1500 pixels on the long side (and the points are scaled to match).</p><p>Each image also gets an alpha map that's 1 at its center and falls off linearly to 0 at its edges, which gets warped along with it. We save three versions of each mosaic:</p><ul><li><b>No blending</b>: each image is just pasted over the previous ones.</li><li><b>Feathering</b>: a weighted average of the images, using the alpha maps as weights.</li><li><b>Two-band blending</b> (a 2-level Laplacian pyramid).</li></ul>",
  // Under the building mosaic.
  "mosaic-building": "With the points spread out, the facade lines up across both seams -- the windows, pillars, and roof run straight across all three photos. Without blending there are some small exposure seams in the sky and street, which both blending methods get rid of. The car hood in the bottom-left is way closer to the camera than the building, so it doesn't line up (best to just crop it out).",
  // Under the café mosaic and close-up: ghosting, and why depth breaks the homography.
  "mosaic-cafe": "My roommate moved between the shots and is right up close to the camera, so their face doesn't line up between the two photos. The ghosting present in the feathered image but not the Laplacian two-band one demonstrates the benefit of a Laplacian stack.",
  // Under the bedroom mosaic and close-up: exposure seams.
  "mosaic-bedroom": "",

  // ===== What I Learned =====
  learned: "I learned that a homography's quality depends a lot on where the correspondences are, not just how precise they are -- points bunched in one spot fit perfectly there and fall apart everywhere else. I also got a better feel for the limits of the model. A homography is exact for a flat scene or a camera that only rotates, so anything at a different depth (or anything that moves between shots) will never line up, no matter how good the points are!"
};
