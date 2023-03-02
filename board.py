from tile import Tile, Type
import random


class Board:
    def __init__(self, width=5, height=5) -> None:
        self.width: int = width
        self.height: int = height
        self.cells: list[Tile] = []

    def setup_board(self) -> None:
        self.cells = []
        for _ in range(self.width * self.height):
            choice = random.randint(1, 10)
            if choice <= 3:
                self.cells.append(Tile(random.choice(list(Type)[2:])))
            elif choice < 9:
                self.cells.append(Tile(Type.ONE))
            else:
                self.cells.append(Tile(Type.VOLTORB))

    def get_cell(self, x: int, y: int) -> Tile:
        return self.cells[y * self.width + x]

    def get_row_value(self, row: int) -> int:
        total = 0
        for x in range(self.width):
            total = total + self.get_cell(x, row).value()

        return total

    def get_column_value(self, column: int) -> int:
        total = 0
        for y in range(self.height):
            total = total + self.get_cell(column, y).value()

        return total

    def get_voltorbs_in_row(self, row: int) -> int:
        total = 0
        for x in range(self.width):
            if self.get_cell(x, row).type == Type.VOLTORB:
                total = total + 1

        return total

    def get_voltorbs_in_column(self, column: int) -> int:
        total = 0
        for y in range(self.height):
            if self.get_cell(column, y).type == Type.VOLTORB:
                total = total + 1

        return total

    def flip_tile(self, x: int, y: int) -> None:
        if x > self.height or y > self.width or x < 0 or y < 0:
            raise ValueError("Selected tile out of bounds")

        self.get_cell(x, y).is_revealed = True

    def check_board(self) -> bool:
        for cell in self.cells:
            if cell.type in [Type.TWO, Type.THREE] and not cell.is_revealed:
                return False

        return True

    def __str__(self) -> str:
        output = ""

        for y in range(self.height):
            for x in range(self.width):
                cell_value = str(self.get_cell(x, y))
                output = output + cell_value + " "

            output = (
                output
                + "| "
                + f"{self.get_row_value(y):2}"
                + " "
                + f"{self.get_voltorbs_in_row(y):2}"
                + "\n"
            )

        output = output + "---" * self.width + "x" + "\n"

        for column in range(self.width):
            output = output + f"{self.get_column_value(column):2}" + " "
        output = output + "\n"
        for column in range(self.width):
            output = output + f"{self.get_voltorbs_in_column(column):2}" + " "

        output = output + "\n"

        return output
