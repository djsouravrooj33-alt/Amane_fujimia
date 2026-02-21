import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# ========= ENV =========
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 8145485145
ALLOWED_GROUP = -1003296016362

# ========= FLASK (Render Port Bind) =========
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram Bot Running"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run).start()

# ========= GROUP CHECK =========
def group_only(update: Update):
    return update.effective_chat.id == ALLOWED_GROUP

# ========= COMMANDS =========
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    await update.message.reply_text(
        "📌 **Available Commands**\n\n"
        "/num 9998887779 → মোবাইল তথ্য\n"
        "/adh 123412341234 → আধার তথ্য\n"
        "/vec DL9C0001 → গাড়ির তথ্য\n"
        "/upi upi@bank → UPI → Bank Details\n"
        "/ifsc SBIN0000001 → IFSC তথ্য"
    )

async def num_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    if not context.args:
        await update.message.reply_text("❌ নাম্বার দিন")
        return
    num = context.args[0]
    url = f"https://num.proportalxc.workers.dev/?mobile={num}"
    r = requests.get(url).json()
    await update.message.reply_text(f"📱 Number Info:\n{r}")

async def adh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    if not context.args:
        await update.message.reply_text("❌ আধার নম্বর দিন")
        return
    adh = context.args[0]
    url = f"https://api.paanel.shop/numapi.php?action=api&key=SALAAR&aadhar={adh}"
    r = requests.get(url).text
    await update.message.reply_text(f"🆔 Aadhaar Info:\n{r}")

async def vec_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    if not context.args:
        await update.message.reply_text("❌ গাড়ির নম্বর দিন")
        return
    rc = context.args[0]
    url = f"https://org.proportalxc.workers.dev/?rc={rc}"
    r = requests.get(url).json()
    await update.message.reply_text(f"🚗 Vehicle Info:\n{r}")

# ========= 🔗 UPI → IFSC → BANK CHAIN =========
async def upi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    if not context.args:
        await update.message.reply_text("❌ UPI ID দিন")
        return

    upi = context.args[0]

    # Step 1: UPI Check
    upi_url = f"https://upi-api.onrender.com/api/upi?upi={upi}"
    upi_res = requests.get(upi_url).json()

    if not upi_res.get("status") or upi_res.get("status") != "VALID":
        await update.message.reply_text("❌ Invalid UPI ID")
        return

    name = upi_res.get("name", "N/A")
    bank = upi_res.get("bank", "N/A")
    ifsc = upi_res.get("ifsc")

    if not ifsc:
        await update.message.reply_text("⚠️ IFSC পাওয়া যায়নি")
        return

    # Step 2: IFSC → Full Bank Details
    bank_url = f"https://ifsc.razorpay.com/{ifsc}"
    bank_res = requests.get(bank_url).json()

    msg = (
        "💳 **UPI → Bank Details**\n\n"
        f"✅ UPI Status: VALID\n"
        f"👤 Name: {name}\n\n"
        f"🏦 Bank: {bank_res.get('BANK')}\n"
        f"🔢 IFSC: {ifsc}\n"
        f"🏢 Branch: {bank_res.get('BRANCH')}\n"
        f"📍 Address: {bank_res.get('ADDRESS')}\n"
        f"🌆 City: {bank_res.get('CITY')}\n"
        f"🗺 State: {bank_res.get('STATE')}\n"
        f"🏧 MICR: {bank_res.get('MICR')}"
    )

    await update.message.reply_text(msg)

async def ifsc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not group_only(update):
        return
    if not context.args:
        await update.message.reply_text("❌ IFSC দিন")
        return
    ifsc = context.args[0]
    url = f"https://ifsc.razorpay.com/{ifsc}"
    r = requests.get(url).json()
    await update.message.reply_text(f"🏦 IFSC Info:\n{r}")

# ========= MAIN =========
def main():
    bot = Application.builder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("help", help_cmd))
    bot.add_handler(CommandHandler("num", num_cmd))
    bot.add_handler(CommandHandler("adh", adh_cmd))
    bot.add_handler(CommandHandler("vec", vec_cmd))
    bot.add_handler(CommandHandler("upi", upi_cmd))
    bot.add_handler(CommandHandler("ifsc", ifsc_cmd))

    print("🤖 Bot Started")
    bot.run_polling()

if __name__ == "__main__":
    main()
