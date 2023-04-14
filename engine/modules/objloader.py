import os


class Material:
    __slots__ = ("name", "diffuse", "ambient", "specular",
                 "emission", "shininess", "texture_name")

    def __init__(self, name, diffuse, ambient, specular, emission, shininess, texture_name=None):
        self.name = name
        self.diffuse = diffuse
        self.ambient = ambient
        self.specular = specular
        self.emission = emission
        self.shininess = shininess
        self.texture_name = texture_name

    def __eq__(self, other):
        return (self.name == other.name and
                self.diffuse == other.diffuse and
                self.ambient == other.ambient and
                self.specular == other.specular and
                self.emission == other.emission and
                self.shininess == other.shininess and
                self.texture_name == other.texture_name)


class Mesh:
    def __init__(self, name):
        self.name = name
        self.material = None

        self.indices = []
        self.vertices = []
        self.normals = []
        self.tex_coords = []
        self.colors = []


def load_material_library(filename):
    file = open(filename, 'r')

    name = None
    diffuse = [1.0, 1.0, 1.0]
    ambient = [1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0]
    emission = [0.0, 0.0, 0.0]
    shininess = 100.0
    opacity = 1.0
    texture_name = None

    matlib = {}

    for line in file:
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'newmtl':
            if name is not None:
                for item in (diffuse, ambient, specular, emission):
                    item.append(opacity)
                matlib[name] = Material(
                    name, diffuse, ambient, specular, emission, shininess, texture_name)
            name = values[1]

        elif name is None:
            pass

        try:
            if values[0] == 'Kd':
                diffuse = list(map(float, values[1:]))
            elif values[0] == 'Ka':
                ambient = list(map(float, values[1:]))
            elif values[0] == 'Ks':
                specular = list(map(float, values[1:]))
            elif values[0] == 'Ke':
                emission = list(map(float, values[1:]))
            elif values[0] == 'Ns':
                shininess = float(values[1])
                shininess = (shininess * 128) / 1000
            elif values[0] == 'd':
                opacity = float(values[1])
            elif values[0] == 'map_Kd':
                texture_name = values[1]

        except BaseException as ex:
            print(ex)

    file.close()

    for item in (diffuse, ambient, specular, emission):
        item.append(opacity)

    matlib[name] = Material(name, diffuse, ambient,
                            specular, emission, shininess, texture_name)

    return matlib


def parse_obj_file(filename):
    materials = {}
    mesh_list = []

    location = os.path.dirname(filename)

    with open(filename, 'r') as f:
        file_contents = f.read()

    material = None
    mesh = None

    vertices = [[0., 0., 0.]]
    normals = [[0., 0., 0.]]
    tex_coords = [[0., 0.]]

    diffuse = [1.0, 1.0, 1.0, 1.0]
    ambient = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    emission = [0.0, 0.0, 0.0, 1.0]
    shininess = 100.0

    default_material = Material(
        "Default", diffuse, ambient, specular, emission, shininess)

    for line in file_contents.splitlines():

        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'v':
            vertices.append(list(map(float, values[1:4])))
        elif values[0] == 'vn':
            normals.append(list(map(float, values[1:4])))
        elif values[0] == 'vt':
            tex_coords.append(list(map(float, values[1:3])))

        elif values[0] == 'mtllib':
            material_abspath = os.path.join(location, values[1])
            materials = load_material_library(filename=material_abspath)

        elif values[0] in ('usemtl', 'usemat'):
            material = materials.get(values[1])
            if mesh is not None:
                mesh.material = material

        elif values[0] == 'o':
            mesh = Mesh(name=values[1])
            mesh_list.append(mesh)

        elif values[0] == 'f':
            if mesh is None:
                mesh = Mesh(name='')
                mesh_list.append(mesh)
            if material is None:
                material = default_material
            if mesh.material is None:
                mesh.material = material

            n1 = None
            nlast = None
            t1 = None
            tlast = None
            v1 = None
            vlast = None

            for i, v in enumerate(values[1:]):
                v_i, t_i, n_i = (
                    list(map(int, [j or 0 for j in v.split('/')])) + [0, 0])[:3]
                if v_i < 0:
                    v_i += len(vertices) - 1
                if t_i < 0:
                    t_i += len(tex_coords) - 1
                if n_i < 0:
                    n_i += len(normals) - 1

                mesh.normals += normals[n_i]
                mesh.tex_coords += tex_coords[t_i]
                mesh.vertices += vertices[v_i]

                if i >= 3:
                    mesh.normals += n1 + nlast
                    mesh.tex_coords += t1 + tlast
                    mesh.vertices += v1 + vlast

                if i == 0:
                    n1 = normals[n_i]
                    t1 = tex_coords[t_i]
                    v1 = vertices[v_i]
                nlast = normals[n_i]
                tlast = tex_coords[t_i]
                vlast = vertices[v_i]

    return mesh_list[0]
