import glm
import math


class MVPController:
    def __init__(self, callback_update, width: int, height: int):
        self.callback_update = callback_update
        self.width = width
        self.height = height
        self.position = glm.vec3(1, 1, -2)
        self.pitch = -0.5
        self.yaw = -0.5
        self.roll = 0.0
        self.speed = 0.4
        self.mouse_speed = 0.01
        self.fov = 90
        self.calc_view_projection()

    def calc_mvp(self, model_matrix=glm.mat4(1.0)):
        return self.projection_matrix * self.view_matrix * model_matrix

    def calc_view_projection(self):
        # 3. Implement the direction, right and up vectors here.
        # Use Euler angles (yaw, pitch) to compute the front (direction) vector.
        front_x = math.cos(self.yaw) * math.cos(self.pitch)
        front_y = math.sin(self.pitch)
        front_z = math.sin(self.yaw) * math.cos(self.pitch)
        front = glm.vec3(front_x, front_y, front_z)
        front = glm.normalize(front)

        world_up = glm.vec3(0, 1, 0)
        self.direction = front
        self.right = glm.normalize(glm.cross(self.direction, world_up))
        self.up = glm.normalize(glm.cross(self.right, self.direction))

        self.view_matrix = glm.lookAt(self.position,
                              self.position + self.direction,
                              self.up)

        self.projection_matrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000)

    def on_keyboard(self, key: bytes, x: int, y: int):
        # 4. Set the corresponding actions based on the key here
        # Suggested keys: w (forward), s (back), a (left), d (right), e (up), r (down)
        if key == b"w":
            self.position += self.direction * self.speed
        elif key == b"s":
            self.position -= self.direction * self.speed
        elif key == b"a":
            self.position -= self.right * self.speed
        elif key == b"d":
            self.position += self.right * self.speed
        elif key == b"e":
            self.position += glm.vec3(0, 1, 0) * self.speed
        elif key == b"r":
            self.position -= glm.vec3(0, 1, 0) * self.speed

        self.calc_view_projection()
        self.callback_update()

    def on_mouse(self, key: int, up: int, x: int, y: int):
        if key == 0 and up == 0:
            self.last_x = x
            self.last_y = y

    def on_mousemove(self, x: int, y: int):
        x_diff = self.last_x - x
        y_diff = self.last_y - y
        self.last_x = x
        self.last_y = y
        self.yaw -= x_diff * self.mouse_speed
        self.pitch -= y_diff * self.mouse_speed
        self.calc_view_projection()
        self.callback_update()

    def on_special_key(self, *args):
        pass

