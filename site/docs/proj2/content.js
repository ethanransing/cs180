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
  overview: "In this project, we explore some applications of Gaussian, partial derivate, convolution, and Laplacian kernels. With no learning we can still achieve some surprising results!",

  // ===== 1.1 Convolutions from Scratch =====
  // Above the code: how the four-loop and two-loop versions work (flipping the
  // kernel, padding mode).
  "conv-from-scratch": "Generally speaking, a convolution is the operation that gets the response of a signal when it's passed through a system. In an image processing this system is referred to as a kernel because it is typically << the input size. We use convolutions in conjuctions with specially-designed kernels to perform feature extraction and blurring among other things. Handwritten code for a convolution operator is included below:",
  // Under the runtime table: compare runtimes, and how boundaries are handled
  // (zero padding / "full" here vs. convolve2d).
  "conv-runtime": "Our two loop runtime is massive faster than the four loop runtime because it takes advantage of numpy's parallelization capabilities. The scipy implementation is massively faster again because it uses the FFT algorithm (which converts the arrays to the Fourier basis so we can multiply rather than divide), netting a significant asymptotic time complexity improvement.",
  // Under the box / Dx / Dy results on your photo.
  "conv-results": "These are the results of a convolution with various kernels!",

  // ===== 1.2 Finite Difference Operator =====
  // Under the partial derivative / gradient magnitude / edge images: what each shows.
  "finite-diff": "The finite difference in X and Y detect significant changes in brightness intensity between left/right and top/bottom pixels, respectively. Combining this allows us to get a general edge detection kernel with a binary threshold.",
  // Justify the 0.25 threshold (tradeoff between finding edges and removing noise).
  "threshold-choice": "I chose 0.25 as a reasonable tradeoff between finding edges and not capturing background noise.",

  // ===== 1.3 Derivative of Gaussian =====
  // Why blur first (the 9x9 Gaussian, sigma ~1.7). Blur-then-differentiate results,
  // including gradient magnitude and edges at threshold 0.08, sit below this.
  "dog-intro": "",
  // Under the DoG results: verify blur-then-differentiate matches the single DoG
  // convolution, and why. (Max difference away from the border: 7.38e-16.)
  "dog-same": "",
  // Under the finite difference vs. DoG comparison: "What differences do you see?"
  "dog-differences": "After applying a Gaussian blur, much of our background noise in our edge detection algorithm is removed. The outline on the true edges is also thicker.",

  // ===== 2.1 Image Sharpening =====
  // Derive unsharp masking, how it combines into a single convolution, and how it
  // relates to blur filters and high frequencies.
  "unsharp-intro": "We can implement a rudimentary unsharpeing algorithm by \"removing the blur\" from the image, which means we subtract a Gaussian blurred version from our original image. We can also add the high frequency components (which typically are the edges) to further sharpen the image.",
  // Under the taj.jpg alpha sweep: how the sharpening amount changes the result.
  "unsharp-taj": "It's interesting to see that as up our power constant, we see an oversharpening effect where the edges have overly high contrast (such as the white glow on the trees).",
  // Under your own image (IMG_4041, sigma 3, alpha 2) and its alpha sweep.
  "unsharp-mine": "These are my attempts to sharpen my chud dog! Our sharpening kernel identified his facial features, eyes, and some of his hair, resulting in a qualitatively sharper image.",
  // Under blur-then-resharpen (IMG_4041): observations comparing the original and the
  // resharpened image.
  "unsharp-resharpen": "The blur-and-resharpen picture appears similar to the original image. One downgrade I noticed was the shelf in the background (which was likely hurt from the overcontrasting applied by the sharpening kernel. But the reconstruction improves on much of the detail on my dog's face.",

  // ===== 2.2 Hybrid Images =====
  // How hybrid images work (low-pass one image, high-pass the other, add).
  "hybrid-intro": "Hybrid images take advantage of the fact that we see high-pass features more clearly at close range, and see low-pass features more clearly at a far distance. This is a neat application of the frequency domain in computation photography!",
  // Under the aligned / low-pass / high-pass images: how the pair was aligned
  // (landmark similarity fit, cropping to the valid region).
  "hybrid-alignment": "",
  // Under the FFT figure: what the log-magnitude spectra show.
  "hybrid-fft": "",
  // Under the Andrew + Goldberg hybrid: the cutoff frequency choice
  // (sigma_low = 6, sigma_high = 3) and how you picked it.
  "hybrid-cutoff": "",
  // Under the Samarth + dog hybrid (sigma_low = 8, sigma_high = 2).
  "hybrid-samarth-dog": "",
  // Under the Derek + Nutmeg hybrid (sigma_low = 9, sigma_high = 4).
  "hybrid-derek-nutmeg": "",

  // ===== 2.3 Gaussian and Laplacian Stacks =====
  // What stacks are and how they differ from pyramids (no downsampling).
  "stacks-intro": "Gaussian and Laplacian stacks are like pyramids in that they recursively apply an operator, but we don't downscale the image at each step. Instead we project each image on top of each other.",
  // Under the apple and orange Gaussian / Laplacian stacks.
  "stacks-levels": "",
  // Under the Figure 3.42 recreation.
  "stacks-fig342": "",

  // ===== 2.4 Multiresolution Blending =====
  // How the blend works (mask Gaussian stack, per-level combination, collapse).
  "blend-intro": "",
  // Under the towel blend (vertical seam, 7 levels).
  "blend-towel": "",
  // Under the golden face on tabby blend (irregular circular mask).
  "blend-faces": "",
  // Under the Laplacian-level figure of your favorite blend.
  "blend-levels": "",

  // ===== What I Learned =====
  // "Tell us about the most important thing you learned from this project."
  learned: "I learned from this project that simple techinques with hand-created kernels and some manual fine-tuning can achieve somewhat remarkable results. I think understanding these techniques will be important to have a strong intuition about future, more complex methods, and help me understand when a simple approach is effective!"
};
