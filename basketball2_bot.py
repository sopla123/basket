import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8671809989:AAEr61_whZVQNb4jOqMzlwSyeLUCDyJXt3Y"

# --- Чтение прокси из файла (опционально) ---
def load_proxy():
    proxy_file = "proxy.txt"
    if os.path.exists(proxy_file):
        with open(proxy_file, "r", encoding="utf-8") as f:
            proxy_url = f.read().strip()
            if proxy_url:
                print(f"✓ Используется прокси")
                return proxy_url
    print("✓ Прокси не используется")
    return None

PROXY_URL = load_proxy()

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Клавиатуры ---
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📚 Теория", callback_data="theory")],
        [InlineKeyboardButton("🎥 Видеоуроки", callback_data="video")],
        [InlineKeyboardButton("📖 Термины", callback_data="terms")],
        [InlineKeyboardButton("ℹ️ О проекте", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="menu")]
    ])

# --- Обработчик команды /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏀 Привет! Я бот для обучения баскетболу.\n\n"
        "Я помогу тебе освоить основы:\n"
        "• Правила игры\n"
        "• Технику бросков и ведения\n"
        "• Баскетбольные термины\n\n"
        "Выбери раздел в меню ниже 👇",
        reply_markup=main_menu()
    )

# --- Обработчик всех кнопок ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    # Возврат в главное меню
    if data == "menu":
        await query.edit_message_text(
            "🏀 Главное меню. Выбери раздел:",
            reply_markup=main_menu()
        )
    
    # Теория (правила и история)
    elif data == "theory":
        await query.edit_message_text(
            "📚 *ОСНОВНЫЕ ПРАВИЛА БАСКЕТБОЛА*\n\n"
            "• *24 секунды* — лимит времени на атаку\n"
            "• *8 секунд* — нужно вывести мяч из тыловой зоны\n"
            "• *3 секунды* — нельзя находиться в краске соперника дольше 3 секунд\n"
            "• *5 фолов* — игрок покидает площадку\n"
            "• *Пробежка* — более 2 шагов с мячом без ведения\n\n"
            "🏆 *ИСТОРИЯ*\n"
            "Игру придумал Джеймс Нейсмит в 1891 году в США.\n"
            "В Россию баскетбол пришёл в 1901 году.\n"
            "С 1936 года — олимпийский вид спорта.\n\n"
            "⭐ *ЗОЛОТОЕ ПРАВИЛО:*\n"
            "Тренируй дриблинг и бросок каждый день!",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
    
    # Видеоуроки
    elif data == "video":
        await query.edit_message_text(
            "🎥 *ВИДЕОУРОКИ ДЛЯ НАЧИНАЮЩИХ*\n\n"
            "📹 *Дриблинг (ведение мяча)*\n"
            "https://rutube.ru/video/16a3be567b8869929e4a70a3280b3db9\n\n"
            "📹 *Бросок в прыжке*\n"
            "https://rutube.ru/video/cf61d0ce4188f61c36bc6f1368311518\n\n"
            "📹 *Правила игры для новичков*\n"
            "https://www.youtube.com/watch?v=NeL7G0bXx3M\n\n"
            "💡 *Совет:* смотри видео и сразу пробуй на площадке!",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
    
    # Словарь терминов
    elif data == "terms":
        await query.edit_message_text(
            "📖 *БАСКЕТБОЛЬНЫЙ СЛОВАРЬ*\n\n"
            "• *Данк* — бросок сверху прямо в кольцо\n"
            "• *Дриблинг* — ведение мяча одной рукой\n"
            "• *Аут* — мяч вышел за пределы площадки\n"
            "• *Фол* — нарушение правил (толчок, задержка, удар по рукам)\n"
            "• *Штрафной бросок* — бросок с линии за фол\n"
            "• *Трёхсекундная зона* — область под кольцом\n"
            "• *Лэй-ап* — бросок после прохода из-под кольца\n"
            "• *Перехват* — отбор мяча в защите\n"
            "• *Блок-шот* — накрытие броска соперника",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
    
    # О проекте
    elif data == "about":
        await query.edit_message_text(
            "ℹ️ *О ПРОЕКТЕ*\n\n"
            "Этот чат-бот создан в рамках индивидуального проекта\n"
            "учеником 10 класса Билык Павлом.\n\n"
            "📌 *Цель:* помощь начинающим спортсменам в изучении баскетбола.\n\n"
            "📅 Серпухов, 2025\n\n"
            "🏀 *Занимайся спортом и развивайся!*",
            parse_mode="Markdown",
            reply_markup=back_button()
        )

# --- Запуск бота ---
def main():
    if PROXY_URL:
        from telegram.request import HTTPXRequest
        request = HTTPXRequest(proxy=PROXY_URL)
        app = Application.builder().token(TOKEN).request(request).build()
    else:
        app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()
