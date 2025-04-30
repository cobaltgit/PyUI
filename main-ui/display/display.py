from display.loaded_font import LoadedFont
from display.font_size import FontSize
import sdl2
import sdl2.ext
import sdl2.sdlttf
from themes.theme import Theme
from devices.device import Device

class Display:
    def __init__(self, theme: Theme, device: Device):
        self.theme = theme
        self.device = device
        self._init_display()
        self.fonts = {
            FontSize.SMALL : self._load_font(self.device.font_size_small),
            FontSize.MEDIUM : self._load_font(self.device.font_size_medium),
            FontSize.LARGE : self._load_font(self.device.font_size_large),
        }
        surf = sdl2.ext.load_image(self.theme.background)
        self.background_texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, surf)
        sdl2.SDL_FreeSurface(surf)
        self.clear()
        self.present()

    def _init_display(self):
        display_mode = sdl2.SDL_DisplayMode()
        if sdl2.SDL_GetCurrentDisplayMode(0, display_mode) != 0:
            print("Failed to get display mode, using fallback 640x480")
            width, height = self.device.screen_width(), self.device.screen_height()
        else:
            width, height = display_mode.w, display_mode.h
            print(f"Display size: {width}x{height}")

        window = sdl2.ext.Window("Minimal SDL2 GUI", size=(width, height), flags=sdl2.SDL_WINDOW_FULLSCREEN)
        window.show()

        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"2")
        # Use default renderer flags
        self.renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)


    def _load_font(self, font_size):
        if sdl2.sdlttf.TTF_Init() == -1:
            raise RuntimeError("Failed to initialize SDL_ttf")

        # Load the TTF font
        font_path = "/mnt/sdcard/spruce/Font Files/Noto.ttf"
        font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
        if not font:
            raise RuntimeError("Could not load font")
        line_height = sdl2.sdlttf.TTF_FontHeight(font)
        return LoadedFont(font,line_height)
        
    def clear(self):
        sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.background_texture, None, None)
    
    def render_text(self,text, x, y, color, size = FontSize.MEDIUM):
        # Create an SDL_Color
        sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
        
        # Render the text to a surface
        surface = sdl2.sdlttf.TTF_RenderText_Blended(self.fonts[size].font, text.encode('utf-8'), sdl_color)
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


    def render_image(self, image_path: str, x: int, y: int):
        # Load the image into an SDL_Surface
        surface = sdl2.sdlimage.IMG_Load(image_path.encode('utf-8'))
        if not surface:
            raise RuntimeError(f"Failed to load image: {image_path}")

        # Create a texture from the surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)
        if not texture:
            sdl2.SDL_FreeSurface(surface)
            raise RuntimeError("Failed to create texture from image surface")

        # Set up the destination rectangle
        rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)

        # Copy the texture to the renderer
        sdl2.SDL_RenderCopy(self.renderer.renderer, texture, None, rect)

        # Clean up
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)
    
    def get_line_height(self, size = FontSize.MEDIUM):
        return self.fonts[size].line_height;
        
    def present(self):
        self.renderer.present();
