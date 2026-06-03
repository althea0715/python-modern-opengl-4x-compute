# Python Modern OpenGL 4x Compute

This project is a high-performance visualization engine designed to bridge the gap between **Data Science/Optimization** and **Real-time 3D Graphics**.

## 🎯 Project Mission
Created by a data scientist for engineering and research, this project aims to visualize complex numerical simulations (e.g., numerical differentiation, mesh-based physics) in real-time. We bypass the complexity of C++ build systems in favor of **Python's agility**, while leveraging **OpenGL 4.6 (Core Profile)** and **Compute Shaders** for GPGPU-accelerated performance.

## 🏗️ Architectural Pillars
1. **Modernity**: Exclusively uses **OpenGL 4.6** and **Direct State Access (DSA)** to eliminate global state management.
2. **Performance**: Focuses on **Compute Shaders (4.3+)** for parallel numerical processing and visualization.
3. **Agility**: Python-first development with **NumPy** integration, using C++/CUDA only where absolute bottlenecks exist.
4. **Type Safety**: Custom type stubs for libraries like `pyassimp` to ensure robust development in IDEs.

## 🚀 Development Roadmap

### Phase 1: High-Fidelity Rendering (Current)
- [x] **Model Loading**: Robust Assimp integration with texture caching.
- [x] **DSA Refactoring**: Modernize buffer and texture management.
- [ ] **Advanced Lighting**: PBR-ready lighting maps (Normal, Specular, Metallic/Roughness).
- [ ] **Dynamic Camera**: Smooth interaction for inspecting complex meshes.

### Phase 2: The GPGPU Bridge (Priority)
- [ ] **SSBO Integration**: Linking NumPy arrays directly to Shader Storage Buffer Objects.
- [ ] **Compute Shader Basics**: Implementing first-pass GPGPU calculations (e.g., particle displacement).
- [ ] **Real-time Plotting**: Visualizing 3D field data and gradient flows.

### Phase 3: Advanced Optimization & Simulation
- [ ] **Instanced Rendering**: High-speed visualization of large-scale point clouds or repeated meshes.
- [ ] **Compute-Driven Culling**: Moving frustum and occlusion culling to the GPU.
- [ ] **Temporal Analysis**: Efficient handling of time-series simulation data.

## 📝 Guidelines
- Detailed guidelines and project information are in the `.GEMINI` folder.
- [**Project Guidelines**](.GEMINI/GUIDELINES.md): Rules for communication and constraints.
- [**Project Info**](.GEMINI/PROJECT_INFO.md): Overview and technologies.

---
*Last Updated: 2026-06-03*
