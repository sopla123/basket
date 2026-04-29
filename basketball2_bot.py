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
        [InlineKeyboardButton("📚 История", callback_data="history")],
        [InlineKeyboardButton("🎥 Видеоуроки", callback_data="video")],
        [InlineKeyboardButton("📖 Термины", callback_data="terms")],
        [InlineKeyboardButton("📝 Оценить бота", callback_data="feedback")],
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
    elif data == "history":
        await query.edit_message_text(
            "📚 *ИСТОРИЯ БАСКЕТБОЛА*\n\n"
            "• Зимой 1891 года перед Нейсмитом встала задача: придумать подвижную игру для студентов, которую можно было бы проводить в закрытом помещении. Он вспомнил детскую игру «утка на скале», суть которой заключалась в попадании мячом в камень. Нейсмит прикрепил две корзины из-под персиков к перилам балкона на высоте 3 метров 5 сантиметров (эта высота сохранилась до сих пор) и разделил группу из 18 студентов на две команды. Целью игры было забросить мяч в корзину соперника.\n",
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
            "https://yandex.ru/video/preview/3754385915304373025\n\n"
            "*Жесты*\n"
            "https://www.sports.ru/basketball/blogs/3229565.html\n"
            "📹 *Передача мяча (пас)*\n"
            "https://rutube.ru/video/76d242c180e3d4c430c78da74bf14cdf\n\n"
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
            "• *Трёхсекундная зона (краска)* — область под кольцом\n"
            "• *Лэй-ап* — бросок после прохода из-под кольца\n"
            "• *Перехват* — отбор мяча в защите\n"
            "• *Блок-шот* — накрытие броска соперника"
            "• *Быстрый прорыв* - Метод нападения, заключающийся в попытке быстрой атаки, когда защита ещё не успела занять эффективные позиции. Обычно случается после перехвата или блок-шота.\n"
            "• *Защитник* - Игрок обороняющейся команды. / Игрок задней линии нападения.\n"
            "• *Зонная защита* - Каждый защитник отвечает за конкретную зону площадки.\n"
            "• *Изоляция / Айзо* - Тактика в нападении, когда игрок с мячом занимает одну сторону площадки, остальные нападающие занимают слабую сторону, оставляя нападающего с мячом играть 1 на 1 с защитником, либо вынуждать защиту сдваиваться, чтобы создать бросок для свободного нападающего. Также можно использовать, если защитник заведомо проигрывает нападающему.\n"
            "*Двойное ведение* - нарушение правил в баскетбольном матче, которое происходит, когда игрок, уже ведущий мяч, снова его берет в руки после того, как мяч уже полностью остановился.\n",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
    
    # О проекте
    elif data == "about":
        await query.edit_message_text(
            "ℹ️ *О ПРОЕКТЕ*\n\n"
            "Этот чат-бот создан в рамках индивидуального проекта\n"
            ""
            "🏀 *Занимайся спортом и развивайся!*",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
    elif data == "feedback":
        await query.edit_message_text(
        "📝 *Помоги улучшить бота!*\n\n"
        "Пожалуйста, пройди короткий опрос — это займёт 1 минуту.\n\n"
        "🔗 *Ссылка на форму:*\n"
        "https://forms.gle/bfREMHETTa1EjuGX7\n\n"
        "После заполнения просто закрой форму и продолжай пользоваться ботом.\n\n"
        "Спасибо за обратную связь! 🙌",
        parse_mode="Markdown",
        reply_markup=back_to_main()
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
