# BUSINESS REQUIREMENTS SPECIFICATION (BRS)
## Ứng dụng Game Snake (Rắn săn mồi)

---

## 1. Tổng quan dự án (Project Overview)

- **Tên Dự án:** Phát triển ứng dụng Game Snake (Rắn săn mồi)
- **Tên Nhóm:** Nhóm 8
- **Ngày cập nhật:** 22/04/2026
- **Mô tả ngắn:** Xây dựng một trò chơi giải trí cổ điển trên môi trường kỹ thuật số (Web/Mobile/Desktop). Người chơi điều khiển một con rắn để thu thập thức ăn, tăng điểm số và kích thước mà không va chạm với chướng ngại vật hoặc chính thân mình.

---

## 2. Giới thiệu

### 2.1 Mục đích
Tài liệu này mô tả các yêu cầu nghiệp vụ chi tiết cho ứng dụng game Snake, cung cấp cơ sở cho việc thiết kế, phát triển và là kim chỉ nam cho các bên liên quan (Stakeholders).

### 2.2 Phạm vi
Ứng dụng Snake là một trò chơi giải trí đơn giản tập trung vào trải nghiệm mượt mà, tính cạnh tranh thông qua điểm số và khả năng tùy biến mức độ khó.

---

## 3. Phương pháp thu thập yêu cầu (Elicitation Methods)

Dựa trên quá trình phân tích, nhóm đã thực hiện các phương pháp sau:
- **Phỏng vấn (Interviews):** Phỏng vấn người chơi tiềm năng để hiểu mong muốn về tính năng (như tốc độ, chế độ chơi).
- **Phân tích đối thủ (Competitor Analysis):** Chơi thử các phiên bản trên Nokia, Google Doodle và YouTube để rút ra ưu/nhược điểm.
- **Khảo sát (Surveys):** Thu thập ý kiến về việc có nên có tường (biên) hay không và nhịp độ tăng tốc độ của game.

---

## 4. Phân loại mức độ ưu tiên (MoSCoW)

- **Must-have (Bắt buộc):** Di chuyển cơ bản, cơ chế ăn mồi dài ra, tính điểm, xử lý va chạm (Game Over).
- **Should-have (Nên có):** Hiệu ứng âm thanh, lưu kỷ lục điểm cao (High Score).
- **Could-have (Có thể có):** Tự động tăng tốc độ theo điểm số, chọn mức độ Khó/Dễ lúc bắt đầu.
- **Won't-have (Không thực hiện lúc này):** Chế độ 2 người chơi (Multiplayer), mồi đặc biệt (mồi độc, tàng hình).

---

## 5. Mục tiêu kinh doanh & Stakeholders

### 5.1 Mục tiêu kinh doanh
- Tạo sản phẩm giải trí dễ tiếp cận, tăng trải nghiệm người dùng.
- Tối ưu hóa hiệu suất để đạt số lượng người chơi quay lại cao.
- Mở rộng tiềm năng kiếm tiền qua quảng cáo hoặc skin trong tương lai.

### 5.2 Stakeholders
- **Product Owner:** Định hướng sản phẩm và phê duyệt yêu cầu.
- **Developer:** Hiện thực hóa các tính năng kỹ thuật.
- **Designer:** Thiết kế giao diện (UI) và trải nghiệm (UX) trực quan.
- **Người chơi:** Đối tượng trải nghiệm và phản hồi sản phẩm.

---

## 6. Yêu cầu chức năng (Functional Requirements)

### 6.1 Khởi tạo trò chơi
- Thiết lập bảng trò chơi dưới dạng lưới (Grid).
- Rắn xuất hiện tại trung tâm với độ dài mặc định (thường là 3 ô).
- Mồi xuất hiện ngẫu nhiên tại các ô trống (không trùng thân rắn).

### 6.2 Cơ chế di chuyển (Snake Control)
- Rắn tự động di chuyển liên tục theo hướng hiện tại.
- **Điều khiển:** Hỗ trợ phím mũi tên/WASD (PC) hoặc vuốt chạm (Mobile).
- **Ràng buộc:** Không cho phép rắn quay ngược hướng 180 độ ngay lập tức (ví dụ: đang đi lên không thể bấm đi xuống ngay).

### 6.3 Tương tác và Xử lý va chạm (Eating & Collision)
- **Ăn mồi:** Khi đầu rắn trùng vị trí mồi, chiều dài tăng thêm 1 ô, cộng điểm và tạo mồi mới.
- **Điều kiện thua (Game Over):** Khi đầu rắn va chạm vào biên (tường) hoặc va chạm vào chính thân mình.

### 6.4 Hệ thống điểm số (Scoring)
- Hiển thị điểm số hiện tại ngay trên màn hình trong khi đang chơi.
- Lưu trữ và hiển thị điểm cao nhất (High Score) sau mỗi lượt chơi.

