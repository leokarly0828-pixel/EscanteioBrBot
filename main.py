import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ver Ligas Principais 🌍", callback_data="ligas")],
        [InlineKeyboardButton("Ajuda ℹ️", callback_data="ajuda")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Olá Leonardo! Eu sou o EscanteioBrBot.\nEscolha uma opção abaixo:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ligas":
        ligas = [
            "🇧🇷 Brasileirão Série A",
            "🏴 Premier League",
            "🇪🇸 La Liga",
            "🇮🇹 Serie A",
            "🇩🇪 Bundesliga",
            "🇫🇷 Ligue 1",
            "🇵🇹 Liga Portugal",
            "🇳🇱 Eredivisie"
        ]
        ligas_text = "\n".join(ligas)
        await query.edit_message_text(f"⚽ Principais Ligas do Mundo (atualizadas a cada 5min):\n\n{ligas_text}")
    elif query.data == "ajuda":
        await query.edit_message_text("ℹ️ Enviarei atualizações automáticas sobre escanteios e ligas populares.\nUse /start para ver o menu novamente.")

async def enviar_ligas_periodicamente(app):
    chat_id = os.getenv("CHAT_ID")  # Opcional: pode configurar depois
    if not chat_id:
        return
    while True:
        ligas = [
            "🇧🇷 Brasileirão Série A",
            "🏴 Premier League",
            "🇪🇸 La Liga",
            "🇮🇹 Serie A",
            "🇩🇪 Bundesliga",
            "🇫🇷 Ligue 1",
            "🇵🇹 Liga Portugal",
            "🇳🇱 Eredivisie"
        ]
        msg = "⚽ Atualização automática das ligas principais:\n\n" + "\n".join(ligas)
        await app.bot.send_message(chat_id=chat_id, text=msg)
        await asyncio.sleep(300)  # 5 minutos

    async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # Inicia envio automático em background
    asyncio.create_task(enviar_ligas_periodicamente(app))

    print("🤖 Bot EscanteioBrBot iniciado com sucesso!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
