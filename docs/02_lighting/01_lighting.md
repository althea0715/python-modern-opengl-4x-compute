# Lighting

## Overview

Most lighting chapters are shader-focused and have minimal differences from the original LearnOpenGL C++ implementation.

The primary logic is implemented in GLSL shaders rather than OpenGL API calls.

---

## Differences from C++

### 1. Almost Same

- Most rendering logic is identical to the original LearnOpenGL examples.
- GLSL shader code can generally be ported directly from C++ examples.
- The Python-side OpenGL code remains mostly unchanged.

---

## Notes

- Nothing.

---

## Implementation

See code:

- src/02_lighting/01_colors/01_colors.py
- src/02_lighting/02_basic_lighting/01_basic_lighting_diffuse.py
- src/02_lighting/02_basic_lighting/02_basic_lighting_specular.py
- src/02_lighting/03_materials/01_materials.py
- src/02_lighting/04_lighting_maps/01_lighting_maps_diffuse.py
- src/02_lighting/04_lighting_maps/02_lighting_maps_specular.py
- src/02_lighting/05_light_casters/01_light_casters_directional.py
- src/02_lighting/05_light_casters/02_light_casters_point.py
- src/02_lighting/05_light_casters/03_light_casters_spot.py
- src/02_lighting/05_light_casters/04_light_casters_spot_soft.py
- src/02_lighting/06_multiple_lights/01_multiple_lights.py
