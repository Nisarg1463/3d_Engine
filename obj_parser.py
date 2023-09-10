class OBJParser:
    def __init__(self, obj_path, mtl_path=None):
        self.obj_path = obj_path
        self.mtl_path = mtl_path

    def read_data(self):
        vertices = []
        normals = []
        faces = []
        uv_mapping = []
        materials = []
        material = ""
        with open(self.obj_path) as file:
            for line in file.readlines():
                if line.startswith("v "):
                    vertices.append(line.split()[1:])
                if line.startswith("vn "):
                    normals.append(line.split()[1:])
                if line.startswith("vt "):
                    uv_mapping.append(line.split()[1:])
                if line.startswith("f "):
                    face = []
                    for elem in line.split()[1:]:
                        element = []
                        for value in elem.split("/"):
                            if value != "":
                                element.append(int(value) - 1)
                            else:
                                element.append(None)
                        face.append(element)
                    faces.append(face)
                    materials.append(material)
                if line.startswith("usemtl "):
                    material = line.split()[1]

        for i in range(len(faces)):
            print(faces[i], materials[i])

    def read_material(self):
        pass
