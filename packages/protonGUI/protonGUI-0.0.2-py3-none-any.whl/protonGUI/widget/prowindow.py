import glfw, typing
from OpenGL.GL import *


class ProWindow():
    def __init__(self) -> None:
        self.width: int
        self.height: int
        self.title: str
        self.obj: typing.Any
        self.background_color: tuple
        
        
    def _framebuffer_size_callback(self, window, width, height) -> None:
        glViewport(0, 0, width, height)
        self.set_size(width, height)
        
        
    def _cursor_pos_callback(self, window, x, y) -> None:
        pass
    
    
    def _key_callback(self, window, key, scancode, action, mods) -> None:
        pass
    
    
    def _mouse_button_callback(self, window, button, action, mods) -> None:
        pass
    
    
    def _scroll_callback(self, window, xoffset, yoffset) -> None:
        pass
    
    
    def init(self, width: int, height: int, title: str, background_color: tuple = (0, 0, 0)) -> bool:
        self.width = width
        self.height = height
        self.title = title
        
        if len(background_color) == 3 and (0 <= color <= 255 for color in background_color) : self.background_color = background_color
        else: self.background_color = (0, 0, 0)

        if self.height > 0 and self.width > 0:
            if not glfw.init(): return False
            
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
            
            self.obj = glfw.create_window(self.width, self.height, self.title, None, None)
            if not self.obj: return False
            glfw.make_context_current(self.obj)
            
            glfw.set_framebuffer_size_callback(self.obj, self._framebuffer_size_callback)
            glfw.set_cursor_pos_callback(self.obj, self._cursor_pos_callback)
            glfw.set_key_callback(self.obj, self._key_callback)
            glfw.set_mouse_button_callback(self.obj, self._mouse_button_callback)
            glfw.set_scroll_callback(self.obj, self._scroll_callback)
            
            return True
        
        else:
            return False
            
            
    def set_size(self, width: int, height: int) -> bool:
        if width > 0 and height > 0:
            glfw.set_window_size(self.obj, width, height)
            return True
        
        else:
            return False
        
        
    def set_title(self, title: str) -> bool:
        if title != "":
            glfw.set_window_title(self.obj, title)
            return True
        
        else:
            return False


    def mainloop(self) -> None:
        while not glfw.window_should_close(self.obj):
            
            glClearColor(self.background_color[0] / 255, self.background_color[1] / 255, self.background_color[2] / 255, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            glfw.poll_events()
            glfw.swap_buffers(self.obj)
            
        glfw.destroy_window(self.obj)
        glfw.terminate()