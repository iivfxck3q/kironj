from .matrix import MatMGLW

class Model:
    def __init__(self,obj) -> None:
        self.obj=obj

        self._x, self._y, self._z = 0, 0, -5
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
        self._model=self.obj.load_scene(path)
        
    def render(self):
        self._model.draw(
            projection_matrix=self.obj.camera._projection,
            camera_matrix=self._matrix@self.obj.camera._matrix
        )