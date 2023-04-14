from .model import loadmodel

class World:
    def __init__(self,obj) -> None:
        self.obj=obj
        self._projection=self.obj.camera._projection

        self.skybox_pt=self.obj.load_program('programs/skybox.glsl')
        self.skybox=loadmodel(self.skybox_pt,'skybox.obj','skybox/skybox.png')
        self.skybox._position,self.skybox._rotation=(0,0,0),(0,0,0)
        self.skybox._textures_location=0

        self.malusk_pt=self.obj.load_program('programs/malusk.glsl')
        self.malusk=loadmodel(self.malusk_pt,'malusk.obj','malusk.jpg')
        self.malusk._position,self.malusk._rotation=(-2,0,0),(0,0,0)
        self.malusk._textures_location=1

        self.box_pt=self.obj.load_program('programs/malusk.glsl')
        self.box=loadmodel(self.box_pt,'box.obj',['box.png','malusk.jpg'])
        self.box._textures_location=1
        
    def render(self,time):
        self.box.update([
            ['_rotation',(time*10, time*10, time*10)]
        
        ])
        
        camera_matrix=self.obj.camera._matrix
        self.skybox.draw(self._projection,camera_matrix)
        self.malusk.draw(self._projection,camera_matrix)
        self.box.draw(self._projection,camera_matrix)

        