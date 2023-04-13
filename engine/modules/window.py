from pathlib import Path
import math

import moderngl
import moderngl_window as mglw

#for build
import moderngl_window.context.pyglet, glcontext, pywavefront

from .camera import Camera


class kironjWindow(mglw.WindowConfig):
    window_size = 848, 480
    aspect_ratio = window_size[0] / window_size[1]
    resource_dir = Path(__file__).parent.resolve() / '../resources'
    title = "kiroNJ"
    
    resizable = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera=Camera(self)
        self._fps=0
        self._color=0.1,0.1,0.1
        self.wnd.mouse_exclusivity=True

    def render(self, time: float, frametime: float):
        self.ctx.clear(*self._color)
        self.camera.move_hundler
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self._fps=time=1 if time==0 else round(self.wnd.frames/time,2)
        
        
    def resize(self, width: int, height: int):
        self.gui.resize(width, height)

    def key_event(self, key, action, modifiers):
        self.camera.key_input(key, action, modifiers)
        self.gui.key_event(key, action, modifiers)
    def mouse_position_event(self, x, y, dx, dy):
        self.camera.mouse_position_input(dx,dy)
        self.gui.mouse_position_event(x, y, dx, dy)
    def mouse_drag_event(self, x, y, dx, dy):
        self.gui.mouse_drag_event(x, y, dx, dy)
    def mouse_scroll_event(self, x_offset, y_offset):
        self.gui.mouse_scroll_event(x_offset, y_offset)
    def mouse_press_event(self, x, y, button):
        self.gui.mouse_press_event(x, y, button)
    def mouse_release_event(self, x: int, y: int, button: int):
        self.gui.mouse_release_event(x, y, button)
    def unicode_char_entered(self, char):
        self.gui.unicode_char_entered(char)

    def draw(obj):
        mglw.run_window_config(obj)