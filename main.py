import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from Scripts.move import Move


class GraphicsEngine:
    def __init__(self, win_size=(1200, 600)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        # create open gl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # shows inside faces
        # self.ctx.front_face = "cw"
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help tract time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # camera
        self.camera = Camera(self, scripts={Move: []})
        # light
        self.light = Light(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # create the context buffer
        self.ctx.clear(color=(0.1, 0.1, 0.1))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
