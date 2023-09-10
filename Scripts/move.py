import pygame as pg
import glm
from Scripts.base import Script


SPEED = 0.01
SENSITVITY = 0.05


class Move(Script):
    def __init__(self, parent) -> None:
        self.parent = parent

    def update(self):
        super().update()
        self.move()
        self.rotate()
        self.update_vectors()

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.parent.rotation[1] -= rel_x * SENSITVITY
        self.parent.rotation[0] += rel_y * SENSITVITY
        self.parent.rotation[0] = max(-89, min(89, self.parent.rotation[0]))

    def update_vectors(self):
        yaw, pitch = (
            glm.radians(self.parent.rotation[1]),
            glm.radians(self.parent.rotation[0]),
        )
        self.parent.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.parent.forward.y = glm.sin(pitch)
        self.parent.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.parent.forward = glm.normalize(self.parent.forward)
        self.parent.right = glm.normalize(
            glm.cross(self.parent.forward, glm.vec3(0, 1, 0))
        )
        self.parent.up = glm.normalize(
            glm.cross(self.parent.forward, self.parent.right)
        )

    def move(self):
        velocity = SPEED * self.parent.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.parent.position += velocity * self.forward
        if keys[pg.K_s]:
            self.parent.position -= velocity * self.forward
        if keys[pg.K_a]:
            self.parent.position += velocity * self.right
        if keys[pg.K_d]:
            self.parent.position -= velocity * self.right
        if keys[pg.K_LCTRL]:
            self.parent.position -= velocity * self.up
        if keys[pg.K_LSHIFT]:
            self.parent.position += velocity * self.up

