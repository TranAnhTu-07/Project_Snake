# BUSINESS REQUIREMENTS SPECIFICATION (BRS)
## Ứng dụng Game Snake (Rắn săn mồi)

---

## 1. Giới thiệu

### 1.1 Mục đích
Tài liệu này mô tả các yêu cầu nghiệp vụ cho ứng dụng game Snake (Rắn săn mồi), nhằm cung cấp cơ sở cho việc thiết kế, phát triển và triển khai hệ thống.

### 1.2 Phạm vi
Ứng dụng Snake là một trò chơi giải trí đơn giản, nơi người chơi điều khiển con rắn để ăn thức ăn, tăng điểm và tránh va chạm.

### 1.3 Định nghĩa
- Snake: Con rắn do người chơi điều khiển
- Food: Thức ăn xuất hiện ngẫu nhiên
- Score: Điểm số của người chơi

---

## 2. Tổng quan hệ thống

### 2.1 Mô tả chung
Ứng dụng là một game đơn giản có thể chạy trên:
- Web
- Mobile (Android/iOS)
- Desktop

### 2.2 Đối tượng người dùng
- Người chơi casual (giải trí)
- Học sinh, sinh viên
- Người dùng yêu thích game cổ điển

---

## 3. Mục tiêu kinh doanh

- Tạo một sản phẩm giải trí đơn giản, dễ tiếp cận
- Tăng trải nghiệm người dùng
- Có thể mở rộng kiếm tiền (quảng cáo, premium)
- Tăng lượt tải và sử dụng

---

## 4. Stakeholders

| Stakeholder        | Vai trò |
|--------------------|--------|
| Product Owner      | Định hướng sản phẩm |
| Developer          | Phát triển hệ thống |
| Designer           | Thiết kế UI/UX |
| Người chơi         | Sử dụng ứng dụng |

---

## 5. Yêu cầu nghiệp vụ (Business Requirements)

### 5.1 Gameplay cơ bản
- Người chơi điều khiển rắn di chuyển theo 4 hướng:
  - Lên / Xuống / Trái / Phải
- Rắn sẽ:
  - Dài ra khi ăn thức ăn
  - Tăng điểm

### 5.2 Điều kiện thắng/thua
- Thua khi:
  - Va vào tường
  - Va vào chính mình
- Game kết thúc và hiển thị điểm

### 5.3 Hệ thống điểm
- Mỗi thức ăn = +1 điểm (hoặc tùy chỉnh)
- Lưu điểm cao nhất (High Score)

### 5.4 Tốc độ game
- Tăng dần theo thời gian hoặc theo điểm

### 5.5 Chế độ chơi
- Chơi đơn (Single Player)
- Có thể mở rộng:
  - Endless mode
  - Level mode

---

## 6. Functional Requirements

### 6.1 Điều khiển
- Bàn phím (PC): Arrow keys / WASD
- Cảm ứng (Mobile): Swipe

### 6.2 Hiển thị
- Hiển thị:
  - Rắn
  - Thức ăn
  - Điểm số
  - Game Over

### 6.3 Hệ thống lưu trữ
- Lưu:
  - High score
- Có thể lưu local hoặc cloud

### 6.4 Restart game
- Cho phép chơi lại sau khi thua

---

## 7. Non-Functional Requirements

### 7.1 Hiệu năng
- Game chạy mượt ≥ 30 FPS
- Load nhanh (< 2 giây)

### 7.2 Khả dụng (Usability)
- Dễ chơi, dễ hiểu
- UI đơn giản

### 7.3 Tương thích
- Hỗ trợ nhiều thiết bị:
  - Mobile
  - Desktop
  - Browser

### 7.4 Bảo mật
- Không yêu cầu cao (trừ khi có tài khoản)

---

## 8. UI/UX Requirements

- Giao diện đơn giản, trực quan
- Màu sắc dễ nhìn
- Hiển thị rõ:
  - Điểm
  - Game Over
- Có âm thanh (tùy chọn):
  - Khi ăn
  - Khi thua

---

## 9. Ràng buộc (Constraints)

- Phải hoạt động offline (nếu là local game)
- Giới hạn tài nguyên thiết bị
- Đơn giản, nhẹ

---

## 10. Giả định (Assumptions)

- Người chơi biết cách điều khiển cơ bản
- Thiết bị có đủ hiệu năng tối thiểu
- Không yêu cầu kết nối internet (trừ khi có leaderboard online)

---

## 11. Rủi ro (Risks)

| Rủi ro | Mô tả |
|--------|------|
| Performance | Game lag trên thiết bị yếu |
| UX | Điều khiển khó trên mobile |
| Retention | Người chơi nhanh chán |

---

## 12. Hướng phát triển tương lai

- Multiplayer
- Leaderboard online
- Skin cho rắn
- Chế độ chơi mới (speed, survival)
- Tích hợp quảng cáo hoặc in-app purchase

---

## 13. Tiêu chí thành công

- Game chạy ổn định
- UX tốt
- Có người chơi quay lại
- Đạt số lượt tải mong muốn

---

## 14. Phụ lục

### 14.1 Luồng cơ bản
1. Start game
2. Điều khiển rắn
3. Ăn thức ăn → tăng điểm
4. Va chạm → Game Over
5. Restart

---
