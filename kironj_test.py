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
        self.wnd.frames
        
    def render(self, time: float, frametime: float):
        super().render(time, frametime)
        self.model.render()
        self.gui.render()
        

if __name__ == '__main__':
    kironjWindow.draw(kironjTest)