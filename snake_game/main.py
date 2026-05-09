# main.py
import pygame
from time import sleep
from settings import *
from game import GameController

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    # Khởi tạo Game Controller
    game = GameController(screen)
    running = True

    while running:
        clock.tick(60)
        
        # 1. Bắt sự kiện (Input)
        running = game.handle_events()
        
        # 2. Xử lý logic (Update)
        game.update()
        
        # 3. Vẽ lên màn hình (Render)
        game.draw()
        
        sleep(0.05)

    pygame.quit()

if __name__ == "__main__":
    main()