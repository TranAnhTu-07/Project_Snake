import pygame
import os
from leaderboard import Leaderboard

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREEN  = (0,   200, 80)
RED    = (220, 50,  50)
GRAY   = (180, 180, 180)
DARK   = (30,  30,  30)
YELLOW = (255, 220, 0)
def resource_path(relative_path):
    """Lấy đường dẫn đúng cả khi chạy .py lẫn .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class Menu:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FONT = os.path.join(BASE_DIR, "fonts", "Roboto-Regular.ttf")
        self.font_big   = pygame.font.Font(FONT, 48)
        self.font_mid   = pygame.font.Font(FONT, 32)
        self.font_small = pygame.font.Font(FONT, 22)
        self.leaderboard = Leaderboard()

    # ── helpers ──────────────────────────────────────────────────────────────
    def _draw_button(self, text, rect, color, hover=False):
        shade = tuple(min(c + 40, 255) for c in color) if hover else color
        pygame.draw.rect(self.screen, shade, rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8)
        lbl = self.font_mid.render(text, True, WHITE)
        self.screen.blit(lbl, lbl.get_rect(center=rect.center))

    def _input_box(self, prompt, y, value, active):
        color = GREEN if active else GRAY
        lbl = self.font_small.render(prompt, True, WHITE)
        self.screen.blit(lbl, (100, y - 28))
        rect = pygame.Rect(100, y, 400, 40)
        pygame.draw.rect(self.screen, DARK, rect, border_radius=6)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=6)
        masked = "*" * len(value) if "Password" in prompt else value
        txt = self.font_small.render(masked, True, WHITE)
        self.screen.blit(txt, (rect.x + 8, rect.y + 8))
        return rect

    # ── UC1 / UC2: Auth screen ────────────────────────────────────────────────
    def show_auth_screen(self) -> tuple[str, str, str]:
        """Returns (action, username, password)  action ∈ {login, register, quit}"""
        username, password = "", ""
        active_field = "username"
        message = ""
        msg_color = WHITE

        btn_login    = pygame.Rect(100, 390, 180, 44)
        btn_register = pygame.Rect(320, 390, 180, 44)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("SNAKE GAME", True, GREEN)
            self.screen.blit(title, title.get_rect(centerx=300, y=60))

            mx, my = pygame.mouse.get_pos()
            self._input_box("Username", 200, username, active_field == "username")
            self._input_box("Password",      280, password, active_field == "password")

            self._draw_button("Login",  btn_login,    (30, 120, 200), btn_login.collidepoint(mx, my))
            self._draw_button("Register",    btn_register, (60, 160, 60),  btn_register.collidepoint(mx, my))

            if message:
                msg_surf = self.font_small.render(message, True, msg_color)
                self.screen.blit(msg_surf, msg_surf.get_rect(centerx=300, y=450))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", "", ""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(100, 200, 400, 40).collidepoint(event.pos):
                        active_field = "username"
                    elif pygame.Rect(100, 280, 400, 40).collidepoint(event.pos):
                        active_field = "password"
                    elif btn_login.collidepoint(event.pos):
                        return "login", username, password
                    elif btn_register.collidepoint(event.pos):
                        return "register", username, password
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        active_field = "password" if active_field == "username" else "username"
                    elif event.key == pygame.K_RETURN:
                        return "login", username, password
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == "username":
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    else:
                        char = event.unicode
                        if char and len(char) == 1:
                            if active_field == "username" and len(username) < 20:
                                username += char
                            elif active_field == "password" and len(password) < 20:
                                password += char

    # ── UC3: Main menu ────────────────────────────────────────────────────────
    def show_main_menu(self, username: str) -> str:
        btn_play1 = pygame.Rect(150, 200, 300, 52)
        btn_play2 = pygame.Rect(150, 268, 300, 52)
        btn_board = pygame.Rect(150, 336, 300, 52)
        btn_out   = pygame.Rect(150, 404, 300, 52)
        btn_quit  = pygame.Rect(150, 472, 300, 52)

        while True:
            self.screen.fill((30,  30,  30)) # Màu DARK
            title = self.font_big.render("SNAKE", True, (0, 200, 80))
            self.screen.blit(title, title.get_rect(centerx=300, y=70))
            user_lbl = self.font_small.render(f"Hello, {username}!", True, (255, 220, 0))
            self.screen.blit(user_lbl, user_lbl.get_rect(centerx=300, y=152))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("1 Player",   btn_play1, (30,140,60),  btn_play1.collidepoint(mx,my))
            self._draw_button("2 Players",   btn_play2, (20,80,180),  btn_play2.collidepoint(mx,my))
            self._draw_button("Leaderboard",     btn_board, (140,80,20),  btn_board.collidepoint(mx,my))
            self._draw_button("Logout",          btn_out,   (60,60,160),  btn_out.collidepoint(mx,my))
            self._draw_button("Quit",              btn_quit,  (160,30,30),  btn_quit.collidepoint(mx,my))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_play1.collidepoint(event.pos): return "play1"
                    if btn_play2.collidepoint(event.pos): return "play2"
                    if btn_board.collidepoint(event.pos): return "leaderboard"
                    if btn_out.collidepoint(event.pos):   return "logout"
                    if btn_quit.collidepoint(event.pos):  return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"
                
    # ── UC2: Nhập tên người chơi 2 ───────────────────────────────
    def show_player2_name(self, username1: str) -> str | None:
        name2 = ""
        message = ""
        btn_ok   = pygame.Rect(150, 380, 130, 44)
        btn_back = pygame.Rect(320, 380, 130, 44)

        while True:
            self.screen.fill((30,  30,  30)) # DARK
            title = self.font_mid.render("2 Players", True, (0, 220, 220)) # CYAN
            self.screen.blit(title, title.get_rect(centerx=300, y=80))

            # Hướng dẫn phím
            font_sm = self.font_small
            self.screen.blit(font_sm.render(f"Player 1: {username1}", True, (100,255,120)), (100,160))
            self.screen.blit(font_sm.render("Controls: WASD", True, (100,255,120)), (100,185))
            pygame.draw.line(self.screen, (180, 180, 180), (80,220),(520,220), 1)
            self.screen.blit(font_sm.render("Player 2 Name:", True, (255, 255, 255)), (100,240))
            self.screen.blit(font_sm.render("Controls: Arrows", True, (100,180,255)), (100,265))

            # Input box P2
            rect2 = pygame.Rect(100, 305, 400, 40)
            pygame.draw.rect(self.screen, (30, 30, 30), rect2, border_radius=6)
            pygame.draw.rect(self.screen, (30, 120, 255), rect2, 2, border_radius=6)
            txt = font_sm.render(name2, True, (255, 255, 255))
            self.screen.blit(txt, (rect2.x+8, rect2.y+8))

            if message:
                self.screen.blit(font_sm.render(message, True, (220, 50, 50)), (100, 355))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("Start", btn_ok,   (30,140,60),  btn_ok.collidepoint(mx,my))
            self._draw_button("Back",btn_back,  (70,70,70),   btn_back.collidepoint(mx,my))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_ok.collidepoint(event.pos):
                        if not name2.strip(): message = "Please enter Player 2's name!"
                        elif name2.strip() == username1: message = "Name cannot be the same as Player 1!"
                        else: return name2.strip()
                    elif btn_back.collidepoint(event.pos): return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name2.strip() and name2.strip() != username1: return name2.strip()
                        else: message = "Invalid name!"
                    elif event.key == pygame.K_BACKSPACE: name2 = name2[:-1]
                    elif event.key == pygame.K_ESCAPE: return None
                    else:
                        char = event.unicode
                        if char and len(char)==1 and len(name2)<20: name2 += char

    # ── UC6: Difficulty ───────────────────────────────────────────────────────
    def show_difficulty_menu(self) -> str | None:
        """Returns: easy | medium | hard | None (back)"""
        btn_easy   = pygame.Rect(200, 230, 200, 50)
        btn_medium = pygame.Rect(200, 300, 200, 50)
        btn_hard   = pygame.Rect(200, 370, 200, 50)
        btn_back   = pygame.Rect(200, 450, 200, 44)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("Difficulty", True, GREEN)
            self.screen.blit(title, title.get_rect(centerx=300, y=130))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("Easy",    btn_easy,   (30, 160, 60),  btn_easy.collidepoint(mx, my))
            self._draw_button("Medium", btn_medium, (180, 140, 0), btn_medium.collidepoint(mx, my))
            self._draw_button("Hard",   btn_hard,   (180, 40, 40),  btn_hard.collidepoint(mx, my))
            self._draw_button("Back", btn_back, (70, 70, 70),   btn_back.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_easy.collidepoint(event.pos):   return "easy"
                    if btn_medium.collidepoint(event.pos): return "medium"
                    if btn_hard.collidepoint(event.pos):   return "hard"
                    if btn_back.collidepoint(event.pos):   return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None

    # ── UC7: Leaderboard ──────────────────────────────────────────────────────
    # ── Leaderboard ───────────────────────────────────────────────
    def show_leaderboard(self):
        top_players = self.leaderboard.get_top(10)
        btn_back = pygame.Rect(200, 520, 200, 44)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("Leaderboard", True, YELLOW)
            self.screen.blit(title, title.get_rect(centerx=300, y=50))

            if not top_players:
                msg = self.font_mid.render("No data available!", True, WHITE)
                self.screen.blit(msg, msg.get_rect(centerx=300, y=250))
            else:
                for i, (name, score) in enumerate(top_players):
                    y = 120 + i * 35
                    # Chỉnh màu cho Top 1, 2, 3 nhìn cho xịn
                    if i == 0: color = YELLOW       # Vàng cho Top 1
                    elif i == 1: color = (192,192,192) # Bạc cho Top 2
                    elif i == 2: color = (205,127,50)  # Đồng cho Top 3
                    else: color = WHITE             # Trắng cho dân thường

                    # TÁCH LÀM 2 PHẦN ĐỂ CĂN LỀ:
                    # 1. Vẽ Tên (Căn trái ở tọa độ x = 140)
                    name_lbl = self.font_mid.render(f"{i+1}. {name}", True, color)
                    self.screen.blit(name_lbl, (140, y))

                    # 2. Vẽ Điểm (Căn phải sao cho đít của chữ điểm luôn nằm ở x = 460)
                    score_lbl = self.font_mid.render(str(score), True, color)
                    score_rect = score_lbl.get_rect(right=460, top=y)
                    self.screen.blit(score_lbl, score_rect)

            mx, my = pygame.mouse.get_pos()
            self._draw_button("Back", btn_back, (70,70,70), btn_back.collidepoint(mx,my))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_back.collidepoint(event.pos): return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

    # ── Utility ───────────────────────────────────────────────────────────────
    def show_message(self, message: str, duration_ms: int = 1800):
        overlay = pygame.Surface((601, 601), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        msg = self.font_mid.render(message, True, WHITE)
        self.screen.blit(msg, msg.get_rect(center=(300, 300)))
        pygame.display.flip()
        pygame.time.delay(duration_ms)
