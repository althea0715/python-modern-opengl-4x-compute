# Texture

## Overview

Use texture objects using modern OpenGL 4.5+ DSA.

This section emphasizes the Immutable Storage concept and the rational choice of image libraries in a Python-centric engineering workflow.

---

## Differences from C++


### 1. Third Party Image libary

- In C++:
  - Commonly uses stb_image.h. It is a lightweight, single-header C library.

- In Python:
  - Dependency Backbone: We choose Pillow because it is the actual backbone for OpenCV, Matplotlib, and Scikit-image. Using it directly minimizes overhead and dependency bloat.
  - Pillow provides predictable RGBA byte layout and integrates cleanly with NumPy-based workflows

###  2. Using DSA

- In traditional OpenGL (C++ tutorials):
  - Uses a bind-based workflow (glGenTextures, glBindTexture, glTexImage2D)

- In this project:
  - Uses DSA functions (glCreateTextures, glTextureStorage2D, glTextureSubImage2D)
  - Objects are created and modified without binding

---

## Notes

- Install dependencies:
  - `pip install pillow`

- We need to be used to pillow for texture on OpenGL.

---

## Implementation

See code:

```
src/01_getting_started/04_texture/01_textures.py
src/01_getting_started/04_texture/02_textures_combined.py
```