import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 BotFather'dan aldığın token buraya
BOT_TOKEN = "7917840005:AAEMRVKSKFeiSX0C5Rxi9wEP3WKBkSbzx08"

# 💱 Döviz çeviri fonksiyonu
def get_exchange(amount, base_currency):
    try:
        base_currency = base_currency.upper()
        target_currencies = ["TRY", "EUR", "PLN"]
        target_currencies.remove(base_currency)

        url = f"https://open.er-api.com/v6/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()

        amount = float(amount)
        results = []

        for target in target_currencies:
            rate = data["rates"][target]
            converted = amount * rate
            results.append(f"{amount} {base_currency} ≈ {converted:.2f} {target}")

        return "\n".join(results)
    except Exception as e:
        return f"Hata oluştu: {e}"

# 🚀 /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! 💱\nLütfen miktarı ve para birimini yaz:\n"
        "Örnekler:\n`100 pln`\n`250 tl`\n`50 eur`"
    )

# 🧠 Mesajları yorumlayan fonksiyon
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().replace(",", ".").strip()

    try:
        if any(c in text for c in ["pln", "try", "tl", "eur"]):
            if "tl" in text and not "try" in text:
                base = "TRY"
                amount = text.split("tl")[0].strip()
            elif "try" in text:
                base = "TRY"
                amount = text.split("try")[0].strip()
            elif "pln" in text:
                base = "PLN"
                amount = text.split("pln")[0].strip()
            elif "eur" in text:
                base = "EUR"
                amount = text.split("eur")[0].strip()
            else:
                await update.message.reply_text("Tanımsız para birimi.")
                return

            cevap = get_exchange(amount, base)
            await update.message.reply_text(cevap)
        else:
            await update.message.reply_text("Lütfen bir miktar ve para birimi yaz. Örnek: 250 pln, 100 eur, 50 tl")
    except Exception as e:
        await update.message.reply_text(f"Mesaj işlenemedi: {e}")

# 🛠 Ana bot fonksiyonu
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("💬 Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
