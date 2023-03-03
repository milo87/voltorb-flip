import pygame as pg
import os
from typing import Tuple


class Assets:
    def __init__(self, assets_dir: str) -> None:
        self.assets_dir = assets_dir

    def load_image(self, name, colorkey=None, scale=1) -> Tuple[pg.Surface, pg.Rect]:
        fullname = os.path.join(self.assets_dir, name)
        image = pg.image.load(fullname)

        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pg.transform.scale(image, size)

        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image, image.get_rect()
