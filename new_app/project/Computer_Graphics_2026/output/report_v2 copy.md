CG_assignment1 — Narrative Report
Date: 2026-03-31

Overview
This project demonstrates the implementation and testing of Tasks 1–4 from the Computer Graphics Programming Assignment 1. The delivered program renders a colored tetrahedron and was extended to include a continuous rotation around the X axis, an Euler-angle based camera controlled with the mouse, and keyboard movement for free navigation. Small compatibility fixes were applied so the program runs on a macOS OpenGL context.

Environment and setup
All development and testing were performed on a MacBook Air running Python 3.10. The runtime requires PyOpenGL, PyOpenGL_accelerate and PyGLM, and the system FreeGLUT library (installable via Homebrew). The working project folder is new_app/project/Computer Graphics 2026/Assignment1.

What I changed and why (narrative)
When first running the provided code, shader lookup and GLSL version mismatches prevented the scene from compiling. To make the program robust across environments, the shader loader was modified to build absolute paths from the script directory and the shaders were adapted to GLSL 1.20 (attribute/varying/gl_FragColor) so they compile on the compatibility GL profile commonly provided on macOS. The program now reliably compiles, links, and uses the vertex and color buffers to draw the tetrahedron.

Task 1 — get the scene to run
The primary goal was to ensure the original scene (tetrahedron with interpolated vertex colors) displays correctly. After fixing the shader path resolution and shader compatibility, the vertex and color buffers were uploaded and the program produced the expected colored tetrahedron. This established a stable baseline for the remaining tasks.

Task 2 — continuous X-axis rotation
To animate the object, the model matrix builder was modified to rotate the tetrahedron around its local X axis. The implementation uses glm.rotate and the elapsed program time as the rotation angle source, producing a smooth, continuous rotation. The screenshots captured at different times show the tetrahedron in various orientations and confirm the rotation works as intended.

Task 3 — Euler-angle camera (mouse look)
The camera logic was implemented using Euler angles (yaw and pitch) to derive the camera’s forward (direction), right, and up vectors. These vectors feed glm.lookAt to produce the view matrix. Mouse movement updates yaw and pitch, the direction vector is recomputed, and the view matrix updates accordingly. Holding and dragging the mouse provides intuitive mouse-look control and the rendered frames demonstrate different viewing angles obtained with the mouse.

Task 4 — keyboard movement
Keyboard controls were added for forward, backward, left, right, up and down movement (W/S/A/D/E/R, keys handled as bytes). Movement updates the camera position along the computed direction, right, and world-up vectors; after each change the view matrix and projection are recalculated and the scene refreshed. These controls allow free navigation around the rotating tetrahedron and the screenshots show the effect of different camera positions.

Results and observations
With the compatibility fixes and the implemented features, the application renders a smoothly shaded, rotating tetrahedron and supports both mouse-look and keyboard navigation. The three representative screenshots included with this report illustrate the rotating object and different camera positions achieved through user input. Performance was satisfactory on the test machine.

Screenshots
[[Screenshot 2026-03-31 at 19.55.14]]
Screenshot 1 — front-left perspective showing the tetrahedron rotated about its local X axis. Vertex colors are interpolated across faces; this view highlights the green/ magenta gradient on the top and side faces.

[[Screenshot 2026-03-31 at 19.55.40]]
Screenshot 2 — lower-right viewpoint showing the underside of the tetrahedron and stronger color blending along the lower edges. The camera has been moved down and right to emphasize depth and shading.

[[Screenshot 2026-03-31 at 19.55.58]]
Screenshot 3 — rotated pose with the camera moved to the right and slightly above; this angle shows the object silhouette and color interpolation across three