import os
import django

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async  # ← ось що додаємо

# Імпорт налаштувань Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_doominium_real_state.settings')
django.setup()

from accounts.models import CustomUser, TelegramVerification

# 🔐 Токен бота з BotFather
BOT_TOKEN = '7630269852:AAHqi0XBWhfcPjrJElFij0mFY4BSfM51PJY'

# 👇 Ця функція буде безпечно працювати з ORM у async-контексті
@sync_to_async
def get_verification_for_user(tg_username):
    user = CustomUser.objects.get(telegram_username=tg_username)
    verification = TelegramVerification.objects.filter(user=user, is_used=False).latest('created_at')
    return verification

# 👋 Обробка команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_username = update.effective_user.username

    try:
        verification = await get_verification_for_user(tg_username)
    except CustomUser.DoesNotExist:
        await update.message.reply_text("❌ Користувача з таким telegram_username не знайдено. Зареєструйся на сайті.")
        return
    except TelegramVerification.DoesNotExist:
        await update.message.reply_text("⚠️ Тобі ще не згенеровано код підтвердження.")
        return

    # 🔗 Кнопка для підтвердження акаунта
    confirm_url = f"http://192.168.0.142:8000/verify/{verification.code}/"  # ← виправлено на http
    button = InlineKeyboardButton("✅ Підтвердити акаунт", url=confirm_url)
    markup = InlineKeyboardMarkup([[button]])

    await update.message.reply_text("👋 Привіт! Натисни кнопку нижче, щоб підтвердити реєстрацію:", reply_markup=markup)

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Бот запущено. Очікуємо /start...")
    app.run_polling()
