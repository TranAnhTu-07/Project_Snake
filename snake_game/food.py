from random import randint

GRID_SIZE = 20  # 20x20 ô

class Food:
    def __init__(self, game_mode="1p"):
        self.game_mode = game_mode #game_mode = 1 là chế độ 1 người, 2 là chế độ 2 người
        # self.position = self._random_pos()
        self.foods = []
        self.value = 1 #set value = 1 cho mồi thường, bằng 2 là mồi to

    def _random_pos(self) -> list[int]:
        return [randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)]
    
    """
   Hàm kiểm tra vị trí mồi sinh ra có hợp lệ ko
    """
    def get_valid_pos(self, snake1_body, snake2_body=None):
        while True:
            pos = self._random_pos()
            is_valid = (pos not in snake1_body)
            if snake2_body:
                is_valid = is_valid and (pos not in snake2_body)
            # Kiểm tra không trùng với các mồi đang có trên sân
            is_valid = is_valid and (pos not in [f['pos'] for f in self.foods])
            if is_valid:
                return pos
            
    """
    [UC9 - Đặng Tuấn Vũ] Hàm cập nhật và quản lý danh sách mồi trên bàn cờ.
    - Chế độ 1 người: Duy trì 1 mồi.
    - Chế độ 2 người: Duy trì 2 mồi hoạt động cùng lúc.
    - Tỉ lệ rớt mồi to (BIG - 2 điểm) là 20%, đảm bảo chỉ có tối đa 1 mồi to trên sân.
    """
    def update_food(self, snake1_body, snake2_body=None):
        max_foods = 2 if self.game_mode == 2 else 1
        has_big_food = any(f['type'] == 'BIG' for f in self.foods)

        while len(self.foods) < max_foods:
            new_pos = self.get_valid_pos(snake1_body, snake2_body)
            
            # Tỉ lệ 20% mồi to, điều kiện: chưa có mồi to nào trên sân
            if not has_big_food and random.random() < 0.2:
                new_type = 'BIG'
                has_big_food = True
            else:
                new_type = 'NORMAL'
            
            self.foods.append({'pos': new_pos, 'type': new_type})

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]
