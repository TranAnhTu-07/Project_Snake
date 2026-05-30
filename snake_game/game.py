import pygame
import os
import math
import random
from food import Food
from score import Score

# Thêm màu sắc cho rắn
GREEN   = (0,   210,  80)
GREEN2  = (0,   160,  50)
BLUE    = (30,  120, 255)
BLUE2   = (20,   80, 180)
BLACK   = (0,     0,   0)
WHITE   = (255, 255, 255)
RED     = (220,  50,  50)
ORANGE  = (255, 160,   0)
YELLOW  = (255, 220,   0)
DARK    = (20,   20,  20)
GRAY    = (180, 180, 180)
CYAN    = (0,   220, 220)


CELL        = 25
GRID_1P     = 20          # 1-player: 20×20
GRID_2P     = 28          # 2-player: 28×28  →  700×700 px
OBSTACLE_COUNT = 8

# tốc độ theo độ khó (giây/bước)
DIFFICULTY_SPEED = {
    "easy":   0.14,
    "medium": 0.08,
    "hard":   0.045,
}

# Chiều ngược
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}

# Vector di chuyển
DELTA = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}
def resource_path(relative_path):
    """Lấy đường dẫn đúng cả khi chạy .py lẫn .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# ═════════════════════════════════════════════════════════════════════════════
#  class Snake: lưu trạng thái của rắn
# ═════════════════════════════════════════════════════════════════════════════
class Snake:
    """Đóng gói toàn bộ trạng thái của 1 con rắn."""
    def __init__(self, start_pos: list[int], start_dir: str,
                 color_body, color_head):
        self.body       = [start_pos[:]]
        self.direction  = start_dir
        self.next_dir   = start_dir
        self.score      = 0
        self.alive      = True
        self.color_body = color_body
        self.color_head = color_head

    def commit_direction(self):
        if self.next_dir != OPPOSITE[self.direction]:
            self.direction = self.next_dir

    def next_head(self) -> list[int]:
        dx, dy = DELTA[self.direction]
        hx, hy = self.body[-1]
        return [hx + dx, hy + dy]

    def move(self) -> list[int]:
        self.commit_direction()
        new_head = self.next_head()
        self.body.append(new_head)
        self.body.pop(0)
        return new_head

    def grow(self):
        self.body.insert(0, self.body[0][:])
        self.score += 1

    def occupied(self) -> set[tuple]:
        return {tuple(s) for s in self.body}

    @property
    def head(self) -> list[int]:
        return self.body[-1]


# ═════════════════════════════════════════════════════════════════════════════
#  class Obstacle
# ═════════════════════════════════════════════════════════════════════════════
class Obstacle:
    """Sinh và lưu danh sách ô chướng ngại vật."""
    COLOR       = (120, 80, 40)
    COLOR_LIGHT = (160, 110, 60)

    def __init__(self):
        self.cells: set[tuple] = set()

    def spawn(self, grid: int, count: int, forbidden: set[tuple]):
        self.cells.clear()
        attempts = 0
        while len(self.cells) < count and attempts < count * 50:
            x = random.randint(1, grid - 2)
            y = random.randint(1, grid - 2)
            pos = (x, y)
            if pos not in forbidden and pos not in self.cells:
                self.cells.add(pos)
            attempts += 1

    def draw(self, screen: pygame.Surface, cell: int):
        for (ox, oy) in self.cells:
            rect = pygame.Rect(ox * cell + 1, oy * cell + 1,
                               cell - 2, cell - 2)
            pygame.draw.rect(screen, self.COLOR, rect, border_radius=3)
            pygame.draw.rect(screen, self.COLOR_LIGHT,
                             pygame.Rect(ox * cell + 2, oy * cell + 2,
                                         cell // 3, cell // 5),
                             border_radius=2)
            
class Game:
    # khởi tạo game
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 username: str, difficulty: str, mode: str = "1p"):
        self.screen     = screen
        self.clock      = clock
        self.username   = username
        self.difficulty = difficulty
        self.mode       = mode
        self.step_delay = DIFFICULTY_SPEED.get(difficulty, 0.08)

        self.is_2p = (mode == "2p")
        self.grid  = GRID_2P if self.is_2p else GRID_1P

        # Resize cửa sổ phù hợp lưới + HUD bar 36px
        pygame.display.set_mode((self.grid * CELL, self.grid * CELL + 36))
        self.screen = pygame.display.get_surface()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FONT = os.path.join(BASE_DIR, "fonts", "Roboto-Regular.ttf")
        self.font_small = pygame.font.Font(FONT, 18)
        self.font_big   = pygame.font.Font(FONT, 40)
        self.font_mid   = pygame.font.Font(FONT, 26)

        self.scorer   = Score()
        self.obstacle = Obstacle()
        self._reset()

    # Reset / khởi tạo trạng thái
    def _reset(self):
        g = self.grid

        if self.is_2p:
            self.snake1 = Snake([g // 4,     g // 2], "right",
                                (0, 210, 80),   (120, 255, 140))
            self.snake2 = Snake([3 * g // 4, g // 2], "left",
                                (30, 120, 220), (100, 180, 255))
            for _ in range(2):
                self.snake1.body.insert(0, self.snake1.body[0][:])
                self.snake2.body.insert(0, self.snake2.body[0][:])
        else:
            self.snake1 = Snake([g // 2 - 2, g // 2], "right",
                                (0, 210, 80),   (120, 255, 140))
            self.snake2 = None
            for _ in range(2):
                self.snake1.body.insert(0, self.snake1.body[0][:])

        forbidden = self._all_occupied() | self._spawn_safe_zone()
        self.obstacle.spawn(self.grid, OBSTACLE_COUNT if self.is_2p else 0,
                            forbidden)

        self.food = Food()
        self.food.respawn(self._all_body_list())

        self.pausing    = False
        self.paused     = False
        self.new_record = False
        self.winner     = None
        self.step_timer = 0.0
        self._go_alpha  = 0
        self._pause_alpha = 0
        self._pause_tick  = 0

        # UC11: đếm ngược sau tiếp tục
        self._countdown   = 0 
        self._countdown_timer = 0.0

    # Di chuyển rắn 
    # Helper: tập hợp ô đã có rắn
    def _all_occupied(self) -> set[tuple]:
        occ = self.snake1.occupied()
        if self.snake2:
            occ |= self.snake2.occupied()
        return occ

    def _all_body_list(self) -> list[list[int]]:
        body = list(self.snake1.body)
        if self.snake2:
            body += list(self.snake2.body)
        return body

    def _spawn_safe_zone(self) -> set[tuple]:
        """Vùng ±3 quanh spawn point để obstacle không block lối ra."""
        g = self.grid
        safe: set[tuple] = set()
        centers = [[g // 4, g // 2]]
        if self.is_2p:
            centers.append([3 * g // 4, g // 2])
        for cx, cy in centers:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    safe.add((cx + dx, cy + dy))
        return safe

# Vẽ
    def _draw(self):
        W = self.grid * CELL
        H = self.grid * CELL
        self.screen.fill(DARK)

        # Lưới mờ
        for i in range(self.grid + 1):
            pygame.draw.line(self.screen, (32, 32, 32),
                             (0, i * CELL), (W, i * CELL))
            pygame.draw.line(self.screen, (32, 32, 32),
                             (i * CELL, 0), (i * CELL, H))

        # Obstacles
        self.obstacle.draw(self.screen, CELL)

        # Snake draw helper
        def draw_snake(snake: Snake):
            for idx, seg in enumerate(snake.body):
                is_head = (idx == len(snake.body) - 1)
                color   = snake.color_head if is_head else snake.color_body
                pygame.draw.rect(
                    self.screen, color,
                    (seg[0] * CELL + 1, seg[1] * CELL + 1,
                     CELL - 2, CELL - 2),
                    border_radius=5 if is_head else 3)

        draw_snake(self.snake1)
        if self.snake2:
            draw_snake(self.snake2)

        # Mồi
        fx, fy = self.food.x * CELL, self.food.y * CELL
        pygame.draw.rect(self.screen, RED,
                         (fx + 3, fy + 3, CELL - 6, CELL - 6), border_radius=6)

        # HUD bar (phía dưới lưới)
        hud_y = H + 2
        if self.is_2p:
            p1_txt   = self.font_small.render(
                f"P1 (WASD): {self.snake1.score}", True, (120, 255, 140))
            p2_txt   = self.font_small.render(
                f"P2 (↑↓←→): {self.snake2.score}", True, (100, 180, 255))
            diff_txt = self.font_small.render(
                f"[{self.difficulty.upper()}]", True, (180, 180, 180))
            self.screen.blit(p1_txt,   (6, hud_y))
            self.screen.blit(p2_txt,   (W // 2 - 20, hud_y))
            self.screen.blit(diff_txt, (W - 90, hud_y))
        else:
            best    = self.scorer.get_high_score(self.username)
            hud_txt = self.font_small.render(
                f"Score: {self.snake1.score}   Best: {best}   [{self.difficulty.upper()}]",
                True, WHITE)
            self.screen.blit(hud_txt, (5, hud_y))

  # pause game
    def _draw_paused(self):
        W, H  = self.screen.get_size()
        CX    = W // 2
        CY    = H // 2

        # UC11: Đếm ngược
        if self._countdown > 0:
            overlay = pygame.Surface((W,H), pygame.SRCALPHA)
            overlay.fill((0,0,0,160))
            self.screen.blit(overlay,(0,0))
            num = self.font_big.render(str(self._countdown), True, YELLOW)
            self.screen.blit(num, num.get_rect(center=(CX,CY)))
            msg = self.font_mid.render("Chuẩn bị...", True, WHITE)
            self.screen.blit(msg, msg.get_rect(centerx=CX, y=CY+60))
            return

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

        # SAU Thêm phần hiện tên người chơi
        tip = font_tip.render(f"Paused  ·  {self.username}", True, (120, 120, 160))
        self.screen.blit(tip, tip.get_rect(centerx=CX, y=panel_y + panel_h - 32))

    # 
    def _draw_countdown(self):
        W, H = self.screen.get_size()
        font = pygame.font.SysFont('sans', 120, bold=True)
        surf = font.render(str(self._countdown), True, YELLOW)
        self.screen.blit(surf, surf.get_rect(center=(W // 2, H // 2)))   
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

# ── Title: GAME OVER (1P) hoặc tên người thắng (2P) ──────────
        if self.is_2p:
            win_colors = {"P1": (120, 255, 140), "P2": (100, 180, 255),
                          "Draw": YELLOW}
            win_labels = {"P1": "Player 1 Wins!", "P2": "Player 2 Wins!",
                          "Draw": "It's a Draw!"}
            title_color = win_colors.get(self.winner, WHITE)
            title_label = win_labels.get(self.winner, "Game Over")
            font_title  = pygame.font.SysFont('sans', 44, bold=True)
        else:
            title_color = (220, 50, 80)
            title_label = "GAME OVER"
            font_title  = pygame.font.SysFont('sans', 52, bold=True)
        title = font_title.render(title_label, True, title_color)
        self.screen.blit(title, title.get_rect(centerx=CX, y=panel_y + 28))

        # Gạch chân dưới title
        line_y = panel_y + 90
        pygame.draw.line(self.screen, (60, 60, 100),
                         (panel_x + 20, line_y), (panel_x + panel_w - 20, line_y), 1)

# ── Score / High Score ────────────────────────────────────────
        font_label = pygame.font.SysFont('sans', 20)
        font_value = pygame.font.SysFont('sans', 32, bold=True)

        if self.is_2p:
            # P1 (trái)
            p1_lbl = font_label.render("PLAYER 1", True, (120, 255, 140))
            p1_val = font_value.render(str(self.snake1.score), True, WHITE)
            self.screen.blit(p1_lbl, p1_lbl.get_rect(centerx=CX - 90, y=panel_y + 105))
            self.screen.blit(p1_val, p1_val.get_rect(centerx=CX - 90, y=panel_y + 128))
            pygame.draw.line(self.screen, (60, 60, 100),
                             (CX, panel_y + 100), (CX, panel_y + 175), 1)
            # P2 (phải)
            p2_lbl = font_label.render("PLAYER 2", True, (100, 180, 255))
            p2_val = font_value.render(str(self.snake2.score), True, WHITE)
            self.screen.blit(p2_lbl, p2_lbl.get_rect(centerx=CX + 90, y=panel_y + 105))
            self.screen.blit(p2_val, p2_val.get_rect(centerx=CX + 90, y=panel_y + 128))
        else:
            high = self.scorer.get_high_score(self.username)
            sc_lbl = font_label.render("SCORE", True, (140, 140, 180))
            sc_val = font_value.render(str(self.snake1.score), True, WHITE)
            self.screen.blit(sc_lbl, sc_lbl.get_rect(centerx=CX - 90, y=panel_y + 105))
            self.screen.blit(sc_val, sc_val.get_rect(centerx=CX - 90, y=panel_y + 128))
            pygame.draw.line(self.screen, (60, 60, 100),
                             (CX, panel_y + 100), (CX, panel_y + 175), 1)
            hs_color = YELLOW if self.new_record else (140, 140, 180)
            hs_lbl = font_label.render("BEST", True, hs_color)
            hs_val = font_value.render(str(high), True,
                                       YELLOW if self.new_record else WHITE)
            self.screen.blit(hs_lbl, hs_lbl.get_rect(centerx=CX + 90, y=panel_y + 105))
            self.screen.blit(hs_val, hs_val.get_rect(centerx=CX + 90, y=panel_y + 128))
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
    def _handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pausing:
            if hasattr(self, '_go_btn_restart') and self._go_btn_restart.collidepoint(event.pos):
                self._reset()
            elif hasattr(self, '_go_btn_menu') and self._go_btn_menu.collidepoint(event.pos):
                return True 
        return False

    #  Xử lý phím bấm
    def _handle_key(self, event):
        if event.type != pygame.KEYDOWN:
            return False

        # Pause chỉ dùng cho 1P
        if not self.is_2p and not self.pausing:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                if not self.paused:
                    # UC11: them thoi gian dem nguoc khi tiep tuc
                    self._countdown       = 3
                    self._countdown_timer = 0.0
                    self._pause_alpha     = 0
                    self._pause_tick      = 0

        if event.key == pygame.K_SPACE and self.pausing:
            self._reset()
            return False
        if event.key == pygame.K_ESCAPE:
            return True

        if self.pausing or self.paused:
            return False

        # Player 1: WASD
        s1 = self.snake1
        if event.key == pygame.K_w and s1.direction != "down":
            s1.next_dir = "up"
        if event.key == pygame.K_s and s1.direction != "up":
            s1.next_dir = "down"
        if event.key == pygame.K_a and s1.direction != "right":
            s1.next_dir = "left"
        if event.key == pygame.K_d and s1.direction != "left":
            s1.next_dir = "right"

        # Player 1 (1P): thêm arrow keys
        if not self.is_2p:
            if event.key == pygame.K_UP    and s1.direction != "down":
                s1.next_dir = "up"
            if event.key == pygame.K_DOWN  and s1.direction != "up":
                s1.next_dir = "down"
            if event.key == pygame.K_LEFT  and s1.direction != "right":
                s1.next_dir = "left"
            if event.key == pygame.K_RIGHT and s1.direction != "left":
                s1.next_dir = "right"

        # Player 2: Arrow keys (chỉ 2P)
        if self.is_2p and self.snake2:
            s2 = self.snake2
            if event.key == pygame.K_UP    and s2.direction != "down":
                s2.next_dir = "up"
            if event.key == pygame.K_DOWN  and s2.direction != "up":
                s2.next_dir = "down"
            if event.key == pygame.K_LEFT  and s2.direction != "right":
                s2.next_dir = "left"
            if event.key == pygame.K_RIGHT and s2.direction != "left":
                s2.next_dir = "right"

        return False
    
    # Bước logic game mỗi step_delay giây
    def _step(self):
        g = self.grid

        self.snake1.commit_direction()
        new_head1 = self.snake1.next_head()

        new_head2 = None
        if self.snake2 and self.snake2.alive:
            self.snake2.commit_direction()
            new_head2 = self.snake2.next_head()

        obs   = self.obstacle.cells
        body1 = self.snake1.occupied()
        body2 = self.snake2.occupied() if self.snake2 else set()

        def out_of_bounds(h):
            return h[0] < 0 or h[0] >= g or h[1] < 0 or h[1] >= g

        def hits_wall_or_self_or_obs(head, own_body):
            return (out_of_bounds(head)
                    or tuple(head) in obs
                    or tuple(head) in {tuple(s) for s in own_body[:-1]})

        dead1 = hits_wall_or_self_or_obs(new_head1, self.snake1.body)
        if new_head2 is not None and tuple(new_head1) in body2:
            dead1 = True

        dead2 = False
        if self.snake2 and self.snake2.alive and new_head2 is not None:
            dead2 = hits_wall_or_self_or_obs(new_head2, self.snake2.body)
            if tuple(new_head2) in body1:
                dead2 = True

        # Head-on: 2 đầu gặp nhau → cả 2 chết
        if new_head2 is not None and new_head1 == new_head2:
            dead1 = dead2 = True

        if dead1:
            self.snake1.alive = False
        if dead2 and self.snake2:
            self.snake2.alive = False

        if self.is_2p:
            s1_alive = self.snake1.alive
            s2_alive = self.snake2 and self.snake2.alive
            if not s1_alive and not s2_alive:
                self.winner  = "Draw"
                self.pausing = True
            elif not s1_alive:
                self.winner  = "P2"
                self.pausing = True
            elif not s2_alive:
                self.winner  = "P1"
                self.pausing = True
        else:
            if not self.snake1.alive:
                self.pausing = True

        if self.pausing:
            if not self.is_2p:
                self.new_record = self.scorer.save_if_high_score(
                    self.username, self.snake1.score)
            return

        self.snake1.move()
        if self.snake2 and self.snake2.alive:
            self.snake2.move()

        fx, fy = self.food.x, self.food.y
        ate    = False

        if self.snake1.head == [fx, fy]:
            self.snake1.grow()
            ate = True
        elif self.snake2 and self.snake2.head == [fx, fy]:
            self.snake2.grow()
            ate = True

        if ate:
            all_bodies = self._all_body_list()
            combined   = self.obstacle.cells | {tuple(s) for s in all_bodies}
            for _ in range(500):
                self.food.respawn(all_bodies)
                if (self.food.x, self.food.y) not in combined:
                    break

    # Main loop
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            # UC11: Cập nhật đồng hồ đếm ngược sau khi tiếp tục
            self._draw()
            if self._countdown > 0:
                self._draw_paused()
                self._countdown_timer += dt
                if self._countdown_timer >= 1.0:
                    self._countdown -= 1
                    self._countdown_timer = 0.0
            if self.paused:
                self._draw_paused()
            elif self.pausing:
                self._draw_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((601, 601))
                    pygame.quit()
                    raise SystemExit
                if self._handle_mouse(event):
                    pygame.display.set_mode((601, 601))
                    return
                if self._handle_key(event):
                    pygame.display.set_mode((601, 601))
                    return

            if not self.pausing and not self.paused:
                self.step_timer += dt
                if self.step_timer >= self.step_delay:
                    self.step_timer = 0.0
                    self._step()
        
GRAY = (180, 180, 180)