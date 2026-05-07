# Transformations

## Overview

This section shows how to apply transformations using glm matrices.

The transformation matrix is passed to the shader through uniform variables.

---

## Differences from C++

###  1. Almost Same

- In traditional OpenGL (C++ tutorials):
  - Uses glm third-party library.

- In this project:
  - Uses glm third-party library.
  - NumPy can also be used for matrix calculations.
  - However, glm provides a more OpenGL-oriented API and matches GLSL conventions closely.
  - glm syntax is very similar to GLSL matrix operations.
  - glm already provides utility functions such as translation, rotation, scaling, and perspective projection.
  - Uses modern OpenGL Direct State Access (DSA) APIs.

---

## Notes

- Install dependencies:
  - `pip install pyglm`

- pyglm does not provide proper type hints, so IDE auto-completion may be limited.

---

## Implementation

See code:

```
src/01_getting_started/05_transformations/01_transformations.py
```