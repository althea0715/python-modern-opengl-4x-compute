# Project Guidelines

This document outlines the coding standards, communication protocols, and development workflows for the **Python Modern OpenGL 4x Compute** project.

## 🛠️ Coding Standards
- **OpenGL Version**: Target **OpenGL 4.6 (Core Profile)**. Do not use deprecated "Legacy" OpenGL functions.
- **DSA (Direct State Access)**: Mandatory for all new implementations. Use `glCreate*`, `glTextureStorage*`, and `glNamedBuffer*` instead of binding-based functions.
- **Typing**: Use Python type hints throughout. Maintain and update stubs in `stubs/` for third-party libraries.
- **Data Handling**: Use **NumPy** for all vertex and numerical data. Ensure memory layouts match C-style structs where required by OpenGL.
- **Naming**: Follow PEP 8 for Python code and `camelCase` for GLSL uniforms where it matches external samples, or as established in the project.

## 💬 Communication Protocols
- **Topic Updates**: Use `update_topic` to signal transitions between research, implementation, and testing phases.
- **Technical Rationale**: Always explain *why* a certain OpenGL pattern (like DSA) is chosen over others.
- **Error Reporting**: Provide full tracebacks and identify if an error is a Python logic issue or an OpenGL state issue.

## 🚀 Development Workflow
- **Surgical Edits**: Use the `replace` tool for targeted changes to minimize context usage.
- **Verification**: Always run `uv run <script>` to verify changes before concluding a task.
- **Documentation**: Keep `GEMINI.md` and `docs/` updated as new features are added.

## ⚠️ Constraints
- Do not modify files in `src/` without a clear directive or fix requirement.
- Never use "hidden" logic or suppress linter warnings without explicit instruction.
