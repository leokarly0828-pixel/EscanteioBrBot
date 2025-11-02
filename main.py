import asyncio
import os
import aiohttp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# 🔑 Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Lista de ligas
LIGAS = [
    ("🇧🇷 Brasileirão Série A", 71),
    ("🏴 Premier League", 39),
    ("🇪🇸 La Liga", 140),
    ("🇮🇹 Serie A", 135),
    ("🇩🇪 Bundesliga", 78),
    ("🇫🇷 Ligue 1", 61),
    ("🇵🇹 Liga Portugal", 94),
    ("🇳🇱 Eredivisie", 88)
]

# 🏁 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(nome, callback_data=str(id_liga))] for nome, id_liga in LIGAS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma liga para ver estatísticas de escanteios:", reply_markup=reply_markup)

# 📊 Responde quando o usuário escolhe uma liga
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    liga_id = query.data

    url = f"https://v3.football.api-sports.io/fixtures?league={liga_id}&season=2025"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()

    if "response" not in data or not data["response"]:
        await query.edit_message_text("❌ Nenhum jogo encontrado no momento.")
        return

    mensagem = f"⚽ Estatísticas de Escanteios - Liga {liga_id}\n\n"
    for jogo in data["response"][:5]:
        home = jogo["teams"]["home"]["name"]
        away = jogo["teams"]["away"]["name"]
        date = jogo["fixture"]["date"][:10]
        mensagem += f"📅 {date}\n🏟️ {home} vs {away}\n\n"

    await query.edit_message_text(mensagem)

# 🔄 Atualizações automáticas (a cada 5 minutos)
async def atualizar_periodicamente(app):
    while True:
        print("🔁 Atualizando informações...")
        await asyncio.sleep(300)

# 🚀 Inicializa o bot
async def main():
    print("🤖 Iniciando EscanteioBrBot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    asyncio.create_task(atualizar_periodicamente(app))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
