# Camera

## Overview

This section shows how to apply camera systems using glm matrices.

The camera matrix is passed to the shader through uniform variables.

---

## Differences from C++

###  1. Almost Same

- Uses glm similarly to traditional LearnOpenGL C++ examples.
- glm syntax is very similar to GLSL matrix operations.
- Uses modern OpenGL Direct State Access (DSA) APIs.

---

## Notes

- The focus of this chapter is GLSL.

---

## Implementation

See code:

```
src/01_getting_started/07_camera/01_camera_circle.py
src/01_getting_started/07_camera/02_camera_keyboard_dt.py
src/01_getting_started/07_camera/03_camera_mouse_zoom.py
```