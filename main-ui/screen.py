import sdl2
import sdl2.ext
import sdl2.sdlttf
import os
from themes.theme import Theme

os.environ["SDL_VIDEODRIVER"] = "KMSDRM"
os.environ["SDL_RENDER_DRIVER"] = "kmsdrm"

class Screen:
    def __init__(self, theme):
        self.theme = theme
        self._init_display()
        self._load_font()
        surf = sdl2.ext.load_image(self.theme.background)
        self.background_texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, surf)
        sdl2.SDL_FreeSurface(surf)
        self.clear()
        self.present()

    def _init_display(self):
        display_mode = sdl2.SDL_DisplayMode()
        if sdl2.SDL_GetCurrentDisplayMode(0, display_mode) != 0:
            print("Failed to get display mode, using fallback 640x480")
            width, height = 640, 480
        else:
            width, height = display_mode.w, display_mode.h
            print(f"Display size: {width}x{height}")

        window = sdl2.ext.Window("Minimal SDL2 GUI", size=(width, height), flags=sdl2.SDL_WINDOW_FULLSCREEN)
        window.show()

        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"2")
        # Use default renderer flags
        self.renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)


    def _load_font(self):
        if sdl2.sdlttf.TTF_Init() == -1:
            raise RuntimeError("Failed to initialize SDL_ttf")

        # Load the TTF font
        font_path = "/mnt/sdcard/spruce/Font Files/Noto.ttf"
        font_size = 16
        self.font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
        if not self.font:
            raise RuntimeError("Could not load font")
        self.line_height = sdl2.sdlttf.TTF_FontHeight(self.font)
        
    def clear(self):
        sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.background_texture, None, None)
    
    def render_text(self,text, x, y, color=(255, 255, 255)):
        # Create an SDL_Color
        sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
        
        # Render the text to a surface
        surface = sdl2.sdlttf.TTF_RenderText_Blended(self.font, text.encode('utf-8'), sdl_color)
        if not surface:
            raise RuntimeError("Failed to render text surface")

        # Create a texture from the surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)
        if not texture:
            sdl2.SDL_FreeSurface(surface)
            raise RuntimeError("Failed to create texture from surface")

        # Get the width and height of the surface
        rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)

        # Copy the texture to the renderer
        sdl2.SDL_RenderCopy(self.renderer.renderer, texture, None, rect)

        # Clean up
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)
    
    def get_line_height(self):
        return self.line_height;
        
    def present(self):
        self.renderer.present();
