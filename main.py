import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from uuid import uuid4
from html import escape
from telegram.constants import ParseMode

# Initialize a list to store messages
user_messages = []

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the user's message to the list
    user_messages.append(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def show_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_messages:
        messages_text = "\n".join(user_messages)
    else:
        messages_text = "Нет сохраненных сообщений."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages_text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Помощь")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # empty query should not be handled
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
            ),
        ),
    ]

    await update.inline_query.answer(results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понял команду.")

if __name__ == '__main__':
    application = ApplicationBuilder().token("INSERT YOUR TOKEN").build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    show_messages_handler = CommandHandler('show_messages', show_messages)

    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    inline_query_handler = InlineQueryHandler(inline_query)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(help_handler)
    application.add_handler(show_messages_handler)
    application.add_handler(inline_query_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
    
