import pygame
from random import randint
from food import Food
from score import Score

GREEN  = (0,   210, 80)
GREEN2 = (0,   160, 50)
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (220, 50,  50)
YELLOW = (255, 220, 0)
DARK   = (20,  20,  20)

CELL = 30
GRID = 20

# tốc độ theo độ khó (giây/bước)
DIFFICULTY_SPEED = {
    "easy":   0.12,
    "medium": 0.07,
    "hard":   0.04,
}

class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 username: str, difficulty: str):
        self.screen     = screen
        self.clock      = clock
        self.username   = username
        self.difficulty = difficulty
        self.step_delay = DIFFICULTY_SPEED.get(difficulty, 0.07)

        self.font_small = pygame.font.SysFont('sans', 20)
        self.font_big   = pygame.font.SysFont('sans', 42, bold=True)
        self.font_mid   = pygame.font.SysFont('sans', 28)

        self.scorer = Score()
        self._reset()

    # Reset / khởi tạo trạng thái
    def _reset(self):
        self.snakes    = [[5, 10]]
        self.direction = "right"
        self.next_dir  = "right"
        self.food      = Food()
        self.food.respawn(self.snakes)
        self.score     = 0
        self.pausing   = False
        self.new_record = False
        self.step_timer = 0.0

    # Di chuyển rắn 
    def _move(self):
        self.direction = self.next_dir
        head = self.snakes[-1]
        if self.direction == "right":
            new_head = [head[0] + 1, head[1]]
        elif self.direction == "left":
            new_head = [head[0] - 1, head[1]]
        elif self.direction == "up":
            new_head = [head[0], head[1] - 1]
        else:
            new_head = [head[0], head[1] + 1]

        self.snakes.append(new_head)
        self.snakes.pop(0)

    # Ăn mồi
    def _check_eat(self):
        head = self.snakes[-1]
        if head[0] == self.food.x and head[1] == self.food.y:
            tail = self.snakes[0]
            self.snakes.insert(0, [tail[0], tail[1]])
            self.food.respawn(self.snakes)
            self.score += 1

    # Kiểm tra va chạm
    def _check_collision(self):
        head = self.snakes[-1]
        # Đụng tường
        if head[0] < 0 or head[0] >= GRID or head[1] < 0 or head[1] >= GRID:
            self.pausing = True
            return
        # Đụng thân
        for segment in self.snakes[:-1]:
            if head == segment:
                self.pausing = True
                return

    # Vẽ
    def _draw(self):
        self.screen.fill(DARK)

        # Lưới mờ
        for i in range(GRID + 1):
            pygame.draw.line(self.screen, (35, 35, 35), (0, i*CELL), (GRID*CELL, i*CELL))
            pygame.draw.line(self.screen, (35, 35, 35), (i*CELL, 0), (i*CELL, GRID*CELL))

        # Rắn
        for idx, seg in enumerate(self.snakes):
            color = GREEN if idx != len(self.snakes) - 1 else (100, 255, 120)
            pygame.draw.rect(self.screen, color,
                             (seg[0]*CELL + 1, seg[1]*CELL + 1, CELL - 2, CELL - 2),
                             border_radius=4)

        # Mồi
        fx, fy = self.food.x * CELL, self.food.y * CELL
        pygame.draw.rect(self.screen, RED, (fx + 3, fy + 3, CELL - 6, CELL - 6), border_radius=6)

        # HUD
        score_txt = self.font_small.render(
            f"Score: {self.score}   Best: {self.scorer.get_high_score(self.username)}   [{self.difficulty.upper()}]",
            True, WHITE)
        self.screen.blit(score_txt, (5, 5))

    def _draw_game_over(self):
        overlay = pygame.Surface((601, 601), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        color = YELLOW if self.new_record else WHITE
        go_txt  = self.font_big.render(f"Game Over!  Score: {self.score}", True, color)
        spc_txt = self.font_mid.render("Space = Chơi lại     Esc = Menu", True, GRAY)

        if self.new_record:
            rec_txt = self.font_mid.render("🏆 Kỷ lục mới!", True, YELLOW)
            self.screen.blit(rec_txt, rec_txt.get_rect(centerx=300, y=220))

        self.screen.blit(go_txt,  go_txt.get_rect(centerx=300,  y=260))
        self.screen.blit(spc_txt, spc_txt.get_rect(centerx=300, y=330))

    # Main game loop
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0 

            self._draw()
            if self.pausing:
                self._draw_game_over()

            pygame.display.flip()

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN:
                    if not self.pausing:
                        if event.key == pygame.K_UP    and self.direction != "down":
                            self.next_dir = "up"
                        if event.key == pygame.K_DOWN  and self.direction != "up":
                            self.next_dir = "down"
                        if event.key == pygame.K_LEFT  and self.direction != "right":
                            self.next_dir = "left"
                        if event.key == pygame.K_RIGHT and self.direction != "left":
                            self.next_dir = "right"

                    if event.key == pygame.K_SPACE and self.pausing:
                        self._reset()
                    if event.key == pygame.K_ESCAPE:
                        return  

            # Bước logic theo step_delay
            if not self.pausing:
                self.step_timer += dt
                if self.step_timer >= self.step_delay:
                    self.step_timer = 0.0
                    self._move()
                    self._check_collision()
                    self._check_eat()

                    # Lưu điểm khi game over
                    if self.pausing:
                        self.new_record = self.scorer.save_if_high_score(
                            self.username, self.score)
GRAY = (180, 180, 180)