### 6.5 Tùy chỉnh (Settings)
- Cho phép người dùng chọn mức độ khó dựa trên tốc độ di chuyển của rắn: Chậm, Trung bình, Nhanh.

### 6.6 Quản lý trạng thái trò chơi (Game State Management)
- **Tạm dừng/Tiếp tục (Pause/Resume):** Cho phép người dùng tạm dừng trò chơi bất kỳ lúc nào thông qua nút bấm trên giao diện hoặc phím tắt và tiếp tục lại ngay tại trạng thái đó.
- **Chơi lại nhanh (Quick Restart):** Cung cấp tùy chọn cho phép người chơi bắt đầu lại một ván mới ngay lập tức sau khi Game Over mà không cần quay lại màn hình chính.
- **Thoát (Quit):** Cho phép người dùng dừng ván chơi hiện tại để quay trở về Menu chính của ứng dụng.

### 6.7 Hệ thống âm thanh và Phản hồi (Audio & Feedback)
- **Hiệu ứng âm thanh:** Hệ thống phát âm thanh ngắn khi rắn ăn mồi thành công và phát âm thanh thông báo khi xảy ra va chạm dẫn đến kết thúc trò chơi.
- **Điều chỉnh âm lượng:** Cung cấp tính năng bật/tắt (Toggle) âm thanh và nhạc nền trong menu cài đặt để phù hợp với nhu cầu người dùng.

### 6.8 Giao diện và Hiệu ứng hình ảnh (UI/UX)
- **Màn hình Menu chính:** Hiển thị các tùy chọn: Bắt đầu chơi (Start), Cài đặt (Settings), Xem điểm cao (High Score) và Thoát (Exit).
- **Màn hình thông báo kết quả:** Hiển thị rõ ràng thông báo "Game Over", số điểm người chơi vừa đạt được và cập nhật kỷ lục mới nếu có.
- **Hiệu ứng đồ họa:** Hiển thị màu sắc phân biệt giữa đầu rắn, thân rắn và thức ăn để người chơi dễ dàng quan sát trên lưới trò chơi.

### 6.9 Tính năng nâng cao (Tùy chọn mở rộng)
- **Tự động tăng tốc:** Hệ thống tự động tăng dần tốc độ di chuyển của rắn sau khi người chơi đạt đến một mốc điểm nhất định để tăng độ thử thách.
- **Hệ thống chướng ngại vật:** Thiết lập các vật cản cố định trên bản đồ tại các cấp độ khó hơn để người chơi phải điều hướng khéo léo hơn.
- **Lưu trữ đám mây:** Hỗ trợ liên kết tài khoản (Google/Facebook) để lưu trữ điểm cao nhất trên hệ thống, cho phép đồng bộ hóa giữa các thiết bị khác nhau.

---

## 7. Yêu cầu phi chức năng (Non-Functional Requirements)

- **Hiệu năng:** Game chạy mượt ≥ 60 FPS, không giật lag ngay cả khi rắn rất dài. Tốc độ tải ứng dụng < 2 giây.
- **Tính khả dụng:** Giao diện tối giản, trực quan, người mới chơi không cần đọc hướng dẫn vẫn hiểu cách chơi.
- **Tương thích:** Chạy tốt trên trình duyệt (Chrome, Safari, Edge) và các hệ điều hành phổ biến (Android, iOS, Windows, macOS).
- **Độ tin cậy:** Không bị crash giữa chừng; tính năng Pause hoạt động chính xác và không gây lỗi logic game.

---

## 8. Rủi ro và Hướng phát triển

### 8.1 Rủi ro
- **Performance:** Giật lag trên các thiết bị cấu hình quá yếu khi thân rắn quá dài.
- **UX:** Cảm giác điều khiển bằng vuốt (swipe) trên mobile có thể không phản hồi nhanh bằng phím bấm vật lý.

### 8.2 Hướng phát triển tương lai
- Hệ thống Leaderboard online để cạnh tranh toàn cầu.
- Cửa hàng (Store) mua skin đa dạng cho rắn và phông nền bản đồ bằng điểm số (Coins) hoặc IAP.
- Tích hợp quảng cáo (Rewarded Ads) để có thêm 1 cơ hội hồi sinh (Revive).

---

## 9. Phụ lục: Luồng hoạt động (Basic Flow)
1. Người chơi mở ứng dụng và chọn **Bắt đầu chơi (Start)**.
2. (Tùy chọn) Chọn mức độ khó (Chậm/Trung bình/Nhanh).
3. Rắn di chuyển và người chơi điều hướng để ăn mồi.
4. Rắn ăn mồi -> Chiều dài tăng -> Điểm số tăng -> Phát âm thanh ăn mồi.
5. Rắn va chạm (tường hoặc thân) -> Phát âm thanh thua -> **Game Over**.
6. Hiển thị điểm số hiện tại và High Score.
7. Người chơi chọn **Chơi lại (Restart)** để tiếp tục ván mới hoặc **Thoát (Quit)** để về Menu chính.
