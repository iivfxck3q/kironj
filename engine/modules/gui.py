import imgui
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class Gui():
    def __init__(self,window) -> None:
        self.window=window

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.window.wnd)

        self.test_input = 0
        
    def render(self):
        imgui.new_frame()
        imgui.begin("DEBUG INFO")
        imgui.text(f"FPS: {self.window._fps}")
        imgui.text(f"Pos: {self.window.camera.position}")
        imgui.text(f"Rotate: {self.window.camera.rotate}")
        imgui.text(f"Direction: {self.window.camera.direction}")

        changed, self.window._color = imgui.color_edit3("BG-Color", *self.window._color)
        changed, self.window.camera._velocity = imgui.slider_float(
            "Velocity:", self.window.camera._velocity,
            0.1, 10
        )
        
        changed, self.window.camera._sensitivity = imgui.slider_float(
            "Sensitivity:", self.window.camera._sensitivity,
            0.1, 10
            
        )
        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    
    def resize(self, width: int, height: int):
        self.imgui.resize(width, height)

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)