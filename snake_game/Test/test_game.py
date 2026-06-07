import pytest
import pygame
from game import Snake, P1_KEYS

@pytest.fixture(autouse=True)
def init_pygame():
    """Fixture tự động khởi tạo và giải phóng pygame cho mỗi test case."""
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def test_snake():
    """Fixture khởi tạo một thực thể Snake mặc định để test."""
    return Snake(
        start_pos=[4, 10], 
        start_dir="right",
        color_body=(0, 210, 80), 
        color_head=(100, 255, 120),
        name="Test Player", 
        keys=P1_KEYS
    )

# TEST CẬP NHẬT VỊ TRÍ (MOVE LOGIC)

def test_snake_initial_state(test_snake):
    """Kiểm tra trạng thái khởi tạo ban đầu của rắn."""
    assert test_snake.body == [[4, 10]]
    assert test_snake.direction == "right"
    assert test_snake.grow == 1
    assert test_snake.alive is True

def test_snake_move_with_grow(test_snake):
    """Kiểm tra di chuyển khi thuộc tính grow > 0 (rắn dài thêm, không mất đuôi)."""
    # Ban đầu grow = 1, di chuyển sang phải
    test_snake.move()
    
    # Đầu mới phải là [5, 10]
    assert test_snake.body[-1] == [5, 10]
    # Vì grow > 0 nên đuôi cũ [4, 10] vẫn giữ nguyên, độ dài tăng lên 2
    assert test_snake.body == [[4, 10], [5, 10]]
    # Thuộc tính grow giảm đi 1 đơn vị
    assert test_snake.grow == 0

def test_snake_move_without_grow(test_snake):
    """Kiểm tra di chuyển bình thường khi grow = 0 (đuôi cũ bị xóa)."""
    test_snake.move() # Bước 1: grow giảm từ 1 về 0. Body lúc này: [[4,10], [5,10]]
    
    # Bước 2: Di chuyển tiếp khi grow = 0
    test_snake.move() # Đầu mới: [6, 10]. Đuôi cũ [4, 10] phải bị xóa.
    
    assert test_snake.body == [[5, 10], [6, 10]]
    assert test_snake.body[-1] == [6, 10]

@pytest.mark.parametrize("direction, expected_head", [
    ("right", [5, 10]),
    ("left",  [3, 10]),
    ("up",    [4, 9]),
    ("down",  [4, 11]),
])
def test_snake_move_all_directions(test_snake, direction, expected_head):
    """Kiểm tra tọa độ đầu rắn thay đổi chính xác theo cả 4 hướng."""
    test_snake.direction = direction
    test_snake.next_dir = direction
    test_snake.move()
    assert test_snake.body[-1] == expected_head


# TEST ĐIỀU KHIỂN (KEY HANDLING LOGIC)
def test_handle_key_valid_turn(test_snake):
    """Kiểm tra rẽ hướng hợp lệ (đang đi 'right' rẽ sang 'up')."""
    # Giả lập sự kiện nhấn phím 'W' (Đi lên trong P1_KEYS)
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
    test_snake.handle_key(event)
    
    # Hướng dự kiến (next_dir) phải được cập nhật thành 'up'
    assert test_snake.next_dir == "up"
    
    # Sau khi gọi hàm move(), hướng chính thức (direction) mới thay đổi
    test_snake.move()
    assert test_snake.direction == "up"
    assert test_snake.body[-1] == [4, 9] # Tọa độ x giữ nguyên, y giảm 1

def test_handle_key_invalid_opposite_turn(test_snake):
    """Kiểm tra chặn quay đầu 180 độ đột ngột (đang đi 'right' cố tình rẽ 'left')."""
    # Giả lập nhấn phím 'A' (Đi sang trái)
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
    test_snake.handle_key(event)
    
    # Hệ thống phải chặn lại, next_dir giữ nguyên là 'right'
    assert test_snake.next_dir == "right"
    
    test_snake.move()
    assert test_snake.direction == "right"
    assert test_snake.body[-1] == [5, 10]

def test_handle_key_unregistered_key(test_snake):
    """Kiểm tra khi bấm các phím không nằm trong bộ điều khiển (ví dụ: SPACE)."""
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    test_snake.handle_key(event)
    
    # Không có gì thay đổi
    assert test_snake.next_dir == "right"

def test_handle_non_keydown_event(test_snake):
    """Kiểm tra hệ thống bỏ qua nếu sự kiện không phải là KEYDOWN (ví dụ: MOUSEBUTTONDOWN)."""
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
    test_snake.handle_key(event)
    
    assert test_snake.next_dir == "right"