import pygame
from leaderboard import Leaderboard

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREEN  = (0,   200, 80)
RED    = (220, 50,  50)
GRAY   = (180, 180, 180)
DARK   = (30,  30,  30)
YELLOW = (255, 220, 0)

class Menu:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.font_big   = pygame.font.SysFont('sans', 48, bold=True)
        self.font_mid   = pygame.font.SysFont('sans', 32)
        self.font_small = pygame.font.SysFont('sans', 22)
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
        masked = "*" * len(value) if "ật" in prompt else value
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
            title = self.font_big.render("🐍  SNAKE GAME", True, GREEN)
            self.screen.blit(title, title.get_rect(centerx=300, y=60))

            mx, my = pygame.mouse.get_pos()
            self._input_box("Tên đăng nhập", 200, username, active_field == "username")
            self._input_box("Mật khẩu",      280, password, active_field == "password")

            self._draw_button("Đăng nhập",  btn_login,    (30, 120, 200), btn_login.collidepoint(mx, my))
            self._draw_button("Đăng ký",    btn_register, (60, 160, 60),  btn_register.collidepoint(mx, my))

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
        """Returns: play | leaderboard | logout | quit"""
        btn_play  = pygame.Rect(200, 220, 200, 50)
        btn_board = pygame.Rect(200, 290, 200, 50)
        btn_out   = pygame.Rect(200, 360, 200, 50)
        btn_quit  = pygame.Rect(200, 430, 200, 50)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("🐍  SNAKE", True, GREEN)
            self.screen.blit(title, title.get_rect(centerx=300, y=80))
            user_lbl = self.font_small.render(f"Xin chào, {username}!", True, YELLOW)
            self.screen.blit(user_lbl, user_lbl.get_rect(centerx=300, y=155))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("▶  Chơi",         btn_play,  (30, 140, 60),  btn_play.collidepoint(mx, my))
            self._draw_button("🏆 Bảng xếp hạng", btn_board, (140, 80, 20),  btn_board.collidepoint(mx, my))
            self._draw_button("🔓 Đăng xuất",     btn_out,   (60, 60, 160),  btn_out.collidepoint(mx, my))
            self._draw_button("✕  Thoát",         btn_quit,  (160, 30, 30),  btn_quit.collidepoint(mx, my))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_play.collidepoint(event.pos):  return "play"
                    if btn_board.collidepoint(event.pos): return "leaderboard"
                    if btn_out.collidepoint(event.pos):   return "logout"
                    if btn_quit.collidepoint(event.pos):  return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"

    # ── UC6: Difficulty ───────────────────────────────────────────────────────
    def show_difficulty_menu(self) -> str | None:
        """Returns: easy | medium | hard | None (back)"""
        btn_easy   = pygame.Rect(200, 230, 200, 50)
        btn_medium = pygame.Rect(200, 300, 200, 50)
        btn_hard   = pygame.Rect(200, 370, 200, 50)
        btn_back   = pygame.Rect(200, 450, 200, 44)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("Độ khó", True, GREEN)
            self.screen.blit(title, title.get_rect(centerx=300, y=130))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("🟢 Dễ",    btn_easy,   (30, 160, 60),  btn_easy.collidepoint(mx, my))
            self._draw_button("🟡 Trung bình", btn_medium, (180, 140, 0), btn_medium.collidepoint(mx, my))
            self._draw_button("🔴 Khó",   btn_hard,   (180, 40, 40),  btn_hard.collidepoint(mx, my))
            self._draw_button("← Quay lại", btn_back, (70, 70, 70),   btn_back.collidepoint(mx, my))

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
    def show_leaderboard(self):
        records = self.leaderboard.get_top(10)
        btn_back = pygame.Rect(200, 530, 200, 44)

        while True:
            self.screen.fill(DARK)
            title = self.font_big.render("🏆 Bảng xếp hạng", True, YELLOW)
            self.screen.blit(title, title.get_rect(centerx=300, y=40))

            for i, (name, score) in enumerate(records):
                color = [YELLOW, GRAY, (205,127,50)][i] if i < 3 else WHITE
                row = self.font_mid.render(f"{i+1:>2}. {name:<15} {score}", True, color)
                self.screen.blit(row, (80, 110 + i * 38))

            if not records:
                empty = self.font_mid.render("Chưa có dữ liệu!", True, GRAY)
                self.screen.blit(empty, empty.get_rect(centerx=300, y=220))

            mx, my = pygame.mouse.get_pos()
            self._draw_button("← Quay lại", btn_back, (70, 70, 70), btn_back.collidepoint(mx, my))
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and btn_back.collidepoint(event.pos):
                    return
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
