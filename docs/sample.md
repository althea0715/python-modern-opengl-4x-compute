# 1.1 Hello Window

## Overview

In this section, we create the first OpenGL window and initialize the rendering context.

This is the minimal setup required before any rendering can happen.

---

## Why this matters

Before drawing anything with OpenGL, we need:

* A window to display output
* An OpenGL context
* An event loop to keep the application running

Without this, OpenGL functions cannot be used.

---

## Key Concepts

### Window and Context

OpenGL itself does not create windows.
We rely on libraries such as GLFW to:

* Create a window
* Initialize an OpenGL context

The context is essential because it stores all OpenGL state.

---

### Event Loop

Rendering applications must run continuously.

A typical loop:

* Process input
* Render frame
* Swap buffers

This loop continues until the window is closed.

---

## Implementation

See code:

```
src/01_getting_started/01_hello_window.py
```

### Main Steps

1. Initialize the windowing system
2. Create a window
3. Make the OpenGL context current
4. Enter the render loop
5. Handle input and window close

---

## Common Pitfalls

### 1. No OpenGL Context

If the context is not created properly:

* OpenGL calls will fail silently
* Nothing will be rendered

---

### 2. Missing Event Loop

If there is no loop:

* The window appears and immediately closes

---

### 3. Incorrect Initialization Order

Order matters:

* Create window → Make context current → Call OpenGL functions

---

## Summary

* OpenGL requires a valid context
* A windowing library is required (e.g., GLFW)
* Rendering happens inside a continuous loop

This forms the foundation for all upcoming examples.
