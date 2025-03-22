import sys
import colorsys

import pygame
import win32api
import win32con
import win32gui

from ctypes import wintypes, WinDLL


def window_config(hwnd) -> None:
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)

    user32 = WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)


def hsv2rgb(h, s, v) -> tuple[int, int, int]:
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)
    
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return (r, g, b)


def main(s, v, size, width, fps):
    pygame.init()
    pygame.display.set_caption("Overlay")
    pygame.time.set_timer(pygame.USEREVENT, int(1000 / fps))
    
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)), pygame.NOFRAME)
    hwnd = pygame.display.get_wm_info()["window"]
    window_config(hwnd)
    
    line_cords = [win32api.GetCursorPos() for _ in range(size)]
    h = 360 / size

    sc.fill((255, 0, 128))
    
    while not win32api.GetAsyncKeyState(win32con.VK_PAUSE):
        x, y = win32api.GetCursorPos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
            elif event.type == pygame.USEREVENT:
                line_cords.insert(0, (x, y))
                line_cords.pop()
                
        sc.fill((255, 0, 128))
        
        if not all([(x, y) == i for i in line_cords[1:]]):
            for i in range(len(line_cords) - 1):
                pygame.draw.line(sc, hsv2rgb(h * i, s, v), line_cords[i], line_cords[i + 1], width=width)

        
        clock.tick(fps)
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main(s=70, v=100, size=60, width=2, fps=360)
    
    # Для плавного переливания цветов, используется цветовое пространство HSV - Hue Saturation Value
    # S - Saturation, это насыщение цвета (0 - 100)
    # V - Value, это яркость цвета (0 - 100)
    # Size - Длина полосы
    # Width - Толщина полосы
