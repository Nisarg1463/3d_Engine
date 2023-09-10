import glm


class GameObject:
    def __init__(
        self,
        app,
        objects=[],
        scripts={},
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    ) -> None:
        self.sub_objects = objects
        self.scripts = []
        for k, v in scripts.items():
            self.scripts.append(k(self, *v))
        self.self_position = position
        self.position = glm.vec3(list(position))
        self.self_rotation = rotation
        self.rotation = glm.vec3(list(rotation))
        self.self_scale = scale
        self.scale = glm.vec3(list(scale))
        self.app = app

    def update(self):
        for script in self.scripts:
            script.update()

        for object in self.sub_objects:
            object.position = self.position + object.self_position
            object.rotation = self.rotation + object.self_rotation
            object.update()
