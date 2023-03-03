import pygame as pg
from pygame.locals import *
import math

from board import Board
from assets import Assets
from tile import Type

TILE_SIZE = 32
PADDING = 5


class GraphicalGame:
    def __init__(self) -> None:
        self.is_running = False
        self.screen = None
        self.board = Board()
        self.assets = Assets("assets")
        self.board_surface = None
        self.x_offset = 0
        self.y_offset = 0
        self.font = None

    def init(self) -> None:
        try:
            pg.init()
        except Exception:
            return
        self.screen = pg.display.set_mode((400, 400), pg.SCALED)
        pg.display.set_caption("Voltorb Flip")
        pg.display.set_icon(self.assets.load_image("voltorb.png")[0])
        self.board_surface = pg.Surface(
            size=(
                (self.board.width * (TILE_SIZE + PADDING)) - PADDING,
                (self.board.height * (TILE_SIZE + PADDING)) - PADDING,
            )
        )

        self.board_surface.set_colorkey(pg.Color("black"))
        self.board.setup_board()

        self.x_offset = self.screen.get_width() / 2 - self.board_surface.get_width() / 2
        self.y_offset = (
            self.screen.get_height() / 2 - self.board_surface.get_width() / 2
        )

        self.font = pg.font.SysFont("Monospace", 10, bold=True)

        self.is_running = True

    def do_loop(self) -> None:
        while self.is_running:
            self.update()
            self.render()

    def update(self):
        self.get_input()

    def render(self) -> None:
        tile_icon, tile_rect = self.assets.load_image("tile_blank.png")
        useless_icon = self.assets.load_image("tile_useless.png")
        possible_voltorb_icon = self.assets.load_image("tile_possible_voltorb.png")

        marked_states = [tile_icon, possible_voltorb_icon[0], useless_icon[0]]

        voltorb_icon = self.assets.load_image("tile_voltorb.png")[0]
        one_icon = self.assets.load_image("tile_1.png")[0]
        two_icon = self.assets.load_image("tile_2.png")[0]
        three_icon = self.assets.load_image("tile_3.png")[0]

        for y in range(self.board.height):
            for x in range(self.board.width):
                cell = self.board.get_cell(x, y)
                if not cell.is_revealed:
                    icon = marked_states[cell.unrevealed_index]
                elif cell.type == Type.ONE:
                    icon = one_icon
                elif cell.type == Type.TWO:
                    icon = two_icon
                elif cell.type == Type.THREE:
                    icon = three_icon
                elif cell.type == Type.VOLTORB:
                    icon = voltorb_icon

                x_tile = x * (tile_rect.width + PADDING)
                y_tile = y * (tile_rect.height + PADDING)
                self.board_surface.blit(icon, dest=(x_tile, y_tile))

        self.screen.fill(pg.Color("lightcyan4"))

        for x in range(self.board.width):
            total = self.board.get_column_value(x)
            voltorbs = self.board.get_voltorbs_in_column(x)
            label = self.font.render(f"{total}/{voltorbs}", 1, pg.Color("black"))
            self.screen.blit(
                label,
                (
                    x * (TILE_SIZE + PADDING)
                    + self.x_offset
                    + (TILE_SIZE / 2 - label.get_width() / 2),
                    self.y_offset + self.board_surface.get_height() + 5,
                ),
            )

        for y in range(self.board.height):
            total = self.board.get_row_value(y)
            voltorbs = self.board.get_voltorbs_in_row(y)
            label = self.font.render(f"{total}/{voltorbs}", 1, pg.Color("black"))
            self.screen.blit(
                label,
                (
                    self.x_offset + self.board_surface.get_width() + 5,
                    y * (TILE_SIZE + PADDING)
                    + self.y_offset
                    + (TILE_SIZE / 2 - label.get_height() / 2),
                ),
            )

        self.screen.blit(self.board_surface, dest=(self.x_offset, self.y_offset))

        pg.display.flip()

    def get_input(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.is_running = False
            # left click = flip tile
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                cell_x = (
                    math.ceil((mouse_x - self.x_offset) / (TILE_SIZE + PADDING)) - 1
                )
                cell_y = (
                    math.ceil((mouse_y - self.y_offset) / (TILE_SIZE + PADDING)) - 1
                )

                clicked_cell = self.board.get_cell(cell_x, cell_y)

                if clicked_cell is not None:
                    if event.button == 1:
                        clicked_cell.is_revealed = True
                    elif event.button == 3:
                        clicked_cell.toggle_mark()


if __name__ == "__main__":
    game = GraphicalGame()
    game.init()
    game.do_loop()
