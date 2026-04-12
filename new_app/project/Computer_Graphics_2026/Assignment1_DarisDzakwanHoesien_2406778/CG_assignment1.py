from OpenGL.GL import *

import glm
import math
import os
from utils.glut_window import GlutWindow
from utils.mvp_controller import MVPController
from OpenGL.GL import shaders
import random
import time

# Define a tetrahedron using triangles
vertex_buffer_data = [
	-1, +0, -1, +1, +0, -1, -1, +0, +1,  # Base 0
	+1, +0, -1, +1, +0, +1, -1, +0, +1,  # Base 1
	-1, +0, -1, +0, +1, +0, +1, +0, -1,  # Side 0
	+1, +0, -1, +0, +1, +0, +1, +0, +1,  # Side 1
	+1, +0, +1, +0, +1, +0, -1, +0, +1,  # Side 2
	-1, +0, +1, +0, +1, +0, -1, +0, -1,  # Side 3
]
# Set random colors for each of the vertices
color_buffer_data = [random.random() for _ in range(len(vertex_buffer_data))]

start_time = time.time()


def read_file(file_path: str) -> str:
    """Reads a text file given a path and returns it as a string."""
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, mode="r") as f:
        contents = f.read()
    return contents


class GLContext:
	"""Used for storing context data in the main window."""
	pass


class Win(GlutWindow):
	"""The main application. Inherits from glut_window.py."""
	def __init__(self, width: int = 800, height: int = 480):
		super().__init__(width, height)
		self.context = GLContext()

	def init_context(self):
		# Read shader files and compile them
		vertex_shader_string = read_file("shaders/vertex_shader.glsl")
		fragment_shader_string = read_file("shaders/fragment_shader.glsl")
		vertex_shader = shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER)
		fragment_shader = shaders.compileShader(
			fragment_shader_string, GL_FRAGMENT_SHADER
		)
		# create program, bind attribute locations (so indices 0 and 1 match the VBO setup),
		# then link the program
		self.shader_program = glCreateProgram()
		glAttachShader(self.shader_program, vertex_shader)
		glAttachShader(self.shader_program, fragment_shader)
		glBindAttribLocation(self.shader_program, 0, b"vertexPosition")
		glBindAttribLocation(self.shader_program, 1, b"vertexColor")
		glLinkProgram(self.shader_program)
		# check link status
		link_status = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
		if not link_status:
			info = glGetProgramInfoLog(self.shader_program)
			raise RuntimeError("Shader program link failed:\n" + info.decode())

		# Get location of the MVP matrix
		self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
		# Generate buffers for vertices and color data and buffer the data
		self.context.vertex_buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glBufferData(
			GL_ARRAY_BUFFER,
			len(vertex_buffer_data) * 4,
			(GLfloat * len(vertex_buffer_data))(*vertex_buffer_data),
			GL_STATIC_DRAW,
		)

		self.context.color_buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glBufferData(
			GL_ARRAY_BUFFER,
			len(color_buffer_data) * 4,
			(GLfloat * len(color_buffer_data))(*color_buffer_data),
			GL_STATIC_DRAW,
		)

	def calc_mvp(self):
		self.calc_model()
		self.context.mvp = self.controller.calc_mvp(self.model_matrix)

	def resize(self, width, height):
		glViewport(0, 0, width, height)
		self.calc_mvp()

	def calc_model(self):
		self.model_matrix = glm.mat4(1)
		# 2. Add code here to make the object rotate
		# Rotate around the X axis continuously using elapsed time
		elapsed = time.time() - start_time
		angle = elapsed  # radians per second; adjust multiplier to change speed
		self.model_matrix = glm.rotate(self.model_matrix, angle, glm.vec3(1, 0, 0))

	def draw(self):
		"""
		The main drawing function. Is called whenever an update occurs.
		"""
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.calc_mvp()
		glUseProgram(self.shader_program)
		glUniformMatrix4fv(
			self.context.mvp_location, 1, GL_FALSE, glm.value_ptr(self.context.mvp)
		)

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

		# draw count = number of vertices = number of floats / 3
		glDrawArrays(GL_TRIANGLES, 0, len(vertex_buffer_data) // 3)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glUseProgram(0)


if __name__ == "__main__":
	win = Win()
	win.controller = MVPController(win.update_if, width=win.width, height=win.height)
	win.init_opengl()
	win.init_context()
	win.run()
