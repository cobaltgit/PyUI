from display.font_purpose import FontPurpose
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
            FontPurpose.GRID_ONE_ROW : self._load_font(FontPurpose.GRID_ONE_ROW),
            FontPurpose.GRID_MULTI_ROW : self._load_font(FontPurpose.GRID_MULTI_ROW),
            FontPurpose.LIST : self._load_font(FontPurpose.LIST),
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


    def _load_font(self, font_purpose):
        if sdl2.sdlttf.TTF_Init() == -1:
            raise RuntimeError("Failed to initialize SDL_ttf")

        # Load the TTF font
        # font_path = "/mnt/sdcard/spruce/Font Files/Noto.ttf"
        font_path = self.theme.get_font(font_purpose)
        font_size = self.theme.get_font_size(font_purpose)
        
        font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
        if not font:
            raise RuntimeError("Could not load font")
        line_height = sdl2.sdlttf.TTF_FontHeight(font)
        return LoadedFont(font,line_height)
        
    def clear(self):
        sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.background_texture, None, None)
    
    def render_text(self,text, x, y, color, purpose : FontPurpose, absolute_x_y = True):
        # Create an SDL_Color
        sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
        
        # Render the text to a surface
        surface = sdl2.sdlttf.TTF_RenderText_Blended(self.fonts[purpose].font, text.encode('utf-8'), sdl_color)
        if not surface:
            raise RuntimeError("Failed to render text surface")

        # Create a texture from the surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)
        if not texture:
            sdl2.SDL_FreeSurface(surface)
            raise RuntimeError("Failed to create texture from surface")

        # Get the width and height of the surface
        if(absolute_x_y) :
            rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)
        else:
            rect = sdl2.SDL_Rect(x - int(surface.contents.w/2), y, surface.contents.w, surface.contents.h)

        # Copy the texture to the renderer
        sdl2.SDL_RenderCopy(self.renderer.renderer, texture, None, rect)

        # Clean up
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)

    def render_text_centered(self,text, x, y, color, purpose : FontPurpose):
        self.render_text(text, x, y, color, purpose, False)

    def render_image(self, image_path: str, x: int, y: int, absolute_x_y = True):
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
        if(absolute_x_y) :
            rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)
        else :
            rect = sdl2.SDL_Rect(x - int(surface.contents.w/2), y, surface.contents.w, surface.contents.h)

        # Copy the texture to the renderer
        sdl2.SDL_RenderCopy(self.renderer.renderer, texture, None, rect)

        # Clean up
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)
        return surface.contents.w, surface.contents.h
    
    def render_image_centered(self, image_path: str, x: int, y: int):
        return self.render_image(image_path,x,y,False)

    def get_line_height(self, purpose : FontPurpose):
        return self.fonts[purpose].line_height;
        
    def present(self):
        self.renderer.present();
