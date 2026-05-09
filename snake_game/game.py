# game.py
import pygame
from settings import *
from snake import Snake
from food import Food

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.SysFont('sans', 20)
        self.font_big = pygame.font.SysFont('sans', 50)
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.pausing = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.pausing:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if event.key == pygame.K_UP: self.snake.change_direction("up")
                    if event.key == pygame.K_DOWN: self.snake.change_direction("down")
                    if event.key == pygame.K_LEFT: self.snake.change_direction("left")
                    if event.key == pygame.K_RIGHT: self.snake.change_direction("right")
        return True

    def update(self):
        if not self.pausing:
            # Lưu lại vị trí đuôi trước khi di chuyển để phòng trường hợp ăn mồi
            tail_x, tail_y = self.snake.body[0]
            
            self.snake.move()

            # Kiểm tra va chạm
            if self.snake.check_collision():
                self.pausing = True

            # Kiểm tra ăn mồi
            head = self.snake.body[-1]
            if head[0] == self.food.position[0] and head[1] == self.food.position[1]:
                self.snake.grow(tail_x, tail_y)
                self.food.randomize()
                self.score += 1

    def draw(self):
        self.screen.fill(BLACK)
        
        # Vẽ các thực thể
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Vẽ điểm
        score_txt = self.font_small.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_txt, (5, 5))

        # Vẽ thông báo thua
        if self.pausing:
            game_over_txt = self.font_big.render(f"Game over, score: {self.score}", True, WHITE)
            press_space_txt = self.font_big.render("Press Space to continue", True, WHITE)
            self.screen.blit(game_over_txt, (50, 200))
            self.screen.blit(press_space_txt, (50, 300))

        pygame.display.flip()