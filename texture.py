import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path="Textures/white.jpeg")
        self.textures[1] = self.get_texture(path="Textures/brick.jpeg")
        self.textures[2] = self.get_texture(path="Textures/crate.jpeg")
        self.textures[3] = self.get_texture(path="Textures/crate1.jpg")
        self.textures["camo"] = self.get_texture(path="Textures/camo1.jpeg")
        self.textures["cat"] = self.get_texture(path="Objects/Cat/Cat.jpg")
        self.textures["skybox"] = self.get_texture_cube(
            dir_path="Textures/Skybox1/", ext="png"
        )
        self.textures["skybox2"] = self.get_texture_cube(
            dir_path="Textures/Skybox2/", ext="jpg"
        )
        self.textures["skybox3"] = self.get_texture_cube(
            dir_path="Textures/Skybox3/", ext="png"
        )

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        # texture.fill("red")
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB"),
        )
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # Anisotrophic filtering
        texture.anisotropy = 32.0
        return texture

    def get_texture_cube(self, dir_path, ext="png"):
        faces = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f"{face}.{ext}").convert()
            if face in ["top", "bottom"]:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            else:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], "RGB")

            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
