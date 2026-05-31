from random import randint

GRID_SIZE = 20  # 20x20 ô

class Food:
    def __init__(self, big=False):
        self.big = big 
        self.position = [0, 0]

    def _random_pos(self) -> list[int]:
        return [randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)]
    """
    [UC9 - Đặng Tuấn Vũ] Hàm sinh lại mồi trên bàn cờ.
    - Chọn ngẫu nhiên một vị trí trong phạm vi bàn chơi.
    - Kiểm tra vị trí không bị chiếm bởi thân rắn hoặc các mồi hiện có.
    - Cập nhật vị trí mới cho mồi khi tìm được ô hợp lệ.
    """
    def respawn(self, occupied: list[list[int]]):
        while True:
            pos = self._random_pos()
            if pos not in occupied:
                self.position = pos
                return

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]

    @property
    def value(self) -> int:
        """Giá trị điểm của mồi: mồi to = 2, mồi nhỏ = 1"""
        return 2 if self.big else 1
