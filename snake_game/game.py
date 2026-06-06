import pygame
import os
import math
import random
from random import randint
from food import Food
from score import Score

# Màu sắc
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
WALL    = (110, 110, 110) 

CELL = 30
GRID = 20

# Điều khiển player 1: WASD
P1_KEYS = {
    pygame.K_w: "up",
    pygame.K_s: "down",
    pygame.K_a: "left",
    pygame.K_d: "right",
}
# Điều khiển player 2: Arrow keys
P2_KEYS = {
    pygame.K_UP:    "up",
    pygame.K_DOWN:  "down",
    pygame.K_LEFT:  "left",
    pygame.K_RIGHT: "right",
}

# Tốc độ cơ bản theo độ khó
BASE_SPEED = {
    "easy":   0.14,
    "medium": 0.11,
    "hard":   0.08,
}

def resource_path(relative_path):
    if hasattr(os.sys, '_MEIPASS'):
        return os.path.join(os.sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class Snake:
    """Đối tượng rắn cho 1 người chơi."""
    def __init__(self, start_pos, start_dir, color_body, color_head, name, keys):
        self.body      = [start_pos]
        self.direction = start_dir
        self.next_dir  = start_dir
        self.color     = color_body
        self.head_color= color_head
        self.name      = name
        self.keys      = keys
        self.score     = 0
        self.alive     = True
        self.grow      = 1  # khởi tạo rắn dài 4 ô

    def handle_key(self, event):
        if event.type != pygame.KEYDOWN:
            return
        OPPOSITE = {"up":"down","down":"up","left":"right","right":"left"}
        if event.key in self.keys:
            new_dir = self.keys[event.key]
            if new_dir != OPPOSITE.get(self.direction):
                self.next_dir = new_dir

    def move(self):
        if not self.alive:
            return
        self.direction = self.next_dir
        head = self.body[-1]
        if self.direction == "right":
            new_head = [head[0] + 1, head[1]]
        elif self.direction == "left":
            new_head = [head[0] - 1, head[1]]
        elif self.direction == "up":
            new_head = [head[0], head[1] - 1]
        else:
            new_head = [head[0], head[1] + 1]
        self.body.append(new_head)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop(0)

    def check_wall_collision(self):
        head = self.body[-1]
        return head[0] < 0 or head[0] >= GRID or head[1] < 0 or head[1] >= GRID

    def check_self_collision(self):
        head = self.body[-1]
        return head in self.body[:-1]

    def draw(self, screen):
        for idx, seg in enumerate(self.body):
            is_head = (idx == len(self.body) - 1)
            color = self.head_color if is_head else self.color
            pygame.draw.rect(screen, color,
                             (seg[0]*CELL + 1, seg[1]*CELL + 1, CELL - 2, CELL - 2),
                             border_radius=4)


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 username: str, difficulty: str, mode: str = "single",
                 username2: str = "Player 2"):
        self.screen     = screen
        self.clock      = clock
        self.username   = username
        self.username2  = username2
        self.difficulty = difficulty
        self.mode       = mode  # "single" | "two_player"
        self.base_delay = BASE_SPEED.get(difficulty, 0.09)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FONT = os.path.join(BASE_DIR, "fonts", "Roboto-Regular.ttf")
        self.font_small = pygame.font.Font(FONT, 18)
        self.font_big   = pygame.font.Font(FONT, 42)
        self.font_mid   = pygame.font.Font(FONT, 26)

        self.scorer = Score()
        self._reset()

    # ── UC5: Tốc độ tăng theo điểm ───────────────────────────────
    def _calc_speed(self):
        total = self.snake1.score + (self.snake2.score if self.mode == "two_player" else 0)
        # Mỗi 5 điểm giảm 0.005s, tối thiểu = base/3
        speed = self.base_delay - (total // 4) * 0.01
        return max(speed, self.base_delay / 3)

    # ── Reset ────────────────────────────────────────────────────
    def _reset(self):
        self.snake1 = Snake(
            start_pos=[4, 10], start_dir="right",
            color_body=GREEN, color_head=(100, 255, 120),
            name=self.username, keys=P1_KEYS
        )
        if self.mode == "two_player":
            self.snake2 = Snake(
                start_pos=[15, 10], start_dir="left",
                color_body=BLUE, color_head=(100, 180, 255),
                name=self.username2, keys=P2_KEYS
            )
        else:
            self.snake2 = None

        # UC9: sinh mồi tự động
        self._spawn_foods()
        self._spawn_obstacles()

        self.pausing      = False
        self.paused       = False
        self.new_record   = False
        self.new_record2  = False
        self.step_timer   = 0.0
        self._go_alpha    = 0
        self._pause_alpha = 0
        self._pause_tick  = 0
        self._countdown   = 0  
        self._countdown_timer = 0.0
        self._winner      = None
        self.score_popups = []

    # UC9: Sinh mồi tự động
    def _spawn_foods(self):
        # [Bước 9.1.1 & 9.1.4] Hệ thống xác định đang ở chế độ 1 hoặc 2 người để xác định số lượng và loại mồi cần sinh.
        count_small = 3 if self.mode == "two_player" else 1
        self.foods = []
        occupied = []
        # [Bước 9.1.3] Lấy danh sách tất cả ô trống trên bản đồ.
        if self.snake1:
            occupied += self.snake1.body
        if self.snake2:
            occupied += self.snake2.body
        for _ in range(count_small):
            f = Food(big=False)
            # [Bước 9.1.6] Hệ thống sinh ngẫu nhiên một tọa độ (x, y) từ danh sách ô trống
            f.respawn(
                occupied + [food.position for food in self.foods]
            )
            # [Bước 9.1.8] Hệ thống đặt mồi vào tọa độ (x, y) trên ma trận bản đồ.
            self.foods.append(f)
    
    # UC3: Sinh chướng ngại vật ngẫu nhiên
    def _spawn_obstacles(self):
        occupied = (
            list(self.snake1.body)
            + (list(self.snake2.body) if self.snake2 else [])
            + [[f.x, f.y] for f in self.foods]
        )
        count = randint(5, 10)
        self.obstacles = []
        attempts = 0
        while len(self.obstacles) < count and attempts < 300:
            x = randint(0, GRID - 1)
            y = randint(0, GRID - 1)
            if [x, y] not in occupied and [x, y] not in self.obstacles:
                self.obstacles.append([x, y])
            attempts += 1


    def _all_body(self):
        bodies = list(self.snake1.body)
        if self.snake2:
            bodies += list(self.snake2.body)
        return bodies

    # [UC9 - Đặng Tuấn Vũ] Hàm xử lý sự kiện ăn mồi.
    def _check_eat(self):
        for snake in [self.snake1, self.snake2]:
            if snake is None or not snake.alive:
                continue
            head = snake.body[-1]
            # [Bước 9.1.2] Hệ thống phát hiện rắn vừa ăn mồi.
            for food in self.foods[:]:
                if [food.x, food.y] == head:
                    snake.score += food.value
                    snake.grow += food.value
                    # Hiệu ứng điểm thưởng bay lên
                    px = food.x * CELL + CELL // 2
                    py = food.y * CELL + CELL // 2
                    label = f"+{food.value}"
                    color = ORANGE if food.big else (120, 255, 160)
                    duration = random.uniform(0.8, 1.2)
                    self.score_popups.append([px, py, label, color, 0.0, duration])
                    # xóa mồi đã ăn
                    self.foods.remove(food)
                    # kiểm tra còn mồi lớn không
                    has_big_food = any(f.big for f in self.foods)
                    # có tỉ lệ 50% sinh ra mồi lớn
                    spawn_big = (
                        self.mode == "two_player"
                        and not has_big_food
                        and random.random() < 0.5
                    )
                    new_food = Food(big=spawn_big)
                    # Truyền ma trận các ô đã bị chiếm vào , hệ thống sinh ngẫu nhiên và xác nhận tọa độ (x,y) không trùng lặp
                    new_food.respawn(
                        self._all_body()
                        + [f.position for f in self.foods]
                        + self.obstacles
                    )
                    self.foods.append(new_food)
                    break
    # UC8: Kiểm tra va chạm 2 rắn
    def _check_collisions(self):
        snakes = [s for s in [self.snake1, self.snake2] if s and s.alive]
        for snake in snakes:
            if snake.check_wall_collision() or snake.check_self_collision():
                snake.alive = False

        # Va chạm chướng ngại vật (cả 1 và 2 người)
        for snake in snakes:
            if snake.alive and snake.body[-1] in self.obstacles:
                snake.alive = False

        # Va chạm giữa 2 rắn (chỉ chế độ 2 người)
        if self.mode == "two_player" and self.snake1.alive and self.snake2.alive:
            h1 = self.snake1.body[-1]
            h2 = self.snake2.body[-1]
            # Đầu rắn 1 đụng thân rắn 2
            if h1 in self.snake2.body[:-1]:
                self.snake1.alive = False
            # Đầu rắn 2 đụng thân rắn 1
            if h2 in self.snake1.body[:-1]:
                self.snake2.alive = False
            # 2 đầu đụng nhau
            if h1 == h2:
                self.snake1.alive = False
                self.snake2.alive = False

        # Kiểm tra game over
        if self.mode == "single":
            if not self.snake1.alive:
                self._trigger_game_over()
        else:
            alive1 = self.snake1.alive
            alive2 = self.snake2.alive
            if not alive1 and not alive2:
                self._trigger_game_over()
            elif not alive1:
                self._winner = "p2"
                self._trigger_game_over()
            elif not alive2:
                self._winner = "p1"
                self._trigger_game_over()

    def _trigger_game_over(self):
        self.pausing = True
        self.new_record  = self.scorer.save_if_high_score(self.username,  self.snake1.score)
        if self.snake2:
            self.new_record2 = self.scorer.save_if_high_score(self.username2, self.snake2.score)
        # UC10: Xác định người thắng
        if self.mode == "two_player" and self._winner is None:
            if self.snake1.score > self.snake2.score:
                self._winner = "p1"
            elif self.snake2.score > self.snake1.score:
                self._winner = "p2"
            else:
                self._winner = "draw"

    # ── Vẽ ──────────────────────────────────────────────────────
    def _draw(self):
        W, H = self.screen.get_size()
        GAME_W = GRID * CELL
        offset_x = 0

        # Nền
        self.screen.fill(DARK)

        # Lưới
        for i in range(GRID + 1):
            pygame.draw.line(self.screen, (35,35,35), (offset_x, i*CELL), (offset_x+GAME_W, i*CELL))
            pygame.draw.line(self.screen, (35,35,35), (offset_x+i*CELL, 0), (offset_x+i*CELL, GRID*CELL))

        # UC3: Vẽ chướng ngại vật
        for obs in self.obstacles:
            pygame.draw.rect(
                self.screen, WALL,
                (obs[0]*CELL + 2, obs[1]*CELL + 2, CELL - 4, CELL - 4),
                border_radius=3
            )
            pygame.draw.rect(
                self.screen, (80, 80, 80),
                (obs[0]*CELL + 2, obs[1]*CELL + 2, CELL - 4, CELL - 4),
                2, border_radius=3
            )

        # Vẽ mồi
        for food in self.foods:
            fx, fy = food.x * CELL, food.y * CELL
            if food.big:
                # Mồi to: cam, lớn hơn
                pygame.draw.rect(self.screen, ORANGE,
                                 (fx + 2, fy + 2, CELL - 4, CELL - 4), border_radius=7)
                lbl = self.font_small.render("x2", True, WHITE)
                self.screen.blit(lbl, (fx + 5, fy + 6))
            else:
                pygame.draw.rect(self.screen, RED,
                                 (fx + 5, fy + 5, CELL - 10, CELL - 10), border_radius=5)

        # Vẽ rắn
        self.snake1.draw(self.screen)
        if self.snake2:
            self.snake2.draw(self.screen)

        # Hiệu ứng điểm thưởng
        self._draw_score_popups()

        # HUD
        self._draw_hud()

    # [UC10 - Đặng Tuấn Vũ] Hàm xử lý hiện điểm
    def _draw_hud(self):
        # [Bước 10.1.2] Hệ thống hiển thị bảng điểm trên giao diện trò chơi.
        W, H = self.screen.get_size()
        
        if self.mode == "single":
            # [Bước 10.1.5] Nếu đang ở chế độ 1 người chơi, hệ thống đồng thời hiển thị điểm cao nhất hiện có.
            hud = self.font_small.render(
                f" {self.username}  Score: {self.snake1.score}   Best: {self.scorer.get_high_score(self.username)}   [{self.difficulty.upper()}]",
                True, WHITE)
            self.screen.blit(hud, (5, 5))
        else:
            # [Bước 10.1.6] Nếu đang ở chế độ 2 người chơi, hệ thống hiển thị điểm của cả Người chơi 1 và Người chơi 2.
            board_width = 230
            board_height = 100
            x = W - board_width - 15 
            y = 15
            # Vẽ nền mờ bo góc
            bg_surface = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, (20, 20, 30, 180), (0, 0, board_width, board_height), border_radius=12)
            pygame.draw.rect(bg_surface, (150, 150, 200, 80), (0, 0, board_width, board_height), width=1, border_radius=12)
            self.screen.blit(bg_surface, (x, y))
            # Tiêu đề bảng điểm
            title_txt = self.font_small.render("BẢNG ĐIỂM", True, WHITE)
            self.screen.blit(title_txt, (x + (board_width - title_txt.get_width()) // 2, y + 8))
            pygame.draw.line(self.screen, (100, 100, 150), (x + 15, y + 32), (x + board_width - 15, y + 32), 1)
            # Render tên và điểm số độc lập của 2 người
            p1_color = (100, 255, 120) 
            p2_color = (100, 180, 255)

            p1_txt = self.font_small.render(f"{self.snake1.name}: {self.snake1.score}", True, p1_color)
            p2_txt = self.font_small.render(f"{self.snake2.name}: {self.snake2.score}", True, p2_color)

            # So sánh điểm để quyết định ai nằm trên (đứng đầu), ai nằm dưới
            pos_top = (x + 15, y + 42)
            pos_bottom = (x + 15, y + 70)

            if self.snake1.score >= self.snake2.score:
                # P1 điểm cao hơn hoặc bằng -> P1 đứng đầu
                self.screen.blit(p1_txt, pos_top)
                self.screen.blit(p2_txt, pos_bottom)
            else:
                # P2 điểm cao hơn -> P2 tự động nhảy lên đầu
                self.screen.blit(p2_txt, pos_top)
                self.screen.blit(p1_txt, pos_bottom)

    def _draw_score_popups(self):
        """Vẽ và cập nhật hiệu ứng điểm thưởng bay lên."""
        dt = self.clock.get_time() / 1000.0
        remaining = []
        for popup in self.score_popups:
            px, py, text, color, age, max_age = popup
            age += dt
            if age >= max_age:
                continue  # hết thời gian -> xóa
            # Bay lên 40px trong suốt thời gian hiệu ứng
            progress = age / max_age          # 0.0 -> 1.0
            cur_y = py - progress * 40
            # Mờ dần ở nửa sau
            alpha = 255 if progress < 0.5 else int(255 * (1.0 - progress) * 2)
            surf = self.font_mid.render(text, True, color)
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(int(px), int(cur_y)))
            self.screen.blit(surf, rect)
            popup[4] = age  # cập nhật age
            remaining.append(popup)
        self.score_popups = remaining

    # UC4: Màn hình pause hiện tên người chơi
    def _draw_paused(self):
        W, H  = self.screen.get_size()
        CX, CY = W//2, H//2

        if self._countdown > 0:
            # UC11: Đếm ngược
            overlay = pygame.Surface((W,H), pygame.SRCALPHA)
            overlay.fill((0,0,0,160))
            self.screen.blit(overlay,(0,0))
            num = self.font_big.render(str(self._countdown), True, YELLOW)
            self.screen.blit(num, num.get_rect(center=(CX,CY)))
            msg = self.font_mid.render("Chuẩn bị...", True, WHITE)
            self.screen.blit(msg, msg.get_rect(centerx=CX, y=CY+60))
            return

        if self._pause_alpha < 200:
            self._pause_alpha = min(self._pause_alpha + 15, 200)
        self._pause_tick += 1

        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,self._pause_alpha))
        self.screen.blit(overlay,(0,0))

        panel_w, panel_h = 400, 300
        panel_x = CX - panel_w//2
        panel_y = CY - panel_h//2

        panel = pygame.Surface((panel_w,panel_h), pygame.SRCALPHA)
        panel.fill((10,10,30,min(self._pause_alpha+30,240)))
        self.screen.blit(panel,(panel_x,panel_y))
        pygame.draw.rect(self.screen,(60,60,160),(panel_x,panel_y,panel_w,panel_h),2,border_radius=16)

        pulse = int(math.sin(self._pause_tick*0.06)*27+228)
        title = pygame.font.SysFont('arial',52,bold=True).render("PAUSED",True,(pulse,int(pulse*0.85),0))
        self.screen.blit(title, title.get_rect(centerx=CX, y=panel_y+20))

        # UC4: Hiện tên người chơi
        if self.mode == "single":
            name_txt = self.font_mid.render(f"Người chơi: {self.username}", True, GREEN)
            self.screen.blit(name_txt, name_txt.get_rect(centerx=CX, y=panel_y+88))
        else:
            n1 = self.font_small.render(f"P1: {self.snake1.name}  {self.snake1.score} điểm", True, (100,255,120))
            n2 = self.font_small.render(f"P2: {self.snake2.name}  {self.snake2.score} điểm", True, (100,180,255))
            self.screen.blit(n1, n1.get_rect(centerx=CX, y=panel_y+82))
            self.screen.blit(n2, n2.get_rect(centerx=CX, y=panel_y+108))

        line_y = panel_y + 140
        pygame.draw.line(self.screen,(50,50,120),(panel_x+24,line_y),(panel_x+panel_w-24,line_y),1)

        font_key   = pygame.font.SysFont('arial',20,bold=True)
        font_label = pygame.font.SysFont('arial',20)

        def draw_hint(key_text, desc_text, y):
            key_surf = font_key.render(key_text, True, (20,20,20))
            kw = key_surf.get_width()+18
            kx = CX - 130
            pygame.draw.rect(self.screen,(200,200,60),(kx,y,kw,28),border_radius=6)
            self.screen.blit(key_surf,(kx+9,y+4))
            desc_surf = font_label.render(desc_text, True,(200,200,220))
            self.screen.blit(desc_surf,(kx+kw+14,y+4))

        draw_hint("P",   "Resume",  panel_y+160)
        draw_hint("ESC", "Main Menu",   panel_y+200)

    # UC7: Game over hiện điểm cả 2 người
    def _draw_game_over(self):
        if self._go_alpha < 210:
            self._go_alpha = min(self._go_alpha+12, 210)

        W, H = self.screen.get_size()
        CX = W//2

        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,self._go_alpha))
        self.screen.blit(overlay,(0,0))

        panel_w = 480 if self.mode == "two_player" else 440
        panel_h = 380 if self.mode == "two_player" else 340
        panel_x = CX - panel_w//2
        panel_y = H//2 - panel_h//2 - 10

        panel = pygame.Surface((panel_w,panel_h), pygame.SRCALPHA)
        panel.fill((15,15,25,min(self._go_alpha+20,240)))
        self.screen.blit(panel,(panel_x,panel_y))
        pygame.draw.rect(self.screen,(60,60,100),(panel_x,panel_y,panel_w,panel_h),2,border_radius=16)

        # Title
        if self.mode == "two_player":
            if self._winner == "p1":
                title_str = f"  {self.snake1.name} WIN!"
                title_col = (100,255,120)
            elif self._winner == "p2":
                title_str = f"  {self.snake2.name} WIN!"
                title_col = (100,180,255)
            else:
                title_str = "HOÀ!"
                title_col = YELLOW
        else:
            title_str = "GAME OVER"
            title_col = (220,50,80)

        font_title = pygame.font.SysFont('arial',46,bold=True)
        title = font_title.render(title_str, True, title_col)
        self.screen.blit(title, title.get_rect(centerx=CX, y=panel_y+20))

        line_y = panel_y + 82
        pygame.draw.line(self.screen,(60,60,100),(panel_x+20,line_y),(panel_x+panel_w-20,line_y),1)

        font_label = pygame.font.SysFont('arial',18)
        font_value = pygame.font.SysFont('arial',30,bold=True)

        # UC7: Điểm số
        if self.mode == "single":
            high = self.scorer.get_high_score(self.username)
            sc_lbl = font_label.render("SCORE", True,(140,140,180))
            sc_val = font_value.render(str(self.snake1.score), True, WHITE)
            self.screen.blit(sc_lbl, sc_lbl.get_rect(centerx=CX-90, y=panel_y+96))
            self.screen.blit(sc_val, sc_val.get_rect(centerx=CX-90, y=panel_y+118))
            pygame.draw.line(self.screen,(60,60,100),(CX,panel_y+92),(CX,panel_y+165),1)
            hs_color = YELLOW if self.new_record else (140,140,180)
            hs_lbl = font_label.render("BEST", True, hs_color)
            hs_val = font_value.render(str(high), True, YELLOW if self.new_record else WHITE)
            self.screen.blit(hs_lbl, hs_lbl.get_rect(centerx=CX+90, y=panel_y+96))
            self.screen.blit(hs_val, hs_val.get_rect(centerx=CX+90, y=panel_y+118))
            if self.new_record:
                badge_font = pygame.font.SysFont('arial',14,bold=True)
                badge = badge_font.render("NEW RECORD",True,(20,20,20))
                bw = badge.get_width()+16
                bx = CX+90-bw//2
                by = panel_y+155
                pygame.draw.rect(self.screen,YELLOW,(bx,by,bw,20),border_radius=4)
                self.screen.blit(badge,(bx+8,by+2))
        else:
            # UC7: 2 người - hiện điểm đầy đủ
            col1x = panel_x + panel_w//4
            col2x = panel_x + 3*panel_w//4
            pygame.draw.line(self.screen,(60,60,100),(CX,panel_y+92),(CX,panel_y+200),1)

            for (cx, snake, is_new, col) in [
                (col1x, self.snake1, self.new_record,  (100,255,120)),
                (col2x, self.snake2, self.new_record2, (100,180,255)),
            ]:
                name_lbl = font_label.render(snake.name, True, col)
                sc_lbl   = font_label.render("SCORE",True,(140,140,180))
                sc_val   = font_value.render(str(snake.score), True, WHITE)
                best_val = self.scorer.get_high_score(snake.name)
                best_lbl = font_label.render(f"BEST: {best_val}", True, YELLOW if is_new else (140,140,180))
                self.screen.blit(name_lbl, name_lbl.get_rect(centerx=cx, y=panel_y+92))
                self.screen.blit(sc_lbl,   sc_lbl.get_rect(centerx=cx,   y=panel_y+116))
                self.screen.blit(sc_val,   sc_val.get_rect(centerx=cx,   y=panel_y+136))
                self.screen.blit(best_lbl, best_lbl.get_rect(centerx=cx, y=panel_y+172))
                if is_new:
                    badge_font = pygame.font.SysFont('arial',13,bold=True)
                    badge = badge_font.render("NEW RECORD",True,(20,20,20))
                    bw = badge.get_width()+12
                    bx = cx-bw//2
                    by = panel_y+192
                    pygame.draw.rect(self.screen,YELLOW,(bx,by,bw,18),border_radius=4)
                    self.screen.blit(badge,(bx+6,by+2))

        # Buttons
        btn_y = panel_y + panel_h - 120
        btn_h = 44
        btn_restart = pygame.Rect(panel_x+30, btn_y, 190, btn_h)
        btn_menu    = pygame.Rect(panel_x+panel_w-220, btn_y, 190, btn_h)
        mx, my = pygame.mouse.get_pos()
        self._go_btn_restart = btn_restart
        self._go_btn_menu    = btn_menu

        def draw_btn(rect, label, base, hover):
            color = hover if rect.collidepoint(mx,my) else base
            pygame.draw.rect(self.screen,color,rect,border_radius=10)
            pygame.draw.rect(self.screen,WHITE,rect,1,border_radius=10)
            txt = pygame.font.SysFont('arial',19,bold=True).render(label,True,WHITE)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

        draw_btn(btn_restart,"RESTART",(30,130,60),(40,180,80))
        draw_btn(btn_menu,"MAIN MENU",(50,50,140),(70,70,190))

        hint_font = pygame.font.SysFont('arial',14)
        hint = hint_font.render("SPACE  restart      ESC  back to menu", True,(90,90,120))
        self.screen.blit(hint, hint.get_rect(centerx=CX, y=panel_y+panel_h-32))

    # ── Event handlers ───────────────────────────────────────────
    def _handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pausing:
            if hasattr(self,'_go_btn_restart') and self._go_btn_restart.collidepoint(event.pos):
                self._reset()
            elif hasattr(self,'_go_btn_menu') and self._go_btn_menu.collidepoint(event.pos):
                return True
        return False

    def _handle_key(self, event):
        if event.type != pygame.KEYDOWN:
            return False

        if self._countdown > 0:
            return False

        if not self.pausing:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                if not self.paused:
                    # UC11: đếm ngược khi tiếp tục
                    self._countdown      = 3
                    self._countdown_timer = 0.0
                    self._pause_alpha    = 0
                    self._pause_tick     = 0
            if not self.paused:
                self.snake1.handle_key(event)
                if self.snake2:
                    self.snake2.handle_key(event)

        if event.key == pygame.K_SPACE and self.pausing:
            self._reset()
        if event.key == pygame.K_ESCAPE:
            return True
        return False

    # ── Step logic ───────────────────────────────────────────────
    def _step(self):
        self.snake1.move()
        if self.snake2:
            self.snake2.move()
        self._check_eat()
        self._check_collisions()

    # ── Main loop ────────────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0

            self._draw()
            if self._countdown > 0:
                self._draw_paused()
                self._countdown_timer += dt
                if self._countdown_timer >= 1.0:
                    self._countdown -= 1
                    self._countdown_timer = 0.0
            elif self.paused:
                self._draw_paused()
            elif self.pausing:
                self._draw_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if self._handle_mouse(event):
                    return
                if self._handle_key(event):
                    return

            if not self.pausing and not self.paused and self._countdown == 0:
                self.step_timer += dt
                step_delay = self._calc_speed()
                if self.step_timer >= step_delay:
                    self.step_timer = 0.0
                    self._step()
