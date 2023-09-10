from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = AdvanceSkybox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        n, s = 80, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, s, z), tex_id=2))
        add(Cat(app, scale=(1, 1, 1), rot=(90, 0, 0), pos=(0, 2, 20)))

    def render(self):
        for obj in self.objects:
            obj.update()
        self.skybox.update()
