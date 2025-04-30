import sdl2
import sdl2.ext
import time
from PIL import Image
import sdl2.sdlttf
from controller import ControllerManager
from screen import ScreenManager
import ctypes
from ctypes import byref

ROM_DIR = "/mnt/sdcard/Roms/"

sdl2.ext.init(controller=True)


controller_manager = ControllerManager()
screen_manager = ScreenManager();

pad = controller_manager.get_controller()

def run_option_toggle_ui():
    line_height = screen_manager.get_line_height() + 10  # add 5px padding between lines
    options = ["01234", "56789", "ABCDE" , "FGHIJ", "abcde", "fghij"]
    toggles = [False] * len(options)

    running = True
    event = sdl2.SDL_Event()

    print("Use D-pad or left stick to navigate. Press A to confirm. Press Start to exit.")
    selected = 0;
    while running:
        while sdl2.SDL_PollEvent(byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
                btn = event.cbutton.button
                if btn == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP:
                    print("⬆️ Up")
                    selected-=1
                elif btn == sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                    print("⬇️ Down")
                    selected+=1
                elif btn == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    print("⬅️ Left")
                elif btn == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    print("➡️ Right")
                elif btn == sdl2.SDL_CONTROLLER_BUTTON_A:
                    print("✅ Confirm (A)")
                    toggles[selected] = not toggles[selected];
                    print(f"Toggling {options[selected]}")

                elif btn == sdl2.SDL_CONTROLLER_BUTTON_START:
                    print("🛑 Exit (Start)")
                    running = False

        screen_manager.clear()
        selected = max(0, selected)
        selected = min(len(options)-1, selected)

        for i, (label, state) in enumerate(zip(options, toggles)):
            text = f"{label.ljust(5)} [{'y' if state else 'n'}]"
            if(i == selected) :
                screen_manager.render_text(text, 50, 50 + i * line_height, color=(255, 255, 0))
            else :
                screen_manager.render_text(text, 50, 50 + i * line_height, color=(255, 255, 255))


        screen_manager.present()

run_option_toggle_ui();
    

