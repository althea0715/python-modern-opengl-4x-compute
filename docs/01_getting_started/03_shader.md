# Shader

## Overview

Use uniforms and multiple vertex attributes in shaders.

This section uses the traditional shader pipeline and introduces a basic shader class.

It also briefly checks the program pipeline (separable shader) for comparison.

---

## Differences from C++


### 1. Same shader compilation process

- In C++:
  - glCreateShader → glCompileShader → glCreateProgram → glAttachShader → glLinkProgram

- In Python:
  - Same process and API calls
  - No difference in shader compilation and linking and usage.
  - Shader behavior is identical to C++, but Python removes boilerplate around string and file handling


### 2. Program pipeline (OpenGL 4.x feature)

- In traditional OpenGL (C++ tutorials):
  - Uses a single program object (vertex + fragment linked together)

- In this project:
  - Tests separable shader pipeline
  - This is only for verification  
    (not used in the main flow, to stay compatible with LearnOpenGL-style structure)


### 3. Shader abstraction

- In C++:
  - Often implemented as a class (e.g. LearnOpenGL Shader class)

- In Python:
  - Similar abstraction can be implemented
  - Simpler due to dynamic typing

---

## Notes

- Some OpenGL APIs require `char**` for shader sources
- In Python, this may require manual conversion via ctypes (verbose)

---

## Implementation

See code:

```
src/01_getting_started/03_shader/01_shaders_uniform.py
src/01_getting_started/03_shader/02_shaders_uniform_with_pipeline.py
src/01_getting_started/03_shader/03_shaders_interpolation.py
src/01_getting_started/03_shader/04_shaders_class.py
```