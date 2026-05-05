# Hello Triangle

## Overview

Use VAO, VBO, and a basic shader in Python.

This section uses Direct State Access (DSA) instead of the traditional bind-based workflow.

---

## Differences from C++

### 1. Using ctypes for object IDs

- In C++:
  - OpenGL object IDs are stored in integer variables (e.g. GLuint)

- In Python:
  - Uses `ctypes` to create compatible integer buffers for OpenGL calls
  - Required when passing references to OpenGL functions (e.g. glCreateBuffers, glCreateVertexArrays)


### 2. Memory Management (NumPy vs C-Struct)

- In C++: 
  - Data is defined via structs or raw arrays (memory is always contiguous).

- In Python (with NumPy):
  - We use `numpy.ndarray` with `dtype=np.float32` to match OpenGL's expected 4-byte floats.
  - `vertices.nbytes` is used to get the total size in bytes (equivalent to `sizeof(vertices)`).
  - Precaution: Ensure the array is C-contiguous (default for new arrays) before passing to OpenGL.

### 3. Using DSA (Direct State Access)

- In traditional OpenGL (C++ tutorials):
  - Uses a bind-based workflow (glBindBuffer, glBindVertexArray)

- In this project:
  - Uses DSA functions (glCreateBuffers, glCreateVertexArrays)
  - Objects are created and modified without binding

---

## Notes

- Install dependencies:
  - `pip install numpy`

- There are multiple ways to handle OpenGL object IDs in Python  
  but `ctypes` provides a simple and explicit approach

- DSA requires OpenGL 4.5+ (or extension support)

---

## Implementation

See code:

```
src/01_getting_started/02_hello_triangle/01_hello_triangle.py
src/01_getting_started/02_hello_triangle/02_hello_triangle_indexed.py
```