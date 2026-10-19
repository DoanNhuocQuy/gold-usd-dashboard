# Quý Market — Vàng & USD/VND
Dashboard tiếng Việt, không cần cài thư viện: mở qua máy chủ HTTP hoặc GitHub Pages.

## Đưa lên GitHub
1. Tạo repository `gold-usd-dashboard` trên tài khoản của anh. Với GitHub Free, chọn Public để sử dụng Pages. Các file code và dữ liệu trong repo Public sẽ công khai.
2. Giải nén, đưa **nội dung bên trong thư mục** vào gốc repo, gồm cả `.github/workflows/`, và commit lên nhánh `main`.
3. Settings → Pages → Build and deployment → Source → **GitHub Actions**.
4. Actions → **Publish GitHub Pages** → Run workflow. URL được trả trong job Deploy; dạng `https://DoanNhuocQuy.github.io/gold-usd-dashboard/` chỉ khả dụng sau khi deploy thành công.
5. Workflow **Update market history and publish** chạy lúc 07:17 giờ Việt Nam từ thứ Hai đến thứ Bảy. Có thể chạy thủ công từ Actions. GitHub có thể trì hoãn hoặc tắt lịch trên repo không hoạt động; nút cập nhật trong app không kích hoạt workflow.

Nếu kết nối ChatGPT chưa thấy repo: cấp quyền cho GitHub app truy cập repo mới, rồi gửi link repo để tiếp tục triển khai.

## Dữ liệu và giới hạn
- Ô vàng hiện tại: Gold API `/price/XAU`, USD/troy ounce, lấy lại tối đa mỗi 30 giây. Tự cập nhật mỗi 60 giây chỉ chạy khi trang được mở và hiển thị. Báo lỗi khi nguồn lỗi, giữ nguyên thời điểm của dữ liệu cũ.
- USD/VND: Frankfurter v2, tỷ giá tham khảo tổng hợp theo ngày; không phải giá mua/bán Vietcombank, tỷ giá tự do hay giá tick realtime. Bấm cập nhật chỉ lấy số liệu mới nhất mà nguồn đã công bố.
- Lịch sử vàng: Yahoo Finance **COMEX Gold Futures GC=F**, giá đóng cửa chưa điều chỉnh. Đây là **hợp đồng kỳ hạn**, khác vàng giao ngay và vàng SJC/nhẫn. Không ghép giá spot vào chuỗi futures. Hợp đồng luân chuyển có thể gây bước nhảy; phiên gần nhất có thể chưa chốt.
- Lịch sử USD/VND: Frankfurter daily. Hai chuỗi có lịch phiên riêng. Chart lọc tối đa 10 năm tính từ ngày mở trang, không tạo hay nội suy thêm báo giá. Bảng và CSV chỉ lấy 1 năm gần nhất, CSV luôn chứa cả năm, không phụ thuộc tìm ngày hoặc phân trang.
- Giá vàng quy đổi VND/lượng = USD/oz × VND/USD × 37.5 / 31.1034768. Không gồm thuế, phí hay chênh lệch thị trường nội địa.
- Không dùng dữ liệu mẫu. `data/` chứa báo giá thực đã tải và thời điểm tải của từng chuỗi. Lịch sử được workflow cập nhật theo ngày; nút trong app tải lại bản đã xuất bản.
- Nếu nhà cung cấp chặn truy cập, đổi schema hoặc ngừng dịch vụ, app hiển thị lỗi/giữ snapshot có nhãn thời gian. Workflow thất bại sẽ không ghi đè lịch sử tốt bằng mảng rỗng.
- Yahoo có thể giới hạn truy cập; cần nguồn dữ liệu được cấp phép nếu dùng thương mại hoặc yêu cầu SLA. Chưa có khóa API, tài khoản hay dữ liệu cá nhân trong mã nguồn.

## Chạy tại máy
```bash
python -m http.server 8080
```
Mở http://localhost:8080. Không mở bằng `file://` vì trình duyệt chặn tải dữ liệu/module.

## Làm mới lịch sử
```bash
python scripts/update_data.py
```
Yêu cầu Python 3.10+. Không có dependencies ngoài thư viện chuẩn.
