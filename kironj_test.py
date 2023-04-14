from engine.modules.window import kironjWindow
from engine.modules.model import Model
from engine.modules.gui import Gui

class kironjTest(kironjWindow):
    title='kironjTest'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.model=Model(self)
        self.model.load('3Dmodels/box.obj')
        self.gui=Gui(self)
        self.texture = self.load_texture_2d(
            '3Dmodels/box.png', mipmap=True, anisotrpy=8)
        self.program = self.load_program('programs/cube_texture_array.glsl')
        # self.program=self.load_program('programs/cube_simple.glsl')
        
        
    def render(self, time: float, frametime: float):
        super().render(time, frametime)
        self.model.render(self.program,self.texture)
        self.gui.render()
        

if __name__ == '__main__':
    kironjWindow.draw(kironjTest)