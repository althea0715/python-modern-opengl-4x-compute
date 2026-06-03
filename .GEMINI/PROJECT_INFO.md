# Project Info: Python Modern OpenGL 4x Compute

## 🌟 Overview
A specialized visualization engine designed for data scientists and researchers to visualize high-performance numerical simulations in real-time using Python and Modern OpenGL.

## 🛠️ Technology Stack
- **Language**: Python 3.12+ (managed by `uv`)
- **Graphics API**: OpenGL 4.6 Core Profile
- **Core Libraries**:
  - `PyOpenGL`: OpenGL bindings for Python.
  - `glfw`: Window management and input.
  - `pyglm`: OpenGL Mathematics for Python.
  - `numpy`: High-performance numerical arrays.
  - `pyassimp`: 3D model loading via Assimp.
  - `Pillow`: Image processing for textures.

## 🎯 Purpose
- **Scientific Visualization**: Rendering mesh-based data from numerical analysis.
- **GPGPU Learning**: Exploring Compute Shaders and SSBOs for parallel processing.
- **Modern Standards Implementation**: Serving as a reference for Direct State Access (DSA) in Python.

## ⚙️ Installation & Execution
- **Environment**: Managed via `uv`.
- **Run Example**: `uv run src/03_model_loading/model_loading.py`
- **Dependencies**: Defined in `pyproject.toml`.

## 📂 Project Structure
- `src/`: Source code organized by LearnOpenGL chapters and custom modules.
- `docs/`: Concept explanations and study notes.
- `stubs/`: Type hint definitions for library compatibility.
- `sample/`: Reference C++ implementations for porting.
