Xây dựng hệ CSDL lưu trữ và tìm kiếm ảnh đồ vật:
 
 1.Hãy xây dựng/sưu tầm một bộ dữ liệu ảnh gồm ít nhất 1000 files ảnh đồ vật khác nhau trong nhà, các ảnh có cùng kích thước, vật trong ảnh có cùng tỉ lệ khung hình (SV tùy chọn định dạng ảnh).
 
 2.Hãy xây dựng một bộ thuộc tính để nhận diện ảnh đồ vật từ bộ dữ liệu đã thu thập (gồm các thuộc tính giúp xác định sự tương đồng giữa các đồ vật, và các thuộc tính giúp phân biệt các đồ vật trong các ảnh). Hãy trình bày cụ thể về lý do lựa chọn và giá trị thông tin của các thuộc tính được sử dụng.
 
 3. Hãy xây dựng hệ CSDL để quản lý các siêu dữ liệu đã chọn, trình bày cơ chế tìm kiếm các ảnh đồ vật tương đồng dựa trên các siêu dữ liệu này.
 
 4. Xây dựng hệ thống tìm kiếm ảnh với đầu vào là một ảnh mới về một đồ vật nào đó đã có và không có trong dữ liệu, đầu ra là 5 ảnh giống nhất, xếp thứ tự giảm dần về độ tương đồng nội dung với ảnh đầu vào.
   a.Trình bày sơ đồ khối của hệ thống và quy trình thực hiện yêu cầu của đề bài.
   b.Trình bày các kết quả trung gian trong quá trình tìm kiếm ảnh tương đồng nói trên.
 
 5. Demo hệ thống và đánh giá kết quả đã đạt được.

## Bộ dữ liệu (Dataset)
  Tổng số category: 19  
  Kích thước ảnh sau chuẩn hóa: 224 × 224 pixels  
  Định dạng: JPG (quality 85%)
  Link tải Dataset (Google Drive):
[ Google Drive - Multimedia Dataset](https://drive.google.com/drive/folders/1K9ALrXmWkwbaiqS4PxRDDte0DmI3BjYI?usp=sharing)
## Nội dung thư mục trên Drive:
- `dataset_raw.zip` — Ảnh gốc (raw)
- `dataset_processed.zip` — Ảnh đã chuẩn hóa (224×224, nền trắng)
