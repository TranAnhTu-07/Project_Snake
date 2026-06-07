import pytest

class MockFood:
    def __init__(self, big=False):
        self.big = big
        # Mồi to 2 điểm, mồi thường 1 điểm
        self.value = 2 if big else 1 
        self.position = [0, 0]

    def respawn(self, occupied_cells):
        import random
        while True:
            new_pos = [random.randint(0, 19), random.randint(0, 19)]
            if new_pos not in occupied_cells:
                self.position = new_pos
                break

# [UC10] Test logic gán điểm số đúng theo loại mồi
def test_food_value_assignment():
    normal_food = MockFood(big=False)
    assert normal_food.value == 1, "Mồi thường phải có giá trị là 1 điểm"
    
    big_food = MockFood(big=True)
    assert big_food.value == 2, "Mồi to (BIG) phải có giá trị là 2 điểm"

# [UC09] Test logic sinh mồi tuyệt đối không đè lên vật cản/thân rắn
def test_food_collision_avoidance():
    f = MockFood(big=False)
    occupied = [[x, y] for x in range(20) for y in range(20) if [x, y] != [10, 10]]
    f.respawn(occupied)
    
    # Kết quả mong đợi: Vị trí mồi sinh ra bắt buộc phải lọt vào ô trống duy nhất là [10, 10]
    assert f.position == [10, 10], "Lỗi: Mồi sinh ra đã đè lên ô bị chiếm!"

class MockSnake:
    def __init__(self, name):
        self.name = name
        self.score = 0
        
    def eat(self, food):
        # Cộng điểm dựa vào giá trị của mồi
        self.score += food.value

class MockHUD:
    def __init__(self, mode="single", snake1=None, snake2=None):
        self.mode = mode
        self.snake1 = snake1
        self.snake2 = snake2
        
    def get_score_display(self):
        # Giả lập text hiển thị trên màn hình
        if self.mode == "single":
            return f"Player: {self.snake1.name} - Score: {self.snake1.score}"
        else:
            return f"{self.snake1.name}: {self.snake1.score} | {self.snake2.name}: {self.snake2.score}"

# [UC10] TEST LOGIC CỘNG ĐIỂM VÀ HIỂN THỊ 
def test_score_update_and_display_single_player():
    snake = MockSnake("Tuan Vu")
    hud = MockHUD(mode="single", snake1=snake)
    
    # Kiểm tra điểm ban đầu phải là 0
    assert hud.get_score_display() == "Player: Tuan Vu - Score: 0", "Lỗi: Điểm ban đầu không hiện là 0"
    
    # Cho rắn ăn mồi thường (1 điểm)
    normal_food = MockFood(big=False)
    snake.eat(normal_food)
    
    # Kiểm tra điểm sau khi ăn và text hiển thị
    assert snake.score == 1, "Lỗi: Điểm của rắn chưa được cộng 1!"
    assert hud.get_score_display() == "Player: Tuan Vu - Score: 1", "Lỗi: Giao diện HUD không cập nhật điểm mới!"

def test_score_update_and_display_two_player():
    snake1 = MockSnake("P1")
    snake2 = MockSnake("P2")
    hud = MockHUD(mode="two_player", snake1=snake1, snake2=snake2)
    
    # Rắn 1 ăn mồi to (2 điểm), Rắn 2 ăn mồi thường (1 điểm)
    snake1.eat(MockFood(big=True))
    snake2.eat(MockFood(big=False))
    
    # Kiểm tra text hiển thị của bảng điểm 2 người
    expected_text = "P1: 2 | P2: 1"
    assert hud.get_score_display() == expected_text, "Lỗi: Giao diện 2 người hiển thị sai điểm số!"