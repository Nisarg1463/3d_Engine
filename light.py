import glm


class Light:
    def __init__(self, app):
        self.pointLights = {0: PointLight(intensity=(0.01, 0.01, 0))}
        self.dirLight = DirectionLight(intensity=(0.01, 0.01, 0))
        self.spotLights = {
            "cam": SpotLight(
                position=app.camera.position,
                direction=app.camera.forward,
                intensity=(0.5, 1, 1),
            )
        }


class PointLight:
    def __init__(
        self,
        position=(3, -6, -3),
        color=(1, 1, 1),
        intensity=(0.1, 0.8, 1.0),
        attenuation=(1.0, 0.09, 0.032),
    ):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # Intensities
        self.Ia = intensity[0] * self.color  # ambient
        self.Id = intensity[1] * self.color  # diffuse
        self.Is = intensity[2] * self.color  # specular
        # attenuation
        self.constant = glm.float32(attenuation[0])
        self.linear = glm.float32(attenuation[1])
        self.quadratic = glm.float32(attenuation[2])


class DirectionLight:
    def __init__(
        self, direction=(3, 6, 3), color=(1, 1, 1), intensity=(0.1, 0.8, 1.0),
    ):
        self.direction = glm.vec3(direction)
        self.color = glm.vec3(color)
        # Intensities
        self.Ia = intensity[0] * self.color  # ambient
        self.Id = intensity[1] * self.color  # diffuse
        self.Is = intensity[2] * self.color  # specular


class SpotLight:
    def __init__(
        self,
        angle=12.5,
        position=(3, -6, -3),
        direction=(3, -6, -3),
        color=(1, 1, 1),
        intensity=(0.1, 0.8, 1.0),
        attenuation=(1.0, 0.09, 0.032),
    ):
        self.position = glm.vec3(position)
        self.direction = glm.vec3(direction)
        self.color = glm.vec3(color)
        self.theta = glm.float32(glm.cos(glm.radians(angle)))
        # Intensities
        self.Ia = intensity[0] * self.color  # ambient
        self.Id = intensity[1] * self.color  # diffuse
        self.Is = intensity[2] * self.color  # specular
        # attenuation
        self.constant = glm.float32(attenuation[0])
        self.linear = glm.float32(attenuation[1])
        self.quadratic = glm.float32(attenuation[2])
