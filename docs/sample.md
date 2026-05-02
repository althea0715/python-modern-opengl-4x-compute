# Hello Window

## Overview

Create a window and initialize the OpenGL context.
This is the minimal setup required before rendering anything.

---

## Concepts

* OpenGL does not create windows → use GLFW
* A context is required to use OpenGL
* Rendering runs inside a continuous event loop

---

## Implementation

See code:

```
src/01_getting_started/01_hello_window.py
src/01_getting_started/02_hello_window_clear.py
```

Steps:

1. Initialize window system
2. Create window
3. Make context current
4. Run render loop

---

## Notes

* No context → OpenGL does not work
* No loop → window closes immediately
* Order matters when initializing
