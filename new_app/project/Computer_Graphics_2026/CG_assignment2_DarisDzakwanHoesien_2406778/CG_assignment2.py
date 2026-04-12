from OpenGL.GL import *
from OpenGL.GL import shaders, GLfloat
import os
import glm
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

                # unbind
                glBindBuffer(GL_ARRAY_BUFFER, 0)

        def init_context_load(self):
                '''
		4. fill here your code to complete the init_context_load function to
		load an external object instead of drawing one with raw triangle.
		'''
                self.shader_program = self.init_shaders()

                self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
                self.context.texture_location = glGetUniformLocation(self.shader_program,
                                                                     "texture_sampler")

                texture = TextureLoader("resources/uvtemplate.png")
                self.context.textureGLID = texture.textureGLID

                # Try to load an external OBJ (expects a UV-mapped model)
                obj_path = "resources/model.obj"
                obj = ObjLoader(obj_path)

                # ObjLoader implementations vary; try common attribute names.
                vertices = None
                uvs = None
                for attr in ("vertices", "vertex_buffer", "vertex_positions", "verts"):
                    if hasattr(obj, attr):
                        vertices = getattr(obj, attr)
                        break
                for attr in ("uvs", "texcoords", "textures", "uv_buffer"):
                    if hasattr(obj, attr):
                        uvs = getattr(obj, attr)
                        break

                if vertices is None:
                    raise RuntimeError("ObjLoader did not provide vertices attribute (tried common names).")
                # Create GL buffers
                self.context.vertexbuffer = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glBufferData(
                    GL_ARRAY_BUFFER,
                    len(vertices) * 4,
                    (GLfloat * len(vertices))(*vertices),
                    GL_STATIC_DRAW
                )

                if uvs is not None:
                    # possibly adjust v coordinate if texture loader uses different convention
                    if texture.inversedVCoords:
                        uvs = list(uvs)  # make mutable copy
                        for i in range(len(uvs)):
                            if i % 2 == 1:
                                uvs[i] = 1.0 - uvs[i]
                    self.context.uvbuffer = glGenBuffers(1)
                    glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
                    glBufferData(
                        GL_ARRAY_BUFFER,
                        len(uvs) * 4,
                        (GLfloat * len(uvs))(*uvs),
                        GL_STATIC_DRAW
                    )
                else:
                    # fallback: generate simple zero UVs to avoid GL errors
                    zero_uvs = [0.0] * (int(len(vertices) / 3) * 2)
                    self.context.uvbuffer = glGenBuffers(1)
                    glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
                    glBufferData(
                        GL_ARRAY_BUFFER,
                        len(zero_uvs) * 4,
                        (GLfloat * len(zero_uvs))(*zero_uvs),
                        GL_STATIC_DRAW
                    )

                # unbind
                glBindBuffer(GL_ARRAY_BUFFER, 0)

        def calc_mvp(self):
                self.calc_model()
                self.context.mvp = self.controller.calc_mvp(self.model_matrix)
                
        def resize(self, width, height):
                glViewport(0, 0, width, height)
                self.calc_mvp()

        def calc_model(self):
                self.model_matrix = glm.mat4(1)

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

                
                glDrawArrays(GL_TRIANGLES, 0, int(len(vertex_buffer_data) / 3))

                glDisableVertexAttribArray(0)
                glDisableVertexAttribArray(1)
                glUseProgram(0)
        

if __name__ == "__main__":
        win = Win()
        win.controller = MVPController(win.update_if, width=win.width, height=win.height)
        win.init_opengl()
        
        #win.init_context_load()
        win.init_context_raw()
        win.run()
