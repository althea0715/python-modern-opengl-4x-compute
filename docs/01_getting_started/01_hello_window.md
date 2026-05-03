# Hello Window

## Overview

Create a window and initialize the OpenGL context in Python.

This section focuses on how the setup differs from a typical C++ OpenGL workflow.

---

## Differences from C++

### 1. No GLAD required

- In C++:
  - Requires GLAD / GLEW for function loading

- In Python:
  - PyOpenGL already provides bindings for OpenGL 3.3+

### 2. No forward declaration (like C++)

- In C++:
  - Functions and variables can be declared before definition
  - This is required due to compile-time type checking

- In Python:
  - No separate declaration phase
  - Functions must be defined before they are used at runtime

---

## Notes

- Install dependencies:
  - `pip install glfw PyOpenGL PyOpenGL_accelerate`

- `moderngl` is not equivalent to C++ OpenGL (different abstraction)

- Initialization order still matters (same as C++)

- We intentionally avoid "pythonic" style  
  - to keep the structure similar to C++  
  - e.g. `glfw.init()` → explicit-style usage

---

## Implementation

See code:

```
src/01_getting_started/01_hello_window/01_hello_window.py
src/01_getting_started/01_hello_window/02_hello_window_clear.py
```