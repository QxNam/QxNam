import re

with open("pre_html.md", "r", encoding="utf-8") as f:
    html_code = f.read()

# Tách các dòng trong thẻ pre
lines = re.findall(r'<pre.*?>(.*?)</pre>', html_code, re.DOTALL)[0].strip().split('\n')

svg_lines = []
font_size = 9
line_height = 11
start_y = 12

max_text_len = 0

for i, line in enumerate(lines):
    y = start_y + (i * line_height)
    matches = re.findall(r'<b style="color:(#(?:[0-9a-fA-F]{3}){1,2})">(.*?)</b>', line)
    
    # Tính độ dài thuần túy của text trên dòng để đo kích thước thực
    line_text_len = sum(len(text) for _, text in matches)
    if line_text_len > max_text_len:
        max_text_len = line_text_len

    tspan_elements = ""
    for color, text in matches:
        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        tspan_elements += f'<tspan fill="{color}">{safe_text}</tspan>'
    
    svg_lines.append(f'  <text x="5" y="{y}" font-family="monospace" font-size="{font_size}px" font-weight="bold">{tspan_elements}</text>')

joined_lines = "\n".join(svg_lines)

# Thiết lập viewBox chuẩn theo kích thước ký tự thực tế (không bị dính thẻ HTML)
total_lines = len(lines)
viewbox_width = int(max_text_len * font_size * 0.6) + 12
viewbox_height = total_lines * line_height + 5

print(f"{viewbox_width=}, {viewbox_height=}")

fig_size = 256
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{fig_size}" height="{fig_size}" viewBox="0 0 {viewbox_width} {viewbox_height}">
  <rect width="100%" height="100%" fill="#ededed" />
{joined_lines}
</svg>
"""

# Lưu ra file svg
with open("images/avatar.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Đã xuất file avatar.svg thành công!")