from PIL import Image, ImageDraw, ImageFont

with open("resources/ascii.md", "r", encoding="utf-8") as f:
    ascii_art = f.read().splitlines()

# 1. Cấu hình font
try:
    font = ImageFont.truetype("Courier", 12)
except IOError:
    font = ImageFont.load_default()

rows = len(ascii_art)
cols = max(len(line) for line in ascii_art) if ascii_art else 0

# 2. Xử lý tỷ lệ ký tự để không bị giãn ngang
bbox = font.getbbox("A")
raw_char_width = bbox[2] - bbox[0]
char_height = bbox[3] - bbox[1] + 4

# NHÂN HỆ SỐ NHỎ HƠN CHO CHIỀU RỘNG (ví dụ 0.6 hoặc 0.65) 
# để bóp chiều ngang của ký tự lại, giúp ảnh không bị bè ra
char_width = max(6, int(raw_char_width * 0.62)) 

padding_x = 20
padding_y = 20

img_width = cols * char_width + padding_x
img_height = rows * char_height + padding_y

# 3. Tạo ảnh và vẽ ký tự với độ rộng đã được co bóp cân đối
image = Image.new("RGB", (img_width, img_height), (255, 255, 255))
draw = ImageDraw.Draw(image)

start_x = 10
start_y = 10

for r, line in enumerate(ascii_art):
    padded_line = line.ljust(cols)
    for c, char in enumerate(padded_line):
        if char != ' ':
            x = start_x + (c * char_width)
            y = start_y + (r * char_height)
            draw.text((x, y), char, fill=(20, 20, 20), font=font)

# 4. Cố định chiều cao (ví dụ: h = 400), chiều rộng tự động co giãn theo tỷ lệ chuẩn mới
target_height = 512
aspect_ratio = img_width / img_height
target_width = int(target_height * aspect_ratio)

final_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

# 5. Lưu kết quả
final_image.save("images/ascii-avatar.png")
print(f"Đã xuất ảnh chuẩn tỷ lệ! Kích thước: {target_width}x{target_height}px")