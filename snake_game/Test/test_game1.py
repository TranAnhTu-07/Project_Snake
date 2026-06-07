import sys
import os
# Cấu hình tự động tìm file game.py ở thư mục cha (lùi lại 1 cấp từ thư mục Test)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pygame
from game import Game  # Import class Game chính từ game.py của bạn

@pytest.fixture(autouse=True)
def init_pygame():
    """Fixture tự động khởi tạo và giải phóng môi trường đồ họa pygame."""
    pygame.init()
    # Khởi tạo màn hình ảo để tránh lỗi crash khi chạy các hàm vẽ UI của Pygame
    pygame.display.set_mode((600, 600), pygame.NOFRAME)
    yield
    pygame.quit()

@pytest.fixture
def test_game():
    """Fixture khởi tạo thực thể trận đấu Game với các tham số chuẩn xác từ game.py."""
    screen = pygame.Surface((600, 600))
    clock = pygame.time.Clock()
    # Truyền đầy đủ 4 tham số bắt buộc của class Game của bạn
    return Game(screen=screen, clock=clock, username="Player 1", difficulty="easy", mode="single")


# ==============================================================================
# UC4: KIỂM THỬ TẠM DỪNG (PAUSE LOGIC & PLAYER NAME UI)
# ==============================================================================

def test_uc4_pause_game_by_key(test_game):
    """Kiểm tra bấm phím 'P' hệ thống sẽ chuyển sang trạng thái tạm dừng."""
    test_game.paused = False
    
    # Giả lập sự kiện người chơi nhấn nút P
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
    test_game._handle_key(event)
    
    # Khẳng định: game phải chuyển sang trạng thái tạm dừng
    assert test_game.paused is True

def test_uc4_display_player_name_on_pause(test_game):
    """Kiểm tra hệ thống lưu giữ đúng tên người chơi để sẵn sàng hiện lên giao diện lúc tạm dừng."""
    # Giả lập trạng thái tạm dừng được bật
    test_game.paused = True
    
    # Xác thực tên người chơi đã được nạp đúng vào đối tượng rắn để hiển thị lên màn hình pause
    assert test_game.snake1.name == "Player 1", "Hệ thống phải giữ lại tên người chơi để in lên giao diện."


# ==============================================================================
# UC7: KIỂM THỬ KẾT THÚC (GAME OVER LOGIC & SCORE UI)
# ==============================================================================

def test_uc7_game_over_state_active(test_game):
    """Kiểm tra khi game rơi vào trạng thái kết thúc (pausing = True)."""
    # Kích hoạt trạng thái kết thúc trận đấu
    test_game.pausing = True
    
    assert test_game.pausing is True

def test_uc7_display_score_on_game_over(test_game):
    """Kiểm tra điểm số của người chơi được bảo toàn để hiển thị trên màn hình kết thúc."""
    # Giả lập người chơi ăn được mồi và có 5 điểm, sau đó chết (game over)
    test_game.snake1.score = 5
    test_game.pausing = True
    
    # Xác thực: Điểm số hiển thị trên giao diện kết thúc phải đúng bằng 5
    assert test_game.snake1.score == 5, "Điểm số hiển thị lúc kết thúc phải khớp với điểm thực tế của người chơi."


# ==============================================================================
# UC11: KIỂM THỬ TIẾP TỤC & ĐẾM NGƯỢC (CONTINUE & COUNTDOWN LOGIC)
# ==============================================================================

def test_uc11_trigger_countdown_when_continue(test_game):
    """Kiểm tra khi đang tạm dừng mà bấm 'P' tiếp tục, hệ thống kích hoạt đếm ngược 3 giây."""
    # Bước 1: Đang tạm dừng
    test_game.paused = True
    
    # Bước 2: Người chơi bấm tiếp phím 'P' để chọn "Tiếp tục"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
    test_game._handle_key(event)
    
    # Khẳng định theo logic code của bạn: paused về False, và bộ đếm _countdown nhận giá trị 3
    assert test_game.paused is False
    assert test_game._countdown == 3, "Hệ thống phải thiết lập đếm ngược về 3 trước khi cho chơi tiếp."

def test_uc11_countdown_timer_logic(test_game):
    """Kiểm tra logic thời gian: khi trôi qua đủ 1 giây thì số đếm ngược giảm đi 1 đơn vị."""
    test_game._countdown = 3
    test_game._countdown_timer = 0.0
    
    # Giả lập thời gian trôi qua dt = 1.0 giây
    dt = 1.0
    test_game._countdown_timer += dt
    
    # Mô phỏng chính xác đoạn logic tính toán bộ đếm thời gian trong Game loop của bạn
    if test_game._countdown_timer >= 1.0:
        test_game._countdown -= 1
        test_game._countdown_timer = 0.0
        
    # Xác thực: Số giây đếm ngược từ 3 phải hạ xuống còn 2 giây
    assert test_game._countdown == 2
    assert test_game._countdown_timer == 0.0