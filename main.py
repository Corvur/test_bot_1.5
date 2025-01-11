# Бот возвращает выводит на экран текст который набрал пользователь (эхо), команда: /caps возвращает текст КАПСОМ. 
# inline-функция форматирования введенного текста(жирный, курсив, капс) чтобы ее вызвать зайдите в любой другой чат (не в нашего бота) введите: "@ИМЯБОТА ВАШ ТЕКСТ" 
#после этого появляются три кнопки фотрматирования текста
# функция show_messages отображает все введенные пользователем сообщения
#функция help выводит справочное сообщение
#функция unknown отправляет сообщение о том, что команда не распознана


import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from uuid import uuid4
from html import escape
from telegram.constants import ParseMode

# Инициализация списка для хранения сообщений пользователя
user_messages = []

# Настройка логирования
'''
подробно про логинг: В данном коде используется стандартный модуль Python для логирования — logging. Давайте разберем настройки логирования в вашем примере более подробно.

1. logging.basicConfig():
Этот метод используется для конфигурации базовых настроек логирования в приложении. 
В вашем случае, он настраивает формат сообщений логирования и минимальный уровень логов, которые будут записываться.
Давайте рассмотрим параметры, которые были указаны:

Параметры:
format: Этот параметр задает формат, в котором будут выводиться сообщения лога.
level: Этот параметр задает минимальный уровень логирования. Сообщения с уровнем ниже этого значения не будут записываться в лог.
2. format='%(asctime)s - %(name)s - %(levelname)s - %(message)s':
Этот параметр задает шаблон для вывода сообщений в лог.

В данном случае строка формата следующая:
%(asctime)s: Время, когда сообщение было записано в лог. Время будет автоматически добавляться в форматируемое сообщение.
%(name)s: Имя логгера, который записывает сообщение. Это значение может быть полезным, если у вас несколько логгеров в приложении (например, для разных модулей).
%(levelname)s: Уровень важности сообщения (например, INFO, DEBUG, WARNING, ERROR, CRITICAL). Это помогает понять, насколько важна информация в сообщении.
%(message)s: Текст самого сообщения, который передается в логгер.
Пример строки лога, которая будет сгенерирована с данным форматом:

yaml
Copy code
2025-01-11 14:33:15,123 - root - INFO - Привет, я бот
Время записи сообщения: 2025-01-11 14:33:15,123
Имя логгера (по умолчанию это root): root
Уровень сообщения: INFO
Сообщение: Привет, я бот 
'''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для обработки команды '/start'
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем приветственное сообщение пользователю
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот")

# Функция для эхо-сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем текст сообщения пользователя в список
    user_messages.append(update.message.text)
    # Отправляем пользователю его же сообщение
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Функция для отображения всех сохраненных сообщений
async def show_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_messages:
        # Если есть сохраненные сообщения, соединяем их в одну строку
        messages_text = "\n".join(user_messages)
    else:
        # Если сообщений нет, выводим соответствующее сообщение
        messages_text = "Нет сохраненных сообщений."
    # Отправляем пользователю список сообщений
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages_text)

# Функция для обработки команды '/caps', которая преобразует текст в верхний регистр
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Преобразуем все аргументы команды в верхний регистр
    text_caps = ' '.join(context.args).upper()
    # Отправляем результат пользователю
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# Функция для обработки команды '/help', которая отправляет текст помощи
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправляем текст с помощью
    await update.message.reply_text("Помощь")

# Функция для обработки inline-запросов
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка inline-запроса. Запускается, когда вы вводите: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # Пустой запрос не обрабатываем
        return

    # Формируем список результатов для inline-запроса
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),  # Генерация уникального ID
            title="Caps",  # Заголовок статьи
            input_message_content=InputTextMessageContent(query.upper()),  # Контент сообщения с текстом в верхнем регистре
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),  # Генерация уникального ID
            title="Bold",  # Заголовок статьи
            input_message_content=InputTextMessageContent(
                f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML  # Контент с жирным текстом в HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),  # Генерация уникального ID
            title="Italic",  # Заголовок статьи
            input_message_content=InputTextMessageContent(
                f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML  # Контент с курсивом в HTML
            ),
        ),
    ]

    # Отправляем результаты inline-запроса
    await update.inline_query.answer(results)

# Функция для обработки неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем сообщение о том, что команда не распознана
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понял команду.")

# Основная часть программы, запуск бота
if __name__ == '__main__':
    # Создаем объект приложения с токеном бота
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Обработчики команд и сообщений
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)  # Обработчик для всех текстовых сообщений, кроме команд
    show_messages_handler = CommandHandler('show_messages', show_messages)  # Обработчик для команды '/show_messages'

    caps_handler = CommandHandler('caps', caps)  # Обработчик для команды '/caps'
    start_handler = CommandHandler('start', start)  # Обработчик для команды '/start'
    help_handler = CommandHandler('help', help_command)  # Обработчик для команды '/help'
    unknown_handler = MessageHandler(filters.COMMAND, unknown)  # Обработчик для неизвестных команд
    inline_query_handler = InlineQueryHandler(inline_query)  # Обработчик для inline-запросов

    # Добавляем обработчики в приложение
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(help_handler)
    application.add_handler(show_messages_handler)
    application.add_handler(inline_query_handler)
    application.add_handler(unknown_handler)

    # Запуск бота с опросом новых сообщений
    application.run_polling()
    
