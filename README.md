# python-modern-opengl-4x-compute

Modern OpenGL implemented in Python, extending beyond rendering into GPU computing.

> This project follows LearnOpenGL (OpenGL 3.3 core)
> and extends it to OpenGL 4.3+ features for compute-oriented workflows.

---

## Why this repository?

Most OpenGL tutorials focus on rendering.

This project focuses on:

* Using the GPU as a computation device
* Compute shader–based parallel processing
* Designing CPU ↔ GPU data pipelines
* Practical use of modern OpenGL features (4.3+)

---

## Features

* OpenGL Core (3.3)
* Compute Shader (4.3+)
* SSBO (Shader Storage Buffer Object)
* Direct State Access (DSA)
* GPU synchronization and memory model
* GPU-driven data pipelines

---

## Roadmap

### Part 1 — Core OpenGL (3.3)

* Window and Context
* First Triangle
* Shader System
* Transformations
* Coordinate Systems
* Lighting
* Model Loading

### Part 2 — Modern Extensions (4.3+)

* Compute Shader (dispatch, work groups)
* SSBO (structured and large data handling)
* DSA (object-oriented API usage)
* Synchronization (barriers, fences)
* Memory model

### Part 3 — GPU Applications

* GPU Particle System
* Image Processing (convolution, blur)
* Parallel Simulation
* Data-oriented GPU design

---

## Examples

* GPU Particle System
* Image Convolution (Compute Shader)
* Parallel Simulation

<!--
TODO: Add GIFs here

Example:
![particle](assets/gifs/particle.gif)
-->

---

## Project Structure

```
src/        # source code (organized by chapter)
docs/       # documentation (book-style)
assets/     # images and results
```

Example:

```
src/
 ├── 01_getting_started/
 ├── 02_lighting/
 ├── 03_model_loading/
 ├── 04_advanced/
 ├── 05_compute/
 └── 06_applications/

docs/
 ├── index.md
 ├── 01_getting_started/
 ├── 05_compute/
 └── 06_applications/
```

---

## Getting Started

```bash
git clone https://github.com/<your-username>/python-modern-opengl-4x-compute
cd python-modern-opengl-4x-compute

pip install -r requirements.txt

python src/01_getting_started/main.py
```

---

## Documentation

Full documentation is available in:

```
docs/index.md
```

(Planned: GitHub Pages)

---

## Tech Stack

* Python
* OpenGL
* PyOpenGL / moderngl
* GLFW
* numpy

---

## Related Projects

This repository is part of a broader GPU learning series:

* Ray Tracing (Python / GPU)
* FDTD Simulation (GPU)

---

## Roadmap (Future Work)

* Persistent Mapping optimization
* Advanced GPU synchronization patterns
* GPU-based physics simulation
* Optional C++ backend for performance-critical components

---

## Summary

This is not just an OpenGL tutorial.

It is a step toward GPU computing.
