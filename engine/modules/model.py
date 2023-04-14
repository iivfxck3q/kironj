from .matrix import MatMGLW
from .objloader import parse_obj_file
import numpy

import moderngl_window as mglw
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry import AttributeNames
from pathlib import Path
from PIL import Image

resource_dir = Path(__file__).parent.resolve() / '../resources'
class ModelProp:
    def __init__(self,vao):
        self._vao=vao
        self._textures=None
        self._textures_location=0
        self._program=None

        self._position=(-2,0,0)
        self._rotation=(0,0,0)
        self._matrix=self.matrix

    @property
    def matrix(self):
        translation = MatMGLW.translate(self._position)
        rotate=MatMGLW.rotatexyz(self._rotation)
        model_matrix = rotate@translation
        return model_matrix.astype("f4")

    def draw(self,projection,camera):
        self._program['texture0'].value = self._textures_location
        self._textures.use(location=self._textures_location)

        self._program['m_proj'].write(projection.astype("f4"))
        self._program['m_model'].write(self._matrix)
        self._program['m_camera'].write(self._matrix@camera.astype("f4"))
        
        self._vao.render(self._program)

def loadmodel(program,path,texture=None):
    m_prop=parse_obj_file(resource_dir / '3Dmodels' / path)

    is_normals=True if m_prop.normals!=[] else False
    is_uvs=True if m_prop.normals!=[] else False

    pos = numpy.array(m_prop.vertices, dtype=numpy.float32)

    if is_normals:
        normal_data = numpy.array(m_prop.normals, dtype=numpy.float32)
    if is_uvs:
        uvs_data = numpy.array(m_prop.tex_coords, dtype=numpy.float32)

    vao = VAO(m_prop.name or "geometry:cube")

    vao.buffer(pos, "3f", [AttributeNames.POSITION])
    if is_normals:
        vao.buffer(normal_data, "3f", [AttributeNames.NORMAL])
    if is_uvs:
        vao.buffer(uvs_data, "2f", [AttributeNames.TEXCOORD_0])

    model=ModelProp(vao)

    model._program=program
    if texture:
        model._textures=loadtexture(texture)
    return model


def loadtexture(textures):
    if isinstance(textures,list):
        count_textures=len(textures)
    else:
        count_textures=1
    for _ in range(count_textures):
        image = Image.open(resource_dir / 'textures' / textures)
        image=image.transpose(Image.FLIP_TOP_BOTTOM)
        if image.palette and image.palette.mode.lower() in ["rgb", "rgba"]:
            mode = mode or image.palette.mode
            image=image.convert(mode)

        data = image.tobytes()
        components = len(data) // (image.size[0] * image.size[1])

        texture=mglw.ctx().texture(image.size, components, data,)

        return texture