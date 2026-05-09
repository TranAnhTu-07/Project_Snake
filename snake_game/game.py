import pygame
import os
import math
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

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FONT = os.path.join(BASE_DIR, "fonts", "Roboto-Regular.ttf")
        self.font_small = pygame.font.Font(FONT, 20)
        self.font_big   = pygame.font.Font(FONT, 42)
        self.font_mid   = pygame.font.Font(FONT, 28)

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
        self.pausing    = False
        self.paused     = False
        self.new_record = False
        self.step_timer = 0.0
        self._go_alpha  = 0          # reset fade-in mỗi ván
        self._pause_alpha = 0        # reset fade-in pause mỗi ván
        self._pause_tick  = 0        # đếm frame cho pulse animation

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
  # pause game
    def _draw_paused(self):
        W, H  = self.screen.get_size()
        CX    = W // 2
        CY    = H // 2

        # ── Fade-in alpha ─────────────────────────────────────────
        if self._pause_alpha < 200:
            self._pause_alpha = min(self._pause_alpha + 15, 200)
        self._pause_tick += 1

        # ── Dark overlay ──────────────────────────────────────────
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self._pause_alpha))
        self.screen.blit(overlay, (0, 0))

        # ── Panel ─────────────────────────────────────────────────
        panel_w, panel_h = 380, 260
        panel_x = CX - panel_w // 2
        panel_y = CY - panel_h // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((10, 10, 30, min(self._pause_alpha + 30, 240)))
        self.screen.blit(panel, (panel_x, panel_y))

        # Viền panel gradient (2 lớp tạo hiệu ứng glow nhẹ)
        pygame.draw.rect(self.screen, (40, 40, 100),
                         (panel_x, panel_y, panel_w, panel_h),
                         2, border_radius=16)
        pygame.draw.rect(self.screen, (60, 60, 160),
                         (panel_x + 1, panel_y + 1, panel_w - 2, panel_h - 2),
                         1, border_radius=15)

        # ── "PAUSED" với pulse animation ──────────────────────────
        # sin() tạo hiệu ứng nhịp đập nhẹ: scale màu từ 200→255
        pulse = int(math.sin(self._pause_tick * 0.06) * 27 + 228)
        pause_color = (pulse, int(pulse * 0.85), 0)   # vàng cam pulse

        font_title = pygame.font.SysFont('sans', 54, bold=True)
        title_surf = font_title.render("PAUSED", True, pause_color)
        self.screen.blit(title_surf,
                         title_surf.get_rect(centerx=CX, y=panel_y + 28))

        # Gạch chân dưới title
        line_y = panel_y + 95
        pygame.draw.line(self.screen, (50, 50, 120),
                         (panel_x + 24, line_y),
                         (panel_x + panel_w - 24, line_y), 1)

        # ── Hai dòng hướng dẫn ────────────────────────────────────
        font_key   = pygame.font.SysFont('sans', 20, bold=True)
        font_label = pygame.font.SysFont('sans', 20)

        def draw_hint(key_text, desc_text, y):
            # Badge phím
            key_surf = font_key.render(key_text, True, (20, 20, 20))
            kw = key_surf.get_width() + 18
            kh = 28
            kx = CX - 120
            ky = y
            pygame.draw.rect(self.screen, (200, 200, 60),
                             (kx, ky, kw, kh), border_radius=6)
            self.screen.blit(key_surf, (kx + 9, ky + 4))

            # Mô tả
            desc_surf = font_label.render(desc_text, True, (200, 200, 220))
            self.screen.blit(desc_surf, (kx + kw + 14, ky + 4))

        draw_hint("P",   "Resume Game",  panel_y + 118)
        draw_hint("ESC", "Main Menu",    panel_y + 162)

        # ── Đường kẻ bottom + tip nhỏ ────────────────────────────
        line_y2 = panel_y + panel_h - 44
        pygame.draw.line(self.screen, (50, 50, 120),
                         (panel_x + 24, line_y2),
                         (panel_x + panel_w - 24, line_y2), 1)

        font_tip = pygame.font.SysFont('sans', 15)
        tip = font_tip.render("Game is paused", True, (70, 70, 100))
        self.screen.blit(tip, tip.get_rect(centerx=CX, y=panel_y + panel_h - 32))
        
    # game over
    def _draw_game_over(self):
        # --- Fade-in alpha tăng dần mỗi frame, tối đa 210 ---
        if not hasattr(self, '_go_alpha'):
            self._go_alpha = 0
        if self._go_alpha < 210:
            self._go_alpha = min(self._go_alpha + 12, 210)

        W, H = 601, 601
        CX = W // 2

        # ── Dark overlay ──────────────────────────────────────────
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self._go_alpha))
        self.screen.blit(overlay, (0, 0))

        # ── Panel bo góc ──────────────────────────────────────────
        panel_w, panel_h = 440, 340
        panel_x = CX - panel_w // 2
        panel_y = H  // 2 - panel_h // 2 - 10
        panel_alpha = min(self._go_alpha + 20, 240)

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((15, 15, 25, panel_alpha))
        self.screen.blit(panel, (panel_x, panel_y))

        # Viền panel
        pygame.draw.rect(self.screen, (60, 60, 100),
                         (panel_x, panel_y, panel_w, panel_h),
                         2, border_radius=16)

        # ── "GAME OVER" title ─────────────────────────────────────
        font_title = pygame.font.SysFont('sans', 52, bold=True)
        title_color = (220, 50, 80)
        title = font_title.render("GAME OVER", True, title_color)
        self.screen.blit(title, title.get_rect(centerx=CX, y=panel_y + 28))

        # Gạch chân dưới title
        line_y = panel_y + 90
        pygame.draw.line(self.screen, (60, 60, 100),
                         (panel_x + 20, line_y), (panel_x + panel_w - 20, line_y), 1)

        # ── Score / High Score ────────────────────────────────────
        font_label = pygame.font.SysFont('sans', 20)
        font_value = pygame.font.SysFont('sans', 32, bold=True)
        high = self.scorer.get_high_score(self.username)

        # Score block (trái)
        sc_lbl = font_label.render("SCORE", True, (140, 140, 180))
        sc_val = font_value.render(str(self.score), True, WHITE)
        self.screen.blit(sc_lbl, sc_lbl.get_rect(centerx=CX - 90, y=panel_y + 105))
        self.screen.blit(sc_val, sc_val.get_rect(centerx=CX - 90, y=panel_y + 128))

        # Divider dọc
        pygame.draw.line(self.screen, (60, 60, 100),
                         (CX, panel_y + 100), (CX, panel_y + 175), 1)

        # High Score block (phải)
        hs_color = YELLOW if self.new_record else (140, 140, 180)
        hs_lbl = font_label.render("BEST", True, hs_color)
        hs_val = font_value.render(str(high), True, YELLOW if self.new_record else WHITE)
        self.screen.blit(hs_lbl, hs_lbl.get_rect(centerx=CX + 90, y=panel_y + 105))
        self.screen.blit(hs_val, hs_val.get_rect(centerx=CX + 90, y=panel_y + 128))

        # Badge "NEW RECORD"
        if self.new_record:
            badge_font = pygame.font.SysFont('sans', 15, bold=True)
            badge = badge_font.render("NEW RECORD", True, (20, 20, 20))
            bw = badge.get_width() + 16
            bx = CX + 90 - bw // 2
            by = panel_y + 168
            pygame.draw.rect(self.screen, YELLOW, (bx, by, bw, 20), border_radius=4)
            self.screen.blit(badge, (bx + 8, by + 2))

        # ── Buttons ───────────────────────────────────────────────
        btn_y      = panel_y + 210
        btn_h      = 46
        btn_restart = pygame.Rect(panel_x + 30,          btn_y, 180, btn_h)
        btn_menu    = pygame.Rect(panel_x + panel_w - 210, btn_y, 180, btn_h)

        mx, my = pygame.mouse.get_pos()
        self._go_btn_restart = btn_restart
        self._go_btn_menu    = btn_menu

        def draw_btn(rect, label, base_color, hover_color):
            color = hover_color if rect.collidepoint(mx, my) else base_color
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=10)
            txt = pygame.font.SysFont('sans', 20, bold=True).render(label, True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

        draw_btn(btn_restart, "RESTART",   (30, 130, 60),  (40, 180, 80))
        draw_btn(btn_menu,    "MAIN MENU", (50, 50, 140),  (70, 70, 190))

        # Hint phím tắt nhỏ phía dưới
        hint_font = pygame.font.SysFont('sans', 15)
        hint = hint_font.render("SPACE  restart      ESC  menu", True, (90, 90, 120))
        self.screen.blit(hint, hint.get_rect(centerx=CX, y=panel_y + panel_h - 28))
  

    # Main game loop
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0 

            self._draw()
            if self.paused:
                self._draw_paused()
            elif self.pausing:
                self._draw_game_over()

            pygame.display.flip()

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN and self.pausing:
                    if hasattr(self, '_go_btn_restart') and self._go_btn_restart.collidepoint(event.pos):
                        self._reset()
                    elif hasattr(self, '_go_btn_menu') and self._go_btn_menu.collidepoint(event.pos):
                        return

                if event.type == pygame.KEYDOWN:
                    if not self.pausing:
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                            if not self.paused:          # vừa resume
                                self._pause_alpha = 0   # fade-in lại lần sau
                                self._pause_tick  = 0
                        if not self.paused:
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
            if not self.pausing and not self.paused:
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