from OpenGL.GL import *
from OpenGL.GL import shaders, GLfloat
import os
import glm
import glob
from utils.obj_loader import ObjLoader
from utils.texture_loader import TextureLoader
from utils.glut_window import GlutWindow
from utils.mvp_controller import MVPController


# Provide small fallback shaders so the program can run even if resource files are missing.
_default_vertex_shader = """#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texcoord;
uniform mat4 mvp;
out vec2 v_texcoord;
void main() {
    gl_Position = mvp * vec4(position, 1.0);
    v_texcoord = texcoord;
}
"""

_default_fragment_shader = """#version 330 core
in vec2 v_texcoord;
out vec4 fragColor;
uniform sampler2D texture_sampler;
void main() {
    fragColor = texture(texture_sampler, v_texcoord);
}
"""

_default_vertex_shader_120 = """#version 120
attribute vec3 vertex_position;
attribute vec2 vertex_uv;
uniform mat4 mvp;
varying vec2 uv;
void main() {
    gl_Position = mvp * vec4(vertex_position, 1.0);
    uv = vertex_uv;
}
"""

_default_fragment_shader_120 = """#version 120
varying vec2 uv;
uniform sampler2D texture_sampler;
void main() {
    gl_FragColor = texture2D(texture_sampler, uv);
}
"""


def read_file(file_path: str, fallback: str = None) -> str:
        """Reads a text file given a path and returns it as a string.
        Tries the given path, then tries relative to this script, otherwise returns fallback (if provided)."""
        # try as given
        try:
                with open(file_path, mode="r") as f:
                        return f.read()
        except FileNotFoundError:
                pass

        # try relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(base_dir, file_path)
        try:
                with open(candidate, mode="r") as f:
                        return f.read()
        except FileNotFoundError:
                pass

        # try resources subfolder next to this script
        candidate2 = os.path.join(base_dir, "resources", os.path.basename(file_path))
        try:
                with open(candidate2, mode="r") as f:
                        return f.read()
        except FileNotFoundError:
                pass

        # fallback to built-in default if provided
        if fallback is not None:
                return fallback

        raise FileNotFoundError(f"Could not find shader file: {file_path}")


# Vertex positions for a unit cube centered at origin (12 triangles -> 36 vertices)
vertex_buffer_data = [
    # Front
    -1.0, -1.0,  1.0,
     1.0, -1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0, -1.0,  1.0,
    # Right
     1.0, -1.0,  1.0,
     1.0, -1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0,  1.0,
     1.0, -1.0,  1.0,
    # Bottom
    -1.0, -1.0,  1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0,  1.0,
     1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
    -1.0, -1.0, -1.0,
    # Top
    -1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0,  1.0,
    # Left
    -1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0,  1.0, -1.0,
    -1.0, -1.0, -1.0,
    # Back
     1.0, -1.0, -1.0,
    -1.0, -1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0, -1.0, -1.0,
]


# UV coordinates mapped to a 3x2 UV template (36 * 2 floats)
u0 = 0.0
u1 = 1.0 / 3.0
u2 = 2.0 / 3.0
u3 = 1.0

v0 = 0.0
v1_ = 1.0 / 3.0
v2_ = 2.0 / 3.0
v3_ = 1.0

uv_buffer_data = [
    # Front (tile col0,row2)
    u0, v2_, u1, v2_, u1, v3_,
    u1, v3_, u0, v3_, u0, v2_,
    # Right (col1,row2)
    u1, v2_, u2, v2_, u2, v3_,
    u2, v3_, u1, v3_, u1, v2_,
    # Bottom (col2,row2)
    u2, v2_, u3, v2_, u3, v3_,
    u3, v2_, u2, v2_, u2, v3_,
    # Top (col0,row1)
    u0, v1_, u1, v1_, u1, v2_,
    u1, v2_, u0, v2_, u0, v1_,
    # Left (col1,row1)
    u1, v1_, u2, v1_, u2, v2_,
    u2, v2_, u1, v2_, u1, v1_,
    # Back (col2,row1)
    u2, v1_, u3, v1_, u3, v2_,
    u3, v2_, u2, v2_, u2, v1_
]


class GLContext:
        """Used for storing context data in the main window."""
        pass


