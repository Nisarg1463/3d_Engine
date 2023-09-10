import glm
import pygame as pg
from gameobject import GameObject

FOV = 50
NEAR = 0.1
FAR = 100


class Camera(GameObject):
    def __init__(
        self,
        app,
        objects=[],
        scripts={},
        position=(0, 0, -4),
        rotation=(0, 90, 0),
        scale=(1, 1, 1),
    ) -> None:
        super().__init__(app, objects, scripts, position, rotation, scale)
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.up = glm.vec3(0, -1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, 1)
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.forward + self.position, self.up)

    def update(self):
        super().update()
        self.app.light.spotLights["cam"].position = glm.vec3(self.position)
        self.app.light.spotLights["cam"].direction = glm.vec3(self.forward)

        self.m_view = self.get_view_matrix()

