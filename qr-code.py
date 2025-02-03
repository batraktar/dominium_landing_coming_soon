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
