# python-modern-opengl-4x-compute

Modern OpenGL implemented in Python, extending beyond rendering into GPU computing.

> This project follows LearnOpenGL (OpenGL 3.3 core)
> and extends it to OpenGL 4.3+ features for compute-oriented workflows.

---

## Motivation

Most data science workflows focus on optimization over static datasets.

However, when working with:

- time-evolving systems
- spatial structures (2D / 3D grids)
- continuous visualization

the problem shifts to:

> **simulation + visualization + performance**

---

## Core Idea

Use the GPU as a **numerical computation engine**, not just a rendering tool.

---

## Why OpenGL?

Vulkan offers maximum control, but comes with significant complexity.

For exploratory and research workflows, the priority is:

- fast iteration
- minimal boilerplate
- direct GPU access

OpenGL provides a practical balance:

- Compute Shader (OpenGL 4.3+)
- integrated rendering + computation
- lower setup cost than Vulkan

---

## Why Python?

This project prioritizes **iteration speed**.

Python enables:

- rapid prototyping
- seamless NumPy/CuPy integration
- flexible simulation design

> prototype fast → validate → port to C++ if needed

---

## What This Project Does

- GPU-based simulation using Compute Shaders
- grid/mesh-based numerical computation
- real-time visualization of evolving systems

Example use cases:

- finite difference methods (FDM)
- cellular automata
- particle systems
- diffusion / wave simulations

---

## Implementation Strategy

- **GLFW + PyOpenGL**  
  → direct mapping to OpenGL (C++-friendly)

- **Direct State Access (DSA)**  
  → modern, explicit resource management

- **Portability-first design**  
  → easily translatable to C++

---

## Philosophy

This is not a graphics engine.

This is about:

- treating the GPU as a **compute device**
- building **time-dependent simulations**
- bridging **data science ↔ real-time systems**