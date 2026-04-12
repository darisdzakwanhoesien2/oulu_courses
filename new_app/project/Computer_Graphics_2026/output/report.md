# CG_assignment1 — Report

Date: 2026-03-31

## 1. Overview
This report documents running and implementing Tasks 1–4 from "CG Programming Assignment 1". The program renders a colored tetrahedron and was extended with a continuous x-axis rotation, an Euler-angle camera (mouse look), and keyboard movement (W/A/S/D + E/R). Shader and resource path fixes were also applied to run on macOS.

## 2. Environment
- macOS (tested on MacBook Air)
- Python 3.10
- Dependencies: PyOpenGL, PyOpenGL_accelerate, PyGLM, freeglut (Homebrew)
- Project folder: new_app/project/Computer Graphics 2026/Assignment1

## 3. Files modified
- CG_assignment1.py
  - Added robust read_file (resolves relative shader paths)
  - Fixed shader program creation and attribute binding
  - Implemented calc_model() rotation using glm.rotate + time
  - Fixed buffer upload and (if needed) glDrawArrays vertex count handling
- utils/mvp_controller.py
  - Implemented calc_view_projection() to compute front/right/up from yaw/pitch
  - Implemented on_keyboard() to move camera position (W/S/A/D/E/R)
  - Hooked callbacks to update view/projection after changes
- shaders/vertex_shader.glsl and shaders/fragment_shader.glsl
  - Set to GLSL 1.20 (attribute/varying/gl_FragColor) for compatibility on macOS GL context

## 4. How each task was implemented

Task 1 — Get the scene to work (1 point)
- Ensured shader files are found by building absolute path from script directory.
- Compiled and linked shaders, bound attribute locations 0 and 1 to vertexPosition and vertexColor.
- Verified vertex and color buffers upload correctly and rendering produces the tetrahedron as in Figure 1.

Task 2 — Continuous rotation over X-axis (2 points)
- Implemented Win.calc_model() in CG_assignment1.py:
  - Compute elapsed time since program start and set angle = elapsed * speed.
  - model_matrix = glm.rotate(glm.mat4(1), angle, glm.vec3(1,0,0))
- Result: tetrahedron rotates continuously around the X axis (screenshots show several orientations).

Task 3 — Camera view matrix with Euler angles (3 points)
- Implemented in utils/mvp_controller.calc_view_projection():
  - Compute front direction from yaw & pitch:
    - front.x = cos(yaw) * cos(pitch)
    - front.y = sin(pitch)
    - front.z = sin(yaw) * cos(pitch)
  - right = normalize(cross(front, worldUp))
  - up = normalize(cross(right, front))
  - view = glm.lookAt(position, position + front, up)
  - projection = glm.perspective(fov, width/height, 0.1, 1000)
- Mouse movement updates yaw/pitch and triggers recalculation.
- Result: mouse-look camera (holding left mouse button to drag) as requested.

Task 4 — Keyboard movement (2 points)
- Implemented on_keyboard in utils/mvp_controller.py:
  - Keys (bytes): b"w" forward, b"s" back, b"a" left, b"d" right, b"e" up, b"r" down
  - Movement applied to position: position += direction * speed, etc.
  - After movement, calc_view_projection() and callback_update() are called.
- Result: free movement around scene; screenshots show different camera positions.

## 5. Shader compatibility fixes
- The machine's GL context rejected newer GLSL versions (330/430). Replaced shaders with GLSL 1.20 style:
  - vertex: attribute / varying / uniform mat4 mvp
  - fragment: varying color -> gl_FragColor
- This ensures compilation on older/compatibility contexts used by macOS GLUT.

## 6. How to run
1. cd to assignment folder:
   - cd "new_app/project/Computer Graphics 2026/Assignment1"
2. Create venv and install:
   - python3 -m venv .venv
   - source .venv/bin/activate
   - pip install --upgrade pip
   - pip install PyOpenGL PyOpenGL_accelerate PyGLM
3. Install GLUT if missing:
   - brew install freeglut
4. Run:
   - python CG_assignment1.py

If shaders fail to compile, check the shader files in shaders/ and ensure the program working directory is the same folder as the script (read_file constructs absolute path).

## 7. Screenshots / Results
- The run produced the expected tetrahedron in multiple orientations and camera positions (images attached in the working directory). Representative frames:
  - Initial scene (Task 1)
  - Rotated views (Task 2)
  - Camera-look views (Task 3)
  - Different camera positions after keyboard movement (Task 4)

(Images displayed in the UI confirm correct rendering: colored faces, smooth interpolation, rotation and camera control.)

## 8. Notes, limitations and suggestions
- Movement is currently frame-step based (per key press). For smooth movement, multiply speed by frame delta-time.
- Pitch clamping advisable to avoid gimbal lock (limit pitch to ~ +/- 89 deg).
- Optionally implement mouse sensitivity scaling and invert Y toggle.
- Additional tasks (optional): translation/scale ordering, cube model, red fragment shader, zoom via FOV, second object with own model matrix, load OBJ — all straightforward extensions.

## 9. Minimal checklist for submission
- CG_assignment1.py — implemented code + comments
- utils/mvp_controller.py — camera & input handling
- shaders/vertex_shader.glsl, shaders/fragment_shader.glsl — GLSL 1.20
- PDF report with screenshots (export this markdown to PDF including the captured images)

---