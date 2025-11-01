import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")

def get_main_leagues():
    headers = {"x-apisports-key": FOOTBALL_API_KEY}
    url = "https://v3.football.api-sports.io/leagues"
    response = requests.get(url, headers=headers)
    data = response.json()
    leagues = []
    for item in data.get("response", []):
        league = item.get("league", {})
        if league.get("type") == "League":
            leagues.append(league.get("name"))
    return leagues[:10]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔄 Atualizar Ligas", callback_data="update_leagues")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Olá, {update.effective_user.first_name}! Eu sou o *EscanteioBrBot*, criado por Leonardo Lopes de Souza.\n\n"
        "Envio as principais ligas do mundo a cada 5 minutos ⚽️",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def update_leagues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leagues = get_main_leagues()
    message = "🌍 *Principais Ligas do Mundo:*\n\n" + "\n".join([f"- {l}" for l in leagues])
    await update.callback_query.message.reply_text(message, parse_mode="Markdown")

async def auto_send(context: ContextTypes.DEFAULT_TYPE):
    chat_ids = context.job.data
    leagues = get_main_leagues()
    message = "🌍 *Principais Ligas do Mundo:*\n\n" + "\n".join([f"- {l}" for l in leagues])
    for chat_id in chat_ids:
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

async def register_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if "chat_ids" not in context.bot_data:
        context.bot_data["chat_ids"] = []
    if chat_id not in context.bot_data["chat_ids"]:
        context.bot_data["chat_ids"].append(chat_id)
        await update.message.reply_text("✅ Você foi registrado para receber atualizações automáticas a cada 5 minutos!")
        context.job_queue.run_repeating(auto_send, interval=300, first=5, data=context.bot_data["chat_ids"])

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", register_chat))
    app.add_handler(CallbackQueryHandler(update_leagues))
    app.run_polling()

if __name__ == "__main__":
    main()
