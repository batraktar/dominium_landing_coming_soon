import qrcode

# Дані для QR-коду
data = "dominium.com.ua"

# Створення QR-коду
qr = qrcode.QRCode(box_size=500, border=5)
qr.add_data(data)
qr.make(fit=True)

# Генерація зображення
img = qr.make_image(fill="black", back_color="white")
img.show()  # Відкриє QR-код
img.save("dominium-qr-code.png")  # Збереже зображення



import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Отримуємо шлях до поточної папки
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Папка, де лежить manage.py

print(PROJECT_ROOT)  # Це і є Application root

