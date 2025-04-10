import qrcode
from PIL import ImageDraw, ImageFont

# Дані для QR-коду
data = "https://3dtour.ua/files/2025/00_AUTO/maison/02_11/1/3Dtour_fin/"
text = "3D Тур"

# Створення QR-коду
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Підключення шрифту Calibri Bold
font_path = "/Users/mac/Desktop/DOMINIUM_REALTY_AGENCY/web-projects/site/landing_doominium_real_state/calibri_bold.ttf"
font_size = 40
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception as e:
    print(f"⚠️ Помилка підключення шрифту: {e}")
    font = ImageFont.load_default()

# Накладання тексту
draw = ImageDraw.Draw(img_qr)
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
img_width, img_height = img_qr.size
position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

# Білий прямокутник під текст (з більшим padding)
padding = 23
corner_radius = 10
rect_coords = [
    position[0] - padding,
    position[1] - padding,
    position[0] + text_width + padding,
    position[1] + text_height + padding
]
draw.rounded_rectangle(rect_coords, radius=corner_radius, fill="white")

# Текст
draw.text(position, text, font=font, fill="black")

# Показ та збереження
img_qr.show()
img_qr.save("qr_with_calibri_text.png")
