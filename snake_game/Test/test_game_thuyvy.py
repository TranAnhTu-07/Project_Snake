import unittest
import pygame
import sys
import os

# Trỏ đường dẫn ngược ra ngoài để gọi được file game.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from game import Game, BASE_SPEED

class TestGameRequirements(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường giả lập trước mỗi lần test"""
        pygame.init()
        self.screen = pygame.Surface((600, 600))
        self.clock = pygame.time.Clock()

    def tearDown(self):
        """Dọn dẹp sau khi test xong"""
        pygame.quit()

    # ==========================================================
    # UC2: CHIA THÀNH 2 CHẾ ĐỘ 1 NGƯỜI VÀ 2 NGƯỜI
    # ==========================================================
    def test_uc2_che_do_1_nguoi(self):
        """Khi bắt đầu trò chơi, nếu là 1 người thì có 1 rắn"""
        game = Game(self.screen, self.clock, username="Player1", difficulty="medium", mode="single")
        
        # Bắt buộc phải có rắn 1
        self.assertIsNotNone(game.snake1, "Lỗi: Chế độ 1 người nhưng không tạo được rắn 1!")
        # Bắt buộc KHÔNG được có rắn 2
        self.assertIsNone(game.snake2, "Lỗi: Chế độ 1 người nhưng lại lòi ra rắn 2!")

    def test_uc2_che_do_2_nguoi(self):
        """Khi bắt đầu trò chơi, nếu 2 thì là 2 rắn"""
        game = Game(self.screen, self.clock, username="Player1", difficulty="medium", mode="two_player", username2="Player2")
        
        # Cả 2 con rắn đều phải xuất hiện
        self.assertIsNotNone(game.snake1, "Lỗi: Chế độ 2 người thiếu rắn 1!")
        self.assertIsNotNone(game.snake2, "Lỗi: Chế độ 2 người thiếu rắn 2!")


    # ==========================================================
    # UC5: MỨC ĐỘ KHÓ DỰA VÀO SỐ ĐIỂM NGƯỜI CHƠI ĐANG CÓ
    # ==========================================================
    def test_uc5_toc_do_tang_khi_diem_cao(self):
        """Điểm càng cao thì tốc độ càng nhanh (thời gian delay giảm xuống)"""
        game = Game(self.screen, self.clock, username="Player1", difficulty="medium", mode="single")
        
        # 1. Lúc mới vô (Điểm = 0): Tốc độ là mặc định
        game.snake1.score = 0
        toc_do_ban_dau = game._calc_speed()
        self.assertEqual(toc_do_ban_dau, BASE_SPEED["medium"])
        
        # 2. Khi ăn được 4 điểm: Tốc độ phải nhanh hơn (delay nhỏ hơn)
        game.snake1.score = 4
        toc_do_muc_1 = game._calc_speed()
        self.assertTrue(toc_do_muc_1 < toc_do_ban_dau, "Lỗi: Điểm tăng nhưng tốc độ không thay đổi!")

        # 3. Khi ăn được 8 điểm: Tốc độ phải nhanh hơn mức 1 nữa
        game.snake1.score = 8
        toc_do_muc_2 = game._calc_speed()
        self.assertTrue(toc_do_muc_2 < toc_do_muc_1, "Lỗi: Điểm càng cao nhưng tốc độ không tăng thêm!")

if __name__ == '__main__':
    unittest.main()
