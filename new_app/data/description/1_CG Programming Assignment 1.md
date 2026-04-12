Task references:
[page_0000.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0000.md)
[page_0001.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0001.md)
[page_0002.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0002.md)
[page_0003.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0003.md)
Explaination of each task (concise):

Get the scene to work (Task 1)
Goal: run the provided program and verify the basic scene renders (tetrahedron, shaders, window).
Steps: open and run [CG_assignment1.py](new_app/data/thesis_dataset/CG Programming Assignment 1/CG_assignment1.py) (main loop, VAO/VBO setup, shader compilation). Fix any missing file paths or library imports. Capture a screenshot of the running window.
Render the scene with rotation (Task 2)
Where to change: the model matrix builder (the notebook mentions "find the calc_model function in the Win class"). See [Win.calc_model](new_app/data/thesis_dataset/CG Programming Assignment 1/CG_assignment1.py).
What to implement: compute a model matrix that rotates continuously around the x-axis. Use glm rotation helpers and time to make it continuous:
Use time.time() (or glfw.get_time()) to get elapsed time.
Build matrix M = translate * rotate_x(elapsed * speed) * scale (if any).
Pass M to the vertex shader as the model (or model-view-projection) uniform.
Result: tetrahedron rotates about x-axis; take screenshot.
Camera view matrix using Euler angles (Task 3)
Where to change: mvp_controller.calc_view_projection.
Goal: implement camera orientation using Euler angles (yaw, pitch) and derive direction (front), right and up vectors.
Typical implementation:
front.x = cos(yaw) * cos(pitch)
front.y = sin(pitch)
front.z = sin(yaw) * cos(pitch)
right = normalize(cross(front, worldUp))
up = normalize(cross(right, front))
view = glm.lookAt(position, position + front, up)
Hook mouse movement (on left-button drag) to update yaw/pitch, recalc front/right/up, update the view. See mvp_controller.calc_view_projection for where to use these vectors.
Result: interactive camera controlled by mouse; take screenshot.
Keyboard movement (Task 4)
Where to change: implement handler in mvp_controller.on_keyboard.
Required moves: forward/backward/left/right/up/down (suggested keys: w/s/a/d/e/r). Note: key argument is bytes (not str).
Implementation approaches:
Move camera position vector along front (forward/back), along right (left/right), and along worldUp or up (up/down).
Use movement speed delta scaled by frame time.
Alternatively, manipulate a model-space position matrix if camera is implemented that way (the assignment suggests manipulating self.position with matrices from calc_view_projection).
Result: free movement in scene; take screenshot.
Additional tasks (optional)
(a) Translation and scaling (correct order)
Important: transform order matters. To scale in object-local coords then rotate then translate, compose M = T * R * S (applied right-to-left: scale → rotate → translate).
(b) Change object to a cube
Replace tetrahedron vertex data with cube vertices + indices; update VBO/EBO and attribute setup.
(c) Set color to red using fragment shader
Modify the fragment shader to output vec4(1.0, 0.0, 0.0, 1.0) or multiply existing color by vec3(1,0,0).
(d) Add zooming to keyboard inputs
Change camera FOV in the projection matrix or move camera along front vector on zoom keys.
(e) Implement a second object with its own model matrix
Create second VAO/VBO and compute a separate model matrix for it; render both objects with their own model uniforms.
(f) Load an object file
Use a loader (e.g., pywavefront, tinyobjloader). Parse vertices/normals/uvs, fill VBO/IBO, set attributes.
Quick pointers / where to edit in your workspace

Main program / model calc: [CG_assignment1.py](new_app/data/thesis_dataset/CG Programming Assignment 1/CG_assignment1.py)
Camera & input controller: mvp_controller.py
Window helper (glut wrapper): glut_window.py
Assignment pages / spec (already open): [page_0000.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0000.md), [page_0001.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0001.md), [page_0002.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0002.md), [page_0003.md](new_app/data/thesis_dataset/CG Programming Assignment 1_pdf/pages/page_0003.md)