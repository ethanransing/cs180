// Hand-written per-section descriptions for this project page. Edit the
// strings below — script.js drops each one (as HTML) into its matching
// .section-desc[data-key] element. Multi-paragraph entries should use a
// <div class="section-desc"> in index.html and wrap each paragraph in <p>.
// Empty strings are hidden on the page, so unwritten sections don't show.
//
// The comment above each key says what the project spec asks that section to
// cover, and which figures it sits under.
window.PROJECT_CONTENT = {
  // Short intro to the project as a whole (pretrained PixNerd flow model, the
  // x_t = (1 - t)·eps + t·x_1 convention: t = 0 is noise, t = 1 is a clean image).
  overview: "In this project, we explore flow models, which learn a velocity field that gradually transports Gaussian noise into clean images. In Part A, we use a large pretrained text-to-image flow model (PixNerd) to denoise, generate, and edit images, and make some optical illusions along the way. In Part B, we build and train our own flow matching model from scratch on MNIST.",

  // ===== 1.1 Constructing Noisy Training Inputs =====
  // Above the interpolate() code: the linear flow-matching path and what t means.
  "interpolate-intro": "",
  // Under the original + t = 0.25 / 0.50 / 0.75 strip: what changes as t grows.
  "interpolate-results": "",

  // ===== 1.2 Classical Denoising =====
  // How the baseline works: rescale x/t, then Gaussian blur; sigma swept over
  // 1, 2, 4, 8, 16 and picked by lowest MSE to the clean image.
  "blur-intro": "",
  // Under the three noisy / blurred pairs: how well blurring does at each t,
  // and which sigma won.
  "blur-results": "",

  // ===== 1.3 One-Step Denoising =====
  // Above the code: x̂_1 = x_t + (1 − t)·v_θ(x_t, t, c), with "a high quality photo".
  "one-step-intro": "",
  // Under the three original / noisy / estimate rows: quality at each t.
  "one-step-results": "",

  // ===== 1.4 Visualizing Velocity =====
  // Above the code: predicted update (1 − t)v̂ vs. ground truth x_1 − x_t, and
  // the per-pixel RGB RMS error map.
  "velocity-intro": "",
  // Under the three t rows: where the prediction disagrees with the ground
  // truth, and how the error changes with t.
  "velocity-results": "",

  // ===== 1.5 Iterative Denoising with Euler Sampling =====
  // Above the code: x_{t+h} = x_t + h·v(x_t, t), recomputing velocity each step,
  // shortening the final step to land on t = 1.
  "euler-intro": "",
  // Under the trajectory from t = 0.50 (h = 0.02, 25 updates).
  "euler-trajectory": "",
  // Under original / blur / one step / Euler on the same input: compare all three.
  "euler-comparison": "",

  // ===== 1.6 Generating Images from Noise =====
  // How sampling from pure noise works (t_start = 0, 50 updates).
  "sampling-intro": "",
  // Under the 5 samples (seeds 180–184): what you observe, e.g. subject bias in
  // the generic prompt.
  "sampling-results": "When we sample images from pure noise, we get human-like outputs in all instances. This suggests that human faces may be overrepresented in the training dataset.",

  // ===== 2.1 Classifier-Free Guidance =====
  // Above the code: v_cfg = v_c + w(v_c − v_u), empty-string null condition, w = 7.
  "cfg-intro": "",
  // Under the CFG samples and the 1.6 samples: compare the two with the same seeds.
  "cfg-results": "Classifier-free guidance gets us results that are not all faces. It also has more saturated and vibrant coloring.",

  // ===== 3.1 Image-to-Image Editing =====
  // Above the code: noise the image to t_start, then integrate to 1 with CFG.
  // How t_start trades off fidelity vs. freedom.
  "edit-intro": "",
  // Under the Campanile edits.
  "edit-campanile": "",
  // Under my image 1 edits (IMG_6976).
  "edit-mine1": "At the smallest starting times the model barely uses the original and invents unrelated scenes (a street, a painted horse statue), but by t = 0.25 the cup is back. Interestingly, the handwritten sticker is one of the last things to come back correctly, which suggests that fine handwriting is hard for the model to reconstruct.",
  // Under my image 2 edits (IMG_8637).
  "edit-mine2": "This is my dog! The low starting times wander far away, even into a colorful cartoon style at t = 0.04 and 0.06, but his white fur and pose come back as early as t = 0.14, earlier than for the matcha drink.",
  // Under the web image edits (seal2.jpeg).
  "edit-web": "Below t = 0.10 the model only keeps the blue and white color layout and turns it into product-style shots of objects. At t = 0.14 it turns the seal into a human face, which lines up with the bias toward people that we saw in 1.6!",
  // Under the hand-drawn edits (seal.png, crabeaterseal.png).
  "edit-drawings": "Since the prompt asks for a photo, the model tends to read the flat drawings as photographed objects like paper, a tablet, or a box at the low starting times. By t = 0.50 both drawings come back almost unchanged, so the model stays faithful to the cartoon style once enough of the original is kept.",

  // ===== 3.2 Text-Guided Image Editing =====
  // Same procedure as 3.1 but with your own prompt in place of "a high quality photo".
  "text-edit-intro": "",
  // Under the Campanile + "a photograph of a dog".
  "text-edit-campanile": "",
  // Under my image 1 + "a realistic photo of a spotted seal".
  "text-edit-mine1": "",
  // Under my image 2 + "a cartoon drawing of a crabeater seal".
  "text-edit-mine2": "",

  // ===== 3.3 Visual Anagrams =====
  // Above the code: average v_cfg(x, t, c_a) with F(v_cfg(F(x), t, c_b)), F = 180° rotation.
  "anagram-intro": "",
  // Under "a rocky mountain" / "a group of seals": prompts and what you observe.
  "anagram-0": "",
  // Under "a ferocious bear" / "a happy dog".
  "anagram-1": "",

  // ===== 3.4 Hybrid Images =====
  // Above the code: lowpass(v_a) + v_b − lowpass(v_b) each Euler step
  // (Gaussian, kernel 265, sigma 16 at 512×512).
  "hybrid-intro": "",
  // Under the mountain / seals hybrid at full size and 64×64.
  "hybrid-0": "",
  // Under the bear / dog hybrid at full size and 64×64.
  "hybrid-1": "",

  // =====================================================
  // ===== Part B: Flow Matching from Scratch =====
  // =====================================================

  // Under the Part B heading: training your own UNet on MNIST, first as a
  // one-step denoiser, then as a flow matching model.
  "b-intro": "In Part B, we train our own UNet on MNIST digits. We start with a single-step denoiser trained with an L2 loss, then extend it into a flow matching model that predicts velocity and generates digits from pure noise, first conditioned only on time and then on the digit class with classifier-free guidance.",

  // ===== B 1.1 Implementing the UNet =====
  // Above the code: the architecture (ConvBlock / DownBlock / UpBlock, skip
  // connections, Flatten / Unflatten bottleneck).
  "b-unet": "",

  // ===== B 1.2 Using the UNet to Train a Denoiser =====
  // The noising process z = x + σε and the L2 denoising objective.
  "b-noising-intro": "",
  // Under the σ = 0.0 … 1.0 strip.
  "b-noising-results": "",
  // 1.2.1, above the loss curve: training setup (σ = 0.5, D = 128, Adam 1e-4,
  // batch 256, 5 epochs).
  "b-denoiser-training": "",
  // Under the epoch 1 / epoch 5 test results.
  "b-denoiser-results": "",
  // 1.2.2, under the OOD figure: how the σ = 0.5 model does at other noise levels.
  "b-ood": "",
  // 1.2.3, above the loss curve: training with pure noise as input.
  "b-pure-noise-intro": "",
  // 1.2.3, under the epoch 1 / 5 outputs (spec asks for this): what patterns
  // appear, how they relate to the digits 0–9, and why (MSE-optimal prediction
  // is a centroid of the training data).
  "b-pure-noise-results": "The pure-noise outputs are blurry shapes rather than distinct digits because it is an average of the training images. The highest intensity is at the center where all digits have pixels. Since the noise is independent of the target digit, it provides no information about which digit to reconstruct, so to optimize MSE our network predicts the mean.",

  // ===== B 2.1 Adding Time Conditioning =====
  // Above the code: how t enters the UNet (FCBlocks scaling the unflatten and
  // up1 outputs), and the flow matching objective (target velocity x_1 − x_0).
  "b-time-cond": "",

  // ===== B 2.2 Training the Time-Conditioned UNet =====
  // Under the loss curve.
  "b-time-training": "",

  // ===== B 2.3 Sampling from the Time-Conditioned UNet =====
  // Above the code: Euler sampling from t = 0 to 1.
  "b-time-sampling-intro": "",
  // Under the epoch 1 / 5 / 10 samples: how quality improves.
  "b-time-sampling-results": "",

  // ===== B 2.4 Adding Class-Conditioning =====
  // Above the code: one-hot class vector, 10% class dropout (p_uncond = 0.1)
  // so the model also learns the unconditional velocity.
  "b-class-cond": "",

  // ===== B 2.5 Training the Class-Conditioned UNet =====
  // Under the loss curves (scheduled vs. constant learning rate).
  "b-class-training": "",

  // ===== B 2.6 Sampling from the Class-Conditioned UNet =====
  // Above the code: CFG with v_u + γ(v_c − v_u), γ = 5.
  "b-class-sampling-intro": "",
  // Under the epoch 1 / 5 / 10 grids.
  "b-class-sampling-results": "",
  // Under the no-scheduler grid (spec asks for this): what you changed to keep
  // performance without the exponential scheduler.
  "b-no-scheduler": "To compensate for the loss of the scheduler, I reduced LR to 0.003. The final samples are visually indistinct, and interestingly the static LR seemed to not affect the time of convergence in the loss curve.",

  // ===== What I Learned =====
  learned: "I learned that flow models allow us to iteratively go from arbitray pure noise to our data distribution (as opposed to a one-step network), and I learned of non-obvious applications in image editing to optical illusions. Training a flow matching model from scratch on MNIST also gave me a much better intuition for what the huge pretrained model in Part A is doing under the hood, like why guidance and the starting time have such a big effect on the results!"
};
