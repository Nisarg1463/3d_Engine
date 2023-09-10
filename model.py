import numpy as np
import moderngl as mgl
import glm


class BaseModel:
    def __init__(
        self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)
    ):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def internal_update(self):
        ...

    def get_model_matrix(self):
        # correct order for transformation
        # scale->rotate->translate
        # Matrix multiply from right to left

        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, self.scale)

        return m_model

    def update(self):
        self.internal_update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale,) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def internal_update(self):
        self.texture.use()
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

        # Point Light
        self.program["light.position"].write(self.app.light.pointLights[0].position)
        self.program["light.Ia"].write(self.app.light.pointLights[0].Ia)
        self.program["light.Id"].write(self.app.light.pointLights[0].Id)
        self.program["light.Is"].write(self.app.light.pointLights[0].Is)
        self.program["light.constant"].write(self.app.light.pointLights[0].constant)
        self.program["light.linear"].write(self.app.light.pointLights[0].linear)
        self.program["light.quadratic"].write(self.app.light.pointLights[0].quadratic)

        # Direction light
        self.program["dirLight.direction"].write(self.app.light.dirLight.direction)
        self.program["dirLight.Ia"].write(self.app.light.dirLight.Ia)
        self.program["dirLight.Id"].write(self.app.light.dirLight.Id)
        self.program["dirLight.Is"].write(self.app.light.dirLight.Is)

        # Spot Light
        self.program["spotLight.position"].write(
            self.app.light.spotLights["cam"].position
        )
        self.program["spotLight.direction"].write(
            self.app.light.spotLights["cam"].direction
        )
        self.program["spotLight.cutoff"].write(self.app.light.spotLights["cam"].theta)
        self.program["spotLight.Ia"].write(self.app.light.spotLights["cam"].Ia)
        self.program["spotLight.Id"].write(self.app.light.spotLights["cam"].Id)
        self.program["spotLight.Is"].write(self.app.light.spotLights["cam"].Is)
        self.program["spotLight.constant"].write(
            self.app.light.spotLights["cam"].constant
        )
        self.program["spotLight.linear"].write(self.app.light.spotLights["cam"].linear)
        self.program["spotLight.quadratic"].write(
            self.app.light.spotLights["cam"].quadratic
        )

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_0"] = 0
        self.texture.use()

        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)


class Cube(ExtendedBaseModel):
    def __init__(
        self,
        app,
        vao_name="cube",
        tex_id=0,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Cat(ExtendedBaseModel):
    def __init__(
        self,
        app,
        vao_name="cat",
        tex_id="cat",
        pos=(0, 0, 0),
        rot=(90, 0, 0),
        scale=(1, 1, 1),
    ) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Sniper(ExtendedBaseModel):
    def __init__(
        self,
        app,
        vao_name="sniper",
        tex_id="camo",
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()


class Skybox(BaseModel):
    def __init__(
        self,
        app,
        vao_name="skybox",
        tex_id="skybox3",
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def internal_update(self):
        self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvanceSkybox(BaseModel):
    def __init__(
        self,
        app,
        vao_name="advance_skybox",
        tex_id="skybox3",
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
    ):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def internal_update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program["m_invProjView"].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)