class Win(GlutWindow):
        def __init__(self, width: int = 800, height: int = 480):
                super().__init__(width, height)
                self.context = GLContext()

        def init_shaders(self):
                # read shader sources (use provided fallbacks if files missing)
                vertex_shader_string = read_file("resources/vertex_shader.glsl", _default_vertex_shader)
                fragment_shader_string = read_file("resources/fragment_shader.glsl", _default_fragment_shader)

                # query GLSL version supported by the current GL context
                try:
                    raw = glGetString(GL_SHADING_LANGUAGE_VERSION)
                    ver_str = raw.decode().split()[0] if raw else "0.0"
                    ver_num = float(ver_str)
                except Exception:
                    ver_num = 0.0

                # detect if loaded shaders require GLSL 3.30+ (or explicitly contain "330")
                requires_330 = ("330" in vertex_shader_string) or ("330" in fragment_shader_string) \
                               or ("#version 3" in vertex_shader_string) or ("#version 3" in fragment_shader_string)

                # if context doesn't support required GLSL, fall back to GLSL 1.20 compatible shaders
                if requires_330 and ver_num < 3.30:
                    vertex_shader_string = read_file("resources/vertex_shader_120.glsl", _default_vertex_shader_120)
                    fragment_shader_string = read_file("resources/fragment_shader_120.glsl", _default_fragment_shader_120)
                # also use 1.20 fallback for very old contexts if no #version declared
                elif ver_num < 1.30 and not ("#version" in vertex_shader_string or "#version" in fragment_shader_string):
                    vertex_shader_string = read_file("resources/vertex_shader_120.glsl", _default_vertex_shader_120)
                    fragment_shader_string = read_file("resources/fragment_shader_120.glsl", _default_fragment_shader_120)

                vertex_shader = shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER)
                fragment_shader = shaders.compileShader(fragment_shader_string, GL_FRAGMENT_SHADER)
                shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
                return shader_program

        def init_context_raw(self):
                self.shader_program = self.init_shaders()

                self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
                self.context.texture_location = glGetUniformLocation(self.shader_program,
                                                                     "texture_sampler")

                texture = TextureLoader("resources/uvtemplate.png")
                
                self.context.textureGLID = texture.textureGLID

                self.context.vertexbuffer  = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glBufferData(
                        GL_ARRAY_BUFFER,
                        len(vertex_buffer_data) * 4,
                        (GLfloat * len(vertex_buffer_data))(*vertex_buffer_data),
                        GL_STATIC_DRAW
                )

                if texture.inversedVCoords:
                        for index in range(len(uv_buffer_data)):
                                if(index % 2):
                                        uv_buffer_data[index] = 1.0 - uv_buffer_data[index]

                '''
		3. fill here your code to define data buffer for storing the
		cube's texture (uv).
		'''
                # create UV buffer
                self.context.uvbuffer = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
                glBufferData(
                        GL_ARRAY_BUFFER,
                        len(uv_buffer_data) * 4,
                        (GLfloat * len(uv_buffer_data))(*uv_buffer_data),
                        GL_STATIC_DRAW
                )

                # set vertex count so draw() works regardless of raw vs loaded object
                self.context.vertex_count = int(len(vertex_buffer_data) / 3)

                # ensure depth test enabled for correct cube rendering
                glEnable(GL_DEPTH_TEST)

                # unbind
                glBindBuffer(GL_ARRAY_BUFFER, 0)

        def init_context_load(self):
                self.shader_program = self.init_shaders()

                self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
                self.context.texture_location = glGetUniformLocation(self.shader_program, "texture_sampler")

                texture = TextureLoader("resources/uvtemplate.png")
                self.context.textureGLID = texture.textureGLID

                # Locate the OBJ file
                base_dir = os.path.dirname(os.path.abspath(__file__))
                candidates = [
                    os.path.join(base_dir, "resources", "model.obj"),
                    os.path.join(base_dir, "resources", "object", "cube.obj"),
                ] + glob.glob(os.path.join(base_dir, "resources", "*.obj")) \
                  + glob.glob(os.path.join(base_dir, "resources", "object", "*.obj"))

                found = None
                for c in candidates:
                    if os.path.exists(c):
                        found = c
                        break

                if not found:
                    print("Warning: no OBJ file found. Falling back to raw cube.")
                    return self.init_context_raw()

                try:
                    obj = ObjLoader(found)
                except Exception as e:
                    print(f"Warning: failed to load OBJ '{found}': {e}. Falling back to raw cube.")
                    return self.init_context_raw()

                # ----------------------------------------------------------------
                # Extract flat vertex and UV arrays from the ObjLoader.
                # Your loader exposes: obj.vertexs, obj.texcoords, obj.indices
                # obj.vertexs  -> list of (x, y, z) tuples  OR flat float list
                # obj.texcoords-> list of (u, v) tuples      OR flat float list
                # obj.indices  -> list of faces, each face = list of (v, vt, vn) tuples
                # ----------------------------------------------------------------
                try:
                    raw_verts   = obj.vertexs   if hasattr(obj, "vertexs")   else []
                    raw_uvs     = obj.texcoords  if hasattr(obj, "texcoords")  else []
                    raw_indices = obj.indices    if hasattr(obj, "indices")    else []

                    out_vertices = []
                    out_uvs      = []

                    def get_pos(raw, idx):
                        """Fetch (x,y,z) from raw using 1-based OBJ index."""
                        i = idx - 1
                        if isinstance(raw[0], (list, tuple)):
                            return list(raw[i])
                        else:
                            # flat float list
                            return [float(raw[i*3]), float(raw[i*3+1]), float(raw[i*3+2])]

                    def get_uv(raw, idx):
                        """Fetch (u,v) from raw using 1-based OBJ index."""
                        i = idx - 1
                        if isinstance(raw[0], (list, tuple)):
                            return list(raw[i])
                        else:
                            # flat float list
                            return [float(raw[i*2]), float(raw[i*2+1])]

                    for face in raw_indices:
                        # face = [(v1,vt1,vn1), (v2,vt2,vn2), (v3,vt3,vn3)]
                        # or could be a flat tuple/list of 3 ints
                        if not isinstance(face[0], (list, tuple)):
                            # flat (v,vt,vn) style, single corner per element
                            face = [face]

                        for corner in face:
                            if isinstance(corner, int):
                                v_idx  = corner
                                vt_idx = corner
                            else:
                                v_idx  = corner[0]
                                vt_idx = corner[1] if len(corner) > 1 and corner[1] is not None else corner[0]

                            pos = get_pos(raw_verts, v_idx)
                            out_vertices.extend(pos)

                            if raw_uvs:
                                uv = get_uv(raw_uvs, vt_idx)
                                out_uvs.extend(uv)
                            else:
                                out_uvs.extend([0.0, 0.0])

                except Exception as e:
                    print(f"Warning: error extracting OBJ data: {e}. Falling back to raw cube.")
                    return self.init_context_raw()

                if not out_vertices:
                    print("Warning: no vertex data extracted from OBJ. Falling back to raw cube.")
                    return self.init_context_raw()

                # Flip V coords if needed
                if texture.inversedVCoords:
                    for i in range(len(out_uvs)):
                        if i % 2 == 1:
                            out_uvs[i] = 1.0 - out_uvs[i]

                # Upload vertex buffer
                self.context.vertexbuffer = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glBufferData(
                    GL_ARRAY_BUFFER,
                    len(out_vertices) * 4,
                    (GLfloat * len(out_vertices))(*out_vertices),
                    GL_STATIC_DRAW
                )

                # Upload UV buffer
                self.context.uvbuffer = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
                glBufferData(
                    GL_ARRAY_BUFFER,
                    len(out_uvs) * 4,
                    (GLfloat * len(out_uvs))(*out_uvs),
                    GL_STATIC_DRAW
                )

                self.context.vertex_count = len(out_vertices) // 3
                glEnable(GL_DEPTH_TEST)
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                print(f"Loaded OBJ '{found}': {self.context.vertex_count} vertices.")
# ...existing code...
        def calc_mvp(self):
                self.calc_model()
                self.context.mvp = self.controller.calc_mvp(self.model_matrix)
                
        def resize(self, width, height):
                glViewport(0, 0, width, height)
                self.calc_mvp()

        def calc_model(self):
                # default identity model matrix
                self.model_matrix = glm.mat4(1)
                # if the controller provides a model transform, prefer it
                if hasattr(self, "controller"):
                    if hasattr(self.controller, "model_matrix"):
                        try:
                            self.model_matrix = self.controller.model_matrix
                        except Exception:
                            pass

        def draw(self):
                """
                The main drawing function. Is called whenever an update occurs.
                """
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.calc_mvp()
                glUseProgram(self.shader_program)
                glUniformMatrix4fv(
                        self.context.mvp_location,
                        1,
                        GL_FALSE,
                        glm.value_ptr(self.context.mvp))

                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.context.textureGLID)
                glUniform1i(self.context.texture_location, 0)

                glEnableVertexAttribArray(0)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
                '''
        3. fill here your code to to enable and bind the texture buffer.
        '''
                # enable and bind UV attribute (location 1)
                glEnableVertexAttribArray(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
                glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

                
                # use recorded vertex count (works both for raw cube and loaded models)
                glDrawArrays(GL_TRIANGLES, 0, getattr(self.context, "vertex_count", int(len(vertex_buffer_data) / 3)))

                glDisableVertexAttribArray(0)
                glDisableVertexAttribArray(1)
                glUseProgram(0)
        

if __name__ == "__main__":
        win = Win()
        win.controller = MVPController(win.update_if, width=win.width, height=win.height)
        win.init_opengl()
        
        #win.init_context_load()
        #win.init_context_raw()
        # To load external model (resources/model.obj) uncomment the following line.
        # Ensure resources/model.obj exists. If not, the raw cube is used instead.
        win.init_context_load()   # use loaded object (falls back to raw if you prefer)
        # win.init_context_raw()
        win.run()
