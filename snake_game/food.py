from random import randint

GRID_SIZE = 20  # 20x20 ô

class Food:
    def __init__(self):
        self.position = self._random_pos()

    def _random_pos(self) -> list[int]:
        return [randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)]

    def respawn(self, snake_body: list[list[int]]):
        """UC10: Sinh mồi ở vị trí ngẫu nhiên, tránh thân rắn."""
        while True:
            pos = self._random_pos()
            if pos not in snake_body:
                self.position = pos
                return

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]
