from .matrix import MatMGLW
from .objloader import parse_obj_file
import numpy

from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry import AttributeNames


class Model:
    def __init__(self,obj) -> None:
        self.obj=obj

        self._x, self._y, self._z = -4, 0, 0
        self._dx, self._dy, self._dz = 0,0,0

        self._model=None

    @property
    def position(self):
        return (self._x, self._y, self._z)
    
    @property
    def rotate(self):
        return (self._dx, self._dy, self._dz)

    @property
    def _matrix(self):
        translation = MatMGLW.translate(self.position)
        rotate=MatMGLW.rotatexyz(self.rotate)

        model_matrix = rotate@translation
        
        return model_matrix
    
    def load(self,path):
        self._model=self.model_create(path)
        
    def render(self,program,texture):
        if texture:
            program['texture0'].value = 0
            texture.use(location=0)
        # program['color'].value = 1.0, 1.0, 1.0, 1.0
        program['m_proj'].write(self.obj.camera._projection.astype("f4"))
        program['m_model'].write(self._matrix.astype("f4"))
        program['m_camera'].write(self._matrix.astype("f4")@self.obj.camera._matrix.astype("f4"))
        self._model.render(program)

    def model_create(self,path) -> VAO:
        m_prop=parse_obj_file(self.obj.resource_dir / path)

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

        return vao