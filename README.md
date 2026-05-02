# python-modern-opengl-4x-compute

Modern OpenGL implemented in Python, extending beyond rendering into GPU computing.

> This project follows LearnOpenGL (OpenGL 3.3 core)
> and extends it to OpenGL 4.3+ features for compute-oriented workflows.

---

## Motivation

As a data scientist, most of my work focuses on optimizing models based on data.
In many cases, time-dependent simulation and visualization are not part of the workflow.

However, while exploring numerical methods involving discretization and mesh-based approaches,
I found myself needing to simulate and visualize data evolving over time.
This naturally leads to GPU-based computation and real-time rendering.

There are several choices for this:

- OpenGL
- DirectX
- Vulkan
- WebGPU

Although DirectX would be the natural choice on Windows,
I wanted a cross-platform solution. That led me to OpenGL.

After studying OpenGL through LearnOpenGL, I gained a solid understanding of the graphics pipeline.
The next step would typically be Vulkan, but Vulkan introduces significant complexity and overhead.

For someone already familiar with GPU computation:

- CUDA exists
- Python ecosystems like NumPy, CuPy, and PyTorch already solve many problems
- C++ is often only used for performance-critical bottlenecks

So the question becomes:

Do we really need Vulkan for GPU computation?

---

## Why OpenGL (4.3+)?

OpenGL 4.3 introduced features that are highly relevant for GPU computing:

- Compute Shader
- SSBO (structured data on GPU)
- Parallel execution on the GPU

However, most "modern OpenGL" tutorials focus only on OpenGL 3.3 (rendering pipeline).
Resources covering OpenGL 4.3+ from a compute perspective are surprisingly limited.

---

## Why this repository?

Most OpenGL tutorials focus on rendering.

This project focuses on:

* Using the GPU as a computation device
* Compute shader–based parallel processing
* Designing CPU ↔ GPU data pipelines
* Practical use of modern OpenGL features (4.3+)

===============================================================================================




---

## Features

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
git clone https://github.com/althea0715/python-modern-opengl-4x-compute.git
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
