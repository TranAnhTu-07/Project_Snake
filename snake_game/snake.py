# snake.py
import pygame
from settings import *

class Snake:
    def __init__(self):
        # Phần tử cuối list là đầu rắn (theo logic cũ của bạn)
        self.body = [[5, 10]]
        self.direction = "right"

    def change_direction(self, new_dir):
        # Kiểm tra logic UC3: Không cho phép quay đầu 180 độ
        if new_dir == "up" and self.direction != "down":
            self.direction = "up"
        elif new_dir == "down" and self.direction != "up":
            self.direction = "down"
        elif new_dir == "left" and self.direction != "right":
            self.direction = "left"
        elif new_dir == "right" and self.direction != "left":
            self.direction = "right"

    def move(self):
        # Logic UC8: Cập nhật vị trí
        head_x, head_y = self.body[-1]
        
        if self.direction == "right":
            self.body.append([head_x + 1, head_y])
        elif self.direction == "left":
            self.body.append([head_x - 1, head_y])
        elif self.direction == "up":
            self.body.append([head_x, head_y - 1])
        elif self.direction == "down":
            self.body.append([head_x, head_y + 1])
            
        # Cắt đuôi (nếu ăn mồi thì sẽ insert lại ở bên GameController)
        self.body.pop(0)

    def grow(self, tail_x, tail_y):
        # Thêm lại khúc đuôi vừa bị cắt nếu ăn mồi
        self.body.insert(0, [tail_x, tail_y])

    def check_collision(self):
        head = self.body[-1]
        # Chạm tường
        if head[0] < 0 or head[0] > GRID_WIDTH - 1 or head[1] < 0 or head[1] > GRID_HEIGHT - 1:
            return True
        # Chạm thân
        for i in range(len(self.body) - 1):
            if head[0] == self.body[i][0] and head[1] == self.body[i][1]:
                return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))