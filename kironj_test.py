from engine.modules.window import kironjWindow
from engine.modules.gui import Gui
from engine.modules.world import World

class kironjTest(kironjWindow):
    title='kironjTest'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.world=World(self)
        self.gui=Gui(self)

    def render(self, time: float, frametime: float):
        super().render(time, frametime)
        self.world.render()
        self.gui.render()
        
if __name__ == '__main__':
    kironjWindow.draw(kironjTest)