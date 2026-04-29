# Chaotic Image Cryptography

A mathematical cybersecurity command-line tool that generates highly secure, pseudo-random encryption keys by discovering unique 3D Strange Attractors in real-time. 

Instead of relying on standard pseudo-random number generators (PRNGs), this engine mines discrete trigonometric mathematical universes, checking for chaotic viability, and uses that chaos to securely encrypt image data.

### 🌌 The Chaos Engine (Trigonometric Attractor)
![Trigonometric Strange Attractor](assets/Screenshot%202026-04-29%20115339.png)
*An example of a mined discrete 3D trigonometric strange attractor used to generate the cryptographic key sequence.*

### Visual Demonstration
![Original to Static](assets/Screenshot%202026-04-28%20125501.png)

![Static to Restored](assets/Screenshot%202026-04-28%20125536.png)

---

## Features
* **Automated Chaos Mining:** Calculates the Largest Lyapunov Exponent (LLE) of mined trigonometric functions to guarantee generated keys are strictly chaotic (λ > 0).
* **C-Level Speeds:** Mathematical engines are JIT-compiled using LLVM (`Numba`) to process millions of chaotic iterations in seconds.
* **Zero-Loss Decryption:** Securely scrambles and restores RGB/A data without a single pixel of degradation.
* **Full CLI Support:** Built with `argparse` for seamless terminal operations.

## Installation

1. Clone this repository to your local machine.
2. Install the required data science and mathematical libraries:
```bash
pip install numpy numba matplotlib
```

## Usage

This tool is operated entirely from the command line.

**View the Help Menu:**
```bash
python main.py --help
```

**Encrypt an Image:**
This automatically mines a new 3D attractor, saves the parameters to `master.key`, and outputs an encrypted image.
```bash
python main.py -e your_image.png
```

**Decrypt an Image:**
This reads the mathematical parameters from your key file and perfectly restores the original image data.
```bash
python main.py -d ENCRYPTED_your_image.png
```

**Using Custom Keys:**
You can specify custom key files using the `-k` flag to manage multiple encrypted files safely:
```bash
python main.py -e top_secret.png -k project_omega.key
```

## Under the Hood

The cryptography relies on two primary phases:
1.  **Confusion (Spatial Shuffling):** The algorithm generates an array of chaotic X coordinates equal to the number of pixels. By sorting this array and tracking the index movements, the original image pixels are completely scattered across the canvas.
2.  **Diffusion (Color Destruction):** The algorithm takes the chaotic Y coordinates, converts the decimal noise into 8-bit integers, and applies a Bitwise XOR (`^`) operation against the image's color channels. This securely overwrites the RGB data.

## Project Structure

```text
├── main.py              # CLI entry point and argument parsing
├── chaos_engine.py      # Numba-compiled math and Lyapunov calculations
├── cryptographer.py     # Image flattening, XOR logic, and reassembly
├── assets/              # Demonstration screenshots and README images
├── research/            # Original Jupyter Notebooks used for prototyping math
├── .gitignore           # Keeps keys and generated images out of version control
└── README.md
