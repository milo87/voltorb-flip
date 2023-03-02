import pygame as pg
from pygame.locals import *


def main():
    is_running = True
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                is_running = False


def init() -> bool:
    try:
        pg.init()
    except Exception:
        return False
    screen = pg.display.set_mode((500, 500), pg.SCALED)
    pg.display.set_caption("Voltorb Flip")

    return True


if __name__ == "__main__":
    if init():
        main()
