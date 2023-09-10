from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        self.vaos["cube"] = self.get_vao(
            program=self.program.programs["default"], vbo=self.vbo.vbos["cube"],
        )
        self.vaos["cat"] = self.get_vao(
            program=self.program.programs["default"], vbo=self.vbo.vbos["cat"],
        )
        self.vaos["sniper"] = self.get_vao(
            program=self.program.programs["default"], vbo=self.vbo.vbos["sniper"],
        )
        self.vaos["skybox"] = self.get_vao(
            program=self.program.programs["skybox"], vbo=self.vbo.vbos["skybox"],
        )
        self.vaos["advance_skybox"] = self.get_vao(
            program=self.program.programs["advance_skybox"],
            vbo=self.vbo.vbos["advance_skybox"],
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
        [vao.release() for vao in self.vaos.values()]
