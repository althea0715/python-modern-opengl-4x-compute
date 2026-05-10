# Coordinate Systems

## Overview

This section shows how to apply coordinate systems using glm matrices.

The coordinate matrix is passed to the shader through uniform variables.

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

- The focus of this chapter is GLSL.

---

## Implementation

See code:

- src/01_getting_started/06_coordinate_systems/01_coordinate_systems.py
- src/01_getting_started/06_coordinate_systems/02_coordinate_systems_depth.py
- src/01_getting_started/06_coordinate_systems/03_coordinate_systems_multiple.py
